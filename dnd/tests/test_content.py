"""Tests for dnd.engine.content."""

from __future__ import annotations

import unittest

from dnd.engine.content import (
    ContentNotFoundError,
    ContentRegistry,
    default_registry,
)


class TestDefaultRegistry(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reg = default_registry()

    def test_seven_core_races_loaded(self):
        ids = {r.id for r in self.reg.all_races()}
        expected = {"human", "dwarf", "elf", "gnome", "half_elf",
                    "half_orc", "halfling"}
        self.assertEqual(ids, expected)

    def test_eleven_base_classes_loaded(self):
        ids = {c.id for c in self.reg.all_classes()}
        expected = {"barbarian", "bard", "cleric", "druid", "fighter",
                    "monk", "paladin", "ranger", "rogue", "sorcerer", "wizard"}
        self.assertEqual(ids, expected)

    def test_skills_loaded(self):
        skill_ids = {s.id for s in self.reg.all_skills()}
        # Spot-check: must include both ability-tagged and Knowledge skills.
        self.assertIn("acrobatics", skill_ids)
        self.assertIn("knowledge_arcana", skill_ids)
        self.assertIn("use_magic_device", skill_ids)
        self.assertGreaterEqual(len(skill_ids), 30)

    def test_feats_loaded(self):
        feat_ids = {f.id for f in self.reg.all_feats()}
        self.assertIn("power_attack", feat_ids)
        self.assertIn("dodge", feat_ids)
        self.assertIn("weapon_focus", feat_ids)

    def test_conditions_loaded(self):
        cond_ids = {c.id for c in self.reg.all_conditions()}
        self.assertIn("blinded", cond_ids)
        self.assertIn("flat_footed", cond_ids)
        self.assertIn("prone", cond_ids)
        self.assertGreaterEqual(len(cond_ids), 30)


class TestRaceData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reg = default_registry()

    def test_human_has_free_choice_bonus(self):
        human = self.reg.get_race("human")
        self.assertEqual(human.ability_modifiers, {})
        self.assertIsNotNone(human.ability_modifier_choice)
        self.assertEqual(human.ability_modifier_choice["bonus"], 2)
        self.assertEqual(human.speed, 30)
        self.assertEqual(human.size, "medium")

    def test_dwarf_has_fixed_modifiers(self):
        dwarf = self.reg.get_race("dwarf")
        self.assertEqual(dwarf.ability_modifiers["con"], 2)
        self.assertEqual(dwarf.ability_modifiers["wis"], 2)
        self.assertEqual(dwarf.ability_modifiers["cha"], -2)
        self.assertIsNone(dwarf.ability_modifier_choice)
        self.assertEqual(dwarf.speed, 20)

    def test_halfling_is_small(self):
        halfling = self.reg.get_race("halfling")
        self.assertEqual(halfling.size, "small")
        self.assertEqual(halfling.speed, 20)


class TestClassData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reg = default_registry()

    def test_fighter_full_bab(self):
        fighter = self.reg.get_class("fighter")
        self.assertEqual(fighter.hit_die, 10)
        self.assertEqual(fighter.level_1.bab, 1)
        self.assertEqual(fighter.level_1.saves["fort"], 2)
        self.assertEqual(fighter.level_1.saves["ref"], 0)
        self.assertEqual(fighter.level_1.saves["will"], 0)
        self.assertIsNone(fighter.spell_progression)

    def test_wizard_d6_hd_and_spell_progression(self):
        wizard = self.reg.get_class("wizard")
        self.assertEqual(wizard.hit_die, 6)
        self.assertEqual(wizard.level_1.bab, 0)
        self.assertEqual(wizard.level_1.saves["will"], 2)
        self.assertIsNotNone(wizard.spell_progression)
        self.assertEqual(wizard.spell_progression["type"], "prepared")
        self.assertEqual(wizard.spell_progression["key_ability"], "int")

    def test_monk_all_good_saves(self):
        monk = self.reg.get_class("monk")
        self.assertEqual(monk.level_1.saves["fort"], 2)
        self.assertEqual(monk.level_1.saves["ref"], 2)
        self.assertEqual(monk.level_1.saves["will"], 2)

    def test_paladin_alignment_restriction(self):
        pal = self.reg.get_class("paladin")
        self.assertEqual(pal.alignment_restriction, "lawful_good")

    def test_rogue_high_skill_points(self):
        rogue = self.reg.get_class("rogue")
        self.assertEqual(rogue.level_1.skill_points_per_level, 8)

    def test_sorcerer_spontaneous(self):
        sorc = self.reg.get_class("sorcerer")
        self.assertEqual(sorc.spell_progression["type"], "spontaneous")
        self.assertEqual(sorc.spell_progression["key_ability"], "cha")


class TestSkillData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reg = default_registry()

    def test_climb_is_armor_check_skill(self):
        climb = self.reg.get_skill("climb")
        self.assertTrue(climb.armor_check_penalty)
        self.assertEqual(climb.ability, "str")

    def test_disable_device_trained_only(self):
        skill = self.reg.get_skill("disable_device")
        self.assertTrue(skill.trained_only)
        self.assertTrue(skill.armor_check_penalty)


class TestFeatData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reg = default_registry()

    def test_power_attack_prereqs(self):
        pa = self.reg.get_feat("power_attack")
        self.assertEqual(pa.type, "combat")
        self.assertEqual(pa.prerequisites["abilities"]["str"], 13)
        self.assertEqual(pa.prerequisites["bab"], 1)

    def test_cleave_requires_power_attack(self):
        cleave = self.reg.get_feat("cleave")
        self.assertIn("power_attack", cleave.prerequisites["feats"])

    def test_skill_focus_has_subtype(self):
        sf = self.reg.get_feat("skill_focus")
        self.assertEqual(sf.subtype, "skill")


class TestMonsterData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reg = default_registry()

    def test_monsters_loaded(self):
        ids = {m.id for m in self.reg.all_monsters()}
        self.assertGreaterEqual(len(ids), 6)
        for required in ("goblin", "kobold", "wolf", "orc", "skeleton"):
            self.assertIn(required, ids)

    def test_goblin_stats(self):
        g = self.reg.get_monster("goblin")
        self.assertEqual(g.size, "small")
        self.assertEqual(g.cr, "1/3")
        self.assertEqual(g.ac["total"], 16)
        self.assertEqual(g.hp, 6)
        # Has at least a melee and a ranged option.
        types = {a["type"] for a in g.attacks}
        self.assertIn("melee", types)
        self.assertIn("ranged", types)

    def test_zombie_staggered_by_default(self):
        z = self.reg.get_monster("human_zombie")
        self.assertIn("staggered", z.permanent_conditions)

    def test_skeleton_is_undead(self):
        s = self.reg.get_monster("skeleton")
        self.assertEqual(s.type, "undead")
        self.assertEqual(s.ability_scores["con"], 0)


class TestLookupErrors(unittest.TestCase):
    def setUp(self) -> None:
        self.reg = default_registry()

    def test_unknown_race(self):
        with self.assertRaises(ContentNotFoundError):
            self.reg.get_race("tiefling")

    def test_unknown_class(self):
        with self.assertRaises(ContentNotFoundError):
            self.reg.get_class("oracle")

    def test_unknown_feat(self):
        with self.assertRaises(ContentNotFoundError):
            self.reg.get_feat("unknown_feat_xyz")


class TestEmptyRegistry(unittest.TestCase):
    def test_empty_registry_has_no_content(self):
        empty = ContentRegistry()
        self.assertEqual(list(empty.all_races()), [])
        self.assertEqual(list(empty.all_classes()), [])

    def test_directory_must_exist(self):
        with self.assertRaises(FileNotFoundError):
            ContentRegistry.from_directory("/nonexistent/path/zzz")


if __name__ == "__main__":
    unittest.main()
