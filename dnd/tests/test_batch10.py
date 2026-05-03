"""Tests for Batch 10 — flipping the remaining PARTIALs to IMPLEMENTED:
maximize true-max-dice via roller, quicken swift cast, ride-by-attack
charge continuation, trample composite."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.spells import cast_spell
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


class TestRollerTakeMax(unittest.TestCase):
    def test_take_max_returns_max_face(self):
        r = Roller(seed=1)
        result = r.roll("5d6", take_max=True)
        self.assertEqual(result.total, 30)
        self.assertEqual(result.terms[0].rolls, (6, 6, 6, 6, 6))

    def test_take_max_handles_flat_modifiers(self):
        r = Roller(seed=1)
        result = r.roll("3d4+2", take_max=True)
        self.assertEqual(result.total, 14)  # 12 + 2

    def test_take_max_default_is_random(self):
        r = Roller(seed=1)
        a = r.roll("5d6")
        # With 5d6, max=30. Random rolls almost always less.
        self.assertLess(a.total, 30)


class TestQuickenSpellSwiftCast(unittest.TestCase):
    def test_quicken_routes_through_swift_slot(self):
        # A wizard with the quicken_spell feat fires a magic missile
        # via the swift slot. The cast should consume a slot 4 levels
        # above the spell's base level (1+4=5).
        from dnd.engine.characters import CharacterRequest, create_character
        from dnd.engine.combatant import combatant_from_character
        # Wizard with enough levels to reach slot level 5.
        # Use a level plan that gives slot_5 access.
        # For simplicity, set resources directly post-construction.
        req = CharacterRequest.from_dict({
            "name": "Quick", "race": "elf", "class": "wizard",
            "alignment": "neutral_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 8, "dex": 14, "con": 14,
                           "int": 16, "wis": 12, "cha": 10}},
            "feats": ["quicken_spell"],
            "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
            "bonus_languages": [],
        })
        char = create_character(req, REGISTRY)
        wizard = combatant_from_character(char, REGISTRY, (5, 5), "x")
        wizard.resources["spell_slot_5"] = 1
        wizard.resources["spell_slot_1"] = 1  # baseline
        wizard.castable_spells = {"magic_missile"}
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (10, 5), "y")
        grid = Grid(width=20, height=10)
        grid.place(wizard)
        grid.place(target)
        enc = Encounter.begin(grid, [wizard, target], Roller(seed=1))
        slot5_before = wizard.resources["spell_slot_5"]
        slot1_before = wizard.resources["spell_slot_1"]
        # Quickened cast in swift slot.
        script = BehaviorScript(name="quicken", rules=[
            Rule(do={"swift": {
                "type": "cast", "spell": "magic_missile",
                "spell_level": 1, "metamagic": ["quicken_spell"],
                "target": "enemy.closest", "defensive": False,
            }}),
        ])
        intent = Interpreter(script).pick_turn(wizard, enc, grid)
        execute_turn(wizard, intent, enc, grid, Roller(seed=1))
        # 1st-level slot untouched, 5th-level slot consumed.
        self.assertEqual(wizard.resources["spell_slot_1"], slot1_before)
        self.assertEqual(
            wizard.resources["spell_slot_5"], slot5_before - 1,
        )

    def test_swift_cast_without_quicken_skips(self):
        from dnd.engine.characters import CharacterRequest, create_character
        from dnd.engine.combatant import combatant_from_character
        req = CharacterRequest.from_dict({
            "name": "Slow", "race": "elf", "class": "wizard",
            "alignment": "neutral_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 8, "dex": 14, "con": 14,
                           "int": 16, "wis": 12, "cha": 10}},
            "feats": ["combat_expertise"],
            "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
            "bonus_languages": [],
        })
        char = create_character(req, REGISTRY)
        wizard = combatant_from_character(char, REGISTRY, (5, 5), "x")
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (10, 5), "y")
        grid = Grid(width=20, height=10)
        grid.place(wizard)
        grid.place(target)
        enc = Encounter.begin(grid, [wizard, target], Roller(seed=1))
        # Plain swift cast (no quicken metamagic) → skip.
        script = BehaviorScript(name="bad_swift", rules=[
            Rule(do={"swift": {
                "type": "cast", "spell": "magic_missile",
                "spell_level": 1, "target": "enemy.closest",
                "defensive": False,
            }}),
        ])
        intent = Interpreter(script).pick_turn(wizard, enc, grid)
        result = execute_turn(wizard, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("skip", kinds)


class TestRideByAttack(unittest.TestCase):
    def test_ride_by_continues_past_target(self):
        # Set up: actor at (3, 5), target at (8, 5). Mount with reach.
        # Total charge = 2× speed. Without ride-by: actor stops at (7, 5).
        # With ride-by: actor continues past target.
        attacker = combatant_from_monster(REGISTRY.get_monster("orc"),
                                          (3, 5), "x")
        attacker.attack_options = [{
            "type": "melee",
            "name": "Lance",
            "weapon_id": "lance",
            "weapon_category": "martial",
            "attack_bonus": 100,
            "damage": "1d8",
            "damage_bonus": 0,
            "damage_type": "P",
            "crit_range": [20, 20],
            "crit_multiplier": 3,
            "range_increment": 0,
            "wield": "two_handed",
        }]
        attacker.extra_feats = ["mounted_combat", "ride_by_attack"]
        # Fake mount link without an actual mount — set mount_id to a
        # dummy so charge thinks we're mounted; we skip a real mount
        # to keep movement simple.
        attacker.mount_id = "fake_mount"
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (8, 5), "y")
        target.max_hp = 9999
        target.current_hp = 9999
        grid = Grid(width=20, height=10)
        grid.place(attacker)
        grid.place(target)
        enc = Encounter.begin(grid, [attacker, target], Roller(seed=1))
        script = BehaviorScript(name="rb", rules=[
            Rule(do={"composite": "charge", "args": {
                "target": "enemy.closest", "ride_by": True,
            }}),
        ])
        intent = Interpreter(script).pick_turn(attacker, enc, grid)
        result = execute_turn(attacker, intent, enc, grid, Roller(seed=1))
        # Actor should have moved past target's column; final x > 7.
        self.assertGreater(attacker.position[0], 7)
        # And there should be at least one ride_by_step event.
        rb_steps = [e for e in result.events if e.kind == "move"
                    and e.detail.get("kind") == "ride_by_step"]
        self.assertGreater(len(rb_steps), 0)


class TestTrample(unittest.TestCase):
    def test_trample_damages_target_and_knocks_prone_on_failed_save(self):
        # Setup: rider on a mount adjacent to a target. Use a wolf as the
        # mount stand-in (it has bite + trip natural attacks). Trample
        # uses the mount's first attack as a hoof stand-in.
        # Reset target's reflex save to a guaranteed failure.
        rider = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        rider.extra_feats = ["mounted_combat", "trample"]
        mount = combatant_from_monster(REGISTRY.get_monster("wolf"),
                                       (6, 5), "x")
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (7, 5), "y")
        target.bases["ref_save"] = -100
        target.max_hp = 9999
        target.current_hp = 9999
        grid = Grid(width=20, height=10)
        grid.place(rider)
        grid.place(mount)
        grid.place(target)
        enc = Encounter.begin(grid, [rider, mount, target], Roller(seed=1))
        # Link rider to mount manually.
        rider.mount_id = mount.id
        mount.rider_id = rider.id
        rider.position = mount.position
        for sq in [s for s, cid in grid._occupancy.items() if cid == rider.id]:
            del grid._occupancy[sq]
        # Trample!
        script = BehaviorScript(name="trample", rules=[
            Rule(do={"composite": "trample", "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(rider, enc, grid)
        before_hp = target.current_hp
        result = execute_turn(rider, intent, enc, grid, Roller(seed=1))
        # Damage was dealt.
        self.assertLess(target.current_hp, before_hp)
        # Target is prone (since ref_save=-100 → save fails).
        self.assertIn("prone", target.conditions)
        # Trample event present.
        trample_events = [e for e in result.events if e.kind == "trample"]
        self.assertEqual(len(trample_events), 1)

    def test_trample_requires_mount(self):
        rider = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        rider.extra_feats = ["trample"]
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (6, 5), "y")
        grid = Grid(width=20, height=10)
        grid.place(rider)
        grid.place(target)
        enc = Encounter.begin(grid, [rider, target], Roller(seed=1))
        script = BehaviorScript(name="trample", rules=[
            Rule(do={"composite": "trample", "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(rider, enc, grid)
        result = execute_turn(rider, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("skip", kinds)


if __name__ == "__main__":
    unittest.main()
