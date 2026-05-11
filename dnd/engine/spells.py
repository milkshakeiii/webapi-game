"""Spellcasting mechanics: save DCs, SR checks, concentration, effect dispatch.

The casting flow:

1. Caster picks a spell, a spell_level slot to consume, targets.
2. Engine consumes the slot.
3. For each target: roll spell resistance (if applicable), then the saving
   throw (if applicable), then apply the effect.
4. Engine records a structured log of every roll.

This module knows how to resolve a small set of effect ``kind`` values
(damage, heal, magic_missile, buffs, conditions, charm). Adding a new
effect kind is a one-function extension here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .combat import resolve_attack, AttackProfile, DefenseProfile
from .combatant import Combatant
from .content import ContentRegistry, Spell
from .dice import Roller
from .modifiers import Modifier, mod


# ---------------------------------------------------------------------------
# Outcome
# ---------------------------------------------------------------------------


@dataclass
class SpellOutcome:
    spell_id: str
    caster_id: str
    success: bool
    targets_affected: list[str]
    damage_per_target: dict[str, int]
    healing_per_target: dict[str, int]
    conditions_applied: dict[str, list[str]]
    modifiers_applied: dict[str, list[dict]]   # per-target list of {value, type, target, expires_round}
    save_dc: int
    log: list[str] = field(default_factory=list)
    # Metamagic feats applied to this cast. Read by handlers that
    # care (e.g., duration-computing handlers check for "extend_spell").
    metamagic: list[str] = field(default_factory=list)
    # Optional grid passed by cast_spell. Used by handlers that need
    # to compute positional bonuses like cover-vs-Reflex. None when
    # there is no spatial context (e.g., scenario-tests casting
    # without a grid).
    grid: object | None = None
    # Optional encounter for handlers that need turn-context lookups
    # (e.g., bardic countersong / distraction reactive intercepts in
    # roll_save). None when the cast happens outside an encounter
    # (scenario tests etc.).
    encounter: object | None = None

    def to_dict(self) -> dict:
        return {
            "spell_id": self.spell_id,
            "caster_id": self.caster_id,
            "success": self.success,
            "save_dc": self.save_dc,
            "targets_affected": list(self.targets_affected),
            "damage_per_target": dict(self.damage_per_target),
            "healing_per_target": dict(self.healing_per_target),
            "conditions_applied": {k: list(v) for k, v in self.conditions_applied.items()},
            "modifiers_applied": {
                k: list(v) for k, v in self.modifiers_applied.items()
            },
            "log": list(self.log),
        }


# ---------------------------------------------------------------------------
# Save DC, caster level, key ability
# ---------------------------------------------------------------------------


_KEY_ABILITY = {
    "cleric": "wis",
    "druid": "wis",
    "wizard": "int",
    "sorcerer": "cha",
    "bard": "cha",
    "paladin": "cha",
    "ranger": "wis",
}


def caster_level(caster: Combatant) -> int:
    """Caster level for a Combatant.

    For v1, equal to total levels of casting classes the caster has. We
    look at the underlying Character (if present) and sum the levels in
    the registered caster classes.
    """
    if caster.template_kind != "character":
        # Monsters use their HD as caster level for spell-like abilities;
        # we don't model monster casters yet.
        return 1
    char = caster.template
    if not char or not getattr(char, "level", None):
        return 1
    return char.level


def key_ability_for(caster: Combatant) -> str | None:
    """Primary spellcasting ability for a character based on their class."""
    if caster.template_kind != "character":
        return None
    char = caster.template
    if char is None:
        return None
    cid = getattr(char, "class_id", None)
    return _KEY_ABILITY.get(cid)


def save_dc_for(
    caster: Combatant, spell_level: int, registry: ContentRegistry,
) -> int:
    """10 + spell level + key ability modifier. Spell Focus / Greater
    Spell Focus add to this DC via ``feat_effects.py`` modifiers."""
    key = key_ability_for(caster)
    if key is None:
        return 10 + spell_level
    # Read the ability score off the caster's modifier collection.
    base_score = 10
    if caster.template is not None and hasattr(caster.template, "base_ability_scores"):
        base_score = caster.template.base_ability_scores.get(key)
    # Apply racial mods plus any active modifiers on ability:{key}.
    total_score = base_score
    for m in caster.modifiers.for_target(f"ability:{key}"):
        total_score += m.value
    ability_mod = (total_score - 10) // 2
    return 10 + spell_level + ability_mod


# ---------------------------------------------------------------------------
# Saving throws
# ---------------------------------------------------------------------------


def roll_save(
    target: Combatant,
    save_kind: str,
    dc: int,
    roller: Roller,
    context: dict | None = None,
    cover_bonus: int = 0,
    encounter=None,
    grid=None,
) -> tuple[bool, int, int]:
    """Roll a saving throw. Returns (passed, natural, total).

    ``context`` is forwarded to ``target.save`` so situational save
    bonuses (hardy, illusion_resistance, etc.) qualify. Default
    behavior (no context) ignores qualified mods.

    ``cover_bonus`` is a flat bonus from PF1 cover (+2 for hard
    cover, +4 for greater cover). Currently only Reflex saves benefit
    per RAW; we apply it unconditionally and let the caller pass 0 for
    non-Reflex contexts.

    ``encounter`` and ``grid``, when both supplied, enable bardic
    countersong / distraction reactive intercepts. RAW: any creature
    within 30 ft of a bard with the matching active performance "may
    use the bard's Perform check result in place of its saving throw
    if, after the saving throw is rolled, the Perform check result
    proves to be higher." The intercept is applied AFTER the natural
    save roll, matching the RAW order. ``context`` should carry
    ``descriptors`` (for sonic / language-dependent → countersong) and
    ``school`` + ``subschool`` (for illusion-pattern / illusion-figment
    → distraction).
    """
    save_total = target.save(save_kind, context=context) + cover_bonus
    r = roller.roll("1d20")
    nat = r.terms[0].rolls[0]
    total = nat + save_total
    # Discharge any single-use buffs (e.g. Guidance).
    target.consume_single_use_buffs()
    # Bardic intercept: swap in the bard's Perform total if higher.
    # Done before the nat-1/nat-20 short-circuits per RAW: "if, after
    # the saving throw is rolled, the Perform check result proves to
    # be higher" — the intercept replaces the rolled total wholesale.
    if encounter is not None and grid is not None and context is not None:
        from .turn_executor import _bardic_save_intercept
        intercepted = _bardic_save_intercept(
            target, save_kind, total, context, encounter, grid,
        )
        if intercepted is not None and intercepted > total:
            total = intercepted
            # The intercept doesn't change the natural roll, so nat-1
            # auto-fail / nat-20 auto-pass still apply per the RAW
            # order ("the saving throw is rolled" first, then the
            # bard's check substitutes).
    if nat == 1:
        return False, nat, total
    if nat == 20:
        return True, nat, total
    return total >= dc, nat, total


_ENERGY_DAMAGE_TYPES: frozenset[str] = frozenset({
    "fire", "cold", "electricity", "acid", "sonic",
})


def _spell_attack_tags(spell, damage_type: str | None) -> frozenset[str]:
    """Build the attack-tag set for a spell-driven damage instance.

    Spells are inherently magical, so the result always contains
    ``"magic"``. The damage type is added as a tag verbatim
    (``"force"``, ``"fire"``, etc.) and any spell descriptors
    (``"force"``, ``"holy"``, ``"good"``, ``"evil"``, ``"law"``,
    ``"chaos"``) are added too — descriptors map directly onto the
    DR-bypass and incorporeal-resolution tag namespace.
    """
    tags: set[str] = {"magic"}
    if damage_type:
        tags.add(damage_type.lower())
    for d in getattr(spell, "descriptors", None) or []:
        tags.add(str(d).lower())
    return frozenset(tags)


def apply_typed_damage(
    target: Combatant, amount: int, damage_type: str | None,
    *, attack_tags: frozenset[str] | None = None, roller=None,
) -> tuple[int, str | None]:
    """Apply ``amount`` damage to ``target``, honoring energy
    immunity / resistance when ``damage_type`` is an energy type and
    incorporeal-target rules when applicable.

    Returns ``(applied, note)`` — applied is the amount that actually
    reduced HP; note is a human-readable trace ("immune", "resisted N",
    "incorporeal_immune", "incorporeal_50pct_miss", or None for normal
    damage).

    Spells should pass ``attack_tags`` containing at least ``"magic"``
    (since spells are magical by RAW) plus any descriptor tags
    (``"force"``, ``"holy"``, etc.). For incorporeal targets:
    non-magical attacks miss outright; force / ghost-touch attacks
    apply normally; other magical attacks roll a 50% miss check.

    Non-energy damage_types and ``None`` are passed through unchanged
    (energy/incorporeal checks excepted).
    """
    if amount <= 0:
        return 0, None
    tags = attack_tags or frozenset()
    note: str | None = None
    if damage_type and damage_type in _ENERGY_DAMAGE_TYPES:
        if damage_type in target.energy_immunity:
            return 0, "immune"
        resist = target.energy_resistance.get(damage_type, 0)
        if resist > 0:
            absorbed = min(resist, amount)
            amount = max(0, amount - resist)
            note = f"resisted {absorbed}"
    # Incorporeal target rules.
    if amount > 0 and getattr(target, "incorporeal", False):
        is_force = (
            "force" in tags
            or (damage_type is not None and damage_type.lower() == "force")
        )
        is_ghost_touch = "ghost_touch" in tags
        if is_force or is_ghost_touch:
            pass  # passes through
        elif "magic" not in tags:
            return 0, "incorporeal_immune"
        elif roller is not None:
            r = roller.roll("1d100")
            val = r.terms[0].rolls[0] if r.terms else int(r.total)
            if val <= 50:
                return 0, "incorporeal_50pct_miss"
    if amount > 0:
        target.take_damage(amount, damage_type=damage_type)
    return amount, note


def disbelief_save(
    target: Combatant,
    source: str,
    dc: int,
    roller: Roller,
    interacted: bool = False,
) -> tuple[bool, int, int]:
    """Roll a Will save to disbelieve an illusion sourced at ``source``.

    PF1 RAW: a creature interacting with an illusion (touching it,
    studying it, witnessing its effect contradict reality) gets a Will
    save at +4. A creature merely seeing the illusion gets the save
    without the +4 bonus.

    On a successful save, all effects sourced at ``source`` are
    cleared from ``target`` via ``remove_effects_from_source`` —
    matching modifier records and tracked conditions are removed.

    Returns ``(passed, natural, total)``.
    """
    bonus = target.save("will")
    if interacted:
        bonus += 4
    r = roller.roll("1d20")
    nat = r.terms[0].rolls[0]
    total = nat + bonus
    if nat == 1:
        passed = False
    elif nat == 20:
        passed = True
    else:
        passed = total >= dc
    if passed:
        target.remove_effects_from_source(source)
    return passed, nat, total


def parse_saving_throw(saving_throw_str: str) -> tuple[str | None, str]:
    """Return (save_kind, semantic).

    Examples:
      "none" → (None, "none")
      "reflex_half" → ("ref", "half")
      "will_negates" → ("will", "negates")
      "will_negates_harmless" → ("will", "negates_harmless")
    """
    if not saving_throw_str or saving_throw_str == "none":
        return None, "none"
    parts = saving_throw_str.split("_", 1)
    save = parts[0]
    semantic = parts[1] if len(parts) > 1 else "negates"
    save_kind = {"reflex": "ref", "fort": "fort", "fortitude": "fort",
                 "will": "will", "ref": "ref"}.get(save, save)
    return save_kind, semantic


# ---------------------------------------------------------------------------
# Spell resistance
# ---------------------------------------------------------------------------


def overcomes_sr(
    caster_lvl: int, target: Combatant, roller: Roller,
) -> tuple[bool, int]:
    """Overcome target's SR if any. Returns (overcame, roll_total)."""
    # For v1 we only honor SR when the target template carries an SR field.
    sr = 0
    if target.template_kind == "monster" and target.template is not None:
        sr = int((target.template.raw or {}).get("spell_resistance", 0))
    if sr <= 0:
        return True, 0  # no SR
    r = roller.roll("1d20")
    natural = r.terms[0].rolls[0]
    total = natural + caster_lvl
    return total >= sr, total


