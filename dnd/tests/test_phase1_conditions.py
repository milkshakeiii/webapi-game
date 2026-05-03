"""Tests for Phase 1 condition plumbing — fear chain, sickened,
dazzled, entangled, dazed/nauseated/fascinated action restrictions,
energy drain, blinded/deafened/petrified PARTIAL → IMPL."""

from __future__ import annotations

import unittest

from dnd.engine.combatant import combatant_from_monster
from dnd.engine.content import default_registry
from dnd.engine.encounter import (
    Turn,
    TurnValidationError,
    validate_turn,
)
from dnd.engine.grid import Grid
from dnd.engine.modifiers import compute as _compute


REGISTRY = default_registry()


def _g():
    return combatant_from_monster(REGISTRY.get_monster("orc"), (0, 0), "x")


def _attack_total(c):
    return _compute(0, c.modifiers.for_target("attack"))


def _save_total(c, kind):
    return _compute(0, c.modifiers.for_target(f"{kind}_save"))


def _skill_check_total(c):
    return _compute(0, c.modifiers.for_target("skill_check"))


# ---------------------------------------------------------------------------
# Fear chain
# ---------------------------------------------------------------------------


class TestFearChain(unittest.TestCase):
    def test_shaken_applies_minus_two_morale_chain(self):
        c = _g()
        atk_before = _attack_total(c)
        will_before = _save_total(c, "will")
        c.add_condition("shaken")
        self.assertEqual(_attack_total(c), atk_before - 2)
        self.assertEqual(_save_total(c, "will"), will_before - 2)
        self.assertEqual(_save_total(c, "fort"), -2)
        self.assertEqual(_save_total(c, "ref"), -2)
        self.assertEqual(_skill_check_total(c), -2)

    def test_shaken_skill_total_includes_skill_check_penalty(self):
        c = _g()
        before = c.skill_total("intimidate")
        c.add_condition("shaken")
        self.assertEqual(c.skill_total("intimidate"), before - 2)

    def test_remove_shaken_clears_modifiers(self):
        c = _g()
        atk_before = _attack_total(c)
        c.add_condition("shaken")
        c.remove_condition("shaken")
        self.assertEqual(_attack_total(c), atk_before)

    def test_frightened_supersedes_shaken(self):
        c = _g()
        c.add_condition("shaken")
        self.assertIn("shaken", c.conditions)
        c.add_condition("frightened")
        self.assertNotIn("shaken", c.conditions)
        self.assertIn("frightened", c.conditions)
        # Penalty stays at -2 (not -4).
        self.assertEqual(_attack_total(c), -2)

    def test_panicked_supersedes_frightened(self):
        c = _g()
        c.add_condition("frightened")
        c.add_condition("panicked")
        self.assertNotIn("frightened", c.conditions)
        self.assertIn("panicked", c.conditions)

    def test_shaken_blocked_when_frightened_present(self):
        c = _g()
        c.add_condition("frightened")
        ok = c.add_condition("shaken")
        self.assertFalse(ok)
        self.assertNotIn("shaken", c.conditions)

    def test_panicked_blocks_attack_actions(self):
        c = _g()
        grid = Grid(width=10, height=10)
        grid.place(c)
        c.add_condition("panicked")
        attack_turn = Turn(standard={"type": "attack",
                                     "args": {"target": "enemy.closest"}})
        with self.assertRaises(TurnValidationError):
            validate_turn(attack_turn, c, grid)

    def test_panicked_allows_movement(self):
        c = _g()
        grid = Grid(width=10, height=10)
        grid.place(c)
        c.add_condition("panicked")
        flee_turn = Turn(move={"type": "move_to", "target": (5, 5)})
        validate_turn(flee_turn, c, grid)  # no raise


# ---------------------------------------------------------------------------
# Sickened
# ---------------------------------------------------------------------------


