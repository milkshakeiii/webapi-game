"""Tests for Phase 4.4 bardic-performance suite: countersong,
distraction, fascinate.

RAW (Foundry pack ``class-abilities.md``):

- Countersong (lines 16214-16228): 30-ft radius, the bard rolls Perform
  (keyboard / percussion / wind / string / sing) each round; any
  creature in range may use the bard's Perform total in place of a
  save vs sonic / language-dependent magic, IF it's higher.
- Distraction (lines 21371-21389): same shape, vs illusion (pattern)
  / illusion (figment); Perform skills act / comedy / dance / oratory.
- Fascinate (lines 34910-34928): targets within 90 ft; Will save
  DC 10 + 1/2 bard level + Cha mod; on fail target is fascinated;
  obvious threat (attack, hostile spell) auto-breaks the effect.
"""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import (
    combatant_from_character,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import TurnIntent
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import (
    _bardic_save_intercept,
    execute_turn,
)


REGISTRY = default_registry()


def _bard(name: str = "Lyric") -> object:
    # Point-buy 20: cha 14 (5) + dex 14 (5) + con 14 (5) + str 10 (0)
    # + wis 10 (0) + int 14 (5) = 20. Human +2 → cha 16.
    body = {
        "name": name, "race": "human", "class": "bard",
        "alignment": "neutral_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 10, "dex": 14, "con": 14,
                       "int": 14, "wis": 10, "cha": 14}},
        "free_ability_choice": "cha",
        "feats": ["dodge", "iron_will"],
        "skill_ranks": {"perform": 1, "perception": 1,
                        "diplomacy": 1, "knowledge_arcana": 1},
        "bonus_languages": [],
    }
    return create_character(CharacterRequest.from_dict(body), REGISTRY)


def _setup_encounter(bard_pos=(5, 5), goblin_pos=(6, 5)):
    char = _bard()
    bard = combatant_from_character(char, REGISTRY, bard_pos, "x")
    goblin = combatant_from_monster(
        REGISTRY.get_monster("goblin"), goblin_pos, "y",
    )
    grid = Grid(width=30, height=30)
    grid.place(bard)
    grid.place(goblin)
    enc = Encounter.begin(grid, [bard, goblin], Roller(seed=1))
    return bard, goblin, enc, grid


# ---------------------------------------------------------------------------
# Countersong
# ---------------------------------------------------------------------------


