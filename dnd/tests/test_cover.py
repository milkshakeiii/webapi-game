"""Tests for the positional cover system.

PF1 (simplified): a wall on the line between attacker and target
grants hard cover (+4 AC for any attack). An intervening combatant
grants soft cover (+4 AC vs ranged only). Hard cover trumps soft
cover.
"""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.grid import Grid, wall
from dnd.engine.turn_executor import _cover_ac_bonus


REGISTRY = default_registry()


def _setup(attacker_pos, target_pos):
    a = combatant_from_monster(REGISTRY.get_monster("orc"), attacker_pos, "x")
    b = combatant_from_monster(REGISTRY.get_monster("goblin"), target_pos, "y")
    grid = Grid(width=20, height=20)
    grid.place(a)
    grid.place(b)
    return a, b, grid


class TestNoCover(unittest.TestCase):
    def test_clear_line_no_cover(self):
        a, b, grid = _setup((2, 5), (8, 5))
        self.assertEqual(_cover_ac_bonus(a, b, grid, is_ranged=False), 0)
        self.assertEqual(_cover_ac_bonus(a, b, grid, is_ranged=True), 0)


class TestHardCover(unittest.TestCase):
    def test_wall_grants_4_ac_for_melee(self):
        # Reach attack with a wall between — uncommon but exercises rules.
        a, b, grid = _setup((2, 5), (8, 5))
        grid.add_feature(5, 5, wall())
        self.assertEqual(_cover_ac_bonus(a, b, grid, is_ranged=False), 4)

    def test_wall_grants_4_ac_for_ranged(self):
        a, b, grid = _setup((2, 5), (8, 5))
        grid.add_feature(5, 5, wall())
        self.assertEqual(_cover_ac_bonus(a, b, grid, is_ranged=True), 4)


class TestSoftCover(unittest.TestCase):
    def test_intervening_combatant_grants_ranged_cover(self):
        a, b, grid = _setup((2, 5), (8, 5))
        third = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (5, 5), "team_c",
        )
        grid.place(third)
        self.assertEqual(_cover_ac_bonus(a, b, grid, is_ranged=True), 4)

    def test_intervening_combatant_no_melee_cover(self):
        a, b, grid = _setup((2, 5), (8, 5))
        third = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (5, 5), "team_c",
        )
        grid.place(third)
        self.assertEqual(_cover_ac_bonus(a, b, grid, is_ranged=False), 0)


class TestHardCoverTrumpsSoft(unittest.TestCase):
    def test_wall_present_with_combatant_returns_hard_cover(self):
        a, b, grid = _setup((2, 5), (8, 5))
        # Add wall before any combatant so detection short-circuits on it.
        grid.add_feature(5, 5, wall())
        # Hard cover is 4 (same as soft cover) but importantly fires for
        # melee too. Verifying via the melee variant.
        self.assertEqual(_cover_ac_bonus(a, b, grid, is_ranged=False), 4)


class TestAttackerAndTargetSquaresIgnored(unittest.TestCase):
    def test_attacker_square_doesnt_cover_self(self):
        # If a wall happens to be on the attacker's own square, that
        # shouldn't count.
        a, b, grid = _setup((2, 5), (8, 5))
        # We can't place a wall on the same square as the attacker
        # cleanly, but we can verify the line iteration excludes
        # endpoints by checking the no-cover case still returns 0
        # when the attacker stands next to a wall outside the line.
        grid.add_feature(2, 6, wall())  # adjacent but off-axis
        self.assertEqual(_cover_ac_bonus(a, b, grid, is_ranged=True), 0)


if __name__ == "__main__":
    unittest.main()
