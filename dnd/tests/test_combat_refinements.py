"""Tests for the combat refinements cluster — helpless target bonus,
weapon proficiency penalty, withdraw no-AoO, and the Run action."""

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
    _has_dex_denied,
    _weapon_not_proficient,
    execute_turn,
)


REGISTRY = default_registry()


def _setup(actor_template, target_template,
           actor_pos=(5, 5), target_pos=(6, 5),
           width=12, height=12):
    a = combatant_from_monster(REGISTRY.get_monster(actor_template),
                               actor_pos, "x")
    b = combatant_from_monster(REGISTRY.get_monster(target_template),
                               target_pos, "y")
    grid = Grid(width=width, height=height)
    grid.place(a)
    grid.place(b)
    enc = Encounter.begin(grid, [a, b], Roller(seed=1))
    return a, b, enc, grid


class TestHelplessAttackerBonus(unittest.TestCase):
    def test_helpless_target_treated_as_flat_footed(self):
        """A helpless target denies its Dex bonus to AC."""
        a, b, _, _ = _setup("orc", "goblin")
        b.add_condition("helpless")
        # _has_dex_denied says yes.
        self.assertTrue(_has_dex_denied(b))

    def test_dying_target_is_dex_denied(self):
        """A dying target is helpless → dex-denied."""
        a, b, _, _ = _setup("orc", "goblin")
        b.add_condition("paralyzed")
        self.assertTrue(_has_dex_denied(b))

    def test_normal_target_not_dex_denied(self):
        a, b, _, _ = _setup("orc", "goblin")
        self.assertFalse(_has_dex_denied(b))


class TestWeaponProficiencyPenalty(unittest.TestCase):
    def _wizard(self, weapon: str):
        # Wizards are proficient with: club, dagger, heavy_crossbow,
        # light_crossbow, quarterstaff. Anything else → -4.
        # 0 + 5 + 5 + 10 + 0 + 0 = 20. Human gets +1 bonus feat
        # → need 2 general feats.
        req = CharacterRequest.from_dict({
            "name": "Aurelia", "race": "human", "class": "wizard",
            "alignment": "neutral_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 10, "dex": 14, "con": 14,
                           "int": 16, "wis": 10, "cha": 10}},
            "free_ability_choice": "int",
            "feats": ["combat_expertise", "iron_will"],
            "skill_ranks": {"spellcraft": 1},
            "bonus_languages": [],
            "equipment": {"weapon": weapon},
        })
        char = create_character(req, REGISTRY)
        return combatant_from_character(char, REGISTRY, (5, 5), "x")

    def test_wizard_with_quarterstaff_is_proficient(self):
        w = self._wizard("quarterstaff")
        chosen = w.attack_options[0]
        self.assertFalse(_weapon_not_proficient(w, chosen))

    def test_wizard_with_longsword_is_not_proficient(self):
        w = self._wizard("longsword")
        chosen = w.attack_options[0]
        self.assertTrue(_weapon_not_proficient(w, chosen))

    def test_wizard_proficiency_set_includes_simple_weapons(self):
        w = self._wizard("quarterstaff")
        # Wizard prof string is the explicit list — no whole-category
        # proficiency, but the specific weapons are present.
        profs = w.weapon_proficiency_categories
        self.assertIn("quarterstaff", profs)
        self.assertIn("dagger", profs)
        self.assertIn("club", profs)

    def test_fighter_has_simple_and_martial(self):
        # 5 + 5 + 5 + 2 + 2 + 1 = 20. Human + fighter → 2 general feats
        # (1 base + 1 human bonus); fighter L1 also gives 1 class bonus feat.
        req = CharacterRequest.from_dict({
            "name": "Edric", "race": "human", "class": "fighter",
            "alignment": "lawful_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 14, "con": 14,
                           "int": 12, "wis": 12, "cha": 11}},
            "free_ability_choice": "str",
            "feats": ["power_attack", "iron_will"],
            "skill_ranks": {"climb": 1, "swim": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "weapon_focus_longsword"},
        })
        char = create_character(req, REGISTRY)
        f = combatant_from_character(char, REGISTRY, (5, 5), "x")
        profs = f.weapon_proficiency_categories
        self.assertIn("simple", profs)
        self.assertIn("martial", profs)

    def test_natural_attack_skips_proficiency_check(self):
        # Goblin morningstar attack — but more importantly, monsters
        # without weapon_proficiency_categories should not trigger
        # the penalty.
        g = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                   (0, 0), "x")
        # Empty profs = "not modeled, assume proficient".
        self.assertFalse(_weapon_not_proficient(g, g.attack_options[0]))

    def test_attack_option_carries_weapon_category(self):
        w = self._wizard("longsword")
        self.assertEqual(w.attack_options[0]["weapon_category"], "martial")


