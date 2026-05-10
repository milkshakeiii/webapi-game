"""Tests for Phase 4.4 monk: unarmed-strike auto-feat + damage
scaling, and flurry of blows.

RAW (Foundry pack ``class-abilities.md``):

- Unarmed Strike: Improved Unarmed Strike auto-bonus at L1; unarmed
  damage scales by monk level + size (Medium L1 = 1d6).
- Flurry of Blows: full-attack only; one extra attack at -2 to all
  attack rolls; BAB from monk class levels equal to monk level for
  these attacks; full Strength on damage; unarmed-strike-only for v1.
"""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import (
    _monk_unarmed_damage_dice,
    combatant_from_character,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid


REGISTRY = default_registry()


def _monk(name: str = "Tian", **overrides) -> object:
    # Point-buy 20: str 14 (5) + dex 14 (5) + con 14 (5) + int 10 (0)
    # + wis 14 (5) + cha 10 (0) = 20. Human +2 to str → 16.
    body = {
        "name": name, "race": "human", "class": "monk",
        "alignment": "lawful_neutral",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 14, "dex": 14, "con": 14,
                       "int": 10, "wis": 14, "cha": 10}},
        "free_ability_choice": "str",
        "feats": ["dodge", "iron_will"],
        "skill_ranks": {"acrobatics": 1, "perception": 1},
        "bonus_languages": [],
        "class_choices": {"monk_bonus_feat": "combat_reflexes"},
    }
    body.update(overrides)
    return create_character(CharacterRequest.from_dict(body), REGISTRY)


# ---------------------------------------------------------------------------
# Damage table — direct unit test of the scaling helper
# ---------------------------------------------------------------------------


class TestMonkUnarmedDamageTable(unittest.TestCase):
    """Verify the table exactly matches the Foundry RAW (Medium row
    on Table: Monk, Small/Large from Table: Small or Large Monk
    Unarmed Damage)."""

    def test_medium_progression(self):
        cases = [
            (1,  "1d6"), (3,  "1d6"),
            (4,  "1d8"), (7,  "1d8"),
            (8,  "1d10"), (11, "1d10"),
            (12, "2d6"), (15, "2d6"),
            (16, "2d8"), (19, "2d8"),
            (20, "2d10"),
        ]
        for level, expected in cases:
            with self.subTest(level=level):
                self.assertEqual(
                    _monk_unarmed_damage_dice(level, "medium"),
                    expected,
                )

    def test_small_progression(self):
        # Small monk drops one die-step at every band.
        self.assertEqual(_monk_unarmed_damage_dice(1, "small"), "1d4")
        self.assertEqual(_monk_unarmed_damage_dice(4, "small"), "1d6")
        self.assertEqual(_monk_unarmed_damage_dice(8, "small"), "1d8")
        self.assertEqual(_monk_unarmed_damage_dice(20, "small"), "2d8")

    def test_large_progression(self):
        # Large monk gains one die-step at every band.
        self.assertEqual(_monk_unarmed_damage_dice(1, "large"), "1d8")
        self.assertEqual(_monk_unarmed_damage_dice(4, "large"), "2d6")
        self.assertEqual(_monk_unarmed_damage_dice(8, "large"), "2d8")
        self.assertEqual(_monk_unarmed_damage_dice(20, "large"), "4d8")


# ---------------------------------------------------------------------------
# Auto-feat + applied attack option
# ---------------------------------------------------------------------------


class TestMonkUnarmedStrikeAutoFeat(unittest.TestCase):
    def test_l1_monk_has_improved_unarmed_strike(self):
        char = _monk()
        # The auto-feat is in Character.feats (the canonical post-
        # creation list of all feats).
        self.assertIn("improved_unarmed_strike", char.feats)

    def test_l1_monk_does_not_get_iuS_via_menu(self):
        # RAW: Improved Unarmed Strike is not in the L1 bonus-feat menu;
        # pickers should be rejected if they try to take it via the menu.
        body = {
            "name": "Tian", "race": "human", "class": "monk",
            "alignment": "lawful_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 14, "con": 14,
                           "int": 10, "wis": 14, "cha": 10}},
            "free_ability_choice": "str",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"acrobatics": 1, "perception": 1},
            "bonus_languages": [],
            "class_choices": {"monk_bonus_feat": "improved_unarmed_strike"},
        }
        from dnd.engine.characters import CharacterCreationError
        with self.assertRaises(CharacterCreationError):
            create_character(CharacterRequest.from_dict(body), REGISTRY)


