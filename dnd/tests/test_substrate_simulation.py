"""End-to-end demo for the Phase 1 DSL v2 substrate.

Runs full encounters using only the new substrate (``actions.py``):
patrons supply a ``Picker`` per actor; a tiny driver loop walks
initiative and asks picks until one team is dead. No use of the v1
``execute_turn``.

Validates that ``enumerate_legal_actions`` + ``apply_action`` are
sufficient to play out a basic combat. Phase 3 will add reactive-
interrupt picker hooks; Phase 2 will wire the v1 executor onto this
substrate via a parity harness.
"""

from __future__ import annotations

import unittest

from dnd.engine.actions import (
    Attack,
    ClosestEnemyPicker,
    EndTurn,
    GameState,
    Move,
    Picker,
    apply_action,
    enumerate_legal_actions,
    run_encounter,
)
from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid


REGISTRY = default_registry()


def _orc(pos, team):
    return combatant_from_monster(REGISTRY.get_monster("orc"), pos, team)


class TestSimpleFight(unittest.TestCase):
    def test_two_adjacent_orcs_fight_to_completion(self):
        a = _orc((5, 5), "x")
        b = _orc((6, 5), "y")
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        state = GameState(encounter=enc, grid=grid)
        pickers = {
            a.id: ClosestEnemyPicker(),
            b.id: ClosestEnemyPicker(),
        }
        log = run_encounter(state, pickers, Roller(seed=1))

        # Fight ended with at most one team standing.
        survivors_x = [c for c in (a, b)
                       if c.team == "x" and c.is_alive()
                       and "dead" not in c.conditions]
        survivors_y = [c for c in (a, b)
                       if c.team == "y" and c.is_alive()
                       and "dead" not in c.conditions]
        self.assertFalse(survivors_x and survivors_y,
                         "fight should end with one side down")
        # Some combat happened.
        attack_events = [e for e in log if "attack" in e.kind]
        self.assertGreater(len(attack_events), 0,
                           "expected at least one attack event")

    def test_distant_orcs_close_then_fight(self):
        """Demonstrates the move-then-attack chain across multiple
        decision points within a single turn — the thing v1 couldn't
        express cleanly."""
        a = _orc((1, 5), "x")
        b = _orc((10, 5), "y")  # 9 squares apart
        grid = Grid(width=20, height=10)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        state = GameState(encounter=enc, grid=grid)
        pickers = {
            a.id: ClosestEnemyPicker(),
            b.id: ClosestEnemyPicker(),
        }
        log = run_encounter(state, pickers, Roller(seed=1),
                            max_rounds=20)

        # Movement happened (the orcs closed the gap).
        move_events = [e for e in log if e.kind == "move"]
        self.assertGreater(len(move_events), 0)
        # Eventually combat resolved.
        survivors = [c for c in (a, b)
                     if c.is_alive() and "dead" not in c.conditions]
        self.assertLessEqual(len(survivors), 1)

    def test_picker_decision_history(self):
        """Verify the substrate calls the picker many times per turn,
        not once. We instrument a Picker that records every call."""
        class RecordingPicker(ClosestEnemyPicker):
            def __init__(self):
                self.calls: list = []

            def pick(self, actor, state, actions):
                self.calls.append([type(a).__name__ for a in actions])
                return super().pick(actor, state, actions)

        a = _orc((1, 5), "x")
        b = _orc((10, 5), "y")
        grid = Grid(width=20, height=10)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        state = GameState(encounter=enc, grid=grid)
        rec = RecordingPicker()
        pickers = {a.id: rec, b.id: ClosestEnemyPicker()}
        run_encounter(state, pickers, Roller(seed=1), max_rounds=5)

        # First call on round 1 should have offered Move (and Charge,
        # full attack, etc. — but not single Attack since enemy is
        # 9 squares away).
        self.assertTrue(len(rec.calls) > 0)
        first = rec.calls[0]
        self.assertIn("Move", first)
        # After picking Move, second call should NOT offer Move
        # (slot consumed).
        if len(rec.calls) > 1:
            second = rec.calls[1]
            self.assertNotIn("Move", second,
                             f"Move should be exhausted; saw {second}")


class TestCustomPicker(unittest.TestCase):
    def test_total_defense_picker_never_attacks(self):
        """Demonstrate writing a custom Picker — patron-style behavior
        spec at the picker level."""
        from dnd.engine.actions import TotalDefense

        class CowardPicker(Picker):
            def pick(self, actor, state, actions):
                # Always Total Defense if available, else Move away,
                # else End Turn.
                for a in actions:
                    if isinstance(a, TotalDefense):
                        return a
                # No attack ever.
                for a in actions:
                    if isinstance(a, Move):
                        return a
                return next(a for a in actions if isinstance(a, EndTurn))

        a = _orc((5, 5), "x")
        b = _orc((6, 5), "y")
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        state = GameState(encounter=enc, grid=grid)
        # 'a' is a coward, 'b' is a fighter.
        pickers = {a.id: CowardPicker(), b.id: ClosestEnemyPicker()}
        log = run_encounter(state, pickers, Roller(seed=1), max_rounds=3)

        # 'a' never attacked.
        a_attacks = [
            e for e in log
            if e.actor_id == a.id and "attack" in e.kind
        ]
        self.assertEqual(len(a_attacks), 0)
        # 'a' did pick Total Defense at some point.
        a_defenses = [
            e for e in log
            if e.actor_id == a.id and e.kind == "total_defense"
        ]
        self.assertGreater(len(a_defenses), 0)


if __name__ == "__main__":
    unittest.main()
