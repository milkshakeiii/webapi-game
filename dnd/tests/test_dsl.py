"""Tests for dnd.engine.dsl."""

from __future__ import annotations

import json
import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import (
    BehaviorScript,
    DSLError,
    Interpreter,
    Rule,
    build_namespace,
    evaluate,
    parse_script,
    script_from_dict,
)
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid


REGISTRY = default_registry()


def _goblin(pos, team="enemies"):
    return combatant_from_monster(REGISTRY.get_monster("goblin"), pos, team)


def _orc(pos, team="enemies"):
    return combatant_from_monster(REGISTRY.get_monster("orc"), pos, team)


def _make_encounter(combatants):
    grid = Grid(width=20, height=20)
    for c in combatants:
        grid.place(c)
    enc = Encounter.begin(grid, combatants, Roller(seed=1))
    return enc, grid


# ---------------------------------------------------------------------------
# Script parsing
# ---------------------------------------------------------------------------


class TestParse(unittest.TestCase):
    def test_minimal_script(self):
        text = json.dumps({
            "name": "test",
            "rules": [{"do": {"composite": "hold"}}],
        })
        s = parse_script(text)
        self.assertEqual(s.name, "test")
        self.assertEqual(len(s.rules), 1)

    def test_full_script(self):
        text = json.dumps({
            "name": "aggressive",
            "rules": [
                {
                    "hero": "any",
                    "when": "enemy.any",
                    "do": {"composite": "charge",
                           "args": {"target": "enemy.closest"}},
                },
                {"do": {"composite": "hold"}},
            ],
        })
        s = parse_script(text)
        self.assertEqual(len(s.rules), 2)
        self.assertEqual(s.rules[0].when, "enemy.any")
        self.assertEqual(s.rules[1].when, None)

    def test_invalid_json(self):
        with self.assertRaises(DSLError):
            parse_script("{not json")

    def test_missing_rules(self):
        with self.assertRaises(DSLError):
            script_from_dict({"name": "no rules"})


# ---------------------------------------------------------------------------
# Safe AST evaluator
# ---------------------------------------------------------------------------


class TestEvaluate(unittest.TestCase):
    def test_constants(self):
        self.assertEqual(evaluate("3", {}), 3)
        self.assertEqual(evaluate("3.5", {}), 3.5)
        self.assertEqual(evaluate("True", {"True": True}), True)

    def test_arithmetic(self):
        self.assertEqual(evaluate("3 + 4", {}), 7)
        self.assertEqual(evaluate("10 - 3 * 2", {}), 4)
        self.assertEqual(evaluate("10 // 3", {}), 3)

    def test_comparison(self):
        self.assertEqual(evaluate("3 < 5", {}), True)
        self.assertEqual(evaluate("3 == 4", {}), False)

    def test_chained_comparison(self):
        self.assertEqual(evaluate("1 < 2 < 3", {}), True)
        self.assertEqual(evaluate("1 < 5 < 3", {}), False)

    def test_boolean_ops(self):
        self.assertEqual(evaluate("True and False", {"True": True, "False": False}), False)
        self.assertEqual(evaluate("True or False", {"True": True, "False": False}), True)
        self.assertEqual(evaluate("not False", {"False": False}), True)

    def test_attribute_lookup(self):
        class Obj:
            x = 5
        ns = {"obj": Obj()}
        self.assertEqual(evaluate("obj.x", ns), 5)

    def test_method_call(self):
        class Obj:
            def double(self, n): return n * 2
        ns = {"obj": Obj()}
        self.assertEqual(evaluate("obj.double(7)", ns), 14)

    def test_unknown_identifier_raises(self):
        with self.assertRaises(DSLError):
            evaluate("foo.bar", {})

    def test_disallowed_subscript(self):
        with self.assertRaises(DSLError):
            evaluate("foo[0]", {"foo": [1, 2, 3]})

    def test_disallowed_lambda(self):
        with self.assertRaises(DSLError):
            evaluate("(lambda x: x)(3)", {})


