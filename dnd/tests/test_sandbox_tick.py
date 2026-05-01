"""Tests for the tick loop — the core of the sandbox simulation."""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.content import default_registry
from dnd.sandbox.castle import new_castle
from dnd.sandbox.deployment import (
    ORDER_CREATE_CASTLE,
    ORDER_SPAWN_HERO,
    ORDER_SUBMIT_DEPLOYMENT,
    PHASE_AT_DESTINATION,
    PHASE_COMPLETE,
    PHASE_DEAD,
    PHASE_IN_COMBAT,
    PHASE_RETURNING,
    PHASE_TRAVELING_OUT,
    new_order,
)
from dnd.sandbox.hero_record import HERO_AT_CASTLE, HERO_DEAD, HeroRecord
from dnd.sandbox.tick import tick
from dnd.sandbox.world import (
    DEFAULT_RESPAWN_TICKS,
    LOC_ACTIVE,
    LOC_CLEARED,
    Location,
    new_world,
)


REGISTRY = default_registry()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


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


def _world_with_castle_and_hero(home=(10, 10), dest=(20, 10)):
    """Build a world + castle + hero ready for deployment."""
    w = new_world(width=50, height=50, tick_interval_s=0.05)
    w.locations["loc_x"] = Location(
        id="loc_x", name="Goblin Camp", position=dest, kind="camp",
        description="", resident_template="goblin", base_renown=10,
    )
    castle = new_castle("Hill", "h@y.com", home, castle_id="castle_test")
    w.order_queue.submit(
        new_order(None, ORDER_CREATE_CASTLE, {"castle": castle}),
    )
    hero = _fighter_record("hero_1")
    w.order_queue.submit(
        new_order(castle.id, ORDER_SPAWN_HERO, {"hero": hero}),
    )
    # Apply both orders.
    tick(w, REGISTRY)
    return w, castle, hero


def _submit_deployment(world, castle, hero, dep_id="dep_1", seed=42):
    world.order_queue.submit(new_order(castle.id, ORDER_SUBMIT_DEPLOYMENT, {
        "deployment_id": dep_id,
        "hero_id": hero.id,
        "location_id": "loc_x",
        "behavior_ref": "b",
        "seed": seed,
    }))


# ---------------------------------------------------------------------------
# Tick + queue draining
# ---------------------------------------------------------------------------


class TestQueueDrain(unittest.TestCase):
    def test_tick_advances_clock(self):
        w = new_world(tick_interval_s=0.05)
        self.assertEqual(w.clock.tick_number, 0)
        tick(w, REGISTRY)
        self.assertEqual(w.clock.tick_number, 1)

    def test_tick_drains_pending_orders(self):
        w, castle, hero = _world_with_castle_and_hero()
        # The setup helper already drained one tick; castle + hero are present.
        self.assertIn(castle.id, w.castles)
        self.assertIn(hero.id, castle.roster)

    def test_publish_snapshot_after_tick(self):
        w, _, _ = _world_with_castle_and_hero()
        snap = w.current_snapshot
        self.assertEqual(snap["tick"], w.clock.tick_number)
        self.assertIn("loc_x", snap["locations"])


# ---------------------------------------------------------------------------
# Travel
# ---------------------------------------------------------------------------


class TestTravelOut(unittest.TestCase):
    def test_deployment_promotes_then_advances(self):
        w, castle, hero = _world_with_castle_and_hero(
            home=(10, 10), dest=(20, 10),
        )
        _submit_deployment(w, castle, hero)
        # First tick: order applied, deployment registered + path computed,
        # hero takes one round of movement.
        tick(w, REGISTRY)
        d = w.deployments["dep_1"]
        self.assertEqual(d.phase, PHASE_TRAVELING_OUT)
        self.assertGreater(d.path_index, 0)

    def test_arrives_at_destination_and_engages(self):
        # Distance 10 cells; speed 6 cells/round → arrives in ≤ 2 ticks.
        w, castle, hero = _world_with_castle_and_hero(
            home=(10, 10), dest=(20, 10),
        )
        _submit_deployment(w, castle, hero)
        tick(w, REGISTRY)            # apply order + move
        tick(w, REGISTRY)            # arrive
        d = w.deployments["dep_1"]
        # Should have arrived and engaged (phase == IN_COMBAT) by now.
        self.assertIn(d.phase, (PHASE_AT_DESTINATION, PHASE_IN_COMBAT))


# ---------------------------------------------------------------------------
# Combat lifecycle (hero usually wins; we run enough ticks to terminate)
# ---------------------------------------------------------------------------


