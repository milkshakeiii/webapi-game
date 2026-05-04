"""Phase 1 substrate tests for the decision-point DSL.

Covers ``enumerate_legal_actions`` and ``apply_action`` for the
core action types: Move, FiveFootStep, Attack, FullAttack, Charge,
Withdraw, TotalDefense, EndTurn.

The substrate runs alongside (not instead of) the v1 executor; these
tests exercise it in isolation. Phase 2 will wire it into
``execute_turn`` with a parity harness.
"""

from __future__ import annotations

import unittest

from dnd.engine.actions import (
    Action,
    Attack,
    Charge,
    EndTurn,
    FiveFootStep,
    FullAttack,
    GameState,
    Move,
    TotalDefense,
    Withdraw,
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


def _build(actor_pos=(5, 5), enemy_pos=None, ally_pos=None,
           grid_w=12, grid_h=12) -> tuple[GameState, list]:
    """Place the actor (an orc on team x) plus optional foes/allies.
    Returns ``(state, [actor, ...others])``."""
    actor = _orc(actor_pos, team="x")
    grid = Grid(width=grid_w, height=grid_h)
    grid.place(actor)
    others = []
    if enemy_pos is not None:
        e = _orc(enemy_pos, team="y")
        grid.place(e)
        others.append(e)
    if ally_pos is not None:
        a = _orc(ally_pos, team="x")
        grid.place(a)
        others.append(a)
    enc = Encounter.begin(grid, [actor, *others], Roller(seed=1))
    state = GameState(encounter=enc, grid=grid)
    return state, [actor, *others]


# ---------------------------------------------------------------------------
# enumerate_legal_actions
# ---------------------------------------------------------------------------


class TestEnumerateAlwaysIncludesEndTurn(unittest.TestCase):
    def test_end_turn_is_always_present(self):
        state, [actor] = _build()
        actions = enumerate_legal_actions(actor, state)
        self.assertTrue(any(isinstance(a, EndTurn) for a in actions))

    def test_dead_actor_only_can_end_turn(self):
        state, [actor] = _build()
        actor.add_condition("dead")
        actions = enumerate_legal_actions(actor, state)
        self.assertEqual(len(actions), 1)
        self.assertIsInstance(actions[0], EndTurn)

    def test_paralyzed_actor_only_can_end_turn(self):
        state, [actor] = _build()
        actor.add_condition("paralyzed")
        actions = enumerate_legal_actions(actor, state)
        self.assertEqual(len(actions), 1)
        self.assertIsInstance(actions[0], EndTurn)


class TestEnumerateMovement(unittest.TestCase):
    def test_movement_offered_when_speed_available(self):
        state, [actor] = _build(actor_pos=(5, 5))
        actions = enumerate_legal_actions(actor, state)
        moves = [a for a in actions if isinstance(a, Move)]
        # Orc speed 30 → 6 squares; expect a non-trivial reachable set.
        self.assertGreater(len(moves), 5)
        # Target square (6, 5) — one square east of (5,5) — should be
        # reachable in one step.
        self.assertTrue(any(m.destination == (6, 5) for m in moves))

    def test_movement_not_offered_when_already_used(self):
        state, [actor] = _build()
        slots = state.slots_for(actor)
        slots.move_used = True
        slots.movement_taken = True
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, Move) for a in actions))

    def test_five_foot_step_offered_to_adjacent_squares(self):
        state, [actor] = _build(actor_pos=(5, 5))
        actions = enumerate_legal_actions(actor, state)
        steps = [a for a in actions if isinstance(a, FiveFootStep)]
        # 8 adjacent squares (no occupants nearby).
        self.assertEqual(len(steps), 8)

    def test_five_foot_step_not_offered_after_movement(self):
        state, [actor] = _build()
        slots = state.slots_for(actor)
        slots.movement_taken = True
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, FiveFootStep) for a in actions))

    def test_grappled_actor_no_movement_or_5ft(self):
        state, [actor] = _build()
        actor.add_condition("grappled")
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, Move) for a in actions))
        self.assertFalse(any(isinstance(a, FiveFootStep) for a in actions))


