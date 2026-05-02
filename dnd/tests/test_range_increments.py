"""Tests for PF1 range-increment penalty on ranged attacks.

PF1 RAW: -2 per increment beyond the first. e.g., a longbow with
range_increment 100 ft hits at -0 within 100 ft, -2 at 100-200,
-4 at 200-300, etc.
"""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import _range_increment_penalty


REGISTRY = default_registry()


def _setup(distance_squares: int):
    """Place an attacker and target N squares apart."""
    a = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
    b = combatant_from_monster(
        REGISTRY.get_monster("goblin"), (distance_squares, 0), "y",
    )
    grid = Grid(width=200, height=10)
    grid.place(a)
    grid.place(b)
    return a, b, grid


class TestRangeIncrement(unittest.TestCase):
    def test_within_first_increment_no_penalty(self):
        a, b, grid = _setup(distance_squares=4)  # 20 ft
        chosen = {"type": "ranged", "range_increment": 30}
        self.assertEqual(
            _range_increment_penalty(chosen, a, b, grid, True), 0,
        )

    def test_just_inside_first_increment(self):
        a, b, grid = _setup(distance_squares=6)  # 30 ft
        chosen = {"type": "ranged", "range_increment": 30}
        self.assertEqual(
            _range_increment_penalty(chosen, a, b, grid, True), 0,
        )

    def test_just_past_first_increment(self):
        a, b, grid = _setup(distance_squares=7)  # 35 ft
        chosen = {"type": "ranged", "range_increment": 30}
        self.assertEqual(
            _range_increment_penalty(chosen, a, b, grid, True), -2,
        )

    def test_second_increment_full(self):
        a, b, grid = _setup(distance_squares=12)  # 60 ft
        chosen = {"type": "ranged", "range_increment": 30}
        self.assertEqual(
            _range_increment_penalty(chosen, a, b, grid, True), -2,
        )

    def test_third_increment(self):
        a, b, grid = _setup(distance_squares=13)  # 65 ft
        chosen = {"type": "ranged", "range_increment": 30}
        self.assertEqual(
            _range_increment_penalty(chosen, a, b, grid, True), -4,
        )

    def test_far_shot(self):
        a, b, grid = _setup(distance_squares=40)  # 200 ft, with rinc 30
        chosen = {"type": "ranged", "range_increment": 30}
        # 200 / 30 → 7 increments → -12 penalty.
        self.assertEqual(
            _range_increment_penalty(chosen, a, b, grid, True), -12,
        )

    def test_longbow_at_100ft(self):
        # range_increment 100 → 100 ft is the first increment, no penalty.
        a, b, grid = _setup(distance_squares=20)  # 100 ft
        chosen = {"type": "ranged", "range_increment": 100}
        self.assertEqual(
            _range_increment_penalty(chosen, a, b, grid, True), 0,
        )

    def test_longbow_at_101ft(self):
        a, b, grid = _setup(distance_squares=21)  # 105 ft
        chosen = {"type": "ranged", "range_increment": 100}
        self.assertEqual(
            _range_increment_penalty(chosen, a, b, grid, True), -2,
        )

    def test_melee_attack_no_penalty(self):
        a, b, grid = _setup(distance_squares=20)
        chosen = {"type": "melee", "range_increment": 0}
        self.assertEqual(
            _range_increment_penalty(chosen, a, b, grid, False), 0,
        )

    def test_no_range_increment_no_penalty(self):
        # Some weapons (e.g., spell-like effects without range incr.)
        # leave the field at 0 — no penalty.
        a, b, grid = _setup(distance_squares=20)
        chosen = {"type": "ranged", "range_increment": 0}
        self.assertEqual(
            _range_increment_penalty(chosen, a, b, grid, True), 0,
        )


if __name__ == "__main__":
    unittest.main()
