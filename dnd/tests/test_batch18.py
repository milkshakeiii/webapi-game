"""Tests for Batch 18: weapon brace, double weapon, regen floor."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.inventory import make_weapon_item
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


class TestBraceVsCharge(unittest.TestCase):
    def test_bracing_wielder_attacks_charger(self):
        # A defender braces a longspear (has_brace=true). When a
        # charger arrives adjacent, the defender gets a free attack
        # at double damage before the charge attack resolves.
        defender = combatant_from_monster(REGISTRY.get_monster("orc"),
                                          (8, 5), "x")
        # Replace defender's weapon with a longspear.
        defender.attack_options = [{
            "type": "melee", "name": "Longspear", "weapon_id": "longspear",
            "weapon_category": "simple", "attack_bonus": 100,
            "damage": "1d8", "damage_bonus": 4, "damage_type": "P",
            "crit_range": [20, 20], "crit_multiplier": 3,
            "range_increment": 0, "wield": "two_handed",
        }]
        defender.held_items["main_hand"] = make_weapon_item(
            "longspear", REGISTRY,
        )
        attacker = combatant_from_monster(REGISTRY.get_monster("orc"),
                                          (3, 5), "y")
        grid = Grid(width=20, height=10)
        grid.place(defender)
        grid.place(attacker)
        enc = Encounter.begin(grid, [defender, attacker], Roller(seed=1))
        # Defender readies brace.
        ready_script = BehaviorScript(name="rb", rules=[
            Rule(do={"composite": "ready_brace", "args": {}}),
        ])
        intent = Interpreter(ready_script).pick_turn(defender, enc, grid)
        result = execute_turn(defender, intent, enc, grid, Roller(seed=1))
        self.assertIn("bracing", defender.conditions)
        # Now attacker charges.
        atk_hp_before = attacker.current_hp
        charge_script = BehaviorScript(name="ch", rules=[
            Rule(do={"composite": "charge",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(charge_script).pick_turn(attacker, enc, grid)
        result = execute_turn(attacker, intent, enc, grid, Roller(seed=1))
        # Brace attack fired.
        kinds = [e.kind for e in result.events]
        self.assertIn("brace_attack", kinds)
        # Brace attack damage was doubled (×2 multiplier in the trace).
        brace = [e for e in result.events if e.kind == "brace_attack"][0]
        trace = brace.detail.get("trace") or []
        self.assertTrue(any("×2" in line for line in trace),
                        f"expected ×2 trace; got {trace}")
        # Bracing is consumed.
        self.assertNotIn("bracing", defender.conditions)

    def test_brace_requires_brace_weapon(self):
        # Orc with default falchion (no has_brace): ready_brace skips.
        defender = combatant_from_monster(REGISTRY.get_monster("orc"),
                                          (5, 5), "x")
        grid = Grid(width=12, height=12)
        grid.place(defender)
        enc = Encounter.begin(grid, [defender], Roller(seed=1))
        events: list = []
        from dnd.engine.turn_executor import _do_ready_brace
        _do_ready_brace(defender, {}, enc, events)
        kinds = [e.kind for e in events]
        self.assertIn("skip", kinds)


class TestDoubleWeapon(unittest.TestCase):
    def test_quarterstaff_grants_offhand_attack(self):
        # Build a wizard wielding a quarterstaff (default loadout).
        from dnd.engine.characters import CharacterRequest, create_character
        from dnd.engine.combatant import combatant_from_character
        req = CharacterRequest.from_dict({
            "name": "DoubleWielder", "race": "human", "class": "wizard",
            "alignment": "neutral_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 14, "con": 14,
                           "int": 12, "wis": 12, "cha": 11}},
            "free_ability_choice": "int",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"spellcraft": 1},
            "bonus_languages": [],
        })
        char = create_character(req, REGISTRY)
        c = combatant_from_character(char, REGISTRY, (5, 5), "x")
        # Quarterstaff is a double weapon → 2 attack options.
        offhand_options = [opt for opt in c.attack_options
                           if opt.get("is_offhand")]
        self.assertEqual(len(offhand_options), 1)
        self.assertEqual(offhand_options[0]["weapon_id"], "quarterstaff")


class TestRegenerationNonBypassFloor(unittest.TestCase):
    def test_non_bypass_damage_floors_at_minus_1(self):
        # Troll-style monster: regeneration 5, bypass = {fire, acid}.
        # A massive slashing hit that would normally kill should floor
        # at -1 instead.
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.regeneration = 5
        g.regeneration_bypass = frozenset({"fire", "acid"})
        g.current_hp = 5
        # 100 slashing damage would put HP at -95. Floor should kick
        # in at -1.
        g.take_damage(100, damage_type="S")
        self.assertEqual(g.current_hp, -1)

    def test_bypass_damage_can_kill(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.regeneration = 5
        g.regeneration_bypass = frozenset({"fire", "acid"})
        g.current_hp = 5
        # Fire damage bypasses → not floored.
        g.take_damage(100, damage_type="fire")
        self.assertEqual(g.current_hp, -95)

    def test_no_regen_no_floor(self):
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        # No regeneration → damage applies normally.
        g.current_hp = 5
        g.take_damage(100, damage_type="S")
        self.assertEqual(g.current_hp, -95)

    def test_no_damage_type_no_floor(self):
        # Damage with no type (legacy callers) doesn't trigger floor.
        g = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        g.regeneration = 5
        g.regeneration_bypass = frozenset({"fire", "acid"})
        g.current_hp = 5
        g.take_damage(100)
        self.assertEqual(g.current_hp, -95)


if __name__ == "__main__":
    unittest.main()
