"""DSL v2 Phase 3.1: AoO selection as a reactive-interrupt picker
decision.

When a movement / spell-cast / ranged-attack provokes from a
threatener, the threatener's registered ``Picker`` (on
``encounter.pickers``) chooses among ``TakeAoO`` (per available
weapon) and ``PassAoO``. With no picker registered, the engine
defaults to "take with weapon 0" — preserving v1 behavior so all
1234 existing tests stay green.

These tests exercise three things:

1. The default picker mirrors v1 (sanity).
2. A custom ``PassAoO`` picker actually skips the AoO when the
   threatener has the option to.
3. A custom weapon-index picker can choose a non-default weapon.
"""

from __future__ import annotations

import unittest

from dnd.engine.actions import (
    Action,
    GameState,
    PassAoO,
    Picker,
    TakeAoO,
)
from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import _do_aoo


REGISTRY = default_registry()


def _orc(pos, team):
    return combatant_from_monster(REGISTRY.get_monster("orc"), pos, team)


def _two_orcs():
    """Threatener at (5,5), provoker at (6,5). Returns the pair plus
    the live encounter so tests can inspect events."""
    threatener = _orc((5, 5), "x")
    provoker = _orc((6, 5), "y")
    grid = Grid(width=12, height=12)
    grid.place(threatener)
    grid.place(provoker)
    enc = Encounter.begin(grid, [threatener, provoker], Roller(seed=1))
    return threatener, provoker, grid, enc


# ---------------------------------------------------------------------------
# Default picker: v1-equivalent (TakeAoO with weapon 0)
# ---------------------------------------------------------------------------


class TestDefaultPicker(unittest.TestCase):
    def test_no_registered_picker_defaults_to_take_weapon_0(self):
        threatener, provoker, grid, enc = _two_orcs()
        events: list = []
        _do_aoo(threatener, provoker, grid, events, encounter=enc)
        kinds = [e.kind for e in events]
        self.assertIn("aoo", kinds)
        # Weapon 0 of an orc is the falchion.
        aoo = next(e for e in events if e.kind == "aoo")
        self.assertEqual(aoo.detail["weapon_index"], 0)


# ---------------------------------------------------------------------------
# Custom Pass picker
# ---------------------------------------------------------------------------


class _AlwaysPassPicker(Picker):
    def pick(self, actor, state, actions):
        for a in actions:
            if isinstance(a, PassAoO):
                return a
        return actions[0]


class TestPassPicker(unittest.TestCase):
    def test_pass_picker_skips_aoo(self):
        threatener, provoker, grid, enc = _two_orcs()
        enc.pickers[threatener.id] = _AlwaysPassPicker()
        before_hp = provoker.current_hp
        events: list = []
        _do_aoo(threatener, provoker, grid, events, encounter=enc)
        kinds = [e.kind for e in events]
        # No AoO event; an aoo_pass event instead.
        self.assertNotIn("aoo", kinds)
        self.assertIn("aoo_pass", kinds)
        # Provoker took no damage.
        self.assertEqual(provoker.current_hp, before_hp)
        # AoO budget not consumed (you can still take a real AoO later).
        self.assertEqual(threatener.aoos_used_this_round, 0)


# ---------------------------------------------------------------------------
# Weapon-index picker
# ---------------------------------------------------------------------------


class _PreferRangedPicker(Picker):
    """Pick the first TakeAoO whose weapon is ranged (per
    actor.attack_options[i].type)."""

    def pick(self, actor, state, actions):
        for a in actions:
            if isinstance(a, TakeAoO):
                opts = actor.attack_options
                if 0 <= a.weapon_index < len(opts):
                    if opts[a.weapon_index].get("type") == "ranged":
                        return a
        # Fallback: weapon 0 (default v1 behavior).
        for a in actions:
            if isinstance(a, TakeAoO) and a.weapon_index == 0:
                return a
        return actions[-1]  # Pass


class TestWeaponIndexPicker(unittest.TestCase):
    def test_picker_can_choose_non_default_weapon(self):
        # Orc has [falchion (melee, idx 0), javelin (ranged, idx 1)].
        threatener, provoker, grid, enc = _two_orcs()
        enc.pickers[threatener.id] = _PreferRangedPicker()
        events: list = []
        _do_aoo(threatener, provoker, grid, events, encounter=enc)
        aoo = next(e for e in events if e.kind == "aoo")
        # Picker should have selected weapon_index=1 (the javelin).
        self.assertEqual(aoo.detail["weapon_index"], 1)


# ---------------------------------------------------------------------------
# Picker sees only the legal-actions list (kind-blind contract)
# ---------------------------------------------------------------------------


class _RecordingPicker(Picker):
    def __init__(self):
        self.last_actions: list[Action] = []

    def pick(self, actor, state, actions):
        self.last_actions = list(actions)
        return actions[-1]  # Pass


class TestKindBlind(unittest.TestCase):
    def test_picker_sees_take_and_pass_actions(self):
        threatener, provoker, grid, enc = _two_orcs()
        rec = _RecordingPicker()
        enc.pickers[threatener.id] = rec
        events: list = []
        _do_aoo(threatener, provoker, grid, events, encounter=enc)
        kinds_offered = {type(a).__name__ for a in rec.last_actions}
        self.assertIn("TakeAoO", kinds_offered)
        self.assertIn("PassAoO", kinds_offered)
        # One TakeAoO per weapon plus one PassAoO; orc has 2 weapons.
        self.assertEqual(len(rec.last_actions), 3)


if __name__ == "__main__":
    unittest.main()
