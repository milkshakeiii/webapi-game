"""PF1 class progression formulas and tables.

BAB and saves follow simple formulas based on the class's progression
type (full/three-quarters/half for BAB; good/poor for each save).
Spell slot progression is tabular — each caster class has a per-level
table of spells per day at each spell level.

Class features per level live in ``content/classes/*.json`` under
``features_by_level``. This module just provides the math.
"""

from __future__ import annotations

from typing import Any


# ---------------------------------------------------------------------------
# BAB
# ---------------------------------------------------------------------------


def bab_at(progression: str, level: int) -> int:
    """PF1 BAB by progression type."""
    if level < 1:
        return 0
    if progression == "full":
        return level
    if progression == "three_quarters":
        return (level * 3) // 4
    if progression == "half":
        return level // 2
    raise ValueError(f"unknown bab_progression {progression!r}")


def iterative_attacks(bab: int) -> list[int]:
    """The list of iterative attack bonuses given a total BAB.

    +6 BAB → [+6, +1]; +11 BAB → [+11, +6, +1]; etc.
    """
    if bab < 6:
        return [bab]
    out: list[int] = []
    cur = bab
    while cur > 0:
        out.append(cur)
        cur -= 5
    return out


# ---------------------------------------------------------------------------
# Saves
# ---------------------------------------------------------------------------


def save_base_at(track: str, level: int) -> int:
    """PF1 base save by progression track."""
    if level < 1:
        return 0
    if track == "good":
        return level // 2 + 2
    if track == "poor":
        return level // 3
    raise ValueError(f"unknown save track {track!r}")


# ---------------------------------------------------------------------------
# Spell slot progression tables
# ---------------------------------------------------------------------------


# Each entry is a class progression: maps class_level (1-20) to a dict
# spell_level (str: "0".."9") -> int slots OR "at_will" for cantrips.
#
# These are the "spells per day" tables from the Core Rulebook
# (excluding bonus slots from key ability score and excluding domain
# / specialist-school slots, which are added separately).


def _full_caster_prepared_table() -> dict[int, dict[str, Any]]:
    """Prepared casters with full progression: cleric, druid, wizard."""
    table: dict[int, dict[str, Any]] = {}
    # Reference table from PF1 CRB.
    # spell_levels available: 0=cantrips, 1-9=spells.
    # Format: (cantrips, lvl1, lvl2, lvl3, lvl4, lvl5, lvl6, lvl7, lvl8, lvl9)
    rows = {
        1:  (3, 1, 0, 0, 0, 0, 0, 0, 0, 0),
        2:  (4, 2, 0, 0, 0, 0, 0, 0, 0, 0),
        3:  (4, 2, 1, 0, 0, 0, 0, 0, 0, 0),
        4:  (4, 3, 2, 0, 0, 0, 0, 0, 0, 0),
        5:  (4, 3, 2, 1, 0, 0, 0, 0, 0, 0),
        6:  (4, 3, 3, 2, 0, 0, 0, 0, 0, 0),
        7:  (4, 4, 3, 2, 1, 0, 0, 0, 0, 0),
        8:  (4, 4, 3, 3, 2, 0, 0, 0, 0, 0),
        9:  (4, 4, 4, 3, 2, 1, 0, 0, 0, 0),
        10: (4, 4, 4, 3, 3, 2, 0, 0, 0, 0),
        11: (4, 5, 4, 4, 3, 2, 1, 0, 0, 0),
        12: (4, 5, 4, 4, 3, 3, 2, 0, 0, 0),
        13: (4, 5, 5, 4, 4, 3, 2, 1, 0, 0),
        14: (4, 5, 5, 4, 4, 3, 3, 2, 0, 0),
        15: (4, 5, 5, 5, 4, 4, 3, 2, 1, 0),
        16: (4, 5, 5, 5, 4, 4, 3, 3, 2, 0),
        17: (4, 5, 5, 5, 5, 4, 4, 3, 2, 1),
        18: (4, 5, 5, 5, 5, 4, 4, 3, 3, 2),
        19: (4, 5, 5, 5, 5, 5, 4, 4, 3, 3),
        20: (4, 5, 5, 5, 5, 5, 4, 4, 4, 4),
    }
    for lvl, slots in rows.items():
        table[lvl] = {str(i): slots[i] for i in range(10)}
    return table


