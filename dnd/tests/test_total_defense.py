"""Tests for the total defense standard action.

PF1: standard action; +4 dodge AC for one round; can't attack while
defending. The bonus expires at the start of the actor's next turn.
"""

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


def _setup():
    a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "team_a")
    b = combatant_from_monster(REGISTRY.get_monster("goblin"), (8, 5), "team_b")
    grid = Grid(width=12, height=12)
    grid.place(a)
    grid.place(b)
    enc = Encounter.begin(grid, [a, b], Roller(seed=1))
    return a, b, enc, grid


class TestTotalDefense(unittest.TestCase):
    def test_applies_plus_4_dodge_ac(self):
        a, _, enc, grid = _setup()
        ac_before = a.ac()
        script = BehaviorScript(name="defend", rules=[
            Rule(do={"slots": {"standard": {"type": "total_defense"}}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        execute_turn(a, intent, enc, grid, Roller(seed=1))
        self.assertEqual(a.ac() - ac_before, 4)

    def test_emits_event(self):
        a, _, enc, grid = _setup()
        script = BehaviorScript(name="defend", rules=[
            Rule(do={"slots": {"standard": {"type": "total_defense"}}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        events = [e for e in result.events if e.kind == "total_defense"]
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].detail["ac_bonus"], 4)

    def test_bonus_expires_next_round(self):
        a, _, enc, grid = _setup()
        ac_before = a.ac()
        script = BehaviorScript(name="defend", rules=[
            Rule(do={"slots": {"standard": {"type": "total_defense"}}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        execute_turn(a, intent, enc, grid, Roller(seed=1))
        self.assertEqual(a.ac() - ac_before, 4)
        # Tick past the bonus's expiration round.
        a.tick_round(enc.round_number + 1)
        self.assertEqual(a.ac(), ac_before)


if __name__ == "__main__":
    unittest.main()
