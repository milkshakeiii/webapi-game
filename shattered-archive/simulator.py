#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ESSENCES = ("lumen", "echo", "motive", "veil")
OPPOSED = {
    ("lumen", "veil"),
    ("veil", "lumen"),
    ("echo", "motive"),
    ("motive", "echo"),
}


@dataclass(frozen=True)
class Reagent:
    reagent_id: str
    name: str
    essences: tuple[int, int, int, int]
    tags: tuple[str, ...]
    cost: int
    count: int


@dataclass(frozen=True)
class Thread:
    essences: tuple[int, int, int, int]
    tags: tuple[str, ...]
    fray: int


@dataclass(frozen=True)
class Contract:
    contract_id: str
    name: str
    minimum_essences: tuple[int, int, int, int]
    maximum_essences: tuple[int, int, int, int]
    required_tags: tuple[str, ...]
    forbidden_tags: tuple[str, ...]
    max_fray: int


@dataclass(frozen=True)
class Puzzle:
    puzzle_id: str
    name: str
    bench_capacity: int
    step_limit: int
    contract: Contract
    reagents: dict[str, Reagent]
    initial_remaining: tuple[tuple[str, int], ...]
    initial_total_cost: int


@dataclass(frozen=True)
class State:
    step: int
    remaining: tuple[tuple[str, int], ...]
    threads: tuple[Thread, ...]

    def signature(self) -> tuple[tuple[tuple[str, int], ...], tuple[Thread, ...]]:
        return self.remaining, self.threads


def essence_tuple(data: dict[str, int]) -> tuple[int, int, int, int]:
    return tuple(int(data[name]) for name in ESSENCES)


def essence_dict(values: tuple[int, int, int, int]) -> dict[str, int]:
    return dict(zip(ESSENCES, values, strict=True))


def sort_thread(thread: Thread) -> tuple[tuple[int, int, int, int], tuple[str, ...], int]:
    return thread.essences, thread.tags, thread.fray


def normalize_tags(tags: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted(set(tags)))


def normalize_threads(threads: Iterable[Thread]) -> tuple[Thread, ...]:
    return tuple(sorted(threads, key=sort_thread))


def load_puzzle(path: Path) -> Puzzle:
    raw = json.loads(path.read_text())
    validate_puzzle(raw)

    reagents: dict[str, Reagent] = {}
    total_cost = 0
    remaining: list[tuple[str, int]] = []
    for item in raw["reagents"]:
        reagent = Reagent(
            reagent_id=item["id"],
            name=item["name"],
            essences=essence_tuple(item["essences"]),
            tags=normalize_tags(item["tags"]),
            cost=int(item["cost"]),
            count=int(item["count"]),
        )
        reagents[reagent.reagent_id] = reagent
        remaining.append((reagent.reagent_id, reagent.count))
        total_cost += reagent.cost * reagent.count

    contract_raw = raw["contract"]
    contract = Contract(
        contract_id=contract_raw["id"],
        name=contract_raw["name"],
        minimum_essences=essence_tuple(contract_raw["minimum_essences"]),
        maximum_essences=essence_tuple(contract_raw["maximum_essences"]),
        required_tags=normalize_tags(contract_raw.get("required_tags", [])),
        forbidden_tags=normalize_tags(contract_raw.get("forbidden_tags", [])),
        max_fray=int(contract_raw["max_fray"]),
    )

    return Puzzle(
        puzzle_id=raw["id"],
        name=raw["name"],
        bench_capacity=int(raw["bench_capacity"]),
        step_limit=int(raw["step_limit"]),
        contract=contract,
        reagents=reagents,
        initial_remaining=tuple(sorted(remaining)),
        initial_total_cost=total_cost,
    )


def validate_puzzle(raw: dict) -> None:
    required_top = {"id", "name", "bench_capacity", "step_limit", "contract", "reagents"}
    missing = required_top.difference(raw)
    if missing:
        raise ValueError(f"Puzzle is missing fields: {sorted(missing)}")
    if raw["bench_capacity"] < 2:
        raise ValueError("bench_capacity must be at least 2")
    if raw["step_limit"] < 1:
        raise ValueError("step_limit must be at least 1")

    seen_ids: set[str] = set()
    for item in raw["reagents"]:
        reagent_id = item["id"]
        if reagent_id in seen_ids:
            raise ValueError(f"Duplicate reagent id: {reagent_id}")
        seen_ids.add(reagent_id)
        ensure_essences(item["essences"], f"reagent {reagent_id}")
        if item["cost"] < 1:
            raise ValueError(f"Reagent {reagent_id} must have cost >= 1")
        if item["count"] < 1:
            raise ValueError(f"Reagent {reagent_id} must have count >= 1")

    contract = raw["contract"]
    ensure_essences(contract["minimum_essences"], "contract minimum_essences")
    ensure_essences(contract["maximum_essences"], "contract maximum_essences")
    if contract["max_fray"] < 0:
        raise ValueError("contract max_fray must be non-negative")


