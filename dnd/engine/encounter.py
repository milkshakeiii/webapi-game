"""Encounter scaffolding: initiative, encounter state, AoO detection.

What's here:

- ``roll_initiative`` — d20 + initiative modifier, ordered by descending
  total.
- ``Encounter`` — live state for a fight: combatants, initiative order,
  round counter, current-actor index, the reactive picker registry.
- ``aoo_triggers_for_movement`` — given a movement step, returns the
  hostile combatants who threaten the origin square and would get an
  attack of opportunity.

Action-economy validation lives in ``actions._validate_intent`` (the
substrate's intent-translation seam).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .combatant import Combatant
from .dice import Roller
from .grid import Grid


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
    # DSL v2 Phase 3: per-actor reactive picker registry. When a
    # reactive interrupt fires (AoO, brace, cleave continuation), the
    # engine looks up the threatener / decision-owner here. Missing
    # entries fall back to v1-equivalent defaults (e.g., AoO uses
    # weapon 0, brace always springs). Active-turn pickers live
    # elsewhere — the encounter only carries reactive ones.
    pickers: dict = field(default_factory=dict)

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
