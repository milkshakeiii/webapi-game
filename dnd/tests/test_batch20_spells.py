"""Tests for batch 20: Silence, Color Spray, Cause Fear."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.spells import cast_spell


REGISTRY = default_registry()


class TestSilence(unittest.TestCase):
    def test_silence_applies_silenced_on_failed_save(self):
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (1, 0), "y")
        target.bases["will_save"] = -100  # ensure save fails
        spell = REGISTRY.get_spell("silence")
        cast_spell(caster, spell, [target], 2, REGISTRY,
                   Roller(seed=1), current_round=1)
        self.assertIn("silenced", target.conditions)

    def test_silence_will_save_negates(self):
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (1, 0), "y")
        # Boost target's save so they pass.
        target.bases["will_save"] = 100
        spell = REGISTRY.get_spell("silence")
        cast_spell(caster, spell, [target], 2, REGISTRY,
                   Roller(seed=1), current_round=1)
        self.assertNotIn("silenced", target.conditions)


class TestColorSpray(unittest.TestCase):
    def test_low_hd_target_gets_full_effect_on_failed_save(self):
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (1, 0), "y")
        target.bases["will_save"] = -100
        # Goblin: 1d6 HD → 1 HD → "≤2" tier.
        spell = REGISTRY.get_spell("color_spray")
        cast_spell(caster, spell, [target], 1, REGISTRY,
                   Roller(seed=1), current_round=1)
        self.assertIn("unconscious", target.conditions)
        self.assertIn("blinded", target.conditions)
        self.assertIn("stunned", target.conditions)

    def test_high_hd_target_only_stunned(self):
        # Use a fake high-HD target by overriding hit_dice.
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (1, 0), "y")
        # Hack: set the template's hit_dice to "8d8".
        target.template.hit_dice = "8d8"
        target.bases["will_save"] = -100
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        spell = REGISTRY.get_spell("color_spray")
        cast_spell(caster, spell, [target], 1, REGISTRY,
                   Roller(seed=1), current_round=1)
        self.assertIn("stunned", target.conditions)
        self.assertNotIn("unconscious", target.conditions)
        self.assertNotIn("blinded", target.conditions)

    def test_will_save_negates(self):
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (1, 0), "y")
        target.bases["will_save"] = 100
        spell = REGISTRY.get_spell("color_spray")
        cast_spell(caster, spell, [target], 1, REGISTRY,
                   Roller(seed=1), current_round=1)
        self.assertNotIn("unconscious", target.conditions)
        self.assertNotIn("stunned", target.conditions)


class TestCauseFear(unittest.TestCase):
    def test_failed_save_applies_frightened(self):
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (1, 0), "y")
        target.bases["will_save"] = -100
        spell = REGISTRY.get_spell("cause_fear")
        cast_spell(caster, spell, [target], 1, REGISTRY,
                   Roller(seed=1), current_round=1)
        self.assertIn("frightened", target.conditions)
        self.assertNotIn("shaken", target.conditions)

    def test_passing_save_applies_shaken(self):
        # Save partial: successful save still applies the lesser
        # (shaken) condition. We need a save that passes — boost the
        # save bonus high.
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (1, 0), "y")
        target.bases["will_save"] = 100
        spell = REGISTRY.get_spell("cause_fear")
        cast_spell(caster, spell, [target], 1, REGISTRY,
                   Roller(seed=1), current_round=1)
        self.assertIn("shaken", target.conditions)
        self.assertNotIn("frightened", target.conditions)


if __name__ == "__main__":
    unittest.main()
