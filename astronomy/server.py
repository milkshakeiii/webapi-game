"""HTTP server for the astronomy observation game."""

import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

from .sessions import SessionStore
from .jobs import ObservationRequest, JobStatus

store = SessionStore()

# ---------------------------------------------------------------------------
# Routing helpers
# ---------------------------------------------------------------------------

_routes = {"GET": [], "POST": []}


def route(method, pattern):
    regex = re.compile("^" + pattern + "$")
    def decorator(fn):
        _routes[method].append((regex, fn))
        return fn
    return decorator


def match_route(method, path):
    for regex, handler in _routes.get(method, []):
        m = regex.match(path)
        if m:
            return handler, m.groupdict()
    return None, {}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

# -- sessions ----------------------------------------------------------------

@route("POST", r"/v1/sessions")
def create_session(body, **kw):
    session = store.create_session()
    return 201, store.session_to_dict(session)


@route("GET", r"/v1/sessions/(?P<session_id>[^/]+)")
def get_session(body, session_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}
    return 200, store.session_to_dict(session)


# -- observations (RTML-style submission) ------------------------------------

@route("POST", r"/v1/sessions/(?P<session_id>[^/]+)/observations")
def submit_observation(body, session_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}

    # Parse RTML-style request
    try:
        target = body.get("target", {})
        request = ObservationRequest(
            target_ra=float(target.get("ra", 0)),
            target_dec=float(target.get("dec", 0)),
            instrument=body.get("instrument", "imager"),
            filter_band=body.get("filter", None),
            exposure_time=float(body.get("exposure_time", 60)),
            scheduling_priority=body.get("scheduling", {}).get("priority", "medium"),
        )
        job = store.submit_observation(session_id, request)
    except (ValueError, TypeError, KeyError) as e:
        return 400, {"error": str(e)}

    return 202, {
        "job_id": job.job_id,
        "status": job.status.value,
        "estimated_completion_secs": round(store.job_queue.processing_duration(job), 2),
        "request": {
            "target": {"ra": request.target_ra, "dec": request.target_dec},
            "instrument": request.instrument,
            "filter": request.filter_band,
            "exposure_time": request.exposure_time,
            "scheduling": {"priority": request.scheduling_priority},
        },
    }


@route("GET", r"/v1/sessions/(?P<session_id>[^/]+)/observations/(?P<job_id>[^/]+)")
def get_observation(body, session_id, job_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}

    job = store.check_job(session_id, job_id)
    if job is None:
        return 404, {"error": "observation not found"}

    result = {
        "job_id": job.job_id,
        "status": job.status.value,
    }

    if job.status == JobStatus.PROCESSING:
        import time
        elapsed = time.time() - (job.started_at or job.queued_at)
        duration = store.job_queue.processing_duration(job)
        result["progress"] = min(1.0, round(elapsed / duration, 2))
        result["retry_after_secs"] = round(max(0, duration - elapsed), 2)
    elif job.status == JobStatus.COMPLETED:
        result["result"] = job.result  # FITS-style headers + data
    elif job.status == JobStatus.FAILED:
        result["error"] = job.error

    return 200, result


@route("GET", r"/v1/sessions/(?P<session_id>[^/]+)/observations")
def list_observations(body, session_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}

    jobs = store.list_jobs(session_id)
    return 200, {
        "observations": [
            {
                "job_id": j.job_id,
                "status": j.status.value,
                "instrument": j.request.instrument,
                "target": {"ra": j.request.target_ra, "dec": j.request.target_dec},
                "exposure_time": j.request.exposure_time,
                "has_result": j.result is not None,
            }
            for j in jobs
        ],
    }


# -- transmit ----------------------------------------------------------------

@route("POST", r"/v1/sessions/(?P<session_id>[^/]+)/transmit")
def transmit(body, session_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}
    try:
        power = float(body.get("power", 1.0))
        result = store.transmit(session_id, power)
    except (ValueError, TypeError) as e:
        return 400, {"error": str(e)}
    return 200, result


# -- sky catalogue (reference) -----------------------------------------------

@route("GET", r"/v1/catalogue")
def get_catalogue(body):
    """Public catalogue — what a real observatory would publish."""
    return 200, {
        "objects": [
            {
                "id": obj.id,
                "name": obj.name,
                "kind": obj.kind,
                "ra": obj.ra,
                "dec": obj.dec,
                "description": obj.description,
            }
            for obj in store.sky.objects
        ],
    }


# ---------------------------------------------------------------------------
# Request handler
# ---------------------------------------------------------------------------

class GameHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self._handle("GET")

    def do_POST(self):
        self._handle("POST")

    def _handle(self, method):
        handler, kwargs = match_route(method, self.path.split("?")[0])
        if handler is None:
            self._respond(404, {"error": "not found"})
            return

        body = {}
        if method == "POST":
            length = int(self.headers.get("Content-Length", 0))
            if length:
                try:
                    body = json.loads(self.rfile.read(length))
                except json.JSONDecodeError:
                    self._respond(400, {"error": "invalid JSON"})
                    return

        try:
            status, data = handler(body, **kwargs)
        except Exception as e:
            self._respond(500, {"error": str(e)})
            return

        self._respond(status, data)

    def _respond(self, status, data):
        body = json.dumps(data, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[astronomy] {args[0]}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(port=8080):
    server = HTTPServer(("", port), GameHandler)
    print(f"Astronomy game server running on http://localhost:{port}")
    print(f"  POST /v1/sessions              - create a telescope session")
    print(f"  POST /v1/sessions/{{id}}/observations - submit observation (RTML-style)")
    print(f"  GET  /v1/sessions/{{id}}/observations/{{job}} - get results (FITS-style)")
    print(f"  GET  /v1/catalogue             - browse the sky catalogue")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
