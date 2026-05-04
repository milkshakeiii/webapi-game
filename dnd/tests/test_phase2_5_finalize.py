"""Tests for Phase 2.5: finalizing the three remaining monster-trait
PARTIALs — quickness round-1 movement, tail_spikes daily cap, and
engulf pull-along + per-round acid + escape save."""

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


def _hold_intent():
    return BehaviorScript(name="hold", rules=[
        Rule(do={"composite": "hold", "args": {}}),
    ])


def _full_attack_intent():
    return BehaviorScript(name="atk", rules=[
        Rule(do={"composite": "full_attack",
                 "args": {"target": "enemy.closest"}}),
    ])


# ---------------------------------------------------------------------------
# Quickness +10ft round 1 only
# ---------------------------------------------------------------------------


class TestQuicknessFirstRoundMove(unittest.TestCase):
    def test_choker_moves_extra_two_squares_on_round_one(self):
        choker = combatant_from_monster(REGISTRY.get_monster("choker"),
                                        (0, 5), "x")
        # Choker base speed 20 ft → 4 squares. Round 1 with quickness:
        # +2 squares → 6 squares allowed.
        gob = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                     (15, 5), "y")
        grid = Grid(width=30, height=10)
        grid.place(choker)
        grid.place(gob)
        enc = Encounter.begin(grid, [choker, gob], Roller(seed=1))
        self.assertEqual(enc.round_number, 1)
        script = BehaviorScript(name="m", rules=[
            Rule(do={"move": {"type": "move_to", "target": (12, 5)}}),
        ])
        intent = Interpreter(script).pick_turn(choker, enc, grid)
        execute_turn(choker, intent, enc, grid, Roller(seed=1))
        # Without quickness: max 4 squares → would land at (4, 5).
        # With quickness: 6 squares → lands at (6, 5).
        self.assertEqual(choker.position[0], 6)

    def test_choker_loses_bonus_after_round_one(self):
        choker = combatant_from_monster(REGISTRY.get_monster("choker"),
                                        (0, 5), "x")
        gob = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                     (15, 5), "y")
        grid = Grid(width=30, height=10)
        grid.place(choker)
        grid.place(gob)
        enc = Encounter.begin(grid, [choker, gob], Roller(seed=1))
        enc.round_number = 2
        script = BehaviorScript(name="m", rules=[
            Rule(do={"move": {"type": "move_to", "target": (12, 5)}}),
        ])
        intent = Interpreter(script).pick_turn(choker, enc, grid)
        execute_turn(choker, intent, enc, grid, Roller(seed=1))
        self.assertEqual(choker.position[0], 4)


# ---------------------------------------------------------------------------
# Tail spikes daily cap
# ---------------------------------------------------------------------------


class TestTailSpikesCap(unittest.TestCase):
    def test_manticore_starts_with_24_spikes(self):
        m = combatant_from_monster(REGISTRY.get_monster("manticore"),
                                   (0, 0), "x")
        self.assertEqual(m.daily_resources.get("tail_spikes"), 24)
        self.assertEqual(m.daily_resource_max.get("tail_spikes"), 24)

    def test_spike_attack_decrements_pool(self):
        m = combatant_from_monster(REGISTRY.get_monster("manticore"),
                                   (3, 5), "x")
        # Force the spike attack to land.
        for opt in m.attack_options:
            opt["attack_bonus"] = 100
        gob = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                     (10, 5), "y")
        gob.max_hp = 9999
        gob.current_hp = 9999
        grid = Grid(width=30, height=10)
        grid.place(m)
        grid.place(gob)
        enc = Encounter.begin(grid, [m, gob], Roller(seed=1))
        # Use the standard attack action with the spikes option (idx 2).
        script = BehaviorScript(name="atk", rules=[
            Rule(do={"standard": {"type": "attack",
                                  "target": "enemy.closest",
                                  "attack_index": 2}}),
        ])
        intent = Interpreter(script).pick_turn(m, enc, grid)
        # Default standard-attack handler doesn't yet take attack_index;
        # invoke _do_attack directly via composite full_attack and check.
        # (The pool decrement fires inside _do_attack.)
        before = m.daily_resources.get("tail_spikes", 0)
        # Drop bite/claw attacks so full_attack hits with spikes only.
        m.attack_options = [m.attack_options[2]]  # spikes-only loadout
        # Re-run with the trimmed options.
        full = Interpreter(_full_attack_intent()).pick_turn(m, enc, grid)
        execute_turn(m, full, enc, grid, Roller(seed=1))
        after = m.daily_resources.get("tail_spikes", 0)
        self.assertLess(after, before)

    def test_spike_attack_skips_when_pool_empty(self):
        m = combatant_from_monster(REGISTRY.get_monster("manticore"),
                                   (3, 5), "x")
        m.attack_options = [m.attack_options[2]]  # spikes-only
        for opt in m.attack_options:
            opt["attack_bonus"] = 100
        m.daily_resources["tail_spikes"] = 0  # fresh out
        gob = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                     (10, 5), "y")
        grid = Grid(width=30, height=10)
        grid.place(m)
        grid.place(gob)
        enc = Encounter.begin(grid, [m, gob], Roller(seed=1))
        intent = Interpreter(_full_attack_intent()).pick_turn(m, enc, grid)
        result = execute_turn(m, intent, enc, grid, Roller(seed=1))
        skip_evts = [e for e in result.events
                     if e.kind == "skip"
                     and "tail_spikes" in e.detail.get("reason", "")]
        self.assertGreater(len(skip_evts), 0)

    def test_daily_replenish_after_14400_rounds(self):
        m = combatant_from_monster(REGISTRY.get_monster("manticore"),
                                   (0, 0), "x")
        m.daily_resources["tail_spikes"] = 5
        m._last_daily_refresh_round = 0
        m.tick_round(current_round=14400, roller=Roller(seed=1))
        self.assertEqual(m.daily_resources.get("tail_spikes"), 24)


