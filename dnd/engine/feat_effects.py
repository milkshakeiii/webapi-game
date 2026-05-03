"""Feat → modifier list.

Each authored feat that has passive mechanical effects produces a list
of ``Modifier`` objects to add to the combatant's ``ModifierCollection``.

Active / situational effects (Power Attack as a turn-time tradeoff,
Cleave as an action, Combat Reflexes as an AoO-rate change) aren't
purely passive — they're wired in the turn executor or combat resolver.
This module covers the passive modifier-shaped feats.

Parameterized feats (Skill Focus, Weapon Focus) are stored on the
character with the parameter encoded after the feat ID — e.g.
``"skill_focus_perception"`` or ``"weapon_focus_longsword"``. The
parser here strips the prefix.
"""

from __future__ import annotations

from .modifiers import Modifier, mod


def feat_modifiers(feat_id: str, character) -> list[Modifier]:
    """Return all passive modifiers granted by ``feat_id`` to ``character``.

    Returns an empty list for feats without passive modifier effects
    (active feats, item-creation feats, etc.).
    """
    src = f"feat:{feat_id}"

    # ── Save-improving feats (untyped +2 to one save). ─────────────
    if feat_id == "iron_will":
        return [mod(2, "untyped", "will_save", src)]
    if feat_id == "lightning_reflexes":
        return [mod(2, "untyped", "ref_save", src)]
    if feat_id == "great_fortitude":
        return [mod(2, "untyped", "fort_save", src)]

    # ── Other passives. ─────────────────────────────────────────────
    if feat_id == "improved_initiative":
        return [mod(4, "untyped", "initiative", src)]
    if feat_id == "toughness":
        # +3 HP at L1; +1 per HD beyond third — i.e. max(3, total_levels).
        level = int(getattr(character, "level", 1) or 1)
        bonus = max(3, level)
        return [mod(bonus, "untyped", "hp_max", src)]
    if feat_id == "dodge":
        return [mod(1, "dodge", "ac", src)]

    # ── Skill-pair feats (each +2 to two skills). ───────────────────
    skill_pairs = {
        "alertness":         [("perception", 2), ("sense_motive", 2)],
        "athletic":          [("climb", 2), ("swim", 2)],
        "stealthy":          [("stealth", 2), ("escape_artist", 2)],
        "persuasive":        [("diplomacy", 2), ("intimidate", 2)],
        "deceitful":         [("bluff", 2), ("disguise", 2)],
        "deft_hands":        [("disable_device", 2), ("sleight_of_hand", 2)],
        "magical_aptitude":  [("spellcraft", 2), ("use_magic_device", 2)],
        "self_sufficient":   [("heal", 2), ("survival", 2)],
        "animal_affinity":   [("handle_animal", 2), ("ride", 2)],
        "acrobatic":         [("acrobatics", 2), ("fly", 2)],
    }
    if feat_id in skill_pairs:
        return [mod(v, "untyped", f"skill:{s}", src) for s, v in skill_pairs[feat_id]]

    # ── Skill Focus (+3 to chosen skill, +6 at 10 ranks; v1 ignores rank scaling). ─
    if feat_id.startswith("skill_focus_"):
        skill_id = feat_id[len("skill_focus_"):]
        return [mod(3, "untyped", f"skill:{skill_id}", src)]
    if feat_id == "skill_focus":
        # Generic — patron didn't pick a skill. No-op.
        return []

    # ── Weapon Focus (+1 attack with chosen weapon). ────────────────
    if feat_id.startswith("weapon_focus_"):
        weapon_id = feat_id[len("weapon_focus_"):]
        return [mod(1, "untyped", f"attack:weapon:{weapon_id}", src)]
    if feat_id == "weapon_focus":
        # Generic Weapon Focus picks the equipped weapon if any.
        weapon = getattr(character, "equipped_weapon", None)
        if weapon:
            return [mod(1, "untyped", f"attack:weapon:{weapon}", src)]
        return []

    # ── Spell Focus (+1 to save DC of chosen school). ───────────────
    if feat_id.startswith("spell_focus_"):
        school = feat_id[len("spell_focus_"):]
        return [mod(1, "untyped", f"spell_dc:{school}", src)]
    if feat_id == "spell_focus":
        return []

    # ── Spell Penetration (+2 caster level checks vs SR). ───────────
    if feat_id == "spell_penetration":
        return [mod(2, "untyped", "spell_resistance_check", src)]

    # ── Point-Blank Shot (+1 attack and damage with ranged within 30 ft). ─
    # We model as a flat +1 to ranged attack/damage; range qualifier
    # isn't enforced in v1 (most ranged shots are at <30 ft anyway).
    if feat_id == "point_blank_shot":
        return [
            mod(1, "untyped", "attack:ranged", src),
            mod(1, "untyped", "damage:ranged", src),
        ]

    # Greater Weapon Focus: +1 attack stacking with Weapon Focus.
    if feat_id.startswith("greater_weapon_focus_"):
        weapon_id = feat_id[len("greater_weapon_focus_"):]
        return [mod(1, "untyped", f"attack:weapon:{weapon_id}", src)]
    # Weapon Specialization: +2 damage with chosen weapon.
    if feat_id.startswith("weapon_specialization_"):
        weapon_id = feat_id[len("weapon_specialization_"):]
        return [mod(2, "untyped", f"damage:weapon:{weapon_id}", src)]
    # Greater Weapon Specialization: +2 damage stacking.
    if feat_id.startswith("greater_weapon_specialization_"):
        weapon_id = feat_id[len("greater_weapon_specialization_"):]
        return [mod(2, "untyped", f"damage:weapon:{weapon_id}", src)]

    # Greater Spell Focus: +1 DC stacking with Spell Focus.
    if feat_id.startswith("greater_spell_focus_"):
        school = feat_id[len("greater_spell_focus_"):]
        return [mod(1, "untyped", f"spell_dc:{school}", src)]

    # Greater Spell Penetration: +2 stacking with Spell Penetration.
    if feat_id == "greater_spell_penetration":
        return [mod(2, "untyped", "spell_resistance_check", src)]

    # Active / situational / not-yet-wired feats produce no modifiers.
    return []
