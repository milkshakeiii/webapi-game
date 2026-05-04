"""DSL v2 substrate Slice 4: active grab bag.

Covers the move/standard/swift/free/full-round actions added beyond
the core movement+attack+cast set: AidAnother, FightDefensively,
Cleave, ChannelEnergy, StunningFist, BardicPerformance, DetectEvil,
DomainPower, EscapeWeb, DrinkPotion, SmiteEvil, RageStart, RageEnd,
DrawWeapon, StandUp, Mount, Dismount, Run, Trample, CoupDeGrace,
TailSpikeVolley.

Each is a thin wrapper over the existing _do_* helper. Tests verify
enumeration gates and slot consumption on apply.
"""

from __future__ import annotations

import unittest

from dnd.engine.actions import (
    AidAnother,
    Cleave,
    CoupDeGrace,
    DetectEvil,
    FightDefensively,
    GameState,
    RageEnd,
    RageStart,
    Run,
    SmiteEvil,
    StandUp,
    StunningFist,
    apply_action,
    enumerate_legal_actions,
)
from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid


REGISTRY = default_registry()


def _orc(pos, team="x"):
    return combatant_from_monster(REGISTRY.get_monster("orc"), pos, team)


def _build(actor_pos=(5, 5), enemy_pos=None, ally_pos=None):
    actor = _orc(actor_pos, "x")
    grid = Grid(width=12, height=12)
    grid.place(actor)
    others = []
    if enemy_pos is not None:
        e = _orc(enemy_pos, "y")
        grid.place(e)
        others.append(e)
    if ally_pos is not None:
        a = _orc(ally_pos, "x")
        grid.place(a)
        others.append(a)
    enc = Encounter.begin(grid, [actor, *others], Roller(seed=1))
    state = GameState(encounter=enc, grid=grid)
    return state, [actor, *others]


# ---------------------------------------------------------------------------
# Standard-action grab bag — enumeration
# ---------------------------------------------------------------------------


class TestEnumerateAidAnother(unittest.TestCase):
    def test_aid_another_offered_per_adjacent_ally(self):
        state, [actor, ally] = _build(actor_pos=(5, 5), ally_pos=(6, 5))
        actions = enumerate_legal_actions(actor, state)
        aids = [a for a in actions if isinstance(a, AidAnother)]
        # Two: mode='attack' and mode='ac'.
        self.assertEqual(len(aids), 2)
        self.assertEqual({a.mode for a in aids}, {"attack", "ac"})

    def test_no_aid_when_no_allies(self):
        state, [actor] = _build()
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, AidAnother) for a in actions))


class TestEnumerateFightDefensivelyAndCleave(unittest.TestCase):
    def test_fight_defensively_per_adjacent_foe(self):
        state, [actor, foe] = _build(enemy_pos=(6, 5))
        actions = enumerate_legal_actions(actor, state)
        fight_def = [a for a in actions if isinstance(a, FightDefensively)]
        self.assertEqual(len(fight_def), 1)
        self.assertEqual(fight_def[0].target_id, foe.id)

    def test_cleave_per_adjacent_foe(self):
        state, [actor, foe] = _build(enemy_pos=(6, 5))
        actions = enumerate_legal_actions(actor, state)
        cleaves = [a for a in actions if isinstance(a, Cleave)]
        self.assertEqual(len(cleaves), 1)
        self.assertEqual(cleaves[0].target_id, foe.id)


class TestEnumerateStunningFistGated(unittest.TestCase):
    def test_no_stunning_fist_without_uses(self):
        state, [actor, foe] = _build(enemy_pos=(6, 5))
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, StunningFist) for a in actions))

    def test_stunning_fist_offered_with_uses(self):
        state, [actor, foe] = _build(enemy_pos=(6, 5))
        actor.resources["stunning_fist_uses"] = 1
        actions = enumerate_legal_actions(actor, state)
        sf = [a for a in actions if isinstance(a, StunningFist)]
        self.assertEqual(len(sf), 1)
        self.assertEqual(sf[0].target_id, foe.id)


class TestEnumerateDetectEvil(unittest.TestCase):
    def test_detect_evil_always_offered(self):
        state, [actor] = _build()
        actions = enumerate_legal_actions(actor, state)
        self.assertTrue(any(isinstance(a, DetectEvil) for a in actions))


# ---------------------------------------------------------------------------
# Swift / Free actions — enumeration
# ---------------------------------------------------------------------------


