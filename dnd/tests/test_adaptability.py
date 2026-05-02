"""Tests for the Half-elf Adaptability racial trait.

PF1: half-elves get a bonus Skill Focus feat at L1 in any one skill.
"""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import combatant_from_character
from dnd.engine.content import default_registry


REGISTRY = default_registry()


def _half_elf_request(skill: str | None = None):
    body = {
        "name": "Lirin", "race": "half_elf", "class": "bard",
        "alignment": "chaotic_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 10, "dex": 14, "con": 13,
                       "int": 12, "wis": 10, "cha": 16}},
        "free_ability_choice": "cha",
        "feats": ["weapon_finesse"],
        "skill_ranks": {"perform": 1, "diplomacy": 1},
        "bonus_languages": ["elven"],
    }
    if skill is not None:
        body["adaptability_skill_focus"] = skill
    return CharacterRequest.from_dict(body)


class TestAdaptability(unittest.TestCase):
    def test_default_grants_skill_focus_perception(self):
        char = create_character(_half_elf_request(), REGISTRY)
        self.assertIn("skill_focus_perception", char.feats)

    def test_explicit_skill_choice_honored(self):
        char = create_character(_half_elf_request("diplomacy"), REGISTRY)
        self.assertIn("skill_focus_diplomacy", char.feats)
        self.assertNotIn("skill_focus_perception", char.feats)

    def test_skill_focus_modifier_lands_on_combatant(self):
        char = create_character(_half_elf_request("diplomacy"), REGISTRY)
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        # +3 Skill Focus to diplomacy; class skill bonus +3 (bard);
        # +3 Cha mod (16 base + 2 racial → 18 → +4? Wait: half-elf has
        # +2 to chosen ability, so cha 16 + 2 = 18, +4. + 1 rank.
        # 1 rank + 4 cha + 3 class skill + 3 skill focus = 11.
        self.assertEqual(c.skill_total("diplomacy"), 11)

    def test_non_half_elf_does_not_get_adaptability_feat(self):
        # Sanity: a human shouldn't get the auto-feat even if the field
        # is set (it's silently ignored — intentional).
        body = {
            "name": "Edric", "race": "human", "class": "fighter",
            "alignment": "lawful_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 16, "dex": 14, "con": 14,
                           "int": 10, "wis": 10, "cha": 10}},
            "free_ability_choice": "str",
            "feats": ["power_attack", "weapon_focus"],
            "skill_ranks": {"climb": 1, "swim": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "cleave"},
            "adaptability_skill_focus": "perception",
        }
        char = create_character(
            CharacterRequest.from_dict(body), REGISTRY,
        )
        # Human shouldn't have the auto-applied skill focus.
        self.assertNotIn("skill_focus_perception", char.feats)


if __name__ == "__main__":
    unittest.main()
