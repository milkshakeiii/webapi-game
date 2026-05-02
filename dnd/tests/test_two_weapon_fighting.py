"""Tests for two-weapon fighting — off-hand weapon model + paired penalties."""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import combatant_from_character, combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


def _ranger(feats=None, offhand="shortsword"):
    """Build a ranger with shortsword + offhand. Default offhand =
    light shortsword for testing the -2/-2 pair with TWF feat."""
    body = {
        "name": "Twinblade", "race": "human", "class": "ranger",
        "alignment": "neutral_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 14, "dex": 16, "con": 14,
                       "int": 10, "wis": 10, "cha": 10}},
        "free_ability_choice": "dex",
        "feats": feats or ["weapon_focus", "iron_will"],
        "skill_ranks": {"perception": 1, "survival": 1},
        "bonus_languages": [],
        "equipment": {"offhand": offhand},
    }
    char = create_character(CharacterRequest.from_dict(body), REGISTRY)
    return char, combatant_from_character(char, REGISTRY, (5, 5), "x")


def _setup(feats=None, offhand="shortsword"):
    char, ranger = _ranger(feats=feats, offhand=offhand)
    target = combatant_from_monster(
        REGISTRY.get_monster("orc"), (6, 5), "y",
    )
    target.max_hp = 9999
    target.current_hp = 9999
    grid = Grid(width=12, height=12)
    grid.place(ranger)
    grid.place(target)
    enc = Encounter.begin(grid, [ranger, target], Roller(seed=1))
    return ranger, target, enc, grid


def _full_attack(ranger, enc, grid, options=None):
    do = {"composite": "full_attack", "args": {"target": "enemy.closest"}}
    if options:
        do["args"]["options"] = options
    script = BehaviorScript(name="twf", rules=[Rule(do=do)])
    intent = Interpreter(script).pick_turn(ranger, enc, grid)
    return execute_turn(ranger, intent, enc, grid, Roller(seed=1))


def _attack_bonuses(events):
    bonuses = []
    for e in events:
        if not e.kind.startswith("full_attack_"):
            continue
        for line in e.detail.get("trace", []):
            if line.startswith("attack "):
                parts = line.split(" = ")[0]
                bonuses.append(int(parts.rsplit("+ ", 1)[1]))
                break
    return bonuses


# ---------------------------------------------------------------------------
# Off-hand weapon presence
# ---------------------------------------------------------------------------


class TestOffhandWeaponModel(unittest.TestCase):
    def test_offhand_attack_option_added(self):
        _, ranger = _ranger(offhand="shortsword")
        offhand = [a for a in ranger.attack_options if a.get("is_offhand")]
        self.assertEqual(len(offhand), 1)
        self.assertEqual(offhand[0]["weapon_id"], "shortsword")

    def test_offhand_damage_uses_half_str(self):
        # Ranger with str 14 (mod +2). Off-hand damage_bonus = +1 (str//2).
        _, ranger = _ranger(offhand="shortsword")
        offhand = [a for a in ranger.attack_options if a.get("is_offhand")][0]
        self.assertEqual(offhand["damage_bonus"], 1)

    def test_no_offhand_no_offhand_attack_option(self):
        body = {
            "name": "Solo", "race": "human", "class": "ranger",
            "alignment": "neutral_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 16, "con": 14,
                           "int": 10, "wis": 10, "cha": 10}},
            "free_ability_choice": "dex",
            "feats": ["weapon_focus", "iron_will"],
            "skill_ranks": {"perception": 1, "survival": 1},
            "bonus_languages": [],
        }
        char = create_character(CharacterRequest.from_dict(body), REGISTRY)
        c = combatant_from_character(char, REGISTRY, (5, 5), "x")
        offhand = [a for a in c.attack_options if a.get("is_offhand")]
        self.assertEqual(offhand, [])


# ---------------------------------------------------------------------------
# TWF in full attack
# ---------------------------------------------------------------------------


class TestTwoWeaponFightingFullAttack(unittest.TestCase):
    def test_twf_adds_offhand_attack(self):
        ranger, _, enc, grid = _setup()
        # Without TWF option: 1 attack (BAB +1 ranger).
        normal = _full_attack(ranger, enc, grid)
        n_normal = sum(1 for e in normal.events
                       if e.kind.startswith("full_attack_"))
        self.assertEqual(n_normal, 1)
        # With TWF option: 1 primary + 1 off-hand = 2.
        ranger.aoos_used_round_marker = -1  # reset between calls
        twf = _full_attack(ranger, enc, grid,
                           options={"two_weapon_fighting": True})
        n_twf = sum(1 for e in twf.events
                    if e.kind.startswith("full_attack_"))
        self.assertEqual(n_twf, 2)

    def test_no_feat_paired_penalty_minus_6_minus_10(self):
        # Ranger has no TWF feat → -6 primary, -10 off-hand. Use feats
        # that don't add per-weapon attack bonuses so we can compare
        # raw numbers.
        ranger, _, enc, grid = _setup(feats=["iron_will", "endurance"])
        result = _full_attack(ranger, enc, grid,
                              options={"two_weapon_fighting": True})
        bonuses = _attack_bonuses(result.events)
        self.assertEqual(len(bonuses), 2)
        offhand_opt = next(a for a in ranger.attack_options
                           if a.get("is_offhand"))
        primary_opt = ranger.attack_options[0]
        self.assertEqual(bonuses[0], primary_opt["attack_bonus"] - 6)
        self.assertEqual(bonuses[1], offhand_opt["attack_bonus"] - 10)

    def test_with_feat_light_offhand_minus_2_minus_2(self):
        ranger, _, enc, grid = _setup(
            feats=["iron_will", "two_weapon_fighting"],
            offhand="shortsword",
        )
        result = _full_attack(ranger, enc, grid,
                              options={"two_weapon_fighting": True})
        bonuses = _attack_bonuses(result.events)
        self.assertEqual(len(bonuses), 2)
        offhand_opt = next(a for a in ranger.attack_options
                           if a.get("is_offhand"))
        primary_opt = ranger.attack_options[0]
        self.assertEqual(bonuses[0], primary_opt["attack_bonus"] - 2)
        self.assertEqual(bonuses[1], offhand_opt["attack_bonus"] - 2)

    def test_with_feat_non_light_offhand_minus_4_minus_8(self):
        # TWF feat with a one-handed (non-light) off-hand = -4/-8.
        ranger, _, enc, grid = _setup(
            feats=["iron_will", "two_weapon_fighting"],
            offhand="longsword",
        )
        result = _full_attack(ranger, enc, grid,
                              options={"two_weapon_fighting": True})
        bonuses = _attack_bonuses(result.events)
        offhand_opt = next(a for a in ranger.attack_options
                           if a.get("is_offhand"))
        primary_opt = ranger.attack_options[0]
        self.assertEqual(bonuses[0], primary_opt["attack_bonus"] - 4)
        self.assertEqual(bonuses[1], offhand_opt["attack_bonus"] - 8)


if __name__ == "__main__":
    unittest.main()
