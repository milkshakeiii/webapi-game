"""Race → modifier list.

PF1 racial traits with passive modifier-shaped effects. Situational
bonuses (e.g., dwarf hatred vs orcs, gnome bonus vs reptilian) are
not modeled here — they need contextual qualifiers we don't have yet.
"""

from __future__ import annotations

from .content import Race
from .modifiers import Modifier, mod


def racial_modifiers(race: Race) -> list[Modifier]:
    """Return passive racial trait modifiers for ``race``.

    Covers: Halfling Luck (+1 racial all saves), Sure-Footed
    (+2 acrobatics/climb), Keen Senses (+2 perception across the races
    that have it), Half-Orc Intimidating (+2 intimidate). Situational
    or conditional traits (e.g., dwarven hardy vs poison) are not here.
    """
    out: list[Modifier] = []
    rid = race.id
    src_prefix = f"racial:{rid}"

    if rid == "halfling":
        for save in ("fort_save", "ref_save", "will_save"):
            out.append(mod(1, "racial", save, f"{src_prefix}:halfling_luck"))
        out.append(mod(2, "racial", "skill:acrobatics", f"{src_prefix}:sure_footed"))
        out.append(mod(2, "racial", "skill:climb", f"{src_prefix}:sure_footed"))
        out.append(mod(2, "racial", "skill:perception", f"{src_prefix}:keen_senses"))

    elif rid == "elf":
        out.append(mod(2, "racial", "skill:perception", f"{src_prefix}:keen_senses"))
        # Elven Magic: +2 caster level checks vs SR; +2 Spellcraft to
        # identify magic items.
        out.append(mod(2, "racial", "spell_resistance_check", f"{src_prefix}:elven_magic"))
        out.append(mod(2, "racial", "skill:spellcraft", f"{src_prefix}:elven_magic"))

    elif rid == "gnome":
        out.append(mod(2, "racial", "skill:perception", f"{src_prefix}:keen_senses"))
        # Illusion Resistance: +2 vs illusion saves — situational, skip.

    elif rid == "half_elf":
        out.append(mod(2, "racial", "skill:perception", f"{src_prefix}:keen_senses"))

    elif rid == "half_orc":
        out.append(mod(2, "racial", "skill:intimidate", f"{src_prefix}:intimidating"))

    elif rid == "dwarf":
        # Stonecunning: +2 Perception for stonework only — situational.
        # Hardy: +2 saves vs poison/spells/SLAs — situational.
        # Stability: +4 CMD vs trip/bull rush — situational.
        # Hatred: +1 attack vs orcs/goblinoids — situational.
        # Defensive Training: +4 dodge AC vs giants — situational.
        # All conditional; not wired in v1.
        pass

    elif rid == "human":
        # No passive modifier-shaped traits — bonus feat and bonus skill
        # rank are already factored at character creation.
        pass

    return out
