"""Tests for sandbox storage helpers."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from dnd.sandbox.storage import (
    append_jsonl,
    data_root,
    ensure_dir,
    read_json,
    read_jsonl,
    write_json_atomic,
)


class TestPathHelpers(unittest.TestCase):
    def test_data_root_from_env(self):
        os.environ["DND_DATA_DIR"] = "/tmp/dnd_test_xyz"
        try:
            self.assertEqual(data_root(), Path("/tmp/dnd_test_xyz"))
        finally:
            del os.environ["DND_DATA_DIR"]

    def test_data_root_default_under_repo(self):
        # No env var set: should land under the repo root, ending in "data".
        os.environ.pop("DND_DATA_DIR", None)
        root = data_root()
        self.assertEqual(root.name, "data")

    def test_ensure_dir_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "a" / "b" / "c"
            ensure_dir(p)
            self.assertTrue(p.exists())
            ensure_dir(p)  # second call is fine
            self.assertTrue(p.exists())


class TestReadWriteJson(unittest.TestCase):
    def test_round_trip_simple(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.json"
            write_json_atomic(p, {"a": 1, "b": [1, 2, 3]})
            self.assertEqual(read_json(p), {"a": 1, "b": [1, 2, 3]})

    def test_read_missing_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(read_json(Path(tmp) / "nope.json"))

    def test_write_creates_parent_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "deep" / "nested" / "x.json"
            write_json_atomic(p, {"hello": "world"})
            self.assertEqual(read_json(p), {"hello": "world"})

    def test_atomic_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.json"
            write_json_atomic(p, {"v": 1})
            write_json_atomic(p, {"v": 2})
            self.assertEqual(read_json(p), {"v": 2})

    def test_set_serialized_as_sorted_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.json"
            write_json_atomic(p, {"tags": {"b", "a", "c"}})
            self.assertEqual(read_json(p), {"tags": ["a", "b", "c"]})

    def test_dataclass_via_to_dict(self):
        from dataclasses import dataclass

        @dataclass
        class Thing:
            x: int
            def to_dict(self):
                return {"x": self.x}

        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.json"
            write_json_atomic(p, Thing(x=42))
            self.assertEqual(read_json(p), {"x": 42})

    def test_unserializable_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.json"
            class Naked: pass
            with self.assertRaises(TypeError):
                write_json_atomic(p, {"k": Naked()})

    def test_no_tempfile_left_behind_on_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.json"
            write_json_atomic(p, {"k": 1})
            # The directory should contain only the target file.
            entries = list(Path(tmp).iterdir())
            self.assertEqual([e.name for e in entries], ["x.json"])

    def test_tempfile_cleaned_up_on_serialization_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.json"
            class Naked: pass
            with self.assertRaises(TypeError):
                write_json_atomic(p, {"k": Naked()})
            # No tempfile should be left in the directory.
            entries = list(Path(tmp).iterdir())
            self.assertEqual(entries, [])


class TestAppendJsonl(unittest.TestCase):
    def test_append_then_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "log.jsonl"
            append_jsonl(p, {"event": "a", "n": 1})
            append_jsonl(p, {"event": "b", "n": 2})
            self.assertEqual(read_jsonl(p), [
                {"event": "a", "n": 1},
                {"event": "b", "n": 2},
            ])

    def test_read_missing_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(read_jsonl(Path(tmp) / "missing.jsonl"), [])

    def test_blank_lines_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "log.jsonl"
            append_jsonl(p, {"a": 1})
            with p.open("a") as f:
                f.write("\n\n  \n")
            append_jsonl(p, {"a": 2})
            self.assertEqual(read_jsonl(p), [{"a": 1}, {"a": 2}])


if __name__ == "__main__":
    unittest.main()
