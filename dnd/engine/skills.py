"""Skill check primitives.

PF1 skill checks are d20 + bonus vs DC. This module wraps the
combatant's ``skill_total`` with rules around take-10, trained-only
skills, opposed checks, and aid another.

The functions are pure (mutate nothing on the combatants) — they take a
``Roller`` and a ``ContentRegistry`` and return result records that
callers can interpret.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .combatant import Combatant
from .content import ContentRegistry
from .dice import Roller


class SkillCheckError(ValueError):
    """Raised when a skill check is requested in an invalid way."""


@dataclass
class SkillCheckResult:
    """Outcome of a single skill check.

    ``success`` is ``None`` when no DC was supplied (e.g., for opposed
    checks where the caller compares totals directly).

    ``blocked_trained_only`` is True when the actor lacks ranks in a
    trained-only skill — in that case ``natural`` and ``total`` are
    zero, ``success`` is False.
    """

    skill_id: str
    actor_id: str
    natural: int
    bonus: int
    total: int
    dc: int | None
    success: bool | None
    took_10: bool
    blocked_trained_only: bool = False
    log: list[str] = field(default_factory=list)


def cumulative_skill_ranks(actor: Combatant, skill_id: str) -> int:
    """Return the number of ranks the actor has invested in a skill.

    Reads the ``ranks``-sourced modifier(s) on the skill target. Returns
    0 if no ranks are recorded.
    """
    ranks = 0
    target = f"skill:{skill_id}"
    for m in actor.modifiers.for_target(target):
        if m.source == "ranks":
            ranks += m.value
    return ranks


def skill_check(
    actor: Combatant,
    skill_id: str,
    dc: int | None,
    roller: Roller,
    registry: ContentRegistry,
    *,
    take_10: bool = False,
    extra_bonus: int = 0,
) -> SkillCheckResult:
    """Roll (or take 10 on) a skill check.

    ``dc`` is the target DC for success/failure determination; pass
    ``None`` when the result will be compared against another roll
    (opposed checks).

    ``take_10`` substitutes 10 for the d20 roll. PF1 RAW forbids take 10
    in stressful situations / combat — enforcement is the caller's job.

    ``extra_bonus`` is a one-off bonus to add (e.g., +2 from a
    successful aid-another check).

    Trained-only skills with 0 ranks short-circuit to a failed result
    with ``blocked_trained_only=True``.
    """
    skill = registry.get_skill(skill_id)
    bonus = actor.skill_total(skill_id) + extra_bonus
    if skill.trained_only and cumulative_skill_ranks(actor, skill_id) <= 0:
        return SkillCheckResult(
            skill_id=skill_id, actor_id=actor.id,
            natural=0, bonus=bonus, total=0,
            dc=dc, success=False, took_10=False,
            blocked_trained_only=True,
            log=[f"trained-only skill {skill_id!r} blocked: 0 ranks"],
        )
    if take_10:
        natural = 10
    else:
        result = roller.roll("1d20")
        natural = result.terms[0].rolls[0]
    total = natural + bonus
    success: bool | None = (total >= dc) if dc is not None else None
    return SkillCheckResult(
        skill_id=skill_id, actor_id=actor.id,
        natural=natural, bonus=bonus, total=total,
        dc=dc, success=success, took_10=take_10,
    )


def opposed_skill_check(
    initiator: Combatant,
    opponent: Combatant,
    initiator_skill_id: str,
    opponent_skill_id: str,
    roller: Roller,
    registry: ContentRegistry,
) -> tuple[SkillCheckResult, SkillCheckResult, bool]:
    """Roll an opposed skill check.

    Returns ``(initiator_result, opponent_result, initiator_wins)``.
    Per PF1 RAW, ties go to the defender — the initiator must beat the
    opponent's total to win.
    """
    a = skill_check(initiator, initiator_skill_id, None, roller, registry)
    b = skill_check(opponent, opponent_skill_id, None, roller, registry)
    initiator_wins = a.total > b.total
    return a, b, initiator_wins


def aid_another_skill(
    aider: Combatant,
    skill_id: str,
    roller: Roller,
    registry: ContentRegistry,
) -> tuple[SkillCheckResult, int]:
    """PF1 aid-another for skills: DC 10 check; +2 circumstance bonus to
    target's next check on success.

    Returns ``(aider_result, bonus_granted)`` — the bonus is 0 or 2.
    Callers pass the bonus into the target's subsequent ``skill_check``
    via ``extra_bonus``.
    """
    result = skill_check(aider, skill_id, 10, roller, registry)
    return result, (2 if result.success else 0)
