"""Session management with economy, physical state, loadout, and jump mechanics."""

import time
import uuid
from dataclasses import dataclass, field

from .sky import Sky, PlayerSource, nearest_beacon
from .jobs import JobQueue, ObservationRequest, ObservationJob, JumpJob, JobStatus
from .telescope import Telescope
from .tracks import TrackManager
from .physics import (
    vec3_distance, vec3_add, light_time_sec, position_to_apparent,
    observation_heat, observation_power,
    jump_charge_duration, jump_charge_emission_power, jump_thermal_debt,
    jump_nav_sigma, cold_spool_visibility, jam_strength,
    SCAN_PROFILES, BASE_POWER_DRAW, BASE_DETECTION_DATA,
    UPLINK_HEAT, UPLINK_POWER_SPIKE,
    SCIENCE_UPLINK_COOLDOWN_SEC, HUNT_UPLINK_COOLDOWN_SEC,
    MAX_CHARGED_HOLD_SEC, ARRIVAL_BLOOM_SEC, SIGMA_PLAYER_POS_AU,
)
from .scoring import (
    hunting_position_score, hunting_hit_score, hunting_rewards,
    position_error_au,
    science_accuracy_score, freshness_factor, novelty_factor, science_reward,
)
from .tracks import TrackManager, TrackEvidence
from .modules import (
    validate_loadout, get_passive_effect, ACTIVE_MODULES,
    MAX_ACTIVE_SLOTS_BASE,
)
from .regions import region_for_position


# ---------------------------------------------------------------------------
# Session
# ---------------------------------------------------------------------------

@dataclass
class Session:
    session_id: str
    player_source: PlayerSource
    observation_count: int = 0
    transmit_power: float = 0.0

    # Economy
    credits: int = 0
    unbanked_data: int = 0
    intel: int = 0

    # Loadout
    passive_modules: list = field(default_factory=list)
    active_modules: list = field(default_factory=list)
    max_active_slots: int = MAX_ACTIVE_SLOTS_BASE

    # Jump state
    jump_state: str = "idle"  # idle, jump_charging, jump_charged, recalibrating
    jump_job_id: str | None = None
    recalibrating_until: float = 0.0

    # Uplink cooldowns
    science_uplink_ready_at: float = 0.0
    hunt_uplink_ready_at: float = 0.0

    # Relay scrutiny (from being hunted)
    relay_scrutiny_until: float = 0.0

    # Tracking
    science_report_counts: dict = field(default_factory=dict)  # (target_id, question_id) → count
    detection_counts: dict = field(default_factory=dict)  # source_id → count

    # Jamming (received from external jammers)
    radio_jam_strength: float = 0.0
    radio_jam_until: float = 0.0

    @property
    def snr_multiplier(self) -> float:
        """Current SNR multiplier based on jump state."""
        if self.jump_state != "recalibrating":
            return 1.0
        now = time.time()
        if now >= self.recalibrating_until:
            return 1.0
        # Rise from 0.65 to 1.0 over ARRIVAL_BLOOM_SEC
        total = ARRIVAL_BLOOM_SEC
        remaining = self.recalibrating_until - now
        progress = 1.0 - (remaining / total)
        return 0.65 + 0.35 * max(0.0, min(1.0, progress))

    @property
    def region_id(self) -> str | None:
        region = region_for_position(self.player_source.position_au)
        return region.id if region else None


# ---------------------------------------------------------------------------
# Session store
# ---------------------------------------------------------------------------

