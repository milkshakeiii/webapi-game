"""Synthesis engine with symbolic thread names and step-by-step trace output.

This module adapts the synthesis rules from simulator.py for use by the HTTP
API.  The simulator uses integer-indexed thread tuples for BFS deduplication;
this engine uses named threads (``dict[str, Thread]``) so clients can reference
threads with symbolic aliases like ``"a"``, ``"ab"``, or ``"core"``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from simulator import (
    ESSENCES,
    OPPOSED,
    Contract,
    Puzzle,
    Thread,
    add_essences,
    essence_dict,
    index_of,
    normalize_tags,
    used_cost,
    with_delta,
)

_NAME_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


class InvalidAction(Exception):
    """Raised when an action is illegal given the current bench state."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass
class BenchState:
    """Mutable state tracked during attempt evaluation."""

    step: int
    remaining: dict[str, int]
    live_threads: dict[str, Thread]
    retired: set[str]
    bench_capacity: int
    step_limit: int

    # Track cost for scoring.
    initial_total_cost: int = 0
    remaining_cost: int = 0


@dataclass
class AttemptResult:
    resolution: str  # "success" | "failure" | "invalid"
    trace: list[dict] = field(default_factory=list)
    summary: dict | None = None
    failed_step: int | None = None
    error: dict | None = None


# ---------------------------------------------------------------------------
# Snapshots for trace output
# ---------------------------------------------------------------------------

def _thread_snapshot(thread: Thread) -> dict:
    return {
        "essences": essence_dict(thread.essences),
        "tags": list(thread.tags),
        "fray": thread.fray,
    }


def _live_threads_snapshot(live: dict[str, Thread]) -> dict:
    return {name: _thread_snapshot(t) for name, t in live.items()}


def _remaining_snapshot(remaining: dict[str, int]) -> dict:
    return dict(remaining)


def _trace_step(step: int, action: dict, bench: BenchState) -> dict:
    return {
        "step": step,
        "action": action,
        "outcome": "ok",
        "live_threads": _live_threads_snapshot(bench.live_threads),
        "remaining_reagents": _remaining_snapshot(bench.remaining),
    }


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def _validate_name(name: str, bench: BenchState) -> None:
    """Ensure *name* is a valid new thread name."""
    if not name or not _NAME_RE.match(name):
        raise InvalidAction(
            "invalid_thread_name",
            f"Thread name '{name}' is not a valid identifier.",
        )
    if name in bench.live_threads:
        raise InvalidAction(
            "duplicate_thread_name",
            f"Thread name '{name}' is already live.",
        )
    if name in bench.retired:
        raise InvalidAction(
            "duplicate_thread_name",
            f"Thread name '{name}' was already used and retired.",
        )


def _require_live(name: str, bench: BenchState) -> Thread:
    """Return the live thread for *name* or raise."""
    if name in bench.retired:
        raise InvalidAction(
            "undefined_thread",
            f"Thread '{name}' was consumed by a prior bind and is no longer live.",
        )
    thread = bench.live_threads.get(name)
    if thread is None:
        raise InvalidAction(
            "undefined_thread",
            f"Thread '{name}' is not live.",
        )
    return thread


def _require_essence(value: str) -> None:
    if value not in ESSENCES:
        raise InvalidAction(
            "invalid_essence",
            f"'{value}' is not a valid essence. Must be one of {ESSENCES}.",
        )


# ---------------------------------------------------------------------------
# Per-action evaluators
# ---------------------------------------------------------------------------