def ensure_essences(values: dict[str, int], label: str) -> None:
    missing = set(ESSENCES).difference(values)
    if missing:
        raise ValueError(f"{label} is missing essences: {sorted(missing)}")
    extra = set(values).difference(ESSENCES)
    if extra:
        raise ValueError(f"{label} has unexpected essences: {sorted(extra)}")
    for name in ESSENCES:
        if int(values[name]) < 0:
            raise ValueError(f"{label} has negative {name}")


def index_of(essence: str) -> int:
    return ESSENCES.index(essence)


def add_essences(
    left: tuple[int, int, int, int], right: tuple[int, int, int, int]
) -> tuple[int, int, int, int]:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def with_delta(
    values: tuple[int, int, int, int], essence: str, delta: int
) -> tuple[int, int, int, int]:
    mutable = list(values)
    mutable[index_of(essence)] += delta
    return tuple(mutable)


def render_thread(thread: Thread) -> str:
    parts = [f"{name[0].upper()}{value}" for name, value in essence_dict(thread.essences).items()]
    tags = ",".join(thread.tags)
    return f"{' '.join(parts)} fray={thread.fray} tags=[{tags}]"


def initial_state(puzzle: Puzzle) -> State:
    return State(step=0, remaining=puzzle.initial_remaining, threads=tuple())


def remaining_to_dict(remaining: tuple[tuple[str, int], ...]) -> dict[str, int]:
    return dict(remaining)


def remaining_cost(puzzle: Puzzle, remaining: tuple[tuple[str, int], ...]) -> int:
    cost = 0
    for reagent_id, count in remaining:
        cost += puzzle.reagents[reagent_id].cost * count
    return cost


def used_cost(puzzle: Puzzle, remaining: tuple[tuple[str, int], ...]) -> int:
    return puzzle.initial_total_cost - remaining_cost(puzzle, remaining)


def is_valid_solution(puzzle: Puzzle, state: State) -> bool:
    if len(state.threads) != 1:
        return False

    thread = state.threads[0]
    contract = puzzle.contract

    if thread.fray > contract.max_fray:
        return False

    thread_tags = set(thread.tags)
    if not set(contract.required_tags).issubset(thread_tags):
        return False
    if set(contract.forbidden_tags).intersection(thread_tags):
        return False

    for idx, value in enumerate(thread.essences):
        if value < contract.minimum_essences[idx]:
            return False
        if value > contract.maximum_essences[idx]:
            return False

    return True


def score_solution(puzzle: Puzzle, state: State) -> int:
    thread = state.threads[0]
    overproduction = 0
    for idx, minimum in enumerate(puzzle.contract.minimum_essences):
        overproduction += max(0, thread.essences[idx] - minimum)

    score = 1000
    score -= 40 * state.step
    score -= 12 * used_cost(puzzle, state.remaining)
    score -= 30 * thread.fray
    score -= 5 * overproduction
    return score