class SessionStore:
    """Manages player sessions against a shared sky."""

    def __init__(self, sky: Sky = None):
        self.sky = sky or Sky(seed=42)
        self.telescope = Telescope(self.sky)
        self.job_queue = JobQueue()
        self.track_manager = TrackManager()
        self._sessions: dict[str, Session] = {}

    def create_session(self) -> Session:
        sid = str(uuid.uuid4())[:12]
        player_src = self.sky.add_player(sid)
        session = Session(session_id=sid, player_source=player_src)
        self._sessions[sid] = session
        return session

    def get_session(self, session_id: str) -> Session | None:
        s = self._sessions.get(session_id)
        if s:
            self._tick(s)
        return s

    def _tick(self, session: Session):
        """Advance session physical state to current time."""
        now = time.time()
        p = session.player_source

        # Apply passive module effects to physical state
        glint_mult = get_passive_effect(session.passive_modules,
                                        "optical_glint_multiplier", 1.0)
        radio_mult = get_passive_effect(session.passive_modules,
                                        "radio_leakage_multiplier", 1.0)
        power_mult = get_passive_effect(session.passive_modules,
                                        "power_draw_multiplier", 1.0)
        heat_cap_mult = get_passive_effect(session.passive_modules,
                                           "heat_capacity_multiplier", 1.0)

        # cold_baffles: reduce glint
        p.optical_glint = 0.1 * glint_mult
        # signal_scrubber: reduce baseline leakage but increase idle power
        p.radio_emissions = 5.0 * radio_mult
        p.power_draw = max(p.power_draw, BASE_POWER_DRAW * power_mult)
        # phase_change_sink: increase heat capacity
        p.heat_sink_capacity = 1.0 * heat_cap_mult

        # phase_change_sink forced vent: if heat exceeds threshold, force venting
        forced_vent = get_passive_effect(session.passive_modules,
                                         "forced_vent_threshold", 1.0)
        if forced_vent < 1.0 and p.stored_heat > p.heat_sink_capacity * forced_vent:
            p.radiator_mode = "venting"

        # cold_baffles: slow heat rejection
        heat_rej_mult = get_passive_effect(session.passive_modules,
                                           "heat_rejection_multiplier", 1.0)
        self.sky.tick_player(session.session_id, now, heat_rej_mult)

        # Check recalibration expiry
        if session.jump_state == "recalibrating" and now >= session.recalibrating_until:
            session.jump_state = "idle"

        # Expire jam state
        if session.radio_jam_strength > 0 and now >= session.radio_jam_until:
            session.radio_jam_strength = 0.0

        # Jump state machine — all transitions happen here, not in check_jump
        if session.jump_state == "jump_charging" and session.jump_job_id:
            job = self.job_queue.get_jump_job(session.jump_job_id)
            if job and job.started_at and job.charge_duration_sec > 0:
                elapsed = now - job.started_at
                # Transition to charged at real completion time
                if elapsed >= job.charge_duration_sec:
                    session.jump_state = "jump_charged"
                    job.charged_at = job.started_at + job.charge_duration_sec
                else:
                    # Modulate cold_spool emission curve while still charging
                    progress = elapsed / job.charge_duration_sec
                    if job.charge_profile == "cold_spool":
                        vis = cold_spool_visibility(progress)
                        base_emission = jump_charge_emission_power(
                            vec3_distance(session.player_source.position_au,
                                          job.destination_au),
                            job.charge_profile)
                        sig_mult = get_passive_effect(
                            session.passive_modules,
                            "jump_signature_multiplier", 1.0)
                        session.player_source.jump_charge_emission = (
                            base_emission * sig_mult * vis)

        if session.jump_state == "jump_charged" and session.jump_job_id:
            job = self.job_queue.get_jump_job(session.jump_job_id)
            if job and job.charged_at:
                hold_time = now - job.charged_at
                if hold_time > MAX_CHARGED_HOLD_SEC:
                    self._abort_jump(session, job)

    # -- observations --------------------------------------------------------

    def submit_observation(self, session_id: str,
                           request: ObservationRequest) -> ObservationJob:
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError("unknown session")
        errors = request.validate()
        if errors:
            raise ValueError("; ".join(errors))

        # Apply heat and power from observation
        p = session.player_source
        heat = observation_heat(request.exposure_time, request.scan_profile)
        p.stored_heat += heat
        p.power_draw = observation_power(request.scan_profile)

        session.observation_count += 1
        return self.job_queue.submit(session_id, request)

    def check_job(self, session_id: str, job_id: str) -> ObservationJob | None:
        job = self.job_queue.get_job(job_id)
        if job is None or job.session_id != session_id:
            return None
        # If processing and ready, run the observation now
        if self.job_queue.is_ready(job) and job.result is None:
            session = self._sessions.get(session_id)
            result = self.telescope.observe(session_id, job.request, session=session)
            self.job_queue.complete_job(job_id, result)
            if session and result:
                self._award_observation_rewards(session, result, job_id=job_id)
        return job

    def _award_observation_rewards(self, session: Session, result: dict,
                                   job_id: str = ""):
        """Award data/intel from observation results and update track files."""
        data = result.get("data", {})
        base_data = data.get("rewards", {}).get("data", 0)
        base_intel = data.get("rewards", {}).get("intel", 0)

        # Apply diminishing returns per source_id
        adjusted_data = 0
        for det in data.get("detections", []):
            sid = det.get("source_id", "")
            if not sid:
                # Uncatalogued source — full reward (these are the interesting ones)
                adjusted_data += BASE_DETECTION_DATA
                continue
            prior = session.detection_counts.get(sid, 0)
            session.detection_counts[sid] = prior + 1
            # 1/(1+prior): first=full, second=half, third=third, etc.
            factor = 1.0 / (1.0 + prior)
            adjusted_data += round(BASE_DETECTION_DATA * factor)

        # Use adjusted_data if we computed per-detection, otherwise fall back
        if data.get("detections"):
            session.unbanked_data += adjusted_data
        else:
            session.unbanked_data += base_data
        session.intel += base_intel

        # Update the rewards field so the client sees what was actually awarded
        data["rewards"] = {"data": adjusted_data if data.get("detections") else base_data,
                           "intel": base_intel}

        session.player_source.power_draw = BASE_POWER_DRAW

        # Auto-populate track files from detections with no catalogue match
        now = time.time()
        for det in data.get("detections", []):
            matches = det.get("catalogue_matches", [])
            has_confident_match = any(m.get("confidence", 0) > 0.5 for m in matches)
            if has_confident_match:
                continue  # skip well-known catalogue objects

            det_id = det.get("detection_id", "")
            flux = det.get("flux", {})
            if "flux_mJy" in det:
                flux["radio_mJy"] = det["flux_mJy"]
            uncertainty = det.get("uncertainty_arcsec",
                                  det.get("uncertainty_arcmin", 60) * 60)
            instrument = result.get("headers", {}).get("INSTRUME", "unknown")

            evidence = TrackEvidence(
                job_id=job_id,
                detection_id=det_id,
                observation_epoch=now,
                apparent_ra_deg=det.get("apparent_ra_deg", 0),
                apparent_dec_deg=det.get("apparent_dec_deg", 0),
                uncertainty_arcsec=uncertainty,
                flux=flux,
                instrument=instrument,
                observer_position_au=dict(session.player_source.position_au),
                region_id=session.region_id,
                noise_floor=data.get("noise_floor_mag", data.get("noise_floor_mJy", 0)),
                scan_profile=result.get("headers", {}).get("SCANPROF", "survey"),
                light_time_sec=det.get("light_time_sec", 0),
            )

            # Try to find an existing track near this position
            existing = self._find_nearby_track(session.session_id, evidence)
            if existing:
                self.track_manager.add_evidence(existing.track_id, evidence, now)
            else:
                self.track_manager.create_track(session.session_id, evidence, now)

    def _find_nearby_track(self, session_id: str, evidence: TrackEvidence):
        """Find an existing track file close to the evidence position."""
        from .sky import _angular_distance
        tracks = self.track_manager.get_session_tracks(session_id)
        for track in tracks:
            est = track.state_estimate
            if not est:
                continue
            track_ra = est.get("apparent_ra_deg", 0)
            track_dec = est.get("apparent_dec_deg", 0)
            dist = _angular_distance(evidence.apparent_ra_deg, evidence.apparent_dec_deg,
                                     track_ra, track_dec)
            if dist < 0.5:  # within 0.5 degrees
                return track
        return None

    def list_jobs(self, session_id: str) -> list[ObservationJob]:
        jobs = self.job_queue.get_session_jobs(session_id)
        session = self._sessions.get(session_id)
        for job in jobs:
            if self.job_queue.is_ready(job) and job.result is None:
                result = self.telescope.observe(session_id, job.request,
                                                session=session)
                self.job_queue.complete_job(job.job_id, result)
                if session and result:
                    self._award_observation_rewards(session, result, job_id=job.job_id)
        return jobs

    # -- transmit (legacy, kept for backward compat) -------------------------

    def transmit(self, session_id: str, power: float) -> dict:
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError("unknown session")
        power = max(0.0, min(10.0, power))
        session.transmit_power = power
        self.sky.boost_player_emission(session_id, power)
        return {
            "transmit_power": power,
            "note": ("Broadcasting increases your radio and optical detectability "
                     "to other players."),
        }

    # -- radiator control ----------------------------------------------------

    def set_radiator_mode(self, session_id: str, mode: str) -> dict:
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError("unknown session")
        if mode not in ("sealed", "balanced", "venting"):
            raise ValueError(f"unknown radiator mode: {mode}")
        session.player_source.radiator_mode = mode
        return {
            "radiator_mode": mode,
            "ir_signature_multiplier": {
                "sealed": 0.2, "balanced": 1.0, "venting": 3.5
            }[mode],
        }

    # -- uplink (science cash-out and hunting reports) -----------------------

    def uplink(self, session_id: str, payload: dict) -> dict:
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError("unknown session")

        now = time.time()
        report_type = payload.get("report_type", "science")

        # Check cooldown
        if report_type == "hunt":
            if now < session.hunt_uplink_ready_at:
                remaining = round(session.hunt_uplink_ready_at - now, 1)
                raise ValueError(f"hunt uplink on cooldown for {remaining}s")
        else:
            if now < session.science_uplink_ready_at:
                remaining = round(session.science_uplink_ready_at - now, 1)
                raise ValueError(f"science uplink on cooldown for {remaining}s")

        # Check relay scrutiny
        if now < session.relay_scrutiny_until:
            remaining = round(session.relay_scrutiny_until - now, 1)
            raise ValueError(f"relay under scrutiny for {remaining}s — uplink degraded")

        # Uplink is a loud radio event — creates a transient burst, not a
        # permanent broadcast increase
        p = session.player_source
        p.stored_heat += UPLINK_HEAT
        BURST_DURATION_SEC = 15.0
        p.radio_burst_power = UPLINK_POWER_SPIKE
        p.radio_burst_until = now + BURST_DURATION_SEC

        # Compute light-time to beacon
        beacon = nearest_beacon(p.position_au)
        beacon_dist = vec3_distance(p.position_au, beacon["position_au"])
        receipt_delay = light_time_sec(beacon_dist)
        receipt_time = now + receipt_delay

        if report_type == "hunt":
            return self._process_hunt_uplink(session, payload, now, receipt_time)
        else:
            return self._process_science_uplink(session, payload, now, receipt_time)

    def _process_science_uplink(self, session: Session, payload: dict,
                                 now: float, receipt_time: float) -> dict:
        """Science uplink: plain banks data→credits, scored generates unbanked_data."""
        session.science_uplink_ready_at = now + SCIENCE_UPLINK_COOLDOWN_SEC
        report_id = "rep-" + str(uuid.uuid4())[:8]

        target_id = payload.get("target_id")
        question_id = payload.get("question_id")
        estimate = payload.get("estimate")

        # If a specific target/question is provided, use scored report
        if target_id and question_id and estimate is not None:
            # Look up the target's hidden state
            target_obj = None
            for obj in self.sky.objects:
                if obj.id == target_id:
                    target_obj = obj
                    break

            if target_obj is None or question_id not in target_obj.hidden_state:
                return {
                    "report_id": report_id,
                    "status": "rejected",
                    "report_type": "science",
                    "reason": f"unknown target or question: {target_id}/{question_id}",
                    "signature_cost": {"heat_added": UPLINK_HEAT, "radio_spike": True},
                }

            truth = target_obj.hidden_state[question_id]
            # Determine question type and scale
            if isinstance(truth, (int, float)):
                qtype = "scalar"
                scale = max(abs(truth) * 0.1, 1.0)  # 10% of truth as scale
            elif isinstance(truth, str):
                qtype = "enum"
                scale = 1.0
            else:
                qtype = "scalar"
                scale = 1.0

            accuracy = science_accuracy_score(estimate, truth, scale, qtype)
            # Freshness: how recently was the LAST report on this question?
            # Use time since last report (or session start if first report).
            key = (target_id, question_id)
            prior = session.science_report_counts.get(key, 0)
            staleness = 0.0  # first report is maximally fresh
            if prior > 0:
                # Approximate: each prior report ages the question
                staleness = prior * 300.0  # ~5min effective age per prior
            freshness = freshness_factor(staleness, 3600)  # 1hr halflife
            novelty = novelty_factor(prior)
            session.science_report_counts[key] = prior + 1

            data_reward, intel_reward = science_reward(
                accuracy, freshness, novelty,
                base_data=20, base_intel=5,
            )
            # Science reports generate unbanked_data, not direct credits.
            # The player still needs to do a plain uplink to bank them.
            session.unbanked_data += data_reward
            session.intel += intel_reward

            return {
                "report_id": report_id,
                "status": "accepted",
                "report_type": "science",
                "receipt_time_offset_sec": round(receipt_time - now, 2),
                "target_id": target_id,
                "question_id": question_id,
                "score": {
                    "accuracy": round(accuracy, 4),
                    "freshness": round(freshness, 4),
                    "novelty": round(novelty, 4),
                },
                "rewards": {"data": data_reward, "intel": intel_reward},
                "signature_cost": {"heat_added": UPLINK_HEAT, "radio_spike": True},
            }

        # Default: bank all unbanked data as credits
        banked = session.unbanked_data
        session.credits += banked
        session.unbanked_data = 0

        return {
            "report_id": report_id,
            "status": "accepted",
            "report_type": "science",
            "receipt_time_offset_sec": round(receipt_time - now, 2),
            "banked_credits": banked,
            "total_credits": session.credits,
            "signature_cost": {"heat_added": UPLINK_HEAT, "radio_spike": True},
        }

    def _process_hunt_uplink(self, session: Session, payload: dict,
                              now: float, receipt_time: float) -> dict:
        """Score a hunting report as a pure guess against truth.

        The player submits a classification guess and position guess.
        Evidence is for the player's own reasoning — the server scores
        only the guess quality against hidden truth at beacon receipt time.
        """
        session.hunt_uplink_ready_at = now + HUNT_UPLINK_COOLDOWN_SEC

        predicted_pos = payload.get("predicted_position_au", {})
        classification = payload.get("classification_guess", "natural")

        # Find nearest rival at receipt_time
        best_target = None
        best_dist = float("inf")
        for sid, p in self.sky.players.items():
            if sid == session.session_id:
                continue
            d = vec3_distance(predicted_pos, p.position_au)
            if d < best_dist:
                best_dist = d
                best_target = (sid, p)

        report_id = "rep-" + str(uuid.uuid4())[:8]

        # Miss if no rival within 3 * SIGMA
        if best_target is None or best_dist > 3 * SIGMA_PLAYER_POS_AU:
            return {
                "report_id": report_id,
                "status": "accepted",
                "report_type": "hunt",
                "receipt_time_offset_sec": round(receipt_time - now, 2),
                "score": {
                    "position_error_au": round(best_dist, 8) if best_target else None,
                    "classification_match": False,
                    "effective_hit_score": 0.0,
                },
                "rewards": {"intel": 0},
                "target_effect": None,
                "signature_cost": {
                    "heat_added": UPLINK_HEAT,
                    "radio_spike": True,
                },
            }

        target_sid, target_player = best_target
        target_session = self._sessions.get(target_sid)

        # Compute hit score
        pos_score = hunting_position_score(predicted_pos, target_player.position_au)
        class_correct = classification == "artificial"
        target_state = target_session.jump_state if target_session else "idle"
        effective = hunting_hit_score(pos_score, class_correct, target_state)

        # Compute rewards and consequences
        consequences = hunting_rewards(effective)

        # Award intel
        session.intel += consequences["intel_reward"]

        # Apply target consequences
        if target_session and effective >= 0.02:
            loss = int(target_session.unbanked_data * consequences["data_loss_fraction"])
            target_session.unbanked_data = max(0, target_session.unbanked_data - loss)
            if consequences["relay_scrutiny_sec"] > 0:
                target_session.relay_scrutiny_until = max(
                    target_session.relay_scrutiny_until,
                    now + consequences["relay_scrutiny_sec"]
                )

        error = position_error_au(predicted_pos, target_player.position_au)

        return {
            "report_id": report_id,
            "status": "accepted",
            "report_type": "hunt",
            "receipt_time_offset_sec": round(receipt_time - now, 2),
            "score": {
                "position_error_au": round(error, 8),
                "classification_match": class_correct,
                "effective_hit_score": round(effective, 4),
            },
            "rewards": {"intel": consequences["intel_reward"]},
            "target_effect": {
                "data_loss_fraction": consequences["data_loss_fraction"],
                "relay_scrutiny_sec": consequences["relay_scrutiny_sec"],
                "uplink_disrupted": consequences["uplink_disrupted"],
            },
            "signature_cost": {
                "heat_added": UPLINK_HEAT,
                "radio_spike": True,
            },
        }

    # -- jump mechanics ------------------------------------------------------

    def start_jump(self, session_id: str, destination_au: dict,
                   charge_profile: str = "standard") -> dict:
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError("unknown session")
        if session.jump_state != "idle":
            raise ValueError(f"cannot start jump: state is {session.jump_state}")
        if charge_profile not in ("cold_spool", "standard", "emergency"):
            raise ValueError(f"unknown charge profile: {charge_profile}")

        p = session.player_source
        distance = vec3_distance(p.position_au, destination_au)
        if distance < 0.00001:
            raise ValueError("destination too close to current position")

        charge_sec = jump_charge_duration(distance, charge_profile)

        # Apply ghost_drive passive if equipped
        charge_time_mult = get_passive_effect(
            session.passive_modules, "jump_charge_time_multiplier", 1.0)
        charge_sec *= charge_time_mult

        now = time.time()
        job = self.job_queue.submit_jump(
            session_id, destination_au, charge_profile,
            charge_sec, now,
        )

        session.jump_state = "jump_charging"
        session.jump_job_id = job.job_id

        # Set jump charge emission on player
        emission = jump_charge_emission_power(distance, charge_profile)
        sig_mult = get_passive_effect(
            session.passive_modules, "jump_signature_multiplier", 1.0)
        p.jump_charge_emission = emission * sig_mult
        p.power_draw = BASE_POWER_DRAW * 3.0  # elevated during charge

        return {
            "job_id": job.job_id,
            "status": "charging",
            "charge_duration_sec": round(charge_sec, 2),
            "destination_au": destination_au,
            "charge_profile": charge_profile,
            "observations_allowed": True,
            "signature_report": {
                "jump_charge_power": round(p.jump_charge_emission, 2),
                "stored_heat_gain_rate": round(
                    jump_thermal_debt(distance, charge_profile) / charge_sec, 4),
            },
        }

    def check_jump(self, session_id: str, job_id: str) -> dict | None:
        """Read-only status check. State transitions happen in _tick()."""
        session = self._sessions.get(session_id)
        if session is None:
            return None
        job = self.job_queue.get_jump_job(job_id)
        if job is None or job.session_id != session_id:
            return None

        # Ensure _tick has run so state is current
        self._tick(session)
        now = time.time()

        if job.status == JobStatus.COMPLETED:
            return {
                "job_id": job.job_id,
                "status": job.result.get("status", "jumped") if job.result else "completed",
                **(job.result or {}),
            }

        if session.jump_state == "jump_charged":
            hold_remaining = MAX_CHARGED_HOLD_SEC - (now - (job.charged_at or now))
            return {
                "job_id": job.job_id,
                "status": "charged",
                "commit_available": True,
                "abort_available": True,
                "hold_remaining_sec": round(max(0, hold_remaining), 1),
                "observations_allowed": True,
            }

        # Still charging
        elapsed = now - (job.started_at or now)
        charge_remaining = max(0, job.charge_duration_sec - elapsed)
        progress = min(1.0, elapsed / max(0.1, job.charge_duration_sec))

        return {
            "job_id": job.job_id,
            "status": "charging",
            "charge_remaining_sec": round(charge_remaining, 1),
            "abort_available": True,
            "observations_allowed": True,
            "signature_report": {
                "jump_charge_power": round(
                    session.player_source.jump_charge_emission, 2),
                "progress": round(progress, 3),
            },
        }

    def commit_jump(self, session_id: str, job_id: str) -> dict:
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError("unknown session")
        if session.jump_state != "jump_charged":
            raise ValueError(f"cannot commit: state is {session.jump_state}")

        job = self.job_queue.get_jump_job(job_id)
        if job is None or job.session_id != session_id:
            raise ValueError("jump job not found")

        now = time.time()
        p = session.player_source

        # Compute arrival (jam_strength affects navigation)
        nav_sigma = jump_nav_sigma(job.charge_profile, session.radio_jam_strength)
        session.radio_jam_strength = 0.0  # consumed on commit
        import random as _random
        rng = _random.Random()
        offset = {
            "x": rng.gauss(0, nav_sigma),
            "y": rng.gauss(0, nav_sigma),
            "z": rng.gauss(0, nav_sigma),
        }
        new_pos = vec3_add(job.destination_au, offset)

        # Apply thermal debt
        distance = vec3_distance(p.position_au, job.destination_au)
        thermal = jump_thermal_debt(distance, job.charge_profile)
        p.stored_heat += thermal

        # Move player
        p.position_au = new_pos

        # Arrival bloom
        bloom_mult = get_passive_effect(
            session.passive_modules, "jump_bloom_multiplier", 1.0)
        p.arrival_bloom = 5.0 * bloom_mult
        p.arrival_bloom_until = now + ARRIVAL_BLOOM_SEC
        p.jump_charge_emission = 0.0
        p.power_draw = BASE_POWER_DRAW

        # Enter recalibration
        session.jump_state = "recalibrating"
        session.recalibrating_until = now + ARRIVAL_BLOOM_SEC

        result = {
            "status": "jumped",
            "new_position_au": {k: round(v, 8) for k, v in new_pos.items()},
            "new_region": session.region_id,
            "arrival_bloom_sec": ARRIVAL_BLOOM_SEC,
            "recalibration_remaining_sec": ARRIVAL_BLOOM_SEC,
            "observations_allowed": True,
            "snr_multiplier": round(session.snr_multiplier, 2),
        }
        self.job_queue.complete_jump(job_id, result)
        return {"job_id": job_id, **result}

    def abort_jump(self, session_id: str, job_id: str) -> dict:
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError("unknown session")
        if session.jump_state not in ("jump_charging", "jump_charged"):
            raise ValueError(f"cannot abort: state is {session.jump_state}")

        job = self.job_queue.get_jump_job(job_id)
        if job is None or job.session_id != session_id:
            raise ValueError("jump job not found")

        self._abort_jump(session, job)

        p = session.player_source
        result = {
            "status": "aborted",
            "position_au": {k: round(v, 8) for k, v in p.position_au.items()},
            "thermal_debt_retained": round(p.stored_heat, 4),
            "observations_allowed": True,
        }
        self.job_queue.complete_jump(job.job_id, result)
        return {"job_id": job_id, **result}

    def _abort_jump(self, session: Session, job: JumpJob):
        """Internal abort — used by explicit abort and auto-timeout."""
        p = session.player_source
        distance = vec3_distance(p.position_au, job.destination_au)
        thermal = jump_thermal_debt(distance, job.charge_profile)
        p.stored_heat += thermal
        p.jump_charge_emission = 0.0
        p.power_draw = BASE_POWER_DRAW
        session.jump_state = "idle"
        session.jump_job_id = None

    # -- jam -----------------------------------------------------------------

    def jam(self, session_id: str, target_ra: float, target_dec: float,
            duration_sec: float = 10.0) -> dict:
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError("unknown session")

        if "directional_jammer" not in session.active_modules:
            raise ValueError("directional_jammer module not equipped")

        now = time.time()
        p = session.player_source
        mod = ACTIVE_MODULES["directional_jammer"]
        jammer_output = mod.effects["jammer_output"]

        # Jammer makes the JAMMER louder (correct: jammer is detectable)
        p.radio_emissions += mod.effects["jammer_radio_emission"]
        p.stored_heat += mod.effects["heat_spike"]

        # Find targets in the aimed direction and apply jam STATE to their
        # sessions — this degrades their radio observations and uplinks,
        # it does NOT increase their emitted signature.
        from .sky import _angular_distance
        affected = []
        for sid, target_p in self.sky.players.items():
            if sid == session_id or not target_p.active:
                continue
            app_ra, app_dec, dist = position_to_apparent(
                p.position_au, target_p.position_au)
            ang = _angular_distance(target_ra, target_dec, app_ra, app_dec)
            if ang > 5.0:
                continue
            js = jam_strength(jammer_output, dist)
            if js < 0.01:
                continue

            target_session = self._sessions.get(sid)
            if target_session:
                # Set (or extend/strengthen) jam state on target session
                target_session.radio_jam_strength = max(
                    target_session.radio_jam_strength, js)
                target_session.radio_jam_until = max(
                    target_session.radio_jam_until, now + duration_sec)

            affected.append({
                "distance_au": round(dist, 6),
                "jam_strength": round(js, 2),
            })

        return {
            "jamming": True,
            "direction": {"ra": target_ra, "dec": target_dec},
            "jammer_output": jammer_output,
            "affected_targets": len(affected),
            "effects": affected,
            "signature_cost": {
                "radio_emission": mod.effects["jammer_radio_emission"],
                "heat_spike": mod.effects["heat_spike"],
            },
        }

    # -- wideband ping -------------------------------------------------------

    def wideband_ping(self, session_id: str) -> dict:
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError("unknown session")
        if "wideband_ping" not in session.active_modules:
            raise ValueError("wideband_ping module not equipped")

        mod = ACTIVE_MODULES["wideband_ping"]
        p = session.player_source
        p.stored_heat += mod.effects["heat_spike"]
        p.radio_burst_power = mod.effects["radio_flash"]
        p.radio_burst_until = time.time() + 5.0

        # Return weak contacts in the region
        ping_radius = mod.effects["ping_radius_au"]
        contacts = []
        for sid, other in self.sky.players.items():
            if sid == session_id or not other.active:
                continue
            dist = vec3_distance(p.position_au, other.position_au)
            if dist <= ping_radius:
                app_ra, app_dec, _ = position_to_apparent(
                    p.position_au, other.position_au)
                contacts.append({
                    "apparent_ra_deg": round(app_ra, 1),
                    "apparent_dec_deg": round(app_dec, 1),
                    "distance_au": round(dist, 4),
                    "strength": round(mod.effects["ping_snr"] / max(dist, 0.0001), 1),
                })
        for obj in self.sky.objects:
            source_pos = obj.position_at(time.time())
            dist = vec3_distance(p.position_au, source_pos)
            if dist <= ping_radius and obj.radio_flux > 10:
                app_ra, app_dec, _ = position_to_apparent(
                    p.position_au, source_pos)
                contacts.append({
                    "apparent_ra_deg": round(app_ra, 1),
                    "apparent_dec_deg": round(app_dec, 1),
                    "distance_au": round(dist, 4),
                    "source_id": obj.id,
                })

        return {
            "ping": True,
            "contacts": contacts,
            "signature_cost": {
                "radio_flash": mod.effects["radio_flash"],
                "heat_spike": mod.effects["heat_spike"],
            },
        }

    # -- burst uplink --------------------------------------------------------

    def burst_uplink(self, session_id: str) -> dict:
        """Instantly bank unbanked_data. Loud radio beam."""
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError("unknown session")
        if "burst_uplink" not in session.active_modules:
            raise ValueError("burst_uplink module not equipped")

        mod = ACTIVE_MODULES["burst_uplink"]
        p = session.player_source
        p.stored_heat += mod.effects["heat_spike"]
        p.radio_burst_power = mod.effects["radio_beam"]
        p.radio_burst_until = time.time() + 10.0

        banked = session.unbanked_data
        session.credits += banked
        session.unbanked_data = 0

        return {
            "burst_uplink": True,
            "banked_credits": banked,
            "total_credits": session.credits,
            "signature_cost": {
                "radio_beam": mod.effects["radio_beam"],
                "heat_spike": mod.effects["heat_spike"],
            },
        }

    # -- decoy beacon --------------------------------------------------------

    def deploy_decoy(self, session_id: str) -> dict:
        """Deploy a decoy source near the player's position."""
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError("unknown session")
        if "decoy_beacon" not in session.active_modules:
            raise ValueError("decoy_beacon module not equipped")

        from .sky import SkyObject, TransientEvent
        mod = ACTIVE_MODULES["decoy_beacon"]
        p = session.player_source
        now = time.time()

        # Place decoy slightly offset from player
        import random as _rng
        r = _rng.Random()
        offset = 0.0003
        decoy_pos = {
            "x": p.position_au["x"] + r.uniform(-offset, offset),
            "y": p.position_au["y"] + r.uniform(-offset, offset),
            "z": p.position_au["z"] + r.uniform(-offset * 0.3, offset * 0.3),
        }

        duration = mod.effects["decoy_duration_sec"]
        self.sky._transient_counter += 1
        decoy_id = f"dcy-{self.sky._transient_counter:04d}"
        decoy = SkyObject(
            id=decoy_id,
            name=f"Decoy #{self.sky._transient_counter}",
            kind="anomaly",
            brightness=18.0,
            radio_flux=mod.effects["decoy_radio"],
            spectrum_class="unknown",
            description="Short-lived artificial source.",
            tags=["transient", "decoy"],
            motion=TransientEvent(decoy_pos, now, duration, 18.0),
        )
        self.sky.objects.append(decoy)

        return {
            "decoy_deployed": True,
            "decoy_id": decoy_id,
            "duration_sec": duration,
            "position_au": {k: round(v, 6) for k, v in decoy_pos.items()},
        }

    # -- module management ---------------------------------------------------

    def set_loadout(self, session_id: str, passive: list[str],
                    active: list[str]) -> dict:
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError("unknown session")
        errors = validate_loadout(passive, active, session.max_active_slots)
        if errors:
            raise ValueError("; ".join(errors))
        session.passive_modules = list(passive)
        session.active_modules = list(active)
        return {
            "passive_modules": session.passive_modules,
            "active_modules": session.active_modules,
        }

    # -- serialization -------------------------------------------------------

    def session_to_dict(self, session: Session) -> dict:
        self._tick(session)
        p = session.player_source
        return {
            "session_id": session.session_id,
            "telescope": {
                "id": f"SCOPE-{session.session_id[:6].upper()}",
                "position_au": {k: round(v, 8) for k, v in p.position_au.items()},
                "transmit_power": session.transmit_power,
            },
            "region": session.region_id,
            "economy": {
                "credits": session.credits,
                "unbanked_data": session.unbanked_data,
                "intel": session.intel,
            },
            "physical_state": {
                "power_draw": round(p.power_draw, 4),
                "stored_heat": round(p.stored_heat, 4),
                "heat_sink_capacity": round(p.heat_sink_capacity, 4),
                "radiator_mode": p.radiator_mode,
            },
            "signatures": {
                "radio_emissions": round(p.radio_emissions, 2),
                "optical_glint": round(p.optical_glint, 4),
                "jump_charge_emission": round(p.jump_charge_emission, 2),
                "arrival_bloom": round(p.arrival_bloom, 2),
            },
            "loadout": {
                "passive_modules": session.passive_modules,
                "active_modules": session.active_modules,
            },
            "jump_state": session.jump_state,
            "recalibration_remaining_sec": round(
                max(0, session.recalibrating_until - time.time()), 1
            ) if session.jump_state == "recalibrating" else 0,
            "snr_multiplier": round(session.snr_multiplier, 4),
            "observations_submitted": session.observation_count,
            "instruments": ["imager", "spectrograph", "radio_receiver"],
            "filters": ["clear", "r_band", "b_band", "h_alpha", "oiii"],
            "scan_profiles": list(SCAN_PROFILES.keys()),
        }