# ---------------------------------------------------------------------------
# Top-level cast
# ---------------------------------------------------------------------------


def cast_spell(
    caster: Combatant,
    spell: Spell,
    targets: list[Combatant],
    spell_level: int,
    registry: ContentRegistry,
    roller: Roller,
    current_round: int = 1,
    metamagic: list[str] | None = None,
    grid: object | None = None,
    encounter: object | None = None,
) -> SpellOutcome:
    """Resolve a spell cast.

    The caller is responsible for slot consumption (so we can support
    different slot pools — domain slots, specialist bonuses, etc.).
    ``current_round`` is used to compute expiration for modifiers with
    bounded duration.

    ``metamagic`` lists feat IDs the caster is applying — currently
    ``empower_spell`` and ``maximize_spell`` are honored as
    post-process damage/healing transforms. ``still_spell`` /
    ``silent_spell`` / ``quicken_spell`` are slot-cost-only here; the
    caller (turn_executor) handles their cast-time effects.
    """
    cl = caster_level(caster)
    dc = save_dc_for(caster, spell_level, registry)
    metamagic = list(metamagic or [])
    # Sorcerer bloodline arcana DC bonuses (fey / infernal / arcane).
    dc += _bloodline_dc_bonus(caster, spell, metamagic)

    outcome = SpellOutcome(
        spell_id=spell.id,
        caster_id=caster.id,
        success=True,
        targets_affected=[],
        damage_per_target={},
        healing_per_target={},
        conditions_applied={},
        modifiers_applied={},
        save_dc=dc,
        metamagic=list(metamagic),
        grid=grid,
        encounter=encounter,
    )
    metamagic_note = (
        f" [metamagic: {', '.join(metamagic)}]" if metamagic else ""
    )
    outcome.log.append(
        f"{caster.name} casts {spell.name}"
        f" (CL {cl}, save DC {dc}){metamagic_note}"
    )

    handler = _EFFECT_HANDLERS.get(spell.effect.get("kind", ""))
    if handler is None:
        outcome.success = False
        outcome.log.append(
            f"effect kind {spell.effect.get('kind')!r} not implemented"
        )
        return outcome

    # HD cap (e.g. sleep affects up to N HD of creatures, lowest first).
    hd_cap = spell.effect.get("max_hit_dice")
    if hd_cap is not None and targets:
        sorted_targets = sorted(
            targets, key=lambda t: _hit_dice(t),
        )
        kept: list[Combatant] = []
        used_hd = 0
        for t in sorted_targets:
            t_hd = _hit_dice(t)
            if used_hd + t_hd <= int(hd_cap):
                kept.append(t)
                used_hd += t_hd
            # Otherwise this target (and any with higher HD) is unaffected.
        targets = kept
        outcome.log.append(
            f"  HD cap {hd_cap}: affecting {len(kept)} target(s) "
            f"({used_hd} HD used)"
        )

    for tgt in targets:
        # Spell resistance.
        if spell.spell_resistance == "yes":
            ok, total = overcomes_sr(cl, tgt, roller)
            if not ok:
                outcome.log.append(
                    f"  SR check failed against {tgt.name} (rolled {total})"
                )
                continue
        # Dispatch to handler.
        handler(
            caster, spell, tgt, dc, cl, registry, roller, outcome,
            current_round=current_round,
        )

    # Metamagic post-processing on the rolled damage / healing numbers.
    # Empower: ×1.5 (rounded down) of the rolled values. Maximize is
    # NOT post-processed: handlers roll with take_max=True so each die
    # already returned its max face. RAW: empower-then-maximize is
    # additive ("damage + half-damage-empowered + max-damage-maximized")
    # but we simplify to multiplicative compose — applying empower
    # after the dice were already maxed gives 1.5× of the maximum,
    # which slightly overshoots the RAW-stacked total.
    if "empower_spell" in metamagic:
        target_lookup = {t.id: t for t in targets}
        for tid, dmg in list(outcome.damage_per_target.items()):
            new_dmg = (dmg * 3) // 2
            delta = new_dmg - dmg
            if delta > 0 and tid in target_lookup:
                target_lookup[tid].take_damage(delta)
            outcome.damage_per_target[tid] = new_dmg
        for tid, heal_amt in list(outcome.healing_per_target.items()):
            new_heal = (heal_amt * 3) // 2
            delta = new_heal - heal_amt
            if delta > 0 and tid in target_lookup:
                target_lookup[tid].heal(delta)
            outcome.healing_per_target[tid] = new_heal
        outcome.log.append("  empower: rolled values ×1.5")

    return outcome


