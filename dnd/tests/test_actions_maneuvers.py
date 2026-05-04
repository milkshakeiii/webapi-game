"""DSL v2 substrate Slice 2: combat maneuvers.

Covers ``Maneuver`` (the 10 maneuver kinds) and the four grapple-
maintenance actions (GrappleDamage / GrappleMove / GrapplePin /
GrappleBreakFree). Enumeration gates on slot consumption + adjacency
+ grappling-state; apply delegates to the existing ``_do_combat_*``
helpers in ``turn_executor``.
"""

from __future__ import annotations

import unittest

from dnd.engine.actions import (
    GameState,
    GrappleBreakFree,
    GrappleDamage,
    GrappleMove,
    GrapplePin,
    Maneuver,
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


def _build(actor_pos=(5, 5), enemy_pos=None):
    actor = _orc(actor_pos, "x")
    grid = Grid(width=12, height=12)
    grid.place(actor)
    others = []
    if enemy_pos is not None:
        e = _orc(enemy_pos, "y")
        grid.place(e)
        others.append(e)
    enc = Encounter.begin(grid, [actor, *others], Roller(seed=1))
    state = GameState(encounter=enc, grid=grid)
    return state, [actor, *others]


# ---------------------------------------------------------------------------
# Enumeration
# ---------------------------------------------------------------------------


class TestEnumerateManeuvers(unittest.TestCase):
    def test_all_ten_maneuvers_offered_against_adjacent_enemy(self):
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        actions = enumerate_legal_actions(actor, state)
        kinds = {a.kind for a in actions if isinstance(a, Maneuver)}
        expected = {"trip", "disarm", "sunder", "bull_rush", "grapple",
                    "drag", "overrun", "reposition", "steal",
                    "dirty_trick"}
        self.assertEqual(kinds, expected)

    def test_no_maneuvers_against_distant_enemy(self):
        state, [actor, enemy] = _build(enemy_pos=(10, 5))
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, Maneuver) for a in actions))

    def test_maneuvers_blocked_when_standard_used(self):
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        state.slots_for(actor).standard_used = True
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, Maneuver) for a in actions))

    def test_grapple_not_offered_when_already_grappling(self):
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        actor.grappling_target_id = enemy.id
        actor.add_condition("grappled")
        actions = enumerate_legal_actions(actor, state)
        # The "grapple" maneuver should be filtered out (can't initiate
        # a second grapple). Other maneuvers still valid via the
        # standard-action gate (though grappled makes some illegal —
        # PF1 RAW).
        grapple_initiations = [
            a for a in actions
            if isinstance(a, Maneuver) and a.kind == "grapple"
        ]
        self.assertEqual(grapple_initiations, [])


class TestEnumerateGrappleMaintenance(unittest.TestCase):
    def test_maintenance_offered_when_grappling(self):
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        actor.grappling_target_id = enemy.id
        actor.add_condition("grappled")
        enemy.grappled_by_id = actor.id
        enemy.add_condition("grappled")
        actions = enumerate_legal_actions(actor, state)
        self.assertTrue(any(isinstance(a, GrappleDamage) for a in actions))
        self.assertTrue(any(isinstance(a, GrapplePin) for a in actions))
        # GrappleMove enumerated per-direction.
        moves = [a for a in actions if isinstance(a, GrappleMove)]
        self.assertGreater(len(moves), 0)

    def test_break_free_offered_when_grappled_by_someone(self):
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        actor.grappled_by_id = enemy.id
        actor.add_condition("grappled")
        enemy.grappling_target_id = actor.id
        enemy.add_condition("grappled")
        actions = enumerate_legal_actions(actor, state)
        break_frees = [a for a in actions if isinstance(a, GrappleBreakFree)]
        # Two: CMB-based and Escape-Artist-based.
        self.assertEqual(len(break_frees), 2)
        self.assertTrue(any(a.use_skill for a in break_frees))
        self.assertTrue(any(not a.use_skill for a in break_frees))

    def test_no_maintenance_when_not_grappling(self):
        state, [actor] = _build()
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, GrappleDamage) for a in actions))
        self.assertFalse(any(isinstance(a, GrapplePin) for a in actions))
        self.assertFalse(any(isinstance(a, GrappleMove) for a in actions))
        self.assertFalse(any(isinstance(a, GrappleBreakFree) for a in actions))


# ---------------------------------------------------------------------------
# Apply
# ---------------------------------------------------------------------------


class TestApplyManeuver(unittest.TestCase):
    def test_trip_against_adjacent_enemy(self):
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        # Pin actor's CMB high so the trip definitely succeeds.
        actor.bases["cmb"] = 99
        result = apply_action(
            Maneuver(actor_id=actor.id, kind="trip", target_id=enemy.id),
            state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).standard_used)
        # On success, target gains prone.
        self.assertIn("prone", enemy.conditions)
        self.assertTrue(any(e.kind.startswith("maneuver_")
                            or "trip" in e.kind
                            for e in result.events))

    def test_grapple_links_both_combatants(self):
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        actor.bases["cmb"] = 99
        apply_action(
            Maneuver(actor_id=actor.id, kind="grapple", target_id=enemy.id),
            state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).standard_used)
        # Both combatants gain "grappled"; link fields set.
        self.assertIn("grappled", actor.conditions)
        self.assertIn("grappled", enemy.conditions)
        self.assertEqual(actor.grappling_target_id, enemy.id)
        self.assertEqual(enemy.grappled_by_id, actor.id)

    def test_dirty_trick_options_carried_through(self):
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        actor.bases["cmb"] = 99
        result = apply_action(
            Maneuver(
                actor_id=actor.id, kind="dirty_trick", target_id=enemy.id,
                options={"condition": "shaken"},
            ),
            state, Roller(seed=1),
        )
        # Target should pick up the chosen condition (shaken, not the
        # default dazzled).
        self.assertIn("shaken", enemy.conditions)


class TestApplyGrappleMaintenance(unittest.TestCase):
    def _setup_grappling(self):
        """Helper: place actor + enemy in a mutual grapple."""
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        actor.grappling_target_id = enemy.id
        actor.add_condition("grappled")
        enemy.grappled_by_id = actor.id
        enemy.add_condition("grappled")
        return state, actor, enemy

    def test_grapple_damage_marks_standard(self):
        state, actor, enemy = self._setup_grappling()
        actor.bases["cmb"] = 99
        apply_action(
            GrappleDamage(actor_id=actor.id), state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).standard_used)

    def test_grapple_pin_marks_standard(self):
        state, actor, enemy = self._setup_grappling()
        actor.bases["cmb"] = 99
        apply_action(
            GrapplePin(actor_id=actor.id), state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).standard_used)

    def test_grapple_move_in_direction(self):
        state, actor, enemy = self._setup_grappling()
        actor.bases["cmb"] = 99
        apply_action(
            GrappleMove(actor_id=actor.id, direction="north"),
            state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).standard_used)

    def test_grapple_break_free_marks_standard(self):
        state, actor, enemy = self._setup_grappling()
        # Swap roles: actor is being grappled by enemy.
        actor.grappling_target_id = None
        actor.grappled_by_id = enemy.id
        enemy.grappling_target_id = actor.id
        enemy.grappled_by_id = None
        actor.bases["cmb"] = 99
        apply_action(
            GrappleBreakFree(actor_id=actor.id),
            state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).standard_used)


if __name__ == "__main__":
    unittest.main()
