"""Phase 2 parity harness for the DSL v2 migration.

Two test layers:

1. ``translate_intent`` — assert that representative v1 ``TurnIntent``
   shapes compile to the right sequence of substrate Actions.
2. ``run_intent_via_substrate`` — assert the substrate-driven runner
   produces the same observable end-state as ``execute_turn`` for a
   handful of scenarios. (Not a byte-for-byte event match — the
   substrate may legitimately reorder cosmetic events. We assert
   final HP / position / conditions are the same.)

Once parity is solid here, Phase 2.2 will flip a feature flag in
``execute_turn`` to route the entire test suite through the substrate;
Phase 2.3 will tear out the v1 dispatch.
"""

from __future__ import annotations

import unittest

from dnd.engine.actions import (
    Attack,
    Cast,
    Charge,
    EndTurn,
    FiveFootStep,
    FullAttack,
    Maneuver,
    Move,
    StandUp,
    TotalDefense,
    run_intent_via_substrate,
    translate_intent,
)
from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import TurnIntent
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


def _orc(pos, team):
    return combatant_from_monster(REGISTRY.get_monster("orc"), pos, team)


def _build(actor_pos=(5, 5), enemy_pos=None):
    actor = _orc(actor_pos, "x")
    grid = Grid(width=20, height=10)
    grid.place(actor)
    others = []
    if enemy_pos is not None:
        e = _orc(enemy_pos, "y")
        grid.place(e)
        others.append(e)
    enc = Encounter.begin(grid, [actor, *others], Roller(seed=1))
    return enc, grid, actor, others


# ---------------------------------------------------------------------------
# translate_intent
# ---------------------------------------------------------------------------


class TestTranslateSimpleSlots(unittest.TestCase):
    def test_attack_standard_slot_compiles_to_attack(self):
        enc, grid, actor, [enemy] = _build(enemy_pos=(6, 5))
        do = {"slots": {"standard": {"type": "attack", "target": enemy}}}
        actions = translate_intent(do, actor, enc, grid)
        # [Attack(...), EndTurn]
        self.assertEqual(len(actions), 2)
        self.assertIsInstance(actions[0], Attack)
        self.assertEqual(actions[0].target_id, enemy.id)
        self.assertIsInstance(actions[1], EndTurn)

    def test_total_defense_standard_slot_compiles(self):
        enc, grid, actor, _ = _build()
        do = {"slots": {"standard": {"type": "total_defense"}}}
        actions = translate_intent(do, actor, enc, grid)
        self.assertEqual(len(actions), 2)
        self.assertIsInstance(actions[0], TotalDefense)
        self.assertIsInstance(actions[1], EndTurn)

    def test_move_to_compiles_to_move(self):
        enc, grid, actor, _ = _build(actor_pos=(5, 5))
        do = {"slots": {"move": {"type": "move_to", "target": (8, 5)}}}
        actions = translate_intent(do, actor, enc, grid)
        self.assertIsInstance(actions[0], Move)
        self.assertEqual(actions[0].destination, (8, 5))

    def test_move_toward_resolves_destination(self):
        enc, grid, actor, [enemy] = _build(actor_pos=(2, 5), enemy_pos=(10, 5))
        do = {"slots": {"move": {"type": "move_toward", "target": enemy}}}
        actions = translate_intent(do, actor, enc, grid)
        self.assertIsInstance(actions[0], Move)
        # Destination should be closer to enemy than start was.
        self.assertGreater(actions[0].destination[0], 2)

    def test_stand_up_compiles_to_standup(self):
        enc, grid, actor, _ = _build()
        do = {"slots": {"move": {"type": "stand_up"}}}
        actions = translate_intent(do, actor, enc, grid)
        self.assertIsInstance(actions[0], StandUp)

    def test_five_foot_step_compiles_to_fivefootstep(self):
        enc, grid, actor, _ = _build(actor_pos=(5, 5))
        do = {"slots": {"five_foot_step": (6, 5)}}
        actions = translate_intent(do, actor, enc, grid)
        self.assertIsInstance(actions[0], FiveFootStep)
        self.assertEqual(actions[0].destination, (6, 5))

    def test_move_plus_standard_compiles_in_order(self):
        """Both slots → both Actions in order: move first, then standard,
        then EndTurn."""
        enc, grid, actor, [enemy] = _build(actor_pos=(2, 5), enemy_pos=(8, 5))
        do = {"slots": {
            "move": {"type": "move_toward", "target": enemy},
            "standard": {"type": "attack", "target": enemy},
        }}
        actions = translate_intent(do, actor, enc, grid)
        self.assertEqual(len(actions), 3)
        self.assertIsInstance(actions[0], Move)
        self.assertIsInstance(actions[1], Attack)
        self.assertIsInstance(actions[2], EndTurn)