class TestMonkUnarmedAttackOption(unittest.TestCase):
    def test_l1_medium_monk_unarmed_does_1d6(self):
        char = _monk()
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        primary = c.attack_options[0]
        self.assertEqual(primary["weapon_id"], "unarmed_strike")
        self.assertEqual(primary["damage"], "1d6")

    def test_l1_monk_full_str_on_unarmed_damage(self):
        # Monks apply full Str to unarmed damage (RAW). Str 14 + human
        # +2 → 16, +3 mod.
        char = _monk()
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        primary = c.attack_options[0]
        self.assertEqual(primary["damage_bonus"], 3)

    def test_non_monk_unarmed_strike_not_scaled(self):
        # A non-monk wielding unarmed_strike (e.g., a fighter) gets the
        # base 1d3 — the monk scaling is class-feature-gated.
        body = {
            "name": "Bob", "race": "human", "class": "fighter",
            "alignment": "true_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 14, "con": 14,
                           "int": 10, "wis": 14, "cha": 10}},
            "free_ability_choice": "str",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"climb": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "weapon_focus_longsword"},
            "equipment": {"weapon": "unarmed_strike", "armor": "none"},
        }
        char = create_character(CharacterRequest.from_dict(body), REGISTRY)
        c = combatant_from_character(char, REGISTRY, (0, 0), "x")
        primary = c.attack_options[0]
        self.assertEqual(primary["weapon_id"], "unarmed_strike")
        self.assertEqual(primary["damage"], "1d3")


# ---------------------------------------------------------------------------
# Flurry of Blows
# ---------------------------------------------------------------------------


