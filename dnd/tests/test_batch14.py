"""Tests for Batch 14: DR multi-keyword AND-semantics, arcane spell
failure from armor, magic area shapes (line, spread, emanation), and
disbelief save."""

from __future__ import annotations

import unittest

from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combat import _apply_dr, DefenseProfile
from dnd.engine.combatant import (
    combatant_from_character,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.dsl import BehaviorScript, Interpreter, Rule
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid, wall
from dnd.engine.modifiers import Modifier
from dnd.engine.spells import (
    apply_typed_damage,
    cast_spell,
    disbelief_save,
)
from dnd.engine.turn_executor import (
    _expand_aoe_emanation,
    _expand_aoe_line,
    _expand_aoe_spread,
    execute_turn,
)


REGISTRY = default_registry()


class TestDRMultiKeyword(unittest.TestCase):
    def test_legacy_or_set_still_works(self):
        # DR 10/silver: any silver-tagged hit bypasses.
        defense = DefenseProfile(ac=10, touch_ac=10, flat_footed_ac=10,
                                 dr=(10, frozenset({"silver"})))
        # Silver hit bypasses fully.
        final, absorbed = _apply_dr(20, defense, "silver")
        self.assertEqual(final, 20)
        self.assertEqual(absorbed, 0)
        # Non-silver hit absorbed.
        final, absorbed = _apply_dr(20, defense, "S")
        self.assertEqual(final, 10)
        self.assertEqual(absorbed, 10)

    def test_or_set_with_two_keywords(self):
        # DR 10/silver or magic: either keyword bypasses.
        defense = DefenseProfile(ac=10, touch_ac=10, flat_footed_ac=10,
                                 dr=(10, frozenset({"silver", "magic"})))
        final, _ = _apply_dr(20, defense, "magic")
        self.assertEqual(final, 20)
        final, _ = _apply_dr(20, defense, "silver")
        self.assertEqual(final, 20)
        final, absorbed = _apply_dr(20, defense, "S")
        self.assertEqual(absorbed, 10)

    def test_and_semantics_requires_both(self):
        # DR 10/silver AND magic: only bypass when both are present.
        and_dr = (frozenset({"silver"}), frozenset({"magic"}))
        defense = DefenseProfile(ac=10, touch_ac=10, flat_footed_ac=10,
                                 dr=(10, and_dr))
        # Silver alone — DOESN'T bypass.
        final, absorbed = _apply_dr(20, defense, "silver")
        self.assertEqual(final, 10)
        self.assertEqual(absorbed, 10)
        # Magic alone — DOESN'T bypass.
        final, absorbed = _apply_dr(20, defense, "magic")
        self.assertEqual(absorbed, 10)
        # Silver and magic together (multi-tagged attack) — bypasses.
        final, absorbed = _apply_dr(20, defense, "silver/magic")
        self.assertEqual(final, 20)
        self.assertEqual(absorbed, 0)


class TestArcaneSpellFailure(unittest.TestCase):
    def _wizard_in_chainmail(self):
        # 0+5+5+10+0+0 = 20.
        req = CharacterRequest.from_dict({
            "name": "ASF Test", "race": "human", "class": "wizard",
            "alignment": "neutral_good",
            "ability_scores": {"method": "point_buy_20",
                "scores": {"str": 10, "dex": 14, "con": 14,
                           "int": 16, "wis": 10, "cha": 10}},
            "free_ability_choice": "int",
            "feats": ["combat_expertise", "iron_will"],
            "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
            "bonus_languages": [],
            "equipment": {"weapon": "quarterstaff", "armor": "chainmail",
                          "shield": None},
        })
        char = create_character(req, REGISTRY)
        return combatant_from_character(char, REGISTRY, (5, 5), "x")

    def test_arcane_caster_in_chainmail_can_fail(self):
        # Chainmail = 30% spell failure. Iterate seeds; at least one
        # should fail and at least one should succeed.
        any_fail = False
        any_pass = False
        for seed in range(1, 30):
            wiz = self._wizard_in_chainmail()
            target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                            (10, 5), "y")
            grid = Grid(width=20, height=10)
            grid.place(wiz)
            grid.place(target)
            enc = Encounter.begin(grid, [wiz, target], Roller(seed=seed))
            slots_before = wiz.resources.get("spell_slot_1", 0)
            script = BehaviorScript(name="cast", rules=[
                Rule(do={"composite": "cast", "args": {
                    "spell": "magic_missile", "spell_level": 1,
                    "target": "enemy.closest", "defensive": False,
                }}),
            ])
            intent = Interpreter(script).pick_turn(wiz, enc, grid)
            result = execute_turn(wiz, intent, enc, grid, Roller(seed=seed))
            kinds = [e.kind for e in result.events]
            failed_asf = any(
                e.kind == "cast_failed"
                and e.detail.get("reason") == "arcane_spell_failure"
                for e in result.events
            )
            if failed_asf:
                any_fail = True
            elif "cast" in kinds:
                any_pass = True
        self.assertTrue(any_fail, "expected at least one ASF failure")
        self.assertTrue(any_pass, "expected at least one ASF pass")

    def test_still_spell_skips_asf(self):
        wiz = self._wizard_in_chainmail()
        wiz.extra_feats = ["still_spell"]
        wiz.resources["spell_slot_2"] = 5
        target = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                        (10, 5), "y")
        grid = Grid(width=20, height=10)
        grid.place(wiz)
        grid.place(target)
        enc = Encounter.begin(grid, [wiz, target], Roller(seed=1))
        # Cast magic missile with still_spell metamagic — no ASF check.
        for seed in range(1, 5):
            wiz.resources["spell_slot_2"] = 5
            script = BehaviorScript(name="cast", rules=[
                Rule(do={"composite": "cast", "args": {
                    "spell": "magic_missile", "spell_level": 1,
                    "metamagic": ["still_spell"],
                    "target": "enemy.closest", "defensive": False,
                }}),
            ])
            intent = Interpreter(script).pick_turn(wiz, enc, grid)
            result = execute_turn(wiz, intent, enc, grid, Roller(seed=seed))
            failed_asf = any(
                e.kind == "cast_failed"
                and e.detail.get("reason") == "arcane_spell_failure"
                for e in result.events
            )
            self.assertFalse(failed_asf,
                             "still_spell should skip ASF check")


