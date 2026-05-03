"""Tests for Batch 13 edge mechanics: armor proficiency penalty,
coup de grace, massive damage, partial charge, fight defensively."""

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
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import (
    _armor_not_proficient_penalty,
    _check_massive_damage,
    _do_attack,
    execute_turn,
)


REGISTRY = default_registry()


def _wizard_in_armor(armor: str | None = None, shield: str | None = None):
    # Wizards are proficient with no armor (armor_proficiencies = "none").
    # Putting them in chainmail should trigger the ACP-on-attacks penalty.
    eq: dict = {"weapon": "quarterstaff"}
    if armor is not None:
        eq["armor"] = armor
    if shield is not None:
        eq["shield"] = shield
    req = CharacterRequest.from_dict({
        "name": "Aurelia", "race": "human", "class": "wizard",
        "alignment": "neutral_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 10, "dex": 14, "con": 14,
                       "int": 16, "wis": 10, "cha": 10}},
        "free_ability_choice": "int",
        "feats": ["combat_expertise", "iron_will"],
        "skill_ranks": {"spellcraft": 1},
        "bonus_languages": [],
        "equipment": eq,
    })
    char = create_character(req, REGISTRY)
    return combatant_from_character(char, REGISTRY, (5, 5), "x")


class TestArmorProficiencyPenalty(unittest.TestCase):
    def test_wizard_unarmored_no_penalty(self):
        w = _wizard_in_armor(armor="none")
        self.assertEqual(_armor_not_proficient_penalty(w), 0)

    def test_wizard_in_chainmail_takes_acp(self):
        w = _wizard_in_armor(armor="chainmail")
        # chainmail ACP = -5
        self.assertEqual(_armor_not_proficient_penalty(w), -5)

    def test_wizard_in_chainmail_with_heavy_shield_stacks(self):
        w = _wizard_in_armor(armor="chainmail",
                             shield="heavy_steel_shield")
        # chainmail -5 + heavy steel shield -2 = -7
        self.assertEqual(_armor_not_proficient_penalty(w), -7)

    def test_fighter_in_chainmail_no_penalty(self):
        # Fighter is proficient with all armor.
        # 5+5+5+2+2+1 = 20
        req = CharacterRequest.from_dict({
            "name": "Edric", "race": "human", "class": "fighter",
            "alignment": "lawful_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 14, "con": 14,
                           "int": 12, "wis": 12, "cha": 11}},
            "free_ability_choice": "str",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"climb": 1, "swim": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "alertness"},
            "equipment": {"weapon": "longsword", "armor": "chainmail",
                          "shield": "heavy_steel_shield"},
        })
        f = combatant_from_character(create_character(req, REGISTRY),
                                     REGISTRY, (5, 5), "x")
        self.assertEqual(_armor_not_proficient_penalty(f), 0)

    def test_natural_attack_monster_no_penalty(self):
        # Goblins have armor_proficiency_categories empty → not modeled.
        g = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (0, 0), "x")
        self.assertEqual(_armor_not_proficient_penalty(g), 0)


