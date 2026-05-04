"""Tests for the audit-driven fixes to Phase 4.2 cantrips:

- Bleed: requires target at -1 or fewer HP (not <= 0)
- Virtue: grants 1 temporary HP (separate pool, not hp_max)
- Guidance: +1 competence on a single d20 roll, discharged on use

Plus the new infrastructure: temp HP pool with stacking rules,
single-use buff consumption from skill / save / attack rolls."""

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
from dnd.engine.modifiers import Modifier
from dnd.engine.skills import skill_check
from dnd.engine.spells import roll_save
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


def _cleric():
    req = CharacterRequest.from_dict({
        "name": "Cael", "race": "human", "class": "cleric",
        "alignment": "neutral_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 10, "dex": 10, "con": 14,
                       "int": 10, "wis": 16, "cha": 14}},
        "free_ability_choice": "wis",
        "feats": ["alertness", "iron_will"],
        "skill_ranks": {"heal": 1, "knowledge_religion": 1},
        "bonus_languages": [],
    })
    char = create_character(req, REGISTRY)
    return combatant_from_character(char, REGISTRY, (5, 5), "x")


# ---------------------------------------------------------------------------
# Bleed: HP threshold
# ---------------------------------------------------------------------------


class TestBleedHpThreshold(unittest.TestCase):
    def test_bleed_skips_target_at_zero_hp(self):
        # RAW: bleed requires "-1 or fewer". A creature at 0 HP
        # (disabled) is NOT a valid target — bug in the prior impl.
        c = _cleric()
        c.casting_type = "prepared"
        c.prepared_spells = {0: ["bleed"]}
        c.castable_spells = {"bleed"}
        c.resources["spell_slot_0"] = 4
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (8, 5), "y")
        target.current_hp = 0  # disabled, not dying
        grid = Grid(width=12, height=12)
        grid.place(c)
        grid.place(target)
        enc = Encounter.begin(grid, [c, target], Roller(seed=1))
        script = BehaviorScript(name="b", rules=[
            Rule(do={"standard": {"type": "cast", "spell": "bleed",
                                  "spell_level": 0, "target": target}}),
        ])
        intent = Interpreter(script).pick_turn(c, enc, grid)
        execute_turn(c, intent, enc, grid, Roller(seed=1))
        self.assertEqual(target.bleed, 0)

    def test_bleed_targets_dying_at_minus_one(self):
        c = _cleric()
        c.casting_type = "prepared"
        c.prepared_spells = {0: ["bleed"]}
        c.castable_spells = {"bleed"}
        c.resources["spell_slot_0"] = 4
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (8, 5), "y")
        target.current_hp = -1
        target.add_condition("dying")
        target.add_condition("stable")
        grid = Grid(width=12, height=12)
        grid.place(c)
        grid.place(target)
        enc = Encounter.begin(grid, [c, target], Roller(seed=1))
        # Find a seed where target fails Will save.
        for seed in range(1, 50):
            target.bleed = 0
            script = BehaviorScript(name="b", rules=[
                Rule(do={"standard": {"type": "cast", "spell": "bleed",
                                      "spell_level": 0, "target": target}}),
            ])
            intent = Interpreter(script).pick_turn(c, enc, grid)
            execute_turn(c, intent, enc, grid, Roller(seed=seed))
            if target.bleed > 0:
                return
        self.fail("no seed in 1..49 caused bleed (Will save kept passing)")


# ---------------------------------------------------------------------------
# Virtue: temporary HP
# ---------------------------------------------------------------------------


