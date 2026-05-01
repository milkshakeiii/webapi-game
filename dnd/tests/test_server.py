"""HTTP integration tests for dnd.server.

Spins up a real ``HTTPServer`` on an ephemeral port in a daemon thread and
exercises the routes via ``urllib``.
"""

from __future__ import annotations

import json
import threading
import unittest
from http.server import HTTPServer
from urllib import request as urlreq, error as urlerr

from dnd.engine.content import default_registry
from dnd.server import ServerContext, make_handler


class _ServerHarness:
    """Spin up the dnd HTTP server on a random port for a test class."""

    def __init__(self):
        self.ctx = ServerContext(default_registry())
        self.httpd = HTTPServer(("127.0.0.1", 0), make_handler(self.ctx))
        self.host, self.port = self.httpd.server_address
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    @property
    def base(self) -> str:
        return f"http://{self.host}:{self.port}"

    def shutdown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=2)

    # ── HTTP helpers ──────────────────────────────────────────────────────

    def get(self, path: str) -> tuple[int, dict | list]:
        req = urlreq.Request(self.base + path, method="GET")
        return self._send(req)

    def post(self, path: str, body: dict) -> tuple[int, dict | list]:
        data = json.dumps(body).encode()
        req = urlreq.Request(
            self.base + path,
            method="POST",
            data=data,
            headers={"Content-Type": "application/json",
                     "Content-Length": str(len(data))},
        )
        return self._send(req)

    def _send(self, req) -> tuple[int, dict | list]:
        try:
            resp = urlreq.urlopen(req, timeout=5)
            status = resp.getcode()
            payload = resp.read().decode("utf-8")
        except urlerr.HTTPError as e:
            status = e.code
            payload = e.read().decode("utf-8")
        try:
            return status, json.loads(payload) if payload else {}
        except json.JSONDecodeError:
            return status, {"_raw": payload}


# ---------------------------------------------------------------------------
# Test class with shared server
# ---------------------------------------------------------------------------


class _ServerTestBase(unittest.TestCase):
    harness: _ServerHarness

    @classmethod
    def setUpClass(cls) -> None:
        cls.harness = _ServerHarness()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.harness.shutdown()


# ---------------------------------------------------------------------------
# Content endpoints
# ---------------------------------------------------------------------------


class TestContentRoutes(_ServerTestBase):
    def test_list_races(self):
        status, body = self.harness.get("/v1/content/races")
        self.assertEqual(status, 200)
        ids = {r["id"] for r in body["races"]}
        self.assertIn("human", ids)
        self.assertIn("halfling", ids)
        self.assertEqual(len(body["races"]), 7)

    def test_get_specific_race(self):
        status, body = self.harness.get("/v1/content/races/dwarf")
        self.assertEqual(status, 200)
        self.assertEqual(body["id"], "dwarf")
        self.assertEqual(body["ability_modifiers"]["con"], 2)

    def test_unknown_race_404(self):
        status, body = self.harness.get("/v1/content/races/tiefling")
        self.assertEqual(status, 404)
        self.assertIn("error", body)

    def test_list_classes(self):
        status, body = self.harness.get("/v1/content/classes")
        self.assertEqual(status, 200)
        self.assertEqual(len(body["classes"]), 11)

    def test_get_class_paladin(self):
        status, body = self.harness.get("/v1/content/classes/paladin")
        self.assertEqual(status, 200)
        self.assertEqual(body["alignment_restriction"], "lawful_good")
        self.assertEqual(body["hit_die"], 10)

    def test_get_unknown_route(self):
        status, body = self.harness.get("/v1/wibble/wobble")
        self.assertEqual(status, 404)
        self.assertEqual(body, {"error": "not found"})

    def test_list_feats(self):
        status, body = self.harness.get("/v1/content/feats")
        self.assertEqual(status, 200)
        ids = {f["id"] for f in body["feats"]}
        self.assertIn("power_attack", ids)

    def test_get_feat(self):
        status, body = self.harness.get("/v1/content/feats/power_attack")
        self.assertEqual(status, 200)
        self.assertEqual(body["prerequisites"]["abilities"]["str"], 13)

    def test_list_skills(self):
        status, body = self.harness.get("/v1/content/skills")
        self.assertEqual(status, 200)
        self.assertGreaterEqual(len(body["skills"]), 30)

    def test_list_conditions(self):
        status, body = self.harness.get("/v1/content/conditions")
        self.assertEqual(status, 200)
        ids = {c["id"] for c in body["conditions"]}
        self.assertIn("blinded", ids)
        self.assertIn("flat_footed", ids)


