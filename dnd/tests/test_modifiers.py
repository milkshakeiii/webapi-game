"""Tests for dnd.engine.modifiers."""

from __future__ import annotations

import unittest

from dnd.engine.modifiers import (
    Modifier,
    ModifierCollection,
    STACKING_TYPES,
    compute,
    compute_with_breakdown,
    mod,
    stat_report,
    with_target,
)


# ---------------------------------------------------------------------------
# compute() — non-stacking (highest of each polarity)
# ---------------------------------------------------------------------------


class TestComputeNonStacking(unittest.TestCase):
    def test_single_modifier(self):
        m = mod(2, "armor", "ac", "leather_armor")
        self.assertEqual(compute(10, [m]), 12)

    def test_two_same_type_take_highest(self):
        # +2 armor (leather) + +4 armor (mage_armor): only +4 applies.
        a = mod(2, "armor", "ac", "leather_armor")
        b = mod(4, "armor", "ac", "mage_armor")
        self.assertEqual(compute(10, [a, b]), 14)

    def test_different_types_both_apply(self):
        # +4 armor + +2 shield = +6
        a = mod(4, "armor", "ac", "mage_armor")
        b = mod(2, "shield", "ac", "shield_spell")
        self.assertEqual(compute(10, [a, b]), 16)

    def test_bonus_and_penalty_same_type_net(self):
        # +4 morale bonus + -2 morale penalty = +2 net
        a = mod(4, "morale", "ac", "heroism")
        b = mod(-2, "morale", "ac", "frightened")
        self.assertEqual(compute(10, [a, b]), 12)

    def test_two_penalties_take_worst(self):
        a = mod(-2, "morale", "ac", "shaken")
        b = mod(-3, "morale", "ac", "doomed")
        self.assertEqual(compute(10, [a, b]), 7)


# ---------------------------------------------------------------------------
# compute() — stacking (dodge, circumstance, untyped sum)
# ---------------------------------------------------------------------------


class TestComputeStacking(unittest.TestCase):
    def test_dodge_stacks(self):
        a = mod(1, "dodge", "ac", "dodge_feat")
        b = mod(1, "dodge", "ac", "mobility")
        self.assertEqual(compute(10, [a, b]), 12)

    def test_circumstance_stacks(self):
        a = mod(2, "circumstance", "attack", "high_ground")
        b = mod(2, "circumstance", "attack", "flanking_help")
        self.assertEqual(compute(0, [a, b]), 4)

    def test_untyped_stacks(self):
        a = mod(1, "untyped", "skill:stealth", "racial_a")
        b = mod(1, "untyped", "skill:stealth", "racial_b")
        self.assertEqual(compute(0, [a, b]), 2)

    def test_stacking_types_constant(self):
        # Sanity check on the STACKING_TYPES set.
        self.assertIn("dodge", STACKING_TYPES)
        self.assertIn("circumstance", STACKING_TYPES)
        self.assertIn("untyped", STACKING_TYPES)
        self.assertNotIn("armor", STACKING_TYPES)
        self.assertNotIn("morale", STACKING_TYPES)


# ---------------------------------------------------------------------------
# compute_with_breakdown
# ---------------------------------------------------------------------------


class TestBreakdown(unittest.TestCase):
    def test_breakdown_includes_suppressed(self):
        a = mod(2, "armor", "ac", "leather_armor")
        b = mod(4, "armor", "ac", "mage_armor")
        total, bds = compute_with_breakdown(10, [a, b])
        self.assertEqual(total, 14)
        self.assertEqual(len(bds), 1)
        bd = bds[0]
        self.assertEqual(bd.type, "armor")
        self.assertEqual(len(bd.applied), 1)
        self.assertEqual(bd.applied[0].source, "mage_armor")
        self.assertEqual(len(bd.suppressed), 1)
        self.assertEqual(bd.suppressed[0].source, "leather_armor")
        self.assertEqual(bd.contribution, 4)

    def test_breakdown_bonus_and_penalty_separate(self):
        a = mod(4, "morale", "fort_save", "heroism")
        b = mod(2, "morale", "fort_save", "minor_buff")
        c = mod(-2, "morale", "fort_save", "shaken")
        total, bds = compute_with_breakdown(0, [a, b, c])
        self.assertEqual(total, 4 + (-2))  # +4 highest bonus, -2 worst penalty
        bd = bds[0]
        applied_sources = {m.source for m in bd.applied}
        self.assertIn("heroism", applied_sources)
        self.assertIn("shaken", applied_sources)
        self.assertNotIn("minor_buff", applied_sources)


