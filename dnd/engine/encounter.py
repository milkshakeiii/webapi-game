"""Encounter scaffolding: turn objects, validation, initiative, AoO detection.

This module defines the data structures and helpers that orchestrate a
combat encounter, but stops short of executing turns. Turn execution
(walking each slot, calling combat math, applying results) lands when
the behavior DSL parser is in place — until then there's no way to
*produce* a Turn from a script.

What's here:

- ``Turn`` — a structured object with the 6 slots PF1's action economy
  defines (full_round, standard, move, swift, five_foot_step, free).
- ``validate_turn`` — parser-time rules that make invalid turns
  unrepresentable (action exclusivity, 5ft-step exclusivity, swift
  uniqueness, free-action legality, actor legality).
- ``roll_initiative`` — d20 + initiative modifier, ordered by descending
  total.
- ``Encounter`` — minimal state for a fight: combatants, initiative
  order, round counter, current-actor index.
- ``aoo_triggers_for_movement`` — given a movement step, returns the
  hostile combatants who threaten the origin square and would get an
  attack of opportunity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .combatant import Combatant
from .dice import Roller
from .grid import Grid


# ---------------------------------------------------------------------------
# Turn dataclass
# ---------------------------------------------------------------------------


# Free-action types the engine accepts; everything else must go in a
# real action slot.
LEGAL_FREE_ACTIONS = frozenset({
    "drop_item",
    "fall_prone",
    "speak",
    "signal",
    "end_concentration",
    "drop_held_charge",
    # PF1 also lists these as free per RAW:
    "cease_concentration",
    "drop_to_floor",
    "release_grapple",
    "press_attack",
    "speak_briefly",
    "use_extraordinary_ability",
})


# Actions whose `type` field implies they consume movement. If any of
# these appear in a `move` slot, no 5ft-step is allowed.
MOVEMENT_ACTIONS_IN_MOVE_SLOT = frozenset({
    "move_to", "move_toward", "move_away",
})

# Full-round actions that include movement.
MOVEMENT_FULL_ROUND_ACTIONS = frozenset({
    "charge", "withdraw", "run",
})


@dataclass(frozen=True)
class Turn:
    """One combatant's actions for a single round.

    All slots are optional. The validator enforces the legal
    combinations. Each slot's value (when not None) is a dict like
    ``{"type": "attack", "target": ..., "options": {...}}``.
    """

    full_round: dict | None = None
    standard: dict | None = None
    move: dict | None = None
    swift: dict | None = None
    five_foot_step: tuple[int, int] | None = None    # destination square
    free: tuple[dict, ...] = ()

    def to_dict(self) -> dict:
        return {
            "full_round": self.full_round,
            "standard": self.standard,
            "move": self.move,
            "swift": self.swift,
            "five_foot_step": self.five_foot_step,
            "free": list(self.free),
        }


class TurnValidationError(ValueError):
    """Raised when a Turn violates PF1's action-economy rules."""


def validate_turn(turn: Turn, combatant: Combatant, grid: Grid) -> None:
    """Validate a Turn against PF1's action economy + actor state.

    Raises ``TurnValidationError`` on the first violation. Pass-through
    means the turn is well-formed and legal for this actor right now.
    """
    # 1) Action exclusivity: full_round forbids standard and move.
    if turn.full_round is not None:
        if turn.standard is not None:
            raise TurnValidationError(
                "full_round action set; standard slot must be null"
            )
        if turn.move is not None:
            raise TurnValidationError(
                "full_round action set; move slot must be null"
            )

    # 2) Five-foot-step exclusivity.
    if turn.five_foot_step is not None:
        if turn.move is not None and _move_includes_movement(turn.move):
            raise TurnValidationError(
                "five_foot_step set; move slot also provides movement"
            )
        if turn.full_round is not None and _full_round_includes_movement(turn.full_round):
            raise TurnValidationError(
                "five_foot_step set; full_round action also provides movement"
            )
        # Validate destination is a single square's distance away.
        ax, ay = combatant.position
        tx, ty = turn.five_foot_step
        if max(abs(tx - ax), abs(ty - ay)) != 1:
            raise TurnValidationError(
                f"five_foot_step destination {turn.five_foot_step} is not "
                f"adjacent to current position {combatant.position}"
            )
        if not grid.in_bounds(tx, ty):
            raise TurnValidationError(
                f"five_foot_step destination {turn.five_foot_step} out of bounds"
            )

    # 3) Free-action legality.
    for fa in turn.free:
        ftype = fa.get("type") if isinstance(fa, dict) else None
        if ftype not in LEGAL_FREE_ACTIONS:
            raise TurnValidationError(
                f"free action {fa!r} not in legal-as-free list "
                f"({sorted(LEGAL_FREE_ACTIONS)})"
            )

    # 4) Actor legality — light checks.
    _check_actor_legality(turn, combatant)