class TestCoupDeGrace(unittest.TestCase):
    def test_coup_de_grace_against_helpless_kills_or_damages(self):
        actor = combatant_from_monster(REGISTRY.get_monster("orc"),
                                       (5, 5), "x")
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (6, 5), "y")
        target.add_condition("helpless")
        grid = Grid(width=12, height=12)
        grid.place(actor)
        grid.place(target)
        enc = Encounter.begin(grid, [actor, target], Roller(seed=1))
        before = target.current_hp
        script = BehaviorScript(name="cdg", rules=[
            Rule(do={"composite": "coup_de_grace",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(actor, enc, grid)
        result = execute_turn(actor, intent, enc, grid, Roller(seed=1))
        # Damage was dealt.
        self.assertLess(target.current_hp, before)
        # Event present.
        cdg = [e for e in result.events if e.kind == "coup_de_grace"]
        self.assertEqual(len(cdg), 1)

    def test_coup_de_grace_against_non_helpless_skips(self):
        actor = combatant_from_monster(REGISTRY.get_monster("orc"),
                                       (5, 5), "x")
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (6, 5), "y")
        # No helpless condition.
        grid = Grid(width=12, height=12)
        grid.place(actor)
        grid.place(target)
        enc = Encounter.begin(grid, [actor, target], Roller(seed=1))
        script = BehaviorScript(name="cdg", rules=[
            Rule(do={"composite": "coup_de_grace",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(actor, enc, grid)
        result = execute_turn(actor, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("skip", kinds)


class TestMassiveDamage(unittest.TestCase):
    def test_below_threshold_no_save(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.max_hp = 9999
        g.current_hp = 9999
        result = _check_massive_damage(g, 49, Roller(seed=1))
        self.assertIsNone(result)

    def test_at_threshold_triggers_save(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.max_hp = 9999
        g.current_hp = 9999
        result = _check_massive_damage(g, 50, Roller(seed=1))
        self.assertIsNotNone(result)
        saved, detail = result
        self.assertIn("save_dc", detail)
        self.assertEqual(detail["save_dc"], 15)

    def test_failed_save_kills(self):
        # Force a low roll: with seed=1, the d20 might pass DC 15 at
        # some point. Iterate to find a failure.
        for seed in range(1, 30):
            g = combatant_from_monster(REGISTRY.get_monster("orc"),
                                       (0, 0), "x")
            g.max_hp = 9999
            g.current_hp = 9999
            g.bases["fort_save"] = -100  # ensure fail
            result = _check_massive_damage(g, 60, Roller(seed=seed))
            self.assertIsNotNone(result)
            saved, _ = result
            if not saved:
                self.assertIn("dead", g.conditions)
                return
        self.fail("expected at least one seed where massive damage killed")


class TestPartialCharge(unittest.TestCase):
    def test_partial_charge_uses_one_x_speed(self):
        # Orc speed 30 = 6 squares; partial = 6, regular = 12.
        # Set up target at distance 8: regular charge reaches it,
        # partial charge does NOT.
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (3, 5), "x")
        t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (12, 5), "y")
        t.max_hp = 9999
        t.current_hp = 9999
        grid = Grid(width=20, height=10)
        grid.place(a)
        grid.place(t)
        enc = Encounter.begin(grid, [a, t], Roller(seed=1))
        script = BehaviorScript(name="pc", rules=[
            Rule(do={"composite": "partial_charge",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        # Distance 9 squares; partial charge max 6 → can't reach → skip.
        kinds = [e.kind for e in result.events]
        self.assertIn("skip", kinds)


class TestFightDefensively(unittest.TestCase):
    def test_grants_dodge_ac_and_attack_penalty(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (6, 5), "y")
        t.max_hp = 9999
        t.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(t)
        enc = Encounter.begin(grid, [a, t], Roller(seed=1))
        ac_before = a.ac()
        script = BehaviorScript(name="fd", rules=[
            Rule(do={"composite": "fight_defensively",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        # AC increased by 2 (dodge).
        self.assertEqual(a.ac(), ac_before + 2)
        # An attack event fired.
        attacks = [e for e in result.events if e.kind == "defensive_attack"]
        self.assertEqual(len(attacks), 1)


class TestRangeIncrementMaxCap(unittest.TestCase):
    def test_beyond_max_range_skips(self):
        # Longbow range increment 100 ft; max = 10 × = 1000 ft.
        # Place target 220 squares away (1100 ft). Should skip.
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 5), "x")
        a.attack_options = [{
            "type": "ranged", "name": "Longbow", "weapon_id": "longbow",
            "weapon_category": "martial", "attack_bonus": 5,
            "damage": "1d8", "damage_bonus": 0, "damage_type": "P",
            "crit_range": [20, 20], "crit_multiplier": 3,
            "range_increment": 100, "wield": "two_handed",
        }]
        t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (220, 5), "y")
        grid = Grid(width=300, height=10)
        grid.place(a)
        grid.place(t)
        enc = Encounter.begin(grid, [a, t], Roller(seed=1))
        events: list = []
        _do_attack(a, t, grid, Roller(seed=1), events,
                   label="ranged", encounter=enc, script_options={})
        skip = [e for e in events if e.kind == "skip"]
        self.assertGreater(len(skip), 0)
        self.assertIn("beyond maximum range",
                      skip[0].detail.get("reason", ""))

    def test_thrown_weapon_caps_at_5_increments(self):
        # Dagger range increment 10 ft; max thrown = 5 × = 50 ft.
        # Place target 12 squares away (60 ft) — beyond cap.
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 5), "x")
        a.attack_options = [{
            "type": "ranged", "name": "Dagger (thrown)", "weapon_id": "dagger",
            "weapon_category": "simple", "attack_bonus": 5,
            "damage": "1d4", "damage_bonus": 0, "damage_type": "P",
            "crit_range": [19, 20], "crit_multiplier": 2,
            "range_increment": 10, "wield": "light",
        }]
        t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (12, 5), "y")
        grid = Grid(width=20, height=10)
        grid.place(a)
        grid.place(t)
        enc = Encounter.begin(grid, [a, t], Roller(seed=1))
        events: list = []
        _do_attack(a, t, grid, Roller(seed=1), events,
                   label="ranged", encounter=enc, script_options={})
        skip = [e for e in events if e.kind == "skip"]
        self.assertGreater(len(skip), 0)


class TestGenericBleed(unittest.TestCase):
    def test_bleed_drains_hp_each_round(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.bleed = 2
        before = g.current_hp
        g.tick_round(1)
        self.assertEqual(g.current_hp, before - 2)
        g.tick_round(2)
        self.assertEqual(g.current_hp, before - 4)

    def test_healing_stops_bleed(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.bleed = 2
        g.fast_healing = 5  # any healing stops bleed
        g.current_hp = g.max_hp - 10  # so heal has room
        before = g.current_hp
        g.tick_round(1)
        # Bleed -2 first, then heal +5 → net +3, and bleed cleared.
        self.assertEqual(g.bleed, 0)
        self.assertEqual(g.current_hp, before - 2 + 5)

    def test_undead_immune_to_bleed(self):
        z = combatant_from_monster(REGISTRY.get_monster("skeleton"),
                                   (0, 0), "x")
        z.bleed = 5
        before = z.current_hp
        z.tick_round(1)
        self.assertEqual(z.current_hp, before)


if __name__ == "__main__":
    unittest.main()
