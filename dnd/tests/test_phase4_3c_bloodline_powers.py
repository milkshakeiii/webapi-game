"""Tests for Phase 4.3c — sorcerer L1 active bloodline powers.

RAW (Foundry pack ``class-abilities.md``):

- Heavenly Fire (Celestial, lines around 43152): ranged touch 30 ft;
  evil → 1d4 + 1 per 2 levels divine damage (no ER/immunity); good →
  heal 1d4 + 1 per 2 levels (1/day per creature); neutral → no effect.
- Draconic Claws (Draconic, around the dragon-bloodline embed): free
  action; 2 claw natural attacks at full BAB, 1d4+Str (1d3 small).
  3 + Cha mod rounds/day.
- Laughing Touch (Fey, line 56227): melee touch, target laughs 1
  round (move action only); mind-affecting.
- Corrupting Touch (Infernal, line 16176): melee touch, shaken for
  max(1, sorc_lvl // 2) rounds; multiple touches add duration.
"""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import (
    combatant_from_character,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import TurnIntent
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


def _sorc(bloodline: str, **extra) -> object:
    body = {
        "name": "Vyx", "race": "human", "class": "sorcerer",
        "alignment": "chaotic_neutral",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 14, "dex": 14, "con": 14,
                       "int": 10, "wis": 10, "cha": 14}},
        "free_ability_choice": "cha",
        "feats": ["dodge", "iron_will"],
        "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
        "bonus_languages": [],
        "class_choices": {"sorcerer_bloodline": bloodline},
    }
    body["class_choices"].update(extra)
    return create_character(CharacterRequest.from_dict(body), REGISTRY)


def _setup(bloodline: str, target_monster: str = "goblin",
           target_pos=(6, 5), **extra):
    char = _sorc(bloodline, **extra)
    sorc = combatant_from_character(char, REGISTRY, (5, 5), "x")
    target = combatant_from_monster(
        REGISTRY.get_monster(target_monster), target_pos, "y",
    )
    target.max_hp = 9999
    target.current_hp = 9999
    grid = Grid(width=20, height=20)
    grid.place(sorc)
    grid.place(target)
    enc = Encounter.begin(grid, [sorc, target], Roller(seed=1))
    return sorc, target, enc, grid


def _invoke(actor, power_id, target, enc, grid):
    do = {"composite": "sorcerer_bloodline_power",
          "args": {"power": power_id, "target": target}}
    intent = TurnIntent(rule_index=0, do=do, namespace={})
    return execute_turn(actor, intent, enc, grid, Roller(seed=1))


# ---------------------------------------------------------------------------
# Heavenly Fire (Celestial)
# ---------------------------------------------------------------------------


class TestHeavenlyFire(unittest.TestCase):
    def test_damages_evil_target(self):
        # Goblins are typically "neutral evil" in the bestiary. Force
        # the alignment for robustness.
        sorc, goblin, enc, grid = _setup("celestial")
        goblin.template = type(goblin.template)(
            **{**goblin.template.__dict__, "alignment": "neutral_evil"}
        ) if hasattr(goblin.template, "__dict__") else goblin.template
        # Force the touch attack to hit.
        sorc.bases["bab"] = 100
        result = _invoke(sorc, "heavenly_fire", goblin, enc, grid)
        ev = next(e for e in result.events
                  if e.kind == "wizard_power_heavenly_fire")
        self.assertEqual(ev.detail["result"], "damage_evil")

    def test_heals_good_target(self):
        sorc, goblin, enc, grid = _setup("celestial")
        # Build a "good" ally — set alignment to good and lower HP.
        align_target = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (5, 6), "x",  # same team
        )
        align_target.template = type(align_target.template)(
            **{**align_target.template.__dict__,
               "alignment": "lawful_good"}
        ) if hasattr(align_target.template, "__dict__") else align_target.template
        align_target.current_hp = 1
        align_target.max_hp = 20
        grid.place(align_target)
        enc.initiative.append(enc.initiative[0].__class__(
            combatant=align_target, roll=10, modifier=0, total=10,
        ))
        result = _invoke(sorc, "heavenly_fire", align_target, enc, grid)
        ev = next(e for e in result.events
                  if e.kind == "wizard_power_heavenly_fire")
        self.assertEqual(ev.detail["result"], "healed_good")
        self.assertGreater(ev.detail["amount"], 0)

    def test_good_creature_already_benefited(self):
        sorc, goblin, enc, grid = _setup("celestial")
        ally = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (5, 6), "x",
        )
        ally.template = type(ally.template)(
            **{**ally.template.__dict__, "alignment": "lawful_good"}
        ) if hasattr(ally.template, "__dict__") else ally.template
        ally.current_hp = 1
        ally.max_hp = 20
        ally.resources["heavenly_fire_received_round"] = 1
        grid.place(ally)
        enc.initiative.append(enc.initiative[0].__class__(
            combatant=ally, roll=10, modifier=0, total=10,
        ))
        result = _invoke(sorc, "heavenly_fire", ally, enc, grid)
        ev = next(e for e in result.events
                  if e.kind == "wizard_power_heavenly_fire")
        self.assertEqual(ev.detail["result"], "good_already_benefited")

    def test_neutral_target_no_effect(self):
        sorc, goblin, enc, grid = _setup("celestial")
        goblin.template = type(goblin.template)(
            **{**goblin.template.__dict__, "alignment": "true_neutral"}
        ) if hasattr(goblin.template, "__dict__") else goblin.template
        result = _invoke(sorc, "heavenly_fire", goblin, enc, grid)
        ev = next(e for e in result.events
                  if e.kind == "wizard_power_heavenly_fire")
        self.assertEqual(ev.detail["result"], "neutral_no_effect")


