"""Tests for the prone state — fall, stand-up provokes AoO, position
modifiers."""

from __future__ import annotations

import unittest

from dnd.engine.combat import AttackProfile, resolve_attack
from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule, build_namespace
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


def _setup(actor_pos=(5, 5), other_pos=(6, 5)):
    a = combatant_from_monster(REGISTRY.get_monster("orc"), actor_pos, "team_a")
    b = combatant_from_monster(REGISTRY.get_monster("goblin"), other_pos, "team_b")
    grid = Grid(width=12, height=12)
    grid.place(a)
    grid.place(b)
    enc = Encounter.begin(grid, [a, b], Roller(seed=1))
    return a, b, enc, grid


# ---------------------------------------------------------------------------
# fall_prone free action
# ---------------------------------------------------------------------------


class TestFallProne(unittest.TestCase):
    def test_fall_prone_free_action_applies_condition(self):
        a, _, enc, grid = _setup()
        intent = type("I", (), {})()
        intent.rule_index = 0
        intent.do = {"free": [{"type": "fall_prone"}]}
        intent.namespace = build_namespace(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        self.assertIn("prone", a.conditions)
        self.assertTrue(any(e.kind == "fall_prone" for e in result.events))


# ---------------------------------------------------------------------------
# stand_up move action
# ---------------------------------------------------------------------------


class TestStandUp(unittest.TestCase):
    def test_stand_up_clears_condition(self):
        a, _, enc, grid = _setup()
        a.add_condition("prone")
        script = BehaviorScript(name="stand", rules=[
            Rule(do={"slots": {"move": {"type": "stand_up"}}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        execute_turn(a, intent, enc, grid, Roller(seed=1))
        self.assertNotIn("prone", a.conditions)

    def test_stand_up_provokes_aoo_from_threatener(self):
        # Place hostile next to the actor so they threaten.
        a, b, enc, grid = _setup(actor_pos=(5, 5), other_pos=(6, 5))
        a.add_condition("prone")
        # Run a few seeds; assert at least one produces an AoO event.
        seen_aoo = False
        for seed in range(1, 30):
            a.add_condition("prone")  # re-set in case prior iterations stood up
            a.current_hp = a.max_hp   # reset hp in case AoO landed before
            script = BehaviorScript(name="stand", rules=[
                Rule(do={"slots": {"move": {"type": "stand_up"}}}),
            ])
            intent = Interpreter(script).pick_turn(a, enc, grid)
            result = execute_turn(a, intent, enc, grid, Roller(seed=seed))
            if any(e.kind == "aoo" for e in result.events):
                seen_aoo = True
                break
        self.assertTrue(seen_aoo, "no AoO event in 30 seeds")

    def test_stand_up_no_aoo_when_no_threatener(self):
        a, b, enc, grid = _setup(actor_pos=(0, 0), other_pos=(11, 11))
        a.add_condition("prone")
        script = BehaviorScript(name="stand", rules=[
            Rule(do={"slots": {"move": {"type": "stand_up"}}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        self.assertFalse(any(e.kind == "aoo" for e in result.events))


# ---------------------------------------------------------------------------
# Position modifiers
#
# We test these directly via resolve_attack with the appropriate attack
# bonus deltas, rather than going end-to-end (which would require many
# seeds to find one where the difference shows up cleanly).
# ---------------------------------------------------------------------------


class TestProneAttackerPenalty(unittest.TestCase):
    """A prone attacker takes -4 to melee attack rolls."""

    def _melee_attack_total(self, attacker, target, grid, seed):
        from dnd.engine.turn_executor import _do_attack
        events = []
        _do_attack(attacker, target, grid, Roller(seed=seed), events)
        atk = next(e for e in events if e.kind == "attack")
        # Reach into the trace to find the d20 + bonus.
        for line in atk.detail["trace"]:
            if line.startswith("attack "):
                # "attack longsword: d20=N + B = T vs AC X"
                parts = line.split(" = ")[0]
                # parts ends with "+ B"
                bonus = int(parts.rsplit("+ ", 1)[1])
                return bonus
        return None

    def test_attack_bonus_drops_by_4_when_prone(self):
        a, b, enc, grid = _setup()
        normal_bonus = self._melee_attack_total(a, b, grid, seed=1)
        a.add_condition("prone")
        prone_bonus = self._melee_attack_total(a, b, grid, seed=1)
        self.assertEqual(normal_bonus - prone_bonus, 4)


class TestProneTargetModifier(unittest.TestCase):
    """Prone target: melee attackers +4, ranged attackers -4."""

    def _melee_attack_bonus_used(self, attacker, target, grid, seed):
        from dnd.engine.turn_executor import _do_attack
        events = []
        _do_attack(attacker, target, grid, Roller(seed=seed), events)
        atk = next(e for e in events if e.kind == "attack")
        for line in atk.detail["trace"]:
            if line.startswith("attack "):
                parts = line.split(" = ")[0]
                return int(parts.rsplit("+ ", 1)[1])
        return None

    def test_melee_attacker_gets_plus_4_vs_prone_target(self):
        a, b, enc, grid = _setup()
        normal = self._melee_attack_bonus_used(a, b, grid, seed=1)
        b.add_condition("prone")
        prone_bonus = self._melee_attack_bonus_used(a, b, grid, seed=1)
        self.assertEqual(prone_bonus - normal, 4)


if __name__ == "__main__":
    unittest.main()
