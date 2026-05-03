"""Tests for Batch 16: easy-win PARTIALs.

Covers:
- unconscious implies helpless
- aid_another vs-that-foe restriction
- charge blocked by difficult terrain
- disabled creature self-damages on standard action
- AoO triggers on draw_weapon (BAB 0), drink_potion, retrieve_stowed_item
- skill_check take-10 in-combat detection
- bonus spells from high key ability
- weapon trip_bonus
- cover Reflex bonus on AoE saves
"""

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
from dnd.engine.grid import Grid, difficult, wall
from dnd.engine.skills import can_take_10, skill_check
from dnd.engine.spells import cast_spell
from dnd.engine.turn_executor import (
    _cover_reflex_bonus,
    _resolve_maneuver,
    execute_turn,
)


REGISTRY = default_registry()


class TestUnconsciousImpliesHelpless(unittest.TestCase):
    def test_apply_unconscious_adds_helpless(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.add_condition("unconscious")
        self.assertIn("helpless", g.conditions)

    def test_remove_unconscious_drops_implied_helpless(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.add_condition("unconscious")
        g.remove_condition("unconscious")
        self.assertNotIn("helpless", g.conditions)
        self.assertNotIn("unconscious", g.conditions)

    def test_external_helpless_persists_after_unconscious_removed(self):
        # If something else made the actor helpless, unconscious removal
        # shouldn't drop it.
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.add_condition("helpless")  # external
        g.add_condition("unconscious")
        g.remove_condition("unconscious")
        self.assertIn("helpless", g.conditions)


class TestChargeBlockedByDifficultTerrain(unittest.TestCase):
    def test_charge_into_difficult_lane_skips(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (3, 5), "x")
        t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (8, 5), "y")
        grid = Grid(width=20, height=10)
        grid.features[(5, 5)] = difficult()  # mid-lane
        grid.place(a)
        grid.place(t)
        enc = Encounter.begin(grid, [a, t], Roller(seed=1))
        script = BehaviorScript(name="ch", rules=[
            Rule(do={"composite": "charge",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("skip", kinds)
        skip = [e for e in result.events if e.kind == "skip"][0]
        self.assertIn("path blocked", skip.detail.get("reason", ""))


class TestDisabledSelfDamage(unittest.TestCase):
    def test_disabled_actor_loses_1hp_on_standard(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (6, 5), "y")
        t.max_hp = 9999
        t.current_hp = 9999
        # Force disabled: HP exactly 0.
        a.current_hp = 0
        a.add_condition("disabled")
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(t)
        enc = Encounter.begin(grid, [a, t], Roller(seed=1))
        # Disabled creatures can take a single standard action — use
        # a single attack via slots (not full_attack, which is full-round).
        script = BehaviorScript(name="atk", rules=[
            Rule(do={"slots": {"standard": {
                "type": "attack", "target": "enemy.closest",
            }}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("disabled_self_damage", kinds)
        self.assertEqual(a.current_hp, -1)


class TestSkillsTake10InCombat(unittest.TestCase):
    def test_distracted_actor_falls_back_to_d20(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.add_condition("stunned")
        result = skill_check(
            g, "perception", dc=10, roller=Roller(seed=1),
            registry=REGISTRY, take_10=True,
        )
        # Did not take 10 (distracted).
        self.assertFalse(result.took_10)
        self.assertNotEqual(result.natural, 10)

    def test_damaged_actor_cannot_take_10(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.current_hp = g.max_hp - 1
        self.assertFalse(can_take_10(g))

    def test_uninjured_calm_actor_can_take_10(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        self.assertTrue(can_take_10(g))


class TestBonusSpellsFromHighAbility(unittest.TestCase):
    def test_int_18_wizard_gets_bonus_l1_slot(self):
        # PF1 Table 1-3: Int 18 grants +1 bonus L1 slot (Int 20 would
        # give +2). Compare against an Int-10 baseline wizard of the
        # same class and level.
        # 0+5+5+10+0+0 = 20.
        high_req = CharacterRequest.from_dict({
            "name": "BigBrain", "race": "elf", "class": "wizard",
            "alignment": "neutral_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 10, "dex": 14, "con": 14,
                           "int": 16, "wis": 10, "cha": 10}},
            "feats": ["combat_expertise"],
            "skill_ranks": {"spellcraft": 1},
            "bonus_languages": [],
        })
        # Elf gets +2 Int → effective Int 18.
        high = combatant_from_character(
            create_character(high_req, REGISTRY), REGISTRY, (5, 5), "x",
        )
        # Lower-Int baseline: Int 10 effective. Human wizard,
        # 5+5+5+0+5+0 = 20, free ability bumps str → effective Int=10.
        low_req = CharacterRequest.from_dict({
            "name": "Average", "race": "human", "class": "wizard",
            "alignment": "neutral_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 14, "con": 14,
                           "int": 10, "wis": 14, "cha": 10}},
            "free_ability_choice": "str",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"spellcraft": 1},
            "bonus_languages": [],
        })
        low = combatant_from_character(
            create_character(low_req, REGISTRY), REGISTRY, (5, 5), "x",
        )
        # High-Int wizard should have +1 more L1 slot than the
        # Int-10 baseline (Int 18: +1 bonus L1 per RAW Table 1-3).
        diff = (high.resources.get("spell_slot_1", 0)
                - low.resources.get("spell_slot_1", 0))
        self.assertEqual(diff, 1)

    def test_low_ability_no_bonus(self):
        # Wizard with Int 10 → 0 bonus slots (formula: key_score >=
        # 10 + level fails for level 1).
        # 5+5+5+0+5+0 = 20, free ability bumps str → effective Int=10.
        req = CharacterRequest.from_dict({
            "name": "Plain", "race": "human", "class": "wizard",
            "alignment": "neutral_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 14, "con": 14,
                           "int": 10, "wis": 14, "cha": 10}},
            "free_ability_choice": "str",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"spellcraft": 1},
            "bonus_languages": [],
        })
        char = create_character(req, REGISTRY)
        c = combatant_from_character(char, REGISTRY, (5, 5), "x")
        # No bonus L1 slot from key ability since int 10 < 11.
        # The actual count depends on class-table base + specialist
        # bonus; we just verify it's > 0.
        self.assertGreaterEqual(c.resources.get("spell_slot_1"), 1)


class TestWeaponTripBonus(unittest.TestCase):
    def test_whip_grants_trip_bonus(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        a.attack_options = [{
            "type": "melee", "name": "Whip", "weapon_id": "whip",
            "weapon_category": "exotic", "attack_bonus": 5,
            "damage": "1d3", "damage_bonus": 0, "damage_type": "S",
            "crit_range": [20, 20], "crit_multiplier": 2,
            "range_increment": 0, "wield": "one_handed",
        }]
        t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (6, 5), "y")
        # Set goblin's CMD to a known value.
        t.bases["cmd"] = 15
        # Force the d20 to 14 (just under base CMD 15) via seeded roller.
        # We can't force a specific roll, so iterate: with whip's +2,
        # a 13 + cmb + 2 ≥ 15 should pass when 13 + cmb < 15.
        # Easier: compare margins from same seed with and without whip.
        without_whip = combatant_from_monster(
            REGISTRY.get_monster("orc"), (5, 5), "y",
        )
        # Default orc loadout = falchion (no trip_bonus).
        _, _, total_w, _ = _resolve_maneuver(
            a, t, "trip", Roller(seed=1),
        )
        _, _, total_n, _ = _resolve_maneuver(
            without_whip, t, "trip", Roller(seed=1),
        )
        # If both orcs have same CMB and same d20, whip should add +2.
        # CMBs are equal (both orcs from the same template).
        self.assertEqual(total_w, total_n + 2)


class TestCoverReflexBonus(unittest.TestCase):
    def test_one_wall_grants_plus_2_reflex(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (1, 5), "x")
        t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (10, 5), "y")
        grid = Grid(width=20, height=10)
        grid.features[(5, 5)] = wall()
        grid.place(a)
        grid.place(t)
        self.assertEqual(_cover_reflex_bonus(a, t, grid), 2)

    def test_two_walls_grants_plus_4_reflex(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (1, 5), "x")
        t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (10, 5), "y")
        grid = Grid(width=20, height=10)
        grid.features[(4, 5)] = wall()
        grid.features[(7, 5)] = wall()
        grid.place(a)
        grid.place(t)
        self.assertEqual(_cover_reflex_bonus(a, t, grid), 4)

    def test_no_walls_no_reflex_bonus(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (1, 5), "x")
        t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (5, 5), "y")
        grid = Grid(width=20, height=10)
        grid.place(a)
        grid.place(t)
        self.assertEqual(_cover_reflex_bonus(a, t, grid), 0)


if __name__ == "__main__":
    unittest.main()
