"""Tests for dnd.engine.encounter."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.encounter import (
    Encounter,
    Turn,
    TurnValidationError,
    aoo_triggers_for_movement,
    aoo_triggers_for_provoking_action,
    roll_initiative,
    validate_turn,
)
from dnd.engine.grid import Grid


REGISTRY = default_registry()


def _goblin(pos, team="enemies"):
    return combatant_from_monster(REGISTRY.get_monster("goblin"), pos, team)


def _orc(pos, team="enemies"):
    return combatant_from_monster(REGISTRY.get_monster("orc"), pos, team)


# ---------------------------------------------------------------------------
# Turn validation
# ---------------------------------------------------------------------------


class TestTurnValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.grid = Grid(width=10, height=10)
        self.actor = _orc((5, 5), team="patrons")
        self.grid.place(self.actor)

    def test_valid_standard_and_move(self):
        t = Turn(
            standard={"type": "attack", "target": "enemy.closest"},
            move={"type": "move_to", "target": (6, 5)},
        )
        validate_turn(t, self.actor, self.grid)  # no raise

    def test_full_round_excludes_standard(self):
        t = Turn(
            full_round={"type": "charge", "target": "enemy.closest"},
            standard={"type": "attack", "target": "x"},
        )
        with self.assertRaises(TurnValidationError):
            validate_turn(t, self.actor, self.grid)

    def test_full_round_excludes_move(self):
        t = Turn(
            full_round={"type": "full_attack", "target": "x"},
            move={"type": "move_to", "target": (6, 5)},
        )
        with self.assertRaises(TurnValidationError):
            validate_turn(t, self.actor, self.grid)

    def test_5ft_step_excludes_movement_in_move_slot(self):
        t = Turn(
            standard={"type": "attack", "target": "x"},
            move={"type": "move_to", "target": (6, 5)},
            five_foot_step=(5, 6),
        )
        with self.assertRaises(TurnValidationError):
            validate_turn(t, self.actor, self.grid)

    def test_5ft_step_excludes_charge(self):
        t = Turn(
            full_round={"type": "charge", "target": "x"},
            five_foot_step=(5, 6),
        )
        with self.assertRaises(TurnValidationError):
            validate_turn(t, self.actor, self.grid)

    def test_5ft_step_must_be_adjacent(self):
        t = Turn(
            standard={"type": "attack", "target": "x"},
            five_foot_step=(7, 7),  # not adjacent to (5, 5)
        )
        with self.assertRaises(TurnValidationError):
            validate_turn(t, self.actor, self.grid)

    def test_5ft_step_with_non_movement_move_slot_ok(self):
        # Drawing a weapon in the move slot doesn't consume movement.
        t = Turn(
            standard={"type": "attack", "target": "x"},
            move={"type": "draw_weapon", "weapon": "longsword"},
            five_foot_step=(5, 6),
        )
        validate_turn(t, self.actor, self.grid)

    def test_illegal_free_action(self):
        t = Turn(free=({"type": "throw_brick"},))
        with self.assertRaises(TurnValidationError):
            validate_turn(t, self.actor, self.grid)

    def test_legal_free_action(self):
        t = Turn(free=({"type": "drop_item", "item": "torch"},))
        validate_turn(t, self.actor, self.grid)

    def test_unconscious_cannot_act(self):
        self.actor.add_condition("unconscious")
        t = Turn(standard={"type": "attack", "target": "x"})
        with self.assertRaises(TurnValidationError):
            validate_turn(t, self.actor, self.grid)

    def test_staggered_blocks_full_round(self):
        self.actor.add_condition("staggered")
        t = Turn(full_round={"type": "full_attack", "target": "x"})
        with self.assertRaises(TurnValidationError):
            validate_turn(t, self.actor, self.grid)

    def test_staggered_blocks_standard_plus_move(self):
        self.actor.add_condition("staggered")
        t = Turn(
            standard={"type": "attack", "target": "x"},
            move={"type": "move_to", "target": (6, 5)},
        )
        with self.assertRaises(TurnValidationError):
            validate_turn(t, self.actor, self.grid)

    def test_staggered_allows_single_action(self):
        self.actor.add_condition("staggered")
        t = Turn(standard={"type": "attack", "target": "x"})
        validate_turn(t, self.actor, self.grid)

    def test_grappled_blocks_drink(self):
        self.actor.add_condition("grappled")
        t = Turn(standard={"type": "drink", "item": "potion"})
        with self.assertRaises(TurnValidationError):
            validate_turn(t, self.actor, self.grid)


# ---------------------------------------------------------------------------
# Initiative
# ---------------------------------------------------------------------------


class TestInitiative(unittest.TestCase):
    def test_initiative_order_descending(self):
        a = _goblin((0, 0), team="a")
        b = _orc((1, 0), team="b")
        rolls = roll_initiative([a, b], Roller(seed=42))
        self.assertEqual(len(rolls), 2)
        self.assertGreaterEqual(rolls[0].total, rolls[1].total)

    def test_each_roll_in_range(self):
        a = _goblin((0, 0))
        rolls = roll_initiative([a], Roller(seed=42))
        self.assertEqual(len(rolls), 1)
        self.assertGreaterEqual(rolls[0].roll, 1)
        self.assertLessEqual(rolls[0].roll, 20)
        self.assertEqual(rolls[0].total, rolls[0].roll + rolls[0].modifier)

    def test_deterministic_with_seed(self):
        a = _goblin((0, 0))
        b = _orc((1, 0))
        a_first = roll_initiative([a, b], Roller(seed=99))[0].combatant.id
        a_second = roll_initiative([a, b], Roller(seed=99))[0].combatant.id
        self.assertEqual(a_first, a_second)


# ---------------------------------------------------------------------------
# Encounter state
# ---------------------------------------------------------------------------


class TestEncounter(unittest.TestCase):
    def test_begin_and_advance(self):
        grid = Grid(width=10, height=10)
        a = _goblin((0, 0), team="patrons")
        b = _orc((9, 9), team="enemies")
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        self.assertEqual(enc.round_number, 1)
        first = enc.current_actor()
        self.assertIsNotNone(first)
        enc.advance_turn()
        second = enc.current_actor()
        self.assertNotEqual(first.id, second.id)
        # After both have gone, round advances.
        enc.advance_turn()
        self.assertEqual(enc.round_number, 2)
        self.assertEqual(enc.current_actor().id, first.id)

    def test_is_over_when_one_team_remains(self):
        grid = Grid(width=10, height=10)
        a = _goblin((0, 0), team="patrons")
        b = _orc((9, 9), team="enemies")
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        self.assertFalse(enc.is_over())
        # Knock out the orc.
        b.take_damage(b.max_hp + 5)
        b.add_condition("unconscious")
        self.assertTrue(enc.is_over())
        self.assertEqual(enc.winner_team(), "patrons")


# ---------------------------------------------------------------------------
# AoO detection
# ---------------------------------------------------------------------------


class TestAoO(unittest.TestCase):
    def test_movement_through_threatened_square_triggers_aoo(self):
        grid = Grid(width=10, height=10)
        threatener = _orc((5, 5), team="enemies")
        mover = _goblin((4, 4), team="patrons")
        grid.place(threatener)
        grid.place(mover)
        # Mover is at (4,4) which IS in threatener's threatened zone.
        # Leaving (4,4) provokes.
        triggers = aoo_triggers_for_movement(grid, mover, (4, 4))
        self.assertEqual(len(triggers), 1)
        self.assertEqual(triggers[0].id, threatener.id)

    def test_same_team_no_aoo(self):
        grid = Grid(width=10, height=10)
        ally = _orc((5, 5), team="patrons")
        mover = _goblin((4, 4), team="patrons")
        grid.place(ally)
        grid.place(mover)
        triggers = aoo_triggers_for_movement(grid, mover, (4, 4))
        self.assertEqual(triggers, [])

    def test_unconscious_threatener_does_not_aoo(self):
        grid = Grid(width=10, height=10)
        threatener = _orc((5, 5), team="enemies")
        threatener.add_condition("unconscious")
        mover = _goblin((4, 4), team="patrons")
        grid.place(threatener)
        grid.place(mover)
        triggers = aoo_triggers_for_movement(grid, mover, (4, 4))
        self.assertEqual(triggers, [])

    def test_provoking_action_triggers(self):
        grid = Grid(width=10, height=10)
        threatener = _orc((5, 5), team="enemies")
        actor = _goblin((4, 4), team="patrons")
        grid.place(threatener)
        grid.place(actor)
        triggers = aoo_triggers_for_provoking_action(grid, actor, "cast")
        self.assertEqual(len(triggers), 1)
        # An attack doesn't normally provoke.
        no_triggers = aoo_triggers_for_provoking_action(grid, actor, "attack")
        self.assertEqual(no_triggers, [])


if __name__ == "__main__":
    unittest.main()
