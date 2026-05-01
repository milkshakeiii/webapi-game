"""Test-scenario harness.

A scenario is a self-contained fight: a grid (with optional terrain), a
set of combatants (each with a position, team, and optional behavior
script), win/loss conditions, and a turn cap. ``run_scenario`` simulates
the encounter to completion and returns a deterministic ``ScenarioResult``
with the full event trace.

The engine that drives the loop is the same one used by the persistent
world; scenarios are isolated only in that they don't touch any
persistent storage.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .characters import Character, CharacterRequest, create_character
from .combatant import (
    Combatant,
    combatant_from_character,
    combatant_from_monster,
)
from .content import ContentRegistry
from .dice import Roller
from .dsl import BehaviorScript, Interpreter, script_from_dict
from .encounter import Encounter
from .grid import Grid, GridFeature, difficult, wall, water
from .turn_executor import (
    TurnEvent,
    TurnResult,
    default_monster_intent,
    execute_turn,
)


# ---------------------------------------------------------------------------
# Scenario spec
# ---------------------------------------------------------------------------


@dataclass
class CombatantSpec:
    """One combatant in a scenario."""

    template_kind: str        # "monster" or "character"
    template_id: str | None   # monster id (if monster); None for inline character
    character_request: dict | None    # character creation request (if character)
    position: tuple[int, int]
    team: str
    behavior: dict | None     # parsed behavior script (or None for default AI)
    name_override: str | None = None


@dataclass
class FeatureSpec:
    x: int
    y: int
    type: str       # "wall", "difficult", "water"


@dataclass
class ScenarioSpec:
    name: str
    width: int
    height: int
    features: list[FeatureSpec] = field(default_factory=list)
    combatants: list[CombatantSpec] = field(default_factory=list)
    turn_limit: int = 50           # round cap
    win_condition: str = "last_team_standing"
    seed: int = 0

    @classmethod
    def from_dict(cls, d: dict) -> ScenarioSpec:
        if not isinstance(d, dict):
            raise ValueError("scenario must be an object")
        features: list[FeatureSpec] = []
        for f in d.get("features") or []:
            features.append(FeatureSpec(
                x=int(f["x"]), y=int(f["y"]), type=str(f["type"]),
            ))
        combatants: list[CombatantSpec] = []
        for c in d.get("combatants") or []:
            kind = str(c.get("template_kind", "monster"))
            if kind == "monster":
                tid = c.get("template_id")
                req = None
            elif kind == "character":
                tid = None
                req = c.get("character_request") or {}
            else:
                raise ValueError(f"unknown template_kind {kind!r}")
            pos = c.get("position") or [0, 0]
            combatants.append(CombatantSpec(
                template_kind=kind,
                template_id=tid,
                character_request=req,
                position=(int(pos[0]), int(pos[1])),
                team=str(c["team"]),
                behavior=c.get("behavior"),
                name_override=c.get("name"),
            ))
        return cls(
            name=str(d.get("name", "<scenario>")),
            width=int(d.get("width", 10)),
            height=int(d.get("height", 10)),
            features=features,
            combatants=combatants,
            turn_limit=int(d.get("turn_limit", 50)),
            win_condition=str(d.get("win_condition", "last_team_standing")),
            seed=int(d.get("seed", 0)),
        )


# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------


@dataclass
class ScenarioResult:
    name: str
    seed: int
    rounds: int
    winner: str | None
    timed_out: bool
    initiative: list[dict]
    turns: list[dict]
    final_state: dict        # per-combatant snapshot (HP, conditions, position)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "seed": self.seed,
            "rounds": self.rounds,
            "winner": self.winner,
            "timed_out": self.timed_out,
            "initiative": list(self.initiative),
            "turns": list(self.turns),
            "final_state": dict(self.final_state),
        }


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


_FEATURE_FACTORIES = {
    "wall":      wall,
    "difficult": difficult,
    "water":     water,
}


def run_scenario(spec: ScenarioSpec, registry: ContentRegistry) -> ScenarioResult:
    """Simulate the scenario to completion (or turn cap)."""
    grid = Grid(width=spec.width, height=spec.height)
    for f in spec.features:
        factory = _FEATURE_FACTORIES.get(f.type)
        if factory is None:
            grid.add_feature(f.x, f.y, GridFeature(type=f.type))
        else:
            grid.add_feature(f.x, f.y, factory())

    seed = spec.seed
    roller = Roller(seed=seed)

    # Build combatants and behavior scripts.
    combatants: list[Combatant] = []
    interpreters: dict[str, Interpreter] = {}
    for cs in spec.combatants:
        c = _build_combatant(cs, registry, roller)
        if cs.name_override:
            c.name = cs.name_override
        grid.place(c)
        combatants.append(c)
        if cs.behavior is not None:
            try:
                script = script_from_dict(cs.behavior)
            except Exception as e:
                raise ValueError(
                    f"invalid behavior for combatant {c.name}: {e}"
                ) from e
            interpreters[c.id] = Interpreter(script)

    enc = Encounter.begin(grid, combatants, roller)

    initiative_dump = [ir.to_dict() for ir in enc.initiative]
    turns: list[dict] = []

    timed_out = False
    while not enc.is_over():
        if enc.round_number > spec.turn_limit:
            timed_out = True
            break
        actor = enc.current_actor()
        if actor is None:
            break
        if not actor.is_alive() or actor.current_hp <= -10 or actor.is_unconscious():
            enc.advance_turn()
            continue
        intent = None
        if actor.id in interpreters:
            intent = interpreters[actor.id].pick_turn(actor, enc, grid)
        else:
            intent = default_monster_intent(actor, enc, grid)
        result = execute_turn(actor, intent, enc, grid, roller)
        turns.append({
            "round": enc.round_number,
            **result.to_dict(),
        })
        enc.advance_turn()

    final_state = {}
    for c in combatants:
        final_state[c.id] = {
            "name": c.name,
            "team": c.team,
            "current_hp": c.current_hp,
            "max_hp": c.max_hp,
            "position": list(c.position),
            "conditions": sorted(c.conditions),
            "alive": c.is_alive() and c.current_hp > 0,
        }

    return ScenarioResult(
        name=spec.name,
        seed=seed,
        rounds=enc.round_number,
        winner=enc.winner_team(),
        timed_out=timed_out,
        initiative=initiative_dump,
        turns=turns,
        final_state=final_state,
    )


# ---------------------------------------------------------------------------
# Combatant construction
# ---------------------------------------------------------------------------


def _build_combatant(
    cs: CombatantSpec,
    registry: ContentRegistry,
    roller: Roller,
) -> Combatant:
    if cs.template_kind == "monster":
        if not cs.template_id:
            raise ValueError("monster combatant requires template_id")
        return combatant_from_monster(
            registry.get_monster(cs.template_id),
            cs.position,
            cs.team,
            name=cs.name_override,
        )
    elif cs.template_kind == "character":
        req_dict = cs.character_request or {}
        request = CharacterRequest.from_dict(req_dict)
        char = create_character(request, registry, roller=roller)
        return combatant_from_character(char, registry, cs.position, cs.team)
    else:
        raise ValueError(f"unknown template_kind {cs.template_kind!r}")
