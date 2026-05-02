"""Tests for HP/death refinements: stabilization, fast healing, regeneration."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.turn_executor import _apply_post_damage_state


REGISTRY = default_registry()


class TestStabilization(unittest.TestCase):
    def _dying_goblin(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        g.current_hp = -3
        _apply_post_damage_state(g)
        self.assertIn("dying", g.conditions)
        return g

    def test_stable_suppresses_bleed(self):
        g = self._dying_goblin()
        g.add_condition("stable")
        g.tick_round(2)
        # No bleed.
        self.assertEqual(g.current_hp, -3)

    def test_no_roller_no_stabilization_attempt(self):
        # Without roller, no stabilization → bleed continues.
        g = self._dying_goblin()
        g.tick_round(2)
        self.assertEqual(g.current_hp, -4)
        self.assertNotIn("stable", g.conditions)

    def test_stabilization_roll_can_succeed(self):
        # Goblin Con 12, +1 mod. d20 + 1 ≥ 10 means d20 ≥ 9.
        # Try seeds until we hit at least one stabilize success.
        successes = 0
        for seed in range(1, 30):
            g = self._dying_goblin()
            r = Roller(seed=seed)
            g.tick_round(2, roller=r)
            if "stable" in g.conditions:
                successes += 1
                # Stable suppresses bleed → HP unchanged from -3.
                self.assertEqual(g.current_hp, -3)
        self.assertGreater(successes, 0)

    def test_stabilization_roll_can_fail(self):
        # Conversely, ensure some seeds fail and bleed.
        failures = 0
        for seed in range(1, 30):
            g = self._dying_goblin()
            r = Roller(seed=seed)
            g.tick_round(2, roller=r)
            if "stable" not in g.conditions:
                failures += 1
                self.assertEqual(g.current_hp, -4)
        self.assertGreater(failures, 0)


class TestFastHealing(unittest.TestCase):
    def test_heals_one_per_round(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        g.fast_healing = 1
        g.current_hp = g.max_hp - 5
        before = g.current_hp
        g.tick_round(2)
        self.assertEqual(g.current_hp, before + 1)

    def test_caps_at_max_hp(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        g.fast_healing = 100
        g.current_hp = g.max_hp - 1
        g.tick_round(2)
        self.assertEqual(g.current_hp, g.max_hp)

    def test_dead_creature_does_not_heal(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        g.fast_healing = 5
        g.current_hp = -50
        g.add_condition("dead")
        g.tick_round(2)
        self.assertEqual(g.current_hp, -50)

    def test_heals_dying_creature_back_above_zero(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        g.fast_healing = 10
        g.current_hp = -3
        g.add_condition("dying")
        g.tick_round(2)
        # 1 HP loss from bleed (no roller for stabilization), then
        # +10 from fast_healing → net +9 → hp 6. (Bleed runs first.)
        self.assertEqual(g.current_hp, 6)


class TestRegeneration(unittest.TestCase):
    def test_regen_heals_each_round(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        g.regeneration = 3
        g.current_hp = g.max_hp - 5
        before = g.current_hp
        g.tick_round(2)
        self.assertEqual(g.current_hp, before + 3)


if __name__ == "__main__":
    unittest.main()
