"""Level-1 character creation and the derived ``CharacterSheet`` view.

A ``Character`` stores only **inputs** — the things the user/server chose
or rolled. All derived values (final ability scores after racial mods, HP,
BAB, saves, skill totals, spell slots) are computed on demand by
``compute_sheet`` against a ``ContentRegistry``.

Stat reports include both the total and the modifier breakdown that
produced it, per the engine's modifier-architecture rule.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from typing import Any

from .content import (
    CharacterClass,
    ContentRegistry,
    Race,
)
from .dice import Roller
from .modifiers import (
    Modifier,
    ModifierCollection,
    mod,
    stat_report,
)


# ---------------------------------------------------------------------------
# Ability scores
# ---------------------------------------------------------------------------


ABILITY_KEYS = ("str", "dex", "con", "int", "wis", "cha")


@dataclass(frozen=True)
class AbilityScores:
    str_: int
    dex: int
    con: int
    int_: int
    wis: int
    cha: int

    @classmethod
    def from_dict(cls, d: dict) -> AbilityScores:
        for k in ABILITY_KEYS:
            if k not in d:
                raise CharacterCreationError(f"missing ability score: {k!r}")
        return cls(
            str_=int(d["str"]),
            dex=int(d["dex"]),
            con=int(d["con"]),
            int_=int(d["int"]),
            wis=int(d["wis"]),
            cha=int(d["cha"]),
        )

    def get(self, ability: str) -> int:
        if ability == "str":
            return self.str_
        if ability == "dex":
            return self.dex
        if ability == "con":
            return self.con
        if ability == "int":
            return self.int_
        if ability == "wis":
            return self.wis
        if ability == "cha":
            return self.cha
        raise KeyError(ability)

    def modifier(self, ability: str) -> int:
        return ability_modifier(self.get(ability))

    def to_dict(self) -> dict[str, int]:
        return {k: self.get(k) for k in ABILITY_KEYS}

    def with_changes(self, deltas: dict[str, int]) -> AbilityScores:
        d = self.to_dict()
        for k, v in deltas.items():
            d[k] = d.get(k, 0) + v
        return AbilityScores.from_dict(d)


def ability_modifier(score: int) -> int:
    """Standard d20 ability modifier: ``(score - 10) // 2``."""
    return (score - 10) // 2


# ---------------------------------------------------------------------------
# Generation methods
# ---------------------------------------------------------------------------


# PF1 point-buy cost table. Mapping score -> cost.
POINT_BUY_COSTS: dict[int, int] = {
    7:  -4, 8:  -2, 9:  -1, 10: 0, 11: 1, 12: 2,
    13:  3, 14:  5, 15:  7, 16: 10, 17: 13, 18: 17,
}

POINT_BUY_BUDGETS: dict[str, int] = {
    "point_buy_10": 10,   # low fantasy
    "point_buy_15": 15,   # standard fantasy (PF1 default)
    "point_buy_20": 20,   # high fantasy
    "point_buy_25": 25,   # epic fantasy
}

STANDARD_ARRAY: tuple[int, ...] = (15, 14, 13, 12, 10, 8)


class CharacterCreationError(ValueError):
    """Raised when a character creation request is invalid."""


def _validate_point_buy(scores: AbilityScores, budget: int) -> None:
    total = 0
    for k in ABILITY_KEYS:
        s = scores.get(k)
        if s not in POINT_BUY_COSTS:
            raise CharacterCreationError(
                f"point-buy ability score {s} for {k!r} out of range (7..18)"
            )
        total += POINT_BUY_COSTS[s]
    if total != budget:
        raise CharacterCreationError(
            f"point-buy total spent {total} does not equal budget {budget}"
        )


def _validate_standard_array(scores: AbilityScores) -> None:
    given = sorted([scores.get(k) for k in ABILITY_KEYS], reverse=True)
    expected = sorted(STANDARD_ARRAY, reverse=True)
    if given != expected:
        raise CharacterCreationError(
            f"standard array must be {expected}; got {given}"
        )


def validate_ability_scores(scores: AbilityScores, method: str) -> None:
    """Check that ``scores`` is a legal output of ``method``."""
    if method == "rolled_4d6kh3":
        return
    if method == "standard_array":
        _validate_standard_array(scores)
        return
    if method in POINT_BUY_BUDGETS:
        _validate_point_buy(scores, POINT_BUY_BUDGETS[method])
        return
    raise CharacterCreationError(f"unknown ability score method: {method!r}")


def roll_ability_scores_4d6kh3(roller: Roller) -> list[int]:
    """Roll six 4d6-keep-highest-3 results. Caller assigns to abilities."""
    return [roller.roll("4d6kh3").total for _ in range(6)]


# ---------------------------------------------------------------------------
# Race & class application — pure helpers
# ---------------------------------------------------------------------------


def apply_racial_modifiers(
    base: AbilityScores,
    race: Race,
    free_choice_target: str | None,
) -> AbilityScores:
    """Add racial modifiers to ``base``, returning the post-racial scores."""
    mods: dict[str, int] = dict(race.ability_modifiers)
    if race.ability_modifier_choice is not None:
        if free_choice_target is None:
            raise CharacterCreationError(
                f"race {race.id!r} requires a free ability bonus target"
            )
        choice = race.ability_modifier_choice
        if free_choice_target not in choice["options"]:
            raise CharacterCreationError(
                f"free ability bonus target {free_choice_target!r} not in "
                f"options {choice['options']}"
            )
        mods[free_choice_target] = mods.get(free_choice_target, 0) + int(choice["bonus"])
    return base.with_changes(mods)


