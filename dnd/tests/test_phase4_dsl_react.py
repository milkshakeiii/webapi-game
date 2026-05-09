"""DSL v2 Phase 4 first slice: ``react: aoo`` clauses end-to-end.

Patrons can now write reactive-interrupt behavior in the DSL instead
of subclassing ``Picker`` in Python:

    rules:
      - react: aoo
        when: provoker.hp_pct < 0.5
        do:
          type: take_aoo
          weapon: 0
      - react: aoo
        do:
          type: pass_aoo

The script gets compiled into a ``CompiledReactivePicker`` and
registered on ``Encounter.pickers`` via ``register_script_pickers``.
When an AoO fires, the picker walks the matching ``react: aoo``
rules in order, evaluates each ``when`` against the reactive
namespace (``provoker`` is a ``SelfRef`` to the foe whose action
provoked), and translates the matching ``do:`` into a ``TakeAoO`` /
``PassAoO`` substrate action.

This test covers:
- Parser accepts ``react:`` / ``sub:`` keys.
- ``register_script_pickers`` only fires for scripts with reactive
  rules (active-only scripts produce no picker registration).
- A `provoker.hp_pct` condition correctly routes between TakeAoO and
  PassAoO based on the provoker's state.
"""

from __future__ import annotations

import unittest

from dnd.engine.actions import (
    CompiledReactivePicker,
    register_script_pickers,
)
from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Rule, script_from_dict
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import _do_aoo


REGISTRY = default_registry()


def _orc(pos, team):
    return combatant_from_monster(REGISTRY.get_monster("orc"), pos, team)


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


class TestParserAcceptsReactSubKeys(unittest.TestCase):
    def test_react_key_is_parsed(self):
        script = script_from_dict({
            "name": "r",
            "rules": [
                {"react": "aoo", "do": {"type": "pass_aoo"}},
            ],
        })
        self.assertEqual(len(script.rules), 1)
        self.assertEqual(script.rules[0].react, "aoo")
        self.assertIsNone(script.rules[0].sub)

    def test_sub_key_is_parsed(self):
        script = script_from_dict({
            "name": "s",
            "rules": [
                {"sub": "full_attack", "do": {"type": "end_full_attack"}},
            ],
        })
        self.assertEqual(script.rules[0].sub, "full_attack")
        self.assertIsNone(script.rules[0].react)

    def test_active_rules_have_neither_set(self):
        script = script_from_dict({
            "name": "a",
            "rules": [
                {"do": {"composite": "charge",
                        "args": {"target": "enemy.closest"}}},
            ],
        })
        self.assertIsNone(script.rules[0].react)
        self.assertIsNone(script.rules[0].sub)


# ---------------------------------------------------------------------------
# register_script_pickers
# ---------------------------------------------------------------------------


class TestRegistration(unittest.TestCase):
    def test_active_only_script_does_not_register(self):
        actor = _orc((5, 5), "x")
        grid = Grid(width=10, height=10)
        grid.place(actor)
        enc = Encounter.begin(grid, [actor], Roller(seed=1))
        script = BehaviorScript(name="active", rules=[
            Rule(do={"composite": "charge",
                     "args": {"target": "enemy.closest"}}),
        ])
        register_script_pickers(actor, script, enc)
        self.assertNotIn(actor.id, enc.pickers)

    def test_script_with_react_rule_registers_picker(self):
        actor = _orc((5, 5), "x")
        grid = Grid(width=10, height=10)
        grid.place(actor)
        enc = Encounter.begin(grid, [actor], Roller(seed=1))
        script = BehaviorScript(name="reactive", rules=[
            Rule(react="aoo", do={"type": "pass_aoo"}),
        ])
        register_script_pickers(actor, script, enc)
        self.assertIn(actor.id, enc.pickers)
        self.assertIsInstance(enc.pickers[actor.id], CompiledReactivePicker)


# ---------------------------------------------------------------------------
# react: aoo end-to-end
# ---------------------------------------------------------------------------


def _setup(threatener_pos=(5, 5), provoker_pos=(6, 5)):
    threatener = _orc(threatener_pos, "x")
    provoker = _orc(provoker_pos, "y")
    grid = Grid(width=12, height=12)
    grid.place(threatener)
    grid.place(provoker)
    enc = Encounter.begin(grid, [threatener, provoker], Roller(seed=1))
    return threatener, provoker, grid, enc


class TestReactAooEndToEnd(unittest.TestCase):
    def test_take_aoo_when_provoker_low_hp(self):
        threatener, provoker, grid, enc = _setup()
        provoker.current_hp = 1  # low — picker takes the AoO
        script = BehaviorScript(name="opportunistic", rules=[
            Rule(react="aoo", when="provoker.hp_pct < 0.5",
                 do={"type": "take_aoo", "weapon": 0}),
            Rule(react="aoo", do={"type": "pass_aoo"}),
        ])
        register_script_pickers(threatener, script, enc)
        events: list = []
        _do_aoo(threatener, provoker, grid, events, encounter=enc)
        kinds = [e.kind for e in events]
        self.assertIn("aoo", kinds)
        self.assertNotIn("aoo_pass", kinds)

    def test_pass_aoo_when_provoker_healthy(self):
        threatener, provoker, grid, enc = _setup()
        # Provoker at full HP — picker conserves the AoO.
        script = BehaviorScript(name="conservative", rules=[
            Rule(react="aoo", when="provoker.hp_pct < 0.5",
                 do={"type": "take_aoo", "weapon": 0}),
            Rule(react="aoo", do={"type": "pass_aoo"}),
        ])
        register_script_pickers(threatener, script, enc)
        events: list = []
        _do_aoo(threatener, provoker, grid, events, encounter=enc)
        kinds = [e.kind for e in events]
        self.assertIn("aoo_pass", kinds)
        self.assertNotIn("aoo", kinds)
        # Budget not consumed.
        self.assertEqual(threatener.aoos_used_this_round, 0)

    def test_take_aoo_with_custom_weapon_index(self):
        threatener, provoker, grid, enc = _setup()
        # Orc has [falchion (idx 0, melee), javelin (idx 1, ranged)].
        # Pick the javelin via DSL.
        script = BehaviorScript(name="ranged_aoo", rules=[
            Rule(react="aoo", do={"type": "take_aoo", "weapon": 1}),
        ])
        register_script_pickers(threatener, script, enc)
        events: list = []
        _do_aoo(threatener, provoker, grid, events, encounter=enc)
        aoo = next(e for e in events if e.kind == "aoo")
        self.assertEqual(aoo.detail["weapon_index"], 1)

    def test_no_matching_rule_falls_back_to_default(self):
        # Script has react rules but none match (no when:false rule).
        # The fallback should be TakeAoO weapon 0 (v1-equivalent).
        threatener, provoker, grid, enc = _setup()
        script = BehaviorScript(name="strict", rules=[
            Rule(react="aoo", when="provoker.hp_pct < 0.0",  # never true
                 do={"type": "pass_aoo"}),
        ])
        register_script_pickers(threatener, script, enc)
        events: list = []
        _do_aoo(threatener, provoker, grid, events, encounter=enc)
        aoo = next(e for e in events if e.kind == "aoo")
        # Default weapon (0) used.
        self.assertEqual(aoo.detail["weapon_index"], 0)


if __name__ == "__main__":
    unittest.main()
