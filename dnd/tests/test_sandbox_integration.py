"""Integration test: boot a real HTTP server with a fast tick worker
and drive the full sandbox loop end-to-end via HTTP.

create castle → upload behavior → spawn hero → submit deployment →
poll deployment → see it through to completion.
"""

from __future__ import annotations

import json
import os
import shutil
import socket
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request

from dnd.server import ServerContext, make_handler
from dnd.engine.content import default_registry
from dnd.sandbox.boot import load_world
from dnd.sandbox.worker import TickWorker


def _free_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def _post(url: str, body: dict | None = None) -> tuple[int, dict]:
    data = json.dumps(body or {}).encode()
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}, method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def _get(url: str) -> tuple[int, dict]:
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


_VALID_BEHAVIOR = (
    '{"name": "aggressive", "rules": ['
    '{"do": {"composite": "charge", "args": {"target": "enemy.closest"}}}'
    ']}'
)


class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="dnd_integration_")
        self._prev = os.environ.get("DND_DATA_DIR")
        os.environ["DND_DATA_DIR"] = self._tmp

        from http.server import HTTPServer
        from socketserver import ThreadingMixIn

        class _ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
            daemon_threads = True

        self.registry = default_registry()
        self.world = load_world(tick_interval_s=0.02)
        self.ctx = ServerContext(self.registry, world=self.world)
        self.worker = TickWorker(self.world, self.registry, persist=False)
        self.port = _free_port()
        self.httpd = _ThreadingHTTPServer(
            ("127.0.0.1", self.port), make_handler(self.ctx),
        )
        self._http_thread = threading.Thread(
            target=self.httpd.serve_forever, daemon=True,
        )
        self._http_thread.start()
        self.worker.start()

    def tearDown(self):
        self.worker.stop(timeout=1.0)
        self.httpd.shutdown()
        self.httpd.server_close()
        if self._prev is None:
            os.environ.pop("DND_DATA_DIR", None)
        else:
            os.environ["DND_DATA_DIR"] = self._prev
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _base(self, path):
        return f"http://127.0.0.1:{self.port}{path}"

    def test_full_loop(self):
        # 1. Create the castle.
        status, resp = _post(self._base("/v1/castles"), {
            "name": "Hill", "patron_email": "h@y.com",
            "home_position": [10, 10],
        })
        self.assertEqual(status, 202)
        cid = resp["id"]

        # 2. Wait for the castle to actually exist (one tick).
        cid = self._wait_for(
            lambda: _get(self._base(f"/v1/castles/{cid}"))[0] == 200,
            label=f"castle {cid} appear",
        ) and cid

        # 3. Upload a behavior script.
        status, _ = _post(
            self._base(f"/v1/castles/{cid}/library/behaviors"),
            {"name": "aggressive", "text": _VALID_BEHAVIOR},
        )
        self.assertEqual(status, 202)
        self._wait_for(
            lambda: _get(self._base(
                f"/v1/castles/{cid}/library/behaviors/aggressive"))[0] == 200,
            label="behavior persisted",
        )

        # 4. Spawn a hero. Goblin camp at (37, 45) per default content;
        # closest reachable is loc_goblin_camp_north.
        hero_payload = {
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
            "behavior_ref": "aggressive",
        }
        status, hresp = _post(
            self._base(f"/v1/castles/{cid}/heroes"), hero_payload,
        )
        self.assertEqual(status, 202)
        hid = hresp["id"]
        self._wait_for(
            lambda: _get(self._base(f"/v1/castles/{cid}/heroes/{hid}"))[0] == 200
                    and _get(self._base(
                        f"/v1/castles/{cid}/heroes/{hid}"))[1]["status"]
                       == "at_castle",
            label="hero at_castle",
        )

        # 5. Submit a deployment to the bundled goblin camp.
        status, dresp = _post(
            self._base(f"/v1/castles/{cid}/deployments"),
            {"hero_id": hid,
             "destination_location_id": "loc_goblin_camp_north",
             "seed": 7},
        )
        self.assertEqual(status, 202)
        did = dresp["id"]

        # 6. Poll until terminal (complete or dead) or timeout. The
        # deployment is "pending" (in the queue, not in world.deployments)
        # for the first tick after submission, returning 404 — that's
        # expected; we keep polling.
        terminal_phases = {"complete", "dead"}
        deadline = time.monotonic() + 8.0
        last_phase = "pending"
        while time.monotonic() < deadline:
            status, body = _get(
                self._base(f"/v1/castles/{cid}/deployments/{did}"),
            )
            if status == 404:
                time.sleep(0.05)
                continue
            self.assertEqual(status, 200)
            last_phase = body.get("phase")
            if last_phase in terminal_phases:
                break
            time.sleep(0.05)
        self.assertIn(
            last_phase, terminal_phases,
            f"deployment didn't reach terminal phase; last={last_phase}",
        )

        # 7. Confirm the world endpoint shows the live tick.
        status, world = _get(self._base("/v1/world"))
        self.assertEqual(status, 200)
        self.assertGreater(world["tick"], 0)
        self.assertIn("loc_goblin_camp_north", world["locations"])

        # 8. since_tick filter returns only the tail.
        status, full = _get(
            self._base(f"/v1/castles/{cid}/deployments/{did}"),
        )
        if full["events"]:
            last = full["events"][-1]["tick"]
            status, partial = _get(
                self._base(
                    f"/v1/castles/{cid}/deployments/{did}?since_tick={last}",
                ),
            )
            self.assertEqual(status, 200)
            self.assertEqual(partial["events"], [])

    def _wait_for(self, predicate, *, label, timeout=4.0):
        """Poll until predicate is truthy or timeout."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                if predicate():
                    return True
            except Exception:
                pass
            time.sleep(0.02)
        self.fail(f"timed out waiting for: {label}")


if __name__ == "__main__":
    unittest.main()
