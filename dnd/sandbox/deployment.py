"""Deployment, DeploymentEvent, WorldEncounter, Order data classes.

Deployments are *standing orders* attached to a hero. The tick worker
walks every active deployment each tick, advancing it one PF1 round
toward its objective. Events are appended to the deployment's log
keyed by the world tick they happened on.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .storage import data_root, read_json, write_json_atomic


# ---------------------------------------------------------------------------
# DeploymentPhase: explicit state machine for the deployment lifecycle
# ---------------------------------------------------------------------------


PHASE_PENDING = "pending"               # accepted by HTTP, not yet promoted
PHASE_TRAVELING_OUT = "traveling_out"   # walking to destination
PHASE_AT_DESTINATION = "at_destination" # arrived; engaging next tick
PHASE_IN_COMBAT = "in_combat"           # combat active
PHASE_RETREATING = "retreating"         # hero broke off, moving back
PHASE_RETURNING = "returning"           # combat done; walking home
PHASE_COMPLETE = "complete"             # banked, hero at_castle
PHASE_DEAD = "dead"                     # hero died on deployment


PHASES = frozenset({
    PHASE_PENDING, PHASE_TRAVELING_OUT, PHASE_AT_DESTINATION,
    PHASE_IN_COMBAT, PHASE_RETREATING, PHASE_RETURNING,
    PHASE_COMPLETE, PHASE_DEAD,
})


TERMINAL_PHASES = frozenset({PHASE_COMPLETE, PHASE_DEAD})


# ---------------------------------------------------------------------------
# DeploymentEvent
# ---------------------------------------------------------------------------


@dataclass
class DeploymentEvent:
    """One thing that happened on a deployment, keyed to a world tick.

    ``kind`` examples: "depart", "step", "arrive", "engage",
    "round" (one combat round resolved), "loot", "return", "death",
    "complete".
    """

    tick: int
    kind: str
    detail: dict

    def to_dict(self) -> dict:
        return {"tick": self.tick, "kind": self.kind, "detail": self.detail}

    @classmethod
    def from_dict(cls, d: dict) -> DeploymentEvent:
        return cls(
            tick=int(d["tick"]),
            kind=str(d["kind"]),
            detail=dict(d.get("detail") or {}),
        )


# ---------------------------------------------------------------------------
# Deployment
# ---------------------------------------------------------------------------


@dataclass
class Deployment:
    """A single hero's standing order, advanced one round per tick."""

    id: str
    castle_id: str
    hero_id: str
    destination_location_id: str
    behavior_ref: str
    plan_ref: str | None

    submitted_at_tick: int           # tick at which the worker drained the order
    seed: int                        # deterministic anchor for this deployment

    phase: str = PHASE_PENDING
    completed_at_tick: int | None = None

    # Path the hero is currently following. A list of grid cells.
    # The hero's position is path[path_index].
    path: list[tuple[int, int]] = field(default_factory=list)
    path_index: int = 0

    # Set while phase == IN_COMBAT.
    encounter_id: str | None = None

    events: list[DeploymentEvent] = field(default_factory=list)

    # Running rewards.
    renown_earned: int = 0
    gold_earned: int = 0
    items_earned: list[str] = field(default_factory=list)

    received_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    # ── Helpers ──────────────────────────────────────────────────────────

    @property
    def hero_position(self) -> tuple[int, int] | None:
        if not self.path:
            return None
        idx = max(0, min(self.path_index, len(self.path) - 1))
        return self.path[idx]

    def is_terminal(self) -> bool:
        return self.phase in TERMINAL_PHASES

    def append_event(self, tick: int, kind: str, detail: dict | None = None) -> None:
        self.events.append(DeploymentEvent(
            tick=tick, kind=kind, detail=dict(detail or {}),
        ))

    # ── Persistence ──────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "castle_id": self.castle_id,
            "hero_id": self.hero_id,
            "destination_location_id": self.destination_location_id,
            "behavior_ref": self.behavior_ref,
            "plan_ref": self.plan_ref,
            "submitted_at_tick": self.submitted_at_tick,
            "seed": self.seed,
            "phase": self.phase,
            "completed_at_tick": self.completed_at_tick,
            "path": [list(p) for p in self.path],
            "path_index": self.path_index,
            "encounter_id": self.encounter_id,
            "events": [e.to_dict() for e in self.events],
            "renown_earned": self.renown_earned,
            "gold_earned": self.gold_earned,
            "items_earned": list(self.items_earned),
            "received_at": self.received_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> Deployment:
        if d.get("phase", PHASE_PENDING) not in PHASES:
            raise ValueError(f"unknown deployment phase {d.get('phase')!r}")
        return cls(
            id=str(d["id"]),
            castle_id=str(d["castle_id"]),
            hero_id=str(d["hero_id"]),
            destination_location_id=str(d["destination_location_id"]),
            behavior_ref=str(d["behavior_ref"]),
            plan_ref=d.get("plan_ref"),
            submitted_at_tick=int(d["submitted_at_tick"]),
            seed=int(d["seed"]),
            phase=str(d.get("phase", PHASE_PENDING)),
            completed_at_tick=(
                int(d["completed_at_tick"])
                if d.get("completed_at_tick") is not None else None
            ),
            path=[tuple(p) for p in (d.get("path") or [])],
            path_index=int(d.get("path_index", 0)),
            encounter_id=d.get("encounter_id"),
            events=[DeploymentEvent.from_dict(e) for e in (d.get("events") or [])],
            renown_earned=int(d.get("renown_earned", 0)),
            gold_earned=int(d.get("gold_earned", 0)),
            items_earned=list(d.get("items_earned") or []),
            received_at=(
                datetime.fromisoformat(d["received_at"])
                if d.get("received_at") else datetime.now(timezone.utc)
            ),
        )


