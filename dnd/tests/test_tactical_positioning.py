"""Tests for Batch 12 tactical positioning: reach weapons, difficult
terrain, concealment, greater/total cover."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid, difficult, wall
from dnd.engine.turn_executor import _do_attack, execute_turn


REGISTRY = default_registry()


class TestReachWeapons(unittest.TestCase):
    def test_longspear_threatens_at_10ft_not_5ft(self):
        # Medium creature wielding longspear: threatens distance 2,
        # NOT distance 1.
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        a.attack_options = [{
            "type": "melee", "name": "Longspear", "weapon_id": "longspear",
            "weapon_category": "simple", "attack_bonus": 5, "damage": "1d8",
            "damage_bonus": 0, "damage_type": "P", "crit_range": [20, 20],
            "crit_multiplier": 3, "range_increment": 0, "wield": "two_handed",
        }]
        grid = Grid(width=20, height=10)
        grid.place(a)
        threatened = grid.threatened_squares(a)
        # Adjacent (5+1, 5) is NOT threatened.
        self.assertNotIn((6, 5), threatened)
        # Two squares away (5+2, 5) IS threatened.
        self.assertIn((7, 5), threatened)

    def test_no_reach_weapon_threatens_adjacent(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        # Default orc loadout uses falchion (no reach).
        grid = Grid(width=20, height=10)
        grid.place(a)
        threatened = grid.threatened_squares(a)
        self.assertIn((6, 5), threatened)
        # 2 squares away NOT threatened (Medium creature reach=1).
        self.assertNotIn((7, 5), threatened)

    def test_natural_attack_monster_threatens_normally(self):
        # Goblin has no weapon_id on its attacks (natural-style).
        # Should fall back to "no reach weapon" → adjacent threat.
        g = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (5, 5), "x")
        grid = Grid(width=20, height=10)
        grid.place(g)
        threatened = grid.threatened_squares(g)
        self.assertIn((6, 5), threatened)


class TestDifficultTerrain(unittest.TestCase):
    def test_walking_through_difficult_terrain_costs_double(self):
        # Speed 30 = 6 squares. With 1 difficult-terrain square in the
        # path, the actor moves only 5 squares (the difficult one
        # consumes 2 of the 6).
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 5), "x")
        grid = Grid(width=20, height=10)
        # Place a single difficult square at (3, 5).
        grid.features[(3, 5)] = difficult()
        grid.place(a)
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (15, 5), "y")
        grid.place(target)
        enc = Encounter.begin(grid, [a, target], Roller(seed=1))
        script = BehaviorScript(name="m", rules=[
            Rule(do={"move": {"type": "move_to", "target": (10, 5)}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        execute_turn(a, intent, enc, grid, Roller(seed=1))
        # Without difficult terrain, orc would have reached (6, 5).
        # With one difficult square, max reach is (5, 5).
        self.assertEqual(a.position[0], 5)


class TestConcealment(unittest.TestCase):
    def test_concealment_can_convert_hit_to_miss(self):
        # Set up an attacker with auto-hit and target with 50%
        # concealment. Across many seeds, ~half should miss.
        misses = 0
        attempts = 30
        for seed in range(1, attempts + 1):
            a = combatant_from_monster(REGISTRY.get_monster("orc"),
                                       (5, 5), "x")
            for opt in a.attack_options:
                opt["attack_bonus"] = 100
            t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                       (6, 5), "y")
            t.concealment = 50
            t.max_hp = 9999
            t.current_hp = 9999
            grid = Grid(width=12, height=12)
            grid.place(a)
            grid.place(t)
            enc = Encounter.begin(grid, [a, t], Roller(seed=seed))
            before = t.current_hp
            events: list = []
            _do_attack(a, t, grid, Roller(seed=seed), events,
                       label="atk", encounter=enc, script_options={})
            if t.current_hp == before:
                misses += 1
        # Roughly half should miss (allow wide tolerance).
        self.assertGreater(misses, 5)
        self.assertLess(misses, attempts - 5)

    def test_no_concealment_always_lands(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        for opt in a.attack_options:
            opt["attack_bonus"] = 100
        t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (6, 5), "y")
        # Default concealment = 0.
        t.max_hp = 9999
        t.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(t)
        enc = Encounter.begin(grid, [a, t], Roller(seed=1))
        for seed in range(1, 11):
            t.current_hp = t.max_hp
            events: list = []
            _do_attack(a, t, grid, Roller(seed=seed), events,
                       label="atk", encounter=enc, script_options={})
            self.assertLess(t.current_hp, t.max_hp)


class TestGreaterCover(unittest.TestCase):
    def _setup(self, walls_in_line: int):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (1, 5), "x")
        for opt in a.attack_options:
            opt["attack_bonus"] = 0  # we'll inspect cover bonus directly
        t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (10, 5), "y")
        grid = Grid(width=20, height=10)
        # Place walls in the line.
        for i in range(walls_in_line):
            grid.features[(3 + i, 5)] = wall()
        grid.place(a)
        grid.place(t)
        return a, t, grid

    def test_no_walls_no_cover(self):
        from dnd.engine.turn_executor import _cover_ac_bonus
        a, t, grid = self._setup(0)
        self.assertEqual(_cover_ac_bonus(a, t, grid, is_ranged=True), 0)

    def test_one_wall_hard_cover_plus_4(self):
        from dnd.engine.turn_executor import _cover_ac_bonus
        a, t, grid = self._setup(1)
        self.assertEqual(_cover_ac_bonus(a, t, grid, is_ranged=True), 4)

    def test_two_walls_greater_cover_plus_8(self):
        from dnd.engine.turn_executor import _cover_ac_bonus
        a, t, grid = self._setup(2)
        self.assertEqual(_cover_ac_bonus(a, t, grid, is_ranged=True), 8)


class TestTotalCover(unittest.TestCase):
    def test_three_or_more_walls_blocks_ranged_attack(self):
        # Ranged attacks should fail outright with total cover.
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (1, 5), "x")
        # Equip a ranged weapon manually.
        a.attack_options = [{
            "type": "ranged", "name": "Longbow", "weapon_id": "longbow",
            "weapon_category": "martial", "attack_bonus": 5, "damage": "1d8",
            "damage_bonus": 0, "damage_type": "P", "crit_range": [20, 20],
            "crit_multiplier": 3, "range_increment": 100, "wield": "two_handed",
        }]
        t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (10, 5), "y")
        grid = Grid(width=20, height=10)
        # 3+ walls in line.
        for i in range(3):
            grid.features[(3 + i, 5)] = wall()
        grid.place(a)
        grid.place(t)
        enc = Encounter.begin(grid, [a, t], Roller(seed=1))
        events: list = []
        _do_attack(a, t, grid, Roller(seed=1), events,
                   label="ranged", encounter=enc, script_options={})
        skip_events = [e for e in events if e.kind == "skip"]
        self.assertGreater(len(skip_events), 0)
        self.assertIn("total cover", skip_events[0].detail.get("reason", ""))


if __name__ == "__main__":
    unittest.main()
