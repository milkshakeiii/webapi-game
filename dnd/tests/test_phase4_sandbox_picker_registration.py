"""DSL v2 Phase 4: auto-registration in the sandbox tick worker.

When a deployment engages and a ``WorldEncounter`` is created, the
hero's behavior script is loaded into ``we._behavior``. If that
script has any ``react:`` or ``sub:`` rules, the engine should
auto-register a ``CompiledReactivePicker`` on the encounter so the
rules fire when interrupts land — without the patron having to call
``register_script_pickers`` manually.

This test sets up a sandbox flow where a hero's library script
contains a ``react: aoo`` rule, runs ticks until engagement, then
inspects ``encounter.pickers`` to confirm the picker is registered
under the hero's combatant id.
"""

from __future__ import annotations

import json
import unittest

from dnd.engine.actions import CompiledReactivePicker
from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.content import default_registry
from dnd.sandbox.castle import new_castle
from dnd.sandbox.deployment import (
    ORDER_CREATE_CASTLE,
    ORDER_SPAWN_HERO,
    ORDER_SUBMIT_DEPLOYMENT,
    PHASE_IN_COMBAT,
    new_order,
)
from dnd.sandbox.hero_record import HeroRecord
from dnd.sandbox.tick import tick
from dnd.sandbox.world import Location, new_world


REGISTRY = default_registry()


def _fighter_hero(hero_id: str = "hero_1",
                  behavior_ref: str = "reactive_b") -> HeroRecord:
    req = CharacterRequest.from_dict({
        "name": "Edric", "race": "human", "class": "fighter",
        "alignment": "lawful_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 16, "dex": 14, "con": 14,
                       "int": 10, "wis": 10, "cha": 10}},
        "free_ability_choice": "str",
        "feats": ["power_attack", "weapon_focus"],
        "skill_ranks": {"climb": 1, "swim": 1},
        "bonus_languages": [],
        "class_choices": {"fighter_bonus_feat": "cleave"},
    })
    char = create_character(req, REGISTRY)
    return HeroRecord(id=hero_id, name="Edric", character=char,
                      behavior_ref=behavior_ref)


# Script as a JSON string (matches what castle.library_behaviors stores).
_REACTIVE_SCRIPT_JSON = json.dumps({
    "name": "reactive",
    "rules": [
        # Active rule: charge the closest foe.
        {"do": {"composite": "charge",
                "args": {"target": "enemy.closest"}}},
        # Reactive rule: pass on AoOs (so the picker gets exercised).
        {"react": "aoo", "do": {"type": "pass_aoo"}},
    ],
})


class TestSandboxPickerRegistration(unittest.TestCase):
    def test_reactive_script_auto_registers_on_engage(self):
        # Build world with a hostile location nearby.
        w = new_world(width=30, height=30, tick_interval_s=0.05)
        w.locations["loc_x"] = Location(
            id="loc_x", name="Goblin Camp", position=(15, 10),
            kind="camp", description="",
            resident_template="goblin", base_renown=10,
        )
        # Castle with the reactive script in its library.
        castle = new_castle("Hill", "h@y.com", (10, 10),
                            castle_id="castle_test")
        castle.library_behaviors["reactive_b"] = _REACTIVE_SCRIPT_JSON

        w.order_queue.submit(
            new_order(None, ORDER_CREATE_CASTLE, {"castle": castle}),
        )
        hero = _fighter_hero("hero_1")
        w.order_queue.submit(
            new_order(castle.id, ORDER_SPAWN_HERO, {"hero": hero}),
        )
        w.order_queue.submit(
            new_order(castle.id, ORDER_SUBMIT_DEPLOYMENT, {
                "deployment_id": "dep_1",
                "hero_id": hero.id,
                "location_id": "loc_x",
                "behavior_ref": "reactive_b",
                "seed": 42,
            }),
        )

        # Tick until engagement (a few ticks at most for distance 5).
        engaged = False
        for _ in range(10):
            tick(w, REGISTRY)
            d = w.deployments.get("dep_1")
            if d is not None and d.phase == PHASE_IN_COMBAT:
                engaged = True
                break
        self.assertTrue(engaged, "deployment should reach IN_COMBAT")

        # Find the active encounter.
        we = next(iter(w.active_encounters.values()))
        encounter = we.engine_encounter
        hero_combatant = we._hero  # type: ignore[attr-defined]

        # Picker registered for the hero.
        self.assertIn(hero_combatant.id, encounter.pickers,
                      "hero's reactive picker should be auto-registered")
        self.assertIsInstance(
            encounter.pickers[hero_combatant.id],
            CompiledReactivePicker,
        )


class TestSandboxNonReactiveScriptNoRegistration(unittest.TestCase):
    """A script with no ``react:`` / ``sub:`` rules should NOT cause
    a picker registration — keeps the registry empty for actors that
    don't need reactive overrides."""

    def test_active_only_script_does_not_register(self):
        w = new_world(width=30, height=30, tick_interval_s=0.05)
        w.locations["loc_x"] = Location(
            id="loc_x", name="Goblin Camp", position=(15, 10),
            kind="camp", description="",
            resident_template="goblin", base_renown=10,
        )
        castle = new_castle("Hill", "h@y.com", (10, 10),
                            castle_id="castle_active_only")
        # Active-only script — no react: rules.
        castle.library_behaviors["active_b"] = json.dumps({
            "name": "active",
            "rules": [
                {"do": {"composite": "charge",
                        "args": {"target": "enemy.closest"}}},
            ],
        })
        w.order_queue.submit(
            new_order(None, ORDER_CREATE_CASTLE, {"castle": castle}),
        )
        hero = _fighter_hero("hero_2", behavior_ref="active_b")
        w.order_queue.submit(
            new_order(castle.id, ORDER_SPAWN_HERO, {"hero": hero}),
        )
        w.order_queue.submit(
            new_order(castle.id, ORDER_SUBMIT_DEPLOYMENT, {
                "deployment_id": "dep_a",
                "hero_id": hero.id,
                "location_id": "loc_x",
                "behavior_ref": "active_b",
                "seed": 42,
            }),
        )
        engaged = False
        for _ in range(10):
            tick(w, REGISTRY)
            d = w.deployments.get("dep_a")
            if d is not None and d.phase == PHASE_IN_COMBAT:
                engaged = True
                break
        self.assertTrue(engaged)
        we = next(iter(w.active_encounters.values()))
        hero_c = we._hero  # type: ignore[attr-defined]
        self.assertNotIn(hero_c.id, we.engine_encounter.pickers)


if __name__ == "__main__":
    unittest.main()
