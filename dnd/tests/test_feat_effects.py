"""Tests for feat & racial passive modifier wiring."""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import combatant_from_character
from dnd.engine.content import default_registry
from dnd.engine.feat_effects import feat_modifiers
from dnd.engine.racial_effects import racial_modifiers


REGISTRY = default_registry()


def _request(**overrides):
    # Default class_choices uses "alertness" — no prereqs and unlikely
    # to clash with feat-effect tests.
    base = {
        "name": "Test Hero", "race": "human", "class": "fighter",
        "alignment": "lawful_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 16, "dex": 14, "con": 14,
                       "int": 10, "wis": 10, "cha": 10}},
        "free_ability_choice": "str",
        "feats": ["power_attack", "weapon_focus"],
        "skill_ranks": {"climb": 1, "swim": 1},
        "bonus_languages": [],
        "class_choices": {"fighter_bonus_feat": "alertness"},
    }
    base.update(overrides)
    return CharacterRequest.from_dict(base)


def _build(**overrides):
    char = create_character(_request(**overrides), REGISTRY)
    return combatant_from_character(char, REGISTRY, position=(0, 0), team="x")


# ---------------------------------------------------------------------------
# feat_modifiers (unit-level)
# ---------------------------------------------------------------------------


class TestFeatModifiersDirect(unittest.TestCase):
    def _char_stub(self, **fields):
        class S:
            pass
        s = S()
        for k, v in fields.items():
            setattr(s, k, v)
        return s

    def test_iron_will(self):
        mods = feat_modifiers("iron_will", self._char_stub())
        self.assertEqual(len(mods), 1)
        self.assertEqual(mods[0].value, 2)
        self.assertEqual(mods[0].target, "will_save")

    def test_great_fortitude(self):
        mods = feat_modifiers("great_fortitude", self._char_stub())
        self.assertEqual(mods[0].target, "fort_save")

    def test_lightning_reflexes(self):
        mods = feat_modifiers("lightning_reflexes", self._char_stub())
        self.assertEqual(mods[0].target, "ref_save")

    def test_improved_initiative(self):
        mods = feat_modifiers("improved_initiative", self._char_stub())
        self.assertEqual(mods[0].value, 4)
        self.assertEqual(mods[0].target, "initiative")

    def test_toughness_at_l1(self):
        mods = feat_modifiers("toughness", self._char_stub(level=1))
        self.assertEqual(mods[0].value, 3)
        self.assertEqual(mods[0].target, "hp_max")

    def test_toughness_at_l5(self):
        mods = feat_modifiers("toughness", self._char_stub(level=5))
        self.assertEqual(mods[0].value, 5)

    def test_dodge(self):
        mods = feat_modifiers("dodge", self._char_stub())
        self.assertEqual(mods[0].value, 1)
        self.assertEqual(mods[0].type, "dodge")
        self.assertEqual(mods[0].target, "ac")

    def test_alertness_pair(self):
        mods = feat_modifiers("alertness", self._char_stub())
        targets = {m.target for m in mods}
        self.assertEqual(targets, {"skill:perception", "skill:sense_motive"})

    def test_skill_focus_perception(self):
        mods = feat_modifiers("skill_focus_perception", self._char_stub())
        self.assertEqual(mods[0].value, 3)
        self.assertEqual(mods[0].target, "skill:perception")

    def test_weapon_focus_with_weapon_picked(self):
        mods = feat_modifiers("weapon_focus_longsword", self._char_stub())
        self.assertEqual(mods[0].value, 1)
        self.assertEqual(mods[0].target, "attack:weapon:longsword")

    def test_weapon_focus_generic_uses_equipped(self):
        mods = feat_modifiers(
            "weapon_focus", self._char_stub(equipped_weapon="greatsword"),
        )
        self.assertEqual(mods[0].target, "attack:weapon:greatsword")

    def test_unknown_feat_no_modifiers(self):
        self.assertEqual(feat_modifiers("nonexistent_feat", self._char_stub()), [])


# ---------------------------------------------------------------------------
# Racial modifiers (unit-level)
# ---------------------------------------------------------------------------


class TestRacialModifiers(unittest.TestCase):
    def test_halfling_all_saves(self):
        race = REGISTRY.get_race("halfling")
        mods = racial_modifiers(race)
        save_mods = [m for m in mods if m.target.endswith("_save")
                     and m.source.endswith("halfling_luck")]
        self.assertEqual(len(save_mods), 3)
        self.assertTrue(all(m.value == 1 and m.type == "racial" for m in save_mods))

    def test_halfling_sure_footed(self):
        race = REGISTRY.get_race("halfling")
        mods = racial_modifiers(race)
        targets = {m.target for m in mods if "sure_footed" in m.source}
        self.assertEqual(targets, {"skill:acrobatics", "skill:climb"})

    def test_half_orc_intimidating(self):
        race = REGISTRY.get_race("half_orc")
        mods = racial_modifiers(race)
        intim = [m for m in mods if m.target == "skill:intimidate"]
        self.assertEqual(len(intim), 1)
        self.assertEqual(intim[0].value, 2)

    def test_elf_keen_senses(self):
        race = REGISTRY.get_race("elf")
        mods = racial_modifiers(race)
        perc = [m for m in mods if m.target == "skill:perception"]
        self.assertEqual(len(perc), 1)
        self.assertEqual(perc[0].value, 2)

    def test_human_no_passive_mods(self):
        race = REGISTRY.get_race("human")
        self.assertEqual(racial_modifiers(race), [])


