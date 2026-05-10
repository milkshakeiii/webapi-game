"""Tests for the HP state machine: -CON death threshold, disabled,
dying-bleed.

PF1 RAW: HP <= -CON kills. HP exactly 0 = disabled. HP -1 to -CON+1 =
dying. Undead/constructs are destroyed at HP 0.
"""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import (
    combatant_from_character,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.actions import _validate_intent
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import _apply_post_damage_state


REGISTRY = default_registry()


# ---------------------------------------------------------------------------
# Death threshold
# ---------------------------------------------------------------------------


class TestDeathThreshold(unittest.TestCase):
    def test_orc_threshold_is_minus_con(self):
        orc = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        # Orc has CON 12.
        self.assertEqual(orc.death_threshold, -12)

    def test_goblin_threshold(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        # Goblin has CON 12.
        self.assertEqual(g.death_threshold, -12)

    def test_skeleton_destroyed_at_zero(self):
        # Undead are destroyed at HP 0.
        sk = combatant_from_monster(
            REGISTRY.get_monster("skeleton"), (0, 0), "x",
        )
        self.assertEqual(sk.death_threshold, 0)

    def test_zombie_destroyed_at_zero(self):
        z = combatant_from_monster(
            REGISTRY.get_monster("human_zombie"), (0, 0), "x",
        )
        self.assertEqual(z.death_threshold, 0)

    def test_character_threshold_uses_final_con(self):
        # Fighter built with CON 14 → threshold -14.
        req = CharacterRequest.from_dict({
            "name": "Edric", "race": "human", "class": "fighter",
            "alignment": "lawful_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 16, "dex": 14, "con": 14,
                           "int": 10, "wis": 10, "cha": 10}},
            "free_ability_choice": "str",
            "feats": ["power_attack", "weapon_focus"],
            "skill_ranks": {"climb": 1, "swim": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "cleave"},
        })
        char = create_character(req, REGISTRY)
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertEqual(c.death_threshold, -14)


# ---------------------------------------------------------------------------
# Post-damage state transitions
# ---------------------------------------------------------------------------


class TestPostDamageState(unittest.TestCase):
    def _goblin(self):
        # Goblin has no ferocity; baseline test subject.
        return combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")

    def test_hp_above_zero_no_state(self):
        g = self._goblin()
        g.current_hp = 3
        _apply_post_damage_state(g)
        self.assertNotIn("dying", g.conditions)
        self.assertNotIn("disabled", g.conditions)
        self.assertNotIn("dead", g.conditions)

    def test_hp_exactly_zero_is_disabled(self):
        g = self._goblin()
        g.current_hp = 0
        _apply_post_damage_state(g)
        self.assertIn("disabled", g.conditions)
        self.assertNotIn("dying", g.conditions)
        self.assertNotIn("dead", g.conditions)

    def test_hp_negative_above_threshold_is_dying(self):
        g = self._goblin()
        # Goblin threshold is -12; -3 is dying.
        g.current_hp = -3
        _apply_post_damage_state(g)
        self.assertIn("dying", g.conditions)
        self.assertNotIn("disabled", g.conditions)
        self.assertNotIn("dead", g.conditions)

    def test_hp_at_threshold_is_dead(self):
        g = self._goblin()
        g.current_hp = -12
        _apply_post_damage_state(g)
        self.assertIn("dead", g.conditions)
        self.assertNotIn("dying", g.conditions)

    def test_hp_below_threshold_is_dead(self):
        g = self._goblin()
        g.current_hp = -50
        _apply_post_damage_state(g)
        self.assertIn("dead", g.conditions)

    def test_skeleton_dies_at_zero(self):
        sk = combatant_from_monster(
            REGISTRY.get_monster("skeleton"), (0, 0), "x",
        )
        sk.current_hp = 0
        _apply_post_damage_state(sk)
        self.assertIn("dead", sk.conditions)
        self.assertNotIn("disabled", sk.conditions)
        self.assertNotIn("dying", sk.conditions)

    def test_disabled_clears_dying_when_healed_back(self):
        g = self._goblin()
        # Wound to dying.
        g.current_hp = -3
        _apply_post_damage_state(g)
        self.assertIn("dying", g.conditions)
        # Heal up to 0 — now disabled, not dying.
        g.current_hp = 0
        _apply_post_damage_state(g)
        self.assertIn("disabled", g.conditions)
        self.assertNotIn("dying", g.conditions)


# ---------------------------------------------------------------------------
# Tick-round bleed
# ---------------------------------------------------------------------------


class TestDyingBleed(unittest.TestCase):
    def test_dying_creature_loses_one_hp_per_round(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        g.current_hp = -3
        _apply_post_damage_state(g)
        self.assertIn("dying", g.conditions)
        g.tick_round(2)
        self.assertEqual(g.current_hp, -4)
        g.tick_round(3)
        self.assertEqual(g.current_hp, -5)

    def test_dying_eventually_kills_at_threshold(self):
        # Goblin threshold -12. Start at -11; 1 tick puts it at -12 = dead.
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        g.current_hp = -11
        _apply_post_damage_state(g)
        self.assertIn("dying", g.conditions)
        g.tick_round(2)
        self.assertIn("dead", g.conditions)
        self.assertNotIn("dying", g.conditions)

    def test_disabled_does_not_bleed(self):
        # HP=0 disabled is stable in itself; no per-round HP loss.
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        g.current_hp = 0
        _apply_post_damage_state(g)
        self.assertIn("disabled", g.conditions)
        g.tick_round(2)
        self.assertEqual(g.current_hp, 0)
        self.assertNotIn("dying", g.conditions)

    def test_stable_suppresses_dying_bleed(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        g.current_hp = -5
        _apply_post_damage_state(g)
        self.assertIn("dying", g.conditions)
        g.add_condition("stable")
        g.tick_round(2)
        # Stable → no bleed even though dying.
        self.assertEqual(g.current_hp, -5)


# ---------------------------------------------------------------------------
# Disabled action restriction
# ---------------------------------------------------------------------------


class TestDisabledValidation(unittest.TestCase):
    def _disabled_goblin(self):
        g = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        g.add_condition("disabled")
        return g

    def test_disabled_cannot_full_round(self):
        g = self._disabled_goblin()
        grid = Grid(width=5, height=5)
        grid.place(g)
        do = {"slots": {"full_round": {"type": "charge", "target": (4, 4)}}}
        self.assertIsNotNone(_validate_intent(g, do, grid))

    def test_disabled_cannot_combine_standard_and_move(self):
        g = self._disabled_goblin()
        grid = Grid(width=5, height=5)
        grid.place(g)
        do = {
            "standard": {"type": "attack", "target": "enemy.closest"},
            "move": {"type": "move_toward", "target": "enemy.closest"},
        }
        self.assertIsNotNone(_validate_intent(g, do, grid))

    def test_disabled_can_take_a_single_standard(self):
        g = self._disabled_goblin()
        grid = Grid(width=5, height=5)
        grid.place(g)
        do = {"standard": {"type": "attack", "target": "enemy.closest"}}
        self.assertIsNone(_validate_intent(g, do, grid))

    def test_disabled_can_take_a_single_move(self):
        g = self._disabled_goblin()
        grid = Grid(width=5, height=5)
        grid.place(g)
        do = {"move": {"type": "move_toward", "target": "enemy.closest"}}
        self.assertIsNone(_validate_intent(g, do, grid))


if __name__ == "__main__":
    unittest.main()
