"""Tests for HeroRecord + combatant_from_hero_record factory."""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import combatant_from_hero_record
from dnd.engine.content import default_registry
from dnd.sandbox.hero_record import (
    HERO_AT_CASTLE,
    HERO_DEAD,
    HERO_DEPLOYED,
    HeroRecord,
)


REGISTRY = default_registry()


def _fighter_character():
    req = CharacterRequest.from_dict({
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
    })
    return create_character(req, REGISTRY)


class TestHeroRecord(unittest.TestCase):
    def test_construct_defaults(self):
        char = _fighter_character()
        h = HeroRecord(
            id="hero_1", name="Edric", character=char,
            behavior_ref="doctrines/melee_aggressive",
        )
        self.assertEqual(h.status, HERO_AT_CASTLE)
        self.assertEqual(h.current_hp, 0)        # set on first materialization
        self.assertEqual(h.deployment_ids, [])

    def test_round_trip(self):
        char = _fighter_character()
        h = HeroRecord(
            id="hero_1", name="Edric", character=char,
            behavior_ref="doctrines/melee_aggressive",
            plan_ref="plans/two_handed",
            current_hp=10, max_hp=12, current_xp=200,
            deployment_ids=["dep_a", "dep_b"],
        )
        h2 = HeroRecord.from_dict(h.to_dict())
        self.assertEqual(h2.id, h.id)
        self.assertEqual(h2.character.race_id, "human")
        self.assertEqual(h2.character.class_id, "fighter")
        self.assertEqual(h2.current_hp, 10)
        self.assertEqual(h2.max_hp, 12)
        self.assertEqual(h2.deployment_ids, ["dep_a", "dep_b"])

    def test_unknown_status_rejected(self):
        char = _fighter_character()
        h = HeroRecord(
            id="x", name="x", character=char, behavior_ref="b",
        )
        bad = h.to_dict()
        bad["status"] = "wibbly"
        with self.assertRaises(ValueError):
            HeroRecord.from_dict(bad)

    def test_is_alive(self):
        char = _fighter_character()
        h = HeroRecord(id="x", name="x", character=char, behavior_ref="b")
        self.assertTrue(h.is_alive())
        h.status = HERO_DEPLOYED
        self.assertTrue(h.is_alive())
        h.status = HERO_DEAD
        self.assertFalse(h.is_alive())


class TestCombatantFromHeroRecord(unittest.TestCase):
    def test_first_materialization_sets_full_hp(self):
        char = _fighter_character()
        h = HeroRecord(
            id="hero_1", name="Edric", character=char,
            behavior_ref="b",
            current_hp=0,    # uninitialized
        )
        c = combatant_from_hero_record(h, REGISTRY, (5, 5), "patrons")
        self.assertEqual(c.current_hp, c.max_hp)
        self.assertGreater(c.current_hp, 0)
        # Record now caches max_hp + current_hp.
        self.assertEqual(h.max_hp, c.max_hp)
        self.assertEqual(h.current_hp, c.max_hp)

    def test_carry_over_hp_respected(self):
        char = _fighter_character()
        # First materialization to learn max_hp.
        h = HeroRecord(
            id="hero_1", name="Edric", character=char, behavior_ref="b",
        )
        c0 = combatant_from_hero_record(h, REGISTRY, (5, 5), "patrons")
        max_hp = c0.max_hp
        # Hero comes home from a fight at half HP; next deployment should
        # start there.
        h.current_hp = max_hp // 2
        c1 = combatant_from_hero_record(h, REGISTRY, (5, 5), "patrons")
        self.assertEqual(c1.current_hp, max_hp // 2)
        self.assertEqual(c1.max_hp, max_hp)

    def test_carry_over_clamped_to_max(self):
        char = _fighter_character()
        h = HeroRecord(
            id="hero_1", name="Edric", character=char, behavior_ref="b",
            current_hp=99999,  # over-healed via some bug?
        )
        c = combatant_from_hero_record(h, REGISTRY, (5, 5), "patrons")
        self.assertEqual(c.current_hp, c.max_hp)


if __name__ == "__main__":
    unittest.main()