class TestSickened(unittest.TestCase):
    def test_applies_attack_damage_save_skill_penalties(self):
        c = _g()
        c.add_condition("sickened")
        self.assertEqual(_attack_total(c), -2)
        self.assertEqual(_compute(0, c.modifiers.for_target("damage")), -2)
        self.assertEqual(_save_total(c, "fort"), -2)
        self.assertEqual(_save_total(c, "ref"), -2)
        self.assertEqual(_save_total(c, "will"), -2)
        self.assertEqual(_skill_check_total(c), -2)

    def test_remove_clears(self):
        c = _g()
        c.add_condition("sickened")
        c.remove_condition("sickened")
        self.assertEqual(_attack_total(c), 0)


# ---------------------------------------------------------------------------
# Dazzled
# ---------------------------------------------------------------------------


class TestDazzled(unittest.TestCase):
    def test_applies_minus_one_attack_and_perception(self):
        c = _g()
        before_perc = c.skill_total("perception")
        c.add_condition("dazzled")
        self.assertEqual(_attack_total(c), -1)
        self.assertEqual(c.skill_total("perception"), before_perc - 1)


# ---------------------------------------------------------------------------
# Entangled
# ---------------------------------------------------------------------------


class TestEntangled(unittest.TestCase):
    def test_applies_attack_dex_speed(self):
        c = _g()
        speed_before = c.speed
        c.add_condition("entangled")
        self.assertEqual(_attack_total(c), -2)
        self.assertEqual(_compute(0, c.modifiers.for_target("ability:dex")),
                         -4 + sum(m.value for m in c.modifiers.for_target(
                             "ability:dex") if m.source != "entangled"))
        self.assertEqual(c.speed, speed_before // 2)

    def test_remove_restores_speed(self):
        c = _g()
        speed_before = c.speed
        c.add_condition("entangled")
        c.remove_condition("entangled")
        self.assertEqual(c.speed, speed_before)

    def test_blocks_charge_and_run(self):
        c = _g()
        grid = Grid(width=20, height=20)
        grid.place(c)
        c.add_condition("entangled")
        charge = Turn(full_round={"composite": "charge",
                                  "args": {"target": "enemy.closest"}})
        with self.assertRaises(TurnValidationError):
            validate_turn(charge, c, grid)


# ---------------------------------------------------------------------------
# Dazed, nauseated, fascinated
# ---------------------------------------------------------------------------


class TestActionRestrictedConditions(unittest.TestCase):
    def test_dazed_blocks_all_actions(self):
        c = _g()
        grid = Grid(width=10, height=10)
        grid.place(c)
        c.add_condition("dazed")
        for slot in ("standard", "move", "swift", "five_foot_step"):
            kwargs = {slot: ((1, 0) if slot == "five_foot_step"
                             else {"type": "attack",
                                   "args": {"target": "enemy.closest"}})}
            t = Turn(**kwargs)
            with self.assertRaises(TurnValidationError):
                validate_turn(t, c, grid)

    def test_nauseated_allows_only_move(self):
        c = _g()
        grid = Grid(width=10, height=10)
        grid.place(c)
        c.add_condition("nauseated")
        # Attack standard: blocked.
        std = Turn(standard={"type": "attack",
                             "args": {"target": "enemy.closest"}})
        with self.assertRaises(TurnValidationError):
            validate_turn(std, c, grid)
        # Move alone: allowed.
        mv = Turn(move={"type": "move_to", "target": (5, 5)})
        validate_turn(mv, c, grid)

    def test_fascinated_blocks_actions_and_perception_penalty(self):
        c = _g()
        grid = Grid(width=10, height=10)
        grid.place(c)
        before_perc = c.skill_total("perception")
        c.add_condition("fascinated")
        self.assertEqual(c.skill_total("perception"), before_perc - 4)
        attack_turn = Turn(standard={"type": "attack",
                                     "args": {"target": "enemy.closest"}})
        with self.assertRaises(TurnValidationError):
            validate_turn(attack_turn, c, grid)


# ---------------------------------------------------------------------------
# Energy drain
# ---------------------------------------------------------------------------


class TestEnergyDrain(unittest.TestCase):
    def test_one_negative_level_applies_minus_one_chain(self):
        c = _g()
        atk_before = _attack_total(c)
        hp_before = c.max_hp
        c.add_condition("energy_drained")
        self.assertEqual(c.negative_levels, 1)
        self.assertEqual(_attack_total(c), atk_before - 1)
        self.assertEqual(_save_total(c, "fort"), -1)
        self.assertEqual(_save_total(c, "ref"), -1)
        self.assertEqual(_save_total(c, "will"), -1)
        self.assertEqual(c.max_hp, hp_before - 5)

    def test_negative_levels_stack(self):
        c = _g()
        c.add_condition("energy_drained")
        c.add_condition("energy_drained")
        self.assertEqual(c.negative_levels, 2)
        self.assertEqual(_attack_total(c), -2)

    def test_remove_one_negative_level_at_a_time(self):
        c = _g()
        c.add_condition("energy_drained")
        c.add_condition("energy_drained")
        c.remove_negative_levels(1)
        self.assertEqual(c.negative_levels, 1)
        self.assertEqual(_attack_total(c), -1)
        self.assertIn("energy_drained", c.conditions)
        c.remove_negative_levels(1)
        self.assertEqual(c.negative_levels, 0)
        self.assertNotIn("energy_drained", c.conditions)

    def test_remove_condition_clears_all_levels(self):
        c = _g()
        c.add_condition("energy_drained")
        c.add_condition("energy_drained")
        c.add_condition("energy_drained")
        c.remove_condition("energy_drained")
        self.assertEqual(c.negative_levels, 0)
        self.assertEqual(_attack_total(c), 0)

    def test_undead_immune_to_energy_drain(self):
        sk = combatant_from_monster(REGISTRY.get_monster("skeleton"),
                                    (0, 0), "x")
        result = sk.add_condition("energy_drained")
        self.assertFalse(result)
        self.assertEqual(sk.negative_levels, 0)


# ---------------------------------------------------------------------------
# Blinded (PARTIAL → IMPL)
# ---------------------------------------------------------------------------


class TestBlindedFull(unittest.TestCase):
    def test_minus_two_ac(self):
        c = _g()
        ac_before = c.ac()
        c.add_condition("blinded")
        self.assertEqual(c.ac(), ac_before - 2)

    def test_half_speed(self):
        c = _g()
        speed_before = c.speed
        c.add_condition("blinded")
        self.assertEqual(c.speed, speed_before // 2)

    def test_minus_four_dex_skill(self):
        c = _g()
        before = c.skill_total("stealth")
        c.add_condition("blinded")
        self.assertEqual(c.skill_total("stealth"), before - 4)

    def test_remove_restores(self):
        c = _g()
        ac_before = c.ac()
        speed_before = c.speed
        c.add_condition("blinded")
        c.remove_condition("blinded")
        self.assertEqual(c.ac(), ac_before)
        self.assertEqual(c.speed, speed_before)


# ---------------------------------------------------------------------------
# Deafened (PARTIAL → IMPL): -4 init.
# ---------------------------------------------------------------------------


class TestDeafenedInit(unittest.TestCase):
    def test_minus_four_init(self):
        c = _g()
        before = c.initiative_modifier()
        c.add_condition("deafened")
        self.assertEqual(c.initiative_modifier(), before - 4)


# ---------------------------------------------------------------------------
# Helpless cascade for sleeping/paralyzed/petrified
# ---------------------------------------------------------------------------


class TestHelplessCascade(unittest.TestCase):
    def test_sleeping_implies_helpless(self):
        c = _g()
        c.add_condition("sleeping")
        self.assertIn("helpless", c.conditions)

    def test_paralyzed_implies_helpless(self):
        c = _g()
        c.add_condition("paralyzed")
        self.assertIn("helpless", c.conditions)

    def test_petrified_implies_helpless(self):
        c = _g()
        c.add_condition("petrified")
        self.assertIn("helpless", c.conditions)

    def test_remove_paralyzed_drops_implied_helpless(self):
        c = _g()
        c.add_condition("paralyzed")
        c.remove_condition("paralyzed")
        self.assertNotIn("helpless", c.conditions)

    def test_double_implication_keeps_helpless(self):
        # paralyzed + sleeping both imply helpless. Removing one should
        # leave helpless in place (the other is still active).
        c = _g()
        c.add_condition("paralyzed")
        c.add_condition("sleeping")
        c.remove_condition("paralyzed")
        self.assertIn("helpless", c.conditions)


if __name__ == "__main__":
    unittest.main()