# ---------------------------------------------------------------------------
# Draconic Claws
# ---------------------------------------------------------------------------


class TestDraconicClaws(unittest.TestCase):
    def test_grow_claws_installs_two_natural_attacks(self):
        sorc, goblin, enc, grid = _setup(
            "draconic", sorcerer_dragon_type="red",
        )
        before_attacks = list(sorc.attack_options)
        result = _invoke(sorc, "draconic_claws", None, enc, grid)
        ev = next(e for e in result.events
                  if e.kind == "wizard_power_draconic_claws")
        self.assertEqual(ev.detail["claw_count"], 2)
        # Two claw entries now in attack_options.
        claws = [a for a in sorc.attack_options
                 if a.get("weapon_id") == "draconic_claw"]
        self.assertEqual(len(claws), 2)
        for c in claws:
            self.assertEqual(c["damage"], "1d4")  # medium L1
            self.assertTrue(c["is_natural"])

    def test_small_sorcerer_does_1d3(self):
        body = {
            "name": "Vyx", "race": "halfling", "class": "sorcerer",
            "alignment": "chaotic_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 14, "con": 14,
                           "int": 10, "wis": 10, "cha": 14}},
            "feats": ["dodge"],
            "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
            "bonus_languages": [],
            "class_choices": {"sorcerer_bloodline": "draconic",
                              "sorcerer_dragon_type": "red"},
        }
        char = create_character(CharacterRequest.from_dict(body), REGISTRY)
        sorc = combatant_from_character(char, REGISTRY, (5, 5), "x")
        goblin = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (6, 5), "y",
        )
        grid = Grid(width=20, height=20)
        grid.place(sorc)
        grid.place(goblin)
        enc = Encounter.begin(grid, [sorc, goblin], Roller(seed=1))
        _invoke(sorc, "draconic_claws", None, enc, grid)
        claws = [a for a in sorc.attack_options
                 if a.get("weapon_id") == "draconic_claw"]
        for c in claws:
            self.assertEqual(c["damage"], "1d3")  # small L1


# ---------------------------------------------------------------------------
# Laughing Touch (Fey)
# ---------------------------------------------------------------------------


class TestLaughingTouch(unittest.TestCase):
    def test_applies_laughing_on_hit(self):
        sorc, goblin, enc, grid = _setup("fey")
        sorc.bases["bab"] = 100
        result = _invoke(sorc, "laughing_touch", goblin, enc, grid)
        ev = next(e for e in result.events
                  if e.kind == "wizard_power_laughing_touch")
        self.assertEqual(ev.detail.get("condition"), "laughing")
        self.assertIn("laughing", goblin.conditions)

    def test_laughing_creature_can_only_move(self):
        # With the condition applied, the intent-legality check
        # should reject a standard or full-round, allow move-only.
        from dnd.engine.actions import _validate_intent
        sorc, goblin, enc, grid = _setup("fey")
        goblin.add_condition("laughing")
        # Standard attack: rejected.
        self.assertIsNotNone(_validate_intent(
            goblin,
            {"standard": {"type": "attack", "target": "enemy.closest"}},
            grid,
        ))
        # Move only: allowed.
        self.assertIsNone(_validate_intent(
            goblin,
            {"move": {"type": "move_to", "target": (10, 10)}},
            grid,
        ))


# ---------------------------------------------------------------------------
# Corrupting Touch (Infernal)
# ---------------------------------------------------------------------------


class TestCorruptingTouch(unittest.TestCase):
    def test_shakens_target_on_hit(self):
        sorc, goblin, enc, grid = _setup("infernal")
        sorc.bases["bab"] = 100
        result = _invoke(sorc, "corrupting_touch", goblin, enc, grid)
        ev = next(e for e in result.events
                  if e.kind == "wizard_power_corrupting_touch")
        self.assertEqual(ev.detail.get("condition"), "shaken")
        # L1 sorc → max(1, 1//2) = 1 round.
        self.assertEqual(ev.detail.get("duration_rounds"), 1)
        self.assertIn("shaken", goblin.conditions)

    def test_multiple_touches_add_duration(self):
        # RAW: "Multiple touches do not stack, but they do add to the
        # duration." Hit twice → duration becomes 1 + 1 = 2.
        sorc, goblin, enc, grid = _setup("infernal")
        sorc.bases["bab"] = 100
        _invoke(sorc, "corrupting_touch", goblin, enc, grid)
        result2 = _invoke(sorc, "corrupting_touch", goblin, enc, grid)
        ev = [e for e in result2.events
              if e.kind == "wizard_power_corrupting_touch"][-1]
        self.assertEqual(ev.detail.get("duration_rounds"), 2)


if __name__ == "__main__":
    unittest.main()