def racial_ability_modifiers(
    race: Race,
    free_choice_target: str | None,
) -> list[Modifier]:
    """Return racial ability score adjustments as ``Modifier`` objects."""
    out: list[Modifier] = []
    for ab, value in race.ability_modifiers.items():
        out.append(mod(value, "racial", f"ability:{ab}", f"race:{race.id}"))
    if race.ability_modifier_choice is not None:
        if free_choice_target is None:
            raise CharacterCreationError(
                f"race {race.id!r} requires a free ability bonus target"
            )
        choice = race.ability_modifier_choice
        if free_choice_target not in choice["options"]:
            raise CharacterCreationError(
                f"free ability bonus target {free_choice_target!r} not in "
                f"options {choice['options']}"
            )
        out.append(mod(
            int(choice["bonus"]),
            "racial",
            f"ability:{free_choice_target}",
            f"race:{race.id}:free_choice",
        ))
    return out


# Alignment helpers --------------------------------------------------------

ALIGNMENTS = {
    "lawful_good", "neutral_good", "chaotic_good",
    "lawful_neutral", "true_neutral", "chaotic_neutral",
    "lawful_evil", "neutral_evil", "chaotic_evil",
}

LAWFUL = {"lawful_good", "lawful_neutral", "lawful_evil"}
CHAOTIC = {"chaotic_good", "chaotic_neutral", "chaotic_evil"}
NEUTRAL_ETHIC = {"neutral_good", "true_neutral", "neutral_evil"}

GOOD = {"lawful_good", "neutral_good", "chaotic_good"}
EVIL = {"lawful_evil", "neutral_evil", "chaotic_evil"}
NEUTRAL_MORAL = {"lawful_neutral", "true_neutral", "chaotic_neutral"}


def _alignment_satisfies(restriction: str | None, alignment: str) -> bool:
    if restriction is None or restriction == "":
        return True
    if alignment not in ALIGNMENTS:
        return False
    if restriction == alignment:
        return True
    if restriction == "lawful":
        return alignment in LAWFUL
    if restriction == "any_nonlawful":
        return alignment not in LAWFUL
    if restriction == "any_neutral":
        return alignment in (NEUTRAL_ETHIC | NEUTRAL_MORAL | {"true_neutral"})
    if restriction == "lawful_good":
        return alignment == "lawful_good"
    if restriction == "within_one_step_of_deity":
        return True
    return False


# ---------------------------------------------------------------------------
# Skill + feat validation helpers (for create_character)
# ---------------------------------------------------------------------------


def compute_skill_points_l1(
    class_: CharacterClass,
    scores: AbilityScores,
    race: Race,
) -> int:
    base = class_.level_1.skill_points_per_level
    int_mod = scores.modifier("int")
    extra_race = int(race.raw.get("extra_skill_ranks_per_level", 0))
    per_level = max(1, base + int_mod) + extra_race
    return per_level * 4   # PF1: level-1 multiplier x4


def validate_skill_ranks(
    class_: CharacterClass,
    race: Race,
    scores: AbilityScores,
    skill_ranks: dict[str, int],
    registry: ContentRegistry,
) -> None:
    if any(r < 0 for r in skill_ranks.values()):
        raise CharacterCreationError("skill ranks cannot be negative")
    for sid, ranks in skill_ranks.items():
        if ranks > 1:
            raise CharacterCreationError(
                f"skill {sid!r} has {ranks} ranks; max at level 1 is 1"
            )
        registry.get_skill(sid)  # raises if unknown
    spent = sum(skill_ranks.values())
    available = compute_skill_points_l1(class_, scores, race)
    if spent > available:
        raise CharacterCreationError(
            f"spent {spent} skill points but only {available} are available"
        )


def required_feat_count_l1(class_: CharacterClass, race: Race) -> int:
    """General feats picked at level 1 (excluding class-granted bonus feats)."""
    base = 1
    extra = int(race.raw.get("extra_feats_at_level_1", 0))
    return base + extra


_PARAMETRIC_FEAT_PREFIXES = ("skill_focus_", "weapon_focus_", "spell_focus_")


def _base_feat_id(fid: str) -> str:
    """Strip parametric suffix to get the underlying registered feat id."""
    for prefix in _PARAMETRIC_FEAT_PREFIXES:
        if fid.startswith(prefix):
            return prefix.rstrip("_")
    return fid


def validate_feats(
    feats: list[str],
    scores: AbilityScores,
    class_: CharacterClass,
    registry: ContentRegistry,
) -> None:
    seen: set[str] = set()
    for fid in feats:
        if fid in seen:
            raise CharacterCreationError(f"feat {fid!r} selected twice")
        seen.add(fid)
        feat = registry.get_feat(_base_feat_id(fid))
        prereqs = feat.prerequisites or {}
        for ab, req_score in (prereqs.get("abilities") or {}).items():
            if scores.get(ab) < int(req_score):
                raise CharacterCreationError(
                    f"feat {fid!r} requires {ab.upper()} {req_score}; "
                    f"have {scores.get(ab)}"
                )
        bab_req = int(prereqs.get("bab", 0))
        if bab_req > class_.level_1.bab:
            raise CharacterCreationError(
                f"feat {fid!r} requires BAB +{bab_req}; "
                f"have +{class_.level_1.bab}"
            )
        cl_req = int(prereqs.get("caster_level", 0))
        if cl_req > 1 and class_.spell_progression is None:
            raise CharacterCreationError(
                f"feat {fid!r} requires caster level {cl_req}; "
                f"class is not a spellcaster"
            )
        for other in prereqs.get("feats") or []:
            if other not in seen and other not in feats:
                raise CharacterCreationError(
                    f"feat {fid!r} requires {other!r}, which is not selected"
                )