class TestEnumerateAttacks(unittest.TestCase):
    def test_attack_offered_against_adjacent_enemy(self):
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        actions = enumerate_legal_actions(actor, state)
        attacks = [a for a in actions if isinstance(a, Attack)]
        self.assertEqual(len(attacks), 1)
        self.assertEqual(attacks[0].target_id, enemy.id)

    def test_attack_not_offered_against_distant_melee_target(self):
        state, [actor, enemy] = _build(enemy_pos=(10, 5))
        actions = enumerate_legal_actions(actor, state)
        # Default orc primary is a melee falchion; distant enemy not
        # in melee range, so no Attack offered.
        self.assertFalse(any(isinstance(a, Attack) for a in actions))

    def test_attack_not_offered_against_ally(self):
        state, [actor, ally] = _build(ally_pos=(6, 5))
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, Attack) for a in actions))

    def test_attack_not_offered_when_standard_used(self):
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        state.slots_for(actor).standard_used = True
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, Attack) for a in actions))


class TestEnumerateFullRound(unittest.TestCase):
    def test_full_attack_offered_against_adjacent_enemy(self):
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        actions = enumerate_legal_actions(actor, state)
        full_attacks = [a for a in actions if isinstance(a, FullAttack)]
        self.assertEqual(len(full_attacks), 1)
        self.assertEqual(full_attacks[0].target_id, enemy.id)

    def test_charge_offered_within_double_speed(self):
        # Speed 30 → 6 squares; charge = 12 squares max. Place enemy
        # at distance 5 (well within charge range, > 2 squares away).
        state, [actor, enemy] = _build(actor_pos=(2, 5), enemy_pos=(7, 5))
        actions = enumerate_legal_actions(actor, state)
        charges = [a for a in actions if isinstance(a, Charge)]
        self.assertEqual(len(charges), 1)

    def test_charge_not_offered_to_adjacent_enemy(self):
        # PF1 RAW: charge requires moving ≥ 10 ft (2 squares).
        state, [actor, enemy] = _build(actor_pos=(5, 5), enemy_pos=(6, 5))
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, Charge) for a in actions))

    def test_full_round_actions_not_offered_after_standard_used(self):
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        state.slots_for(actor).standard_used = True
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, FullAttack) for a in actions))
        self.assertFalse(any(isinstance(a, Charge) for a in actions))
        self.assertFalse(any(isinstance(a, Withdraw) for a in actions))


class TestEnumerateTotalDefense(unittest.TestCase):
    def test_total_defense_offered_when_standard_available(self):
        state, [actor] = _build()
        actions = enumerate_legal_actions(actor, state)
        self.assertTrue(any(isinstance(a, TotalDefense) for a in actions))

    def test_total_defense_not_offered_when_standard_used(self):
        state, [actor] = _build()
        state.slots_for(actor).standard_used = True
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, TotalDefense) for a in actions))


# ---------------------------------------------------------------------------
# apply_action
# ---------------------------------------------------------------------------


class TestApplyEndTurn(unittest.TestCase):
    def test_end_turn_marks_slot(self):
        state, [actor] = _build()
        result = apply_action(EndTurn(actor_id=actor.id),
                              state, Roller(seed=1))
        self.assertEqual(result.events, [])
        self.assertTrue(state.slots_for(actor).turn_ended)


class TestApplyMove(unittest.TestCase):
    def test_move_changes_position_and_marks_slot(self):
        state, [actor] = _build(actor_pos=(5, 5))
        before = actor.position
        result = apply_action(
            Move(actor_id=actor.id, destination=(7, 5)),
            state, Roller(seed=1),
        )
        self.assertNotEqual(actor.position, before)
        slots = state.slots_for(actor)
        self.assertTrue(slots.move_used)
        self.assertTrue(slots.movement_taken)
        # Move events emitted.
        self.assertTrue(any(e.kind == "move" for e in result.events))


