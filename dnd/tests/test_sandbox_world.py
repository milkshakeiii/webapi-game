"""Tests for the sandbox world module: clock, location, queue, world."""

from __future__ import annotations

import os
import tempfile
import threading
import unittest
from datetime import datetime, timezone

from dnd.sandbox.boot import load_world, save_world
from dnd.sandbox.world import (
    DEFAULT_RESPAWN_TICKS,
    LOC_ACTIVE,
    LOC_CLEARED,
    Location,
    OrderQueue,
    World,
    WorldClock,
    new_world,
)


class TestWorldClock(unittest.TestCase):
    def test_round_trip(self):
        c = WorldClock(
            started_at=datetime(2026, 4, 30, 12, 0, tzinfo=timezone.utc),
            tick_number=42,
            tick_interval_s=6.0,
        )
        d = c.to_dict()
        c2 = WorldClock.from_dict(d)
        self.assertEqual(c.tick_number, c2.tick_number)
        self.assertEqual(c.tick_interval_s, c2.tick_interval_s)
        self.assertEqual(c.started_at, c2.started_at)


class TestLocation(unittest.TestCase):
    def _data(self):
        return {
            "id": "loc_x",
            "name": "X Camp",
            "position": [10, 20],
            "kind": "camp",
            "description": "test",
            "resident_template": "goblin",
            "base_renown": 10,
            "state": "active",
            "respawn_ticks": 14400,
        }

    def test_round_trip(self):
        loc = Location.from_dict(self._data())
        self.assertEqual(loc.id, "loc_x")
        self.assertEqual(loc.position, (10, 20))
        self.assertEqual(loc.state, LOC_ACTIVE)
        again = Location.from_dict(loc.to_dict())
        self.assertEqual(again, loc)

    def test_default_respawn_ticks(self):
        d = self._data()
        del d["respawn_ticks"]
        loc = Location.from_dict(d)
        self.assertEqual(loc.respawn_ticks, DEFAULT_RESPAWN_TICKS)

    def test_unknown_state_rejected(self):
        d = self._data()
        d["state"] = "wibbly"
        with self.assertRaises(ValueError):
            Location.from_dict(d)

    def test_cleared_persists_who_and_when(self):
        loc = Location.from_dict(self._data())
        loc.state = LOC_CLEARED
        loc.cleared_at_tick = 1234
        loc.cleared_by_castle = "castle_abc"
        re = Location.from_dict(loc.to_dict())
        self.assertEqual(re.state, LOC_CLEARED)
        self.assertEqual(re.cleared_at_tick, 1234)
        self.assertEqual(re.cleared_by_castle, "castle_abc")


class TestOrderQueue(unittest.TestCase):
    def test_submit_drain(self):
        q = OrderQueue()
        q.submit("a")
        q.submit("b")
        self.assertEqual(len(q), 2)
        self.assertEqual(q.drain(), ["a", "b"])
        self.assertEqual(len(q), 0)

    def test_drain_when_empty(self):
        q = OrderQueue()
        self.assertEqual(q.drain(), [])

    def test_thread_safe_concurrent_submit(self):
        q = OrderQueue()
        n_threads = 8
        per_thread = 200
        def producer(start):
            for i in range(per_thread):
                q.submit(start + i)
        threads = [threading.Thread(target=producer, args=(t * per_thread,))
                   for t in range(n_threads)]
        for t in threads: t.start()
        for t in threads: t.join()
        items = q.drain()
        self.assertEqual(len(items), n_threads * per_thread)
        # Every value 0..total-1 should appear once.
        self.assertEqual(sorted(items), list(range(n_threads * per_thread)))


class TestWorld(unittest.TestCase):
    def test_new_world_defaults(self):
        w = new_world()
        self.assertEqual(w.width, 200)
        self.assertEqual(w.height, 200)
        self.assertEqual(w.clock.tick_number, 0)
        self.assertEqual(w.clock.tick_interval_s, 6.0)
        self.assertEqual(w.locations, {})

    def test_round_trip_through_dict(self):
        w = new_world()
        w.locations["x"] = Location(
            id="x", name="X", position=(1, 2), kind="camp",
            description="", resident_template="goblin", base_renown=5,
        )
        w.impassable_cells.add((10, 10))
        w.clock.tick_number = 5
        w2 = World.from_dict(w.to_dict())
        self.assertEqual(w2.width, w.width)
        self.assertEqual(w2.clock.tick_number, 5)
        self.assertIn("x", w2.locations)
        self.assertEqual(w2.locations["x"].position, (1, 2))
        self.assertIn((10, 10), w2.impassable_cells)

    def test_publish_snapshot_updates_current(self):
        w = new_world()
        w.locations["x"] = Location(
            id="x", name="X", position=(1, 2), kind="camp",
            description="", resident_template="goblin", base_renown=5,
        )
        # Before publish, current_snapshot returns a default-shaped dict.
        snap0 = w.current_snapshot
        self.assertEqual(snap0["locations"], {})
        w.clock.tick_number = 3
        w.publish_snapshot()
        snap1 = w.current_snapshot
        self.assertEqual(snap1["tick"], 3)
        self.assertIn("x", snap1["locations"])

    def test_snapshot_pointer_is_atomic_swap(self):
        # Simulate the tick worker publishing while readers deref —
        # readers should always see a coherent snapshot.
        w = new_world()
        w.publish_snapshot()
        seen = []
        stop = threading.Event()
        def reader():
            while not stop.is_set():
                snap = w.current_snapshot
                seen.append(snap["tick"])
        rt = threading.Thread(target=reader, daemon=True)
        rt.start()
        for n in range(1, 100):
            w.clock.tick_number = n
            w.publish_snapshot()
        stop.set()
        rt.join(timeout=1.0)
        # Every observed tick is one we actually published (i.e. an int
        # in [0, 99]). No half-built or junk values.
        for t in seen:
            self.assertIsInstance(t, int)
            self.assertGreaterEqual(t, 0)
            self.assertLessEqual(t, 99)


# ---------------------------------------------------------------------------
# Boot
# ---------------------------------------------------------------------------


class TestBoot(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="dnd_boot_test_")
        self._prev = os.environ.get("DND_DATA_DIR")
        os.environ["DND_DATA_DIR"] = self._tmp

    def tearDown(self):
        if self._prev is None:
            del os.environ["DND_DATA_DIR"]
        else:
            os.environ["DND_DATA_DIR"] = self._prev
        import shutil
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_first_boot_creates_world_from_content(self):
        w = load_world(tick_interval_s=0.05)
        # All bundled locations should be present.
        self.assertIn("loc_goblin_camp_north", w.locations)
        self.assertIn("loc_orc_warband", w.locations)
        self.assertIn("loc_skeleton_crypt", w.locations)
        self.assertIn("loc_kobold_warren", w.locations)
        self.assertEqual(w.clock.tick_interval_s, 0.05)

    def test_save_then_load_round_trip(self):
        w1 = load_world(tick_interval_s=0.05)
        w1.clock.tick_number = 42
        w1.locations["loc_goblin_camp_north"].state = LOC_CLEARED
        w1.locations["loc_goblin_camp_north"].cleared_at_tick = 40
        save_world(w1)
        w2 = load_world(tick_interval_s=0.05)
        # Persisted clock wins over the parameter.
        self.assertEqual(w2.clock.tick_number, 42)
        self.assertEqual(
            w2.locations["loc_goblin_camp_north"].state, LOC_CLEARED,
        )


if __name__ == "__main__":
    unittest.main()
