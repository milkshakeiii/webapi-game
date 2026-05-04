"""Tests for Phase 4.3a — cleric domains.

Covers domain pick at L1, granted-power per-day pool, and the four
fully-wired power kinds (touch_heal, touch_buff, touch_info,
ranged_damage)."""

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
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


def _cleric(domains=("healing", "war")):
    req = CharacterRequest.from_dict({
        "name": "Cael", "race": "human", "class": "cleric",
        "alignment": "neutral_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 10, "dex": 10, "con": 14,
                       "int": 10, "wis": 16, "cha": 14}},
        "free_ability_choice": "wis",
        "feats": ["alertness", "iron_will"],
        "skill_ranks": {"heal": 1, "knowledge_religion": 1},
        "bonus_languages": [],
        "class_choices": {"domains": list(domains)},
    })
    char = create_character(req, REGISTRY)
    return combatant_from_character(char, REGISTRY, (5, 5), "x")


def _power_intent(domain_id, target=None):
    args = {"domain_id": domain_id}
    if target is not None:
        args["target"] = target
    return BehaviorScript(name="dom", rules=[
        Rule(do={"composite": "domain_power", "args": args}),
    ])


# ---------------------------------------------------------------------------
# Domain pick + per-day pool
# ---------------------------------------------------------------------------


class TestDomainPick(unittest.TestCase):
    def test_cleric_records_picked_domains(self):
        c = _cleric(("healing", "war"))
        self.assertEqual(c.domains, ["healing", "war"])

    def test_each_domain_gets_uses_pool(self):
        c = _cleric(("healing", "war"))
        # Wis 16 + 2 human racial = 18 → +4 mod. 3 + 4 = 7 uses.
        self.assertEqual(c.resources.get("domain_rebuke_death_uses"), 7)
        self.assertEqual(c.resources.get("domain_battle_rage_uses"), 7)

    def test_unknown_domain_silently_skipped(self):
        c = _cleric(("healing", "not_a_domain"))
        self.assertIn("domain_rebuke_death_uses", c.resources)
        # not_a_domain produced nothing — cleric.domains still records it
        # for later validation, but no resource pool was added.
        self.assertNotIn("domain_unknown_uses", c.resources)


# ---------------------------------------------------------------------------
# Healing — Rebuke Death (touch_heal)
# ---------------------------------------------------------------------------


class TestRebukeDeath(unittest.TestCase):
    def test_heals_dying_target_and_consumes_use(self):
        c = _cleric(("healing", "war"))
        ally = combatant_from_monster(REGISTRY.get_monster("orc"),
                                      (6, 5), "x")
        ally.current_hp = -3
        ally.add_condition("dying")
        grid = Grid(width=12, height=12)
        grid.place(c)
        grid.place(ally)
        enc = Encounter.begin(grid, [c, ally], Roller(seed=1))
        before_uses = c.resources["domain_rebuke_death_uses"]
        intent = Interpreter(_power_intent(
            "healing", ally,
        )).pick_turn(c, enc, grid)
        result = execute_turn(c, intent, enc, grid, Roller(seed=1))
        evt = next(e for e in result.events if e.kind == "domain_power")
        self.assertEqual(evt.detail["domain_id"], "healing")
        self.assertGreater(evt.detail["healed"], 0)
        self.assertEqual(c.resources["domain_rebuke_death_uses"],
                         before_uses - 1)
        # Once HP >= 0, dying lifted.
        self.assertGreater(ally.current_hp, -3)

    def test_skips_when_target_above_zero_hp(self):
        c = _cleric(("healing", "war"))
        ally = combatant_from_monster(REGISTRY.get_monster("orc"),
                                      (6, 5), "x")
        # ally above 0 HP — Rebuke Death has no target.
        grid = Grid(width=12, height=12)
        grid.place(c)
        grid.place(ally)
        enc = Encounter.begin(grid, [c, ally], Roller(seed=1))
        intent = Interpreter(_power_intent(
            "healing", ally,
        )).pick_turn(c, enc, grid)
        result = execute_turn(c, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("skip", kinds)


# ---------------------------------------------------------------------------
# War — Battle Rage (touch_buff: damage)
# ---------------------------------------------------------------------------


class TestBattleRage(unittest.TestCase):
    def test_grants_damage_buff_on_ally(self):
        c = _cleric(("healing", "war"))
        ally = combatant_from_monster(REGISTRY.get_monster("orc"),
                                      (6, 5), "x")
        grid = Grid(width=12, height=12)
        grid.place(c)
        grid.place(ally)
        enc = Encounter.begin(grid, [c, ally], Roller(seed=1))
        before_dmg_mods = sum(
            m.value for m in ally.modifiers.for_target("damage")
            if m.source.startswith("domain:")
        )
        intent = Interpreter(_power_intent(
            "war", ally,
        )).pick_turn(c, enc, grid)
        result = execute_turn(c, intent, enc, grid, Roller(seed=1))
        evt = next(e for e in result.events if e.kind == "domain_power")
        self.assertEqual(evt.detail["domain_id"], "war")
        # Now ally has at least +1 untyped damage from the buff.
        after_dmg_mods = sum(
            m.value for m in ally.modifiers.for_target("damage")
            if m.source.startswith("domain:")
        )
        self.assertGreater(after_dmg_mods, before_dmg_mods)


# ---------------------------------------------------------------------------
# Knowledge — Lore Keeper (touch_info)
# ---------------------------------------------------------------------------


class TestLoreKeeper(unittest.TestCase):
    def test_returns_creature_metadata(self):
        c = _cleric(("knowledge", "good"))
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (6, 5), "y")
        grid = Grid(width=12, height=12)
        grid.place(c)
        grid.place(target)
        enc = Encounter.begin(grid, [c, target], Roller(seed=1))
        intent = Interpreter(_power_intent(
            "knowledge", target,
        )).pick_turn(c, enc, grid)
        result = execute_turn(c, intent, enc, grid, Roller(seed=1))
        evt = next(e for e in result.events if e.kind == "domain_power")
        self.assertEqual(evt.detail["info"]["type"], "humanoid")
        self.assertIn("evil", evt.detail["info"]["alignment"])


