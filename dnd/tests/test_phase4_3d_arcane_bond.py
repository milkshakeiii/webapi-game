"""Tests for Phase 4.3d slice 1 — wizard Arcane Bond (bonded object).

RAW (Foundry pack ``Arcane Bond``, class-abilities.md lines 3785-3807):

> A bonded object can be used once per day to cast any one spell that
> the wizard has in his spellbook and is capable of casting, even if
> the spell is not prepared. ... This spell cannot be modified by
> metamagic feats or other abilities. The bonded object cannot be
> used to cast spells from the wizard's opposition schools.

Validates:
- class_choices.arcane_bond_type validation (amulet/ring/staff/wand/
  weapon/familiar; defaults to "amulet" when omitted).
- Daily ``arcane_bond_uses`` resource seeded for bonded-object forms
  (familiar form does not get the pool).
- ``use_arcane_bond: true`` cast-time flag bypasses the prepared-
  spell gate, decrements the daily pool, rejects metamagic, rejects
  opposition-school spells.
"""

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
from dnd.engine.dsl import TurnIntent
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


def _wiz(*, bond_type=None, school="universalist",
         opposition=None, **extra) -> object:
    body = {
        "name": "Mira", "race": "human", "class": "wizard",
        "alignment": "true_neutral",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 10, "dex": 14, "con": 14,
                       "int": 14, "wis": 10, "cha": 14}},
        "free_ability_choice": "int",
        "feats": ["dodge", "iron_will"],
        "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
        "bonus_languages": [],
        "class_choices": {"wizard_school": school},
    }
    if bond_type is not None:
        body["class_choices"]["arcane_bond_type"] = bond_type
    if opposition is not None:
        body["class_choices"]["wizard_opposition_schools"] = opposition
    body["class_choices"].update(extra)
    return create_character(CharacterRequest.from_dict(body), REGISTRY)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestArcaneBondValidation(unittest.TestCase):
    def test_unknown_bond_type_rejected(self):
        with self.assertRaises(CharacterCreationError) as ctx:
            _wiz(bond_type="cape")
        self.assertIn("RAW menu", str(ctx.exception))

    def test_omitted_bond_type_accepted_defaults_to_amulet(self):
        # No arcane_bond_type provided — engine defaults; no raise.
        char = _wiz()
        self.assertIsNotNone(char)

    def test_each_bond_type_accepted(self):
        for bond in ("amulet", "ring", "staff", "wand", "weapon",
                     "familiar"):
            with self.subTest(bond=bond):
                char = _wiz(bond_type=bond)
                self.assertIsNotNone(char)


# ---------------------------------------------------------------------------
# Daily resource seeded for non-familiar bonds
# ---------------------------------------------------------------------------


class TestArcaneBondUsesResource(unittest.TestCase):
    def test_amulet_seeded(self):
        char = _wiz(bond_type="amulet")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertEqual(c.resources.get("arcane_bond_uses"), 1)

    def test_weapon_seeded(self):
        char = _wiz(bond_type="weapon")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertEqual(c.resources.get("arcane_bond_uses"), 1)

    def test_familiar_not_seeded(self):
        char = _wiz(bond_type="familiar")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertNotIn("arcane_bond_uses", c.resources)

    def test_default_seeded(self):
        # No arcane_bond_type → defaults to amulet → resource seeded.
        char = _wiz()
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertEqual(c.resources.get("arcane_bond_uses"), 1)


# ---------------------------------------------------------------------------
# Bonded-object cast-time behavior
# ---------------------------------------------------------------------------


def _setup_cast_encounter(wiz_char):
    wiz = combatant_from_character(wiz_char, REGISTRY, (5, 5), "x")
    goblin = combatant_from_monster(
        REGISTRY.get_monster("goblin"), (7, 5), "y",
    )
    goblin.max_hp = 9999
    goblin.current_hp = 9999
    grid = Grid(width=20, height=20)
    grid.place(wiz)
    grid.place(goblin)
    enc = Encounter.begin(grid, [wiz, goblin], Roller(seed=1))
    return wiz, goblin, enc, grid


def _cast(wiz, spell_id, target, enc, grid, **args):
    do = {"composite": "cast",
          "args": {"spell": spell_id, "target": target,
                   "spell_level": 1, **args}}
    intent = TurnIntent(rule_index=0, do=do, namespace={})
    return execute_turn(wiz, intent, enc, grid, Roller(seed=1))


