"""Decision-point substrate for the v2 DSL.

See ``dnd/DECISION_POINT_DSL.md`` for the full design. This module is
the Phase 1 deliverable: the ``Action`` hierarchy plus
``enumerate_legal_actions`` / ``apply_action``. The existing
``execute_turn`` path is untouched; we'll wire it onto this substrate
in Phase 2.

Phase 1 scope (this commit):

- Action subclasses: ``Move``, ``FiveFootStep``, ``Attack``,
  ``FullAttack``, ``Charge``, ``Withdraw``, ``TotalDefense``,
  ``EndTurn``.
- ``GameState`` wrapper carrying per-actor turn-slot accounting.
- ``enumerate_legal_actions`` and ``apply_action`` for the actions
  above. Implementation delegates to the existing ``_do_*`` helpers
  in ``turn_executor`` to avoid duplicating logic.

Out of scope (later in Phase 1 or in Phase 2+): Cast, combat
maneuvers, reactive interrupts, sub-action decision points, the
parity harness wiring into ``execute_turn``.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from .combatant import Combatant
from .dice import Roller
from .encounter import Encounter
from .grid import Grid


# ---------------------------------------------------------------------------
# Action hierarchy
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Action:
    """Base for all atomic actions surfaced at decision points.

    Each concrete subclass carries the parameters required to resolve
    it. Pickers receive a ``list[Action]`` from
    ``enumerate_legal_actions`` and select one; the engine never
    chooses for them.
    """

    actor_id: str


@dataclass(frozen=True)
class EndTurn(Action):
    """Voluntary end of turn. Always present in the legal list unless
    the actor is forced (e.g., confused-attacks-self has run its
    substituted action)."""


@dataclass(frozen=True)
class Move(Action):
    """Walk to ``destination`` along the engine's pathfinder, up to
    the actor's per-action movement allowance. Provokes AoOs from any
    threatener whose square is left along the way."""

    destination: tuple[int, int]


@dataclass(frozen=True)
class FiveFootStep(Action):
    """Take a 5-ft step to ``destination`` (must be exactly one square
    away from the actor's current position). Does not provoke. Mutually
    exclusive with movement on the same turn."""

    destination: tuple[int, int]


@dataclass(frozen=True)
class Attack(Action):
    """Single melee or ranged attack against ``target_id`` using
    ``weapon_index`` (into ``actor.attack_options``)."""

    target_id: str
    weapon_index: int = 0


@dataclass(frozen=True)
class FullAttack(Action):
    """Full-attack action: all iteratives against ``target_id``.
    Sub-action decision points between iteratives (retarget / stop)
    arrive in Phase 3; Phase 1 resolves the entire chain inline like
    the v1 executor does."""

    target_id: str


@dataclass(frozen=True)
class Charge(Action):
    """Full-round charge to ``target_id`` along a straight line,
    ending with a single melee attack at +2 / -2 AC."""

    target_id: str


@dataclass(frozen=True)
class Withdraw(Action):
    """Full-round retreat in the cardinal/intercardinal direction,
    up to 2x speed; first square of movement does not provoke."""

    direction: str  # "north" / "south" / "east" / "west" / etc.


@dataclass(frozen=True)
class TotalDefense(Action):
    """Standard action: +4 dodge AC for one round; cannot attack."""


# ---------------------------------------------------------------------------
# Per-turn slot accounting and game-state wrapper
# ---------------------------------------------------------------------------


@dataclass
class TurnSlots:
    """Per-turn action-economy tracker for one actor.

    Reset at the start of each actor's turn (the substrate's
    responsibility, not the picker's). Used by
    ``enumerate_legal_actions`` to filter out actions whose slot is
    already spent.
    """

    standard_used: bool = False
    move_used: bool = False
    swift_used: bool = False
    five_foot_step_used: bool = False
    full_round_used: bool = False
    movement_taken: bool = False  # any squares of movement consumed
    turn_ended: bool = False


@dataclass
class GameState:
    """Substrate wrapper over (encounter, grid) plus per-actor turn
    slots. The picker sees this read-only; the substrate mutates it
    inside ``apply_action``."""

    encounter: Encounter
    grid: Grid
    turn_slots: dict[str, TurnSlots] = field(default_factory=dict)

    def slots_for(self, actor: Combatant) -> TurnSlots:
        slots = self.turn_slots.get(actor.id)
        if slots is None:
            slots = TurnSlots()
            self.turn_slots[actor.id] = slots
        return slots

    def reset_turn(self, actor: Combatant) -> None:
        """Reset ``actor``'s slot tracker for a fresh turn."""
        self.turn_slots[actor.id] = TurnSlots()


@dataclass
class ApplyResult:
    """What ``apply_action`` returned: the events the action emitted.

    Phase 2 will add ``next_decision_owner`` and reactive-interrupt
    ordering. For Phase 1 the substrate produces only a flat event
    stream (matching the v1 executor's output)."""

    events: list  # list[TurnEvent], imported indirectly to avoid cycles


# ---------------------------------------------------------------------------
# enumerate_legal_actions
# ---------------------------------------------------------------------------


def enumerate_legal_actions(
    actor: Combatant,
    state: GameState,
) -> list[Action]:
    """Every action ``actor`` may take from ``state`` right now.

    ``EndTurn`` is always present (the actor can voluntarily end at
    any time). The other actions surface only when the actor's
    condition state, slot accounting, and grid permit them.

    Phase 1 covers movement / attack / full-attack / charge /
    withdraw / total-defense; later actions (Cast, maneuvers,
    reactive interrupts) will be added here as they're implemented.
    """
    actions: list[Action] = [EndTurn(actor_id=actor.id)]
    slots = state.slots_for(actor)

    if slots.turn_ended:
        return actions

    # Actor inability gates: dead / unconscious / dying / paralyzed /
    # petrified actors can't take actions. Stunned and dazed gate
    # too — see Combatant condition handling.
    if not _can_take_actions(actor):
        return actions

    grid = state.grid
    encounter = state.encounter

    # Movement options ─────────────────────────────────────────────────
    # 5-ft step: legal only when no movement has been taken yet, the
    # five_foot_step slot itself isn't spent, and the actor isn't
    # grappled / paralyzed / etc.
    if (
        not slots.movement_taken
        and not slots.five_foot_step_used
        and not slots.full_round_used
        and "grappled" not in actor.conditions
        and "pinned" not in actor.conditions
    ):
        for dest in _adjacent_legal_squares(actor, grid):
            actions.append(FiveFootStep(actor_id=actor.id, destination=dest))

    # Move: standard move action.
    if (
        not slots.move_used
        and not slots.movement_taken
        and not slots.full_round_used
        and "grappled" not in actor.conditions
    ):
        from .turn_executor import _movement_squares  # avoid cycle at import time
        budget = _movement_squares(actor, encounter)
        for dest in _reachable_squares(actor, grid, budget):
            actions.append(Move(actor_id=actor.id, destination=dest))

    # Attack options (melee + ranged) ─────────────────────────────────
    # An Attack consumes the standard slot. Surfaced for every visible
    # legal target.
    if not slots.standard_used and not slots.full_round_used:
        for target in _attackable_targets(actor, grid):
            actions.append(Attack(
                actor_id=actor.id, target_id=target.id, weapon_index=0,
            ))

    # Full-round options ──────────────────────────────────────────────
    # FullAttack / Charge / Withdraw all consume the full-round slot;
    # offered only if neither standard nor move has been used.
    if (
        not slots.standard_used
        and not slots.move_used
        and not slots.full_round_used
    ):
        for target in _attackable_targets(actor, grid):
            actions.append(FullAttack(actor_id=actor.id, target_id=target.id))
        for target in _chargeable_targets(actor, grid, encounter):
            actions.append(Charge(actor_id=actor.id, target_id=target.id))
        # Withdraw: list the cardinal/intercardinal directions where a
        # path of any length is possible; the apply step computes the
        # actual destination.
        for direction in _viable_withdraw_directions(actor, grid):
            actions.append(Withdraw(actor_id=actor.id, direction=direction))

    # Total Defense (standard action, no attack permitted) ────────────
    if not slots.standard_used and not slots.full_round_used:
        actions.append(TotalDefense(actor_id=actor.id))

    return actions


# ---------------------------------------------------------------------------
# apply_action
# ---------------------------------------------------------------------------


def apply_action(
    action: Action,
    state: GameState,
    roller: Roller,
) -> ApplyResult:
    """Resolve ``action`` against ``state``, mutating it in place.

    Delegates to the existing ``_do_*`` helpers in ``turn_executor``
    where possible to avoid duplicating logic. Returns the emitted
    event stream; Phase 2 will extend the result to carry the next
    decision-point's owner and any reactive-interrupt scheduling.
    """
    from .turn_executor import (  # local import to avoid cycle
        TurnEvent,
        _do_attack,
        _do_charge,
        _do_full_attack,
        _do_withdraw,
        _do_5ft_step,
        _move_along,
        _movement_squares,
    )
    from .modifiers import Modifier

    actor = state.grid.combatants.get(action.actor_id)
    if actor is None:
        # Defensive: the picker handed us an action whose actor isn't
        # on the grid. Treat as a no-op skip.
        evt = TurnEvent(action.actor_id, "skip", {
            "reason": "apply_action: actor not on grid",
        })
        return ApplyResult(events=[evt])

    events: list = []
    slots = state.slots_for(actor)
    grid = state.grid
    encounter = state.encounter

    if isinstance(action, EndTurn):
        slots.turn_ended = True
        return ApplyResult(events=events)

    if isinstance(action, Move):
        budget = _movement_squares(actor, encounter)
        _move_along(actor, action.destination, budget, grid, events,
                    encounter=encounter)
        slots.move_used = True
        slots.movement_taken = True
        return ApplyResult(events=events)

    if isinstance(action, FiveFootStep):
        _do_5ft_step(actor, action.destination, grid, {}, events)
        slots.five_foot_step_used = True
        slots.movement_taken = True
        return ApplyResult(events=events)

    if isinstance(action, Attack):
        target = grid.combatants.get(action.target_id)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "attack: target gone"}))
            return ApplyResult(events=events)
        _do_attack(actor, target, grid, roller, events,
                   encounter=encounter,
                   attack_index=action.weapon_index)
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, FullAttack):
        target = grid.combatants.get(action.target_id)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "full_attack: target gone"}))
            return ApplyResult(events=events)
        _do_full_attack(actor, target, {}, grid, roller, events,
                        encounter=encounter)
        slots.full_round_used = True
        return ApplyResult(events=events)

    if isinstance(action, Charge):
        target = grid.combatants.get(action.target_id)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "charge: target gone"}))
            return ApplyResult(events=events)
        _do_charge(actor, {"target": target}, encounter, grid, roller,
                   {}, events)
        slots.full_round_used = True
        return ApplyResult(events=events)

    if isinstance(action, Withdraw):
        _do_withdraw(actor, {"direction": action.direction}, encounter,
                     grid, events)
        slots.full_round_used = True
        return ApplyResult(events=events)

    if isinstance(action, TotalDefense):
        cur_round = encounter.round_number if encounter else 1
        src = "total_defense"
        actor.modifiers.remove_by_source(src)
        actor.modifiers.add(Modifier(
            value=4, type="dodge", target="ac",
            source=src, expires_round=cur_round + 1,
        ))
        events.append(TurnEvent(actor.id, "total_defense", {
            "ac_bonus": 4, "expires_round": cur_round + 1,
        }))
        slots.standard_used = True
        return ApplyResult(events=events)

    raise NotImplementedError(
        f"apply_action: action class {type(action).__name__} "
        f"not yet handled in Phase 1 substrate"
    )


