"""Tests for Phase 4.2 — cantrip / orison at-will semantics + the
new combat-relevant 0-level spells (ray_of_frost, disrupt_undead,
flare, touch_of_fatigue, bleed, resistance, virtue, guidance)."""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import (
    combatant_from_character,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


def _wizard():
    req = CharacterRequest.from_dict({
        "name": "Wiz", "race": "human", "class": "wizard",
        "alignment": "true_neutral",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 8, "dex": 14, "con": 12,
                       "int": 16, "wis": 14, "cha": 10}},
        "free_ability_choice": "int",
        "feats": ["alertness", "iron_will"],
        "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
        "bonus_languages": ["draconic"],
    })
    char = create_character(req, REGISTRY)
    return combatant_from_character(char, REGISTRY, (5, 5), "x")


def _cleric():
    req = CharacterRequest.from_dict({
        "name": "Cael", "race": "human", "class": "cleric",
        "alignment": "neutral_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 10, "dex": 10, "con": 14,
                       "int": 10, "wis": 16, "cha": 14}},
        "free_ability_choice": "wis",
        "feats": ["alertness", "iron_will"],
        "skill_ranks": {"heal": 1, "knowledge_religion": 1},
        "bonus_languages": [],
    })
    char = create_character(req, REGISTRY)
    return combatant_from_character(char, REGISTRY, (5, 5), "x")


def _cast_intent(spell_id, target_obj=None, spell_level=0):
    return BehaviorScript(name="cast", rules=[
        Rule(do={"standard": {
            "type": "cast",
            "spell": spell_id,
            "spell_level": spell_level,
            "target": target_obj,
        }}),
    ])


# ---------------------------------------------------------------------------
# At-will semantics
# ---------------------------------------------------------------------------


class TestCantripAtWill(unittest.TestCase):
    def test_wizard_cantrip_does_not_consume_slot(self):
        wiz = _wizard()
        wiz.casting_type = "prepared"
        wiz.prepared_spells = {0: ["ray_of_frost"], 1: ["magic_missile"]}
        wiz.castable_spells = {"ray_of_frost", "magic_missile"}
        wiz.resources["spell_slot_0"] = 4
        wiz.resources["spell_slot_1"] = 1
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (6, 5), "y")
        target.max_hp = 9999
        target.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(wiz)
        grid.place(target)
        enc = Encounter.begin(grid, [wiz, target], Roller(seed=1))
        # Cast ray_of_frost three times; slot count should not drop.
        for _ in range(3):
            intent = Interpreter(_cast_intent(
                "ray_of_frost", target, 0,
            )).pick_turn(wiz, enc, grid)
            execute_turn(wiz, intent, enc, grid, Roller(seed=1))
        self.assertEqual(wiz.resources["spell_slot_0"], 4)
        # ray_of_frost still in prepared_spells (not consumed).
        self.assertIn("ray_of_frost", wiz.prepared_spells[0])

    def test_wizard_l1_spell_consumes_slot_normally(self):
        wiz = _wizard()
        wiz.casting_type = "prepared"
        wiz.prepared_spells = {0: ["ray_of_frost"], 1: ["magic_missile"]}
        wiz.castable_spells = {"ray_of_frost", "magic_missile"}
        wiz.resources["spell_slot_0"] = 4
        wiz.resources["spell_slot_1"] = 1
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (6, 5), "y")
        target.max_hp = 9999
        target.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(wiz)
        grid.place(target)
        enc = Encounter.begin(grid, [wiz, target], Roller(seed=1))
        intent = Interpreter(_cast_intent(
            "magic_missile", target, 1,
        )).pick_turn(wiz, enc, grid)
        execute_turn(wiz, intent, enc, grid, Roller(seed=1))
        # L1 slot consumed; magic_missile prep entry burned.
        self.assertEqual(wiz.resources["spell_slot_1"], 0)
        self.assertEqual(wiz.prepared_spells.get(1, []), [])


# ---------------------------------------------------------------------------
# Ray of Frost
# ---------------------------------------------------------------------------


class TestRayOfFrost(unittest.TestCase):
    def test_ray_of_frost_can_damage_target(self):
        wiz = _wizard()
        wiz.casting_type = "prepared"
        wiz.prepared_spells = {0: ["ray_of_frost"]}
        wiz.castable_spells = {"ray_of_frost"}
        wiz.resources["spell_slot_0"] = 4
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (6, 5), "y")
        target.max_hp = 9999
        target.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(wiz)
        grid.place(target)
        enc = Encounter.begin(grid, [wiz, target], Roller(seed=1))
        # Boost wizard's BAB for the touch attack to land predictably.
        wiz.bases["bab"] = 100
        before = target.current_hp
        for seed in range(1, 30):
            intent = Interpreter(_cast_intent(
                "ray_of_frost", target, 0,
            )).pick_turn(wiz, enc, grid)
            execute_turn(wiz, intent, enc, grid, Roller(seed=seed))
            if target.current_hp < before:
                return
        self.fail("no seed in 1..29 landed any cold damage")


