"""Tests for apply_order — the only legal world-mutation entry point."""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.content import default_registry
from dnd.sandbox.castle import Castle, RENOWN_COST_L1_HERO, new_castle
from dnd.sandbox.deployment import (
    ORDER_CREATE_CASTLE,
    ORDER_SPAWN_HERO,
    ORDER_SUBMIT_DEPLOYMENT,
    ORDER_UPLOAD_BEHAVIOR,
    ORDER_UPLOAD_PLAN,
    PHASE_TRAVELING_OUT,
    new_order,
)
from dnd.sandbox.hero_record import HERO_AT_CASTLE, HERO_DEPLOYED, HeroRecord
from dnd.sandbox.orders import _compute_path, apply_order
from dnd.sandbox.world import LOC_ACTIVE, LOC_CLEARED, Location, new_world


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
    return HeroRecord(id=hid, name="Edric", character=char, behavior_ref="b")


def _bootstrap_world():
    w = new_world(width=50, height=50, tick_interval_s=0.05)
    w.locations["loc_x"] = Location(
        id="loc_x", name="X", position=(20, 20), kind="camp",
        description="", resident_template="goblin", base_renown=10,
    )
    return w


# ---------------------------------------------------------------------------
# create_castle
# ---------------------------------------------------------------------------


class TestCreateCastle(unittest.TestCase):
    def test_creates_castle(self):
        w = _bootstrap_world()
        c = new_castle("Hill", "h@y.com", (10, 10))
        order = new_order(None, ORDER_CREATE_CASTLE, {"castle": c})
        apply_order(order, w)
        self.assertIn(c.id, w.castles)
        self.assertEqual(order.accepted_at_tick, 0)

    def test_idempotent_on_repeat(self):
        w = _bootstrap_world()
        c = new_castle("Hill", "h@y.com", (10, 10))
        apply_order(new_order(None, ORDER_CREATE_CASTLE, {"castle": c}), w)
        apply_order(new_order(None, ORDER_CREATE_CASTLE, {"castle": c}), w)
        self.assertEqual(len(w.castles), 1)


# ---------------------------------------------------------------------------
# spawn_hero
# ---------------------------------------------------------------------------


class TestSpawnHero(unittest.TestCase):
    def _world_with_castle(self):
        w = _bootstrap_world()
        c = new_castle("Hill", "h@y.com", (10, 10))
        w.castles[c.id] = c
        return w, c

    def test_spawns_hero_and_charges_renown(self):
        w, c = self._world_with_castle()
        hero = _fighter_record("hero_a")
        before = c.renown
        order = new_order(c.id, ORDER_SPAWN_HERO, {"hero": hero})
        apply_order(order, w)
        self.assertIn("hero_a", c.roster)
        self.assertEqual(c.roster["hero_a"].status, HERO_AT_CASTLE)
        self.assertEqual(c.renown, before - RENOWN_COST_L1_HERO)
        # Ledger entry recorded.
        self.assertTrue(any(e.reason == "spawn_hero" for e in c.renown_ledger))

    def test_dropped_when_renown_insufficient(self):
        w, c = self._world_with_castle()
        c.renown = 5  # not enough
        hero = _fighter_record("hero_a")
        apply_order(new_order(c.id, ORDER_SPAWN_HERO, {"hero": hero}), w)
        self.assertNotIn("hero_a", c.roster)
        self.assertEqual(c.renown, 5)

    def test_idempotent_on_duplicate_id(self):
        w, c = self._world_with_castle()
        hero = _fighter_record("hero_a")
        apply_order(new_order(c.id, ORDER_SPAWN_HERO, {"hero": hero}), w)
        # Second spawn with same id is dropped (no double charge).
        balance_after_first = c.renown
        apply_order(new_order(c.id, ORDER_SPAWN_HERO, {"hero": hero}), w)
        self.assertEqual(c.renown, balance_after_first)

    def test_dropped_when_castle_unknown(self):
        w = _bootstrap_world()
        hero = _fighter_record("hero_a")
        apply_order(new_order("castle_nope", ORDER_SPAWN_HERO, {"hero": hero}), w)
        # Nothing added (no castle to add to).
        self.assertEqual(w.castles, {})


# ---------------------------------------------------------------------------
# submit_deployment
# ---------------------------------------------------------------------------


