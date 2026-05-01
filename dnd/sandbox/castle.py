"""Castle: the patron's persistent identity.

A castle owns:

- A renown balance + an append-only ledger of every income/spend entry.
- A treasury (gold; items deferred to Phase 4).
- A roster (heroes currently at-castle or deployed) and a graveyard
  (heroes who died on deployment, kept for history).
- A library of behavior scripts and level-up plans the patron has
  uploaded. Reusable across heroes; one script can drive many heroes.
- A home position on the world grid (where deployments depart and
  return).

Persistence is one JSON file per castle at ``data/castles/{id}.json``.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .hero_record import HeroRecord
from .storage import data_root, read_json, write_json_atomic


# Default starting renown for a new castle.
NEW_CASTLE_STARTING_RENOWN = 100

# Renown cost to spawn an L1 hero. (Higher levels are deferred; this is
# the only cost shape v1 uses.)
RENOWN_COST_L1_HERO = 10


# ---------------------------------------------------------------------------
# Renown ledger
# ---------------------------------------------------------------------------


@dataclass
class RenownEntry:
    """One entry in the append-only ledger.

    Positive ``delta`` is income; negative is a spend. ``reason`` is a
    short tag (e.g., ``"deployment_reward"``, ``"spawn_hero"``); ``ref``
    is an optional related object id (deployment id, hero id, etc.).
    """

    tick: int
    delta: int
    reason: str
    ref: str | None = None
    note: str = ""

    def to_dict(self) -> dict:
        return {
            "tick": self.tick,
            "delta": self.delta,
            "reason": self.reason,
            "ref": self.ref,
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, d: dict) -> RenownEntry:
        return cls(
            tick=int(d["tick"]),
            delta=int(d["delta"]),
            reason=str(d["reason"]),
            ref=d.get("ref"),
            note=str(d.get("note", "")),
        )


# ---------------------------------------------------------------------------
# Castle
# ---------------------------------------------------------------------------


@dataclass
class Castle:
    """One patron's persistent state."""

    id: str
    name: str
    patron_email: str
    home_position: tuple[int, int]

    renown: int = NEW_CASTLE_STARTING_RENOWN
    lifetime_renown: int = NEW_CASTLE_STARTING_RENOWN

    treasury_gold: int = 0

    roster: dict[str, HeroRecord] = field(default_factory=dict)
    graveyard: dict[str, HeroRecord] = field(default_factory=dict)

    # Behavior scripts and level-up plans stored as raw text (the
    # engine parses them on use). Keyed by patron-chosen name.
    library_behaviors: dict[str, str] = field(default_factory=dict)
    library_plans: dict[str, str] = field(default_factory=dict)

    renown_ledger: list[RenownEntry] = field(default_factory=list)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    # ── Renown ───────────────────────────────────────────────────────────

    def credit(
        self, amount: int, reason: str, *, tick: int, ref: str | None = None,
        note: str = "",
    ) -> None:
        """Add renown. Negative amounts are rejected (use ``debit``)."""
        if amount < 0:
            raise ValueError("credit amount must be >= 0")
        if amount == 0:
            return
        self.renown += amount
        self.lifetime_renown += amount
        self.renown_ledger.append(RenownEntry(
            tick=tick, delta=amount, reason=reason, ref=ref, note=note,
        ))

    def debit(
        self, amount: int, reason: str, *, tick: int, ref: str | None = None,
        note: str = "",
    ) -> None:
        """Spend renown. Caller must ensure balance is sufficient."""
        if amount < 0:
            raise ValueError("debit amount must be >= 0")
        if amount > self.renown:
            raise ValueError(
                f"insufficient renown: need {amount}, have {self.renown}"
            )
        if amount == 0:
            return
        self.renown -= amount
        self.renown_ledger.append(RenownEntry(
            tick=tick, delta=-amount, reason=reason, ref=ref, note=note,
        ))

    # ── Roster ───────────────────────────────────────────────────────────

    def add_hero(self, hero: HeroRecord) -> None:
        if hero.id in self.roster or hero.id in self.graveyard:
            raise ValueError(f"hero {hero.id!r} already in this castle")
        self.roster[hero.id] = hero

    def get_hero(self, hero_id: str) -> HeroRecord | None:
        return self.roster.get(hero_id) or self.graveyard.get(hero_id)

    def bury(self, hero_id: str, *, died_at_tick: int) -> None:
        """Move a hero from the active roster to the graveyard."""
        hero = self.roster.pop(hero_id, None)
        if hero is None:
            raise KeyError(hero_id)
        from .hero_record import HERO_DEAD
        hero.status = HERO_DEAD
        hero.died_at = datetime.now(timezone.utc)
        self.graveyard[hero_id] = hero

    # ── Persistence ──────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "patron_email": self.patron_email,
            "home_position": list(self.home_position),
            "renown": self.renown,
            "lifetime_renown": self.lifetime_renown,
            "treasury_gold": self.treasury_gold,
            "roster": {hid: h.to_dict() for hid, h in self.roster.items()},
            "graveyard": {hid: h.to_dict() for hid, h in self.graveyard.items()},
            "library_behaviors": dict(self.library_behaviors),
            "library_plans": dict(self.library_plans),
            "renown_ledger": [e.to_dict() for e in self.renown_ledger],
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> Castle:
        return cls(
            id=str(d["id"]),
            name=str(d["name"]),
            patron_email=str(d["patron_email"]),
            home_position=tuple(d["home_position"]),
            renown=int(d.get("renown", 0)),
            lifetime_renown=int(d.get("lifetime_renown", 0)),
            treasury_gold=int(d.get("treasury_gold", 0)),
            roster={
                hid: HeroRecord.from_dict(h)
                for hid, h in (d.get("roster") or {}).items()
            },
            graveyard={
                hid: HeroRecord.from_dict(h)
                for hid, h in (d.get("graveyard") or {}).items()
            },
            library_behaviors=dict(d.get("library_behaviors") or {}),
            library_plans=dict(d.get("library_plans") or {}),
            renown_ledger=[
                RenownEntry.from_dict(e) for e in (d.get("renown_ledger") or [])
            ],
            created_at=(
                datetime.fromisoformat(d["created_at"])
                if d.get("created_at") else datetime.now(timezone.utc)
            ),
        )