def _move_includes_movement(move_action: dict) -> bool:
    return move_action.get("type") in MOVEMENT_ACTIONS_IN_MOVE_SLOT


def _full_round_includes_movement(fr_action: dict) -> bool:
    return fr_action.get("type") in MOVEMENT_FULL_ROUND_ACTIONS


def _check_actor_legality(turn: Turn, combatant: Combatant) -> None:
    """Light state-aware checks. Raises TurnValidationError if illegal."""
    conds = combatant.conditions

    if "dead" in conds or "unconscious" in conds:
        if any(s is not None for s in (
            turn.full_round, turn.standard, turn.move, turn.swift, turn.five_foot_step
        )) or turn.free:
            raise TurnValidationError(
                f"combatant {combatant.id} cannot act ({conds & {'dead', 'unconscious'}})"
            )

    if "paralyzed" in conds or "petrified" in conds:
        if any(s is not None for s in (
            turn.full_round, turn.standard, turn.move, turn.five_foot_step
        )):
            raise TurnValidationError(
                f"combatant {combatant.id} cannot take physical actions ({conds & {'paralyzed', 'petrified'}})"
            )

    if "staggered" in conds:
        # Staggered: only one move OR standard (no full-round actions).
        if turn.full_round is not None:
            raise TurnValidationError(
                "staggered combatant cannot take a full-round action"
            )
        if turn.standard is not None and turn.move is not None:
            raise TurnValidationError(
                "staggered combatant can take a single move OR standard action, not both"
            )

    if "disabled" in conds:
        # Disabled (HP exactly 0): same action restriction as staggered.
        # PF1 RAW: a standard action also deals 1 HP nonlethal damage
        # to self (often dropping the actor into dying); not modeled
        # here yet — handled at action resolution if at all.
        if turn.full_round is not None:
            raise TurnValidationError(
                "disabled combatant cannot take a full-round action"
            )
        if turn.standard is not None and turn.move is not None:
            raise TurnValidationError(
                "disabled combatant can take a single move OR standard action, not both"
            )

    if "grappled" in conds:
        # PF1: a grappled creature cannot move (no walk, run, charge,
        # withdraw); cannot make actions requiring two free hands;
        # cannot take attacks of opportunity (handled at AoO time).
        if turn.move is not None:
            mtype = turn.move.get("type")
            if mtype in ("move_to", "move_toward", "move_away"):
                raise TurnValidationError(
                    "grappled combatant cannot move (must escape grapple first)"
                )
        if turn.full_round is not None:
            full_kind = turn.full_round.get("composite") or turn.full_round.get("type")
            if full_kind in ("charge", "withdraw", "run"):
                raise TurnValidationError(
                    f"grappled combatant cannot take {full_kind!r} action"
                )
        if turn.five_foot_step is not None:
            raise TurnValidationError(
                "grappled combatant cannot take a 5-ft step"
            )
        if turn.standard is not None:
            stype = turn.standard.get("type")
            if stype == "drink":
                raise TurnValidationError(
                    "can't drink potion while grappled (needs free hand)"
                )

    if "prone" in conds:
        # Prone allows nothing except stand_up as your move action and
        # melee/ranged with penalties. Skip detailed enforcement for v1.
        pass

    if "dazed" in conds or "fascinated" in conds or "cowering" in conds:
        # PF1: dazed → no actions for 1 round (defenses normal).
        # Fascinated → no actions; standard action breaks free.
        # Cowering → no actions, denies Dex (handled separately).
        if any(s is not None for s in (
            turn.full_round, turn.standard, turn.move,
            turn.swift, turn.five_foot_step,
        )) or turn.free:
            blocking = conds & {"dazed", "fascinated", "cowering"}
            raise TurnValidationError(
                f"combatant {combatant.id} cannot act ({blocking})"
            )

    if "nauseated" in conds:
        # PF1: only a single move action — no standard, no full-round,
        # no swift, no free actions, no 5-ft step.
        if any(s is not None for s in (
            turn.full_round, turn.standard, turn.swift, turn.five_foot_step,
        )) or turn.free:
            raise TurnValidationError(
                "nauseated combatant can only take a single move action"
            )

    if "entangled" in conds:
        # PF1: entangled creature cannot run or charge. Other movement
        # is allowed (at half speed, enforced via the entangled
        # condition's speed mutation in combatant._on_condition_applied).
        if turn.full_round is not None:
            kind = turn.full_round.get("composite") or turn.full_round.get("type")
            if kind in ("charge", "run"):
                raise TurnValidationError(
                    f"entangled combatant cannot take {kind!r} action"
                )

    if "fatigued" in conds or "exhausted" in conds:
        # PF1: a fatigued creature cannot run or charge; exhausted
        # inherits this restriction.
        if turn.full_round is not None:
            kind = turn.full_round.get("composite") or turn.full_round.get("type")
            if kind in ("charge", "run"):
                state = "exhausted" if "exhausted" in conds else "fatigued"
                raise TurnValidationError(
                    f"{state} combatant cannot take {kind!r} action"
                )

    if "panicked" in conds:
        # PF1: panicked creature drops items, flees, and cannot attack
        # except in self-defense (effectively reduced to move + total
        # defense). The engine doesn't enforce flee direction; we just
        # ban offensive standard / full-round actions.
        for val in (turn.standard, turn.full_round):
            if val is None:
                continue
            kind = val.get("composite") or val.get("type")
            if kind in (
                "attack", "cast", "charge", "full_attack",
                "cleave", "stunning_fist", "smite_evil",
                "ready_brace", "rage_start", "trample",
                "grapple_start", "grapple_damage", "grapple_pin",
                "grapple_move", "grapple_reverse",
            ):
                raise TurnValidationError(
                    f"panicked combatant cannot take {kind!r} action"
                )