# ---------------------------------------------------------------------------
# Duration helpers
# ---------------------------------------------------------------------------


def _hit_dice(target: Combatant) -> int:
    """Approximate HD for a Combatant.

    For monsters: parse the leading integer of ``hit_dice`` (e.g., "1d10+1" → 1).
    For characters: total class levels from the underlying Character.
    Default 1 if neither template is recognised.
    """
    if target.template_kind == "monster" and target.template is not None:
        hd_str = getattr(target.template, "hit_dice", "1") or "1"
        try:
            return max(1, int(hd_str.split("d")[0]))
        except (ValueError, IndexError):
            return 1
    if target.template_kind == "character" and target.template is not None:
        return max(1, int(getattr(target.template, "level", 1)))
    return 1


def _expires_round(
    effect: dict, caster_level_value: int, current_round: int,
    extend: bool = False,
) -> int | None:
    """Compute expires_round given the effect's duration spec.

    Reads ``duration_rounds_per_caster_level``,
    ``duration_minutes_per_caster_level``, or
    ``duration_hours_per_caster_level`` from the effect dict.

    ``extend``: if True, doubles the computed duration (Extend Spell
    metamagic). Has no effect on instantaneous durations.

    Returns ``None`` for instantaneous or untracked durations.
    """
    rounds: int | None = None
    if "duration_rounds_per_caster_level" in effect:
        rounds = int(effect["duration_rounds_per_caster_level"]) * caster_level_value
    elif "duration_minutes_per_caster_level" in effect:
        rounds = int(effect["duration_minutes_per_caster_level"]) * caster_level_value * 10
    elif "duration_hours_per_caster_level" in effect:
        rounds = int(effect["duration_hours_per_caster_level"]) * caster_level_value * 600
    if rounds is None or rounds <= 0:
        return None
    if extend:
        rounds *= 2
    return current_round + rounds


