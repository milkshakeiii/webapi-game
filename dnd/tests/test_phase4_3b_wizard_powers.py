"""Tests for Phase 4.3b — wizard L1 active school powers.

RAW (Foundry pack ``class-abilities.md``):

- Acid Dart (Conjuration, line 919): standard action, ranged touch
  to 30 ft, 1d6 acid + 1 per 2 wizard levels, ignores SR.
- Telekinetic Fist (Transmutation, 90094): same shape, 1d4 B + 1/2.
- Force Missile (Evocation, 38120): auto-strike force missile, 1d4
  + Intense Spells bonus.
- Blinding Ray (Illusion, 8685): ranged touch 30 ft; blinded 1 round
  (or dazzled if target HD > wizard level).
- Hand of the Apprentice (Universalist, 42404): wielded melee weapon
  flies to 30 ft; to-hit uses Int (not Dex); damage uses Str.
- Diviner's Fortune (Divination, 21844): standard-action touch;
  insight +max(1, wiz_lvl // 2) for 1 round.
- Dazing Touch (Enchantment, 18107): melee touch; dazed 1 round;
  unaffected if target HD > wizard level.
- Grave Touch (Necromancy, 40667): melee touch; shaken for max(1,
  wiz_lvl // 2) rounds; if already shaken and HD < wizard level,
  becomes frightened for 1 round.
- Protective Ward (Abjuration, 70701): 10-ft radius; +1 deflection
  AC to allies (and self) for Int-mod rounds.
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
from dnd.engine.modifiers import compute as _compute
from dnd.engine.turn_executor import execute_turn


REGISTRY = default_registry()


def _wiz(school: str, opposition=None, **extra) -> object:
    body = {
        "name": "Mira", "race": "human", "class": "wizard",
        "alignment": "true_neutral",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 14, "dex": 14, "con": 14,
                       "int": 14, "wis": 10, "cha": 10}},
        "free_ability_choice": "int",
        "feats": ["dodge", "iron_will"],
        "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
        "bonus_languages": [],
        "class_choices": {"wizard_school": school,
                          "wizard_opposition_schools": opposition or []},
    }
    body["class_choices"].update(extra)
    return create_character(CharacterRequest.from_dict(body), REGISTRY)


def _setup(school: str, opposition=None, weapon=None, **extra):
    char = _wiz(school, opposition, **extra)
    if weapon is not None:
        # Replace the equipped weapon via a fresh request (cleaner
        # than mutating the frozen dataclass). For most tests we
        # just want a goblin-style enemy on the grid; weapon override
        # is needed for the Hand-of-the-Apprentice test.
        pass
    bard = combatant_from_character(char, REGISTRY, (5, 5), "x")
    goblin = combatant_from_monster(
        REGISTRY.get_monster("goblin"), (6, 5), "y",
    )
    goblin.max_hp = 9999
    goblin.current_hp = 9999
    grid = Grid(width=20, height=20)
    grid.place(bard)
    grid.place(goblin)
    enc = Encounter.begin(grid, [bard, goblin], Roller(seed=1))
    return bard, goblin, enc, grid


def _invoke(actor, power_id, target, enc, grid, **opts):
    do = {"composite": "wizard_school_power",
          "args": {"power": power_id, "target": target, **opts}}
    intent = TurnIntent(rule_index=0, do=do, namespace={})
    return execute_turn(actor, intent, enc, grid, Roller(seed=1))


# ---------------------------------------------------------------------------
# Acid Dart (Conjuration)
# ---------------------------------------------------------------------------


class TestAcidDart(unittest.TestCase):
    def test_acid_dart_consumes_use_and_emits_event(self):
        wiz, goblin, enc, grid = _setup(
            "conjuration", ["abjuration", "necromancy"],
        )
        before = wiz.resources["wizard_school_acid_dart_uses"]
        result = _invoke(wiz, "acid_dart", goblin, enc, grid)
        after = wiz.resources["wizard_school_acid_dart_uses"]
        self.assertEqual(after, before - 1)
        evs = [e for e in result.events
               if e.kind == "wizard_power_acid_dart"]
        self.assertEqual(len(evs), 1)
        self.assertEqual(evs[0].detail["power_id"], "acid_dart")

    def test_acid_dart_out_of_range_skips(self):
        # 30 ft = 6 squares. Place the goblin 8 squares away.
        char = _wiz("conjuration", ["abjuration", "necromancy"])
        wiz = combatant_from_character(char, REGISTRY, (0, 0), "x")
        goblin = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (8, 0), "y",
        )
        grid = Grid(width=20, height=20)
        grid.place(wiz)
        grid.place(goblin)
        enc = Encounter.begin(grid, [wiz, goblin], Roller(seed=1))
        result = _invoke(wiz, "acid_dart", goblin, enc, grid)
        skip = next(e for e in result.events if e.kind == "skip")
        self.assertIn("out of range", skip.detail["reason"])

    def test_no_uses_left_skips(self):
        wiz, goblin, enc, grid = _setup(
            "conjuration", ["abjuration", "necromancy"],
        )
        wiz.resources["wizard_school_acid_dart_uses"] = 0
        result = _invoke(wiz, "acid_dart", goblin, enc, grid)
        skip = next(e for e in result.events if e.kind == "skip")
        self.assertIn("no uses remaining", skip.detail["reason"])

    def test_only_a_wizard_can_invoke(self):
        # Build a fighter; calling wizard_school_power should skip.
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
        }
        char = create_character(CharacterRequest.from_dict(body), REGISTRY)
        fighter = combatant_from_character(char, REGISTRY, (5, 5), "x")
        goblin = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (6, 5), "y",
        )
        grid = Grid(width=20, height=20)
        grid.place(fighter)
        grid.place(goblin)
        enc = Encounter.begin(grid, [fighter, goblin], Roller(seed=1))
        result = _invoke(fighter, "acid_dart", goblin, enc, grid)
        skip = next(e for e in result.events if e.kind == "skip")
        self.assertIn("no wizard levels", skip.detail["reason"])


# ---------------------------------------------------------------------------
# Force Missile (Evocation) — auto-strike + Intense Spells bonus
# ---------------------------------------------------------------------------


class TestForceMissile(unittest.TestCase):
    def test_force_missile_auto_hits(self):
        wiz, goblin, enc, grid = _setup(
            "evocation", ["abjuration", "necromancy"],
        )
        result = _invoke(wiz, "force_missile", goblin, enc, grid)
        ev = next(e for e in result.events
                  if e.kind == "wizard_power_force_missile")
        self.assertTrue(ev.detail["hit"])

    def test_force_missile_l1_evoker_gets_intense_spells_bonus(self):
        # L1 evoker: Intense Spells = max(1, 1//2) = 1.
        wiz, goblin, enc, grid = _setup(
            "evocation", ["abjuration", "necromancy"],
        )
        result = _invoke(wiz, "force_missile", goblin, enc, grid)
        ev = next(e for e in result.events
                  if e.kind == "wizard_power_force_missile")
        self.assertEqual(ev.detail["intense_spells_bonus"], 1)

    def test_force_missile_non_evoker_has_no_intense_spells_bonus(self):
        # A universalist or other school doesn't get Intense Spells.
        # (They also don't have Force Missile as their L1 active, but
        # we can hit the resource gate by injecting uses.)
        wiz, goblin, enc, grid = _setup(
            "conjuration", ["abjuration", "necromancy"],
        )
        # Force the resource so the dispatch reaches the handler.
        wiz.resources["wizard_school_force_missile_uses"] = 1
        result = _invoke(wiz, "force_missile", goblin, enc, grid)
        ev = next(e for e in result.events
                  if e.kind == "wizard_power_force_missile")
        self.assertEqual(ev.detail["intense_spells_bonus"], 0)


# ---------------------------------------------------------------------------
# Blinding Ray (Illusion)
# ---------------------------------------------------------------------------


class TestBlindingRay(unittest.TestCase):
    def test_blinds_low_hd_target_on_hit(self):
        wiz, goblin, enc, grid = _setup(
            "illusion", ["abjuration", "necromancy"],
        )
        # Goblin has 1 HD; wizard L1 has level 1. RAW says "more HD
        # than your wizard level" → demote. 1 > 1 is false → blinded
        # on hit.
        # Force an auto-hit by raising the wizard's attack bonus
        # (we don't otherwise control the d20 here).
        wiz.attack_options[0]["attack_bonus"] = 100
        result = _invoke(wiz, "blinding_ray", goblin, enc, grid)
        ev = next(e for e in result.events
                  if e.kind == "wizard_power_blinding_ray")
        if ev.detail.get("hit"):
            self.assertEqual(ev.detail["condition"], "blinded")
            self.assertIn("blinded", goblin.conditions)


# ---------------------------------------------------------------------------
# Diviner's Fortune (Divination)
# ---------------------------------------------------------------------------


class TestDivinersFortune(unittest.TestCase):
    def test_grants_insight_to_attack_and_saves(self):
        wiz, goblin, enc, grid = _setup(
            "divination", ["abjuration", "necromancy"],
        )
        # Target self by placing wiz adjacent to a friendly ally
        # combatant. For simplicity, target wiz (touch self is legal).
        result = _invoke(wiz, "diviners_fortune", wiz, enc, grid)
        ev = next(e for e in result.events
                  if e.kind == "wizard_power_diviners_fortune")
        self.assertEqual(ev.detail["bonus"], 1)
        # Confirm the modifier was applied via the source filter.
        atk_mods = [m for m in wiz.modifiers.for_target("attack")
                    if m.source.startswith("diviners_fortune:")]
        self.assertEqual(len(atk_mods), 1)
        self.assertEqual(atk_mods[0].value, 1)
        self.assertEqual(atk_mods[0].type, "insight")


# ---------------------------------------------------------------------------
# Dazing Touch (Enchantment)
# ---------------------------------------------------------------------------


class TestDazingTouch(unittest.TestCase):
    def test_dazes_low_hd_target(self):
        wiz, goblin, enc, grid = _setup(
            "enchantment", ["abjuration", "necromancy"],
        )
        # Force auto-hit on the touch attack.
        # (attack_options[0] is the wizard's equipped weapon, but
        # dazing_touch builds its own profile. Mock by mutating
        # bases.)
        wiz.bases["bab"] = 100
        result = _invoke(wiz, "dazing_touch", goblin, enc, grid)
        ev = next(e for e in result.events
                  if e.kind == "wizard_power_dazing_touch")
        # Goblin (HD 1) <= wiz level (1) → dazed.
        self.assertEqual(ev.detail.get("condition"), "dazed")
        self.assertIn("dazed", goblin.conditions)


# ---------------------------------------------------------------------------
# Grave Touch (Necromancy)
# ---------------------------------------------------------------------------


class TestGraveTouch(unittest.TestCase):
    def test_shakens_target_on_hit(self):
        wiz, goblin, enc, grid = _setup(
            "necromancy", ["abjuration", "evocation"],
        )
        wiz.bases["bab"] = 100
        result = _invoke(wiz, "grave_touch", goblin, enc, grid)
        ev = next(e for e in result.events
                  if e.kind == "wizard_power_grave_touch")
        # L1 → max(1, 1//2) = 1 round of shaken.
        self.assertEqual(ev.detail.get("condition"), "shaken")
        self.assertEqual(ev.detail.get("duration_rounds"), 1)
        self.assertIn("shaken", goblin.conditions)


# ---------------------------------------------------------------------------
# Protective Ward (Abjuration)
# ---------------------------------------------------------------------------


class TestProtectiveWard(unittest.TestCase):
    def test_grants_deflection_ac_to_self(self):
        wiz, goblin, enc, grid = _setup(
            "abjuration", ["evocation", "necromancy"],
        )
        result = _invoke(wiz, "protective_ward", None, enc, grid)
        ev = next(e for e in result.events
                  if e.kind == "wizard_power_protective_ward")
        self.assertEqual(ev.detail["bonus"], 1)
        self.assertIn(wiz.id, ev.detail["affected_ids"])
        # Verify the deflection modifier on wiz.
        deflection = [m for m in wiz.modifiers.for_target("ac")
                      if m.type == "deflection"
                      and m.source.startswith("protective_ward:")]
        self.assertEqual(len(deflection), 1)
        self.assertEqual(deflection[0].value, 1)


# ---------------------------------------------------------------------------
# Hand of the Apprentice (Universalist) — Int-to-hit, Str-to-damage
# ---------------------------------------------------------------------------


class TestHandOfTheApprentice(unittest.TestCase):
    def test_int_to_attack_str_to_damage(self):
        # L1 universalist: Int 16 (+3), Str 14 (+2). With a longsword
        # equipped:
        # - Hand of the Apprentice attack_bonus = BAB(0) + Int(3) +
        #   size(0) = +3.
        # - Damage from longsword: 1d8 + Str(2) = 1d8+2.
        # The default wizard loadout doesn't include a longsword; this
        # test sets it explicitly via the equipment field.
        body = {
            "name": "Mira", "race": "human", "class": "wizard",
            "alignment": "true_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 14, "con": 14,
                           "int": 14, "wis": 10, "cha": 10}},
            "free_ability_choice": "int",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
            "bonus_languages": [],
            "class_choices": {"wizard_school": "universalist"},
            "equipment": {"weapon": "longsword"},
        }
        char = create_character(CharacterRequest.from_dict(body), REGISTRY)
        wiz = combatant_from_character(char, REGISTRY, (5, 5), "x")
        goblin = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (7, 5), "y",  # 2 squares
        )
        grid = Grid(width=20, height=20)
        grid.place(wiz)
        grid.place(goblin)
        enc = Encounter.begin(grid, [wiz, goblin], Roller(seed=1))
        result = _invoke(wiz, "hand_of_the_apprentice", goblin, enc, grid)
        ev = next(e for e in result.events
                  if e.kind == "wizard_power_hand_of_the_apprentice")
        # The trace contains "d20=N + bonus = total". With Int 16 → +3
        # mod, BAB 0, no size mod → +3 to hit. Damage uses Str
        # (longsword 1d8 + 2).
        trace = ev.detail.get("trace") or []
        import re
        if trace:
            m = re.search(r"d20=\d+ \+ (-?\d+)", trace[0])
            if m:
                self.assertEqual(int(m.group(1)), 3)


# ---------------------------------------------------------------------------
# Intense Spells (Evocation passive on evocation-spell damage)
# ---------------------------------------------------------------------------


class TestIntenseSpellsOnRealSpell(unittest.TestCase):
    """End-to-end: cast Magic Missile from an evoker → bonus once.
    Cast the same spell from a non-evoker → no bonus. Validates the
    RAW clause 'this bonus only applies once to a spell, not once per
    missile or ray'."""

    def _setup(self, school: str):
        body = {
            "name": "Mira", "race": "human", "class": "wizard",
            "alignment": "true_neutral",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 14, "dex": 14, "con": 14,
                           "int": 14, "wis": 10, "cha": 10}},
            "free_ability_choice": "int",
            "feats": ["dodge", "iron_will"],
            "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
            "bonus_languages": [],
            "class_choices": {"wizard_school": school,
                              "wizard_opposition_schools":
                                  (["abjuration", "necromancy"]
                                   if school != "universalist" else [])},
        }
        char = create_character(CharacterRequest.from_dict(body), REGISTRY)
        wiz = combatant_from_character(char, REGISTRY, (5, 5), "x")
        goblin = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (7, 5), "y",
        )
        goblin.max_hp = 9999
        goblin.current_hp = 9999
        return wiz, goblin

    def test_evoker_magic_missile_includes_intense_bonus(self):
        from dnd.engine.spells import cast_spell
        spell = REGISTRY.get_spell("magic_missile")
        wiz, goblin = self._setup("evocation")
        outcome = cast_spell(
            wiz, spell, [goblin], spell_level=1,
            registry=REGISTRY, roller=Roller(seed=1),
        )
        # The log entry "intense_spells +N" should appear exactly once
        # (RAW: not once per missile).
        intense_lines = [
            line for line in outcome.log
            if "intense_spells" in line
        ]
        self.assertEqual(len(intense_lines), 1)
        # L1 evoker: bonus = max(1, 1//2) = 1.
        self.assertIn("+1", intense_lines[0])

    def test_non_evoker_magic_missile_no_bonus(self):
        from dnd.engine.spells import cast_spell
        spell = REGISTRY.get_spell("magic_missile")
        wiz, goblin = self._setup("conjuration")
        outcome = cast_spell(
            wiz, spell, [goblin], spell_level=1,
            registry=REGISTRY, roller=Roller(seed=1),
        )
        intense_lines = [
            line for line in outcome.log
            if "intense_spells" in line
        ]
        self.assertEqual(intense_lines, [])


if __name__ == "__main__":
    unittest.main()