def _full_caster_spontaneous_table() -> dict[int, dict[str, Any]]:
    """Sorcerer / oracle: spontaneous full caster (one level slower than wizard)."""
    table: dict[int, dict[str, Any]] = {}
    rows = {
        1:  ("at_will", 3, 0, 0, 0, 0, 0, 0, 0, 0),
        2:  ("at_will", 4, 0, 0, 0, 0, 0, 0, 0, 0),
        3:  ("at_will", 5, 0, 0, 0, 0, 0, 0, 0, 0),
        4:  ("at_will", 6, 3, 0, 0, 0, 0, 0, 0, 0),
        5:  ("at_will", 6, 4, 0, 0, 0, 0, 0, 0, 0),
        6:  ("at_will", 6, 5, 3, 0, 0, 0, 0, 0, 0),
        7:  ("at_will", 6, 6, 4, 0, 0, 0, 0, 0, 0),
        8:  ("at_will", 6, 6, 5, 3, 0, 0, 0, 0, 0),
        9:  ("at_will", 6, 6, 6, 4, 0, 0, 0, 0, 0),
        10: ("at_will", 6, 6, 6, 5, 3, 0, 0, 0, 0),
        11: ("at_will", 6, 6, 6, 6, 4, 0, 0, 0, 0),
        12: ("at_will", 6, 6, 6, 6, 5, 3, 0, 0, 0),
        13: ("at_will", 6, 6, 6, 6, 6, 4, 0, 0, 0),
        14: ("at_will", 6, 6, 6, 6, 6, 5, 3, 0, 0),
        15: ("at_will", 6, 6, 6, 6, 6, 6, 4, 0, 0),
        16: ("at_will", 6, 6, 6, 6, 6, 6, 5, 3, 0),
        17: ("at_will", 6, 6, 6, 6, 6, 6, 6, 4, 0),
        18: ("at_will", 6, 6, 6, 6, 6, 6, 6, 5, 3),
        19: ("at_will", 6, 6, 6, 6, 6, 6, 6, 6, 4),
        20: ("at_will", 6, 6, 6, 6, 6, 6, 6, 6, 6),
    }
    for lvl, slots in rows.items():
        table[lvl] = {str(i): slots[i] for i in range(10)}
    return table


def _sorcerer_spells_known_table() -> dict[int, dict[str, int]]:
    rows = {
        1:  (4, 2, 0, 0, 0, 0, 0, 0, 0, 0),
        2:  (5, 2, 0, 0, 0, 0, 0, 0, 0, 0),
        3:  (5, 3, 0, 0, 0, 0, 0, 0, 0, 0),
        4:  (6, 3, 1, 0, 0, 0, 0, 0, 0, 0),
        5:  (6, 4, 2, 0, 0, 0, 0, 0, 0, 0),
        6:  (7, 4, 2, 1, 0, 0, 0, 0, 0, 0),
        7:  (7, 5, 3, 2, 0, 0, 0, 0, 0, 0),
        8:  (8, 5, 3, 2, 1, 0, 0, 0, 0, 0),
        9:  (8, 5, 4, 3, 2, 0, 0, 0, 0, 0),
        10: (9, 5, 4, 3, 2, 1, 0, 0, 0, 0),
        11: (9, 5, 5, 4, 3, 2, 0, 0, 0, 0),
        12: (9, 5, 5, 4, 3, 2, 1, 0, 0, 0),
        13: (9, 5, 5, 4, 4, 3, 2, 0, 0, 0),
        14: (9, 5, 5, 4, 4, 3, 2, 1, 0, 0),
        15: (9, 5, 5, 4, 4, 4, 3, 2, 0, 0),
        16: (9, 5, 5, 4, 4, 4, 3, 2, 1, 0),
        17: (9, 5, 5, 4, 4, 4, 3, 3, 2, 0),
        18: (9, 5, 5, 4, 4, 4, 3, 3, 2, 1),
        19: (9, 5, 5, 4, 4, 4, 3, 3, 3, 2),
        20: (9, 5, 5, 4, 4, 4, 3, 3, 3, 3),
    }
    return {lvl: {str(i): row[i] for i in range(10)} for lvl, row in rows.items()}


