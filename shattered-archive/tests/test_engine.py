"""Tests for the synthesis engine with symbolic thread names."""

import sys
import unittest
from pathlib import Path

# Ensure project root is importable.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import AttemptResult, evaluate_attempt
from simulator import load_puzzle

LANTERN = load_puzzle(Path(__file__).resolve().parent.parent / "examples" / "lantern_puzzle.json")


class TestLanternKnownSolution(unittest.TestCase):
    """The API spec documents a known 6-step solution with score 646."""

    def test_known_best_solution(self):
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "add", "reagent_id": "catalogue_oil", "as": "b"},
            {"op": "add", "reagent_id": "mirror_dust", "as": "c"},
            {"op": "bind", "left": "a", "right": "b", "into": "ab", "bonus_essence": "echo"},
            {"op": "bind", "left": "ab", "right": "c", "into": "core", "bonus_essence": "lumen"},
            {"op": "distill", "thread": "core", "essence": "lumen"},
        ]
        result = evaluate_attempt(LANTERN, actions)
        self.assertEqual(result.resolution, "success")
        self.assertIsNotNone(result.summary)
        self.assertTrue(result.summary["contract_satisfied"])
        self.assertEqual(result.summary["steps_used"], 6)
        self.assertEqual(result.summary["score"], 646)
        self.assertEqual(len(result.trace), 6)

        final = result.summary["final_thread"]
        self.assertEqual(final["essences"]["lumen"], 6)
        self.assertEqual(final["essences"]["echo"], 4)
        self.assertEqual(final["fray"], 1)
        self.assertIn("relic", final["tags"])

    def test_trace_structure(self):
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
        ]
        result = evaluate_attempt(LANTERN, actions)
        # One step only, won't satisfy contract.
        self.assertEqual(result.resolution, "failure")
        self.assertEqual(len(result.trace), 1)
        step = result.trace[0]
        self.assertEqual(step["step"], 1)
        self.assertEqual(step["outcome"], "ok")
        self.assertIn("a", step["live_threads"])
        self.assertEqual(step["remaining_reagents"]["archive_dust"], 0)


class TestAddAction(unittest.TestCase):
    def test_unknown_reagent(self):
        actions = [{"op": "add", "reagent_id": "nonexistent", "as": "a"}]
        result = evaluate_attempt(LANTERN, actions)
        self.assertEqual(result.resolution, "invalid")
        self.assertEqual(result.failed_step, 1)
        self.assertEqual(result.error["code"], "unknown_reagent")

    def test_duplicate_name(self):
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "add", "reagent_id": "catalogue_oil", "as": "a"},
        ]
        result = evaluate_attempt(LANTERN, actions)
        self.assertEqual(result.resolution, "invalid")
        self.assertEqual(result.failed_step, 2)
        self.assertEqual(result.error["code"], "duplicate_thread_name")

    def test_bench_full(self):
        # Bench capacity is 3.
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "add", "reagent_id": "catalogue_oil", "as": "b"},
            {"op": "add", "reagent_id": "mirror_dust", "as": "c"},
            {"op": "add", "reagent_id": "brass_filament", "as": "d"},
        ]
        result = evaluate_attempt(LANTERN, actions)
        self.assertEqual(result.resolution, "invalid")
        self.assertEqual(result.failed_step, 4)
        self.assertEqual(result.error["code"], "bench_full")

    def test_reagent_exhausted(self):
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "bind", "left": "a", "right": "a", "into": "x"},
        ]
        result = evaluate_attempt(LANTERN, actions)
        # "a" and "a" are the same name — invalid bind.
        self.assertEqual(result.resolution, "invalid")


