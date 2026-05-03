"""Tests for the attack-tag system.

Covers the four-by-three matrix of attack flavor (non-magical /
magic / force / ghost-touch) × target (corporeal / incorporeal),
plus DR-bypass-by-tag (e.g. dr_10_magic on the gargoyle).
"""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import Monster, default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.inventory import InventoryItem
from dnd.engine.spells import apply_typed_damage, _spell_attack_tags
from dnd.engine.turn_executor import (
    _weapon_attack_tags,
    execute_turn,
)


REGISTRY = default_registry()


def _ghost(position=(0, 0), team="y") -> "Combatant":
    """Build a synthetic incorporeal undead for testing."""
    g = Monster(
        id="phantom", name="Phantom", summary="Test ghost.",
        cr="3", xp=800, alignment="neutral",
        size="medium", type="undead", subtypes=["incorporeal"],
        ability_scores={"str": 0, "dex": 14, "con": 0,
                        "int": 10, "wis": 10, "cha": 14},
        hit_dice="3d8", hp=20, init=2, senses=["darkvision_60"],
        speed=30,
        ac={"total": 13, "touch": 13, "flat_footed": 11,
            "deflection": 2, "dex": 2},
        saves={"fort": 1, "ref": 3, "will": 3},
        bab=2, cmb=0, cmd=12,
        attacks=[{"type": "melee", "name": "incorporeal touch",
                  "attack_bonus": 4, "damage": "1d6",
                  "damage_type": "neg", "crit_range": [20, 20],
                  "crit_multiplier": 2}],
        feats=[], skills={}, languages=[],
        racial_traits=[], equipment=[],
        permanent_conditions=[],
    )
    return combatant_from_monster(g, position, team)


# ---------------------------------------------------------------------------
# Tag derivation
# ---------------------------------------------------------------------------