# ---------------------------------------------------------------------------
# End-to-end: Combatant reflects feats and racial traits
# ---------------------------------------------------------------------------


class TestCombatantWithFeats(unittest.TestCase):
    def test_iron_will_raises_will_save(self):
        c = _build(feats=["power_attack", "iron_will"])
        # Fighter Will base = 0 (poor), Wis 10 → +0; iron_will +2 = 2.
        self.assertEqual(c.save("will"), 2)

    def test_toughness_raises_hp(self):
        # Without toughness: fighter L1 with Con 14 = 10 + 2 = 12 HP.
        c_without = _build(feats=["power_attack", "weapon_focus"])
        c_with = _build(feats=["toughness", "weapon_focus"])
        self.assertEqual(c_with.max_hp - c_without.max_hp, 3)

    def test_dodge_raises_ac(self):
        c_with = _build(feats=["dodge", "weapon_focus"])
        c_without = _build(feats=["power_attack", "weapon_focus"])
        self.assertEqual(c_with.ac() - c_without.ac(), 1)

    def test_improved_initiative_raises_init(self):
        c = _build(feats=["improved_initiative", "weapon_focus"])
        # Fighter with Dex 14 → +2 Dex init. +4 from feat. Total +6.
        self.assertEqual(c.initiative_modifier(), 6)

    def test_skill_focus_perception(self):
        # Fighter has 0 ranks in perception by default. Override the
        # default fighter bonus feat to avoid alertness's +2 perception.
        c = _build(feats=["power_attack", "skill_focus_perception"],
                   skill_ranks={"perception": 1, "swim": 1},
                   class_choices={"fighter_bonus_feat": "improved_initiative"})
        # 1 rank + 0 Wis + 3 skill_focus = 4. Perception isn't a fighter
        # class skill so no class-skill bonus.
        self.assertEqual(c.skill_total("perception"), 4)


class TestCombatantWithRacialTraits(unittest.TestCase):
    def test_halfling_perception_includes_keen(self):
        # Halfling rogue with 0 ranks perception. Gets 2 from keen senses
        # via racial trait. Plus Wis 12 mod +1 = 3.
        req = CharacterRequest.from_dict({
            "name": "Pim", "race": "halfling", "class": "rogue",
            "alignment": "chaotic_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 10, "dex": 14, "con": 14,
                           "int": 13, "wis": 12, "cha": 14}},
            "feats": ["weapon_finesse"],
            "skill_ranks": {"perception": 1, "stealth": 1, "acrobatics": 1},
            "bonus_languages": ["elven"],
        })
        char = create_character(req, REGISTRY)
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        # 1 rank + Wis +1 + class skill +3 + halfling keen +2 = 7
        self.assertEqual(c.skill_total("perception"), 7)

    def test_halfling_save_bonus(self):
        req = CharacterRequest.from_dict({
            "name": "Pim", "race": "halfling", "class": "rogue",
            "alignment": "chaotic_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 10, "dex": 14, "con": 14,
                           "int": 13, "wis": 12, "cha": 14}},
            "feats": ["weapon_finesse"],
            "skill_ranks": {"perception": 1, "stealth": 1},
            "bonus_languages": ["elven"],
        })
        char = create_character(req, REGISTRY)
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        # Rogue Will base = 0; Wis +1; Halfling Luck +1; total 2.
        self.assertEqual(c.save("will"), 2)
        # Fort base = 0 (poor); Con 14 → +2; Halfling +1; total 3.
        self.assertEqual(c.save("fort"), 3)

    def test_half_orc_intimidate_bonus(self):
        # Half-orc rogue with 1 rank in intimidate as a class skill.
        # 14/14/14/13/10/12 = 5+5+5+3+0+2 = 20.
        req = CharacterRequest.from_dict({
            "name": "Grok", "race": "half_orc", "class": "rogue",
            "alignment": "chaotic_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 14, "con": 14,
                           "int": 13, "wis": 10, "cha": 12}},
            "free_ability_choice": "str",
            "feats": ["weapon_finesse"],
            "skill_ranks": {"intimidate": 1, "stealth": 1},
            "bonus_languages": [],
        })
        char = create_character(req, REGISTRY)
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        # 1 rank + Cha +1 + class skill +3 + half-orc +2 = 7
        self.assertEqual(c.skill_total("intimidate"), 7)


if __name__ == "__main__":
    unittest.main()
