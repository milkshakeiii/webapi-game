"""Tests for dnd.engine.dice."""

from __future__ import annotations

import random
import unittest

from dnd.engine.dice import DiceError, Roller, roll


class TestBasicRolls(unittest.TestCase):
    def test_single_d20(self):
        r = Roller(seed=1).roll("1d20")
        self.assertEqual(r.expression, "1d20")
        self.assertGreaterEqual(r.total, 1)
        self.assertLessEqual(r.total, 20)
        self.assertEqual(len(r.terms), 1)
        self.assertEqual(len(r.terms[0].rolls), 1)

    def test_multiple_dice_sum(self):
        r = Roller(seed=1).roll("2d6")
        self.assertEqual(len(r.terms[0].rolls), 2)
        self.assertEqual(r.total, sum(r.terms[0].rolls))
        self.assertGreaterEqual(r.total, 2)
        self.assertLessEqual(r.total, 12)

    def test_flat_modifier(self):
        r = Roller(seed=1).roll("1d20+5")
        self.assertEqual(len(r.terms), 2)
        self.assertEqual(r.terms[1].subtotal, 5)
        self.assertEqual(r.total, r.terms[0].subtotal + 5)

    def test_negative_modifier(self):
        r = Roller(seed=1).roll("1d20-2")
        self.assertEqual(len(r.terms), 2)
        self.assertEqual(r.terms[1].subtotal, -2)
        self.assertEqual(r.total, r.terms[0].subtotal - 2)

    def test_only_flat(self):
        r = Roller(seed=1).roll("5")
        self.assertEqual(r.total, 5)
        self.assertEqual(len(r.terms), 1)

    def test_multiple_dice_terms(self):
        r = Roller(seed=42).roll("2d6+1d8+3")
        self.assertEqual(len(r.terms), 3)
        self.assertEqual(len(r.terms[0].rolls), 2)
        self.assertEqual(len(r.terms[1].rolls), 1)
        self.assertEqual(r.terms[2].subtotal, 3)
        self.assertEqual(
            r.total,
            sum(r.terms[0].rolls) + sum(r.terms[1].rolls) + 3,
        )

    def test_subtraction_of_dice(self):
        r = Roller(seed=42).roll("1d8-1d4")
        self.assertEqual(len(r.terms), 2)
        self.assertEqual(r.terms[1].sign, -1)
        self.assertEqual(
            r.total,
            sum(r.terms[0].rolls) - sum(r.terms[1].rolls),
        )

    def test_d_uppercase(self):
        # Some folks write "1D20"; should still parse.
        r = Roller(seed=1).roll("1D20")
        self.assertEqual(len(r.terms[0].rolls), 1)


class TestKeepModifiers(unittest.TestCase):
    def test_keep_highest_3_of_4(self):
        # The standard ability score generation roll.
        r = Roller(seed=1).roll("4d6kh3")
        self.assertEqual(len(r.terms[0].rolls), 4)
        self.assertEqual(len(r.terms[0].kept), 3)
        self.assertEqual(r.total, sum(r.terms[0].kept))
        # The kept set should be the largest 3 values.
        sorted_rolls = sorted(r.terms[0].rolls, reverse=True)
        self.assertEqual(
            sorted(r.terms[0].kept, reverse=True),
            sorted_rolls[:3],
        )

    def test_keep_lowest_1(self):
        r = Roller(seed=1).roll("4d6kl1")
        self.assertEqual(len(r.terms[0].kept), 1)
        self.assertEqual(r.terms[0].kept[0], min(r.terms[0].rolls))

    def test_keep_kh_uppercase(self):
        r = Roller(seed=1).roll("4d6KH3")
        self.assertEqual(len(r.terms[0].kept), 3)


