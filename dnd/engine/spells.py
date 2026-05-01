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
    """10 + spell level + key ability modifier (+ Spell Focus, not yet wired)."""
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
) -> tuple[bool, int, int]:
    """Roll a saving throw. Returns (passed, natural, total)."""
    save_total = target.save(save_kind)
    r = roller.roll("1d20")
    nat = r.terms[0].rolls[0]
    total = nat + save_total
    if nat == 1:
        return False, nat, total
    if nat == 20:
        return True, nat, total
    return total >= dc, nat, total


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
) -> SpellOutcome:
    """Resolve a spell cast.

    The caller is responsible for slot consumption (so we can support
    different slot pools — domain slots, specialist bonuses, etc.).
    ``current_round`` is used to compute expiration for modifiers with
    bounded duration.
    """
    cl = caster_level(caster)
    dc = save_dc_for(caster, spell_level, registry)

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
    )
    outcome.log.append(
        f"{caster.name} casts {spell.name} (CL {cl}, save DC {dc})"
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
) -> int | None:
    """Compute expires_round given the effect's duration spec.

    Reads ``duration_rounds_per_caster_level``,
    ``duration_minutes_per_caster_level``, or
    ``duration_hours_per_caster_level`` from the effect dict.

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
    r = roller.roll(dice_str)
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
    total_damage = 0
    for i in range(count):
        r = roller.roll(dmg_dice)
        total_damage += r.total
        out.log.append(f"  missile {i+1}: {r.breakdown}")
    target.take_damage(total_damage)
    if target.current_hp <= 0:
        target.add_condition("dying")
    if target.current_hp <= -10:
        target.add_condition("dead")
    out.targets_affected.append(target.id)
    out.damage_per_target[target.id] = total_damage
    out.log.append(f"  {count} missile(s) hit {target.name} for {total_damage}")


def _handle_scaling_damage(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    eff = spell.effect
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
    rolled = roller.roll(expr)
    raw_damage = rolled.total

    # Save halves?
    save_kind, semantic = parse_saving_throw(spell.saving_throw)
    final = raw_damage
    if save_kind:
        passed, nat, total = roll_save(target, save_kind, dc, roller)
        out.log.append(
            f"  {target.name} {save_kind} save: d20={nat}+{target.save(save_kind)}={total} vs DC {dc} → "
            f"{'PASS' if passed else 'FAIL'}"
        )
        if passed and semantic == "half":
            final = raw_damage // 2
        elif passed and semantic in ("negates", "harmless_negates"):
            final = 0
    target.take_damage(final)
    if target.current_hp <= 0:
        target.add_condition("dying")
    if target.current_hp <= -10:
        target.add_condition("dead")
    out.targets_affected.append(target.id)
    out.damage_per_target[target.id] = final
    out.log.append(f"  {target.name} takes {final} damage (rolled {raw_damage})")


def _handle_buff_target(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    eff = spell.effect
    mods = eff.get("modifiers") or []
    expires = _expires_round(eff, cl, current_round)
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


def _handle_apply_condition_save(
    caster: Combatant, spell: Spell, target: Combatant, dc: int,
    cl: int, registry: ContentRegistry, roller: Roller, out: SpellOutcome,
    current_round: int = 1,
) -> None:
    eff = spell.effect
    cond = str(eff["condition"])
    save_kind, _ = parse_saving_throw(spell.saving_throw)
    if save_kind:
        passed, nat, total = roll_save(target, save_kind, dc, roller)
        out.log.append(
            f"  {target.name} {save_kind} save: d20={nat}+{target.save(save_kind)}={total} vs DC {dc} → "
            f"{'PASS' if passed else 'FAIL'}"
        )
        if passed:
            return
    target.add_condition(cond)
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
        passed, nat, total = roll_save(target, save_kind, dc, roller)
        out.log.append(
            f"  {target.name} {save_kind} save: d20={nat}+{target.save(save_kind)}={total} vs DC {dc} → "
            f"{'PASS' if passed else 'FAIL'}"
        )
        if passed:
            return
    # Team flip: target joins caster's team for the spell duration.
    original_team = target.team
    target.team = caster.team
    target.add_modifier(Modifier(
        value=0, type="untyped", target="charm_marker",
        source=f"spell:{spell.id}", expires_round=None,
    ))
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
}
