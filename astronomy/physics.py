"""Physical constants, heat model, and signature computation."""

import math

# ---------------------------------------------------------------------------
# Constants (from Appendix B)
# ---------------------------------------------------------------------------

LIGHT_TIME_SEC_PER_AU = 499.004784
SIGMA_PLAYER_POS_AU = 0.0002          # ~30,000 km
CHARGING_WINDOW_FACTOR = 1.25
RECALIBRATION_WINDOW_FACTOR = 1.10
SCIENCE_UPLINK_COOLDOWN_SEC = 30
HUNT_UPLINK_COOLDOWN_SEC = 90

# Jump constants
BASE_JUMP_CHARGE_SEC = 20
JUMP_CHARGE_SEC_PER_AU = 2400
MAX_CHARGED_HOLD_SEC = 30
BASE_JUMP_NAV_SIGMA_AU = 0.00002
ARRIVAL_BLOOM_SEC = 8

# Thermal constants
BASE_POWER_DRAW = 1.0                 # idle power draw
HEAT_CAPACITY = 1.0                   # stored_heat at which radiators must dump
HEAT_PER_POWER_PER_SEC = 0.002        # heat generated per unit power per second
OBSERVATION_HEAT_BASE = 0.02          # base heat from any observation
OBSERVATION_HEAT_PER_SEC = 0.0005     # heat per second of exposure
UPLINK_HEAT = 0.08                    # heat from an uplink action
UPLINK_POWER_SPIKE = 6.0              # temporary power during uplink

# Radiator mode rates (heat rejected per second)
RADIATOR_RATES = {
    "sealed": 0.0005,
    "balanced": 0.003,
    "venting": 0.012,
}

# Radiator IR signature multipliers
RADIATOR_IR_SIGNATURE = {
    "sealed": 0.2,
    "balanced": 1.0,
    "venting": 3.5,
}

# Scan profile multipliers
SCAN_PROFILES = {
    "low_power": {
        "snr_multiplier": 0.7,
        "power_multiplier": 0.5,
        "heat_multiplier": 0.4,
        "leakage_multiplier": 0.3,
    },
    "survey": {
        "snr_multiplier": 1.0,
        "power_multiplier": 1.0,
        "heat_multiplier": 1.0,
        "leakage_multiplier": 1.0,
    },
    "boosted": {
        "snr_multiplier": 1.4,
        "power_multiplier": 1.8,
        "heat_multiplier": 2.0,
        "leakage_multiplier": 1.5,
    },
    "overclocked": {
        "snr_multiplier": 1.8,
        "power_multiplier": 3.0,
        "heat_multiplier": 4.0,
        "leakage_multiplier": 3.0,
    },
}

# Charge profile multipliers
CHARGE_PROFILES = {
    "cold_spool": {
        "charge_multiplier": 1.8,
        "signature_multiplier": 0.7,
        "thermal_multiplier": 0.8,
        "nav_sigma_multiplier": 0.8,
    },
    "standard": {
        "charge_multiplier": 1.0,
        "signature_multiplier": 1.0,
        "thermal_multiplier": 1.0,
        "nav_sigma_multiplier": 1.0,
    },
    "emergency": {
        "charge_multiplier": 0.55,
        "signature_multiplier": 1.8,
        "thermal_multiplier": 1.5,
        "nav_sigma_multiplier": 1.8,
    },
}

# Reward constants
BASE_DETECTION_DATA = 5
BASE_CLASSIFICATION_DATA = 10
BASE_ANOMALY_DATA = 15
BASE_REACQUISITION_DATA = 3


# ---------------------------------------------------------------------------
# 3D helpers
# ---------------------------------------------------------------------------

def vec3_distance(a: dict, b: dict) -> float:
    """Euclidean distance between two {x, y, z} dicts in AU."""
    dx = a["x"] - b["x"]
    dy = a["y"] - b["y"]
    dz = a["z"] - b["z"]
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def vec3_add(a: dict, b: dict) -> dict:
    return {"x": a["x"] + b["x"], "y": a["y"] + b["y"], "z": a["z"] + b["z"]}


def vec3_scale(v: dict, s: float) -> dict:
    return {"x": v["x"] * s, "y": v["y"] * s, "z": v["z"] * s}


def light_time_sec(distance_au: float) -> float:
    return distance_au * LIGHT_TIME_SEC_PER_AU


# ---------------------------------------------------------------------------
# Position to apparent sky coordinates
# ---------------------------------------------------------------------------

def position_to_apparent(observer_pos: dict, source_pos: dict) -> tuple[float, float, float]:
    """Convert 3D positions to apparent RA/Dec and distance.

    Returns (ra_deg, dec_deg, distance_au).
    """
    dx = source_pos["x"] - observer_pos["x"]
    dy = source_pos["y"] - observer_pos["y"]
    dz = source_pos["z"] - observer_pos["z"]
    dist = math.sqrt(dx * dx + dy * dy + dz * dz)
    if dist < 1e-15:
        return 0.0, 0.0, 0.0
    # dec from z
    dec = math.degrees(math.asin(max(-1.0, min(1.0, dz / dist))))
    # ra from x, y
    ra = math.degrees(math.atan2(dy, dx)) % 360.0
    return ra, dec, dist


# ---------------------------------------------------------------------------
# Signature computation
# ---------------------------------------------------------------------------

