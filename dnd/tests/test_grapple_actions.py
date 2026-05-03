"""Tests for the full grapple action set: damage, move, pin, escape."""

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


def _setup_grappled():
    """Two adjacent orcs; the first is grappling the second."""
    a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
    b = combatant_from_monster(REGISTRY.get_monster("orc"), (6, 5), "y")
    a.bases["cmb"] = 30  # auto-pass maintain checks
    b.bases["cmd"] = 5
    a.grappling_target_id = b.id
    b.grappled_by_id = a.id
    a.add_condition("grappled")
    b.add_condition("grappled")
    grid = Grid(width=20, height=10)
    grid.place(a)
    grid.place(b)
    enc = Encounter.begin(grid, [a, b], Roller(seed=1))
    return a, b, enc, grid


class TestGrappleDamage(unittest.TestCase):
    def test_damage_reduces_target_hp(self):
        a, b, enc, grid = _setup_grappled()
        before = b.current_hp
        script = BehaviorScript(name="gd", rules=[
            Rule(do={"composite": "grapple_damage", "args": {}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("grapple_damage", kinds)
        # Damage was dealt.
        self.assertLess(b.current_hp, before)

    def test_grapple_damage_skips_when_not_grappling(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        grid = Grid(width=10, height=10)
        grid.place(a)
        enc = Encounter.begin(grid, [a], Roller(seed=1))
        script = BehaviorScript(name="gd", rules=[
            Rule(do={"composite": "grapple_damage", "args": {}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        self.assertIn("skip", [e.kind for e in result.events])


class TestGrapplePin(unittest.TestCase):
    def test_pin_sets_pinned_and_helpless(self):
        a, b, enc, grid = _setup_grappled()
        script = BehaviorScript(name="gp", rules=[
            Rule(do={"composite": "grapple_pin", "args": {}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        execute_turn(a, intent, enc, grid, Roller(seed=1))
        self.assertIn("pinned", b.conditions)
        self.assertIn("helpless", b.conditions)


class TestGrappleMove(unittest.TestCase):
    def test_move_relocates_both(self):
        a, b, enc, grid = _setup_grappled()
        a_old = a.position
        b_old = b.position
        script = BehaviorScript(name="gm", rules=[
            Rule(do={"composite": "grapple_move",
                     "args": {"direction": "north"}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        execute_turn(a, intent, enc, grid, Roller(seed=1))
        # Both moved.
        self.assertNotEqual(a.position, a_old)
        self.assertEqual(b.position, a_old)  # b dragged to a's old spot


class TestGrappleBreakFree(unittest.TestCase):
    def test_break_free_clears_grapple(self):
        a, b, enc, grid = _setup_grappled()
        # Boost b's CMB so they pass.
        b.bases["cmb"] = 50
        a.bases["cmb"] = 0  # easy DC
        script = BehaviorScript(name="bf", rules=[
            Rule(do={"composite": "grapple_break_free",
                     "args": {"method": "cmb"}}),
        ])
        intent = Interpreter(script).pick_turn(b, enc, grid)
        execute_turn(b, intent, enc, grid, Roller(seed=1))
        # Both lost grappled.
        self.assertNotIn("grappled", a.conditions)
        self.assertNotIn("grappled", b.conditions)
        self.assertIsNone(a.grappling_target_id)
        self.assertIsNone(b.grappled_by_id)

    def test_break_free_pinned_clears_pinned_and_helpless(self):
        a, b, enc, grid = _setup_grappled()
        b.add_condition("pinned")
        b.add_condition("helpless")
        b.bases["cmb"] = 50
        a.bases["cmb"] = 0
        script = BehaviorScript(name="bf", rules=[
            Rule(do={"composite": "grapple_break_free",
                     "args": {"method": "cmb"}}),
        ])
        intent = Interpreter(script).pick_turn(b, enc, grid)
        execute_turn(b, intent, enc, grid, Roller(seed=1))
        self.assertNotIn("pinned", b.conditions)
        self.assertNotIn("helpless", b.conditions)

    def test_escape_artist_method(self):
        a, b, enc, grid = _setup_grappled()
        a.bases["cmb"] = 0
        # Just verify the method=escape_artist path runs without error.
        script = BehaviorScript(name="bf", rules=[
            Rule(do={"composite": "grapple_break_free",
                     "args": {"method": "escape_artist"}}),
        ])
        intent = Interpreter(script).pick_turn(b, enc, grid)
        result = execute_turn(b, intent, enc, grid, Roller(seed=1))
        self.assertIn("grapple_break_free", [e.kind for e in result.events])
        ev = [e for e in result.events
              if e.kind == "grapple_break_free"][0]
        self.assertEqual(ev.detail["method"], "escape_artist")


if __name__ == "__main__":
    unittest.main()
