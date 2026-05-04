"""Tests for Phase 2.1 easy monster racial traits — channel_resistance,
ooze_traits, cold_immunity, displacement, resistance_save, light_sensitivity."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.modifiers import compute_with_context
from dnd.engine.spells import apply_typed_damage, roll_save


REGISTRY = default_registry()


# ---------------------------------------------------------------------------
# Channel resistance (ghoul)
# ---------------------------------------------------------------------------


class TestChannelResistance(unittest.TestCase):
    def test_ghoul_save_includes_channel_resistance_only_in_channel_context(self):
        ghoul = combatant_from_monster(REGISTRY.get_monster("ghoul"),
                                       (0, 0), "x")
        # Plain Will save: no channel context → ghoul's natural Will only.
        plain = compute_with_context(
            ghoul.bases.get("will_save", 0),
            ghoul.modifiers.for_target("will_save"),
            {},
        )
        # Will save vs channel energy: +2 from channel_resistance_2 trait.
        with_channel = compute_with_context(
            ghoul.bases.get("will_save", 0),
            ghoul.modifiers.for_target("will_save"),
            {"effect_type": "channel_energy"},
        )
        self.assertEqual(with_channel - plain, 2)


# ---------------------------------------------------------------------------
# Cold immunity (skeleton)
# ---------------------------------------------------------------------------


class TestColdImmunity(unittest.TestCase):
    def test_skeleton_immune_to_cold_damage(self):
        sk = combatant_from_monster(REGISTRY.get_monster("skeleton"),
                                    (0, 0), "x")
        applied, note = apply_typed_damage(sk, 50, "cold")
        self.assertEqual(applied, 0)
        self.assertEqual(note, "immune")

    def test_skeleton_still_takes_fire_damage(self):
        sk = combatant_from_monster(REGISTRY.get_monster("skeleton"),
                                    (0, 0), "x")
        hp_before = sk.current_hp
        apply_typed_damage(sk, 5, "fire")
        self.assertEqual(sk.current_hp, hp_before - 5)


# ---------------------------------------------------------------------------
# Displacement (displacer beast)
# ---------------------------------------------------------------------------


class TestDisplacement(unittest.TestCase):
    def test_displacer_beast_has_concealment_50(self):
        db = combatant_from_monster(REGISTRY.get_monster("displacer_beast"),
                                    (0, 0), "x")
        self.assertEqual(db.concealment, 50)


# ---------------------------------------------------------------------------
# Resistance save (displacer beast)
# ---------------------------------------------------------------------------


class TestResistanceSave(unittest.TestCase):
    def test_displacer_beast_save_includes_plus_two_vs_spells(self):
        db = combatant_from_monster(REGISTRY.get_monster("displacer_beast"),
                                    (0, 0), "x")
        plain = compute_with_context(
            db.bases.get("will_save", 0),
            db.modifiers.for_target("will_save"),
            {},
        )
        vs_spell = compute_with_context(
            db.bases.get("will_save", 0),
            db.modifiers.for_target("will_save"),
            {"effect_tags": ["spell"]},
        )
        self.assertEqual(vs_spell - plain, 2)


# ---------------------------------------------------------------------------
# Ooze traits (gelatinous cube)
# ---------------------------------------------------------------------------


class TestOozeTraits(unittest.TestCase):
    def test_gel_cube_immune_to_mind_affecting_set(self):
        cube = combatant_from_monster(REGISTRY.get_monster("gelatinous_cube"),
                                      (0, 0), "x")
        for cond in ("charmed", "fascinated", "shaken", "frightened",
                     "panicked", "dazed", "confused", "sleeping",
                     "paralyzed", "stunned", "fatigued", "exhausted",
                     "nauseated", "sickened"):
            self.assertIn(cond, cube.condition_immunities,
                          f"gel cube should be immune to {cond}")

    def test_gel_cube_apply_charm_returns_false(self):
        cube = combatant_from_monster(REGISTRY.get_monster("gelatinous_cube"),
                                      (0, 0), "x")
        result = cube.add_condition("charmed")
        self.assertFalse(result)
        self.assertNotIn("charmed", cube.conditions)


# ---------------------------------------------------------------------------
# Light sensitivity (kobold, orc)
# ---------------------------------------------------------------------------


class TestLightSensitivity(unittest.TestCase):
    def test_kobold_in_bright_light_becomes_dazzled(self):
        k = combatant_from_monster(REGISTRY.get_monster("kobold"), (0, 0), "x")
        self.assertNotIn("dazzled", k.conditions)
        k.in_bright_light = True
        k.update_light_sensitivity_state()
        self.assertIn("dazzled", k.conditions)

    def test_kobold_leaving_bright_light_clears_dazzled(self):
        k = combatant_from_monster(REGISTRY.get_monster("kobold"), (0, 0), "x")
        k.in_bright_light = True
        k.update_light_sensitivity_state()
        self.assertIn("dazzled", k.conditions)
        k.in_bright_light = False
        k.update_light_sensitivity_state()
        self.assertNotIn("dazzled", k.conditions)

    def test_orc_uses_same_plumbing(self):
        o = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        o.in_bright_light = True
        o.update_light_sensitivity_state()
        self.assertIn("dazzled", o.conditions)

    def test_non_sensitive_creature_unchanged(self):
        # Goblin has no light_sensitivity — flag flip is a no-op.
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        g.in_bright_light = True
        g.update_light_sensitivity_state()
        self.assertNotIn("dazzled", g.conditions)


# ---------------------------------------------------------------------------
# Stalker (bugbear) — verifies skill totals as a sanity check
# ---------------------------------------------------------------------------


class TestStalkerBugbear(unittest.TestCase):
    def test_bugbear_skills_already_include_class_skill_bonus(self):
        b = combatant_from_monster(REGISTRY.get_monster("bugbear"),
                                   (0, 0), "x")
        # JSON has stealth=8, perception=5; the +3 class-skill bonus
        # is baked in. Just verify the totals are exposed.
        self.assertEqual(b.skill_total("stealth"), 8)
        self.assertEqual(b.skill_total("perception"), 5)


if __name__ == "__main__":
    unittest.main()
