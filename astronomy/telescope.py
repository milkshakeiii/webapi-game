"""Telescope observation engine: instruments, noise model, and FITS-style output."""

import math
import random
import time
from dataclasses import dataclass

from .sky import Sky, SkyObject, PlayerSource, angular_distance
from .jobs import ObservationRequest


# ---------------------------------------------------------------------------
# Instrument definitions
# ---------------------------------------------------------------------------

@dataclass
class InstrumentSpec:
    name: str
    fov_radius: float        # field of view radius in degrees
    sensitivity: float       # lower = can detect fainter sources
    wavelength: str          # "optical", "radio", "narrow_optical"


INSTRUMENTS = {
    "imager": InstrumentSpec(
        name="Wide-Field Imager",
        fov_radius=1.5,
        sensitivity=1.0,
        wavelength="optical",
    ),
    "spectrograph": InstrumentSpec(
        name="Fibre Spectrograph",
        fov_radius=0.05,      # single-object, tiny FOV
        sensitivity=0.8,
        wavelength="optical",
    ),
    "radio_receiver": InstrumentSpec(
        name="Radio Receiver Array",
        fov_radius=3.0,       # wide beam
        sensitivity=1.0,
        wavelength="radio",
    ),
}

# Filter throughput multipliers (how well each filter transmits signal)
FILTER_THROUGHPUT = {
    None: 1.0,
    "clear": 1.0,
    "r_band": 0.8,
    "b_band": 0.7,
    "h_alpha": 0.3,     # narrow-band, faint but isolates emission
    "oiii": 0.25,
}

# Bonus for emission objects observed through matching narrow-band filter
NARROWBAND_BONUS = {
    "h_alpha": {"emission"},
    "oiii": {"emission"},
}


# ---------------------------------------------------------------------------
# Noise model
# ---------------------------------------------------------------------------

def noise_floor(exposure_time: float, instrument: InstrumentSpec,
                filter_band: str | None) -> float:
    """
    Compute the noise floor for an observation.
    Lower noise = can detect fainter sources.
    Noise decreases with sqrt(exposure_time).
    """
    base_noise = 20.0  # magnitude limit with 1s exposure
    # Longer exposure => deeper observation (can see fainter things)
    exposure_gain = 2.5 * math.log10(max(1.0, exposure_time))
    throughput = FILTER_THROUGHPUT.get(filter_band, 1.0)
    # Effective limiting magnitude
    limit = base_noise + exposure_gain / instrument.sensitivity
    # Narrow-band filters reduce overall depth but reveal specific features
    limit = limit + 2.5 * math.log10(max(0.1, throughput))
    return limit


def radio_noise_floor(exposure_time: float) -> float:
    """Minimum detectable radio flux in mJy."""
    # Baseline sensitivity ~50 mJy, improves with sqrt(time)
    return 50.0 / math.sqrt(max(1.0, exposure_time))


def detection_snr(source_brightness: float, noise: float) -> float:
    """Signal-to-noise ratio for an optical source. Higher = clearer detection."""
    if source_brightness >= noise:
        return 0.0  # below noise floor
    diff = noise - source_brightness  # magnitudes above noise floor
    return min(100.0, 10 ** (diff / 2.5))


def radio_detection_snr(flux: float, noise_mJy: float) -> float:
    if flux <= noise_mJy:
        return 0.0
    return min(100.0, flux / noise_mJy)


# ---------------------------------------------------------------------------
# Observation processor
# ---------------------------------------------------------------------------

