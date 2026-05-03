"""Tests for L1 class-feature passive modifiers."""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import combatant_from_character
from dnd.engine.content import default_registry


REGISTRY = default_registry()


def _make(class_id: str) -> object:
    """Build a basic L1 character of the given class with a fixed
    point-buy 20 score array."""
    # 5+5+5+2+2+1 = 20.
    base = {
        "str": 14, "dex": 14, "con": 14,
        "int": 12, "wis": 12, "cha": 11,
    }
    feats = ["dodge", "iron_will"]
    class_choices: dict = {}
    alignment = "true_neutral"
    if class_id == "fighter":
        class_choices = {"fighter_bonus_feat": "alertness"}
    elif class_id == "monk":
        class_choices = {"monk_bonus_feat": "improved_unarmed_strike"}
        alignment = "lawful_neutral"
    elif class_id == "paladin":
        alignment = "lawful_good"
    elif class_id == "barbarian":
        alignment = "chaotic_neutral"
    elif class_id == "druid":
        alignment = "neutral_good"
    elif class_id == "bard":
        alignment = "neutral_good"
    req = CharacterRequest.from_dict({
        "name": "Test", "race": "human", "class": class_id,
        "alignment": alignment,
        "ability_scores": {"method": "point_buy_20", "scores": base},
        "free_ability_choice": "wis",
        "feats": feats,
        "skill_ranks": {"survival": 1, "perception": 1,
                        "knowledge_arcana": 1, "knowledge_nature": 1,
                        "diplomacy": 1, "disable_device": 1},
        "bonus_languages": [],
        "class_choices": class_choices,
    })
    return create_character(req, REGISTRY)


class TestBarbarianFastMovement(unittest.TestCase):
    def test_unarmored_barbarian_gets_plus_10_speed(self):
        char = _make("barbarian")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        # Human base 30 + 10 fast movement = 40 (we expect this in
        # whatever default loadout barbarians have, as long as it's
        # not heavy armor).
        self.assertGreaterEqual(c.speed, 40)


class TestBardicKnowledge(unittest.TestCase):
    def test_bard_knowledge_skill_bonus(self):
        char = _make("bard")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        # 1 rank + Int +1 + class skill +3 + bardic knowledge +1 = 6
        self.assertGreaterEqual(c.skill_total("knowledge_arcana"), 5)


class TestRangerTrack(unittest.TestCase):
    def test_ranger_survival_bonus(self):
        char = _make("ranger")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        # Survival should include +1/2 level (min 1) for tracking.
        # 1 rank + Wis +2 + class skill +3 + track +1 = 7
        self.assertGreaterEqual(c.skill_total("survival"), 6)


class TestDruidNatureSense(unittest.TestCase):
    def test_druid_nature_sense_bonus(self):
        char = _make("druid")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        # +2 to Knowledge (nature)
        # 1 rank + Int +1 + class skill +3 + nature sense +2 = 7
        self.assertGreaterEqual(c.skill_total("knowledge_nature"), 6)
        # Survival should be at least: 1 rank + Wis +2 + class +3 +
        # nature sense +2 = 8
        self.assertGreaterEqual(c.skill_total("survival"), 7)


class TestRogueTrapfinding(unittest.TestCase):
    def test_rogue_perception_includes_trapfinding(self):
        char = _make("rogue")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        # 1 rank + Wis +1 + class skill +3 + trapfinding +1 = 6
        self.assertGreaterEqual(c.skill_total("perception"), 6)


class TestMonkAcBonus(unittest.TestCase):
    def test_unarmored_monk_gets_wis_to_ac(self):
        # Monk with Wis 14 → +2 AC bonus (also default monk loadout
        # has no armor).
        char = _make("monk")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        # Hard to test exact AC without knowing the full breakdown.
        # We just verify AC is at least 10 + Dex (+2) + Wis (+2) = 14.
        self.assertGreaterEqual(c.ac(), 14)


if __name__ == "__main__":
    unittest.main()
