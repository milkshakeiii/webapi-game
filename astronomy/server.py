"""HTTP server for the astronomy observation game."""

import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

from .sessions import SessionStore
from .jobs import ObservationRequest, JobStatus
from .regions import REGIONS

store = SessionStore()

# ---------------------------------------------------------------------------
# Routing helpers
# ---------------------------------------------------------------------------

_routes = {"GET": [], "POST": [], "DELETE": []}


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

    try:
        target = body.get("target", {})
        request = ObservationRequest(
            target_ra=float(target.get("ra", 0)),
            target_dec=float(target.get("dec", 0)),
            instrument=body.get("instrument", "imager"),
            filter_band=body.get("filter", None),
            exposure_time=float(body.get("exposure_time", 60)),
            scheduling_priority=body.get("scheduling", {}).get("priority", "medium"),
            scan_profile=body.get("scan_profile", "survey"),
            active_module=body.get("active_module", None),
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
            "scan_profile": request.scan_profile,
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
        result["result"] = job.result
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
                "scan_profile": j.request.scan_profile,
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


# -- radiator control --------------------------------------------------------

@route("POST", r"/v1/sessions/(?P<session_id>[^/]+)/radiators")
def set_radiators(body, session_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}
    try:
        mode = body.get("mode", "balanced")
        result = store.set_radiator_mode(session_id, mode)
    except (ValueError, TypeError) as e:
        return 400, {"error": str(e)}
    return 200, result


# -- uplink (science cash-out + hunting reports) -----------------------------

@route("POST", r"/v1/sessions/(?P<session_id>[^/]+)/uplink")
def uplink(body, session_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}
    try:
        result = store.uplink(session_id, body)
    except (ValueError, TypeError) as e:
        return 400, {"error": str(e)}
    return 200, result


# -- jump mechanics ----------------------------------------------------------

@route("POST", r"/v1/sessions/(?P<session_id>[^/]+)/jump")
def start_jump(body, session_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}
    try:
        destination = body.get("destination_au", {})
        if not all(k in destination for k in ("x", "y", "z")):
            return 400, {"error": "destination_au must have x, y, z"}
        dest = {
            "x": float(destination["x"]),
            "y": float(destination["y"]),
            "z": float(destination["z"]),
        }
        profile = body.get("charge_profile", "standard")
        result = store.start_jump(session_id, dest, profile)
    except (ValueError, TypeError) as e:
        return 400, {"error": str(e)}
    return 202, result


@route("GET", r"/v1/sessions/(?P<session_id>[^/]+)/jump/(?P<job_id>[^/]+)")
def get_jump(body, session_id, job_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}
    result = store.check_jump(session_id, job_id)
    if result is None:
        return 404, {"error": "jump job not found"}
    return 200, result


@route("POST", r"/v1/sessions/(?P<session_id>[^/]+)/jump/(?P<job_id>[^/]+)/commit")
def commit_jump(body, session_id, job_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}
    try:
        result = store.commit_jump(session_id, job_id)
    except (ValueError, TypeError) as e:
        return 400, {"error": str(e)}
    return 200, result


@route("DELETE", r"/v1/sessions/(?P<session_id>[^/]+)/jump/(?P<job_id>[^/]+)")
def abort_jump(body, session_id, job_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}
    try:
        result = store.abort_jump(session_id, job_id)
    except (ValueError, TypeError) as e:
        return 400, {"error": str(e)}
    return 200, result


# -- track files -------------------------------------------------------------

@route("GET", r"/v1/sessions/(?P<session_id>[^/]+)/track-files")
def list_tracks(body, session_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}
    tracks = store.track_manager.get_session_tracks(session_id)
    return 200, {
        "tracks": [store.track_manager.track_to_dict(t) for t in tracks],
    }


# -- jam ---------------------------------------------------------------------

@route("POST", r"/v1/sessions/(?P<session_id>[^/]+)/jam")
def jam(body, session_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}
    try:
        target_ra = float(body.get("target_ra", 0))
        target_dec = float(body.get("target_dec", 0))
        result = store.jam(session_id, target_ra, target_dec)
    except (ValueError, TypeError) as e:
        return 400, {"error": str(e)}
    return 200, result


# -- wideband ping -----------------------------------------------------------

@route("POST", r"/v1/sessions/(?P<session_id>[^/]+)/ping")
def wideband_ping(body, session_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}
    try:
        result = store.wideband_ping(session_id)
    except (ValueError, TypeError) as e:
        return 400, {"error": str(e)}
    return 200, result


# -- burst uplink ------------------------------------------------------------

@route("POST", r"/v1/sessions/(?P<session_id>[^/]+)/burst-uplink")
def burst_uplink(body, session_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}
    try:
        result = store.burst_uplink(session_id)
    except (ValueError, TypeError) as e:
        return 400, {"error": str(e)}
    return 200, result


# -- decoy -------------------------------------------------------------------

@route("POST", r"/v1/sessions/(?P<session_id>[^/]+)/decoy")
def deploy_decoy(body, session_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}
    try:
        result = store.deploy_decoy(session_id)
    except (ValueError, TypeError) as e:
        return 400, {"error": str(e)}
    return 200, result


# -- loadout -----------------------------------------------------------------

@route("POST", r"/v1/sessions/(?P<session_id>[^/]+)/loadout")
def set_loadout(body, session_id):
    session = store.get_session(session_id)
    if session is None:
        return 404, {"error": "session not found"}
    try:
        passive = body.get("passive_modules", [])
        active = body.get("active_modules", [])
        result = store.set_loadout(session_id, passive, active)
    except (ValueError, TypeError) as e:
        return 400, {"error": str(e)}
    return 200, result


# -- system info -------------------------------------------------------------

@route("GET", r"/v1/system/regions")
def get_regions(body):
    return 200, {
        "regions": [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "ir_background": r.ir_background,
                "radio_noise": r.radio_noise,
                "dust_opacity": r.dust_opacity,
                "solar_flux": r.solar_flux,
                "relay_coverage": r.relay_coverage,
                "center_au": r.center_au,
                "radius_au": r.radius_au,
            }
            for r in REGIONS
        ],
    }


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

    def do_DELETE(self):
        self._handle("DELETE")

    def _handle(self, method):
        handler, kwargs = match_route(method, self.path.split("?")[0])
        if handler is None:
            self._respond(404, {"error": "not found"})
            return

        body = {}
        if method in ("POST", "DELETE"):
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
    print()
    print("  Sessions & state:")
    print(f"    POST /v1/sessions                         - create a telescope session")
    print(f"    GET  /v1/sessions/{{id}}                    - get session state")
    print()
    print("  Observations:")
    print(f"    POST /v1/sessions/{{id}}/observations       - submit observation (RTML)")
    print(f"    GET  /v1/sessions/{{id}}/observations/{{job}} - get results (FITS)")
    print(f"    GET  /v1/sessions/{{id}}/observations        - list all observations")
    print()
    print("  Actions:")
    print(f"    POST /v1/sessions/{{id}}/uplink              - bank data or hunt report")
    print(f"    POST /v1/sessions/{{id}}/radiators           - set radiator mode")
    print(f"    POST /v1/sessions/{{id}}/loadout             - equip modules")
    print(f"    POST /v1/sessions/{{id}}/transmit            - broadcast signal")
    print(f"    POST /v1/sessions/{{id}}/jam                 - activate jammer")
    print()
    print("  Movement:")
    print(f"    POST /v1/sessions/{{id}}/jump                - start jump charge")
    print(f"    GET  /v1/sessions/{{id}}/jump/{{job}}          - check jump status")
    print(f"    POST /v1/sessions/{{id}}/jump/{{job}}/commit   - commit jump")
    print(f"    DEL  /v1/sessions/{{id}}/jump/{{job}}          - abort jump")
    print()
    print("  Info:")
    print(f"    GET  /v1/system/regions                    - list solar system regions")
    print(f"    GET  /v1/sessions/{{id}}/track-files         - list track files")
    print(f"    GET  /v1/catalogue                         - browse sky catalogue")
    print()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
