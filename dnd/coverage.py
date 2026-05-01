"""Source of truth: which PF1 mechanics the engine actually implements.

The companion file ``PF1_COVERAGE.md`` is the human-readable narrative;
this module is what ``tests/test_coverage.py`` reads to enforce that
every mechanic *declared in content* (a monster's racial trait, a
class's class feature, a spell's effect kind, etc.) is either:

  * implemented and known to the tracker, or
  * explicitly recorded here as deferred / out of scope.

If a content addition introduces an ID that isn't in this module, the
test fails. That forces a triage moment: implement it, or write it
down here as deferred (with a note explaining why).

Status meanings:
    IMPLEMENTED      — wired in code, tested.
    PARTIAL          — partially wired; the note describes the gap.
    NOT_IMPLEMENTED  — recognized; engine ignores it for now.
    OUT_OF_SCOPE     — won't implement; reason in the note.
"""

from __future__ import annotations

from typing import Literal

Status = Literal["IMPLEMENTED", "PARTIAL", "NOT_IMPLEMENTED", "OUT_OF_SCOPE"]

IMPLEMENTED: Status = "IMPLEMENTED"
PARTIAL: Status = "PARTIAL"
NOT_IMPLEMENTED: Status = "NOT_IMPLEMENTED"
OUT_OF_SCOPE: Status = "OUT_OF_SCOPE"


Entry = tuple[Status, str]   # (status, note)


# ---------------------------------------------------------------------------
# Player race traits — declared in dnd/content/races/*.json under "traits"
# ---------------------------------------------------------------------------

PLAYER_RACE_TRAITS: dict[str, Entry] = {
    # Halfling
    "fearless":              (NOT_IMPLEMENTED, "+2 morale vs fear effects (situational)"),
    "halfling_luck":         (IMPLEMENTED,     "+1 racial bonus to all saves; via racial_effects.py"),
    "keen_senses_halfling":  (IMPLEMENTED,     "+2 racial Perception; via racial_effects.py"),
    "sure_footed":           (IMPLEMENTED,     "+2 racial Acrobatics/Climb; via racial_effects.py"),
    "weapon_familiarity_halfling": (NOT_IMPLEMENTED,
        "halfling weapons treated as martial; no weapon-familiarity model yet"),

    # Elf
    "elven_immunities":      (NOT_IMPLEMENTED, "+2 vs enchantments, immunity to magic sleep"),
    "elven_magic":           (IMPLEMENTED,     "+2 caster level vs SR + Spellcraft to ID magic items"),
    "keen_senses":           (IMPLEMENTED,     "+2 racial Perception"),
    "weapon_familiarity_elven": (NOT_IMPLEMENTED, "no weapon-familiarity model yet"),

    # Gnome
    "defensive_training_gnome": (NOT_IMPLEMENTED, "+4 dodge AC vs giants (situational)"),
    "gnome_magic":             (NOT_IMPLEMENTED, "1/day SLAs + bonus DC for illusions"),
    "hatred_gnome":            (NOT_IMPLEMENTED, "+1 attack vs reptilian/goblinoid (situational)"),
    "illusion_resistance":     (NOT_IMPLEMENTED, "+2 saves vs illusion (situational)"),
    "keen_senses_gnome":       (IMPLEMENTED,     "+2 racial Perception"),
    "obsessive":               (NOT_IMPLEMENTED, "+2 to a chosen Craft/Profession"),
    "weapon_familiarity_gnome": (NOT_IMPLEMENTED, "no weapon-familiarity model yet"),

    # Half-elf
    "adaptability":          (NOT_IMPLEMENTED, "Skill Focus as bonus feat at L1"),
    "elf_blood":             (OUT_OF_SCOPE,    "tag-only trait, no mechanical effect"),
    "elven_immunities_he":   (NOT_IMPLEMENTED, "same as elven_immunities"),
    "keen_senses_he":        (IMPLEMENTED,     "+2 racial Perception"),
    "multitalented":         (NOT_IMPLEMENTED, "two favored classes; favored-class system not modeled"),

    # Half-orc
    "intimidating":          (IMPLEMENTED,     "+2 racial Intimidate"),
    "orc_blood":             (OUT_OF_SCOPE,    "tag-only trait, no mechanical effect"),
    "orc_ferocity":          (NOT_IMPLEMENTED, "1/day stay-conscious-when-dropped (player version)"),
    "weapon_familiarity_orc": (NOT_IMPLEMENTED, "no weapon-familiarity model yet"),

    # Dwarf
    "defensive_training":    (NOT_IMPLEMENTED, "+4 dodge AC vs giants (situational)"),
    "hardy":                 (NOT_IMPLEMENTED, "+2 vs poison/spells/SLAs (situational)"),
    "hatred":                (NOT_IMPLEMENTED, "+1 attack vs orcs/goblinoids (situational)"),
    "stability":             (NOT_IMPLEMENTED, "+4 CMD vs bull rush/trip while standing on ground"),
    "stonecunning":          (NOT_IMPLEMENTED, "+2 Perception for stonework, automatic check within 10 ft"),
    "weapon_familiarity_dwarven": (NOT_IMPLEMENTED, "no weapon-familiarity model yet"),

    # Human
    "bonus_feat":            (IMPLEMENTED,     "extra L1 feat; factored in character creation"),
    "skilled":               (IMPLEMENTED,     "+1 skill rank/level; factored in character creation"),
}


