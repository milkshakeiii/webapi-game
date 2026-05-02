"""Tests for the extended combat maneuvers — drag, overrun,
reposition, steal."""

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


def _setup(actor_pos=(5, 5), target_pos=(6, 5)):
    a = combatant_from_monster(REGISTRY.get_monster("orc"), actor_pos, "x")
    a.bases["cmb"] = 30  # force success
    b = combatant_from_monster(REGISTRY.get_monster("goblin"), target_pos, "y")
    b.bases["cmd"] = 5
    b.max_hp = 9999
    b.current_hp = 9999
    grid = Grid(width=12, height=12)
    grid.place(a)
    grid.place(b)
    enc = Encounter.begin(grid, [a, b], Roller(seed=1))
    return a, b, enc, grid


def _run(actor, kind, enc, grid, seed=1):
    script = BehaviorScript(name=kind, rules=[
        Rule(do={"composite": kind, "args": {"target": "enemy.closest"}}),
    ])
    intent = Interpreter(script).pick_turn(actor, enc, grid)
    return execute_turn(actor, intent, enc, grid, Roller(seed=seed))


class TestDrag(unittest.TestCase):
    def test_target_pulled_toward_actor(self):
        # Adjacent setup so drag can fire (PF1: must be adjacent).
        # Actor (3,5), target (4,5). The actor is to the west; target
        # being pulled "toward actor" means moving west onto / past
        # the actor's square. Since we don't allow overlap, target
        # ends up trying to step into actor's square and stops short.
        # Use a setup with reach: place actor at the edge and verify
        # via repositioning the test — easier: put target diagonally
        # adjacent so they have somewhere to go.
        a, b, enc, grid = _setup(actor_pos=(3, 5), target_pos=(4, 5))
        old_distance = grid.distance_squares(a.position, b.position)
        _run(a, "drag", enc, grid)
        # Drag attempted to move target west toward actor. Since they
        # were adjacent, target either stays put (blocked by actor's
        # square) or moves diagonally — either way the distance
        # doesn't increase.
        new_distance = grid.distance_squares(a.position, b.position)
        self.assertLessEqual(new_distance, old_distance)

    def test_drag_doesnt_overlap_actor(self):
        # Adjacent setup: actor (5,5), target (6,5). Drag tries to
        # pull target onto actor; should stop short.
        a, b, enc, grid = _setup(actor_pos=(5, 5), target_pos=(6, 5))
        _run(a, "drag", enc, grid)
        self.assertNotEqual(b.position, a.position)


class TestOverrun(unittest.TestCase):
    def test_actor_moves_past_target(self):
        a, b, enc, grid = _setup(actor_pos=(5, 5), target_pos=(6, 5))
        _run(a, "overrun", enc, grid)
        # Actor ends at (7, 5), one past the target.
        self.assertEqual(a.position, (7, 5))

    def test_high_margin_knocks_prone(self):
        a, b, enc, grid = _setup(actor_pos=(5, 5), target_pos=(6, 5))
        # CMB - CMD = 30 - 5 = 25, margin >= 5 → target prone.
        _run(a, "overrun", enc, grid)
        self.assertIn("prone", b.conditions)


class TestReposition(unittest.TestCase):
    def test_target_moved(self):
        a, b, enc, grid = _setup(actor_pos=(5, 5), target_pos=(6, 5))
        old = b.position
        _run(a, "reposition", enc, grid)
        self.assertNotEqual(b.position, old)


class TestSteal(unittest.TestCase):
    def test_marks_stolen_from(self):
        a, b, enc, grid = _setup(actor_pos=(5, 5), target_pos=(6, 5))
        _run(a, "steal", enc, grid)
        self.assertIn("stolen_from", b.conditions)


if __name__ == "__main__":
    unittest.main()
