"""Tests for Phase 4.3a follow-up — closing the easy + medium PARTIAL
gaps the audit found:

- fatigued / exhausted: explicit run/charge ban
- improved-X feats: defensive +2 CMD vs that maneuver
- rock_catching: size-scaled DC + once-per-round limit
- tail_spike_volley composite (manticore standard-action volley)
- escape_web composite (Str / Escape Artist DC 16)
- invisible attacker: pinpoint-by-Perception removes Dex denial
- petrified: stone-body half HP + hardness 8 + 50-damage shatter
"""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter, Turn, TurnValidationError, validate_turn
from dnd.engine.grid import Grid
from dnd.engine.modifiers import Modifier, compute_with_context
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


# ---------------------------------------------------------------------------
# fatigued run/charge ban
# ---------------------------------------------------------------------------


class TestFatiguedRunBan(unittest.TestCase):
    def test_fatigued_cannot_charge(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (3, 5), "x")
        c.add_condition("fatigued")
        grid = Grid(width=20, height=10)
        grid.place(c)
        turn = Turn(full_round={"composite": "charge",
                                "args": {"target": "enemy.closest"}})
        with self.assertRaises(TurnValidationError):
            validate_turn(turn, c, grid)

    def test_exhausted_cannot_run(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (3, 5), "x")
        c.add_condition("exhausted")
        grid = Grid(width=20, height=10)
        grid.place(c)
        turn = Turn(full_round={"composite": "run",
                                "args": {"direction": "east"}})
        with self.assertRaises(TurnValidationError):
            validate_turn(turn, c, grid)


# ---------------------------------------------------------------------------
# Improved-X defensive CMD
# ---------------------------------------------------------------------------


class TestImprovedDefensiveCmd(unittest.TestCase):
    def _orc_with_feat(self, feat_id):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        c.extra_feats.append(feat_id)
        # Re-apply feat modifiers (combatant_from_monster doesn't auto-fold
        # extra_feats into the modifier collection — for the test we
        # simulate the bonus directly via the feat_modifiers helper).
        from dnd.engine.feat_effects import feat_modifiers
        for m in feat_modifiers(feat_id, c.template):
            c.modifiers.add(m)
        return c

    def test_improved_grapple_grants_plus_two_cmd_vs_grapple(self):
        c = self._orc_with_feat("improved_grapple")
        plain_cmd = c.cmd()
        cmd_vs_grapple = c.cmd(context={"maneuver": "grapple"})
        self.assertEqual(cmd_vs_grapple - plain_cmd, 2)

    def test_improved_grapple_does_not_apply_to_disarm(self):
        c = self._orc_with_feat("improved_grapple")
        plain = c.cmd()
        vs_disarm = c.cmd(context={"maneuver": "disarm"})
        self.assertEqual(vs_disarm, plain)

    def test_improved_disarm_grants_plus_two_cmd_vs_disarm(self):
        c = self._orc_with_feat("improved_disarm")
        plain = c.cmd()
        vs_disarm = c.cmd(context={"maneuver": "disarm"})
        self.assertEqual(vs_disarm - plain, 2)


# ---------------------------------------------------------------------------
# rock_catching size DC + once/round
# ---------------------------------------------------------------------------


class TestRockCatching(unittest.TestCase):
    def test_dc_uses_thrower_size(self):
        # Hill giant (size large) → DC 25.
        from dnd.engine.turn_executor import _ROCK_CATCH_DC
        self.assertEqual(_ROCK_CATCH_DC["large"], 25)
        self.assertEqual(_ROCK_CATCH_DC["medium"], 20)
        self.assertEqual(_ROCK_CATCH_DC["small"], 15)

    def test_once_per_round_limit(self):
        giant = combatant_from_monster(REGISTRY.get_monster("hill_giant"),
                                       (3, 3), "y")
        # Synthesize another giant on the same team to act as target
        # (also has rock_catching). Place a separate target with
        # rock_catching so the catch fires.
        receiver = combatant_from_monster(REGISTRY.get_monster("hill_giant"),
                                          (10, 10), "x")
        # Pin attack to land + force rock attack option.
        for opt in giant.attack_options:
            opt["attack_bonus"] = 100
        grid = Grid(width=30, height=20)
        grid.place(giant)
        grid.place(receiver)
        enc = Encounter.begin(grid, [giant, receiver], Roller(seed=1))
        # Boost receiver's Reflex so the catch always succeeds once.
        receiver.modifiers.add(Modifier(value=99, type="untyped",
                                        target="ref_save",
                                        source="test_high_ref"))
        # Fire two rock attacks in the same round; both should attempt
        # to land. The first catch succeeds (DC ≤ ref+99), the second
        # is short-circuited by the once-per-round limit.
        for i in range(2):
            script = BehaviorScript(name=f"rock{i}", rules=[
                Rule(do={"standard": {"type": "attack",
                                      "target": receiver}}),
            ])
            # Force the giant to use the rock attack (index 1).
            giant.attack_options = [a for a in giant.attack_options
                                     if a.get("name") == "rock"]
            intent = Interpreter(script).pick_turn(giant, enc, grid)
            execute_turn(giant, intent, enc, grid, Roller(seed=1))
        # Receiver should have last_rock_caught_round set to round 1.
        self.assertEqual(
            int(receiver.resources.get("last_rock_caught_round", -1)),
            enc.round_number,
        )


