"""HTTP server for the D&D Sandbox API.

Phase 1 endpoints:

- GET  /v1/content/races
- GET  /v1/content/races/{id}
- GET  /v1/content/classes
- GET  /v1/content/classes/{id}
- GET  /v1/content/feats
- GET  /v1/content/feats/{id}
- GET  /v1/content/skills
- GET  /v1/content/skills/{id}
- GET  /v1/content/conditions
- GET  /v1/content/conditions/{id}
- POST /v1/dice
- POST /v1/characters

No persistent state: characters are returned to the caller, not stored.
Castle persistence and deployments come in later phases.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, is_dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Callable

from .engine.characters import (
    CharacterCreationError,
    CharacterRequest,
    compute_sheet,
    create_character,
)
from .engine.content import ContentNotFoundError, ContentRegistry, default_registry
from .engine.dice import DiceError, Roller
from .engine.scenario import ScenarioSpec, run_scenario
from .sandbox import routes as sb_routes
from .sandbox.boot import load_world
from .sandbox.world import World
from .sandbox.worker import TickWorker


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------


Route = tuple[str, "re.Pattern[str]", Callable]
_routes: list[Route] = []


def route(method: str, pattern: str):
    """Register a route handler for ``method`` and regex ``pattern``."""
    compiled = re.compile(pattern)

    def decorator(fn: Callable) -> Callable:
        _routes.append((method, compiled, fn))
        return fn

    return decorator


# ---------------------------------------------------------------------------
# Request / response helpers
# ---------------------------------------------------------------------------


def _read_json(handler: BaseHTTPRequestHandler) -> dict | None:
    length = int(handler.headers.get("Content-Length", 0))
    if length == 0:
        return {}
    raw = handler.rfile.read(length)
    try:
        body = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    if not isinstance(body, dict):
        return None
    return body


def _respond(handler: BaseHTTPRequestHandler, status: int, body: Any) -> None:
    payload = json.dumps(body, indent=2, default=_json_default).encode()
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(payload)))
    handler.end_headers()
    handler.wfile.write(payload)


def _json_default(obj):
    if is_dataclass(obj):
        return asdict(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def _error(handler: BaseHTTPRequestHandler, status: int, message: str) -> None:
    _respond(handler, status, {"error": message})


def _content_to_dict(obj) -> dict:
    """Serialize a Race/Class/Skill/Feat/Condition dataclass to a JSON dict."""
    d = asdict(obj)
    # Drop the duplicate ``raw`` blob — the typed fields already cover it.
    d.pop("raw", None)
    return d


# ---------------------------------------------------------------------------
# Content endpoints
# ---------------------------------------------------------------------------


@route("GET", r"/v1/content/races$")
def list_races(handler, match, ctx):
    _respond(handler, 200, {"races": [_content_to_dict(r) for r in ctx.registry.all_races()]})


@route("GET", r"/v1/content/races/(?P<rid>[A-Za-z0-9_\-]+)$")
def get_race(handler, match, ctx):
    try:
        race = ctx.registry.get_race(match.group("rid"))
    except ContentNotFoundError as e:
        return _error(handler, 404, str(e))
    _respond(handler, 200, _content_to_dict(race))


@route("GET", r"/v1/content/classes$")
def list_classes(handler, match, ctx):
    _respond(handler, 200, {"classes": [_content_to_dict(c) for c in ctx.registry.all_classes()]})


@route("GET", r"/v1/content/classes/(?P<cid>[A-Za-z0-9_\-]+)$")
def get_class(handler, match, ctx):
    try:
        cls = ctx.registry.get_class(match.group("cid"))
    except ContentNotFoundError as e:
        return _error(handler, 404, str(e))
    _respond(handler, 200, _content_to_dict(cls))


@route("GET", r"/v1/content/feats$")
def list_feats(handler, match, ctx):
    _respond(handler, 200, {"feats": [_content_to_dict(f) for f in ctx.registry.all_feats()]})


@route("GET", r"/v1/content/feats/(?P<fid>[A-Za-z0-9_\-]+)$")
def get_feat(handler, match, ctx):
    try:
        feat = ctx.registry.get_feat(match.group("fid"))
    except ContentNotFoundError as e:
        return _error(handler, 404, str(e))
    _respond(handler, 200, _content_to_dict(feat))


@route("GET", r"/v1/content/skills$")
def list_skills(handler, match, ctx):
    _respond(handler, 200, {"skills": [_content_to_dict(s) for s in ctx.registry.all_skills()]})


@route("GET", r"/v1/content/skills/(?P<sid>[A-Za-z0-9_\-]+)$")
def get_skill(handler, match, ctx):
    try:
        skill = ctx.registry.get_skill(match.group("sid"))
    except ContentNotFoundError as e:
        return _error(handler, 404, str(e))
    _respond(handler, 200, _content_to_dict(skill))


@route("GET", r"/v1/content/conditions$")
def list_conditions(handler, match, ctx):
    _respond(handler, 200, {"conditions": [_content_to_dict(c) for c in ctx.registry.all_conditions()]})


@route("GET", r"/v1/content/conditions/(?P<cid>[A-Za-z0-9_\-]+)$")
def get_condition(handler, match, ctx):
    try:
        cond = ctx.registry.get_condition(match.group("cid"))
    except ContentNotFoundError as e:
        return _error(handler, 404, str(e))
    _respond(handler, 200, _content_to_dict(cond))


@route("GET", r"/v1/content/monsters$")
def list_monsters(handler, match, ctx):
    _respond(handler, 200, {"monsters": [_content_to_dict(m) for m in ctx.registry.all_monsters()]})


@route("GET", r"/v1/content/monsters/(?P<mid>[A-Za-z0-9_\-]+)$")
def get_monster(handler, match, ctx):
    try:
        monster = ctx.registry.get_monster(match.group("mid"))
    except ContentNotFoundError as e:
        return _error(handler, 404, str(e))
    _respond(handler, 200, _content_to_dict(monster))


@route("GET", r"/v1/content/weapons$")
def list_weapons(handler, match, ctx):
    _respond(handler, 200, {"weapons": [_content_to_dict(w) for w in ctx.registry.all_weapons()]})


@route("GET", r"/v1/content/weapons/(?P<wid>[A-Za-z0-9_\-]+)$")
def get_weapon(handler, match, ctx):
    try:
        w = ctx.registry.get_weapon(match.group("wid"))
    except ContentNotFoundError as e:
        return _error(handler, 404, str(e))
    _respond(handler, 200, _content_to_dict(w))


@route("GET", r"/v1/content/armor$")
def list_armor(handler, match, ctx):
    _respond(handler, 200, {"armor": [_content_to_dict(a) for a in ctx.registry.all_armor()]})


@route("GET", r"/v1/content/armor/(?P<aid>[A-Za-z0-9_\-]+)$")
def get_armor_route(handler, match, ctx):
    try:
        a = ctx.registry.get_armor(match.group("aid"))
    except ContentNotFoundError as e:
        return _error(handler, 404, str(e))
    _respond(handler, 200, _content_to_dict(a))


@route("GET", r"/v1/content/shields$")
def list_shields(handler, match, ctx):
    _respond(handler, 200, {"shields": [_content_to_dict(s) for s in ctx.registry.all_shields()]})


@route("GET", r"/v1/content/shields/(?P<sid>[A-Za-z0-9_\-]+)$")
def get_shield_route(handler, match, ctx):
    try:
        s = ctx.registry.get_shield(match.group("sid"))
    except ContentNotFoundError as e:
        return _error(handler, 404, str(e))
    _respond(handler, 200, _content_to_dict(s))


@route("GET", r"/v1/content/spells$")
def list_spells(handler, match, ctx):
    _respond(handler, 200, {"spells": [_content_to_dict(s) for s in ctx.registry.all_spells()]})


@route("GET", r"/v1/content/spells/(?P<sid>[A-Za-z0-9_\-]+)$")
def get_spell_route(handler, match, ctx):
    try:
        s = ctx.registry.get_spell(match.group("sid"))
    except ContentNotFoundError as e:
        return _error(handler, 404, str(e))
    _respond(handler, 200, _content_to_dict(s))


# ---------------------------------------------------------------------------
# Scenario runner
# ---------------------------------------------------------------------------


@route("POST", r"/v1/scenarios/run$")
def post_scenario_run(handler, match, ctx):
    body = _read_json(handler)
    if body is None:
        return _error(handler, 400, "malformed JSON body")
    try:
        spec = ScenarioSpec.from_dict(body)
    except Exception as e:
        return _error(handler, 400, f"invalid scenario: {e}")
    try:
        result = run_scenario(spec, ctx.registry)
    except ContentNotFoundError as e:
        return _error(handler, 404, str(e))
    except (ValueError, KeyError, TypeError) as e:
        return _error(handler, 422, str(e))
    _respond(handler, 200, result.to_dict())


# ---------------------------------------------------------------------------
# Dice
# ---------------------------------------------------------------------------


@route("POST", r"/v1/dice$")
def post_dice(handler, match, ctx):
    body = _read_json(handler)
    if body is None:
        return _error(handler, 400, "malformed JSON body")
    expr = body.get("expression")
    if not isinstance(expr, str) or not expr.strip():
        return _error(handler, 400, "missing or empty 'expression' (string)")
    seed = body.get("seed")
    if seed is not None and not isinstance(seed, int):
        return _error(handler, 400, "'seed' must be an integer if provided")
    try:
        result = Roller(seed=seed).roll(expr)
    except DiceError as e:
        return _error(handler, 400, f"dice error: {e}")
    _respond(handler, 200, result.to_dict())


# ---------------------------------------------------------------------------
# Character creation
# ---------------------------------------------------------------------------


@route("POST", r"/v1/characters$")
def post_character(handler, match, ctx):
    body = _read_json(handler)
    if body is None:
        return _error(handler, 400, "malformed JSON body")
    try:
        request = CharacterRequest.from_dict(body)
    except CharacterCreationError as e:
        return _error(handler, 400, str(e))
    except (KeyError, TypeError, ValueError) as e:
        return _error(handler, 400, f"bad request: {e}")
    try:
        character = create_character(request, ctx.registry, roller=Roller(seed=body.get("seed")))
    except CharacterCreationError as e:
        return _error(handler, 422, str(e))
    except ContentNotFoundError as e:
        return _error(handler, 404, str(e))
    sheet = compute_sheet(character, ctx.registry)
    _respond(handler, 201, {
        "character": character.to_dict(),
        "sheet": sheet.to_dict(),
    })


# ---------------------------------------------------------------------------
# Sandbox routes (castles, heroes, deployments, world)
# ---------------------------------------------------------------------------


def _query_int(handler: BaseHTTPRequestHandler, key: str) -> int | None:
    """Pull a single int query-string param from ``handler.path``."""
    if "?" not in handler.path:
        return None
    qs = handler.path.split("?", 1)[1]
    for pair in qs.split("&"):
        if "=" not in pair:
            continue
        k, v = pair.split("=", 1)
        if k == key:
            try:
                return int(v)
            except ValueError:
                return None
    return None


@route("POST", r"/v1/castles$")
def post_castle_route(handler, match, ctx):
    body = _read_json(handler)
    if body is None:
        return _error(handler, 400, "malformed JSON body")
    status, resp = sb_routes.post_castle(ctx.world, body)
    _respond(handler, status, resp)


@route("GET", r"/v1/castles/(?P<cid>[A-Za-z0-9_\-]+)$")
def get_castle_route(handler, match, ctx):
    status, resp = sb_routes.get_castle(ctx.world, match.group("cid"))
    _respond(handler, status, resp)


@route("POST", r"/v1/castles/(?P<cid>[A-Za-z0-9_\-]+)/library/behaviors$")
def post_behavior_route(handler, match, ctx):
    body = _read_json(handler)
    if body is None:
        return _error(handler, 400, "malformed JSON body")
    status, resp = sb_routes.post_castle_behavior(
        ctx.world, match.group("cid"), body,
    )
    _respond(handler, status, resp)


@route("GET", r"/v1/castles/(?P<cid>[A-Za-z0-9_\-]+)/library/behaviors/(?P<name>[A-Za-z0-9_\-/]+)$")
def get_behavior_route(handler, match, ctx):
    status, resp = sb_routes.get_castle_behavior(
        ctx.world, match.group("cid"), match.group("name"),
    )
    _respond(handler, status, resp)


@route("POST", r"/v1/castles/(?P<cid>[A-Za-z0-9_\-]+)/library/plans$")
def post_plan_route(handler, match, ctx):
    body = _read_json(handler)
    if body is None:
        return _error(handler, 400, "malformed JSON body")
    status, resp = sb_routes.post_castle_plan(
        ctx.world, match.group("cid"), body,
    )
    _respond(handler, status, resp)


@route("GET", r"/v1/castles/(?P<cid>[A-Za-z0-9_\-]+)/library/plans/(?P<name>[A-Za-z0-9_\-/]+)$")
def get_plan_route(handler, match, ctx):
    status, resp = sb_routes.get_castle_plan(
        ctx.world, match.group("cid"), match.group("name"),
    )
    _respond(handler, status, resp)


@route("POST", r"/v1/castles/(?P<cid>[A-Za-z0-9_\-]+)/heroes$")
def post_hero_route(handler, match, ctx):
    body = _read_json(handler)
    if body is None:
        return _error(handler, 400, "malformed JSON body")
    status, resp = sb_routes.post_hero(
        ctx.world, match.group("cid"), body, ctx.registry,
    )
    _respond(handler, status, resp)


@route("GET", r"/v1/castles/(?P<cid>[A-Za-z0-9_\-]+)/heroes$")
def list_heroes_route(handler, match, ctx):
    status, resp = sb_routes.list_heroes(ctx.world, match.group("cid"))
    _respond(handler, status, resp)


@route("GET", r"/v1/castles/(?P<cid>[A-Za-z0-9_\-]+)/heroes/(?P<hid>[A-Za-z0-9_\-]+)$")
def get_hero_route(handler, match, ctx):
    status, resp = sb_routes.get_hero(
        ctx.world, match.group("cid"), match.group("hid"),
    )
    _respond(handler, status, resp)


@route("POST", r"/v1/castles/(?P<cid>[A-Za-z0-9_\-]+)/deployments$")
def post_deployment_route(handler, match, ctx):
    body = _read_json(handler)
    if body is None:
        return _error(handler, 400, "malformed JSON body")
    status, resp = sb_routes.post_deployment(
        ctx.world, match.group("cid"), body,
    )
    _respond(handler, status, resp)


@route("GET", r"/v1/castles/(?P<cid>[A-Za-z0-9_\-]+)/deployments$")
def list_deployments_route(handler, match, ctx):
    status, resp = sb_routes.list_deployments(ctx.world, match.group("cid"))
    _respond(handler, status, resp)


@route("GET", r"/v1/castles/(?P<cid>[A-Za-z0-9_\-]+)/deployments/(?P<did>[A-Za-z0-9_\-]+)(?:\?.*)?$")
def get_deployment_route(handler, match, ctx):
    since = _query_int(handler, "since_tick")
    status, resp = sb_routes.get_deployment(
        ctx.world, match.group("cid"), match.group("did"), since_tick=since,
    )
    _respond(handler, status, resp)


@route("GET", r"/v1/world(?:\?.*)?$")
def get_world_route(handler, match, ctx):
    status, resp = sb_routes.get_world(ctx.world)
    _respond(handler, status, resp)


# ---------------------------------------------------------------------------
# Server context & handler factory
# ---------------------------------------------------------------------------


class ServerContext:
    """Bag of state passed to every route handler."""

    def __init__(
        self, registry: ContentRegistry, world: World | None = None,
    ):
        self.registry = registry
        self.world = world


def make_handler(ctx: ServerContext):
    class Handler(BaseHTTPRequestHandler):
        def _dispatch(self, method: str) -> None:
            for route_method, pattern, fn in _routes:
                if route_method != method:
                    continue
                m = pattern.match(self.path)
                if m:
                    try:
                        fn(self, m, ctx)
                    except Exception as e:  # last-ditch
                        _error(self, 500, f"internal error: {e}")
                    return
            _error(self, 404, "not found")

        def do_GET(self) -> None:
            self._dispatch("GET")

        def do_POST(self) -> None:
            self._dispatch("POST")

        def log_message(self, format, *args) -> None:  # noqa: A002
            # Quiet logging by default; tests rely on this not being noisy.
            return

    return Handler


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def serve(
    host: str = "127.0.0.1",
    port: int = 8080,
    *,
    tick_interval_s: float = 6.0,
    persist: bool = True,
) -> None:
    """Start the HTTP server and the background tick worker."""
    from socketserver import ThreadingMixIn

    class _ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
        daemon_threads = True

    registry = default_registry()
    world = load_world(tick_interval_s=tick_interval_s)
    ctx = ServerContext(registry, world=world)
    worker = TickWorker(world, registry, persist=persist)
    worker.start()
    httpd = _ThreadingHTTPServer((host, port), make_handler(ctx))
    print(f"D&D Sandbox listening on http://{host}:{port} "
          f"(tick={tick_interval_s}s, persist={persist})")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        worker.stop()
        httpd.server_close()


def main() -> None:
    parser = argparse.ArgumentParser(prog="dnd")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument(
        "--tick-interval", type=float, default=6.0,
        help="Seconds per PF1 round (tick). Default 6.0; "
             "set to 0.05 for tests.",
    )
    parser.add_argument(
        "--no-persist", action="store_true",
        help="Don't write to data/ — useful for ephemeral test runs.",
    )
    args = parser.parse_args()
    serve(
        host=args.host, port=args.port,
        tick_interval_s=args.tick_interval,
        persist=not args.no_persist,
    )


if __name__ == "__main__":
    main()
