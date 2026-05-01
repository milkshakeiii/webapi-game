"""Walk a LevelUpPlan and produce cumulative character state at a level.

For a character at ``target_level``, compute:

- Total class levels (per class id, for multiclass support).
- BAB summed across class levels.
- Save bases summed across class levels.
- Total HP from HD + Con + chosen hp_method per level.
- Cumulative skill ranks per skill (with budget validation).
- All feats earned (general at every odd level, plus class-bonus and
  racial bonus feats).
- Ability bumps applied at L4/8/12/16/20.
- Spell slots and spells-known progressions.
- Class features acquired at each level.

Validation surface is incomplete — high-leverage checks (feat
prerequisites against running ability scores, skill rank max, ability
bump only at allowed levels) are enforced; finer-grained PF1 rules
(multiclass alignment shifts, archetype trades, prestige class
requirements) are out of scope for v1.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .characters import (
    AbilityScores,
    apply_racial_modifiers,
    racial_ability_modifiers,
    validate_feats,
)
from .content import CharacterClass, ContentRegistry, Race
from .level_plan import LevelEntry, LevelPlanError, LevelUpPlan
from .progression import (
    ability_bump_levels,
    bab_at,
    bonus_spells_per_day,
    general_feat_levels,
    save_base_at,
    spells_known_at,
    spells_per_day_at,
)


# ---------------------------------------------------------------------------
# Cumulative state
# ---------------------------------------------------------------------------


@dataclass
class CumulativeState:
    """The character's full state at a particular level."""

    target_level: int
    class_levels: dict[str, int]                # class_id → levels in that class
    bab: int
    saves: dict[str, int]                       # fort/ref/will base totals
    hp_max: int
    hp_breakdown: list[int]                     # per-level HP gained
    skill_ranks: dict[str, int]                 # cumulative ranks per skill
    feats: list[str]                            # all feats accumulated
    class_features: list[dict]                  # all class features acquired
    ability_bumps: dict[str, int]               # ability key → total bumps
    final_ability_scores: AbilityScores         # post-racial + post-bumps
    spells_per_day: dict[str, Any]              # final spells/day
    spells_known: dict[str, int]                # for spontaneous casters
    spellbook: list[str]                        # for wizards (cumulative)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_plan(
    plan: LevelUpPlan,
    base_scores: AbilityScores,
    race: Race,
    free_choice: str | None,
    starting_class_id: str,
    starting_feats: list[str],
    starting_skill_ranks: dict[str, int],
    starting_class_choices: dict[str, Any],
    registry: ContentRegistry,
) -> None:
    """Walk the plan and validate every level's legality."""
    if plan.target_level == 1:
        return  # nothing to validate beyond L1

    # We mimic the applicator: walk levels, raising LevelPlanError on the
    # first violation. The applicator below shares this logic; we keep it
    # separate so the API can validate without producing the full state.
    apply_plan(
        plan=plan,
        base_scores=base_scores,
        race=race,
        free_choice=free_choice,
        starting_class_id=starting_class_id,
        starting_feats=starting_feats,
        starting_skill_ranks=starting_skill_ranks,
        starting_class_choices=starting_class_choices,
        registry=registry,
        validate_only=True,
    )


# ---------------------------------------------------------------------------
# Applicator
# ---------------------------------------------------------------------------


