"""Background tick worker.

Runs ``tick(world, registry)`` once every ``world.clock.tick_interval_s``
real seconds in a daemon thread. Owns nothing the HTTP layer can see;
the only contract is "the world advances at the configured rate."

The worker also handles per-tick persistence: after each tick body
returns, it writes the world map and any changed castles/deployments
to disk. Persistence is best-effort — if disk is wedged, we skip and
keep the in-memory simulation running.
"""

from __future__ import annotations

import threading
import time
import traceback

from dnd.engine.content import ContentRegistry

from .boot import save_world
from .castle import save_castle
from .deployment import save_deployment
from .tick import tick
from .world import World


class TickWorker:
    """Daemon-thread tick driver."""

    def __init__(
        self,
        world: World,
        registry: ContentRegistry,
        *,
        persist: bool = True,
    ) -> None:
        self.world = world
        self.registry = registry
        self.persist = persist
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._tick_count = 0
        self._error_count = 0

    # ── Lifecycle ────────────────────────────────────────────────────────

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._run, name="dnd-tick-worker", daemon=True,
        )
        self._thread.start()

    def stop(self, timeout: float = 5.0) -> None:
        """Signal stop and wait briefly for the thread to exit."""
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=timeout)
            self._thread = None

    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    @property
    def tick_count(self) -> int:
        return self._tick_count

    @property
    def error_count(self) -> int:
        return self._error_count

    # ── Internals ────────────────────────────────────────────────────────

    def _run(self) -> None:
        interval = self.world.clock.tick_interval_s
        # The clock can't realistically be < ~10ms in dev; clamp here so
        # a misconfigured TICK_INTERVAL doesn't spin a CPU.
        if interval <= 0:
            interval = 0.05
        while not self._stop.is_set():
            started = time.monotonic()
            try:
                tick(self.world, self.registry)
                self._tick_count += 1
                if self.persist:
                    self._persist()
            except Exception:
                self._error_count += 1
                # Don't kill the worker on a single bad tick. Print and
                # carry on so the loop self-recovers if state is fine
                # next tick.
                traceback.print_exc()
            elapsed = time.monotonic() - started
            sleep_for = max(0.0, interval - elapsed)
            # Wait on the stop event so shutdown is responsive.
            if self._stop.wait(timeout=sleep_for):
                return

    def _persist(self) -> None:
        """Write world + castles + deployments to disk."""
        try:
            save_world(self.world)
        except Exception:
            traceback.print_exc()
        for castle in self.world.castles.values():
            try:
                save_castle(castle)
            except Exception:
                traceback.print_exc()
        for deployment in self.world.deployments.values():
            try:
                save_deployment(deployment)
            except Exception:
                traceback.print_exc()
