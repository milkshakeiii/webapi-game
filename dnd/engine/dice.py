"""Seeded dice expression parser and roller.

Supports the dice expressions we actually need for PF1:

- ``1d20``         — single die
- ``2d6+3``        — dice plus flat modifier
- ``1d8-1``        — dice minus flat modifier
- ``4d6kh3``       — roll 4d6, keep highest 3 (for ability score gen)
- ``4d6kl1``       — roll 4d6, keep lowest 1
- ``2d6+1d8+5``    — multiple dice terms
- ``5``            — flat number
- ``1d20`` etc are case-insensitive

Determinism is preserved by passing a seed (or a pre-built Random) into
the Roller. Two Rollers built from the same seed produce identical roll
sequences across runs and across processes.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from typing import Iterable


# A term is a dice or flat block with an optional leading sign:
#     [+-]? (NdM[kh|kl][N] | N)
TERM_PATTERN = re.compile(
    r"""
    \s*
    (?P<sign>[+-])?\s*
    (?:
        (?P<count>\d+)\s*[dD]\s*(?P<sides>\d+)
        (?:\s*(?P<keep>kh|kl|KH|KL)\s*(?P<keep_n>\d+))?
        |
        (?P<flat>\d+)
    )
    """,
    re.VERBOSE,
)


@dataclass(frozen=True)
class Term:
    """One signed term in a dice expression."""

    expression: str          # e.g. "+4d6kh3", "-1d8", "+5"
    sign: int                # +1 or -1
    count: int               # number of dice; 0 if flat
    sides: int               # die size; 0 if flat
    keep: str | None         # "kh", "kl", or None
    keep_n: int              # how many to keep; 0 if no keep clause
    flat: int                # flat modifier; 0 if dice
    rolls: tuple[int, ...]   # every individual die rolled (empty if flat)
    kept: tuple[int, ...]    # the rolls that actually contributed
    subtotal: int            # sign * (sum(kept) or flat)

    def to_dict(self) -> dict:
        return {
            "expression": self.expression,
            "sign": self.sign,
            "rolls": list(self.rolls),
            "kept": list(self.kept),
            "flat": self.flat if not self.rolls else None,
            "subtotal": self.subtotal,
        }


@dataclass(frozen=True)
class RollResult:
    """The full result of evaluating a dice expression."""

    expression: str
    total: int
    terms: tuple[Term, ...]
    breakdown: str

    def to_dict(self) -> dict:
        return {
            "expression": self.expression,
            "total": self.total,
            "terms": [t.to_dict() for t in self.terms],
            "breakdown": self.breakdown,
        }


class DiceError(ValueError):
    """Raised when a dice expression cannot be parsed or evaluated."""


def _validate_term(count: int, sides: int, keep: str | None, keep_n: int) -> None:
    if sides == 0:
        raise DiceError("die size must be at least 1")
    if count == 0:
        raise DiceError("die count must be at least 1")
    if count > 1000:
        raise DiceError("die count must be at most 1000")
    if sides > 1000:
        raise DiceError("die size must be at most 1000")
    if keep is not None:
        if keep_n < 1 or keep_n > count:
            raise DiceError(
                f"keep count {keep_n} must be between 1 and {count}"
            )


class Roller:
    """Wraps a ``random.Random`` and rolls dice expressions against it."""

    def __init__(self, seed: int | None = None, rng: random.Random | None = None):
        if rng is not None:
            self.rng = rng
        else:
            self.rng = random.Random(seed)

    def roll(self, expression: str, *, take_max: bool = False) -> RollResult:
        """Parse ``expression`` and roll the dice. Returns a ``RollResult``.

        ``take_max``: when True, every die returns its maximum face
        value instead of rolling. Used by Maximize Spell metamagic to
        produce the RAW behavior (each die takes its max).
        """

        if not expression or not expression.strip():
            raise DiceError("empty dice expression")

        cleaned = expression.strip()
        terms: list[Term] = []
        cursor = 0

        for i, match in enumerate(TERM_PATTERN.finditer(cleaned)):
            # The first term may omit a sign (defaulting to +). Subsequent
            # terms must have an explicit + or -.
            if match.start() != cursor:
                raise DiceError(
                    f"unparsable text in expression at offset {cursor}: "
                    f"{cleaned[cursor:match.start()]!r}"
                )
            sign_str = match.group("sign")
            if sign_str is None:
                if i != 0:
                    raise DiceError(
                        f"missing operator before term {match.group(0).strip()!r}"
                    )
                sign = 1
            else:
                sign = -1 if sign_str == "-" else 1

            if match.group("flat") is not None:
                flat = int(match.group("flat"))
                terms.append(Term(
                    expression=match.group(0).strip(),
                    sign=sign,
                    count=0, sides=0, keep=None, keep_n=0,
                    flat=flat, rolls=(), kept=(),
                    subtotal=sign * flat,
                ))
            else:
                count = int(match.group("count"))
                sides = int(match.group("sides"))
                keep_raw = match.group("keep")
                keep = keep_raw.lower() if keep_raw else None
                keep_n = int(match.group("keep_n")) if match.group("keep_n") else 0
                _validate_term(count, sides, keep, keep_n)

                if take_max:
                    rolls = tuple(sides for _ in range(count))
                else:
                    rolls = tuple(self.rng.randint(1, sides) for _ in range(count))
                if keep == "kh":
                    kept = tuple(sorted(rolls, reverse=True)[:keep_n])
                elif keep == "kl":
                    kept = tuple(sorted(rolls)[:keep_n])
                else:
                    kept = rolls
                subtotal = sign * sum(kept)
                terms.append(Term(
                    expression=match.group(0).strip(),
                    sign=sign,
                    count=count, sides=sides,
                    keep=keep, keep_n=keep_n,
                    flat=0, rolls=rolls, kept=kept,
                    subtotal=subtotal,
                ))

            cursor = match.end()

        if cursor != len(cleaned):
            raise DiceError(
                f"unparsable trailing text: {cleaned[cursor:]!r}"
            )
        if not terms:
            raise DiceError(f"no dice or numbers in expression: {expression!r}")

        total = sum(t.subtotal for t in terms)
        breakdown = _format_breakdown(terms, total)
        return RollResult(
            expression=cleaned,
            total=total,
            terms=tuple(terms),
            breakdown=breakdown,
        )


def _format_breakdown(terms: Iterable[Term], total: int) -> str:
    """Format a roll for human reading, e.g. ``[5,3,4]+2 = 14``."""
    parts: list[str] = []
    for i, t in enumerate(terms):
        if i == 0:
            prefix = "" if t.sign == 1 else "-"
        else:
            prefix = " + " if t.sign == 1 else " - "
        if t.rolls:
            inner = ",".join(str(r) for r in t.rolls)
            if t.kept != t.rolls:
                kept = ",".join(str(r) for r in t.kept)
                parts.append(f"{prefix}[{inner}]→keep[{kept}]")
            else:
                parts.append(f"{prefix}[{inner}]")
        else:
            parts.append(f"{prefix}{t.flat}")
    return "".join(parts) + f" = {total}"


def roll(expression: str, seed: int | None = None) -> RollResult:
    """One-shot convenience helper: roll an expression with an optional seed."""
    return Roller(seed=seed).roll(expression)
