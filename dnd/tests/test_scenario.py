"""Tests for dnd.engine.scenario."""

from __future__ import annotations

import unittest

from dnd.engine.content import default_registry
from dnd.engine.scenario import ScenarioSpec, run_scenario


REGISTRY = default_registry()


def _basic_fighter_request() -> dict:
    return {
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
    }


# ---------------------------------------------------------------------------
# ScenarioSpec parsing
# ---------------------------------------------------------------------------


class TestSpecParsing(unittest.TestCase):
    def test_minimal_spec(self):
        spec = ScenarioSpec.from_dict({
            "name": "test",
            "width": 10,
            "height": 10,
            "combatants": [
                {"template_kind": "monster", "template_id": "goblin",
                 "position": [5, 5], "team": "enemies"},
            ],
        })
        self.assertEqual(spec.name, "test")
        self.assertEqual(spec.width, 10)
        self.assertEqual(len(spec.combatants), 1)

    def test_features_parsed(self):
        spec = ScenarioSpec.from_dict({
            "name": "with_walls",
            "width": 10, "height": 10,
            "features": [
                {"x": 5, "y": 5, "type": "wall"},
                {"x": 6, "y": 5, "type": "difficult"},
            ],
            "combatants": [],
        })
        self.assertEqual(len(spec.features), 2)
        self.assertEqual(spec.features[0].type, "wall")


# ---------------------------------------------------------------------------
# End-to-end scenario runs
# ---------------------------------------------------------------------------


