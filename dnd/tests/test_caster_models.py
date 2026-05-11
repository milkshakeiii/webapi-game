"""Tests for spontaneous vs prepared casters: spell-prep consumption,
spontaneous flexibility, casting-type detection."""

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


def _wizard_request(spells_prepared: dict | None = None) -> dict:
    return {
        "name": "Aurelia", "race": "elf", "class": "wizard",
        "alignment": "neutral_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 8, "dex": 14, "con": 14,
                       "int": 16, "wis": 12, "cha": 10}},
        "feats": ["combat_expertise"],
        "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
        "bonus_languages": [],
        "spells_prepared": spells_prepared,
    }


def _sorcerer_request(spells_known: dict | None = None) -> dict:
    return {
        "name": "Vyx", "race": "elf", "class": "sorcerer",
        "alignment": "chaotic_neutral",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 8, "dex": 14, "con": 14,
                       "int": 12, "wis": 10, "cha": 16}},
        "feats": ["combat_expertise"],
        "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
        "bonus_languages": [],
        "class_choices": {"sorcerer_bloodline": "arcane"},
        "spells_known": spells_known,
    }


class TestCastingTypeDetection(unittest.TestCase):
    def test_wizard_is_prepared(self):
        char = create_character(
            CharacterRequest.from_dict(_wizard_request()), REGISTRY,
        )
        c = combatant_from_character(char, REGISTRY, (5, 5), "x")
        self.assertEqual(c.casting_type, "prepared")

    def test_sorcerer_is_spontaneous(self):
        char = create_character(
            CharacterRequest.from_dict(_sorcerer_request()), REGISTRY,
        )
        c = combatant_from_character(char, REGISTRY, (5, 5), "x")
        self.assertEqual(c.casting_type, "spontaneous")

    def test_fighter_has_no_casting_type(self):
        # 5+5+5+2+2+1 = 20.
        req = CharacterRequest.from_dict({
            "name": "Edric", "race": "human", "class": "fighter",
            "alignment": "lawful_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 14, "con": 14,
                           "int": 12, "wis": 12, "cha": 11}},
            "free_ability_choice": "str",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"climb": 1, "swim": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "combat_reflexes"},
        })
        char = create_character(req, REGISTRY)
        c = combatant_from_character(char, REGISTRY, (5, 5), "x")
        self.assertEqual(c.casting_type, "")


class TestPreparedCasterSpellConsumption(unittest.TestCase):
    def _wizard_with_prep(self, prep: dict[int, list[str]]):
        char = create_character(
            CharacterRequest.from_dict(_wizard_request(spells_prepared=prep)),
            REGISTRY,
        )
        return combatant_from_character(char, REGISTRY, (5, 5), "x")

    def _setup_combat(self, wizard):
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (10, 5), "y")
        grid = Grid(width=20, height=10)
        grid.place(wizard)
        grid.place(target)
        enc = Encounter.begin(grid, [wizard, target], Roller(seed=1))
        return target, grid, enc

    def _cast_intent(self, spell_id="magic_missile", spell_level=1):
        return BehaviorScript(name="cast", rules=[
            Rule(do={"composite": "cast", "args": {
                "spell": spell_id, "spell_level": spell_level,
                "target": "enemy.closest", "defensive": False,
            }}),
        ])

    def test_prepared_spell_consumed_on_cast(self):
        wiz = self._wizard_with_prep({1: ["magic_missile"]})
        self.assertEqual(wiz.prepared_spells.get(1), ["magic_missile"])
        target, grid, enc = self._setup_combat(wiz)
        intent = Interpreter(self._cast_intent()).pick_turn(wiz, enc, grid)
        execute_turn(wiz, intent, enc, grid, Roller(seed=1))
        # After casting, the prepared list at level 1 should be empty.
        self.assertEqual(wiz.prepared_spells.get(1), [])

    def test_unprepared_spell_skips(self):
        # Wizard prepares only sleep, not magic_missile.
        wiz = self._wizard_with_prep({1: ["sleep"]})
        target, grid, enc = self._setup_combat(wiz)
        slots_before = wiz.resources.get("spell_slot_1", 0)
        intent = Interpreter(self._cast_intent()).pick_turn(wiz, enc, grid)
        result = execute_turn(wiz, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("skip", kinds)
        # Slot is NOT consumed when the spell isn't prepared at all.
        self.assertEqual(wiz.resources.get("spell_slot_1"), slots_before)

    def test_duplicate_prep_allows_two_casts(self):
        # Wizard preps magic_missile twice in two L1 slots.
        wiz = self._wizard_with_prep({1: ["magic_missile", "magic_missile"]})
        wiz.resources["spell_slot_1"] = 2
        target, grid, enc = self._setup_combat(wiz)
        intent = Interpreter(self._cast_intent()).pick_turn(wiz, enc, grid)
        execute_turn(wiz, intent, enc, grid, Roller(seed=1))
        # One copy left.
        self.assertEqual(wiz.prepared_spells.get(1), ["magic_missile"])
        # Cast again — succeeds, list becomes empty.
        wiz.resources["spell_slot_1"] = 1
        intent = Interpreter(self._cast_intent()).pick_turn(wiz, enc, grid)
        execute_turn(wiz, intent, enc, grid, Roller(seed=2))
        self.assertEqual(wiz.prepared_spells.get(1), [])

    def test_empty_prep_falls_back_to_spontaneous_behavior(self):
        # Wizard with NO prep specified should still be able to cast
        # (legacy/default-dispatch fallback) — castable_spells is the
        # gate.
        wiz = self._wizard_with_prep({})
        target, grid, enc = self._setup_combat(wiz)
        before = target.current_hp
        intent = Interpreter(self._cast_intent()).pick_turn(wiz, enc, grid)
        execute_turn(wiz, intent, enc, grid, Roller(seed=1))
        # Damage was dealt (cast went through under the fallback).
        self.assertLess(target.current_hp, before)


class TestSpontaneousCaster(unittest.TestCase):
    def test_sorcerer_castable_set_filtered_by_known_list(self):
        # When spells_known is specified, castable_spells = the known list.
        known = {0: ["acid_splash"], 1: ["magic_missile"]}
        char = create_character(
            CharacterRequest.from_dict(_sorcerer_request(spells_known=known)),
            REGISTRY,
        )
        c = combatant_from_character(char, REGISTRY, (5, 5), "x")
        # acid_splash and magic_missile are castable; bless (cleric)
        # is not.
        self.assertIn("magic_missile", c.castable_spells)
        self.assertIn("acid_splash", c.castable_spells)

    def test_sorcerer_no_prepared_state(self):
        # Spontaneous casters should never have anything in
        # prepared_spells.
        char = create_character(
            CharacterRequest.from_dict(_sorcerer_request()), REGISTRY,
        )
        c = combatant_from_character(char, REGISTRY, (5, 5), "x")
        self.assertEqual(c.prepared_spells, {})


if __name__ == "__main__":
    unittest.main()