# ---------------------------------------------------------------------------
# Enumeration helpers
# ---------------------------------------------------------------------------


def _can_take_actions(actor: Combatant) -> bool:
    """Conservative liveness check. Mirrors the gates that
    ``execute_turn`` applies via ``validate_turn``."""
    if not actor.is_alive():
        return False
    if "dead" in actor.conditions:
        return False
    if actor.is_unconscious():
        return False
    if "dying" in actor.conditions:
        return False
    if "paralyzed" in actor.conditions:
        return False
    if "petrified" in actor.conditions:
        return False
    if "dazed" in actor.conditions:
        return False
    if "cowering" in actor.conditions:
        return False
    if "fascinated" in actor.conditions:
        return False
    return True


def _adjacent_legal_squares(
    actor: Combatant, grid: Grid,
) -> list[tuple[int, int]]:
    """Squares one step from ``actor.position`` that are passable and
    not occupied. Used for FiveFootStep enumeration."""
    ax, ay = actor.position
    out: list[tuple[int, int]] = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            sq = (ax + dx, ay + dy)
            if not grid.in_bounds(*sq):
                continue
            f = grid.features.get(sq)
            if f is not None and f.blocks_movement:
                continue
            if grid._occupancy.get(sq) is not None:
                continue
            # Difficult terrain forbids 5-ft step (audit gap; tracked).
            # We still surface it here; apply_action delegates to
            # _do_5ft_step which will be tightened in Phase 1 cleanup.
            out.append(sq)
    return out