# ---------------------------------------------------------------------------
# tail_spike_volley
# ---------------------------------------------------------------------------


class TestTailSpikeVolley(unittest.TestCase):
    def test_volley_fires_four_attacks_or_until_pool_empty(self):
        m = combatant_from_monster(REGISTRY.get_monster("manticore"),
                                   (3, 5), "x")
        for opt in m.attack_options:
            opt["attack_bonus"] = 100
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (10, 5), "y")
        target.max_hp = 9999
        target.current_hp = 9999
        grid = Grid(width=30, height=10)
        grid.place(m)
        grid.place(target)
        enc = Encounter.begin(grid, [m, target], Roller(seed=1))
        script = BehaviorScript(name="v", rules=[
            Rule(do={"composite": "tail_spike_volley",
                     "args": {"target": "enemy.closest"}}),
        ])
        before_pool = m.daily_resources.get("tail_spikes", 0)
        intent = Interpreter(script).pick_turn(m, enc, grid)
        result = execute_turn(m, intent, enc, grid, Roller(seed=1))
        evt = next(e for e in result.events if e.kind == "tail_spike_volley")
        self.assertEqual(evt.detail["fired"], 4)
        self.assertEqual(
            m.daily_resources.get("tail_spikes", 0),
            before_pool - 4,
        )

    def test_volley_stops_when_pool_empties(self):
        m = combatant_from_monster(REGISTRY.get_monster("manticore"),
                                   (3, 5), "x")
        for opt in m.attack_options:
            opt["attack_bonus"] = 100
        m.daily_resources["tail_spikes"] = 2
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (10, 5), "y")
        target.max_hp = 9999
        target.current_hp = 9999
        grid = Grid(width=30, height=10)
        grid.place(m)
        grid.place(target)
        enc = Encounter.begin(grid, [m, target], Roller(seed=1))
        script = BehaviorScript(name="v", rules=[
            Rule(do={"composite": "tail_spike_volley",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(m, enc, grid)
        result = execute_turn(m, intent, enc, grid, Roller(seed=1))
        evt = next(e for e in result.events if e.kind == "tail_spike_volley")
        self.assertEqual(evt.detail["fired"], 2)


# ---------------------------------------------------------------------------
# escape_web
# ---------------------------------------------------------------------------


class TestEscapeWeb(unittest.TestCase):
    def test_strong_target_escapes_web(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        c.add_condition("entangled")
        c.register_sourced_condition("web:spider1", "entangled")
        # Boost Str so the check is reliable.
        c.modifiers.add(Modifier(value=20, type="untyped",
                                 target="ability:str",
                                 source="test_super_str"))
        grid = Grid(width=12, height=12)
        grid.place(c)
        enc = Encounter.begin(grid, [c], Roller(seed=1))
        script = BehaviorScript(name="ew", rules=[
            Rule(do={"composite": "escape_web", "args": {}}),
        ])
        intent = Interpreter(script).pick_turn(c, enc, grid)
        result = execute_turn(c, intent, enc, grid, Roller(seed=1))
        evt = next(e for e in result.events if e.kind == "escape_web")
        self.assertTrue(evt.detail["passed"])
        self.assertNotIn("entangled", c.conditions)


# ---------------------------------------------------------------------------
# Invisible pinpoint
# ---------------------------------------------------------------------------


class TestInvisiblePinpoint(unittest.TestCase):
    def test_successful_perception_records_pinpoint(self):
        # Boost target's Perception so the DC 20 check always passes.
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        a.add_condition("invisible")
        for opt in a.attack_options:
            opt["attack_bonus"] = 100
        b = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (6, 5), "y")
        b.modifiers.add(Modifier(value=99, type="untyped",
                                 target="skill:perception",
                                 source="test_perception"))
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        script = BehaviorScript(name="atk", rules=[
            Rule(do={"composite": "full_attack",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        execute_turn(a, intent, enc, grid, Roller(seed=1))
        # b should have pinpointed a.
        self.assertIn(a.id, b.pinpointed_invisible)


# ---------------------------------------------------------------------------
# Petrified stone-body
# ---------------------------------------------------------------------------


class TestPetrifiedStoneBody(unittest.TestCase):
    def test_petrification_halves_max_hp(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        before_max = c.max_hp
        c.add_condition("petrified")
        self.assertEqual(c.max_hp, before_max // 2)
        self.assertLessEqual(c.current_hp, c.max_hp)

    def test_remove_petrified_restores_max_hp(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        before_max = c.max_hp
        c.add_condition("petrified")
        c.remove_condition("petrified")
        self.assertEqual(c.max_hp, before_max)

    def test_hardness_8_reduces_incoming_damage(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        c.add_condition("petrified")
        before = c.current_hp
        c.take_damage(10)  # 10 - 8 hardness = 2 actual
        self.assertEqual(before - c.current_hp, 2)

    def test_fifty_plus_damage_shatters(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        c.add_condition("petrified")
        c.take_damage(50)
        self.assertIn("dead", c.conditions)


if __name__ == "__main__":
    unittest.main()
