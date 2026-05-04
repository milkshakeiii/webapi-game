"""Tests for the ongoing-effects pipeline (poison + disease) — both
the day/round translation via the global 6-second tick and the new
viper / otyugh monsters that exercise the system."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


def _full_attack_intent():
    return BehaviorScript(name="atk", rules=[
        Rule(do={"composite": "full_attack",
                 "args": {"target": "enemy.closest"}}),
    ])


# ---------------------------------------------------------------------------
# Ongoing-effect queue API
# ---------------------------------------------------------------------------


class TestOngoingEffectQueue(unittest.TestCase):
    def test_queue_replaces_same_id(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        c.queue_ongoing_effect(
            id="x", type="poison",
            period_rounds=1, save_kind="fort", save_dc=10,
            ability_damage=[("str", "1d2")],
            current_round=0,
        )
        c.queue_ongoing_effect(
            id="x", type="poison",
            period_rounds=1, save_kind="fort", save_dc=20,
            ability_damage=[("dex", "1d2")],
            current_round=5,
        )
        self.assertEqual(len(c.ongoing_effects), 1)
        self.assertEqual(c.ongoing_effects[0]["save_dc"], 20)

    def test_tick_skips_when_next_tick_in_future(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        c.queue_ongoing_effect(
            id="late", type="poison",
            period_rounds=1, save_kind="fort", save_dc=10,
            ability_damage=[("str", "1d2")],
            current_round=0, onset_rounds=10,
        )
        c.tick_round(current_round=5, roller=Roller(seed=1))
        # Still queued, no damage.
        self.assertEqual(len(c.ongoing_effects), 1)
        self.assertEqual(c.ability_damage.get("str", 0), 0)

    def test_tick_applies_damage_on_save_fail(self):
        c = combatant_from_monster(REGISTRY.get_monster("goblin"), (0, 0), "x")
        c.queue_ongoing_effect(
            id="venom", type="poison",
            period_rounds=1, remaining_ticks=4,
            save_kind="fort", save_dc=99,    # auto-fail
            ability_damage=[("str", "1d2")],
            cure_consec=1,
            current_round=0, onset_rounds=1,
        )
        roller = Roller(seed=1)
        for r in range(1, 5):
            c.tick_round(current_round=r, roller=roller)
        self.assertGreater(c.ability_damage.get("str", 0), 0)
        # 4 ticks consumed, effect should be removed.
        self.assertFalse(any(e["id"] == "venom" for e in c.ongoing_effects))

    def test_save_success_clears_one_save_cure_poison(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        c.queue_ongoing_effect(
            id="auto_save", type="poison",
            period_rounds=1, remaining_ticks=4,
            save_kind="fort", save_dc=1,   # auto-pass (need 1)
            ability_damage=[("str", "1d2")],
            cure_consec=1,
            current_round=0, onset_rounds=1,
        )
        c.tick_round(current_round=1, roller=Roller(seed=1))
        self.assertFalse(any(e["id"] == "auto_save"
                             for e in c.ongoing_effects))


# ---------------------------------------------------------------------------
# Disease day cadence
# ---------------------------------------------------------------------------


class TestDiseaseCadence(unittest.TestCase):
    def test_ghoul_fever_does_not_tick_during_a_short_encounter(self):
        # A brand-new disease entry has onset of 14400 rounds. In
        # 5 rounds of an encounter, no save / damage should fire.
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        c.queue_ongoing_effect(
            id="diseased_bite", type="disease",
            period_rounds=14400, onset_rounds=14400,
            save_kind="fort", save_dc=99,  # auto-fail to amplify
            ability_damage=[("con", "1d3"), ("dex", "1d3")],
            cure_consec=2,
            current_round=0,
        )
        c.add_condition("diseased")
        roller = Roller(seed=1)
        for r in range(1, 6):
            c.tick_round(current_round=r, roller=roller)
        # No damage — onset hasn't elapsed.
        self.assertEqual(c.ability_damage.get("con", 0), 0)
        self.assertEqual(c.ability_damage.get("dex", 0), 0)
        self.assertIn("diseased", c.conditions)

    def test_ghoul_fever_ticks_after_one_simulated_day(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        c.queue_ongoing_effect(
            id="diseased_bite", type="disease",
            period_rounds=14400, onset_rounds=14400,
            save_kind="fort", save_dc=99,  # auto-fail
            ability_damage=[("con", "1d3"), ("dex", "1d3")],
            cure_consec=2,
            current_round=0,
        )
        c.add_condition("diseased")
        # Fast-forward to day 1.
        c.tick_round(current_round=14400, roller=Roller(seed=1))
        # Damage should have applied.
        self.assertGreater(c.ability_damage.get("con", 0), 0)
        self.assertGreater(c.ability_damage.get("dex", 0), 0)

    def test_two_consecutive_saves_cure_disease(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        c.queue_ongoing_effect(
            id="diseased_bite", type="disease",
            period_rounds=14400, onset_rounds=14400,
            save_kind="fort", save_dc=1,  # auto-pass
            ability_damage=[("con", "1d3")],
            cure_consec=2,
            current_round=0,
        )
        c.add_condition("diseased")
        c.tick_round(current_round=14400, roller=Roller(seed=1))
        # First save: passed, but not cured yet.
        self.assertTrue(any(e["id"] == "diseased_bite"
                            for e in c.ongoing_effects))
        c.tick_round(current_round=14400 * 2, roller=Roller(seed=1))
        # Second consecutive save → cured.
        self.assertFalse(any(e["id"] == "diseased_bite"
                             for e in c.ongoing_effects))
        self.assertNotIn("diseased", c.conditions)


# ---------------------------------------------------------------------------
# Viper poison (Con damage)
# ---------------------------------------------------------------------------


class TestViper(unittest.TestCase):
    def test_viper_bite_queues_con_damage_poison(self):
        for seed in range(1, 50):
            v = combatant_from_monster(REGISTRY.get_monster("viper"),
                                       (5, 5), "x")
            for opt in v.attack_options:
                opt["attack_bonus"] = 100
            t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                       (6, 5), "y")
            t.max_hp = 9999
            t.current_hp = 9999
            grid = Grid(width=12, height=12)
            grid.place(v)
            grid.place(t)
            enc = Encounter.begin(grid, [v, t], Roller(seed=seed))
            intent = Interpreter(_full_attack_intent()).pick_turn(v, enc, grid)
            execute_turn(v, intent, enc, grid, Roller(seed=seed))
            poison = [e for e in t.ongoing_effects
                      if e.get("id") == "poison_viper"]
            if poison:
                # Verify ability damage spec is Con.
                self.assertEqual(poison[0]["ability_damage"][0][0], "con")
                return
        self.fail("no seed in 1..49 queued viper poison")


# ---------------------------------------------------------------------------
# Otyugh filth fever
# ---------------------------------------------------------------------------


class TestOtyughDisease(unittest.TestCase):
    def test_otyugh_bite_queues_filth_fever(self):
        # Otyugh has 3 attacks (2 tentacles + bite); only the bite
        # carries filth_fever. Run multiple rounds to give the bite
        # a chance to land.
        for seed in range(1, 50):
            o = combatant_from_monster(REGISTRY.get_monster("otyugh"),
                                       (3, 3), "x")
            for opt in o.attack_options:
                opt["attack_bonus"] = 100
            t = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                       (5, 4), "y")
            t.max_hp = 9999
            t.current_hp = 9999
            grid = Grid(width=12, height=12)
            grid.place(o)
            grid.place(t)
            enc = Encounter.begin(grid, [o, t], Roller(seed=seed))
            intent = Interpreter(_full_attack_intent()).pick_turn(o, enc, grid)
            execute_turn(o, intent, enc, grid, Roller(seed=seed))
            disease = [e for e in t.ongoing_effects
                       if e.get("id") == "filth_fever"]
            if disease:
                self.assertIn("diseased", t.conditions)
                # 1d3 Dex + 1d3 Con damage profile.
                abilities = {x[0] for x in disease[0]["ability_damage"]}
                self.assertEqual(abilities, {"con", "dex"})
                return
        self.fail("no seed in 1..49 queued otyugh filth fever")


# ---------------------------------------------------------------------------
# Type immunities (undead vs disease/poison/ability-damage)
# ---------------------------------------------------------------------------


class TestUndeadImmunities(unittest.TestCase):
    def test_skeleton_immune_to_poison_entry(self):
        # Skeleton is undead → poison immune. Spider bite shouldn't
        # queue an effect.
        s = combatant_from_monster(REGISTRY.get_monster("giant_spider"),
                                   (5, 5), "x")
        for opt in s.attack_options:
            opt["attack_bonus"] = 100
        sk = combatant_from_monster(REGISTRY.get_monster("skeleton"),
                                    (6, 5), "y")
        sk.max_hp = 9999
        sk.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(s)
        grid.place(sk)
        enc = Encounter.begin(grid, [s, sk], Roller(seed=1))
        intent = Interpreter(_full_attack_intent()).pick_turn(s, enc, grid)
        result = execute_turn(s, intent, enc, grid, Roller(seed=1))
        # No ongoing poison; poison event reports "immune".
        self.assertFalse(any(e.get("id") == "poison_giant_spider"
                             for e in sk.ongoing_effects))
        evt = next((e for e in result.events if e.kind == "poison_on_hit"),
                   None)
        self.assertIsNotNone(evt)
        self.assertTrue(evt.detail.get("immune"))

    def test_skeleton_immune_to_ability_damage(self):
        sk = combatant_from_monster(REGISTRY.get_monster("skeleton"),
                                    (0, 0), "x")
        sk.apply_ability_damage("str", 4)
        self.assertEqual(sk.ability_damage.get("str", 0), 0)


if __name__ == "__main__":
    unittest.main()
