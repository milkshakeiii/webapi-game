"""Sky model: fictional objects and player positions in a shared sky."""

import math
import random
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Coordinate helpers
# ---------------------------------------------------------------------------

def angular_distance(ra1, dec1, ra2, dec2):
    """Great-circle distance in degrees between two sky positions."""
    ra1, dec1, ra2, dec2 = (math.radians(x) for x in (ra1, dec1, ra2, dec2))
    cos_d = (math.sin(dec1) * math.sin(dec2) +
             math.cos(dec1) * math.cos(dec2) * math.cos(ra1 - ra2))
    cos_d = max(-1.0, min(1.0, cos_d))
    return math.degrees(math.acos(cos_d))


# ---------------------------------------------------------------------------
# Sky objects
# ---------------------------------------------------------------------------

@dataclass
class SkyObject:
    id: str
    name: str
    kind: str                  # star, nebula, pulsar, galaxy, anomaly
    ra: float                  # 0-360
    dec: float                 # -90 to +90
    brightness: float          # apparent magnitude (lower = brighter)
    radio_flux: float          # mJy, radio emission strength
    spectrum_class: str        # e.g. "O", "B", "G", "emission", "synchrotron"
    description: str = ""
    tags: list = field(default_factory=list)


@dataclass
class PlayerSource:
    """A player's telescope as seen by other observers."""
    session_id: str
    ra: float
    dec: float
    radio_flux: float = 5.0        # baseline radio leakage
    optical_brightness: float = 18.0   # faint by default
    active: bool = True
    broadcast_power: float = 0.0   # extra signal if transmitting


# ---------------------------------------------------------------------------
# Catalogue of fictional objects
# ---------------------------------------------------------------------------

CATALOGUE = [
    SkyObject("ngf-1", "Lyrion Nebula", "nebula",
              ra=42.5, dec=15.3, brightness=8.2, radio_flux=120.0,
              spectrum_class="emission",
              description="A sprawling emission nebula threaded with ionised hydrogen filaments.",
              tags=["extended", "h_alpha"]),
    SkyObject("ngf-2", "Kael's Star", "star",
              ra=42.8, dec=15.1, brightness=4.1, radio_flux=0.5,
              spectrum_class="G",
              description="A G-type main-sequence star at the heart of the Lyrion Nebula."),
    SkyObject("ngf-3", "Vorantis Pulsar", "pulsar",
              ra=128.7, dec=-44.2, brightness=22.0, radio_flux=850.0,
              spectrum_class="synchrotron",
              description="A millisecond pulsar emitting powerful radio jets.",
              tags=["periodic", "radio_loud"]),
    SkyObject("ngf-4", "The Cinderfield", "nebula",
              ra=200.1, dec=5.8, brightness=11.5, radio_flux=45.0,
              spectrum_class="emission",
              description="A supernova remnant glowing in soft X-ray and radio.",
              tags=["extended", "remnant"]),
    SkyObject("ngf-5", "Duskwell Galaxy", "galaxy",
              ra=310.0, dec=-12.4, brightness=13.0, radio_flux=200.0,
              spectrum_class="composite",
              description="A barred spiral galaxy with an active nucleus.",
              tags=["extended", "agn"]),
    SkyObject("ngf-6", "Whisper Point", "anomaly",
              ra=77.3, dec=62.1, brightness=25.0, radio_flux=1200.0,
              spectrum_class="unknown",
              description="An unresolved radio source with no optical counterpart.",
              tags=["radio_loud", "unidentified"]),
    SkyObject("ngf-7", "Ember Twin A", "star",
              ra=180.0, dec=-30.0, brightness=6.5, radio_flux=2.0,
              spectrum_class="B",
              description="A hot blue star in a binary system."),
    SkyObject("ngf-8", "Ember Twin B", "star",
              ra=180.1, dec=-30.05, brightness=7.8, radio_flux=1.5,
              spectrum_class="B",
              description="The fainter companion of the Ember Twin system."),
    SkyObject("ngf-9", "The Quiet Arch", "nebula",
              ra=350.0, dec=45.0, brightness=14.0, radio_flux=10.0,
              spectrum_class="reflection",
              description="A faint reflection nebula, visible only in long exposures.",
              tags=["extended", "faint"]),
    SkyObject("ngf-10", "Meridian Beacon", "pulsar",
              ra=0.5, dec=0.2, brightness=20.0, radio_flux=600.0,
              spectrum_class="synchrotron",
              description="A slow pulsar near the celestial equator.",
              tags=["periodic", "radio_loud"]),
    SkyObject("ngf-11", "Thorngate Cluster", "star",
              ra=95.0, dec=22.0, brightness=9.0, radio_flux=5.0,
              spectrum_class="mixed",
              description="A loose open cluster of ~40 stars.",
              tags=["cluster"]),
    SkyObject("ngf-12", "Pale Drift", "galaxy",
              ra=265.0, dec=-55.0, brightness=16.0, radio_flux=80.0,
              spectrum_class="elliptical",
              description="A distant elliptical galaxy with a fading radio halo.",
              tags=["extended"]),
]


class Sky:
    """Shared sky state containing catalogue objects and player sources."""

    def __init__(self, seed=None):
        self.objects: list[SkyObject] = list(CATALOGUE)
        self.players: dict[str, PlayerSource] = {}
        self._rng = random.Random(seed)

    # -- player management ---------------------------------------------------

    def add_player(self, session_id: str) -> PlayerSource:
        ra = self._rng.uniform(0, 360)
        dec = self._rng.uniform(-70, 70)
        src = PlayerSource(session_id=session_id, ra=ra, dec=dec)
        self.players[session_id] = src
        return src

    def remove_player(self, session_id: str):
        self.players.pop(session_id, None)

    def boost_player_emission(self, session_id: str, power: float):
        """When a player transmits, increase their detectability."""
        p = self.players.get(session_id)
        if p:
            p.broadcast_power = power

    # -- query ---------------------------------------------------------------

    def objects_in_fov(self, ra: float, dec: float, radius: float):
        """Return catalogue objects within radius degrees of (ra, dec)."""
        return [obj for obj in self.objects
                if angular_distance(ra, dec, obj.ra, obj.dec) <= radius]

    def players_in_fov(self, ra: float, dec: float, radius: float,
                       exclude_session: str = None):
        """Return player sources within radius, excluding self."""
        results = []
        for sid, p in self.players.items():
            if sid == exclude_session or not p.active:
                continue
            if angular_distance(ra, dec, p.ra, p.dec) <= radius:
                results.append(p)
        return results