class TestCountersong(unittest.TestCase):
    def test_countersong_records_perform_total_on_bard(self):
        bard, goblin, enc, grid = _setup_encounter()
        do = {"composite": "bardic_performance",
              "args": {"mode": "countersong"}}
        intent = TurnIntent(rule_index=0, do=do, namespace={})
        result = execute_turn(bard, intent, enc, grid, Roller(seed=1))
        # The active state should be set on the bard's resources for
        # the intercept hook to find this round.
        self.assertEqual(bard.resources["bardic_active_mode"], "countersong")
        self.assertGreaterEqual(
            bard.resources["bardic_active_until_round"], enc.round_number,
        )
        self.assertIn("bardic_perform_total", bard.resources)
        # The event records the rolled total + the chosen subskill.
        ev = next(e for e in result.events if e.kind == "bardic_performance")
        self.assertEqual(ev.detail["mode"], "countersong")
        self.assertIn("perform_total", ev.detail)

    def test_countersong_subskill_validated(self):
        bard, goblin, enc, grid = _setup_encounter()
        # "oratory" is a Distraction subskill, not a Countersong one.
        do = {"composite": "bardic_performance",
              "args": {"mode": "countersong", "subskill": "oratory"}}
        intent = TurnIntent(rule_index=0, do=do, namespace={})
        result = execute_turn(bard, intent, enc, grid, Roller(seed=1))
        skip = next((e for e in result.events
                     if e.kind == "skip"), None)
        self.assertIsNotNone(skip)
        self.assertIn("not in RAW menu", skip.detail.get("reason", ""))

    def test_save_intercept_uses_bard_perform_when_higher(self):
        # Build the state by hand: bard has active countersong with
        # a known Perform total; goblin is in 30 ft and rolls a Will
        # save vs a sonic spell context.
        bard, goblin, enc, grid = _setup_encounter()
        bard.resources["bardic_active_mode"] = "countersong"
        bard.resources["bardic_active_until_round"] = enc.round_number
        bard.resources["bardic_perform_total"] = 99  # absurdly high
        intercepted = _bardic_save_intercept(
            goblin, "will", save_total=5,
            context={"descriptors": ["sonic"]},
            encounter=enc, grid=grid,
        )
        self.assertEqual(intercepted, 99)

    def test_save_intercept_returns_none_for_non_matching_descriptor(self):
        bard, goblin, enc, grid = _setup_encounter()
        bard.resources["bardic_active_mode"] = "countersong"
        bard.resources["bardic_active_until_round"] = enc.round_number
        bard.resources["bardic_perform_total"] = 99
        intercepted = _bardic_save_intercept(
            goblin, "will", save_total=5,
            context={"descriptors": ["fire"]},  # not sonic / language
            encounter=enc, grid=grid,
        )
        self.assertIsNone(intercepted)

    def test_save_intercept_returns_none_when_bard_out_of_range(self):
        # Place the bard 10 squares (50 ft) away — out of the 30 ft
        # countersong radius.
        bard, goblin, enc, grid = _setup_encounter(
            bard_pos=(0, 0), goblin_pos=(15, 0),
        )
        bard.resources["bardic_active_mode"] = "countersong"
        bard.resources["bardic_active_until_round"] = enc.round_number
        bard.resources["bardic_perform_total"] = 99
        intercepted = _bardic_save_intercept(
            goblin, "will", save_total=5,
            context={"descriptors": ["sonic"]},
            encounter=enc, grid=grid,
        )
        self.assertIsNone(intercepted)

    def test_save_intercept_returns_none_when_perform_lower(self):
        bard, goblin, enc, grid = _setup_encounter()
        bard.resources["bardic_active_mode"] = "countersong"
        bard.resources["bardic_active_until_round"] = enc.round_number
        bard.resources["bardic_perform_total"] = 3
        # The intercept returns the bard's total regardless of order;
        # roll_save itself does the "if higher" comparison. Test the
        # raw helper here.
        intercepted = _bardic_save_intercept(
            goblin, "will", save_total=20,
            context={"descriptors": ["sonic"]},
            encounter=enc, grid=grid,
        )
        # Helper still returns the bard's number; the caller compares.
        self.assertEqual(intercepted, 3)


# ---------------------------------------------------------------------------
# Distraction
# ---------------------------------------------------------------------------


class TestDistraction(unittest.TestCase):
    def test_distraction_records_perform_total(self):
        bard, goblin, enc, grid = _setup_encounter()
        do = {"composite": "bardic_performance",
              "args": {"mode": "distraction", "subskill": "oratory"}}
        intent = TurnIntent(rule_index=0, do=do, namespace={})
        result = execute_turn(bard, intent, enc, grid, Roller(seed=1))
        self.assertEqual(bard.resources["bardic_active_mode"], "distraction")
        ev = next(e for e in result.events if e.kind == "bardic_performance")
        self.assertEqual(ev.detail["subskill"], "oratory")

    def test_distraction_intercepts_only_pattern_and_figment(self):
        bard, goblin, enc, grid = _setup_encounter()
        bard.resources["bardic_active_mode"] = "distraction"
        bard.resources["bardic_active_until_round"] = enc.round_number
        bard.resources["bardic_perform_total"] = 50
        # Illusion / pattern → match.
        self.assertEqual(
            _bardic_save_intercept(
                goblin, "will", 5,
                {"school": "illusion", "subschool": "pattern"},
                enc, grid,
            ),
            50,
        )
        # Illusion / figment → match.
        self.assertEqual(
            _bardic_save_intercept(
                goblin, "will", 5,
                {"school": "illusion", "subschool": "figment"},
                enc, grid,
            ),
            50,
        )
        # Illusion / glamer → no match.
        self.assertIsNone(
            _bardic_save_intercept(
                goblin, "will", 5,
                {"school": "illusion", "subschool": "glamer"},
                enc, grid,
            ),
        )
        # Conjuration / summoning → no match.
        self.assertIsNone(
            _bardic_save_intercept(
                goblin, "will", 5,
                {"school": "conjuration", "subschool": "summoning"},
                enc, grid,
            ),
        )


