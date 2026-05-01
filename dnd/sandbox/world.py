"""World, clock, location, and the order queue.

The ``World`` is the single in-memory root of all sandbox state — the
grid, the clock, the live deployments, the live encounters, the
castles (loaded into memory at boot, persisted back on every tick).

The tick worker is the sole writer of this state. HTTP write handlers
deposit ``Order`` objects into ``world.order_queue`` and the worker
drains them at the top of every tick.

HTTP read handlers deref ``world.current_snapshot`` — a JSON-shaped
dict updated by ``world.publish_snapshot()`` at the end of every tick.
Reads are lock-free; the worst they can see is "one tick stale".
"""

from __future__ import annotations

import threading
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


# ---------------------------------------------------------------------------
# Clock
# ---------------------------------------------------------------------------


@dataclass
class WorldClock:
    """The single global timeline.

    ``tick_number`` is the PF1 round number for the entire world. Every
    deployment, encounter, and location respawn is indexed by it.
    ``tick_interval_s`` is the wall-clock seconds between ticks
    (default 6.0 in prod, ~0.05 in test).
    """

    started_at: datetime
    tick_number: int = 0
    tick_interval_s: float = 6.0

    def to_dict(self) -> dict:
        return {
            "started_at": self.started_at.isoformat(),
            "tick_number": self.tick_number,
            "tick_interval_s": self.tick_interval_s,
        }

    @classmethod
    def from_dict(cls, d: dict) -> WorldClock:
        return cls(
            started_at=datetime.fromisoformat(d["started_at"]),
            tick_number=int(d["tick_number"]),
            tick_interval_s=float(d["tick_interval_s"]),
        )


# ---------------------------------------------------------------------------
# Location
# ---------------------------------------------------------------------------


# Location lifecycle states.
LOC_ACTIVE = "active"           # resident creatures present; engageable
LOC_CLEARED = "cleared"         # cleared; respawn pending
LOC_RESPAWNING = "respawning"   # transitional; not currently used in v1
LOCATION_STATES = frozenset({LOC_ACTIVE, LOC_CLEARED, LOC_RESPAWNING})


# Default respawn delay in ticks. 14400 ticks * 6s = 24 real-hours.
DEFAULT_RESPAWN_TICKS = 14400


@dataclass
class Location:
    """A point of interest on the world grid."""

    id: str
    name: str
    position: tuple[int, int]
    kind: str                      # "lair" | "ruins" | "camp" | ...
    description: str
    resident_template: str         # references content/encounters or a monster id
    base_renown: int               # renown earned by clearing this location

    state: str = LOC_ACTIVE
    cleared_at_tick: int | None = None
    cleared_by_castle: str | None = None
    respawn_ticks: int = DEFAULT_RESPAWN_TICKS

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "position": list(self.position),
            "kind": self.kind,
            "description": self.description,
            "resident_template": self.resident_template,
            "base_renown": self.base_renown,
            "state": self.state,
            "cleared_at_tick": self.cleared_at_tick,
            "cleared_by_castle": self.cleared_by_castle,
            "respawn_ticks": self.respawn_ticks,
        }

    @classmethod
    def from_dict(cls, d: dict) -> Location:
        if d.get("state", LOC_ACTIVE) not in LOCATION_STATES:
            raise ValueError(f"unknown location state {d.get('state')!r}")
        pos = d["position"]
        return cls(
            id=str(d["id"]),
            name=str(d["name"]),
            position=(int(pos[0]), int(pos[1])),
            kind=str(d["kind"]),
            description=str(d.get("description", "")),
            resident_template=str(d["resident_template"]),
            base_renown=int(d.get("base_renown", 10)),
            state=str(d.get("state", LOC_ACTIVE)),
            cleared_at_tick=(
                int(d["cleared_at_tick"]) if d.get("cleared_at_tick") is not None else None
            ),
            cleared_by_castle=d.get("cleared_by_castle"),
            respawn_ticks=int(d.get("respawn_ticks", DEFAULT_RESPAWN_TICKS)),
        )


# ---------------------------------------------------------------------------
# OrderQueue: thread-safe FIFO between HTTP and the tick worker
# ---------------------------------------------------------------------------


class OrderQueue:
    """Thread-safe FIFO of pending orders.

    HTTP write handlers call ``submit(order)``. The tick worker calls
    ``drain()`` at the top of each tick to take everything at once
    and apply each in order.

    We use a ``deque`` + lock rather than ``queue.Queue`` because we
    want a single atomic "snapshot then clear" rather than blocking
    pop-one-at-a-time.
    """

    def __init__(self) -> None:
        self._items: deque = deque()
        self._lock = threading.Lock()

    def submit(self, order: Any) -> None:
        with self._lock:
            self._items.append(order)

    def drain(self) -> list[Any]:
        with self._lock:
            items = list(self._items)
            self._items.clear()
        return items

    def __len__(self) -> int:
        with self._lock:
            return len(self._items)