class TestFlurryOfBlows(unittest.TestCase):
    """RAW (Foundry pack ``Flurry of Blows``):

    - Full-attack action only.
    - One additional attack at -2 penalty on all attack rolls (TWF-
      like) at L1.
    - Monk's BAB from monk class levels equals his monk level for
      these attacks. (L1: BAB-for-flurry = 1, even though normal
      monk BAB is 0.)
    - Full Strength bonus on damage rolls for all flurry attacks.
    - Cannot use any weapon other than unarmed strike or a special
      monk weapon. (v1: unarmed-only.)
    """

    def _setup_combat(self, monk_str_score: int = 14):
        # Build a monk vs. a goblin in melee range and a clean grid.
        body = {
            "name": "Tian", "race": "human", "class": "monk",
            "alignment": "lawful_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": monk_str_score, "dex": 14, "con": 14,
                           "int": 10, "wis": 14, "cha": 10}},
            "free_ability_choice": "str",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"acrobatics": 1, "perception": 1},
            "bonus_languages": [],
            "class_choices": {"monk_bonus_feat": "combat_reflexes"},
        }
        char = create_character(CharacterRequest.from_dict(body), REGISTRY)
        monk = combatant_from_character(char, REGISTRY, (5, 5), "x")
        target = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (6, 5), "y",
        )
        # Make target effectively unkillable so we can count attacks
        # without tripping early-stop.
        target.max_hp = 9999
        target.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(monk)
        grid.place(target)
        enc = Encounter.begin(grid, [monk, target], Roller(seed=1))
        return monk, target, enc, grid

    def _run_flurry(self, monk, target, enc, grid):
        from dnd.engine.dsl import TurnIntent
        from dnd.engine.turn_executor import execute_turn
        do = {"composite": "full_attack",
              "args": {"target": target, "options": {"flurry": True}}}
        intent = TurnIntent(rule_index=0, do=do, namespace={})
        return execute_turn(monk, intent, enc, grid, Roller(seed=1))

    def test_l1_monk_flurry_makes_two_attacks(self):
        # L1 flurry = 1 normal + 1 extra = 2 unarmed strikes.
        monk, target, enc, grid = self._setup_combat()
        result = self._run_flurry(monk, target, enc, grid)
        attack_events = [e for e in result.events
                         if e.kind.startswith("full_attack_")]
        self.assertEqual(
            len(attack_events), 2,
            f"expected 2 attacks, got {len(attack_events)}: {result.events}",
        )

    def test_flurry_uses_unarmed_strike_only(self):
        monk, target, enc, grid = self._setup_combat()
        result = self._run_flurry(monk, target, enc, grid)
        for e in result.events:
            if e.kind.startswith("full_attack_"):
                # Each attack event references the weapon name.
                self.assertEqual(
                    e.detail.get("weapon"), "Unarmed Strike",
                    f"flurry attack used wrong weapon: {e.detail}",
                )

    def test_flurry_at_l1_uses_monk_level_as_bab(self):
        # At L1, the monk's normal BAB is 0. Flurry RAW: BAB equals
        # monk level for these attacks → +1. With Str 16 (point-buy
        # 14 + human +2) → +3 mod, and the -2 TWF penalty: net to-hit
        # = 1 (flurry BAB) + 3 (Str) - 2 (TWF) = +2 per attack.
        monk, target, enc, grid = self._setup_combat(monk_str_score=14)
        result = self._run_flurry(monk, target, enc, grid)
        # Pull the to-hit bonus from each attack's trace string. The
        # combat resolver formats "d20=N + bonus = total".
        import re
        bonuses: list[int] = []
        for e in result.events:
            if not e.kind.startswith("full_attack_"):
                continue
            trace = e.detail.get("trace") or []
            if trace:
                m = re.search(r"d20=\d+ \+ (-?\d+)", trace[0])
                if m:
                    bonuses.append(int(m.group(1)))
        self.assertEqual(
            bonuses, [2, 2],
            f"expected both attacks at +2; got {bonuses}",
        )

    def test_flurry_full_str_on_all_damage(self):
        # RAW: full Str bonus on damage for ALL flurry attacks (including
        # the "off-hand-style" extra). Str 16 (after human +2) → +3.
        # Both attacks should land with damage bonus +3 reflected in
        # the trace's "bonus=+3" segment.
        monk, target, enc, grid = self._setup_combat(monk_str_score=14)
        result = self._run_flurry(monk, target, enc, grid)
        import re
        damage_bonuses: list[int] = []
        for e in result.events:
            if not e.kind.startswith("full_attack_"):
                continue
            if not e.detail.get("hit"):
                continue
            for line in (e.detail.get("trace") or []):
                m = re.search(r"bonus=\+?(-?\d+)", line)
                if m:
                    damage_bonuses.append(int(m.group(1)))
                    break
        self.assertTrue(
            damage_bonuses,
            "expected at least one hit to verify damage bonus",
        )
        for db in damage_bonuses:
            self.assertEqual(
                db, 3,
                f"damage_bonus should be +3 (full Str on every flurry "
                f"attack); got {db}",
            )

    def test_flurry_without_monk_levels_is_inert(self):
        # A non-monk passing flurry: True should fall through to a
        # normal full-attack (no extra attacks, no -2 penalty).
        body = {
            "name": "Bob", "race": "human", "class": "fighter",
            "alignment": "true_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 14, "con": 14,
                           "int": 10, "wis": 14, "cha": 10}},
            "free_ability_choice": "str",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"climb": 1},
            "bonus_languages": [],
            "class_choices": {"fighter_bonus_feat": "weapon_focus_longsword"},
            "equipment": {"weapon": "unarmed_strike", "armor": "none"},
        }
        char = create_character(CharacterRequest.from_dict(body), REGISTRY)
        fighter = combatant_from_character(char, REGISTRY, (5, 5), "x")
        target = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (6, 5), "y",
        )
        target.max_hp = 9999
        target.current_hp = 9999
        grid = Grid(width=12, height=12)
        grid.place(fighter)
        grid.place(target)
        enc = Encounter.begin(grid, [fighter, target], Roller(seed=1))
        from dnd.engine.dsl import TurnIntent
        from dnd.engine.turn_executor import execute_turn
        do = {"composite": "full_attack",
              "args": {"target": target, "options": {"flurry": True}}}
        intent = TurnIntent(rule_index=0, do=do, namespace={})
        result = execute_turn(fighter, intent, enc, grid, Roller(seed=1))
        attack_events = [e for e in result.events
                         if e.kind.startswith("full_attack_")]
        self.assertEqual(
            len(attack_events), 1,
            "non-monk should not get the flurry extra attack",
        )


if __name__ == "__main__":
    unittest.main()
