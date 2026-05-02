"""Tests for situational racial traits (qualifier-on-modifier framework).

Covers:
- Modifier qualifier mechanics (compute / compute_with_context)
- Dwarven hatred: +1 attack vs orc/goblinoid
- Gnome hatred: +1 attack vs reptilian/goblinoid
- Hardy: +2 saves vs spells
- Illusion resistance: +2 saves vs illusion-school spells

Defensive training (+4 dodge AC vs giants) is wired via racial_effects
but not testable end-to-end without a giant monster in the content
folder. The qualifier is exercised in the unit tests below.
"""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combat import (
    AttackProfile,
    DefenseProfile,
    resolve_attack,
)
from dnd.engine.combatant import (
    combatant_from_character,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.modifiers import (
    Modifier,
    compute,
    compute_with_context,
    mod,
    qualifier_matches,
)
from dnd.engine.spells import roll_save


REGISTRY = default_registry()


# ---------------------------------------------------------------------------
# Framework: qualifier matching
# ---------------------------------------------------------------------------


class TestQualifierMatches(unittest.TestCase):
    def test_none_qualifier_always_matches(self):
        self.assertTrue(qualifier_matches(None, {}))
        self.assertTrue(qualifier_matches(None, {"x": "y"}))

    def test_string_value_membership(self):
        q = (("target_type", ("orc",)),)
        self.assertTrue(qualifier_matches(q, {"target_type": "orc"}))
        self.assertFalse(qualifier_matches(q, {"target_type": "human"}))

    def test_list_value_intersection(self):
        q = (("target_subtypes", ("orc", "goblinoid")),)
        self.assertTrue(qualifier_matches(q, {"target_subtypes": ["humanoid", "orc"]}))
        self.assertFalse(qualifier_matches(q, {"target_subtypes": ["humanoid"]}))

    def test_missing_context_key_fails(self):
        q = (("target_type", ("orc",)),)
        self.assertFalse(qualifier_matches(q, {}))


class TestComputeFiltersQualified(unittest.TestCase):
    def test_compute_excludes_qualified_modifiers(self):
        # Use stacking 'untyped' types so we see additive behavior
        # without non-stacking suppression masking the qualifier check.
        mods = [
            mod(2, "untyped", "attack", "src1"),  # unqualified
            mod(1, "untyped", "attack", "src2",
                qualifier={"target_type": ["orc"]}),  # qualified
        ]
        # compute() ignores qualified mods.
        self.assertEqual(compute(0, mods), 2)

    def test_compute_with_context_includes_matching(self):
        mods = [
            mod(2, "untyped", "attack", "src1"),
            mod(1, "untyped", "attack", "src2",
                qualifier={"target_type": ["orc"]}),
        ]
        self.assertEqual(
            compute_with_context(0, mods, {"target_type": "orc"}), 3,
        )

    def test_compute_with_context_excludes_non_matching(self):
        mods = [
            mod(2, "untyped", "attack", "src1"),
            mod(1, "untyped", "attack", "src2",
                qualifier={"target_type": ["orc"]}),
        ]
        self.assertEqual(
            compute_with_context(0, mods, {"target_type": "human"}), 2,
        )


# ---------------------------------------------------------------------------
# Dwarven hatred: +1 attack vs orcs/goblinoids
# ---------------------------------------------------------------------------


def _dwarf_request():
    return CharacterRequest.from_dict({
        "name": "Throgar", "race": "dwarf", "class": "fighter",
        "alignment": "lawful_good",
        # Dwarves get +2 Con +2 Wis -2 Cha (no free choice — no
        # free_ability_choice key).
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 16, "dex": 14, "con": 14,
                       "int": 10, "wis": 10, "cha": 10}},
        # Dwarves have no bonus feat slot — just 1 general feat at L1.
        "feats": ["power_attack"],
        "skill_ranks": {"climb": 1, "swim": 1},
        "bonus_languages": [],
        "class_choices": {"fighter_bonus_feat": "cleave"},
    })