# ---------------------------------------------------------------------------
# Monster racial traits — declared in dnd/content/monsters/*.json under
# "racial_traits". These are the per-monster special qualities/attacks.
# ---------------------------------------------------------------------------

MONSTER_RACIAL_TRAITS: dict[str, Entry] = {
    # Goblin
    "fast":                  (IMPLEMENTED,     "factored into monster.speed (30 ft) at content time"),
    "skilled_rider":         (OUT_OF_SCOPE,    "+4 Ride on goblin dogs; no Ride/mounted-combat subgame in v1"),

    # Kobold
    "light_sensitivity":     (PARTIAL,         "trait declared; no daylight context in encounters yet, so dormant"),

    # Orc
    "ferocity":              (IMPLEMENTED,     "stay conscious below 0 HP; 1 HP/round bleed; via _apply_post_damage_state"),
    "light_sensitivity_orc": (PARTIAL,         "same as light_sensitivity"),

    # Skeleton
    "undead_traits":         (PARTIAL,         "type='undead' recognized for channel; immunities (mind-affecting, bleed, disease, paralysis, poison, sleep, stun) not enforced — dormant until consumers add those effects"),
    "dr_5_bludgeoning":      (IMPLEMENTED,     "wired via _parse_dr_trait + Combatant.damage_reduction; resolve_attack honors it"),
    "cold_immunity":         (NOT_IMPLEMENTED, "no engine source of cold damage yet; build immunity infra alongside the first cold-damage spell"),

    # Wolf
    "trip_attack":           (NOT_IMPLEMENTED, "free trip on bite hit; needs CMB/CMD trip mechanic"),

    # Zombie
    "undead_traits_zombie":  (PARTIAL,         "same as undead_traits"),
    "dr_5_slashing":         (IMPLEMENTED,     "wired via _parse_dr_trait; resolve_attack honors it"),
}


# ---------------------------------------------------------------------------
# Class features — declared in classes/*.json under level_1.class_features
# ---------------------------------------------------------------------------

