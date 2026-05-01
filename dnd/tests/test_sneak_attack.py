"""Tests for Sneak Attack precision damage."""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combat import AttackProfile, DefenseProfile, resolve_attack
from dnd.engine.combatant import (
    combatant_from_character,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import _sneak_attack_dice


REGISTRY = default_registry()


def _rogue_request(level=1):
    base = {
        "name": "Pim", "race": "halfling", "class": "rogue",
        "alignment": "chaotic_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 10, "dex": 14, "con": 14,
                       "int": 13, "wis": 12, "cha": 14}},
        "feats": ["weapon_finesse"],
        "skill_ranks": {"stealth": 1, "perception": 1, "acrobatics": 1},
        "bonus_languages": ["elven"],
    }
    if level > 1:
        levels = {}
        for L in range(2, level + 1):
            entry = {"class": "rogue", "skill_ranks": {"stealth": 1}}
            if L % 2 == 1:
                entry["feat_general"] = "improved_initiative"
            if L in (4, 8, 12, 16, 20):
                entry["ability_bump"] = "dex"
            levels[str(L)] = entry
        base["level_plan"] = {
            "name": "rogue_progression",
            "target_level": level,
            "levels": levels,
        }
    return CharacterRequest.from_dict(base)


def _fighter_request():
    return CharacterRequest.from_dict({
        "name": "Edric", "race": "human", "class": "fighter",
        "alignment": "lawful_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 16, "dex": 14, "con": 14,
                       "int": 10, "wis": 10, "cha": 10}},
        "free_ability_choice": "str",
        "feats": ["power_attack", "weapon_focus"],
        "skill_ranks": {"climb": 1, "swim": 1},
        "bonus_languages": [],
        "class_choices": {"fighter_bonus_feat": "improved_initiative"},
    })


class TestSneakAttackDiceFormula(unittest.TestCase):
    def test_l1_rogue_gets_1d6(self):
        char = create_character(_rogue_request(1), REGISTRY)
        rogue = combatant_from_character(char, REGISTRY, (5, 5), "patrons")
        goblin = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (6, 5), "enemies")
        goblin.add_condition("flat_footed")  # auto-qualify
        grid = Grid(width=10, height=10)
        grid.place(rogue)
        grid.place(goblin)
        enc = Encounter.begin(grid, [rogue, goblin], Roller(seed=1))
        dice = _sneak_attack_dice(rogue, goblin, grid, enc)
        self.assertEqual(dice, "1d6")

    def test_l3_rogue_gets_2d6(self):
        char = create_character(_rogue_request(3), REGISTRY)
        rogue = combatant_from_character(char, REGISTRY, (5, 5), "patrons")
        goblin = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (6, 5), "enemies")
        goblin.add_condition("flat_footed")
        grid = Grid(width=10, height=10)
        grid.place(rogue)
        grid.place(goblin)
        enc = Encounter.begin(grid, [rogue, goblin], Roller(seed=1))
        dice = _sneak_attack_dice(rogue, goblin, grid, enc)
        self.assertEqual(dice, "2d6")

    def test_non_rogue_gets_no_sneak_attack(self):
        char = create_character(_fighter_request(), REGISTRY)
        fighter = combatant_from_character(char, REGISTRY, (5, 5), "patrons")
        goblin = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (6, 5), "enemies")
        goblin.add_condition("flat_footed")
        grid = Grid(width=10, height=10)
        grid.place(fighter)
        grid.place(goblin)
        enc = Encounter.begin(grid, [fighter, goblin], Roller(seed=1))
        dice = _sneak_attack_dice(fighter, goblin, grid, enc)
        self.assertEqual(dice, "")