class TestWithdrawNoAoO(unittest.TestCase):
    def test_first_square_doesnt_provoke(self):
        """Withdraw: first square of movement is safe."""
        # Set up: orc adjacent to goblin. Goblin withdraws — should NOT
        # take an AoO from the orc on the first square.
        a, b, enc, grid = _setup("orc", "goblin",
                                 actor_pos=(5, 5), target_pos=(6, 5))
        # The goblin is going to withdraw away from the orc (east).
        b_starting_hp = b.current_hp
        script = BehaviorScript(name="withdraw", rules=[
            Rule(do={"composite": "withdraw", "args": {"direction": "east"}}),
        ])
        intent = Interpreter(script).pick_turn(b, enc, grid)
        execute_turn(b, intent, enc, grid, Roller(seed=1))
        # Goblin shouldn't have lost HP from an AoO.
        self.assertEqual(b.current_hp, b_starting_hp)
        # And should have moved.
        self.assertNotEqual(b.position, (6, 5))


class TestRun(unittest.TestCase):
    def test_run_moves_4x_speed(self):
        # Big grid — orc speed 30 = 6 squares; run = 24 squares.
        a, _, enc, grid = _setup("orc", "goblin",
                                 actor_pos=(5, 5), target_pos=(40, 40),
                                 width=50, height=50)
        before = a.position
        script = BehaviorScript(name="run", rules=[
            Rule(do={"composite": "run", "args": {"direction": "east"}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        execute_turn(a, intent, enc, grid, Roller(seed=1))
        dx = abs(a.position[0] - before[0])
        dy = abs(a.position[1] - before[1])
        moved = max(dx, dy)
        # Distance moved should be > regular speed (6 squares).
        self.assertGreater(moved, 6)

    def test_run_loses_dex_to_ac(self):
        # Use a high-Dex character so the lost AC bonus is observable.
        # 2 + 10 + 5 + 2 + 1 + 0 = 20. Human → 2 feats.
        req = CharacterRequest.from_dict({
            "name": "Swift", "race": "human", "class": "rogue",
            "alignment": "true_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 12, "dex": 16, "con": 14,
                           "int": 12, "wis": 11, "cha": 10}},
            "free_ability_choice": "dex",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"acrobatics": 1, "stealth": 1},
            "bonus_languages": [],
        })
        char = create_character(req, REGISTRY)
        rogue = combatant_from_character(char, REGISTRY, (5, 5), "x")
        ac_before = rogue.ac()
        # Place enemy and grid so we can run a turn.
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (10, 10), "y")
        grid = Grid(width=20, height=20)
        grid.place(rogue)
        grid.place(target)
        enc = Encounter.begin(grid, [rogue, target], Roller(seed=1))
        script = BehaviorScript(name="run", rules=[
            Rule(do={"composite": "run", "args": {"direction": "east"}}),
        ])
        intent = Interpreter(script).pick_turn(rogue, enc, grid)
        execute_turn(rogue, intent, enc, grid, Roller(seed=1))
        # AC should drop by the Dex-mod (rogue Dex 18 → +4).
        ac_after = rogue.ac()
        self.assertLess(ac_after, ac_before)

    def test_run_event_emitted(self):
        a, _, enc, grid = _setup("orc", "goblin",
                                 actor_pos=(5, 5), target_pos=(40, 40),
                                 width=50, height=50)
        script = BehaviorScript(name="run", rules=[
            Rule(do={"composite": "run", "args": {"direction": "east"}}),
        ])
        intent = Interpreter(script).pick_turn(a, enc, grid)
        result = execute_turn(a, intent, enc, grid, Roller(seed=1))
        run_events = [e for e in result.events if e.kind == "run"]
        self.assertEqual(len(run_events), 1)


if __name__ == "__main__":
    unittest.main()
