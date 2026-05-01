"""Tests for dnd.engine.combat."""

from __future__ import annotations

import unittest

from dnd.engine.combat import (
    AttackProfile,
    DefenseProfile,
    _split_damage_string,
    attack_profile_from_monster_attack,
    attack_roll,
    damage_roll,
    resolve_attack,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller


# ---------------------------------------------------------------------------
# Reference profiles
# ---------------------------------------------------------------------------


def _longsword(bonus: int = 4, damage_bonus: int = 3) -> AttackProfile:
    return AttackProfile(
        attack_bonus=bonus,
        damage_dice="1d8",
        damage_bonus=damage_bonus,
        crit_range=(19, 20),
        crit_multiplier=2,
        damage_type="S",
        name="longsword",
    )


def _orc_falchion(bonus: int = 4, damage_bonus: int = 4) -> AttackProfile:
    # 18-20/x2 great-crit weapon
    return AttackProfile(
        attack_bonus=bonus,
        damage_dice="2d4",
        damage_bonus=damage_bonus,
        crit_range=(18, 20),
        crit_multiplier=2,
        damage_type="S",
        name="falchion",
    )


def _ac(total: int = 14, dr: tuple[int, frozenset[str]] | None = None) -> DefenseProfile:
    return DefenseProfile(ac=total, touch_ac=total, flat_footed_ac=total, dr=dr)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestAttackRoll(unittest.TestCase):
    def test_attack_roll_seeded(self):
        rng = Roller(seed=1)
        nat_a, total_a = attack_roll(rng, 5)
        rng_b = Roller(seed=1)
        nat_b, total_b = attack_roll(rng_b, 5)
        self.assertEqual(nat_a, nat_b)
        self.assertEqual(total_a, total_b)
        self.assertEqual(total_a, nat_a + 5)
        self.assertGreaterEqual(nat_a, 1)
        self.assertLessEqual(nat_a, 20)


class TestDamageRoll(unittest.TestCase):
    def test_simple_1d8(self):
        rng = Roller(seed=42)
        total, individual = damage_roll(rng, "1d8", 3, 1)
        self.assertEqual(len(individual), 1)
        self.assertEqual(total, individual[0] + 3)

    def test_crit_doubles_dice_and_bonus(self):
        # 1d8 weapon, +3 bonus, x2 crit. Two die rolls + 6 (3 doubled).
        rng_a = Roller(seed=42)
        rng_b = Roller(seed=42)
        non_crit_total, non_crit_dice = damage_roll(rng_a, "1d8", 3, 1)
        crit_total, crit_dice = damage_roll(rng_b, "1d8", 3, 2)
        self.assertEqual(len(non_crit_dice), 1)
        self.assertEqual(len(crit_dice), 2)
        # Crit damage = double-die total + 2*3 bonus.
        self.assertEqual(crit_total, sum(crit_dice) + 6)


class TestSplitDamageString(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(_split_damage_string("1d8+3"), ("1d8", 3))
        self.assertEqual(_split_damage_string("2d4+4"), ("2d4", 4))
        self.assertEqual(_split_damage_string("1d6"), ("1d6", 0))
        self.assertEqual(_split_damage_string("1d4-1"), ("1d4", -1))


class TestResolveAttackBasics(unittest.TestCase):
    def test_natural_one_auto_miss(self):
        # Find a seed where the d20 rolls a 1.
        for seed in range(1, 200):
            rng = Roller(seed=seed)
            nat, _ = attack_roll(rng, 0)
            if nat == 1:
                rng = Roller(seed=seed)
                outcome = resolve_attack(_longsword(bonus=20), _ac(total=10), rng)
                self.assertFalse(outcome.hit)
                self.assertTrue(outcome.natural_1)
                self.assertEqual(outcome.damage, 0)
                return
        self.fail("never rolled a 1 in 200 seeds")

    def test_natural_twenty_auto_hit(self):
        for seed in range(1, 200):
            rng = Roller(seed=seed)
            nat, _ = attack_roll(rng, 0)
            if nat == 20:
                rng = Roller(seed=seed)
                # Defender AC is impossibly high.
                outcome = resolve_attack(_longsword(bonus=0), _ac(total=100), rng)
                self.assertTrue(outcome.hit)
                self.assertTrue(outcome.natural_20)
                self.assertGreater(outcome.damage, 0)
                return
        self.fail("never rolled a 20 in 200 seeds")

    def test_normal_miss(self):
        # Force a moderate roll vs an AC we don't beat.
        rng = Roller(seed=7)
        outcome = resolve_attack(_longsword(bonus=0), _ac(total=30), rng)
        self.assertFalse(outcome.hit)
        self.assertEqual(outcome.damage, 0)

    def test_normal_hit(self):
        rng = Roller(seed=7)
        outcome = resolve_attack(_longsword(bonus=20), _ac(total=10), rng)
        self.assertTrue(outcome.hit)
        # Successful hit: at least 1 damage.
        self.assertGreaterEqual(outcome.damage, 1)


class TestCriticalThreats(unittest.TestCase):
    def test_threat_in_range_confirms(self):
        # Find a seed where the first d20 = 19 (within 19-20) and the
        # confirmation is also a hit.
        for seed in range(1, 500):
            rng = Roller(seed=seed)
            nat1, _ = attack_roll(rng, 0)
            if nat1 != 19:
                continue
            nat2, _ = attack_roll(rng, 0)
            if nat2 < 5:
                continue  # too low to confirm against modest AC
            rng = Roller(seed=seed)
            outcome = resolve_attack(_longsword(bonus=10), _ac(total=10), rng)
            self.assertTrue(outcome.hit)
            self.assertTrue(outcome.threatened)
            self.assertTrue(outcome.crit)
            return
        self.fail("never rolled 19 with confirming follow-up in 500 seeds")

    def test_threat_outside_range_not_threatened(self):
        # Falchion threatens on 18-20; an 17 should not threaten.
        for seed in range(1, 500):
            rng = Roller(seed=seed)
            nat, _ = attack_roll(rng, 0)
            if nat == 17:
                rng = Roller(seed=seed)
                outcome = resolve_attack(_orc_falchion(bonus=10), _ac(total=10), rng)
                self.assertTrue(outcome.hit)
                self.assertFalse(outcome.threatened)
                self.assertFalse(outcome.crit)
                return
        self.fail("never rolled a 17 in 500 seeds")


class TestDamageReduction(unittest.TestCase):
    def test_dr_absorbs_damage(self):
        rng = Roller(seed=1)
        # Slashing weapon vs. DR 5/bludgeoning. DR applies; absorbed at most 5.
        ac = DefenseProfile(
            ac=10, touch_ac=10, flat_footed_ac=10,
            dr=(5, frozenset({"bludgeoning"})),
        )
        outcome = resolve_attack(_longsword(bonus=20), ac, rng)
        if outcome.hit:
            self.assertGreaterEqual(outcome.dr_absorbed, 1)

    def test_dr_bypassed_by_correct_type(self):
        # Bludgeoning attack against DR 5/bludgeoning bypasses the DR.
        rng = Roller(seed=1)
        ac = DefenseProfile(
            ac=10, touch_ac=10, flat_footed_ac=10,
            dr=(5, frozenset({"bludgeoning"})),
        )
        bludgeon = AttackProfile(
            attack_bonus=20, damage_dice="1d6", damage_bonus=2,
            crit_range=(20, 20), crit_multiplier=2,
            damage_type="B", name="club",
        )
        outcome = resolve_attack(bludgeon, ac, rng)
        if outcome.hit:
            self.assertEqual(outcome.dr_absorbed, 0)


class TestSituationalAC(unittest.TestCase):
    def test_flat_footed_ac_used(self):
        # Defender has lower flat-footed AC.
        ac = DefenseProfile(ac=20, touch_ac=15, flat_footed_ac=12)
        rng = Roller(seed=3)
        # We just verify it's consulting the right number.
        outcome = resolve_attack(_longsword(bonus=0), ac, rng, situation="flat_footed")
        self.assertEqual(outcome.target_ac, 12)


# ---------------------------------------------------------------------------
# Integration with monster content
# ---------------------------------------------------------------------------


class TestMonsterAttackProfile(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reg = default_registry()

    def test_goblin_short_sword(self):
        goblin = self.reg.get_monster("goblin")
        atk = next(a for a in goblin.attacks if a["name"] == "short sword")
        profile = attack_profile_from_monster_attack(atk)
        self.assertEqual(profile.attack_bonus, 2)
        self.assertEqual(profile.damage_dice, "1d4")
        self.assertEqual(profile.damage_bonus, 0)
        self.assertEqual(profile.crit_range, (19, 20))

    def test_resolve_goblin_vs_basic_target(self):
        goblin = self.reg.get_monster("goblin")
        atk = attack_profile_from_monster_attack(
            next(a for a in goblin.attacks if a["name"] == "short sword"),
        )
        defense = _ac(total=14)
        rng = Roller(seed=10)
        outcome = resolve_attack(atk, defense, rng)
        # Sanity: no crashes, damage is in valid range.
        if outcome.hit:
            self.assertGreaterEqual(outcome.damage, 1)
            self.assertLessEqual(outcome.damage, 4 * 2)  # max 1d4*2 + 0


if __name__ == "__main__":
    unittest.main()