class TestSneakAttackTriggers(unittest.TestCase):
    def setUp(self) -> None:
        self.char = create_character(_rogue_request(1), REGISTRY)
        self.rogue = combatant_from_character(self.char, REGISTRY, (5, 5), "patrons")
        self.goblin = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (6, 5), "enemies")
        self.grid = Grid(width=10, height=10)
        self.grid.place(self.rogue)
        self.grid.place(self.goblin)
        self.enc = Encounter.begin(
            self.grid, [self.rogue, self.goblin], Roller(seed=1))

    def test_no_qualification_returns_empty(self):
        # Rogue alone, target has full Dex, no flank — no sneak attack.
        self.assertEqual(
            _sneak_attack_dice(self.rogue, self.goblin, self.grid, self.enc),
            "",
        )

    def test_flat_footed_target_qualifies(self):
        self.goblin.add_condition("flat_footed")
        self.assertEqual(
            _sneak_attack_dice(self.rogue, self.goblin, self.grid, self.enc),
            "1d6",
        )

    def test_paralyzed_target_qualifies(self):
        self.goblin.add_condition("paralyzed")
        self.assertEqual(
            _sneak_attack_dice(self.rogue, self.goblin, self.grid, self.enc),
            "1d6",
        )

    def test_sleeping_target_qualifies(self):
        self.goblin.add_condition("sleeping")
        self.assertEqual(
            _sneak_attack_dice(self.rogue, self.goblin, self.grid, self.enc),
            "1d6",
        )


class TestSneakAttackFlanking(unittest.TestCase):
    def test_flanking_with_ally_qualifies(self):
        rogue = combatant_from_character(
            create_character(_rogue_request(1), REGISTRY),
            REGISTRY, (4, 5), "patrons")
        ally = combatant_from_character(
            create_character(_fighter_request(), REGISTRY),
            REGISTRY, (6, 5), "patrons")
        goblin = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (5, 5), "enemies")
        grid = Grid(width=10, height=10)
        grid.place(rogue)
        grid.place(ally)
        grid.place(goblin)
        enc = Encounter.begin(grid, [rogue, ally, goblin], Roller(seed=1))
        # Rogue at (4, 5), ally at (6, 5), goblin at (5, 5) between them.
        # Both threaten goblin from opposite sides — flanking.
        dice = _sneak_attack_dice(rogue, goblin, grid, enc)
        self.assertEqual(dice, "1d6")

    def test_no_flank_no_sneak_attack(self):
        rogue = combatant_from_character(
            create_character(_rogue_request(1), REGISTRY),
            REGISTRY, (4, 5), "patrons")
        ally = combatant_from_character(
            create_character(_fighter_request(), REGISTRY),
            REGISTRY, (4, 4), "patrons")  # same side as rogue
        goblin = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (5, 5), "enemies")
        grid = Grid(width=10, height=10)
        grid.place(rogue)
        grid.place(ally)
        grid.place(goblin)
        enc = Encounter.begin(grid, [rogue, ally, goblin], Roller(seed=1))
        # Rogue and ally on same side of goblin; not flanking.
        dice = _sneak_attack_dice(rogue, goblin, grid, enc)
        self.assertEqual(dice, "")


class TestSneakAttackInCombat(unittest.TestCase):
    def test_attack_with_precision_dice_adds_damage(self):
        # Direct combat math test: same attack with vs without precision
        # dice. Find a seed that produces a hit.
        attack_no_sa = AttackProfile(
            attack_bonus=10, damage_dice="1d6", damage_bonus=0,
            crit_range=(20, 20), crit_multiplier=2,
            damage_type="P", name="shortsword",
        )
        attack_with_sa = AttackProfile(
            attack_bonus=10, damage_dice="1d6", damage_bonus=0,
            crit_range=(20, 20), crit_multiplier=2,
            damage_type="P", name="shortsword",
            precision_damage_dice="1d6",
        )
        defense = DefenseProfile(ac=12, touch_ac=12, flat_footed_ac=12)
        # Use the same RNG seed for both — the d20 + first d6 are identical.
        # The version with precision should be HIGHER by an extra d6 roll.
        out_no = resolve_attack(attack_no_sa, defense, Roller(seed=42))
        out_yes = resolve_attack(attack_with_sa, defense, Roller(seed=42))
        if not out_no.hit:
            self.skipTest("seed didn't produce a hit; not a real failure")
        self.assertTrue(out_yes.hit)
        self.assertGreater(out_yes.damage, out_no.damage)
        # Precision damage should be in the trace.
        self.assertTrue(any("precision" in line for line in out_yes.log))

    def test_precision_not_multiplied_on_crit(self):
        # Force a crit by making attack always succeed with high crit range.
        attack = AttackProfile(
            attack_bonus=20, damage_dice="1d6", damage_bonus=0,
            crit_range=(2, 20), crit_multiplier=2,  # always threat
            damage_type="P", name="rapier",
            precision_damage_dice="1d6",
        )
        defense = DefenseProfile(ac=10, touch_ac=10, flat_footed_ac=10)
        # Run multiple seeds; check that whenever we crit, precision
        # damage is one die's worth (not doubled).
        crits_seen = 0
        for seed in range(1, 200):
            r = Roller(seed=seed)
            out = resolve_attack(attack, defense, r)
            if not out.crit:
                continue
            crits_seen += 1
            # Look for "precision: dice=1d6" in log — should show 1 roll,
            # not 2.
            prec_line = next(
                (line for line in out.log if line.startswith("precision")),
                None,
            )
            self.assertIsNotNone(prec_line)
            # Format: "precision: dice=1d6 rolls=[N] → N"
            self.assertIn("rolls=[", prec_line)
            # Count rolls inside [].
            inside = prec_line.split("[")[1].split("]")[0]
            n_rolls = len([x for x in inside.split(",") if x.strip()])
            self.assertEqual(
                n_rolls, 1,
                f"precision rolls should be 1 (not multiplied on crit); got "
                f"{n_rolls}: {prec_line}",
            )
            if crits_seen >= 5:
                break
        self.assertGreater(crits_seen, 0,
            "no crit triggered in 200 seeds — adjust test")