def _bard_spells_per_day_table() -> dict[int, dict[str, Any]]:
    """Bard: 2/3-progression spontaneous caster, max 6th-level spells."""
    rows = {
        1:  ("at_will", 1, 0, 0, 0, 0, 0),
        2:  ("at_will", 2, 0, 0, 0, 0, 0),
        3:  ("at_will", 3, 0, 0, 0, 0, 0),
        4:  ("at_will", 3, 1, 0, 0, 0, 0),
        5:  ("at_will", 4, 2, 0, 0, 0, 0),
        6:  ("at_will", 4, 3, 0, 0, 0, 0),
        7:  ("at_will", 4, 3, 1, 0, 0, 0),
        8:  ("at_will", 4, 4, 2, 0, 0, 0),
        9:  ("at_will", 5, 4, 3, 0, 0, 0),
        10: ("at_will", 5, 4, 3, 1, 0, 0),
        11: ("at_will", 5, 4, 4, 2, 0, 0),
        12: ("at_will", 5, 5, 4, 3, 0, 0),
        13: ("at_will", 5, 5, 4, 3, 1, 0),
        14: ("at_will", 5, 5, 4, 4, 2, 0),
        15: ("at_will", 5, 5, 5, 4, 3, 0),
        16: ("at_will", 5, 5, 5, 4, 3, 1),
        17: ("at_will", 5, 5, 5, 4, 4, 2),
        18: ("at_will", 5, 5, 5, 5, 4, 3),
        19: ("at_will", 5, 5, 5, 5, 5, 4),
        20: ("at_will", 5, 5, 5, 5, 5, 5),
    }
    return {lvl: {str(i): row[i] for i in range(7)} for lvl, row in rows.items()}


def _bard_spells_known_table() -> dict[int, dict[str, int]]:
    rows = {
        1:  (4, 2, 0, 0, 0, 0, 0),
        2:  (5, 3, 0, 0, 0, 0, 0),
        3:  (6, 4, 0, 0, 0, 0, 0),
        4:  (6, 4, 2, 0, 0, 0, 0),
        5:  (6, 4, 3, 0, 0, 0, 0),
        6:  (6, 4, 4, 0, 0, 0, 0),
        7:  (6, 5, 4, 2, 0, 0, 0),
        8:  (6, 5, 4, 3, 0, 0, 0),
        9:  (6, 5, 5, 4, 0, 0, 0),
        10: (6, 5, 5, 4, 2, 0, 0),
        11: (6, 6, 5, 4, 3, 0, 0),
        12: (6, 6, 5, 5, 4, 0, 0),
        13: (6, 6, 6, 5, 4, 2, 0),
        14: (6, 6, 6, 5, 4, 3, 0),
        15: (6, 6, 6, 5, 5, 4, 0),
        16: (6, 6, 6, 6, 5, 4, 2),
        17: (6, 6, 6, 6, 5, 4, 3),
        18: (6, 6, 6, 6, 5, 5, 4),
        19: (6, 6, 6, 6, 6, 5, 4),
        20: (6, 6, 6, 6, 6, 5, 5),
    }
    return {lvl: {str(i): row[i] for i in range(7)} for lvl, row in rows.items()}