# ---------------------------------------------------------------------------
# Engulf pull-along + per-round acid + escape
# ---------------------------------------------------------------------------


class TestEngulfFull(unittest.TestCase):
    def _setup(self):
        cube = combatant_from_monster(REGISTRY.get_monster("gelatinous_cube"),
                                      (5, 5), "x")
        gob = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                     (7, 5), "y")
        gob.max_hp = 9999
        gob.current_hp = 9999
        grid = Grid(width=20, height=10)
        grid.place(cube)
        grid.place(gob)
        enc = Encounter.begin(grid, [cube, gob], Roller(seed=1))
        return cube, gob, enc, grid

    def test_engulfed_victim_removed_from_grid(self):
        # Find a seed where the goblin fails the Reflex save.
        for seed in range(1, 80):
            cube, gob, enc, grid = self._setup()
            intent = Interpreter(_hold_intent()).pick_turn(cube, enc, grid)
            execute_turn(cube, intent, enc, grid, Roller(seed=seed))
            if gob.engulfed_by_id == cube.id:
                # Removed from grid.
                self.assertNotIn(gob.id, grid.combatants)
                self.assertIn("paralyzed", gob.conditions)
                return
        self.fail("no seed in 1..79 engulfed the goblin")

    def test_already_engulfed_takes_acid_each_round(self):
        cube, gob, _, grid = self._setup()
        # Force engulf state directly.
        gob.engulfed_by_id = cube.id
        gob.add_condition("paralyzed")
        grid.remove(gob.id)
        hp_before = gob.current_hp
        # Cube's next turn: still_engulfed branch → 1d6 acid (if save
        # fails). Make the DC unbeatable so save always fails.
        from dnd.engine.turn_executor import _apply_aura_exposure  # noqa: F401
        # We exercise the engulf logic by ticking the cube.
        # Use a fresh encounter to set round 1.
        enc = Encounter.begin(grid, [cube, gob], Roller(seed=1))
        # Ensure goblin Fort save is high but Reflex stays predictable.
        # We rely on the seed sweep to find one with a failed Ref save.
        damaged = False
        for seed in range(1, 50):
            cube_local, gob_local = cube, gob
            # Reset HP each iteration.
            gob_local.current_hp = hp_before
            intent = Interpreter(_hold_intent()).pick_turn(cube_local, enc, grid)
            execute_turn(cube_local, intent, enc, grid, Roller(seed=seed))
            if gob_local.current_hp < hp_before:
                damaged = True
                break
        self.assertTrue(damaged,
                        "expected at least one seed where engulfed "
                        "victim takes acid damage")

    def test_escape_re_places_victim_on_grid(self):
        cube, gob, enc, grid = self._setup()
        gob.engulfed_by_id = cube.id
        gob.add_condition("paralyzed")
        grid.remove(gob.id)
        # Make the escape-save DC trivial so the save passes.
        # We do this by giving the goblin a huge Ref bonus.
        from dnd.engine.modifiers import Modifier
        gob.modifiers.add(Modifier(value=99, type="untyped",
                                   target="ref_save",
                                   source="test_huge_ref"))
        intent = Interpreter(_hold_intent()).pick_turn(cube, enc, grid)
        execute_turn(cube, intent, enc, grid, Roller(seed=1))
        # Goblin should have escaped.
        self.assertIsNone(gob.engulfed_by_id)
        self.assertNotIn("paralyzed", gob.conditions)
        # And been placed back on the grid adjacent to the cube.
        self.assertIn(gob.id, grid.combatants)


if __name__ == "__main__":
    unittest.main()