# ---------------------------------------------------------------------------
# Dice endpoint
# ---------------------------------------------------------------------------


class TestDiceRoute(_ServerTestBase):
    def test_simple_roll(self):
        status, body = self.harness.post("/v1/dice", {"expression": "1d20+5", "seed": 42})
        self.assertEqual(status, 200)
        self.assertEqual(body["expression"], "1d20+5")
        self.assertGreaterEqual(body["total"], 6)
        self.assertLessEqual(body["total"], 25)
        self.assertEqual(len(body["terms"]), 2)

    def test_seeded_determinism(self):
        a = self.harness.post("/v1/dice", {"expression": "4d6kh3", "seed": 99})
        b = self.harness.post("/v1/dice", {"expression": "4d6kh3", "seed": 99})
        self.assertEqual(a[1]["total"], b[1]["total"])

    def test_invalid_expression(self):
        status, body = self.harness.post("/v1/dice", {"expression": "garbage"})
        self.assertEqual(status, 400)
        self.assertIn("error", body)

    def test_missing_expression(self):
        status, body = self.harness.post("/v1/dice", {})
        self.assertEqual(status, 400)


# ---------------------------------------------------------------------------
# Character creation endpoint
# ---------------------------------------------------------------------------


class TestCharacterRoute(_ServerTestBase):
    def _valid_fighter_body(self) -> dict:
        return {
            "name": "Sir Edric",
            "race": "human",
            "class": "fighter",
            "alignment": "lawful_good",
            "ability_scores": {
                "method": "point_buy_20",
                "scores": {
                    "str": 16, "dex": 14, "con": 14,
                    "int": 10, "wis": 10, "cha": 10,
                },
            },
            "free_ability_choice": "str",
            "feats": ["power_attack", "weapon_focus"],
            "skill_ranks": {"climb": 1, "swim": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "cleave"},
        }

    def test_create_fighter(self):
        status, body = self.harness.post("/v1/characters", self._valid_fighter_body())
        self.assertEqual(status, 201)
        char = body["character"]
        sheet = body["sheet"]
        self.assertEqual(char["race_id"], "human")
        self.assertEqual(char["class_id"], "fighter")
        self.assertEqual(char["base_ability_scores"]["str"], 16)
        self.assertEqual(sheet["ability_scores"]["str"]["total"], 18)
        self.assertEqual(sheet["hp"]["total"], 12)
        self.assertEqual(sheet["bab"], 1)
        # Stat report exposes contributors.
        self.assertGreaterEqual(len(sheet["saves"]["fort"]["modifiers"]), 1)

    def test_alignment_violation_returns_422(self):
        body = self._valid_fighter_body()
        body["class"] = "paladin"
        body["alignment"] = "neutral_evil"
        status, response = self.harness.post("/v1/characters", body)
        self.assertEqual(status, 422)
        self.assertIn("error", response)

    def test_invalid_request_returns_400(self):
        status, body = self.harness.post("/v1/characters", {"name": "Half"})
        self.assertEqual(status, 400)

    def test_unknown_class_returns_404(self):
        body = self._valid_fighter_body()
        body["class"] = "oracle"
        status, _ = self.harness.post("/v1/characters", body)
        self.assertEqual(status, 404)

    def test_full_sheet_includes_class_features(self):
        status, body = self.harness.post("/v1/characters", self._valid_fighter_body())
        self.assertEqual(status, 201)
        features = [f["id"] for f in body["sheet"]["class_features"]]
        self.assertIn("fighter_bonus_combat_feat_1", features)


# ---------------------------------------------------------------------------
# Equipment endpoints
# ---------------------------------------------------------------------------


