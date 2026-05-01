"""Tests for dnd.engine.sizes."""

from __future__ import annotations

import unittest

from dnd.engine.sizes import (
    SIZE_NAMES,
    SIZE_TABLE,
    get_size,
    size_modifiers,
)


class TestSizeTable(unittest.TestCase):
    def test_all_sizes_present(self):
        for name in SIZE_NAMES:
            self.assertIn(name, SIZE_TABLE)

    def test_medium_is_neutral(self):
        med = get_size("medium")
        self.assertEqual(med.ac_attack_mod, 0)
        self.assertEqual(med.cmb_cmd_mod, 0)
        self.assertEqual(med.stealth_mod, 0)
        self.assertEqual(med.footprint_squares, 1)

    def test_small_modifiers(self):
        s = get_size("small")
        self.assertEqual(s.ac_attack_mod, 1)
        self.assertEqual(s.cmb_cmd_mod, -1)
        self.assertEqual(s.stealth_mod, 4)

    def test_large_modifiers(self):
        L = get_size("large")
        self.assertEqual(L.ac_attack_mod, -1)
        self.assertEqual(L.cmb_cmd_mod, 1)
        self.assertEqual(L.stealth_mod, -4)
        self.assertEqual(L.footprint_squares, 2)
        self.assertEqual(L.natural_reach_ft_long, 5)
        self.assertEqual(L.natural_reach_ft_tall, 10)

    def test_huge_reach_squares(self):
        h = get_size("huge")
        self.assertEqual(h.reach_squares_long, 2)
        self.assertEqual(h.reach_squares_tall, 3)
        self.assertEqual(h.footprint_squares, 3)

    def test_colossal_extreme(self):
        c = get_size("colossal")
        self.assertEqual(c.ac_attack_mod, -8)
        self.assertEqual(c.cmb_cmd_mod, 8)
        self.assertEqual(c.footprint_squares, 6)
        self.assertEqual(c.natural_reach_ft_tall, 30)

    def test_unknown_size_raises(self):
        with self.assertRaises(KeyError):
            get_size("titanic")


class TestSizeModifiers(unittest.TestCase):
    def test_medium_emits_no_modifiers(self):
        self.assertEqual(size_modifiers("medium"), [])

    def test_small_emits_expected_targets(self):
        mods = size_modifiers("small")
        targets = {(m.target, m.value, m.type) for m in mods}
        self.assertIn(("ac", 1, "size"), targets)
        self.assertIn(("attack", 1, "size"), targets)
        self.assertIn(("cmb", -1, "size"), targets)
        self.assertIn(("cmd", -1, "size"), targets)
        self.assertIn(("skill:stealth", 4, "size"), targets)

    def test_large_emits_negative_ac_and_attack(self):
        mods = size_modifiers("large")
        ac_mods = [m for m in mods if m.target == "ac"]
        self.assertEqual(len(ac_mods), 1)
        self.assertEqual(ac_mods[0].value, -1)
        self.assertEqual(ac_mods[0].type, "size")

    def test_all_modifiers_tagged_size_type(self):
        for size in ("small", "large", "huge", "colossal"):
            for m in size_modifiers(size):
                self.assertEqual(m.type, "size")
                self.assertEqual(m.source, f"size:{size}")


if __name__ == "__main__":
    unittest.main()