class TestWeaponTagDerivation(unittest.TestCase):
    def test_mundane_weapon_has_no_tags(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        chosen = a.attack_options[0]
        tags = _weapon_attack_tags(a, chosen)
        self.assertEqual(tags, frozenset())

    def test_plus_one_weapon_gets_magic_tag(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        a.held_items["main_hand"] = InventoryItem(
            instance_id="x", item_id="longsword", item_type="weapon",
            current_hp=10, max_hp=10, hardness=10,
            properties={"enhancement_bonus": 1},
        )
        tags = _weapon_attack_tags(a, a.attack_options[0])
        self.assertIn("magic", tags)

    def test_ghost_touch_weapon_gets_both_tags(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        a.held_items["main_hand"] = InventoryItem(
            instance_id="x", item_id="longsword", item_type="weapon",
            current_hp=10, max_hp=10, hardness=10,
            properties={"special_abilities": ["ghost_touch"]},
        )
        tags = _weapon_attack_tags(a, a.attack_options[0])
        self.assertIn("magic", tags)
        self.assertIn("ghost_touch", tags)

    def test_silver_weapon_material_tag(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        a.held_items["main_hand"] = InventoryItem(
            instance_id="x", item_id="dagger", item_type="weapon",
            current_hp=10, max_hp=10, hardness=10,
            properties={"material": "silver"},
        )
        tags = _weapon_attack_tags(a, a.attack_options[0])
        self.assertIn("silver", tags)
        # Silver alone (alchemical silver) is not magical.
        self.assertNotIn("magic", tags)


class TestSpellTagDerivation(unittest.TestCase):
    def test_spell_always_magic(self):
        spell = REGISTRY.get_spell("magic_missile")
        tags = _spell_attack_tags(spell, "force")
        self.assertIn("magic", tags)
        self.assertIn("force", tags)

    def test_spell_descriptors_become_tags(self):
        # Magic missile has descriptor "force" too.
        spell = REGISTRY.get_spell("magic_missile")
        tags = _spell_attack_tags(spell, "force")
        # Descriptor "force" matches the damage_type tag — single entry.
        self.assertIn("force", tags)


# ---------------------------------------------------------------------------
# Incorporeal target × attack flavor matrix
# ---------------------------------------------------------------------------


class TestIncorporealVsAttacks(unittest.TestCase):
    def test_mundane_weapon_cannot_hurt_ghost(self):
        # Orc with default falchion (no enhancement) attacks the ghost.
        # Result: every hit converts to 'incorporeal: non-magical
        # attack — full immunity'.
        for seed in range(1, 11):
            a = combatant_from_monster(REGISTRY.get_monster("orc"),
                                       (5, 5), "x")
            for opt in a.attack_options:
                opt["attack_bonus"] = 100  # always hit
            t = _ghost(position=(6, 5))
            hp_before = t.current_hp
            grid = Grid(width=12, height=12)
            grid.place(a)
            grid.place(t)
            enc = Encounter.begin(grid, [a, t], Roller(seed=seed))
            script = BehaviorScript(name="atk", rules=[
                Rule(do={"composite": "full_attack",
                         "args": {"target": "enemy.closest"}}),
            ])
            intent = Interpreter(script).pick_turn(a, enc, grid)
            execute_turn(a, intent, enc, grid, Roller(seed=seed))
            self.assertEqual(t.current_hp, hp_before,
                             f"seed {seed}: mundane attack damaged ghost")

    def test_plus_one_weapon_rolls_50pct_miss_vs_ghost(self):
        # +1 weapon: each hit has 50% chance to be ignored. Tally over
        # many seeds.
        misses = 0
        attempts = 30
        for seed in range(1, attempts + 1):
            a = combatant_from_monster(REGISTRY.get_monster("orc"),
                                       (5, 5), "x")
            for opt in a.attack_options:
                opt["attack_bonus"] = 100
            a.held_items["main_hand"] = InventoryItem(
                instance_id="x", item_id="falchion", item_type="weapon",
                current_hp=10, max_hp=10, hardness=10,
                properties={"enhancement_bonus": 1},
            )
            t = _ghost(position=(6, 5))
            t.max_hp = 9999
            t.current_hp = 9999
            grid = Grid(width=12, height=12)
            grid.place(a)
            grid.place(t)
            enc = Encounter.begin(grid, [a, t], Roller(seed=seed))
            hp_before = t.current_hp
            script = BehaviorScript(name="atk", rules=[
                Rule(do={"composite": "full_attack",
                         "args": {"target": "enemy.closest"}}),
            ])
            intent = Interpreter(script).pick_turn(a, enc, grid)
            execute_turn(a, intent, enc, grid, Roller(seed=seed))
            if t.current_hp == hp_before:
                misses += 1
        # Roughly half should miss; allow wide tolerance.
        self.assertGreater(misses, 5)
        self.assertLess(misses, attempts - 5)

    def test_ghost_touch_weapon_always_damages_ghost(self):
        # Ghost-touch bypasses the 50% miss entirely.
        for seed in range(1, 11):
            a = combatant_from_monster(REGISTRY.get_monster("orc"),
                                       (5, 5), "x")
            for opt in a.attack_options:
                opt["attack_bonus"] = 100
            a.held_items["main_hand"] = InventoryItem(
                instance_id="x", item_id="falchion", item_type="weapon",
                current_hp=10, max_hp=10, hardness=10,
                properties={"special_abilities": ["ghost_touch"]},
            )
            t = _ghost(position=(6, 5))
            t.max_hp = 9999
            t.current_hp = 9999
            grid = Grid(width=12, height=12)
            grid.place(a)
            grid.place(t)
            enc = Encounter.begin(grid, [a, t], Roller(seed=seed))
            hp_before = t.current_hp
            script = BehaviorScript(name="atk", rules=[
                Rule(do={"composite": "full_attack",
                         "args": {"target": "enemy.closest"}}),
            ])
            intent = Interpreter(script).pick_turn(a, enc, grid)
            execute_turn(a, intent, enc, grid, Roller(seed=seed))
            self.assertLess(t.current_hp, hp_before,
                            f"seed {seed}: ghost-touch failed to damage ghost")


# ---------------------------------------------------------------------------
# Spell side: magic missile (force) and fireball-style spells
# ---------------------------------------------------------------------------


class TestIncorporealVsSpellDamage(unittest.TestCase):
    def test_magic_missile_force_always_damages_ghost(self):
        # Force damage bypasses incorporeal's 50% — should always hit.
        target = _ghost()
        roller = Roller(seed=1)
        # Apply force damage 10 times; all should land.
        for _ in range(10):
            hp_before = target.current_hp
            applied, note = apply_typed_damage(
                target, 5, "force",
                attack_tags=frozenset({"magic", "force"}),
                roller=roller,
            )
            self.assertEqual(applied, 5)
            self.assertEqual(note, None)
            target.current_hp = hp_before  # reset for next iteration

    def test_fireball_fire_damage_rolls_50pct_vs_ghost(self):
        # Fire damage IS magic but not force; should miss ~half the
        # time. Sample seeds.
        misses = 0
        attempts = 30
        for seed in range(1, attempts + 1):
            target = _ghost()
            roller = Roller(seed=seed)
            applied, note = apply_typed_damage(
                target, 10, "fire",
                attack_tags=frozenset({"magic", "fire"}),
                roller=roller,
            )
            if applied == 0:
                misses += 1
        self.assertGreater(misses, 5)
        self.assertLess(misses, attempts - 5)

    def test_no_magic_tag_means_incorporeal_immune(self):
        # Synthetic damage with no magic tag (e.g., a hypothetical
        # mundane environmental hazard) cannot harm ghost.
        target = _ghost()
        roller = Roller(seed=1)
        applied, note = apply_typed_damage(
            target, 100, "fire",
            attack_tags=frozenset(),  # no magic
            roller=roller,
        )
        self.assertEqual(applied, 0)
        self.assertEqual(note, "incorporeal_immune")


# ---------------------------------------------------------------------------
# DR bypass via tags: dr_10_magic
# ---------------------------------------------------------------------------


class TestDrBypassByTag(unittest.TestCase):
    def test_mundane_weapon_blocked_by_dr_magic(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        for opt in a.attack_options:
            opt["attack_bonus"] = 100
            opt["damage_bonus"] = 0
            opt["damage"] = "1d6"  # small damage so DR matters
        t = combatant_from_monster(REGISTRY.get_monster("gargoyle"),
                                   (6, 5), "y")
        t.max_hp = 9999
        t.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(t)
        enc = Encounter.begin(grid, [a, t], Roller(seed=1))
        # Attack 5 times; DR 10/magic eats every hit (average dmg 3-4).
        # Verify at least one full_attack event shows damage absorbed.
        script = BehaviorScript(name="atk", rules=[
            Rule(do={"composite": "full_attack",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        attack_evts = [e for e in result.events
                       if e.kind.startswith("full_attack")]
        self.assertGreater(len(attack_evts), 0)
        # No damage should have leaked through DR.
        damages = [e.detail.get("damage", 0) for e in attack_evts]
        self.assertTrue(all(d == 0 for d in damages),
                        f"expected DR to absorb all damage; got {damages}")

    def test_plus_one_weapon_bypasses_dr_magic(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        for opt in a.attack_options:
            opt["attack_bonus"] = 100
            opt["damage"] = "1d8"
            opt["damage_bonus"] = 5
        a.held_items["main_hand"] = InventoryItem(
            instance_id="x", item_id="falchion", item_type="weapon",
            current_hp=10, max_hp=10, hardness=10,
            properties={"enhancement_bonus": 1},
        )
        t = combatant_from_monster(REGISTRY.get_monster("gargoyle"),
                                   (6, 5), "y")
        t.max_hp = 9999
        t.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(t)
        enc = Encounter.begin(grid, [a, t], Roller(seed=1))
        hp_before = t.current_hp
        script = BehaviorScript(name="atk", rules=[
            Rule(do={"composite": "full_attack",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        execute_turn(a, intent, enc, grid, Roller(seed=1))
        self.assertLess(t.current_hp, hp_before,
                        "magic weapon should bypass DR/magic")


if __name__ == "__main__":
    unittest.main()
