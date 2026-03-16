"""Sky model: solar system sources, player craft, and shared state."""

import math
import random
import time
from dataclasses import dataclass, field

from .physics import (
    vec3_distance, position_to_apparent, light_time_sec,
    tick_heat, BASE_POWER_DRAW,
)
from .regions import region_for_position, default_spawn_region


# ---------------------------------------------------------------------------
# Motion classes
# ---------------------------------------------------------------------------

class OrbitalMotion:
    """Circular orbit for catalogue bodies."""

    def __init__(self, radius_au: float, phase_deg: float, period_sec: float,
                 inclination_deg: float = 0.0, center: dict = None):
        self.radius_au = radius_au
        self.phase_rad = math.radians(phase_deg)
        self.period_sec = max(1.0, period_sec)
        self.inclination_rad = math.radians(inclination_deg)
        self.center = center or {"x": 0.0, "y": 0.0, "z": 0.0}

    def position_at(self, t: float) -> dict:
        angle = self.phase_rad + 2 * math.pi * t / self.period_sec
        cos_i = math.cos(self.inclination_rad)
        sin_i = math.sin(self.inclination_rad)
        x = self.center["x"] + self.radius_au * math.cos(angle)
        y = self.center["y"] + self.radius_au * math.sin(angle) * cos_i
        z = self.center["z"] + self.radius_au * math.sin(angle) * sin_i
        return {"x": x, "y": y, "z": z}


class StaticPosition:
    """Fixed position (relays, derelicts, background sources)."""

    def __init__(self, position: dict):
        self.pos = dict(position)

    def position_at(self, t: float) -> dict:
        return dict(self.pos)


class TransientEvent:
    """Temporary source that decays over time."""

    def __init__(self, position: dict, spawn_time: float,
                 lifetime_sec: float, peak_brightness: float):
        self.pos = dict(position)
        self.spawn_time = spawn_time
        self.lifetime_sec = lifetime_sec
        self.peak_brightness = peak_brightness

    def position_at(self, t: float) -> dict:
        return dict(self.pos)

    def brightness_at(self, t: float) -> float:
        age = t - self.spawn_time
        if age < 0 or age > self.lifetime_sec:
            return 30.0  # invisible
        decay = 1.0 - (age / self.lifetime_sec)
        return self.peak_brightness + 2.5 * math.log10(max(0.01, decay))

    def is_active(self, t: float) -> bool:
        age = t - self.spawn_time
        return 0 <= age <= self.lifetime_sec


# ---------------------------------------------------------------------------
# Sky objects
# ---------------------------------------------------------------------------

@dataclass
class SkyObject:
    id: str
    name: str
    kind: str                  # star, nebula, pulsar, galaxy, anomaly,
                               # asteroid, comet, relay, derelict, debris
    brightness: float          # apparent magnitude at 1 AU (lower = brighter)
    radio_flux: float          # mJy at 1 AU
    spectrum_class: str
    description: str = ""
    tags: list = field(default_factory=list)
    motion: object = None      # OrbitalMotion, StaticPosition, or TransientEvent
    hidden_state: dict = field(default_factory=dict)

    def position_at(self, t: float) -> dict:
        if self.motion is not None:
            return self.motion.position_at(t)
        return {"x": 0.0, "y": 0.0, "z": 0.0}


# ---------------------------------------------------------------------------
# Player source
# ---------------------------------------------------------------------------

@dataclass
class PlayerSource:
    """A player's craft as seen by other observers."""
    session_id: str
    position_au: dict = field(default_factory=lambda: {"x": 0.0, "y": 0.0, "z": 0.0})
    active: bool = True
    broadcast_power: float = 0.0       # sustained deliberate transmit (via /transmit)
    # Transient radio burst (from uplink actions)
    radio_burst_power: float = 0.0
    radio_burst_until: float = 0.0
    # Physical state
    power_draw: float = BASE_POWER_DRAW
    stored_heat: float = 0.0
    heat_sink_capacity: float = 1.0
    radiator_mode: str = "balanced"
    radio_emissions: float = 5.0     # deliberate + leakage (mJy at source)
    optical_glint: float = 0.1       # baseline aperture glint
    # Jump state
    jump_charge_emission: float = 0.0
    arrival_bloom: float = 0.0
    arrival_bloom_until: float = 0.0
    # Timing
    last_tick: float = 0.0

    @property
    def effective_radio_power(self) -> float:
        """Total deliberate radio output: sustained broadcast + active burst."""
        return self.broadcast_power + self.radio_burst_power


