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
    "defensive_training_gnome": (IMPLEMENTED,    "+4 dodge AC vs giants via qualifier-on-modifier"),
    "gnome_magic":             (NOT_IMPLEMENTED, "1/day SLAs + bonus DC for illusions"),
    "hatred_gnome":            (IMPLEMENTED,     "+1 attack vs reptilian/goblinoid via qualifier"),
    "illusion_resistance":     (IMPLEMENTED,     "+2 saves vs illusion school via qualifier; spell handlers pass effect_tags=[school] context"),
    "keen_senses_gnome":       (IMPLEMENTED,     "+2 racial Perception"),
    "obsessive":               (NOT_IMPLEMENTED, "+2 to a chosen Craft/Profession"),
    "weapon_familiarity_gnome": (NOT_IMPLEMENTED, "no weapon-familiarity model yet"),

    # Half-elf
    "adaptability":          (IMPLEMENTED,     "auto-adds skill_focus_<skill> at L1; configurable via CharacterRequest.adaptability_skill_focus, defaults to perception"),
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
    "defensive_training":    (IMPLEMENTED,     "+4 dodge AC vs giants via qualifier-on-modifier; checked at attack-resolution time"),
    "hardy":                 (IMPLEMENTED,     "+2 saves vs spells/poisons/SLAs via qualifier; spell saves pass effect_tags=['spell',school] context"),
    "hatred":                (IMPLEMENTED,     "+1 attack vs orcs/goblinoids via qualifier on the actor's 'attack' modifier"),
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
    "undead_traits":         (PARTIAL,         "type='undead' recognized for channel; bleed immunity wired in tick_round; condition immunities (mind-affecting / paralysis / sleep / stun / fatigue / nausea / fear / etc.) wired via Combatant.add_condition immunity check; disease/poison effect-types not yet modeled (no consumers)"),
    "dr_5_bludgeoning":      (IMPLEMENTED,     "wired via _parse_dr_trait + Combatant.damage_reduction; resolve_attack honors it"),
    "cold_immunity":         (NOT_IMPLEMENTED, "no engine source of cold damage yet; build immunity infra alongside the first cold-damage spell"),

    # Wolf
    "trip_attack":           (NOT_IMPLEMENTED, "free trip on bite hit; needs CMB/CMD trip mechanic"),

    # Zombie
    "undead_traits_zombie":  (PARTIAL,         "same as undead_traits — same immunity set wired"),
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
    "stunning_fist_1day":     (IMPLEMENTED,     "stunning_fist composite: declares + attacks; on hit target rolls Fort vs DC 10 + 1/2 level + Wis or stunned 1 round; use consumed regardless of hit"),
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
    "prone":           (IMPLEMENTED,     "fall_prone free action applies the condition; stand_up move action provokes AoO from threateners; -4 melee attacker, +4 melee-attacker-vs-target, -4 ranged-attacker-vs-target wired in _do_attack"),
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
    "combat_reflexes":       (IMPLEMENTED,     "AoO limit = 1 + Dex (min 1) when feat present; throttled per-round in _do_aoo via Combatant.aoos_used_this_round"),
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
    "precise_shot":          (IMPLEMENTED,     "negates the -4 firing-into-melee penalty in _firing_into_melee_penalty"),
    "rapid_shot":            (IMPLEMENTED,     "extra ranged attack at top BAB; -2 to all attacks this round; via _do_full_attack with options.rapid_shot=true"),
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
# Core mechanics — base rules that apply to everyone, not declared as
# content items.
#
# These rules live in the SRD chapter prose (Combat, Magic, Skills,
# Equipment, Adventuring), not as YAML in any pack. Keys are dotted
# (e.g., ``combat.charge``); the human-readable narrative is in
# ``PF1_COVERAGE.md``.
#
# Unlike other categories, this one has NO content-side scanner — we
# can't auto-detect omissions from this list. Discipline: when a new
# base rule comes up in playtest or implementation, add it here.
# ---------------------------------------------------------------------------