class TestVirtueTempHp(unittest.TestCase):
    def test_virtue_grants_temp_hp_pool(self):
        c = _cleric()
        c.casting_type = "prepared"
        c.prepared_spells = {0: ["virtue"]}
        c.castable_spells = {"virtue"}
        c.resources["spell_slot_0"] = 4
        ally = combatant_from_monster(REGISTRY.get_monster("orc"),
                                      (5, 6), "x")
        before_max = ally.max_hp
        before_temp = ally.temp_hp
        grid = Grid(width=12, height=12)
        grid.place(c)
        grid.place(ally)
        enc = Encounter.begin(grid, [c, ally], Roller(seed=1))
        script = BehaviorScript(name="v", rules=[
            Rule(do={"standard": {"type": "cast", "spell": "virtue",
                                  "spell_level": 0, "target": ally}}),
        ])
        intent = Interpreter(script).pick_turn(c, enc, grid)
        execute_turn(c, intent, enc, grid, Roller(seed=1))
        # max_hp UNCHANGED; temp_hp +1.
        self.assertEqual(ally.max_hp, before_max)
        self.assertEqual(ally.temp_hp, before_temp + 1)

    def test_temp_hp_absorbs_damage_first(self):
        ally = combatant_from_monster(REGISTRY.get_monster("orc"),
                                      (0, 0), "x")
        ally.apply_temp_hp(3, expires_round=10)
        before_hp = ally.current_hp
        ally.take_damage(2)
        # Temp HP took the hit.
        self.assertEqual(ally.current_hp, before_hp)
        self.assertEqual(ally.temp_hp, 1)

    def test_temp_hp_does_not_stack(self):
        ally = combatant_from_monster(REGISTRY.get_monster("orc"),
                                      (0, 0), "x")
        ally.apply_temp_hp(3, expires_round=10)
        ally.apply_temp_hp(2, expires_round=10)
        # Higher pool wins (3, not 5).
        self.assertEqual(ally.temp_hp, 3)
        ally.apply_temp_hp(7, expires_round=10)
        self.assertEqual(ally.temp_hp, 7)

    def test_temp_hp_expires_in_tick_round(self):
        ally = combatant_from_monster(REGISTRY.get_monster("orc"),
                                      (0, 0), "x")
        ally.apply_temp_hp(5, expires_round=3)
        ally.tick_round(current_round=4, roller=Roller(seed=1))
        self.assertEqual(ally.temp_hp, 0)


# ---------------------------------------------------------------------------
# Guidance: discharge-on-use
# ---------------------------------------------------------------------------


class TestGuidanceDischarge(unittest.TestCase):
    def _setup_with_guidance(self):
        c = _cleric()
        c.casting_type = "prepared"
        c.prepared_spells = {0: ["guidance"]}
        c.castable_spells = {"guidance"}
        c.resources["spell_slot_0"] = 4
        ally = combatant_from_monster(REGISTRY.get_monster("orc"),
                                      (5, 6), "x")
        grid = Grid(width=12, height=12)
        grid.place(c)
        grid.place(ally)
        enc = Encounter.begin(grid, [c, ally], Roller(seed=1))
        script = BehaviorScript(name="g", rules=[
            Rule(do={"standard": {"type": "cast", "spell": "guidance",
                                  "spell_level": 0, "target": ally}}),
        ])
        intent = Interpreter(script).pick_turn(c, enc, grid)
        execute_turn(c, intent, enc, grid, Roller(seed=1))
        return c, ally, enc, grid

    def test_guidance_applies_modifiers_to_all_d20_targets(self):
        c, ally, enc, grid = self._setup_with_guidance()
        for target in (
            "attack", "fort_save", "ref_save", "will_save", "skill_check",
        ):
            mods = list(ally.modifiers.for_target(target))
            self.assertTrue(
                any(m.source.startswith("single_use:guidance:")
                    for m in mods),
                f"missing guidance mod on {target}",
            )
        # Source registered in pending_single_use_sources.
        self.assertTrue(any(
            s.startswith("single_use:guidance:")
            for s in ally.pending_single_use_sources
        ))

    def test_guidance_consumed_by_first_skill_check(self):
        c, ally, enc, grid = self._setup_with_guidance()
        # Roll a skill check — should consume guidance.
        skill_check(ally, "perception", dc=10, roller=Roller(seed=1),
                    registry=REGISTRY)
        # All single-use mods cleared.
        for target in (
            "attack", "fort_save", "ref_save", "will_save", "skill_check",
        ):
            mods = list(ally.modifiers.for_target(target))
            self.assertFalse(
                any(m.source.startswith("single_use:guidance:")
                    for m in mods),
                f"guidance mod still present on {target} after skill check",
            )
        self.assertEqual(ally.pending_single_use_sources, set())

    def test_guidance_consumed_by_first_save(self):
        c, ally, enc, grid = self._setup_with_guidance()
        roll_save(ally, "will", dc=15, roller=Roller(seed=1))
        # Cleared.
        mods = list(ally.modifiers.for_target("attack"))
        self.assertFalse(any(
            m.source.startswith("single_use:guidance:") for m in mods
        ))


if __name__ == "__main__":
    unittest.main()
