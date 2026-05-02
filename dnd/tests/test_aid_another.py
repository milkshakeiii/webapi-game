"""Tests for the Aid Another composite action."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.modifiers import compute as _compute
from dnd.engine.turn_executor import _do_aid_another


REGISTRY = default_registry()


def _setup():
    """Two allies adjacent to a single foe."""
    helper = combatant_from_monster(
        REGISTRY.get_monster("orc"), (5, 5), "team_a",
    )
    ally = combatant_from_monster(
        REGISTRY.get_monster("orc"), (4, 5), "team_a",
    )
    foe = combatant_from_monster(
        REGISTRY.get_monster("goblin"), (5, 6), "team_b",
    )
    grid = Grid(width=12, height=12)
    grid.place(helper)
    grid.place(ally)
    grid.place(foe)
    enc = Encounter.begin(grid, [helper, ally, foe], Roller(seed=1))
    return helper, ally, foe, grid, enc


class TestAidAnotherSuccess(unittest.TestCase):
    def _do(self, mode, seed=1):
        helper, ally, foe, grid, enc = _setup()
        events = []
        ns = {"ally": ally, "foe": foe}
        _do_aid_another(
            helper, {"ally": "ally", "foe": "foe", "mode": mode},
            enc, grid, Roller(seed=seed), ns, events,
        )
        return helper, ally, foe, events

    def test_attack_mode_grants_plus_2_to_ally_attack(self):
        # Run several seeds to find one that hits DC 10.
        for seed in range(1, 30):
            helper, ally, foe, events = self._do("attack", seed=seed)
            ev = events[0]
            if ev.detail["passed"]:
                bonus = _compute(0, ally.modifiers.for_target("attack"))
                self.assertEqual(bonus, 2)
                return
        self.skipTest("no successful aid roll across 30 seeds")

    def test_ac_mode_grants_plus_2_dodge_ac_to_ally(self):
        for seed in range(1, 30):
            helper, ally, foe, events = self._do("ac", seed=seed)
            ev = events[0]
            if ev.detail["passed"]:
                ac_before_aid = ally.ac()
                # The +2 dodge AC went directly into the modifier
                # collection; ally.ac() includes it now.
                # Compute "without aid" ac by stripping the modifier.
                aid_mods = [m for m in ally.modifiers.modifiers
                            if m.source.startswith("aid_another:")]
                self.assertTrue(aid_mods)
                self.assertEqual(aid_mods[0].value, 2)
                self.assertEqual(aid_mods[0].type, "dodge")
                self.assertEqual(aid_mods[0].target, "ac")
                return
        self.skipTest("no successful aid roll across 30 seeds")


class TestAidAnotherFailure(unittest.TestCase):
    def test_failed_aid_grants_no_bonus(self):
        # Use a helper with no attack bonus (synthetic) so DC 10 is
        # almost always failed unless we roll 10+ on d20.
        helper, ally, foe, grid, enc = _setup()
        helper.attack_options[0]["attack_bonus"] = -10
        events = []
        ns = {"ally": ally, "foe": foe}
        _do_aid_another(
            helper, {"ally": "ally", "foe": "foe", "mode": "attack"},
            enc, grid, Roller(seed=1), ns, events,
        )
        ev = events[0]
        self.assertFalse(ev.detail["passed"])
        self.assertEqual(_compute(0, ally.modifiers.for_target("attack")), 0)


class TestAidAnotherGuards(unittest.TestCase):
    def test_no_foe_skips(self):
        helper, ally, foe, grid, enc = _setup()
        events = []
        _do_aid_another(
            helper, {"ally": "ally", "foe": None, "mode": "attack"},
            enc, grid, Roller(seed=1), {"ally": ally}, events,
        )
        self.assertTrue(any(e.kind == "skip" for e in events))

    def test_foe_not_adjacent_skips(self):
        helper, ally, foe, grid, enc = _setup()
        # Move foe far away.
        grid.move(foe, (11, 11))
        events = []
        _do_aid_another(
            helper, {"ally": "ally", "foe": "foe", "mode": "attack"},
            enc, grid, Roller(seed=1), {"ally": ally, "foe": foe}, events,
        )
        skips = [e for e in events if e.kind == "skip"]
        self.assertTrue(skips)
        self.assertIn("not in melee reach", skips[0].detail.get("reason", ""))

    def test_unknown_mode_skips(self):
        helper, ally, foe, grid, enc = _setup()
        events = []
        _do_aid_another(
            helper, {"ally": "ally", "foe": "foe", "mode": "wibbly"},
            enc, grid, Roller(seed=1), {"ally": ally, "foe": foe}, events,
        )
        self.assertTrue(any(e.kind == "skip" for e in events))


class TestAidAnotherExpires(unittest.TestCase):
    def test_bonus_expires_at_end_of_round(self):
        for seed in range(1, 30):
            helper, ally, foe, grid, enc = _setup()
            events = []
            ns = {"ally": ally, "foe": foe}
            _do_aid_another(
                helper, {"ally": "ally", "foe": "foe", "mode": "attack"},
                enc, grid, Roller(seed=seed), ns, events,
            )
            ev = events[0]
            if not ev.detail["passed"]:
                continue
            # Bonus is present this round.
            self.assertEqual(
                _compute(0, ally.modifiers.for_target("attack")), 2,
            )
            # Tick to current_round + 1 — bonus expires.
            ally.tick_round(enc.round_number + 1)
            self.assertEqual(
                _compute(0, ally.modifiers.for_target("attack")), 0,
            )
            return
        self.skipTest("no successful aid roll across 30 seeds")


if __name__ == "__main__":
    unittest.main()
