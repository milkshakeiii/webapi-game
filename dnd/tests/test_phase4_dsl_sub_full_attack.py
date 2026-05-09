"""DSL v2 Phase 4: ``sub: full_attack`` end-to-end.

Patrons can intervene between iteratives in a full-attack chain:

    rules:
      - sub: full_attack
        when: current_target.hp_pct < 0.1
        do: end_full_attack
      - sub: full_attack
        do: continue_full_attack

Useful for things like "stop hitting a near-dead foe; save the
follow-up swings for next round" or "always end after one iterative
to conserve a per-attack resource".

Default behavior (no picker / no matching rule) preserves v1: keep
swinging while the target is alive, stop when they go down.
"""

from __future__ import annotations

import unittest

from dnd.engine.actions import register_script_pickers
from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


def _orc(pos, team):
    return combatant_from_monster(REGISTRY.get_monster("orc"), pos, team)


def _setup_high_bab_attacker():
    """BAB 11 → 3 iteratives. Auto-hit weapon to make outcomes
    deterministic. Tank target with lots of HP so it doesn't die."""
    attacker = _orc((5, 5), "x")
    attacker.bases["bab"] = 11
    attacker.attack_options = [{
        "type": "melee", "name": "Test Sword",
        "weapon_id": "longsword", "weapon_category": "martial",
        "attack_bonus": 100, "damage": "1d6", "damage_bonus": 4,
        "damage_type": "S", "crit_range": [20, 20],
        "crit_multiplier": 2, "range_increment": 0,
    }]
    target = _orc((6, 5), "y")
    target.max_hp = target.current_hp = 9999
    grid = Grid(width=12, height=12)
    grid.place(attacker)
    grid.place(target)
    enc = Encounter.begin(grid, [attacker, target], Roller(seed=1))
    return attacker, target, grid, enc


def _full_attack(attacker, target, enc, grid):
    script = BehaviorScript(name="fa", rules=[
        Rule(do={"composite": "full_attack",
                 "args": {"target": target}}),
    ])
    intent = Interpreter(script).pick_turn(attacker, enc, grid)
    return execute_turn(attacker, intent, enc, grid, Roller(seed=1))


def _count_iteratives(events) -> int:
    return sum(1 for e in events if e.kind.startswith("full_attack_"))


class TestDefaultSubFullAttack(unittest.TestCase):
    def test_default_runs_all_iteratives_against_live_target(self):
        attacker, target, grid, enc = _setup_high_bab_attacker()
        result = _full_attack(attacker, target, enc, grid)
        # No picker, target stays alive — should run all 3 iteratives.
        self.assertEqual(_count_iteratives(result.events), 3)


class TestEndFullAttackEarly(unittest.TestCase):
    def test_dsl_can_end_after_first_iterative(self):
        attacker, target, grid, enc = _setup_high_bab_attacker()
        # Always end after the first iterative.
        script = BehaviorScript(name="single_swing", rules=[
            Rule(sub="full_attack", do={"type": "end_full_attack"}),
        ])
        register_script_pickers(attacker, script, enc)
        result = _full_attack(attacker, target, enc, grid)
        # Only iterative 1 fired.
        self.assertEqual(_count_iteratives(result.events), 1)


class TestConditionalEnd(unittest.TestCase):
    def test_continue_while_target_high_hp_then_end(self):
        attacker, target, grid, enc = _setup_high_bab_attacker()
        # End early when target is below 10% HP, otherwise continue.
        # Each iterative does ~5 damage. Target HP=9999 means
        # always above 10% — picker should always Continue.
        script = BehaviorScript(name="finisher", rules=[
            Rule(sub="full_attack",
                 when="current_target.hp_pct < 0.1",
                 do={"type": "end_full_attack"}),
            Rule(sub="full_attack",
                 do={"type": "continue_full_attack"}),
        ])
        register_script_pickers(attacker, script, enc)
        result = _full_attack(attacker, target, enc, grid)
        # All 3 iteratives ran (target HP stays >> 10%).
        self.assertEqual(_count_iteratives(result.events), 3)


class TestEndOnDeadTargetIsDefault(unittest.TestCase):
    def test_default_ends_when_target_dies_mid_chain(self):
        attacker, target, grid, enc = _setup_high_bab_attacker()
        # Make target fragile so the first iterative kills it.
        target.max_hp = 1
        target.current_hp = 1
        # No picker — default behavior should stop after kill.
        result = _full_attack(attacker, target, enc, grid)
        # Just iterative 1 fired (default break-on-death).
        self.assertEqual(_count_iteratives(result.events), 1)


if __name__ == "__main__":
    unittest.main()
