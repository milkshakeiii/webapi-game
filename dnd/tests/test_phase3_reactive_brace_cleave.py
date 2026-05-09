"""DSL v2 Phase 3.2 + 3.3: brace and cleave-continuation as picker
decisions.

Brace: when a charge ends adjacent to a wielder with the ``bracing``
condition + a brace-flagged weapon, the bracer's registered Picker
chooses between ``Brace`` (spring it, ×2 damage, condition consumed)
and ``PassBrace`` (let the charge through, condition stays for a
later trigger this round). Default: Brace.

Cleave continuation: on a successful primary cleave hit, the cleaver's
Picker chooses among ``CleaveTo(secondary_id)`` (one per adjacent
foe excluding the primary) and ``PassCleave``. Default: first
adjacent foe (matches v1's hardcoded behavior)."""

from __future__ import annotations

import unittest

from dnd.engine.actions import (
    Brace,
    CleaveTo,
    PassBrace,
    PassCleave,
    Picker,
)
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
        "weapon_id": "longspear",
        "weapon_category": "simple",
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
    # Defender readies brace.
    ready_script = BehaviorScript(name="rb", rules=[
        Rule(do={"composite": "ready_brace", "args": {}}),
    ])
    intent = Interpreter(ready_script).pick_turn(defender, enc, grid)
    execute_turn(defender, intent, enc, grid, Roller(seed=1))
    return defender, attacker, grid, enc


class TestBraceDefault(unittest.TestCase):
    def test_default_picker_springs_brace(self):
        defender, attacker, grid, enc = _setup_brace_vs_charge()
        # Charge with no picker registered — default = Brace.
        charge_script = BehaviorScript(name="ch", rules=[
            Rule(do={"composite": "charge",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(charge_script).pick_turn(attacker, enc, grid)
        result = execute_turn(attacker, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("brace_attack", kinds)
        # Bracing was consumed.
        self.assertNotIn("bracing", defender.conditions)


class _PassBracePicker(Picker):
    def pick(self, actor, state, actions):
        for a in actions:
            if isinstance(a, PassBrace):
                return a
        return actions[0]


class TestBracePass(unittest.TestCase):
    def test_pass_picker_skips_brace_and_keeps_condition(self):
        defender, attacker, grid, enc = _setup_brace_vs_charge()
        enc.pickers[defender.id] = _PassBracePicker()
        charge_script = BehaviorScript(name="ch", rules=[
            Rule(do={"composite": "charge",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(charge_script).pick_turn(attacker, enc, grid)
        result = execute_turn(attacker, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertNotIn("brace_attack", kinds)
        self.assertIn("brace_pass", kinds)
        # bracing condition remains for a later trigger this round.
        self.assertIn("bracing", defender.conditions)


# ---------------------------------------------------------------------------
# Cleave continuation
# ---------------------------------------------------------------------------


def _setup_cleave():
    """Cleaver flanked by two foes; primary at (6,5), secondary at
    (4,5). Cleaver has the cleave feat."""
    cleaver = _orc((5, 5), "x")
    cleaver.extra_feats = ["cleave"]
    # Auto-hit weapon to guarantee primary connects.
    cleaver.attack_options = [{
        "type": "melee", "name": "Test Sword",
        "weapon_id": "longsword",
        "weapon_category": "martial",
        "attack_bonus": 100, "damage": "1d6", "damage_bonus": 4,
        "damage_type": "S", "crit_range": [20, 20],
        "crit_multiplier": 2, "range_increment": 0,
    }]
    primary = _orc((6, 5), "y")
    primary.max_hp = primary.current_hp = 9999  # don't die from primary
    secondary_a = _orc((4, 5), "y")
    secondary_b = _orc((5, 4), "y")
    grid = Grid(width=12, height=12)
    grid.place(cleaver)
    grid.place(primary)
    grid.place(secondary_a)
    grid.place(secondary_b)
    enc = Encounter.begin(
        grid, [cleaver, primary, secondary_a, secondary_b],
        Roller(seed=1),
    )
    return cleaver, primary, secondary_a, secondary_b, grid, enc


def _cleave(cleaver, primary, enc, grid):
    script = BehaviorScript(name="cleave", rules=[
        Rule(do={"composite": "cleave", "args": {"target": primary}}),
    ])
    intent = Interpreter(script).pick_turn(cleaver, enc, grid)
    return execute_turn(cleaver, intent, enc, grid, Roller(seed=1))


class TestCleaveDefault(unittest.TestCase):
    def test_default_picks_first_adjacent_foe(self):
        cleaver, primary, sec_a, sec_b, grid, enc = _setup_cleave()
        result = _cleave(cleaver, primary, enc, grid)
        kinds = [e.kind for e in result.events]
        # Primary + secondary attacks both fired.
        self.assertIn("cleave_primary", kinds)
        self.assertIn("cleave_secondary", kinds)


class _PreferCleaveBPicker(Picker):
    """Prefer secondary B over A. Picker pattern-matches on the
    target_id field."""

    def __init__(self, prefer_id):
        self.prefer_id = prefer_id

    def pick(self, actor, state, actions):
        for a in actions:
            if isinstance(a, CleaveTo) and a.target_id == self.prefer_id:
                return a
        # Fall back to first.
        for a in actions:
            if isinstance(a, CleaveTo):
                return a
        return actions[-1]


class TestCleavePicker(unittest.TestCase):
    def test_picker_can_choose_secondary(self):
        cleaver, primary, sec_a, sec_b, grid, enc = _setup_cleave()
        enc.pickers[cleaver.id] = _PreferCleaveBPicker(sec_b.id)
        before_a = sec_a.current_hp
        before_b = sec_b.current_hp
        _cleave(cleaver, primary, enc, grid)
        # Secondary B took damage; A did not.
        self.assertEqual(sec_a.current_hp, before_a)
        self.assertLess(sec_b.current_hp, before_b)


class _PassCleavePicker(Picker):
    def pick(self, actor, state, actions):
        for a in actions:
            if isinstance(a, PassCleave):
                return a
        return actions[0]


class TestCleavePass(unittest.TestCase):
    def test_pass_picker_skips_cleave_continuation(self):
        cleaver, primary, sec_a, sec_b, grid, enc = _setup_cleave()
        enc.pickers[cleaver.id] = _PassCleavePicker()
        before_a = sec_a.current_hp
        before_b = sec_b.current_hp
        result = _cleave(cleaver, primary, enc, grid)
        kinds = [e.kind for e in result.events]
        # No secondary attack.
        self.assertNotIn("cleave_secondary", kinds)
        no_followup = next(
            e for e in result.events if e.kind == "cleave_no_followup"
        )
        self.assertEqual(no_followup.detail.get("reason"), "picker_passed")
        # Neither secondary was damaged.
        self.assertEqual(sec_a.current_hp, before_a)
        self.assertEqual(sec_b.current_hp, before_b)


if __name__ == "__main__":
    unittest.main()