class TestArcaneBondCast(unittest.TestCase):
    def test_bonded_cast_bypasses_prep_and_consumes_use(self):
        # Universalist wizard with the amulet bond. Spells prepared
        # leaves Magic Missile UN-prepared; arcane_bond lets the wizard
        # cast it anyway.
        body = {
            "name": "Mira", "race": "human", "class": "wizard",
            "alignment": "true_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 10, "dex": 14, "con": 14,
                           "int": 14, "wis": 10, "cha": 14}},
            "free_ability_choice": "int",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
            "bonus_languages": [],
            "class_choices": {"arcane_bond_type": "amulet",
                              "wizard_school": "universalist"},
            "spells_prepared": {"1": ["shield"]},  # NOT magic_missile
        }
        char = create_character(CharacterRequest.from_dict(body), REGISTRY)
        wiz, goblin, enc, grid = _setup_cast_encounter(char)
        before = wiz.resources["arcane_bond_uses"]
        result = _cast(wiz, "magic_missile", goblin, enc, grid,
                       use_arcane_bond=True)
        # The cast should resolve (not skip with not-prepared reason).
        skips = [e for e in result.events
                 if e.kind == "skip"
                 and "not prepared" in e.detail.get("reason", "")]
        self.assertEqual(
            skips, [],
            f"unexpected not-prepared skip; events={result.events}",
        )
        cast_events = [e for e in result.events if e.kind == "cast"]
        self.assertEqual(len(cast_events), 1)
        # Use consumed.
        self.assertEqual(
            wiz.resources["arcane_bond_uses"], before - 1,
        )

    def test_second_bonded_cast_rejected_after_use_spent(self):
        body = {
            "name": "Mira", "race": "human", "class": "wizard",
            "alignment": "true_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 10, "dex": 14, "con": 14,
                           "int": 14, "wis": 10, "cha": 14}},
            "free_ability_choice": "int",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
            "bonus_languages": [],
            "class_choices": {"arcane_bond_type": "amulet",
                              "wizard_school": "universalist"},
            "spells_prepared": {"1": ["shield"]},
        }
        char = create_character(CharacterRequest.from_dict(body), REGISTRY)
        wiz, goblin, enc, grid = _setup_cast_encounter(char)
        _cast(wiz, "magic_missile", goblin, enc, grid,
              use_arcane_bond=True)
        # Second attempt the same encounter (or day): rejected.
        result = _cast(wiz, "magic_missile", goblin, enc, grid,
                       use_arcane_bond=True)
        skip = next(e for e in result.events if e.kind == "skip")
        self.assertIn("1/day already spent", skip.detail["reason"])

    def test_bonded_cast_with_metamagic_rejected(self):
        body = {
            "name": "Mira", "race": "human", "class": "wizard",
            "alignment": "true_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 10, "dex": 14, "con": 14,
                           "int": 14, "wis": 10, "cha": 14}},
            "free_ability_choice": "int",
            "feats": ["dodge", "empower_spell"],
            "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
            "bonus_languages": [],
            "class_choices": {"arcane_bond_type": "amulet",
                              "wizard_school": "universalist"},
            "spells_prepared": {"1": ["shield"]},
        }
        char = create_character(CharacterRequest.from_dict(body), REGISTRY)
        wiz, goblin, enc, grid = _setup_cast_encounter(char)
        result = _cast(wiz, "magic_missile", goblin, enc, grid,
                       use_arcane_bond=True,
                       metamagic=["empower_spell"])
        skip = next(e for e in result.events if e.kind == "skip")
        self.assertIn("cannot be modified by metamagic",
                      skip.detail["reason"])

    def test_bonded_cast_opposition_school_rejected(self):
        # Evoker with abjuration as opposition. Bonded cast of Shield
        # (abjuration) → rejected.
        body = {
            "name": "Mira", "race": "human", "class": "wizard",
            "alignment": "true_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 10, "dex": 14, "con": 14,
                           "int": 14, "wis": 10, "cha": 14}},
            "free_ability_choice": "int",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
            "bonus_languages": [],
            "class_choices": {"arcane_bond_type": "amulet",
                              "wizard_school": "evocation",
                              "wizard_opposition_schools":
                                  ["abjuration", "necromancy"]},
            "spells_prepared": {"1": ["magic_missile"]},
        }
        char = create_character(CharacterRequest.from_dict(body), REGISTRY)
        wiz, goblin, enc, grid = _setup_cast_encounter(char)
        result = _cast(wiz, "shield", goblin, enc, grid,
                       use_arcane_bond=True)
        skip = next(e for e in result.events if e.kind == "skip")
        self.assertIn("opposition schools",
                      skip.detail["reason"])

    def test_bonded_cast_without_flag_still_requires_prep(self):
        # Sanity check: without use_arcane_bond, the normal prep
        # gate still rejects an unprepared spell.
        body = {
            "name": "Mira", "race": "human", "class": "wizard",
            "alignment": "true_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 10, "dex": 14, "con": 14,
                           "int": 14, "wis": 10, "cha": 14}},
            "free_ability_choice": "int",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
            "bonus_languages": [],
            "class_choices": {"arcane_bond_type": "amulet",
                              "wizard_school": "universalist"},
            "spells_prepared": {"1": ["shield"]},
        }
        char = create_character(CharacterRequest.from_dict(body), REGISTRY)
        wiz, goblin, enc, grid = _setup_cast_encounter(char)
        result = _cast(wiz, "magic_missile", goblin, enc, grid)
        skip = next(e for e in result.events if e.kind == "skip")
        self.assertIn("not prepared", skip.detail["reason"])


if __name__ == "__main__":
    unittest.main()
