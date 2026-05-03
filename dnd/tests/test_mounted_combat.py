"""Tests for the mounted-combat batch — mount/dismount, rider tracking,
and lance-on-charge double damage."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import (
    _do_dismount,
    _do_mount,
    execute_turn,
)


REGISTRY = default_registry()


def _setup_pair(rider_pos=(5, 5), mount_pos=(6, 5),
                rider="goblin", mount="orc"):
    rider_c = combatant_from_monster(REGISTRY.get_monster(rider),
                                     rider_pos, "x")
    mount_c = combatant_from_monster(REGISTRY.get_monster(mount),
                                     mount_pos, "x")
    grid = Grid(width=20, height=10)
    grid.place(rider_c)
    grid.place(mount_c)
    enc = Encounter.begin(grid, [rider_c, mount_c], Roller(seed=1))
    return rider_c, mount_c, enc, grid


class TestMountAction(unittest.TestCase):
    def test_mount_links_rider_and_mount(self):
        rider, mount, enc, grid = _setup_pair()
        events: list = []
        ns = {"target": mount}
        _do_mount(rider, {"target": mount}, grid, ns, events)
        self.assertEqual(rider.mount_id, mount.id)
        self.assertEqual(mount.rider_id, rider.id)
        # Rider is at the mount's anchor.
        self.assertEqual(rider.position, mount.position)

    def test_mount_target_must_be_adjacent(self):
        rider, mount, enc, grid = _setup_pair(rider_pos=(0, 0),
                                              mount_pos=(10, 0))
        events: list = []
        ns = {"target": mount}
        _do_mount(rider, {"target": mount}, grid, ns, events)
        self.assertIsNone(rider.mount_id)
        self.assertEqual(events[-1].kind, "skip")

    def test_cannot_mount_already_carrying(self):
        rider, mount, enc, grid = _setup_pair()
        # First, link them.
        events: list = []
        _do_mount(rider, {"target": mount}, grid, {}, events)
        # Now try to mount again from another rider (use a fresh goblin).
        rider2 = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (6, 6), "x")
        grid.place(rider2)
        events2: list = []
        _do_mount(rider2, {"target": mount}, grid, {}, events2)
        self.assertIsNone(rider2.mount_id)
        self.assertEqual(events2[-1].kind, "skip")


class TestDismountAction(unittest.TestCase):
    def test_dismount_clears_link(self):
        rider, mount, enc, grid = _setup_pair()
        events: list = []
        _do_mount(rider, {"target": mount}, grid, {}, events)
        events_d: list = []
        _do_dismount(rider, {}, grid, events_d)
        self.assertIsNone(rider.mount_id)
        self.assertIsNone(mount.rider_id)
        self.assertEqual(events_d[-1].kind, "dismount")

    def test_dismount_when_not_mounted_skips(self):
        rider, mount, enc, grid = _setup_pair()
        events: list = []
        _do_dismount(rider, {}, grid, events)
        self.assertEqual(events[-1].kind, "skip")


class TestRiderFollowsMount(unittest.TestCase):
    def test_rider_position_tracks_mount_movement(self):
        rider, mount, enc, grid = _setup_pair(rider_pos=(5, 5),
                                              mount_pos=(6, 5))
        events: list = []
        _do_mount(rider, {"target": mount}, grid, {}, events)
        # Mount moves east via a simple move script.
        script = BehaviorScript(name="m", rules=[
            Rule(do={"move": {"type": "move_to", "target": (10, 5)}}),
        ])
        intent = Interpreter(script).pick_turn(mount, enc, grid)
        execute_turn(mount, intent, enc, grid, Roller(seed=1))
        # Rider's position should have followed the mount.
        self.assertEqual(rider.position, mount.position)


class TestLanceCharge(unittest.TestCase):
    def test_mounted_lance_charge_doubles_damage(self):
        # Verify the damage-doubling code path inside _do_attack by
        # directly invoking it with the charge_lance_double_damage flag
        # set. This is what _do_charge does when it sees a mounted
        # lance-wielder.
        from dnd.engine.turn_executor import _do_attack
        attacker = combatant_from_monster(REGISTRY.get_monster("orc"),
                                          (5, 5), "x")
        attacker.attack_options = [{
            "type": "melee",
            "name": "Lance",
            "weapon_id": "lance",
            "weapon_category": "martial",
            "attack_bonus": 100,  # auto-hit
            "damage": "1d8",
            "damage_bonus": 4,
            "damage_type": "P",
            "crit_range": [20, 20],
            "crit_multiplier": 3,
            "range_increment": 0,
            "wield": "two_handed",
        }]
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (6, 5), "y")
        target.max_hp = 9999
        target.current_hp = 9999
        grid = Grid(width=20, height=10)
        grid.place(attacker)
        grid.place(target)
        enc = Encounter.begin(grid, [attacker, target], Roller(seed=1))
        # Baseline single attack: no lance flag.
        events_no_flag: list = []
        target_hp_before = target.current_hp
        _do_attack(attacker, target, grid, Roller(seed=1), events_no_flag,
                   label="baseline", encounter=enc, script_options={})
        baseline_damage = target_hp_before - target.current_hp
        # Now reset and try with the flag.
        target.current_hp = target.max_hp
        events_flagged: list = []
        target_hp_before = target.current_hp
        _do_attack(attacker, target, grid, Roller(seed=1), events_flagged,
                   label="lance_charge", encounter=enc,
                   script_options={"charge_damage_multiplier": 2})
        flagged_damage = target_hp_before - target.current_hp
        # Same RNG seed → same hit roll, same damage roll → doubling
        # is visible cleanly.
        self.assertEqual(flagged_damage, baseline_damage * 2)
        # Trace should mention the doubling.
        atk_event = next(e for e in events_flagged
                         if e.kind == "lance_charge")
        trace = atk_event.detail.get("trace") or []
        self.assertTrue(
            any("×2" in line for line in trace),
            f"expected mounted charge ×2 trace line; got {trace}",
        )


if __name__ == "__main__":
    unittest.main()
