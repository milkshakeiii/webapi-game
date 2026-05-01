"""Tests for the ferocity racial trait (orcs and similar creatures)."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.turn_executor import (
    _apply_post_damage_state,
    _has_racial_trait,
)


REGISTRY = default_registry()


def _orc(pos=(5, 5)):
    return combatant_from_monster(
        REGISTRY.get_monster("orc"), pos, "enemies",
    )


def _goblin(pos=(5, 5)):
    return combatant_from_monster(
        REGISTRY.get_monster("goblin"), pos, "enemies",
    )


# ---------------------------------------------------------------------------
# Trait detection
# ---------------------------------------------------------------------------


class TestRacialTraitDetection(unittest.TestCase):
    def test_orc_has_ferocity(self):
        orc = _orc()
        self.assertTrue(_has_racial_trait(orc, "ferocity"))

    def test_goblin_does_not_have_ferocity(self):
        goblin = _goblin()
        self.assertFalse(_has_racial_trait(goblin, "ferocity"))

    def test_unknown_trait_returns_false(self):
        orc = _orc()
        self.assertFalse(_has_racial_trait(orc, "nonsense_trait"))


# ---------------------------------------------------------------------------
# Post-damage state transitions
# ---------------------------------------------------------------------------


class TestPostDamageState(unittest.TestCase):
    def test_orc_below_zero_stays_conscious(self):
        orc = _orc()
        orc.current_hp = -3  # below 0 but above -10
        _apply_post_damage_state(orc)
        self.assertIn("ferocity_active", orc.conditions)
        self.assertIn("staggered", orc.conditions)
        self.assertNotIn("dying", orc.conditions)
        self.assertNotIn("dead", orc.conditions)

    def test_goblin_below_zero_starts_dying(self):
        goblin = _goblin()
        goblin.current_hp = -3
        _apply_post_damage_state(goblin)
        self.assertIn("dying", goblin.conditions)
        self.assertNotIn("ferocity_active", goblin.conditions)

    def test_orc_at_or_below_minus_10_dies(self):
        orc = _orc()
        orc.current_hp = -10
        _apply_post_damage_state(orc)
        self.assertIn("dead", orc.conditions)
        self.assertNotIn("ferocity_active", orc.conditions)
        self.assertNotIn("staggered", orc.conditions)

    def test_orc_killed_outright_clears_ferocity_state(self):
        # Orc was below 0 with ferocity, then a follow-up hit kills.
        orc = _orc()
        orc.current_hp = -3
        _apply_post_damage_state(orc)
        self.assertIn("ferocity_active", orc.conditions)
        # Next hit drops to -12.
        orc.current_hp = -12
        _apply_post_damage_state(orc)
        self.assertIn("dead", orc.conditions)
        self.assertNotIn("ferocity_active", orc.conditions)
        self.assertNotIn("staggered", orc.conditions)
        self.assertNotIn("dying", orc.conditions)

    def test_orc_at_zero_or_above_no_state_change(self):
        orc = _orc()
        orc.current_hp = 1
        _apply_post_damage_state(orc)
        self.assertNotIn("ferocity_active", orc.conditions)
        self.assertNotIn("dying", orc.conditions)
        self.assertNotIn("dead", orc.conditions)


# ---------------------------------------------------------------------------
# tick_round bleed
# ---------------------------------------------------------------------------


class TestFerocityBleed(unittest.TestCase):
    def test_orc_loses_one_hp_per_round_while_below_zero(self):
        orc = _orc()
        orc.current_hp = -3
        _apply_post_damage_state(orc)
        self.assertIn("ferocity_active", orc.conditions)
        # Tick a round; HP drops by 1.
        orc.tick_round(2)
        self.assertEqual(orc.current_hp, -4)
        # And again.
        orc.tick_round(3)
        self.assertEqual(orc.current_hp, -5)

    def test_bleed_eventually_kills(self):
        orc = _orc()
        orc.current_hp = -8
        _apply_post_damage_state(orc)
        self.assertIn("ferocity_active", orc.conditions)
        # 2 rounds of bleed pushes HP from -8 to -10 → dead.
        orc.tick_round(2)  # -9
        self.assertNotIn("dead", orc.conditions)
        orc.tick_round(3)  # -10 → dead
        self.assertIn("dead", orc.conditions)
        self.assertNotIn("ferocity_active", orc.conditions)
        self.assertNotIn("staggered", orc.conditions)

    def test_no_bleed_if_above_zero(self):
        # If something heals an orc back above 0, no bleed.
        orc = _orc()
        orc.current_hp = -3
        _apply_post_damage_state(orc)
        # Heal back above 0 (mid-encounter cure light wounds, etc.).
        orc.current_hp = 2
        # ferocity_active wasn't auto-cleared, but bleed only fires when
        # HP <= 0; a real implementation would clear ferocity_active
        # after healing, but for v1 the condition is sticky and just
        # doesn't bleed while HP > 0.
        orc.tick_round(2)
        self.assertEqual(orc.current_hp, 2)

    def test_non_ferocious_creature_no_bleed(self):
        # A wounded goblin (without ferocity_active) shouldn't bleed.
        goblin = _goblin()
        goblin.current_hp = 2
        goblin.tick_round(2)
        self.assertEqual(goblin.current_hp, 2)


# ---------------------------------------------------------------------------
# End-to-end: orc keeps fighting after dropping below 0
# ---------------------------------------------------------------------------


class TestFerocityInCombat(unittest.TestCase):
    def test_orc_below_zero_is_not_dying(self):
        orc = _orc(pos=(5, 5))
        # Force HP below 0 directly (simpler than building a full
        # combat sequence that produces it deterministically).
        orc.current_hp = -2
        _apply_post_damage_state(orc)
        self.assertFalse(orc.is_unconscious(),
                         "orc with ferocity should still be conscious")
        self.assertTrue(orc.is_alive())
        self.assertIn("staggered", orc.conditions)


if __name__ == "__main__":
    unittest.main()
