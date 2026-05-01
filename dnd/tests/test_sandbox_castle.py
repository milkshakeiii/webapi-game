"""Tests for the Castle dataclass + renown ledger + persistence."""

from __future__ import annotations

import os
import shutil
import tempfile
import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.content import default_registry
from dnd.sandbox.castle import (
    NEW_CASTLE_STARTING_RENOWN,
    RENOWN_COST_L1_HERO,
    Castle,
    load_all_castles,
    load_castle,
    new_castle,
    save_castle,
)
from dnd.sandbox.hero_record import HERO_DEAD, HeroRecord


REGISTRY = default_registry()


def _fighter_record(hid="hero_1"):
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
    char = create_character(req, REGISTRY)
    return HeroRecord(
        id=hid, name="Edric", character=char, behavior_ref="b",
    )


class TestCastleConstruction(unittest.TestCase):
    def test_new_castle_defaults(self):
        c = new_castle("Hill of the Hawk", "h@example.com", (10, 10))
        self.assertEqual(c.renown, NEW_CASTLE_STARTING_RENOWN)
        self.assertEqual(c.lifetime_renown, NEW_CASTLE_STARTING_RENOWN)
        self.assertEqual(c.roster, {})
        self.assertEqual(c.graveyard, {})
        self.assertTrue(c.id.startswith("castle_"))

    def test_explicit_id(self):
        c = new_castle("X", "x@y.com", (0, 0), castle_id="castle_test_xyz")
        self.assertEqual(c.id, "castle_test_xyz")


class TestRenownLedger(unittest.TestCase):
    def test_credit_increases_balances(self):
        c = new_castle("X", "x@y.com", (0, 0))
        c.credit(50, "deployment_reward", tick=10, ref="dep_1")
        self.assertEqual(c.renown, NEW_CASTLE_STARTING_RENOWN + 50)
        self.assertEqual(c.lifetime_renown, NEW_CASTLE_STARTING_RENOWN + 50)
        self.assertEqual(len(c.renown_ledger), 1)
        e = c.renown_ledger[0]
        self.assertEqual(e.delta, 50)
        self.assertEqual(e.tick, 10)

    def test_debit_decreases_balance(self):
        c = new_castle("X", "x@y.com", (0, 0))
        c.debit(RENOWN_COST_L1_HERO, "spawn_hero", tick=5)
        self.assertEqual(c.renown, NEW_CASTLE_STARTING_RENOWN - RENOWN_COST_L1_HERO)
        # Lifetime renown is NOT decreased by spending.
        self.assertEqual(c.lifetime_renown, NEW_CASTLE_STARTING_RENOWN)
        self.assertEqual(c.renown_ledger[0].delta, -RENOWN_COST_L1_HERO)

    def test_debit_overspend_raises(self):
        c = new_castle("X", "x@y.com", (0, 0))
        with self.assertRaises(ValueError):
            c.debit(c.renown + 1, "overspend", tick=1)

    def test_zero_amounts_no_op(self):
        c = new_castle("X", "x@y.com", (0, 0))
        c.credit(0, "noop", tick=1)
        c.debit(0, "noop", tick=1)
        self.assertEqual(c.renown_ledger, [])

    def test_negative_amount_rejected(self):
        c = new_castle("X", "x@y.com", (0, 0))
        with self.assertRaises(ValueError):
            c.credit(-5, "bug", tick=1)
        with self.assertRaises(ValueError):
            c.debit(-5, "bug", tick=1)


class TestRoster(unittest.TestCase):
    def test_add_hero(self):
        c = new_castle("X", "x@y.com", (0, 0))
        h = _fighter_record()
        c.add_hero(h)
        self.assertIn(h.id, c.roster)
        self.assertEqual(c.get_hero(h.id), h)

    def test_add_hero_duplicate_rejected(self):
        c = new_castle("X", "x@y.com", (0, 0))
        h = _fighter_record()
        c.add_hero(h)
        with self.assertRaises(ValueError):
            c.add_hero(h)

    def test_bury_moves_to_graveyard(self):
        c = new_castle("X", "x@y.com", (0, 0))
        h = _fighter_record()
        c.add_hero(h)
        c.bury(h.id, died_at_tick=42)
        self.assertNotIn(h.id, c.roster)
        self.assertIn(h.id, c.graveyard)
        self.assertEqual(c.graveyard[h.id].status, HERO_DEAD)
        self.assertIsNotNone(c.graveyard[h.id].died_at)

    def test_bury_unknown_raises(self):
        c = new_castle("X", "x@y.com", (0, 0))
        with self.assertRaises(KeyError):
            c.bury("not_in_roster", died_at_tick=1)

    def test_get_hero_finds_in_graveyard_too(self):
        c = new_castle("X", "x@y.com", (0, 0))
        h = _fighter_record()
        c.add_hero(h)
        c.bury(h.id, died_at_tick=1)
        self.assertEqual(c.get_hero(h.id).status, HERO_DEAD)


class TestCastlePersistence(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="dnd_castle_test_")
        self._prev = os.environ.get("DND_DATA_DIR")
        os.environ["DND_DATA_DIR"] = self._tmp

    def tearDown(self):
        if self._prev is None:
            del os.environ["DND_DATA_DIR"]
        else:
            os.environ["DND_DATA_DIR"] = self._prev
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_round_trip(self):
        c = new_castle("Hill", "h@y.com", (10, 12))
        c.credit(20, "first_kill", tick=5)
        c.add_hero(_fighter_record("hero_a"))
        c.library_behaviors["aggressive"] = "{name: 'a'}"
        save_castle(c)
        loaded = load_castle(c.id)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.name, "Hill")
        self.assertEqual(loaded.home_position, (10, 12))
        self.assertEqual(loaded.renown, 120)
        self.assertEqual(loaded.lifetime_renown, 120)
        self.assertIn("hero_a", loaded.roster)
        self.assertEqual(loaded.library_behaviors["aggressive"], "{name: 'a'}")
        self.assertEqual(len(loaded.renown_ledger), 1)

    def test_load_missing_returns_none(self):
        self.assertIsNone(load_castle("castle_does_not_exist"))

    def test_load_all_castles(self):
        c1 = new_castle("A", "a@y.com", (0, 0))
        c2 = new_castle("B", "b@y.com", (1, 1))
        save_castle(c1)
        save_castle(c2)
        all_ = load_all_castles()
        self.assertIn(c1.id, all_)
        self.assertIn(c2.id, all_)

    def test_load_all_empty_when_no_dir(self):
        self.assertEqual(load_all_castles(), {})


if __name__ == "__main__":
    unittest.main()