CLASS_FEATURES_L1: dict[str, Entry] = {
    # Barbarian
    "fast_movement":         (NOT_IMPLEMENTED, "+10 ft speed (light/no armor); engine doesn't customize speed per class"),
    "rage":                  (IMPLEMENTED,     "rage_start/rage_end composite actions; resource tracked"),

    # Bard
    "bardic_knowledge":      (NOT_IMPLEMENTED, "+1/2 level on Knowledge checks"),
    "bardic_performance":    (PARTIAL,         "Inspire Courage implemented; Countersong, Distraction, Fascinate not"),
    "cantrips_bard":         (NOT_IMPLEMENTED, "0-level spell list"),

    # Cleric
    "aura_cleric":            (OUT_OF_SCOPE,    "tag-only; mostly relevant to Detect Alignment"),
    "channel_energy_1d6":     (IMPLEMENTED,     "channel_energy composite; heal_living/harm_undead modes"),
    "domains":                (NOT_IMPLEMENTED, "domain selection + domain spells/powers"),
    "spontaneous_casting":    (NOT_IMPLEMENTED, "swap prepared slot for cure spell"),
    "orisons":                (NOT_IMPLEMENTED, "0-level spell list"),

    # Druid
    "nature_bond":            (NOT_IMPLEMENTED, "animal companion or domain choice"),
    "nature_sense":           (NOT_IMPLEMENTED, "+2 Knowledge (nature) and Survival"),
    "wild_empathy_druid":     (NOT_IMPLEMENTED, "diplomacy-style check vs animals"),
    "orisons_druid":          (NOT_IMPLEMENTED, "0-level spell list"),

    # Fighter
    "fighter_bonus_combat_feat_1": (IMPLEMENTED, "extra combat feat slot at L1; selected via class_choices"),

    # Monk
    "ac_bonus_monk":          (NOT_IMPLEMENTED, "+Wis to AC + class-level bonus, conditional on no armor"),
    "flurry_of_blows":        (NOT_IMPLEMENTED, "extra unarmed attacks at -2/-2"),
    "stunning_fist_1day":     (PARTIAL,         "resource counter populated; composite action not yet exposed"),
    "unarmed_strike":         (NOT_IMPLEMENTED, "improved unarmed strike auto-feat + scaling damage"),
    "monk_bonus_feat_1":      (IMPLEMENTED,     "extra feat at L1; selected via class_choices"),

    # Paladin
    "aura_of_good":           (OUT_OF_SCOPE,    "tag-only"),
    "detect_evil":            (NOT_IMPLEMENTED, "at-will detect evil"),
    "smite_evil_1day":        (IMPLEMENTED,     "smite_evil composite; resource tracked"),

    # Ranger
    "first_favored_enemy":    (NOT_IMPLEMENTED, "+2 attack/damage/skills vs chosen creature type"),
    "track":                  (NOT_IMPLEMENTED, "+1/2 level to Survival for tracking"),
    "wild_empathy_ranger":    (NOT_IMPLEMENTED, "diplomacy-style check vs animals"),

    # Rogue
    "sneak_attack_1d6":       (IMPLEMENTED,     "precision damage when target denied Dex / flanked"),
    "trapfinding":            (NOT_IMPLEMENTED, "+1/2 level Perception/Disable Device for traps"),

    # Sorcerer
    "bloodline":              (NOT_IMPLEMENTED, "bloodline selection + powers + bonus spells"),
    "eschew_materials":       (IMPLEMENTED,     "passive feat (no material components for cheap spells)"),
    "cantrips_sorcerer":      (NOT_IMPLEMENTED, "0-level at-will spells"),

    # Wizard
    "arcane_school":          (NOT_IMPLEMENTED, "school specialization + bonus slots + powers"),
    "arcane_bond":             (NOT_IMPLEMENTED, "bonded item or familiar"),
    "scribe_scroll":           (NOT_IMPLEMENTED, "item creation feat — crafting deferred to Phase 4"),
    "cantrips_wizard":         (NOT_IMPLEMENTED, "0-level prepared spells"),
}


# ---------------------------------------------------------------------------
# Conditions — declared in dnd/content/conditions/conditions.json
# A condition is "implemented" when the engine actually changes behavior
# based on it being set (validation, modifiers, action restrictions).
# ---------------------------------------------------------------------------

