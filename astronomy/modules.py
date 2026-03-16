"""Passive and active module definitions."""

from dataclasses import dataclass


@dataclass
class ModuleDef:
    id: str
    name: str
    slot_type: str  # "passive" or "active"
    description: str
    effects: dict   # key → value modifiers


# ---------------------------------------------------------------------------
# Passive modules (reshape behavior without constant input)
# ---------------------------------------------------------------------------

PASSIVE_MODULES = {
    "cold_baffles": ModuleDef(
        id="cold_baffles",
        name="Cold Baffles",
        slot_type="passive",
        description="Reduce aperture glint and stray light, but trap more heat.",
        effects={
            "optical_glint_multiplier": 0.4,
            "heat_rejection_multiplier": 0.7,
        },
    ),
    "signal_scrubber": ModuleDef(
        id="signal_scrubber",
        name="Signal Scrubber",
        slot_type="passive",
        description="Reduce radio leakage and sidebands, but draw extra power.",
        effects={
            "radio_leakage_multiplier": 0.3,
            "power_draw_multiplier": 1.3,
        },
    ),
    "phase_change_sink": ModuleDef(
        id="phase_change_sink",
        name="Phase-Change Sink",
        slot_type="passive",
        description="Store more heat before radiating, but forces long cooldown once full.",
        effects={
            "heat_capacity_multiplier": 2.5,
            "forced_vent_threshold": 0.9,  # fraction of capacity
        },
    ),
    "expanded_cache": ModuleDef(
        id="expanded_cache",
        name="Expanded Cache",
        slot_type="passive",
        description="Hold more unbanked data, but lose more if disrupted.",
        effects={
            "cache_capacity_multiplier": 2.0,
            "disruption_loss_multiplier": 1.5,
        },
    ),
    "ghost_drive": ModuleDef(
        id="ghost_drive",
        name="Ghost Drive",
        slot_type="passive",
        description="Reduce jump-charge signature and arrival bloom, but increase charge time.",
        effects={
            "jump_signature_multiplier": 0.5,
            "jump_bloom_multiplier": 0.4,
            "jump_charge_time_multiplier": 1.4,
        },
    ),
}


# ---------------------------------------------------------------------------
# Active modules (powerful but create loud signatures)
# ---------------------------------------------------------------------------

ACTIVE_MODULES = {
    "deep_field_overclock": ModuleDef(
        id="deep_field_overclock",
        name="Deep-Field Overclock",
        slot_type="active",
        description="Better sensitivity for one observation. Big power draw and heat.",
        effects={
            "snr_bonus": 0.5,
            "power_spike": 4.0,
            "heat_spike": 0.15,
            "timing_leakage_spike": 3.0,
        },
    ),
    "wideband_ping": ModuleDef(
        id="wideband_ping",
        name="Wideband Ping",
        slot_type="active",
        description="Instant weak contacts across the region. Obvious radio flash.",
        effects={
            "ping_radius_au": 0.01,
            "ping_snr": 3.0,
            "radio_flash": 500.0,
            "heat_spike": 0.05,
        },
    ),
    "directional_jammer": ModuleDef(
        id="directional_jammer",
        name="Directional Jammer",
        slot_type="active",
        description="Degrades target's radio astrometry and uplink quality.",
        effects={
            "jammer_output": 200.0,
            "jammer_radio_emission": 300.0,
            "heat_spike": 0.08,
        },
    ),
    "target_illuminator": ModuleDef(
        id="target_illuminator",
        name="Target Illuminator",
        slot_type="active",
        description="Wider spectrograph lock or higher acquisition chance.",
        effects={
            "spectrograph_fov_multiplier": 3.0,
            "optical_emission": 5.0,
            "heat_spike": 0.04,
        },
    ),
    "burst_uplink": ModuleDef(
        id="burst_uplink",
        name="Burst Uplink",
        slot_type="active",
        description="Bank data immediately from unsafe space. Detectable radio beam.",
        effects={
            "instant_bank": True,
            "radio_beam": 400.0,
            "heat_spike": 0.06,
        },
    ),
    "decoy_beacon": ModuleDef(
        id="decoy_beacon",
        name="Decoy Beacon",
        slot_type="active",
        description="Creates a false heated or transmitting source.",
        effects={
            "decoy_duration_sec": 120,
            "decoy_ir": 0.3,
            "decoy_radio": 50.0,
        },
    ),
}

ALL_MODULES = {**PASSIVE_MODULES, **ACTIVE_MODULES}


# ---------------------------------------------------------------------------
# Loadout
# ---------------------------------------------------------------------------

MAX_PASSIVE_SLOTS = 2
MAX_ACTIVE_SLOTS_BASE = 1
MAX_ACTIVE_SLOTS_UPGRADED = 2


def validate_loadout(passive_ids: list[str], active_ids: list[str],
                     max_active: int = MAX_ACTIVE_SLOTS_BASE) -> list[str]:
    """Validate a loadout configuration. Returns list of errors."""
    errors = []
    if len(passive_ids) > MAX_PASSIVE_SLOTS:
        errors.append(f"too many passive modules (max {MAX_PASSIVE_SLOTS})")
    if len(active_ids) > max_active:
        errors.append(f"too many active modules (max {max_active})")
    for pid in passive_ids:
        if pid not in PASSIVE_MODULES:
            errors.append(f"unknown passive module: {pid}")
    for aid in active_ids:
        if aid not in ACTIVE_MODULES:
            errors.append(f"unknown active module: {aid}")
    if len(set(passive_ids)) != len(passive_ids):
        errors.append("duplicate passive modules")
    if len(set(active_ids)) != len(active_ids):
        errors.append("duplicate active modules")
    return errors


def get_passive_effect(passive_ids: list[str], effect_key: str,
                       default: float = 1.0) -> float:
    """Get the combined effect of all passive modules for a given key.

    Multiplicative combination for multipliers.
    """
    result = default
    for pid in passive_ids:
        mod = PASSIVE_MODULES.get(pid)
        if mod and effect_key in mod.effects:
            result *= mod.effects[effect_key]
    return result