class TestApplyFiveFootStep(unittest.TestCase):
    def test_five_foot_step_to_adjacent(self):
        state, [actor] = _build(actor_pos=(5, 5))
        result = apply_action(
            FiveFootStep(actor_id=actor.id, destination=(6, 5)),
            state, Roller(seed=1),
        )
        self.assertEqual(actor.position, (6, 5))
        slots = state.slots_for(actor)
        self.assertTrue(slots.five_foot_step_used)
        self.assertTrue(slots.movement_taken)
        self.assertTrue(any(e.kind == "move" for e in result.events))


class TestApplyAttack(unittest.TestCase):
    def test_attack_emits_event_and_marks_standard(self):
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        result = apply_action(
            Attack(actor_id=actor.id, target_id=enemy.id),
            state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).standard_used)
        self.assertTrue(any(e.kind == "attack" for e in result.events))


class TestApplyFullAttack(unittest.TestCase):
    def test_full_attack_marks_full_round(self):
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        result = apply_action(
            FullAttack(actor_id=actor.id, target_id=enemy.id),
            state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).full_round_used)
        # At least one attack-like event emitted (label = "full_attack_<i>").
        self.assertTrue(any("attack" in e.kind for e in result.events))


class TestApplyCharge(unittest.TestCase):
    def test_charge_resolves_and_marks_full_round(self):
        state, [actor, enemy] = _build(actor_pos=(2, 5), enemy_pos=(7, 5))
        result = apply_action(
            Charge(actor_id=actor.id, target_id=enemy.id),
            state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).full_round_used)
        # Should have produced at least move events and an attack.
        kinds = [e.kind for e in result.events]
        self.assertIn("move", kinds)


class TestApplyWithdraw(unittest.TestCase):
    def test_withdraw_marks_full_round(self):
        state, [actor] = _build(actor_pos=(5, 5))
        result = apply_action(
            Withdraw(actor_id=actor.id, direction="east"),
            state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).full_round_used)


class TestApplyTotalDefense(unittest.TestCase):
    def test_total_defense_adds_dodge_modifier(self):
        state, [actor] = _build()
        before_ac = actor.ac()
        result = apply_action(
            TotalDefense(actor_id=actor.id), state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).standard_used)
        self.assertEqual(actor.ac() - before_ac, 4)
        self.assertTrue(any(e.kind == "total_defense" for e in result.events))


# ---------------------------------------------------------------------------
# Slot-accounting interplay
# ---------------------------------------------------------------------------


class TestSlotAccountingChain(unittest.TestCase):
    def test_move_then_attack_legal_sequence(self):
        state, [actor, enemy] = _build(actor_pos=(2, 5), enemy_pos=(7, 5))
        # Step 1: enumerate offers Move toward enemy.
        actions = enumerate_legal_actions(actor, state)
        move_to_adjacent = next(
            a for a in actions
            if isinstance(a, Move) and a.destination == (6, 5)
        )
        apply_action(move_to_adjacent, state, Roller(seed=1))
        # Step 2: enumerate now offers Attack but not Move.
        actions = enumerate_legal_actions(actor, state)
        self.assertFalse(any(isinstance(a, Move) for a in actions))
        attacks = [a for a in actions if isinstance(a, Attack)]
        self.assertEqual(len(attacks), 1)
        self.assertEqual(attacks[0].target_id, enemy.id)

    def test_full_round_blocks_subsequent_actions(self):
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        apply_action(
            FullAttack(actor_id=actor.id, target_id=enemy.id),
            state, Roller(seed=1),
        )
        actions = enumerate_legal_actions(actor, state)
        # Only EndTurn should remain.
        non_end_turn = [a for a in actions if not isinstance(a, EndTurn)]
        self.assertEqual(non_end_turn, [])


class TestResetTurn(unittest.TestCase):
    def test_reset_turn_clears_slots(self):
        state, [actor, enemy] = _build(enemy_pos=(6, 5))
        apply_action(
            FullAttack(actor_id=actor.id, target_id=enemy.id),
            state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(actor).full_round_used)
        state.reset_turn(actor)
        self.assertFalse(state.slots_for(actor).full_round_used)
        actions = enumerate_legal_actions(actor, state)
        self.assertTrue(any(isinstance(a, FullAttack) for a in actions))


if __name__ == "__main__":
    unittest.main()
