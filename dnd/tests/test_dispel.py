"""Tests for dispel magic and spell-source tracking."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.spells import active_spell_sources, cast_spell


REGISTRY = default_registry()


class TestActiveSpellSources(unittest.TestCase):
    def test_empty_when_no_spells_active(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        self.assertEqual(active_spell_sources(g), [])

    def test_lists_spell_sources_from_modifiers(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        # Cast bless on the orc (gives a +1 morale to attack/saves).
        bless = REGISTRY.get_spell("bless")
        cast_spell(g, bless, [g], 1, REGISTRY, Roller(seed=1), current_round=1)
        sources = active_spell_sources(g)
        self.assertIn("spell:bless", sources)


class TestDispelMagic(unittest.TestCase):
    def test_successful_dispel_removes_modifier(self):
        # Cast bless on an orc, then dispel it. Bless adds +1 modifiers
        # sourced "spell:bless"; after dispel they should be gone (when
        # the dispel check passes).
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (1, 0), "x")
        bless = REGISTRY.get_spell("bless")
        cast_spell(caster, bless, [target], 1, REGISTRY,
                   Roller(seed=1), current_round=1)
        self.assertIn("spell:bless", active_spell_sources(target))
        # Now dispel. Iterate seeds until one passes.
        dispel = REGISTRY.get_spell("dispel_magic")
        for seed in range(1, 30):
            target2 = combatant_from_monster(REGISTRY.get_monster("orc"),
                                             (1, 0), "x")
            cast_spell(caster, bless, [target2], 1, REGISTRY,
                       Roller(seed=1), current_round=1)
            self.assertIn("spell:bless", active_spell_sources(target2))
            cast_spell(caster, dispel, [target2], 3, REGISTRY,
                       Roller(seed=seed), current_round=2)
            if "spell:bless" not in active_spell_sources(target2):
                return  # successful dispel observed
        self.fail("expected at least one seed where dispel succeeded")

    def test_failed_dispel_leaves_effect_intact(self):
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (1, 0), "x")
        bless = REGISTRY.get_spell("bless")
        dispel = REGISTRY.get_spell("dispel_magic")
        # Find a seed where dispel FAILS (low d20 roll).
        for seed in range(1, 30):
            target2 = combatant_from_monster(REGISTRY.get_monster("orc"),
                                             (1, 0), "x")
            cast_spell(caster, bless, [target2], 1, REGISTRY,
                       Roller(seed=1), current_round=1)
            cast_spell(caster, dispel, [target2], 3, REGISTRY,
                       Roller(seed=seed), current_round=2)
            if "spell:bless" in active_spell_sources(target2):
                return  # observed failure path
        self.fail("expected at least one seed where dispel failed")

    def test_dispel_no_active_effects_is_noop(self):
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (1, 0), "x")
        dispel = REGISTRY.get_spell("dispel_magic")
        outcome = cast_spell(caster, dispel, [target], 3, REGISTRY,
                             Roller(seed=1), current_round=1)
        # No effects, so target shouldn't be listed in targets_affected.
        self.assertNotIn(target.id, outcome.targets_affected)


class TestSourcedConditionTracking(unittest.TestCase):
    def test_charm_registers_condition_source(self):
        # The charm handler should call register_sourced_condition so
        # dispel can find and clear the "charmed" condition.
        from dnd.engine.spells import _handle_charm
        # Build the test rig directly (skip cast pipeline).
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (1, 0), "y")
        # Override the goblin's will-save to fail every time so the
        # charm always lands.
        target.bases["will_save"] = -100
        from dnd.engine.spells import SpellOutcome
        out = SpellOutcome(
            spell_id="charm_person", caster_id=caster.id,
            success=True, targets_affected=[],
            damage_per_target={}, healing_per_target={},
            conditions_applied={}, modifiers_applied={}, save_dc=15,
        )
        spell = REGISTRY.get_spell("charm_person")
        _handle_charm(caster, spell, target, 15, 1, REGISTRY,
                      Roller(seed=1), out, current_round=1)
        # Charmed condition tracked under spell:charm_person source.
        self.assertIn("spell:charm_person", target.sourced_conditions)
        self.assertIn("charmed", target.sourced_conditions["spell:charm_person"])

    def test_remove_effects_from_source_clears_both(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        # Manually add a fake spell modifier and tracked condition.
        from dnd.engine.modifiers import Modifier
        g.add_modifier(Modifier(value=2, type="morale", target="attack",
                                source="spell:fake_buff"))
        g.add_condition("blessed_test")
        g.register_sourced_condition("spell:fake_buff", "blessed_test")
        # Remove.
        n_mods, conds = g.remove_effects_from_source("spell:fake_buff")
        self.assertEqual(n_mods, 1)
        self.assertEqual(conds, ["blessed_test"])
        self.assertNotIn("blessed_test", g.conditions)


if __name__ == "__main__":
    unittest.main()