def apply_plan(
    plan: LevelUpPlan,
    base_scores: AbilityScores,
    race: Race,
    free_choice: str | None,
    starting_class_id: str,
    starting_feats: list[str],
    starting_skill_ranks: dict[str, int],
    starting_class_choices: dict[str, Any],
    registry: ContentRegistry,
    validate_only: bool = False,
) -> CumulativeState:
    """Walk levels 1..plan.target_level and produce cumulative state."""

    final_l1_scores = apply_racial_modifiers(base_scores, race, free_choice)

    class_levels: dict[str, int] = {starting_class_id: 1}
    feats: list[str] = list(starting_feats)
    skill_ranks: dict[str, int] = dict(starting_skill_ranks)
    class_features: list[dict] = []
    ability_bumps: dict[str, int] = {}
    hp_breakdown: list[int] = []
    spellbook: list[str] = []
    spells_known_total: dict[str, int] = {}

    # L1 base contributions (HP, class features, etc.).
    starting_class = registry.get_class(starting_class_id)
    hp_breakdown.append(starting_class.hit_die + final_l1_scores.modifier("con"))
    class_features.extend(starting_class.level_1.class_features)

    # Iterate levels 2..target.
    cumulative_int_mod_at = lambda scores: scores.modifier("int")

    for level in range(2, plan.target_level + 1):
        entry = plan.levels[level]
        cls = registry.get_class(entry.class_id)

        # Track class levels.
        class_levels[entry.class_id] = class_levels.get(entry.class_id, 0) + 1

        # ── Ability bumps applied first, before later validations use them.
        if level in ability_bump_levels(plan.target_level):
            if not entry.ability_bump:
                raise LevelPlanError(
                    f"level {level}: ability_bump required at L{level} "
                    f"(every 4 levels); none provided"
                )
            if entry.ability_bump not in ("str", "dex", "con", "int", "wis", "cha"):
                raise LevelPlanError(
                    f"level {level}: ability_bump {entry.ability_bump!r} invalid"
                )
            ability_bumps[entry.ability_bump] = (
                ability_bumps.get(entry.ability_bump, 0) + 1
            )
        else:
            if entry.ability_bump:
                raise LevelPlanError(
                    f"level {level}: ability_bump only allowed at L4/8/12/16/20"
                )

        # Compute current ability scores after bumps.
        bumps_dict = {k: v for k, v in ability_bumps.items()}
        cur_scores = final_l1_scores.with_changes(bumps_dict)

        # ── HP for this level.
        hp_gain = _compute_hp_for_level(cls, entry, cur_scores)
        hp_breakdown.append(hp_gain)

        # ── Skill ranks.
        skill_budget = _skill_points_for_level(cls, race, cur_scores, level)
        spent = sum(entry.skill_ranks.values())
        if spent > skill_budget:
            raise LevelPlanError(
                f"level {level}: spent {spent} skill ranks but only "
                f"{skill_budget} available"
            )
        for sid, ranks in entry.skill_ranks.items():
            if ranks < 0:
                raise LevelPlanError(
                    f"level {level}: negative ranks for {sid!r}"
                )
            registry.get_skill(sid)  # raises if unknown
            new_total = skill_ranks.get(sid, 0) + ranks
            if new_total > level:
                raise LevelPlanError(
                    f"level {level}: skill {sid!r} would have {new_total} ranks; "
                    f"max at L{level} is {level}"
                )
            skill_ranks[sid] = new_total

        # ── General feat at odd levels.
        if level in general_feat_levels(plan.target_level):
            if not entry.feat_general:
                raise LevelPlanError(
                    f"level {level}: general feat required at odd level"
                )
            feats.append(entry.feat_general)
        else:
            if entry.feat_general:
                raise LevelPlanError(
                    f"level {level}: general feat only granted at odd levels"
                )

        # ── Class bonus feat (placeholder — would check class-specific schedule).
        if entry.feat_class_bonus:
            feats.append(entry.feat_class_bonus)

        # ── Validate cumulative feat list against current ability/BAB.
        try:
            cumulative_bab = sum(
                bab_at(_progression_for(rcls, registry), lvl)
                for rcls, lvl in class_levels.items()
            )
            validate_feats(
                feats,
                cur_scores,
                _virtual_class_at_bab(cls, cumulative_bab, registry),
                registry,
            )
        except Exception as e:
            raise LevelPlanError(
                f"level {level}: feat validation failed: {e}"
            )

        # ── Class features added at this level.
        # For now, only the entry's class features come from JSON's
        # features_by_level; absent → empty list.
        added_features = _features_for_class_at_level(cls, level)
        class_features.extend(added_features)

        # ── Spells known / spellbook (caster classes).
        if entry.spells_known_added:
            for sid in entry.spells_known_added:
                spells_known_total[sid] = spells_known_total.get(sid, 0) + 1
        if entry.spellbook_added:
            spellbook.extend(entry.spellbook_added)

        if validate_only:
            continue

    # ── Final aggregation.
    bab_total = sum(
        bab_at(_progression_for(class_id, registry), n)
        for class_id, n in class_levels.items()
    )
    saves = _aggregate_saves(class_levels, registry)

    final_ability_scores = final_l1_scores.with_changes(
        {k: v for k, v in ability_bumps.items()}
    )

    spells_per_day = _aggregate_spells_per_day(class_levels, final_ability_scores)
    spells_known = _aggregate_spells_known(class_levels)

    return CumulativeState(
        target_level=plan.target_level,
        class_levels=dict(class_levels),
        bab=bab_total,
        saves=saves,
        hp_max=sum(hp_breakdown),
        hp_breakdown=hp_breakdown,
        skill_ranks=dict(skill_ranks),
        feats=list(feats),
        class_features=list(class_features),
        ability_bumps=dict(ability_bumps),
        final_ability_scores=final_ability_scores,
        spells_per_day=spells_per_day,
        spells_known=spells_known,
        spellbook=list(spellbook),
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _progression_for(class_id: str, registry: ContentRegistry) -> str:
    """Class BAB progression type — looked up from JSON or defaulted."""
    cls = registry.get_class(class_id)
    raw = cls.raw or {}
    explicit = raw.get("bab_progression")
    if explicit:
        return str(explicit)
    # Fall back: infer from the class's L1 BAB.
    bab1 = cls.level_1.bab
    if bab1 == 1:
        return "full"
    # Both 3/4 and 1/2 give BAB 0 at L1; differentiate by hit die.
    if cls.hit_die >= 8:
        return "three_quarters"
    return "half"


def _virtual_class_at_bab(
    base_class: CharacterClass,
    cumulative_bab: int,
    registry: ContentRegistry,
) -> CharacterClass:
    """Synthesize a CharacterClass-like wrapper with the cumulative BAB.

    The feat validator only reads ``class_.level_1.bab`` and
    ``class_.spell_progression``; we don't need a full clone. Instead
    we just patch the BAB on a copy.
    """
    from copy import deepcopy
    out = deepcopy(base_class)
    out.level_1.bab = cumulative_bab
    return out


def _aggregate_saves(
    class_levels: dict[str, int],
    registry: ContentRegistry,
) -> dict[str, int]:
    saves = {"fort": 0, "ref": 0, "will": 0}
    for class_id, levels in class_levels.items():
        cls = registry.get_class(class_id)
        for save_kind in saves:
            track = (cls.raw or {}).get("save_progression", {}).get(save_kind)
            if not track:
                # Infer from L1: base 2 → good; base 0 → poor.
                base_at_1 = cls.level_1.saves.get(save_kind, 0)
                track = "good" if base_at_1 >= 2 else "poor"
            saves[save_kind] += save_base_at(track, levels)
    return saves


def _compute_hp_for_level(
    cls: CharacterClass,
    entry: LevelEntry,
    scores: AbilityScores,
) -> int:
    con_mod = scores.modifier("con")
    if entry.hp_method == "max":
        return cls.hit_die + con_mod
    if entry.hp_method == "fixed_half":
        # PF1 standard: HD/2 + 1 + Con mod.
        return cls.hit_die // 2 + 1 + con_mod
    if entry.hp_method == "rolled":
        if entry.hp_roll is None:
            raise LevelPlanError(
                f"hp_method 'rolled' requires hp_roll to be supplied"
            )
        if entry.hp_roll < 1 or entry.hp_roll > cls.hit_die:
            raise LevelPlanError(
                f"hp_roll {entry.hp_roll} not in 1..{cls.hit_die}"
            )
        return entry.hp_roll + con_mod
    raise LevelPlanError(f"unknown hp_method {entry.hp_method!r}")


def _skill_points_for_level(
    cls: CharacterClass,
    race: Race,
    scores: AbilityScores,
    level: int,
) -> int:
    base = cls.level_1.skill_points_per_level
    int_mod = scores.modifier("int")
    extra = int(race.raw.get("extra_skill_ranks_per_level", 0))
    per_level = max(1, base + int_mod) + extra
    return per_level


def _features_for_class_at_level(
    cls: CharacterClass,
    class_level: int,
) -> list[dict]:
    raw = cls.raw or {}
    fbl = raw.get("features_by_level") or {}
    return list(fbl.get(str(class_level)) or [])


def _aggregate_spells_per_day(
    class_levels: dict[str, int],
    scores: AbilityScores,
) -> dict[str, Any]:
    """Combine spell slots across class levels (single-class only for v1)."""
    if len(class_levels) != 1:
        # Multiclass casters: each class tracks separately. v1 simplification
        # exposes the highest-leveled caster class.
        caster_classes = [
            (cid, lv) for cid, lv in class_levels.items()
            if cid in ("cleric", "druid", "wizard", "sorcerer", "bard",
                       "paladin", "ranger")
        ]
        if not caster_classes:
            return {}
        caster_classes.sort(key=lambda t: -t[1])
        cid, lv = caster_classes[0]
    else:
        cid, lv = next(iter(class_levels.items()))

    base = spells_per_day_at(cid, lv)
    if not base:
        return {}
    # Bonus slots from key ability score.
    key_ability_map = {
        "cleric": "wis", "druid": "wis", "wizard": "int",
        "sorcerer": "cha", "bard": "cha", "paladin": "cha", "ranger": "wis",
    }
    key = key_ability_map.get(cid)
    if key is not None:
        bonus = bonus_spells_per_day(scores.get(key))
        for slvl, extra in bonus.items():
            if slvl in base and base[slvl] != "at_will" and base[slvl] > 0:
                base[slvl] = int(base[slvl]) + extra
    return base


def _aggregate_spells_known(class_levels: dict[str, int]) -> dict[str, int]:
    if len(class_levels) != 1:
        # Multiclass: take highest spontaneous caster.
        spont = [(cid, lv) for cid, lv in class_levels.items()
                 if cid in ("sorcerer", "bard")]
        if not spont:
            return {}
        spont.sort(key=lambda t: -t[1])
        cid, lv = spont[0]
    else:
        cid, lv = next(iter(class_levels.items()))
    return spells_known_at(cid, lv)
