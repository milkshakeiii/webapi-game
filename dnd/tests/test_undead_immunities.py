"""Tests for undead/construct condition immunities.

PF1 RAW: undead are immune to mind-affecting effects, paralysis, sleep,
stun, fatigue, exhaustion, disease, poison, nausea, fear effects.
"""

from __future__ import annotations

import unittest

from dnd.engine.combatant import (
    UNDEAD_CONDITION_IMMUNITIES,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


class TestImmunitySet(unittest.TestCase):
    def test_skeleton_carries_immunity_set(self):
        sk = combatant_from_monster(
            REGISTRY.get_monster("skeleton"), (0, 0), "x",
        )
        # Spot-check a few; the full set is constant.
        for cond in ("stunned", "paralyzed", "charmed", "fatigued",
                     "frightened", "sleeping"):
            self.assertIn(cond, sk.condition_immunities, f"{cond} missing")

    def test_zombie_carries_immunity_set(self):
        z = combatant_from_monster(
            REGISTRY.get_monster("human_zombie"), (0, 0), "x",
        )
        for cond in ("stunned", "paralyzed", "sleeping", "exhausted"):
            self.assertIn(cond, z.condition_immunities)

    def test_living_creatures_have_no_immunities(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        self.assertEqual(g.condition_immunities, set())

    def test_undead_immunity_set_constant_matches(self):
        sk = combatant_from_monster(
            REGISTRY.get_monster("skeleton"), (0, 0), "x",
        )
        self.assertEqual(sk.condition_immunities, set(UNDEAD_CONDITION_IMMUNITIES))


class TestAddConditionRespectsImmunity(unittest.TestCase):
    def test_skeleton_cant_be_stunned(self):
        sk = combatant_from_monster(
            REGISTRY.get_monster("skeleton"), (0, 0), "x",
        )
        applied = sk.add_condition("stunned")
        self.assertFalse(applied)
        self.assertNotIn("stunned", sk.conditions)

    def test_skeleton_cant_be_charmed(self):
        sk = combatant_from_monster(
            REGISTRY.get_monster("skeleton"), (0, 0), "x",
        )
        applied = sk.add_condition("charmed")
        self.assertFalse(applied)
        self.assertNotIn("charmed", sk.conditions)

    def test_skeleton_cant_be_paralyzed(self):
        sk = combatant_from_monster(
            REGISTRY.get_monster("skeleton"), (0, 0), "x",
        )
        applied = sk.add_condition("paralyzed")
        self.assertFalse(applied)
        self.assertNotIn("paralyzed", sk.conditions)

    def test_non_immune_condition_still_applies(self):
        # Skeletons are NOT immune to "prone" or "blinded"; those should
        # apply normally.
        sk = combatant_from_monster(
            REGISTRY.get_monster("skeleton"), (0, 0), "x",
        )
        applied = sk.add_condition("prone")
        self.assertTrue(applied)
        self.assertIn("prone", sk.conditions)

    def test_living_creature_can_be_stunned(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        applied = g.add_condition("stunned")
        self.assertTrue(applied)
        self.assertIn("stunned", g.conditions)


class TestStunningFistFailsAgainstUndead(unittest.TestCase):
    """End-to-end: even on a successful Fort save fail, undead don't
    end up stunned."""

    def test_skeleton_target_never_stunned(self):
        # We use a monk-equivalent: orc with fake stunning_fist_uses
        # resource and the feat in extra_feats. Easier than building a
        # full character.
        from dnd.engine.combatant import combatant_from_monster as cfm
        attacker = cfm(REGISTRY.get_monster("orc"), (5, 5), "team_a")
        attacker.resources["stunning_fist_uses"] = 5
        attacker.extra_feats = ["stunning_fist"]

        skeleton = cfm(REGISTRY.get_monster("skeleton"), (6, 5), "team_b")
        skeleton.max_hp = 9999
        skeleton.current_hp = 9999

        grid = Grid(width=12, height=12)
        grid.place(attacker)
        grid.place(skeleton)
        enc = Encounter.begin(grid, [attacker, skeleton], Roller(seed=1))

        script = BehaviorScript(name="stun", rules=[
            Rule(do={"composite": "stunning_fist",
                     "args": {"target": "enemy.closest"}}),
        ])
        # Run several seeds; even if save fails, skeleton must not be
        # stunned because of immunity.
        for seed in range(1, 30):
            attacker.resources["stunning_fist_uses"] = 5
            skeleton.conditions.discard("stunned")
            intent = Interpreter(script).pick_turn(attacker, enc, grid)
            execute_turn(attacker, intent, enc, grid, Roller(seed=seed))
            self.assertNotIn("stunned", skeleton.conditions,
                             f"seed {seed}: skeleton ended up stunned")


if __name__ == "__main__":
    unittest.main()
