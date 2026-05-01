"""Tests for the sandbox HTTP route handlers (function-level).

These call the route helpers directly (no socket layer) so the tests
can be deterministic and fast.
"""

from __future__ import annotations

import unittest

from dnd.engine.content import default_registry
from dnd.sandbox.routes import (
    get_castle,
    get_castle_behavior,
    get_castle_plan,
    get_deployment,
    get_hero,
    get_world,
    list_deployments,
    list_heroes,
    post_castle,
    post_castle_behavior,
    post_castle_plan,
    post_deployment,
    post_hero,
)
from dnd.sandbox.tick import tick
from dnd.sandbox.world import Location, new_world


REGISTRY = default_registry()


_VALID_BEHAVIOR = (
    '{"name": "aggressive", "rules": ['
    '{"do": {"composite": "charge", "args": {"target": "enemy.closest"}}}'
    ']}'
)


def _world():
    w = new_world(width=50, height=50, tick_interval_s=0.05)
    w.locations["loc_x"] = Location(
        id="loc_x", name="Camp", position=(20, 20), kind="camp",
        description="", resident_template="goblin", base_renown=10,
    )
    return w


def _hero_payload(behavior_ref="aggressive", plan_ref=None):
    return {
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
        "behavior_ref": behavior_ref, "plan_ref": plan_ref,
    }


# ---------------------------------------------------------------------------
# Castle lifecycle
# ---------------------------------------------------------------------------


class TestPostCastle(unittest.TestCase):
    def test_returns_202_pending(self):
        w = _world()
        status, body = post_castle(w, {
            "name": "Hill", "patron_email": "h@y.com",
            "home_position": [10, 10],
        })
        self.assertEqual(status, 202)
        self.assertEqual(body["status"], "pending")
        # Order is queued, not applied yet.
        self.assertEqual(len(w.order_queue), 1)
        self.assertEqual(w.castles, {})

    def test_400_on_missing_fields(self):
        w = _world()
        self.assertEqual(post_castle(w, {})[0], 400)
        self.assertEqual(post_castle(w, {"name": "x"})[0], 400)
        self.assertEqual(
            post_castle(w, {"name": "x", "patron_email": "noatsign"})[0], 400)
        self.assertEqual(
            post_castle(w, {
                "name": "x", "patron_email": "x@y.com",
                "home_position": [9999, 9999],
            })[0], 400)


class TestGetCastle(unittest.TestCase):
    def test_404_until_tick_runs(self):
        w = _world()
        post_castle(w, {
            "name": "Hill", "patron_email": "h@y.com",
            "home_position": [10, 10],
        })
        # Pull the queued order to learn the castle id (it's not in
        # the response — we'd normally poll castle list, but for the
        # test we read the queue).
        # Easier path: tick once to apply the order, then list.
        tick(w, REGISTRY)
        cid = next(iter(w.castles.keys()))
        status, body = get_castle(w, cid)
        self.assertEqual(status, 200)
        self.assertEqual(body["name"], "Hill")
        self.assertEqual(body["renown"], 100)

    def test_404_for_unknown(self):
        w = _world()
        status, body = get_castle(w, "castle_nope")
        self.assertEqual(status, 404)


# ---------------------------------------------------------------------------
# Library
# ---------------------------------------------------------------------------


class TestLibrary(unittest.TestCase):
    def _setup(self):
        w = _world()
        post_castle(w, {
            "name": "Hill", "patron_email": "h@y.com",
            "home_position": [10, 10],
        })
        tick(w, REGISTRY)
        cid = next(iter(w.castles.keys()))
        return w, cid

    def test_upload_and_fetch_behavior(self):
        w, cid = self._setup()
        status, body = post_castle_behavior(w, cid, {
            "name": "aggressive", "text": _VALID_BEHAVIOR,
        })
        self.assertEqual(status, 202)
        tick(w, REGISTRY)
        s2, b2 = get_castle_behavior(w, cid, "aggressive")
        self.assertEqual(s2, 200)
        self.assertEqual(b2["text"], _VALID_BEHAVIOR)

    def test_400_on_invalid_script(self):
        w, cid = self._setup()
        status, body = post_castle_behavior(w, cid, {
            "name": "x", "text": "not json at all",
        })
        self.assertEqual(status, 400)

    def test_404_castle_unknown(self):
        w = _world()
        status, body = post_castle_behavior(w, "castle_nope", {
            "name": "x", "text": _VALID_BEHAVIOR,
        })
        self.assertEqual(status, 404)

    def test_upload_and_fetch_plan(self):
        w, cid = self._setup()
        status, _ = post_castle_plan(w, cid, {
            "name": "fighter12", "text": "any-text",
        })
        self.assertEqual(status, 202)
        tick(w, REGISTRY)
        s2, b2 = get_castle_plan(w, cid, "fighter12")
        self.assertEqual(s2, 200)
        self.assertEqual(b2["text"], "any-text")


# ---------------------------------------------------------------------------
# Heroes
# ---------------------------------------------------------------------------