# RAW (Foundry monk Bonus Feat): "Catch Off-Guard, Combat Reflexes,
# Deflect Arrows, Dodge, Improved Grapple, Scorpion Style, and Throw
# Anything." Improved Unarmed Strike is NOT on the L1 menu — the monk
# gets it free as part of the Unarmed Strike feature.
_MONK_L1_BONUS_FEAT_LIST: frozenset[str] = frozenset({
    "catch_off_guard", "combat_reflexes", "deflect_arrows",
    "dodge", "improved_grapple",
    "scorpion_style", "throw_anything",
})


# RAW (Arcane School): the eight specialty schools + universalist.
_WIZARD_SPECIALTY_SCHOOLS: frozenset[str] = frozenset({
    "abjuration", "conjuration", "divination", "enchantment",
    "evocation", "illusion", "necromancy", "transmutation",
    "universalist",
})


# RAW (Foundry pack ``Sorcerer Bloodline``): the five CRB bloodlines.
_SORCERER_BLOODLINES_CRB: frozenset[str] = frozenset({
    "arcane", "celestial", "draconic", "fey", "infernal",
})

# RAW (Foundry pack ``Draconic Bloodline``): "At 1st level, you must
# select one of the chromatic or metallic dragon types. This choice
# cannot be changed." Ten options (5 chromatic + 5 metallic).
_DRACONIC_DRAGON_TYPES: frozenset[str] = frozenset({
    "black", "blue", "green", "red", "white",
    "brass", "bronze", "copper", "gold", "silver",
})


def validate_sorcerer_bloodline_choices(
    class_choices: dict,
    registry: ContentRegistry | None = None,
) -> None:
    """Validate ``sorcerer_bloodline`` + ``sorcerer_dragon_type`` per RAW.

    RAW (Foundry pack ``Sorcerer Bloodline``):
    > A sorcerer must pick one bloodline upon taking her first level
    > of sorcerer. Once made, this choice cannot be changed.

    Rules enforced:
    - ``sorcerer_bloodline`` is required and must be in the 5 CRB
      bloodlines.
    - Draconic specifically requires ``sorcerer_dragon_type`` (any of
      the 10 chromatic/metallic dragons).
    """
    bloodline = (class_choices or {}).get("sorcerer_bloodline")
    if not bloodline:
        raise CharacterCreationError(
            "sorcerer requires class_choices.sorcerer_bloodline at L1"
        )
    if bloodline not in _SORCERER_BLOODLINES_CRB:
        raise CharacterCreationError(
            f"sorcerer_bloodline {bloodline!r} is not a recognized CRB "
            f"bloodline (allowed: {sorted(_SORCERER_BLOODLINES_CRB)})"
        )
    if bloodline == "draconic":
        dragon = (class_choices or {}).get("sorcerer_dragon_type")
        if not dragon:
            raise CharacterCreationError(
                "draconic bloodline requires "
                "class_choices.sorcerer_dragon_type at L1"
            )
        if dragon not in _DRACONIC_DRAGON_TYPES:
            raise CharacterCreationError(
                f"sorcerer_dragon_type {dragon!r} not in the RAW menu "
                f"(allowed: {sorted(_DRACONIC_DRAGON_TYPES)})"
            )


# RAW (Foundry pack ``Arcane Bond``): five bonded-object categories
# plus the familiar form.
_ARCANE_BOND_TYPES: frozenset[str] = frozenset({
    "amulet", "ring", "staff", "wand", "weapon", "familiar",
})


def validate_wizard_arcane_bond(
    class_choices: dict,
    registry: ContentRegistry | None = None,
) -> None:
    """Validate ``arcane_bond_type`` per RAW.

    RAW: "Objects that are the subject of an arcane bond must fall
    into one of the following categories: amulet, ring, staff, wand,
    or weapon. ... A familiar is a magical pet..."

    Required at L1 per RAW; defaults to ``amulet`` at sheet build
    when omitted (same defaulting style as ``wizard_school`` →
    universalist). Explicit values must be in the RAW menu. Familiar
    form requires an additional ``familiar_animal`` choice from the
    familiar list (validated separately when bond_type == 'familiar').
    """
    bond = (class_choices or {}).get("arcane_bond_type")
    if bond is None:
        return  # defaults to "amulet" at sheet build
    if bond not in _ARCANE_BOND_TYPES:
        raise CharacterCreationError(
            f"arcane_bond_type {bond!r} not in the RAW menu "
            f"(allowed: {sorted(_ARCANE_BOND_TYPES)})"
        )