# ---------------------------------------------------------------------------
# Effect handlers
# ---------------------------------------------------------------------------


def _handle_heal(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    eff = spell.effect
    dice_str = str(eff.get("dice", "1d8"))
    plus_cl = bool(eff.get("plus_caster_level", True))
    max_plus = int(eff.get("max_plus", 5))
    bonus = min(cl, max_plus) if plus_cl else 0
    take_max = "maximize_spell" in out.metamagic
    r = roller.roll(dice_str, take_max=take_max)
    healed = r.total + bonus
    target.heal(healed)
    if "dying" in target.conditions and target.current_hp >= 0:
        target.remove_condition("dying")
    out.targets_affected.append(target.id)
    out.healing_per_target[target.id] = healed
    out.log.append(f"  heals {target.name} for {healed} (rolled {r.total} + {bonus})")


def _handle_magic_missile(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    # Determine missile count.
    eff = spell.effect
    table = eff.get("missiles_at_caster_level") or {}
    count = 1
    for level_str, c in sorted(table.items(), key=lambda x: int(x[0])):
        if cl >= int(level_str):
            count = int(c)
    dmg_dice = str(eff.get("damage_per_missile", "1d4+1"))
    take_max = "maximize_spell" in out.metamagic
    requires_touch = bool(
        eff.get("ranged_touch_attack") or eff.get("melee_touch_attack")
    )
    ranged = bool(eff.get("ranged_touch_attack"))
    total_damage = 0
    hit_count = 0
    total_dice = 0  # for draconic bloodline arcana per-die accounting
    for i in range(count):
        if requires_touch:
            hit, log_lines = resolve_spell_touch_attack(
                caster, target, ranged=ranged, roller=roller,
                grid=out.grid,
            )
            out.log.extend(log_lines)
            if not hit:
                continue
        r = roller.roll(dmg_dice, take_max=take_max)
        total_damage += r.total
        hit_count += 1
        # Count dice rolled in this missile so draconic arcana can
        # apply +1 per die. ``r.terms[0]`` holds the rolled-dice list
        # when the expression contains a die term; we sum dice across
        # all terms defensively.
        for term in r.terms:
            total_dice += len(getattr(term, "rolls", []) or [])
        out.log.append(f"  missile {i+1}: {r.breakdown}")
    # Intense Spells (Evocation school L1 passive): once per spell,
    # add max(1, wiz_lvl // 2) to evocation damage.
    if hit_count > 0:
        intense = _intense_spells_bonus(caster, spell)
        if intense:
            total_damage += intense
            out.log.append(f"  intense_spells +{intense}")
    # Draconic Bloodline arcana: +1 damage per die rolled on a
    # matching-energy spell (RAW: "deals +1 point of damage per die
    # rolled").
    if hit_count > 0:
        draconic = _draconic_damage_bonus_per_die(caster, spell)
        if draconic and total_dice:
            extra = draconic * total_dice
            total_damage += extra
            out.log.append(f"  draconic_arcana +{extra} ({total_dice}×{draconic})")
    damage_type = str(eff.get("damage_type", "force")) or None
    spell_tags = _spell_attack_tags(spell, damage_type)
    applied, energy_note = apply_typed_damage(
        target, total_damage, damage_type,
        attack_tags=spell_tags, roller=roller,
    )
    if target.current_hp <= 0:
        target.add_condition("dying")
    if target.current_hp <= -10:
        target.add_condition("dead")
    out.targets_affected.append(target.id)
    out.damage_per_target[target.id] = applied
    note = f" ({energy_note})" if energy_note else ""
    out.log.append(
        f"  {hit_count}/{count} missile(s) hit {target.name} "
        f"for {applied}{note}"
    )


def _handle_scaling_damage(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    eff = spell.effect
    # Touch-attack roll if the spell requires one. On miss, the
    # spell has no effect (RAW: a missed touch attack does nothing).
    if eff.get("ranged_touch_attack") or eff.get("melee_touch_attack"):
        ranged = bool(eff.get("ranged_touch_attack"))
        hit, log_lines = resolve_spell_touch_attack(
            caster, target, ranged=ranged, roller=roller,
            grid=out.grid,
        )
        out.log.extend(log_lines)
        if not hit:
            return
    dice_per = str(eff.get("dice", "1d4"))
    scaling = eff.get("scaling", "fixed")
    max_dice = int(eff.get("max_dice", 1))
    if scaling == "per_caster_level":
        n_dice = min(cl, max_dice)
    else:
        n_dice = 1
    # Build expression like "5d4" from "1d4" * 5.
    base = dice_per.split("d")
    sides = base[1].split("+")[0]
    expr = f"{n_dice}d{sides}"
    take_max = "maximize_spell" in out.metamagic
    rolled = roller.roll(expr, take_max=take_max)
    raw_damage = rolled.total

    # Save halves?
    save_kind, semantic = parse_saving_throw(spell.saving_throw)
    final = raw_damage
    if save_kind:
        # Cover Reflex bonus: +2 (hard) or +4 (greater) when there are
        # walls between the caster and the target. Computed only when
        # the cast received a grid context.
        cover_bonus = 0
        if save_kind == "ref" and out.grid is not None:
            from .turn_executor import _cover_reflex_bonus
            cover_bonus = _cover_reflex_bonus(caster, target, out.grid)
        passed, nat, total = roll_save(
            target, save_kind, dc, roller,
            context=_spell_save_context(spell),
            cover_bonus=cover_bonus,
            encounter=out.encounter, grid=out.grid,
        )
        cover_note = f" + {cover_bonus} cover" if cover_bonus else ""
        out.log.append(
            f"  {target.name} {save_kind} save: d20={nat}+"
            f"{target.save(save_kind)}{cover_note}={total} vs DC {dc} → "
            f"{'PASS' if passed else 'FAIL'}"
        )
        if passed and semantic == "half":
            final = raw_damage // 2
        elif passed and semantic in ("negates", "harmless_negates"):
            final = 0
    # Intense Spells (Evocation school L1 passive): adds once per
    # spell. Applied after save-halving so the bonus contributes
    # cleanly to both half-damage and full-damage outcomes.
    if final > 0:
        intense = _intense_spells_bonus(caster, spell)
        if intense:
            final += intense
            out.log.append(f"  intense_spells +{intense}")
        # Draconic Bloodline arcana: +1 damage per die rolled on a
        # matching-energy spell. For scaling-damage spells we know
        # the die count from ``n_dice`` (set above).
        draconic = _draconic_damage_bonus_per_die(caster, spell)
        if draconic:
            extra = draconic * n_dice
            final += extra
            out.log.append(f"  draconic_arcana +{extra} "
                           f"({n_dice}×{draconic})")
    damage_type = str(eff.get("damage_type", "")) or None
    spell_tags = _spell_attack_tags(spell, damage_type)
    applied, energy_note = apply_typed_damage(
        target, final, damage_type,
        attack_tags=spell_tags, roller=roller,
    )
    if target.current_hp <= 0:
        target.add_condition("dying")
    if target.current_hp <= -10:
        target.add_condition("dead")
    out.targets_affected.append(target.id)
    out.damage_per_target[target.id] = applied
    note = f" ({energy_note})" if energy_note else ""
    out.log.append(
        f"  {target.name} takes {applied} {damage_type or ''} damage"
        f" (rolled {raw_damage}){note}"
    )


def _handle_buff_target(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    eff = spell.effect
    mods = eff.get("modifiers") or []
    expires = _expires_round(
        eff, cl, current_round,
        extend="extend_spell" in out.metamagic,
    )
    applied_records: list[dict] = []
    for m in mods:
        modifier = mod(
            value=int(m["value"]),
            type=str(m["modifier_type"]),
            target=str(m["target"]),
            source=f"spell:{spell.id}",
            expires_round=expires,
        )
        target.add_modifier(modifier)
        applied_records.append({
            "value": modifier.value,
            "type": modifier.type,
            "target": modifier.target,
            "expires_round": modifier.expires_round,
        })
    out.targets_affected.append(target.id)
    out.modifiers_applied.setdefault(target.id, []).extend(applied_records)
    duration_msg = f" (expires R{expires})" if expires else ""
    pretty = ", ".join(
        f"{'+' if r['value'] >= 0 else ''}{r['value']} {r['type']} to {r['target']}"
        for r in applied_records
    )
    out.log.append(f"  {target.name}: {pretty}{duration_msg}")


def _handle_buff_party(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    # The encounter loop should pre-filter targets to allies; we just apply.
    _handle_buff_target(caster, spell, target, dc, cl, registry, roller, out)


def resolve_spell_touch_attack(
    caster: Combatant,
    target: Combatant,
    *,
    ranged: bool,
    roller: Roller,
    grid=None,
    encounter=None,
) -> tuple[bool, list[str]]:
    """Roll a spell touch attack against ``target``'s touch AC.

    PF1 RAW: spells flagged as ranged_touch_attack or
    melee_touch_attack require an attack roll vs the target's touch
    AC. Hit on total ≥ touch AC OR natural 20; auto-miss on natural 1.
    BAB + Dex (ranged) or BAB + Str (melee) + size; range increment
    penalty for ranged-touch beyond the spell's first range increment
    (we use the close/medium/long bands for the spell's stated range
    rather than a strict per-increment table — within the spell's max
    range, no penalty in v1).

    Returns ``(hit, log_lines)``.
    """
    bab = int(caster.bases.get("bab", 0))
    ability = "dex" if ranged else "str"
    if (
        caster.template_kind == "character"
        and caster.template is not None
    ):
        scores = caster.template.base_ability_scores
        try:
            base = int(scores.get(ability) or 10)
        except TypeError:
            base = 10
        for m in caster.modifiers.for_target(f"ability:{ability}"):
            base += m.value
        score = int(base)
    elif (
        caster.template_kind == "monster"
        and caster.template is not None
    ):
        scores = getattr(caster.template, "ability_scores", None) or {}
        score = int(scores.get(ability, 10) or 10)
    else:
        score = 10
    ability_mod = (score - 10) // 2 if score > 0 else 0
    # Size modifier to attack — typed AC mods carry size; we mirror
    # via the actor's size if available. PF1 size-to-attack table:
    # Fine +8, Diminutive +4, Tiny +2, Small +1, Medium 0, Large -1,
    # Huge -2, Gargantuan -4, Colossal -8.
    size_to_atk = {
        "fine": 8, "diminutive": 4, "tiny": 2, "small": 1,
        "medium": 0, "large": -1, "huge": -2,
        "gargantuan": -4, "colossal": -8,
    }
    size_mod = size_to_atk.get(
        str(getattr(caster, "size", "medium")).lower(), 0,
    )
    # General-purpose attack modifiers (Inspire Courage, etc.).
    from .modifiers import compute as _compute_mod
    attack_general = _compute_mod(0, caster.modifiers.for_target("attack"))
    if ranged:
        attack_general += _compute_mod(
            0, caster.modifiers.for_target("attack:ranged"),
        )
    bonus = bab + ability_mod + size_mod + attack_general
    r = roller.roll("1d20")
    nat = int(r.terms[0].rolls[0])
    total = nat + bonus
    target_ac = target.ac("touch")
    hit = (nat == 20) or (nat != 1 and total >= target_ac)
    label = "ranged touch" if ranged else "melee touch"
    log = [
        f"  {label} attack: d20={nat} + {bonus} = {total} "
        f"vs touch AC {target_ac} → {'HIT' if hit else 'MISS'}"
    ]
    return hit, log


def _sorcerer_bloodline_id(caster: Combatant) -> str:
    """Return the caster's sorcerer bloodline id, or empty if not a
    sorcerer."""
    if caster.template_kind != "character" or caster.template is None:
        return ""
    return str((caster.template.class_choices or {}).get(
        "sorcerer_bloodline", "",
    ))


def _bloodline_dc_bonus(
    caster: Combatant, spell: Spell, metamagic: list[str],
) -> int:
    """Bloodline arcana save-DC bonuses (Phase 4.3c).

    - Fey (RAW Foundry pack ``Fey Bloodline``): +2 DC on
      compulsion-subschool spells.
    - Infernal (RAW ``Infernal Bloodline``): +2 DC on charm-
      subschool spells.
    - Arcane (RAW ``Arcane Bloodline``): +1 DC when at least one
      applied metamagic raises the spell's slot level (does not
      stack with itself; excludes Heighten Spell, which is the only
      Heighten-style we model).

    Other bloodlines: 0.
    """
    bl = _sorcerer_bloodline_id(caster)
    if not bl:
        return 0
    if caster.class_levels.get("sorcerer", 0) <= 0:
        return 0
    subschool = (spell.subschool or "").lower()
    if bl == "fey" and subschool == "compulsion":
        return 2
    if bl == "infernal" and subschool == "charm":
        return 2
    if bl == "arcane":
        # Slot-increasing metamagic (per RAW: any feat that increases
        # slot used by ≥1; ``heighten_spell`` is excluded). We
        # currently model empower_spell (+2 slot), maximize_spell
        # (+3 slot), extend_spell (+1 slot), quicken_spell (+4),
        # still_spell (+1), silent_spell (+1).
        slot_raising = {"empower_spell", "maximize_spell",
                        "extend_spell", "quicken_spell",
                        "still_spell", "silent_spell"}
        if any(m in slot_raising for m in (metamagic or [])):
            return 1
    return 0


def _draconic_damage_bonus_per_die(
    caster: Combatant, spell: Spell,
) -> int:
    """Draconic Bloodline arcana: +1 damage per die rolled when the
    spell's energy descriptor matches the sorcerer's chosen dragon
    type. Matching is done via the bloodline JSON's
    ``dragon_energy_by_type`` table.
    """
    bl = _sorcerer_bloodline_id(caster)
    if bl != "draconic":
        return 0
    if caster.class_levels.get("sorcerer", 0) <= 0:
        return 0
    descriptors = {str(d).lower() for d in (spell.descriptors or [])}
    if not descriptors:
        return 0
    dragon_type = (caster.template.class_choices or {}).get(
        "sorcerer_dragon_type", "",
    )
    # Reuse the bloodline JSON's mapping rather than hardcoding here.
    from .content import default_registry
    try:
        bl_data = default_registry().get_sorcerer_bloodline("draconic")
    except Exception:
        return 0
    energy_map = (bl_data.raw or {}).get("dragon_energy_by_type", {})
    matching = energy_map.get(dragon_type)
    if matching and matching.lower() in descriptors:
        return 1
    return 0


def _intense_spells_bonus(caster: Combatant, spell: Spell) -> int:
    """Evoker's Intense Spells passive: when an evocation spell deals
    hit-point damage, add max(1, wiz_lvl // 2) to the damage (once per
    spell, not once per missile / ray). Other classes / non-evocation
    spells: 0.

    RAW (Foundry pack ``Intense Spells``): "Whenever you cast an
    evocation spell that deals hit point damage, add 1/2 your wizard
    level to the damage (minimum +1). This bonus only applies once to
    a spell, not once per missile or ray ..."
    """
    if (spell.school or "").lower() != "evocation":
        return 0
    if caster.template_kind != "character" or caster.template is None:
        return 0
    school = ((caster.template.class_choices or {}).get("wizard_school")
              or "")
    if school != "evocation":
        return 0
    wl = int(caster.class_levels.get("wizard", 0))
    if wl <= 0:
        return 0
    return max(1, wl // 2)


def _spell_save_context(spell: Spell) -> dict:
    """Build the effect-tag context for save resolution against a spell.

    Used by:
    - situational racial save bonuses (hardy +2 vs spells,
      illusion_resistance +2 vs illusion, etc.) via ``effect_tags``.
    - bardic countersong / distraction reactive intercepts (matching on
      ``descriptors`` for sonic / language-dependent and on
      ``school`` + ``subschool`` for illusion-pattern / illusion-figment).
    """
    tags: list[str] = ["spell"]
    if spell.school:
        tags.append(spell.school.lower())
    return {
        "effect_tags": tags,
        "school": (spell.school or "").lower(),
        "subschool": (spell.subschool or "").lower(),
        "descriptors": [str(d).lower() for d in (spell.descriptors or [])],
    }


def _handle_apply_condition_save(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    """Apply a condition gated by a saving throw.

    PF1 ``save negates`` semantic: save fail → condition applied;
    save success → no effect.

    PF1 ``save partial`` semantic: save fail → primary condition
    applied; save success → lesser condition applied (declared on the
    spell as ``effect.condition_on_save_success``). Cause Fear is
    the canonical example: fail → frightened, success → shaken.
    """
    eff = spell.effect
    cond = str(eff["condition"])
    cond_on_save = eff.get("condition_on_save_success")
    # Touch-attack roll if the spell requires one (e.g. touch_of_fatigue).
    if eff.get("ranged_touch_attack") or eff.get("melee_touch_attack"):
        ranged = bool(eff.get("ranged_touch_attack"))
        hit, log_lines = resolve_spell_touch_attack(
            caster, target, ranged=ranged, roller=roller,
            grid=out.grid,
        )
        out.log.extend(log_lines)
        if not hit:
            return
    save_kind, _ = parse_saving_throw(spell.saving_throw)
    if save_kind:
        passed, nat, total = roll_save(
            target, save_kind, dc, roller, context=_spell_save_context(spell),
            encounter=out.encounter, grid=out.grid,
        )
        out.log.append(
            f"  {target.name} {save_kind} save: d20={nat}+{target.save(save_kind)}={total} vs DC {dc} → "
            f"{'PASS' if passed else 'FAIL'}"
        )
        if passed:
            if cond_on_save:
                # Save partial: apply the lesser condition.
                if target.add_condition(str(cond_on_save)):
                    target.register_sourced_condition(
                        f"spell:{spell.id}", str(cond_on_save),
                    )
                out.targets_affected.append(target.id)
                out.conditions_applied.setdefault(
                    target.id, [],
                ).append(str(cond_on_save))
                out.log.append(
                    f"  {target.name} (save partial): {cond_on_save}"
                )
            return
    if target.add_condition(cond):
        target.register_sourced_condition(f"spell:{spell.id}", cond)
    out.targets_affected.append(target.id)
    out.conditions_applied.setdefault(target.id, []).append(cond)
    out.log.append(f"  {target.name} now has condition: {cond}")


def _handle_charm(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    save_kind, _ = parse_saving_throw(spell.saving_throw)
    if save_kind:
        passed, nat, total = roll_save(
            target, save_kind, dc, roller, context=_spell_save_context(spell),
            encounter=out.encounter, grid=out.grid,
        )
        out.log.append(
            f"  {target.name} {save_kind} save: d20={nat}+{target.save(save_kind)}={total} vs DC {dc} → "
            f"{'PASS' if passed else 'FAIL'}"
        )
        if passed:
            return
    # Team flip: target joins caster's team for the spell duration.
    original_team = target.team
    target.team = caster.team
    source = f"spell:{spell.id}"
    target.add_modifier(Modifier(
        value=0, type="untyped", target="charm_marker",
        source=source, expires_round=None,
    ))
    target.add_condition("charmed")
    target.register_sourced_condition(source, "charmed")
    out.targets_affected.append(target.id)
    out.conditions_applied.setdefault(target.id, []).append("charmed")
    out.log.append(
        f"  {target.name} is charmed and joins {caster.team} (was {original_team})"
    )


def _handle_stabilize(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    if "dying" in target.conditions:
        target.remove_condition("dying")
        target.add_condition("stable")
        out.targets_affected.append(target.id)
        out.log.append(f"  stabilizes {target.name}")
    else:
        out.log.append(f"  {target.name} not dying, no effect")


def _handle_utility(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    out.log.append(f"  {spell.name} cast (utility, no combat effect)")
    out.targets_affected.append(target.id)


def active_spell_sources(target: Combatant) -> list[str]:
    """Enumerate active ``spell:<id>`` sources currently affecting ``target``.

    Walks the target's modifiers and the sourced-condition map, and
    returns each unique ``spell:*`` source. Used by dispel to pick a
    candidate to remove.
    """
    sources: set[str] = set()
    for m in target.modifiers.modifiers:
        if m.source.startswith("spell:"):
            sources.add(m.source)
    for src in target.sourced_conditions.keys():
        if src.startswith("spell:"):
            sources.add(src)
    return sorted(sources)


def _handle_dispel_magic(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    """PF1 targeted dispel: pick the highest-CL effect on the target,
    roll 1d20 + caster_level vs DC 11 + that effect's CL.

    For v1 we don't track per-effect CL (modifiers don't store it), so
    we use a flat DC 11 + the dispelling caster's own CL as a stand-in
    for "average opposed check". That matches the PF1 expected-value
    behavior reasonably (a level-7 wizard dispelling a level-7 effect
    rolls vs DC 18 = need 11+ on d20 = 50% — which matches RAW for
    same-CL).
    """
    sources = active_spell_sources(target)
    if not sources:
        out.log.append(f"  {target.name} has no active spell effects to dispel")
        return
    # PF1 default: target the most-recent / highest-CL. We don't track
    # CL per modifier; pick the first source alphabetically for
    # determinism.
    target_source = sources[0]
    dispel_dc = 11 + cl
    r = roller.roll("1d20")
    nat = r.terms[0].rolls[0]
    total = nat + cl
    out.log.append(
        f"  dispel {target_source} on {target.name}: d20={nat}+{cl}={total} "
        f"vs DC {dispel_dc} → {'PASS' if total >= dispel_dc else 'FAIL'}"
    )
    if total >= dispel_dc:
        n_mods, cond_ids = target.remove_effects_from_source(target_source)
        out.targets_affected.append(target.id)
        out.log.append(
            f"  dispelled: {n_mods} modifier(s), conditions cleared: {cond_ids}"
        )


def _handle_color_spray(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    """PF1 Color Spray: HD-tiered effect on failed Will save.

    - 2 HD or less: unconscious + blind + stunned
    - 3-5 HD: blind + stunned
    - 6+ HD: stunned
    Successful Will save negates entirely. We approximate the
    multi-step duration (RAW: unconscious 2d4 → blind 1d4 → stunned
    1) by applying the conditions; the engine ticks them down or
    leaves them indefinite — for v1 we don't track per-condition
    durations on these stack-applied conditions.
    """
    save_kind, _ = parse_saving_throw(spell.saving_throw)
    if save_kind:
        passed, nat, total = roll_save(
            target, save_kind, dc, roller,
            context=_spell_save_context(spell),
            encounter=out.encounter, grid=out.grid,
        )
        out.log.append(
            f"  {target.name} {save_kind} save: d20={nat}+"
            f"{target.save(save_kind)}={total} vs DC {dc} → "
            f"{'PASS' if passed else 'FAIL'}"
        )
        if passed:
            return
    hd = _hit_dice(target)
    source = f"spell:{spell.id}"
    applied: list[str] = []
    if hd <= 2:
        for c in ("unconscious", "blinded", "stunned"):
            if target.add_condition(c):
                target.register_sourced_condition(source, c)
                applied.append(c)
    elif hd <= 5:
        for c in ("blinded", "stunned"):
            if target.add_condition(c):
                target.register_sourced_condition(source, c)
                applied.append(c)
    else:
        if target.add_condition("stunned"):
            target.register_sourced_condition(source, "stunned")
            applied.append("stunned")
    if applied:
        out.targets_affected.append(target.id)
        out.conditions_applied.setdefault(target.id, []).extend(applied)
        out.log.append(
            f"  {target.name} ({hd} HD) now: {', '.join(applied)}"
        )


def _handle_apply_single_use_buff(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    """Apply a discharge-on-roll buff that's consumed by the next
    qualifying d20 roll (Guidance: +1 competence on a single attack /
    save / skill check). The same source is laid down on every
    candidate roll target; first roll consumes them all.
    """
    eff = spell.effect
    value = int(eff.get("value", 1))
    bonus_type = str(eff.get("modifier_type", "competence"))
    expires = _expires_round(
        eff, cl, current_round,
        extend="extend_spell" in out.metamagic,
    )
    src = f"single_use:{spell.id}:{caster.id}"
    targets = list(eff.get("targets") or [
        "attack", "fort_save", "ref_save", "will_save", "skill_check",
    ])
    for tgt in targets:
        target.modifiers.add(mod(
            value=value, type=bonus_type, target=str(tgt),
            source=src, expires_round=expires,
        ))
    target.pending_single_use_sources.add(src)
    out.targets_affected.append(target.id)
    out.log.append(
        f"  {target.name}: +{value} {bonus_type} on next "
        f"{'/'.join(targets)} (single-use, src={src})"
    )


def _handle_apply_temp_hp(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    """Grant temporary hit points to ``target`` (Virtue, False Life
    when wired, etc.). RAW: temp HP doesn't stack with itself; the
    higher pool wins. Duration is per-spell; expiry handled in
    Combatant.tick_round.
    """
    eff = spell.effect
    amount = int(eff.get("amount", 1))
    expires = _expires_round(
        eff, cl, current_round,
        extend="extend_spell" in out.metamagic,
    )
    target.apply_temp_hp(amount, expires)
    out.targets_affected.append(target.id)
    duration_msg = f" (expires R{expires})" if expires else ""
    out.log.append(
        f"  {target.name}: +{amount} temporary HP{duration_msg} "
        f"(pool now {target.temp_hp})"
    )


def _handle_apply_bleed(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    """Apply ongoing bleed damage (Bleed cantrip: 1 HP/round on a
    target with HP <= 0). Will save negates."""
    eff = spell.effect
    # RAW: target must have -1 or fewer HP (i.e. dying / stable, not
    # disabled-at-0). The flag name is historical; the check is
    # current_hp <= -1 not <= 0.
    requires_below_zero = bool(eff.get("requires_below_zero_hp"))
    if requires_below_zero and target.current_hp > -1:
        out.log.append(
            f"  {target.name} is not at -1 or fewer HP; bleed has no effect"
        )
        return
    save_kind, semantic = parse_saving_throw(spell.saving_throw)
    if save_kind:
        passed, nat, total = roll_save(
            target, save_kind, dc, roller,
            context=_spell_save_context(spell),
            encounter=out.encounter, grid=out.grid,
        )
        out.log.append(
            f"  {target.name} {save_kind} save: d20={nat}+"
            f"{target.save(save_kind)}={total} vs DC {dc} → "
            f"{'PASS' if passed else 'FAIL'}"
        )
        if passed and semantic in ("negates", "harmless_negates"):
            return
    amount = int(eff.get("amount", 1))
    target.apply_bleed(amount)
    out.targets_affected.append(target.id)
    out.log.append(
        f"  {target.name} starts bleeding ({amount} HP/round)"
    )


_EFFECT_HANDLERS: dict[str, Any] = {
    "heal":                  _handle_heal,
    "magic_missile":         _handle_magic_missile,
    "scaling_damage":        _handle_scaling_damage,
    "buff_target":           _handle_buff_target,
    "buff_party":            _handle_buff_party,
    "apply_condition_save":  _handle_apply_condition_save,
    "charm":                 _handle_charm,
    "stabilize":             _handle_stabilize,
    "utility":               _handle_utility,
    "dispel_magic":          _handle_dispel_magic,
    "color_spray":           _handle_color_spray,
    "apply_bleed":           _handle_apply_bleed,
    "apply_temp_hp":         _handle_apply_temp_hp,
    "apply_single_use_buff": _handle_apply_single_use_buff,
}