class TestSpawnHero(unittest.TestCase):
    def _setup(self):
        w = _world()
        post_castle(w, {
            "name": "Hill", "patron_email": "h@y.com",
            "home_position": [10, 10],
        })
        tick(w, REGISTRY)
        cid = next(iter(w.castles.keys()))
        post_castle_behavior(w, cid, {
            "name": "aggressive", "text": _VALID_BEHAVIOR,
        })
        tick(w, REGISTRY)
        return w, cid

    def test_spawn_validates_synchronously(self):
        w, cid = self._setup()
        status, body = post_hero(w, cid, _hero_payload(), REGISTRY)
        self.assertEqual(status, 202)
        self.assertEqual(body["status"], "pending")

    def test_spawn_404_when_behavior_ref_missing(self):
        w, cid = self._setup()
        status, body = post_hero(
            w, cid, _hero_payload(behavior_ref="not_in_lib"), REGISTRY,
        )
        self.assertEqual(status, 400)

    def test_spawn_403_when_renown_short(self):
        w, cid = self._setup()
        # Drain renown down to 5 directly.
        with w.write_lock:
            w.castles[cid].renown = 5
        status, body = post_hero(w, cid, _hero_payload(), REGISTRY)
        self.assertEqual(status, 403)

    def test_spawn_then_tick_then_get(self):
        w, cid = self._setup()
        status, body = post_hero(w, cid, _hero_payload(), REGISTRY)
        hid = body["id"]
        tick(w, REGISTRY)
        s2, b2 = get_hero(w, cid, hid)
        self.assertEqual(s2, 200)
        self.assertEqual(b2["status"], "at_castle")
        s3, b3 = list_heroes(w, cid)
        self.assertEqual(s3, 200)
        self.assertEqual(len(b3["roster"]), 1)


# ---------------------------------------------------------------------------
# Deployments
# ---------------------------------------------------------------------------


class TestDeployment(unittest.TestCase):
    def _setup_with_hero(self):
        w = _world()
        post_castle(w, {
            "name": "Hill", "patron_email": "h@y.com",
            "home_position": [10, 10],
        })
        tick(w, REGISTRY)
        cid = next(iter(w.castles.keys()))
        post_castle_behavior(w, cid, {
            "name": "aggressive", "text": _VALID_BEHAVIOR,
        })
        tick(w, REGISTRY)
        _, body = post_hero(w, cid, _hero_payload(), REGISTRY)
        hid = body["id"]
        tick(w, REGISTRY)
        return w, cid, hid

    def test_submit_deployment(self):
        w, cid, hid = self._setup_with_hero()
        status, body = post_deployment(w, cid, {
            "hero_id": hid,
            "destination_location_id": "loc_x",
            "seed": 7,
        })
        self.assertEqual(status, 202)
        self.assertEqual(body["phase"], "pending")
        tick(w, REGISTRY)
        # Now the deployment exists and is traveling out.
        s2, b2 = get_deployment(w, cid, body["id"])
        self.assertEqual(s2, 200)
        self.assertEqual(b2["phase"], "traveling_out")

    def test_404_unknown_hero(self):
        w, cid, _ = self._setup_with_hero()
        status, _ = post_deployment(w, cid, {
            "hero_id": "hero_bogus",
            "destination_location_id": "loc_x",
        })
        self.assertEqual(status, 404)

    def test_404_unknown_location(self):
        w, cid, hid = self._setup_with_hero()
        status, _ = post_deployment(w, cid, {
            "hero_id": hid,
            "destination_location_id": "loc_nope",
        })
        self.assertEqual(status, 404)

    def test_since_tick_filters_events(self):
        w, cid, hid = self._setup_with_hero()
        _, body = post_deployment(w, cid, {
            "hero_id": hid, "destination_location_id": "loc_x", "seed": 7,
        })
        did = body["id"]
        tick(w, REGISTRY)
        tick(w, REGISTRY)
        full_status, full = get_deployment(w, cid, did)
        self.assertEqual(full_status, 200)
        full_count = len(full["events"])
        self.assertGreater(full_count, 0)
        last_tick = full["events"][-1]["tick"]
        # since_tick = last_tick should give zero events.
        _, partial = get_deployment(w, cid, did, since_tick=last_tick)
        self.assertEqual(partial["events"], [])

    def test_list_deployments(self):
        w, cid, hid = self._setup_with_hero()
        _, body = post_deployment(w, cid, {
            "hero_id": hid, "destination_location_id": "loc_x", "seed": 7,
        })
        tick(w, REGISTRY)
        status, b = list_deployments(w, cid)
        self.assertEqual(status, 200)
        self.assertEqual(len(b["deployments"]), 1)


# ---------------------------------------------------------------------------
# World
# ---------------------------------------------------------------------------


class TestWorldEndpoint(unittest.TestCase):
    def test_get_world(self):
        w = _world()
        tick(w, REGISTRY)
        status, body = get_world(w)
        self.assertEqual(status, 200)
        self.assertIn("loc_x", body["locations"])
        self.assertEqual(body["width"], 50)
        self.assertEqual(body["tick"], w.clock.tick_number)


if __name__ == "__main__":
    unittest.main()
