"""Carrying capacity and load-category penalties.

PF1 RAW: each Strength score has a heavy-load weight. Light load is
heavy/3, medium load is heavy*2/3. Carrying medium or heavy load
imposes the same Max Dex Bonus, armor check penalty, and speed
reduction as wearing the matching armor category.

For v1 we model:
- carried weight (sum of equipped weapon, off-hand weapon, armor, shield)
- load category (light / medium / heavy / overloaded)
- penalties: armor check penalty stacking with armor's ACP, applied
  to ACP-affected skills.

Speed reduction and Max-Dex caps from encumbrance are NOT yet wired —
documented in the coverage table.
"""

from __future__ import annotations


# Heavy-load capacity by Strength score (PF1 SRD table). Index 0 is a
# placeholder for Str 0 (an undefined score). Values for Str 1–29 cover
# the practical PC/NPC range; Str ≥ 30 uses the doubling-by-10 rule.
_HEAVY_LOAD_LB: tuple[int, ...] = (
    0,         # 0 (undefined; treated as overloaded)
    10, 20, 30, 40, 50, 60, 70, 80, 90, 100,        # 1–10
    115, 130, 150, 175, 200, 230, 260, 300, 350, 400,  # 11–20
    460, 520, 600, 700, 800, 920, 1040, 1200, 1400, 1600,  # 21–30
)


def heavy_load_for(str_score: int) -> int:
    """Return the heavy-load weight (lb) for the given Strength score.

    Below Str 1 the creature can't lift anything (0). For Str above 30,
    PF1 RAW says every +10 points multiplies by 4.
    """
    if str_score <= 0:
        return 0
    if str_score < len(_HEAVY_LOAD_LB):
        return _HEAVY_LOAD_LB[str_score]
    over = str_score - 30
    multiplier = 4 ** (over // 10)
    return _HEAVY_LOAD_LB[30] * multiplier


def load_category(weight: float, str_score: int) -> str:
    """Return one of ``light``, ``medium``, ``heavy``, ``overloaded``."""
    heavy = heavy_load_for(str_score)
    if heavy <= 0:
        return "overloaded"
    light_max = heavy / 3.0
    medium_max = heavy * 2.0 / 3.0
    if weight > heavy:
        return "overloaded"
    if weight > medium_max:
        return "heavy"
    if weight > light_max:
        return "medium"
    return "light"


def carried_weight(character, registry) -> float:
    """Sum the weight of the character's equipped gear.

    Pure helper: doesn't read inventory or other carried items, just
    the four gear slots tracked on the Character (weapon, off-hand,
    armor, shield).
    """
    total = 0.0
    if character.equipped_weapon:
        total += float(registry.get_weapon(character.equipped_weapon).weight)
    off = getattr(character, "equipped_offhand_weapon", None)
    if off and off != "none":
        total += float(registry.get_weapon(off).weight)
    armor_id = character.equipped_armor
    if armor_id and armor_id != "none":
        total += float(registry.get_armor(armor_id).weight)
    if character.equipped_shield:
        total += float(registry.get_shield(character.equipped_shield).weight)
    return total


# PF1 RAW: medium load = -3 ACP and max Dex +3; heavy load = -6 ACP
# and max Dex +1 (matches medium / heavy armor profile).
LOAD_ACP_PENALTY: dict[str, int] = {
    "light":      0,
    "medium":     -3,
    "heavy":      -6,
    "overloaded": -6,  # treat as heavy until movement-impossibility wires up
}


LOAD_MAX_DEX: dict[str, int | None] = {
    "light":      None,
    "medium":     3,
    "heavy":      1,
    "overloaded": 0,
}


# PF1 RAW: medium / heavy load reduces speed exactly the same way
# medium / heavy armor does — a fixed table from base speed to reduced
# speed.
_REDUCED_SPEED_TABLE: dict[int, int] = {
    5:  5,
    10: 5,
    15: 10,
    20: 15,
    25: 15,
    30: 20,
    35: 25,
    40: 30,
    45: 30,
    50: 35,
    60: 40,
    70: 45,
    80: 50,
    90: 60,
}


def reduced_speed(base: int) -> int:
    """Return PF1 medium-/heavy-armor (== medium/heavy load) reduced speed."""
    if base <= 0:
        return 0
    return _REDUCED_SPEED_TABLE.get(base, max(5, (base // 15) * 10))


def effective_speed(base: int, armor_data, load: str) -> int:
    """Combine race speed with armor speed and encumbrance speed.

    Per PF1 RAW: ``your speed decreases according to your armor or
    load, whichever is worse``. We apply the reduction once if either
    medium/heavy armor OR medium/heavy load is present (taking the
    minimum of the two reductions).
    """
    speed = base
    armor_reduces = False
    if armor_data is not None:
        cat = (getattr(armor_data, "category", "") or "").lower()
        if cat in ("medium", "heavy"):
            armor_reduces = True
    load_reduces = load in ("medium", "heavy", "overloaded")
    if armor_reduces or load_reduces:
        speed = reduced_speed(speed)
    return speed
