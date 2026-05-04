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
    "stability":             (IMPLEMENTED,     "+4 CMD vs trip / bull_rush via qualifier on cmd modifier; cmd(context) honors {'maneuver': kind}"),
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
    "light_sensitivity":     (IMPLEMENTED,    "Combatant.in_bright_light flag + update_light_sensitivity_state() applies/removes dazzled when sensitivity racial trait is present. Engine-wide daylight context is opt-in (callers flip the flag); the standard dazzled condition then drops attack/perception"),

    # Orc
    "ferocity":              (IMPLEMENTED,     "stay conscious below 0 HP; 1 HP/round bleed; via _apply_post_damage_state"),
    "light_sensitivity_orc": (IMPLEMENTED,    "same plumbing as light_sensitivity (kobold) — has_racial_trait('light_sensitivity_orc') triggers the same dazzled toggle"),

    # Skeleton
    "undead_traits":         (PARTIAL,         "type='undead' recognized for channel; bleed immunity wired in tick_round; condition immunities (mind-affecting / paralysis / sleep / stun / fatigue / nausea / fear / etc.) wired via Combatant.add_condition immunity check; disease/poison effect-types not yet modeled (no consumers)"),
    "dr_5_bludgeoning":      (IMPLEMENTED,     "wired via _parse_dr_trait + Combatant.damage_reduction; resolve_attack honors it"),
    "cold_immunity":         (IMPLEMENTED,    "_apply_monster_racial_traits adds 'cold' to energy_immunity for any monster with the trait; apply_typed_damage short-circuits to 'immune' for cold damage; fully wired alongside cold-damage spells (cone of cold, ice storm, cold magic missile)"),

    # Wolf
    "trip_attack":           (IMPLEMENTED,     "free trip CMB after successful melee hit; wired in _do_attack via _has_racial_trait + _resolve_maneuver"),

    # Zombie
    "undead_traits_zombie":  (PARTIAL,         "same as undead_traits — same immunity set wired"),
    "dr_5_slashing":         (IMPLEMENTED,     "wired via _parse_dr_trait; resolve_attack honors it"),

    # Bestiary 1 additions
    "paralysis_ghoul":       (IMPLEMENTED,    "_resolve_paralysis_rider fires after a successful melee hit by a creature with the trait. DC = 10 + 1/2 HD + Cha mod. Fort save negates; failure → paralyzed for 1d4+1 rounds (cascades to helpless via _IMPLIES_HELPLESS). RAW elf immunity is NOT enforced in v1."),
    "channel_resistance_2":  (IMPLEMENTED,    "_apply_monster_racial_traits adds qualifier-based +N to fort/ref/will saves with qualifier {'effect_type': 'channel_energy'}; _do_channel_energy passes context={'effect_type': 'channel_energy'} to roll_save so the bonus applies. Generalizes via channel_resistance_<N> trait id."),
    "diseased_bite":         (PARTIAL,        "Fort save vs DC 10 + 1/2 HD + Cha mod fires on hit; failure applies the 'diseased' marker condition. The daily ability-damage cycle (1d3 Con + 1d3 Dex per day for ghoul fever, etc.) is NOT simulated — needs a long-rest tick that v1 doesn't have."),
    "stalker_bugbear":       (IMPLEMENTED,    "Perception/Stealth class-skill bonus is already baked into bugbear.skills totals in the JSON; no per-trait wiring needed (monsters use pre-computed skill totals, so the class-skill +3 is in the number)"),
    "hold_breath":           (OUT_OF_SCOPE,   "Aquatic mechanic (Con × 4 rounds underwater). The engine doesn't model underwater combat or drowning — out-of-scope per the verticality-adjacent rule (water as an environmental dimension we don't simulate). Defer indefinitely."),
    "stench":                (IMPLEMENTED,    "Aura framework in _apply_aura_exposure: 30-ft Fort save vs DC 10 + 1/2 HD + Con mod, fail → sickened for 1d6 rounds. Cooldown=encounter (one save per source). Other troglodytes immune by template id. Saves stored in Combatant.aura_saves_taken."),
    "regeneration_5_fire_acid": (IMPLEMENTED,  "regeneration field + bypass set populated; floors at -1 vs non-bypass via take_damage"),
    "rend":                  (IMPLEMENTED,    "_do_full_attack tracks claw hits (attack-option name starting with 'claw') and on 2+ in a single full-attack, applies +1d6+1 untyped damage at the end of the routine. Wired with _has_racial_trait('rend')."),
    "freeze_gargoyle":       (OUT_OF_SCOPE,   "stealth-as-statue is a non-combat ambush helper (gargoyles freeze before initiative is rolled, then attack on round 1). The engine starts encounters with combatants already revealed; freeze never triggers in our scope. Defer indefinitely."),
    "dr_10_magic":           (IMPLEMENTED,    "_parse_dr_trait wires it on the gargoyle; _bypass_dr now consults AttackProfile.attack_tags so magic-tagged weapons (enhancement_bonus>0 or any special_ability) bypass the DR. Mundane weapons remain blocked."),
    "grab":                  (IMPLEMENTED,    "_resolve_grab_rider runs on a successful natural-weapon hit when actor has 'grab' (or 'blood_drain' as the auto-grab variant). Owlbear-style: opposed CMB; success links the pair (grappling_target_id / grappled_by_id) and applies grappled to both. Stirge-style auto-grab skips the roll."),
    "petrifying_gaze":       (IMPLEMENTED,    "Aura framework with cooldown='round' (fresh save each round). 30-ft Fort save vs DC 10 + 1/2 HD + Cha mod, fail → petrified (cascades to helpless). Other basilisks immune by template id."),
    "rock_throwing_120":     (IMPLEMENTED,    "Hill giant 'rock' attack option is a standard ranged attack with range_increment=120; resolves through resolve_attack like any other thrown weapon."),
    "rock_catching":         (IMPLEMENTED,    "_do_attack post-resolve: if target has rock_catching and the incoming ranged attack is a 'rock' (by weapon_id or name), the target rolls Reflex DC 15. On success, the hit is converted to a miss with reason 'rock caught'. RAW size-based DC scaling (15/20/25) and the once-per-round limit are simplified to a flat 15."),
    "natural_cunning":       (OUT_OF_SCOPE,   "minotaur immunity to maze spell. No maze spell in v1; the immunity has nothing to grant immunity to. Defer until maze lands."),
    "powerful_charge":       (IMPLEMENTED,    "_do_charge picks the gore attack (or attack option 0) and routes through charge_damage_multiplier=2 for any actor with the 'powerful_charge' trait."),
    "tail_spikes":           (PARTIAL,        "Manticore 'spikes' is a standard ranged attack with range_increment=180 and resolves through resolve_attack. The 6-spike-volley-as-standard-action and 24/day cap are NOT modeled (no daily-uses framework for monster ranged attacks yet)."),
    "displacement":          (IMPLEMENTED,    "_apply_monster_racial_traits sets concealment=50 on any monster with the trait. _do_attack honors concealment with a 1d100 ≤ 50 miss roll on every hit"),
    "resistance_save":       (IMPLEMENTED,    "+2 racial saves vs spells via qualifier-based modifiers (qualifier {'effect_tags': ['spell']}). Spell-resolved saves pass the effect_tags context so the bonus applies"),
    "poison_giant_spider":   (PARTIAL,        "_resolve_giant_spider_poison fires Fort save vs DC 10 + 1/2 HD + Con mod after a successful bite; failure applies 1d2 Str ability damage IMMEDIATELY (one tick). RAW says 1d2 Str / round for 4 rounds — the recurring rounds and dual-save cure are NOT modeled (no poison framework yet)."),
    "web_giant_spider":      (IMPLEMENTED,    "'web' composite action: targets a creature within 50ft (10 squares); Reflex save vs DC 10 + 1/2 HD + Con mod or entangled (sourced under 'web:<actor.id>'). The 8/day cap and STR/EA escape DC 16 from web aren't modeled in v1."),
    "constrict_strangle":    (IMPLEMENTED,    "_apply_end_of_turn_racial_effects: while grappling, deals 1d4+3 bludgeoning damage and applies 'silenced' (registered to source 'constrict_strangle:<actor.id>'). The silenced condition blocks V-component spells via the existing _do_cast check."),
    "quickness":             (PARTIAL,        "_apply_monster_racial_traits adds +1 enhancement to initiative for any actor with the 'quickness' trait. The +10ft first-round-move clause is NOT modeled (no round-1 movement-bonus path yet)."),
    "rake_lion":             (IMPLEMENTED,    "_apply_end_of_turn_racial_effects executes 2 free claw attacks (the actor's first 2 'claw'-named attack options) against the grappled target each round."),
    "pounce":                (IMPLEMENTED,    "_do_charge (after the standard charge attack) runs every remaining attack_option against the same target with the +2 charge bonus. Triggered by _has_racial_trait('pounce')."),
    "engulf":                (PARTIAL,        "_apply_end_of_turn_racial_effects checks adjacent enemies of an engulf-source: Reflex DC 10 + 1/2 HD + Str mod or paralyzed + 1d6 acid damage. RAW move-into-square mechanic is approximated as 'end of cube's turn while adjacent'; pull-along and continuous acid each round are partial."),
    "transparent":           (OUT_OF_SCOPE,   "DC 15 Perception to spot the cube before stumbling into it. The engine starts encounters with all combatants visible to each other; the surprise round / undetected mechanic isn't modeled. Defer indefinitely."),
    "ooze_traits":           (IMPLEMENTED,    "_apply_monster_racial_traits adds the full PF1 ooze immunity set to condition_immunities: charmed/fascinated/frightened/shaken/panicked/dazed/confused/sleeping/paralyzed/stunned/fatigued/exhausted/nauseated/sickened. Crit/precision-damage immunity isn't condition-shaped (needs an attack-resolution flag) — covered for the dnd sandbox by gel cube's hp/ac numbers"),
    "captivating_song":      (IMPLEMENTED,    "Aura framework: 300-ft (60 squares) Will save vs DC 10 + 1/2 HD + Cha mod, fail → fascinated. Cooldown=encounter (single save). Other harpies immune by template id."),
    "blood_drain":           (IMPLEMENTED,    "_resolve_grab_rider auto-grabs on a successful touch (no opposed roll). _apply_end_of_turn_racial_effects then drains 1d4 Con damage per round via apply_ability_damage('con'), capped at 4 cumulative (stored in resources['blood_drain_dealt'])."),
}