def _evaluate_add(puzzle: Puzzle, bench: BenchState, action: dict) -> None:
    reagent_id = action.get("reagent_id")
    alias = action.get("as")

    if reagent_id is None:
        raise InvalidAction("missing_field", "add action requires 'reagent_id'.")
    if alias is None:
        raise InvalidAction("missing_field", "add action requires 'as'.")

    if reagent_id not in puzzle.reagents:
        raise InvalidAction(
            "unknown_reagent",
            f"Reagent '{reagent_id}' does not exist in this puzzle.",
        )
    if bench.remaining.get(reagent_id, 0) < 1:
        raise InvalidAction(
            "reagent_exhausted",
            f"Reagent '{reagent_id}' has no remaining uses.",
        )
    if len(bench.live_threads) >= bench.bench_capacity:
        raise InvalidAction("bench_full", "The bench is full.")

    _validate_name(alias, bench)

    reagent = puzzle.reagents[reagent_id]
    bench.remaining[reagent_id] -= 1
    bench.remaining_cost -= reagent.cost
    bench.live_threads[alias] = Thread(
        essences=reagent.essences,
        tags=reagent.tags,
        fray=0,
    )


def _evaluate_bind(puzzle: Puzzle, bench: BenchState, action: dict) -> None:
    left_name = action.get("left")
    right_name = action.get("right")
    into_name = action.get("into")
    bonus_essence = action.get("bonus_essence")

    if left_name is None:
        raise InvalidAction("missing_field", "bind action requires 'left'.")
    if right_name is None:
        raise InvalidAction("missing_field", "bind action requires 'right'.")
    if into_name is None:
        raise InvalidAction("missing_field", "bind action requires 'into'.")
    if left_name == right_name:
        raise InvalidAction("invalid_bind", "Cannot bind a thread with itself.")

    left = _require_live(left_name, bench)
    right = _require_live(right_name, bench)
    _validate_name(into_name, bench)

    shared_tags = set(left.tags).intersection(right.tags)
    essences = add_essences(left.essences, right.essences)
    fray = left.fray + right.fray

    if shared_tags:
        if bonus_essence is not None:
            _require_essence(bonus_essence)
            bonus_idx = index_of(bonus_essence)
            if left.essences[bonus_idx] <= 0 or right.essences[bonus_idx] <= 0:
                raise InvalidAction(
                    "invalid_bonus",
                    f"Bonus essence '{bonus_essence}' must be positive in both threads.",
                )
            essences = with_delta(essences, bonus_essence, 1)
    else:
        if bonus_essence is not None:
            raise InvalidAction(
                "invalid_bonus",
                "Bonus essence is not allowed on an unstable bind (no shared tags).",
            )
        fray += 2

    merged = Thread(
        essences=essences,
        tags=normalize_tags((*left.tags, *right.tags)),
        fray=fray,
    )

    del bench.live_threads[left_name]
    del bench.live_threads[right_name]
    bench.retired.add(left_name)
    bench.retired.add(right_name)
    bench.live_threads[into_name] = merged


def _evaluate_distill(puzzle: Puzzle, bench: BenchState, action: dict) -> None:
    thread_name = action.get("thread")
    essence = action.get("essence")

    if thread_name is None:
        raise InvalidAction("missing_field", "distill action requires 'thread'.")
    if essence is None:
        raise InvalidAction("missing_field", "distill action requires 'essence'.")

    _require_essence(essence)
    current = _require_live(thread_name, bench)

    values = list(current.essences)
    target_idx = index_of(essence)
    for idx, value in enumerate(values):
        if idx == target_idx:
            values[idx] += 2
        elif value > 0:
            values[idx] -= 1

    bench.live_threads[thread_name] = Thread(
        essences=tuple(values),
        tags=current.tags,
        fray=current.fray + 1,
    )