class TestEquipmentRoutes(_ServerTestBase):
    def test_list_weapons(self):
        status, body = self.harness.get("/v1/content/weapons")
        self.assertEqual(status, 200)
        ids = {w["id"] for w in body["weapons"]}
        self.assertIn("longsword", ids)
        self.assertIn("greataxe", ids)

    def test_get_weapon(self):
        status, body = self.harness.get("/v1/content/weapons/longsword")
        self.assertEqual(status, 200)
        self.assertEqual(body["damage_dice"], "1d8")

    def test_list_armor(self):
        status, body = self.harness.get("/v1/content/armor")
        self.assertEqual(status, 200)
        ids = {a["id"] for a in body["armor"]}
        self.assertIn("leather", ids)
        self.assertIn("full_plate", ids)

    def test_list_shields(self):
        status, body = self.harness.get("/v1/content/shields")
        self.assertEqual(status, 200)
        ids = {s["id"] for s in body["shields"]}
        self.assertIn("light_steel_shield", ids)


# ---------------------------------------------------------------------------
# Scenario runner endpoint
# ---------------------------------------------------------------------------


class TestLevelUpRoute(_ServerTestBase):
    def test_create_l5_fighter(self):
        body = {
            "name": "Sir Edric the Veteran",
            "race": "human",
            "class": "fighter",
            "alignment": "lawful_good",
            "ability_scores": {
                "method": "point_buy_20",
                "scores": {"str": 16, "dex": 14, "con": 14,
                           "int": 10, "wis": 10, "cha": 10},
            },
            "free_ability_choice": "str",
            "feats": ["power_attack", "weapon_focus"],
            "skill_ranks": {"climb": 1, "swim": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "cleave"},
            "level_plan": {
                "name": "fighter_to_5",
                "target_level": 5,
                "levels": {
                    "2": {"class": "fighter", "feat_class_bonus": "dodge"},
                    "3": {"class": "fighter", "feat_general": "toughness"},
                    "4": {"class": "fighter", "ability_bump": "str",
                          "feat_class_bonus": "combat_reflexes"},
                    "5": {"class": "fighter", "feat_general": "iron_will"},
                },
            },
        }
        status, response = self.harness.post("/v1/characters", body)
        self.assertEqual(status, 201)
        sheet = response["sheet"]
        self.assertEqual(sheet["level"], 5)
        self.assertEqual(sheet["bab"], 5)
        self.assertEqual(sheet["ability_scores"]["str"]["total"], 19)
        # Cumulative feats: power_attack, weapon_focus, cleave, dodge,
        # toughness, combat_reflexes, iron_will = at least 7
        self.assertGreaterEqual(len(sheet["feats"]), 7)


class TestScenarioRoute(_ServerTestBase):
    def _fighter_request(self) -> dict:
        return {
            "name": "Sir Edric",
            "race": "human",
            "class": "fighter",
            "alignment": "lawful_good",
            "ability_scores": {
                "method": "point_buy_20",
                "scores": {"str": 16, "dex": 14, "con": 14,
                           "int": 10, "wis": 10, "cha": 10},
            },
            "free_ability_choice": "str",
            "feats": ["power_attack", "weapon_focus"],
            "skill_ranks": {"climb": 1, "swim": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "cleave"},
        }

    def test_run_fighter_vs_goblin(self):
        body = {
            "name": "demo",
            "width": 20, "height": 10,
            "seed": 7,
            "turn_limit": 30,
            "combatants": [
                {
                    "template_kind": "character",
                    "character_request": self._fighter_request(),
                    "position": [2, 5],
                    "team": "patrons",
                    "behavior": {
                        "name": "bruiser",
                        "rules": [
                            {"when": "enemy.in_range(1) is not None",
                             "do": {"composite": "full_attack",
                                    "args": {"target": "enemy.closest"}}},
                            {"when": "enemy.any",
                             "do": {"composite": "charge",
                                    "args": {"target": "enemy.closest"}}},
                        ],
                    },
                },
                {
                    "template_kind": "monster",
                    "template_id": "goblin",
                    "position": [10, 5],
                    "team": "enemies",
                },
            ],
        }
        status, response = self.harness.post("/v1/scenarios/run", body)
        self.assertEqual(status, 200)
        self.assertEqual(response["winner"], "patrons")
        self.assertGreater(len(response["turns"]), 0)
        # Trace shape: each turn entry has events.
        self.assertIn("events", response["turns"][0])

    def test_invalid_scenario_returns_400(self):
        status, body = self.harness.post("/v1/scenarios/run",
                                          {"name": "bad", "combatants": "not a list"})
        self.assertEqual(status, 400)


if __name__ == "__main__":
    unittest.main()
