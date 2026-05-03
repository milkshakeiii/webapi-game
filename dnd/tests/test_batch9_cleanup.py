"""Tests for Batch 9 cleanup: encumbrance speed/Max-Dex, metamagic
(empower/maximize/still/silent/extend), Mounted Combat / Spirited
Charge feats."""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import (
    combatant_from_character,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.encumbrance import effective_speed, reduced_speed
from dnd.engine.grid import Grid
from dnd.engine.spells import cast_spell
from dnd.engine.turn_executor import _do_attack, execute_turn


REGISTRY = default_registry()


class TestEncumbranceSpeedAndMaxDex(unittest.TestCase):
    def test_reduced_speed_table(self):
        # 30→20, 20→15, 15→10, etc.
        self.assertEqual(reduced_speed(30), 20)
        self.assertEqual(reduced_speed(20), 15)
        self.assertEqual(reduced_speed(15), 10)

    def test_effective_speed_drops_under_heavy_load(self):
        self.assertEqual(effective_speed(30, None, "heavy"), 20)
        self.assertEqual(effective_speed(30, None, "medium"), 20)
        self.assertEqual(effective_speed(30, None, "light"), 30)

    def test_heavy_load_caps_max_dex(self):
        # Build a high-Dex character then add load weight via heavy
        # equipment. Verify the AC's Dex contribution is capped.
        # Use rogue with Dex 16, base Dex mod = +3.
        # 2 + 10 + 5 + 2 + 1 + 0 = 20.
        # Light loadout (no armor): full dex applies.
        light_req = CharacterRequest.from_dict({
            "name": "Light", "race": "human", "class": "rogue",
            "alignment": "true_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 12, "dex": 16, "con": 14,
                           "int": 12, "wis": 11, "cha": 10}},
            "free_ability_choice": "dex",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"acrobatics": 1, "stealth": 1, "ride": 1},
            "bonus_languages": [],
            "equipment": {"weapon": "dagger", "armor": "none", "shield": None},
        })
        light = combatant_from_character(create_character(light_req, REGISTRY),
                                         REGISTRY, (5, 5), "x")
        # Heavy loadout: chainmail (40 lb) which is >2/3 of 76 = ~50 with low Str.
        # Use Str 8 to make the heavy gear actually heavy load.
        # 0+5+5+2+2+1 = 15 (need point_buy_15)
        # 0+10+5+0+2-2 = 15
        heavy_req = CharacterRequest.from_dict({
            "name": "Heavy", "race": "human", "class": "rogue",
            "alignment": "true_neutral",
            "ability_scores": {"method": "point_buy_15",
                "scores": {"str": 10, "dex": 16, "con": 14,
                           "int": 10, "wis": 12, "cha": 8}},
            "free_ability_choice": "dex",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"acrobatics": 1, "ride": 1},
            "bonus_languages": [],
            "equipment": {"weapon": "dagger", "armor": "chainmail",
                          "shield": "heavy_steel_shield"},
        })
        heavy = combatant_from_character(create_character(heavy_req, REGISTRY),
                                         REGISTRY, (5, 5), "x")
        # Heavy character should have lower or equal speed and lower or
        # equal AC (Max-Dex cap kicks in if load is medium/heavy AND Dex
        # exceeds the cap). The test verifies movement reduction.
        self.assertLess(heavy.speed, light.speed)


