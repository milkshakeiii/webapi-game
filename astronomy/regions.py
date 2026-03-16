"""Solar system regions with distinct physical backgrounds."""

from dataclasses import dataclass


@dataclass
class Region:
    id: str
    name: str
    description: str
    ir_background: float       # infrared clutter (higher = harder to spot radiators)
    radio_noise: float         # ambient radio interference (mJy baseline)
    dust_opacity: float        # optical attenuation (0=clear, 1=opaque)
    solar_flux: float          # passive heating pressure (higher = more glint/heat)
    relay_coverage: float      # uplink quality (0-1, higher = cheaper uplinks)
    typical_range_scale: float  # AU, typical distance between contacts
    center_au: dict            # {x, y, z} center position in AU
    radius_au: float           # region extent


REGIONS = [
    Region(
        id="dust-veil",
        name="Dust Veil",
        description=(
            "Dense dust clouds and debris from a shattered moonlet. "
            "High infrared background hides radiator output but degrades fine imaging."
        ),
        ir_background=0.8,
        radio_noise=15.0,
        dust_opacity=0.6,
        solar_flux=0.3,
        relay_coverage=0.2,
        typical_range_scale=0.002,
        center_au={"x": 0.0, "y": 0.0, "z": 0.0},
        radius_au=0.01,
    ),
    Region(
        id="relay-spine",
        name="Relay Spine",
        description=(
            "A corridor of navigation beacons and comm relays. "
            "Excellent uplink coverage but full of listeners."
        ),
        ir_background=0.2,
        radio_noise=40.0,
        dust_opacity=0.1,
        solar_flux=0.5,
        relay_coverage=0.9,
        typical_range_scale=0.003,
        center_au={"x": 0.02, "y": 0.0, "z": 0.0},
        radius_au=0.015,
    ),
    Region(
        id="quiet-dark",
        name="Quiet Dark",
        description=(
            "Open space far from clutter. Superb passive observing "
            "but any emission stands out sharply."
        ),
        ir_background=0.05,
        radio_noise=5.0,
        dust_opacity=0.02,
        solar_flux=0.15,
        relay_coverage=0.4,
        typical_range_scale=0.005,
        center_au={"x": -0.02, "y": 0.015, "z": 0.005},
        radius_au=0.02,
    ),
    Region(
        id="broken-array",
        name="Broken Array",
        description=(
            "Wreckage of an old antenna farm. Cluttered radio reflections, "
            "debris shadows, and strong opportunities for ambushes."
        ),
        ir_background=0.4,
        radio_noise=60.0,
        dust_opacity=0.3,
        solar_flux=0.4,
        relay_coverage=0.3,
        typical_range_scale=0.001,
        center_au={"x": 0.01, "y": -0.02, "z": -0.003},
        radius_au=0.008,
    ),
]

REGION_MAP = {r.id: r for r in REGIONS}


def region_for_position(pos: dict) -> Region | None:
    """Find which region a position falls inside, or None if in open space."""
    from .physics import vec3_distance
    best = None
    best_dist = float("inf")
    for region in REGIONS:
        d = vec3_distance(pos, region.center_au)
        if d <= region.radius_au and d < best_dist:
            best = region
            best_dist = d
    return best


def default_spawn_region() -> Region:
    return REGION_MAP["quiet-dark"]
