"""Room graph, exploration commands, and world effects.

Rooms are loaded from ``content/rooms.json``.  Each session gets its own
mutable deep copy of the room graph so that world effects (e.g. unlocking
an exit after solving a puzzle) are scoped to individual sessions.
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from pathlib import Path

CONTENT_DIR = Path(__file__).resolve().parent / "content"

# Puzzle effects applied on successful commit.
PUZZLE_EFFECTS: dict[str, list[dict]] = {
    "lower_stacks_lantern": [
        {
            "type": "unlock_exit",
            "room_id": "lower_stacks_entry",
            "exit_id": "north_stair",
        },
        {
            "type": "room_text_change",
            "room_id": "lower_stacks_entry",
            "target": "lantern_bowl",
            "description": "The bowl now burns with a pale archive flame. The stairway below is faintly lit.",
        },
    ],
    "iron_seal_ward": [
        {
            "type": "unlock_exit",
            "room_id": "deep_stacks",
            "exit_id": "east_gate",
        },
        {
            "type": "room_text_change",
            "room_id": "deep_stacks",
            "target": "iron_seal",
            "description": "The seal's wards have dissolved. The iron disc hangs loose, the gate behind it open.",
        },
    ],
    "index_restoration": [
        {
            "type": "room_text_change",
            "room_id": "index_chamber",
            "target": "archive_index",
            "description": "The Index hums with restored knowledge. Its pages are whole and legible again.",
        },
    ],
}

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Exit:
    exit_id: str
    label: str
    target_room_id: str
    locked: bool
    reason: str | None

@dataclass
class Interactable:
    id: str
    label: str
    kind: str
    description: str
    puzzle_id: str | None

@dataclass
class Room:
    room_id: str
    title: str
    description: str
    exits: list[Exit] = field(default_factory=list)
    interactables: list[Interactable] = field(default_factory=list)


@dataclass
class CommandResult:
    result: str  # "ok" | "error"
    narration: str
    room: dict | None = None
    active_puzzle: dict | None = None
    error_code: str | None = None


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def _load_rooms_template() -> dict[str, Room]:
    raw = json.loads((CONTENT_DIR / "rooms.json").read_text())
    rooms: dict[str, Room] = {}
    for item in raw:
        exits = [
            Exit(
                exit_id=e["exit_id"],
                label=e["label"],
                target_room_id=e["target_room_id"],
                locked=e["locked"],
                reason=e.get("reason"),
            )
            for e in item.get("exits", [])
        ]
        interactables = [
            Interactable(
                id=i["id"],
                label=i["label"],
                kind=i["kind"],
                description=i["description"],
                puzzle_id=i.get("puzzle_id"),
            )
            for i in item.get("interactables", [])
        ]
        room = Room(
            room_id=item["room_id"],
            title=item["title"],
            description=item["description"],
            exits=exits,
            interactables=interactables,
        )
        rooms[room.room_id] = room
    return rooms


_ROOMS_TEMPLATE: dict[str, Room] | None = None


def get_rooms_template() -> dict[str, Room]:
    global _ROOMS_TEMPLATE
    if _ROOMS_TEMPLATE is None:
        _ROOMS_TEMPLATE = _load_rooms_template()
    return _ROOMS_TEMPLATE


def copy_rooms() -> dict[str, Room]:
    """Return a deep copy of the room template for a new session."""
    return copy.deepcopy(get_rooms_template())


START_ROOM = "lower_stacks_entry"


# ---------------------------------------------------------------------------
# Room serialisation helpers
# ---------------------------------------------------------------------------

def room_summary(room: Room) -> dict:
    return {
        "room_id": room.room_id,
        "title": room.title,
    }


def room_view(room: Room) -> dict:
    return {
        "room_id": room.room_id,
        "title": room.title,
        "description": room.description,
        "exits": [
            {
                "exit_id": e.exit_id,
                "label": e.label,
                "locked": e.locked,
                **({"reason": e.reason} if e.locked and e.reason else {}),
            }
            for e in room.exits
        ],
        "interactables": [
            {
                "id": i.id,
                "label": i.label,
                "kind": i.kind,
            }
            for i in room.interactables
        ],
    }


# ---------------------------------------------------------------------------
# Exploration commands
# ---------------------------------------------------------------------------

def execute_look(room: Room) -> CommandResult:
    parts = [room.description]
    if room.exits:
        exit_lines = []
        for e in room.exits:
            status = " (locked)" if e.locked else ""
            exit_lines.append(f"  {e.label}{status}")
        parts.append("Exits:\n" + "\n".join(exit_lines))
    if room.interactables:
        items = ", ".join(i.label for i in room.interactables)
        parts.append(f"You see: {items}.")
    return CommandResult(
        result="ok",
        narration="\n\n".join(parts),
        room=room_summary(room),
    )


def execute_move(
    rooms: dict[str, Room],
    current_room: Room,
    exit_label: str,
) -> tuple[CommandResult, str | None]:
    """Attempt to move.  Returns (result, new_room_id or None)."""
    for e in current_room.exits:
        if e.label == exit_label or e.exit_id == exit_label:
            if e.locked:
                return (
                    CommandResult(
                        result="error",
                        narration=e.reason or "That way is blocked.",
                        room=room_summary(current_room),
                        error_code="exit_locked",
                    ),
                    None,
                )
            target = rooms.get(e.target_room_id)
            if target is None:
                return (
                    CommandResult(
                        result="error",
                        narration="That exit leads nowhere.",
                        error_code="invalid_exit",
                    ),
                    None,
                )
            return (
                CommandResult(
                    result="ok",
                    narration=f"You move {e.label}.\n\n{target.description}",
                    room=room_summary(target),
                ),
                target.room_id,
            )
    return (
        CommandResult(
            result="error",
            narration=f"There is no exit '{exit_label}' here.",
            error_code="unknown_exit",
        ),
        None,
    )


def execute_inspect(
    room: Room,
    target_id: str,
    puzzle_status: dict[str, str],
) -> CommandResult:
    for i in room.interactables:
        if i.id == target_id:
            narration = i.description
            active_puzzle = None
            if i.puzzle_id:
                status = puzzle_status.get(i.puzzle_id, "active")
                if status == "solved":
                    narration += "\n\nThis puzzle has already been solved."
                active_puzzle = {
                    "puzzle_id": i.puzzle_id,
                    "status": status,
                }
            return CommandResult(
                result="ok",
                narration=narration,
                room=room_summary(room),
                active_puzzle=active_puzzle,
            )
    return CommandResult(
        result="error",
        narration=f"There is nothing called '{target_id}' here.",
        error_code="unknown_target",
    )


# ---------------------------------------------------------------------------
# World effects
# ---------------------------------------------------------------------------

def apply_effects(rooms: dict[str, Room], puzzle_id: str) -> list[dict]:
    """Apply world effects for a solved puzzle.  Returns the list of effects."""
    effects = PUZZLE_EFFECTS.get(puzzle_id, [])
    for effect in effects:
        if effect["type"] == "unlock_exit":
            room = rooms.get(effect["room_id"])
            if room:
                for e in room.exits:
                    if e.exit_id == effect["exit_id"]:
                        e.locked = False
                        e.reason = None
        elif effect["type"] == "room_text_change":
            room = rooms.get(effect["room_id"])
            if room:
                for i in room.interactables:
                    if i.id == effect["target"]:
                        i.description = effect["description"]
    return effects
