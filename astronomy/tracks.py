"""Track file management for aggregating observations into source tracks."""

import uuid
from dataclasses import dataclass, field


@dataclass
class TrackEvidence:
    job_id: str
    detection_id: str
    observation_epoch: float  # timestamp
    apparent_ra_deg: float
    apparent_dec_deg: float
    uncertainty_arcsec: float
    flux: dict  # band → value
    instrument: str
    observer_position_au: dict = field(default_factory=lambda: {"x": 0, "y": 0, "z": 0})
    region_id: str | None = None
    noise_floor: float = 0.0
    scan_profile: str = "survey"
    light_time_sec: float = 0.0


@dataclass
class TrackFile:
    track_id: str
    session_id: str
    source_status: str = "provisional"  # provisional, confirmed, stale
    evidence: list[TrackEvidence] = field(default_factory=list)
    state_estimate: dict = field(default_factory=dict)
    motion_hypothesis: str = "unknown"
    catalogue_match: dict = field(default_factory=lambda: {
        "best_target_id": None, "confidence": 0.0
    })
    signal_summary: dict = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    created_at: float = 0.0
    updated_at: float = 0.0


class TrackManager:
    """Manages track files for a session."""

    def __init__(self):
        self._tracks: dict[str, TrackFile] = {}  # track_id → TrackFile
        self._by_session: dict[str, list[str]] = {}  # session_id → [track_id]

    def create_track(self, session_id: str, evidence: TrackEvidence,
                     timestamp: float) -> TrackFile:
        track_id = "trk-" + str(uuid.uuid4())[:8]
        track = TrackFile(
            track_id=track_id,
            session_id=session_id,
            evidence=[evidence],
            created_at=timestamp,
            updated_at=timestamp,
        )
        self._update_estimates(track)
        self._tracks[track_id] = track
        self._by_session.setdefault(session_id, []).append(track_id)
        return track

    def add_evidence(self, track_id: str, evidence: TrackEvidence,
                     timestamp: float) -> TrackFile | None:
        track = self._tracks.get(track_id)
        if track is None:
            return None
        track.evidence.append(evidence)
        track.updated_at = timestamp
        self._update_estimates(track)
        return track

    def get_track(self, track_id: str) -> TrackFile | None:
        return self._tracks.get(track_id)

    def get_session_tracks(self, session_id: str) -> list[TrackFile]:
        track_ids = self._by_session.get(session_id, [])
        return [self._tracks[tid] for tid in track_ids if tid in self._tracks]

    def _update_estimates(self, track: TrackFile):
        """Recompute state estimate from evidence."""
        if not track.evidence:
            return

        # Weighted average position (weight by 1/uncertainty^2)
        total_weight = 0.0
        ra_sum = 0.0
        dec_sum = 0.0
        latest_epoch = 0.0

        flux_optical = []
        flux_ir = []
        flux_radio = []

        for ev in track.evidence:
            w = 1.0 / max(0.1, ev.uncertainty_arcsec) ** 2
            total_weight += w
            ra_sum += ev.apparent_ra_deg * w
            dec_sum += ev.apparent_dec_deg * w
            latest_epoch = max(latest_epoch, ev.observation_epoch)

            if "optical_mag" in ev.flux:
                flux_optical.append(ev.flux["optical_mag"])
            if "ir_mag" in ev.flux:
                flux_ir.append(ev.flux["ir_mag"])
            if "radio_mJy" in ev.flux:
                flux_radio.append(ev.flux["radio_mJy"])

        if total_weight > 0:
            avg_ra = ra_sum / total_weight
            avg_dec = dec_sum / total_weight
            # Position sigma decreases with more evidence
            pos_sigma = 1.0 / (total_weight ** 0.5) if total_weight > 0 else 999.0
        else:
            avg_ra = track.evidence[-1].apparent_ra_deg
            avg_dec = track.evidence[-1].apparent_dec_deg
            pos_sigma = 999.0

        track.state_estimate = {
            "fit_epoch": latest_epoch,
            "apparent_ra_deg": round(avg_ra, 6),
            "apparent_dec_deg": round(avg_dec, 6),
            "position_sigma_arcsec": round(pos_sigma, 4),
        }

        # Signal summary
        summary = {}
        if flux_optical:
            summary["optical_mag"] = round(sum(flux_optical) / len(flux_optical), 2)
        if flux_ir:
            summary["ir_mag"] = round(sum(flux_ir) / len(flux_ir), 2)
        if flux_radio:
            summary["radio_flux_mJy"] = round(sum(flux_radio) / len(flux_radio), 2)
        track.signal_summary = summary

        # Motion hypothesis from spread
        if len(track.evidence) >= 2:
            ras = [e.apparent_ra_deg for e in track.evidence]
            decs = [e.apparent_dec_deg for e in track.evidence]
            ra_spread = max(ras) - min(ras)
            dec_spread = max(decs) - min(decs)
            total_spread = (ra_spread ** 2 + dec_spread ** 2) ** 0.5
            if total_spread < 0.001:
                track.motion_hypothesis = "stationary_or_low_drift"
            elif total_spread < 0.01:
                track.motion_hypothesis = "slow_drift"
            else:
                track.motion_hypothesis = "significant_motion"

        # Notes
        track.notes = []
        if not track.catalogue_match["best_target_id"]:
            track.notes.append("no confident catalogue match")
        if len(track.evidence) == 1:
            track.notes.append("single observation — needs follow-up")

    def track_to_dict(self, track: TrackFile) -> dict:
        return {
            "track_id": track.track_id,
            "source_status": track.source_status,
            "evidence": [
                {
                    "job_id": ev.job_id,
                    "detection_id": ev.detection_id,
                    "observation_epoch": ev.observation_epoch,
                    "observer_position_au": ev.observer_position_au,
                    "apparent_ra_deg": ev.apparent_ra_deg,
                    "apparent_dec_deg": ev.apparent_dec_deg,
                    "uncertainty_arcsec": ev.uncertainty_arcsec,
                    "flux": ev.flux,
                    "instrument": ev.instrument,
                    "region_id": ev.region_id,
                    "noise_floor": ev.noise_floor,
                    "scan_profile": ev.scan_profile,
                    "light_time_sec": ev.light_time_sec,
                }
                for ev in track.evidence
            ],
            "state_estimate": track.state_estimate,
            "motion_hypothesis": track.motion_hypothesis,
            "catalogue_match": track.catalogue_match,
            "signal_summary": track.signal_summary,
            "notes": track.notes,
        }