class TestTranslateComposites(unittest.TestCase):
    def test_charge_compiles_to_charge(self):
        enc, grid, actor, [enemy] = _build(actor_pos=(2, 5), enemy_pos=(8, 5))
        do = {"composite": "charge", "args": {"target": enemy}}
        actions = translate_intent(do, actor, enc, grid)
        self.assertIsInstance(actions[0], Charge)
        self.assertEqual(actions[0].target_id, enemy.id)

    def test_full_attack_compiles_to_fullattack(self):
        enc, grid, actor, [enemy] = _build(enemy_pos=(6, 5))
        do = {"composite": "full_attack", "args": {"target": enemy}}
        actions = translate_intent(do, actor, enc, grid)
        self.assertIsInstance(actions[0], FullAttack)

    def test_hold_compiles_to_endturn_only(self):
        enc, grid, actor, _ = _build()
        do = {"composite": "hold"}
        actions = translate_intent(do, actor, enc, grid)
        # No Action besides EndTurn.
        self.assertEqual(len(actions), 1)
        self.assertIsInstance(actions[0], EndTurn)

    def test_combat_maneuver_composite(self):
        enc, grid, actor, [enemy] = _build(enemy_pos=(6, 5))
        do = {"composite": "trip", "args": {"target": enemy}}
        actions = translate_intent(do, actor, enc, grid)
        self.assertIsInstance(actions[0], Maneuver)
        self.assertEqual(actions[0].kind, "trip")
        self.assertEqual(actions[0].target_id, enemy.id)

    def test_dirty_trick_carries_options(self):
        enc, grid, actor, [enemy] = _build(enemy_pos=(6, 5))
        do = {"composite": "dirty_trick",
              "args": {"target": enemy, "condition": "shaken"}}
        actions = translate_intent(do, actor, enc, grid)
        man = actions[0]
        self.assertEqual(man.options.get("condition"), "shaken")

    def test_cast_composite_compiles_to_cast(self):
        enc, grid, actor, [enemy] = _build(enemy_pos=(6, 5))
        do = {"composite": "cast",
              "args": {"spell": "magic_missile", "spell_level": 1,
                       "target": enemy}}
        actions = translate_intent(do, actor, enc, grid)
        self.assertIsInstance(actions[0], Cast)
        self.assertEqual(actions[0].spell_id, "magic_missile")
        self.assertEqual(actions[0].target_id, enemy.id)


# ---------------------------------------------------------------------------
# run_intent_via_substrate end-to-end parity
# ---------------------------------------------------------------------------


def _run_both(intent_factory, *, with_enemy=True):
    """Build two parallel encounters from the same factory, run one via
    execute_turn and one via run_intent_via_substrate, return both
    actor states for comparison."""
    def build():
        enc, grid, actor, others = _build(
            actor_pos=(2, 5),
            enemy_pos=(8, 5) if with_enemy else None,
        )
        return enc, grid, actor, others
    enc_a, grid_a, actor_a, others_a = build()
    enc_b, grid_b, actor_b, others_b = build()

    intent_a = intent_factory(actor_a, others_a)
    intent_b = intent_factory(actor_b, others_b)

    res_a = execute_turn(actor_a, intent_a, enc_a, grid_a, Roller(seed=1))
    res_b = run_intent_via_substrate(
        actor_b, intent_b, enc_b, grid_b, Roller(seed=1),
    )
    return (actor_a, others_a, res_a), (actor_b, others_b, res_b)


