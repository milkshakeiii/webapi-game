"""Telescope observation engine: instruments, noise model, signatures, and FITS-style output."""

import math
import random
import time
import uuid
from dataclasses import dataclass

from .sky import Sky, SkyObject, _angular_distance
from .jobs import ObservationRequest
from .physics import (
    SCAN_PROFILES, inverse_square_flux, compute_signatures,
    light_time_sec, BASE_DETECTION_DATA, BASE_CLASSIFICATION_DATA,
    observation_heat, observation_power,
)
from .modules import ACTIVE_MODULES
from .regions import region_for_position


# ---------------------------------------------------------------------------
# Instrument definitions
# ---------------------------------------------------------------------------

@dataclass
class InstrumentSpec:
    name: str
    fov_radius: float        # field of view radius in degrees
    sensitivity: float
    wavelength: str           # "optical" or "radio"


INSTRUMENTS = {
    "imager": InstrumentSpec(
        name="Wide-Field Imager",
        fov_radius=1.5,
        sensitivity=1.0,
        wavelength="optical",
    ),
    "spectrograph": InstrumentSpec(
        name="Fibre Spectrograph",
        fov_radius=0.05,
        sensitivity=0.8,
        wavelength="optical",
    ),
    "radio_receiver": InstrumentSpec(
        name="Radio Receiver Array",
        fov_radius=3.0,
        sensitivity=1.0,
        wavelength="radio",
    ),
}

FILTER_THROUGHPUT = {
    None: 1.0,
    "clear": 1.0,
    "r_band": 0.8,
    "b_band": 0.7,
    "h_alpha": 0.3,
    "oiii": 0.25,
}

NARROWBAND_BONUS = {
    "h_alpha": {"emission"},
    "oiii": {"emission"},
}


# ---------------------------------------------------------------------------
# Noise model
# ---------------------------------------------------------------------------

def noise_floor(exposure_time: float, instrument: InstrumentSpec,
                filter_band: str | None) -> float:
    base_noise = 20.0
    exposure_gain = 2.5 * math.log10(max(1.0, exposure_time))
    throughput = FILTER_THROUGHPUT.get(filter_band, 1.0)
    limit = base_noise + exposure_gain / instrument.sensitivity
    limit = limit + 2.5 * math.log10(max(0.1, throughput))
    return limit


def radio_noise_floor(exposure_time: float) -> float:
    return 50.0 / math.sqrt(max(1.0, exposure_time))