CORE_MECHANICS: dict[str, Entry] = {
    # ── Combat: turn structure & action economy ──────────────────────────
    "combat.initiative":             (IMPLEMENTED,    "d20 + Dex; encounter.roll_initiative"),
    "combat.surprise_round":         (NOT_IMPLEMENTED, "no surprise mechanic; all combatants act from round 1"),
    "combat.action_types":           (IMPLEMENTED,    "Turn slots cover standard/move/swift/free/full_round/5ft_step"),
    "combat.5_foot_step":            (IMPLEMENTED,    "validate_turn enforces exclusivity; one square only"),
    "combat.full_round_action":      (IMPLEMENTED,    "Turn.full_round forbids standard+move; charge/withdraw/full_attack are full-round"),
    "combat.swift_action":           (PARTIAL,        "Turn.swift slot exists but most consumers (smite_evil, etc.) call it composite — minor; immediate-action conversion not modeled"),
    "combat.free_action":            (PARTIAL,        "validation accepts a fixed allowlist (drop_item, fall_prone, speak, signal, end_concentration, drop_held_charge); not all RAW free actions enumerated"),
    "combat.immediate_action":       (NOT_IMPLEMENTED, "consumes next round's swift; no model"),

    # ── Combat: attack rolls & critical hits ────────────────────────────
    "combat.attack_roll":            (IMPLEMENTED,    "d20 + bonuses; nat 1 auto-miss; nat 20 auto-hit"),
    "combat.iterative_attacks":      (IMPLEMENTED,    "BAB-scaled in _do_full_attack: 1@BAB1-5, 2@6-10, 3@11-15, 4@16+"),
    "combat.crit_threat_and_confirm": (IMPLEMENTED,   "weapon crit_range threats; confirmation roll same bonuses; nat 1 fails confirm"),
    "combat.crit_multiplier":        (IMPLEMENTED,    "damage_roll multiplies dice + static bonus by weapon's crit_multiplier"),
    "combat.precision_damage":       (IMPLEMENTED,    "AttackProfile.precision_damage_dice rolled separately, NOT multiplied on crit"),
    "combat.touch_attack":           (IMPLEMENTED,    "AC variant via defense_profile().touch_ac"),
    "combat.ranged_touch_attack":    (IMPLEMENTED,    "same touch AC; range increment not yet enforced"),
    "combat.flat_footed_ac":         (IMPLEMENTED,    "AC variant via defense_profile().flat_footed_ac"),

    # ── Combat: damage, DR, energy ──────────────────────────────────────
    "combat.dr_application":         (IMPLEMENTED,    "_apply_dr in combat.py; bypass keywords (S/P/B/silver/magic/etc.); first-DR-wins on multi-DR creatures (rare today)"),
    "combat.dr_multi_keyword":       (NOT_IMPLEMENTED, "DR 10/silver and magic — bypass-keyword set is OR; AND semantics needed"),
    "combat.energy_damage":          (NOT_IMPLEMENTED, "no engine source of fire/cold/electricity/acid/sonic damage yet"),
    "combat.energy_resistance":      (NOT_IMPLEMENTED, "no consumers — pair with first energy-damage spell"),
    "combat.energy_immunity":        (NOT_IMPLEMENTED, "same"),
    "combat.bleed_damage":           (PARTIAL,        "ferocity-bleed implemented in tick_round; no generic bleed-condition system"),
    "combat.nonlethal_damage":       (NOT_IMPLEMENTED, "no separate nonlethal HP track"),

    # ── Combat: defenses, cover, concealment, flanking ───────────────────
    "combat.cover":                  (PARTIAL,        "hard cover (+4 AC) wired via _cover_ac_bonus + Bresenham; +2 Reflex bonus not yet applied (no consumer cares yet)"),
    "combat.greater_cover":          (NOT_IMPLEMENTED, "+8 AC, +4 Reflex; needs 'majority of line blocked' detection"),
    "combat.soft_cover":             (IMPLEMENTED,    "intervening combatant grants +4 AC vs ranged via _cover_ac_bonus"),
    "combat.total_cover":            (NOT_IMPLEMENTED, "blocks line of effect entirely; needs spell-targeting check"),
    "combat.concealment":            (NOT_IMPLEMENTED, "20% miss chance"),
    "combat.total_concealment":      (NOT_IMPLEMENTED, "50% miss chance"),
    "combat.flanking":               (IMPLEMENTED,    "+2 attack to both flankers; grid.is_flanked_by + _flanking_attack_bonus"),
    "combat.higher_ground":          (NOT_IMPLEMENTED, "+1 attack from above"),

    # ── Combat: AoOs ────────────────────────────────────────────────────
    "combat.aoo":                    (IMPLEMENTED,    "1 AoO/round; aoo_triggers_for_movement + _do_aoo"),
    "combat.aoo_extra_combat_reflexes": (IMPLEMENTED,    "_aoo_limit returns 1 + Dex when feat present; per-round counter on Combatant"),
    "combat.aoo_provoking_actions":  (PARTIAL,        "leaving threatened square + stand_up + non-defensive cast trigger; drink-potion / draw-weapon / retrieve-stowed-item not wired"),
    "combat.threatened_squares":     (PARTIAL,        "grid.threatened_squares; 5-ft (normal) and 10-ft (reach weapons) not differentiated yet"),
    "combat.reach_weapons":          (NOT_IMPLEMENTED, "10-ft threat with no adjacent — not modeled"),

    # ── Combat: special attacks & maneuvers ──────────────────────────────
    "combat.combat_maneuver_basic":  (NOT_IMPLEMENTED, "CMB vs CMD framework not built"),
    "combat.bull_rush":              (NOT_IMPLEMENTED, "push 5 ft + 5/+5 over CMD"),
    "combat.disarm":                 (NOT_IMPLEMENTED, "force drop weapon"),
    "combat.drag":                   (NOT_IMPLEMENTED, "pull target"),
    "combat.grapple":                (NOT_IMPLEMENTED, "restrain target"),
    "combat.overrun":                (NOT_IMPLEMENTED, "move through enemy"),
    "combat.reposition":             (NOT_IMPLEMENTED, "move target around"),
    "combat.steal":                  (NOT_IMPLEMENTED, "take item"),
    "combat.sunder":                 (NOT_IMPLEMENTED, "damage object/weapon"),
    "combat.trip":                   (NOT_IMPLEMENTED, "knock prone; wolf trip-on-bite is the immediate consumer"),
    "combat.coup_de_grace":          (NOT_IMPLEMENTED, "auto-crit on helpless + Fort save vs death"),
    "combat.massive_damage":         (NOT_IMPLEMENTED, "Fort save vs die at 50+ damage from one source"),
    "combat.aid_another":            (PARTIAL,         "composite 'aid_another' with mode='attack'|'ac'; DC 10 attack roll → +2 (circumstance) attack OR +2 dodge AC for 1 round; 'vs that specific foe' restriction not modeled (bonus is universal)"),
    "combat.fight_defensively":      (NOT_IMPLEMENTED, "-4 attack for +2 dodge AC"),
    "combat.total_defense":          (IMPLEMENTED,    "+4 dodge AC for 1 round (expires_round = current_round + 1); via _do_standard"),

    # ── Combat: charge & full-round movement ─────────────────────────────
    "combat.charge":                 (PARTIAL,        "min-distance, straight-line, lane-clear, end-adjacent enforced; difficult terrain not (engine has no terrain types)"),
    "combat.partial_charge":         (NOT_IMPLEMENTED, "charge as standard action when full-round unavailable"),
    "combat.withdraw":               (PARTIAL,        "full-round; first-square-no-AoO not yet enforced (just moves)"),
    "combat.run":                    (NOT_IMPLEMENTED, "x4 speed, lose Dex to AC, straight line"),

    # ── Combat: ranged attacks ──────────────────────────────────────────
    "combat.range_increments":       (PARTIAL,         "-2 attack per increment via _range_increment_penalty in _do_attack; max-range cap (5/10 increments) not yet enforced — long shots are punished but not forbidden"),
    "combat.firing_into_melee":      (IMPLEMENTED,    "-4 attack via _firing_into_melee_penalty in _do_attack; negated by Precise Shot feat. Detection: any other combatant adjacent to target."),
    "combat.point_blank_shot":       (IMPLEMENTED,    "feat applies +1 attack/damage to ranged via attack:ranged modifier"),

    # ── Combat: weapon use & wielding ───────────────────────────────────
    "combat.weapon_proficiency_penalty": (NOT_IMPLEMENTED, "-4 attack if not proficient with weapon used"),
    "combat.armor_proficiency_penalty": (NOT_IMPLEMENTED, "ACP applies to attack rolls without armor proficiency"),
    "combat.armor_check_penalty":    (IMPLEMENTED,    "ACP applied to relevant skill checks via combatant_from_character"),
    "combat.armor_max_dex":          (IMPLEMENTED,    "Dex bonus to AC capped by armor's max_dex_bonus"),
    "combat.two_handed_str_bonus":   (IMPLEMENTED,    "1.5×Str damage when wield='two_handed'"),
    "combat.off_hand_str_bonus":     (NOT_IMPLEMENTED, "0.5×Str off-hand; pair with two-weapon fighting work"),
    "combat.off_hand_attack":        (NOT_IMPLEMENTED, "no off-hand attack path in _do_full_attack"),
    "combat.shield_use":             (IMPLEMENTED,    "shield AC applied via combatant_from_character; no shield-bash attack profile yet"),
    "combat.weapon_finesse_use":     (IMPLEMENTED,    "Dex to attack for finesse weapons; combatant_from_character"),

    # ── Combat: HP, dying, death ────────────────────────────────────────
    "combat.hp_max":                 (IMPLEMENTED,    "computed from class HD + Con + bonuses"),
    "combat.dying":                  (PARTIAL,        "set when HP < 0 (above death threshold); 1 HP/round bleed via tick_round; DC 10 Con stabilization roll not yet modeled"),
    "combat.disabled":               (PARTIAL,        "set when HP exactly 0; turn validation restricts to 1 standard or 1 move; 1-HP-on-standard not yet modeled"),
    "combat.stable":                 (PARTIAL,        "suppresses dying-bleed when set on combatant; auto-stabilization roll + Heal-skill aid not modeled"),
    "combat.unconscious":            (PARTIAL,        "is_unconscious checks the condition; turn validation prevents acts"),
    "combat.dead_threshold":         (IMPLEMENTED,    "PF1 RAW: HP <= -CON for living; 0 for undead/constructs (no Con score). Cached on Combatant.death_threshold at construction"),
    "combat.helpless_attacker_bonus": (NOT_IMPLEMENTED, "+4 melee attack vs helpless; Dex treated as 0"),

    # ── Combat: healing ─────────────────────────────────────────────────
    "combat.healing_natural":        (NOT_IMPLEMENTED, "1 HP/level/8 hr; no rest-time mechanic in combat-only loop"),
    "combat.healing_full_rest":      (NOT_IMPLEMENTED, "full HP after 8 hr rest"),
    "combat.healing_magical":        (IMPLEMENTED,    "cure spells implemented as heal effect kind"),
    "combat.fast_healing":           (NOT_IMPLEMENTED, "X HP/round automatic"),
    "combat.regeneration":           (NOT_IMPLEMENTED, "HP/round + bypass-by-energy-type semantics"),

    # ── Combat: movement modes & terrain ────────────────────────────────
    "combat.movement_walk":          (IMPLEMENTED,    "speed-30 walk = 6 cells/round in our grid"),
    "combat.movement_difficult_terrain": (NOT_IMPLEMENTED, "2x cost; engine has no terrain types"),
    "combat.movement_fly":           (NOT_IMPLEMENTED, "no fly mode; some monsters have it as a tag only"),
    "combat.movement_swim":          (NOT_IMPLEMENTED, "no swim mode"),
    "combat.movement_climb":         (NOT_IMPLEMENTED, "no climb mode"),
    "combat.movement_burrow":        (NOT_IMPLEMENTED, "no burrow mode"),
    "combat.mounted_combat":         (NOT_IMPLEMENTED, "no mount/rider system"),
    "combat.underwater_combat":      (NOT_IMPLEMENTED, "no underwater terrain"),
    "combat.squeezing":              (OUT_OF_SCOPE,   "v1 doesn't model tight-quarters movement"),

    # ── Magic: spell mechanics ──────────────────────────────────────────
    "magic.spell_slots":             (IMPLEMENTED,    "per-Combatant resources, populated from class table at level-up"),
    "magic.bonus_spells_high_ability": (PARTIAL,      "ability-based bonus slots not added on top of class table"),
    "magic.spell_save_dc":           (IMPLEMENTED,    "10 + spell_level + key_ability_mod via spells.save_dc_for"),
    "magic.spell_resistance":        (IMPLEMENTED,    "d20 + caster_level vs target SR via spells.overcomes_sr"),
    "magic.caster_level":            (IMPLEMENTED,    "spells.caster_level returns char.level for v1; multiclass partial"),
    "magic.spell_failure_armor":     (NOT_IMPLEMENTED, "arcane casters in armor have % failure chance"),
    "magic.spell_known_vs_prepared": (PARTIAL,        "castable_spells set populated; preparation slot system not fully modeled"),

    # ── Magic: components & casting ─────────────────────────────────────
    "magic.casting_components_v":    (NOT_IMPLEMENTED, "verbal — silenced/deafened cannot cast"),
    "magic.casting_components_s":    (NOT_IMPLEMENTED, "somatic — needs free hand"),
    "magic.casting_components_m":    (NOT_IMPLEMENTED, "material — needs component"),
    "magic.casting_components_f":    (NOT_IMPLEMENTED, "focus item required"),
    "magic.casting_components_df":   (NOT_IMPLEMENTED, "divine focus (holy symbol)"),
    "magic.casting_components_xp":   (OUT_OF_SCOPE,   "3.5e XP-cost components; PF1 uses gp instead"),
    "magic.casting_in_threatened_square": (IMPLEMENTED, "non-defensive cast provokes; defensive concentration check via spells.cast_spell"),
    "magic.casting_defensively":     (IMPLEMENTED,    "DC 15 + spell level concentration; nat 1 fails"),
    "magic.concentration_on_damage": (NOT_IMPLEMENTED, "DC 10 + damage dealt; not modeled mid-cast"),
    "magic.concentration_grappled":  (NOT_IMPLEMENTED, "DC 10 + spell level + grapple CMB"),
    "magic.dispel_magic":            (NOT_IMPLEMENTED, "caster level check vs target's CL"),
    "magic.counterspell":            (NOT_IMPLEMENTED, "ready action with same/dispel + CL check"),
    "magic.metamagic":               (NOT_IMPLEMENTED, "Empower/Maximize/Quicken/Still/Silent — none wired"),

    # ── Magic: spell areas & targeting ──────────────────────────────────
    "magic.target_personal":         (IMPLEMENTED,    "self-only spells (e.g., cat's grace)"),
    "magic.target_touch":            (IMPLEMENTED,    "single creature touched"),
    "magic.target_ranged":           (IMPLEMENTED,    "single creature at close/medium/long range"),
    "magic.area_burst":              (IMPLEMENTED,    "_expand_aoe_burst by radius from center"),
    "magic.area_emanation":          (NOT_IMPLEMENTED, "lasting aura from caster outward"),
    "magic.area_cone":               (IMPLEMENTED,    "_expand_aoe_cone via 90° wedge test"),
    "magic.area_line":               (NOT_IMPLEMENTED, "narrow line from caster"),
    "magic.spread":                  (NOT_IMPLEMENTED, "burst that follows corners/around obstacles"),

    # ── Magic: save semantics ───────────────────────────────────────────
    "magic.save_negates":            (IMPLEMENTED,    "save = no effect"),
    "magic.save_half":               (IMPLEMENTED,    "save = halve damage"),
    "magic.save_partial":            (PARTIAL,        "some apply_condition_save handlers do partial; varies per spell"),
    "magic.save_disbelief":          (NOT_IMPLEMENTED, "illusions allow disbelief save on interaction"),

    # ── Skills ──────────────────────────────────────────────────────────
    "skills.untrained_checks":       (IMPLEMENTED,    "skill_total works regardless of ranks unless trained-only"),
    "skills.trained_only":           (NOT_IMPLEMENTED, "trained-only skills (Disable Device, etc.) usable at 0 ranks"),
    "skills.armor_check_penalty":    (IMPLEMENTED,    "applied to ACP-affected skills via combatant_from_character"),
    "skills.opposed_checks":         (NOT_IMPLEMENTED, "engine has no opposed-check API"),
    "skills.aid_another_skill":      (NOT_IMPLEMENTED, "DC 10 to grant +2 to another's check"),
    "skills.take_10":                (NOT_IMPLEMENTED, "skip the d20 if no immediate danger"),
    "skills.take_20":                (OUT_OF_SCOPE,   "20× time; no time-pressure model in v1"),
    "skills.class_skill_bonus":      (IMPLEMENTED,    "+3 to skill_total when 1+ ranks invested in class skill"),
    "skills.skill_synergy":          (OUT_OF_SCOPE,   "3.5e holdover; PF1 doesn't have skill synergies"),

    # ── Equipment & encumbrance ─────────────────────────────────────────
    "equipment.weapon_categories":   (PARTIAL,        "weapon JSONs declare type but no category-based proficiency check"),
    "equipment.weapon_special_properties": (PARTIAL, "JSONs carry properties (reach, double, brace, trip-bonus); rarely consulted at attack time"),
    "equipment.encumbrance":         (NOT_IMPLEMENTED, "no encumbrance tracking; carried items have no weight"),
    "equipment.armor_donning_time":  (NOT_IMPLEMENTED, "no time-to-don model"),

    # ── Adventuring: vision, environment ────────────────────────────────
    "adventuring.vision_normal":     (NOT_IMPLEMENTED, "no light-level model"),
    "adventuring.vision_low_light":  (NOT_IMPLEMENTED, "doubles range in dim light"),
    "adventuring.vision_darkvision": (NOT_IMPLEMENTED, "60 ft in total darkness; declared on monsters but not consulted"),
    "adventuring.light_sources":     (NOT_IMPLEMENTED, "torch/lantern/sunrod ranges"),
    "adventuring.falling_damage":    (NOT_IMPLEMENTED, "1d6 per 10 ft, max 20d6"),
    "adventuring.drowning":          (NOT_IMPLEMENTED, "Con score in rounds, then HP/round"),
    "adventuring.environmental_temperature": (NOT_IMPLEMENTED, "heat/cold non-lethal damage tracks"),
    "adventuring.travel_overland":   (OUT_OF_SCOPE,   "world tick is 6s/round; overland travel is per-cell movement at PF1 speed"),
    "adventuring.forced_march":      (OUT_OF_SCOPE,   "no day-level travel model"),
    "adventuring.aging":             (OUT_OF_SCOPE,   "no aging mechanic; characters don't change ability scores over time in v1"),
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
    "core_mechanics":        CORE_MECHANICS,
}


def status_for(category: str, item_id: str) -> Entry | None:
    """Look up the (status, note) for an item, or None if unknown."""
    return CATEGORIES.get(category, {}).get(item_id)


def declared_ids(category: str) -> set[str]:
    """All IDs the tracker knows about for a category."""
    return set(CATEGORIES.get(category, {}).keys())