def _reachable_squares(
    actor: Combatant, grid: Grid, budget: int,
) -> list[tuple[int, int]]:
    """BFS from ``actor.position`` over passable, unoccupied cells,
    bounded by ``budget`` step count.

    Difficult terrain doubles the cost per cell entered. Uses the
    grid's feature map (``GridFeature.movement_cost_multiplier``)."""
    if budget <= 0:
        return []
    start = actor.position
    visited: dict[tuple[int, int], int] = {start: 0}
    queue: deque[tuple[tuple[int, int], int]] = deque([(start, 0)])
    while queue:
        cell, cost = queue.popleft()
        if cost >= budget:
            continue
        cx, cy = cell
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nxt = (cx + dx, cy + dy)
                if not grid.in_bounds(*nxt):
                    continue
                if nxt == start:
                    continue
                f = grid.features.get(nxt)
                if f is not None and f.blocks_movement:
                    continue
                if grid._occupancy.get(nxt) is not None:
                    continue
                step_cost = 1
                if f is not None and f.movement_cost_multiplier > 1:
                    step_cost = int(f.movement_cost_multiplier)
                ncost = cost + step_cost
                if ncost > budget:
                    continue
                if nxt in visited and visited[nxt] <= ncost:
                    continue
                visited[nxt] = ncost
                queue.append((nxt, ncost))
    visited.pop(start, None)
    return sorted(visited.keys())