# ---------------------------------------------------------------------------
# Catalogue
# ---------------------------------------------------------------------------

CATALOGUE = [
    # --- Stars and nebulae (distant background, high brightness) ---
    SkyObject("ngf-1", "Lyrion Nebula", "nebula",
              brightness=8.2, radio_flux=120.0, spectrum_class="emission",
              description="A sprawling emission nebula threaded with ionised hydrogen filaments.",
              tags=["extended", "h_alpha"],
              motion=StaticPosition({"x": -0.005, "y": 0.008, "z": 0.001})),
    SkyObject("ngf-2", "Kael's Star", "star",
              brightness=4.1, radio_flux=0.5, spectrum_class="G",
              description="A G-type main-sequence star at the heart of the Lyrion Nebula.",
              motion=StaticPosition({"x": -0.004, "y": 0.009, "z": 0.001})),
    SkyObject("ngf-3", "Vorantis Pulsar", "pulsar",
              brightness=22.0, radio_flux=850.0, spectrum_class="synchrotron",
              description="A millisecond pulsar emitting powerful radio jets.",
              tags=["periodic", "radio_loud"],
              motion=StaticPosition({"x": 0.015, "y": -0.012, "z": -0.008})),
    SkyObject("ngf-4", "The Cinderfield", "nebula",
              brightness=11.5, radio_flux=45.0, spectrum_class="emission",
              description="A supernova remnant glowing in soft X-ray and radio.",
              tags=["extended", "remnant"],
              motion=StaticPosition({"x": -0.018, "y": -0.003, "z": 0.002})),
    SkyObject("ngf-5", "Duskwell Galaxy", "galaxy",
              brightness=13.0, radio_flux=200.0, spectrum_class="composite",
              description="A barred spiral galaxy with an active nucleus.",
              tags=["extended", "agn"],
              motion=StaticPosition({"x": 0.025, "y": -0.015, "z": -0.005})),
    SkyObject("ngf-6", "Whisper Point", "anomaly",
              brightness=25.0, radio_flux=1200.0, spectrum_class="unknown",
              description="An unresolved radio source with no optical counterpart.",
              tags=["radio_loud", "unidentified"],
              motion=StaticPosition({"x": 0.003, "y": 0.012, "z": 0.010})),
    SkyObject("ngf-7", "Ember Twin A", "star",
              brightness=6.5, radio_flux=2.0, spectrum_class="B",
              description="A hot blue star in a binary system.",
              motion=StaticPosition({"x": -0.020, "y": -0.010, "z": -0.005})),
    SkyObject("ngf-8", "Ember Twin B", "star",
              brightness=7.8, radio_flux=1.5, spectrum_class="B",
              description="The fainter companion of the Ember Twin system.",
              motion=StaticPosition({"x": -0.020, "y": -0.0101, "z": -0.005})),
    SkyObject("ngf-9", "The Quiet Arch", "nebula",
              brightness=14.0, radio_flux=10.0, spectrum_class="reflection",
              description="A faint reflection nebula, visible only in long exposures.",
              tags=["extended", "faint"],
              motion=StaticPosition({"x": 0.005, "y": 0.020, "z": 0.015})),
    SkyObject("ngf-10", "Thorngate Cluster", "star",
              brightness=9.0, radio_flux=5.0, spectrum_class="mixed",
              description="A loose open cluster of ~40 stars.",
              tags=["cluster"],
              motion=StaticPosition({"x": 0.010, "y": 0.008, "z": 0.004})),
    SkyObject("ngf-11", "Pale Drift", "galaxy",
              brightness=16.0, radio_flux=80.0, spectrum_class="elliptical",
              description="A distant elliptical galaxy with a fading radio halo.",
              tags=["extended"],
              motion=StaticPosition({"x": -0.012, "y": -0.025, "z": -0.020})),

    # --- Orbiting bodies (monitoring targets) ---
    SkyObject("ast-101", "Greystone", "asteroid",
              brightness=16.0, radio_flux=0.0, spectrum_class="silicate",
              description="A large silicate asteroid with a slow tumble.",
              tags=["rocky"],
              motion=OrbitalMotion(0.008, 30, 7200, inclination_deg=5),
              hidden_state={"spin_period_sec": 14310, "albedo": 0.15,
                            "thermal_inertia": 0.3}),
    SkyObject("ast-102", "Cinderblock", "asteroid",
              brightness=17.5, radio_flux=0.0, spectrum_class="carbonaceous",
              description="A dark carbonaceous body shedding dust.",
              tags=["dark", "dusty"],
              motion=OrbitalMotion(0.006, 120, 5400, inclination_deg=12),
              hidden_state={"spin_period_sec": 28800, "albedo": 0.04,
                            "thermal_inertia": 0.6}),
    SkyObject("com-201", "Frostplume", "comet",
              brightness=14.0, radio_flux=2.0, spectrum_class="volatile",
              description="An active comet with visible coma and dust jets.",
              tags=["outgassing", "volatile"],
              motion=OrbitalMotion(0.012, 200, 14400, inclination_deg=20),
              hidden_state={"outgassing_rate": 0.7, "plume_angle_deg": 45}),

    # --- Relays and derelicts ---
    SkyObject("rly-301", "Meridian Beacon", "relay",
              brightness=20.0, radio_flux=600.0, spectrum_class="synchrotron",
              description="A navigation relay near the field center.",
              tags=["periodic", "radio_loud", "relay"],
              motion=StaticPosition({"x": 0.001, "y": 0.0, "z": 0.0}),
              hidden_state={"power_cycle_sec": 120, "sideband_pattern": "regular"}),
    SkyObject("drk-401", "Wraith Hulk", "derelict",
              brightness=21.0, radio_flux=15.0, spectrum_class="metallic",
              description="A drifting derelict with intermittent power spikes.",
              tags=["metallic", "intermittent"],
              motion=OrbitalMotion(0.016, 280, 20000, inclination_deg=8),
              hidden_state={"power_cycle_sec": 900, "attitude_period_sec": 3600}),

    # --- Debris / dust features ---
    SkyObject("deb-501", "Shardfield", "debris",
              brightness=19.0, radio_flux=8.0, spectrum_class="metallic",
              description="A dense cluster of metallic debris with radio reflections.",
              tags=["debris", "metallic"],
              motion=OrbitalMotion(0.010, 150, 10000, inclination_deg=3),
              hidden_state={"density_peak_offset_deg": 0.3,
                            "heating_curve": "slow_rise"}),
]