class TestFlankingAttackBonus(unittest.TestCase):
    """Flanking grants +2 attack to BOTH flankers, not just the rogue."""

    def test_fighter_flanking_gets_plus_2_attack(self):
        # Fighter and rogue flank a goblin; fighter's attack bonus should
        # include +2 flanking.
        from dnd.engine.turn_executor import (
            _flanking_attack_bonus, _is_flanking,
        )
        fighter = combatant_from_character(
            create_character(_fighter_request(), REGISTRY),
            REGISTRY, (4, 5), "patrons")
        rogue = combatant_from_character(
            create_character(_rogue_request(1), REGISTRY),
            REGISTRY, (6, 5), "patrons")
        goblin = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (5, 5), "enemies")
        grid = Grid(width=10, height=10)
        grid.place(fighter)
        grid.place(rogue)
        grid.place(goblin)
        enc = Encounter.begin(grid, [fighter, rogue, goblin], Roller(seed=1))

        # Fighter is flanking (rogue is on opposite side of goblin).
        self.assertTrue(_is_flanking(fighter, goblin, grid, enc))
        bonus = _flanking_attack_bonus(
            fighter, goblin, grid, enc, is_ranged=False,
        )
        self.assertEqual(bonus, 2)
        # Rogue is also flanking from her own perspective.
        self.assertTrue(_is_flanking(rogue, goblin, grid, enc))

    def test_solo_attacker_no_flanking_bonus(self):
        from dnd.engine.turn_executor import _flanking_attack_bonus
        fighter = combatant_from_character(
            create_character(_fighter_request(), REGISTRY),
            REGISTRY, (4, 5), "patrons")
        goblin = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (5, 5), "enemies")
        grid = Grid(width=10, height=10)
        grid.place(fighter)
        grid.place(goblin)
        enc = Encounter.begin(grid, [fighter, goblin], Roller(seed=1))
        bonus = _flanking_attack_bonus(
            fighter, goblin, grid, enc, is_ranged=False,
        )
        self.assertEqual(bonus, 0)

    def test_ranged_attack_no_flanking_bonus(self):
        from dnd.engine.turn_executor import _flanking_attack_bonus
        fighter = combatant_from_character(
            create_character(_fighter_request(), REGISTRY),
            REGISTRY, (4, 5), "patrons")
        rogue = combatant_from_character(
            create_character(_rogue_request(1), REGISTRY),
            REGISTRY, (6, 5), "patrons")
        goblin = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (5, 5), "enemies")
        grid = Grid(width=10, height=10)
        grid.place(fighter)
        grid.place(rogue)
        grid.place(goblin)
        enc = Encounter.begin(grid, [fighter, rogue, goblin], Roller(seed=1))
        # Even though they flank, ranged attacks don't get the bonus.
        bonus = _flanking_attack_bonus(
            fighter, goblin, grid, enc, is_ranged=True,
        )
        self.assertEqual(bonus, 0)


if __name__ == "__main__":
    unittest.main()