class TestDeterminism(unittest.TestCase):
    def test_same_seed_same_rolls(self):
        a = Roller(seed=42).roll("4d6kh3")
        b = Roller(seed=42).roll("4d6kh3")
        self.assertEqual(a.terms[0].rolls, b.terms[0].rolls)
        self.assertEqual(a.total, b.total)

    def test_different_seeds_diverge_in_practice(self):
        # Not strictly guaranteed for any single roll, but a sequence of
        # 6 ability rolls must differ between sensible seeds.
        seq_a = [Roller(seed=1).roll("4d6kh3").total for _ in range(6)]
        seq_b = [Roller(seed=2).roll("4d6kh3").total for _ in range(6)]
        # Wait — each call rebuilds the Roller, so seq_a and seq_b are
        # really just the *first* roll of two seeds, repeated. Use one
        # Roller instead.
        roller_a = Roller(seed=1)
        roller_b = Roller(seed=2)
        seq_a = [roller_a.roll("4d6kh3").total for _ in range(6)]
        seq_b = [roller_b.roll("4d6kh3").total for _ in range(6)]
        self.assertNotEqual(seq_a, seq_b)

    def test_external_random_passed_in(self):
        rng = random.Random(99)
        r1 = Roller(rng=rng).roll("1d20").total
        r2 = Roller(rng=rng).roll("1d20").total
        # Sharing the same Random across rollers continues the sequence.
        rng_check = random.Random(99)
        expected = [rng_check.randint(1, 20), rng_check.randint(1, 20)]
        self.assertEqual([r1, r2], expected)


class TestEdgeCases(unittest.TestCase):
    def test_d1_always_one(self):
        # 1d1 must always roll 1; useful for deterministic tests.
        for seed in range(10):
            self.assertEqual(Roller(seed=seed).roll("1d1").total, 1)

    def test_whitespace_tolerance(self):
        r = Roller(seed=1).roll("  2d6 + 3  ")
        self.assertEqual(len(r.terms), 2)
        self.assertEqual(r.terms[1].subtotal, 3)

    def test_breakdown_is_human_readable(self):
        r = Roller(seed=1).roll("1d20+5")
        # Just sanity-check structure: should mention the rolls and total.
        self.assertIn("=", r.breakdown)
        self.assertIn(str(r.total), r.breakdown)

    def test_keep_breakdown_shows_dropped(self):
        r = Roller(seed=1).roll("4d6kh3")
        self.assertIn("→keep", r.breakdown)


class TestValidation(unittest.TestCase):
    def test_empty_expression(self):
        with self.assertRaises(DiceError):
            Roller(seed=1).roll("")
        with self.assertRaises(DiceError):
            Roller(seed=1).roll("   ")

    def test_garbage_expression(self):
        with self.assertRaises(DiceError):
            Roller(seed=1).roll("hello")

    def test_zero_sides(self):
        with self.assertRaises(DiceError):
            Roller(seed=1).roll("1d0")

    def test_zero_count(self):
        with self.assertRaises(DiceError):
            Roller(seed=1).roll("0d6")

    def test_keep_more_than_rolled(self):
        with self.assertRaises(DiceError):
            Roller(seed=1).roll("3d6kh4")

    def test_keep_zero(self):
        with self.assertRaises(DiceError):
            Roller(seed=1).roll("3d6kh0")

    def test_count_too_large(self):
        with self.assertRaises(DiceError):
            Roller(seed=1).roll("100000d6")

    def test_missing_operator_between_terms(self):
        with self.assertRaises(DiceError):
            Roller(seed=1).roll("1d6 1d8")

    def test_trailing_garbage(self):
        with self.assertRaises(DiceError):
            Roller(seed=1).roll("1d6 garbage")


class TestSerialization(unittest.TestCase):
    def test_to_dict_roundtrip(self):
        r = Roller(seed=1).roll("4d6kh3+2")
        d = r.to_dict()
        self.assertEqual(d["expression"], "4d6kh3+2")
        self.assertEqual(d["total"], r.total)
        self.assertEqual(len(d["terms"]), 2)
        self.assertEqual(d["terms"][1]["flat"], 2)
        self.assertEqual(len(d["terms"][0]["rolls"]), 4)
        self.assertEqual(len(d["terms"][0]["kept"]), 3)


class TestConvenienceHelper(unittest.TestCase):
    def test_top_level_roll(self):
        r = roll("1d20", seed=1)
        a = roll("1d20", seed=1)
        self.assertEqual(r.total, a.total)


if __name__ == "__main__":
    unittest.main()