# ---------------------------------------------------------------------------
# World
# ---------------------------------------------------------------------------


@dataclass
class World:
    """Root of the in-memory sandbox state.

    The tick worker mutates this object; HTTP read handlers see it
    through ``current_snapshot``.

    ``castles``, ``deployments``, ``active_encounters`` are kept as
    dicts-by-id for O(1) lookup. They live in memory; persistence
    fans out to per-castle and per-deployment files.
    """

    width: int
    height: int
    clock: WorldClock
    locations: dict[str, Location] = field(default_factory=dict)
    impassable_cells: set[tuple[int, int]] = field(default_factory=set)

    # Live state — populated at boot from disk, mutated by the tick worker.
    castles: dict[str, Any] = field(default_factory=dict)        # castle_id → Castle
    deployments: dict[str, Any] = field(default_factory=dict)    # deployment_id → Deployment
    active_encounters: dict[str, Any] = field(default_factory=dict)

    # Inter-thread coordination.
    order_queue: OrderQueue = field(default_factory=OrderQueue)
    write_lock: threading.RLock = field(default_factory=threading.RLock)

    # Last-published snapshot for HTTP readers. Updated atomically at
    # end of each tick. ``None`` until the first tick runs.
    _snapshot: dict | None = None

    # ── Snapshot publication ─────────────────────────────────────────────

    def publish_snapshot(self) -> None:
        """Refresh the read-only snapshot exposed to HTTP handlers.

        Must be called from inside the tick body (i.e. with the write
        lock held). Builds a fresh dict and assigns it; the assignment
        itself is GIL-atomic, so HTTP readers never see a half-built
        view.
        """
        snap = {
            "tick": self.clock.tick_number,
            "tick_interval_s": self.clock.tick_interval_s,
            "started_at": self.clock.started_at.isoformat(),
            "width": self.width,
            "height": self.height,
            "locations": {lid: loc.to_dict() for lid, loc in self.locations.items()},
            "impassable_cells": sorted(list(self.impassable_cells)),
        }
        self._snapshot = snap

    @property
    def current_snapshot(self) -> dict:
        """Return the most recently published snapshot.

        Lock-free. Returns an empty dict-shaped snapshot if no tick
        has run yet (rather than ``None``, so HTTP responses are
        always well-shaped).
        """
        if self._snapshot is None:
            return {
                "tick": self.clock.tick_number,
                "tick_interval_s": self.clock.tick_interval_s,
                "started_at": self.clock.started_at.isoformat(),
                "width": self.width,
                "height": self.height,
                "locations": {},
                "impassable_cells": [],
            }
        return self._snapshot

    # ── Serialization (whole-world dump for data/world.json) ────────────

    def to_dict(self) -> dict:
        """Persistent representation of the world map only.

        Castles and deployments persist to their own files; this dict
        is what ``data/world.json`` stores.
        """
        return {
            "width": self.width,
            "height": self.height,
            "clock": self.clock.to_dict(),
            "locations": [loc.to_dict() for loc in self.locations.values()],
            "impassable_cells": sorted(list(self.impassable_cells)),
        }

    @classmethod
    def from_dict(cls, d: dict) -> World:
        clock = (
            WorldClock.from_dict(d["clock"]) if "clock" in d
            else WorldClock(started_at=datetime.now(timezone.utc))
        )
        locs = {
            loc_dict["id"]: Location.from_dict(loc_dict)
            for loc_dict in d.get("locations") or []
        }
        impassable = {tuple(p) for p in d.get("impassable_cells") or []}
        return cls(
            width=int(d["width"]),
            height=int(d["height"]),
            clock=clock,
            locations=locs,
            impassable_cells=impassable,
        )


# ---------------------------------------------------------------------------
# Boot helpers
# ---------------------------------------------------------------------------


def new_world(
    width: int = 200,
    height: int = 200,
    tick_interval_s: float = 6.0,
) -> World:
    """Construct a fresh empty world. Locations are added by the boot
    layer (see ``boot.py`` / hand-authored content)."""
    return World(
        width=width,
        height=height,
        clock=WorldClock(
            started_at=datetime.now(timezone.utc),
            tick_number=0,
            tick_interval_s=tick_interval_s,
        ),
    )
