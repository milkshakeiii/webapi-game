"""Tests for the conditions-cluster batch — fatigued/exhausted ability
penalties, grappled action restrictions, and blinded miss chance."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.actions import _validate_intent
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.modifiers import compute as _compute
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


def _ability_total(combatant, ability):
    return _compute(0, combatant.modifiers.for_target(f"ability:{ability}"))


class TestFatigued(unittest.TestCase):
    def test_applies_str_dex_penalty(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        before_str = _ability_total(g, "str")
        before_dex = _ability_total(g, "dex")
        g.add_condition("fatigued")
        self.assertEqual(_ability_total(g, "str"), before_str - 2)
        self.assertEqual(_ability_total(g, "dex"), before_dex - 2)

    def test_remove_clears_penalty(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        baseline_str = _ability_total(g, "str")
        g.add_condition("fatigued")
        g.remove_condition("fatigued")
        self.assertEqual(_ability_total(g, "str"), baseline_str)
        self.assertNotIn("fatigued", g.conditions)

    def test_double_apply_does_not_stack(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        baseline_str = _ability_total(g, "str")
        g.add_condition("fatigued")
        g.add_condition("fatigued")
        # Penalty should be -2, not -4.
        self.assertEqual(_ability_total(g, "str"), baseline_str - 2)

    def test_fatigued_cannot_apply_when_exhausted(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.add_condition("exhausted")
        before_str = _ability_total(g, "str")
        result = g.add_condition("fatigued")
        self.assertFalse(result)
        # No additional penalty.
        self.assertEqual(_ability_total(g, "str"), before_str)


class TestExhausted(unittest.TestCase):
    def test_applies_minus_six_str_dex_and_halves_speed(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        speed_before = g.speed
        before_str = _ability_total(g, "str")
        g.add_condition("exhausted")
        self.assertEqual(_ability_total(g, "str"), before_str - 6)
        self.assertEqual(g.speed, speed_before // 2)

    def test_supersedes_fatigued(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        baseline_str = _ability_total(g, "str")
        g.add_condition("fatigued")
        # Now -2.
        self.assertEqual(_ability_total(g, "str"), baseline_str - 2)
        g.add_condition("exhausted")
        # Fatigued should be cleared; exhausted -6 only.
        self.assertNotIn("fatigued", g.conditions)
        self.assertEqual(_ability_total(g, "str"), baseline_str - 6)

    def test_remove_restores_speed(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        speed_before = g.speed
        g.add_condition("exhausted")
        g.remove_condition("exhausted")
        self.assertEqual(g.speed, speed_before)


class TestGrappled(unittest.TestCase):
    def test_applies_attack_penalty(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        attack_before = _compute(0, g.modifiers.for_target("attack"))
        g.add_condition("grappled")
        attack_after = _compute(0, g.modifiers.for_target("attack"))
        self.assertEqual(attack_after, attack_before - 2)

    def test_applies_dex_penalty(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        dex_before = _ability_total(g, "dex")
        g.add_condition("grappled")
        self.assertEqual(_ability_total(g, "dex"), dex_before - 4)

    def test_remove_clears_modifiers(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        attack_before = _compute(0, g.modifiers.for_target("attack"))
        dex_before = _ability_total(g, "dex")
        g.add_condition("grappled")
        g.remove_condition("grappled")
        self.assertEqual(_compute(0, g.modifiers.for_target("attack")),
                         attack_before)
        self.assertEqual(_ability_total(g, "dex"), dex_before)

    def test_validation_blocks_movement(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        grid = Grid(width=10, height=10)
        grid.place(g)
        g.add_condition("grappled")
        do = {"move": {"type": "move_to", "target": (5, 0)}}
        self.assertIsNotNone(_validate_intent(g, do, grid))

    def test_validation_blocks_5ft_step(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        grid = Grid(width=10, height=10)
        grid.place(g)
        g.add_condition("grappled")
        do = {"five_foot_step": (1, 0)}
        self.assertIsNotNone(_validate_intent(g, do, grid))

    def test_validation_blocks_charge(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        grid = Grid(width=10, height=10)
        grid.place(g)
        g.add_condition("grappled")
        do = {"composite": "charge", "args": {"target": "enemy.closest"}}
        self.assertIsNotNone(_validate_intent(g, do, grid))


class TestBlindedMissChance(unittest.TestCase):
    def _setup(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        b = combatant_from_monster(REGISTRY.get_monster("goblin"), (6, 5), "y")
        # Make orc effectively impossible to miss the goblin (high atk).
        for opt in a.attack_options:
            opt["attack_bonus"] = 100
        b.max_hp = 9999
        b.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        return a, b, enc, grid

    def test_blinded_attacker_misses_about_half_the_time(self):
        # With concealment-like miss roll of 50%, ~half of attempts should
        # convert hits to misses. Iterate seeds and tally.
        misses = 0
        attempts = 30
        for seed in range(1, attempts + 1):
            a, b, enc, grid = self._setup()
            a.add_condition("blinded")
            b_hp_before = b.current_hp
            script = BehaviorScript(name="atk", rules=[
                Rule(do={"composite": "full_attack",
                         "args": {"target": "enemy.closest"}}),
            ])
            intent = Interpreter(script).pick_turn(a, enc, grid)
            execute_turn(a, intent, enc, grid, Roller(seed=seed))
            if b.current_hp == b_hp_before:
                misses += 1
        # Expect ~half the attacks to miss; allow a wide tolerance.
        self.assertGreater(misses, 5)
        self.assertLess(misses, attempts - 5)

    def test_unblinded_orc_always_hits(self):
        # Sanity check: with attack +100 and not blinded, every attack
        # should land. Confirms blinded is the only thing that misses.
        for seed in range(1, 11):
            a, b, enc, grid = self._setup()
            b_hp_before = b.current_hp
            script = BehaviorScript(name="atk", rules=[
                Rule(do={"composite": "full_attack",
                         "args": {"target": "enemy.closest"}}),
            ])
            intent = Interpreter(script).pick_turn(a, enc, grid)
            execute_turn(a, intent, enc, grid, Roller(seed=seed))
            self.assertLess(b.current_hp, b_hp_before)


if __name__ == "__main__":
    unittest.main()