# ---------------------------------------------------------------------------
# Initiative
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class InitiativeRoll:
    combatant: Combatant
    roll: int
    modifier: int
    total: int

    def to_dict(self) -> dict:
        return {
            "combatant_id": self.combatant.id,
            "name": self.combatant.name,
            "roll": self.roll,
            "modifier": self.modifier,
            "total": self.total,
        }


def roll_initiative(
    combatants: Iterable[Combatant],
    roller: Roller,
) -> list[InitiativeRoll]:
    """Roll d20 + initiative_modifier for each combatant.

    Returns InitiativeRoll list sorted by ``total`` descending. Ties are
    broken by initiative modifier (higher first), then by roll order
    (stable). PF1's official tiebreaker is "everyone with the same total
    rolls a d20 again until ties are broken"; for determinism we use the
    simpler modifier-tiebreak.
    """
    results: list[InitiativeRoll] = []
    for c in combatants:
        mod = c.initiative_modifier()
        r = roller.roll("1d20")
        natural = r.terms[0].rolls[0]
        results.append(InitiativeRoll(
            combatant=c,
            roll=natural,
            modifier=mod,
            total=natural + mod,
        ))
    results.sort(key=lambda ir: (-ir.total, -ir.modifier))
    return results


# ---------------------------------------------------------------------------
# Encounter state
# ---------------------------------------------------------------------------