# ---------------------------------------------------------------------------
# WorldEncounter: links the engine's Encounter to deployments + a location
# ---------------------------------------------------------------------------


@dataclass
class WorldEncounter:
    """Sandbox-side wrapper around an in-progress combat encounter.

    The combat engine's ``Encounter`` is held by reference; the
    sandbox owns "where this fight is happening" and "which
    deployments' heroes are in it."
    """

    id: str
    location_id: str | None
    deployment_ids: list[str]
    started_at_tick: int
    ended_at_tick: int | None = None

    # The engine's Encounter object. Not serialized — encounters are
    # ephemeral and live only in memory while phase == IN_COMBAT.
    engine_encounter: Any = None
    grid: Any = None


# ---------------------------------------------------------------------------
# Order
# ---------------------------------------------------------------------------


# Order kinds the worker knows how to apply.
ORDER_SPAWN_HERO = "spawn_hero"
ORDER_SUBMIT_DEPLOYMENT = "submit_deployment"
ORDER_UPLOAD_BEHAVIOR = "upload_behavior"
ORDER_UPLOAD_PLAN = "upload_plan"
ORDER_CREATE_CASTLE = "create_castle"

KNOWN_ORDER_KINDS = frozenset({
    ORDER_SPAWN_HERO, ORDER_SUBMIT_DEPLOYMENT,
    ORDER_UPLOAD_BEHAVIOR, ORDER_UPLOAD_PLAN, ORDER_CREATE_CASTLE,
})


@dataclass
class Order:
    """A queued state-mutation request from an HTTP handler.

    HTTP handlers do all validation up front (so a malformed request
    is a synchronous 4xx, not a deferred error). ``payload`` carries
    the validated data structures (e.g., a fully constructed
    ``Character`` for a ``spawn_hero`` order).
    """

    id: str
    castle_id: str | None       # None for create_castle (no castle yet)
    kind: str
    payload: dict
    received_at: datetime
    accepted_at_tick: int | None = None

    def __post_init__(self) -> None:
        if self.kind not in KNOWN_ORDER_KINDS:
            raise ValueError(f"unknown order kind {self.kind!r}")


def new_order(
    castle_id: str | None,
    kind: str,
    payload: dict,
) -> Order:
    return Order(
        id=f"ord_{uuid.uuid4().hex[:8]}",
        castle_id=castle_id,
        kind=kind,
        payload=payload,
        received_at=datetime.now(timezone.utc),
    )


# ---------------------------------------------------------------------------
# Persistence helpers for Deployment
# ---------------------------------------------------------------------------


def _deployment_file(deployment_id: str) -> Path:
    return data_root() / "deployments" / f"{deployment_id}.json"


def save_deployment(d: Deployment) -> None:
    write_json_atomic(_deployment_file(d.id), d.to_dict())


def load_deployment(deployment_id: str) -> Deployment | None:
    raw = read_json(_deployment_file(deployment_id))
    return Deployment.from_dict(raw) if raw is not None else None


def load_all_deployments() -> dict[str, Deployment]:
    """Load every deployment file into a dict by id."""
    out: dict[str, Deployment] = {}
    deployments_dir = data_root() / "deployments"
    if not deployments_dir.exists():
        return out
    for path in sorted(deployments_dir.glob("*.json")):
        raw = read_json(path)
        if raw is None:
            continue
        try:
            d = Deployment.from_dict(raw)
            out[d.id] = d
        except Exception:
            continue
    return out
