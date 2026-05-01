"""Tests for dnd.engine.grid."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.grid import (
    Grid,
    GridFeature,
    PlacementError,
    difficult,
    wall,
)


REGISTRY = default_registry()


def _goblin(pos: tuple[int, int], team: str = "enemies"):
    return combatant_from_monster(REGISTRY.get_monster("goblin"), pos, team)


def _orc(pos: tuple[int, int], team: str = "enemies"):
    return combatant_from_monster(REGISTRY.get_monster("orc"), pos, team)


# ---------------------------------------------------------------------------
# Distance
# ---------------------------------------------------------------------------


class TestDistance(unittest.TestCase):
    def test_same_square_zero(self):
        self.assertEqual(Grid.distance_squares((0, 0), (0, 0)), 0)

    def test_orthogonal(self):
        self.assertEqual(Grid.distance_squares((0, 0), (3, 0)), 3)
        self.assertEqual(Grid.distance_squares((0, 0), (0, 5)), 5)

    def test_diagonal_5_10_5(self):
        # 1 diagonal = 5 ft = 1 sq.
        self.assertEqual(Grid.distance_squares((0, 0), (1, 1)), 1)
        # 2 diagonals = 5 + 10 = 15 ft = 3 sq.
        self.assertEqual(Grid.distance_squares((0, 0), (2, 2)), 3)
        # 3 diagonals = 5 + 10 + 5 = 20 ft = 4 sq.
        self.assertEqual(Grid.distance_squares((0, 0), (3, 3)), 4)
        # 4 diagonals = 5 + 10 + 5 + 10 = 30 ft = 6 sq.
        self.assertEqual(Grid.distance_squares((0, 0), (4, 4)), 6)

    def test_mixed(self):
        # 5 over, 3 up: 3 diagonals + 2 straight = 20 + 10 = 30 ft = 6 sq.
        self.assertEqual(Grid.distance_squares((0, 0), (5, 3)), 6)

    def test_distance_feet(self):
        self.assertEqual(Grid.distance_feet((0, 0), (2, 2)), 15)


# ---------------------------------------------------------------------------
# Placement
# ---------------------------------------------------------------------------


class TestPlacement(unittest.TestCase):
    def test_place_medium_combatant(self):
        g = Grid(width=10, height=10)
        c = _orc((4, 4))
        g.place(c)
        self.assertEqual(g.occupant(4, 4), c.id)
        self.assertEqual(g.occupant(0, 0), None)

    def test_place_small_at_edge(self):
        g = Grid(width=10, height=10)
        c = _goblin((0, 0))
        g.place(c)
        self.assertEqual(g.occupant(0, 0), c.id)

    def test_place_out_of_bounds(self):
        g = Grid(width=5, height=5)
        c = _goblin((10, 10))
        with self.assertRaises(PlacementError):
            g.place(c)

    def test_place_overlapping(self):
        g = Grid(width=10, height=10)
        a = _goblin((4, 4), team="a")
        b = _goblin((4, 4), team="b")
        g.place(a)
        with self.assertRaises(PlacementError):
            g.place(b)

    def test_place_on_wall(self):
        g = Grid(width=10, height=10)
        g.add_feature(4, 4, wall())
        c = _goblin((4, 4))
        with self.assertRaises(PlacementError):
            g.place(c)

    def test_remove(self):
        g = Grid(width=10, height=10)
        c = _goblin((4, 4))
        g.place(c)
        g.remove(c.id)
        self.assertIsNone(g.occupant(4, 4))

    def test_move(self):
        g = Grid(width=10, height=10)
        c = _goblin((4, 4))
        g.place(c)
        g.move(c, (5, 5))
        self.assertEqual(c.position, (5, 5))
        self.assertIsNone(g.occupant(4, 4))
        self.assertEqual(g.occupant(5, 5), c.id)


# ---------------------------------------------------------------------------
# Distance between combatants
# ---------------------------------------------------------------------------


class TestCombatantDistance(unittest.TestCase):
    def test_adjacent_orthogonal(self):
        g = Grid(width=10, height=10)
        a = _goblin((4, 4), team="a")
        b = _orc((5, 4), team="b")
        g.place(a)
        g.place(b)
        self.assertEqual(g.distance_between(a, b), 1)
        self.assertTrue(g.is_adjacent(a, b))

    def test_adjacent_diagonal(self):
        g = Grid(width=10, height=10)
        a = _goblin((4, 4), team="a")
        b = _orc((5, 5), team="b")
        g.place(a)
        g.place(b)
        self.assertTrue(g.is_adjacent(a, b))

    def test_not_adjacent(self):
        g = Grid(width=10, height=10)
        a = _goblin((0, 0), team="a")
        b = _orc((5, 5), team="b")
        g.place(a)
        g.place(b)
        self.assertFalse(g.is_adjacent(a, b))


# ---------------------------------------------------------------------------
# Threatened squares
# ---------------------------------------------------------------------------


class TestThreatening(unittest.TestCase):
    def test_medium_threatens_8_squares(self):
        g = Grid(width=10, height=10)
        orc = _orc((5, 5))
        g.place(orc)
        threatened = g.threatened_squares(orc)
        # Medium creature with 5-ft reach threatens 8 surrounding squares.
        self.assertEqual(len(threatened), 8)
        for sq in [(4, 4), (5, 4), (6, 4),
                   (4, 5),         (6, 5),
                   (4, 6), (5, 6), (6, 6)]:
            self.assertIn(sq, threatened)

    def test_threatens_combatant(self):
        g = Grid(width=10, height=10)
        a = _orc((5, 5), team="a")
        b = _goblin((6, 5), team="b")
        c = _goblin((9, 9), team="c")
        g.place(a)
        g.place(b)
        g.place(c)
        self.assertTrue(g.threatens(a, b))
        self.assertFalse(g.threatens(a, c))


# ---------------------------------------------------------------------------
# Flanking
# ---------------------------------------------------------------------------


class TestFlanking(unittest.TestCase):
    def test_flanked_opposite_sides(self):
        g = Grid(width=10, height=10)
        target = _orc((5, 5), team="enemy")
        a = _goblin((4, 5), team="patron")
        b = _goblin((6, 5), team="patron")
        g.place(target)
        g.place(a)
        g.place(b)
        self.assertTrue(g.is_flanked_by(target, a, b))

    def test_not_flanked_same_side(self):
        g = Grid(width=10, height=10)
        target = _orc((5, 5), team="enemy")
        a = _goblin((4, 5), team="patron")
        b = _goblin((4, 6), team="patron")
        g.place(target)
        g.place(a)
        g.place(b)
        # Both on the west/southwest — not opposite sides.
        self.assertFalse(g.is_flanked_by(target, a, b))


# ---------------------------------------------------------------------------
# Line of sight
# ---------------------------------------------------------------------------


class TestLineOfSight(unittest.TestCase):
    def test_clear_los(self):
        g = Grid(width=10, height=10)
        self.assertTrue(g.line_of_sight((0, 0), (9, 9)))

    def test_wall_blocks(self):
        g = Grid(width=10, height=10)
        g.add_feature(5, 5, wall())
        # (5, 5) is on the diagonal from (0,0) to (9,9).
        self.assertFalse(g.line_of_sight((0, 0), (9, 9)))

    def test_difficult_does_not_block(self):
        g = Grid(width=10, height=10)
        g.add_feature(5, 5, difficult())
        self.assertTrue(g.line_of_sight((0, 0), (9, 9)))


# ---------------------------------------------------------------------------
# Terrain helpers
# ---------------------------------------------------------------------------


class TestFeatures(unittest.TestCase):
    def test_passable_logic(self):
        g = Grid(width=5, height=5)
        g.add_feature(2, 2, wall())
        self.assertFalse(g.is_passable(2, 2))
        self.assertTrue(g.is_passable(0, 0))
        self.assertTrue(g.is_difficult(0, 0) is False)

    def test_difficult_terrain_passable(self):
        g = Grid(width=5, height=5)
        g.add_feature(1, 1, difficult())
        self.assertTrue(g.is_passable(1, 1))
        self.assertTrue(g.is_difficult(1, 1))


if __name__ == "__main__":
    unittest.main()