@dataclass
class Encounter:
    """Live state of an in-progress encounter."""

    grid: Grid
    initiative: list[InitiativeRoll] = field(default_factory=list)
    round_number: int = 0
    current_index: int = 0
    log: list[dict] = field(default_factory=list)
    # Optional roller carried between rounds. Used by tick_round's
    # stabilization check (and any other between-round dice rolls).
    roller: Roller | None = None

    @classmethod
    def begin(
        cls,
        grid: Grid,
        combatants: Iterable[Combatant],
        roller: Roller,
    ) -> Encounter:
        order = roll_initiative(combatants, roller)
        return cls(
            grid=grid, initiative=order, round_number=1, current_index=0,
            roller=roller,
        )

    def current_actor(self) -> Combatant | None:
        if not self.initiative:
            return None
        return self.initiative[self.current_index].combatant

    def advance_turn(self) -> None:
        """Move to the next combatant; bump round if we wrap around."""
        if not self.initiative:
            return
        self.current_index += 1
        if self.current_index >= len(self.initiative):
            self.current_index = 0
            self.round_number += 1
            for ir in self.initiative:
                ir.combatant.tick_round(self.round_number, roller=self.roller)

    def alive_combatants_on(self, team: str) -> list[Combatant]:
        return [
            ir.combatant for ir in self.initiative
            if ir.combatant.team == team and ir.combatant.is_alive()
            and ir.combatant.current_hp > 0
        ]

    def is_over(self) -> bool:
        """Default termination: only one team has conscious combatants."""
        teams_alive = {
            ir.combatant.team
            for ir in self.initiative
            if ir.combatant.current_hp > 0 and not ir.combatant.is_unconscious()
        }
        return len(teams_alive) <= 1

    def winner_team(self) -> str | None:
        teams_alive = {
            ir.combatant.team
            for ir in self.initiative
            if ir.combatant.current_hp > 0 and not ir.combatant.is_unconscious()
        }
        if len(teams_alive) == 1:
            return next(iter(teams_alive))
        return None


# ---------------------------------------------------------------------------
# Attack-of-opportunity detection
# ---------------------------------------------------------------------------


def aoo_triggers_for_movement(
    grid: Grid,
    mover: Combatant,
    leaving_square: tuple[int, int],
) -> list[Combatant]:
    """Hostile combatants who get an AoO when ``mover`` leaves ``leaving_square``.

    PF1: moving out of a threatened square provokes from the threatener
    (with exceptions for charge starts, withdraw's first square, and
    teleportation effects). The encounter loop is responsible for
    excluding those exceptions; this function just identifies who
    threatens the square.

    Allies on the same team don't trigger AoOs.
    """
    triggers: list[Combatant] = []
    for cid, other in grid.combatants.items():
        if other.id == mover.id:
            continue
        if other.team == mover.team:
            continue
        # Skip combatants who can't act (dying, unconscious, paralyzed).
        if other.is_unconscious():
            continue
        if "paralyzed" in other.conditions or "petrified" in other.conditions:
            continue
        if leaving_square in grid.threatened_squares(other):
            triggers.append(other)
    return triggers


def aoo_triggers_for_provoking_action(
    grid: Grid,
    actor: Combatant,
    action_type: str,
) -> list[Combatant]:
    """Hostile combatants who get an AoO when ``actor`` performs the action.

    Some actions inherently provoke from anyone threatening you: casting
    a spell (without cast-defensive), drinking a potion, retrieving a
    stowed item, etc. We just enumerate threateners; the encounter loop
    decides whether an action provokes based on the action type.
    """
    if action_type not in PROVOKING_ACTION_TYPES:
        return []
    triggers: list[Combatant] = []
    for cid, other in grid.combatants.items():
        if other.id == actor.id or other.team == actor.team:
            continue
        if other.is_unconscious():
            continue
        if "paralyzed" in other.conditions or "petrified" in other.conditions:
            continue
        if grid.threatens(other, actor):
            triggers.append(other)
    return triggers


# Action types that, by default, provoke an AoO from threateners.
PROVOKING_ACTION_TYPES = frozenset({
    "cast",                  # Casting (without cast_defensive)
    "drink",                 # Drinking a potion
    "use_item",              # Using a magic item that requires concentration
    "stand_up",              # Standing up from prone
    "draw_weapon",           # Unless you have BAB +1 (handled elsewhere)
    "ranged_attack",         # Making a ranged attack while threatened
})