class TestBindAction(unittest.TestCase):
    def test_unstable_bind_adds_fray(self):
        # archive_dust (ink) + sunleaf (botanic) — no shared tag.
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "add", "reagent_id": "sunleaf", "as": "b"},
            {"op": "bind", "left": "a", "right": "b", "into": "ab"},
        ]
        result = evaluate_attempt(LANTERN, actions)
        # Should succeed as an action, but final thread has +2 fray.
        self.assertEqual(result.resolution, "failure")
        step3 = result.trace[2]
        ab = step3["live_threads"]["ab"]
        self.assertEqual(ab["fray"], 2)

    def test_stable_bind_no_bonus(self):
        # archive_dust (ink) + catalogue_oil (ink, relic) — shared tag "ink".
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "add", "reagent_id": "catalogue_oil", "as": "b"},
            {"op": "bind", "left": "a", "right": "b", "into": "ab"},
        ]
        result = evaluate_attempt(LANTERN, actions)
        step3 = result.trace[2]
        ab = step3["live_threads"]["ab"]
        self.assertEqual(ab["fray"], 0)
        # Essences: archive(1,2,0,0) + catalogue(0,1,1,0) = (1,3,1,0)
        self.assertEqual(ab["essences"]["lumen"], 1)
        self.assertEqual(ab["essences"]["echo"], 3)

    def test_bonus_on_unstable_bind_rejected(self):
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "add", "reagent_id": "sunleaf", "as": "b"},
            {"op": "bind", "left": "a", "right": "b", "into": "ab", "bonus_essence": "lumen"},
        ]
        result = evaluate_attempt(LANTERN, actions)
        self.assertEqual(result.resolution, "invalid")
        self.assertEqual(result.error["code"], "invalid_bonus")

    def test_retired_thread_cannot_be_reused(self):
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "add", "reagent_id": "catalogue_oil", "as": "b"},
            {"op": "bind", "left": "a", "right": "b", "into": "ab"},
            {"op": "distill", "thread": "a", "essence": "lumen"},
        ]
        result = evaluate_attempt(LANTERN, actions)
        self.assertEqual(result.resolution, "invalid")
        self.assertEqual(result.failed_step, 4)
        self.assertEqual(result.error["code"], "undefined_thread")


class TestDistillAction(unittest.TestCase):
    def test_distill_arithmetic(self):
        # archive_dust: lumen=1, echo=2, motive=0, veil=0
        # distill lumen: +2 lumen, -1 echo (above 0), motive stays 0, veil stays 0, +1 fray
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "distill", "thread": "a", "essence": "lumen"},
        ]
        result = evaluate_attempt(LANTERN, actions)
        step2 = result.trace[1]
        a = step2["live_threads"]["a"]
        self.assertEqual(a["essences"]["lumen"], 3)
        self.assertEqual(a["essences"]["echo"], 1)
        self.assertEqual(a["fray"], 1)


class TestReweaveAction(unittest.TestCase):
    def test_basic_reweave(self):
        # archive_dust: lumen=1, echo=2
        # reweave echo -> lumen, amount 1: lumen=2, echo=1, fray=+1
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "reweave", "thread": "a", "from_essence": "echo", "to_essence": "lumen", "amount": 1},
        ]
        result = evaluate_attempt(LANTERN, actions)
        step2 = result.trace[1]
        a = step2["live_threads"]["a"]
        self.assertEqual(a["essences"]["lumen"], 2)
        self.assertEqual(a["essences"]["echo"], 1)
        self.assertEqual(a["fray"], 1)

    def test_opposed_reweave_extra_fray(self):
        # echo -> motive is an opposed pair
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "reweave", "thread": "a", "from_essence": "echo", "to_essence": "motive", "amount": 1},
        ]
        result = evaluate_attempt(LANTERN, actions)
        step2 = result.trace[1]
        a = step2["live_threads"]["a"]
        self.assertEqual(a["fray"], 2)  # opposed: +2 fray

    def test_insufficient_source(self):
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "reweave", "thread": "a", "from_essence": "motive", "to_essence": "lumen", "amount": 1},
        ]
        result = evaluate_attempt(LANTERN, actions)
        self.assertEqual(result.resolution, "invalid")
        self.assertEqual(result.error["code"], "insufficient_essence")


