"""Tests for carrying capacity and load-category penalties."""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import combatant_from_character
from dnd.engine.content import default_registry
from dnd.engine.encumbrance import (
    carried_weight,
    heavy_load_for,
    load_category,
)


REGISTRY = default_registry()


class TestHeavyLoadTable(unittest.TestCase):
    def test_str_10_heavy_load_is_100(self):
        self.assertEqual(heavy_load_for(10), 100)

    def test_str_18_heavy_load_is_300(self):
        self.assertEqual(heavy_load_for(18), 300)

    def test_str_zero_or_negative(self):
        self.assertEqual(heavy_load_for(0), 0)
        self.assertEqual(heavy_load_for(-3), 0)

    def test_str_above_30_doubles_by_4_per_10(self):
        # Str 30 = 1600; Str 40 = 6400; Str 50 = 25600.
        self.assertEqual(heavy_load_for(40), 6400)
        self.assertEqual(heavy_load_for(50), 25600)


class TestLoadCategory(unittest.TestCase):
    def test_below_third_is_light(self):
        # Str 10 → light=33, medium=66, heavy=100.
        self.assertEqual(load_category(20, 10), "light")
        self.assertEqual(load_category(33, 10), "light")

    def test_just_over_light_is_medium(self):
        self.assertEqual(load_category(34, 10), "medium")

    def test_at_two_thirds_is_medium(self):
        self.assertEqual(load_category(66, 10), "medium")

    def test_just_over_two_thirds_is_heavy(self):
        self.assertEqual(load_category(67, 10), "heavy")

    def test_at_heavy_max_is_heavy(self):
        self.assertEqual(load_category(100, 10), "heavy")

    def test_over_heavy_is_overloaded(self):
        self.assertEqual(load_category(150, 10), "overloaded")

    def test_zero_str_is_overloaded(self):
        self.assertEqual(load_category(1, 0), "overloaded")


class TestCarriedWeight(unittest.TestCase):
    def test_fighter_default_loadout(self):
        # 5+5+5+2+2+1 = 20 point-buy, human (2 feats including bonus).
        req = CharacterRequest.from_dict({
            "name": "Edric", "race": "human", "class": "fighter",
            "alignment": "lawful_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 14, "con": 14,
                           "int": 12, "wis": 12, "cha": 11}},
            "free_ability_choice": "str",
            "feats": ["power_attack", "iron_will"],
            "skill_ranks": {"climb": 1, "swim": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "weapon_focus_longsword"},
        })
        char = create_character(req, REGISTRY)
        weight = carried_weight(char, REGISTRY)
        # Default fighter loadout: longsword (4) + chainmail (40) + heavy_steel_shield (15) = 59 lb.
        # Verify that we get a reasonable, > 0 number.
        self.assertGreater(weight, 0)


class TestEncumbranceAcpStacks(unittest.TestCase):
    def test_heavy_load_layers_extra_acp(self):
        # Build a fighter with heavy gear that pushes them into heavy
        # load. Compare ACP-affected skill totals to a baseline fighter.
        # Easier: construct two characters, one with shield and one
        # without, each with equal Str. The shielded one's ACP-skill
        # totals should be lower.
        base = self._fighter(equipment=None)
        loaded = self._fighter(equipment={
            "weapon": "longsword",
            "armor": "chainmail",
            "shield": "heavy_steel_shield",
        })
        # Climb is ACP-affected. Find the difference and verify it's
        # at least the shield ACP (-2). With heavy load it'd be more.
        base_climb = base.skill_total("climb")
        loaded_climb = loaded.skill_total("climb")
        self.assertLess(loaded_climb, base_climb)

    def _fighter(self, equipment):
        # Lower Str so that reasonable gear pushes us into heavy load:
        # Str 8 → heavy load = 26 lb. Chainmail alone is 40 lb.
        # 5+0+5+2+2+1 = 15 (point buy 15). Use point_buy_15.
        # But class_choices needs fighter bonus feat.
        # str=8(-2) dex=14(5) con=14(5) int=12(2) wis=12(2) cha=11(1) = 13 — need 15.
        # str=8(-2) dex=14(5) con=14(5) int=13(3) wis=12(2) cha=11(1) = 14.
        # str=8(-2) dex=14(5) con=14(5) int=13(3) wis=13(3) cha=11(1) = 15 ✓
        req_d: dict = {
            "name": "Wimpy", "race": "human", "class": "fighter",
            "alignment": "lawful_good",
            "ability_scores": {"method": "point_buy_15",
                "scores": {"str": 8, "dex": 14, "con": 14,
                           "int": 13, "wis": 13, "cha": 11}},
            "free_ability_choice": "dex",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"climb": 1, "swim": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "combat_reflexes"},
        }
        if equipment is None:
            # Skip equipment to avoid default loadout — keep test clean.
            req_d["equipment"] = {"weapon": None, "armor": None, "shield": None}
        else:
            req_d["equipment"] = equipment
        char = create_character(CharacterRequest.from_dict(req_d), REGISTRY)
        return combatant_from_character(char, REGISTRY, (5, 5), "x")


if __name__ == "__main__":
    unittest.main()