# ---------------------------------------------------------------------------
# Construction + persistence helpers
# ---------------------------------------------------------------------------


def new_castle(
    name: str,
    patron_email: str,
    home_position: tuple[int, int],
    *,
    starting_renown: int = NEW_CASTLE_STARTING_RENOWN,
    castle_id: str | None = None,
) -> Castle:
    cid = castle_id or f"castle_{uuid.uuid4().hex[:8]}"
    return Castle(
        id=cid,
        name=name,
        patron_email=patron_email,
        home_position=home_position,
        renown=starting_renown,
        lifetime_renown=starting_renown,
    )


def _castle_file(castle_id: str) -> Path:
    return data_root() / "castles" / f"{castle_id}.json"


def save_castle(castle: Castle) -> None:
    write_json_atomic(_castle_file(castle.id), castle.to_dict())


def load_castle(castle_id: str) -> Castle | None:
    raw = read_json(_castle_file(castle_id))
    return Castle.from_dict(raw) if raw is not None else None


def load_all_castles() -> dict[str, Castle]:
    """Load every castle from disk into a dict by id."""
    out: dict[str, Castle] = {}
    castles_dir = data_root() / "castles"
    if not castles_dir.exists():
        return out
    for path in sorted(castles_dir.glob("*.json")):
        raw = read_json(path)
        if raw is None:
            continue
        try:
            c = Castle.from_dict(raw)
            out[c.id] = c
        except Exception:
            # Skip corrupt files; let an admin fix manually.
            continue
    return out