class TestAreaLine(unittest.TestCase):
    def test_line_hits_combatants_along_path(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        t1 = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                    (8, 5), "y")
        t2 = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                    (10, 5), "y")
        # Off-axis goblin; not on line.
        t3 = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                    (8, 8), "y")
        grid = Grid(width=30, height=20)
        grid.place(a)
        grid.place(t1)
        grid.place(t2)
        grid.place(t3)
        enc = Encounter.begin(grid, [a, t1, t2, t3], Roller(seed=1))
        spell = REGISTRY.get_spell("lightning_bolt")
        targets = _expand_aoe_line(
            a, spell, {"target": (15, 5)}, {}, enc, grid,
        )
        ids = {t.id for t in targets}
        self.assertIn(t1.id, ids)
        self.assertIn(t2.id, ids)
        self.assertNotIn(t3.id, ids)

    def test_line_stops_at_wall(self):
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        t1 = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                    (8, 5), "y")
        # Past-wall target should NOT be hit.
        t2 = combatant_from_monster(REGISTRY.get_monster("goblin"),
                                    (12, 5), "y")
        grid = Grid(width=30, height=20)
        grid.features[(10, 5)] = wall()
        grid.place(a)
        grid.place(t1)
        grid.place(t2)
        enc = Encounter.begin(grid, [a, t1, t2], Roller(seed=1))
        spell = REGISTRY.get_spell("lightning_bolt")
        targets = _expand_aoe_line(
            a, spell, {"target": (15, 5)}, {}, enc, grid,
        )
        ids = {t.id for t in targets}
        self.assertIn(t1.id, ids)
        self.assertNotIn(t2.id, ids)


class TestAreaSpread(unittest.TestCase):
    def test_spread_is_blocked_by_walls(self):
        # Place fireball center at (10, 5). Goblin at (12, 5). Wall at
        # (11, 5) blocks the straight burst. Spread reroutes around if
        # there's an opening — we'll set up a wall that fully blocks.
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (3, 5), "x")
        # In-radius goblin behind a wall.
        t_blocked = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (12, 5), "y",
        )
        # In-radius goblin with no wall in between.
        t_clear = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (10, 5), "y",
        )
        grid = Grid(width=30, height=20)
        # A wall ring between (12,5) and the spread origin (10,5).
        grid.features[(11, 5)] = wall()
        grid.features[(11, 4)] = wall()
        grid.features[(11, 6)] = wall()
        grid.features[(12, 4)] = wall()
        grid.features[(12, 6)] = wall()
        grid.features[(13, 5)] = wall()
        grid.place(a)
        grid.place(t_clear)
        grid.place(t_blocked)
        enc = Encounter.begin(grid, [a, t_clear, t_blocked], Roller(seed=1))
        spell = REGISTRY.get_spell("fireball")
        targets = _expand_aoe_spread(
            a, spell, {"target": (10, 5)}, {}, enc, grid,
        )
        ids = {t.id for t in targets}
        # Clear goblin is hit; walled-off goblin is NOT hit.
        self.assertIn(t_clear.id, ids)
        self.assertNotIn(t_blocked.id, ids)