def compute_signatures(power_draw: float, stored_heat: float,
                       radiator_mode: str, radio_emissions: float,
                       optical_glint: float, jump_charge_emission: float,
                       arrival_bloom: float) -> dict:
    """Compute the observable signature of a player craft.

    Returns a dict of band-specific brightness values.
    """
    rad_rate = RADIATOR_RATES.get(radiator_mode, RADIATOR_RATES["balanced"])
    ir_sig = RADIATOR_IR_SIGNATURE.get(radiator_mode, 1.0)

    # Infrared: driven by radiator output and stored heat pressure
    radiator_output = rad_rate * (1.0 + stored_heat * 2.0)
    ir_brightness = radiator_output * ir_sig * 50.0  # scale to magnitude-like

    # Radio: leakage + deliberate emissions + jump charge
    total_radio = radio_emissions + jump_charge_emission

    # Optical: glint + active illumination + arrival bloom
    total_optical = optical_glint + arrival_bloom

    # Power draw contribution to timing leakage (radio)
    timing_leakage = power_draw * 0.3
    total_radio += timing_leakage

    return {
        "ir_brightness": ir_brightness,
        "radio_flux": total_radio,
        "optical_brightness": total_optical,
        "radiator_output": radiator_output,
        "power_draw": power_draw,
    }


def inverse_square_flux(source_flux: float, distance_au: float) -> float:
    """Apply inverse-square falloff to a flux value."""
    if distance_au < 0.00001:
        distance_au = 0.00001
    return source_flux / (distance_au * distance_au)


def flux_to_magnitude(flux: float, zero_point: float = 20.0) -> float:
    """Convert a flux-like value to an apparent magnitude.

    Lower magnitude = brighter. zero_point is the magnitude at flux=1.0.
    """
    if flux <= 0:
        return 30.0  # effectively invisible
    return zero_point - 2.5 * math.log10(flux)


# ---------------------------------------------------------------------------
# Heat tick
# ---------------------------------------------------------------------------

def tick_heat(stored_heat: float, power_draw: float,
              radiator_mode: str, dt_sec: float,
              rejection_multiplier: float = 1.0) -> tuple[float, float]:
    """Advance heat state by dt_sec.

    Returns (new_stored_heat, heat_rejected_this_tick).
    rejection_multiplier: from passive modules (e.g. cold_baffles 0.7).
    """
    # Heat generated
    heat_in = power_draw * HEAT_PER_POWER_PER_SEC * dt_sec

    # Heat rejected
    rad_rate = RADIATOR_RATES.get(radiator_mode, RADIATOR_RATES["balanced"])
    heat_out = rad_rate * dt_sec * (1.0 + stored_heat) * rejection_multiplier

    new_heat = max(0.0, stored_heat + heat_in - heat_out)
    return new_heat, heat_out


def observation_heat(exposure_time: float, scan_profile: str = "survey") -> float:
    """Heat generated by an observation."""
    profile = SCAN_PROFILES.get(scan_profile, SCAN_PROFILES["survey"])
    return (OBSERVATION_HEAT_BASE + OBSERVATION_HEAT_PER_SEC * exposure_time) * profile["heat_multiplier"]


def observation_power(scan_profile: str = "survey") -> float:
    """Power draw during an observation."""
    profile = SCAN_PROFILES.get(scan_profile, SCAN_PROFILES["survey"])
    return BASE_POWER_DRAW * profile["power_multiplier"]


# ---------------------------------------------------------------------------
# Cold spool visibility curve
# ---------------------------------------------------------------------------

def cold_spool_visibility(progress: float) -> float:
    """Visibility factor for cold_spool charge profile.

    Starts ambiguous, becomes obvious late in charge.
    """
    return 0.35 + 0.65 * progress * progress


# ---------------------------------------------------------------------------
# Jump computation
# ---------------------------------------------------------------------------

def jump_charge_duration(distance_au: float, charge_profile: str) -> float:
    """How long a jump charge takes in seconds."""
    profile = CHARGE_PROFILES.get(charge_profile, CHARGE_PROFILES["standard"])
    base = BASE_JUMP_CHARGE_SEC + JUMP_CHARGE_SEC_PER_AU * distance_au
    return base * profile["charge_multiplier"]


def jump_charge_emission_power(distance_au: float, charge_profile: str) -> float:
    """Signature power emitted during jump charge."""
    profile = CHARGE_PROFILES.get(charge_profile, CHARGE_PROFILES["standard"])
    return (0.5 + 12 * distance_au) * profile["signature_multiplier"]


def jump_thermal_debt(distance_au: float, charge_profile: str) -> float:
    """Heat gained from a jump charge/commit/abort."""
    profile = CHARGE_PROFILES.get(charge_profile, CHARGE_PROFILES["standard"])
    return (0.15 + 4 * distance_au) * profile["thermal_multiplier"]


def jump_nav_sigma(charge_profile: str, jam_strength: float = 0.0) -> float:
    """Navigation uncertainty for jump arrival."""
    profile = CHARGE_PROFILES.get(charge_profile, CHARGE_PROFILES["standard"])
    return BASE_JUMP_NAV_SIGMA_AU * profile["nav_sigma_multiplier"] * (1 + jam_strength)


# ---------------------------------------------------------------------------
# Jamming
# ---------------------------------------------------------------------------

def jam_strength(jammer_output: float, distance_au: float) -> float:
    """Effective jam strength at a given distance."""
    d = max(distance_au, 0.00001)
    return jammer_output / (d * d)


def effective_radio_noise(base_noise: float, jam: float) -> float:
    """Radio noise floor with jamming applied."""
    return base_noise * (1 + jam)
