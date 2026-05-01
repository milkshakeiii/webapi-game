"""Tests for the level-up plan + multi-level character build."""

from __future__ import annotations

import unittest

from dnd.engine.characters import (
    CharacterCreationError,
    CharacterRequest,
    compute_sheet,
    create_character,
)
from dnd.engine.combatant import combatant_from_character
from dnd.engine.content import default_registry
from dnd.engine.level_plan import LevelEntry, LevelPlanError, LevelUpPlan
from dnd.engine.progression import (
    ability_bump_levels,
    bab_at,
    bonus_spells_per_day,
    general_feat_levels,
    iterative_attacks,
    save_base_at,
    spells_known_at,
    spells_per_day_at,
)


REGISTRY = default_registry()


def _basic_fighter_request_dict() -> dict:
    return {
        "name": "Sir Edric",
        "race": "human",
        "class": "fighter",
        "alignment": "lawful_good",
        "ability_scores": {
            "method": "point_buy_20",
            "scores": {"str": 16, "dex": 14, "con": 14,
                       "int": 10, "wis": 10, "cha": 10},
        },
        "free_ability_choice": "str",
        "feats": ["power_attack", "weapon_focus"],
        "skill_ranks": {"climb": 1, "swim": 1},
        "bonus_languages": [],
        "class_choices": {"fighter_bonus_feat": "cleave"},
    }


# ---------------------------------------------------------------------------
# Progression formulas
# ---------------------------------------------------------------------------


class TestBabFormulas(unittest.TestCase):
    def test_full_progression(self):
        for L in range(1, 21):
            self.assertEqual(bab_at("full", L), L)

    def test_three_quarters(self):
        # L1=0, L2=1, L3=2, L4=3, L5=3, L6=4, L7=5, L8=6
        cases = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 3), (6, 4),
                 (7, 5), (8, 6), (12, 9), (20, 15)]
        for level, expected in cases:
            self.assertEqual(bab_at("three_quarters", level), expected, level)

    def test_half(self):
        # L1=0, L2=1, L3=1, L4=2, L20=10
        cases = [(1, 0), (2, 1), (3, 1), (4, 2), (5, 2),
                 (6, 3), (10, 5), (20, 10)]
        for level, expected in cases:
            self.assertEqual(bab_at("half", level), expected, level)


class TestSaveFormulas(unittest.TestCase):
    def test_good_save(self):
        cases = [(1, 2), (2, 3), (3, 3), (4, 4), (5, 4),
                 (10, 7), (15, 9), (20, 12)]
        for level, expected in cases:
            self.assertEqual(save_base_at("good", level), expected)

    def test_poor_save(self):
        cases = [(1, 0), (2, 0), (3, 1), (4, 1), (5, 1),
                 (6, 2), (10, 3), (20, 6)]
        for level, expected in cases:
            self.assertEqual(save_base_at("poor", level), expected)


class TestIterativeAttacks(unittest.TestCase):
    def test_low_bab(self):
        self.assertEqual(iterative_attacks(0), [0])
        self.assertEqual(iterative_attacks(5), [5])

    def test_two_attacks(self):
        self.assertEqual(iterative_attacks(6), [6, 1])
        self.assertEqual(iterative_attacks(10), [10, 5])

    def test_three_attacks(self):
        self.assertEqual(iterative_attacks(11), [11, 6, 1])
        self.assertEqual(iterative_attacks(15), [15, 10, 5])

    def test_four_attacks(self):
        self.assertEqual(iterative_attacks(16), [16, 11, 6, 1])
        self.assertEqual(iterative_attacks(20), [20, 15, 10, 5])


class TestSpellTables(unittest.TestCase):
    def test_wizard_l1(self):
        slots = spells_per_day_at("wizard", 1)
        self.assertEqual(slots["0"], 3)
        self.assertEqual(slots["1"], 1)
        self.assertEqual(slots["2"], 0)

    def test_wizard_l5(self):
        slots = spells_per_day_at("wizard", 5)
        self.assertEqual(slots["0"], 4)
        self.assertEqual(slots["1"], 3)
        self.assertEqual(slots["2"], 2)
        self.assertEqual(slots["3"], 1)

    def test_sorcerer_known(self):
        known = spells_known_at("sorcerer", 1)
        self.assertEqual(known["0"], 4)
        self.assertEqual(known["1"], 2)

    def test_paladin_no_spells_until_l4(self):
        self.assertEqual(spells_per_day_at("paladin", 1), {})
        self.assertEqual(spells_per_day_at("paladin", 3), {})
        slots4 = spells_per_day_at("paladin", 4)
        self.assertEqual(slots4["1"], 0)  # baseline; bonus from Cha may add
        slots5 = spells_per_day_at("paladin", 5)
        self.assertEqual(slots5["1"], 1)

    def test_bonus_spells_from_ability(self):
        # Score 18 → +1 to L1, L2, L3, L4 (one bonus slot at every level
        # the score qualifies for).
        bonus = bonus_spells_per_day(18)
        self.assertEqual(bonus.get("1"), 1)
        self.assertEqual(bonus.get("2"), 1)
        self.assertEqual(bonus.get("3"), 1)
        self.assertEqual(bonus.get("4"), 1)
        self.assertNotIn("5", bonus)

    def test_no_bonus_below_12(self):
        self.assertEqual(bonus_spells_per_day(10), {})
        self.assertEqual(bonus_spells_per_day(11), {})