class Telescope:
    """Processes observation requests against the sky model."""

    def __init__(self, sky: Sky, rng_seed=None):
        self.sky = sky
        self._rng = random.Random(rng_seed)

    def observe(self, session_id: str, request: ObservationRequest) -> dict:
        """Run an observation and return a FITS-style result dict."""
        instrument = INSTRUMENTS[request.instrument]
        ra, dec = request.target_ra, request.target_dec
        now = time.time()

        # -- build FITS headers -----------------------------------------------
        headers = {
            "SIMPLE": True,
            "BITPIX": -32,
            "NAXIS": 2,
            "TELESCOP": f"SCOPE-{session_id[:6].upper()}",
            "INSTRUME": instrument.name,
            "RA": round(ra, 6),
            "DEC": round(dec, 6),
            "EXPTIME": request.exposure_time,
            "FILTER": (request.filter_band or "clear").upper(),
            "DATE-OBS": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
            "MJD-OBS": round(now / 86400.0 + 40587.0, 6),
            "FOV-RAD": instrument.fov_radius,
            "BUNIT": "mJy" if request.instrument == "radio_receiver" else "mag",
            "ORIGIN": "webapi-game/astronomy",
        }

        # -- detect sources ----------------------------------------------------
        if request.instrument == "radio_receiver":
            data = self._observe_radio(session_id, ra, dec, instrument, request)
        elif request.instrument == "spectrograph":
            data = self._observe_spectrum(session_id, ra, dec, instrument, request)
        else:
            data = self._observe_image(session_id, ra, dec, instrument, request)

        return {"headers": headers, "data": data}

    # -- imager ----------------------------------------------------------------

    def _observe_image(self, session_id, ra, dec, instrument, request):
        noise = noise_floor(request.exposure_time, instrument, request.filter_band)
        objects = self.sky.objects_in_fov(ra, dec, instrument.fov_radius)
        players = self.sky.players_in_fov(ra, dec, instrument.fov_radius,
                                          exclude_session=session_id)

        detections = []
        for obj in objects:
            brightness = self._adjusted_brightness(obj, request.filter_band)
            snr = detection_snr(brightness, noise)
            if snr > 1.0:
                detections.append({
                    "source_id": obj.id,
                    "name": obj.name,
                    "kind": obj.kind,
                    "ra": obj.ra,
                    "dec": obj.dec,
                    "magnitude": round(brightness, 2),
                    "snr": round(snr, 2),
                    "offset_deg": round(angular_distance(ra, dec, obj.ra, obj.dec), 4),
                })

        for p in players:
            brightness = p.optical_brightness - (p.broadcast_power * 0.5)
            snr = detection_snr(brightness, noise)
            if snr > 1.0:
                # Add positional jitter inversely proportional to SNR
                jitter = max(0.001, 0.1 / snr)
                detections.append({
                    "source_id": f"UNK-{p.session_id[:6].upper()}",
                    "name": None,
                    "kind": "unidentified",
                    "ra": round(p.ra + self._rng.gauss(0, jitter), 4),
                    "dec": round(p.dec + self._rng.gauss(0, jitter), 4),
                    "magnitude": round(brightness, 2),
                    "snr": round(snr, 2),
                    "offset_deg": round(angular_distance(ra, dec, p.ra, p.dec), 4),
                })

        return {
            "type": "image",
            "noise_floor_mag": round(noise, 2),
            "fov_radius_deg": instrument.fov_radius,
            "n_sources": len(detections),
            "detections": sorted(detections, key=lambda d: d["magnitude"]),
        }

    # -- spectrograph ----------------------------------------------------------

    def _observe_spectrum(self, session_id, ra, dec, instrument, request):
        noise = noise_floor(request.exposure_time, instrument, request.filter_band)

        # Find the nearest source within the tiny slit FOV
        objects = self.sky.objects_in_fov(ra, dec, instrument.fov_radius)
        players = self.sky.players_in_fov(ra, dec, instrument.fov_radius,
                                          exclude_session=session_id)

        target = None
        target_type = None
        min_dist = float("inf")

        for obj in objects:
            d = angular_distance(ra, dec, obj.ra, obj.dec)
            if d < min_dist:
                min_dist = d
                target = obj
                target_type = "catalogue"

        for p in players:
            d = angular_distance(ra, dec, p.ra, p.dec)
            if d < min_dist:
                min_dist = d
                target = p
                target_type = "player"

        if target is None:
            return {
                "type": "spectrum",
                "target_acquired": False,
                "noise_floor_mag": round(noise, 2),
                "note": "No source found within spectrograph slit.",
            }

        if target_type == "catalogue":
            brightness = self._adjusted_brightness(target, request.filter_band)
            snr = detection_snr(brightness, noise)
            if snr < 1.0:
                return {
                    "type": "spectrum",
                    "target_acquired": False,
                    "noise_floor_mag": round(noise, 2),
                    "note": "Source too faint for spectral analysis at this exposure.",
                }
            return {
                "type": "spectrum",
                "target_acquired": True,
                "source_id": target.id,
                "name": target.name,
                "kind": target.kind,
                "spectrum_class": target.spectrum_class,
                "snr": round(snr, 2),
                "features": self._spectral_features(target, snr),
            }
        else:
            # Player source spectrum
            brightness = target.optical_brightness - (target.broadcast_power * 0.5)
            snr = detection_snr(brightness, noise)
            if snr < 1.0:
                return {
                    "type": "spectrum",
                    "target_acquired": False,
                    "noise_floor_mag": round(noise, 2),
                    "note": "Source too faint for spectral analysis at this exposure.",
                }
            return {
                "type": "spectrum",
                "target_acquired": True,
                "source_id": f"UNK-{target.session_id[:6].upper()}",
                "kind": "artificial",
                "spectrum_class": "non-thermal",
                "snr": round(snr, 2),
                "features": {
                    "lines": ["unidentified narrow emission"],
                    "continuum": "flat, non-stellar",
                    "classification_hint": "Possible artificial origin",
                    "broadcast_detected": target.broadcast_power > 0,
                },
            }

    # -- radio -----------------------------------------------------------------

    def _observe_radio(self, session_id, ra, dec, instrument, request):
        noise_mJy = radio_noise_floor(request.exposure_time)
        objects = self.sky.objects_in_fov(ra, dec, instrument.fov_radius)
        players = self.sky.players_in_fov(ra, dec, instrument.fov_radius,
                                          exclude_session=session_id)

        detections = []
        for obj in objects:
            snr = radio_detection_snr(obj.radio_flux, noise_mJy)
            if snr > 1.0:
                detections.append({
                    "source_id": obj.id,
                    "name": obj.name,
                    "kind": obj.kind,
                    "ra": obj.ra,
                    "dec": obj.dec,
                    "flux_mJy": round(obj.radio_flux, 2),
                    "snr": round(snr, 2),
                    "offset_deg": round(angular_distance(ra, dec, obj.ra, obj.dec), 4),
                    "periodic": "periodic" in (obj.tags or []),
                })

        for p in players:
            total_flux = p.radio_flux + p.broadcast_power * 100
            snr = radio_detection_snr(total_flux, noise_mJy)
            if snr > 1.0:
                jitter = max(0.01, 0.5 / snr)
                detections.append({
                    "source_id": f"UNK-{p.session_id[:6].upper()}",
                    "name": None,
                    "kind": "unidentified",
                    "ra": round(p.ra + self._rng.gauss(0, jitter), 4),
                    "dec": round(p.dec + self._rng.gauss(0, jitter), 4),
                    "flux_mJy": round(total_flux, 2),
                    "snr": round(snr, 2),
                    "offset_deg": round(angular_distance(ra, dec, p.ra, p.dec), 4),
                    "periodic": False,
                    "signal_character": "narrowband" if p.broadcast_power > 0 else "wideband",
                })

        return {
            "type": "radio_map",
            "noise_floor_mJy": round(noise_mJy, 2),
            "fov_radius_deg": instrument.fov_radius,
            "n_sources": len(detections),
            "detections": sorted(detections, key=lambda d: -d["flux_mJy"]),
        }

    # -- helpers ---------------------------------------------------------------

    def _adjusted_brightness(self, obj: SkyObject, filter_band: str | None) -> float:
        """Adjust brightness for filter and object type."""
        mag = obj.brightness
        # Narrow-band filters make everything fainter...
        throughput = FILTER_THROUGHPUT.get(filter_band, 1.0)
        if throughput < 1.0:
            mag -= 2.5 * math.log10(max(0.01, throughput))
        # ...but emission objects are brighter in matching narrow-bands
        bonus_tags = NARROWBAND_BONUS.get(filter_band, set())
        if bonus_tags & set(obj.tags or []):
            mag -= 2.0  # emission object shines through narrow-band
        return mag

    def _spectral_features(self, obj: SkyObject, snr: float) -> dict:
        """Generate spectral feature report based on object type and SNR."""
        features = {"lines": [], "continuum": "", "snr_quality": ""}

        if snr > 20:
            features["snr_quality"] = "excellent"
        elif snr > 5:
            features["snr_quality"] = "good"
        else:
            features["snr_quality"] = "marginal"

        cls = obj.spectrum_class
        if cls in ("O", "B"):
            features["continuum"] = "blue, rising toward UV"
            features["lines"] = ["He II absorption", "H-beta absorption"]
        elif cls == "G":
            features["continuum"] = "solar-type, peak ~550nm"
            features["lines"] = ["Ca II H&K absorption", "Fe I absorption", "H-alpha absorption"]
        elif cls == "emission":
            features["continuum"] = "faint continuum with strong emission"
            features["lines"] = ["H-alpha emission", "N II emission", "S II emission"]
            if snr > 10:
                features["lines"].append("O III emission")
        elif cls == "synchrotron":
            features["continuum"] = "power-law, non-thermal"
            features["lines"] = ["featureless"]
        elif cls == "composite":
            features["continuum"] = "mixed stellar + non-thermal"
            features["lines"] = ["H-alpha emission", "Ca II absorption", "Fe II emission"]
        elif cls == "reflection":
            features["continuum"] = "blue-shifted stellar reflection"
            features["lines"] = ["scattered stellar absorption lines"]
        elif cls == "elliptical":
            features["continuum"] = "red, old stellar population"
            features["lines"] = ["Ca II absorption", "Mg I absorption"]
        elif cls == "mixed":
            features["continuum"] = "composite, multiple stellar types"
            features["lines"] = ["blended absorption features"]
        else:
            features["continuum"] = "unclassified"
            features["lines"] = ["unidentified features"]

        return features