CONDITIONS: dict[str, Entry] = {
    "bleed":           (NOT_IMPLEMENTED, "ferocity bleed is hand-rolled; no generic bleed system"),
    "blinded":         (PARTIAL,         "denies Dex to AC (via _SNEAK_ATTACK_DENY_DEX_CONDITIONS); 50% miss chance not modeled"),
    "confused":        (NOT_IMPLEMENTED, "random action table"),
    "cowering":        (PARTIAL,         "denies Dex (sneak attack qualifies); other restrictions not modeled"),
    "dazed":           (NOT_IMPLEMENTED, "no actions but defenses normal"),
    "dazzled":         (NOT_IMPLEMENTED, "-1 attack rolls; required for light sensitivity"),
    "deafened":        (NOT_IMPLEMENTED, "-4 initiative; 20% spell failure for verbal"),
    "dead":            (IMPLEMENTED,     "set by _apply_post_damage_state; turn validation prevents acts"),
    "disabled":        (NOT_IMPLEMENTED, "0 HP exactly; one move OR standard"),
    "dying":           (IMPLEMENTED,     "set by _apply_post_damage_state at HP <= 0; deployment marks DEAD on encounter end if hero is dying"),
    "energy_drained":  (NOT_IMPLEMENTED, "negative levels"),
    "entangled":       (NOT_IMPLEMENTED, "-2 attack, -4 Dex, can't run/charge"),
    "exhausted":       (NOT_IMPLEMENTED, "-6 Str/Dex, 1/2 speed"),
    "fascinated":      (NOT_IMPLEMENTED, "no actions; -4 perception"),
    "fatigued":        (PARTIAL,         "set as side-effect of rage_end; doesn't apply -2 Str/Dex penalty yet"),
    "flat_footed":     (IMPLEMENTED,     "AC variant computed; sneak attack qualifies"),
    "frightened":      (NOT_IMPLEMENTED, "-2 attack/save/skill; must flee"),
    "grappled":        (PARTIAL,         "validation prevents some actions; full grappling rules not modeled"),
    "helpless":        (PARTIAL,         "denies Dex (sneak attack qualifies); coup-de-grace not modeled"),
    "incorporeal":     (NOT_IMPLEMENTED, "ghost/shadow attack rules"),
    "invisible":       (NOT_IMPLEMENTED, "+2 attack, denies Dex; 50% miss for attackers"),
    "nauseated":       (NOT_IMPLEMENTED, "only move actions"),
    "panicked":        (NOT_IMPLEMENTED, "drop items, flee"),
    "paralyzed":       (PARTIAL,         "denies Dex (sneak attack qualifies); turn validation prevents acts; helpless follow-on not modeled"),
    "petrified":       (PARTIAL,         "turn validation prevents physical acts; helpless follow-on not modeled"),
    "pinned":          (PARTIAL,         "denies Dex (sneak attack qualifies); pinned action set not modeled"),
    "prone":           (PARTIAL,         "stand_up move action exists; -4 melee attack / +4 AC vs ranged not applied"),
    "shaken":          (NOT_IMPLEMENTED, "-2 attack/save/skill"),
    "sickened":        (NOT_IMPLEMENTED, "-2 attack/damage/save/skill"),
    "sleeping":        (PARTIAL,         "denies Dex (sneak attack qualifies); helpless follow-on not modeled"),
    "squeezing":       (OUT_OF_SCOPE,    "rare; deferred indefinitely"),
    "stable":          (NOT_IMPLEMENTED, "stops dying HP loss"),
    "staggered":       (PARTIAL,         "encounter validation prevents combining move + standard; ferocity sets it"),
    "stunned":         (PARTIAL,         "denies Dex (sneak attack qualifies); drops held items, no actions for 1 round"),
    "unconscious":     (PARTIAL,         "is_unconscious checks the condition; turn validation prevents acts"),
}


# ---------------------------------------------------------------------------
# Feats — declared in dnd/content/feats/feats.json
# A feat is "implemented" if it has effect in the engine (passive
# modifiers via feat_effects.py OR active wiring in turn_executor).
# ---------------------------------------------------------------------------