def validate_wizard_school_choices(
    class_choices: dict,
    registry: ContentRegistry | None = None,
) -> None:
    """Validate ``wizard_school`` + ``wizard_opposition_schools`` per RAW.

    RAW (Foundry pack ``Arcane School``):

    > A wizard can choose to specialize in one school of magic ... A
    > wizard that does not select a school receives the universalist
    > school instead.

    > A wizard that chooses to specialize in one school of magic must
    > select two other schools as his opposition schools ...

    Rules enforced:
    - ``wizard_school`` must be in the 9 CRB schools (or absent, in
      which case the wizard defaults to universalist at sheet-build).
    - For specialists: exactly two opposition schools, neither being
      the chosen specialty, both valid school ids.
    - For universalists: opposition_schools must be empty / absent.
    """
    school = (class_choices or {}).get("wizard_school")
    if school is None:
        return  # defaults to universalist
    if school not in _WIZARD_SPECIALTY_SCHOOLS:
        raise CharacterCreationError(
            f"wizard_school {school!r} is not a recognized school "
            f"(allowed: {sorted(_WIZARD_SPECIALTY_SCHOOLS)})"
        )
    opposition_raw = (class_choices or {}).get("wizard_opposition_schools")
    opposition = list(opposition_raw or [])
    if school == "universalist":
        if opposition:
            raise CharacterCreationError(
                "universalist wizards have no opposition schools; "
                f"got {opposition!r}"
            )
        return
    if len(opposition) != 2:
        raise CharacterCreationError(
            "specialist wizards must pick exactly two opposition "
            f"schools (got {len(opposition)})"
        )
    if len(set(opposition)) != 2:
        raise CharacterCreationError(
            f"opposition schools must be distinct (got {opposition!r})"
        )
    for op in opposition:
        if op not in _WIZARD_SPECIALTY_SCHOOLS or op == "universalist":
            raise CharacterCreationError(
                f"opposition school {op!r} is not a recognized "
                f"specialty school"
            )
        if op == school:
            raise CharacterCreationError(
                f"opposition school {op!r} cannot equal the chosen "
                f"specialty"
            )


def _extract_class_bonus_feats(
    class_: CharacterClass,
    class_choices: dict,
    registry: ContentRegistry | None = None,
) -> list[str]:
    """Pull any feats granted at level 1 by class choice.

    Per-class feat-pool restrictions are enforced here:
    - fighter: bonus feat must be type='combat'
    - monk: bonus feat must come from the monk-L1 list (RAW menu)
    """
    bonus: list[str] = []
    if class_.id == "fighter":
        feat_id = class_choices.get("fighter_bonus_feat")
        if not feat_id:
            raise CharacterCreationError(
                "fighter requires class_choices.fighter_bonus_feat at L1"
            )
        if registry is not None:
            try:
                feat = registry.get_feat(_base_feat_id(feat_id))
            except Exception as e:
                raise CharacterCreationError(
                    f"fighter bonus feat {feat_id!r} not found: {e}"
                )
            if (feat.type or "").lower() != "combat":
                raise CharacterCreationError(
                    f"fighter bonus feat {feat_id!r} must be type 'combat'; "
                    f"got {feat.type!r}"
                )
        bonus.append(feat_id)
    elif class_.id == "monk":
        feat_id = class_choices.get("monk_bonus_feat")
        if not feat_id:
            raise CharacterCreationError(
                "monk requires class_choices.monk_bonus_feat at L1"
            )
        base = _base_feat_id(feat_id)
        if base not in _MONK_L1_BONUS_FEAT_LIST:
            raise CharacterCreationError(
                f"monk L1 bonus feat {feat_id!r} not in the RAW menu "
                f"(allowed: {sorted(_MONK_L1_BONUS_FEAT_LIST)})"
            )
        bonus.append(feat_id)
        # RAW (Unarmed Strike, Foundry pack): "At 1st level, a monk
        # gains Improved Unarmed Strike as a bonus feat." Auto-add it
        # in addition to the chosen feat.
        bonus.append("improved_unarmed_strike")
    elif class_.id == "wizard":
        bonus.append("scribe_scroll")
    elif class_.id == "sorcerer":
        bonus.append("eschew_materials")
    return bonus


# ---------------------------------------------------------------------------
# Character (inputs only)
# ---------------------------------------------------------------------------


def _int_keyed_dict(d: dict | None) -> dict[int, list[str]] | None:
    """Coerce a JSON-decoded dict whose keys are stringified ints into
    a dict[int, list[str]]. Returns ``None`` if input is None."""
    if d is None:
        return None
    out: dict[int, list[str]] = {}
    for k, v in d.items():
        out[int(k)] = list(v or [])
    return out