class TestAreaEmanation(unittest.TestCase):
    def test_emanation_targets_allies_within_range(self):
        # bless_aura targets allies within 50 ft (10 squares).
        from dnd.engine.combatant import combatant_from_character
        a = combatant_from_monster(REGISTRY.get_monster("orc"), (5, 5), "x")
        ally_close = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (7, 5), "x",
        )
        ally_far = combatant_from_monster(
            REGISTRY.get_monster("goblin"), (25, 5), "x",
        )
        grid = Grid(width=40, height=20)
        grid.place(a)
        grid.place(ally_close)
        grid.place(ally_far)
        enc = Encounter.begin(grid, [a, ally_close, ally_far],
                              Roller(seed=1))
        spell = REGISTRY.get_spell("bless_aura")
        targets = _expand_aoe_emanation(
            a, spell, {}, {}, enc, grid,
        )
        ids = {t.id for t in targets}
        self.assertIn(ally_close.id, ids)
        self.assertNotIn(ally_far.id, ids)
        # Caster is in their own emanation.
        self.assertIn(a.id, ids)


class TestDisbeliefSave(unittest.TestCase):
    def test_passing_save_clears_sourced_effects(self):
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        # Apply a fake illusion: a marker modifier + a tracked condition.
        target.add_modifier(Modifier(
            value=0, type="untyped", target="illusion_marker",
            source="spell:silent_image",
        ))
        target.add_condition("fascinated")
        target.register_sourced_condition("spell:silent_image", "fascinated")
        # Force a passing save with a high d20 roll: nat 20 always passes.
        for seed in range(1, 30):
            # Reset condition for each seed.
            t2 = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
            t2.add_modifier(Modifier(
                value=0, type="untyped", target="illusion_marker",
                source="spell:silent_image",
            ))
            t2.add_condition("fascinated")
            t2.register_sourced_condition("spell:silent_image", "fascinated")
            passed, _, _ = disbelief_save(
                t2, "spell:silent_image", dc=15,
                roller=Roller(seed=seed), interacted=False,
            )
            if passed:
                # Effect cleared.
                self.assertNotIn("fascinated", t2.conditions)
                self.assertNotIn("spell:silent_image",
                                 t2.sourced_conditions)
                return
        self.fail("expected at least one seed where disbelief passed")

    def test_failing_save_leaves_effects(self):
        target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                        (0, 0), "x")
        target.bases["will_save"] = -100
        target.add_condition("fascinated")
        target.register_sourced_condition("spell:silent_image", "fascinated")
        passed, _, _ = disbelief_save(
            target, "spell:silent_image", dc=20,
            roller=Roller(seed=1), interacted=False,
        )
        self.assertFalse(passed)
        self.assertIn("fascinated", target.conditions)

    def test_interaction_grants_plus_4_bonus(self):
        # With interacted=True, the save bonus is +4 higher than not.
        # Iterate seeds and confirm that the +4 case passes more often.
        passes_no = 0
        passes_yes = 0
        for seed in range(1, 50):
            target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                            (0, 0), "x")
            target.add_condition("fascinated")
            target.register_sourced_condition(
                "spell:silent_image", "fascinated",
            )
            passed, _, _ = disbelief_save(
                target, "spell:silent_image", dc=20,
                roller=Roller(seed=seed), interacted=False,
            )
            if passed:
                passes_no += 1
            target = combatant_from_monster(REGISTRY.get_monster("orc"),
                                            (0, 0), "x")
            target.add_condition("fascinated")
            target.register_sourced_condition(
                "spell:silent_image", "fascinated",
            )
            passed, _, _ = disbelief_save(
                target, "spell:silent_image", dc=20,
                roller=Roller(seed=seed), interacted=True,
            )
            if passed:
                passes_yes += 1
        # Interaction should produce at least as many passes (and
        # typically strictly more on average).
        self.assertGreaterEqual(passes_yes, passes_no)


if __name__ == "__main__":
    unittest.main()
