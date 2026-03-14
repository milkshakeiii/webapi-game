"""Session management for the astronomy game."""

import uuid
from dataclasses import dataclass, field

from .sky import Sky, PlayerSource
from .jobs import JobQueue, ObservationRequest, ObservationJob
from .telescope import Telescope


@dataclass
class Session:
    session_id: str
    player_source: PlayerSource
    observation_count: int = 0
    transmit_power: float = 0.0


class SessionStore:
    """Manages player sessions against a shared sky."""

    def __init__(self, sky: Sky = None):
        self.sky = sky or Sky(seed=42)
        self.telescope = Telescope(self.sky)
        self.job_queue = JobQueue()
        self._sessions: dict[str, Session] = {}

    def create_session(self) -> Session:
        sid = str(uuid.uuid4())[:12]
        player_src = self.sky.add_player(sid)
        session = Session(session_id=sid, player_source=player_src)
        self._sessions[sid] = session
        return session

    def get_session(self, session_id: str) -> Session | None:
        return self._sessions.get(session_id)

    def submit_observation(self, session_id: str,
                           request: ObservationRequest) -> ObservationJob:
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError("unknown session")
        errors = request.validate()
        if errors:
            raise ValueError("; ".join(errors))
        session.observation_count += 1
        return self.job_queue.submit(session_id, request)

    def check_job(self, session_id: str, job_id: str) -> ObservationJob | None:
        job = self.job_queue.get_job(job_id)
        if job is None or job.session_id != session_id:
            return None
        # If processing and ready, run the observation now
        if self.job_queue.is_ready(job) and job.result is None:
            result = self.telescope.observe(session_id, job.request)
            self.job_queue.complete_job(job_id, result)
        return job

    def list_jobs(self, session_id: str) -> list[ObservationJob]:
        jobs = self.job_queue.get_session_jobs(session_id)
        # Tick any ready jobs
        for job in jobs:
            if self.job_queue.is_ready(job) and job.result is None:
                result = self.telescope.observe(session_id, job.request)
                self.job_queue.complete_job(job.job_id, result)
        return jobs

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

    def session_to_dict(self, session: Session) -> dict:
        p = session.player_source
        return {
            "session_id": session.session_id,
            "telescope": {
                "id": f"SCOPE-{session.session_id[:6].upper()}",
                "position": {"ra": round(p.ra, 4), "dec": round(p.dec, 4)},
                "transmit_power": session.transmit_power,
            },
            "observations_submitted": session.observation_count,
            "instruments": ["imager", "spectrograph", "radio_receiver"],
            "filters": ["clear", "r_band", "b_band", "h_alpha", "oiii"],
        }