@dataclass
class Character:
    """The static inputs that define a character.

    All derived stats (post-racial ability scores, HP, BAB, saves, skill
    totals, spell slots, etc.) are computed by ``compute_sheet`` from this
    plus a ``ContentRegistry``. Nothing here caches end results.
    """

    id: str
    name: str
    race_id: str
    class_id: str
    level: int
    alignment: str

    # Inputs the user/server chose at L1.
    base_ability_scores: AbilityScores         # before racial modifiers
    ability_score_method: str
    free_ability_choice: str | None            # for human/half-elf/half-orc
    feats: list[str]                           # L1 feats: chosen + class-derived
    skill_ranks: dict[str, int]                # L1 ranks per skill
    bonus_languages: list[str]                 # bonus language picks
    favored_class: str
    class_choices: dict[str, Any]              # e.g. fighter_bonus_feat selection

    # Equipment (item IDs into the content registry).
    equipped_weapon: str | None                # main weapon; None for unarmed
    equipped_armor: str                        # "none" for unarmored
    equipped_shield: str | None                # None if no shield

    # Currency rolled or supplied at creation.
    starting_gold: int

    # Off-hand weapon for two-weapon fighting. ``None`` if none equipped.
    equipped_offhand_weapon: str | None = None

    # Level-up plan from L2 to target_level. None for L1 characters.
    level_plan: dict | None = None             # serialized LevelUpPlan

    # Spell-prep state (modified at the castle, baked into the
    # combatant at dispatch).
    #
    # ``spells_prepared``: for prepared casters (wizard / cleric /
    # druid / paladin / ranger / witch / magus). Maps spell level →
    # list of spell IDs prepared today. Duplicates are allowed (a
    # wizard may prepare magic_missile twice into two L1 slots). The
    # list length must equal the class's spells-per-day at that level.
    #
    # ``spells_known``: for spontaneous casters (sorcerer / bard /
    # oracle / summoner / skald). Maps spell level → list of spell
    # IDs known. Each level's list must equal the class's
    # spells-known count for that level.
    #
    # If None, the engine uses class defaults (spontaneous: all
    # eligible spells; prepared: a 'sensible default' from class hints
    # — for v1, just pick the first N spells from the spell list at
    # each level).
    spells_prepared: dict[int, list[str]] | None = None
    spells_known: dict[int, list[str]] | None = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["base_ability_scores"] = self.base_ability_scores.to_dict()
        return d

    @classmethod
    def from_dict(cls, d: dict) -> Character:
        """Reconstruct a Character from its serialized form."""
        ab = d["base_ability_scores"]
        scores = ab if isinstance(ab, AbilityScores) else AbilityScores.from_dict(ab)
        return cls(
            id=str(d["id"]),
            name=str(d["name"]),
            race_id=str(d["race_id"]),
            class_id=str(d["class_id"]),
            level=int(d["level"]),
            alignment=str(d["alignment"]),
            base_ability_scores=scores,
            ability_score_method=str(d["ability_score_method"]),
            free_ability_choice=d.get("free_ability_choice"),
            feats=list(d.get("feats") or []),
            skill_ranks=dict(d.get("skill_ranks") or {}),
            bonus_languages=list(d.get("bonus_languages") or []),
            favored_class=str(d.get("favored_class") or d["class_id"]),
            class_choices=dict(d.get("class_choices") or {}),
            equipped_weapon=d.get("equipped_weapon"),
            equipped_armor=str(d.get("equipped_armor") or "none"),
            equipped_shield=d.get("equipped_shield"),
            equipped_offhand_weapon=d.get("equipped_offhand_weapon"),
            starting_gold=int(d.get("starting_gold", 0)),
            level_plan=d.get("level_plan"),
            spells_prepared=_int_keyed_dict(d.get("spells_prepared")),
            spells_known=_int_keyed_dict(d.get("spells_known")),
        )


# Default loadouts per class (item IDs from content/{weapons,armor,shields}).
DEFAULT_LOADOUTS: dict[str, dict[str, str | None]] = {
    "fighter":   {"weapon": "longsword",      "armor": "leather",      "shield": "light_steel_shield"},
    "barbarian": {"weapon": "greataxe",       "armor": "leather",      "shield": None},
    "rogue":     {"weapon": "shortsword",     "armor": "leather",      "shield": None},
    "monk":      {"weapon": "unarmed_strike", "armor": "none",         "shield": None},
    "ranger":    {"weapon": "longsword",      "armor": "leather",      "shield": None},
    "paladin":   {"weapon": "longsword",      "armor": "scale_mail",   "shield": "light_steel_shield"},
    "cleric":    {"weapon": "longsword",      "armor": "scale_mail",   "shield": "light_steel_shield"},
    "druid":     {"weapon": "scimitar",       "armor": "hide",         "shield": None},
    "bard":      {"weapon": "rapier",         "armor": "studded_leather", "shield": None},
    "sorcerer":  {"weapon": "dagger",         "armor": "none",         "shield": None},
    "wizard":    {"weapon": "quarterstaff",   "armor": "none",         "shield": None},
}


# ---------------------------------------------------------------------------
# CharacterRequest
# ---------------------------------------------------------------------------


@dataclass
class CharacterRequest:
    name: str
    race_id: str
    class_id: str
    alignment: str
    ability_scores: AbilityScores
    ability_score_method: str
    feats: list[str]
    skill_ranks: dict[str, int]
    languages: list[str]
    free_ability_choice: str | None = None
    favored_class: str | None = None
    class_choices: dict[str, Any] = field(default_factory=dict)
    starting_gold: int | None = None
    # Equipment overrides (default to class loadout when omitted).
    equipped_weapon: str | None = None    # None = use class default
    equipped_armor: str | None = None
    equipped_shield: str | None = None
    equipped_offhand_weapon: str | None = None  # off-hand weapon for TWF
    weapon_explicitly_none: bool = False  # True iff caller asked for unarmed
    shield_explicitly_none: bool = False
    # Level-up plan (optional). When provided, the character is built
    # all the way up to plan.target_level.
    level_plan: dict | None = None
    # Half-elf Adaptability racial trait: bonus Skill Focus feat at L1.
    # Skill ID for the bonus Skill Focus. Defaults to "perception" if
    # omitted; ignored unless race is half-elf.
    adaptability_skill_focus: str | None = None

    # Spell-prep state (see Character for semantics). Modified at the
    # castle by players, baked into the Combatant at dispatch time.
    spells_prepared: dict[int, list[str]] | None = None
    spells_known: dict[int, list[str]] | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CharacterRequest:
        ab = d.get("ability_scores")
        if ab is None or "scores" not in ab or "method" not in ab:
            raise CharacterCreationError(
                "ability_scores must include 'method' and 'scores'"
            )
        equipment = d.get("equipment") or {}
        # Distinguish "key absent" (use default) from "explicitly null" (no item).
        weapon_present = "weapon" in equipment
        shield_present = "shield" in equipment
        return cls(
            name=str(d["name"]),
            race_id=str(d["race"]),
            class_id=str(d["class"]),
            alignment=str(d["alignment"]),
            ability_scores=AbilityScores.from_dict(ab["scores"]),
            ability_score_method=str(ab["method"]),
            feats=list(d.get("feats") or []),
            skill_ranks=dict(d.get("skill_ranks") or {}),
            languages=list(d.get("bonus_languages") or []),
            free_ability_choice=d.get("free_ability_choice"),
            favored_class=d.get("favored_class"),
            class_choices=dict(d.get("class_choices") or {}),
            starting_gold=(int(d["starting_gold"])
                           if d.get("starting_gold") is not None else None),
            equipped_weapon=equipment.get("weapon"),
            equipped_armor=equipment.get("armor"),
            equipped_shield=equipment.get("shield"),
            equipped_offhand_weapon=equipment.get("offhand"),
            weapon_explicitly_none=(weapon_present and equipment.get("weapon") is None),
            shield_explicitly_none=(shield_present and equipment.get("shield") is None),
            level_plan=d.get("level_plan"),
            adaptability_skill_focus=d.get("adaptability_skill_focus"),
            spells_prepared=_int_keyed_dict(d.get("spells_prepared")),
            spells_known=_int_keyed_dict(d.get("spells_known")),
        )


