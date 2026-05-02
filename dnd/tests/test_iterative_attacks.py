"""Tests for PF1 iterative-attack BAB scaling.

Confirms _iterative_attack_count returns the RAW count at every
BAB threshold, and that _do_full_attack actually emits that many
attack events end-to-end.
"""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import (
    _iterative_attack_count,
    execute_turn,
)


REGISTRY = default_registry()


# PF1 RAW: 1@0-5, 2@6-10, 3@11-15, 4@16+.
_EXPECTED = [
    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
    (6, 2), (7, 2), (8, 2), (9, 2), (10, 2),
    (11, 3), (12, 3), (13, 3), (14, 3), (15, 3),
    (16, 4), (17, 4), (18, 4), (19, 4), (20, 4),
]


class TestIterativeAttackCount(unittest.TestCase):
    """Pure unit tests of the formula."""

    def test_raw_table_matches(self):
        for bab, expected in _EXPECTED:
            with self.subTest(bab=bab):
                self.assertEqual(_iterative_attack_count(bab), expected)

    def test_thresholds(self):
        # The four boundary points where the count steps up.
        self.assertEqual(_iterative_attack_count(5), 1)
        self.assertEqual(_iterative_attack_count(6), 2)
        self.assertEqual(_iterative_attack_count(10), 2)
        self.assertEqual(_iterative_attack_count(11), 3)
        self.assertEqual(_iterative_attack_count(15), 3)
        self.assertEqual(_iterative_attack_count(16), 4)

    def test_negative_bab_clamps_to_one(self):
        # Some critters have technically-negative BAB; everyone still
        # gets one attack.
        self.assertEqual(_iterative_attack_count(-1), 1)
        self.assertEqual(_iterative_attack_count(-99), 1)


class TestFullAttackEmitsExpectedCount(unittest.TestCase):
    """End-to-end: a full_attack composite at a given BAB produces
    that many ``full_attack_N`` events (one per iterative)."""

    def _setup(self, bab: int):
        attacker = combatant_from_monster(
            REGISTRY.get_monster("orc"), (5, 5), "team_a",
        )
        # Override BAB without rebuilding the whole template.
        attacker.bases["bab"] = bab
        # Update the attack option's attack_bonus to match the new BAB
        # so the attacker can plausibly hit and we don't break the
        # default attacks at the structural level.
        if attacker.attack_options:
            base = attacker.attack_options[0]
            base["attack_bonus"] = bab + 4  # rough: BAB + Str-ish

        # Use a high-HP dummy so the test target doesn't die mid-round
        # and short-circuit the attack loop.
        target = combatant_from_monster(
            REGISTRY.get_monster("orc"), (6, 5), "team_b",
        )
        target.max_hp = 9999
        target.current_hp = 9999

        grid = Grid(width=12, height=12)
        grid.place(attacker)
        grid.place(target)
        enc = Encounter.begin(grid, [attacker, target], Roller(seed=1))

        script = BehaviorScript(name="full_attack", rules=[
            Rule(do={"composite": "full_attack",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(attacker, enc, grid)
        return attacker, target, enc, grid, intent

    def _count_full_attack_events(self, bab: int) -> int:
        attacker, target, enc, grid, intent = self._setup(bab)
        result = execute_turn(attacker, intent, enc, grid, Roller(seed=1))
        return sum(
            1 for e in result.events
            if e.kind.startswith("full_attack_")
        )

    def test_bab_5_emits_1(self):
        self.assertEqual(self._count_full_attack_events(5), 1)

    def test_bab_6_emits_2(self):
        self.assertEqual(self._count_full_attack_events(6), 2)

    def test_bab_11_emits_3(self):
        self.assertEqual(self._count_full_attack_events(11), 3)

    def test_bab_16_emits_4(self):
        self.assertEqual(self._count_full_attack_events(16), 4)

    def test_bab_20_emits_4(self):
        self.assertEqual(self._count_full_attack_events(20), 4)


if __name__ == "__main__":
    unittest.main()