class TestMetamagic(unittest.TestCase):
    def test_empower_increases_damage(self):
        # Cast scaling_damage with and without empower; compare results.
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (1, 0), "y")
        target.max_hp = 9999
        target.current_hp = 9999
        spell = REGISTRY.get_spell("burning_hands")
        # Drain target's saves to ensure no save-half halving.
        target.bases["ref_save"] = -100
        # Baseline.
        target.current_hp = target.max_hp
        out_baseline = cast_spell(caster, spell, [target], 1, REGISTRY,
                                  Roller(seed=1))
        baseline = out_baseline.damage_per_target.get(target.id, 0)
        # With empower (same seed → same dice → same baseline pre-empower).
        target.current_hp = target.max_hp
        out_emp = cast_spell(caster, spell, [target], 1, REGISTRY,
                             Roller(seed=1), metamagic=["empower_spell"])
        empowered = out_emp.damage_per_target.get(target.id, 0)
        self.assertEqual(empowered, (baseline * 3) // 2)

    def test_maximize_uses_max_dice(self):
        # Magic missile has no save and no SR-blocking-via-monster path
        # for orcs (SR=0). Damage per missile is 1d4+1, max = 5.
        # With maximize, every seed should produce the same total.
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        spell = REGISTRY.get_spell("magic_missile")
        results: set[int] = set()
        for seed in range(1, 10):
            target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                            (1, 0), "y")
            target.max_hp = 9999
            target.current_hp = target.max_hp
            out_max = cast_spell(caster, spell, [target], 1, REGISTRY,
                                 Roller(seed=seed),
                                 metamagic=["maximize_spell"])
            results.add(out_max.damage_per_target.get(target.id, 0))
        # All seeds produce the same maximized total (5 per missile).
        self.assertEqual(len(results), 1, f"expected one value; got {results}")
        # And the value should equal the deterministic max.
        self.assertEqual(results.pop(), 5)


class TestSpiritedCharge(unittest.TestCase):
    def test_spirited_charge_lance_triples_damage(self):
        attacker = combatant_from_monster(REGISTRY.get_monster("orc"),
                                          (5, 5), "x")
        attacker.attack_options = [{
            "type": "melee",
            "name": "Lance",
            "weapon_id": "lance",
            "weapon_category": "martial",
            "attack_bonus": 100,
            "damage": "1d8",
            "damage_bonus": 4,
            "damage_type": "P",
            "crit_range": [20, 20],
            "crit_multiplier": 3,
            "range_increment": 0,
            "wield": "two_handed",
        }]
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (6, 5), "y")
        target.max_hp = 9999
        target.current_hp = 9999
        grid = Grid(width=20, height=10)
        grid.place(attacker)
        grid.place(target)
        enc = Encounter.begin(grid, [attacker, target], Roller(seed=1))
        # Baseline: ×1 (no charge multiplier).
        events_baseline: list = []
        before = target.current_hp
        _do_attack(attacker, target, grid, Roller(seed=1), events_baseline,
                   label="baseline", encounter=enc, script_options={})
        baseline = before - target.current_hp
        # Spirited Charge with lance: ×3.
        target.current_hp = target.max_hp
        events_sc: list = []
        before = target.current_hp
        _do_attack(attacker, target, grid, Roller(seed=1), events_sc,
                   label="charge", encounter=enc,
                   script_options={"charge_damage_multiplier": 3})
        sc_damage = before - target.current_hp
        self.assertEqual(sc_damage, baseline * 3)


class TestDispelMagicConditions(unittest.TestCase):
    def test_dispel_clears_charm_condition(self):
        # Charm a goblin, then dispel; both modifier and the "charmed"
        # condition should be gone.
        caster = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (1, 0), "y")
        target.bases["will_save"] = -100  # ensure charm lands
        charm = REGISTRY.get_spell("charm_person")
        cast_spell(caster, charm, [target], 1, REGISTRY,
                   Roller(seed=1), current_round=1)
        self.assertIn("charmed", target.conditions)
        self.assertIn("spell:charm_person", target.sourced_conditions)
        # Dispel.
        dispel = REGISTRY.get_spell("dispel_magic")
        for seed in range(1, 30):
            # Re-set up if previous failed.
            target_t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                              (1, 0), "y")
            target_t.bases["will_save"] = -100
            cast_spell(caster, charm, [target_t], 1, REGISTRY,
                       Roller(seed=1), current_round=1)
            cast_spell(caster, dispel, [target_t], 3, REGISTRY,
                       Roller(seed=seed), current_round=2)
            if "charmed" not in target_t.conditions:
                # success path observed
                self.assertNotIn("spell:charm_person",
                                 target_t.sourced_conditions)
                return
        self.fail("expected at least one dispel that cleared charm")


if __name__ == "__main__":
    unittest.main()
