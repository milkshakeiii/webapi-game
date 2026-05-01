"""World boot: load hand-authored locations and construct the initial
world or load the persisted world snapshot.

Boot order on server start:

1. If ``data/world.json`` exists → load it. The locations baked in
   from the last run come back, including their cleared-state.
2. Otherwise → fresh world: load every JSON file under
   ``dnd/content/locations/`` and place those locations on a new
   empty 200×200 world. Persist immediately.
"""

from __future__ import annotations

import json
from pathlib import Path

from .storage import data_root, read_json, write_json_atomic
from .world import LOC_ACTIVE, Location, World, new_world


# ---------------------------------------------------------------------------
# Content paths
# ---------------------------------------------------------------------------


def _locations_content_dir() -> Path:
    """Path to the bundled location templates."""
    here = Path(__file__).resolve()
    # dnd/sandbox/boot.py → dnd/content/locations
    return here.parent.parent / "content" / "locations"


def _world_file_path() -> Path:
    return data_root() / "world.json"


# ---------------------------------------------------------------------------
# Load / construct
# ---------------------------------------------------------------------------


def load_world(tick_interval_s: float = 6.0) -> World:
    """Load the persisted world, or construct a fresh one from content.

    ``tick_interval_s`` is honored only when constructing fresh; an
    existing ``world.json`` carries its own clock.
    """
    persisted = read_json(_world_file_path())
    if persisted is not None:
        return World.from_dict(persisted)
    return _fresh_world(tick_interval_s)


def save_world(world: World) -> None:
    """Persist the world map (locations + clock) to ``data/world.json``.

    Castles, deployments, and other state live in their own files;
    this function only writes the world map slice.
    """
    write_json_atomic(_world_file_path(), world.to_dict())


def _fresh_world(tick_interval_s: float) -> World:
    """Build a new 200×200 world populated from bundled location files."""
    world = new_world(width=200, height=200, tick_interval_s=tick_interval_s)
    for loc in _read_bundled_locations():
        world.locations[loc.id] = loc
    return world


def _read_bundled_locations() -> list[Location]:
    """Read every JSON file under ``content/locations/``."""
    out: list[Location] = []
    d = _locations_content_dir()
    if not d.exists():
        return out
    for path in sorted(d.glob("*.json")):
        with path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        # Default state to ACTIVE if not specified by content.
        raw.setdefault("state", LOC_ACTIVE)
        out.append(Location.from_dict(raw))
    return out
