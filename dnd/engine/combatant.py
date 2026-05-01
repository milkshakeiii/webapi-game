"""The runtime view of a participant in combat.

A ``Combatant`` is the *mutable* view that lives on the grid: HP, active
conditions, position, expended-resource counters, and the modifier
collection that drives every derived stat. Static data — race, class,
level-up plan, monster template — is referenced via ``template``; the
Combatant never mutates it.

Two factories build Combatants:

- ``combatant_from_monster(monster, position, team)`` — full-featured;
  monsters carry their full stat block in content.
- ``combatant_from_character(character, registry, position, team)`` —
  partial; awaits the equipment catalog before attack options can be
  computed automatically.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from .characters import (
    AbilityScores,
    Character,
    apply_racial_modifiers,
    racial_ability_modifiers,
)
from .combat import DefenseProfile
from .content import ContentRegistry, Monster
from .modifiers import Modifier, ModifierCollection, compute, mod
from .sizes import get_size, size_modifiers


# ---------------------------------------------------------------------------
# Combatant
# ---------------------------------------------------------------------------


# Filters used to derive situational AC values.
_TOUCH_EXCLUDED_TYPES = frozenset({"armor", "shield", "natural"})


@dataclass
class Combatant:
    """Runtime state for a single combat participant."""

    id: str
    name: str
    team: str             # for friend/foe checks; same team = ally
    size: str
    speed: int            # base land speed in feet
    reach_class: str      # "tall" or "long" — determines natural reach

    # Bases are inherent values for this combatant, before any typed
    # modifiers apply. Examples: AC base is 10; CMD base is 10 + BAB;
    # CMB base is BAB.
    bases: dict[str, int]

    # Every typed modifier from race, class, equipment, conditions,
    # spells, etc. is in here.
    modifiers: ModifierCollection

    # Pre-built attack options. For monsters these come from the JSON
    # stat block; for characters they're computed from equipment (TBD).
    attack_options: list[dict]

    # Mutable state.
    current_hp: int
    max_hp: int
    position: tuple[int, int]
    facing: str = "north"
    conditions: set[str] = field(default_factory=set)
    resources: dict[str, int] = field(default_factory=dict)

    # Reference back to the source data.
    template_kind: str = "unknown"   # "monster" or "character"
    template: Any = None             # Monster or Character

    # Spells the combatant can cast (filtered to their class list at
    # levels they have slots for). Empty for non-casters and monsters.
    castable_spells: set[str] = field(default_factory=set)

    # Smite target id (paladin Smite Evil declared target). Empty when none.
    smite_target_id: str | None = None

    # ── Derived stat queries ──────────────────────────────────────────────

    def ac(self, situation: str = "normal") -> int:
        """Return AC for the given situation: ``normal``, ``touch``, or
        ``flat_footed``."""
        mods = list(self.modifiers.for_target("ac"))
        if situation == "touch":
            mods = [m for m in mods if m.type not in _TOUCH_EXCLUDED_TYPES]
        elif situation == "flat_footed":
            mods = [
                m for m in mods
                if m.type != "dodge" and "dex" not in m.source.lower()
            ]
        elif situation != "normal":
            raise ValueError(f"unknown AC situation {situation!r}")
        return compute(self.bases.get("ac", 10), mods)

    def save(self, kind: str) -> int:
        """Return Fort/Ref/Will save total."""
        if kind not in ("fort", "ref", "will"):
            raise ValueError(f"unknown save kind {kind!r}")
        target = f"{kind}_save"
        return compute(self.bases.get(target, 0), self.modifiers.for_target(target))

    def cmb(self) -> int:
        return compute(self.bases.get("cmb", 0), self.modifiers.for_target("cmb"))

    def cmd(self) -> int:
        return compute(self.bases.get("cmd", 10), self.modifiers.for_target("cmd"))

    def skill_total(self, skill_id: str) -> int:
        target = f"skill:{skill_id}"
        return compute(0, self.modifiers.for_target(target))

    def initiative_modifier(self) -> int:
        return compute(self.bases.get("initiative", 0),
                       self.modifiers.for_target("initiative"))

    def defense_profile(self) -> DefenseProfile:
        """Bundle the AC values for combat resolution."""
        return DefenseProfile(
            ac=self.ac("normal"),
            touch_ac=self.ac("touch"),
            flat_footed_ac=self.ac("flat_footed"),
            dr=None,  # DR support comes when conditions/equipment do.
        )

    @property
    def hp_pct(self) -> float:
        return (self.current_hp / self.max_hp) if self.max_hp else 0.0

    # ── Liveness ──────────────────────────────────────────────────────────

    def is_alive(self) -> bool:
        return "dead" not in self.conditions

    def is_dying(self) -> bool:
        return "dying" in self.conditions

    def is_unconscious(self) -> bool:
        return "unconscious" in self.conditions or "dying" in self.conditions

    # ── Mutations ─────────────────────────────────────────────────────────

    def take_damage(self, amount: int) -> None:
        if amount < 0:
            raise ValueError(f"damage must be >= 0, got {amount}")
        self.current_hp -= amount

    def heal(self, amount: int) -> None:
        if amount < 0:
            raise ValueError(f"heal must be >= 0, got {amount}")
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def add_condition(self, condition_id: str) -> None:
        self.conditions.add(condition_id)

    def remove_condition(self, condition_id: str) -> None:
        self.conditions.discard(condition_id)

    def add_modifier(self, modifier: Modifier) -> None:
        self.modifiers.add(modifier)

    def remove_modifiers_from_source(self, source: str) -> int:
        return self.modifiers.remove_by_source(source)

    def tick_round(self, current_round: int) -> list[Modifier]:
        """Drop any modifiers whose duration has elapsed at this round."""
        return self.modifiers.prune_expired(current_round)


# ---------------------------------------------------------------------------
# Factories
# ---------------------------------------------------------------------------


def _new_id() -> str:
    return f"combatant_{uuid.uuid4().hex[:8]}"


# Map keys in monster.ac dict → modifier types.
_AC_KEY_TO_TYPE: dict[str, str] = {
    "armor":      "armor",
    "shield":     "shield",
    "natural":    "natural",
    "deflection": "deflection",
    "dodge":      "dodge",
    "size":       "size",
    "dex":        "ability",  # Dex is an ability mod, not a typed combat bonus
}


def combatant_from_monster(
    monster: Monster,
    position: tuple[int, int],
    team: str,
    *,
    name: str | None = None,
) -> Combatant:
    """Build a Combatant from a monster template.

    Monsters' stat blocks are pre-computed: HP, AC components, saves,
    attacks all come straight from the JSON. We unpack the AC
    breakdown into typed modifiers so that situational AC (touch /
    flat-footed) can be computed by filtering them.
    """
    coll = ModifierCollection()
    source_prefix = f"monster:{monster.id}"

    # Unpack AC modifiers from the breakdown dict.
    for key, value in monster.ac.items():
        if key in ("total", "touch", "flat_footed"):
            continue
        if value == 0:
            continue
        mod_type = _AC_KEY_TO_TYPE.get(key, "untyped")
        if key == "dex":
            coll.add(mod(int(value), mod_type, "ac", f"{source_prefix}:dex_modifier"))
        else:
            coll.add(mod(int(value), mod_type, "ac", f"{source_prefix}:{key}"))

    # Initiative bonus comes from the JSON's `init` field.
    if monster.init != 0:
        coll.add(mod(monster.init, "untyped", "initiative",
                     f"{source_prefix}:init"))

    # Skills: each entry's value is the full skill total. Treat as
    # untyped modifier so skill_total() returns the JSON number.
    for skill_id, total in monster.skills.items():
        if total != 0:
            coll.add(mod(int(total), "untyped", f"skill:{skill_id}",
                         f"{source_prefix}:skill_block"))

    return Combatant(
        id=_new_id(),
        name=name or monster.name,
        team=team,
        size=monster.size,
        speed=monster.speed,
        reach_class="tall" if monster.size in ("medium", "small") else _infer_reach_class(monster),
        bases={
            "ac":        10,
            "fort_save": int(monster.saves.get("fort", 0)),
            "ref_save":  int(monster.saves.get("ref",  0)),
            "will_save": int(monster.saves.get("will", 0)),
            "bab":       monster.bab,
            "cmb":       monster.cmb,
            "cmd":       monster.cmd,
            "initiative": 0,  # already added as a modifier above
        },
        modifiers=coll,
        attack_options=[dict(a) for a in monster.attacks],
        current_hp=monster.hp,
        max_hp=monster.hp,
        position=position,
        conditions=set(monster.permanent_conditions),
        resources={},
        template_kind="monster",
        template=monster,
    )


def _infer_reach_class(monster: Monster) -> str:
    """Heuristic for monster reach class.

    PF1 doesn't store this on stat blocks directly; we guess from type.
    Animals, oozes, vermin tend to be 'long'. Humanoids and giants are
    'tall'. For v1 this is approximate; we'll annotate templates later
    if it matters.
    """
    if monster.type in ("animal", "vermin", "ooze"):
        return "long"
    return "tall"


def combatant_from_hero_record(
    hero_record,
    registry: ContentRegistry,
    position: tuple[int, int],
    team: str,
) -> Combatant:
    """Materialize a Combatant for a deployment from a sandbox HeroRecord.

    The HeroRecord carries the static ``Character`` plus carry-over
    state (current HP from prior deployments, etc.). This factory
    builds a fresh combat-ready combatant honoring that carry-over.
    """
    c = combatant_from_character(
        hero_record.character, registry, position, team,
    )
    # Honor carried HP if the record has been initialized; otherwise
    # the character's max_hp as set by the engine is the right starting
    # value (used at first spawn).
    if hero_record.current_hp > 0:
        c.current_hp = min(hero_record.current_hp, c.max_hp)
    # Cache max_hp on the record for UI; persisted on next save.
    hero_record.max_hp = c.max_hp
    if hero_record.current_hp <= 0:
        hero_record.current_hp = c.max_hp
    return c


def combatant_from_character(
    character: Character,
    registry: ContentRegistry,
    position: tuple[int, int],
    team: str,
) -> Combatant:
    """Build a Combatant from a character, including equipped gear and
    multi-level progression if the character has a level plan."""
    race = registry.get_race(character.race_id)
    class_ = registry.get_class(character.class_id)

    # Walk the level-up plan (or trivially construct L1 state) to get
    # cumulative HP, BAB, saves, feats, skill ranks, and ability bumps.
    from .level_plan import LevelUpPlan
    from .leveling import apply_plan
    if character.level_plan and character.level > 1:
        plan = LevelUpPlan.from_dict(character.level_plan)
    else:
        plan = LevelUpPlan(name="<l1>", target_level=1, levels={})
    cumulative = apply_plan(
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

    coll = ModifierCollection()

    coll.add_many(racial_ability_modifiers(race, character.free_ability_choice))
    coll.add_many(size_modifiers(race.size))

    # Racial trait passive modifiers (e.g., Halfling Luck, Keen Senses).
    from .racial_effects import racial_modifiers as _race_mods
    coll.add_many(_race_mods(race))

    # Per-feat passive modifiers (e.g., Toughness, Dodge, Skill Focus).
    from .feat_effects import feat_modifiers as _feat_mods
    for fid in character.feats:
        coll.add_many(_feat_mods(fid, character))

    final_scores: AbilityScores = cumulative.final_ability_scores

    str_mod = final_scores.modifier("str")
    dex_mod = final_scores.modifier("dex")
    con_mod = final_scores.modifier("con")
    wis_mod = final_scores.modifier("wis")

    # ── Equipment lookups ─────────────────────────────────────────────────
    armor_data = None
    if character.equipped_armor and character.equipped_armor != "none":
        armor_data = registry.get_armor(character.equipped_armor)
    shield_data = None
    if character.equipped_shield:
        shield_data = registry.get_shield(character.equipped_shield)
    weapon_data = None
    if character.equipped_weapon:
        weapon_data = registry.get_weapon(character.equipped_weapon)

    # ── AC: Dex (capped by armor), armor bonus, shield bonus ──────────────
    ac_dex_mod = dex_mod
    if armor_data is not None and armor_data.max_dex_bonus < dex_mod:
        ac_dex_mod = armor_data.max_dex_bonus
    if ac_dex_mod != 0:
        coll.add(mod(ac_dex_mod, "ability", "ac", "dex_modifier"))
    if armor_data is not None and armor_data.ac_bonus > 0:
        coll.add(mod(armor_data.ac_bonus, "armor", "ac",
                     f"armor:{armor_data.id}"))
    if shield_data is not None and shield_data.ac_bonus > 0:
        coll.add(mod(shield_data.ac_bonus, "shield", "ac",
                     f"shield:{shield_data.id}"))

    # Saves: Fort gets Con, Ref gets Dex, Will gets Wis.
    if con_mod != 0:
        coll.add(mod(con_mod, "ability", "fort_save", "con_modifier"))
    if dex_mod != 0:
        coll.add(mod(dex_mod, "ability", "ref_save", "dex_modifier"))
    if wis_mod != 0:
        coll.add(mod(wis_mod, "ability", "will_save", "wis_modifier"))

    # CMB / CMD.
    if str_mod != 0:
        coll.add(mod(str_mod, "ability", "cmb", "str_modifier"))
        coll.add(mod(str_mod, "ability", "cmd", "str_modifier"))
    if dex_mod != 0:
        coll.add(mod(dex_mod, "ability", "cmd", "dex_modifier"))

    # Initiative: Dex.
    if dex_mod != 0:
        coll.add(mod(dex_mod, "ability", "initiative", "dex_modifier"))

    # Skills: cumulative ranks + class skill bonus + ability modifier + ACP.
    class_skills = set(class_.level_1.class_skills)
    for cid in cumulative.class_levels:
        if cid != class_.id:
            try:
                class_skills.update(registry.get_class(cid).level_1.class_skills)
            except Exception:
                pass
    for skill_id, ranks in cumulative.skill_ranks.items():
        if ranks <= 0:
            continue
        try:
            skill = registry.get_skill(skill_id)
        except KeyError:
            continue
        coll.add(mod(ranks, "untyped", f"skill:{skill_id}", "ranks"))
        ab = final_scores.modifier(skill.ability)
        if ab != 0:
            coll.add(mod(ab, "ability", f"skill:{skill_id}",
                         f"{skill.ability}_modifier"))
        if skill_id in class_skills:
            coll.add(mod(3, "untyped", f"skill:{skill_id}", "class_skill_bonus"))
        # Armor check penalty applies to a known set of skills.
        if skill.armor_check_penalty:
            acp = 0
            if armor_data is not None:
                acp += armor_data.armor_check_penalty
            if shield_data is not None:
                acp += shield_data.armor_check_penalty
            if acp < 0:
                coll.add(mod(acp, "untyped", f"skill:{skill_id}",
                             "armor_check_penalty"))

    # ── Attack options from equipped weapon ───────────────────────────────
    attack_options: list[dict] = []
    if weapon_data is not None:
        size_data = get_size(race.size)
        size_mod_atk = size_data.ac_attack_mod
        bab = cumulative.bab
        if weapon_data.is_melee:
            ability_mod = (max(str_mod, dex_mod)
                           if weapon_data.is_finesse else str_mod)
            attack_bonus = bab + ability_mod + size_mod_atk
            if weapon_data.wield == "two_handed":
                damage_bonus = (str_mod * 3) // 2
            else:
                damage_bonus = str_mod
            attack_type = "melee"
        else:
            attack_bonus = bab + dex_mod + size_mod_atk
            damage_bonus = 0
            attack_type = "ranged"
        attack_options.append({
            "type": attack_type,
            "name": weapon_data.name,
            "weapon_id": weapon_data.id,
            "attack_bonus": attack_bonus,
            "damage": weapon_data.damage_dice,
            "damage_bonus": damage_bonus,
            "damage_type": weapon_data.damage_type,
            "crit_range": list(weapon_data.crit_range),
            "crit_multiplier": weapon_data.crit_multiplier,
            "range_increment": weapon_data.range_increment,
            "wield": weapon_data.wield,
        })

    # HP from cumulative HD + Con; add any hp_max modifiers (Toughness etc).
    from .modifiers import compute as _compute
    hp_max = cumulative.hp_max + _compute(0, coll.for_target("hp_max"))
    bab = cumulative.bab

    # Populate castable spells based on class + level.
    castable: set[str] = set()
    if cumulative.spells_per_day:
        max_castable_level = max(
            (int(k) for k, v in cumulative.spells_per_day.items()
             if (isinstance(v, int) and v > 0) or v == "at_will"),
            default=0,
        )
        for sid, spell in registry.spells.items():
            if class_.id in spell.level_by_class:
                if spell.level_by_class[class_.id] <= max_castable_level:
                    castable.add(sid)
            # Multiclass casters: also include spells from other caster classes.
            for cid in cumulative.class_levels:
                if cid != class_.id and cid in spell.level_by_class:
                    castable.add(sid)
    # Slot resources keyed by spell level.
    spell_slot_resources: dict[str, int] = {}
    if cumulative.spells_per_day:
        for slvl, count in cumulative.spells_per_day.items():
            if isinstance(count, int):
                spell_slot_resources[f"spell_slot_{slvl}"] = count

    # Class-specific per-day / per-encounter pools.
    cha_mod = final_scores.modifier("cha")
    barbarian_levels = cumulative.class_levels.get("barbarian", 0)
    paladin_levels = cumulative.class_levels.get("paladin", 0)
    cleric_levels = cumulative.class_levels.get("cleric", 0)
    bard_levels = cumulative.class_levels.get("bard", 0)
    monk_levels = cumulative.class_levels.get("monk", 0)
    if barbarian_levels > 0:
        # Rage rounds: 4 + Con + 2/level beyond 1st.
        spell_slot_resources["rage_rounds"] = (
            4 + con_mod + 2 * max(0, barbarian_levels - 1)
        )
    if paladin_levels > 0:
        # Smite Evil: 1/day at L1, +1 every 3 levels.
        spell_slot_resources["smite_evil_uses"] = 1 + (paladin_levels - 1) // 3
    if cleric_levels > 0:
        # Channel Energy: 3 + Cha mod per day.
        spell_slot_resources["channel_uses"] = max(0, 3 + cha_mod)
    if bard_levels > 0:
        # Bardic Performance: 4 + Cha + 2/level beyond 1st rounds/day.
        spell_slot_resources["performance_rounds"] = (
            4 + cha_mod + 2 * max(0, bard_levels - 1)
        )
    if monk_levels > 0:
        # Stunning Fist: monk level + 1 (other classes can have it via feat).
        spell_slot_resources["stunning_fist_uses"] = monk_levels

    return Combatant(
        id=_new_id(),
        name=character.name,
        team=team,
        size=race.size,
        speed=race.speed,
        reach_class="tall",
        bases={
            "ac":        10,
            "fort_save": int(cumulative.saves.get("fort", 0)),
            "ref_save":  int(cumulative.saves.get("ref",  0)),
            "will_save": int(cumulative.saves.get("will", 0)),
            "bab":       bab,
            "cmb":       bab,       # size & ability via modifiers
            "cmd":       10 + bab,  # size, Str, Dex via modifiers
            "initiative": 0,
        },
        modifiers=coll,
        attack_options=attack_options,
        current_hp=hp_max,
        max_hp=hp_max,
        position=position,
        conditions=set(),
        resources=spell_slot_resources,
        template_kind="character",
        template=character,
        castable_spells=castable,
    )