# ---------------------------------------------------------------------------
# create_character — validates and constructs an input-only Character
# ---------------------------------------------------------------------------


def create_character(
    request: CharacterRequest,
    registry: ContentRegistry,
    roller: Roller | None = None,
) -> Character:
    """Validate ``request`` and return a Character holding only the inputs.

    Derived stats are not computed here. Use ``compute_sheet`` to view
    HP, AC, saves, skill totals, etc.
    """
    if request.alignment not in ALIGNMENTS:
        raise CharacterCreationError(f"unknown alignment: {request.alignment!r}")
    if not request.name.strip():
        raise CharacterCreationError("character name is required")

    race = registry.get_race(request.race_id)
    class_ = registry.get_class(request.class_id)

    validate_ability_scores(request.ability_scores, request.ability_score_method)
    final_scores = apply_racial_modifiers(
        request.ability_scores, race, request.free_ability_choice
    )

    if not _alignment_satisfies(class_.alignment_restriction, request.alignment):
        raise CharacterCreationError(
            f"class {class_.id!r} requires alignment "
            f"{class_.alignment_restriction!r}, got {request.alignment!r}"
        )

    # Languages.
    int_mod = final_scores.modifier("int")
    bonus_lang_budget = max(0, int_mod)
    if len(request.languages) > bonus_lang_budget:
        raise CharacterCreationError(
            f"selected {len(request.languages)} bonus languages; only "
            f"{bonus_lang_budget} permitted (Int modifier)"
        )
    for lang in request.languages:
        if "any" not in race.languages_bonus and lang not in race.languages_bonus:
            raise CharacterCreationError(
                f"bonus language {lang!r} not in this race's bonus list"
            )

    # Feats.
    expected_feat_count = required_feat_count_l1(class_, race)
    class_bonus_feats = _extract_class_bonus_feats(
        class_, request.class_choices, registry,
    )
    chosen_general_feats = list(request.feats)
    if len(chosen_general_feats) != expected_feat_count:
        raise CharacterCreationError(
            f"expected {expected_feat_count} general feat(s); got "
            f"{len(chosen_general_feats)}"
        )
    all_feats = chosen_general_feats + class_bonus_feats
    # Half-elf Adaptability racial trait: bonus Skill Focus at L1.
    if race.id == "half_elf":
        skill_id = request.adaptability_skill_focus or "perception"
        adaptability_feat = f"skill_focus_{skill_id}"
        if adaptability_feat not in all_feats:
            all_feats.append(adaptability_feat)
    validate_feats(all_feats, final_scores, class_, registry)

    # Class-specific class_choices validation.
    if class_.id == "wizard":
        validate_wizard_school_choices(request.class_choices, registry)
        validate_wizard_arcane_bond(request.class_choices, registry)
    elif class_.id == "sorcerer":
        validate_sorcerer_bloodline_choices(request.class_choices, registry)

    # Skill ranks.
    validate_skill_ranks(class_, race, final_scores, request.skill_ranks, registry)

    # Starting gold.
    if request.starting_gold is not None:
        starting_gold = request.starting_gold
    else:
        gold_roller = roller or Roller()
        roll = gold_roller.roll(class_.starting_gold_dice)
        starting_gold = roll.total * class_.starting_gold_multiplier

    favored_class = request.favored_class or class_.id

    # Equipment selection: explicit overrides win, else class default.
    loadout = DEFAULT_LOADOUTS.get(class_.id, {"weapon": None, "armor": "none", "shield": None})

    if request.equipped_weapon is not None:
        weapon_id: str | None = request.equipped_weapon
    elif request.weapon_explicitly_none:
        weapon_id = None
    else:
        weapon_id = loadout.get("weapon")

    armor_id = request.equipped_armor or loadout.get("armor", "none")

    if request.equipped_shield is not None:
        shield_id: str | None = request.equipped_shield
    elif request.shield_explicitly_none:
        shield_id = None
    else:
        shield_id = loadout.get("shield")

    # Validate equipment exists (skip None and "none").
    if weapon_id is not None:
        registry.get_weapon(weapon_id)
    if armor_id is not None and armor_id != "none":
        registry.get_armor(armor_id)
    elif armor_id == "none":
        pass  # unarmored is fine
    if shield_id is not None:
        registry.get_shield(shield_id)

    # Validate and store the level-up plan if provided.
    plan_dict: dict | None = None
    target_level = 1
    if request.level_plan is not None:
        from .level_plan import LevelUpPlan, LevelPlanError
        from .leveling import validate_plan
        try:
            plan = LevelUpPlan.from_dict(request.level_plan)
        except LevelPlanError as e:
            raise CharacterCreationError(f"invalid level_plan: {e}")
        if plan.target_level > 1:
            try:
                validate_plan(
                    plan=plan,
                    base_scores=request.ability_scores,
                    race=race,
                    free_choice=request.free_ability_choice,
                    starting_class_id=class_.id,
                    starting_feats=all_feats,
                    starting_skill_ranks=dict(request.skill_ranks),
                    starting_class_choices=dict(request.class_choices),
                    registry=registry,
                )
            except LevelPlanError as e:
                raise CharacterCreationError(f"level_plan validation failed: {e}")
        plan_dict = plan.to_dict()
        target_level = plan.target_level

    return Character(
        id=f"hero_{uuid.uuid4().hex[:12]}",
        name=request.name,
        race_id=race.id,
        class_id=class_.id,
        level=target_level,
        alignment=request.alignment,
        base_ability_scores=request.ability_scores,
        ability_score_method=request.ability_score_method,
        free_ability_choice=request.free_ability_choice,
        feats=all_feats,
        skill_ranks=dict(request.skill_ranks),
        bonus_languages=list(request.languages),
        favored_class=favored_class,
        class_choices=dict(request.class_choices),
        equipped_weapon=weapon_id,
        equipped_armor=armor_id or "none",
        equipped_shield=shield_id,
        equipped_offhand_weapon=request.equipped_offhand_weapon,
        starting_gold=starting_gold,
        level_plan=plan_dict,
        spells_prepared=request.spells_prepared,
        spells_known=request.spells_known,
    )