class TestSubmitDeployment(unittest.TestCase):
    def _setup(self):
        w = _bootstrap_world()
        c = new_castle("Hill", "h@y.com", (10, 10))
        w.castles[c.id] = c
        hero = _fighter_record("hero_a")
        c.add_hero(hero)
        return w, c, hero

    def test_promotes_to_traveling_out(self):
        w, c, hero = self._setup()
        order = new_order(c.id, ORDER_SUBMIT_DEPLOYMENT, {
            "deployment_id": "dep_1", "hero_id": hero.id,
            "location_id": "loc_x",
            "behavior_ref": "b", "plan_ref": None, "seed": 42,
        })
        apply_order(order, w)
        self.assertIn("dep_1", w.deployments)
        d = w.deployments["dep_1"]
        self.assertEqual(d.phase, PHASE_TRAVELING_OUT)
        self.assertEqual(d.hero_id, hero.id)
        self.assertGreater(len(d.path), 0)
        self.assertEqual(d.path[0], (10, 10))   # starts at home
        self.assertEqual(d.path[-1], (20, 20))  # ends at destination
        self.assertEqual(c.roster[hero.id].status, HERO_DEPLOYED)
        # A "depart" event was recorded.
        self.assertTrue(any(e.kind == "depart" for e in d.events))

    def test_dropped_when_hero_already_deployed(self):
        w, c, hero = self._setup()
        hero.status = HERO_DEPLOYED
        apply_order(new_order(c.id, ORDER_SUBMIT_DEPLOYMENT, {
            "deployment_id": "dep_1", "hero_id": hero.id,
            "location_id": "loc_x", "behavior_ref": "b",
        }), w)
        self.assertNotIn("dep_1", w.deployments)

    def test_dropped_when_location_cleared(self):
        w, c, hero = self._setup()
        w.locations["loc_x"].state = LOC_CLEARED
        apply_order(new_order(c.id, ORDER_SUBMIT_DEPLOYMENT, {
            "deployment_id": "dep_1", "hero_id": hero.id,
            "location_id": "loc_x", "behavior_ref": "b",
        }), w)
        self.assertNotIn("dep_1", w.deployments)

    def test_seed_used_when_provided(self):
        w, c, hero = self._setup()
        apply_order(new_order(c.id, ORDER_SUBMIT_DEPLOYMENT, {
            "deployment_id": "dep_1", "hero_id": hero.id,
            "location_id": "loc_x", "behavior_ref": "b",
            "seed": 9999,
        }), w)
        self.assertEqual(w.deployments["dep_1"].seed, 9999)

    def test_seed_derived_when_omitted(self):
        w, c, hero = self._setup()
        apply_order(new_order(c.id, ORDER_SUBMIT_DEPLOYMENT, {
            "deployment_id": "dep_1", "hero_id": hero.id,
            "location_id": "loc_x", "behavior_ref": "b",
        }), w)
        self.assertGreater(w.deployments["dep_1"].seed, 0)


# ---------------------------------------------------------------------------
# upload_behavior / upload_plan
# ---------------------------------------------------------------------------


class TestLibraryUploads(unittest.TestCase):
    def _setup(self):
        w = _bootstrap_world()
        c = new_castle("Hill", "h@y.com", (10, 10))
        w.castles[c.id] = c
        return w, c

    def test_upload_behavior(self):
        w, c = self._setup()
        apply_order(new_order(c.id, ORDER_UPLOAD_BEHAVIOR, {
            "name": "aggressive", "text": "{name: 'a'}",
        }), w)
        self.assertEqual(c.library_behaviors["aggressive"], "{name: 'a'}")

    def test_upload_plan(self):
        w, c = self._setup()
        apply_order(new_order(c.id, ORDER_UPLOAD_PLAN, {
            "name": "fighter12", "text": "plan-text",
        }), w)
        self.assertEqual(c.library_plans["fighter12"], "plan-text")


# ---------------------------------------------------------------------------
# Pathfinding
# ---------------------------------------------------------------------------


class TestComputePath(unittest.TestCase):
    def test_straight_line(self):
        w = new_world(width=20, height=20)
        path = _compute_path((0, 0), (5, 5), w)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (5, 5))
        # Diagonal length = 5 (Chebyshev).
        self.assertEqual(len(path), 6)

    def test_routes_around_impassable(self):
        w = new_world(width=20, height=20)
        # Wall blocking (3,3)..(3,7).
        for y in range(3, 8):
            w.impassable_cells.add((3, y))
        path = _compute_path((0, 5), (10, 5), w)
        self.assertEqual(path[0], (0, 5))
        self.assertEqual(path[-1], (10, 5))
        # No path cell is impassable.
        self.assertFalse(any(p in w.impassable_cells for p in path))

    def test_same_start_and_goal(self):
        w = new_world(width=20, height=20)
        self.assertEqual(_compute_path((5, 5), (5, 5), w), [(5, 5)])


if __name__ == "__main__":
    unittest.main()
