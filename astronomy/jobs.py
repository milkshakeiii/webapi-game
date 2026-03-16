"""Async observation and jump job queues."""

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum


class JobStatus(Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


VALID_SCAN_PROFILES = {"low_power", "survey", "boosted", "overclocked"}


@dataclass
class ObservationRequest:
    """RTML-style observation request."""
    target_ra: float
    target_dec: float
    instrument: str            # "imager", "spectrograph", "radio_receiver"
    filter_band: str | None    # "clear", "h_alpha", "oiii", "r_band", "b_band", None
    exposure_time: float       # seconds
    scheduling_priority: str = "medium"  # "low", "medium", "high", "override"
    scan_profile: str = "survey"  # "low_power", "survey", "boosted", "overclocked"
    active_module: str | None = None

    def validate(self):
        errors = []
        if not (0 <= self.target_ra <= 360):
            errors.append("target.ra must be 0-360")
        if not (-90 <= self.target_dec <= 90):
            errors.append("target.dec must be -90 to +90")
        if self.instrument not in ("imager", "spectrograph", "radio_receiver"):
            errors.append(f"unknown instrument: {self.instrument}")
        valid_filters = {None, "clear", "h_alpha", "oiii", "r_band", "b_band"}
        if self.filter_band not in valid_filters:
            errors.append(f"unknown filter: {self.filter_band}")
        if not (1 <= self.exposure_time <= 3600):
            errors.append("exposure_time must be 1-3600 seconds")
        if self.scheduling_priority not in ("low", "medium", "high", "override"):
            errors.append(f"unknown priority: {self.scheduling_priority}")
        if self.scan_profile not in VALID_SCAN_PROFILES:
            errors.append(f"unknown scan_profile: {self.scan_profile}")
        return errors


@dataclass
class ObservationJob:
    """A queued observation with status tracking."""
    job_id: str
    session_id: str
    request: ObservationRequest
    status: JobStatus = JobStatus.QUEUED
    queued_at: float = 0.0
    started_at: float | None = None
    completed_at: float | None = None
    result: dict | None = None     # FITS-style result once complete
    error: str | None = None


@dataclass
class JumpJob:
    """A jump charge job."""
    job_id: str
    session_id: str
    destination_au: dict
    charge_profile: str
    charge_duration_sec: float
    status: JobStatus = JobStatus.QUEUED
    started_at: float | None = None
    charged_at: float | None = None
    completed_at: float | None = None
    result: dict | None = None


class JobQueue:
    """In-memory job queue with time-based completion."""

    # Processing time = base + per-second rate * exposure
    BASE_PROCESSING_SECS = 2.0
    PER_EXPOSURE_SEC_RATE = 0.01   # 1% of exposure time as processing overhead

    def __init__(self):
        self._jobs: dict[str, ObservationJob] = {}
        self._jump_jobs: dict[str, JumpJob] = {}
        self._by_session: dict[str, list[str]] = {}

    def submit(self, session_id: str, request: ObservationRequest) -> ObservationJob:
        job_id = str(uuid.uuid4())[:12]
        now = time.time()
        job = ObservationJob(
            job_id=job_id,
            session_id=session_id,
            request=request,
            status=JobStatus.QUEUED,
            queued_at=now,
            started_at=now,  # start immediately (single-telescope queue)
        )
        job.status = JobStatus.PROCESSING
        self._jobs[job_id] = job
        self._by_session.setdefault(session_id, []).append(job_id)
        return job

    def processing_duration(self, job: ObservationJob) -> float:
        """How long this job takes to complete in real seconds."""
        return (self.BASE_PROCESSING_SECS +
                self.PER_EXPOSURE_SEC_RATE * job.request.exposure_time)

    def is_ready(self, job: ObservationJob) -> bool:
        if job.status != JobStatus.PROCESSING or job.started_at is None:
            return False
        elapsed = time.time() - job.started_at
        return elapsed >= self.processing_duration(job)

    def get_job(self, job_id: str) -> ObservationJob | None:
        return self._jobs.get(job_id)

    def get_session_jobs(self, session_id: str) -> list[ObservationJob]:
        job_ids = self._by_session.get(session_id, [])
        return [self._jobs[jid] for jid in job_ids if jid in self._jobs]

    def complete_job(self, job_id: str, result: dict):
        job = self._jobs.get(job_id)
        if job:
            job.status = JobStatus.COMPLETED
            job.completed_at = time.time()
            job.result = result

    def fail_job(self, job_id: str, error: str):
        job = self._jobs.get(job_id)
        if job:
            job.status = JobStatus.FAILED
            job.completed_at = time.time()
            job.error = error

    # -- jump jobs -----------------------------------------------------------

    def submit_jump(self, session_id: str, destination_au: dict,
                    charge_profile: str, charge_duration_sec: float,
                    now: float) -> JumpJob:
        job_id = "jmp-" + str(uuid.uuid4())[:8]
        job = JumpJob(
            job_id=job_id,
            session_id=session_id,
            destination_au=destination_au,
            charge_profile=charge_profile,
            charge_duration_sec=charge_duration_sec,
            status=JobStatus.PROCESSING,
            started_at=now,
        )
        self._jump_jobs[job_id] = job
        return job

    def get_jump_job(self, job_id: str) -> JumpJob | None:
        return self._jump_jobs.get(job_id)

    def complete_jump(self, job_id: str, result: dict):
        job = self._jump_jobs.get(job_id)
        if job:
            job.status = JobStatus.COMPLETED
            job.completed_at = time.time()
            job.result = result
