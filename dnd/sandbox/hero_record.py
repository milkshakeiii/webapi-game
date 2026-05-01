"""Sandbox-side hero state.

A ``HeroRecord`` is the persistent slice of a hero — the static
``Character`` (race, class, feats, skills, equipment, level plan) plus
the mutable carry-over state between deployments (current HP, current
XP, status, deployment history).

The ``Combatant`` used during combat is *materialized* from a hero
record at deployment start by ``combatant_from_hero_record``. Combat
mutates the Combatant; on deployment end, we copy the relevant
fields (current HP, conditions worth keeping, etc.) back into the
HeroRecord.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from dnd.engine.characters import Character


# Hero lifecycle states.
HERO_AT_CASTLE = "at_castle"     # in residence; can be assigned a deployment
HERO_DEPLOYED = "deployed"       # currently out on a deployment
HERO_DEAD = "dead"               # in the graveyard
HERO_STATES = frozenset({HERO_AT_CASTLE, HERO_DEPLOYED, HERO_DEAD})


@dataclass
class HeroRecord:
    """Persistent state for one hero across deployments."""

    id: str
    name: str
    character: Character
    behavior_ref: str
    plan_ref: str | None = None

    status: str = HERO_AT_CASTLE
    current_hp: int = 0          # set by spawn / deployment finalization
    max_hp: int = 0              # cached for UI; recomputed on materialization
    current_xp: int = 0

    deployment_ids: list[str] = field(default_factory=list)
    spawned_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    died_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "character": self.character.to_dict(),
            "behavior_ref": self.behavior_ref,
            "plan_ref": self.plan_ref,
            "status": self.status,
            "current_hp": self.current_hp,
            "max_hp": self.max_hp,
            "current_xp": self.current_xp,
            "deployment_ids": list(self.deployment_ids),
            "spawned_at": self.spawned_at.isoformat(),
            "died_at": self.died_at.isoformat() if self.died_at else None,
        }

    @classmethod
    def from_dict(cls, d: dict) -> HeroRecord:
        if d.get("status", HERO_AT_CASTLE) not in HERO_STATES:
            raise ValueError(f"unknown hero status {d.get('status')!r}")
        return cls(
            id=str(d["id"]),
            name=str(d["name"]),
            character=Character.from_dict(d["character"]),
            behavior_ref=str(d["behavior_ref"]),
            plan_ref=d.get("plan_ref"),
            status=str(d.get("status", HERO_AT_CASTLE)),
            current_hp=int(d.get("current_hp", 0)),
            max_hp=int(d.get("max_hp", 0)),
            current_xp=int(d.get("current_xp", 0)),
            deployment_ids=list(d.get("deployment_ids") or []),
            spawned_at=datetime.fromisoformat(d["spawned_at"])
                if d.get("spawned_at") else datetime.now(timezone.utc),
            died_at=(datetime.fromisoformat(d["died_at"])
                     if d.get("died_at") else None),
        )

    def is_alive(self) -> bool:
        return self.status != HERO_DEAD