# ---------------------------------------------------------------------------
# Air — Lightning Arc (ranged_damage)
# ---------------------------------------------------------------------------


class TestLightningArc(unittest.TestCase):
    def test_ranged_damage_against_target_in_range(self):
        c = _cleric(("air", "good"))
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (8, 5), "y")
        grid = Grid(width=20, height=10)
        grid.place(c)
        grid.place(target)
        enc = Encounter.begin(grid, [c, target], Roller(seed=1))
        before_hp = target.current_hp
        intent = Interpreter(_power_intent(
            "air", target,
        )).pick_turn(c, enc, grid)
        result = execute_turn(c, intent, enc, grid, Roller(seed=1))
        evt = next(e for e in result.events if e.kind == "domain_power")
        self.assertEqual(evt.detail["damage_type"], "electricity")
        self.assertLess(target.current_hp, before_hp)

    def test_skips_target_out_of_range(self):
        c = _cleric(("air", "good"))
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (15, 5), "y")  # 10 squares = 50ft, beyond 30ft
        grid = Grid(width=30, height=10)
        grid.place(c)
        grid.place(target)
        enc = Encounter.begin(grid, [c, target], Roller(seed=1))
        intent = Interpreter(_power_intent(
            "air", target,
        )).pick_turn(c, enc, grid)
        result = execute_turn(c, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("skip", kinds)


# ---------------------------------------------------------------------------
# Power-pool exhaustion
# ---------------------------------------------------------------------------


class TestDomainPoolExhaustion(unittest.TestCase):
    def test_skip_when_no_uses_left(self):
        c = _cleric(("healing", "war"))
        c.resources["domain_battle_rage_uses"] = 0
        ally = combatant_from_monster(REGISTRY.get_monster("orc"),
                                      (6, 5), "x")
        grid = Grid(width=12, height=12)
        grid.place(c)
        grid.place(ally)
        enc = Encounter.begin(grid, [c, ally], Roller(seed=1))
        intent = Interpreter(_power_intent(
            "war", ally,
        )).pick_turn(c, enc, grid)
        result = execute_turn(c, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("skip", kinds)


# ---------------------------------------------------------------------------
# Non-picked domain rejected
# ---------------------------------------------------------------------------


class TestUnpickedDomainRejected(unittest.TestCase):
    def test_cleric_cannot_use_domain_they_didnt_pick(self):
        c = _cleric(("healing", "war"))
        ally = combatant_from_monster(REGISTRY.get_monster("orc"),
                                      (6, 5), "x")
        grid = Grid(width=12, height=12)
        grid.place(c)
        grid.place(ally)
        enc = Encounter.begin(grid, [c, ally], Roller(seed=1))
        intent = Interpreter(_power_intent(
            "knowledge", ally,
        )).pick_turn(c, enc, grid)
        result = execute_turn(c, intent, enc, grid, Roller(seed=1))
        kinds = [e.kind for e in result.events]
        self.assertIn("skip", kinds)


if __name__ == "__main__":
    unittest.main()
