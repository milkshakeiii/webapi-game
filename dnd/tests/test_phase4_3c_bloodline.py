"""Tests for Phase 4.3c — sorcerer bloodline: choice validation,
draconic dragon-type, bonus class skill, L1 active power uses/day.

RAW (Foundry pack ``Sorcerer Bloodline``, lines 82069-82083):

> A sorcerer must pick one bloodline upon taking her first level of
> sorcerer. Once made, this choice cannot be changed.

Per-bloodline class skill verified (CRB p. 73-77):
- Arcane: Knowledge (any one) — we model as Knowledge (arcana).
- Celestial: Heal.
- Draconic: Perception.
- Fey: Knowledge (nature).
- Infernal: Diplomacy.

RAW (Draconic Bloodline, line 82372):
> At 1st level, you must select one of the chromatic or metallic
> dragon types. This choice cannot be changed.
"""

from __future__ import annotations

import unittest

from dnd.engine.characters import (
    CharacterCreationError,
    CharacterRequest,
    create_character,
)
from dnd.engine.combatant import combatant_from_character
from dnd.engine.content import default_registry


REGISTRY = default_registry()


def _sorcerer(**class_choices) -> object:
    body = {
        "name": "Vyx", "race": "human", "class": "sorcerer",
        "alignment": "chaotic_neutral",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 10, "dex": 14, "con": 14,
                       "int": 10, "wis": 14, "cha": 14}},
        "free_ability_choice": "cha",
        "feats": ["dodge", "iron_will"],
        "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
        "bonus_languages": [],
        "class_choices": dict(class_choices),
    }
    return create_character(CharacterRequest.from_dict(body), REGISTRY)


# ---------------------------------------------------------------------------
# Bloodline-choice validation
# ---------------------------------------------------------------------------


class TestBloodlineValidation(unittest.TestCase):
    def test_omitting_bloodline_rejected(self):
        with self.assertRaises(CharacterCreationError) as ctx:
            _sorcerer()
        self.assertIn("sorcerer_bloodline", str(ctx.exception))

    def test_unknown_bloodline_rejected(self):
        with self.assertRaises(CharacterCreationError) as ctx:
            _sorcerer(sorcerer_bloodline="aberrant")
        self.assertIn("not a recognized CRB bloodline",
                      str(ctx.exception))

    def test_draconic_requires_dragon_type(self):
        with self.assertRaises(CharacterCreationError) as ctx:
            _sorcerer(sorcerer_bloodline="draconic")
        self.assertIn("dragon_type", str(ctx.exception))

    def test_unknown_dragon_type_rejected(self):
        with self.assertRaises(CharacterCreationError) as ctx:
            _sorcerer(sorcerer_bloodline="draconic",
                      sorcerer_dragon_type="cthulhu")
        self.assertIn("not in the RAW menu", str(ctx.exception))

    def test_all_five_crb_bloodlines_accepted(self):
        for bl in ("arcane", "celestial", "fey", "infernal"):
            with self.subTest(bloodline=bl):
                char = _sorcerer(sorcerer_bloodline=bl)
                self.assertIsNotNone(char)
        # Draconic needs a dragon type.
        for dt in ("red", "gold", "white", "blue", "black", "green",
                   "silver", "bronze", "copper", "brass"):
            with self.subTest(dragon_type=dt):
                char = _sorcerer(sorcerer_bloodline="draconic",
                                 sorcerer_dragon_type=dt)
                self.assertIsNotNone(char)


# ---------------------------------------------------------------------------
# Bonus class skill
# ---------------------------------------------------------------------------


class TestBloodlineClassSkill(unittest.TestCase):
    """Each bloodline grants one bonus class skill. With 1 rank in
    that skill, the character should get the +3 class-skill bonus."""

    def _ranked_in(self, skill_id: str, bloodline: str,
                   dragon_type: str | None = None):
        body = {
            "name": "Vyx", "race": "human", "class": "sorcerer",
            "alignment": "chaotic_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 10, "dex": 14, "con": 14,
                           "int": 10, "wis": 14, "cha": 14}},
            "free_ability_choice": "cha",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {skill_id: 1, "spellcraft": 1},
            "bonus_languages": [],
            "class_choices": {"sorcerer_bloodline": bloodline},
        }
        if dragon_type:
            body["class_choices"]["sorcerer_dragon_type"] = dragon_type
        return create_character(CharacterRequest.from_dict(body), REGISTRY)

    def _has_class_skill_bonus(self, c, skill_id: str) -> bool:
        for m in c.modifiers.for_target(f"skill:{skill_id}"):
            if m.source == "class_skill_bonus" and m.value == 3:
                return True
        return False

    def test_celestial_grants_heal(self):
        char = self._ranked_in("heal", "celestial")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertTrue(self._has_class_skill_bonus(c, "heal"))

    def test_draconic_grants_perception(self):
        char = self._ranked_in("perception", "draconic",
                               dragon_type="red")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertTrue(self._has_class_skill_bonus(c, "perception"))

    def test_fey_grants_knowledge_nature(self):
        char = self._ranked_in("knowledge_nature", "fey")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertTrue(self._has_class_skill_bonus(c, "knowledge_nature"))

    def test_infernal_grants_diplomacy(self):
        char = self._ranked_in("diplomacy", "infernal")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertTrue(self._has_class_skill_bonus(c, "diplomacy"))


# ---------------------------------------------------------------------------
# L1 active power uses/day
# ---------------------------------------------------------------------------


class TestBloodlineActiveUsesPerDay(unittest.TestCase):
    """RAW: 3 + Cha mod uses per day for each L1 active power."""

    def test_celestial_heavenly_fire_uses(self):
        char = _sorcerer(sorcerer_bloodline="celestial")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        # Cha 14 + human +2 = 16, +3 mod. Uses = 6.
        self.assertEqual(
            c.resources.get("sorcerer_bloodline_heavenly_fire_uses"), 6,
        )

    def test_draconic_claws_uses(self):
        char = _sorcerer(sorcerer_bloodline="draconic",
                         sorcerer_dragon_type="red")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertEqual(
            c.resources.get("sorcerer_bloodline_draconic_claws_uses"), 6,
        )

    def test_fey_laughing_touch_uses(self):
        char = _sorcerer(sorcerer_bloodline="fey")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertEqual(
            c.resources.get("sorcerer_bloodline_laughing_touch_uses"), 6,
        )

    def test_infernal_corrupting_touch_uses(self):
        char = _sorcerer(sorcerer_bloodline="infernal")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertEqual(
            c.resources.get("sorcerer_bloodline_corrupting_touch_uses"), 6,
        )

    def test_arcane_has_no_active_uses_resource(self):
        # Arcane bloodline's L1 power is Arcane Bond (deferred), not
        # a 3+Cha-mod-style active.
        char = _sorcerer(sorcerer_bloodline="arcane")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        any_active = [k for k in c.resources
                      if k.startswith("sorcerer_bloodline_")]
        self.assertEqual(any_active, [])


if __name__ == "__main__":
    unittest.main()