def detection_snr(source_brightness: float, noise: float) -> float:
    if source_brightness >= noise:
        return 0.0
    diff = noise - source_brightness
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

    def observe(self, session_id: str, request: ObservationRequest,
                session=None) -> dict:
        instrument = INSTRUMENTS[request.instrument]
        ra, dec = request.target_ra, request.target_dec
        now = time.time()

        # Scan profile SNR multiplier
        profile = SCAN_PROFILES.get(request.scan_profile, SCAN_PROFILES["survey"])
        snr_mult = profile["snr_multiplier"]

        # Active module SNR bonus
        active_heat = 0.0
        active_power = 0.0
        active_radio = 0.0
        fov_mult = 1.0
        if request.active_module and request.active_module in ACTIVE_MODULES:
            mod = ACTIVE_MODULES[request.active_module]
            effects = mod.effects
            snr_mult += effects.get("snr_bonus", 0.0)
            active_heat = effects.get("heat_spike", 0.0)
            active_power = effects.get("power_spike", 0.0)
            active_radio = effects.get("timing_leakage_spike", 0.0)
            fov_mult = effects.get("spectrograph_fov_multiplier", 1.0)

        # Recalibration penalty
        if session is not None:
            snr_mult *= session.snr_multiplier

        # Heat penalty: high stored heat degrades SNR
        observer = self.sky.players.get(session_id)
        heat_penalty = 1.0
        if observer and observer.stored_heat > 0.5:
            heat_penalty = max(0.5, 1.0 - (observer.stored_heat - 0.5) * 0.4)
            snr_mult *= heat_penalty

        # Apply active module signature costs to observer
        if observer and (active_heat > 0 or active_radio > 0):
            observer.stored_heat += active_heat
            observer.radio_emissions += active_radio
            observer.power_draw += active_power

        # FITS headers
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
            "SCANPROF": request.scan_profile,
            "DATE-OBS": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
            "MJD-OBS": round(now / 86400.0 + 40587.0, 6),
            "FOV-RAD": instrument.fov_radius,
            "BUNIT": "mJy" if request.instrument == "radio_receiver" else "mag",
            "ORIGIN": "webapi-game/astronomy",
        }

        observer_pos = observer.position_au if observer else {"x": 0, "y": 0, "z": 0}

        # Apply FOV multiplier from active module (target_illuminator)
        effective_instrument = instrument
        if fov_mult != 1.0 and request.instrument == "spectrograph":
            effective_instrument = InstrumentSpec(
                name=instrument.name, fov_radius=instrument.fov_radius * fov_mult,
                sensitivity=instrument.sensitivity, wavelength=instrument.wavelength,
            )

        # Get observer's jam state for radio degradation
        observer_jam = 0.0
        if session is not None and hasattr(session, 'radio_jam_strength'):
            if session.radio_jam_strength > 0:
                observer_jam = session.radio_jam_strength

        if request.instrument == "radio_receiver":
            data = self._observe_radio(session_id, ra, dec, instrument,
                                       request, snr_mult, observer_pos, now,
                                       observer_jam)
        elif request.instrument == "spectrograph":
            data = self._observe_spectrum(session_id, ra, dec, effective_instrument,
                                          request, snr_mult, observer_pos, now)
        else:
            data = self._observe_image(session_id, ra, dec, instrument,
                                       request, snr_mult, observer_pos, now)

        # Compute signature report for this observation
        obs_profile = SCAN_PROFILES.get(request.scan_profile, SCAN_PROFILES["survey"])
        sig_report = {
            "heat_generated": round(
                observation_heat(request.exposure_time, request.scan_profile)
                + active_heat, 4),
            "power_draw": round(
                observation_power(request.scan_profile) + active_power, 2),
            "leakage_multiplier": obs_profile["leakage_multiplier"],
        }
        if active_radio > 0:
            sig_report["active_module_radio"] = round(active_radio, 2)
        if heat_penalty < 1.0:
            sig_report["heat_penalty"] = round(heat_penalty, 2)

        data["signature_report"] = sig_report

        return {"headers": headers, "data": data}

    # -- imager ----------------------------------------------------------------

    def _observe_image(self, session_id, ra, dec, instrument, request,
                       snr_mult, observer_pos, obs_time):
        noise = noise_floor(request.exposure_time, instrument, request.filter_band)

        region = region_for_position(observer_pos)
        if region:
            noise -= region.dust_opacity * 2.0

        fov_objects = self.sky.sources_in_fov(
            observer_pos, ra, dec, instrument.fov_radius, obs_time)
        fov_players = self.sky.players_in_fov(
            observer_pos, ra, dec, instrument.fov_radius,
            exclude_session=session_id)

        detections = []
        total_data_reward = 0

        for obj, app_ra, app_dec, dist, delay in fov_objects:
            brightness = self._adjusted_brightness(obj, request.filter_band)
            snr = detection_snr(brightness, noise) * snr_mult
            if snr > 1.0:
                det_id = "det-img-" + str(uuid.uuid4())[:6]
                uncertainty = max(0.1, 30.0 / snr)
                detections.append({
                    "detection_id": det_id,
                    "source_id": obj.id,
                    "name": obj.name,
                    "kind": obj.kind,
                    "apparent_ra_deg": round(app_ra, 4),
                    "apparent_dec_deg": round(app_dec, 4),
                    "uncertainty_arcsec": round(uncertainty, 2),
                    "flux": {"optical_mag": round(brightness, 2)},
                    "snr": round(snr, 2),
                    "light_time_sec": round(delay, 2),
                    "catalogue_matches": [
                        {"target_id": obj.id,
                         "confidence": round(min(1.0, snr / 20), 2)}
                    ],
                })
                total_data_reward += BASE_DETECTION_DATA

        for p, app_ra, app_dec, dist in fov_players:
            brightness = self._player_optical_brightness(p, dist)
            snr = detection_snr(brightness, noise) * snr_mult
            if snr > 1.0:
                jitter = max(0.001, 0.1 / snr)
                det_id = "det-img-" + str(uuid.uuid4())[:6]
                uncertainty = max(0.1, 30.0 / snr)
                det_ra = app_ra + self._rng.gauss(0, jitter)
                det_dec = app_dec + self._rng.gauss(0, jitter)

                motion_hint = {}
                if p.jump_charge_emission > 0:
                    motion_hint["broadband_charge_detected"] = True

                detection = {
                    "detection_id": det_id,
                    "apparent_ra_deg": round(det_ra, 4),
                    "apparent_dec_deg": round(det_dec, 4),
                    "uncertainty_arcsec": round(uncertainty, 2),
                    "flux": {"optical_mag": round(brightness, 2)},
                    "shape_hint": "point",
                    "snr": round(snr, 2),
                    "catalogue_matches": [],
                }
                if motion_hint:
                    detection["motion_hint"] = motion_hint
                detections.append(detection)

        return {
            "type": "image",
            "observation_epoch": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime(obs_time)),
            "noise_floor_mag": round(noise, 2),
            "fov_radius_deg": instrument.fov_radius,
            "n_sources": len(detections),
            "detections": sorted(detections,
                                 key=lambda d: d["flux"].get("optical_mag", 30)),
            "rewards": {"data": total_data_reward, "intel": 0},
        }

    # -- spectrograph ----------------------------------------------------------

    def _observe_spectrum(self, session_id, ra, dec, instrument, request,
                          snr_mult, observer_pos, obs_time):
        noise = noise_floor(request.exposure_time, instrument, request.filter_band)

        fov_objects = self.sky.sources_in_fov(
            observer_pos, ra, dec, instrument.fov_radius, obs_time)
        fov_players = self.sky.players_in_fov(
            observer_pos, ra, dec, instrument.fov_radius,
            exclude_session=session_id)

        # Find nearest source in the tiny slit
        target = None
        target_type = None
        target_dist = 0.0
        min_ang = float("inf")

        for obj, app_ra, app_dec, dist, delay in fov_objects:
            ang = _angular_distance(ra, dec, app_ra, app_dec)
            if ang < min_ang:
                min_ang = ang
                target = obj
                target_type = "catalogue"
                target_dist = dist

        for p, app_ra, app_dec, dist in fov_players:
            ang = _angular_distance(ra, dec, app_ra, app_dec)
            if ang < min_ang:
                min_ang = ang
                target = p
                target_type = "player"
                target_dist = dist

        no_result = {
            "type": "spectrum",
            "observation_epoch": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime(obs_time)),
            "target_acquired": False,
            "noise_floor_mag": round(noise, 2),
            "rewards": {"data": 0, "intel": 0},
        }

        if target is None:
            no_result["note"] = "No source found within spectrograph slit."
            return no_result

        if target_type == "catalogue":
            brightness = self._adjusted_brightness(target, request.filter_band)
            snr = detection_snr(brightness, noise) * snr_mult
            if snr < 1.0:
                no_result["note"] = "Source too faint for spectral analysis at this exposure."
                return no_result

            features = self._spectral_features(target, snr)
            material_hints = []
            intel_reward = 0
            if target.kind in ("relay", "derelict"):
                material_hints = ["painted metal or composite panel"]
                intel_reward = 3

            return {
                "type": "spectrum",
                "observation_epoch": time.strftime(
                    "%Y-%m-%dT%H:%M:%SZ", time.gmtime(obs_time)),
                "target_acquired": True,
                "source_id": target.id,
                "name": target.name,
                "kind": target.kind,
                "spectrum_class": target.spectrum_class,
                "snr": round(snr, 2),
                "light_time_sec": round(light_time_sec(target_dist), 2),
                "features": features,
                "material_hints": material_hints,
                "catalogue_matches": [
                    {"target_id": target.id,
                     "confidence": round(min(1.0, snr / 15), 2)}
                ],
                "rewards": {"data": BASE_CLASSIFICATION_DATA, "intel": intel_reward},
            }
        else:
            # Player source
            brightness = self._player_optical_brightness(target, target_dist)
            snr = detection_snr(brightness, noise) * snr_mult
            if snr < 1.0:
                no_result["note"] = "Source too faint for spectral analysis at this exposure."
                return no_result

            continuum = "flat, non-stellar"
            line_features = ["unidentified narrow emission"]
            material_hints = []

            if snr > 5:
                continuum = "flat-to-rising infrared"
                line_features.append("broad thermal continuum")
                material_hints.append("heated radiator surface")
            if target.stored_heat > 0.3 and snr > 10:
                material_hints.append("active thermal management")
            if target.jump_charge_emission > 0 and snr > 3:
                line_features.append("broadband non-thermal emission")
                material_hints.append("high-energy field source")

            det_id = "det-spec-" + str(uuid.uuid4())[:6]
            return {
                "type": "spectrum",
                "observation_epoch": time.strftime(
                    "%Y-%m-%dT%H:%M:%SZ", time.gmtime(obs_time)),
                "target_acquired": True,
                "source_ref": det_id,
                "spectrum_class": "non-thermal",
                "snr": round(snr, 2),
                "continuum_fit": continuum,
                "line_features": line_features,
                "material_hints": material_hints,
                "catalogue_matches": [],
                "rewards": {"data": 0, "intel": 5},
            }

    # -- radio -----------------------------------------------------------------

    def _observe_radio(self, session_id, ra, dec, instrument, request,
                       snr_mult, observer_pos, obs_time, observer_jam=0.0):
        noise_mJy = radio_noise_floor(request.exposure_time)

        region = region_for_position(observer_pos)
        if region:
            noise_mJy += region.radio_noise

        # Jamming raises the observer's radio noise floor
        if observer_jam > 0:
            noise_mJy *= (1.0 + observer_jam)

        fov_objects = self.sky.sources_in_fov(
            observer_pos, ra, dec, instrument.fov_radius, obs_time)
        fov_players = self.sky.players_in_fov(
            observer_pos, ra, dec, instrument.fov_radius,
            exclude_session=session_id)

        detections = []
        total_data_reward = 0

        for obj, app_ra, app_dec, dist, delay in fov_objects:
            flux = inverse_square_flux(obj.radio_flux, max(dist, 0.0001))
            snr = radio_detection_snr(flux, noise_mJy) * snr_mult
            if snr > 1.0:
                det_id = "det-rad-" + str(uuid.uuid4())[:6]
                uncertainty = max(0.5, 120.0 / snr)
                detections.append({
                    "detection_id": det_id,
                    "source_id": obj.id,
                    "name": obj.name,
                    "kind": obj.kind,
                    "apparent_ra_deg": round(app_ra, 4),
                    "apparent_dec_deg": round(app_dec, 4),
                    "uncertainty_arcmin": round(uncertainty, 2),
                    "flux_mJy": round(flux, 2),
                    "snr": round(snr, 2),
                    "light_time_sec": round(delay, 2),
                    "periodic": "periodic" in (obj.tags or []),
                    "burstiness": 0.0,
                    "catalogue_matches": [
                        {"target_id": obj.id,
                         "confidence": round(min(1.0, snr / 20), 2)}
                    ],
                })
                total_data_reward += BASE_DETECTION_DATA

        for p, app_ra, app_dec, dist in fov_players:
            sigs = compute_signatures(
                p.power_draw, p.stored_heat, p.radiator_mode,
                p.radio_emissions, p.optical_glint,
                p.jump_charge_emission, p.arrival_bloom,
            )
            total_radio = sigs["radio_flux"] + p.effective_radio_power * 100
            flux = inverse_square_flux(total_radio, max(dist, 0.0001))
            snr = radio_detection_snr(flux, noise_mJy) * snr_mult
            if snr > 1.0:
                jitter = max(0.01, 0.5 / snr)
                det_id = "det-rad-" + str(uuid.uuid4())[:6]
                uncertainty = max(0.5, 120.0 / snr)
                det_ra = app_ra + self._rng.gauss(0, jitter)
                det_dec = app_dec + self._rng.gauss(0, jitter)

                burstiness = 0.0
                bandwidth_hz = 2000
                spectral_slope = -0.5
                if p.broadcast_power > 0:
                    burstiness = 0.1
                    bandwidth_hz = 800
                    spectral_slope = 0.0
                if p.jump_charge_emission > 0:
                    burstiness = 0.7
                    bandwidth_hz = 50000
                    spectral_slope = -0.2

                detections.append({
                    "detection_id": det_id,
                    "apparent_ra_deg": round(det_ra, 4),
                    "apparent_dec_deg": round(det_dec, 4),
                    "uncertainty_arcmin": round(uncertainty, 2),
                    "flux_mJy": round(flux, 2),
                    "snr": round(snr, 2),
                    "bandwidth_hz": bandwidth_hz,
                    "spectral_slope": spectral_slope,
                    "burstiness": round(burstiness, 2),
                    "periodic": False,
                    "catalogue_matches": [],
                })

        return {
            "type": "radio_map",
            "observation_epoch": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime(obs_time)),
            "noise_floor_mJy": round(noise_mJy, 2),
            "fov_radius_deg": instrument.fov_radius,
            "n_sources": len(detections),
            "detections": sorted(detections, key=lambda d: -d["flux_mJy"]),
            "rewards": {"data": total_data_reward, "intel": 0},
        }

    # -- helpers ---------------------------------------------------------------

    def _player_optical_brightness(self, p, dist: float) -> float:
        """Compute a player's apparent optical magnitude from signatures and distance.

        Optical brightness comes from IR, glint, and bloom — not radio broadcast.
        """
        sigs = compute_signatures(
            p.power_draw, p.stored_heat, p.radiator_mode,
            p.radio_emissions, p.optical_glint,
            p.jump_charge_emission, p.arrival_bloom,
        )
        ir_flux = inverse_square_flux(sigs["ir_brightness"] + 1.0, dist)
        opt_flux = inverse_square_flux(sigs["optical_brightness"] + 0.5, dist)
        total_flux = ir_flux + opt_flux
        if total_flux > 0:
            return 20.0 - 2.5 * math.log10(total_flux)
        return 25.0

    def _adjusted_brightness(self, obj: SkyObject, filter_band: str | None) -> float:
        mag = obj.brightness
        throughput = FILTER_THROUGHPUT.get(filter_band, 1.0)
        if throughput < 1.0:
            mag -= 2.5 * math.log10(max(0.01, throughput))
        bonus_tags = NARROWBAND_BONUS.get(filter_band, set())
        if bonus_tags & set(obj.tags or []):
            mag -= 2.0
        return mag

    def _spectral_features(self, obj: SkyObject, snr: float) -> dict:
        features = {"lines": [], "continuum": "", "snr_quality": ""}

        if snr > 20:
            features["snr_quality"] = "excellent"
        elif snr > 5:
            features["snr_quality"] = "good"
        else:
            features["snr_quality"] = "marginal"

        cls = obj.spectrum_class
        spec_map = {
            "O": ("blue, rising toward UV", ["He II absorption", "H-beta absorption"]),
            "B": ("blue, rising toward UV", ["He II absorption", "H-beta absorption"]),
            "G": ("solar-type, peak ~550nm", ["Ca II H&K absorption", "Fe I absorption", "H-alpha absorption"]),
            "synchrotron": ("power-law, non-thermal", ["featureless"]),
            "composite": ("mixed stellar + non-thermal", ["H-alpha emission", "Ca II absorption", "Fe II emission"]),
            "reflection": ("blue-shifted stellar reflection", ["scattered stellar absorption lines"]),
            "elliptical": ("red, old stellar population", ["Ca II absorption", "Mg I absorption"]),
            "mixed": ("composite, multiple stellar types", ["blended absorption features"]),
            "silicate": ("rocky, silicate absorption bands", ["silicate 10μm feature", "olivine bands"]),
            "carbonaceous": ("dark, carbon-rich surface", ["C-H stretch", "organic absorption"]),
            "volatile": ("cometary, scattered solar", ["CN emission", "C2 Swan bands", "OH emission"]),
            "metallic": ("metallic reflectance", ["Fe absorption", "Ni absorption"]),
            "unknown": ("unclassified", ["unidentified features"]),
        }

        if cls == "emission":
            features["continuum"] = "faint continuum with strong emission"
            features["lines"] = ["H-alpha emission", "N II emission", "S II emission"]
            if snr > 10:
                features["lines"].append("O III emission")
        elif cls in spec_map:
            features["continuum"], features["lines"] = spec_map[cls]
            features["lines"] = list(features["lines"])  # copy
        else:
            features["continuum"] = "unclassified"
            features["lines"] = ["unidentified features"]

        return features