class TestFeatAndBumpSchedule(unittest.TestCase):
    def test_general_feat_levels(self):
        self.assertEqual(general_feat_levels(20),
                         [1, 3, 5, 7, 9, 11, 13, 15, 17, 19])

    def test_ability_bump_levels(self):
        self.assertEqual(ability_bump_levels(20), [4, 8, 12, 16, 20])
        self.assertEqual(ability_bump_levels(7), [4])
        self.assertEqual(ability_bump_levels(3), [])


# ---------------------------------------------------------------------------
# LevelUpPlan parsing & validation
# ---------------------------------------------------------------------------


class TestPlanParsing(unittest.TestCase):
    def test_minimal_plan(self):
        plan = LevelUpPlan.from_dict({
            "name": "test", "target_level": 1, "levels": {},
        })
        self.assertEqual(plan.target_level, 1)
        self.assertEqual(plan.levels, {})

    def test_plan_must_cover_every_level(self):
        with self.assertRaises(LevelPlanError):
            LevelUpPlan.from_dict({
                "name": "gap",
                "target_level": 3,
                "levels": {
                    "2": {"class": "fighter"},
                    # missing "3"
                },
            })

    def test_plan_target_level_range(self):
        with self.assertRaises(LevelPlanError):
            LevelUpPlan.from_dict({
                "name": "x", "target_level": 0, "levels": {},
            })

    def test_round_trip(self):
        plan = LevelUpPlan.from_dict({
            "name": "two-hander",
            "target_level": 2,
            "levels": {
                "2": {
                    "class": "fighter",
                    "hp_method": "fixed_half",
                    "skill_ranks": {"climb": 1},
                    "feat_class_bonus": "weapon_specialization",
                },
            },
        })
        d = plan.to_dict()
        plan2 = LevelUpPlan.from_dict(d)
        self.assertEqual(plan2.target_level, 2)
        self.assertEqual(plan2.levels[2].class_id, "fighter")


# ---------------------------------------------------------------------------
# Multi-level character creation
# ---------------------------------------------------------------------------


class TestMultiLevelFighter(unittest.TestCase):
    def _request_with_plan(self, levels: dict) -> CharacterRequest:
        body = _basic_fighter_request_dict()
        body["level_plan"] = {
            "name": "fighter_progression",
            "target_level": max(int(k) for k in levels) if levels else 1,
            "levels": levels,
        }
        return CharacterRequest.from_dict(body)

    def test_l2_fighter_bab_and_saves(self):
        # Note: L2 is even, so no general feat.
        req = self._request_with_plan({
            "2": {
                "class": "fighter",
                "hp_method": "fixed_half",
                "skill_ranks": {"climb": 1, "swim": 1},
                "feat_class_bonus": "improved_initiative",
            },
        })
        char = create_character(req, REGISTRY)
        sheet = compute_sheet(char, REGISTRY)
        self.assertEqual(char.level, 2)
        self.assertEqual(sheet.bab, 2)              # full BAB at L2
        self.assertEqual(sheet.saves["fort"]["base"], 3)  # good save L2
        self.assertEqual(sheet.saves["ref"]["base"], 0)   # poor save L2
        self.assertEqual(sheet.saves["will"]["base"], 0)
        # HP: L1 max 10+2 + L2 fixed_half (10/2+1)+2 = 12 + 8 = 20
        self.assertEqual(sheet.hp["total"], 20)

    def test_l5_fighter_full_progression(self):
        req = self._request_with_plan({
            "2": {
                "class": "fighter",
                "hp_method": "fixed_half",
                "skill_ranks": {"climb": 1},
                "feat_class_bonus": "dodge",
            },
            "3": {
                "class": "fighter",
                "hp_method": "fixed_half",
                "skill_ranks": {"swim": 1},
                "feat_general": "toughness",
            },
            "4": {
                "class": "fighter",
                "hp_method": "fixed_half",
                "skill_ranks": {"climb": 1},
                "ability_bump": "str",
                "feat_class_bonus": "combat_reflexes",
            },
            "5": {
                "class": "fighter",
                "hp_method": "fixed_half",
                "skill_ranks": {"climb": 1},
                "feat_general": "iron_will",
            },
        })
        char = create_character(req, REGISTRY)
        sheet = compute_sheet(char, REGISTRY)
        self.assertEqual(char.level, 5)
        self.assertEqual(sheet.bab, 5)
        self.assertEqual(sheet.saves["fort"]["base"], 4)
        self.assertEqual(sheet.saves["will"]["base"], 1)
        # Str bumps from 18 (L1) to 19 (L4 ability_bump).
        self.assertEqual(sheet.ability_scores["str"]["total"], 19)
        # Cumulative feats: power_attack, weapon_focus, cleave (L1), dodge (L2),
        # toughness (L3), combat_reflexes (L4), iron_will (L5) = 7 feats.
        self.assertGreaterEqual(len(sheet.feats), 7)
        self.assertIn("toughness", sheet.feats)
        self.assertIn("dodge", sheet.feats)
        self.assertIn("combat_reflexes", sheet.feats)
        self.assertIn("iron_will", sheet.feats)


