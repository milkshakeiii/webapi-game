"""Content loader for SRD-derived game data.

JSON content files live in ``dnd/content/`` and are loaded once at startup
into a :class:`ContentRegistry`. The registry exposes typed lookups by id.

The schema is permissive — we keep the JSON simple and let the engine pick
out the fields it needs. Unknown keys are preserved on the dataclass via
the ``raw`` attribute so that future engine code can read newly-added
fields without a schema migration.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Race:
    id: str
    name: str
    summary: str
    size: str
    speed: int
    ability_modifiers: dict[str, int]
    ability_modifier_choice: dict | None
    languages_starting: list[str]
    languages_bonus: list[str]
    vision: str
    traits: list[dict]
    raw: dict = field(default_factory=dict)


@dataclass
class ClassLevel1:
    bab: int
    saves: dict[str, int]
    skill_points_per_level: int
    class_skills: list[str]
    weapon_proficiencies: str
    armor_proficiencies: str
    class_features: list[dict]


@dataclass
class CharacterClass:
    id: str
    name: str
    summary: str
    hit_die: int
    alignment_restriction: str | None
    starting_gold_dice: str
    starting_gold_multiplier: int
    level_1: ClassLevel1
    spell_progression: dict | None
    raw: dict = field(default_factory=dict)


@dataclass
class Skill:
    id: str
    name: str
    ability: str
    trained_only: bool
    armor_check_penalty: bool
    has_subtype: bool = False
    raw: dict = field(default_factory=dict)


@dataclass
class Feat:
    id: str
    name: str
    type: str
    prerequisites: dict
    summary: str
    subtype: str | None = None
    raw: dict = field(default_factory=dict)


@dataclass
class Condition:
    id: str
    name: str
    summary: str
    raw: dict = field(default_factory=dict)


@dataclass
class Weapon:
    id: str
    name: str
    category: str          # "simple", "martial", "exotic"
    wield: str             # "light", "one_handed", "two_handed"
    damage_dice: str       # e.g. "1d8", "2d4"
    damage_type: str       # "S", "P", "B", "P/S", etc.
    crit_range: tuple[int, int]
    crit_multiplier: int
    is_melee: bool = True
    is_finesse: bool = False
    can_throw: bool = False
    range_increment: int = 0  # 0 means no ranged use
    has_reach: bool = False   # PF1 "reach weapon": threatens at 10 ft, not 5
    has_brace: bool = False   # set vs charge for double damage
    is_double: bool = False   # double weapon — both ends usable simultaneously
    trip_bonus: int = 0       # bonus to trip CMB (whip, scythe, flail = +2)
    weight: float = 0.0
    cost_gp: float = 0.0
    raw: dict = field(default_factory=dict)


@dataclass
class Armor:
    id: str
    name: str
    category: str          # "none", "light", "medium", "heavy"
    ac_bonus: int
    max_dex_bonus: int     # 99 for unarmored
    armor_check_penalty: int   # negative or zero
    arcane_spell_failure: int  # percentage
    speed_30_reduced_to: int
    speed_20_reduced_to: int
    weight: float = 0.0
    cost_gp: float = 0.0
    raw: dict = field(default_factory=dict)


@dataclass
class Shield:
    id: str
    name: str
    ac_bonus: int
    armor_check_penalty: int
    arcane_spell_failure: int
    is_tower: bool = False
    weight: float = 0.0
    cost_gp: float = 0.0
    raw: dict = field(default_factory=dict)


@dataclass
class Spell:
    id: str
    name: str
    school: str
    subschool: str
    descriptors: list[str]
    level_by_class: dict[str, int]   # class_id → spell level
    components: list[str]            # ["V", "S", "M", ...]
    casting_time: str
    range: str
    target: str
    duration: str
    saving_throw: str                # "none" / "reflex_half" / "will_negates" / etc.
    spell_resistance: str            # "yes" / "no" / "yes_harmless"
    effect: dict                     # see content/spells/*.json schemas
    summary: str
    raw: dict = field(default_factory=dict)


@dataclass
class Domain:
    """Cleric / druid domain (CRB).

    A domain bundles:
    - One L1 granted power (an active SLA-style ability or passive
      modifier), tracked per-day if active.
    - A list of bonus spells, one per spell level — the cleric
      adds these to their preparable list and gains one bonus
      domain slot per level.
    - Higher-level granted powers (typically L8 / L20) — represented
      as a list, indexed by class level.
    """
    id: str
    name: str
    summary: str
    granted_power_l1: dict          # {id, name, summary, mechanic, uses_per_day_formula}
    spells_per_level: dict[str, str]  # "1" → spell_id
    higher_level_powers: list[dict] = field(default_factory=list)
    raw: dict = field(default_factory=dict)


@dataclass
class ArcaneSchool:
    """Wizard arcane school (CRB).

    A specialist wizard picks one school at L1 plus two opposition
    schools (RAW: any non-specialty school may be an opposition
    school). Each school grants two L1 powers — typically one active
    SLA-style ability (uses/day = 3 + Int mod) and one passive bonus —
    plus a higher-level power (L8 in CRB, deferred). The
    ``universalist`` school has no opposition schools and no bonus
    spell slot, but gains its own L1 active power.
    """
    id: str
    name: str
    summary: str
    is_universalist: bool
    granted_power_l1_active: dict   # {id, name, summary, kind, ...}
    granted_power_l1_passive: dict  # {id, name, summary, kind, ...}
    higher_level_powers: list[dict] = field(default_factory=list)
    raw: dict = field(default_factory=dict)


@dataclass
class Monster:
    id: str
    name: str
    summary: str
    cr: str
    xp: int
    alignment: str
    size: str
    type: str
    subtypes: list[str]
    ability_scores: dict[str, int]
    hit_dice: str
    hp: int
    init: int
    senses: list[str]
    speed: int
    ac: dict[str, int]
    saves: dict[str, int]
    bab: int
    cmb: int
    cmd: int
    attacks: list[dict]
    feats: list[str]
    skills: dict[str, int]
    languages: list[str]
    racial_traits: list[dict]
    equipment: list[str]
    permanent_conditions: list[str] = field(default_factory=list)
    raw: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Loader helpers
# ---------------------------------------------------------------------------


def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _race_from_dict(d: dict) -> Race:
    return Race(
        id=d["id"],
        name=d["name"],
        summary=d.get("summary", ""),
        size=d["size"],
        speed=int(d["speed"]),
        ability_modifiers=dict(d.get("ability_modifiers") or {}),
        ability_modifier_choice=d.get("ability_modifier_choice"),
        languages_starting=list(d.get("languages_starting") or []),
        languages_bonus=list(d.get("languages_bonus") or []),
        vision=d.get("vision", "normal"),
        traits=list(d.get("traits") or []),
        raw=d,
    )


def _class_from_dict(d: dict) -> CharacterClass:
    l1 = d["level_1"]
    return CharacterClass(
        id=d["id"],
        name=d["name"],
        summary=d.get("summary", ""),
        hit_die=int(d["hit_die"]),
        alignment_restriction=d.get("alignment_restriction"),
        starting_gold_dice=d.get("starting_gold_dice", "0d6"),
        starting_gold_multiplier=int(d.get("starting_gold_multiplier", 10)),
        level_1=ClassLevel1(
            bab=int(l1["bab"]),
            saves=dict(l1["saves"]),
            skill_points_per_level=int(l1["skill_points_per_level"]),
            class_skills=list(l1["class_skills"]),
            weapon_proficiencies=l1.get("weapon_proficiencies", ""),
            armor_proficiencies=l1.get("armor_proficiencies", ""),
            class_features=list(l1.get("class_features") or []),
        ),
        spell_progression=d.get("spell_progression"),
        raw=d,
    )


def _skill_from_dict(d: dict) -> Skill:
    return Skill(
        id=d["id"],
        name=d["name"],
        ability=d["ability"],
        trained_only=bool(d.get("trained_only", False)),
        armor_check_penalty=bool(d.get("armor_check_penalty", False)),
        has_subtype=bool(d.get("has_subtype", False)),
        raw=d,
    )


def _feat_from_dict(d: dict) -> Feat:
    return Feat(
        id=d["id"],
        name=d["name"],
        type=d.get("type", "general"),
        prerequisites=dict(d.get("prerequisites") or {}),
        summary=d.get("summary", ""),
        subtype=d.get("subtype"),
        raw=d,
    )


def _condition_from_dict(d: dict) -> Condition:
    return Condition(
        id=d["id"],
        name=d["name"],
        summary=d.get("summary", ""),
        raw=d,
    )


def _weapon_from_dict(d: dict) -> Weapon:
    cr = d.get("crit_range") or [20, 20]
    return Weapon(
        id=d["id"],
        name=d["name"],
        category=d.get("category", "simple"),
        wield=d.get("wield", "one_handed"),
        damage_dice=d.get("damage_dice", "1d4"),
        damage_type=d.get("damage_type", "B"),
        crit_range=(int(cr[0]), int(cr[1])),
        crit_multiplier=int(d.get("crit_multiplier", 2)),
        is_melee=bool(d.get("is_melee", True)),
        is_finesse=bool(d.get("is_finesse", False)),
        can_throw=bool(d.get("can_throw", False)),
        range_increment=int(d.get("range_increment", 0)),
        has_reach=bool(d.get("has_reach", False)),
        has_brace=bool(d.get("has_brace", False)),
        is_double=bool(d.get("is_double", False)),
        trip_bonus=int(d.get("trip_bonus", 0)),
        weight=float(d.get("weight", 0)),
        cost_gp=float(d.get("cost_gp", 0)),
        raw=d,
    )


def _armor_from_dict(d: dict) -> Armor:
    return Armor(
        id=d["id"],
        name=d["name"],
        category=d.get("category", "light"),
        ac_bonus=int(d.get("ac_bonus", 0)),
        max_dex_bonus=int(d.get("max_dex_bonus", 99)),
        armor_check_penalty=int(d.get("armor_check_penalty", 0)),
        arcane_spell_failure=int(d.get("arcane_spell_failure", 0)),
        speed_30_reduced_to=int(d.get("speed_30_reduced_to", 30)),
        speed_20_reduced_to=int(d.get("speed_20_reduced_to", 20)),
        weight=float(d.get("weight", 0)),
        cost_gp=float(d.get("cost_gp", 0)),
        raw=d,
    )


def _shield_from_dict(d: dict) -> Shield:
    return Shield(
        id=d["id"],
        name=d["name"],
        ac_bonus=int(d.get("ac_bonus", 0)),
        armor_check_penalty=int(d.get("armor_check_penalty", 0)),
        arcane_spell_failure=int(d.get("arcane_spell_failure", 0)),
        is_tower=bool(d.get("is_tower", False)),
        weight=float(d.get("weight", 0)),
        cost_gp=float(d.get("cost_gp", 0)),
        raw=d,
    )


def _spell_from_dict(d: dict) -> Spell:
    return Spell(
        id=d["id"],
        name=d["name"],
        school=d.get("school", ""),
        subschool=d.get("subschool", ""),
        descriptors=list(d.get("descriptors") or []),
        level_by_class=dict(d.get("level_by_class") or {}),
        components=list(d.get("components") or []),
        casting_time=d.get("casting_time", "standard"),
        range=d.get("range", ""),
        target=d.get("target", ""),
        duration=d.get("duration", ""),
        saving_throw=d.get("saving_throw", "none"),
        spell_resistance=d.get("spell_resistance", "no"),
        effect=dict(d.get("effect") or {}),
        summary=d.get("summary", ""),
        raw=d,
    )


def _arcane_school_from_dict(d: dict) -> ArcaneSchool:
    return ArcaneSchool(
        id=d["id"],
        name=d["name"],
        summary=d.get("summary", ""),
        is_universalist=bool(d.get("is_universalist", False)),
        granted_power_l1_active=dict(d.get("granted_power_l1_active") or {}),
        granted_power_l1_passive=dict(d.get("granted_power_l1_passive") or {}),
        higher_level_powers=list(d.get("higher_level_powers") or []),
        raw=d,
    )


def _domain_from_dict(d: dict) -> Domain:
    return Domain(
        id=d["id"],
        name=d["name"],
        summary=d.get("summary", ""),
        granted_power_l1=dict(d.get("granted_power_l1") or {}),
        spells_per_level=dict(d.get("spells_per_level") or {}),
        higher_level_powers=list(d.get("higher_level_powers") or []),
        raw=d,
    )


def _monster_from_dict(d: dict) -> Monster:
    return Monster(
        id=d["id"],
        name=d["name"],
        summary=d.get("summary", ""),
        cr=str(d.get("cr", "0")),
        xp=int(d.get("xp", 0)),
        alignment=d.get("alignment", "true_neutral"),
        size=d["size"],
        type=d["type"],
        subtypes=list(d.get("subtypes") or []),
        ability_scores=dict(d.get("ability_scores") or {}),
        hit_dice=d.get("hit_dice", ""),
        hp=int(d.get("hp", 0)),
        init=int(d.get("init", 0)),
        senses=list(d.get("senses") or []),
        speed=int(d.get("speed", 0)),
        ac=dict(d.get("ac") or {}),
        saves=dict(d.get("saves") or {}),
        bab=int(d.get("bab", 0)),
        cmb=int(d.get("cmb", 0)),
        cmd=int(d.get("cmd", 0)),
        attacks=list(d.get("attacks") or []),
        feats=list(d.get("feats") or []),
        skills=dict(d.get("skills") or {}),
        languages=list(d.get("languages") or []),
        racial_traits=list(d.get("racial_traits") or []),
        equipment=list(d.get("equipment") or []),
        permanent_conditions=list(d.get("permanent_conditions") or []),
        raw=d,
    )


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class ContentNotFoundError(KeyError):
    """Raised when requested content does not exist in the registry."""


@dataclass
class ContentRegistry:
    races: dict[str, Race] = field(default_factory=dict)
    classes: dict[str, CharacterClass] = field(default_factory=dict)
    skills: dict[str, Skill] = field(default_factory=dict)
    feats: dict[str, Feat] = field(default_factory=dict)
    conditions: dict[str, Condition] = field(default_factory=dict)
    monsters: dict[str, Monster] = field(default_factory=dict)
    weapons: dict[str, Weapon] = field(default_factory=dict)
    armor: dict[str, Armor] = field(default_factory=dict)
    shields: dict[str, Shield] = field(default_factory=dict)
    spells: dict[str, Spell] = field(default_factory=dict)
    domains: dict[str, Domain] = field(default_factory=dict)
    arcane_schools: dict[str, ArcaneSchool] = field(default_factory=dict)

    @classmethod
    def from_directory(cls, content_dir: str | Path) -> ContentRegistry:
        """Load all content from ``content_dir`` and return a registry."""
        root = Path(content_dir)
        if not root.is_dir():
            raise FileNotFoundError(f"content directory not found: {root}")

        registry = cls()
        registry._load_races(root / "races")
        registry._load_classes(root / "classes")
        registry._load_skills(root / "skills")
        registry._load_feats(root / "feats")
        registry._load_conditions(root / "conditions")
        registry._load_monsters(root / "monsters")
        registry._load_weapons(root / "weapons")
        registry._load_armor(root / "armor")
        registry._load_shields(root / "shields")
        registry._load_spells(root / "spells")
        registry._load_domains(root / "domains")
        registry._load_arcane_schools(root / "wizard_schools")
        return registry

    def _load_domains(self, dirpath: Path) -> None:
        if not dirpath.is_dir():
            return
        for path in sorted(dirpath.glob("*.json")):
            data = _load_json(path)
            domain = _domain_from_dict(data)
            self.domains[domain.id] = domain

    def _load_arcane_schools(self, dirpath: Path) -> None:
        if not dirpath.is_dir():
            return
        for path in sorted(dirpath.glob("*.json")):
            data = _load_json(path)
            school = _arcane_school_from_dict(data)
            self.arcane_schools[school.id] = school

    def _load_races(self, dirpath: Path) -> None:
        if not dirpath.is_dir():
            return
        for path in sorted(dirpath.glob("*.json")):
            data = _load_json(path)
            race = _race_from_dict(data)
            self.races[race.id] = race

    def _load_classes(self, dirpath: Path) -> None:
        if not dirpath.is_dir():
            return
        for path in sorted(dirpath.glob("*.json")):
            data = _load_json(path)
            cls = _class_from_dict(data)
            self.classes[cls.id] = cls

    def _load_skills(self, dirpath: Path) -> None:
        if not dirpath.is_dir():
            return
        for path in sorted(dirpath.glob("*.json")):
            entries = _load_json(path)
            for d in entries:
                skill = _skill_from_dict(d)
                self.skills[skill.id] = skill

    def _load_feats(self, dirpath: Path) -> None:
        if not dirpath.is_dir():
            return
        for path in sorted(dirpath.glob("*.json")):
            entries = _load_json(path)
            for d in entries:
                feat = _feat_from_dict(d)
                self.feats[feat.id] = feat

    def _load_conditions(self, dirpath: Path) -> None:
        if not dirpath.is_dir():
            return
        for path in sorted(dirpath.glob("*.json")):
            entries = _load_json(path)
            for d in entries:
                cond = _condition_from_dict(d)
                self.conditions[cond.id] = cond

    def _load_monsters(self, dirpath: Path) -> None:
        if not dirpath.is_dir():
            return
        for path in sorted(dirpath.glob("*.json")):
            data = _load_json(path)
            monster = _monster_from_dict(data)
            self.monsters[monster.id] = monster

    def _load_weapons(self, dirpath: Path) -> None:
        if not dirpath.is_dir():
            return
        for path in sorted(dirpath.glob("*.json")):
            entries = _load_json(path)
            for d in entries:
                w = _weapon_from_dict(d)
                self.weapons[w.id] = w

    def _load_armor(self, dirpath: Path) -> None:
        if not dirpath.is_dir():
            return
        for path in sorted(dirpath.glob("*.json")):
            entries = _load_json(path)
            for d in entries:
                a = _armor_from_dict(d)
                self.armor[a.id] = a

    def _load_shields(self, dirpath: Path) -> None:
        if not dirpath.is_dir():
            return
        for path in sorted(dirpath.glob("*.json")):
            entries = _load_json(path)
            for d in entries:
                s = _shield_from_dict(d)
                self.shields[s.id] = s

    def _load_spells(self, dirpath: Path) -> None:
        if not dirpath.is_dir():
            return
        for path in sorted(dirpath.glob("*.json")):
            entries = _load_json(path)
            for d in entries:
                s = _spell_from_dict(d)
                self.spells[s.id] = s

    # ── lookups ───────────────────────────────────────────────────────────

    def get_race(self, race_id: str) -> Race:
        try:
            return self.races[race_id]
        except KeyError:
            raise ContentNotFoundError(f"race not found: {race_id!r}")

    def get_class(self, class_id: str) -> CharacterClass:
        try:
            return self.classes[class_id]
        except KeyError:
            raise ContentNotFoundError(f"class not found: {class_id!r}")

    def get_skill(self, skill_id: str) -> Skill:
        try:
            return self.skills[skill_id]
        except KeyError:
            raise ContentNotFoundError(f"skill not found: {skill_id!r}")

    def get_feat(self, feat_id: str) -> Feat:
        try:
            return self.feats[feat_id]
        except KeyError:
            raise ContentNotFoundError(f"feat not found: {feat_id!r}")

    def get_condition(self, condition_id: str) -> Condition:
        try:
            return self.conditions[condition_id]
        except KeyError:
            raise ContentNotFoundError(f"condition not found: {condition_id!r}")

    def get_monster(self, monster_id: str) -> Monster:
        try:
            return self.monsters[monster_id]
        except KeyError:
            raise ContentNotFoundError(f"monster not found: {monster_id!r}")

    def get_weapon(self, weapon_id: str) -> Weapon:
        try:
            return self.weapons[weapon_id]
        except KeyError:
            raise ContentNotFoundError(f"weapon not found: {weapon_id!r}")

    def get_armor(self, armor_id: str) -> Armor:
        try:
            return self.armor[armor_id]
        except KeyError:
            raise ContentNotFoundError(f"armor not found: {armor_id!r}")

    def get_shield(self, shield_id: str) -> Shield:
        try:
            return self.shields[shield_id]
        except KeyError:
            raise ContentNotFoundError(f"shield not found: {shield_id!r}")

    def get_spell(self, spell_id: str) -> Spell:
        try:
            return self.spells[spell_id]
        except KeyError:
            raise ContentNotFoundError(f"spell not found: {spell_id!r}")

    def get_arcane_school(self, school_id: str) -> ArcaneSchool:
        try:
            return self.arcane_schools[school_id]
        except KeyError:
            raise ContentNotFoundError(
                f"arcane school not found: {school_id!r}"
            )

    def all_arcane_schools(self) -> Iterable[ArcaneSchool]:
        return self.arcane_schools.values()

    def get_domain(self, domain_id: str) -> Domain:
        try:
            return self.domains[domain_id]
        except KeyError:
            raise ContentNotFoundError(f"domain not found: {domain_id!r}")

    def all_domains(self) -> Iterable[Domain]:
        return self.domains.values()

    def all_races(self) -> Iterable[Race]:
        return self.races.values()

    def all_classes(self) -> Iterable[CharacterClass]:
        return self.classes.values()

    def all_skills(self) -> Iterable[Skill]:
        return self.skills.values()

    def all_feats(self) -> Iterable[Feat]:
        return self.feats.values()

    def all_conditions(self) -> Iterable[Condition]:
        return self.conditions.values()

    def all_monsters(self) -> Iterable[Monster]:
        return self.monsters.values()

    def all_weapons(self) -> Iterable[Weapon]:
        return self.weapons.values()

    def all_armor(self) -> Iterable[Armor]:
        return self.armor.values()

    def all_shields(self) -> Iterable[Shield]:
        return self.shields.values()

    def all_spells(self) -> Iterable[Spell]:
        return self.spells.values()


# ---------------------------------------------------------------------------
# Default registry
# ---------------------------------------------------------------------------


_DEFAULT_CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"


def default_registry() -> ContentRegistry:
    """Load the bundled content directory."""
    return ContentRegistry.from_directory(_DEFAULT_CONTENT_DIR)
