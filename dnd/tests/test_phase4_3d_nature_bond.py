"""Tests for Phase 4.3d slice 2 — druid Nature Bond (domain path).

RAW (Foundry pack ``Nature Bond``, class-abilities.md lines 64318-
64336; CRB p. 50):

> At 1st level, a druid forms a bond with nature. This bond can take
> one of two forms. The first is a close tie to the natural world,
> granting the druid one of the following cleric domains: Air,
> Animal, Earth, Fire, Plant, Water, or Weather. ... A druid that
> selects this option also receives additional domain spell slots,
> just like a cleric. She must prepare the spell from her domain in
> this slot and this spell cannot be used to cast a spell
> spontaneously. The second option is to form a close bond with an
> animal companion.

Slice 2 covers the domain branch end-to-end:
- nature_bond_type validation.
- domain pick restricted to the 7-domain druid list.
- domain pipeline (bonus slot, auto-prepared domain spell) wired
  through the same path as cleric domains.

Animal companion path is validated (requires base-animal pick) but
Combatant materialization is deferred to slice 3.
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


def _druid(**class_choices) -> object:
    body = {
        "name": "Wren", "race": "human", "class": "druid",
        "alignment": "neutral_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 10, "dex": 14, "con": 14,
                       "int": 10, "wis": 14, "cha": 14}},
        "free_ability_choice": "wis",
        "feats": ["dodge", "iron_will"],
        "skill_ranks": {"survival": 1, "knowledge_nature": 1},
        "bonus_languages": [],
        "class_choices": dict(class_choices),
    }
    return create_character(CharacterRequest.from_dict(body), REGISTRY)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestNatureBondValidation(unittest.TestCase):
    def test_default_is_accepted_as_animal_companion(self):
        # Omitting nature_bond_type defaults to animal_companion.
        # In slice 2 the animal_companion branch requires base_animal
        # — so omitting BOTH should fail.
        with self.assertRaises(CharacterCreationError) as ctx:
            _druid()
        self.assertIn("animal_companion_base_animal",
                      str(ctx.exception))

    def test_unknown_nature_bond_type_rejected(self):
        with self.assertRaises(CharacterCreationError):
            _druid(nature_bond_type="storm")

    def test_domain_requires_exactly_one_pick(self):
        # Zero domains.
        with self.assertRaises(CharacterCreationError):
            _druid(nature_bond_type="domain", domains=[])
        # Two domains (cleric-style, but druid only picks one).
        with self.assertRaises(CharacterCreationError):
            _druid(nature_bond_type="domain",
                   domains=["air", "fire"])

    def test_non_druid_allowed_domain_rejected(self):
        # Healing is a cleric domain, not on the druid list.
        with self.assertRaises(CharacterCreationError) as ctx:
            _druid(nature_bond_type="domain",
                   domains=["healing"])
        self.assertIn("druid-allowed list", str(ctx.exception))

    def test_each_druid_domain_accepted(self):
        for d in ("air", "animal", "earth", "fire",
                  "plant", "water", "weather"):
            with self.subTest(domain=d):
                char = _druid(nature_bond_type="domain", domains=[d])
                self.assertIsNotNone(char)

    def test_animal_companion_requires_base_animal(self):
        with self.assertRaises(CharacterCreationError):
            _druid(nature_bond_type="animal_companion")
        # With base_animal: accepted (Combatant materialization is
        # slice 3, but validation should pass).
        char = _druid(nature_bond_type="animal_companion",
                      animal_companion_base_animal="wolf")
        self.assertIsNotNone(char)


# ---------------------------------------------------------------------------
# Domain pipeline (bonus slot + auto-prepared domain spell)
# ---------------------------------------------------------------------------


class TestDruidDomainPipeline(unittest.TestCase):
    def test_water_domain_seeds_bonus_slot_for_content_levels(self):
        # The water-domain spell pipeline only adds a bonus
        # ``domain_slot_<L>`` for levels whose spell exists in our
        # content. Most water-domain L1-L4 entries (obscuring_mist,
        # fog_cloud, water_breathing, control_water) aren't in
        # content yet, so no L1 bonus. Ice Storm (L5) and Cone of
        # Cold (L6) ARE in content — confirming the pipeline runs
        # for druids the same way it does for clerics. Backfilling
        # the missing low-level spells will surface those slots
        # automatically.
        char = _druid(nature_bond_type="domain",
                      domains=["water"])
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertEqual(c.resources.get("domain_slot_5"), 1)
        self.assertEqual(c.resources.get("domain_slot_6"), 1)

    def test_water_domain_seeds_icicle_uses(self):
        # Icicle is the L1 granted power; 3 + Wis mod uses/day.
        # Wis 14 + human +2 to wis (free_ability_choice) → 16, +3
        # mod. So 6 uses.
        char = _druid(nature_bond_type="domain",
                      domains=["water"])
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertEqual(c.resources.get("domain_icicle_uses"), 6)

    def test_water_domain_auto_prepares_content_l5_spell(self):
        # Same content gap as the slot test: L1 water-domain spell
        # not in our catalog yet. Verify auto-prep works at the
        # levels where the spell IS catalogued.
        char = _druid(nature_bond_type="domain",
                      domains=["water"])
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertIn("ice_storm",
                      c.prepared_spells.get(5, []))

    def test_animal_companion_does_not_get_domain_slot(self):
        # When nature_bond is animal_companion, no domain resources
        # should be seeded.
        char = _druid(nature_bond_type="animal_companion",
                      animal_companion_base_animal="wolf")
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertNotIn("domain_slot_1", c.resources)

    def test_plant_domain_deferred_handler_no_uses(self):
        # Wooden Fist's handler is marked deferred → no uses pool.
        char = _druid(nature_bond_type="domain",
                      domains=["plant"])
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        self.assertNotIn("domain_wooden_fist_uses", c.resources)


if __name__ == "__main__":
    unittest.main()
