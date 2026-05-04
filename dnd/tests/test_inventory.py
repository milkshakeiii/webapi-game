"""Tests for the inventory subsystem: held items, carried items, and
the disarm / sunder / steal maneuvers operating on real items."""

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
from dnd.engine.inventory import (
    InventoryItem,
    make_consumable_item,
    make_weapon_item,
)
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


def _fighter(team="x", pos=(5, 5)):
    # 5+5+5+2+2+1 = 20.
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
        "class_choices": {"fighter_bonus_feat": "combat_reflexes"},
    })
    char = create_character(req, REGISTRY)
    return combatant_from_character(char, REGISTRY, pos, team)


class TestInventoryItem(unittest.TestCase):
    def test_take_damage_below_hardness_absorbs_fully(self):
        item = InventoryItem(
            instance_id="i1", item_id="longsword", item_type="weapon",
            current_hp=20, max_hp=20, hardness=10,
        )
        loss = item.take_damage(5)
        self.assertEqual(loss, 0)
        self.assertEqual(item.current_hp, 20)

    def test_take_damage_above_hardness_subtracts_difference(self):
        item = InventoryItem(
            instance_id="i1", item_id="longsword", item_type="weapon",
            current_hp=20, max_hp=20, hardness=10,
        )
        loss = item.take_damage(15)
        self.assertEqual(loss, 5)
        self.assertEqual(item.current_hp, 15)

    def test_at_half_hp_item_is_broken(self):
        item = InventoryItem(
            instance_id="i1", item_id="longsword", item_type="weapon",
            current_hp=20, max_hp=20, hardness=0,
        )
        item.take_damage(11)
        self.assertTrue(item.broken)

    def test_destroyed_at_zero_hp(self):
        item = InventoryItem(
            instance_id="i1", item_id="longsword", item_type="weapon",
            current_hp=5, max_hp=20, hardness=0,
        )
        item.take_damage(100)
        self.assertEqual(item.current_hp, 0)
        self.assertTrue(item.is_destroyed())


class TestCharacterInventory(unittest.TestCase):
    def test_fighter_held_items_populated(self):
        f = _fighter()
        # Default fighter loadout: longsword + chainmail + heavy steel shield.
        self.assertIn("main_hand", f.held_items)
        self.assertIn("armor", f.held_items)
        self.assertIn("shield", f.held_items)
        self.assertEqual(f.held_items["main_hand"].item_id, "longsword")
        self.assertGreater(f.held_items["main_hand"].max_hp, 0)
        self.assertGreater(f.held_items["main_hand"].hardness, 0)


class TestDisarm(unittest.TestCase):
    def test_disarm_removes_weapon_from_held_items(self):
        attacker = _fighter()
        target = _fighter(team="y", pos=(6, 5))
        # Force the attacker's CMB high so disarm always succeeds.
        attacker.bases["cmb"] = 30
        target.bases["cmd"] = 5
        grid = Grid(width=20, height=10)
        grid.place(attacker)
        grid.place(target)
        enc = Encounter.begin(grid, [attacker, target], Roller(seed=1))
        # Pre-state: target has a longsword.
        self.assertEqual(target.held_items["main_hand"].item_id,
                         "longsword")
        script = BehaviorScript(name="d", rules=[
            Rule(do={"composite": "disarm",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(attacker, enc, grid)
        execute_turn(attacker, intent, enc, grid, Roller(seed=1))
        # Weapon removed from held_items.
        self.assertNotIn("main_hand", target.held_items)

    def test_disarm_high_margin_transfers_to_attacker(self):
        attacker = _fighter()
        target = _fighter(team="y", pos=(6, 5))
        attacker.bases["cmb"] = 50
        target.bases["cmd"] = 5
        grid = Grid(width=20, height=10)
        grid.place(attacker)
        grid.place(target)
        enc = Encounter.begin(grid, [attacker, target], Roller(seed=1))
        script = BehaviorScript(name="d", rules=[
            Rule(do={"composite": "disarm",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(attacker, enc, grid)
        execute_turn(attacker, intent, enc, grid, Roller(seed=1))
        # On margin ≥ 10, the weapon transfers to the attacker.
        # CMB 50 vs CMD 5 → margin ≥ 45 → transfers.
        ids = [it.item_id for it in attacker.carried_items]
        self.assertIn("longsword", ids)


class TestSunder(unittest.TestCase):
    def test_sunder_damages_weapon(self):
        attacker = _fighter()
        target = _fighter(team="y", pos=(6, 5))
        attacker.bases["cmb"] = 30
        target.bases["cmd"] = 5
        # Weak weapon: lower current_hp and hardness so the test is
        # deterministic.
        target.held_items["main_hand"].max_hp = 100
        target.held_items["main_hand"].current_hp = 100
        target.held_items["main_hand"].hardness = 0
        grid = Grid(width=20, height=10)
        grid.place(attacker)
        grid.place(target)
        enc = Encounter.begin(grid, [attacker, target], Roller(seed=1))
        before_hp = target.held_items["main_hand"].current_hp
        script = BehaviorScript(name="s", rules=[
            Rule(do={"composite": "sunder",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(attacker, enc, grid)
        execute_turn(attacker, intent, enc, grid, Roller(seed=1))
        # Weapon took some HP damage.
        self.assertLess(target.held_items["main_hand"].current_hp,
                        before_hp)


class TestSteal(unittest.TestCase):
    def test_steal_with_no_carried_items_skips(self):
        attacker = _fighter()
        target = _fighter(team="y", pos=(6, 5))
        attacker.bases["cmb"] = 30
        target.bases["cmd"] = 5
        grid = Grid(width=20, height=10)
        grid.place(attacker)
        grid.place(target)
        enc = Encounter.begin(grid, [attacker, target], Roller(seed=1))
        script = BehaviorScript(name="st", rules=[
            Rule(do={"composite": "steal",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(attacker, enc, grid)
        execute_turn(attacker, intent, enc, grid, Roller(seed=1))
        self.assertEqual(attacker.carried_items, [])

    def test_steal_with_carried_item_transfers(self):
        attacker = _fighter()
        target = _fighter(team="y", pos=(6, 5))
        attacker.bases["cmb"] = 30
        target.bases["cmd"] = 5
        # Plant a potion on the target.
        item = make_consumable_item("potion_cure_light")
        target.carried_items.append(item)
        grid = Grid(width=20, height=10)
        grid.place(attacker)
        grid.place(target)
        enc = Encounter.begin(grid, [attacker, target], Roller(seed=1))
        script = BehaviorScript(name="st", rules=[
            Rule(do={"composite": "steal",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(attacker, enc, grid)
        execute_turn(attacker, intent, enc, grid, Roller(seed=1))
        # Potion moved.
        self.assertEqual(target.carried_items, [])
        self.assertEqual(len(attacker.carried_items), 1)
        self.assertEqual(attacker.carried_items[0].item_id,
                         "potion_cure_light")


if __name__ == "__main__":
    unittest.main()
