"""Tests for Phase 1.2 condition gap-fillers — bleed framework,
coup-de-grace vs helpless, and disabled self-damage."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


# ---------------------------------------------------------------------------
# Bleed
# ---------------------------------------------------------------------------


class TestBleed(unittest.TestCase):
    def test_apply_bleed_sets_condition_and_amount(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        c.apply_bleed(2)
        self.assertEqual(c.bleed, 2)
        self.assertIn("bleed", c.conditions)

    def test_apply_bleed_stacks(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        c.apply_bleed(2)
        c.apply_bleed(3)
        self.assertEqual(c.bleed, 5)

    def test_tick_round_applies_bleed_damage(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        c.apply_bleed(3)
        hp_before = c.current_hp
        c.tick_round(current_round=1)
        self.assertEqual(c.current_hp, hp_before - 3)
        self.assertIn("bleed", c.conditions)  # still bleeding next round

    def test_heal_stops_bleed(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        c.apply_bleed(3)
        c.current_hp = c.current_hp - 5  # take some damage so heal does something
        c.heal(2)
        self.assertEqual(c.bleed, 0)
        self.assertNotIn("bleed", c.conditions)

    def test_undead_immune_to_bleed(self):
        sk = combatant_from_monster(REGISTRY.get_monster("skeleton"),
                                    (0, 0), "x")
        sk.apply_bleed(5)
        self.assertEqual(sk.bleed, 0)
        self.assertNotIn("bleed", sk.conditions)

    def test_stop_bleed_clears(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        c.apply_bleed(4)
        c.stop_bleed()
        self.assertEqual(c.bleed, 0)
        self.assertNotIn("bleed", c.conditions)


# ---------------------------------------------------------------------------
# Coup-de-grace
# ---------------------------------------------------------------------------


class TestCoupDeGrace(unittest.TestCase):
    def _setup(self):
        attacker = combatant_from_monster(REGISTRY.get_monster("orc"),
                                          (5, 5), "x")
        # Crank damage so the Fort save DC is unbeatable: any miss-by-save
        # resolves as instant death.
        attacker.attack_options = [{
            "type": "melee", "name": "executioner",
            "weapon_id": "falchion",
            "weapon_category": "exotic",
            "attack_bonus": 100,
            "damage": "2d4", "damage_bonus": 100,
            "damage_type": "S",
            "crit_range": [20, 20], "crit_multiplier": 2,
        }]
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (6, 5), "y")
        # Make target helpless via the sleeping condition.
        target.add_condition("sleeping")
        grid = Grid(width=12, height=12)
        grid.place(attacker)
        grid.place(target)
        enc = Encounter.begin(grid, [attacker, target], Roller(seed=1))
        return attacker, target, enc, grid

    def test_coup_de_grace_kills_helpless_via_save_or_die(self):
        a, t, enc, grid = self._setup()
        script = BehaviorScript(name="cdg", rules=[
            Rule(do={"composite": "coup_de_grace",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("coup_de_grace", kinds)
        cdg = next(e for e in result.events if e.kind == "coup_de_grace")
        # DC ≥ 110 with this weapon; even a nat-20 + Fort 3 only reaches
        # 23. Save must fail → instant death.
        self.assertFalse(cdg.detail["fort_passed"])
        self.assertTrue(cdg.detail["died"])
        self.assertIn("dead", t.conditions)

    def test_coup_de_grace_skips_when_target_not_helpless(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"),
                                   (5, 5), "x")
        t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (6, 5), "y")
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(t)
        enc = Encounter.begin(grid, [a, t], Roller(seed=1))
        script = BehaviorScript(name="cdg", rules=[
            Rule(do={"composite": "coup_de_grace",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        # Should skip without killing.
        self.assertNotIn("coup_de_grace", kinds)
        self.assertIn("skip", kinds)
        self.assertNotIn("dead", t.conditions)


# ---------------------------------------------------------------------------
# Disabled self-damage
# ---------------------------------------------------------------------------


class TestDisabledSelfDamage(unittest.TestCase):
    def test_disabled_takes_one_hp_after_standard(self):
        # Use goblin — no ferocity, so -1 HP cleanly enters dying.
        a = combatant_from_monster(REGISTRY.get_monster("goblin"), (5, 5), "x")
        b = combatant_from_monster(REGISTRY.get_monster("orc"), (6, 5), "y")
        # Force disabled state: HP exactly 0.
        a.current_hp = 0
        a.add_condition("disabled")
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        script = BehaviorScript(name="atk", rules=[
            Rule(do={"standard": {"type": "attack",
                                  "target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("disabled_self_damage", kinds)
        # Took 1 HP self-damage; goblin should now be at -1, dying.
        self.assertEqual(a.current_hp, -1)
        self.assertIn("dying", a.conditions)

    def test_orc_disabled_self_damage_triggers_ferocity(self):
        # Orcs have ferocity: at HP <= 0 they go staggered + active
        # rather than dying. The self-damage hook still fires; the
        # post-damage state just resolves to staggered.
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        b = combatant_from_monster(REGISTRY.get_monster("goblin"), (6, 5), "y")
        a.current_hp = 0
        a.add_condition("disabled")
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        script = BehaviorScript(name="atk", rules=[
            Rule(do={"standard": {"type": "attack",
                                  "target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("disabled_self_damage", kinds)
        self.assertEqual(a.current_hp, -1)
        self.assertIn("ferocity_active", a.conditions)


if __name__ == "__main__":
    unittest.main()