class TestStabilizeAction(unittest.TestCase):
    def test_stabilize(self):
        # Distill to get fray, then stabilize.
        # archive_dust: L1 E2 M0 V0
        # distill lumen: L3 E1 M0 V0 fray=1
        # stabilize reduce=lumen: L2 E1 M0 V0 fray=0
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "distill", "thread": "a", "essence": "lumen"},
            {"op": "stabilize", "thread": "a", "reduce_essence": "lumen"},
        ]
        result = evaluate_attempt(LANTERN, actions)
        step3 = result.trace[2]
        a = step3["live_threads"]["a"]
        self.assertEqual(a["essences"]["lumen"], 2)
        self.assertEqual(a["fray"], 0)

    def test_zero_fray_rejected(self):
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "stabilize", "thread": "a", "reduce_essence": "echo"},
        ]
        result = evaluate_attempt(LANTERN, actions)
        self.assertEqual(result.resolution, "invalid")
        self.assertEqual(result.error["code"], "zero_fray")

    def test_not_highest_rejected(self):
        # archive_dust: L1 E2 M0 V0
        # distill lumen: L3 E1 M0 V0 fray=1 — highest is lumen (3)
        # stabilize reduce=echo should fail (echo=1 is not highest)
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "distill", "thread": "a", "essence": "lumen"},
            {"op": "stabilize", "thread": "a", "reduce_essence": "echo"},
        ]
        result = evaluate_attempt(LANTERN, actions)
        self.assertEqual(result.resolution, "invalid")
        self.assertEqual(result.error["code"], "not_highest_essence")


class TestContractViolations(unittest.TestCase):
    def test_minimum_not_met(self):
        # Single reagent won't satisfy contract minimums.
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
        ]
        result = evaluate_attempt(LANTERN, actions)
        self.assertEqual(result.resolution, "failure")
        codes = [v["code"] for v in result.summary["violations"]]
        self.assertIn("minimum_essence_not_met", codes)

    def test_required_tag_missing(self):
        # sunleaf has tag "botanic", not "relic".
        actions = [
            {"op": "add", "reagent_id": "sunleaf", "as": "a"},
        ]
        result = evaluate_attempt(LANTERN, actions)
        self.assertEqual(result.resolution, "failure")
        codes = [v["code"] for v in result.summary["violations"]]
        self.assertIn("required_tag_missing", codes)


class TestStepLimit(unittest.TestCase):
    def test_exceeding_step_limit(self):
        # Lantern step limit is 6.  Try 7 adds (some will fail due to bench, but
        # we can alternate add+distill).
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "distill", "thread": "a", "essence": "lumen"},
            {"op": "distill", "thread": "a", "essence": "lumen"},
            {"op": "distill", "thread": "a", "essence": "lumen"},
            {"op": "distill", "thread": "a", "essence": "lumen"},
            {"op": "distill", "thread": "a", "essence": "lumen"},
            {"op": "distill", "thread": "a", "essence": "lumen"},  # 7th action
        ]
        result = evaluate_attempt(LANTERN, actions)
        self.assertEqual(result.resolution, "invalid")
        self.assertEqual(result.failed_step, 7)
        self.assertEqual(result.error["code"], "step_limit_exceeded")


class TestWrongThreadCount(unittest.TestCase):
    def test_two_threads_remaining(self):
        actions = [
            {"op": "add", "reagent_id": "archive_dust", "as": "a"},
            {"op": "add", "reagent_id": "catalogue_oil", "as": "b"},
        ]
        result = evaluate_attempt(LANTERN, actions)
        self.assertEqual(result.resolution, "failure")
        codes = [v["code"] for v in result.summary["violations"]]
        self.assertIn("wrong_thread_count", codes)


if __name__ == "__main__":
    unittest.main()
