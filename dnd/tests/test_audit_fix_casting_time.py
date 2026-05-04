"""Tests for audit fix #9: Spell.casting_time is now consulted.

Two parts:

1. The swift slot accepts a cast either when the spell has a native
   ``casting_time == "swift"`` OR when the cast carries the
   ``quicken_spell`` metamagic. Previously only metamagic-quickened
   casts were accepted; native swift-time spells (none yet in
   content, but supported now) would have been rejected.

2. _do_cast emits a ``cast_long_casting_time`` event when the spell's
   casting time is full-round / 1-round / multi-round so the deferral
   gap is visible. The engine still resolves the spell on the current
   turn — proper 'completes just before next turn' semantics are a
   future change tracked in coverage.
"""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster, combatant_from_character
from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import TurnIntent
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import (
    _classify_casting_time,
    _do_cast,
    execute_turn,
)


REGISTRY = default_registry()


def _wizard():
    req = CharacterRequest.from_dict({
        "name": "Wiz", "race": "human", "class": "wizard",
        "alignment": "true_neutral",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 8, "dex": 14, "con": 14,
                       "int": 16, "wis": 12, "cha": 10}},
        "free_ability_choice": "int",
        "feats": ["iron_will", "great_fortitude"],
        "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
        "bonus_languages": [],
    })
    char = create_character(req, REGISTRY)
    return combatant_from_character(char, REGISTRY, (5, 5), "x")


# ---------------------------------------------------------------------------
# _classify_casting_time
# ---------------------------------------------------------------------------


class TestClassifyCastingTime(unittest.TestCase):
    def test_standard_default(self):
        self.assertEqual(_classify_casting_time("standard"), "standard")
        self.assertEqual(_classify_casting_time(""), "standard")

    def test_swift_variants(self):
        self.assertEqual(_classify_casting_time("swift"), "swift")
        self.assertEqual(_classify_casting_time("1 swift"), "swift")
        self.assertEqual(_classify_casting_time("1_swift"), "swift")

    def test_immediate(self):
        self.assertEqual(_classify_casting_time("immediate"), "immediate")
        self.assertEqual(_classify_casting_time("1 immediate"), "immediate")

    def test_one_round(self):
        self.assertEqual(_classify_casting_time("1 round"), "multi_round")
        self.assertEqual(_classify_casting_time("1_round"), "multi_round")

    def test_multiround(self):
        self.assertEqual(_classify_casting_time("3_rounds"), "multi_round")
        self.assertEqual(_classify_casting_time("10 rounds"), "multi_round")

    def test_full_round(self):
        self.assertEqual(_classify_casting_time("full_round"), "full_round")
        self.assertEqual(_classify_casting_time("full-round"), "full_round")

    def test_long_durations(self):
        self.assertEqual(_classify_casting_time("1_minute"), "multi_round")
        self.assertEqual(_classify_casting_time("8 hours"), "multi_round")
        self.assertEqual(_classify_casting_time("1_day"), "multi_round")


# ---------------------------------------------------------------------------
# Swift slot: native swift-time + quickened metamagic both accepted
# ---------------------------------------------------------------------------


class TestSwiftSlotAcceptsBoth(unittest.TestCase):
    def test_quickened_metamagic_still_works(self):
        """Metamagic-quickened cast in the swift slot still resolves."""
        c = _wizard()
        c.casting_type = "prepared"
        c.prepared_spells = {0: ["light"]}
        c.castable_spells = {"light"}
        c.resources["spell_slot_4"] = 1  # quickened bumps to L4 slot

        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                         (6, 5), "y")
        grid = Grid(width=12, height=12)
        grid.place(c)
        grid.place(target)
        enc = Encounter.begin(grid, [c, target], Roller(seed=1))

        do = {
            "swift": {
                "type": "cast", "spell": "light", "spell_level": 0,
                "metamagic": ["quicken_spell"],
                "target": target,
            },
        }
        intent = TurnIntent(rule_index=0, do=do, namespace={})
        result = execute_turn(c, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        # Should NOT skip with "swift cast requires …"
        for e in result.events:
            if e.kind == "skip" and "swift cast" in str(e.detail.get("reason", "")):
                self.fail(f"swift cast unexpectedly skipped: {e.detail}")

    def test_non_swift_non_quickened_in_swift_slot_skips(self):
        """A non-swift spell without quicken metamagic in the swift
        slot still skips (swift cast requires either)."""
        c = _wizard()
        c.casting_type = "prepared"
        c.prepared_spells = {0: ["light"]}
        c.castable_spells = {"light"}
        c.resources["spell_slot_0"] = 1
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                         (6, 5), "y")
        grid = Grid(width=12, height=12)
        grid.place(c)
        grid.place(target)
        enc = Encounter.begin(grid, [c, target], Roller(seed=1))

        do = {
            "swift": {
                "type": "cast", "spell": "light", "spell_level": 0,
                "target": target,
            },
        }
        intent = TurnIntent(rule_index=0, do=do, namespace={})
        result = execute_turn(c, intent, enc, grid, Roller(seed=1))
        skip = next(
            (e for e in result.events
             if e.kind == "skip"
             and "swift cast" in str(e.detail.get("reason", ""))),
            None,
        )
        self.assertIsNotNone(skip,
                             "expected swift-cast skip when not quickened")


# ---------------------------------------------------------------------------
# Multi-round casts emit a visibility event
# ---------------------------------------------------------------------------


class TestMultiRoundCastVisibility(unittest.TestCase):
    def test_sleep_emits_long_casting_time_event(self):
        """Sleep has casting_time '1 round'; _do_cast should emit a
        cast_long_casting_time event."""
        c = _wizard()
        c.casting_type = "prepared"
        c.prepared_spells = {1: ["sleep"]}
        c.castable_spells = {"sleep"}
        c.resources["spell_slot_1"] = 1

        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                         (8, 5), "y")
        grid = Grid(width=12, height=12)
        grid.place(c)
        grid.place(target)
        enc = Encounter.begin(grid, [c, target], Roller(seed=1))

        events: list = []
        _do_cast(c, {"spell": "sleep", "spell_level": 1, "target": target},
                 enc, grid, Roller(seed=1), {}, events)
        kinds = [e.kind for e in events]
        self.assertIn("cast_long_casting_time", kinds,
                      f"expected long-casting-time event for sleep; "
                      f"got {kinds}")
        evt = next(e for e in events if e.kind == "cast_long_casting_time")
        self.assertEqual(evt.detail["classification"], "multi_round")
        self.assertEqual(evt.detail["spell_id"], "sleep")

    def test_standard_cast_does_not_emit_long_event(self):
        """A standard-time spell (light) doesn't emit the visibility
        event."""
        c = _wizard()
        c.casting_type = "prepared"
        c.prepared_spells = {0: ["light"]}
        c.castable_spells = {"light"}
        c.resources["spell_slot_0"] = 4

        grid = Grid(width=12, height=12)
        grid.place(c)
        enc = Encounter.begin(grid, [c], Roller(seed=1))

        events: list = []
        _do_cast(c, {"spell": "light", "spell_level": 0, "target": c},
                 enc, grid, Roller(seed=1), {}, events)
        kinds = [e.kind for e in events]
        self.assertNotIn("cast_long_casting_time", kinds)

    def test_lesser_restoration_three_rounds(self):
        """lesser_restoration has casting_time '3_rounds'; classifies
        as multi_round."""
        spell = REGISTRY.get_spell("lesser_restoration")
        self.assertEqual(_classify_casting_time(spell.casting_time),
                         "multi_round")


if __name__ == "__main__":
    unittest.main()
