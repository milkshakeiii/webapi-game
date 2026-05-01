"""Size table for PF1 creatures.

Each size category produces a known set of mechanical effects (AC/attack
mod, CMB/CMD mod, stealth mod, grid footprint, natural reach, carry
capacity). All numeric effects are emitted as ``Modifier`` objects so
the engine treats them uniformly with every other modifier source.

Sizes:

::

    fine       -8/+8 CMB     1 sq footprint  shared with allies
    diminutive -4/+4 CMB     1 sq footprint  shared with allies
    tiny       -2/+2 CMB     1 sq footprint  shared with allies
    small      -1/+1 CMB     1 sq footprint  5 ft reach
    medium      0/0  CMB     1 sq footprint  5 ft reach
    large      +1/-1 CMB     2 sq footprint  10 ft reach (tall) / 5 ft (long)
    huge       +2/-2 CMB     3 sq footprint  15 ft (tall) / 10 ft (long)
    gargantuan +4/-4 CMB     4 sq footprint  20 ft (tall) / 15 ft (long)
    colossal   +8/-8 CMB     6 sq footprint  30 ft (tall) / 20 ft (long)
"""

from __future__ import annotations

from dataclasses import dataclass

from .modifiers import Modifier, mod


SIZE_NAMES = (
    "fine", "diminutive", "tiny", "small", "medium",
    "large", "huge", "gargantuan", "colossal",
)


@dataclass(frozen=True)
class SizeData:
    """All mechanical effects of being a particular size category."""

    name: str
    rank: int                # ordinal: fine=-4 .. medium=0 .. colossal=+4
    ac_attack_mod: int       # +1 small / -1 large / etc. (size mod to AC and attack)
    cmb_cmd_mod: int         # opposite sign of ac_attack_mod
    stealth_mod: int         # special size modifier to Stealth
    footprint_squares: int   # width = height in squares (1 for med-and-smaller)
    natural_reach_ft_long: int   # natural reach for "long" creatures
    natural_reach_ft_tall: int   # natural reach for "tall" creatures
    space_ft: int                # space the creature occupies, in feet
    carry_multiplier: float      # carrying-capacity multiplier vs medium

    @property
    def reach_squares_long(self) -> int:
        return self.natural_reach_ft_long // 5

    @property
    def reach_squares_tall(self) -> int:
        return self.natural_reach_ft_tall // 5


SIZE_TABLE: dict[str, SizeData] = {
    "fine":       SizeData("fine",       -4, +8, -8, +16, 1, 0, 0, 0, 1/8),
    "diminutive": SizeData("diminutive", -3, +4, -4, +12, 1, 0, 0, 0, 1/4),
    "tiny":       SizeData("tiny",       -2, +2, -2,  +8, 1, 0, 0, 0, 1/2),
    "small":      SizeData("small",      -1, +1, -1,  +4, 1, 5, 5, 5, 0.75),
    "medium":     SizeData("medium",      0,  0,  0,   0, 1, 5, 5, 5, 1.0),
    "large":      SizeData("large",      +1, -1, +1,  -4, 2, 5, 10, 10, 2.0),
    "huge":       SizeData("huge",       +2, -2, +2,  -8, 3, 10, 15, 15, 4.0),
    "gargantuan": SizeData("gargantuan", +3, -4, +4, -12, 4, 15, 20, 20, 8.0),
    "colossal":   SizeData("colossal",   +4, -8, +8, -16, 6, 20, 30, 30, 16.0),
}


def get_size(name: str) -> SizeData:
    """Return the SizeData for a size name. Raises KeyError if unknown."""
    if name not in SIZE_TABLE:
        raise KeyError(f"unknown size: {name!r}; known: {sorted(SIZE_TABLE)}")
    return SIZE_TABLE[name]


def size_modifiers(size_name: str) -> list[Modifier]:
    """Return all stat modifiers applied by being the given size.

    Always tagged with type ``"size"`` so they don't stack with each
    other and they net properly with explicit size-changing magic.
    """
    sd = get_size(size_name)
    source = f"size:{size_name}"
    out: list[Modifier] = []
    if sd.ac_attack_mod != 0:
        out.append(mod(sd.ac_attack_mod, "size", "ac", source))
        out.append(mod(sd.ac_attack_mod, "size", "attack", source))
    if sd.cmb_cmd_mod != 0:
        out.append(mod(sd.cmb_cmd_mod, "size", "cmb", source))
        out.append(mod(sd.cmb_cmd_mod, "size", "cmd", source))
    if sd.stealth_mod != 0:
        out.append(mod(sd.stealth_mod, "size", "skill:stealth", source))
    return out