def _evaluate_reweave(puzzle: Puzzle, bench: BenchState, action: dict) -> None:
    thread_name = action.get("thread")
    from_essence = action.get("from_essence")
    to_essence = action.get("to_essence")
    amount = action.get("amount")

    if thread_name is None:
        raise InvalidAction("missing_field", "reweave action requires 'thread'.")
    if from_essence is None:
        raise InvalidAction("missing_field", "reweave action requires 'from_essence'.")
    if to_essence is None:
        raise InvalidAction("missing_field", "reweave action requires 'to_essence'.")
    if amount is None:
        raise InvalidAction("missing_field", "reweave action requires 'amount'.")

    amount = int(amount)
    if amount not in (1, 2):
        raise InvalidAction("invalid_amount", "Reweave amount must be 1 or 2.")
    if from_essence == to_essence:
        raise InvalidAction(
            "invalid_reweave",
            "from_essence and to_essence must be different.",
        )

    _require_essence(from_essence)
    _require_essence(to_essence)
    current = _require_live(thread_name, bench)

    values = list(current.essences)
    from_idx = index_of(from_essence)
    to_idx = index_of(to_essence)
    if values[from_idx] < amount:
        raise InvalidAction(
            "insufficient_essence",
            f"Source essence '{from_essence}' ({values[from_idx]}) is too small for reweave of {amount}.",
        )

    values[from_idx] -= amount
    values[to_idx] += amount
    fray_cost = 2 if (from_essence, to_essence) in OPPOSED else 1

    bench.live_threads[thread_name] = Thread(
        essences=tuple(values),
        tags=current.tags,
        fray=current.fray + fray_cost,
    )


def _evaluate_stabilize(puzzle: Puzzle, bench: BenchState, action: dict) -> None:
    thread_name = action.get("thread")
    reduce_essence = action.get("reduce_essence")

    if thread_name is None:
        raise InvalidAction("missing_field", "stabilize action requires 'thread'.")
    if reduce_essence is None:
        raise InvalidAction("missing_field", "stabilize action requires 'reduce_essence'.")

    _require_essence(reduce_essence)
    current = _require_live(thread_name, bench)

    if current.fray == 0:
        raise InvalidAction(
            "zero_fray",
            "Cannot stabilize a thread with zero fray.",
        )

    reduce_idx = index_of(reduce_essence)
    highest = max(current.essences)
    if current.essences[reduce_idx] != highest:
        raise InvalidAction(
            "not_highest_essence",
            f"reduce_essence '{reduce_essence}' is not one of the current highest essences.",
        )

    values = list(current.essences)
    values[reduce_idx] -= 1

    bench.live_threads[thread_name] = Thread(
        essences=tuple(values),
        tags=current.tags,
        fray=max(0, current.fray - 2),
    )


_EVALUATORS = {
    "add": _evaluate_add,
    "bind": _evaluate_bind,
    "distill": _evaluate_distill,
    "reweave": _evaluate_reweave,
    "stabilize": _evaluate_stabilize,
}


# ---------------------------------------------------------------------------
# Contract checking
# ---------------------------------------------------------------------------

def check_contract(thread: Thread, contract: Contract) -> list[dict]:
    """Return a list of violation dicts.  Empty list means success."""
    violations: list[dict] = []

    for idx, name in enumerate(ESSENCES):
        if thread.essences[idx] < contract.minimum_essences[idx]:
            violations.append({
                "code": "minimum_essence_not_met",
                "field": name,
                "expected": contract.minimum_essences[idx],
                "actual": thread.essences[idx],
            })
        if thread.essences[idx] > contract.maximum_essences[idx]:
            violations.append({
                "code": "maximum_essence_exceeded",
                "field": name,
                "expected": contract.maximum_essences[idx],
                "actual": thread.essences[idx],
            })

    thread_tags = set(thread.tags)
    for tag in contract.required_tags:
        if tag not in thread_tags:
            violations.append({
                "code": "required_tag_missing",
                "tag": tag,
            })
    for tag in contract.forbidden_tags:
        if tag in thread_tags:
            violations.append({
                "code": "forbidden_tag_present",
                "tag": tag,
            })

    if thread.fray > contract.max_fray:
        violations.append({
            "code": "fray_exceeded",
            "expected": contract.max_fray,
            "actual": thread.fray,
        })

    return violations


