"""Tests for the energy damage system: damage typing, resistance,
immunity, and the new iconic spells (fireball, lightning bolt, etc.)."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.spells import apply_typed_damage, cast_spell


REGISTRY = default_registry()


class TestApplyTypedDamage(unittest.TestCase):
    def test_no_damage_type_passes_through(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        before = g.current_hp
        applied, note = apply_typed_damage(g, 5, None)
        self.assertEqual(applied, 5)
        self.assertEqual(g.current_hp, before - 5)
        self.assertIsNone(note)

    def test_non_energy_type_passes_through(self):
        # "force" is not energy — magic missile damage.
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.energy_resistance["fire"] = 100
        before = g.current_hp
        applied, _ = apply_typed_damage(g, 5, "force")
        self.assertEqual(applied, 5)
        self.assertEqual(g.current_hp, before - 5)

    def test_energy_resistance_reduces_damage(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.energy_resistance["fire"] = 5
        before = g.current_hp
        applied, note = apply_typed_damage(g, 12, "fire")
        self.assertEqual(applied, 7)  # 12 - 5
        self.assertEqual(g.current_hp, before - 7)
        self.assertEqual(note, "resisted 5")

    def test_resistance_caps_at_damage_amount(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.energy_resistance["cold"] = 100
        before = g.current_hp
        applied, note = apply_typed_damage(g, 8, "cold")
        self.assertEqual(applied, 0)
        self.assertEqual(g.current_hp, before)
        self.assertEqual(note, "resisted 8")

    def test_immunity_blocks_damage_completely(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.energy_immunity.add("fire")
        before = g.current_hp
        applied, note = apply_typed_damage(g, 100, "fire")
        self.assertEqual(applied, 0)
        self.assertEqual(g.current_hp, before)
        self.assertEqual(note, "immune")

    def test_immunity_only_for_listed_type(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.energy_immunity.add("fire")
        before = g.current_hp
        applied, _ = apply_typed_damage(g, 6, "cold")
        self.assertEqual(applied, 6)
        self.assertEqual(g.current_hp, before - 6)


class TestFireballThroughCastSpell(unittest.TestCase):
    def test_fireball_deals_fire_damage(self):
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (1, 0), "y")
        target.bases["ref_save"] = -100
        spell = REGISTRY.get_spell("fireball")
        before = target.current_hp
        out = cast_spell(caster, spell, [target], 3, REGISTRY,
                         Roller(seed=1))
        self.assertGreater(before - target.current_hp, 0)
        self.assertEqual(out.damage_per_target.get(target.id),
                         before - target.current_hp)

    def test_fireball_blocked_by_fire_immunity(self):
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (1, 0), "y")
        target.bases["ref_save"] = -100
        target.energy_immunity.add("fire")
        spell = REGISTRY.get_spell("fireball")
        before = target.current_hp
        cast_spell(caster, spell, [target], 3, REGISTRY,
                   Roller(seed=1))
        self.assertEqual(target.current_hp, before)

    def test_fireball_reduced_by_fire_resistance(self):
        # Resistance 5 should reduce each fireball cast by exactly 5.
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        spell = REGISTRY.get_spell("fireball")
        baseline_target = combatant_from_monster(
            REGISTRY.get_monster("orc"), (1, 0), "y")
        baseline_target.bases["ref_save"] = -100
        baseline_target.max_hp = 9999
        baseline_target.current_hp = 9999
        before = baseline_target.current_hp
        cast_spell(caster, spell, [baseline_target], 3, REGISTRY,
                   Roller(seed=42))
        baseline_damage = before - baseline_target.current_hp

        resisted_target = combatant_from_monster(
            REGISTRY.get_monster("orc"), (1, 0), "y")
        resisted_target.bases["ref_save"] = -100
        resisted_target.max_hp = 9999
        resisted_target.current_hp = 9999
        resisted_target.energy_resistance["fire"] = 5
        before = resisted_target.current_hp
        cast_spell(caster, spell, [resisted_target], 3, REGISTRY,
                   Roller(seed=42))
        resisted_damage = before - resisted_target.current_hp
        # Expect baseline - 5 == resisted (if baseline > 5), else 0.
        self.assertEqual(resisted_damage, max(0, baseline_damage - 5))


class TestLightningBolt(unittest.TestCase):
    def test_lightning_bolt_deals_electricity_damage(self):
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (1, 0), "y")
        target.bases["ref_save"] = -100
        spell = REGISTRY.get_spell("lightning_bolt")
        before = target.current_hp
        cast_spell(caster, spell, [target], 3, REGISTRY,
                   Roller(seed=1))
        self.assertGreater(before - target.current_hp, 0)

    def test_lightning_bolt_blocked_by_electricity_immunity(self):
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (1, 0), "y")
        target.bases["ref_save"] = -100
        target.energy_immunity.add("electricity")
        spell = REGISTRY.get_spell("lightning_bolt")
        before = target.current_hp
        cast_spell(caster, spell, [target], 3, REGISTRY,
                   Roller(seed=1))
        self.assertEqual(target.current_hp, before)


class TestScorchingRay(unittest.TestCase):
    def test_scorching_ray_uses_magic_missile_handler(self):
        # Scorching ray uses kind=magic_missile but with damage_type=fire.
        # Resistance should still apply.
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (1, 0), "y")
        target.energy_immunity.add("fire")
        spell = REGISTRY.get_spell("scorching_ray")
        before = target.current_hp
        cast_spell(caster, spell, [target], 2, REGISTRY,
                   Roller(seed=1))
        self.assertEqual(target.current_hp, before)


class TestColdSpell(unittest.TestCase):
    def test_cone_of_cold_blocked_by_cold_immunity(self):
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (1, 0), "y")
        target.bases["ref_save"] = -100
        target.energy_immunity.add("cold")
        spell = REGISTRY.get_spell("cone_of_cold")
        before = target.current_hp
        cast_spell(caster, spell, [target], 5, REGISTRY,
                   Roller(seed=1))
        self.assertEqual(target.current_hp, before)


class TestMagicMissileNotEnergy(unittest.TestCase):
    def test_magic_missile_force_damage_ignores_fire_immunity(self):
        # Magic missile is "force" damage — fire immunity should not help.
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (1, 0), "y")
        target.energy_immunity.add("fire")
        spell = REGISTRY.get_spell("magic_missile")
        before = target.current_hp
        cast_spell(caster, spell, [target], 1, REGISTRY,
                   Roller(seed=1))
        self.assertLess(target.current_hp, before)


if __name__ == "__main__":
    unittest.main()
