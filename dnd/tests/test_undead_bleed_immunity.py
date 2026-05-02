"""Tests for undead/construct immunity to bleed effects.

PF1 RAW: undead and constructs ignore all bleed effects. The engine
applies this guard in Combatant.tick_round so future bleed sources
(ferocity, dying-bleed, weapon enchantments) all respect it.
"""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry


REGISTRY = default_registry()


class TestBleedImmunityFlag(unittest.TestCase):
    def test_skeleton_is_immune(self):
        sk = combatant_from_monster(
            REGISTRY.get_monster("skeleton"), (0, 0), "x",
        )
        self.assertTrue(sk.is_immune_to_bleed())

    def test_zombie_is_immune(self):
        z = combatant_from_monster(
            REGISTRY.get_monster("human_zombie"), (0, 0), "x",
        )
        self.assertTrue(z.is_immune_to_bleed())

    def test_goblin_is_susceptible(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        self.assertFalse(g.is_immune_to_bleed())

    def test_orc_is_susceptible(self):
        o = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        self.assertFalse(o.is_immune_to_bleed())


class TestBleedSkippedForImmuneCombatants(unittest.TestCase):
    def test_undead_with_ferocity_active_does_not_bleed(self):
        # Synthetic case: skeleton can never naturally have ferocity,
        # but if a future content addition mistakenly grants it, the
        # bleed must not apply.
        sk = combatant_from_monster(
            REGISTRY.get_monster("skeleton"), (0, 0), "x",
        )
        sk.current_hp = -3
        sk.add_condition("ferocity_active")
        sk.tick_round(2)
        # No HP loss.
        self.assertEqual(sk.current_hp, -3)
        # And not dead either (skeleton would already be destroyed at
        # HP 0 via its threshold; but the negative-HP-via-bleed path
        # doesn't fire).
        self.assertNotIn("dead", sk.conditions)

    def test_undead_in_dying_state_does_not_bleed(self):
        # Same idea: skeleton can't naturally enter dying (destroyed
        # at HP 0), but if synthetically set, bleed must not apply.
        sk = combatant_from_monster(
            REGISTRY.get_monster("skeleton"), (0, 0), "x",
        )
        sk.current_hp = -2
        sk.add_condition("dying")
        sk.tick_round(2)
        self.assertEqual(sk.current_hp, -2)

    def test_living_creature_with_ferocity_still_bleeds(self):
        # Sanity check: the guard doesn't accidentally turn off bleed
        # for living creatures.
        orc = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        orc.current_hp = -5
        orc.add_condition("ferocity_active")
        orc.tick_round(2)
        self.assertEqual(orc.current_hp, -6)


if __name__ == "__main__":
    unittest.main()