def apply_action(puzzle: Puzzle, state: State, action: dict) -> State:
    if state.step >= puzzle.step_limit:
        raise ValueError("step limit exceeded")

    op = action["op"]
    next_step = state.step + 1

    if op == "add":
        if len(state.threads) >= puzzle.bench_capacity:
            raise ValueError("bench is full")

        remaining = remaining_to_dict(state.remaining)
        reagent_id = action["reagent_id"]
        if remaining.get(reagent_id, 0) < 1:
            raise ValueError(f"reagent {reagent_id} is unavailable")

        remaining[reagent_id] -= 1
        thread = Thread(
            essences=puzzle.reagents[reagent_id].essences,
            tags=puzzle.reagents[reagent_id].tags,
            fray=0,
        )
        threads = normalize_threads((*state.threads, thread))
        return State(step=next_step, remaining=tuple(sorted(remaining.items())), threads=threads)

    if op == "bind":
        left_idx = int(action["left_thread"])
        right_idx = int(action["right_thread"])
        if left_idx == right_idx:
            raise ValueError("bind requires two distinct threads")
        if left_idx < 0 or right_idx < 0 or left_idx >= len(state.threads) or right_idx >= len(state.threads):
            raise ValueError("thread index out of range")

        left = state.threads[left_idx]
        right = state.threads[right_idx]
        shared_tags = set(left.tags).intersection(right.tags)
        essences = add_essences(left.essences, right.essences)
        fray = left.fray + right.fray

        bonus_essence = action.get("bonus_essence")
        if shared_tags:
            if bonus_essence is not None:
                bonus_idx = index_of(bonus_essence)
                if left.essences[bonus_idx] <= 0 or right.essences[bonus_idx] <= 0:
                    raise ValueError("bonus_essence must be positive in both threads")
                essences = with_delta(essences, bonus_essence, 1)
        else:
            if bonus_essence is not None:
                raise ValueError("bonus_essence is not allowed on an unstable bind")
            fray += 2

        merged = Thread(
            essences=essences,
            tags=normalize_tags((*left.tags, *right.tags)),
            fray=fray,
        )
        survivors = [
            thread
            for idx, thread in enumerate(state.threads)
            if idx not in (left_idx, right_idx)
        ]
        threads = normalize_threads((*survivors, merged))
        return State(step=next_step, remaining=state.remaining, threads=threads)

    if op == "distill":
        thread_idx = int(action["thread"])
        if thread_idx < 0 or thread_idx >= len(state.threads):
            raise ValueError("thread index out of range")
        essence = action["essence"]
        current = state.threads[thread_idx]
        values = list(current.essences)
        target_idx = index_of(essence)
        for idx, value in enumerate(values):
            if idx == target_idx:
                values[idx] += 2
            elif value > 0:
                values[idx] -= 1
        updated = Thread(essences=tuple(values), tags=current.tags, fray=current.fray + 1)
        threads = list(state.threads)
        threads[thread_idx] = updated
        return State(step=next_step, remaining=state.remaining, threads=normalize_threads(threads))

    if op == "reweave":
        thread_idx = int(action["thread"])
        if thread_idx < 0 or thread_idx >= len(state.threads):
            raise ValueError("thread index out of range")
        from_essence = action["from_essence"]
        to_essence = action["to_essence"]
        amount = int(action["amount"])
        if amount not in (1, 2):
            raise ValueError("amount must be 1 or 2")
        if from_essence == to_essence:
            raise ValueError("from_essence and to_essence must differ")

        current = state.threads[thread_idx]
        values = list(current.essences)
        from_idx = index_of(from_essence)
        to_idx = index_of(to_essence)
        if values[from_idx] < amount:
            raise ValueError("source essence is too small for reweave")

        values[from_idx] -= amount
        values[to_idx] += amount
        fray_cost = 2 if (from_essence, to_essence) in OPPOSED else 1
        updated = Thread(essences=tuple(values), tags=current.tags, fray=current.fray + fray_cost)
        threads = list(state.threads)
        threads[thread_idx] = updated
        return State(step=next_step, remaining=state.remaining, threads=normalize_threads(threads))

    if op == "stabilize":
        thread_idx = int(action["thread"])
        if thread_idx < 0 or thread_idx >= len(state.threads):
            raise ValueError("thread index out of range")

        current = state.threads[thread_idx]
        if current.fray == 0:
            raise ValueError("cannot stabilize a thread with zero fray")

        reduce_essence = action["reduce_essence"]
        reduce_idx = index_of(reduce_essence)
        highest = max(current.essences)
        if current.essences[reduce_idx] != highest:
            raise ValueError("reduce_essence must be one of the current highest essences")

        values = list(current.essences)
        values[reduce_idx] -= 1
        updated = Thread(
            essences=tuple(values),
            tags=current.tags,
            fray=max(0, current.fray - 2),
        )
        threads = list(state.threads)
        threads[thread_idx] = updated
        return State(step=next_step, remaining=state.remaining, threads=normalize_threads(threads))

    raise ValueError(f"unknown op: {op}")


def enumerate_actions(state: State, puzzle: Puzzle) -> list[dict]:
    if state.step >= puzzle.step_limit:
        return []

    actions: list[dict] = []

    if len(state.threads) < puzzle.bench_capacity:
        for reagent_id, count in state.remaining:
            if count > 0:
                actions.append({"op": "add", "reagent_id": reagent_id})

    for left_idx in range(len(state.threads)):
        for right_idx in range(left_idx + 1, len(state.threads)):
            left = state.threads[left_idx]
            right = state.threads[right_idx]
            shared_tags = set(left.tags).intersection(right.tags)
            shared_positive = [
                essence
                for essence in ESSENCES
                if left.essences[index_of(essence)] > 0 and right.essences[index_of(essence)] > 0
            ]
            if shared_tags and shared_positive:
                for essence in shared_positive:
                    actions.append(
                        {
                            "op": "bind",
                            "left_thread": left_idx,
                            "right_thread": right_idx,
                            "bonus_essence": essence,
                        }
                    )
            else:
                actions.append({"op": "bind", "left_thread": left_idx, "right_thread": right_idx})

    for thread_idx, thread in enumerate(state.threads):
        for essence in ESSENCES:
            actions.append({"op": "distill", "thread": thread_idx, "essence": essence})

        for from_essence in ESSENCES:
            source_value = thread.essences[index_of(from_essence)]
            if source_value == 0:
                continue
            for to_essence in ESSENCES:
                if to_essence == from_essence:
                    continue
                for amount in (1, 2):
                    if source_value >= amount:
                        actions.append(
                            {
                                "op": "reweave",
                                "thread": thread_idx,
                                "from_essence": from_essence,
                                "to_essence": to_essence,
                                "amount": amount,
                            }
                        )

        if thread.fray > 0:
            highest = max(thread.essences)
            for idx, value in enumerate(thread.essences):
                if value == highest:
                    actions.append(
                        {
                            "op": "stabilize",
                            "thread": thread_idx,
                            "reduce_essence": ESSENCES[idx],
                        }
                    )

    return sorted(actions, key=action_sort_key)


