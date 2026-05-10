"""Tests for Phase 4.1 — Detect Evil, First Favored Enemy,
Spontaneous Casting (cleric cure-swap), and per-class feat-pool
restrictions at L1."""

from __future__ import annotations

import unittest

from dnd.engine.characters import (
    CharacterCreationError,
    CharacterRequest,
    create_character,
)
from dnd.engine.combatant import (
    combatant_from_character,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.modifiers import compute_with_context
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


# ---------------------------------------------------------------------------
# Detect Evil
# ---------------------------------------------------------------------------


def _paladin():
    req = CharacterRequest.from_dict({
        "name": "Aravis", "race": "human", "class": "paladin",
        "alignment": "lawful_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 14, "dex": 12, "con": 14,
                       "int": 10, "wis": 13, "cha": 14}},
        "free_ability_choice": "cha",
        "feats": ["alertness", "iron_will"],
        "skill_ranks": {"diplomacy": 1, "heal": 1},
        "bonus_languages": [],
    })
    char = create_character(req, REGISTRY)
    return combatant_from_character(char, REGISTRY, (5, 5), "x")


class TestDetectEvil(unittest.TestCase):
    def test_paladin_detects_evil_orc(self):
        pal = _paladin()
        orc = combatant_from_monster(REGISTRY.get_monster("orc"), (6, 5), "y")
        # Force orc alignment via the monster template (already chaotic_evil).
        grid = Grid(width=12, height=12)
        grid.place(pal)
        grid.place(orc)
        enc = Encounter.begin(grid, [pal, orc], Roller(seed=1))
        script = BehaviorScript(name="d", rules=[
            Rule(do={"composite": "detect_evil",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(pal, enc, grid)
        result = execute_turn(pal, intent, enc, grid, Roller(seed=1))
        evt = next(e for e in result.events if e.kind == "detect_evil")
        self.assertEqual(evt.detail["target_id"], orc.id)
        self.assertTrue(evt.detail["is_evil"])
        self.assertIn("evil", evt.detail["alignment"])

    def test_non_paladin_skips_detect_evil(self):
        # A fighter trying to use detect_evil should be skipped.
        req = CharacterRequest.from_dict({
            "name": "Edric", "race": "human", "class": "fighter",
            "alignment": "lawful_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 16, "dex": 14, "con": 14,
                           "int": 10, "wis": 10, "cha": 10}},
            "free_ability_choice": "str",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"climb": 1, "swim": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "weapon_focus_longsword"},
        })
        fighter = combatant_from_character(
            create_character(req, REGISTRY), REGISTRY, (5, 5), "x")
        orc = combatant_from_monster(REGISTRY.get_monster("orc"), (6, 5), "y")
        grid = Grid(width=12, height=12)
        grid.place(fighter)
        grid.place(orc)
        enc = Encounter.begin(grid, [fighter, orc], Roller(seed=1))
        script = BehaviorScript(name="d", rules=[
            Rule(do={"composite": "detect_evil",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(fighter, enc, grid)
        result = execute_turn(fighter, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertNotIn("detect_evil", kinds)


# ---------------------------------------------------------------------------
# First Favored Enemy
# ---------------------------------------------------------------------------


def _ranger(favored: str | None = None):
    body = {
        "name": "Selka", "race": "human", "class": "ranger",
        "alignment": "neutral_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 14, "dex": 16, "con": 14,
                       "int": 10, "wis": 12, "cha": 8}},
        "free_ability_choice": "dex",
        "feats": ["weapon_focus", "iron_will"],
        "skill_ranks": {"perception": 1, "survival": 1},
        "bonus_languages": [],
    }
    if favored:
        body["class_choices"] = {"first_favored_enemy": favored}
    char = create_character(CharacterRequest.from_dict(body), REGISTRY)
    return combatant_from_character(char, REGISTRY, (5, 5), "x")


class TestFirstFavoredEnemy(unittest.TestCase):
    def test_humanoid_favored_enemy_grants_plus_two_vs_orc(self):
        ranger = _ranger(favored="humanoid")
        orc_ctx = {"target_type": "humanoid",
                   "target_subtypes": ["orc"]}
        baseline = compute_with_context(
            0, ranger.modifiers.for_target("attack"), {},
        )
        vs_orc = compute_with_context(
            0, ranger.modifiers.for_target("attack"), orc_ctx,
        )
        self.assertEqual(vs_orc - baseline, 2)

    def test_no_favored_enemy_pick_means_no_bonus(self):
        ranger = _ranger(favored=None)
        orc_ctx = {"target_type": "humanoid",
                   "target_subtypes": ["orc"]}
        baseline = compute_with_context(
            0, ranger.modifiers.for_target("attack"), {},
        )
        vs_orc = compute_with_context(
            0, ranger.modifiers.for_target("attack"), orc_ctx,
        )
        self.assertEqual(vs_orc, baseline)

    def test_favored_enemy_does_not_apply_to_other_types(self):
        ranger = _ranger(favored="undead")
        orc_ctx = {"target_type": "humanoid",
                   "target_subtypes": ["orc"]}
        baseline = compute_with_context(
            0, ranger.modifiers.for_target("attack"), {},
        )
        vs_orc = compute_with_context(
            0, ranger.modifiers.for_target("attack"), orc_ctx,
        )
        self.assertEqual(vs_orc, baseline)


# ---------------------------------------------------------------------------
# Spontaneous casting (cleric cure-swap)
# ---------------------------------------------------------------------------


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


class TestSpontaneousCasting(unittest.TestCase):
    def test_cleric_can_swap_prep_for_cure_light_wounds(self):
        cleric = _cleric()
        # Prepare bull's_strength at L2 — the cleric will sacrifice
        # this to cast cure_light_wounds (also L2 cure progression
        # for the cleric — actually CLW is L1, so use bless at L1).
        cleric.casting_type = "prepared"
        # Force a spell slot to exist (might not after creation).
        cleric.resources["spell_slot_1"] = 2
        cleric.prepared_spells = {1: ["bless"]}
        cleric.castable_spells = {"bless", "cure_light_wounds"}
        ally = combatant_from_monster(REGISTRY.get_monster("orc"),
                                      (5, 6), "x")
        ally.current_hp = 1
        grid = Grid(width=12, height=12)
        grid.place(cleric)
        grid.place(ally)
        enc = Encounter.begin(grid, [cleric, ally], Roller(seed=1))
        script = BehaviorScript(name="cure", rules=[
            Rule(do={"standard": {
                "type": "cast",
                "spell": "cure_light_wounds",
                "spell_level": 1,
                "spontaneous_cure": True,
                "target": ally,
            }}),
        ])
        intent = Interpreter(script).pick_turn(cleric, enc, grid)
        result = execute_turn(cleric, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("cast", kinds)
        # Bless was burned in place of cure_light_wounds.
        self.assertNotIn("bless", cleric.prepared_spells.get(1, []))
        # Slot consumed.
        self.assertEqual(cleric.resources.get("spell_slot_1", 0), 1)
        # Ally healed.
        self.assertGreater(ally.current_hp, 1)

    def test_non_cleric_cannot_use_spontaneous_cure(self):
        # Wizard with a prepared L1 cure_light_wounds attempt should
        # fail (only clerics + druids — and we only support cleric).
        req = CharacterRequest.from_dict({
            "name": "Wiz", "race": "human", "class": "wizard",
            "alignment": "true_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 8, "dex": 14, "con": 12,
                           "int": 16, "wis": 14, "cha": 10}},
            "free_ability_choice": "int",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
            "bonus_languages": ["draconic"],
        })
        wiz = combatant_from_character(
            create_character(req, REGISTRY), REGISTRY, (5, 5), "x")
        wiz.resources["spell_slot_1"] = 1
        wiz.prepared_spells = {1: ["magic_missile"]}
        wiz.castable_spells = {"magic_missile", "cure_light_wounds"}
        ally = combatant_from_monster(REGISTRY.get_monster("orc"),
                                      (5, 6), "x")
        grid = Grid(width=12, height=12)
        grid.place(wiz)
        grid.place(ally)
        enc = Encounter.begin(grid, [wiz, ally], Roller(seed=1))
        script = BehaviorScript(name="cure", rules=[
            Rule(do={"standard": {
                "type": "cast",
                "spell": "cure_light_wounds",
                "spell_level": 1,
                "spontaneous_cure": True,
                "target": ally,
            }}),
        ])
        intent = Interpreter(script).pick_turn(wiz, enc, grid)
        result = execute_turn(wiz, intent, enc, grid, Roller(seed=1))
        skips = [e for e in result.events if e.kind == "skip"]
        self.assertGreater(len(skips), 0)
        self.assertIn("not a cleric", skips[0].detail["reason"])


# ---------------------------------------------------------------------------
# Fighter feat-pool filter (combat-only)
# ---------------------------------------------------------------------------


class TestFighterFeatPool(unittest.TestCase):
    def test_fighter_l1_bonus_feat_must_be_combat(self):
        body = {
            "name": "Edric", "race": "human", "class": "fighter",
            "alignment": "lawful_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 16, "dex": 14, "con": 14,
                           "int": 10, "wis": 10, "cha": 10}},
            "free_ability_choice": "str",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"climb": 1, "swim": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "alertness"},  # general, not combat
        }
        with self.assertRaises(CharacterCreationError) as ctx:
            create_character(CharacterRequest.from_dict(body), REGISTRY)
        self.assertIn("type 'combat'", str(ctx.exception))

    def test_fighter_combat_feat_accepted(self):
        body = {
            "name": "Edric", "race": "human", "class": "fighter",
            "alignment": "lawful_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 16, "dex": 14, "con": 14,
                           "int": 10, "wis": 10, "cha": 10}},
            "free_ability_choice": "str",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"climb": 1, "swim": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "weapon_focus_longsword"},
        }
        # Should not raise.
        create_character(CharacterRequest.from_dict(body), REGISTRY)