# ---------------------------------------------------------------------------
# Beacons (for uplink light-time computation)
# ---------------------------------------------------------------------------

BEACONS = [
    {"id": "beacon-alpha", "position_au": {"x": 0.001, "y": 0.0, "z": 0.0}},
    {"id": "beacon-beta", "position_au": {"x": 0.02, "y": 0.0, "z": 0.0}},
    {"id": "beacon-gamma", "position_au": {"x": -0.015, "y": 0.01, "z": 0.005}},
]


def nearest_beacon(pos: dict) -> dict:
    best = BEACONS[0]
    best_dist = vec3_distance(pos, best["position_au"])
    for b in BEACONS[1:]:
        d = vec3_distance(pos, b["position_au"])
        if d < best_dist:
            best = b
            best_dist = d
    return best


# ---------------------------------------------------------------------------
# Sky
# ---------------------------------------------------------------------------

class Sky:
    """Shared sky state containing catalogue objects and player sources."""

    TRANSIENT_TEMPLATES = [
        ("Radio Burst", "anomaly", 22.0, 400.0, "unknown",
         ["radio_loud", "transient"], 120),
        ("Thermal Bloom", "anomaly", 15.0, 5.0, "emission",
         ["transient", "thermal"], 300),
        ("Debris Flash", "debris", 17.0, 20.0, "metallic",
         ["transient", "metallic"], 60),
        ("Relay Ghost", "anomaly", 23.0, 150.0, "unknown",
         ["transient", "radio_loud"], 180),
    ]

    def __init__(self, seed=None):
        self.objects: list[SkyObject] = list(CATALOGUE)
        self.players: dict[str, PlayerSource] = {}
        self._rng = random.Random(seed)
        self._next_transient_check: float = 0.0
        self._transient_counter: int = 0

    # -- player management ---------------------------------------------------

    def add_player(self, session_id: str) -> PlayerSource:
        region = default_spawn_region()
        r = region.radius_au * 0.8
        x = region.center_au["x"] + self._rng.uniform(-r, r)
        y = region.center_au["y"] + self._rng.uniform(-r, r)
        z = region.center_au["z"] + self._rng.uniform(-r * 0.3, r * 0.3)
        pos = {"x": x, "y": y, "z": z}

        now = time.time()
        src = PlayerSource(session_id=session_id, position_au=pos, last_tick=now)
        self.players[session_id] = src
        return src

    def remove_player(self, session_id: str):
        self.players.pop(session_id, None)

    def boost_player_emission(self, session_id: str, power: float):
        p = self.players.get(session_id)
        if p:
            p.broadcast_power = power

    def tick_player(self, session_id: str, now: float = None,
                    heat_rejection_mult: float = 1.0):
        """Update a player's physical state to the current time."""
        p = self.players.get(session_id)
        if p is None:
            return
        if now is None:
            now = time.time()
        dt = now - p.last_tick
        if dt <= 0:
            return
        p.stored_heat, _ = tick_heat(p.stored_heat, p.power_draw,
                                     p.radiator_mode, dt, heat_rejection_mult)
        # Decay arrival bloom
        if p.arrival_bloom > 0 and now > p.arrival_bloom_until:
            p.arrival_bloom = 0.0
            p.jump_charge_emission = 0.0
        # Decay radio burst
        if p.radio_burst_power > 0 and now > p.radio_burst_until:
            p.radio_burst_power = 0.0
        p.last_tick = now

        # Spawn/cleanup transients periodically
        self._maybe_spawn_transient(now)

    def _maybe_spawn_transient(self, now: float):
        """Periodically spawn transient events and clean up expired ones."""
        if now < self._next_transient_check:
            return
        self._next_transient_check = now + 60  # check every 60s

        # Remove expired transients
        self.objects = [
            obj for obj in self.objects
            if obj.motion is None
            or not isinstance(obj.motion, TransientEvent)
            or obj.motion.is_active(now)
        ]

        # Spawn a new transient with ~20% chance per check
        if self._rng.random() < 0.2 and self.players:
            tmpl = self._rng.choice(self.TRANSIENT_TEMPLATES)
            name, kind, brightness, radio, spectrum, tags, lifetime = tmpl
            self._transient_counter += 1

            # Spawn near a random region center
            from .regions import REGIONS
            region = self._rng.choice(REGIONS)
            r = region.radius_au * 0.7
            pos = {
                "x": region.center_au["x"] + self._rng.uniform(-r, r),
                "y": region.center_au["y"] + self._rng.uniform(-r, r),
                "z": region.center_au["z"] + self._rng.uniform(-r * 0.3, r * 0.3),
            }

            obj = SkyObject(
                id=f"trn-{self._transient_counter:04d}",
                name=f"{name} #{self._transient_counter}",
                kind=kind,
                brightness=brightness,
                radio_flux=radio,
                spectrum_class=spectrum,
                description=f"Transient {kind} event in {region.name}.",
                tags=list(tags),
                motion=TransientEvent(pos, now, lifetime, brightness),
            )
            self.objects.append(obj)

    # -- query ---------------------------------------------------------------

    def sources_in_fov(self, observer_pos: dict, target_ra: float,
                       target_dec: float, fov_radius: float,
                       t: float = None):
        """Return catalogue objects within FOV from observer's perspective.

        Returns list of (object, apparent_ra, apparent_dec, distance_au, light_delay_sec).
        """
        if t is None:
            t = time.time()
        results = []
        for obj in self.objects:
            source_pos = obj.position_at(t)
            app_ra, app_dec, dist = position_to_apparent(observer_pos, source_pos)
            ang = _angular_distance(target_ra, target_dec, app_ra, app_dec)
            if ang <= fov_radius:
                delay = light_time_sec(dist)
                results.append((obj, app_ra, app_dec, dist, delay))
        return results

    def players_in_fov(self, observer_pos: dict, target_ra: float,
                       target_dec: float, fov_radius: float,
                       exclude_session: str = None):
        """Return players within FOV from observer's perspective.

        Returns list of (player, apparent_ra, apparent_dec, distance_au).
        """
        results = []
        for sid, p in self.players.items():
            if sid == exclude_session or not p.active:
                continue
            app_ra, app_dec, dist = position_to_apparent(observer_pos, p.position_au)
            ang = _angular_distance(target_ra, target_dec, app_ra, app_dec)
            if ang <= fov_radius:
                results.append((p, app_ra, app_dec, dist))
        return results


# ---------------------------------------------------------------------------
# Angular distance helper
# ---------------------------------------------------------------------------

def _angular_distance(ra1, dec1, ra2, dec2):
    """Great-circle distance in degrees between two sky positions."""
    ra1, dec1, ra2, dec2 = (math.radians(x) for x in (ra1, dec1, ra2, dec2))
    cos_d = (math.sin(dec1) * math.sin(dec2) +
             math.cos(dec1) * math.cos(dec2) * math.cos(ra1 - ra2))
    cos_d = max(-1.0, min(1.0, cos_d))
    return math.degrees(math.acos(cos_d))