def action_sort_key(action: dict) -> tuple:
    if action["op"] == "add":
        return (0, action["reagent_id"])
    if action["op"] == "bind":
        return (1, action["left_thread"], action["right_thread"], action.get("bonus_essence", ""))
    if action["op"] == "distill":
        return (2, action["thread"], action["essence"])
    if action["op"] == "reweave":
        return (
            3,
            action["thread"],
            action["from_essence"],
            action["to_essence"],
            action["amount"],
        )
    if action["op"] == "stabilize":
        return (4, action["thread"], action["reduce_essence"])
    raise ValueError(f"unknown op: {action['op']}")


def action_to_text(action: dict) -> str:
    op = action["op"]
    if op == "add":
        return f"add {action['reagent_id']}"
    if op == "bind":
        bonus = f" bonus={action['bonus_essence']}" if "bonus_essence" in action else ""
        return f"bind {action['left_thread']} {action['right_thread']}{bonus}"
    if op == "distill":
        return f"distill {action['thread']} {action['essence']}"
    if op == "reweave":
        return (
            f"reweave {action['thread']} {action['from_essence']}->{action['to_essence']}"
            f" x{action['amount']}"
        )
    if op == "stabilize":
        return f"stabilize {action['thread']} reduce={action['reduce_essence']}"
    raise ValueError(f"unknown op: {op}")


def search(puzzle: Puzzle, top_n: int) -> dict:
    start = initial_state(puzzle)
    queue = deque([(start, [])])
    seen_best_step: dict[tuple, int] = {start.signature(): 0}
    states_by_depth: defaultdict[int, int] = defaultdict(int)
    states_by_depth[0] = 1
    valid_solutions: list[tuple[int, State, list[dict]]] = []

    while queue:
        state, history = queue.popleft()

        if is_valid_solution(puzzle, state):
            valid_solutions.append((score_solution(puzzle, state), state, history))

        if state.step >= puzzle.step_limit:
            continue

        for action in enumerate_actions(state, puzzle):
            try:
                next_state = apply_action(puzzle, state, action)
            except ValueError:
                continue

            signature = next_state.signature()
            best_step = seen_best_step.get(signature)
            if best_step is not None and best_step <= next_state.step:
                continue

            seen_best_step[signature] = next_state.step
            states_by_depth[next_state.step] += 1
            queue.append((next_state, [*history, action]))

    valid_solutions.sort(
        key=lambda item: (
            -item[0],
            item[1].step,
            [action_to_text(action) for action in item[2]],
        )
    )

    return {
        "states_by_depth": dict(sorted(states_by_depth.items())),
        "unique_states": sum(states_by_depth.values()),
        "valid_solutions": valid_solutions[:top_n],
        "valid_solution_count": len(valid_solutions),
    }


def print_report(puzzle: Puzzle, report: dict, top_n: int) -> None:
    print(f"Puzzle: {puzzle.name}")
    print(f"Bench capacity: {puzzle.bench_capacity} | Step limit: {puzzle.step_limit}")
    print(f"Contract: {puzzle.contract.name}")
    print()
    print("Unique states by depth:")
    for depth, count in report["states_by_depth"].items():
        print(f"  {depth}: {count}")

    print()
    print(f"Unique reachable states: {report['unique_states']}")
    print(f"Valid end states: {report['valid_solution_count']}")

    if report["valid_solution_count"] == 0:
        return

    print()
    print(f"Top {min(top_n, report['valid_solution_count'])} solutions:")
    for rank, (score, state, history) in enumerate(report["valid_solutions"], start=1):
        print()
        print(f"{rank}. score={score} steps={state.step} cost={used_cost(puzzle, state.remaining)}")
        for step_number, action in enumerate(history, start=1):
            print(f"   {step_number}. {action_to_text(action)}")
        print(f"   final: {render_thread(state.threads[0])}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Search the Shattered Archive synthesis space.")
    parser.add_argument("puzzle", type=Path, help="Path to a puzzle JSON file")
    parser.add_argument("--top", type=int, default=5, help="How many top solutions to print")
    args = parser.parse_args()

    puzzle = load_puzzle(args.puzzle)
    report = search(puzzle, top_n=args.top)
    print_report(puzzle, report, top_n=args.top)


if __name__ == "__main__":
    main()