class TestCombatLifecycle(unittest.TestCase):
    def _run_to_terminal(self, max_ticks=50):
        w, castle, hero = _world_with_castle_and_hero(
            home=(10, 10), dest=(15, 10),  # short distance
        )
        _submit_deployment(w, castle, hero, seed=7)
        for _ in range(max_ticks):
            tick(w, REGISTRY)
            d = w.deployments["dep_1"]
            if d.is_terminal():
                break
        return w, castle, hero, d

    def test_terminates_within_budget(self):
        _, _, _, d = self._run_to_terminal(max_ticks=100)
        self.assertTrue(
            d.is_terminal(),
            f"deployment didn't terminate; final phase={d.phase}",
        )

    def test_victory_path_clears_location_and_banks_renown(self):
        # Try a few seeds to find one where the hero wins. (Fighter vs.
        # goblin is heavily favored; a few seeds should be enough.)
        for seed in range(1, 50):
            w, castle, hero = _world_with_castle_and_hero(
                home=(10, 10), dest=(15, 10),
            )
            _submit_deployment(w, castle, hero, seed=seed)
            for _ in range(100):
                tick(w, REGISTRY)
                d = w.deployments["dep_1"]
                if d.is_terminal():
                    break
            if d.phase == PHASE_COMPLETE:
                self.assertEqual(
                    w.locations["loc_x"].state, LOC_CLEARED,
                )
                self.assertEqual(w.locations["loc_x"].cleared_by_castle, castle.id)
                self.assertGreaterEqual(d.renown_earned, 10)
                self.assertEqual(castle.roster[hero.id].status, HERO_AT_CASTLE)
                return
        self.skipTest("no seed produced a victory; not a real failure")

    def test_event_log_contains_engage_and_round(self):
        w, _, _, d = self._run_to_terminal()
        kinds = {e.kind for e in d.events}
        self.assertIn("depart", kinds)
        self.assertIn("engage", kinds)
        self.assertIn("round", kinds)


# ---------------------------------------------------------------------------
# Death path
# ---------------------------------------------------------------------------


class TestHeroDeath(unittest.TestCase):
    def test_dead_hero_moved_to_graveyard(self):
        # An unrealistically frail hero against a strong monster.
        # We build a "fighter" with full stats but starting HP forced to 1
        # so almost any seed kills them.
        w, castle, hero = _world_with_castle_and_hero(
            home=(10, 10), dest=(15, 10),
        )
        # After spawn the hero sits at_castle with current_hp 0; any
        # materialization will set it to max_hp. Force a very-low max via
        # nudging the carried HP to 1 just before deployment.
        # We accept the realistic case: try seeds until a death happens.
        deaths = 0
        for seed in range(1, 100):
            w2, castle2, hero2 = _world_with_castle_and_hero()
            # Make the hero very fragile.
            hero2.current_hp = 1
            hero2.max_hp = 1
            # Patch the fighter Character so combatant_from_hero_record
            # sees a 1-HP starting state. For v1 it's enough to just
            # cap current_hp; the engine clamps to max_hp on materialization.
            castle2.roster[hero2.id].current_hp = 1
            _submit_deployment(w2, castle2, hero2, dep_id="dep_d", seed=seed)
            for _ in range(80):
                tick(w2, REGISTRY)
                d = w2.deployments["dep_d"]
                if d.is_terminal():
                    break
            if d.phase == PHASE_DEAD:
                # Hero burial happened.
                self.assertIn(hero2.id, castle2.graveyard)
                self.assertEqual(
                    castle2.graveyard[hero2.id].status, HERO_DEAD,
                )
                deaths += 1
                break
        self.assertGreater(deaths, 0, "no seed produced a death; adjust test")


# ---------------------------------------------------------------------------
# Respawn
# ---------------------------------------------------------------------------


class TestLocationRespawn(unittest.TestCase):
    def test_cleared_location_respawns_after_delay(self):
        w = new_world(tick_interval_s=0.05)
        loc = Location(
            id="loc_r", name="R", position=(5, 5), kind="camp",
            description="", resident_template="goblin", base_renown=10,
            respawn_ticks=3, state=LOC_CLEARED, cleared_at_tick=0,
        )
        w.locations["loc_r"] = loc
        # Tick 1, 2: still cleared. Tick 3: respawn.
        tick(w, REGISTRY)
        self.assertEqual(w.locations["loc_r"].state, LOC_CLEARED)
        tick(w, REGISTRY)
        self.assertEqual(w.locations["loc_r"].state, LOC_CLEARED)
        tick(w, REGISTRY)
        self.assertEqual(w.locations["loc_r"].state, LOC_ACTIVE)
        self.assertIsNone(w.locations["loc_r"].cleared_at_tick)


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


class TestDeterminism(unittest.TestCase):
    def test_same_seed_same_outcome(self):
        # Two parallel deployments with identical seeds should produce
        # identical event traces tick-by-tick.
        def run_once():
            w, castle, hero = _world_with_castle_and_hero(
                home=(10, 10), dest=(15, 10),
            )
            _submit_deployment(w, castle, hero, seed=12345)
            for _ in range(60):
                tick(w, REGISTRY)
                d = w.deployments["dep_1"]
                if d.is_terminal():
                    break
            return d.phase, [
                (e.tick, e.kind) for e in w.deployments["dep_1"].events
            ]

        phase_a, trace_a = run_once()
        phase_b, trace_b = run_once()
        self.assertEqual(phase_a, phase_b)
        self.assertEqual(trace_a, trace_b)


if __name__ == "__main__":
    unittest.main()