FEATS: dict[str, Entry] = {
    "alertness":             (IMPLEMENTED,     "+2 perception/sense_motive"),
    "athletic":              (IMPLEMENTED,     "+2 climb/swim"),
    "cleave":                (IMPLEMENTED,     "composite action; -2 AC for the round"),
    "combat_expertise":      (IMPLEMENTED,     "attack-time tradeoff; 1-round dodge AC"),
    "combat_reflexes":       (NOT_IMPLEMENTED, "extra AoOs/round = Dex mod; only 1 AoO/round modeled"),
    "diehard":               (NOT_IMPLEMENTED, "act normally while dying"),
    "dodge":                 (IMPLEMENTED,     "+1 dodge AC"),
    "empower_spell":         (NOT_IMPLEMENTED, "metamagic: +50% damage/heal at +2 spell level"),
    "endurance":             (NOT_IMPLEMENTED, "+4 to various endurance-related checks"),
    "eschew_materials":      (NOT_IMPLEMENTED, "skip cheap material components"),
    "great_fortitude":       (IMPLEMENTED,     "+2 fort save"),
    "improved_initiative":   (IMPLEMENTED,     "+4 initiative"),
    "improved_unarmed_strike": (NOT_IMPLEMENTED, "treats unarmed as armed; lethal damage option"),
    "iron_will":             (IMPLEMENTED,     "+2 will save"),
    "lightning_reflexes":    (IMPLEMENTED,     "+2 ref save"),
    "persuasive":            (IMPLEMENTED,     "+2 diplomacy/intimidate"),
    "point_blank_shot":      (IMPLEMENTED,     "+1 attack/damage with ranged"),
    "power_attack":          (IMPLEMENTED,     "attack-time tradeoff; wield-scaled damage bonus"),
    "precise_shot":          (NOT_IMPLEMENTED, "no -4 firing into melee"),
    "rapid_shot":            (NOT_IMPLEMENTED, "extra ranged attack at -2/-2"),
    "run":                   (NOT_IMPLEMENTED, "x4 speed for run action"),
    "scribe_scroll":         (NOT_IMPLEMENTED, "crafting feat — deferred to Phase 4"),
    "skill_focus":           (IMPLEMENTED,     "+3 to chosen skill (parametric)"),
    "spell_focus":           (IMPLEMENTED,     "+1 DC to chosen school (parametric)"),
    "spell_penetration":     (IMPLEMENTED,     "+2 caster level vs SR"),
    "stealthy":              (IMPLEMENTED,     "+2 stealth/escape_artist"),
    "toughness":             (IMPLEMENTED,     "+max(3, level) hp_max"),
    "two_weapon_fighting":   (NOT_IMPLEMENTED, "extra off-hand attack with reduced penalties"),
    "weapon_finesse":        (IMPLEMENTED,     "use Dex for melee attack rolls; via combatant.is_finesse path"),
    "weapon_focus":          (IMPLEMENTED,     "+1 attack with chosen weapon (parametric)"),
}


# ---------------------------------------------------------------------------
# Spell effect kinds — declared in dnd/content/spells/spells.json under
# "effect.kind". A kind is "implemented" if there's a matching handler
# in spells._EFFECT_HANDLERS.
# ---------------------------------------------------------------------------

SPELL_EFFECT_KINDS: dict[str, Entry] = {
    "apply_condition_save":  (IMPLEMENTED, "save-or-be-condition (e.g., color spray)"),
    "buff_party":            (IMPLEMENTED, "AoE party buff"),
    "buff_target":           (IMPLEMENTED, "single-target buff with duration"),
    "charm":                 (IMPLEMENTED, "shift attitude/control via Will save"),
    "heal":                  (IMPLEMENTED, "restore HP"),
    "magic_missile":         (IMPLEMENTED, "auto-hit force damage with multi-missile"),
    "scaling_damage":        (IMPLEMENTED, "AoE damage scaling with caster level (e.g., fireball)"),
    "stabilize":             (IMPLEMENTED, "stop dying HP loss"),
    "utility":               (IMPLEMENTED, "no mechanical effect; flavor / GM-call"),
}


# ---------------------------------------------------------------------------
# Top-level lookup helper
# ---------------------------------------------------------------------------


CATEGORIES: dict[str, dict[str, Entry]] = {
    "player_race_traits":    PLAYER_RACE_TRAITS,
    "monster_racial_traits": MONSTER_RACIAL_TRAITS,
    "class_features_l1":     CLASS_FEATURES_L1,
    "conditions":            CONDITIONS,
    "feats":                 FEATS,
    "spell_effect_kinds":    SPELL_EFFECT_KINDS,
}


def status_for(category: str, item_id: str) -> Entry | None:
    """Look up the (status, note) for an item, or None if unknown."""
    return CATEGORIES.get(category, {}).get(item_id)


def declared_ids(category: str) -> set[str]:
    """All IDs the tracker knows about for a category."""
    return set(CATEGORIES.get(category, {}).keys())