class TestMultiLevelCombatant(unittest.TestCase):
    def test_l5_combatant_uses_full_bab(self):
        body = _basic_fighter_request_dict()
        body["level_plan"] = {
            "name": "f5",
            "target_level": 5,
            "levels": {
                str(L): {
                    "class": "fighter",
                    "hp_method": "fixed_half",
                    "skill_ranks": {},
                    "feat_general": ("toughness" if L == 3 else
                                     "iron_will" if L == 5 else None),
                    "feat_class_bonus": ("dodge" if L == 2 else
                                         "combat_reflexes" if L == 4 else None),
                    "ability_bump": ("str" if L == 4 else None),
                }
                for L in range(2, 6)
            },
        }
        req = CharacterRequest.from_dict(body)
        char = create_character(req, REGISTRY)
        c = combatant_from_character(char, REGISTRY, position=(0, 0), team="patrons")
        # BAB should be 5 at L5.
        self.assertEqual(c.bases["bab"], 5)
        # HP is L1 max + 4 levels of fixed_half. L1 = 10+2 = 12. L2-L5 each
        # = 10/2+1 + 2 = 8. Total = 12 + 32 = 44.
        self.assertEqual(c.max_hp, 44)
        # Attack uses the cumulative BAB.
        if c.attack_options:
            atk = c.attack_options[0]
            # BAB 5 + Str (now 19, mod +4) + size 0 = 9
            self.assertEqual(atk["attack_bonus"], 9)


class TestPlanValidation(unittest.TestCase):
    def test_ability_bump_required_at_l4(self):
        body = _basic_fighter_request_dict()
        body["level_plan"] = {
            "name": "missing_bump",
            "target_level": 4,
            "levels": {
                "2": {"class": "fighter", "feat_class_bonus": "dodge"},
                "3": {"class": "fighter", "feat_general": "toughness"},
                "4": {"class": "fighter"},  # no ability_bump
            },
        }
        req = CharacterRequest.from_dict(body)
        with self.assertRaises(CharacterCreationError):
            create_character(req, REGISTRY)

    def test_feat_at_even_level_rejected(self):
        body = _basic_fighter_request_dict()
        body["level_plan"] = {
            "name": "feat_at_even",
            "target_level": 2,
            "levels": {
                "2": {
                    "class": "fighter",
                    "feat_general": "toughness",  # not allowed at L2 (even)
                },
            },
        }
        req = CharacterRequest.from_dict(body)
        with self.assertRaises(CharacterCreationError):
            create_character(req, REGISTRY)

    def test_too_many_skill_ranks_at_level(self):
        body = _basic_fighter_request_dict()
        body["level_plan"] = {
            "name": "skill_overflow",
            "target_level": 2,
            "levels": {
                "2": {
                    "class": "fighter",
                    "skill_ranks": {
                        "climb": 1, "swim": 1, "intimidate": 1,
                        "ride": 1, "survival": 1, "knowledge_engineering": 1,
                    },  # 6 ranks; fighter has 2 + Int 0 + human 1 = 3 per level
                    "feat_class_bonus": "dodge",
                },
            },
        }
        req = CharacterRequest.from_dict(body)
        with self.assertRaises(CharacterCreationError):
            create_character(req, REGISTRY)


if __name__ == "__main__":
    unittest.main()