# ---------------------------------------------------------------------------
# Scoring (same formula as simulator.score_solution)
# ---------------------------------------------------------------------------

def _score(puzzle: Puzzle, bench: BenchState, thread: Thread) -> int:
    overproduction = 0
    for idx, minimum in enumerate(puzzle.contract.minimum_essences):
        overproduction += max(0, thread.essences[idx] - minimum)

    cost_used = bench.initial_total_cost - bench.remaining_cost
    score = 1000
    score -= 40 * bench.step
    score -= 12 * cost_used
    score -= 30 * thread.fray
    score -= 5 * overproduction
    return score


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def evaluate_attempt(puzzle: Puzzle, actions: list[dict]) -> AttemptResult:
    """Evaluate a full synthesis attempt and return the result with trace."""

    # Build initial bench state.
    remaining = dict(puzzle.initial_remaining)
    remaining_cost = sum(
        puzzle.reagents[rid].cost * count for rid, count in remaining.items()
    )

    bench = BenchState(
        step=0,
        remaining=remaining,
        live_threads={},
        retired=set(),
        bench_capacity=puzzle.bench_capacity,
        step_limit=puzzle.step_limit,
        initial_total_cost=puzzle.initial_total_cost,
        remaining_cost=remaining_cost,
    )

    trace: list[dict] = []

    for action_index, action in enumerate(actions):
        op = action.get("op")
        if op is None:
            return AttemptResult(
                resolution="invalid",
                trace=trace,
                failed_step=action_index + 1,
                error={"code": "missing_field", "message": "Action is missing 'op'."},
            )

        evaluator = _EVALUATORS.get(op)
        if evaluator is None:
            return AttemptResult(
                resolution="invalid",
                trace=trace,
                failed_step=action_index + 1,
                error={
                    "code": "unknown_op",
                    "message": f"Unknown operation '{op}'.",
                },
            )

        if bench.step >= bench.step_limit:
            return AttemptResult(
                resolution="invalid",
                trace=trace,
                failed_step=action_index + 1,
                error={
                    "code": "step_limit_exceeded",
                    "message": f"Step limit of {bench.step_limit} has been reached.",
                },
            )

        try:
            evaluator(puzzle, bench, action)
        except InvalidAction as exc:
            return AttemptResult(
                resolution="invalid",
                trace=trace,
                failed_step=action_index + 1,
                error={"code": exc.code, "message": exc.message},
            )

        bench.step += 1
        trace.append(_trace_step(bench.step, action, bench))

    # --- Evaluate final state ---
    live_names = list(bench.live_threads.keys())

    if len(live_names) != 1:
        violations = [{"code": "wrong_thread_count", "expected": 1, "actual": len(live_names)}]
        final_thread_data = None
        score = 0
        if live_names:
            # Pick the first live thread for reporting.
            first = bench.live_threads[live_names[0]]
            final_thread_data = _thread_snapshot(first)
        return AttemptResult(
            resolution="failure",
            trace=trace,
            summary={
                "contract_satisfied": False,
                "steps_used": bench.step,
                "step_limit": bench.step_limit,
                "cost_used": bench.initial_total_cost - bench.remaining_cost,
                "score": score,
                "final_thread": final_thread_data,
                "violations": violations,
            },
        )

    final_name = live_names[0]
    final_thread = bench.live_threads[final_name]
    violations = check_contract(final_thread, puzzle.contract)

    cost_used = bench.initial_total_cost - bench.remaining_cost
    score = _score(puzzle, bench, final_thread) if not violations else 0

    return AttemptResult(
        resolution="success" if not violations else "failure",
        trace=trace,
        summary={
            "contract_satisfied": not violations,
            "steps_used": bench.step,
            "step_limit": bench.step_limit,
            "cost_used": cost_used,
            "score": score,
            "final_thread": _thread_snapshot(final_thread),
            "violations": violations,
        },
    )
