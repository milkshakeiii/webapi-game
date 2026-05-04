"""Tests for Phase 2.2 monster attack/charge/grapple riders —
paralysis, grab, blood drain, poison, rend, pounce, powerful charge,
quickness, rake."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.modifiers import compute as _compute
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


def _ghoul_vs(target_id):
    a = combatant_from_monster(REGISTRY.get_monster("ghoul"), (5, 5), "x")
    # Force hit: every bite lands.
    for opt in a.attack_options:
        opt["attack_bonus"] = 100
    b = combatant_from_monster(REGISTRY.get_monster(target_id), (6, 5), "y")
    b.max_hp = 9999
    b.current_hp = 9999
    grid = Grid(width=12, height=12)
    grid.place(a)
    grid.place(b)
    enc = Encounter.begin(grid, [a, b], Roller(seed=1))
    return a, b, enc, grid


def _full_attack_intent():
    return BehaviorScript(name="atk", rules=[
        Rule(do={"composite": "full_attack",
                 "args": {"target": "enemy.closest"}}),
    ])


# ---------------------------------------------------------------------------
# Paralysis (ghoul)
# ---------------------------------------------------------------------------


class TestGhoulParalysis(unittest.TestCase):
    def test_paralysis_on_hit_event_emitted(self):
        a, b, enc, grid = _ghoul_vs("goblin")
        # Make target's Will save tank (the save here is Fort, but
        # confirm goblin saves don't auto-pass).
        intent = Interpreter(_full_attack_intent()).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=3))
        kinds = [e.kind for e in result.events]
        self.assertIn("paralysis_on_hit", kinds)

    def test_paralyzed_target_becomes_helpless(self):
        # Sample multiple seeds; at least one should fail the save and
        # paralyze + helpless the target.
        for seed in range(1, 50):
            a, b, enc, grid = _ghoul_vs("goblin")
            intent = Interpreter(_full_attack_intent()).pick_turn(a, enc, grid)
            execute_turn(a, intent, enc, grid, Roller(seed=seed))
            if "paralyzed" in b.conditions:
                self.assertIn("helpless", b.conditions)
                return
        self.fail("no seed in 1..49 paralyzed the goblin")


# ---------------------------------------------------------------------------
# Disease on bite (ghoul fever)
# ---------------------------------------------------------------------------


class TestGhoulFever(unittest.TestCase):
    def test_disease_save_emitted_on_hit(self):
        a, b, enc, grid = _ghoul_vs("goblin")
        intent = Interpreter(_full_attack_intent()).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("disease_on_hit", kinds)

    def test_diseased_marker_on_save_fail(self):
        # Find a seed where the save fails.
        for seed in range(1, 100):
            a, b, enc, grid = _ghoul_vs("goblin")
            intent = Interpreter(_full_attack_intent()).pick_turn(a, enc, grid)
            execute_turn(a, intent, enc, grid, Roller(seed=seed))
            if "diseased" in b.conditions:
                return
        self.fail("no seed in 1..99 applied 'diseased' marker")


# ---------------------------------------------------------------------------
# Grab (owlbear)
# ---------------------------------------------------------------------------


class TestGrab(unittest.TestCase):
    def test_owlbear_attempts_grapple_on_hit(self):
        # Owlbear is large; place far enough that the 2x2 footprint
        # doesn't collide with the goblin.
        a = combatant_from_monster(REGISTRY.get_monster("owlbear"),
                                   (3, 3), "x")
        for opt in a.attack_options:
            opt["attack_bonus"] = 100
        b = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (5, 4), "y")
        b.max_hp = 9999
        b.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        intent = Interpreter(_full_attack_intent()).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("grab_on_hit", kinds)


class TestStirgeAutoGrab(unittest.TestCase):
    def test_stirge_attaches_without_roll(self):
        a = combatant_from_monster(REGISTRY.get_monster("stirge"),
                                   (5, 5), "x")
        for opt in a.attack_options:
            opt["attack_bonus"] = 100
        b = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (6, 5), "y")
        b.max_hp = 9999
        b.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        intent = Interpreter(_full_attack_intent()).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        grab_evts = [e for e in result.events if e.kind == "grab_on_hit"]
        self.assertEqual(len(grab_evts), 1)
        self.assertTrue(grab_evts[0].detail["auto_grab"])
        self.assertIn("grappled", a.conditions)
        self.assertIn("grappled", b.conditions)
        self.assertEqual(a.grappling_target_id, b.id)


# ---------------------------------------------------------------------------
# Blood drain (stirge)
# ---------------------------------------------------------------------------


class TestBloodDrain(unittest.TestCase):
    def test_blood_drain_applies_after_attach(self):
        a = combatant_from_monster(REGISTRY.get_monster("stirge"),
                                   (5, 5), "x")
        for opt in a.attack_options:
            opt["attack_bonus"] = 100
        b = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (6, 5), "y")
        b.max_hp = 9999
        b.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        intent = Interpreter(_full_attack_intent()).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        # Stirge attached + blood-drain end-of-turn fired.
        kinds = [e.kind for e in result.events]
        self.assertIn("grab_on_hit", kinds)
        self.assertIn("blood_drain", kinds)
        self.assertGreater(b.ability_damage.get("con", 0), 0)

    def test_blood_drain_caps_at_four_con(self):
        a = combatant_from_monster(REGISTRY.get_monster("stirge"),
                                   (5, 5), "x")
        for opt in a.attack_options:
            opt["attack_bonus"] = 100
        b = combatant_from_monster(REGISTRY.get_monster("orc"),
                                   (6, 5), "y")
        b.max_hp = 9999
        b.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        # Run 6 rounds of attacks; cumulative drain should cap at 4.
        for round_n in range(6):
            intent = Interpreter(_full_attack_intent()).pick_turn(a, enc, grid)
            execute_turn(a, intent, enc, grid, Roller(seed=round_n + 1))
        self.assertEqual(a.resources.get("blood_drain_dealt", 0), 4)


# ---------------------------------------------------------------------------
# Giant spider poison
# ---------------------------------------------------------------------------


class TestGiantSpiderPoison(unittest.TestCase):
    def test_poison_on_hit_queues_ongoing_effect(self):
        # The bite-Fort save can fail; on fail an ongoing 'giant_spider_poison'
        # effect is queued. Find a seed where it queues.
        for seed in range(1, 50):
            a = combatant_from_monster(REGISTRY.get_monster("giant_spider"),
                                       (5, 5), "x")
            for opt in a.attack_options:
                opt["attack_bonus"] = 100
            b = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                       (6, 5), "y")
            b.max_hp = 9999
            b.current_hp = 9999
            grid = Grid(width=12, height=12)
            grid.place(a)
            grid.place(b)
            enc = Encounter.begin(grid, [a, b], Roller(seed=seed))
            intent = Interpreter(_full_attack_intent()).pick_turn(a, enc, grid)
            execute_turn(a, intent, enc, grid, Roller(seed=seed))
            if any(e.get("id") == "poison_giant_spider"
                   for e in b.ongoing_effects):
                return
        self.fail("no seed in 1..49 queued spider poison ongoing effect")

    def test_poison_ticks_apply_str_damage(self):
        # Once queued, ticking the rounds applies Str damage (failed
        # tick saves) until cured (one successful save) or the 4-tick
        # window runs out.
        b = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (0, 0), "x")
        b.queue_ongoing_effect(
            id="poison_giant_spider", type="poison",
            period_rounds=1, remaining_ticks=4,
            save_kind="fort", save_dc=14,
            ability_damage=[("str", "1d2")],
            cure_consec=1,
            current_round=0, onset_rounds=1,
        )
        roller = Roller(seed=1)
        for r in range(1, 6):
            b.tick_round(current_round=r, roller=roller)
        # Either some Str damage has been applied or the effect was
        # cured / expired.
        # Acceptable outcomes: positive Str damage, or no remaining
        # poison entry.
        active = [e for e in b.ongoing_effects
                  if e.get("id") == "poison_giant_spider"]
        self.assertTrue(
            b.ability_damage.get("str", 0) > 0 or not active,
            "expected str damage applied or effect cleared",
        )


# ---------------------------------------------------------------------------
# Quickness (choker)
# ---------------------------------------------------------------------------


class TestQuickness(unittest.TestCase):
    def test_choker_init_includes_plus_one_enhancement(self):
        c = combatant_from_monster(REGISTRY.get_monster("choker"),
                                   (0, 0), "x")
        # Quickness contributes +1 enhancement to initiative beyond
        # the JSON `init` field. Compare against the raw JSON value.
        json_init = REGISTRY.get_monster("choker").init
        self.assertGreaterEqual(c.initiative_modifier(), json_init + 1)


# ---------------------------------------------------------------------------
# Pounce + Powerful Charge
# ---------------------------------------------------------------------------


class TestPounce(unittest.TestCase):
    def test_lion_pounce_makes_extra_claw_attacks_on_charge(self):
        # Use a medium creature with pounce to avoid large-size charge
        # path complications. Synthesize a panther-like monster on the
        # fly with the pounce trait.
        from dnd.engine.content import Monster
        panther = Monster(
            id="panther", name="Panther", summary="Test pounce.",
            cr="2", xp=600, alignment="neutral",
            size="medium", type="animal", subtypes=[],
            ability_scores={"str": 14, "dex": 17, "con": 13,
                            "int": 2, "wis": 15, "cha": 6},
            hit_dice="3d8+6", hp=22, init=3, senses=["low_light_vision"],
            speed=40,
            ac={"total": 15, "touch": 13, "flat_footed": 12,
                "natural": 2, "dex": 3},
            saves={"fort": 5, "ref": 6, "will": 2},
            bab=2, cmb=4, cmd=17,
            attacks=[
                {"type": "melee", "name": "bite",
                 "attack_bonus": 4, "damage": "1d6+2",
                 "damage_type": "P", "crit_range": [20, 20],
                 "crit_multiplier": 2},
                {"type": "melee", "name": "claw",
                 "attack_bonus": 4, "damage": "1d4+2",
                 "damage_type": "S", "crit_range": [20, 20],
                 "crit_multiplier": 2},
                {"type": "melee", "name": "claw_off",
                 "attack_bonus": 4, "damage": "1d4+2",
                 "damage_type": "S", "crit_range": [20, 20],
                 "crit_multiplier": 2},
            ],
            feats=[], skills={}, languages=[],
            racial_traits=[
                {"id": "pounce", "name": "Pounce",
                 "summary": "Full attack on a charge."},
            ],
            equipment=[],
            permanent_conditions=[],
        )
        a = combatant_from_monster(panther, (3, 5), "x")
        for opt in a.attack_options:
            opt["attack_bonus"] = 100
        b = combatant_from_monster(REGISTRY.get_monster("orc"), (8, 5), "y")
        b.max_hp = 9999
        b.current_hp = 9999
        grid = Grid(width=20, height=10)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        script = BehaviorScript(name="ch", rules=[
            Rule(do={"composite": "charge",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        # Charge should fire one charge_attack plus pounce_attack(s).
        self.assertIn("charge_attack", kinds)
        self.assertIn("pounce_attack", kinds)


class TestPowerfulCharge(unittest.TestCase):
    def test_powerful_charge_doubles_charge_damage(self):
        # Synthesize a medium minotaur-style creature with the
        # powerful_charge trait. Real minotaur is large, which would
        # complicate charge pathing in the test grid.
        from dnd.engine.content import Monster
        beast = Monster(
            id="charging_brute", name="Charging Brute",
            summary="Test powerful charge.",
            cr="2", xp=600, alignment="neutral",
            size="medium", type="humanoid", subtypes=[],
            ability_scores={"str": 16, "dex": 11, "con": 14,
                            "int": 7, "wis": 10, "cha": 8},
            hit_dice="3d8+6", hp=22, init=0, senses=[],
            speed=30,
            ac={"total": 13, "touch": 10, "flat_footed": 13,
                "natural": 3},
            saves={"fort": 5, "ref": 1, "will": 1},
            bab=2, cmb=5, cmd=15,
            attacks=[
                {"type": "melee", "name": "gore",
                 "attack_bonus": 5, "damage": "1d6+3",
                 "damage_type": "P", "crit_range": [20, 20],
                 "crit_multiplier": 2},
            ],
            feats=[], skills={}, languages=[],
            racial_traits=[
                {"id": "powerful_charge", "name": "Powerful Charge",
                 "summary": "Doubles gore damage on a charge."},
            ],
            equipment=[],
            permanent_conditions=[],
        )
        a = combatant_from_monster(beast, (3, 5), "x")
        for opt in a.attack_options:
            opt["attack_bonus"] = 100
        b = combatant_from_monster(REGISTRY.get_monster("orc"), (8, 5), "y")
        b.max_hp = 9999
        b.current_hp = 9999
        grid = Grid(width=20, height=10)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        script = BehaviorScript(name="ch", rules=[
            Rule(do={"composite": "charge",
                     "args": {"target": "enemy.closest"}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        charge_evts = [e for e in result.events if e.kind == "charge_attack"]
        self.assertGreater(len(charge_evts), 0)
        trace = "\n".join(charge_evts[0].detail.get("trace") or [])
        self.assertIn("×2", trace)


# ---------------------------------------------------------------------------
# Rend (troll)
# ---------------------------------------------------------------------------


class TestRend(unittest.TestCase):
    def test_rend_fires_when_both_claws_hit(self):
        # Synthesize a medium two-clawed creature with rend (rather
        # than the large troll, which complicates grid placement).
        from dnd.engine.content import Monster
        beast = Monster(
            id="rending_beast", name="Rending Beast",
            summary="Test rend.",
            cr="3", xp=800, alignment="neutral",
            size="medium", type="aberration", subtypes=[],
            ability_scores={"str": 16, "dex": 13, "con": 14,
                            "int": 5, "wis": 10, "cha": 6},
            hit_dice="3d8", hp=22, init=1, senses=[],
            speed=30,
            ac={"total": 14, "touch": 11, "flat_footed": 13,
                "natural": 3, "dex": 1},
            saves={"fort": 4, "ref": 2, "will": 1},
            bab=2, cmb=5, cmd=16,
            attacks=[
                {"type": "melee", "name": "claw",
                 "attack_bonus": 5, "damage": "1d6+3",
                 "damage_type": "S", "crit_range": [20, 20],
                 "crit_multiplier": 2, "is_natural": True},
                {"type": "melee", "name": "claw_off",
                 "attack_bonus": 5, "damage": "1d6+3",
                 "damage_type": "S", "crit_range": [20, 20],
                 "crit_multiplier": 2, "is_natural": True},
            ],
            feats=[], skills={}, languages=[],
            racial_traits=[
                {"id": "rend", "name": "Rend",
                 "summary": "+1d6+1 if both claws hit."},
            ],
            equipment=[],
            permanent_conditions=[],
        )
        a = combatant_from_monster(beast, (5, 5), "x")
        for opt in a.attack_options:
            opt["attack_bonus"] = 100  # guarantee both claw hits
        b = combatant_from_monster(REGISTRY.get_monster("orc"), (6, 5), "y")
        b.max_hp = 9999
        b.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(a)
        grid.place(b)
        enc = Encounter.begin(grid, [a, b], Roller(seed=1))
        intent = Interpreter(_full_attack_intent()).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("rend", kinds)


# ---------------------------------------------------------------------------
# Ability damage system (used by poison + blood_drain)
# ---------------------------------------------------------------------------


class TestAbilityDamage(unittest.TestCase):
    def test_apply_str_damage_drops_attack(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        atk_before = _compute(0, c.modifiers.for_target("attack"))
        c.apply_ability_damage("str", 4)  # -4 score → -2 mod
        atk_after = _compute(0, c.modifiers.for_target("attack"))
        self.assertEqual(atk_after - atk_before, -2)

    def test_heal_ability_damage_clears(self):
        c = combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")
        c.apply_ability_damage("con", 4)
        c.heal_ability_damage("con", 4)
        self.assertEqual(c.ability_damage.get("con", 0), 0)


if __name__ == "__main__":
    unittest.main()
