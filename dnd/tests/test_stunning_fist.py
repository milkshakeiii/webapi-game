"""Tests for the Stunning Fist composite action.

PF1 RAW: declare a Fort-save rider (DC 10 + 1/2 char level + Wis) on
a melee attack. Use is consumed regardless of hit/miss; on hit, target
rolls Fort or is stunned 1 round.
"""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import (
    combatant_from_character,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


def _monk_request():
    return CharacterRequest.from_dict({
        "name": "Friar Pim", "race": "human", "class": "monk",
        "alignment": "lawful_good",
        # Point-buy 20: 5+5+2+(-2)+10+0 = 20.
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 14, "dex": 14, "con": 12,
                       "int": 8, "wis": 16, "cha": 10}},
        "free_ability_choice": "wis",
        "feats": ["improved_initiative", "iron_will"],
        "skill_ranks": {"acrobatics": 1, "perception": 1},
        "bonus_languages": [],
        "class_choices": {"monk_bonus_feat": "dodge"},
    })


def _setup(monk_pos=(5, 5), goblin_pos=(6, 5)):
    char = create_character(_monk_request(), REGISTRY)
    monk = combatant_from_character(char, REGISTRY, monk_pos, "patrons")
    goblin = combatant_from_monster(
        REGISTRY.get_monster("goblin"), goblin_pos, "enemies",
    )
    grid = Grid(width=12, height=12)
    grid.place(monk)
    grid.place(goblin)
    enc = Encounter.begin(grid, [monk, goblin], Roller(seed=1))
    return monk, goblin, enc, grid


class TestStunningFistResource(unittest.TestCase):
    def test_l1_monk_has_one_use(self):
        monk, _, _, _ = _setup()
        self.assertEqual(monk.resources.get("stunning_fist_uses"), 1)


class TestStunningFistExecution(unittest.TestCase):
    def _run(self, seed=1):
        monk, goblin, enc, grid = _setup()
        script = BehaviorScript(name="stun", rules=[
            Rule(do={"composite": "stunning_fist",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(monk, enc, grid)
        result = execute_turn(monk, intent, enc, grid, Roller(seed=seed))
        return monk, goblin, result

    def test_consumes_use_even_when_no_hit_outcome_recorded(self):
        # Whether the attack lands or misses, the use is consumed.
        monk, goblin, result = self._run(seed=1)
        self.assertEqual(monk.resources["stunning_fist_uses"], 0)
        # A declare event always fires.
        self.assertTrue(any(e.kind == "stunning_fist_declare" for e in result.events))

    def test_attack_event_emitted(self):
        _, _, result = self._run(seed=1)
        self.assertTrue(any(e.kind == "stunning_fist_attack" for e in result.events))

    def test_save_event_only_on_hit(self):
        # Run several seeds; for each that produced a hit, assert a
        # stunning_fist_save event fired. For seeds that missed, no
        # save event.
        seen_hit = False
        seen_miss = False
        for seed in range(1, 60):
            _, _, result = self._run(seed=seed)
            attack = next(e for e in result.events
                          if e.kind == "stunning_fist_attack")
            saves = [e for e in result.events
                     if e.kind == "stunning_fist_save"]
            if attack.detail["hit"]:
                seen_hit = True
                self.assertEqual(len(saves), 1,
                                 f"seed {seed} hit but no save event")
            else:
                seen_miss = True
                self.assertEqual(len(saves), 0,
                                 f"seed {seed} missed but save event fired")
            if seen_hit and seen_miss:
                break
        self.assertTrue(seen_hit, "no hit produced across 60 seeds")

    def test_stunned_condition_applied_on_save_failure(self):
        # Try seeds until we get a hit AND a failed save → stunned.
        for seed in range(1, 200):
            monk, goblin, result = self._run(seed=seed)
            saves = [e for e in result.events
                     if e.kind == "stunning_fist_save"]
            if saves and not saves[0].detail.get("passed"):
                self.assertIn("stunned", goblin.conditions)
                return
        self.skipTest("no save failure across 200 seeds")

    def test_stunned_expires_after_one_round(self):
        for seed in range(1, 200):
            monk, goblin, result = self._run(seed=seed)
            saves = [e for e in result.events
                     if e.kind == "stunning_fist_save"]
            if saves and not saves[0].detail.get("passed"):
                # Goblin is stunned this round (round 1 of encounter).
                self.assertIn("stunned", goblin.conditions)
                # Tick to round 2 — stun expires.
                goblin.tick_round(2)
                self.assertNotIn("stunned", goblin.conditions)
                return
        self.skipTest("no save failure across 200 seeds")


class TestStunningFistGuards(unittest.TestCase):
    def test_no_uses_skips(self):
        monk, goblin, enc, grid = _setup()
        monk.resources["stunning_fist_uses"] = 0
        script = BehaviorScript(name="stun", rules=[
            Rule(do={"composite": "stunning_fist",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(monk, enc, grid)
        result = execute_turn(monk, intent, enc, grid, Roller(seed=1))
        self.assertTrue(any(e.kind == "skip" for e in result.events))
        self.assertFalse(any(e.kind == "stunning_fist_attack"
                             for e in result.events))

    def test_target_not_adjacent_skips(self):
        monk, goblin, enc, grid = _setup(monk_pos=(2, 5), goblin_pos=(8, 5))
        script = BehaviorScript(name="stun", rules=[
            Rule(do={"composite": "stunning_fist",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(monk, enc, grid)
        result = execute_turn(monk, intent, enc, grid, Roller(seed=1))
        skips = [e for e in result.events if e.kind == "skip"]
        self.assertTrue(skips)
        self.assertIn("not adjacent", skips[0].detail.get("reason", ""))


if __name__ == "__main__":
    unittest.main()
