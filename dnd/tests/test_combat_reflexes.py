"""Tests for Combat Reflexes — extra AoOs per round equal to Dex mod."""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import (
    combatant_from_character,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import _aoo_limit, _can_take_aoo, _do_aoo


REGISTRY = default_registry()


def _fighter(feats, scores=None, free_ability="dex"):
    req = CharacterRequest.from_dict({
        "name": "Edric", "race": "human", "class": "fighter",
        "alignment": "lawful_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": scores or {"str": 14, "dex": 16, "con": 14,
                                 "int": 10, "wis": 10, "cha": 10}},
        "free_ability_choice": free_ability,
        "feats": feats,
        "skill_ranks": {"climb": 1, "swim": 1},
        "bonus_languages": [],
        "class_choices": {"fighter_bonus_feat": "weapon_focus_longsword"},
    })
    char = create_character(req, REGISTRY)
    return combatant_from_character(char, REGISTRY, (5, 5), "x")


class TestAooLimit(unittest.TestCase):
    def test_default_limit_is_one(self):
        # A goblin has no combat_reflexes; baseline is 1 AoO/round.
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        self.assertEqual(_aoo_limit(g), 1)

    def test_combat_reflexes_adds_dex_mod(self):
        # Fighter Dex 18 (16 base + 2 racial) → +4 mod → 5 AoOs/round.
        f = _fighter(["combat_reflexes", "iron_will"])
        self.assertEqual(_aoo_limit(f), 1 + 4)

    def test_combat_reflexes_low_dex_minimum_one(self):
        # If Dex mod is negative or zero, limit is at least 1.
        # Point-buy 20: 10 + 0 + 5 + 3 + 1 + 1 = 20. Free ability bump
        # goes to str so dex stays 10.
        f = _fighter(
            ["combat_reflexes", "iron_will"],
            scores={"str": 16, "dex": 10, "con": 14,
                    "int": 13, "wis": 11, "cha": 11},
            free_ability="str",
        )
        self.assertEqual(_aoo_limit(f), 1)


class TestAooThrottling(unittest.TestCase):
    def test_first_aoo_allowed(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        self.assertTrue(_can_take_aoo(g, current_round=1))

    def test_second_aoo_blocked_without_combat_reflexes(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        # Manually consume 1 AoO this round.
        g.aoos_used_round_marker = 1
        g.aoos_used_this_round = 1
        self.assertFalse(_can_take_aoo(g, current_round=1))

    def test_aoo_count_resets_next_round(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        g.aoos_used_round_marker = 1
        g.aoos_used_this_round = 1
        # Different round → counter resets, AoO allowed.
        self.assertTrue(_can_take_aoo(g, current_round=2))

    def test_combat_reflexes_allows_multiple(self):
        f = _fighter(["combat_reflexes", "iron_will"])
        # Dex +4 → 5 AoOs/round. Consume 4, 5th still allowed.
        f.aoos_used_round_marker = 1
        f.aoos_used_this_round = 4
        self.assertTrue(_can_take_aoo(f, current_round=1))
        f.aoos_used_this_round = 5
        self.assertFalse(_can_take_aoo(f, current_round=1))


class TestAooEndToEnd(unittest.TestCase):
    def test_second_aoo_in_round_blocked_without_feat(self):
        threatener = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (5, 5), "team_a",
        )
        target = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (6, 5), "team_b",
        )
        target.max_hp = 9999
        target.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(threatener)
        grid.place(target)
        enc = Encounter.begin(grid, [threatener, target], Roller(seed=1))

        events = []
        # First AoO this round: fires.
        _do_aoo(threatener, target, grid, events, encounter=enc)
        first_aoos = [e for e in events if e.kind == "aoo"]
        self.assertEqual(len(first_aoos), 1)
        # Second AoO same round: throttled, no event.
        events.clear()
        _do_aoo(threatener, target, grid, events, encounter=enc)
        second_aoos = [e for e in events if e.kind == "aoo"]
        self.assertEqual(len(second_aoos), 0)


if __name__ == "__main__":
    unittest.main()