# ---------------------------------------------------------------------------
# ModifierCollection
# ---------------------------------------------------------------------------


class TestCollection(unittest.TestCase):
    def test_add_and_for_target(self):
        c = ModifierCollection()
        c.add(mod(2, "armor", "ac", "leather"))
        c.add(mod(3, "ability", "fort_save", "con_mod"))
        self.assertEqual(len(c.for_target("ac")), 1)
        self.assertEqual(len(c.for_target("fort_save")), 1)
        self.assertEqual(len(c.for_target("ref_save")), 0)

    def test_remove_by_source(self):
        c = ModifierCollection()
        c.add(mod(2, "armor", "ac", "leather"))
        c.add(mod(2, "shield", "ac", "shield_a"))
        c.add(mod(2, "armor", "ac", "leather"))  # second one with same source
        removed = c.remove_by_source("leather")
        self.assertEqual(removed, 2)
        remaining = c.for_target("ac")
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].source, "shield_a")

    def test_total(self):
        c = ModifierCollection()
        c.add(mod(2, "armor", "ac", "leather"))
        c.add(mod(2, "shield", "ac", "lt_shield"))
        c.add(mod(1, "size", "ac", "small"))
        c.add(mod(3, "ability", "ac", "dex_mod"))
        # Base 10 + 2 + 2 + 1 + 3 = 18.
        self.assertEqual(c.total(10, "ac"), 18)

    def test_prune_expired(self):
        c = ModifierCollection()
        c.add(mod(4, "enhancement", "ability:str", "bulls_strength", expires_round=10))
        c.add(mod(2, "armor", "ac", "leather"))  # permanent
        expired = c.prune_expired(10)
        self.assertEqual(len(expired), 1)
        self.assertEqual(expired[0].source, "bulls_strength")
        self.assertEqual(len(c.modifiers), 1)
        # Pruning at an earlier round shouldn't remove anything.
        expired_again = c.prune_expired(9)
        self.assertEqual(expired_again, [])

    def test_breakdown_via_collection(self):
        c = ModifierCollection()
        c.add(mod(2, "armor", "ac", "leather"))
        c.add(mod(4, "armor", "ac", "mage_armor"))
        total, bds = c.breakdown(10, "ac")
        self.assertEqual(total, 14)
        self.assertEqual(len(bds), 1)


# ---------------------------------------------------------------------------
# stat_report
# ---------------------------------------------------------------------------


class TestStatReport(unittest.TestCase):
    def test_simple_report_shape(self):
        a = mod(2, "armor", "ac", "leather")
        b = mod(4, "armor", "ac", "mage_armor")
        c = mod(3, "ability", "ac", "dex_mod")
        report = stat_report(10, "base_ac_10", [a, b, c])
        self.assertEqual(report["total"], 17)  # 10 + 4 (mage_armor) + 3 (dex)
        self.assertEqual(report["base"], 10)
        self.assertEqual(report["base_source"], "base_ac_10")
        applied_sources = {m["source"] for m in report["modifiers"]}
        self.assertIn("mage_armor", applied_sources)
        self.assertIn("dex_mod", applied_sources)
        suppressed_sources = {m["source"] for m in report.get("suppressed", [])}
        self.assertIn("leather", suppressed_sources)


# ---------------------------------------------------------------------------
# with_target
# ---------------------------------------------------------------------------


class TestWithTarget(unittest.TestCase):
    def test_replicates_modifiers_with_new_target(self):
        rage_str = mod(4, "morale", "ability:str", "rage")
        rage_con = mod(4, "morale", "ability:con", "rage")
        # If we wanted to express the same thing as a single base, we could
        # use with_target to make multiples.
        retargeted = with_target([rage_str], "ability:con")
        self.assertEqual(retargeted[0].target, "ability:con")
        self.assertEqual(retargeted[0].value, 4)


if __name__ == "__main__":
    unittest.main()