class TestEnumerateSmiteEvil(unittest.TestCase):
    def test_smite_evil_gated_on_uses(self):
        state, [actor, foe] = _build(enemy_pos=(10, 5))
        # No uses → no smite.
        self.assertFalse(any(isinstance(a, SmiteEvil)
                             for a in enumerate_legal_actions(actor, state)))
        actor.resources["smite_evil_uses"] = 1
        # Should now offer one per visible enemy.
        smites = [
            a for a in enumerate_legal_actions(actor, state)
            if isinstance(a, SmiteEvil)
        ]
        self.assertEqual(len(smites), 1)
        self.assertEqual(smites[0].target_id, foe.id)


class TestEnumerateRage(unittest.TestCase):
    def test_rage_start_offered_when_rounds_available_and_not_raging(self):
        state, [actor] = _build()
        actor.resources["rage_rounds"] = 3
        actions = enumerate_legal_actions(actor, state)
        self.assertTrue(any(isinstance(a, RageStart) for a in actions))
        self.assertFalse(any(isinstance(a, RageEnd) for a in actions))

    def test_rage_end_offered_when_raging(self):
        state, [actor] = _build()
        actor.resources["rage_rounds"] = 3
        actor.add_condition("raging")
        actions = enumerate_legal_actions(actor, state)
        self.assertTrue(any(isinstance(a, RageEnd) for a in actions))
        self.assertFalse(any(isinstance(a, RageStart) for a in actions))

    def test_no_rage_actions_without_rounds(self):
        state, [actor] = _build()
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, RageStart) for a in actions))
        self.assertFalse(any(isinstance(a, RageEnd) for a in actions))


# ---------------------------------------------------------------------------
# Move-action grab bag — enumeration
# ---------------------------------------------------------------------------


class TestEnumerateStandUp(unittest.TestCase):
    def test_stand_up_offered_when_prone(self):
        state, [actor] = _build()
        actor.add_condition("prone")
        actions = enumerate_legal_actions(actor, state)
        self.assertTrue(any(isinstance(a, StandUp) for a in actions))

    def test_stand_up_not_offered_when_upright(self):
        state, [actor] = _build()
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, StandUp) for a in actions))


# ---------------------------------------------------------------------------
# Full-round grab bag — enumeration
# ---------------------------------------------------------------------------


class TestEnumerateRun(unittest.TestCase):
    def test_run_directions_offered(self):
        state, [actor] = _build()
        actions = enumerate_legal_actions(actor, state)
        runs = [a for a in actions if isinstance(a, Run)]
        # 8 directions, all open → 8 Run actions.
        self.assertEqual(len(runs), 8)


class TestEnumerateCoupDeGrace(unittest.TestCase):
    def test_coup_offered_against_helpless(self):
        state, [actor, foe] = _build(enemy_pos=(6, 5))
        foe.add_condition("helpless")
        actions = enumerate_legal_actions(actor, state)
        coups = [a for a in actions if isinstance(a, CoupDeGrace)]
        self.assertEqual(len(coups), 1)

    def test_no_coup_against_conscious_foe(self):
        state, [actor, foe] = _build(enemy_pos=(6, 5))
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, CoupDeGrace) for a in actions))


# ---------------------------------------------------------------------------
# Apply: smoke tests for slot accounting
# ---------------------------------------------------------------------------


class TestApplySmokeStandard(unittest.TestCase):
    def test_aid_another_marks_standard(self):
        state, [actor, ally] = _build(actor_pos=(5, 5), ally_pos=(6, 5))
        apply_action(
            AidAnother(actor_id=actor.id, ally_id=ally.id, mode="attack"),
            state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).standard_used)

    def test_fight_defensively_marks_standard(self):
        state, [actor, foe] = _build(enemy_pos=(6, 5))
        apply_action(
            FightDefensively(actor_id=actor.id, target_id=foe.id),
            state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).standard_used)

    def test_detect_evil_marks_standard(self):
        state, [actor] = _build()
        apply_action(
            DetectEvil(actor_id=actor.id), state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).standard_used)


class TestApplySmokeMove(unittest.TestCase):
    def test_stand_up_marks_move(self):
        state, [actor] = _build()
        actor.add_condition("prone")
        apply_action(
            StandUp(actor_id=actor.id), state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).move_used)
        self.assertNotIn("prone", actor.conditions)


class TestApplySmokeFullRound(unittest.TestCase):
    def test_run_marks_full_round(self):
        state, [actor] = _build()
        apply_action(
            Run(actor_id=actor.id, direction="east"),
            state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).full_round_used)


class TestApplySmokeFreeAndSwift(unittest.TestCase):
    def test_smite_marks_swift(self):
        state, [actor, foe] = _build(enemy_pos=(6, 5))
        actor.resources["smite_evil_uses"] = 1
        apply_action(
            SmiteEvil(actor_id=actor.id, target_id=foe.id),
            state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).swift_used)


if __name__ == "__main__":
    unittest.main()
