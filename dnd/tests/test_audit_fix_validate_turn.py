"""Tests for audit fix #2: validate_turn now runs on the executor path.

Before: only unit tests called validate_turn; the live executor would
silently run any combination of slots a DSL script produced. The fix
threads validation into execute_turn, so invalid intents skip with a
clear ``invalid_turn`` reason instead of running.
"""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import TurnIntent
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import _intent_to_turn, execute_turn


REGISTRY = default_registry()


def _orc(pos=(5, 5), team="x"):
    return combatant_from_monster(REGISTRY.get_monster("orc"), pos, team)


def _run(actor, do, grid, enc):
    intent = TurnIntent(rule_index=0, do=do, namespace={})
    return execute_turn(actor, intent, enc, grid, Roller(seed=1))


class TestExecutorRunsValidation(unittest.TestCase):
    def test_move_plus_5ft_step_is_rejected(self):
        """A slots dict with movement-move AND a 5-ft step is illegal
        per RAW; the executor should skip with invalid_turn."""
        actor = _orc()
        grid = Grid(width=12, height=12)
        grid.place(actor)
        enc = Encounter.begin(grid, [actor], Roller(seed=1))

        do = {
            "slots": {
                "move": {"type": "move_to", "target": (4, 5)},
                "five_foot_step": (6, 5),
            },
        }
        result = _run(actor, do, grid, enc)
        kinds = [e.kind for e in result.events]
        self.assertIn("skip", kinds)
        skip = next(e for e in result.events if e.kind == "skip")
        self.assertEqual(skip.detail.get("reason"), "invalid_turn")
        self.assertIn("five_foot_step", skip.detail.get("detail", "").lower())

    def test_paralyzed_actor_cannot_act(self):
        """A paralyzed actor's turn is rejected by the validator."""
        actor = _orc()
        actor.add_condition("paralyzed")
        target = _orc((6, 5), "y")
        grid = Grid(width=12, height=12)
        grid.place(actor)
        grid.place(target)
        enc = Encounter.begin(grid, [actor, target], Roller(seed=1))

        do = {
            "slots": {
                "standard": {"type": "attack", "target": target},
            },
        }
        result = _run(actor, do, grid, enc)
        skip = next(e for e in result.events if e.kind == "skip")
        self.assertEqual(skip.detail.get("reason"), "invalid_turn")

    def test_dazed_actor_cannot_act(self):
        actor = _orc()
        actor.add_condition("dazed")
        target = _orc((6, 5), "y")
        grid = Grid(width=12, height=12)
        grid.place(actor)
        grid.place(target)
        enc = Encounter.begin(grid, [actor, target], Roller(seed=1))

        do = {
            "slots": {"standard": {"type": "attack", "target": target}},
        }
        result = _run(actor, do, grid, enc)
        skip = next(e for e in result.events if e.kind == "skip")
        self.assertEqual(skip.detail.get("reason"), "invalid_turn")

    def test_valid_slots_form_runs_normally(self):
        """A well-formed slots dict (move + standard) runs as before."""
        actor = _orc()
        target = _orc((7, 5), "y")
        grid = Grid(width=12, height=12)
        grid.place(actor)
        grid.place(target)
        enc = Encounter.begin(grid, [actor, target], Roller(seed=1))

        do = {
            "slots": {
                "move": {"type": "move_toward", "target": target},
                "standard": {"type": "attack", "target": target},
            },
        }
        result = _run(actor, do, grid, enc)
        kinds = [e.kind for e in result.events]
        # No invalid_turn skip; normal events present.
        invalid = [e for e in result.events
                   if e.kind == "skip" and e.detail.get("reason") == "invalid_turn"]
        self.assertEqual(invalid, [], f"unexpected validation skip; events={kinds}")

    def test_full_round_composite_charge_validates_ok(self):
        """A charge composite is mapped to the full_round slot for
        validation and runs through normally."""
        actor = _orc()
        target = _orc((9, 5), "y")
        grid = Grid(width=20, height=10)
        grid.place(actor)
        grid.place(target)
        enc = Encounter.begin(grid, [actor, target], Roller(seed=1))

        do = {"composite": "charge", "args": {"target": target}}
        result = _run(actor, do, grid, enc)
        invalid = [e for e in result.events
                   if e.kind == "skip" and e.detail.get("reason") == "invalid_turn"]
        self.assertEqual(invalid, [],
                         f"charge unexpectedly rejected: {result.events}")


class TestIntentToTurn(unittest.TestCase):
    def test_charge_routes_to_full_round_slot(self):
        do = {"composite": "charge", "args": {"target": "x"}}
        t = _intent_to_turn(do)
        self.assertIsNotNone(t.full_round)
        self.assertIsNone(t.standard)
        self.assertEqual(t.full_round["composite"], "charge")

    def test_cast_routes_to_standard_slot(self):
        do = {"composite": "cast", "args": {"spell": "bless"}}
        t = _intent_to_turn(do)
        self.assertIsNotNone(t.standard)
        self.assertIsNone(t.full_round)
        self.assertEqual(t.standard["composite"], "cast")

    def test_rage_start_does_not_consume_a_slot(self):
        """rage_start is a free composite — no Turn slots populated."""
        do = {"composite": "rage_start", "args": {}}
        t = _intent_to_turn(do)
        self.assertIsNone(t.full_round)
        self.assertIsNone(t.standard)
        self.assertIsNone(t.move)
        self.assertEqual(t.free, ())

    def test_slots_form_passthrough(self):
        do = {"slots": {"standard": {"type": "attack"},
                        "move": {"type": "move_to", "target": (0, 0)}}}
        t = _intent_to_turn(do)
        self.assertEqual(t.standard["type"], "attack")
        self.assertEqual(t.move["type"], "move_to")

    def test_inline_slots_form(self):
        """Plain dict with slot keys (no ``slots`` wrapper)."""
        do = {"standard": {"type": "attack"},
              "move": {"type": "move_to", "target": (0, 0)}}
        t = _intent_to_turn(do)
        self.assertEqual(t.standard["type"], "attack")
        self.assertEqual(t.move["type"], "move_to")


if __name__ == "__main__":
    unittest.main()