# ---------------------------------------------------------------------------
# Class features — declared in classes/*.json under level_1.class_features
# ---------------------------------------------------------------------------

CLASS_FEATURES_L1: dict[str, Entry] = {
    # Barbarian
    "fast_movement":         (IMPLEMENTED,    "+10 ft speed (light/no armor); applied as a 'speed'-target modifier in combatant_from_character, factored into _effective_speed"),
    "rage":                  (IMPLEMENTED,     "rage_start/rage_end composite actions; resource tracked"),

    # Bard
    "bardic_knowledge":      (IMPLEMENTED,    "+1/2 level (min 1) untyped on every Knowledge skill; applied at combatant_from_character"),
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
    "nature_sense":           (IMPLEMENTED,    "+2 Knowledge (nature) and +2 Survival; applied at combatant_from_character"),
    "wild_empathy_druid":     (PARTIAL,        "Diplomacy +druid_level applied (used vs animals; the 'vs animals' qualifier isn't enforced in v1)"),
    "orisons_druid":          (NOT_IMPLEMENTED, "0-level spell list"),

    # Fighter
    "fighter_bonus_combat_feat_1": (IMPLEMENTED, "extra combat feat slot at L1; selected via class_choices"),

    # Monk
    "ac_bonus_monk":          (IMPLEMENTED,    "+Wis to AC + monk_level/4; gated on armor.category != 'medium'/'heavy'. Wired in combatant_from_character"),
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
    "bleed":           (IMPLEMENTED,    "Combatant.bleed accumulator + apply_bleed/stop_bleed; tick_round subtracts HP per round and clears on heal/death; bleed condition tracks active bleeding; bleed-immune (undead/constructs) skip the loss"),
    "blinded":         (IMPLEMENTED,    "denies Dex to AC (via _has_dex_denied) + 50% miss chance applied when blinded attacks (1d100 ≤ 50 → outcome converted to miss in _do_attack); -2 AC, half speed, -4 to Acrobatics/Climb/Disable/Fly/Ride/SoH/Stealth/Swim wired in _on_condition_applied"),
    "confused":        (IMPLEMENTED,    "execute_turn intercepts a confused actor with the d100 PF1 table: 01-25 act normally, 26-50 babble, 51-75 self-attack (1d8+Str), 76-100 attack nearest creature (any team). Single-attack form for the attack-nearest case (full-attack vs. single-attack RAW reading is ambiguous; we use the conservative single-attack)"),
    "cowering":        (IMPLEMENTED,    "denies Dex via _DEX_DENIED_CONDITIONS; validate_turn blocks all action slots"),
    "dazed":           (IMPLEMENTED,    "validate_turn blocks all action slots (full_round/standard/move/swift/5ft/free)"),
    "dazzled":         (IMPLEMENTED,    "-1 untyped to attack and skill:perception via _on_condition_applied"),
    "deafened":        (IMPLEMENTED,    "20% spell-failure roll for V-component spells in _do_cast; -4 untyped to initiative wired in _on_condition_applied"),
    "dead":            (IMPLEMENTED,     "set by _apply_post_damage_state; turn validation prevents acts"),
    "disabled":        (IMPLEMENTED,    "validate_turn restricts to one move OR standard (no full-round); _execute_slots applies 1 HP self-damage after the standard resolves (drops the actor into dying)"),
    "dying":           (IMPLEMENTED,     "set by _apply_post_damage_state at HP <= 0; deployment marks DEAD on encounter end if hero is dying"),
    "energy_drained":  (IMPLEMENTED,    "negative_levels counter on Combatant; apply_negative_levels(n) adds -1 untyped to attack/fort/ref/will/skill_check per level + -5 max_hp; remove_negative_levels lifts one level at a time. add_condition('energy_drained') stacks; remove_condition strips all. Undead/constructs immune."),
    "entangled":       (IMPLEMENTED,    "-2 attack, -4 ability:dex, half speed via _on_condition_applied; charge/run banned in validate_turn"),
    "exhausted":       (IMPLEMENTED,     "-6 untyped to ability:str/dex via condition hook; speed halved on apply, restored on remove; supersedes fatigued"),
    "fascinated":      (IMPLEMENTED,    "-4 untyped to skill:perception via _on_condition_applied; validate_turn blocks all action slots"),
    "fatigued":        (IMPLEMENTED,     "-2 untyped to ability:str/dex via condition hook on add_condition; cleared by remove_condition; can't run/charge enforcement is implicit (run/charge no longer reachable while fatigued via -2 ability score, but the explicit ban is not yet in turn validation)"),
    "flat_footed":     (IMPLEMENTED,     "AC variant computed; sneak attack qualifies"),
    "frightened":      (IMPLEMENTED,    "-2 morale to attack/all saves/skill_check via _on_condition_applied; supersedes shaken (and is superseded by panicked) via add_condition tier-suppression"),
    "grappled":        (IMPLEMENTED,     "-2 untyped attack penalty + -4 untyped Dex penalty added on apply; validate_turn blocks moves, 5-ft step, charge/withdraw/run; full grapple action set (escape, reverse, etc.) not modeled, but action restriction is in place"),
    "helpless":        (IMPLEMENTED,    "denies Dex (sneak attack qualifies); auto-implied by unconscious/sleeping/paralyzed/petrified via _IMPLIES_HELPLESS cascade; coup_de_grace composite delivers auto-hit + auto-crit damage and Fort save (DC 10 + damage) or instant death; provokes AoO from threateners"),
    "incorporeal":     (IMPLEMENTED,    "Combatant.incorporeal flag set from monster.subtypes. AttackProfile.attack_tags carries weapon-derived tags (magic / ghost_touch / silver / cold_iron / adamantine / material). _do_attack post-resolve check: non-magical attacks miss with 'incorporeal: full immunity'; force or ghost_touch tags pass through; other magic attacks roll a 50% miss. apply_typed_damage applies the same logic for spells (force/ghost_touch bypass; non-magical immune; otherwise 50% miss roll). RAW corporeal-source-damage HALVING is NOT modeled — RAW says 50% chance to ignore, which IS modeled, so this matches the rules-text actually used by published incorporeal monsters."),
    "invisible":       (IMPLEMENTED,    "invisible condition sets concealment=50 (and restores prior value on remove). In _do_attack: an invisible attacker grants +2 to melee attack rolls and forces the target's AC to flat-footed (Dex denied). Pinpoint-by-Perception isn't modeled — attackers always treat invisible targets as undetected."),
    "nauseated":       (IMPLEMENTED,    "validate_turn allows only a single move action; standard/full_round/swift/5ft/free all banned"),
    "panicked":        (IMPLEMENTED,    "-2 morale chain like frightened (tier suppression); validate_turn additionally bans attack/cast/charge/full_attack/cleave/stunning_fist/smite_evil/ready_brace/rage_start/trample/grapple_*"),
    "paralyzed":       (IMPLEMENTED,    "denies Dex (sneak attack qualifies); turn validation prevents acts; helpless follow-on wired via _IMPLIES_HELPLESS cascade"),
    "petrified":       (IMPLEMENTED,    "denies Dex (sneak attack qualifies — petrified added to _DEX_DENIED_CONDITIONS); turn validation prevents physical acts; helpless follow-on wired via _IMPLIES_HELPLESS cascade. Hardness-8/half-HP body transformation not modeled."),
    "pinned":          (IMPLEMENTED,    "denies Dex (sneak attack qualifies); set by grapple_pin composite (CMB-5 vs CMD); also applies 'helpless'. Cleared on grapple_break_free or remove_condition('grappled')"),
    "prone":           (IMPLEMENTED,     "fall_prone free action applies the condition; stand_up move action provokes AoO from threateners; -4 melee attacker, +4 melee-attacker-vs-target, -4 ranged-attacker-vs-target wired in _do_attack"),
    "shaken":          (IMPLEMENTED,    "-2 morale to attack/all saves/skill_check via _on_condition_applied; superseded by frightened/panicked"),
    "sickened":        (IMPLEMENTED,    "-2 untyped to attack/damage/all saves/skill_check via _on_condition_applied"),
    "sleeping":        (IMPLEMENTED,    "denies Dex (sneak attack qualifies); helpless follow-on wired via _IMPLIES_HELPLESS cascade"),
    "squeezing":       (OUT_OF_SCOPE,    "rare; deferred indefinitely"),
    "stable":          (IMPLEMENTED,     "set by DC 10 Con check in tick_round when a roller is provided to the encounter; suppresses dying-bleed"),
    "staggered":       (IMPLEMENTED,    "validate_turn enforces a single move OR standard (no full-round); ferocity sets it; turn validation enforces it"),
    "stunned":         (IMPLEMENTED,    "denies Dex (sneak attack qualifies); drops held items; no actions enforced via stunned_until_round in tick_round; cleared automatically when round reached"),
    "unconscious":     (IMPLEMENTED,    "is_unconscious checks the condition; turn validation prevents acts; applying 'unconscious' adds 'helpless' (tracked under 'implied_by_unconscious' source)"),
    "silenced":        (IMPLEMENTED,    "applied by the Silence spell. Read by _do_cast: V-component spells from a silenced caster fail with reason='verbal_component_blocked'"),
    "bracing":         (IMPLEMENTED,    "set by ready_brace composite for one round; consumed by the brace-attack trigger in _do_charge (×2 damage on the bracing wielder's first hit against the charger)"),
    "diseased":        (PARTIAL,        "marker condition applied by diseased_bite (ghoul fever) on a failed Fort save. Daily ability-damage onset cycle (1d3 Con + 1d3 Dex / day for ghoul fever) NOT modeled — needs a long-rest tick."),
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
    "empower_spell":         (IMPLEMENTED,    "metamagic: ×1.5 to rolled damage/healing at +2 spell-slot level. Caster declares via cast args.metamagic"),
    "maximize_spell":        (IMPLEMENTED,    "metamagic: +3 spell-slot level. Roller.roll(take_max=True) routes through scaling_damage / magic_missile / heal handlers, returning max face for every die (RAW behavior)"),
    "still_spell":           (IMPLEMENTED,    "metamagic: +1 spell-slot level. Skips somatic-component checks (no S → no grappled/two-handed restriction)"),
    "silent_spell":          (IMPLEMENTED,    "metamagic: +1 spell-slot level. Skips verbal-component checks (no V → no silenced/deafened restriction)"),
    "quicken_spell":         (IMPLEMENTED,    "metamagic: +4 spell-slot level. Cast-as-swift-action wired in execute_turn: when do.swift is a cast with quicken_spell metamagic, _do_cast routes through and consumes the bumped slot"),
    "extend_spell":          (IMPLEMENTED,    "metamagic: +1 spell-slot level. Doubles computed duration via _expires_round(extend=True) when 'extend_spell' is in outcome.metamagic"),
    "mounted_combat":        (IMPLEMENTED,    "Once a target with rider_id is hit, the rider rolls a Ride check (DC = attack_total). On success, hit is converted to miss in _do_attack"),
    "spirited_charge":       (IMPLEMENTED,    "Doubles charge damage multiplier when mounted: ×3 with lance, ×2 otherwise. Set in _do_charge via charge_damage_multiplier in script_options"),
    "ride_by_attack":        (IMPLEMENTED,    "When charge args include ride_by=True and the actor has the feat (and is mounted), the charge continues along the same line past the target for any remaining charge-square capacity. The mount rides through the target's square; AoOs from the target are skipped on the post-attack continuation"),
    "trample":               (IMPLEMENTED,    "trample composite action: target adjacent to mount makes a Reflex save (DC 10 + 1/2 mount HD + mount Str mod) for half damage from the mount's first attack profile; failure → prone + full damage"),
    "deceitful":             (IMPLEMENTED,    "+2 Bluff/Disguise via feat_effects.skill_pairs"),
    "deft_hands":            (IMPLEMENTED,    "+2 Disable Device/Sleight of Hand via feat_effects.skill_pairs"),
    "magical_aptitude":      (IMPLEMENTED,    "+2 Spellcraft/Use Magic Device via feat_effects.skill_pairs"),
    "self_sufficient":       (IMPLEMENTED,    "+2 Heal/Survival via feat_effects.skill_pairs"),
    "animal_affinity":       (IMPLEMENTED,    "+2 Handle Animal/Ride via feat_effects.skill_pairs"),
    "acrobatic":             (IMPLEMENTED,    "+2 Acrobatics/Fly via feat_effects.skill_pairs"),
    "improved_critical":     (NOT_IMPLEMENTED, "doubles weapon threat range — needs threat-range modifier path on attack_options"),
    "vital_strike":          (NOT_IMPLEMENTED, "roll weapon damage dice 2× on a single attack action — needs single-attack action mode"),
    "improved_vital_strike": (NOT_IMPLEMENTED, "vital strike ×3"),
    "greater_vital_strike":  (NOT_IMPLEMENTED, "vital strike ×4"),
    "weapon_specialization": (IMPLEMENTED,    "+2 damage with chosen weapon — feat_effects parses 'weapon_specialization_<weapon_id>' and applies a +2 untyped to damage:weapon:<id>"),
    "greater_weapon_focus":  (IMPLEMENTED,    "+1 attack stacking on Weapon Focus — feat_effects parses 'greater_weapon_focus_<weapon_id>' and applies +1 untyped to attack:weapon:<id>"),
    "greater_weapon_specialization": (IMPLEMENTED, "+2 damage stacking on Weapon Specialization — feat_effects parses 'greater_weapon_specialization_<weapon_id>'"),
    "two_weapon_defense":    (NOT_IMPLEMENTED, "+1 shield AC while wielding two weapons"),
    "improved_two_weapon_fighting": (NOT_IMPLEMENTED, "extra off-hand attack at -5 cumulative"),
    "greater_two_weapon_fighting":  (NOT_IMPLEMENTED, "third off-hand attack at -10 cumulative"),
    "improved_initiative_chain": (NOT_IMPLEMENTED, "Reactionary trait stand-in"),
    "iron_will_chain":       (NOT_IMPLEMENTED, "1/day re-roll Will save after fail"),
    "great_fortitude_chain": (NOT_IMPLEMENTED, "1/day re-roll Fort save after fail"),
    "lightning_reflexes_chain": (NOT_IMPLEMENTED, "1/day re-roll Ref save after fail"),
    "greater_spell_focus":   (IMPLEMENTED,    "+1 DC stacking on Spell Focus — feat_effects parses 'greater_spell_focus_<school>' and applies +1 to spell_dc:<school>"),
    "greater_spell_penetration": (IMPLEMENTED, "+2 to caster-level checks vs SR (stacks with Spell Penetration) — feat_effects entry"),
    "augment_summoning":     (NOT_IMPLEMENTED, "summoned creatures get +4 enhancement Str/Con — needs summon system"),
    "natural_spell":         (NOT_IMPLEMENTED, "cast spells in wild shape — needs wild shape system"),
    "wild_shape":            (NOT_IMPLEMENTED, "druid class feature — gating Natural Spell"),
    "improved_grapple":      (NOT_IMPLEMENTED, "no provoke on grapple, +2 grapple CMB/CMD"),
    "improved_disarm":       (NOT_IMPLEMENTED, "no provoke on disarm, +2 disarm CMB/CMD"),
    "improved_trip":         (NOT_IMPLEMENTED, "no provoke on trip, +2 trip CMB/CMD"),
    "improved_sunder":       (NOT_IMPLEMENTED, "no provoke on sunder, +2 sunder CMB/CMD"),
    "improved_bull_rush":    (NOT_IMPLEMENTED, "no provoke on bull rush, +2 CMB/CMD"),
    "improved_overrun":      (NOT_IMPLEMENTED, "no provoke on overrun, +2 CMB"),
    "improved_feint":        (NOT_IMPLEMENTED, "feint as a move action — needs feint mechanic"),
    "deadly_aim":            (NOT_IMPLEMENTED, "ranged Power Attack analog: -X attack for +2X damage"),
    "manyshot":              (NOT_IMPLEMENTED, "first ranged attack of full attack fires two arrows on one roll"),
    "improved_precise_shot": (NOT_IMPLEMENTED, "ignore concealment less than total"),
    "shot_on_the_run":       (NOT_IMPLEMENTED, "split full-round move with a single ranged attack mid-move"),
    "spring_attack":         (NOT_IMPLEMENTED, "split full-round move with a single melee attack mid-move"),
    "mobility":              (NOT_IMPLEMENTED, "+4 dodge AC vs movement-triggered AoOs"),
    "whirlwind_attack":      (NOT_IMPLEMENTED, "single attack vs every opponent in reach as full-round"),
    "stunning_fist":         (PARTIAL,         "stunning_fist composite already implemented (active wiring); the FEAT entry exists but data-only — feat-effects modifiers around DC are not separately wired"),
    "deflect_arrows":        (NOT_IMPLEMENTED, "1/round, treat one ranged attack as miss"),
    "snatch_arrows":         (NOT_IMPLEMENTED, "catch deflected arrows, throw thrown weapons back"),
    "brew_potion":           (NOT_IMPLEMENTED, "create potions; crafting subsystem"),
    "craft_wand":            (NOT_IMPLEMENTED, "create wands; crafting subsystem"),
    "craft_wondrous_item":   (NOT_IMPLEMENTED, "create wondrous items; crafting subsystem"),
    "craft_magic_arms_and_armor": (NOT_IMPLEMENTED, "create magic arms/armor; crafting subsystem"),
    "craft_rod":             (NOT_IMPLEMENTED, "create rods; crafting subsystem"),
    "craft_staff":           (NOT_IMPLEMENTED, "create staves; crafting subsystem"),
    "forge_ring":            (NOT_IMPLEMENTED, "create rings; crafting subsystem"),
    "leadership":            (NOT_IMPLEMENTED, "cohort + followers; needs hireling/cohort system"),
    "blind_fight":           (NOT_IMPLEMENTED, "re-roll concealment miss chance; half-speed when blinded"),
    "weapon_proficiency_simple":  (NOT_IMPLEMENTED, "data-only: grants 'simple' to weapon_proficiency_categories"),
    "weapon_proficiency_martial": (NOT_IMPLEMENTED, "data-only: grants one martial weapon"),
    "weapon_proficiency_exotic":  (NOT_IMPLEMENTED, "data-only: grants one exotic weapon"),
    "armor_proficiency_light":    (NOT_IMPLEMENTED, "data-only: grants 'light' armor proficiency"),
    "armor_proficiency_medium":   (NOT_IMPLEMENTED, "data-only: grants 'medium' armor proficiency"),
    "armor_proficiency_heavy":    (NOT_IMPLEMENTED, "data-only: grants 'heavy' armor proficiency"),
    "shield_proficiency":         (NOT_IMPLEMENTED, "data-only: grants 'shields_normal'"),
    "tower_shield_proficiency":   (NOT_IMPLEMENTED, "data-only: grants 'shield_tower'"),
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
    "two_weapon_fighting":   (IMPLEMENTED,     "off-hand attack added during full_attack with options.two_weapon_fighting=true; paired penalties: -2/-2 (light off-hand + feat), -4/-8 (heavy + feat), -6/-10 (no feat). Improved/Greater TWF (more off-hand iteratives) deferred."),
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
    "color_spray":           (IMPLEMENTED, "HD-tiered effect on failed Will save: ≤2 HD = unconscious + blind + stunned; 3-5 HD = blind + stunned; 6+ HD = stunned"),
    "dispel_magic":          (IMPLEMENTED, "1d20 + CL vs DC 11 + caster's CL; removes one ongoing spell-source's modifiers + tracked conditions"),
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
    "combat.swift_action":           (IMPLEMENTED,    "Turn.swift slot honored by execute_turn — currently routes quicken-cast through it; smite_evil / rage_start / bardic_performance work via the composite path with the standard action-economy validator gating them. PF1 RAW limit of one swift per turn is enforced structurally (Turn.swift is a single dict slot)"),
    "combat.free_action":            (IMPLEMENTED,    "validation allowlist covers PF1 RAW free actions: drop_item, fall_prone, speak, signal, end_concentration / cease_concentration, drop_held_charge, drop_to_floor, release_grapple, press_attack, speak_briefly, use_extraordinary_ability"),
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
    "combat.dr_multi_keyword":       (IMPLEMENTED,    "_bypass_dr in combat.py supports two shapes: legacy flat OR-set (frozenset of keywords) and new AND-of-OR-groups (tuple of frozensets, every group must match). 'DR 10/silver and magic' = (10, (frozenset({'silver'}), frozenset({'magic'})))"),
    "combat.energy_damage":          (IMPLEMENTED,    "fire / cold / electricity / acid / sonic recognized in spells.apply_typed_damage; spell handlers (scaling_damage, magic_missile) read effect.damage_type and route through it. Spells: burning_hands, fireball, lightning_bolt, shocking_grasp, scorching_ray, cone_of_cold, acid_arrow, acid_splash"),
    "combat.energy_resistance":      (IMPLEMENTED,    "Combatant.energy_resistance: dict[damage_type, points-per-hit]; apply_typed_damage subtracts points before damage applies. Resistance caps at the damage amount (no negative damage)"),
    "combat.energy_immunity":        (IMPLEMENTED,    "Combatant.energy_immunity: set[damage_type]; apply_typed_damage drops damage to 0 with note='immune'"),
    "combat.bleed_damage":           (IMPLEMENTED,    "Combatant.bleed (HP/round) applies in tick_round; immune for undead/constructs (is_immune_to_bleed); any healing stops it"),
    "combat.nonlethal_damage":       (NOT_IMPLEMENTED, "no separate nonlethal HP track"),

    # ── Combat: defenses, cover, concealment, flanking ───────────────────
    "combat.cover":                  (IMPLEMENTED,    "hard cover (+4 AC) when one wall in line; +2 Reflex bonus computed via _cover_reflex_bonus and threaded through cast_spell → roll_save → scaling_damage handler (and any other save site that takes a grid context). Greater cover and total cover handled separately"),
    "combat.greater_cover":          (IMPLEMENTED,    "+8 AC when 2 walls intervene in the Bresenham line. Modeled as 'more than half the line blocked' via wall count"),
    "combat.soft_cover":             (IMPLEMENTED,    "intervening combatant grants +4 AC vs ranged via _cover_ac_bonus"),
    "combat.total_cover":            (IMPLEMENTED,    "_total_cover_blocks_line returns True when 3+ walls intervene; ranged attacks skip with 'total cover blocks line of effect' reason"),
    "combat.concealment":            (IMPLEMENTED,    "Combatant.concealment percentage (0/20/50). _do_attack rolls 1d100 after a successful hit; ≤ concealment converts to miss"),
    "combat.total_concealment":      (IMPLEMENTED,    "Same field; set Combatant.concealment=50 (e.g., invisible targets) and the miss-roll path applies it identically"),
    "combat.flanking":               (IMPLEMENTED,    "+2 attack to both flankers; grid.is_flanked_by + _flanking_attack_bonus"),
    "combat.higher_ground":          (NOT_IMPLEMENTED, "+1 attack from above"),

    # ── Combat: AoOs ────────────────────────────────────────────────────
    "combat.aoo":                    (IMPLEMENTED,    "1 AoO/round; aoo_triggers_for_movement + _do_aoo"),
    "combat.aoo_extra_combat_reflexes": (IMPLEMENTED,    "_aoo_limit returns 1 + Dex when feat present; per-round counter on Combatant"),
    "combat.aoo_provoking_actions":  (IMPLEMENTED,    "leaving threatened square, stand_up, non-defensive cast, draw_weapon (BAB 0), drink_potion, retrieve_stowed_item — all trigger AoO via aoo_triggers_for_provoking_action in _do_move"),
    "combat.threatened_squares":     (IMPLEMENTED,    "grid.threatened_squares uses (min_d, max_d) range — normal weapon threatens 1..reach; reach weapon (has_reach) shifts to (reach+1, reach+1) — adjacent NOT threatened, +5 ft beyond IS"),
    "combat.reach_weapons":          (IMPLEMENTED,    "Weapon.has_reach detected; grid.threatened_squares shifts threat from min/max=0/reach to min/max=reach+1/reach+1 — wielder threatens at +5 ft beyond normal reach but NOT adjacent. Longspear / glaive / lance carry has_reach=true"),

    # ── Combat: special attacks & maneuvers ──────────────────────────────
    "combat.combat_maneuver_basic":  (IMPLEMENTED,    "_resolve_maneuver: d20 + actor.cmb vs target.cmd(context={'maneuver': kind}); enables Stability and similar qualified CMD bonuses"),
    "combat.bull_rush":              (IMPLEMENTED,    "composite 'bull_rush'; pushes target 1 + (margin//5) squares directly away from actor; stops on impassable"),
    "combat.disarm":                 (IMPLEMENTED,    "composite 'disarm' actually removes the InventoryItem from target.held_items['main_hand']. Margin ≥ 10 transfers it to the attacker's carried_items; otherwise dropped at the target's square (recorded on encounter.dropped_items if available). Attack options pruned so target can't keep using the lost weapon"),
    "combat.drag":                   (IMPLEMENTED,    "composite 'drag': pulls target 1+(margin//5) squares toward actor; stops at actor's square"),
    "combat.grapple":                (IMPLEMENTED,    "composite 'grapple' marks both as 'grappled' and links via grappling_target_id / grappled_by_id. Full action set: grapple_damage (CMB vs CMD → weapon damage), grapple_move (move both up to half speed), grapple_pin (CMB-5 vs CMD → 'pinned' + 'helpless'), grapple_break_free (CMB or Escape Artist vs grappler's CMB → both lose grappled, target loses pinned/helpless)"),
    "combat.overrun":                (IMPLEMENTED,    "composite 'overrun': actor moves past target; target prone if margin >= 5"),
    "combat.reposition":             (IMPLEMENTED,    "composite 'reposition': move target up to (1 + margin//5) squares; default destination = one square away from actor"),
    "combat.steal":                  (IMPLEMENTED,    "composite 'steal' transfers an InventoryItem from target.carried_items to actor.carried_items on success. args.item_id may specify which item; default is the first carried item"),
    "combat.sunder":                 (IMPLEMENTED,    "composite 'sunder' rolls actor's weapon damage and applies it to target's main-hand InventoryItem (after hardness reduction). Item gains ``broken`` flag at half max HP; destroyed and removed from held_items at 0 HP. Attack options pruned"),
    "combat.trip":                   (IMPLEMENTED,    "composite 'trip' applies prone on success; also fires automatically after a successful melee hit for creatures with the 'trip_attack' racial trait (wolf)"),
    "combat.coup_de_grace":          (IMPLEMENTED,    "_do_coup_de_grace composite: full-round vs adjacent helpless / paralyzed / sleeping / unconscious / pinned target; deals weapon damage at the crit multiplier; target rolls Fort DC 10 + damage or dies. Provoking-AoO not modeled (mostly redundant — actor is already in melee)"),
    "combat.massive_damage":         (IMPLEMENTED,    "_check_massive_damage fires after damage in _do_attack: 50+ damage from one source → Fort DC 15 or die. Bypasses dying-threshold rules"),
    "combat.aid_another":            (IMPLEMENTED,    "composite 'aid_another' with mode='attack'|'ac'; DC 10 attack roll → +2 attack vs the named foe (qualifier on target_id) OR +2 dodge AC vs the named foe (qualifier on attacker_id). Bonus only applies when context matches the foe's id"),
    "combat.fight_defensively":      (IMPLEMENTED,    "_do_fight_defensively composite: -4 to attack, +2 dodge AC for one round (expires next round). Single attack against the named target"),
    "combat.total_defense":          (IMPLEMENTED,    "+4 dodge AC for 1 round (expires_round = current_round + 1); via _do_standard"),

    # ── Combat: charge & full-round movement ─────────────────────────────
    "combat.charge":                 (IMPLEMENTED,    "min-distance, straight-line, lane-clear, end-adjacent enforced; _charge_path_clear rejects difficult-terrain cells in the lane"),
    "combat.partial_charge":         (IMPLEMENTED,    "_do_partial_charge composite: delegates to _do_charge with max_squares_override = 1× speed (regular charge uses 2× speed)"),
    "combat.withdraw":               (IMPLEMENTED,    "full-round, 2× speed in a direction; first square does not provoke AoO (skip_aoo_first_step in _move_along)"),
    "combat.run":                    (IMPLEMENTED,    "composite 'run': 4× speed in a straight line, loses Dex bonus to AC for the round (added as -dex_to_ac modifier expiring next round)"),

    # ── Combat: ranged attacks ──────────────────────────────────────────
    "combat.range_increments":       (IMPLEMENTED,    "-2 attack per increment via _range_increment_penalty; max-range cap enforced via _out_of_max_range — thrown weapons (can_throw=true) cap at 5 increments, projectiles at 10. Out-of-range attacks skip with reason='target beyond maximum range'"),
    "combat.firing_into_melee":      (IMPLEMENTED,    "-4 attack via _firing_into_melee_penalty in _do_attack; negated by Precise Shot feat. Detection: any other combatant adjacent to target."),
    "combat.point_blank_shot":       (IMPLEMENTED,    "feat applies +1 attack/damage to ranged via attack:ranged modifier"),

    # ── Combat: weapon use & wielding ───────────────────────────────────
    "combat.weapon_proficiency_penalty": (IMPLEMENTED,    "-4 attack via _weapon_not_proficient in _do_attack; classes' weapon_proficiencies parsed into Combatant.weapon_proficiency_categories at construction (categories or specific weapon IDs); racial weapon familiarity (orc/elf/halfling) folded in"),
    "combat.armor_proficiency_penalty": (IMPLEMENTED,    "Combatant.armor_proficiency_categories populated by parsing class data; _armor_not_proficient_penalty layers ACP onto attack rolls when wearing armor / shield outside proficiencies (stacks, e.g., chainmail -5 + heavy shield -2 = -7)"),
    "combat.armor_check_penalty":    (IMPLEMENTED,    "ACP applied to relevant skill checks via combatant_from_character"),
    "combat.armor_max_dex":          (IMPLEMENTED,    "Dex bonus to AC capped by armor's max_dex_bonus"),
    "combat.two_handed_str_bonus":   (IMPLEMENTED,    "1.5×Str damage when wield='two_handed'"),
    "combat.off_hand_str_bonus":     (IMPLEMENTED,    "0.5×Str (round toward zero) wired in combatant_from_character for the off-hand attack option"),
    "combat.off_hand_attack":        (IMPLEMENTED,    "off-hand attack option added to attack_options when equipped_offhand_weapon is set; _do_full_attack iterates it when options.two_weapon_fighting=true"),
    "combat.shield_use":             (IMPLEMENTED,    "shield AC applied via combatant_from_character; no shield-bash attack profile yet"),
    "combat.weapon_finesse_use":     (IMPLEMENTED,    "Dex to attack for finesse weapons; combatant_from_character"),

    # ── Combat: HP, dying, death ────────────────────────────────────────
    "combat.hp_max":                 (IMPLEMENTED,    "computed from class HD + Con + bonuses"),
    "combat.dying":                  (IMPLEMENTED,    "set when HP < 0; 1 HP/round bleed via tick_round; DC 10 Con stabilization roll fires when a roller is provided to tick_round (Encounter passes its own)"),
    "combat.disabled":               (IMPLEMENTED,    "set when HP exactly 0; turn validation restricts to 1 standard or 1 move; standard-action self-damage of 1 HP fires from execute_turn via _turn_used_standard_action heuristic (any attack/cast/etc. event triggers the cost). Emits 'disabled_self_damage' event"),
    "combat.stable":                 (IMPLEMENTED,    "suppresses dying-bleed when set; reached via DC 10 Con check in tick_round or via the 'stable' condition being applied externally"),
    "combat.unconscious":            (IMPLEMENTED,    "is_unconscious checks the condition; turn validation prevents acts; applying 'unconscious' also adds 'helpless' (tracked under 'implied_by_unconscious' source so removal of unconscious drops the implied helpless without clobbering externally-applied helpless)"),
    "combat.dead_threshold":         (IMPLEMENTED,    "PF1 RAW: HP <= -CON for living; 0 for undead/constructs (no Con score). Cached on Combatant.death_threshold at construction"),
    "combat.helpless_attacker_bonus": (IMPLEMENTED,    "+4 melee attack vs helpless target (not ranged); target is dex-denied via _has_dex_denied (helpless/paralyzed/pinned/stunned/etc.) → flat-footed AC used in resolve_attack"),

    # ── Combat: healing ─────────────────────────────────────────────────
    "combat.healing_natural":        (NOT_IMPLEMENTED, "1 HP/level/8 hr; no rest-time mechanic in combat-only loop"),
    "combat.healing_full_rest":      (NOT_IMPLEMENTED, "full HP after 8 hr rest"),
    "combat.healing_magical":        (IMPLEMENTED,    "cure spells implemented as heal effect kind"),
    "combat.fast_healing":           (IMPLEMENTED,    "Combatant.fast_healing: X HP/round in tick_round, capped at max_hp; dead creatures don't heal"),
    "combat.regeneration":           (IMPLEMENTED,    "Combatant.regeneration heals X/round in tick_round. Non-bypass damage (damage_type not in regeneration_bypass) is floored at -1 in take_damage — the creature can't be killed by non-bypass damage, but stays at -1 and continues regenerating. Bypass-type damage applies normally and CAN kill"),

    # ── Combat: movement modes & terrain ────────────────────────────────
    "combat.movement_walk":          (IMPLEMENTED,    "speed-30 walk = 6 cells/round in our grid"),
    "combat.movement_difficult_terrain": (IMPLEMENTED,    "GridFeature(movement_cost_multiplier=2.0) recognized in _move_along; entering a difficult square consumes (multiplier-1) extra steps from the actor's movement budget"),
    "combat.movement_fly":           (OUT_OF_SCOPE,   "no verticality in v1"),
    "combat.movement_swim":          (OUT_OF_SCOPE,   "no aquatic subgame in v1"),
    "combat.movement_climb":         (OUT_OF_SCOPE,   "no 3D terrain in v1"),
    "combat.movement_burrow":        (OUT_OF_SCOPE,   "no 3D terrain in v1"),
    "combat.mounted_combat":         (IMPLEMENTED,    "mount_id/rider_id link; mount/dismount composite actions; rider position follows mount in _move_along; mounted-lance charge ×2 damage (×3 with Spirited Charge feat); Mounted Combat feat lets rider negate hit-on-mount via Ride check (DC = attack roll). Trample / Ride-By Attack feats are PARTIAL (declared, partial wiring); mount AI on rider's turn deferred"),
    "combat.underwater_combat":      (OUT_OF_SCOPE,   "no aquatic subgame in v1"),
    "combat.squeezing":              (OUT_OF_SCOPE,   "v1 doesn't model tight-quarters movement"),

    # ── Magic: spell mechanics ──────────────────────────────────────────
    "magic.spell_slots":             (IMPLEMENTED,    "per-Combatant resources, populated from class table at level-up"),
    "magic.bonus_spells_high_ability": (IMPLEMENTED,  "progression.bonus_spells_per_day applies PF1 Table 1-3 mod-based bonuses to spells_per_day in leveling._aggregate_spells_per_day; bonus is added to the slot count for any spell level the caster's class table grants"),
    "magic.spell_save_dc":           (IMPLEMENTED,    "10 + spell_level + key_ability_mod via spells.save_dc_for"),
    "magic.spell_resistance":        (IMPLEMENTED,    "d20 + caster_level vs target SR via spells.overcomes_sr"),
    "magic.caster_level":            (IMPLEMENTED,    "spells.caster_level returns char.level for v1; multiclass partial"),
    "magic.spell_failure_armor":     (IMPLEMENTED,    "_is_arcane_caster + _arcane_spell_failure_pct in turn_executor; 1d100 ≤ ASF% in _do_cast for S-component spells. Slot consumed on failure. Skipped if 'still_spell' metamagic is applied"),
    "magic.spell_known_vs_prepared": (IMPLEMENTED,    "Combatant.casting_type ('prepared' / 'spontaneous' / '') read from class.spell_progression.type. Prepared casters consume from Combatant.prepared_spells (populated from Character.spells_prepared at dispatch); spontaneous use Combatant.castable_spells (from Character.spells_known when set, else class-wide list). Empty prep is a permissive fallback so default-dispatched heroes still cast"),

    # ── Magic: components & casting ─────────────────────────────────────
    "magic.casting_components_v":    (IMPLEMENTED,    "V-component spells fail outright when caster is silenced; deafened caster has 20% spell-failure roll. The Silence spell applies the silenced condition (Will negates)"),
    "magic.casting_components_s":    (IMPLEMENTED,    "Grappled S-component cast requires DC 10 + 4 + spell level concentration; failure consumes slot. Two-handed-weapon-blocks-S enforced when BOTH hands are filled (main_hand=two-handed weapon AND off_hand=anything) — pragmatic exception for wizards with a single quarterstaff in main_hand and no off-hand allows them to re-grip for casting"),
    "magic.casting_components_m":    (NOT_IMPLEMENTED, "material — no component-tracking yet; assumed always available"),
    "magic.casting_components_f":    (NOT_IMPLEMENTED, "focus item required"),
    "magic.casting_components_df":   (NOT_IMPLEMENTED, "divine focus (holy symbol)"),
    "magic.casting_components_xp":   (OUT_OF_SCOPE,   "3.5e XP-cost components; PF1 uses gp instead"),
    "magic.casting_in_threatened_square": (IMPLEMENTED, "non-defensive cast provokes; defensive concentration check via spells.cast_spell"),
    "magic.casting_defensively":     (IMPLEMENTED,    "DC 15 + spell level concentration; nat 1 fails"),
    "magic.concentration_on_damage": (IMPLEMENTED,    "DC 10 + damage + spell level concentration roll fired in _do_cast when AoO during a non-defensive cast deals damage; failure consumes slot and emits cast_failed"),
    "magic.concentration_grappled":  (IMPLEMENTED,    "DC 10 + 4 + spell level concentration roll on S-component cast while grappled; failure consumes slot. Uses flat +4 stand-in instead of looking up the actual grappler's CMB"),
    "magic.dispel_magic":            (IMPLEMENTED,    "dispel_magic spell + _handle_dispel_magic: enumerates spell:* sources on target via active_spell_sources, rolls 1d20+CL vs DC 11+CL, on success calls remove_effects_from_source which clears both modifiers and tracked conditions"),
    "magic.counterspell":            (NOT_IMPLEMENTED, "ready action with same/dispel + CL check — needs readied/triggered-action queue (deferred)"),
    "magic.metamagic":               (IMPLEMENTED,    "Empower (×1.5 post-process), Maximize (true max-dice via roller take_max), Still (skip somatic), Silent (skip verbal), Extend (duration ×2), Quicken (cast as swift action). Slot cost = base + sum(level adjustments). All five metamagic feats fully wired"),

    # ── Magic: spell areas & targeting ──────────────────────────────────
    "magic.target_personal":         (IMPLEMENTED,    "self-only spells (e.g., cat's grace)"),
    "magic.target_touch":            (IMPLEMENTED,    "single creature touched"),
    "magic.target_ranged":           (IMPLEMENTED,    "single creature at close/medium/long range"),
    "magic.area_burst":              (IMPLEMENTED,    "_expand_aoe_burst by radius from center"),
    "magic.area_emanation":          (IMPLEMENTED,    "_expand_aoe_emanation: snapshot of combatants within range of caster at cast time. The emanation 'follows' the caster via duration modifiers; the on-cast target list is point-in-time"),
    "magic.area_cone":               (IMPLEMENTED,    "_expand_aoe_cone via 90° wedge test"),
    "magic.area_line":               (IMPLEMENTED,    "_expand_aoe_line: walks a unit-vector path from caster toward target square up to area.size_ft / 5; stops at the first wall (line of sight)"),
    "magic.spread":                  (IMPLEMENTED,    "_expand_aoe_spread: BFS from origin through unblocked cells up to area.size_ft / 5 path-distance; walls block expansion (so spread fills around obstacles, doesn't go through them). Used by fireball"),

    # ── Magic: save semantics ───────────────────────────────────────────
    "magic.save_negates":            (IMPLEMENTED,    "save = no effect"),
    "magic.save_half":               (IMPLEMENTED,    "save = halve damage"),
    "magic.save_partial":            (IMPLEMENTED,    "_handle_apply_condition_save honors effect.condition_on_save_success: failed save applies effect.condition (e.g., frightened), passing save applies the lesser condition (e.g., shaken). Cause Fear is the canonical exemplar"),
    "magic.save_disbelief":          (IMPLEMENTED,    "spells.disbelief_save(target, source, dc, roller, interacted): rolls Will + (4 if interacted) vs DC; on success calls remove_effects_from_source which clears modifiers and tracked conditions sourced under the illusion. Caller decides when an interaction triggers the re-save"),

    # ── Skills ──────────────────────────────────────────────────────────
    "skills.untrained_checks":       (IMPLEMENTED,    "skill_total works regardless of ranks unless trained-only"),
    "skills.trained_only":           (IMPLEMENTED,    "skill_check (skills.py) returns blocked_trained_only=True when actor has 0 ranks in a trained-only skill"),
    "skills.armor_check_penalty":    (IMPLEMENTED,    "applied to ACP-affected skills via combatant_from_character"),
    "skills.opposed_checks":         (IMPLEMENTED,    "skills.opposed_skill_check rolls both, ties go to defender (initiator must beat opponent's total)"),
    "skills.aid_another_skill":      (IMPLEMENTED,    "skills.aid_another_skill: DC 10 check returns +2 bonus on success; caller passes via skill_check(extra_bonus=2)"),
    "skills.take_10":                (IMPLEMENTED,    "skill_check honors take_10 only when can_take_10(actor) returns True — disallowed when distracted (stunned / dazed / frightened / etc.) or damaged (current_hp < max_hp). Otherwise silently falls back to a d20 roll"),
    "skills.take_20":                (OUT_OF_SCOPE,   "20× time; no time-pressure model in v1"),
    "skills.class_skill_bonus":      (IMPLEMENTED,    "+3 to skill_total when 1+ ranks invested in class skill"),
    "skills.skill_synergy":          (OUT_OF_SCOPE,   "3.5e holdover; PF1 doesn't have skill synergies"),

    # ── Equipment & encumbrance ─────────────────────────────────────────
    "equipment.weapon_categories":   (IMPLEMENTED,    "weapon_category tagged on attack_options; Combatant.weapon_proficiency_categories holds the actor's allowed categories + specific weapon IDs; -4 attack penalty when wielding outside proficiencies (see _weapon_not_proficient in turn_executor)"),
    "equipment.weapon_special_properties": (IMPLEMENTED, "Weapon dataclass exposes has_reach (consulted in threat zones), has_brace (ready_brace composite + brace-attack trigger in _do_charge with ×2 damage), is_double (synthesized off-hand attack option from main_hand for double weapons like quarterstaff), trip_bonus (consulted in trip CMB)"),
    "equipment.encumbrance":         (IMPLEMENTED,    "carried_weight + load_category in encumbrance.py; combatant_from_character applies medium/heavy ACP, Max-Dex cap (taking the more restrictive of armor and load), and speed reduction via effective_speed (worse-of-armor-or-load)"),
    "equipment.armor_donning_time":  (NOT_IMPLEMENTED, "no time-to-don model"),

    # ── Adventuring: vision, environment ────────────────────────────────
    "adventuring.vision_normal":     (NOT_IMPLEMENTED, "no light-level model"),
    "adventuring.vision_low_light":  (NOT_IMPLEMENTED, "doubles range in dim light"),
    "adventuring.vision_darkvision": (NOT_IMPLEMENTED, "60 ft in total darkness; declared on monsters but not consulted"),
    "adventuring.light_sources":     (NOT_IMPLEMENTED, "torch/lantern/sunrod ranges"),
    "adventuring.falling_damage":    (OUT_OF_SCOPE,   "no verticality in v1"),
    "adventuring.drowning":          (OUT_OF_SCOPE,   "no aquatic subgame in v1"),
    "adventuring.environmental_temperature": (OUT_OF_SCOPE, "no environment / weather model in v1"),
    "adventuring.travel_overland":   (OUT_OF_SCOPE,   "world tick is 6s/round; overland travel is per-cell movement at PF1 speed"),
    "adventuring.forced_march":      (OUT_OF_SCOPE,   "no day-level travel model in v1"),
    "adventuring.aging":             (OUT_OF_SCOPE,   "no aging mechanic in v1"),
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
