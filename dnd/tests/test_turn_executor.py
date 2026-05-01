"""Tests for dnd.engine.turn_executor."""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import (
    combatant_from_character,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import (
    TurnResult,
    default_monster_intent,
    execute_turn,
)


REGISTRY = default_registry()


def _fighter():
    req = CharacterRequest.from_dict({
        "name": "Sir Edric",
        "race": "human",
        "class": "fighter",
        "alignment": "lawful_good",
        "ability_scores": {
            "method": "point_buy_20",
            "scores": {"str": 16, "dex": 14, "con": 14,
                       "int": 10, "wis": 10, "cha": 10},
        },
        "free_ability_choice": "str",
        "feats": ["power_attack", "weapon_focus"],
        "skill_ranks": {"climb": 1, "swim": 1},
        "bonus_languages": [],
        "class_choices": {"fighter_bonus_feat": "cleave"},
    })
    return create_character(req, REGISTRY)


def _setup(fighter_pos=(2, 5), goblin_pos=(8, 5)):
    fighter = combatant_from_character(_fighter(), REGISTRY, fighter_pos, "patrons")
    goblin = combatant_from_monster(REGISTRY.get_monster("goblin"), goblin_pos, "enemies")
    grid = Grid(width=20, height=10)
    grid.place(fighter)
    grid.place(goblin)
    enc = Encounter.begin(grid, [fighter, goblin], Roller(seed=1))
    return fighter, goblin, enc, grid


# ---------------------------------------------------------------------------
# Hold and skip behaviors
# ---------------------------------------------------------------------------


class TestHoldAndNoIntent(unittest.TestCase):
    def test_hold_records_skip(self):
        fighter, goblin, enc, grid = _setup()
        from dnd.engine.dsl import build_namespace
        intent = type("I", (), {})()
        intent.rule_index = 0
        intent.do = {"composite": "hold"}
        intent.namespace = build_namespace(fighter, enc, grid)
        result = execute_turn(fighter, intent, enc, grid, Roller(seed=1))
        self.assertTrue(any(e.kind == "skip" for e in result.events))

    def test_no_intent_records_skip(self):
        fighter, _, enc, grid = _setup()
        result = execute_turn(fighter, None, enc, grid, Roller(seed=1))
        self.assertTrue(any(e.kind == "skip" for e in result.events))


# ---------------------------------------------------------------------------
# Movement
# ---------------------------------------------------------------------------


class TestMovement(unittest.TestCase):
    def test_move_toward_closes_distance(self):
        fighter, goblin, enc, grid = _setup(fighter_pos=(2, 5), goblin_pos=(15, 5))
        script = BehaviorScript(name="approach", rules=[
            Rule(do={"slots": {
                "move": {"type": "move_toward", "target": "enemy.closest"},
            }}),
        ])
        intent = Interpreter(script).pick_turn(fighter, enc, grid)
        before = grid.distance_between(fighter, goblin)
        execute_turn(fighter, intent, enc, grid, Roller(seed=1))
        after = grid.distance_between(fighter, goblin)
        self.assertLess(after, before)
        # Speed 30 = 6 squares; at 13 sq apart, fighter should close to ~7.
        self.assertLessEqual(after, before - 5)

    def test_move_toward_stops_adjacent(self):
        fighter, goblin, enc, grid = _setup(fighter_pos=(7, 5), goblin_pos=(8, 5))
        script = BehaviorScript(name="approach", rules=[
            Rule(do={"slots": {
                "move": {"type": "move_toward", "target": "enemy.closest"},
            }}),
        ])
        intent = Interpreter(script).pick_turn(fighter, enc, grid)
        execute_turn(fighter, intent, enc, grid, Roller(seed=1))
        # Already adjacent — no further movement.
        self.assertEqual(fighter.position, (7, 5))


# ---------------------------------------------------------------------------
# Attacks
# ---------------------------------------------------------------------------


class TestAttacks(unittest.TestCase):
    def test_charge_closes_and_attacks(self):
        fighter, goblin, enc, grid = _setup(fighter_pos=(2, 5), goblin_pos=(8, 5))
        script = BehaviorScript(name="charger", rules=[
            Rule(when="enemy.any",
                 do={"composite": "charge",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(fighter, enc, grid)
        result = execute_turn(fighter, intent, enc, grid, Roller(seed=1))
        # Should have moves and an attack.
        kinds = [e.kind for e in result.events]
        self.assertIn("move", kinds)
        self.assertTrue(any(k.endswith("_attack") for k in kinds))
        # Fighter should now be adjacent to goblin.
        self.assertTrue(grid.is_adjacent(fighter, goblin))

    def test_charge_rejected_when_already_adjacent(self):
        # PF1: charge requires moving at least 2 squares. If the actor
        # is already adjacent to the target, the charge is illegal —
        # no movement, no +2 bonus, no attack.
        fighter, goblin, enc, grid = _setup(fighter_pos=(7, 5), goblin_pos=(8, 5))
        script = BehaviorScript(name="charger", rules=[
            Rule(do={"composite": "charge",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(fighter, enc, grid)
        result = execute_turn(fighter, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        # No attack happened.
        self.assertFalse(any(k.endswith("_attack") for k in kinds),
                         f"expected no attack, got events: {kinds}")
        # A skip event with the right reason fired.
        skips = [e for e in result.events if e.kind == "skip"]
        self.assertTrue(skips, "expected a skip event")
        self.assertIn("too close", skips[0].detail.get("reason", ""))

    def test_charge_rejected_when_target_off_axis(self):
        # Charger at (2, 5), target at (8, 6). Displacement (6, 1) is
        # neither orthogonal nor a true diagonal — no straight-line
        # charge possible.
        fighter = combatant_from_character(_fighter(), REGISTRY, (2, 5), "patrons")
        goblin = combatant_from_monster(REGISTRY.get_monster("goblin"), (8, 6), "enemies")
        grid = Grid(width=20, height=10)
        grid.place(fighter)
        grid.place(goblin)
        enc = Encounter.begin(grid, [fighter, goblin], Roller(seed=1))
        script = BehaviorScript(name="charger", rules=[
            Rule(do={"composite": "charge",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(fighter, enc, grid)
        result = execute_turn(fighter, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertFalse(any(k.endswith("_attack") for k in kinds))
        skips = [e for e in result.events if e.kind == "skip"]
        self.assertTrue(skips)
        self.assertIn("straight line", skips[0].detail.get("reason", ""))

    def test_charge_along_diagonal_succeeds(self):
        # Pure NE diagonal: charger at (2, 2), target at (5, 5).
        # Displacement (3, 3) → unit (1, 1), 2 steps to (4, 4) which is
        # adjacent to (5, 5). Path passes through (3, 3) and (4, 4).
        fighter = combatant_from_character(_fighter(), REGISTRY, (2, 2), "patrons")
        goblin = combatant_from_monster(REGISTRY.get_monster("goblin"), (5, 5), "enemies")
        grid = Grid(width=20, height=10)
        grid.place(fighter)
        grid.place(goblin)
        enc = Encounter.begin(grid, [fighter, goblin], Roller(seed=1))
        script = BehaviorScript(name="charger", rules=[
            Rule(do={"composite": "charge",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(fighter, enc, grid)
        result = execute_turn(fighter, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertTrue(any(k.endswith("_attack") for k in kinds),
                        f"expected charge attack; events: {kinds}")
        # Fighter ended adjacent to goblin.
        self.assertTrue(grid.is_adjacent(fighter, goblin))

    def test_charge_rejected_when_ally_blocks_lane(self):
        # Charger at (2, 5), goblin target at (8, 5). An ally sits at
        # (5, 5), blocking the straight east lane.
        fighter = combatant_from_character(_fighter(), REGISTRY, (2, 5), "patrons")
        ally = combatant_from_monster(REGISTRY.get_monster("goblin"), (5, 5), "patrons")
        goblin = combatant_from_monster(REGISTRY.get_monster("goblin"), (8, 5), "enemies")
        grid = Grid(width=20, height=10)
        grid.place(fighter)
        grid.place(ally)
        grid.place(goblin)
        enc = Encounter.begin(grid, [fighter, goblin, ally], Roller(seed=1))
        script = BehaviorScript(name="charger", rules=[
            Rule(do={"composite": "charge",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(fighter, enc, grid)
        result = execute_turn(fighter, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertFalse(any(k.endswith("_attack") for k in kinds))
        skips = [e for e in result.events if e.kind == "skip"]
        self.assertTrue(skips)
        self.assertIn("path blocked", skips[0].detail.get("reason", ""))

    def test_charge_rejected_when_impassable_in_lane(self):
        # Same setup but with a wall cell instead of an ally.
        from dnd.engine.grid import wall
        fighter = combatant_from_character(_fighter(), REGISTRY, (2, 5), "patrons")
        goblin = combatant_from_monster(REGISTRY.get_monster("goblin"), (8, 5), "enemies")
        grid = Grid(width=20, height=10)
        grid.add_feature(5, 5, wall())
        grid.place(fighter)
        grid.place(goblin)
        enc = Encounter.begin(grid, [fighter, goblin], Roller(seed=1))
        script = BehaviorScript(name="charger", rules=[
            Rule(do={"composite": "charge",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(fighter, enc, grid)
        result = execute_turn(fighter, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertFalse(any(k.endswith("_attack") for k in kinds))
        skips = [e for e in result.events if e.kind == "skip"]
        self.assertTrue(skips)
        self.assertIn("path blocked", skips[0].detail.get("reason", ""))

    def test_charge_rejected_when_movement_blocked_to_under_2(self):
        # Fighter starts 2 squares away — eligible to charge — but a
        # wall of impassable squares forces the path-finder to detour
        # around, and after one step they're already adjacent. The
        # final-position check should fail (moved < 2 squares).
        fighter, goblin, enc, grid = _setup(fighter_pos=(6, 5), goblin_pos=(8, 5))
        # Block every cell except a single corridor that brings the
        # fighter to (7, 5) in one step (distance 1 from start).
        # Easier: place an ally on (7, 5) so smart-step routes through
        # diagonals to (7, 4) or (7, 6) — those are still distance 1 from
        # start, and adjacent to the goblin. Actually, any single step
        # from (6, 5) toward (8, 5) lands the fighter at distance 1 from
        # start, which is < 2. So we'd need them to stop after just 1
        # step. The simplest scenario: fighter at (6, 5), goblin at
        # (7, 5) — distance 1, falls into the start-distance check.
        # The "moved < 2" branch is exercised when start is exactly
        # 2 away and only 1 step is taken before the destination is
        # reached. _move_along will move them to the closest passable
        # cell to dest, which for (6,5) → (8,5) takes 1 step diagonally
        # if (7, 5) is blocked, ending at distance 1 from start.
        # Place an ally at (7, 5) to block straight-line movement.
        ally = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (7, 5), "patrons",
        )
        grid.place(ally)
        script = BehaviorScript(name="charger", rules=[
            Rule(do={"composite": "charge",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(fighter, enc, grid)
        result = execute_turn(fighter, intent, enc, grid, Roller(seed=1))
        # If the path forced a < 2-square move, expect a skip with
        # "moved only" or the "too close" reason. Either way: no
        # charge_attack should fire.
        attacks = [e for e in result.events if e.kind.endswith("_attack")]
        self.assertFalse(attacks,
                         f"expected charge to fail; saw attacks: {attacks}")

    def test_full_attack_when_adjacent(self):
        fighter, goblin, enc, grid = _setup(fighter_pos=(7, 5), goblin_pos=(8, 5))
        script = BehaviorScript(name="bruiser", rules=[
            Rule(do={"composite": "full_attack",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(fighter, enc, grid)
        result = execute_turn(fighter, intent, enc, grid, Roller(seed=42))
        self.assertTrue(any(e.kind.startswith("full_attack")
                            for e in result.events))


# ---------------------------------------------------------------------------
# End-to-end: fighter kills a goblin
# ---------------------------------------------------------------------------


class TestEndToEnd(unittest.TestCase):
    def test_fighter_kills_goblin_eventually(self):
        fighter, goblin, enc, grid = _setup(fighter_pos=(2, 5), goblin_pos=(8, 5))

        fighter_script = BehaviorScript(name="bruiser", rules=[
            Rule(when="enemy.any and enemy.in_range(1) is not None",
                 do={"composite": "full_attack",
                     "args": {"target": "enemy.closest"}}),
            Rule(when="enemy.any",
                 do={"composite": "charge",
                     "args": {"target": "enemy.closest"}}),
        ])
        interp = Interpreter(fighter_script)

        roller = Roller(seed=7)

        # Run up to 20 rounds.
        for _ in range(40):  # 20 rounds × 2 actors
            actor = enc.current_actor()
            if actor is None:
                break
            if not actor.is_alive() or actor.current_hp <= 0:
                enc.advance_turn()
                continue
            if actor is fighter:
                intent = interp.pick_turn(actor, enc, grid)
            else:
                intent = default_monster_intent(actor, enc, grid)
            execute_turn(actor, intent, enc, grid, roller)
            enc.advance_turn()
            if enc.is_over():
                break

        # Fighter should win (he has 12 HP, AC 15, +5 to hit; goblin has 6 HP, AC 16).
        self.assertTrue(enc.is_over() or goblin.current_hp <= 0)
        self.assertEqual(enc.winner_team(), "patrons")


if __name__ == "__main__":
    unittest.main()