# ---------------------------------------------------------------------------
# CharacterSheet (derived view)
# ---------------------------------------------------------------------------


@dataclass
class CharacterSheet:
    """A derived view of a Character. Shows totals and modifier breakdowns.

    Always built fresh by ``compute_sheet``. Nothing here is authoritative
    state — the source of truth is the ``Character``.
    """

    id: str
    name: str
    race_id: str
    class_id: str
    level: int
    alignment: str
    size: str
    speed: int

    base_ability_scores: dict[str, int]
    ability_scores: dict[str, dict]    # {ability: stat_report}

    hp: dict                           # stat_report for hp_max
    bab: int
    saves: dict[str, dict]             # {fort/ref/will: stat_report}

    skill_points_total: int
    skills: dict[str, dict]            # {skill_id: stat_report}

    feats: list[str]
    class_features: list[dict]
    racial_traits: list[dict]

    languages: list[str]
    weapon_proficiencies: str
    armor_proficiencies: str

    spells_per_day: dict[str, Any] | None
    spells_known_count: dict[str, int] | None

    starting_gold: int
    favored_class: str

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# compute_sheet
# ---------------------------------------------------------------------------


def compute_sheet(character: Character, registry: ContentRegistry) -> CharacterSheet:
    """Compute the derived view of ``character`` against ``registry``.

    For a level-1 character (no plan), the sheet reflects the L1
    state. For higher levels (plan provided), walks levels 2..N
    accumulating BAB, saves, HP, ability bumps, feats, and spells.
    """
    race = registry.get_race(character.race_id)
    class_ = registry.get_class(character.class_id)

    # ── Walk the plan (if any) to get cumulative state at character.level.
    cumulative = _build_cumulative_state(character, race, class_, registry)

    # ── Ability scores (post-racial + bumps from leveling).
    coll = ModifierCollection()
    coll.add_many(racial_ability_modifiers(race, character.free_ability_choice))
    # Apply ability bumps as modifiers (so they show in the breakdown).
    for ab, count in cumulative.ability_bumps.items():
        coll.add(mod(count, "inherent", f"ability:{ab}",
                     f"ability_bump_total"))

    ability_reports: dict[str, dict] = {}
    for ab in ABILITY_KEYS:
        base = character.base_ability_scores.get(ab)
        ability_reports[ab] = stat_report(
            base, f"base_{ab}_score",
            coll.for_target(f"ability:{ab}"),
        )

    final_scores = cumulative.final_ability_scores

    # ── HP report.
    con_mod = final_scores.modifier("con")
    hp_mods: list[Modifier] = []
    if con_mod != 0:
        # Effective Con contribution = con_mod * total_levels
        total_levels = sum(cumulative.class_levels.values())
        hp_mods.append(mod(con_mod * total_levels, "ability", "hp_max",
                           f"con_per_level_x{total_levels}"))
    # Base = sum of HD per level (raw, before Con).
    raw_hd_total = sum(cumulative.hp_breakdown) - (con_mod * sum(cumulative.class_levels.values()))
    hp_report = stat_report(
        raw_hd_total, "hit_dice_summed",
        hp_mods,
    )

    # ── Saves: cumulative class bases + ability mods.
    saves: dict[str, dict] = {}
    for save_kind, save_ability in (("fort", "con"), ("ref", "dex"), ("will", "wis")):
        base = cumulative.saves.get(save_kind, 0)
        ab_mod = final_scores.modifier(save_ability)
        saves[save_kind] = stat_report(
            base, f"class_save_base_total",
            [mod(ab_mod, "ability", f"{save_kind}_save",
                 f"{save_ability}_modifier")],
        )

    # ── Skill reports — using cumulative ranks.
    class_skills = set(class_.level_1.class_skills)
    # Add class skills from any other classes the plan involved.
    for cid in cumulative.class_levels:
        if cid != class_.id:
            try:
                other = registry.get_class(cid)
                class_skills.update(other.level_1.class_skills)
            except Exception:
                pass

    skill_reports: dict[str, dict] = {}
    for skill_id, ranks in cumulative.skill_ranks.items():
        if ranks <= 0:
            continue
        skill = registry.get_skill(skill_id)
        ab_mod = final_scores.modifier(skill.ability)
        mods: list[Modifier] = [
            mod(ranks, "untyped", f"skill:{skill_id}", "ranks"),
            mod(ab_mod, "ability", f"skill:{skill_id}",
                f"{skill.ability}_modifier"),
        ]
        if skill_id in class_skills and ranks >= 1:
            mods.append(
                mod(3, "untyped", f"skill:{skill_id}", "class_skill_bonus")
            )
        skill_reports[skill_id] = stat_report(0, "no_base", mods)

    skill_points_total = compute_skill_points_l1(class_, final_scores, race)

    # Languages: starting + chosen bonus.
    languages = list(race.languages_starting) + list(character.bonus_languages)

    return CharacterSheet(
        id=character.id,
        name=character.name,
        race_id=race.id,
        class_id=class_.id,
        level=character.level,
        alignment=character.alignment,
        size=race.size,
        speed=race.speed,
        base_ability_scores=character.base_ability_scores.to_dict(),
        ability_scores=ability_reports,
        hp=hp_report,
        bab=cumulative.bab,
        saves=saves,
        skill_points_total=skill_points_total,
        skills=skill_reports,
        feats=list(cumulative.feats),
        class_features=list(cumulative.class_features),
        racial_traits=list(race.traits),
        languages=languages,
        weapon_proficiencies=class_.level_1.weapon_proficiencies,
        armor_proficiencies=class_.level_1.armor_proficiencies,
        spells_per_day=cumulative.spells_per_day or None,
        spells_known_count=cumulative.spells_known or None,
        starting_gold=character.starting_gold,
        favored_class=character.favored_class,
    )