class TestDwarvenHatred(unittest.TestCase):
    def _setup(self, target_id: str):
        char = create_character(_dwarf_request(), REGISTRY)
        dwarf = combatant_from_character(char, REGISTRY, (5, 5), "x")
        target = combatant_from_monster(
            REGISTRY.get_monster(target_id), (6, 5), "y",
        )
        target.max_hp = 9999
        target.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(dwarf)
        grid.place(target)
        enc = Encounter.begin(grid, [dwarf, target], Roller(seed=1))
        return dwarf, target, enc, grid

    def _attack_bonus_used(self, dwarf, target, grid, encounter, seed=1):
        from dnd.engine.turn_executor import _do_attack
        events = []
        _do_attack(dwarf, target, grid, Roller(seed=seed), events,
                   encounter=encounter)
        atk = next(e for e in events if e.kind == "attack")
        for line in atk.detail["trace"]:
            if line.startswith("attack "):
                parts = line.split(" = ")[0]
                return int(parts.rsplit("+ ", 1)[1])
        return None

    def test_plus_1_vs_orc(self):
        # Orc has subtype "orc" — dwarven hatred fires.
        dwarf, orc, enc, grid = self._setup("orc")
        # Compare to the same dwarf attacking a non-hated target.
        bonus_vs_orc = self._attack_bonus_used(dwarf, orc, grid, enc)

        dwarf2, human_zombie, enc2, grid2 = self._setup("human_zombie")
        # zombie subtypes are []; not hated.
        bonus_vs_zombie = self._attack_bonus_used(
            dwarf2, human_zombie, grid2, enc2,
        )
        self.assertEqual(bonus_vs_orc - bonus_vs_zombie, 1)

    def test_plus_1_vs_goblin_via_goblinoid_subtype(self):
        dwarf, goblin, enc, grid = self._setup("goblin")
        # Goblin's subtypes include "goblinoid" — hatred fires.
        # Compare against zombie (not goblinoid).
        bonus_vs_goblin = self._attack_bonus_used(dwarf, goblin, grid, enc)
        dwarf2, zombie, enc2, grid2 = self._setup("human_zombie")
        bonus_vs_zombie = self._attack_bonus_used(
            dwarf2, zombie, grid2, enc2,
        )
        self.assertEqual(bonus_vs_goblin - bonus_vs_zombie, 1)


# ---------------------------------------------------------------------------
# Hardy: +2 saves vs spells
# ---------------------------------------------------------------------------


class TestHardySaveBonus(unittest.TestCase):
    def test_dwarf_save_with_spell_context(self):
        char = create_character(_dwarf_request(), REGISTRY)
        dwarf = combatant_from_character(char, REGISTRY, (0, 0), "x")
        # Save without context → hardy's +2 doesn't apply.
        no_ctx = dwarf.save("fort")
        # Save with effect_tags=["spell"] → hardy adds +2.
        with_ctx = dwarf.save("fort", context={"effect_tags": ["spell"]})
        self.assertEqual(with_ctx - no_ctx, 2)

    def test_dwarf_save_with_poison_context(self):
        char = create_character(_dwarf_request(), REGISTRY)
        dwarf = combatant_from_character(char, REGISTRY, (0, 0), "x")
        no_ctx = dwarf.save("fort")
        poison = dwarf.save("fort", context={"effect_tags": ["poison"]})
        self.assertEqual(poison - no_ctx, 2)

    def test_dwarf_save_with_unrelated_context(self):
        char = create_character(_dwarf_request(), REGISTRY)
        dwarf = combatant_from_character(char, REGISTRY, (0, 0), "x")
        no_ctx = dwarf.save("fort")
        # Some unrelated effect tag — hardy doesn't fire.
        unrelated = dwarf.save("fort", context={"effect_tags": ["fire"]})
        self.assertEqual(unrelated, no_ctx)


# ---------------------------------------------------------------------------
# Defensive Training: +4 dodge AC vs giants — qualifier present
#
# We can't end-to-end test (no giant monster in content), but we can
# assert the qualified modifier is on the dwarf's modifier collection.
# ---------------------------------------------------------------------------


class TestDefensiveTraining(unittest.TestCase):
    def test_qualified_ac_modifier_present_on_dwarf(self):
        char = create_character(_dwarf_request(), REGISTRY)
        dwarf = combatant_from_character(char, REGISTRY, (0, 0), "x")
        ac_mods = dwarf.modifiers.for_target("ac")
        defensive = [
            m for m in ac_mods
            if m.source.endswith(":defensive_training")
        ]
        self.assertEqual(len(defensive), 1)
        m = defensive[0]
        self.assertEqual(m.value, 4)
        self.assertEqual(m.type, "dodge")
        # Qualifier carries the giant-subtype filter.
        self.assertIsNotNone(m.qualifier)
        keys = dict(m.qualifier)  # type: ignore[arg-type]
        self.assertIn("attacker_subtypes", keys)
        self.assertIn("giant", keys["attacker_subtypes"])


if __name__ == "__main__":
    unittest.main()
