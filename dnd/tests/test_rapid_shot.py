"""Tests for the Rapid Shot feat.

PF1: full-round action; one extra ranged attack at the highest BAB;
all ranged attacks this round take -2.
"""

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


def _ranged_orc(bab: int, has_rapid_shot: bool):
    """Build an orc combatant with the given BAB and (optionally) the
    rapid_shot feat. We override BAB and substitute a ranged attack
    profile so we don't have to spin up a full character."""
    orc = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "team_a")
    orc.bases["bab"] = bab
    # Make the primary attack ranged so Rapid Shot is legal.
    if orc.attack_options:
        orc.attack_options[0] = {
            "type": "ranged",
            "name": "javelin",
            "attack_bonus": bab + 2,
            "damage": "1d6",
            "damage_bonus": 0,
            "damage_type": "P",
            "crit_range": [20, 20],
            "crit_multiplier": 2,
            "range_increment": 30,
        }
    # Inject the feat onto the monster template's feats list.
    if has_rapid_shot:
        orc.extra_feats = ["rapid_shot"]
    return orc


def _setup(bab: int, has_rapid_shot: bool):
    archer = _ranged_orc(bab, has_rapid_shot)
    target = combatant_from_monster(
        REGISTRY.get_monster("orc"), (10, 5), "team_b",
    )
    target.max_hp = 9999
    target.current_hp = 9999
    grid = Grid(width=20, height=10)
    grid.place(archer)
    grid.place(target)
    enc = Encounter.begin(grid, [archer, target], Roller(seed=1))
    return archer, target, enc, grid


def _full_attack(archer, enc, grid, options=None):
    intent_do = {"composite": "full_attack",
                 "args": {"target": "enemy.closest"}}
    if options is not None:
        intent_do["args"]["options"] = options
    script = BehaviorScript(name="ra", rules=[Rule(do=intent_do)])
    intent = Interpreter(script).pick_turn(archer, enc, grid)
    return execute_turn(archer, intent, enc, grid, Roller(seed=1))


class TestRapidShotAttackCount(unittest.TestCase):
    def test_bab_5_no_rapid_shot_one_attack(self):
        archer, _, enc, grid = _setup(5, has_rapid_shot=False)
        result = _full_attack(archer, enc, grid)
        n = sum(1 for e in result.events if e.kind.startswith("full_attack_"))
        self.assertEqual(n, 1)

    def test_bab_5_with_rapid_shot_two_attacks(self):
        archer, _, enc, grid = _setup(5, has_rapid_shot=True)
        result = _full_attack(archer, enc, grid, options={"rapid_shot": True})
        n = sum(1 for e in result.events if e.kind.startswith("full_attack_"))
        self.assertEqual(n, 2)

    def test_bab_11_with_rapid_shot_four_attacks(self):
        # BAB 11 normally = 3 attacks; with Rapid Shot = 4.
        archer, _, enc, grid = _setup(11, has_rapid_shot=True)
        result = _full_attack(archer, enc, grid, options={"rapid_shot": True})
        n = sum(1 for e in result.events if e.kind.startswith("full_attack_"))
        self.assertEqual(n, 4)


class TestRapidShotPenalty(unittest.TestCase):
    def _attack_bonuses(self, archer, enc, grid, options=None):
        result = _full_attack(archer, enc, grid, options=options)
        bonuses = []
        for e in result.events:
            if not e.kind.startswith("full_attack_"):
                continue
            for line in e.detail.get("trace", []):
                if line.startswith("attack "):
                    parts = line.split(" = ")[0]
                    bonuses.append(int(parts.rsplit("+ ", 1)[1]))
                    break
        return bonuses

    def test_bonus_minus_2_across_all_attacks(self):
        # BAB 11 archer; without Rapid Shot, bonuses are +N, +N-5, +N-10.
        # With Rapid Shot: +N-2, +N-2, +N-7, +N-12.
        archer, _, enc, grid = _setup(11, has_rapid_shot=True)
        normal = self._attack_bonuses(archer, enc, grid)
        # Reset attack count between calls.
        archer.aoos_used_round_marker = -1
        rapid = self._attack_bonuses(
            archer, enc, grid, options={"rapid_shot": True},
        )
        # With Rapid Shot the highest-BAB attack appears twice (at top
        # BAB - 2 each). Plus the same iteratives all shifted by -2.
        # All rapid_shot bonuses = (corresponding normal bonus) - 2,
        # plus an extra +N-2 inserted at the front.
        self.assertEqual(len(rapid), len(normal) + 1)
        # Every entry in `rapid` after the first one should equal
        # the corresponding entry in `normal` minus 2.
        for n, r in zip(normal, rapid[1:]):
            self.assertEqual(r, n - 2)
        # The first rapid-shot attack is at top BAB - 2, which equals
        # the first normal attack - 2.
        self.assertEqual(rapid[0], normal[0] - 2)


class TestRapidShotGuards(unittest.TestCase):
    def test_no_feat_no_extra_attack(self):
        # Even if rapid_shot=True is requested, no feat = no extra attack.
        archer, _, enc, grid = _setup(11, has_rapid_shot=False)
        result = _full_attack(
            archer, enc, grid, options={"rapid_shot": True},
        )
        n = sum(1 for e in result.events if e.kind.startswith("full_attack_"))
        # BAB 11 without Rapid Shot = 3 attacks.
        self.assertEqual(n, 3)

    def test_melee_attack_no_rapid_shot(self):
        # Even with the feat, Rapid Shot doesn't apply to melee weapons.
        # Build a melee orc with the feat and request rapid_shot.
        archer = combatant_from_monster(
            REGISTRY.get_monster("orc"), (5, 5), "team_a",
        )
        archer.bases["bab"] = 11
        archer.extra_feats = ["rapid_shot"]
        # First attack option is the orc's melee falchion — leave as-is.
        target = combatant_from_monster(
            REGISTRY.get_monster("orc"), (6, 5), "team_b",
        )
        target.max_hp = 9999
        target.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(archer)
        grid.place(target)
        enc = Encounter.begin(grid, [archer, target], Roller(seed=1))
        result = _full_attack(
            archer, enc, grid, options={"rapid_shot": True},
        )
        n = sum(1 for e in result.events if e.kind.startswith("full_attack_"))
        # BAB 11 melee = 3 attacks (no rapid shot bump).
        self.assertEqual(n, 3)


if __name__ == "__main__":
    unittest.main()
