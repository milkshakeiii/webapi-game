"""Tests for Phase 4.3b — wizard arcane school: choice validation,
opposition schools, bonus L1 spell slot, and L1 passive powers.

RAW (Foundry pack ``Arcane School``, ``class-abilities.md`` 4051-4068):

> A wizard can choose to specialize in one school of magic ... a
> wizard that does not select a school receives the universalist
> school instead. A wizard that chooses to specialize ... must
> select two other schools as his opposition schools.

> Each arcane school gives the wizard a number of school powers.
> In addition, specialist wizards receive an additional spell slot
> of each spell level he can cast, from 1st on up. ... Wizards with
> the universalist school do not receive a school slot.

L1 passive powers verified here:
- Forewarned (Divination): +max(1, wiz_lvl // 2) untyped to initiative.
- Enchanting Smile (Enchantment): +2 enhancement to Bluff / Diplomacy
  / Intimidate, +1 per 5 wizard levels.
- Physical Enhancement (Transmutation): +1 enhancement to one chosen
  physical ability (str / dex / con).
- Resistance (Abjuration): energy resistance 5 to a chosen energy
  type (default fire).
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
from dnd.engine.modifiers import compute as _compute


REGISTRY = default_registry()


def _wizard(**class_choices) -> object:
    # Point-buy 20: int 14 (5) + con 14 (5) + dex 14 (5) + str 10 (0)
    # + wis 10 (0) + cha 14 (5) = 20. Human +2 → Int 16.
    body = {
        "name": "Mira", "race": "human", "class": "wizard",
        "alignment": "true_neutral",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 10, "dex": 14, "con": 14,
                       "int": 14, "wis": 10, "cha": 14}},
        "free_ability_choice": "int",
        "feats": ["dodge", "iron_will"],
        "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1,
                        "diplomacy": 1, "bluff": 1, "intimidate": 1},
        "bonus_languages": [],
        "class_choices": dict(class_choices),
    }
    return create_character(CharacterRequest.from_dict(body), REGISTRY)


# ---------------------------------------------------------------------------
# School-choice validation
# ---------------------------------------------------------------------------


class TestSchoolValidation(unittest.TestCase):
    def test_default_no_choice_is_accepted(self):
        # Omitting wizard_school is legal — defaults to universalist
        # at sheet-build time.
        char = _wizard()
        self.assertIsNotNone(char)

    def test_unknown_school_rejected(self):
        with self.assertRaises(CharacterCreationError) as ctx:
            _wizard(wizard_school="alchemy")
        self.assertIn("not a recognized school", str(ctx.exception))

    def test_specialist_requires_exactly_two_opposition(self):
        # Zero opposition schools.
        with self.assertRaises(CharacterCreationError):
            _wizard(wizard_school="evocation",
                    wizard_opposition_schools=[])
        # One opposition school.
        with self.assertRaises(CharacterCreationError):
            _wizard(wizard_school="evocation",
                    wizard_opposition_schools=["abjuration"])
        # Three opposition schools.
        with self.assertRaises(CharacterCreationError):
            _wizard(wizard_school="evocation",
                    wizard_opposition_schools=["abjuration",
                                               "necromancy",
                                               "illusion"])

    def test_opposition_must_differ_from_specialty(self):
        with self.assertRaises(CharacterCreationError) as ctx:
            _wizard(wizard_school="evocation",
                    wizard_opposition_schools=["evocation",
                                               "necromancy"])
        self.assertIn("cannot equal", str(ctx.exception))

    def test_opposition_must_be_distinct(self):
        with self.assertRaises(CharacterCreationError) as ctx:
            _wizard(wizard_school="evocation",
                    wizard_opposition_schools=["abjuration",
                                               "abjuration"])
        self.assertIn("distinct", str(ctx.exception))

    def test_universalist_cannot_have_opposition(self):
        with self.assertRaises(CharacterCreationError) as ctx:
            _wizard(wizard_school="universalist",
                    wizard_opposition_schools=["abjuration",
                                               "necromancy"])
        self.assertIn("no opposition", str(ctx.exception))

    def test_valid_specialist_accepted(self):
        char = _wizard(wizard_school="evocation",
                       wizard_opposition_schools=["abjuration",
                                                  "necromancy"])
        self.assertIsNotNone(char)


# ---------------------------------------------------------------------------
# Bonus L1 spell slot (specialist gets one extra; universalist does not)
# ---------------------------------------------------------------------------


class TestSpecialistBonusSlot(unittest.TestCase):
    def test_specialist_gets_extra_l1_slot(self):
        char = _wizard(wizard_school="evocation",
                       wizard_opposition_schools=["abjuration",
                                                  "necromancy"])
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        # Wizard base: 1 L1 slot. Int 16 → +1 bonus L1 slot. Specialist
        # → +1 more. Expected = 3.
        self.assertEqual(c.resources.get("spell_slot_1"), 3)

    def test_universalist_does_not_get_extra_l1_slot(self):
        char = _wizard(wizard_school="universalist")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        # Universalist gets the base L1 + Int bonus, not the specialist
        # bonus. Expected = 2.
        self.assertEqual(c.resources.get("spell_slot_1"), 2)


# ---------------------------------------------------------------------------
# L1 active power: uses/day seeded as 3 + Int mod
# ---------------------------------------------------------------------------


class TestActivePowerUsesPerDay(unittest.TestCase):
    def test_evoker_gets_force_missile_uses(self):
        char = _wizard(wizard_school="evocation",
                       wizard_opposition_schools=["abjuration",
                                                  "necromancy"])
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        # Int 16 → +3 mod. 3 + 3 = 6 uses/day.
        self.assertEqual(
            c.resources.get("wizard_school_force_missile_uses"), 6,
        )

    def test_universalist_gets_hand_of_apprentice_uses(self):
        char = _wizard(wizard_school="universalist")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertEqual(
            c.resources.get("wizard_school_hand_of_the_apprentice_uses"),
            6,
        )


# ---------------------------------------------------------------------------
# L1 passive powers
# ---------------------------------------------------------------------------


class TestForewarned(unittest.TestCase):
    """Forewarned (Divination): +max(1, wiz_lvl // 2) to initiative."""

    def test_l1_divination_grants_plus_one_init(self):
        char = _wizard(wizard_school="divination",
                       wizard_opposition_schools=["abjuration",
                                                  "necromancy"])
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        forewarned_mods = [m for m in c.modifiers.for_target("initiative")
                           if m.source == "wizard_school:divination"]
        self.assertEqual(len(forewarned_mods), 1)
        self.assertEqual(forewarned_mods[0].value, 1)

    def test_evoker_does_not_get_init_bonus(self):
        char = _wizard(wizard_school="evocation",
                       wizard_opposition_schools=["abjuration",
                                                  "necromancy"])
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        forewarned_mods = [m for m in c.modifiers.for_target("initiative")
                           if m.source.startswith("wizard_school:")]
        self.assertEqual(forewarned_mods, [])


class TestEnchantingSmile(unittest.TestCase):
    """Enchantment passive: +2 enhancement to Bluff / Diplomacy /
    Intimidate."""

    def test_enchanter_gets_plus_two_to_social_skills(self):
        char = _wizard(wizard_school="enchantment",
                       wizard_opposition_schools=["abjuration",
                                                  "necromancy"])
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        for skill in ("bluff", "diplomacy", "intimidate"):
            with self.subTest(skill=skill):
                bonus = _compute(0, c.modifiers.for_target(f"skill:{skill}"))
                # The +2 enhancement should be a component of the total;
                # there can be other Cha-based contributions, so just
                # verify the enhancement-typed bonus is present.
                enh_mods = [m for m in c.modifiers.for_target(
                    f"skill:{skill}") if m.type == "enhancement"
                    and m.source.startswith("wizard_school:enchantment")]
                self.assertEqual(len(enh_mods), 1)
                self.assertEqual(enh_mods[0].value, 2)

    def test_evoker_does_not_get_enchanting_smile(self):
        char = _wizard(wizard_school="evocation",
                       wizard_opposition_schools=["abjuration",
                                                  "necromancy"])
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        enh_mods = [m for m in c.modifiers.for_target("skill:bluff")
                    if m.source.startswith("wizard_school:")]
        self.assertEqual(enh_mods, [])


class TestPhysicalEnhancement(unittest.TestCase):
    """Transmutation passive: +1 enhancement to one chosen physical
    ability."""

    def test_default_physical_enhancement_targets_str(self):
        char = _wizard(wizard_school="transmutation",
                       wizard_opposition_schools=["abjuration",
                                                  "necromancy"])
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        enh_str = [m for m in c.modifiers.for_target("ability:str")
                   if m.type == "enhancement"
                   and m.source.startswith("wizard_school:transmutation")]
        self.assertEqual(len(enh_str), 1)
        self.assertEqual(enh_str[0].value, 1)

    def test_can_choose_dex(self):
        char = _wizard(wizard_school="transmutation",
                       wizard_opposition_schools=["abjuration",
                                                  "necromancy"],
                       wizard_physical_enhancement_choice="dex")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        enh_dex = [m for m in c.modifiers.for_target("ability:dex")
                   if m.type == "enhancement"
                   and m.source.startswith("wizard_school:transmutation")]
        self.assertEqual(len(enh_dex), 1)
        self.assertEqual(enh_dex[0].value, 1)

    def test_mental_ability_rejected(self):
        # RAW: physical ability only.
        with self.assertRaises(Exception):  # ValueError, raised at build
            char = _wizard(wizard_school="transmutation",
                           wizard_opposition_schools=["abjuration",
                                                      "necromancy"],
                           wizard_physical_enhancement_choice="int")
            combatant_from_character(char, REGISTRY, (0, 0), "x")


class TestAbjurationResistance(unittest.TestCase):
    """Abjuration passive: energy resistance 5 (chosen daily)."""

    def test_default_resistance_is_fire_5(self):
        char = _wizard(wizard_school="abjuration",
                       wizard_opposition_schools=["evocation",
                                                  "necromancy"])
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertEqual(c.energy_resistance.get("fire"), 5)

    def test_can_choose_cold(self):
        char = _wizard(wizard_school="abjuration",
                       wizard_opposition_schools=["evocation",
                                                  "necromancy"],
                       wizard_resistance_energy="cold")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertEqual(c.energy_resistance.get("cold"), 5)
        self.assertNotIn("fire", c.energy_resistance)


# ---------------------------------------------------------------------------
# Opposition-school cost-doubling at spell prep
# ---------------------------------------------------------------------------


class TestOppositionPrepCost(unittest.TestCase):
    """RAW (Arcane School): 'A wizard who prepares spells from his
    opposition schools must use two spell slots of that level to
    prepare the spell.'"""

    def _wiz_with_prep(self, school: str, opposition, prepared) -> object:
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
            "class_choices": {"wizard_school": school,
                              "wizard_opposition_schools": opposition},
            "spells_prepared": prepared,
        }
        return create_character(CharacterRequest.from_dict(body), REGISTRY)

    def test_preparing_an_opposition_spell_consumes_two_slots(self):
        # Evoker with abjuration opposition. Magic Missile is an
        # evocation L1, so it costs 1 slot. Shield is an abjuration
        # L1 — opposition for this evoker — so it should consume two
        # L1 slots.
        # Base L1 slots: 1 (class) + 1 (Int bonus) + 1 (specialist) = 3.
        # Preparing Shield uses 2 → leaves 1 cast-capacity.
        char = self._wiz_with_prep(
            "evocation", ["abjuration", "necromancy"],
            {"1": ["shield"]},
        )
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertEqual(c.resources.get("spell_slot_1"), 2)

    def test_preparing_non_opposition_spell_costs_one_slot(self):
        # Same evoker prepping Magic Missile (evocation, the
        # specialty) costs 1 slot → 3 - 0 (no extra cost) = 3.
        char = self._wiz_with_prep(
            "evocation", ["abjuration", "necromancy"],
            {"1": ["magic_missile"]},
        )
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertEqual(c.resources.get("spell_slot_1"), 3)

    def test_universalist_pays_no_opposition_cost(self):
        # Universalists have no opposition schools, so they shouldn't
        # be penalized for prepping any school's spell. Universalist
        # gets 2 L1 slots total (1 class + 1 Int bonus).
        char = self._wiz_with_prep(
            "universalist", [],
            {"1": ["shield"]},  # Abjuration spell.
        )
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertEqual(c.resources.get("spell_slot_1"), 2)


if __name__ == "__main__":
    unittest.main()
