#!/usr/bin/env python3
"""HTTP server for Shattered Archive.

Usage:
    python3 server.py [--port 8080] [--host 127.0.0.1]
"""

from __future__ import annotations

import argparse
import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Callable

from sessions import SessionStore

# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

Route = tuple[str, re.Pattern[str], Callable]
_routes: list[Route] = []


def route(method: str, pattern: str):
    """Decorator to register a route handler."""
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
        return json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def _respond(handler: BaseHTTPRequestHandler, status: int, body: dict) -> None:
    payload = json.dumps(body, indent=2).encode()
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(payload)))
    handler.end_headers()
    handler.wfile.write(payload)


def _error(handler: BaseHTTPRequestHandler, status: int, message: str) -> None:
    _respond(handler, status, {"error": message})


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

@route("POST", r"/v1/sessions$")
def handle_create_session(handler: BaseHTTPRequestHandler, _match, store: SessionStore):
    body = _read_json(handler)
    if body is None:
        return _error(handler, 400, "Malformed JSON.")
    session = store.create()
    _respond(handler, 201, {
        "session": {
            "session_id": session.session_id,
            "game": session.game,
            "status": session.status,
        },
        "room": {
            "room_id": session.current_room.room_id,
            "title": session.current_room.title,
            "description": session.current_room.description,
        },
        "active_puzzle": session.puzzle_summary(),
    })


@route("GET", r"/v1/sessions/(?P<session_id>[^/]+)$")
def handle_get_session(handler: BaseHTTPRequestHandler, match, store: SessionStore):
    session = store.get(match.group("session_id"))
    if session is None:
        return _error(handler, 404, "Session not found.")
    _respond(handler, 200, session.session_view())


@route("POST", r"/v1/sessions/(?P<session_id>[^/]+)/commands$")
def handle_command(handler: BaseHTTPRequestHandler, match, store: SessionStore):
    session = store.get(match.group("session_id"))
    if session is None:
        return _error(handler, 404, "Session not found.")
    body = _read_json(handler)
    if body is None:
        return _error(handler, 400, "Malformed JSON.")
    if "op" not in body:
        return _error(handler, 400, "Missing 'op' field.")

    result = store.execute_command(session, body)

    from sessions import _gen_id
    command_id = _gen_id("cmd_")

    response: dict = {
        "command_id": command_id,
        "result": result.result,
        "narration": result.narration,
    }
    if result.room:
        response["room"] = result.room
    if result.active_puzzle:
        response["active_puzzle"] = result.active_puzzle
    if result.error_code:
        response["error_code"] = result.error_code
    _respond(handler, 200, response)


@route("GET", r"/v1/sessions/(?P<session_id>[^/]+)/puzzles/(?P<puzzle_id>[^/]+)$")
def handle_get_puzzle(handler: BaseHTTPRequestHandler, match, store: SessionStore):
    session = store.get(match.group("session_id"))
    if session is None:
        return _error(handler, 404, "Session not found.")
    puzzle_id = match.group("puzzle_id")
    view = session.puzzle_view(puzzle_id)
    if view is None:
        return _error(handler, 404, "Puzzle not found.")
    _respond(handler, 200, view)


@route("POST", r"/v1/sessions/(?P<session_id>[^/]+)/puzzles/(?P<puzzle_id>[^/]+)/attempts$")
def handle_attempt(handler: BaseHTTPRequestHandler, match, store: SessionStore):
    session = store.get(match.group("session_id"))
    if session is None:
        return _error(handler, 404, "Session not found.")
    body = _read_json(handler)
    if body is None:
        return _error(handler, 400, "Malformed JSON.")

    puzzle_id = match.group("puzzle_id")
    response, status, error_msg = store.evaluate_attempt(session, puzzle_id, body)
    if error_msg:
        return _error(handler, status, error_msg)
    _respond(handler, status, response)


# ---------------------------------------------------------------------------
# Handler factory
# ---------------------------------------------------------------------------

def make_handler(store: SessionStore):
    class Handler(BaseHTTPRequestHandler):
        def _dispatch(self, method: str) -> None:
            for route_method, pattern, fn in _routes:
                if route_method != method:
                    continue
                m = pattern.match(self.path)
                if m:
                    fn(self, m, store)
                    return
            _error(self, 404, "Not found.")

        def do_GET(self) -> None:
            self._dispatch("GET")

        def do_POST(self) -> None:
            self._dispatch("POST")

        def log_message(self, format, *args) -> None:
            # Quieter logging: method + path + status only.
            pass

    return Handler


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Shattered Archive API server")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--host", type=str, default="127.0.0.1")
    args = parser.parse_args()

    store = SessionStore()
    server = HTTPServer((args.host, args.port), make_handler(store))
    print(f"Shattered Archive API running on http://{args.host}:{args.port}/v1")
    print(f"Loaded {len(store._puzzles)} puzzle(s)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