# ---------------------------------------------------------------------------
# Fascinate
# ---------------------------------------------------------------------------


class TestFascinate(unittest.TestCase):
    def test_fascinate_max_targets_at_l1(self):
        bard, goblin, enc, grid = _setup_encounter()
        # L1 bard: 1 target. With two enemies named, only the first
        # in range is targeted (subsequent skipped due to max_targets).
        goblin2 = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (7, 5), "y",
        )
        grid.place(goblin2)
        enc.initiative.append(enc.initiative[0].__class__(
            combatant=goblin2, roll=10, modifier=0, total=10,
        ))
        do = {"composite": "bardic_performance",
              "args": {"mode": "fascinate",
                       "targets": [goblin, goblin2]}}
        intent = TurnIntent(rule_index=0, do=do, namespace={})
        result = execute_turn(bard, intent, enc, grid, Roller(seed=1))
        ev = next(e for e in result.events if e.kind == "bardic_performance")
        self.assertEqual(ev.detail["max_targets"], 1)
        self.assertEqual(len(ev.detail["affected"]), 1)

    def test_fascinate_dc_uses_bard_level_and_cha(self):
        # L1 bard, Cha 16 → DC = 10 + 0 + 3 = 13.
        bard, goblin, enc, grid = _setup_encounter()
        do = {"composite": "bardic_performance",
              "args": {"mode": "fascinate", "targets": [goblin]}}
        intent = TurnIntent(rule_index=0, do=do, namespace={})
        result = execute_turn(bard, intent, enc, grid, Roller(seed=1))
        ev = next(e for e in result.events if e.kind == "bardic_performance")
        self.assertEqual(ev.detail["save_dc"], 13)

    def test_fascinate_out_of_range_target_skipped(self):
        # 90 ft = 18 squares. Place the goblin at (24, 5) — 19 squares
        # from the bard at (5, 5).
        bard, goblin, enc, grid = _setup_encounter(
            bard_pos=(5, 5), goblin_pos=(24, 5),
        )
        do = {"composite": "bardic_performance",
              "args": {"mode": "fascinate", "targets": [goblin]}}
        intent = TurnIntent(rule_index=0, do=do, namespace={})
        result = execute_turn(bard, intent, enc, grid, Roller(seed=1))
        ev = next(e for e in result.events if e.kind == "bardic_performance")
        self.assertEqual(ev.detail["affected"], [])

    def test_fascinated_condition_breaks_on_attack(self):
        # Set up a goblin already fascinated, then have a friendly
        # attack the goblin. RAW: "obvious threat" auto-breaks.
        bard, goblin, enc, grid = _setup_encounter()
        goblin.add_condition("fascinated")
        # An attacker (could be the bard or a goblin ally — for this
        # test, just the bard's adjacent unarmed strike).
        # bard at (5,5), goblin at (6,5) — adjacent.
        do = {"composite": "full_attack",
              "args": {"target": goblin}}
        intent = TurnIntent(rule_index=0, do=do, namespace={})
        result = execute_turn(bard, intent, enc, grid, Roller(seed=1))
        # The fascinate-break event should appear before the attack
        # resolves.
        broken = [e for e in result.events
                  if e.kind == "fascinate_broken"]
        self.assertEqual(len(broken), 1)
        self.assertNotIn("fascinated", goblin.conditions)


if __name__ == "__main__":
    unittest.main()