def _attackable_targets(
    actor: Combatant, grid: Grid,
) -> list[Combatant]:
    """Hostile combatants the actor can plausibly attack right now.

    For melee weapons: any adjacent enemy. For ranged weapons: any
    enemy on the grid (range increments are penalty math, not legality
    gates — total cover is checked at apply time, where it can also
    skip with a clear reason)."""
    if not actor.attack_options:
        return []
    primary = actor.attack_options[0]
    is_ranged = primary.get("type") == "ranged"
    out: list[Combatant] = []
    for cid, other in grid.combatants.items():
        if other.id == actor.id:
            continue
        if other.team == actor.team:
            continue
        if not other.is_alive():
            continue
        if "dead" in other.conditions:
            continue
        if is_ranged:
            out.append(other)
        elif grid.is_adjacent(actor, other):
            out.append(other)
    return out


def _chargeable_targets(
    actor: Combatant, grid: Grid, encounter: Encounter,
) -> list[Combatant]:
    """Enemies the actor could feasibly charge to. Conservative — the
    apply step does the strict straight-line / lane-clear check, so
    here we only filter on distance and basic visibility."""
    if not actor.attack_options:
        return []
    if actor.attack_options[0].get("type") == "ranged":
        # Charge requires a melee attack at the end.
        return []
    from .turn_executor import _movement_squares
    speed = _movement_squares(actor, encounter)
    max_dist = speed * 2  # charge = up to 2x speed
    out: list[Combatant] = []
    for cid, other in grid.combatants.items():
        if other.id == actor.id:
            continue
        if other.team == actor.team:
            continue
        if not other.is_alive():
            continue
        d = grid.distance_squares(actor.position, other.position)
        # PF1 charge: minimum 2 squares (10 ft) from start.
        if d < 2 or d > max_dist:
            continue
        out.append(other)
    return out


def _viable_withdraw_directions(
    actor: Combatant, grid: Grid,
) -> list[str]:
    """Cardinal/intercardinal directions where the first step out of
    the actor's square is into a passable, unoccupied cell. Coarse —
    the apply step walks the full path."""
    deltas = {
        "north": (0, -1), "south": (0, 1),
        "east": (1, 0), "west": (-1, 0),
        "northeast": (1, -1), "northwest": (-1, -1),
        "southeast": (1, 1), "southwest": (-1, 1),
    }
    out: list[str] = []
    ax, ay = actor.position
    for name, (dx, dy) in deltas.items():
        sq = (ax + dx, ay + dy)
        if not grid.in_bounds(*sq):
            continue
        f = grid.features.get(sq)
        if f is not None and f.blocks_movement:
            continue
        if grid._occupancy.get(sq) is not None:
            continue
        out.append(name)
    return out
