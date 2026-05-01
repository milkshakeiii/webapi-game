"""Level-up plans.

A ``LevelUpPlan`` pre-commits a hero's progression from level 2 to a
target level. The validator checks each entry's legality at submission
time so the patron knows upfront if their build is impossible. The
applicator walks the plan and produces a multi-level character sheet.

Per-level decisions captured:

- ``class_id`` — the class taken this level (multiclassing supported).
- ``hp_method`` — ``"max"`` / ``"fixed_half"`` / ``"rolled"``.
- ``skill_ranks`` — *additional* ranks allocated this level (deltas, not
  cumulative).
- ``feat_general`` — chosen feat at every odd level.
- ``feat_class_bonus`` — chosen class-bonus feat at class-specific levels
  (fighter every even level, monk L1/2/6/etc., wizard L5/10/15/20).
- ``ability_bump`` — ability key (``"str"``..``"cha"``) at L4/8/12/16/20.
- ``class_choices`` — class-specific picks (rogue talent, mercy, etc.).
- ``spells_known_added`` — for sorcerer/bard at this level.
- ``spellbook_added`` — for wizard at this level.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class LevelPlanError(ValueError):
    """Raised when a LevelUpPlan is invalid for the given hero."""


@dataclass(frozen=True)
class LevelEntry:
    class_id: str
    hp_method: str = "fixed_half"
    skill_ranks: dict[str, int] = field(default_factory=dict)
    feat_general: str | None = None
    feat_class_bonus: str | None = None
    ability_bump: str | None = None
    class_choices: dict[str, Any] = field(default_factory=dict)
    spells_known_added: list[str] = field(default_factory=list)
    spellbook_added: list[str] = field(default_factory=list)
    hp_roll: int | None = None    # used when hp_method == "rolled"; pre-rolled at plan submit

    @classmethod
    def from_dict(cls, d: dict) -> LevelEntry:
        if not isinstance(d, dict):
            raise LevelPlanError(f"level entry must be an object, got {type(d).__name__}")
        return cls(
            class_id=str(d["class"]),
            hp_method=str(d.get("hp_method", "fixed_half")),
            skill_ranks=dict(d.get("skill_ranks") or {}),
            feat_general=d.get("feat_general"),
            feat_class_bonus=d.get("feat_class_bonus"),
            ability_bump=d.get("ability_bump"),
            class_choices=dict(d.get("class_choices") or {}),
            spells_known_added=list(d.get("spells_known_added") or []),
            spellbook_added=list(d.get("spellbook_added") or []),
            hp_roll=d.get("hp_roll"),
        )

    def to_dict(self) -> dict:
        return {
            "class": self.class_id,
            "hp_method": self.hp_method,
            "skill_ranks": dict(self.skill_ranks),
            "feat_general": self.feat_general,
            "feat_class_bonus": self.feat_class_bonus,
            "ability_bump": self.ability_bump,
            "class_choices": dict(self.class_choices),
            "spells_known_added": list(self.spells_known_added),
            "spellbook_added": list(self.spellbook_added),
            "hp_roll": self.hp_roll,
        }


@dataclass
class LevelUpPlan:
    name: str
    target_level: int
    levels: dict[int, LevelEntry]    # keys 2..target_level

    @classmethod
    def from_dict(cls, d: dict) -> LevelUpPlan:
        if not isinstance(d, dict):
            raise LevelPlanError("plan must be an object")
        target = int(d.get("target_level", 1))
        if target < 1 or target > 20:
            raise LevelPlanError(f"target_level {target} out of range 1..20")
        levels: dict[int, LevelEntry] = {}
        raw_levels = d.get("levels") or {}
        if not isinstance(raw_levels, dict):
            raise LevelPlanError("'levels' must be a mapping of level → entry")
        for k, v in raw_levels.items():
            try:
                ki = int(k)
            except (ValueError, TypeError):
                raise LevelPlanError(f"level key {k!r} is not an integer")
            if ki < 2 or ki > target:
                raise LevelPlanError(
                    f"level {ki} out of range 2..{target}"
                )
            levels[ki] = LevelEntry.from_dict(v)
        # All levels 2..target must be present.
        for L in range(2, target + 1):
            if L not in levels:
                raise LevelPlanError(f"plan missing entry for level {L}")
        return cls(
            name=str(d.get("name", "<unnamed>")),
            target_level=target,
            levels=levels,
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "target_level": self.target_level,
            "levels": {str(L): e.to_dict() for L, e in self.levels.items()},
        }