# ---------------------------------------------------------------------------
# Bleed
# ---------------------------------------------------------------------------


class TestBleedCantrip(unittest.TestCase):
    def test_bleed_starts_bleed_on_dying_target(self):
        cleric = _cleric()
        cleric.casting_type = "prepared"
        cleric.prepared_spells = {0: ["bleed"]}
        cleric.castable_spells = {"bleed"}
        cleric.resources["spell_slot_0"] = 4
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (6, 5), "y")
        target.current_hp = -3  # dying
        target.add_condition("dying")
        target.add_condition("stable")
        grid = Grid(width=12, height=12)
        grid.place(cleric)
        grid.place(target)
        enc = Encounter.begin(grid, [cleric, target], Roller(seed=1))
        # Find a seed where target fails the Will save.
        for seed in range(1, 50):
            target.bleed = 0
            intent = Interpreter(_cast_intent(
                "bleed", target, 0,
            )).pick_turn(cleric, enc, grid)
            execute_turn(cleric, intent, enc, grid, Roller(seed=seed))
            if target.bleed > 0:
                self.assertIn("bleed", target.conditions)
                return
        self.fail("no seed in 1..49 applied bleed")

    def test_bleed_skips_when_target_alive(self):
        cleric = _cleric()
        cleric.casting_type = "prepared"
        cleric.prepared_spells = {0: ["bleed"]}
        cleric.castable_spells = {"bleed"}
        cleric.resources["spell_slot_0"] = 4
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (6, 5), "y")
        # Target is at full HP, not dying.
        grid = Grid(width=12, height=12)
        grid.place(cleric)
        grid.place(target)
        enc = Encounter.begin(grid, [cleric, target], Roller(seed=1))
        intent = Interpreter(_cast_intent(
            "bleed", target, 0,
        )).pick_turn(cleric, enc, grid)
        execute_turn(cleric, intent, enc, grid, Roller(seed=1))
        # No bleed because requires_below_zero_hp.
        self.assertEqual(target.bleed, 0)


# ---------------------------------------------------------------------------
# Resistance (buff)
# ---------------------------------------------------------------------------


class TestResistanceCantrip(unittest.TestCase):
    def test_resistance_grants_plus_one_to_all_saves(self):
        cleric = _cleric()
        cleric.casting_type = "prepared"
        cleric.prepared_spells = {0: ["resistance"]}
        cleric.castable_spells = {"resistance"}
        cleric.resources["spell_slot_0"] = 4
        ally = combatant_from_monster(REGISTRY.get_monster("orc"),
                                      (5, 6), "x")
        # Target self.
        grid = Grid(width=12, height=12)
        grid.place(cleric)
        grid.place(ally)
        enc = Encounter.begin(grid, [cleric, ally], Roller(seed=1))
        before_will = cleric.save("will")
        intent = Interpreter(_cast_intent(
            "resistance", cleric, 0,
        )).pick_turn(cleric, enc, grid)
        execute_turn(cleric, intent, enc, grid, Roller(seed=1))
        after_will = cleric.save("will")
        self.assertEqual(after_will - before_will, 1)


# ---------------------------------------------------------------------------
# Disrupt Undead
# ---------------------------------------------------------------------------


class TestDisruptUndead(unittest.TestCase):
    def test_disrupt_undead_can_damage_skeleton(self):
        wiz = _wizard()
        wiz.casting_type = "prepared"
        wiz.prepared_spells = {0: ["disrupt_undead"]}
        wiz.castable_spells = {"disrupt_undead"}
        wiz.resources["spell_slot_0"] = 4
        wiz.bases["bab"] = 100
        sk = combatant_from_monster(REGISTRY.get_monster("skeleton"),
                                    (6, 5), "y")
        sk.max_hp = 9999
        sk.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(wiz)
        grid.place(sk)
        enc = Encounter.begin(grid, [wiz, sk], Roller(seed=1))
        before = sk.current_hp
        for seed in range(1, 30):
            intent = Interpreter(_cast_intent(
                "disrupt_undead", sk, 0,
            )).pick_turn(wiz, enc, grid)
            execute_turn(wiz, intent, enc, grid, Roller(seed=seed))
            if sk.current_hp < before:
                return
        self.fail("no seed in 1..29 dealt disrupt_undead damage")


if __name__ == "__main__":
    unittest.main()
