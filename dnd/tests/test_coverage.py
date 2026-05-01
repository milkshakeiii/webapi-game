"""Coverage enforcement: every PF1 mechanic declared in content must
be classified in ``dnd/coverage.py``.

This is the safety net for "did we forget to wire X up?" If a new
monster is added with an undeclared racial trait, or a new class with
a class feature we haven't classified, this test fails. The author
must either (a) implement the mechanic and mark it IMPLEMENTED or
(b) classify it as PARTIAL / NOT_IMPLEMENTED / OUT_OF_SCOPE with a
note.

The test does NOT enforce that an entry tagged IMPLEMENTED is
actually wired in code — that's what the rest of the test suite is
for. It only enforces that the inventory is complete.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from dnd.coverage import (
    CATEGORIES,
    IMPLEMENTED,
    NOT_IMPLEMENTED,
    OUT_OF_SCOPE,
    PARTIAL,
    declared_ids,
)


CONTENT_ROOT = Path(__file__).resolve().parent.parent / "content"


# ---------------------------------------------------------------------------
# Content scanners
# ---------------------------------------------------------------------------


def _scan_monster_racial_traits() -> set[str]:
    out: set[str] = set()
    for f in sorted((CONTENT_ROOT / "monsters").glob("*.json")):
        d = json.loads(f.read_text())
        for t in d.get("racial_traits") or []:
            if isinstance(t, dict) and "id" in t:
                out.add(t["id"])
    return out


def _scan_player_race_traits() -> set[str]:
    out: set[str] = set()
    for f in sorted((CONTENT_ROOT / "races").glob("*.json")):
        d = json.loads(f.read_text())
        for t in d.get("traits") or []:
            if isinstance(t, dict) and "id" in t:
                out.add(t["id"])
    return out


def _scan_class_features_l1() -> set[str]:
    out: set[str] = set()
    for f in sorted((CONTENT_ROOT / "classes").glob("*.json")):
        d = json.loads(f.read_text())
        for t in (d.get("level_1") or {}).get("class_features") or []:
            if isinstance(t, dict) and "id" in t:
                out.add(t["id"])
    return out


def _scan_conditions() -> set[str]:
    raw = json.loads((CONTENT_ROOT / "conditions" / "conditions.json").read_text())
    items = raw.get("conditions", raw) if isinstance(raw, dict) else raw
    return {c["id"] for c in items if isinstance(c, dict) and "id" in c}


def _scan_feats() -> set[str]:
    raw = json.loads((CONTENT_ROOT / "feats" / "feats.json").read_text())
    items = raw.get("feats", raw) if isinstance(raw, dict) else raw
    return {f["id"] for f in items if isinstance(f, dict) and "id" in f}


def _scan_spell_effect_kinds() -> set[str]:
    raw = json.loads((CONTENT_ROOT / "spells" / "spells.json").read_text())
    items = raw.get("spells", raw) if isinstance(raw, dict) else raw
    out: set[str] = set()
    for s in items:
        kind = (s.get("effect") or {}).get("kind")
        if kind:
            out.add(kind)
    return out


SCANNERS = {
    "player_race_traits":    _scan_player_race_traits,
    "monster_racial_traits": _scan_monster_racial_traits,
    "class_features_l1":     _scan_class_features_l1,
    "conditions":            _scan_conditions,
    "feats":                 _scan_feats,
    "spell_effect_kinds":    _scan_spell_effect_kinds,
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestCoverageCompleteness(unittest.TestCase):
    """Every declared content ID must be classified in coverage.py."""

    def _check(self, category: str) -> None:
        scan = SCANNERS[category]
        in_content = scan()
        in_tracker = declared_ids(category)
        missing = sorted(in_content - in_tracker)
        self.assertFalse(
            missing,
            f"\n{category}: {len(missing)} content ID(s) missing from "
            f"dnd/coverage.py:\n  " + "\n  ".join(missing) + "\n\n"
            "Add an entry to coverage.py marking each as IMPLEMENTED, "
            "PARTIAL, NOT_IMPLEMENTED, or OUT_OF_SCOPE with a one-line "
            "note explaining the status.",
        )

    def test_player_race_traits(self):       self._check("player_race_traits")
    def test_monster_racial_traits(self):    self._check("monster_racial_traits")
    def test_class_features_l1(self):        self._check("class_features_l1")
    def test_conditions(self):               self._check("conditions")
    def test_feats(self):                    self._check("feats")
    def test_spell_effect_kinds(self):       self._check("spell_effect_kinds")


class TestCoverageNoStaleEntries(unittest.TestCase):
    """coverage.py shouldn't mention IDs that no longer appear in content.

    Stale entries clutter the tracker and create false confidence about
    what's "implemented." When content drops an ID, the corresponding
    coverage entry should also be removed.
    """

    def _check(self, category: str) -> None:
        scan = SCANNERS[category]
        in_content = scan()
        in_tracker = declared_ids(category)
        stale = sorted(in_tracker - in_content)
        self.assertFalse(
            stale,
            f"\n{category}: {len(stale)} entry(s) in coverage.py with no "
            f"matching content:\n  " + "\n  ".join(stale) + "\n\n"
            "Remove these from coverage.py (or restore the content if "
            "the deletion was unintended).",
        )

    def test_player_race_traits(self):       self._check("player_race_traits")
    def test_monster_racial_traits(self):    self._check("monster_racial_traits")
    def test_class_features_l1(self):        self._check("class_features_l1")
    def test_conditions(self):               self._check("conditions")
    def test_feats(self):                    self._check("feats")
    def test_spell_effect_kinds(self):       self._check("spell_effect_kinds")


class TestCoverageStatusValues(unittest.TestCase):
    """Every entry must have a recognized status value."""

    def test_all_statuses_valid(self):
        valid = {IMPLEMENTED, PARTIAL, NOT_IMPLEMENTED, OUT_OF_SCOPE}
        for cat_name, cat in CATEGORIES.items():
            for item_id, (status, note) in cat.items():
                self.assertIn(
                    status, valid,
                    f"{cat_name}.{item_id}: invalid status {status!r}",
                )
                self.assertTrue(
                    isinstance(note, str) and note.strip(),
                    f"{cat_name}.{item_id}: empty note (every entry "
                    "needs a one-line explanation)",
                )


# ---------------------------------------------------------------------------
# Visibility: a roll-up summary that humans can eyeball
# ---------------------------------------------------------------------------


class TestCoverageSummary(unittest.TestCase):
    """Print a per-category roll-up. Always passes; for human eyeballing
    when running tests verbosely."""

    def test_summary(self):
        lines = ["", "PF1 coverage roll-up:"]
        for cat_name, cat in CATEGORIES.items():
            counts = {IMPLEMENTED: 0, PARTIAL: 0, NOT_IMPLEMENTED: 0, OUT_OF_SCOPE: 0}
            for _, (status, _) in cat.items():
                counts[status] = counts.get(status, 0) + 1
            total = sum(counts.values())
            lines.append(
                f"  {cat_name:24s}  total={total:3d}  "
                f"impl={counts[IMPLEMENTED]:3d}  "
                f"partial={counts[PARTIAL]:3d}  "
                f"not_impl={counts[NOT_IMPLEMENTED]:3d}  "
                f"oos={counts[OUT_OF_SCOPE]:3d}"
            )
        # Print without failing.
        print("\n".join(lines))


if __name__ == "__main__":
    unittest.main()