def _quarter_caster_table() -> dict[int, dict[str, Any]]:
    """Paladin / ranger: starts at L4, max 4th-level spells."""
    rows = {
        # No spells L1-3.
        4:  (0, 0, 0, 0, 0),
        5:  (0, 1, 0, 0, 0),
        6:  (0, 1, 0, 0, 0),
        7:  (0, 1, 0, 0, 0),
        8:  (0, 1, 1, 0, 0),
        9:  (0, 2, 1, 0, 0),
        10: (0, 2, 1, 0, 0),
        11: (0, 2, 1, 1, 0),
        12: (0, 2, 2, 1, 0),
        13: (0, 3, 2, 1, 0),
        14: (0, 3, 2, 1, 1),
        15: (0, 3, 2, 2, 1),
        16: (0, 3, 3, 2, 1),
        17: (0, 4, 3, 2, 1),
        18: (0, 4, 3, 2, 2),
        19: (0, 4, 3, 3, 3),
        20: (0, 4, 4, 3, 3),
    }
    out: dict[int, dict[str, Any]] = {}
    for lvl in range(1, 21):
        if lvl not in rows:
            out[lvl] = {}
        else:
            row = rows[lvl]
            out[lvl] = {str(i): row[i] for i in range(5)}
    return out


# Cached tables.
PROGRESSION_TABLES: dict[str, dict[int, dict[str, Any]]] = {
    "full_caster_prepared":    _full_caster_prepared_table(),
    "full_caster_spontaneous": _full_caster_spontaneous_table(),
    "bard":                    _bard_spells_per_day_table(),
    "quarter_caster":          _quarter_caster_table(),
}

SPELLS_KNOWN_TABLES: dict[str, dict[int, dict[str, int]]] = {
    "sorcerer": _sorcerer_spells_known_table(),
    "bard":     _bard_spells_known_table(),
}


# Map class id → table key for spells per day.
CLASS_SPELL_PROGRESSION: dict[str, str] = {
    "cleric":   "full_caster_prepared",
    "druid":    "full_caster_prepared",
    "wizard":   "full_caster_prepared",
    "sorcerer": "full_caster_spontaneous",
    "bard":     "bard",
    "paladin":  "quarter_caster",
    "ranger":   "quarter_caster",
}


def spells_per_day_at(class_id: str, level: int) -> dict[str, Any]:
    """Base spells per day for a class at a given level (no bonus slots)."""
    key = CLASS_SPELL_PROGRESSION.get(class_id)
    if key is None:
        return {}
    return dict(PROGRESSION_TABLES[key].get(level, {}))


def spells_known_at(class_id: str, level: int) -> dict[str, int]:
    """Spells known for a spontaneous caster at a given level."""
    key = "sorcerer" if class_id == "sorcerer" else (
        "bard" if class_id == "bard" else None
    )
    if key is None:
        return {}
    return dict(SPELLS_KNOWN_TABLES[key].get(level, {}))


# ---------------------------------------------------------------------------
# Bonus spells from key ability score (PF1 CRB Table 1-3)
# ---------------------------------------------------------------------------


def bonus_spells_per_day(score: int) -> dict[str, int]:
    """Return extra spell slots granted by a key ability score.

    PF1 CRB Table 1-3: bonus slots at spell level N depend on the
    ability *modifier* (not the raw score). Specifically:

        bonus(N) = (mod - N) // 4 + 1   when mod >= N
                 = 0                    when mod < N
    """
    mod_value = (score - 10) // 2
    out: dict[str, int] = {}
    for spell_level in range(1, 10):
        if mod_value < spell_level:
            break
        out[str(spell_level)] = (mod_value - spell_level) // 4 + 1
    return out


# ---------------------------------------------------------------------------
# General-feat / ability-bump schedule
# ---------------------------------------------------------------------------


def general_feat_levels(target_level: int) -> list[int]:
    """Levels at which a general feat is granted (every odd level)."""
    return [L for L in range(1, target_level + 1) if L % 2 == 1]


def ability_bump_levels(target_level: int) -> list[int]:
    """Levels at which a +1 to one ability score is granted."""
    return [L for L in range(4, target_level + 1, 4)]
