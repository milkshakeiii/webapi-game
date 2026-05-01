"""Tests for Deployment, DeploymentEvent, WorldEncounter, and Order."""

from __future__ import annotations

import os
import shutil
import tempfile
import unittest

from dnd.sandbox.deployment import (
    KNOWN_ORDER_KINDS,
    ORDER_SPAWN_HERO,
    ORDER_SUBMIT_DEPLOYMENT,
    PHASE_COMPLETE,
    PHASE_DEAD,
    PHASE_IN_COMBAT,
    PHASE_PENDING,
    PHASE_TRAVELING_OUT,
    Deployment,
    DeploymentEvent,
    Order,
    WorldEncounter,
    load_all_deployments,
    load_deployment,
    new_order,
    save_deployment,
)


def _basic_deployment(**overrides):
    base = {
        "id": "dep_1", "castle_id": "c", "hero_id": "h",
        "destination_location_id": "loc_x", "behavior_ref": "b",
        "plan_ref": None, "submitted_at_tick": 5, "seed": 42,
    }
    base.update(overrides)
    return Deployment(**base)


class TestDeployment(unittest.TestCase):
    def test_default_phase_is_pending(self):
        d = _basic_deployment()
        self.assertEqual(d.phase, PHASE_PENDING)
        self.assertFalse(d.is_terminal())

    def test_terminal_phases(self):
        d = _basic_deployment(phase=PHASE_COMPLETE)
        self.assertTrue(d.is_terminal())
        d2 = _basic_deployment(phase=PHASE_DEAD)
        self.assertTrue(d2.is_terminal())

    def test_hero_position_from_path(self):
        d = _basic_deployment(path=[(0, 0), (1, 1), (2, 2)], path_index=1)
        self.assertEqual(d.hero_position, (1, 1))

    def test_hero_position_clamps(self):
        d = _basic_deployment(path=[(0, 0), (1, 1)], path_index=99)
        self.assertEqual(d.hero_position, (1, 1))

    def test_hero_position_empty_path_is_none(self):
        d = _basic_deployment()
        self.assertIsNone(d.hero_position)

    def test_append_event(self):
        d = _basic_deployment()
        d.append_event(10, "depart", {"from": [0, 0]})
        self.assertEqual(len(d.events), 1)
        self.assertEqual(d.events[0].tick, 10)
        self.assertEqual(d.events[0].kind, "depart")

    def test_round_trip(self):
        d = _basic_deployment(
            phase=PHASE_TRAVELING_OUT,
            path=[(0, 0), (1, 1)], path_index=1,
            encounter_id="enc_x",
            renown_earned=10, gold_earned=5, items_earned=["coin"],
        )
        d.append_event(6, "depart", {"from": [0, 0]})
        d.append_event(7, "step", {"to": [1, 1]})
        d2 = Deployment.from_dict(d.to_dict())
        self.assertEqual(d2.phase, PHASE_TRAVELING_OUT)
        self.assertEqual(d2.path, [(0, 0), (1, 1)])
        self.assertEqual(d2.path_index, 1)
        self.assertEqual(d2.encounter_id, "enc_x")
        self.assertEqual(d2.renown_earned, 10)
        self.assertEqual(len(d2.events), 2)
        self.assertEqual(d2.events[0].kind, "depart")

    def test_unknown_phase_rejected(self):
        d = _basic_deployment()
        bad = d.to_dict()
        bad["phase"] = "wibbly"
        with self.assertRaises(ValueError):
            Deployment.from_dict(bad)


class TestDeploymentEvent(unittest.TestCase):
    def test_round_trip(self):
        e = DeploymentEvent(tick=12, kind="round", detail={"hp": 7})
        again = DeploymentEvent.from_dict(e.to_dict())
        self.assertEqual(again, e)


class TestWorldEncounter(unittest.TestCase):
    def test_construct(self):
        we = WorldEncounter(
            id="enc_1", location_id="loc_x",
            deployment_ids=["dep_a", "dep_b"],
            started_at_tick=10,
        )
        self.assertEqual(we.deployment_ids, ["dep_a", "dep_b"])
        self.assertIsNone(we.ended_at_tick)


class TestOrder(unittest.TestCase):
    def test_new_order_assigns_id(self):
        o = new_order("c", ORDER_SPAWN_HERO, {"foo": 1})
        self.assertTrue(o.id.startswith("ord_"))
        self.assertEqual(o.kind, ORDER_SPAWN_HERO)
        self.assertEqual(o.payload, {"foo": 1})
        self.assertIsNone(o.accepted_at_tick)

    def test_unknown_kind_rejected(self):
        with self.assertRaises(ValueError):
            Order(
                id="ord_x", castle_id="c", kind="bogus",
                payload={}, received_at=None,  # type: ignore[arg-type]
            )

    def test_known_order_kinds(self):
        # All declared kinds should pass the check.
        for kind in KNOWN_ORDER_KINDS:
            new_order("c", kind, {})


class TestDeploymentPersistence(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="dnd_dep_test_")
        self._prev = os.environ.get("DND_DATA_DIR")
        os.environ["DND_DATA_DIR"] = self._tmp

    def tearDown(self):
        if self._prev is None:
            del os.environ["DND_DATA_DIR"]
        else:
            os.environ["DND_DATA_DIR"] = self._prev
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_round_trip(self):
        d = _basic_deployment(phase=PHASE_IN_COMBAT, path=[(0, 0), (1, 0)])
        d.append_event(6, "depart", {})
        save_deployment(d)
        d2 = load_deployment(d.id)
        self.assertIsNotNone(d2)
        self.assertEqual(d2.phase, PHASE_IN_COMBAT)
        self.assertEqual(d2.path, [(0, 0), (1, 0)])
        self.assertEqual(len(d2.events), 1)

    def test_load_missing_returns_none(self):
        self.assertIsNone(load_deployment("dep_missing"))

    def test_load_all_empty(self):
        self.assertEqual(load_all_deployments(), {})

    def test_load_all_round_trip(self):
        save_deployment(_basic_deployment(id="dep_a"))
        save_deployment(_basic_deployment(id="dep_b"))
        all_ = load_all_deployments()
        self.assertIn("dep_a", all_)
        self.assertIn("dep_b", all_)


if __name__ == "__main__":
    unittest.main()
