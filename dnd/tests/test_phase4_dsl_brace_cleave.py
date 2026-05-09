"""DSL v2 Phase 4 second slice: ``react: brace`` and ``react: cleave``
end-to-end.

Mirrors the Phase 3 Python-Picker tests in
``test_phase3_reactive_brace_cleave.py`` but drives behavior from a
``BehaviorScript`` registered via ``register_script_pickers``.
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
from dnd.engine.inventory import make_weapon_item
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


def _orc(pos, team):
    return combatant_from_monster(REGISTRY.get_monster("orc"), pos, team)


# ---------------------------------------------------------------------------
# Brace
# ---------------------------------------------------------------------------


def _setup_brace_vs_charge():
    defender = _orc((8, 5), "x")
    defender.attack_options = [{
        "type": "melee", "name": "Longspear",
        "weapon_id": "longspear", "weapon_category": "simple",
        "attack_bonus": 100, "damage": "1d8", "damage_bonus": 4,
        "damage_type": "P", "crit_range": [20, 20],
        "crit_multiplier": 3, "range_increment": 0,
        "wield": "two_handed",
    }]
    defender.held_items["main_hand"] = make_weapon_item(
        "longspear", REGISTRY,
    )
    attacker = _orc((3, 5), "y")
    grid = Grid(width=20, height=10)
    grid.place(defender)
    grid.place(attacker)
    enc = Encounter.begin(grid, [defender, attacker], Roller(seed=1))
    ready_script = BehaviorScript(name="rb", rules=[
        Rule(do={"composite": "ready_brace", "args": {}}),
    ])
    intent = Interpreter(ready_script).pick_turn(defender, enc, grid)
    execute_turn(defender, intent, enc, grid, Roller(seed=1))
    return defender, attacker, grid, enc


def _charge(attacker, enc, grid):
    script = BehaviorScript(name="ch", rules=[
        Rule(do={"composite": "charge",
                 "args": {"target": "enemy.closest"}}),
    ])
    intent = Interpreter(script).pick_turn(attacker, enc, grid)
    return execute_turn(attacker, intent, enc, grid, Roller(seed=1))


class TestDSLPassBrace(unittest.TestCase):
    def test_dsl_pass_brace_keeps_condition(self):
        defender, attacker, grid, enc = _setup_brace_vs_charge()
        # Defender's reactive script: always pass brace.
        defender_script = BehaviorScript(name="conserve", rules=[
            Rule(react="brace", do={"type": "pass_brace"}),
        ])
        register_script_pickers(defender, defender_script, enc)
        result = _charge(attacker, enc, grid)
        kinds = [e.kind for e in result.events]
        self.assertNotIn("brace_attack", kinds)
        self.assertIn("brace_pass", kinds)
        self.assertIn("bracing", defender.conditions)

    def test_conditional_brace_on_charger_hp(self):
        defender, attacker, grid, enc = _setup_brace_vs_charge()
        # Brace only on healthy chargers (>50% HP). Bring the
        # charger to 1 HP to force a Pass.
        attacker.current_hp = 1
        defender_script = BehaviorScript(name="hp_gate", rules=[
            Rule(react="brace", when="charger.hp_pct < 0.5",
                 do={"type": "pass_brace"}),
            Rule(react="brace", do={"type": "brace"}),
        ])
        register_script_pickers(defender, defender_script, enc)
        result = _charge(attacker, enc, grid)
        kinds = [e.kind for e in result.events]
        self.assertIn("brace_pass", kinds)
        self.assertIn("bracing", defender.conditions)


# ---------------------------------------------------------------------------
# Cleave continuation
# ---------------------------------------------------------------------------


def _setup_cleave():
    cleaver = _orc((5, 5), "x")
    cleaver.extra_feats = ["cleave"]
    cleaver.attack_options = [{
        "type": "melee", "name": "Test Sword",
        "weapon_id": "longsword", "weapon_category": "martial",
        "attack_bonus": 100, "damage": "1d6", "damage_bonus": 4,
        "damage_type": "S", "crit_range": [20, 20],
        "crit_multiplier": 2, "range_increment": 0,
    }]
    primary = _orc((6, 5), "y")
    primary.max_hp = primary.current_hp = 9999
    sec_a = _orc((4, 5), "y")
    sec_b = _orc((5, 4), "y")
    grid = Grid(width=12, height=12)
    grid.place(cleaver)
    grid.place(primary)
    grid.place(sec_a)
    grid.place(sec_b)
    enc = Encounter.begin(grid, [cleaver, primary, sec_a, sec_b],
                          Roller(seed=1))
    return cleaver, primary, sec_a, sec_b, grid, enc


def _cleave(cleaver, primary, enc, grid):
    script = BehaviorScript(name="cleave", rules=[
        Rule(do={"composite": "cleave", "args": {"target": primary}}),
    ])
    intent = Interpreter(script).pick_turn(cleaver, enc, grid)
    return execute_turn(cleaver, intent, enc, grid, Roller(seed=1))


class TestDSLCleaveContinuation(unittest.TestCase):
    def test_dsl_pass_cleave_skips_continuation(self):
        cleaver, primary, sec_a, sec_b, grid, enc = _setup_cleave()
        cleaver_script = BehaviorScript(name="single_swing", rules=[
            Rule(react="cleave", do={"type": "pass_cleave"}),
        ])
        register_script_pickers(cleaver, cleaver_script, enc)
        before_a = sec_a.current_hp
        before_b = sec_b.current_hp
        result = _cleave(cleaver, primary, enc, grid)
        kinds = [e.kind for e in result.events]
        self.assertNotIn("cleave_secondary", kinds)
        self.assertEqual(sec_a.current_hp, before_a)
        self.assertEqual(sec_b.current_hp, before_b)

    def test_dsl_cleave_to_with_target_expression(self):
        """Patron uses an expression like 'enemy.lowest_hp' as the
        cleave secondary target. Set sec_b to be the lowest-HP enemy
        so the picker should land on it."""
        cleaver, primary, sec_a, sec_b, grid, enc = _setup_cleave()
        primary.current_hp = 9999  # already set; keep it high
        sec_a.current_hp = 999
        sec_b.current_hp = 1  # lowest
        cleaver_script = BehaviorScript(name="finishing_blow", rules=[
            Rule(react="cleave",
                 do={"type": "cleave_to", "target": "enemy.lowest_hp"}),
        ])
        register_script_pickers(cleaver, cleaver_script, enc)
        before_a = sec_a.current_hp
        before_b_pre = sec_b.current_hp
        _cleave(cleaver, primary, enc, grid)
        # Secondary B (lowest HP) was the target; A was untouched.
        self.assertEqual(sec_a.current_hp, before_a)
        self.assertLess(sec_b.current_hp, before_b_pre)


if __name__ == "__main__":
    unittest.main()
