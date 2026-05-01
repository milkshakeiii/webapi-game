"""Typed modifier system.

The load-bearing rule across the engine: never store derived ints. Store
*inputs* and a list of typed modifiers, then compute on demand.

A ``Modifier`` is a tagged numeric adjustment to a specific stat
(``target``), tagged with a type that controls stacking. The
``compute()`` function walks a list of modifiers and applies the
stacking rules:

- Stacking types (``dodge``, ``circumstance``, ``untyped``) — every
  modifier contributes; sum them all.
- Non-stacking types (everything else) — for each polarity, only the
  most extreme value applies. So multiple +morale bonuses contribute
  only the highest; multiple -morale penalties contribute only the
  worst; bonus and penalty of the same type net against each other.

This module is data-only: it doesn't track game time. Modifier
expiration is handled by whoever holds the ``ModifierCollection``
(typically a ``Combatant``) by removing or filtering modifiers based
on their ``expires_round``.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field, replace
from typing import Iterable


# ---------------------------------------------------------------------------
# Modifier types
# ---------------------------------------------------------------------------


# Types whose modifiers all stack with each other.
STACKING_TYPES: frozenset[str] = frozenset({"dodge", "circumstance", "untyped"})

# A non-exhaustive list of valid modifier types. We don't enforce this set
# (untyped modifiers are a thing) but the engine should produce these names
# for known sources.
KNOWN_TYPES: frozenset[str] = frozenset({
    "alchemical", "armor", "circumstance", "competence", "deflection",
    "dodge", "enhancement", "inherent", "insight", "luck", "morale",
    "natural", "profane", "racial", "resistance", "sacred", "shield",
    "size", "trait", "untyped",
    # Used for ability-derived adjustments (e.g., Con mod's contribution to
    # a Fort save). Not strictly a PF1 modifier type, but useful for the
    # breakdown report.
    "ability",
    # The "base" pseudo-type: only ever used in the breakdown view.
    "base",
})


# ---------------------------------------------------------------------------
# Modifier dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Modifier:
    """A single typed adjustment to a single stat target.

    - ``value``: signed int (positive bonus, negative penalty).
    - ``type``: one of ``KNOWN_TYPES``. Determines stacking.
    - ``target``: which stat this modifier applies to. Conventional
      strings: ``"ac"``, ``"attack"``, ``"fort_save"``, ``"ref_save"``,
      ``"will_save"``, ``"cmb"``, ``"cmd"``, ``"hp_max"``,
      ``"ability:str"``, ``"skill:stealth"``, ``"speed"``, etc.
    - ``source``: human-readable identifier of where this modifier came
      from. Used for traces and for selectively removing modifiers
      (e.g., when rage ends).
    - ``expires_round``: absolute round number at which this modifier
      expires. ``None`` for permanent. The collection holder is
      responsible for ticking and pruning expired modifiers.
    """

    value: int
    type: str
    target: str
    source: str
    expires_round: int | None = None

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "type": self.type,
            "target": self.target,
            "source": self.source,
            "expires_round": self.expires_round,
        }


# ---------------------------------------------------------------------------
# Compute
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TypeBreakdown:
    """How modifiers of a single type combined, after stacking rules."""

    type: str
    applied: list[Modifier]      # modifiers that actually contributed
    suppressed: list[Modifier]   # modifiers that lost out to a same-type peer
    contribution: int            # net signed contribution to the total


def compute(base: int, mods: Iterable[Modifier]) -> int:
    """Apply ``mods`` to ``base`` and return the total."""
    total = base
    for type_, values in _group_by_type(mods).items():
        if type_ in STACKING_TYPES:
            total += sum(v.value for v in values)
        else:
            total += _net_non_stacking(values)
    return total


def compute_with_breakdown(
    base: int,
    mods: Iterable[Modifier],
) -> tuple[int, list[TypeBreakdown]]:
    """Return ``(total, breakdowns)`` so callers can show their work.

    Each ``TypeBreakdown`` describes which modifiers of a given type
    actually contributed and which got suppressed. Useful for API
    responses that show patrons why their score is what it is.
    """
    breakdowns: list[TypeBreakdown] = []
    total = base
    for type_, ms in _group_by_type(mods).items():
        if type_ in STACKING_TYPES:
            contribution = sum(m.value for m in ms)
            breakdowns.append(TypeBreakdown(
                type=type_,
                applied=list(ms),
                suppressed=[],
                contribution=contribution,
            ))
            total += contribution
        else:
            applied, suppressed = _split_non_stacking(ms)
            contribution = sum(m.value for m in applied)
            breakdowns.append(TypeBreakdown(
                type=type_,
                applied=applied,
                suppressed=suppressed,
                contribution=contribution,
            ))
            total += contribution
    return total, breakdowns


def _net_non_stacking(mods: list[Modifier]) -> int:
    pos = [m.value for m in mods if m.value > 0]
    neg = [m.value for m in mods if m.value < 0]
    return (max(pos) if pos else 0) + (min(neg) if neg else 0)


def _split_non_stacking(
    mods: list[Modifier],
) -> tuple[list[Modifier], list[Modifier]]:
    """Pick which modifiers actually applied for a non-stacking type."""
    pos = [m for m in mods if m.value > 0]
    neg = [m for m in mods if m.value < 0]
    zero = [m for m in mods if m.value == 0]

    applied: list[Modifier] = list(zero)  # zero-value mods are inert; let them
                                          # appear as "applied" with no effect.
    suppressed: list[Modifier] = []

    if pos:
        # Highest-value positive applies. Tie-broken by source name for
        # deterministic ordering.
        winner = max(pos, key=lambda m: (m.value, m.source))
        applied.append(winner)
        suppressed.extend(m for m in pos if m is not winner)
    if neg:
        # Most-extreme-negative penalty applies.
        winner = min(neg, key=lambda m: (m.value, m.source))
        applied.append(winner)
        suppressed.extend(m for m in neg if m is not winner)

    return applied, suppressed


def _group_by_type(mods: Iterable[Modifier]) -> dict[str, list[Modifier]]:
    grouped: dict[str, list[Modifier]] = defaultdict(list)
    for m in mods:
        grouped[m.type].append(m)
    return dict(grouped)


# ---------------------------------------------------------------------------
# Collection
# ---------------------------------------------------------------------------


@dataclass
class ModifierCollection:
    """A bag of modifiers held by a Combatant (or anything else)."""

    modifiers: list[Modifier] = field(default_factory=list)

    # ── construction ──────────────────────────────────────────────────────

    def add(self, mod: Modifier) -> None:
        self.modifiers.append(mod)

    def add_many(self, mods: Iterable[Modifier]) -> None:
        self.modifiers.extend(mods)

    def remove_by_source(self, source: str) -> int:
        """Drop every modifier with the given ``source``. Returns count."""
        before = len(self.modifiers)
        self.modifiers = [m for m in self.modifiers if m.source != source]
        return before - len(self.modifiers)

    def prune_expired(self, current_round: int) -> list[Modifier]:
        """Drop and return any modifiers whose ``expires_round`` <= the round."""
        kept: list[Modifier] = []
        expired: list[Modifier] = []
        for m in self.modifiers:
            if m.expires_round is not None and m.expires_round <= current_round:
                expired.append(m)
            else:
                kept.append(m)
        self.modifiers = kept
        return expired

    # ── queries ───────────────────────────────────────────────────────────

    def for_target(self, target: str) -> list[Modifier]:
        return [m for m in self.modifiers if m.target == target]

    def for_targets(self, targets: Iterable[str]) -> list[Modifier]:
        targets_set = set(targets)
        return [m for m in self.modifiers if m.target in targets_set]

    def from_source(self, source: str) -> list[Modifier]:
        return [m for m in self.modifiers if m.source == source]

    def total(self, base: int, target: str) -> int:
        """Compute the final value for a stat target."""
        return compute(base, self.for_target(target))

    def breakdown(
        self, base: int, target: str
    ) -> tuple[int, list[TypeBreakdown]]:
        return compute_with_breakdown(base, self.for_target(target))

    # ── debugging ─────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {"modifiers": [m.to_dict() for m in self.modifiers]}

    def copy(self) -> ModifierCollection:
        return ModifierCollection(modifiers=list(self.modifiers))


# ---------------------------------------------------------------------------
# Convenience: render a per-stat report for the API
# ---------------------------------------------------------------------------


def stat_report(
    base: int,
    base_label: str,
    mods: Iterable[Modifier],
) -> dict:
    """Return a JSON-friendly view of a stat: total, base, contributors.

    Used by the HTTP layer to expose both the total and *why*.

    ``base_label`` describes the source of the base value
    (e.g., ``"class:fighter:fort"`` for Fortitude save base).
    """
    total, breakdowns = compute_with_breakdown(base, mods)
    contributing: list[dict] = []
    suppressed: list[dict] = []
    for b in breakdowns:
        for m in b.applied:
            contributing.append(m.to_dict())
        for m in b.suppressed:
            suppressed.append(m.to_dict())
    out: dict = {
        "total": total,
        "base": base,
        "base_source": base_label,
        "modifiers": contributing,
    }
    if suppressed:
        out["suppressed"] = suppressed
    return out


# ---------------------------------------------------------------------------
# Helpers for constructing modifiers concisely
# ---------------------------------------------------------------------------


def mod(
    value: int,
    type: str,
    target: str,
    source: str,
    expires_round: int | None = None,
) -> Modifier:
    """Concise constructor — same fields as ``Modifier``, easier to read."""
    return Modifier(
        value=value, type=type, target=target,
        source=source, expires_round=expires_round,
    )


def with_target(modifiers: Iterable[Modifier], new_target: str) -> list[Modifier]:
    """Return new modifiers with the same fields but a different target.

    Useful when the same source contributes to multiple stats (e.g.,
    rage contributes morale bonuses to Str, Con, and Will saves).
    """
    return [replace(m, target=new_target) for m in modifiers]