# ---------------------------------------------------------------------------
# Vocabulary against an encounter
# ---------------------------------------------------------------------------


class TestVocabulary(unittest.TestCase):
    def setUp(self) -> None:
        self.actor = _goblin((5, 5), team="patrons")
        self.foe = _orc((6, 5), team="enemies")
        self.enc, self.grid = _make_encounter([self.actor, self.foe])
        self.ns = build_namespace(self.actor, self.enc, self.grid)

    def test_self_hp(self):
        self.assertEqual(evaluate("self.hp", self.ns), self.actor.current_hp)
        self.assertEqual(evaluate("self.hp_max", self.ns), self.actor.max_hp)
        self.assertEqual(evaluate("self.hp_pct", self.ns), 1.0)

    def test_enemy_any(self):
        self.assertTrue(evaluate("enemy.any", self.ns))

    def test_enemy_count(self):
        self.assertEqual(evaluate("enemy.count", self.ns), 1)

    def test_enemy_closest_returns_combatant(self):
        result = evaluate("enemy.closest", self.ns)
        self.assertIs(result, self.foe)

    def test_enemy_in_range_within(self):
        self.assertIs(evaluate("enemy.in_range(3)", self.ns), self.foe)

    def test_enemy_in_range_too_far(self):
        # Move the foe away.
        self.foe.position = (15, 15)
        self.grid.move(self.foe, (15, 15))
        # Re-build namespace so resolvers see the updated grid.
        ns = build_namespace(self.actor, self.enc, self.grid)
        self.assertIsNone(evaluate("enemy.in_range(3)", ns))

    def test_self_has_condition(self):
        self.assertFalse(evaluate("self.has_condition('blinded')", self.ns))
        self.actor.add_condition("blinded")
        self.assertTrue(evaluate("self.has_condition('blinded')", self.ns))

    def test_compound_expression(self):
        self.assertTrue(
            evaluate("enemy.any and enemy.count == 1", self.ns)
        )


# ---------------------------------------------------------------------------
# Interpreter
# ---------------------------------------------------------------------------


class TestInterpreter(unittest.TestCase):
    def test_picks_first_matching_rule(self):
        script = BehaviorScript(name="test", rules=[
            Rule(when="enemy.any", do={"composite": "charge",
                                        "args": {"target": "enemy.closest"}}),
            Rule(do={"composite": "hold"}),
        ])
        actor = _goblin((5, 5), team="patrons")
        foe = _orc((6, 5), team="enemies")
        enc, grid = _make_encounter([actor, foe])

        interp = Interpreter(script)
        intent = interp.pick_turn(actor, enc, grid)
        self.assertIsNotNone(intent)
        self.assertEqual(intent.rule_index, 0)
        self.assertEqual(intent.do["composite"], "charge")

    def test_falls_through_to_default(self):
        script = BehaviorScript(name="test", rules=[
            Rule(when="enemy.count > 5",
                 do={"composite": "withdraw"}),
            Rule(do={"composite": "hold"}),
        ])
        actor = _goblin((5, 5), team="patrons")
        foe = _orc((6, 5), team="enemies")
        enc, grid = _make_encounter([actor, foe])
        interp = Interpreter(script)
        intent = interp.pick_turn(actor, enc, grid)
        self.assertEqual(intent.rule_index, 1)
        self.assertEqual(intent.do["composite"], "hold")

    def test_no_match_returns_none(self):
        # Every rule has a condition that fails.
        script = BehaviorScript(name="test", rules=[
            Rule(when="enemy.count > 99",
                 do={"composite": "hold"}),
        ])
        actor = _goblin((5, 5), team="patrons")
        foe = _orc((6, 5), team="enemies")
        enc, grid = _make_encounter([actor, foe])
        interp = Interpreter(script)
        self.assertIsNone(interp.pick_turn(actor, enc, grid))


if __name__ == "__main__":
    unittest.main()
