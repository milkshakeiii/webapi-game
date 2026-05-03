"""Tests for Phase 1.3 condition gap-fillers — invisible, incorporeal,
and confused (random action table)."""

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


# ---------------------------------------------------------------------------
# Invisible
# ---------------------------------------------------------------------------


class TestInvisible(unittest.TestCase):
    def test_invisible_sets_concealment(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        c.add_condition("invisible")
        self.assertEqual(c.concealment, 50)

    def test_remove_invisible_restores_concealment(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        c.add_condition("invisible")
        c.remove_condition("invisible")
        self.assertEqual(c.concealment, 0)

    def test_invisible_attacker_uses_flat_footed_ac_and_plus_two(self):
        # Goblin AC 16 / flat-footed 14. Invisible orc attacker should
        # roll vs flat-footed AC 14 and gain +2 attack.
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        a.attack_options = [{
            "type": "melee", "name": "knife",
            "weapon_id": "dagger",
            "weapon_category": "simple",
            "attack_bonus": 0,
            "damage": "1d4", "damage_bonus": 0,
            "damage_type": "P",
            "crit_range": [20, 20], "crit_multiplier": 2,
        }]
        a.add_condition("invisible")
        b = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (6, 5), "y")
        b.max_hp = 9999
        b.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        script = BehaviorScript(name="atk", rules=[
            Rule(do={"composite": "full_attack",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=42))
        attack_evts = [e for e in result.events
                       if e.kind.startswith("full_attack")]
        self.assertGreater(len(attack_evts), 0)
        trace = "\n".join(attack_evts[0].detail.get("trace") or [])
        # Flat-footed AC 14 for goblin; attack bonus includes +2 from
        # invisible (declared base 0 → trace shows '+2').
        self.assertIn("AC 14", trace)
        self.assertIn("+ 2 = ", trace)


# ---------------------------------------------------------------------------
# Incorporeal
# ---------------------------------------------------------------------------


class TestIncorporeal(unittest.TestCase):
    def test_monster_with_incorporeal_subtype_gets_incorporeal_flag(self):
        # We don't have a CRB ghost yet, so synthesize a Monster
        # with the incorporeal subtype manually.
        from dnd.engine.content import Monster
        ghost = Monster(
            id="phantom", name="Phantom", summary="Test ghost.",
            cr="3", xp=800, alignment="neutral",
            size="medium", type="undead", subtypes=["incorporeal"],
            ability_scores={"str": 0, "dex": 14, "con": 0,
                            "int": 10, "wis": 10, "cha": 14},
            hit_dice="3d8", hp=20, init=2, senses=["darkvision_60"],
            speed=30,
            ac={"total": 13, "touch": 13, "flat_footed": 11,
                "deflection": 2, "dex": 2},
            saves={"fort": 1, "ref": 3, "will": 3},
            bab=2, cmb=0, cmd=12,
            attacks=[{"type": "melee", "name": "incorporeal touch",
                      "attack_bonus": 4, "damage": "1d6",
                      "damage_type": "neg", "crit_range": [20, 20],
                      "crit_multiplier": 2}],
            feats=[], skills={}, languages=[],
            racial_traits=[], equipment=[],
            permanent_conditions=[],
        )
        c = combatant_from_monster(ghost, (0, 0), "x")
        self.assertTrue(c.incorporeal)
        # Concealment is no longer auto-set for incorporeal — the
        # tag-aware miss check in _do_attack handles the 50% directly.
        self.assertEqual(c.concealment, 0)


# ---------------------------------------------------------------------------
# Confused
# ---------------------------------------------------------------------------


class TestConfused(unittest.TestCase):
    def _setup_pair(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        b = combatant_from_monster(REGISTRY.get_monster("goblin"), (6, 5), "y")
        a.add_condition("confused")
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        return a, b, enc, grid

    def _attack_intent(self, target_expr="enemy.closest"):
        return BehaviorScript(name="atk", rules=[
            Rule(do={"composite": "full_attack",
                     "args": {"target": target_expr}}),
        ])

    def test_confusion_distributes_outcomes(self):
        # Sample many seeds; each of the 4 outcomes should appear.
        outcomes = {"act_normally": 0, "babble": 0,
                    "self_attack": 0, "attack_nearest": 0}
        for seed in range(1, 81):
            a, b, enc, grid = self._setup_pair()
            script = self._attack_intent()
            intent = Interpreter(script).pick_turn(a, enc, grid)
            result = execute_turn(a, intent, enc, grid, Roller(seed=seed))
            kinds = [e.kind for e in result.events]
            if "confused_act_normally" in kinds:
                outcomes["act_normally"] += 1
            elif "confused_babble" in kinds:
                outcomes["babble"] += 1
            elif "confused_self_attack" in kinds:
                outcomes["self_attack"] += 1
            elif "confused_attack_nearest" in kinds:
                outcomes["attack_nearest"] += 1
        # Every outcome should have appeared at least once across 80
        # seeds (each outcome is roughly 25%).
        for k, v in outcomes.items():
            self.assertGreater(v, 0, f"never rolled {k}: {outcomes}")

    def test_confused_self_attack_damages_actor(self):
        # Find a seed that yields self_attack and verify HP loss.
        for seed in range(1, 200):
            a, b, enc, grid = self._setup_pair()
            hp_before = a.current_hp
            script = self._attack_intent()
            intent = Interpreter(script).pick_turn(a, enc, grid)
            result = execute_turn(a, intent, enc, grid, Roller(seed=seed))
            evts = [e for e in result.events if e.kind == "confused_self_attack"]
            if evts:
                self.assertLess(a.current_hp, hp_before)
                self.assertGreaterEqual(evts[0].detail["damage"], 1)
                return
        self.fail("no seed in [1,200] triggered confused_self_attack")


if __name__ == "__main__":
    unittest.main()
