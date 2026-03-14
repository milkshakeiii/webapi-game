"""In-memory session store and session lifecycle."""

from __future__ import annotations

import secrets
from dataclasses import dataclass, field
from pathlib import Path

from engine import AttemptResult, evaluate_attempt
from simulator import Puzzle, load_puzzle
from world import (
    CommandResult,
    Room,
    apply_effects,
    copy_rooms,
    execute_inspect,
    execute_look,
    execute_move,
    room_summary,
    room_view,
    START_ROOM,
)

PUZZLE_DIR = Path(__file__).resolve().parent / "content" / "puzzles"


def _load_all_puzzles() -> dict[str, Puzzle]:
    puzzles: dict[str, Puzzle] = {}
    if PUZZLE_DIR.exists():
        for path in sorted(PUZZLE_DIR.glob("*.json")):
            puzzle = load_puzzle(path)
            puzzles[puzzle.puzzle_id] = puzzle
    # Also load from examples/ for backward compat.
    examples = Path(__file__).resolve().parent / "examples"
    if examples.exists():
        for path in sorted(examples.glob("*.json")):
            puzzle = load_puzzle(path)
            if puzzle.puzzle_id not in puzzles:
                puzzles[puzzle.puzzle_id] = puzzle
    return puzzles


def _gen_id(prefix: str) -> str:
    return f"{prefix}{secrets.token_hex(16)}"


@dataclass
class Session:
    session_id: str
    game: str
    status: str
    current_room_id: str
    rooms: dict[str, Room]
    puzzles: dict[str, Puzzle]
    puzzle_status: dict[str, str] = field(default_factory=dict)
    puzzle_revisions: dict[str, int] = field(default_factory=dict)
    active_puzzle_id: str | None = None
    inventory: list = field(default_factory=list)
    solved_puzzles: set[str] = field(default_factory=set)

    @property
    def current_room(self) -> Room:
        return self.rooms[self.current_room_id]

    def puzzle_summary(self) -> dict | None:
        if self.active_puzzle_id is None:
            return None
        puzzle = self.puzzles.get(self.active_puzzle_id)
        if puzzle is None:
            return None
        return {
            "puzzle_id": puzzle.puzzle_id,
            "title": puzzle.name,
            "status": self.puzzle_status.get(puzzle.puzzle_id, "active"),
        }

    def session_view(self) -> dict:
        return {
            "session_id": self.session_id,
            "game": self.game,
            "status": self.status,
            "room": room_view(self.current_room),
            "inventory": self.inventory,
            "active_puzzle": self.puzzle_summary(),
        }

    def puzzle_view(self, puzzle_id: str) -> dict | None:
        puzzle = self.puzzles.get(puzzle_id)
        if puzzle is None:
            return None
        return {
            "puzzle_id": puzzle.puzzle_id,
            "title": puzzle.name,
            "status": self.puzzle_status.get(puzzle.puzzle_id, "active"),
            "puzzle_revision": self.puzzle_revisions.get(puzzle.puzzle_id, 1),
            "bench_capacity": puzzle.bench_capacity,
            "step_limit": puzzle.step_limit,
            "contract": {
                "minimum_essences": dict(zip(
                    ("lumen", "echo", "motive", "veil"),
                    puzzle.contract.minimum_essences,
                )),
                "maximum_essences": dict(zip(
                    ("lumen", "echo", "motive", "veil"),
                    puzzle.contract.maximum_essences,
                )),
                "required_tags": list(puzzle.contract.required_tags),
                "forbidden_tags": list(puzzle.contract.forbidden_tags),
                "max_fray": puzzle.contract.max_fray,
            },
            "reagents": [
                {
                    "id": r.reagent_id,
                    "name": r.name,
                    "essences": dict(zip(
                        ("lumen", "echo", "motive", "veil"),
                        r.essences,
                    )),
                    "tags": list(r.tags),
                    "cost": r.cost,
                    "count": r.count,
                }
                for r in puzzle.reagents.values()
            ],
        }


class SessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}
        self._puzzles: dict[str, Puzzle] = _load_all_puzzles()

    def create(self) -> Session:
        session_id = _gen_id("ses_")
        rooms = copy_rooms()
        session = Session(
            session_id=session_id,
            game="shattered_archive",
            status="active",
            current_room_id=START_ROOM,
            rooms=rooms,
            puzzles=dict(self._puzzles),
            puzzle_status={pid: "active" for pid in self._puzzles},
            puzzle_revisions={pid: 1 for pid in self._puzzles},
        )
        # Auto-activate the first room's puzzle.
        for interactable in rooms[START_ROOM].interactables:
            if interactable.puzzle_id and interactable.puzzle_id in self._puzzles:
                session.active_puzzle_id = interactable.puzzle_id
                break
        self._sessions[session_id] = session
        return session

    def get(self, session_id: str) -> Session | None:
        return self._sessions.get(session_id)

    # ------------------------------------------------------------------
    # Commands
    # ------------------------------------------------------------------

    def execute_command(self, session: Session, command: dict) -> CommandResult:
        op = command.get("op")
        room = session.current_room

        if op == "look":
            result = execute_look(room)
            result.active_puzzle = session.puzzle_summary()
            return result

        if op == "move":
            exit_label = command.get("exit", "")
            result, new_room_id = execute_move(session.rooms, room, exit_label)
            if new_room_id:
                session.current_room_id = new_room_id
                # Auto-activate puzzle in new room if there is one.
                new_room = session.current_room
                for interactable in new_room.interactables:
                    if (
                        interactable.puzzle_id
                        and interactable.puzzle_id in session.puzzles
                        and session.puzzle_status.get(interactable.puzzle_id) == "active"
                    ):
                        session.active_puzzle_id = interactable.puzzle_id
                        break
            result.active_puzzle = session.puzzle_summary()
            return result

        if op == "inspect":
            target = command.get("target", "")
            result = execute_inspect(room, target, session.puzzle_status)
            # If inspect activates a puzzle, set it on the session.
            if result.active_puzzle and result.active_puzzle.get("status") == "active":
                session.active_puzzle_id = result.active_puzzle["puzzle_id"]
            result.active_puzzle = session.puzzle_summary()
            return result

        return CommandResult(
            result="error",
            narration=f"Unknown command: {op}",
            room=room_summary(room),
            error_code="unknown_command",
        )

    # ------------------------------------------------------------------
    # Attempts
    # ------------------------------------------------------------------

    def evaluate_attempt(
        self,
        session: Session,
        puzzle_id: str,
        body: dict,
    ) -> tuple[dict | None, int, str | None]:
        """Evaluate a synthesis attempt.

        Returns (response_body, http_status, error_message).
        """
        puzzle = session.puzzles.get(puzzle_id)
        if puzzle is None:
            return None, 404, "Puzzle not found."

        mode = body.get("mode")
        if mode not in ("simulate", "commit"):
            return None, 400, "mode must be 'simulate' or 'commit'."

        revision = body.get("puzzle_revision")
        current_revision = session.puzzle_revisions.get(puzzle_id, 1)
        if revision is not None and revision != current_revision:
            return None, 409, f"Stale puzzle_revision. Current is {current_revision}."

        if mode == "commit" and session.puzzle_status.get(puzzle_id) == "solved":
            return None, 409, "Puzzle is already solved."

        actions = body.get("actions")
        if not isinstance(actions, list):
            return None, 400, "actions must be an array."

        result: AttemptResult = evaluate_attempt(puzzle, actions)

        attempt_id = _gen_id("att_")
        response: dict = {
            "attempt_id": attempt_id,
            "session_id": session.session_id,
            "puzzle_id": puzzle_id,
            "puzzle_revision": current_revision,
            "mode": mode,
            "resolution": result.resolution,
        }

        if result.resolution == "invalid":
            response["failed_step"] = result.failed_step
            response["error"] = result.error
            response["trace"] = result.trace
        else:
            response["summary"] = result.summary
            response["trace"] = result.trace

        # Apply commit effects.
        if mode == "commit" and result.resolution == "success":
            session.puzzle_status[puzzle_id] = "solved"
            session.solved_puzzles.add(puzzle_id)
            session.puzzle_revisions[puzzle_id] = current_revision + 1
            effects = apply_effects(session.rooms, puzzle_id)
            response["commit"] = {
                "applied": True,
                "puzzle_status": "solved",
                "effects": effects,
            }

        return response, 200, None
