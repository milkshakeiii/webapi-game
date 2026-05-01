"""Tests for monster damage reduction wired from racial_traits."""

from __future__ import annotations

import unittest

from dnd.engine.combat import (
    AttackProfile,
    DefenseProfile,
    resolve_attack,
)
from dnd.engine.combatant import (
    _monster_damage_reduction,
    _parse_dr_trait,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller


REGISTRY = default_registry()


class TestParseDrTrait(unittest.TestCase):
    def test_bludgeoning(self):
        self.assertEqual(
            _parse_dr_trait("dr_5_bludgeoning"),
            (5, frozenset({"bludgeoning"})),
        )

    def test_slashing(self):
        self.assertEqual(
            _parse_dr_trait("dr_5_slashing"),
            (5, frozenset({"slashing"})),
        )

    def test_higher_amount(self):
        self.assertEqual(
            _parse_dr_trait("dr_10_silver"),
            (10, frozenset({"silver"})),
        )

    def test_non_dr_trait_returns_none(self):
        self.assertIsNone(_parse_dr_trait("ferocity"))
        self.assertIsNone(_parse_dr_trait("light_sensitivity"))
        self.assertIsNone(_parse_dr_trait(""))

    def test_malformed_amount_returns_none(self):
        self.assertIsNone(_parse_dr_trait("dr_xx_slashing"))


class TestMonsterDR(unittest.TestCase):
    def test_skeleton_has_dr_5_bludgeoning(self):
        sk = combatant_from_monster(
            REGISTRY.get_monster("skeleton"), (0, 0), "enemies",
        )
        self.assertEqual(
            sk.damage_reduction, (5, frozenset({"bludgeoning"})),
        )
        # And it propagates into the defense_profile.
        prof = sk.defense_profile()
        self.assertEqual(prof.dr, (5, frozenset({"bludgeoning"})))

    def test_zombie_has_dr_5_slashing(self):
        z = combatant_from_monster(
            REGISTRY.get_monster("human_zombie"), (0, 0), "enemies",
        )
        self.assertEqual(
            z.damage_reduction, (5, frozenset({"slashing"})),
        )

    def test_goblin_has_no_dr(self):
        g = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (0, 0), "enemies",
        )
        self.assertIsNone(g.damage_reduction)

    def test_orc_has_no_dr(self):
        # Orcs have ferocity but no DR.
        o = combatant_from_monster(
            REGISTRY.get_monster("orc"), (0, 0), "enemies",
        )
        self.assertIsNone(o.damage_reduction)


# ---------------------------------------------------------------------------
# End-to-end: DR actually reduces damage in resolve_attack
# ---------------------------------------------------------------------------


class TestDrInCombat(unittest.TestCase):
    def test_slashing_attack_vs_skeleton_reduced(self):
        sk = combatant_from_monster(
            REGISTRY.get_monster("skeleton"), (0, 0), "enemies",
        )
        # An attack that always hits and always rolls max-ish damage,
        # using slashing damage type which DOES NOT bypass dr/bludgeoning.
        attack = AttackProfile(
            attack_bonus=20, damage_dice="1d6", damage_bonus=10,
            crit_range=(20, 20), crit_multiplier=2,
            damage_type="S", name="longsword",
        )
        before = sk.current_hp
        out = resolve_attack(attack, sk.defense_profile(), Roller(seed=1))
        self.assertTrue(out.hit)
        self.assertGreater(out.dr_absorbed, 0)
        # Damage applied to HP would be (raw - 5), capped non-negative.
        # Just confirm the outcome's "damage" is the post-DR number and
        # is at least 5 less than the pre-DR raw damage.
        self.assertEqual(out.damage, out.damage_dealt_pre_dr - out.dr_absorbed)

    def test_bludgeoning_attack_vs_skeleton_bypasses(self):
        sk = combatant_from_monster(
            REGISTRY.get_monster("skeleton"), (0, 0), "enemies",
        )
        attack = AttackProfile(
            attack_bonus=20, damage_dice="1d6", damage_bonus=10,
            crit_range=(20, 20), crit_multiplier=2,
            damage_type="B", name="warhammer",
        )
        out = resolve_attack(attack, sk.defense_profile(), Roller(seed=1))
        self.assertTrue(out.hit)
        # Bludgeoning bypasses DR — no absorption.
        self.assertEqual(out.dr_absorbed, 0)
        self.assertEqual(out.damage, out.damage_dealt_pre_dr)

    def test_slashing_attack_vs_zombie_bypasses(self):
        z = combatant_from_monster(
            REGISTRY.get_monster("human_zombie"), (0, 0), "enemies",
        )
        # Zombie DR is /slashing — slashing weapons DO bypass.
        attack = AttackProfile(
            attack_bonus=20, damage_dice="1d6", damage_bonus=10,
            crit_range=(20, 20), crit_multiplier=2,
            damage_type="S", name="longsword",
        )
        out = resolve_attack(attack, z.defense_profile(), Roller(seed=1))
        self.assertTrue(out.hit)
        self.assertEqual(out.dr_absorbed, 0)

    def test_piercing_attack_vs_zombie_reduced(self):
        z = combatant_from_monster(
            REGISTRY.get_monster("human_zombie"), (0, 0), "enemies",
        )
        # Piercing does NOT bypass dr/slashing.
        attack = AttackProfile(
            attack_bonus=20, damage_dice="1d6", damage_bonus=10,
            crit_range=(20, 20), crit_multiplier=2,
            damage_type="P", name="rapier",
        )
        out = resolve_attack(attack, z.defense_profile(), Roller(seed=1))
        self.assertTrue(out.hit)
        self.assertGreater(out.dr_absorbed, 0)


if __name__ == "__main__":
    unittest.main()