class TestRunIntentParity(unittest.TestCase):
    def test_attack_intent_parity(self):
        def make(actor, others):
            return TurnIntent(
                rule_index=0,
                do={"slots": {"standard": {
                    "type": "attack", "target": others[0],
                }}},
                namespace={},
            )
        # Move actor adjacent first (otherwise attack fails for both).
        # Easier: use a different builder. Let's build adjacent here.
        a_actor = _orc((5, 5), "x")
        a_enemy = _orc((6, 5), "y")
        a_grid = Grid(width=12, height=12)
        a_grid.place(a_actor); a_grid.place(a_enemy)
        a_enc = Encounter.begin(a_grid, [a_actor, a_enemy], Roller(seed=1))

        b_actor = _orc((5, 5), "x")
        b_enemy = _orc((6, 5), "y")
        b_grid = Grid(width=12, height=12)
        b_grid.place(b_actor); b_grid.place(b_enemy)
        b_enc = Encounter.begin(b_grid, [b_actor, b_enemy], Roller(seed=1))

        intent_a = TurnIntent(0, {"slots": {"standard": {
            "type": "attack", "target": a_enemy,
        }}}, {})
        intent_b = TurnIntent(0, {"slots": {"standard": {
            "type": "attack", "target": b_enemy,
        }}}, {})

        execute_turn(a_actor, intent_a, a_enc, a_grid, Roller(seed=1))
        run_intent_via_substrate(b_actor, intent_b, b_enc, b_grid,
                                 Roller(seed=1))
        # Same final HP on the targets.
        self.assertEqual(a_enemy.current_hp, b_enemy.current_hp)
        self.assertEqual(a_enemy.position, b_enemy.position)
        self.assertEqual(set(a_enemy.conditions), set(b_enemy.conditions))

    def test_move_then_attack_parity(self):
        # Both runs see the actor close on the enemy and attack.
        a_actor = _orc((2, 5), "x")
        a_enemy = _orc((4, 5), "y")
        a_grid = Grid(width=20, height=10)
        a_grid.place(a_actor); a_grid.place(a_enemy)
        a_enc = Encounter.begin(a_grid, [a_actor, a_enemy], Roller(seed=1))

        b_actor = _orc((2, 5), "x")
        b_enemy = _orc((4, 5), "y")
        b_grid = Grid(width=20, height=10)
        b_grid.place(b_actor); b_grid.place(b_enemy)
        b_enc = Encounter.begin(b_grid, [b_actor, b_enemy], Roller(seed=1))

        intent_a = TurnIntent(0, {"slots": {
            "move": {"type": "move_toward", "target": a_enemy},
            "standard": {"type": "attack", "target": a_enemy},
        }}, {})
        intent_b = TurnIntent(0, {"slots": {
            "move": {"type": "move_toward", "target": b_enemy},
            "standard": {"type": "attack", "target": b_enemy},
        }}, {})

        execute_turn(a_actor, intent_a, a_enc, a_grid, Roller(seed=1))
        run_intent_via_substrate(b_actor, intent_b, b_enc, b_grid,
                                 Roller(seed=1))

        self.assertEqual(a_actor.position, b_actor.position)
        self.assertEqual(a_enemy.current_hp, b_enemy.current_hp)

    def test_charge_intent_parity(self):
        a_actor = _orc((2, 5), "x")
        a_enemy = _orc((7, 5), "y")
        a_grid = Grid(width=20, height=10)
        a_grid.place(a_actor); a_grid.place(a_enemy)
        a_enc = Encounter.begin(a_grid, [a_actor, a_enemy], Roller(seed=1))

        b_actor = _orc((2, 5), "x")
        b_enemy = _orc((7, 5), "y")
        b_grid = Grid(width=20, height=10)
        b_grid.place(b_actor); b_grid.place(b_enemy)
        b_enc = Encounter.begin(b_grid, [b_actor, b_enemy], Roller(seed=1))

        intent_a = TurnIntent(0, {"composite": "charge",
                                  "args": {"target": a_enemy}}, {})
        intent_b = TurnIntent(0, {"composite": "charge",
                                  "args": {"target": b_enemy}}, {})

        execute_turn(a_actor, intent_a, a_enc, a_grid, Roller(seed=1))
        run_intent_via_substrate(b_actor, intent_b, b_enc, b_grid,
                                 Roller(seed=1))

        self.assertEqual(a_actor.position, b_actor.position)
        self.assertEqual(a_enemy.current_hp, b_enemy.current_hp)

    def test_hold_intent_parity(self):
        a_enc, a_grid, a_actor, _ = _build()
        b_enc, b_grid, b_actor, _ = _build()
        intent_a = TurnIntent(0, {"composite": "hold"}, {})
        intent_b = TurnIntent(0, {"composite": "hold"}, {})
        res_a = execute_turn(a_actor, intent_a, a_enc, a_grid,
                             Roller(seed=1))
        res_b = run_intent_via_substrate(
            b_actor, intent_b, b_enc, b_grid, Roller(seed=1),
        )
        self.assertEqual(
            [e.kind for e in res_a.events],
            [e.kind for e in res_b.events],
        )

    def test_none_intent_parity(self):
        a_enc, a_grid, a_actor, _ = _build()
        b_enc, b_grid, b_actor, _ = _build()
        res_a = execute_turn(a_actor, None, a_enc, a_grid, Roller(seed=1))
        res_b = run_intent_via_substrate(b_actor, None, b_enc, b_grid,
                                         Roller(seed=1))
        self.assertEqual(
            [e.kind for e in res_a.events],
            [e.kind for e in res_b.events],
        )


if __name__ == "__main__":
    unittest.main()