def _build_cumulative_state(
    character: Character,
    race: Race,
    class_: CharacterClass,
    registry: ContentRegistry,
):
    """Internal: produce the cumulative state via the leveling module.

    Always returns a state — for L1 characters, the state is just the
    L1 starting values.
    """
    from .leveling import apply_plan
    from .level_plan import LevelUpPlan

    if character.level_plan and character.level > 1:
        plan = LevelUpPlan.from_dict(character.level_plan)
    else:
        # Build a trivial L1-only plan.
        plan = LevelUpPlan(name="<l1-only>", target_level=1, levels={})

    return apply_plan(
        plan=plan,
        base_scores=character.base_ability_scores,
        race=race,
        free_choice=character.free_ability_choice,
        starting_class_id=class_.id,
        starting_feats=list(character.feats),
        starting_skill_ranks=dict(character.skill_ranks),
        starting_class_choices=dict(character.class_choices),
        registry=registry,
    )


# ---------------------------------------------------------------------------
# Spellcasting at L1
# ---------------------------------------------------------------------------


def _compute_spells_l1(
    class_: CharacterClass,
    scores: AbilityScores,
    class_choices: dict,
) -> tuple[dict[str, Any] | None, dict[str, int] | None]:
    sp = class_.spell_progression
    if sp is None:
        return None, None
    per_day = dict(sp.get("spells_per_day_l1") or {})
    key = sp["key_ability"]
    ab_score = scores.get(key)
    bonus_table = _bonus_spells_per_day(ab_score)
    for slvl_str, bonus in bonus_table.items():
        if slvl_str in per_day and per_day[slvl_str] != "at_will":
            per_day[slvl_str] = int(per_day[slvl_str]) + bonus
    domain = sp.get("domain_slots_l1") or {}
    for slvl_str, slots in domain.items():
        if slvl_str in per_day and per_day[slvl_str] != "at_will":
            per_day[slvl_str] = int(per_day[slvl_str]) + int(slots)
    if class_.id == "wizard":
        school = (class_choices or {}).get("wizard_school", "universalist")
        if school and school != "universalist":
            spec = sp.get("specialist_bonus_slots_l1") or {}
            for slvl_str, slots in spec.items():
                if slvl_str in per_day and per_day[slvl_str] != "at_will":
                    per_day[slvl_str] = int(per_day[slvl_str]) + int(slots)
    known = dict(sp.get("spells_known_l1") or {}) or None
    return per_day, known


def _bonus_spells_per_day(score: int) -> dict[str, int]:
    if score < 12:
        return {}
    out: dict[str, int] = {}
    for spell_level in range(1, 10):
        threshold = 10 + spell_level
        if score < threshold:
            break
        extra = (score - threshold) // 8 + 1
        out[str(spell_level)] = extra
    return out


# ---------------------------------------------------------------------------
# Backwards-compat helpers for tests that compute saves/HP directly
# ---------------------------------------------------------------------------


def compute_hp_l1(class_: CharacterClass, scores: AbilityScores) -> int:
    """Convenience: the L1 max-HP integer (for tests / direct callers)."""
    return class_.hit_die + scores.modifier("con")


def compute_saves(class_: CharacterClass, scores: AbilityScores) -> dict[str, int]:
    """Convenience: the L1 save totals as a dict."""
    base = class_.level_1.saves
    return {
        "fort": base.get("fort", 0) + scores.modifier("con"),
        "ref":  base.get("ref",  0) + scores.modifier("dex"),
        "will": base.get("will", 0) + scores.modifier("wis"),
    }