class TestRunScenario(unittest.TestCase):
    def test_fighter_kills_goblin(self):
        spec = ScenarioSpec.from_dict({
            "name": "goblin_patrol_cr1",
            "width": 20, "height": 10,
            "seed": 7,
            "turn_limit": 30,
            "combatants": [
                {
                    "template_kind": "character",
                    "character_request": _basic_fighter_request(),
                    "position": [2, 5],
                    "team": "patrons",
                    "behavior": {
                        "name": "bruiser",
                        "rules": [
                            {"when": "enemy.in_range(1) is not None",
                             "do": {"composite": "full_attack",
                                    "args": {"target": "enemy.closest"}}},
                            {"when": "enemy.any",
                             "do": {"composite": "charge",
                                    "args": {"target": "enemy.closest"}}},
                        ],
                    },
                },
                {
                    "template_kind": "monster",
                    "template_id": "goblin",
                    "position": [10, 5],
                    "team": "enemies",
                },
            ],
        })
        result = run_scenario(spec, REGISTRY)
        self.assertEqual(result.winner, "patrons")
        self.assertFalse(result.timed_out)
        # Should have at least a few turns.
        self.assertGreater(len(result.turns), 0)
        # Final state shows fighter alive, goblin not.
        states = list(result.final_state.values())
        fighter_state = [s for s in states if s["team"] == "patrons"][0]
        goblin_state = [s for s in states if s["team"] == "enemies"][0]
        self.assertTrue(fighter_state["alive"])
        self.assertFalse(goblin_state["alive"])

    def test_deterministic_with_same_seed(self):
        body = {
            "name": "rerun_test",
            "width": 20, "height": 10,
            "seed": 42,
            "turn_limit": 30,
            "combatants": [
                {
                    "template_kind": "character",
                    "character_request": _basic_fighter_request(),
                    "position": [2, 5],
                    "team": "patrons",
                    "behavior": {
                        "name": "bruiser",
                        "rules": [
                            {"when": "enemy.in_range(1) is not None",
                             "do": {"composite": "full_attack",
                                    "args": {"target": "enemy.closest"}}},
                            {"when": "enemy.any",
                             "do": {"composite": "charge",
                                    "args": {"target": "enemy.closest"}}},
                        ],
                    },
                },
                {
                    "template_kind": "monster",
                    "template_id": "goblin",
                    "position": [10, 5],
                    "team": "enemies",
                },
            ],
        }
        spec1 = ScenarioSpec.from_dict(body)
        spec2 = ScenarioSpec.from_dict(body)
        result1 = run_scenario(spec1, REGISTRY)
        result2 = run_scenario(spec2, REGISTRY)
        self.assertEqual(result1.winner, result2.winner)
        self.assertEqual(result1.rounds, result2.rounds)
        # Initiative order should match.
        order1 = [ir["combatant_id"] for ir in result1.initiative]
        order2 = [ir["combatant_id"] for ir in result2.initiative]
        # IDs are random; compare by name instead.
        names1 = [ir["name"] for ir in result1.initiative]
        names2 = [ir["name"] for ir in result2.initiative]
        self.assertEqual(names1, names2)

    def test_wizard_magic_missiles_goblin(self):
        """End-to-end: wizard casts magic_missile via DSL → kills goblin."""
        wizard_request = {
            "name": "Aurelia",
            "race": "elf",
            "class": "wizard",
            "alignment": "true_neutral",
            "ability_scores": {
                "method": "point_buy_20",
                "scores": {"str": 8, "dex": 14, "con": 14,
                           "int": 16, "wis": 12, "cha": 10},
            },
            "feats": ["combat_expertise"],
            "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
            "bonus_languages": [],
        }
        spec = ScenarioSpec.from_dict({
            "name": "wizard_vs_goblin",
            "width": 20, "height": 10,
            "seed": 11,
            "turn_limit": 20,
            "combatants": [
                {
                    "template_kind": "character",
                    "character_request": wizard_request,
                    "position": [2, 5],
                    "team": "patrons",
                    "behavior": {
                        "name": "blaster",
                        "rules": [
                            {"when": "enemy.any",
                             "do": {"composite": "cast",
                                    "args": {"spell": "magic_missile",
                                             "target": "enemy.closest",
                                             "spell_level": 1}}},
                        ],
                    },
                },
                {
                    "template_kind": "monster",
                    "template_id": "goblin",
                    "position": [10, 5],
                    "team": "enemies",
                },
            ],
        })
        result = run_scenario(spec, REGISTRY)
        # Verify the wizard cast at least one magic missile.
        cast_events = [
            e for t in result.turns for e in t["events"]
            if e["kind"] == "cast"
        ]
        self.assertGreater(len(cast_events), 0)
        # The cast event detail should show the magic_missile spell + damage.
        first_cast = cast_events[0]
        self.assertEqual(first_cast["detail"]["spell_id"], "magic_missile")
        self.assertGreater(
            sum(first_cast["detail"]["damage_per_target"].values()),
            0,
        )

    def test_cleric_heals_wounded_ally(self):
        """End-to-end: cleric in a party casts cure_light_wounds via DSL."""
        cleric_request = {
            "name": "Brother Reith",
            "race": "human",
            "class": "cleric",
            "alignment": "lawful_good",
            "ability_scores": {
                "method": "point_buy_20",
                "scores": {"str": 14, "dex": 10, "con": 14,
                           "int": 10, "wis": 14, "cha": 14},
            },
            "free_ability_choice": "wis",
            "feats": ["toughness", "iron_will"],
            "skill_ranks": {"heal": 1, "knowledge_religion": 1},
            "bonus_languages": [],
        }
        wounded_fighter = {
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
        }
        # Need at least two teams or the encounter terminates immediately.
        # Add a goblin to make the encounter live; the cleric heals
        # whoever in the party is hurt.
        spec = ScenarioSpec.from_dict({
            "name": "heal_party",
            "width": 12, "height": 10,
            "seed": 5,
            "turn_limit": 8,
            "combatants": [
                {
                    "template_kind": "character",
                    "character_request": cleric_request,
                    "position": [2, 5],
                    "team": "patrons",
                    "behavior": {
                        "name": "healer",
                        "rules": [
                            {"when": "ally.lowest_hp_pct is not None",
                             "do": {"composite": "cast",
                                    "args": {"spell": "cure_light_wounds",
                                             "target": "ally.lowest_hp_pct",
                                             "spell_level": 1}}},
                        ],
                    },
                },
                {
                    "template_kind": "character",
                    "character_request": wounded_fighter,
                    "position": [4, 5],
                    "team": "patrons",
                    "behavior": {
                        "name": "tank",
                        "rules": [
                            {"when": "enemy.in_range(1) is not None",
                             "do": {"composite": "full_attack",
                                    "args": {"target": "enemy.closest"}}},
                            {"when": "enemy.any",
                             "do": {"composite": "charge",
                                    "args": {"target": "enemy.closest"}}},
                        ],
                    },
                },
                {
                    "template_kind": "monster",
                    "template_id": "goblin",
                    "position": [10, 5],
                    "team": "enemies",
                },
            ],
        })
        result = run_scenario(spec, REGISTRY)
        cast_events = [
            e for t in result.turns for e in t["events"]
            if e["kind"] == "cast"
        ]
        # Cleric's first turn should fire her heal rule (an ally always
        # exists, even at full HP — cure_light_wounds is "harmless" and
        # ally.lowest_hp_pct returns the lowest, including herself).
        self.assertGreater(len(cast_events), 0)
        self.assertEqual(cast_events[0]["detail"]["spell_id"],
                         "cure_light_wounds")

    def test_turn_limit_timeout(self):
        # Two combatants on opposite sides of a giant grid with no behavior;
        # they default to monster AI which approaches but might not finish in time.
        spec = ScenarioSpec.from_dict({
            "name": "stalemate",
            "width": 50, "height": 50,
            "seed": 1,
            "turn_limit": 2,   # very short cap
            "combatants": [
                {"template_kind": "monster", "template_id": "goblin",
                 "position": [5, 5], "team": "a"},
                {"template_kind": "monster", "template_id": "goblin",
                 "position": [45, 45], "team": "b"},
            ],
        })
        result = run_scenario(spec, REGISTRY)
        self.assertTrue(result.timed_out)


if __name__ == "__main__":
    unittest.main()
