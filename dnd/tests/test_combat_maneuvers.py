"""Tests for combat maneuvers — trip / disarm / sunder / bull_rush / grapple.

Plus wolf trip-on-bite and dwarven Stability (+4 CMD vs trip / bull_rush).
"""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import (
    combatant_from_character,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import (
    _resolve_maneuver,
    execute_turn,
)


REGISTRY = default_registry()


def _setup(actor_id="orc", target_id="goblin"):
    a = combatant_from_monster(REGISTRY.get_monster(actor_id), (5, 5), "x")
    b = combatant_from_monster(REGISTRY.get_monster(target_id), (6, 5), "y")
    b.max_hp = 9999
    b.current_hp = 9999
    grid = Grid(width=12, height=12)
    grid.place(a)
    grid.place(b)
    enc = Encounter.begin(grid, [a, b], Roller(seed=1))
    return a, b, enc, grid


def _run_composite(actor, kind, target_ref, enc, grid, seed=1):
    script = BehaviorScript(name=kind, rules=[
        Rule(do={"composite": kind, "args": {"target": target_ref}}),
    ])
    intent = Interpreter(script).pick_turn(actor, enc, grid)
    return execute_turn(actor, intent, enc, grid, Roller(seed=seed))


class TestResolveManeuver(unittest.TestCase):
    def test_returns_pass_total_margin(self):
        # Override CMB / CMD synthetically so the math is predictable.
        a, b, _, _ = _setup()
        a.bases["cmb"] = 10
        b.bases["cmd"] = 12
        # Roller seed=1: first d20 roll is some natural; with CMB +10
        # most rolls clear CMD 12. Just verify the structure.
        passed, nat, total, margin = _resolve_maneuver(a, b, "trip", Roller(seed=1))
        self.assertEqual(total, nat + 10)
        self.assertEqual(margin, total - 12)


class TestTripComposite(unittest.TestCase):
    def test_successful_trip_makes_target_prone(self):
        # Force success: synthetic CMB high, CMD low.
        a, b, enc, grid = _setup()
        a.bases["cmb"] = 30
        b.bases["cmd"] = 5
        result = _run_composite(a, "trip", "enemy.closest", enc, grid)
        ev = next(e for e in result.events if e.kind == "maneuver_trip")
        self.assertTrue(ev.detail["passed"])
        self.assertIn("prone", b.conditions)

    def test_failed_trip_no_prone(self):
        a, b, enc, grid = _setup()
        a.bases["cmb"] = -50
        b.bases["cmd"] = 50
        _run_composite(a, "trip", "enemy.closest", enc, grid)
        self.assertNotIn("prone", b.conditions)


class TestBullRushPushes(unittest.TestCase):
    def test_target_moves_back(self):
        a, b, enc, grid = _setup()
        a.bases["cmb"] = 30
        b.bases["cmd"] = 5
        old_pos = b.position
        _run_composite(a, "bull_rush", "enemy.closest", enc, grid)
        self.assertNotEqual(b.position, old_pos)


class TestGrapple(unittest.TestCase):
    def test_both_grappled_on_success(self):
        a, b, enc, grid = _setup()
        a.bases["cmb"] = 30
        b.bases["cmd"] = 5
        _run_composite(a, "grapple", "enemy.closest", enc, grid)
        self.assertIn("grappled", a.conditions)
        self.assertIn("grappled", b.conditions)


class TestDisarmAndSunder(unittest.TestCase):
    def test_disarm_marks_disarmed(self):
        a, b, enc, grid = _setup()
        a.bases["cmb"] = 30
        b.bases["cmd"] = 5
        _run_composite(a, "disarm", "enemy.closest", enc, grid)
        self.assertIn("disarmed", b.conditions)

    def test_sunder_marks_weapon_broken(self):
        a, b, enc, grid = _setup()
        a.bases["cmb"] = 30
        b.bases["cmd"] = 5
        _run_composite(a, "sunder", "enemy.closest", enc, grid)
        self.assertIn("weapon_broken", b.conditions)


class TestWolfTripOnBite(unittest.TestCase):
    def test_wolf_trip_on_successful_bite(self):
        wolf = combatant_from_monster(
            REGISTRY.get_monster("wolf"), (5, 5), "x",
        )
        wolf.bases["cmb"] = 30  # ensure trip succeeds
        target = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (6, 5), "y",
        )
        target.bases["cmd"] = 5
        target.max_hp = 9999
        target.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(wolf)
        grid.place(target)
        enc = Encounter.begin(grid, [wolf, target], Roller(seed=1))

        # Try several seeds until a bite hits.
        from dnd.engine.turn_executor import _do_attack
        for seed in range(1, 60):
            target.conditions.discard("prone")
            events = []
            _do_attack(
                wolf, target, grid, Roller(seed=seed), events,
                encounter=enc,
            )
            atk = next(e for e in events if e.kind == "attack")
            if atk.detail["hit"]:
                # On hit, a trip_on_hit event should follow with the result.
                trips = [e for e in events if e.kind == "trip_on_hit"]
                self.assertEqual(len(trips), 1)
                # We forced CMB high vs CMD low, so trip should pass
                # and target should be prone.
                self.assertTrue(trips[0].detail["passed"])
                self.assertIn("prone", target.conditions)
                return
        self.skipTest("no successful bite in 60 seeds")

    def test_wolf_no_trip_on_miss(self):
        wolf = combatant_from_monster(
            REGISTRY.get_monster("wolf"), (5, 5), "x",
        )
        target = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (6, 5), "y",
        )
        target.max_hp = 9999
        target.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(wolf)
        grid.place(target)
        enc = Encounter.begin(grid, [wolf, target], Roller(seed=1))

        from dnd.engine.turn_executor import _do_attack
        for seed in range(1, 60):
            events = []
            # Override goblin AC to make sure misses happen.
            wolf.attack_options[0]["attack_bonus"] = -50
            _do_attack(
                wolf, target, grid, Roller(seed=seed), events,
                encounter=enc,
            )
            atk = next(e for e in events if e.kind == "attack")
            if not atk.detail["hit"]:
                trips = [e for e in events if e.kind == "trip_on_hit"]
                self.assertEqual(trips, [])
                return
        self.skipTest("no miss in 60 seeds")


class TestDwarvenStability(unittest.TestCase):
    def test_dwarf_cmd_higher_against_trip(self):
        req = CharacterRequest.from_dict({
            "name": "Throgar", "race": "dwarf", "class": "fighter",
            "alignment": "lawful_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 16, "dex": 14, "con": 14,
                           "int": 10, "wis": 10, "cha": 10}},
            "feats": ["power_attack"],
            "skill_ranks": {"climb": 1, "swim": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "cleave"},
        })
        char = create_character(req, REGISTRY)
        dwarf = combatant_from_character(char, REGISTRY, (0, 0), "x")
        baseline = dwarf.cmd()
        vs_trip = dwarf.cmd(context={"maneuver": "trip"})
        vs_bullrush = dwarf.cmd(context={"maneuver": "bull_rush"})
        vs_disarm = dwarf.cmd(context={"maneuver": "disarm"})
        self.assertEqual(vs_trip - baseline, 4)
        self.assertEqual(vs_bullrush - baseline, 4)
        self.assertEqual(vs_disarm - baseline, 0)


if __name__ == "__main__":
    unittest.main()
