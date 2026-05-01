"""Tests for the background tick worker.

These run with a very fast tick interval so the test suite stays
sub-second per test.
"""

from __future__ import annotations

import os
import shutil
import tempfile
import time
import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.content import default_registry
from dnd.sandbox.castle import new_castle
from dnd.sandbox.deployment import (
    ORDER_CREATE_CASTLE,
    ORDER_SPAWN_HERO,
    new_order,
)
from dnd.sandbox.hero_record import HeroRecord
from dnd.sandbox.worker import TickWorker
from dnd.sandbox.world import new_world


REGISTRY = default_registry()


def _spawn_setup():
    w = new_world(width=20, height=20, tick_interval_s=0.01)
    castle = new_castle("Hill", "h@y.com", (5, 5))
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
    hero = HeroRecord(id="hero_1", name="Edric", character=char,
                      behavior_ref="b")
    return w, castle, hero


class TestTickWorker(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="dnd_worker_test_")
        self._prev = os.environ.get("DND_DATA_DIR")
        os.environ["DND_DATA_DIR"] = self._tmp

    def tearDown(self):
        if self._prev is None:
            del os.environ["DND_DATA_DIR"]
        else:
            os.environ["DND_DATA_DIR"] = self._prev
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_starts_and_stops(self):
        w, _, _ = _spawn_setup()
        worker = TickWorker(w, REGISTRY, persist=False)
        worker.start()
        try:
            time.sleep(0.05)  # let it tick a few times
            self.assertTrue(worker.is_running())
            self.assertGreater(worker.tick_count, 0)
        finally:
            worker.stop(timeout=1.0)
        self.assertFalse(worker.is_running())

    def test_drains_orders_submitted_concurrently(self):
        w, castle, hero = _spawn_setup()
        worker = TickWorker(w, REGISTRY, persist=False)
        worker.start()
        try:
            w.order_queue.submit(
                new_order(None, ORDER_CREATE_CASTLE, {"castle": castle}),
            )
            w.order_queue.submit(
                new_order(castle.id, ORDER_SPAWN_HERO, {"hero": hero}),
            )
            # Wait until the hero is registered (or time out).
            deadline = time.monotonic() + 2.0
            while time.monotonic() < deadline:
                if hero.id in w.castles.get(castle.id, _SentinelCastle()).roster:
                    break
                time.sleep(0.01)
        finally:
            worker.stop(timeout=1.0)
        self.assertIn(castle.id, w.castles)
        self.assertIn(hero.id, w.castles[castle.id].roster)

    def test_persistence_writes_files(self):
        w, castle, hero = _spawn_setup()
        worker = TickWorker(w, REGISTRY, persist=True)
        worker.start()
        try:
            w.order_queue.submit(
                new_order(None, ORDER_CREATE_CASTLE, {"castle": castle}),
            )
            deadline = time.monotonic() + 2.0
            while time.monotonic() < deadline:
                if castle.id in w.castles:
                    break
                time.sleep(0.01)
            time.sleep(0.05)  # give the worker time to persist
        finally:
            worker.stop(timeout=1.0)
        from pathlib import Path
        castle_file = Path(self._tmp) / "castles" / f"{castle.id}.json"
        world_file = Path(self._tmp) / "world.json"
        self.assertTrue(castle_file.exists())
        self.assertTrue(world_file.exists())

    def test_idempotent_start(self):
        w, _, _ = _spawn_setup()
        worker = TickWorker(w, REGISTRY, persist=False)
        worker.start()
        try:
            worker.start()  # second start is a no-op
            time.sleep(0.05)
            self.assertTrue(worker.is_running())
        finally:
            worker.stop(timeout=1.0)


class _SentinelCastle:
    roster: dict = {}


if __name__ == "__main__":
    unittest.main()
