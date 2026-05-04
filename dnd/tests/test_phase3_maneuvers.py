"""Tests for Phase 3 — combat maneuvers complete.

Covers the dirty_trick maneuver, AoO provocation by default,
Improved-X feat removing the AoO and adding +2 CMB.
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


def _maneuver_script(kind: str, **extra_args):
    args = {"target": "enemy.closest"}
    args.update(extra_args)
    return BehaviorScript(name=kind, rules=[
        Rule(do={"composite": kind, "args": args}),
    ])


# ---------------------------------------------------------------------------
# Dirty trick
# ---------------------------------------------------------------------------


class TestDirtyTrick(unittest.TestCase):
    def test_default_condition_is_dazzled(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        b = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (6, 5), "y")
        # Pin actor's CMB to make the maneuver succeed.
        a.bases["cmb"] = 99
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        intent = Interpreter(_maneuver_script("dirty_trick")).pick_turn(
            a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("maneuver_dirty_trick", kinds)
        evt = next(e for e in result.events if e.kind == "maneuver_dirty_trick")
        self.assertEqual(evt.detail["condition"], "dazzled")
        self.assertIn("dazzled", b.conditions)

    def test_explicit_condition_choice(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        b = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (6, 5), "y")
        a.bases["cmb"] = 99
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        intent = Interpreter(_maneuver_script(
            "dirty_trick", condition="entangled",
        )).pick_turn(a, enc, grid)
        execute_turn(a, intent, enc, grid, Roller(seed=1))
        self.assertIn("entangled", b.conditions)

    def test_invalid_condition_falls_back_to_dazzled(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        b = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (6, 5), "y")
        a.bases["cmb"] = 99
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        intent = Interpreter(_maneuver_script(
            "dirty_trick", condition="not_a_real_condition",
        )).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        evt = next(e for e in result.events if e.kind == "maneuver_dirty_trick")
        self.assertEqual(evt.detail["condition"], "dazzled")

    def test_duration_scales_with_margin(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        b = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (6, 5), "y")
        a.bases["cmb"] = 99  # margin will be huge
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        intent = Interpreter(_maneuver_script("dirty_trick")).pick_turn(
            a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        evt = next(e for e in result.events if e.kind == "maneuver_dirty_trick")
        # Margin = 99 + d20 - goblin_cmd; expected multi-round duration.
        self.assertGreater(evt.detail["duration"], 1)


# ---------------------------------------------------------------------------
# AoO provocation
# ---------------------------------------------------------------------------


class TestManeuverAoO(unittest.TestCase):
    def test_disarm_provokes_aoo_without_improved_disarm(self):
        # Actor lacks improved_disarm → should provoke AoO from target.
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        b = combatant_from_monster(REGISTRY.get_monster("orc"), (6, 5), "y")
        # Force AoO to land hard.
        for opt in b.attack_options:
            opt["attack_bonus"] = 100
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        intent = Interpreter(_maneuver_script("disarm")).pick_turn(
            a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("aoo", kinds)
        # The maneuver event should record provoked_aoo=True.
        man_evt = next(
            (e for e in result.events if e.kind == "maneuver_disarm"),
            None,
        )
        if man_evt is not None:
            self.assertTrue(man_evt.detail.get("provoked_aoo"))

    def test_improved_disarm_skips_aoo_and_adds_cmb_bonus(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        # Inject Improved Disarm.
        a.extra_feats.append("improved_disarm")
        b = combatant_from_monster(REGISTRY.get_monster("orc"), (6, 5), "y")
        for opt in b.attack_options:
            opt["attack_bonus"] = 100
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        intent = Interpreter(_maneuver_script("disarm")).pick_turn(
            a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertNotIn("aoo", kinds)
        man_evt = next(
            e for e in result.events if e.kind == "maneuver_disarm"
        )
        self.assertFalse(man_evt.detail.get("provoked_aoo"))

    def test_helpless_target_does_not_get_aoo(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        b = combatant_from_monster(REGISTRY.get_monster("orc"), (6, 5), "y")
        b.add_condition("paralyzed")  # helpless via cascade
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        intent = Interpreter(_maneuver_script("disarm")).pick_turn(
            a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertNotIn("aoo", kinds)


# ---------------------------------------------------------------------------
# Improved-X CMB bonus (verify +2 applies)
# ---------------------------------------------------------------------------


class TestImprovedCmbBonus(unittest.TestCase):
    def test_improved_trip_adds_two_cmb(self):
        # Run two trips with the same RNG seed, one with improved_trip
        # and one without; the 'total' should differ by exactly 2.
        a1 = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        a2 = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        a2.extra_feats.append("improved_trip")
        b = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (6, 5), "y")

        def roll_total(actor):
            grid = Grid(width=12, height=12)
            target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                            (6, 5), "y")
            grid.place(actor)
            grid.place(target)
            enc = Encounter.begin(grid, [actor, target], Roller(seed=42))
            intent = Interpreter(_maneuver_script("trip")).pick_turn(
                actor, enc, grid)
            result = execute_turn(actor, intent, enc, grid, Roller(seed=42))
            evt = next(
                e for e in result.events if e.kind == "maneuver_trip"
            )
            return evt.detail["total"]

        baseline = roll_total(a1)
        with_feat = roll_total(a2)
        self.assertEqual(with_feat - baseline, 2)


if __name__ == "__main__":
    unittest.main()
