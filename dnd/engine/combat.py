"""Stateless combat math primitives.

Pure functions that take attacker/defender profiles and a seeded ``Roller``
and return structured attack outcomes. No notion of turns, action economy,
encounters, or behavior scripts in this module — those layers sit on top.

Everything is deterministic given the same RNG state, including critical
threat confirmation rolls.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .dice import Roller


# ---------------------------------------------------------------------------
# Profiles
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AttackProfile:
    """All inputs needed to make a single attack roll.

    ``attack_bonus`` is the *final* bonus including BAB, ability modifier,
    size modifier, weapon focus, magic enhancement, etc. The combat module
    does not break it down — that's the job of the layer that constructs
    the profile.

    ``precision_damage_dice`` (e.g. ``"3d6"``) is added on hit but does
    NOT multiply on a crit (PF1 RAW). Used for Sneak Attack and similar
    precision sources. Empty string means no precision damage.
    """

    attack_bonus: int
    damage_dice: str          # e.g., "1d8", "2d4", "1d6"
    damage_bonus: int         # ability + magic + situational
    crit_range: tuple[int, int]
    crit_multiplier: int
    damage_type: str = ""     # e.g., "S", "P", "B", "P/S", "B/P/S"
    name: str = ""            # display label, e.g., "longsword"
    precision_damage_dice: str = ""


@dataclass(frozen=True)
class DefenseProfile:
    """All inputs needed to evaluate a single attack against a defender."""

    ac: int                                 # full AC
    touch_ac: int                           # touch AC (no armor/shield/natural)
    flat_footed_ac: int                     # flat-footed AC (no Dex)
    dr: tuple[int, frozenset[str]] | None = None
    """Damage reduction: (amount, bypass-keywords). e.g., (5, frozenset({"slashing"}))."""


# ---------------------------------------------------------------------------
# Outcome
# ---------------------------------------------------------------------------


@dataclass
class AttackOutcome:
    """Result of a single attack resolution."""

    hit: bool
    crit: bool
    natural_1: bool
    natural_20: bool

    attack_natural: int       # the d20 roll
    attack_total: int         # natural + bonus
    target_ac: int

    threatened: bool          # did the natural fall in the crit range?
    confirm_natural: int | None
    confirm_total: int | None

    damage: int               # final damage applied (0 if miss)
    damage_dealt_pre_dr: int
    dr_absorbed: int

    log: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ac_for_situation(defense: DefenseProfile, situation: str) -> int:
    if situation == "normal":
        return defense.ac
    if situation == "touch":
        return defense.touch_ac
    if situation == "flat_footed":
        return defense.flat_footed_ac
    raise ValueError(f"unknown ac situation {situation!r}; expected normal/touch/flat_footed")


def _bypass_dr(damage_type: str, bypass) -> bool:
    """Does ``damage_type`` bypass the listed DR keywords?

    DR-bypass keywords use full words ("slashing", "piercing",
    "bludgeoning", "magic", "silver", "cold_iron", "adamantine",
    "good", "lawful", "epic", etc). Damage-type strings use
    abbreviations ("S", "P", "B") and may include multiple options
    separated by '/'.

    Two shapes are accepted for backwards compatibility:

    - **flat OR-set** (legacy): a single ``frozenset`` / iterable of
      keywords. Bypass succeeds if ANY damage-type matches ANY keyword.
      Used for simple DR like "DR 10/silver" or "DR 10/silver or magic".

    - **AND of OR-groups**: a tuple/list of frozensets, each an
      OR-group. Bypass succeeds only when EVERY group is matched by
      some damage-type. Used for "DR 10/silver and magic" → the
      attack must be silver AND magic to bypass.

    Detection: if ``bypass`` is empty, treat as flat. Otherwise, look
    at the first element — if it's a string, this is a flat set; if
    it's an iterable of strings, this is the AND form.
    """
    type_map = {"S": "slashing", "P": "piercing", "B": "bludgeoning"}
    types = {type_map.get(t.strip(), t.strip().lower()) for t in damage_type.split("/")}
    if not bypass:
        return False
    # Detect shape.
    bypass_list = list(bypass)
    if isinstance(bypass_list[0], str):
        # Flat OR-set — legacy shape.
        return bool(types & {s.lower() for s in bypass_list})
    # AND-of-OR-groups: each element is an iterable of keywords.
    for group in bypass_list:
        group_set = {s.lower() for s in group}
        if not (types & group_set):
            return False
    return True


def _apply_dr(damage: int, defense: DefenseProfile, damage_type: str) -> tuple[int, int]:
    """Return ``(final_damage, absorbed)`` after applying any DR."""
    if damage <= 0 or defense.dr is None:
        return max(0, damage), 0
    amount, bypass = defense.dr
    if _bypass_dr(damage_type, bypass):
        return damage, 0
    absorbed = min(amount, damage)
    return damage - absorbed, absorbed


# ---------------------------------------------------------------------------
# Attack roll
# ---------------------------------------------------------------------------


def attack_roll(roller: Roller, attack_bonus: int) -> tuple[int, int]:
    """Roll d20 + bonus. Returns (natural, total)."""
    r = roller.roll("1d20")
    natural = r.terms[0].rolls[0]
    return natural, natural + attack_bonus


def damage_roll(
    roller: Roller,
    dice: str,
    bonus: int,
    crit_dice_count: int = 1,
) -> tuple[int, list[int]]:
    """Roll weapon damage. ``crit_dice_count`` multiplies the dice (and the
    bonus, except for non-multiplying mods which we don't yet model).

    Returns ``(total, individual_die_rolls)``.

    For x2 crit pass ``crit_dice_count=2``; x3 crit pass 3; etc. PF1 doubles
    the *dice* and the *static bonus*. (Precision damage like sneak attack
    does NOT multiply, but Phase 2 doesn't model precision damage yet.)
    """
    if crit_dice_count < 1:
        raise ValueError(f"crit_dice_count must be >= 1, got {crit_dice_count}")
    individual: list[int] = []
    total = 0
    for _ in range(crit_dice_count):
        r = roller.roll(dice)
        # Sum the rolls (not the modifiers — the dice expression here is
        # expected to be just dice, e.g. "1d8", not "1d8+3").
        for term in r.terms:
            if term.rolls:
                individual.extend(term.kept)
                total += sum(term.kept)
    flat_bonus_total = bonus * crit_dice_count
    return total + flat_bonus_total, individual


# ---------------------------------------------------------------------------
# resolve_attack
# ---------------------------------------------------------------------------


def resolve_attack(
    attack: AttackProfile,
    defense: DefenseProfile,
    roller: Roller,
    situation: str = "normal",
) -> AttackOutcome:
    """Resolve a single PF1 attack.

    Steps:
        1. Roll d20 + attack bonus. Natural 1 auto-misses; natural 20 auto-hits.
        2. Compare to AC for the chosen ``situation``.
        3. If attack roll is in the weapon's crit range, threaten a crit:
           roll a confirmation. If the confirmation also hits AC, it's a crit.
        4. Roll damage. On a crit, multiply dice and static bonus by the
           weapon's crit multiplier.
        5. Apply DR according to damage type and bypass keywords.
    """
    target_ac = _ac_for_situation(defense, situation)
    log: list[str] = []

    nat, total = attack_roll(roller, attack.attack_bonus)
    log.append(
        f"attack {attack.name or 'weapon'}: d20={nat} + {attack.attack_bonus} = {total} vs AC {target_ac}"
    )

    is_nat_1 = (nat == 1)
    is_nat_20 = (nat == 20)
    if is_nat_1:
        log.append("natural 1 — automatic miss")
        return AttackOutcome(
            hit=False, crit=False,
            natural_1=True, natural_20=False,
            attack_natural=nat, attack_total=total, target_ac=target_ac,
            threatened=False, confirm_natural=None, confirm_total=None,
            damage=0, damage_dealt_pre_dr=0, dr_absorbed=0, log=log,
        )

    auto_hit = is_nat_20
    hit = auto_hit or (total >= target_ac)
    crit_low, crit_high = attack.crit_range
    threatened = (crit_low <= nat <= crit_high) and hit

    confirm_nat: int | None = None
    confirm_total: int | None = None
    crit = False
    if threatened:
        confirm_nat, confirm_total = attack_roll(roller, attack.attack_bonus)
        log.append(
            f"crit threat — confirm: d20={confirm_nat} + {attack.attack_bonus} "
            f"= {confirm_total} vs AC {target_ac}"
        )
        crit = (confirm_nat != 1) and (confirm_nat == 20 or confirm_total >= target_ac)
        if crit:
            log.append(f"confirmed (x{attack.crit_multiplier})")
        else:
            log.append("confirmation failed")

    if not hit:
        log.append("miss")
        return AttackOutcome(
            hit=False, crit=False,
            natural_1=False, natural_20=False,
            attack_natural=nat, attack_total=total, target_ac=target_ac,
            threatened=threatened, confirm_natural=confirm_nat, confirm_total=confirm_total,
            damage=0, damage_dealt_pre_dr=0, dr_absorbed=0, log=log,
        )

    multiplier = attack.crit_multiplier if crit else 1
    raw_damage, individual = damage_roll(
        roller, attack.damage_dice, attack.damage_bonus, crit_dice_count=multiplier
    )
    raw_damage = max(1, raw_damage)  # PF1: a successful hit always deals at least 1 damage.
    log.append(
        f"damage: dice={attack.damage_dice}x{multiplier} bonus=+{attack.damage_bonus*multiplier} "
        f"rolls={individual} → {raw_damage}"
    )

    # Precision damage (e.g., Sneak Attack). Rolled separately, NEVER
    # multiplied on a crit, added to total damage.
    if attack.precision_damage_dice:
        pdmg, pdice = damage_roll(
            roller, attack.precision_damage_dice, 0, crit_dice_count=1,
        )
        log.append(
            f"precision: dice={attack.precision_damage_dice} rolls={pdice} → {pdmg}"
        )
        raw_damage += pdmg

    final_damage, absorbed = _apply_dr(raw_damage, defense, attack.damage_type)
    if absorbed:
        log.append(f"DR absorbed {absorbed}")

    return AttackOutcome(
        hit=True, crit=crit,
        natural_1=False, natural_20=is_nat_20,
        attack_natural=nat, attack_total=total, target_ac=target_ac,
        threatened=threatened, confirm_natural=confirm_nat, confirm_total=confirm_total,
        damage=final_damage,
        damage_dealt_pre_dr=raw_damage,
        dr_absorbed=absorbed,
        log=log,
    )


# ---------------------------------------------------------------------------
# Convenience: build an AttackProfile from a monster's attack dict
# ---------------------------------------------------------------------------


def attack_profile_from_monster_attack(d: dict) -> AttackProfile:
    """Convert one entry from ``Monster.attacks`` into an ``AttackProfile``.

    Accepts strings of the form ``"1d6+1"`` for damage and splits into dice
    and bonus.
    """
    dmg = d["damage"]
    dice, bonus = _split_damage_string(dmg)
    crit_range = d.get("crit_range") or [20, 20]
    return AttackProfile(
        attack_bonus=int(d["attack_bonus"]),
        damage_dice=dice,
        damage_bonus=bonus,
        crit_range=(int(crit_range[0]), int(crit_range[1])),
        crit_multiplier=int(d.get("crit_multiplier", 2)),
        damage_type=str(d.get("damage_type", "")),
        name=str(d.get("name", "")),
    )


def _split_damage_string(s: str) -> tuple[str, int]:
    """Split ``"1d6+1"`` → (``"1d6"``, ``1``). Negative bonuses too."""
    s = s.replace(" ", "")
    # Find the first +/- after a 'd'.
    after_dice = s.find("d")
    if after_dice == -1:
        # Just a flat number (rare for weapon damage but allowed).
        return "0d1", int(s)
    # Look for + or - after the dice expression.
    sign_pos = -1
    for i in range(after_dice + 1, len(s)):
        if s[i] in "+-":
            sign_pos = i
            break
    if sign_pos == -1:
        return s, 0
    return s[:sign_pos], int(s[sign_pos:])
