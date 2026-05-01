"""Tests for dnd.engine.characters."""

from __future__ import annotations

import unittest

from dnd.engine.characters import (
    ABILITY_KEYS,
    AbilityScores,
    CharacterCreationError,
    CharacterRequest,
    POINT_BUY_COSTS,
    STANDARD_ARRAY,
    ability_modifier,
    apply_racial_modifiers,
    compute_hp_l1,
    compute_saves,
    compute_sheet,
    compute_skill_points_l1,
    create_character,
    required_feat_count_l1,
    roll_ability_scores_4d6kh3,
    validate_ability_scores,
    validate_feats,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller


REGISTRY = default_registry()


def _scores(**kw) -> AbilityScores:
    base = {"str": 10, "dex": 10, "con": 10, "int": 10, "wis": 10, "cha": 10}
    base.update(kw)
    return AbilityScores.from_dict(base)


def _basic_fighter_request(**overrides) -> CharacterRequest:
    """A minimal valid fighter request (20-point buy)."""
    # 16/14/14/10/10/10 = 10+5+5+0+0+0 = 20.
    base = dict(
        name="Sir Edric",
        race="human",
        **{"class": "fighter"},
        alignment="lawful_good",
        ability_scores={
            "method": "point_buy_20",
            "scores": {
                "str": 16, "dex": 14, "con": 14,
                "int": 10, "wis": 10, "cha": 10,
            },
        },
        free_ability_choice="str",
        feats=["power_attack", "weapon_focus"],
        skill_ranks={"climb": 1, "swim": 1},
        bonus_languages=[],
        class_choices={"fighter_bonus_feat": "cleave"},
    )
    base.update(overrides)
    return CharacterRequest.from_dict(base)


# ---------------------------------------------------------------------------
# Pure helpers
# ---------------------------------------------------------------------------


class TestAbilityModifier(unittest.TestCase):
    def test_standard_modifiers(self):
        cases = [
            (1, -5), (3, -4), (5, -3), (7, -2), (9, -1),
            (10, 0), (11, 0), (12, 1), (14, 2), (16, 3),
            (18, 4), (20, 5),
        ]
        for score, expected in cases:
            self.assertEqual(ability_modifier(score), expected, score)


class TestPointBuy(unittest.TestCase):
    def test_classic_20_valid(self):
        # 16/14/14/10/10/8: +10 +5 +5 +0 +0 -2 = 18  (one over 20-budget? let's see)
        # PF1 costs: 16=10, 14=5, 14=5, 10=0, 10=0, 8=-2 -> 18 spent. Not 20.
        # Adjust to a properly-budgeted 20 array.
        # 16/14/13/12/10/8 = 10+5+3+2+0-2 = 18. Still off.
        # Let's compute a known-good 20-point spread: 16/14/14/10/10/10 = 10+5+5+0+0+0 = 20.
        s = _scores(str=16, dex=14, con=14, int=10, wis=10, cha=10)
        validate_ability_scores(s, "point_buy_20")

    def test_classic_20_off_by_one_rejected(self):
        s = _scores(str=16, dex=14, con=14, int=10, wis=10, cha=8)  # 18 spent
        with self.assertRaises(CharacterCreationError):
            validate_ability_scores(s, "point_buy_20")

    def test_score_out_of_range(self):
        s = _scores(str=19)  # > 18 illegal pre-racial
        with self.assertRaises(CharacterCreationError):
            validate_ability_scores(s, "point_buy_20")
        s = _scores(str=6)
        with self.assertRaises(CharacterCreationError):
            validate_ability_scores(s, "point_buy_20")

    def test_point_buy_table_sanity(self):
        self.assertEqual(POINT_BUY_COSTS[10], 0)
        self.assertEqual(POINT_BUY_COSTS[18], 17)
        self.assertEqual(POINT_BUY_COSTS[7], -4)


class TestStandardArray(unittest.TestCase):
    def test_valid_assignment(self):
        # Standard array is 15/14/13/12/10/8. Any permutation should pass.
        s = _scores(str=15, dex=14, con=13, int=12, wis=10, cha=8)
        validate_ability_scores(s, "standard_array")

    def test_wrong_values_rejected(self):
        s = _scores(str=18, dex=14, con=13, int=12, wis=10, cha=8)
        with self.assertRaises(CharacterCreationError):
            validate_ability_scores(s, "standard_array")


class TestRolled(unittest.TestCase):
    def test_rolled_method_passes_anything(self):
        s = _scores(str=18, dex=18, con=18, int=18, wis=18, cha=18)
        validate_ability_scores(s, "rolled_4d6kh3")

    def test_six_rolls(self):
        rolls = roll_ability_scores_4d6kh3(Roller(seed=42))
        self.assertEqual(len(rolls), 6)
        for r in rolls:
            self.assertGreaterEqual(r, 3)
            self.assertLessEqual(r, 18)


# ---------------------------------------------------------------------------
# Race & class application
# ---------------------------------------------------------------------------


class TestRacialModifiers(unittest.TestCase):
    def test_dwarf_fixed(self):
        s = _scores(str=10, dex=10, con=10, int=10, wis=10, cha=10)
        dwarf = REGISTRY.get_race("dwarf")
        out = apply_racial_modifiers(s, dwarf, None)
        self.assertEqual(out.con, 12)
        self.assertEqual(out.wis, 12)
        self.assertEqual(out.cha, 8)
        self.assertEqual(out.str_, 10)

    def test_human_free_choice(self):
        s = _scores(str=15)
        human = REGISTRY.get_race("human")
        out = apply_racial_modifiers(s, human, "str")
        self.assertEqual(out.str_, 17)
        self.assertEqual(out.dex, 10)

    def test_human_requires_choice(self):
        s = _scores()
        human = REGISTRY.get_race("human")
        with self.assertRaises(CharacterCreationError):
            apply_racial_modifiers(s, human, None)

    def test_human_invalid_choice(self):
        s = _scores()
        human = REGISTRY.get_race("human")
        with self.assertRaises(CharacterCreationError):
            apply_racial_modifiers(s, human, "luck")


class TestSavesAndHP(unittest.TestCase):
    def test_fighter_saves_with_high_con(self):
        s = _scores(con=16)
        saves = compute_saves(REGISTRY.get_class("fighter"), s)
        self.assertEqual(saves["fort"], 2 + 3)
        self.assertEqual(saves["ref"], 0)
        self.assertEqual(saves["will"], 0)

    def test_wizard_will_save(self):
        s = _scores(wis=12)
        saves = compute_saves(REGISTRY.get_class("wizard"), s)
        self.assertEqual(saves["will"], 2 + 1)

    def test_max_hp_at_l1(self):
        s = _scores(con=14)
        fighter = REGISTRY.get_class("fighter")
        self.assertEqual(compute_hp_l1(fighter, s), 10 + 2)
        wizard = REGISTRY.get_class("wizard")
        self.assertEqual(compute_hp_l1(wizard, s), 6 + 2)


class TestSkillPoints(unittest.TestCase):
    def test_fighter_minimum_with_no_int(self):
        s = _scores(int=10)
        fighter = REGISTRY.get_class("fighter")
        human = REGISTRY.get_race("human")
        # 2 base + 0 int + 1 human = 3 per level, x4 at L1 = 12
        self.assertEqual(compute_skill_points_l1(fighter, s, human), 12)

    def test_rogue_high_int(self):
        s = _scores(int=14)
        rogue = REGISTRY.get_class("rogue")
        elf = REGISTRY.get_race("elf")
        # 8 + 2 + 0 = 10/lvl, x4 = 40
        self.assertEqual(compute_skill_points_l1(rogue, s, elf), 40)

    def test_negative_int_minimum_one(self):
        s = _scores(int=8)
        wizard = REGISTRY.get_class("wizard")
        elf = REGISTRY.get_race("elf")
        # 2 base + (-1) = 1 (minimum 1), x4 = 4
        self.assertEqual(compute_skill_points_l1(wizard, s, elf), 4)


class TestRequiredFeats(unittest.TestCase):
    def test_human_has_extra_feat(self):
        human = REGISTRY.get_race("human")
        fighter = REGISTRY.get_class("fighter")
        self.assertEqual(required_feat_count_l1(fighter, human), 2)

    def test_dwarf_has_one_feat(self):
        dwarf = REGISTRY.get_race("dwarf")
        fighter = REGISTRY.get_class("fighter")
        self.assertEqual(required_feat_count_l1(fighter, dwarf), 1)


class TestFeatPrereqs(unittest.TestCase):
    def test_power_attack_str_requirement(self):
        s = _scores(str=12)  # below 13
        fighter = REGISTRY.get_class("fighter")
        with self.assertRaises(CharacterCreationError):
            validate_feats(["power_attack"], s, fighter, REGISTRY)
        # At Str 13 with BAB 1 it's fine.
        s_ok = _scores(str=13)
        validate_feats(["power_attack"], s_ok, fighter, REGISTRY)

    def test_power_attack_bab_requirement(self):
        s = _scores(str=14)
        wizard = REGISTRY.get_class("wizard")  # BAB 0
        with self.assertRaises(CharacterCreationError):
            validate_feats(["power_attack"], s, wizard, REGISTRY)

    def test_cleave_requires_power_attack_listed(self):
        s = _scores(str=14)
        fighter = REGISTRY.get_class("fighter")
        # Cleave alone (without power_attack listed) must fail.
        with self.assertRaises(CharacterCreationError):
            validate_feats(["cleave"], s, fighter, REGISTRY)
        # With power_attack also selected, OK.
        validate_feats(["power_attack", "cleave"], s, fighter, REGISTRY)

    def test_no_duplicate_feats(self):
        s = _scores(str=14)
        fighter = REGISTRY.get_class("fighter")
        with self.assertRaises(CharacterCreationError):
            validate_feats(["power_attack", "power_attack"], s, fighter, REGISTRY)

    def test_unknown_feat(self):
        s = _scores(str=14)
        fighter = REGISTRY.get_class("fighter")
        with self.assertRaises(Exception):
            validate_feats(["nonexistent_feat"], s, fighter, REGISTRY)


# ---------------------------------------------------------------------------
# Full-stack tests
# ---------------------------------------------------------------------------


class TestCreateFighter(unittest.TestCase):
    def test_basic_human_fighter(self):
        req = _basic_fighter_request()
        char = create_character(req, REGISTRY)
        self.assertEqual(char.race_id, "human")
        self.assertEqual(char.class_id, "fighter")
        self.assertEqual(char.level, 1)
        self.assertEqual(char.alignment, "lawful_good")
        # Inputs preserved on the Character.
        self.assertEqual(char.base_ability_scores.str_, 16)
        # Derived stats live on the sheet.
        sheet = compute_sheet(char, REGISTRY)
        self.assertEqual(sheet.ability_scores["str"]["total"], 18)  # 16 + 2 human
        self.assertEqual(sheet.hp["total"], 12)         # 10 HD + 2 Con mod
        self.assertEqual(sheet.bab, 1)
        self.assertEqual(sheet.saves["fort"]["total"], 4)  # 2 + 2 Con
        self.assertEqual(sheet.saves["ref"]["total"], 2)   # 0 + 2 Dex
        self.assertEqual(sheet.saves["will"]["total"], 0)
        # Two feats picked (human gets +1) plus class bonus (cleave).
        self.assertIn("power_attack", char.feats)
        self.assertIn("weapon_focus", char.feats)
        self.assertIn("cleave", char.feats)
        self.assertEqual(len(char.feats), 3)
        # Skills: climb and swim each gain +3 class skill bonus + Str mod.
        climb = sheet.skills["climb"]
        self.assertEqual(climb["total"], 1 + 4 + 3)  # rank + Str mod + class skill
        self.assertEqual(climb["base"], 0)

    def test_to_dict_serialization(self):
        char = create_character(_basic_fighter_request(), REGISTRY)
        sheet = compute_sheet(char, REGISTRY)
        d = sheet.to_dict()
        self.assertEqual(d["class_id"], "fighter")
        self.assertEqual(d["ability_scores"]["str"]["total"], 18)
        self.assertEqual(d["base_ability_scores"]["str"], 16)
        self.assertEqual(d["hp"]["total"], 12)
        self.assertEqual(d["saves"]["fort"]["total"], 4)
        # Modifier breakdown is exposed.
        self.assertGreaterEqual(len(d["saves"]["fort"]["modifiers"]), 1)


class TestCreateOtherClasses(unittest.TestCase):
    def test_wizard_minimal(self):
        # 8/14/14/16/12/10 = -2+5+5+10+2+0 = 20.
        req = CharacterRequest.from_dict({
            "name": "Aurelia",
            "race": "elf",
            "class": "wizard",
            "alignment": "true_neutral",
            "ability_scores": {
                "method": "point_buy_20",
                "scores": {
                    "str": 8, "dex": 14, "con": 14,
                    "int": 16, "wis": 12, "cha": 10,
                },
            },
            "feats": ["combat_expertise"],
            "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
            "bonus_languages": [],
        })
        char = create_character(req, REGISTRY)
        sheet = compute_sheet(char, REGISTRY)
        self.assertEqual(char.class_id, "wizard")
        self.assertEqual(sheet.ability_scores["dex"]["total"], 16)   # 14 + 2 elf
        self.assertEqual(sheet.ability_scores["int"]["total"], 18)   # 16 + 2 elf
        self.assertEqual(sheet.ability_scores["con"]["total"], 12)   # 14 - 2 elf
        # Wizard auto-grants Scribe Scroll.
        self.assertIn("scribe_scroll", char.feats)
        self.assertEqual(len(char.feats), 2)
        # Spells: 3 cantrips/day, 1 first level + 1 from Int 18 (bonus spells).
        self.assertEqual(sheet.spells_per_day["0"], 3)
        self.assertEqual(sheet.spells_per_day["1"], 1 + 1)

    def test_paladin_alignment_strict(self):
        # Paladin requires LG. Try with NG.
        req = CharacterRequest.from_dict({
            "name": "Sir Wrong",
            "race": "human",
            "class": "paladin",
            "alignment": "neutral_good",
            "ability_scores": {
                "method": "point_buy_20",
                "scores": {
                    "str": 16, "dex": 12, "con": 14,
                    "int": 10, "wis": 10, "cha": 14,
                },
            },
            "free_ability_choice": "cha",
            "feats": ["power_attack", "weapon_focus"],
            "skill_ranks": {"diplomacy": 1, "ride": 1},
            "bonus_languages": [],
        })
        with self.assertRaises(CharacterCreationError):
            create_character(req, REGISTRY)

    def test_paladin_lawful_good_passes(self):
        # 16/12/14/10/10/13 = 10+2+5+0+0+3 = 20.
        req = CharacterRequest.from_dict({
            "name": "Sir Honest",
            "race": "human",
            "class": "paladin",
            "alignment": "lawful_good",
            "ability_scores": {
                "method": "point_buy_20",
                "scores": {
                    "str": 16, "dex": 12, "con": 14,
                    "int": 10, "wis": 10, "cha": 13,
                },
            },
            "free_ability_choice": "cha",
            "feats": ["power_attack", "weapon_focus"],
            "skill_ranks": {"diplomacy": 1, "ride": 1},
            "bonus_languages": [],
        })
        char = create_character(req, REGISTRY)
        sheet = compute_sheet(char, REGISTRY)
        self.assertEqual(char.class_id, "paladin")
        self.assertEqual(sheet.ability_scores["cha"]["total"], 15)  # 13 + 2 human

    def test_monk_lawful(self):
        # Monk must be lawful — try with chaotic.
        # 14/14/14/10/14/10 = 5+5+5+0+5+0 = 20.
        req = CharacterRequest.from_dict({
            "name": "Wrong Monk",
            "race": "human",
            "class": "monk",
            "alignment": "chaotic_good",
            "ability_scores": {
                "method": "point_buy_20",
                "scores": {
                    "str": 14, "dex": 14, "con": 14,
                    "int": 10, "wis": 14, "cha": 10,
                },
            },
            "free_ability_choice": "wis",
            "feats": ["combat_reflexes", "improved_initiative"],
            "skill_ranks": {"acrobatics": 1, "perception": 1},
            "bonus_languages": [],
            "class_choices": {"monk_bonus_feat": "dodge"},
        })
        with self.assertRaises(CharacterCreationError):
            create_character(req, REGISTRY)

    def test_barbarian_no_lawful(self):
        # Barbarian must be non-lawful — try LG.
        # 16/14/14/10/10/10 = 10+5+5+0+0+0 = 20.
        req = CharacterRequest.from_dict({
            "name": "Wrong Rage",
            "race": "human",
            "class": "barbarian",
            "alignment": "lawful_good",
            "ability_scores": {
                "method": "point_buy_20",
                "scores": {
                    "str": 16, "dex": 14, "con": 14,
                    "int": 10, "wis": 10, "cha": 10,
                },
            },
            "free_ability_choice": "str",
            "feats": ["power_attack", "weapon_focus"],
            "skill_ranks": {"climb": 1, "perception": 1},
            "bonus_languages": [],
        })
        with self.assertRaises(CharacterCreationError):
            create_character(req, REGISTRY)


class TestErrorPaths(unittest.TestCase):
    def test_unknown_race(self):
        req = _basic_fighter_request(race="tiefling")
        with self.assertRaises(Exception):
            create_character(req, REGISTRY)

    def test_too_many_skill_ranks(self):
        # Dwarf fighter with Int 10 has (2+0)*4 = 8 ranks at L1.
        # 14/12/14/10/14/13 = 5+2+5+0+5+3 = 20.
        req = _basic_fighter_request(
            race="dwarf",
            free_ability_choice=None,
            ability_scores={
                "method": "point_buy_20",
                "scores": {
                    "str": 14, "dex": 12, "con": 14,
                    "int": 10, "wis": 14, "cha": 13,
                },
            },
            feats=["power_attack"],  # 1 feat (no human bonus)
            skill_ranks={
                "climb": 1, "swim": 1, "intimidate": 1, "ride": 1,
                "survival": 1, "craft": 1, "profession": 1,
                "knowledge_dungeoneering": 1, "knowledge_engineering": 1,
            },
        )
        with self.assertRaises(CharacterCreationError):
            create_character(req, REGISTRY)

    def test_more_than_one_rank_at_l1(self):
        req = _basic_fighter_request(skill_ranks={"climb": 2})
        with self.assertRaises(CharacterCreationError):
            create_character(req, REGISTRY)

    def test_wrong_feat_count_too_few(self):
        # Human fighter expects 2 chosen feats; only give 1.
        req = _basic_fighter_request(feats=["power_attack"])
        with self.assertRaises(CharacterCreationError):
            create_character(req, REGISTRY)

    def test_wrong_feat_count_too_many(self):
        req = _basic_fighter_request(
            feats=["power_attack", "weapon_focus", "improved_initiative"]
        )
        with self.assertRaises(CharacterCreationError):
            create_character(req, REGISTRY)

    def test_fighter_without_class_choice(self):
        req_dict = {
            "name": "FlawedFighter",
            "race": "human",
            "class": "fighter",
            "alignment": "lawful_good",
            "ability_scores": {
                "method": "point_buy_20",
                "scores": {
                    "str": 16, "dex": 14, "con": 14,
                    "int": 10, "wis": 10, "cha": 10,
                },
            },
            "free_ability_choice": "str",
            "feats": ["power_attack", "weapon_focus"],
            "skill_ranks": {"climb": 1, "swim": 1},
            "bonus_languages": [],
            # no class_choices
        }
        req = CharacterRequest.from_dict(req_dict)
        with self.assertRaises(CharacterCreationError):
            create_character(req, REGISTRY)


if __name__ == "__main__":
    unittest.main()
