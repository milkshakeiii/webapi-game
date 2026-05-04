"""Tests for audit batch A — six one-line/short corrections from the
RAW-vs-engine audit:

1. Defensive cast DC = 15 + 2L (was 15 + L).
2. Grapple pin DC has no +5 difficulty (was CMB - 5 vs CMD).
3. Draw weapon does not provoke AoO (RAW Action Table).
4. Combat maneuvers honor nat 1 / nat 20 auto-fail / auto-succeed.
5. CMD pulls deflection/dodge/etc. from AC modifiers; flat-footed
   denies Dex bonus and dodge bonuses to CMD.
6. Concentration vs. grappler uses the grappler's actual CMB, not +4.
"""

from __future__ import annotations

import unittest

from dnd.engine.combatant import (
    Combatant,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.modifiers import mod
from dnd.engine.turn_executor import (
    _do_cast,
    _do_grapple_pin,
    _do_move_action,
    _resolve_maneuver,
)


REGISTRY = default_registry()


def _orc(pos=(5, 5), team="x"):
    return combatant_from_monster(REGISTRY.get_monster("orc"), pos, team)


# ---------------------------------------------------------------------------
# 1. Defensive cast DC = 15 + 2 * L
# ---------------------------------------------------------------------------


class TestDefensiveCastDC(unittest.TestCase):
    def test_third_level_spell_dc_is_21(self):
        """Cast 3rd-level spell defensively while threatened; DC must
        be 15 + 2*3 = 21, not 15 + 3 = 18."""
        from dnd.engine.combatant import combatant_from_character
        from dnd.engine.characters import CharacterRequest, create_character

        req = CharacterRequest.from_dict({
            "name": "Caster", "race": "human", "class": "cleric",
            "alignment": "neutral_good",
            "ability_scores": {
                "method": "point_buy_20",
                "scores": {"str": 10, "dex": 10, "con": 14,
                           "int": 10, "wis": 16, "cha": 14},
            },
            "free_ability_choice": "wis",
            "feats": ["iron_will", "great_fortitude"],
            "skill_ranks": {"heal": 1, "knowledge_religion": 1},
            "bonus_languages": [],
        })
        char = create_character(req, REGISTRY)
        c = combatant_from_character(char, REGISTRY, (5, 5), "x")
        c.casting_type = "prepared"
        c.prepared_spells = {3: ["dispel_magic"]}
        c.castable_spells = {"dispel_magic"}
        c.resources["spell_slot_3"] = 1

        threatener = _orc((6, 5), "y")
        grid = Grid(width=10, height=10)
        grid.place(c)
        grid.place(threatener)
        enc = Encounter.begin(grid, [c, threatener], Roller(seed=1))

        events: list = []
        # Force a low concentration roll by using a known seed that
        # rolls 1; we only care about the DC value reported in the
        # event detail.
        _do_cast(c, {"spell": "dispel_magic", "spell_level": 3,
                     "target": threatener, "defensive": True},
                 enc, grid, Roller(seed=1), {}, events)

        cast_failed = [e for e in events if e.kind == "cast_failed"
                       and e.detail.get("reason") == "concentration_failed"]
        if cast_failed:
            dc = cast_failed[0].detail["concentration_check"]["dc"]
            self.assertEqual(dc, 21,
                             "RAW: defensive concentration DC = 15 + 2L; "
                             f"3rd-level spell expects 21, got {dc}")
            return
        # If the check passed, scan for the DC in any cast_attempt detail.
        # As a fallback, try all events with a concentration_check field.
        for e in events:
            check = e.detail.get("concentration_check") if e.detail else None
            if check and "dc" in check:
                self.assertEqual(check["dc"], 21)
                return
        self.fail(f"no concentration_check DC observed in {[e.kind for e in events]}")


# ---------------------------------------------------------------------------
# 2. Pin DC: no -5 / +5 difficulty modifier
# ---------------------------------------------------------------------------


class TestGrapplePinNoExtraDC(unittest.TestCase):
    def test_pin_uses_raw_cmb_vs_cmd(self):
        """A pin maintain check should be a regular CMB vs CMD roll
        (no +5 DC). With actor cmb 4 and target cmd 14, success
        requires natural 10+; with the old -5 difficulty it would
        have required natural 15+."""
        actor = _orc((5, 5), "x")
        target = _orc((6, 5), "y")
        actor.grappling_target_id = target.id
        actor.add_condition("grappled")
        target.add_condition("grappled")
        target.grappled_by_id = actor.id

        grid = Grid(width=10, height=10)
        grid.place(actor)
        grid.place(target)
        enc = Encounter.begin(grid, [actor, target], Roller(seed=1))

        # Find a seed that rolls 12 on the d20 (12 + 4 cmb = 16 >= 14).
        # With the old formula (cmb 4 - 5 = -1), 12 + -1 = 11 < 14 — fail.
        # We just need ANY seed where the pin succeeds with the new
        # formula but would have failed with the old.
        for seed in range(1, 100):
            actor_copy = _orc((5, 5), "x")
            target_copy = _orc((6, 5), "y")
            actor_copy.grappling_target_id = target_copy.id
            target_copy.grappled_by_id = actor_copy.id
            actor_copy.add_condition("grappled")
            target_copy.add_condition("grappled")
            grid_c = Grid(width=10, height=10)
            grid_c.place(actor_copy)
            grid_c.place(target_copy)
            enc_c = Encounter.begin(grid_c, [actor_copy, target_copy],
                                    Roller(seed=seed))
            events: list = []
            _do_grapple_pin(actor_copy, {}, enc_c, grid_c,
                            Roller(seed=seed), {}, events)
            pin = [e for e in events if e.kind == "grapple_pin"][0]
            nat = pin.detail.get("natural")
            passed = pin.detail.get("passed")
            # Verify: passed iff nat + cmb >= cmd.
            cmb = actor_copy.cmb()
            cmd_val = target_copy.cmd(context={"maneuver": "grapple"})
            expected_passed = (nat + cmb >= cmd_val) or nat == 20
            if nat == 1:
                expected_passed = False
            self.assertEqual(passed, expected_passed,
                             f"seed={seed}: nat={nat}, cmb={cmb}, "
                             f"cmd={cmd_val}, pin formula off")


# ---------------------------------------------------------------------------
# 3. Draw weapon does not provoke
# ---------------------------------------------------------------------------


class TestDrawWeaponNoAoO(unittest.TestCase):
    def test_draw_weapon_in_threatened_square_does_not_provoke(self):
        """RAW: drawing a weapon never provokes (Action Table footnote
        only adjusts the action cost from move to free at BAB +1)."""
        actor = _orc((5, 5), "x")
        actor.bases["bab"] = 0  # below the +1 threshold
        threatener = _orc((6, 5), "y")  # adjacent, threatens

        grid = Grid(width=10, height=10)
        grid.place(actor)
        grid.place(threatener)
        enc = Encounter.begin(grid, [actor, threatener], Roller(seed=1))

        events: list = []
        _do_move_action(actor,
                        {"type": "draw_weapon", "weapon": "longsword"},
                        enc, grid, {}, events)
        kinds = [e.kind for e in events]
        self.assertNotIn("aoo", kinds,
                         f"draw_weapon should not provoke; got {kinds}")
        self.assertIn("draw_weapon", kinds)


# ---------------------------------------------------------------------------
# 4. Combat maneuver nat 1 / nat 20
# ---------------------------------------------------------------------------


class TestManeuverNat1And20(unittest.TestCase):
    def test_nat_20_succeeds_against_huge_cmd(self):
        """Even when CMB total can't reach CMD, a natural 20 succeeds."""
        actor = _orc((5, 5), "x")
        actor.bases["cmb"] = 0  # bare-bones
        target = _orc((6, 5), "y")
        target.bases["cmd"] = 999  # impossible without nat 20

        grid = Grid(width=10, height=10)
        grid.place(actor)
        grid.place(target)
        enc = Encounter.begin(grid, [actor, target], Roller(seed=1))

        # Find a seed where the d20 rolls 20.
        for seed in range(1, 500):
            r = Roller(seed=seed)
            test_roll = r.roll("1d20").terms[0].rolls[0]
            if test_roll == 20:
                # Now run the maneuver with the same seed.
                passed, nat, total, margin = _resolve_maneuver(
                    actor, target, "trip", Roller(seed=seed),
                )
                self.assertEqual(nat, 20)
                self.assertTrue(passed,
                                f"nat 20 must succeed; total={total}, "
                                f"cmd={target.cmd()}")
                return
        self.fail("no seed rolled a nat 20 in 1..499")

    def test_nat_1_fails_against_trivial_cmd(self):
        """Even when CMB easily clears CMD, a natural 1 fails."""
        actor = _orc((5, 5), "x")
        actor.bases["cmb"] = 100  # auto-clear
        target = _orc((6, 5), "y")
        target.bases["cmd"] = 5

        grid = Grid(width=10, height=10)
        grid.place(actor)
        grid.place(target)
        enc = Encounter.begin(grid, [actor, target], Roller(seed=1))

        for seed in range(1, 500):
            r = Roller(seed=seed)
            test_roll = r.roll("1d20").terms[0].rolls[0]
            if test_roll == 1:
                passed, nat, total, margin = _resolve_maneuver(
                    actor, target, "trip", Roller(seed=seed),
                )
                self.assertEqual(nat, 1)
                self.assertFalse(passed,
                                 f"nat 1 must fail even at total {total}")
                return
        self.fail("no seed rolled a nat 1 in 1..499")


# ---------------------------------------------------------------------------
# 5. CMD bleeds AC bonus types; flat-footed denies Dex/dodge to CMD
# ---------------------------------------------------------------------------


class TestCmdBleedThroughAndFlatFooted(unittest.TestCase):
    def test_dodge_ac_bonus_increases_cmd(self):
        c = _orc()
        before = c.cmd()
        c.modifiers.add(mod(2, "dodge", "ac", "test_dodge"))
        self.assertEqual(c.cmd(), before + 2)

    def test_deflection_ac_bonus_increases_cmd(self):
        c = _orc()
        before = c.cmd()
        c.modifiers.add(mod(2, "deflection", "ac", "test_ring"))
        self.assertEqual(c.cmd(), before + 2)

    def test_armor_ac_bonus_does_not_bleed_to_cmd(self):
        """Armor / shield / natural bonuses to AC explicitly do NOT
        contribute to CMD."""
        c = _orc()
        before = c.cmd()
        c.modifiers.add(mod(5, "armor", "ac", "test_armor"))
        c.modifiers.add(mod(3, "shield", "ac", "test_shield"))
        c.modifiers.add(mod(4, "natural", "ac", "test_amulet"))
        self.assertEqual(c.cmd(), before)

    def test_flat_footed_denies_dex_to_cmd(self):
        """Flat-footed creature loses its Dex contribution to CMD."""
        # Use a character so Dex modifier is on the modifier list.
        from dnd.engine.combatant import combatant_from_character
        from dnd.engine.characters import CharacterRequest, create_character
        req = CharacterRequest.from_dict({
            "name": "Tum", "race": "human", "class": "rogue",
            "alignment": "chaotic_neutral",
            "ability_scores": {
                "method": "point_buy_20",
                "scores": {"str": 10, "dex": 16, "con": 14,
                           "int": 13, "wis": 10, "cha": 12},
            },
            "free_ability_choice": "dex",
            "feats": ["weapon_finesse", "iron_will"],
            "skill_ranks": {"acrobatics": 1, "stealth": 1,
                            "perception": 1, "disable_device": 1,
                            "sleight_of_hand": 1, "bluff": 1,
                            "diplomacy": 1, "knowledge_local": 1},
            "bonus_languages": [],
        })
        char = create_character(req, REGISTRY)
        c = combatant_from_character(char, REGISTRY, (5, 5), "x")
        normal_cmd = c.cmd()
        c.add_condition("flat_footed")
        flat_cmd = c.cmd()
        # Dex 16 base + 2 racial (human +2 to dex) = 18 -> mod 4.
        self.assertEqual(normal_cmd - flat_cmd, 4,
                         f"flat-footed should remove Dex (4) from CMD; "
                         f"got delta {normal_cmd - flat_cmd}")

    def test_flat_footed_denies_dodge_bonus_to_cmd(self):
        c = _orc()
        c.modifiers.add(mod(3, "dodge", "ac", "test_dodge"))
        normal_cmd = c.cmd()
        c.add_condition("flat_footed")
        flat_cmd = c.cmd()
        self.assertEqual(normal_cmd - flat_cmd, 3,
                         "flat-footed should drop dodge from CMD too")


# ---------------------------------------------------------------------------
# 6. Concentration DC vs grappler uses real CMB
# ---------------------------------------------------------------------------


class TestGrappledConcentrationUsesRealCMB(unittest.TestCase):
    def test_grappler_with_high_cmb_raises_dc(self):
        """A high-CMB grappler makes concentration much harder than the
        old hardcoded +4 stand-in."""
        from dnd.engine.combatant import combatant_from_character
        from dnd.engine.characters import CharacterRequest, create_character

        req = CharacterRequest.from_dict({
            "name": "Caster", "race": "human", "class": "cleric",
            "alignment": "neutral_good",
            "ability_scores": {
                "method": "point_buy_20",
                "scores": {"str": 10, "dex": 10, "con": 14,
                           "int": 10, "wis": 16, "cha": 14},
            },
            "free_ability_choice": "wis",
            "feats": ["iron_will", "great_fortitude"],
            "skill_ranks": {"heal": 1, "knowledge_religion": 1},
            "bonus_languages": [],
        })
        char = create_character(req, REGISTRY)
        caster = combatant_from_character(char, REGISTRY, (5, 5), "x")
        caster.casting_type = "prepared"
        caster.prepared_spells = {1: ["bless"]}
        caster.castable_spells = {"bless"}
        caster.resources["spell_slot_1"] = 1

        # Grappler with CMB 15 — much higher than old +4 stand-in.
        grappler = _orc((6, 5), "y")
        grappler.bases["cmb"] = 15
        caster.add_condition("grappled")
        caster.grappled_by_id = grappler.id
        grappler.add_condition("grappled")
        grappler.grappling_target_id = caster.id

        grid = Grid(width=10, height=10)
        grid.place(caster)
        grid.place(grappler)
        enc = Encounter.begin(grid, [caster, grappler], Roller(seed=1))

        # Force the cast to fail concentration so we can read the DC.
        events: list = []
        _do_cast(caster, {"spell": "bless", "spell_level": 1,
                          "target": caster, "defensive": False},
                 enc, grid, Roller(seed=1), {}, events)

        # Find the somatic_grappled_concentration_failed event (or any
        # cast_failed with concentration_check.dc).
        for e in events:
            check = e.detail.get("concentration_check") if e.detail else None
            if check and "dc" in check:
                # DC = 10 + grappler.cmb (15) + spell_level (1) = 26
                self.assertEqual(check["dc"], 26,
                                 f"DC should be 10 + 15 + 1 = 26, "
                                 f"got {check['dc']}")
                return
        # If concentration didn't fail, the test still asserts via the
        # known DC formula by re-running with a guaranteed-low roll.
        # Try seed range to find a failing one.
        for seed in range(1, 200):
            events = []
            caster.resources["spell_slot_1"] = 1
            _do_cast(caster, {"spell": "bless", "spell_level": 1,
                              "target": caster, "defensive": False},
                     enc, grid, Roller(seed=seed), {}, events)
            for e in events:
                check = e.detail.get("concentration_check") if e.detail else None
                if check and "dc" in check:
                    self.assertEqual(check["dc"], 26)
                    return
        self.fail("no seed in 1..199 surfaced a concentration_check DC")


if __name__ == "__main__":
    unittest.main()
