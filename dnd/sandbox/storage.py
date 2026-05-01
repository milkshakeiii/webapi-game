"""Atomic JSON-on-disk persistence helpers.

Every write goes to a sibling tempfile and is moved into place with
``os.replace``. That gives us:

- atomicity: a reader either sees the old file or the new one, never
  a partial write;
- crash safety: a partially-written tempfile is just garbage to clean
  up next boot, not a corrupt save.

Reads are best-effort: if the file is missing, the caller gets
``None`` and decides whether that's fatal.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def data_root() -> Path:
    """Root of the writable data directory.

    Honors ``DND_DATA_DIR`` if set so test runs can use a temp dir.
    Defaults to ``./data`` relative to the project root.
    """
    env = os.environ.get("DND_DATA_DIR")
    if env:
        return Path(env)
    here = Path(__file__).resolve()
    # dnd/sandbox/storage.py → repo root is two parents up.
    return here.parent.parent.parent / "data"


def ensure_dir(p: Path) -> None:
    """Create the directory if missing. Idempotent."""
    p.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Read / write
# ---------------------------------------------------------------------------


def read_json(path: Path) -> Any | None:
    """Read JSON from ``path`` or return ``None`` if the file is missing."""
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def write_json_atomic(path: Path, data: Any) -> None:
    """Write ``data`` as JSON to ``path`` atomically.

    Writes to a tempfile in the same directory (so ``os.replace`` is
    a same-filesystem rename), fsyncs, then renames over the target.
    """
    ensure_dir(path.parent)
    fd, tmp_path = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=str(path.parent),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True, default=_default)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except Exception:
        # Best-effort cleanup of the tempfile on failure.
        try:
            os.unlink(tmp_path)
        except FileNotFoundError:
            pass
        raise


def _default(obj):
    """JSON encoder fallback: dataclasses, sets, paths, datetimes."""
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if isinstance(obj, (set, frozenset)):
        return sorted(obj)
    if isinstance(obj, Path):
        return str(obj)
    # datetime / date — emit ISO 8601.
    iso = getattr(obj, "isoformat", None)
    if callable(iso):
        return iso()
    raise TypeError(f"object of type {type(obj).__name__} is not JSON serializable")


# ---------------------------------------------------------------------------
# Append-only event log (one line of JSON per event)
# ---------------------------------------------------------------------------


def append_jsonl(path: Path, record: Any) -> None:
    """Append a single JSON record (one line) to ``path``.

    Used for daily event logs that grow indefinitely. Not atomic
    against concurrent writers — caller must serialize externally
    (the tick worker is the sole writer for sandbox event logs).
    """
    ensure_dir(path.parent)
    line = json.dumps(record, default=_default)
    with path.open("a", encoding="utf-8") as f:
        f.write(line)
        f.write("\n")


def read_jsonl(path: Path) -> list[Any]:
    """Read all records from a JSONL file. Empty list if missing."""
    try:
        out: list[Any] = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                out.append(json.loads(line))
        return out
    except FileNotFoundError:
        return []
