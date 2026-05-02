"""Tests for the PF1 firing-into-melee -4 penalty.

PF1 RAW: ranged attacks against a target engaged in melee with another
combatant suffer -4. Negated by Precise Shot.
"""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import _firing_into_melee_penalty


REGISTRY = default_registry()


def _three_combatant_setup(target_engaged: bool):
    """Archer + their ranged target (a goblin), and optionally a
    third combatant adjacent to the target (which makes the target
    'engaged in melee')."""
    archer = combatant_from_monster(
        REGISTRY.get_monster("goblin"), (0, 5), "team_a",
    )
    target = combatant_from_monster(
        REGISTRY.get_monster("goblin"), (10, 5), "team_b",
    )
    grid = Grid(width=20, height=20)
    grid.place(archer)
    grid.place(target)
    others = []
    if target_engaged:
        engager = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (11, 5), "team_a",
        )
        grid.place(engager)
        others.append(engager)
    enc = Encounter.begin(
        grid, [archer, target] + others, Roller(seed=1),
    )
    return archer, target, grid, enc


class TestFiringIntoMelee(unittest.TestCase):
    def test_solo_target_no_penalty(self):
        archer, target, grid, enc = _three_combatant_setup(target_engaged=False)
        self.assertEqual(
            _firing_into_melee_penalty(archer, target, grid, enc, True), 0,
        )

    def test_engaged_target_minus_4(self):
        archer, target, grid, enc = _three_combatant_setup(target_engaged=True)
        self.assertEqual(
            _firing_into_melee_penalty(archer, target, grid, enc, True), -4,
        )

    def test_melee_attack_no_penalty(self):
        archer, target, grid, enc = _three_combatant_setup(target_engaged=True)
        # Even with a third combatant adjacent to target, melee attacks
        # don't suffer this particular penalty (it's a ranged-only rule).
        self.assertEqual(
            _firing_into_melee_penalty(archer, target, grid, enc, False), 0,
        )

    def test_dead_engager_does_not_count(self):
        # If the third combatant is at -10 HP / dead, target isn't really
        # "engaged in melee" anymore.
        archer, target, grid, enc = _three_combatant_setup(target_engaged=True)
        # Find the engager and kill them.
        for ir in enc.initiative:
            c = ir.combatant
            if c.id not in (archer.id, target.id):
                c.current_hp = -50
                c.add_condition("dead")
        self.assertEqual(
            _firing_into_melee_penalty(archer, target, grid, enc, True), 0,
        )


class TestPreciseShotNegates(unittest.TestCase):
    def test_precise_shot_negates_penalty(self):
        # We need a character with Precise Shot. Build a fighter on
        # the fly with the feat.
        from dnd.engine.characters import CharacterRequest, create_character
        from dnd.engine.combatant import combatant_from_character
        req = CharacterRequest.from_dict({
            "name": "Robin", "race": "human", "class": "fighter",
            "alignment": "neutral_good",
            # 5 + 10 + 5 + 0 + 0 + 0 = 20.
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 16, "con": 14,
                           "int": 10, "wis": 10, "cha": 10}},
            "free_ability_choice": "dex",
            "feats": ["point_blank_shot", "precise_shot"],
            "skill_ranks": {"climb": 1, "swim": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "weapon_focus"},
        })
        char = create_character(req, REGISTRY)
        archer = combatant_from_character(char, REGISTRY, (0, 5), "team_a")
        target = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (10, 5), "team_b",
        )
        engager = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (11, 5), "team_a",
        )
        grid = Grid(width=20, height=20)
        grid.place(archer)
        grid.place(target)
        grid.place(engager)
        enc = Encounter.begin(
            grid, [archer, target, engager], Roller(seed=1),
        )
        # Without Precise Shot we'd see -4; with it, 0.
        self.assertEqual(
            _firing_into_melee_penalty(archer, target, grid, enc, True), 0,
        )


if __name__ == "__main__":
    unittest.main()
