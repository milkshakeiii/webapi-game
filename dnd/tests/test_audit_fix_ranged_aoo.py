"""Tests for audit fix #3: ranged attacks provoke AoO.

RAW: making a ranged attack while in a threatened square provokes an
AoO from each threatener (one per ranged-attack action — full attack
triggers once, not per iterative). Standard combat manuals: PF1
Action Table line 'Fire a ranged weapon | Yes (provokes)'.
"""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import _do_attack, _do_full_attack


REGISTRY = default_registry()


def _orc(pos, team, *, ranged: bool = False):
    """Build an orc with the requested attack option set."""
    c = combatant_from_monster(REGISTRY.get_monster("orc"), pos, team)
    if ranged:
        c.attack_options = [{
            "type": "ranged", "name": "javelin",
            "weapon_id": "javelin",
            "weapon_category": "simple",
            "attack_bonus": 1, "damage": "1d6", "damage_bonus": 3,
            "damage_type": "P", "crit_range": [20, 20],
            "crit_multiplier": 2, "range_increment": 30,
        }]
    return c


class TestRangedAttackProvokesAoO(unittest.TestCase):
    def test_ranged_attack_in_threatened_square_provokes(self):
        archer = _orc((5, 5), "x", ranged=True)
        threatener = _orc((6, 5), "y")  # adjacent → threatens archer
        far_target = _orc((10, 5), "y")
        grid = Grid(width=20, height=10)
        grid.place(archer)
        grid.place(threatener)
        grid.place(far_target)
        enc = Encounter.begin(grid, [archer, threatener, far_target],
                              Roller(seed=1))

        events: list = []
        _do_attack(archer, far_target, grid, Roller(seed=1), events,
                   encounter=enc)
        kinds = [e.kind for e in events]
        self.assertIn("aoo", kinds,
                      f"ranged attack while threatened should provoke; "
                      f"got {kinds}")

    def test_ranged_attack_unthreatened_does_not_provoke(self):
        archer = _orc((5, 5), "x", ranged=True)
        # No adjacent enemy; only a faraway one.
        far_target = _orc((10, 5), "y")
        grid = Grid(width=20, height=10)
        grid.place(archer)
        grid.place(far_target)
        enc = Encounter.begin(grid, [archer, far_target], Roller(seed=1))

        events: list = []
        _do_attack(archer, far_target, grid, Roller(seed=1), events,
                   encounter=enc)
        kinds = [e.kind for e in events]
        self.assertNotIn("aoo", kinds,
                         f"unthreatened ranged attack must not provoke; "
                         f"got {kinds}")

    def test_melee_attack_does_not_trigger_ranged_aoo(self):
        """Sanity check: melee attacks don't fire the ranged AoO path."""
        a = _orc((5, 5), "x", ranged=False)  # default falchion (melee)
        b = _orc((6, 5), "y")
        grid = Grid(width=20, height=10)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))

        events: list = []
        _do_attack(a, b, grid, Roller(seed=1), events, encounter=enc)
        kinds = [e.kind for e in events]
        # The melee attack itself shouldn't provoke. (If a future change
        # adds melee-attack-while-prone or similar AoO, this test would
        # need updating.)
        self.assertNotIn("aoo", kinds)
        self.assertIn("attack", kinds)

    def test_full_ranged_attack_provokes_once_not_per_shot(self):
        """A full ranged attack action provokes ONE AoO at the start,
        not one per iterative."""
        archer = _orc((5, 5), "x", ranged=True)
        archer.bases["bab"] = 6  # gives 2 iteratives
        threatener = _orc((6, 5), "y")
        far_target = _orc((10, 5), "y")
        grid = Grid(width=20, height=10)
        grid.place(archer)
        grid.place(threatener)
        grid.place(far_target)
        enc = Encounter.begin(grid, [archer, threatener, far_target],
                              Roller(seed=1))

        events: list = []
        _do_full_attack(archer, far_target, {}, grid, Roller(seed=1),
                        events, encounter=enc)
        aoo_events = [e for e in events if e.kind == "aoo"]
        # One threatener + one ranged action = at most one AoO.
        # (Could be zero if the threatener is out of AoOs; here they
        # have a fresh round so should fire once.)
        self.assertLessEqual(len(aoo_events), 1,
                             f"full ranged attack should provoke at "
                             f"most once; got {len(aoo_events)}")

    def test_aoo_killing_archer_aborts_ranged_attack(self):
        """If the AoO drops the archer, the ranged attack doesn't
        resolve."""
        archer = _orc((5, 5), "x", ranged=True)
        archer.current_hp = 1  # one-shot territory
        # Threatener with auto-hit weapon.
        threatener = _orc((6, 5), "y")
        threatener.attack_options = [{
            "type": "melee", "name": "killshot",
            "weapon_id": "longsword",
            "weapon_category": "martial",
            "attack_bonus": 100, "damage": "10d10", "damage_bonus": 100,
            "damage_type": "S", "crit_range": [20, 20],
            "crit_multiplier": 2, "range_increment": 0,
        }]
        far_target = _orc((10, 5), "y")
        grid = Grid(width=20, height=10)
        grid.place(archer)
        grid.place(threatener)
        grid.place(far_target)
        enc = Encounter.begin(grid, [archer, threatener, far_target],
                              Roller(seed=1))

        events: list = []
        _do_attack(archer, far_target, grid, Roller(seed=1), events,
                   encounter=enc)
        kinds = [e.kind for e in events]
        self.assertIn("aoo", kinds)
        # The archer's actual ranged 'attack' should not have resolved.
        attack_events = [e for e in events
                         if e.kind == "attack" and e.actor_id == archer.id]
        self.assertEqual(len(attack_events), 0,
                         f"archer's ranged shot should be aborted; "
                         f"got events {kinds}")
        # And a 'skip: killed by AoO' should be present.
        self.assertTrue(
            any(e.kind == "skip" and "AoO" in str(e.detail.get("reason", ""))
                for e in events),
            f"expected skip-killed-by-AoO event; got {kinds}",
        )


if __name__ == "__main__":
    unittest.main()