class TestMonkFeatPool(unittest.TestCase):
    def test_monk_l1_bonus_feat_off_menu_rejected(self):
        body = {
            "name": "Tian", "race": "human", "class": "monk",
            "alignment": "lawful_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 14, "con": 14,
                           "int": 10, "wis": 14, "cha": 10}},
            "free_ability_choice": "wis",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"acrobatics": 1, "perception": 1},
            "bonus_languages": [],
            "class_choices": {"monk_bonus_feat": "weapon_focus_longsword"},
        }
        with self.assertRaises(CharacterCreationError) as ctx:
            create_character(CharacterRequest.from_dict(body), REGISTRY)
        self.assertIn("RAW menu", str(ctx.exception))

    def test_monk_l1_bonus_feat_on_menu_accepted(self):
        body = {
            "name": "Tian", "race": "human", "class": "monk",
            "alignment": "lawful_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 14, "con": 14,
                           "int": 10, "wis": 14, "cha": 10}},
            "free_ability_choice": "wis",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"acrobatics": 1, "perception": 1},
            "bonus_languages": [],
            "class_choices": {"monk_bonus_feat": "combat_reflexes"},
        }
        create_character(CharacterRequest.from_dict(body), REGISTRY)


if __name__ == "__main__":
    unittest.main()
