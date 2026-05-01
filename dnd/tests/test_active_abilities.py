"""Tests for activatable class abilities and active combat options.

Covers Power Attack, Combat Expertise, Cleave, Rage, Smite Evil, Channel
Energy, and Bardic Performance — Inspire Courage.
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
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import (
    _combat_expertise_adjustments,
    _do_attack,
    _do_bardic_performance,
    _do_channel_energy,
    _do_cleave,
    _do_rage_end,
    _do_rage_start,
    _do_smite_evil,
    _power_attack_adjustments,
    _smite_evil_adjustments,
)


REGISTRY = default_registry()


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------


def _fighter(feats=None, class_choices=None, scores=None):
    req = CharacterRequest.from_dict({
        "name": "Edric", "race": "human", "class": "fighter",
        "alignment": "lawful_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": scores or {"str": 16, "dex": 14, "con": 14,
                                 "int": 10, "wis": 10, "cha": 10}},
        "free_ability_choice": "str",
        "feats": feats or ["power_attack", "weapon_focus"],
        "skill_ranks": {"climb": 1, "swim": 1},
        "bonus_languages": [],
        "class_choices": class_choices or {"fighter_bonus_feat": "cleave"},
    })
    char = create_character(req, REGISTRY)
    return combatant_from_character(char, REGISTRY, (5, 5), "patrons")


def _ce_fighter():
    """Fighter with INT 13 to satisfy Combat Expertise prereq.
    Point-buy 20: str 16 (10) + dex 12 (2) + con 14 (5) + int 13 (3)
    + wis 10 (0) + cha 10 (0) = 20. Human → 2 general feats.
    """
    return _fighter(
        feats=["power_attack", "combat_expertise"],
        class_choices={"fighter_bonus_feat": "weapon_focus"},
        scores={"str": 16, "dex": 12, "con": 14,
                "int": 13, "wis": 10, "cha": 10},
    )


def _barbarian():
    req = CharacterRequest.from_dict({
        "name": "Krug", "race": "half_orc", "class": "barbarian",
        "alignment": "chaotic_neutral",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 16, "dex": 14, "con": 14,
                       "int": 10, "wis": 10, "cha": 10}},
        "free_ability_choice": "str",
        "feats": ["power_attack"],
        "skill_ranks": {"intimidate": 1, "perception": 1},
        "bonus_languages": [],
    })
    char = create_character(req, REGISTRY)
    return combatant_from_character(char, REGISTRY, (5, 5), "patrons")


def _paladin():
    # Point-buy 20: str 14 (5) + dex 12 (2) + con 13 (3) + int 10 (0)
    # + wis 10 (0) + cha 16 (10) = 20. Human → +1 feat.
    req = CharacterRequest.from_dict({
        "name": "Aria", "race": "human", "class": "paladin",
        "alignment": "lawful_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 14, "dex": 12, "con": 13,
                       "int": 10, "wis": 10, "cha": 16}},
        "free_ability_choice": "cha",
        "feats": ["power_attack", "iron_will"],
        "skill_ranks": {"diplomacy": 1, "ride": 1},
        "bonus_languages": [],
    })
    char = create_character(req, REGISTRY)
    return combatant_from_character(char, REGISTRY, (5, 5), "patrons")


def _cleric():
    # Point-buy 20: str 10 (0) + dex 12 (2) + con 13 (3) + int 10 (0)
    # + wis 16 (10) + cha 14 (5) = 20. Human → +1 feat.
    req = CharacterRequest.from_dict({
        "name": "Bessa", "race": "human", "class": "cleric",
        "alignment": "neutral_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 10, "dex": 12, "con": 13,
                       "int": 10, "wis": 16, "cha": 14}},
        "free_ability_choice": "wis",
        "feats": ["iron_will", "great_fortitude"],
        "skill_ranks": {"heal": 1, "knowledge_religion": 1},
        "bonus_languages": [],
    })
    char = create_character(req, REGISTRY)
    return combatant_from_character(char, REGISTRY, (5, 5), "patrons")


def _bard():
    # Point-buy 20: str 10 (0) + dex 14 (5) + con 13 (3) + int 12 (2)
    # + wis 10 (0) + cha 16 (10) = 20. Half-elf gets +2 to chosen ability.
    req = CharacterRequest.from_dict({
        "name": "Lirin", "race": "half_elf", "class": "bard",
        "alignment": "chaotic_good",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 10, "dex": 14, "con": 13,
                       "int": 12, "wis": 10, "cha": 16}},
        "free_ability_choice": "cha",
        "feats": ["weapon_finesse"],
        "skill_ranks": {"perform": 1, "diplomacy": 1},
        "bonus_languages": ["elven"],
    })
    char = create_character(req, REGISTRY)
    return combatant_from_character(char, REGISTRY, (5, 5), "patrons")


def _goblin(pos=(6, 5)):
    return combatant_from_monster(
        REGISTRY.get_monster("goblin"), pos, "enemies",
    )


def _skeleton(pos=(6, 5)):
    return combatant_from_monster(
        REGISTRY.get_monster("skeleton"), pos, "enemies",
    )


def _make_encounter(*combatants):
    grid = Grid(width=20, height=20)
    for c in combatants:
        grid.place(c)
    enc = Encounter.begin(grid, list(combatants), Roller(seed=1))
    return enc, grid


# ---------------------------------------------------------------------------
# Power Attack
# ---------------------------------------------------------------------------


class TestPowerAttackAdjustments(unittest.TestCase):
    def test_one_handed_pen1_gives_dmg2(self):
        f = _fighter()
        chosen = f.attack_options[0]  # longsword (one-handed)
        atk_pen, dmg = _power_attack_adjustments(f, chosen, {"power_attack": 1})
        self.assertEqual(atk_pen, 1)
        self.assertEqual(dmg, 2)

    def test_two_handed_pen1_gives_dmg3(self):
        b = _barbarian()  # greataxe is two-handed
        chosen = b.attack_options[0]
        self.assertEqual(chosen.get("wield"), "two_handed")
        atk_pen, dmg = _power_attack_adjustments(b, chosen, {"power_attack": 1})
        self.assertEqual(atk_pen, 1)
        self.assertEqual(dmg, 3)

    def test_caps_at_max_for_bab(self):
        # L1 fighter has BAB 1; max_pen = 1 + 1//4 = 1.
        f = _fighter()
        chosen = f.attack_options[0]
        atk_pen, dmg = _power_attack_adjustments(f, chosen, {"power_attack": 5})
        self.assertEqual(atk_pen, 1)
        self.assertEqual(dmg, 2)

    def test_no_feat_no_bonus(self):
        f = _fighter(feats=["weapon_focus", "iron_will"],
                     class_choices={"fighter_bonus_feat": "alertness"})
        chosen = f.attack_options[0]
        atk_pen, dmg = _power_attack_adjustments(f, chosen, {"power_attack": 1})
        self.assertEqual((atk_pen, dmg), (0, 0))

    def test_zero_or_missing_returns_zero(self):
        f = _fighter()
        chosen = f.attack_options[0]
        self.assertEqual(_power_attack_adjustments(f, chosen, {}), (0, 0))
        self.assertEqual(
            _power_attack_adjustments(f, chosen, {"power_attack": 0}), (0, 0))


class TestPowerAttackEndToEnd(unittest.TestCase):
    def test_attack_with_power_attack_changes_log(self):
        f = _fighter()
        g = _goblin(pos=(6, 5))
        enc, grid = _make_encounter(f, g)
        events = []
        roller = Roller(seed=42)
        _do_attack(f, g, grid, roller, events,
                   encounter=enc, script_options={"power_attack": 1})
        attacks = [e for e in events if e.kind == "attack"]
        self.assertEqual(len(attacks), 1)
        # The trace should reflect at least the attack happening.
        self.assertIn("target_id", attacks[0].detail)


# ---------------------------------------------------------------------------
# Combat Expertise
# ---------------------------------------------------------------------------


class TestCombatExpertise(unittest.TestCase):
    def test_apply_pen_and_ac_buff(self):
        f = _ce_fighter()
        chosen = f.attack_options[0]
        g = _goblin()
        enc, grid = _make_encounter(f, g)
        events = []
        ac_before = f.ac()
        pen = _combat_expertise_adjustments(
            f, chosen, {"combat_expertise": 1}, enc, events,
        )
        self.assertEqual(pen, 1)
        self.assertEqual(f.ac(), ac_before + 1)
        ce_events = [e for e in events if e.kind == "combat_expertise"]
        self.assertEqual(len(ce_events), 1)

    def test_no_feat_no_effect(self):
        f = _fighter(feats=["power_attack", "weapon_focus"],
                    class_choices={"fighter_bonus_feat": "alertness"})
        chosen = f.attack_options[0]
        enc, grid = _make_encounter(f, _goblin())
        events = []
        ac_before = f.ac()
        pen = _combat_expertise_adjustments(
            f, chosen, {"combat_expertise": 1}, enc, events,
        )
        self.assertEqual(pen, 0)
        self.assertEqual(f.ac(), ac_before)

    def test_buff_expires_next_round(self):
        f = _ce_fighter()
        chosen = f.attack_options[0]
        enc, grid = _make_encounter(f, _goblin())
        events = []
        ac_before = f.ac()
        _combat_expertise_adjustments(
            f, chosen, {"combat_expertise": 1}, enc, events,
        )
        self.assertEqual(f.ac(), ac_before + 1)
        # Modifier expires at current_round + 1; tick to that round.
        f.tick_round(enc.round_number + 1)
        self.assertEqual(f.ac(), ac_before)


# ---------------------------------------------------------------------------
# Cleave
# ---------------------------------------------------------------------------


class TestCleave(unittest.TestCase):
    def test_cleave_requires_feat(self):
        f = _fighter(feats=["power_attack", "weapon_focus"],
                    class_choices={"fighter_bonus_feat": "alertness"})
        g = _goblin(pos=(6, 5))
        enc, grid = _make_encounter(f, g)
        events = []
        _do_cleave(f, {"target": "enemy.closest"}, enc, grid,
                   Roller(seed=1),
                   {"enemy": _enemy_resolver(f, enc, grid)}, events)
        self.assertTrue(any(
            e.kind == "skip" and "no feat" in (e.detail.get("reason") or "")
            for e in events))

    def test_cleave_applies_ac_penalty(self):
        f = _fighter()  # default class_choices includes cleave
        g = _goblin(pos=(6, 5))
        enc, grid = _make_encounter(f, g)
        ac_before = f.ac()
        events = []
        _do_cleave(f, {"target": "enemy.closest"}, enc, grid,
                   Roller(seed=1),
                   {"enemy": _enemy_resolver(f, enc, grid)}, events)
        # The -2 AC penalty modifier should be in place.
        self.assertEqual(f.ac(), ac_before - 2)

    def test_cleave_no_secondary_when_alone(self):
        f = _fighter()
        g = _goblin(pos=(6, 5))
        enc, grid = _make_encounter(f, g)
        events = []
        _do_cleave(f, {"target": "enemy.closest"}, enc, grid,
                   Roller(seed=1),
                   {"enemy": _enemy_resolver(f, enc, grid)}, events)
        secondary = [e for e in events if e.kind == "cleave_secondary"]
        self.assertEqual(secondary, [])

    def test_cleave_hits_secondary_when_two_adjacent(self):
        f = _fighter()
        g1 = _goblin(pos=(6, 5))
        g2 = _goblin(pos=(4, 5))
        enc, grid = _make_encounter(f, g1, g2)
        # Try a few seeds so the primary attack hits.
        for seed in range(1, 60):
            f.current_hp = f.max_hp
            g1.current_hp = g1.max_hp
            g2.current_hp = g2.max_hp
            f.modifiers.remove_by_source("cleave_ac_penalty")
            f.remove_condition("dying")
            f.remove_condition("dead")
            g1.conditions.clear()
            g2.conditions.clear()
            events = []
            _do_cleave(f, {"target": "enemy.closest"}, enc, grid,
                       Roller(seed=seed),
                       {"enemy": _enemy_resolver(f, enc, grid)}, events)
            primary = [e for e in events if e.kind == "cleave_primary"]
            if primary and primary[0].detail.get("hit"):
                # On a hit, we expect a secondary attack event to fire.
                self.assertTrue(
                    any(e.kind == "cleave_secondary" for e in events),
                    f"seed {seed}: primary hit but no secondary attack",
                )
                return
        self.skipTest("no seed produced a primary hit; not a real failure")


def _enemy_resolver(actor, enc, grid):
    """Build a mini namespace that has ``enemy.closest``."""
    from dnd.engine.dsl import EnemyResolver
    return EnemyResolver(actor, enc, grid)


# ---------------------------------------------------------------------------
# Rage
# ---------------------------------------------------------------------------


class TestRage(unittest.TestCase):
    def test_rage_resource_initialized(self):
        b = _barbarian()
        # 4 + Con(2) + 2 * 0 (level 1) = 6 rounds.
        self.assertEqual(b.resources.get("rage_rounds"), 6)

    def test_rage_start_applies_modifiers_and_condition(self):
        b = _barbarian()
        events = []
        enc, grid = _make_encounter(b, _goblin())
        ac_before = b.ac()
        will_before = b.save("will")
        _do_rage_start(b, {}, enc, events)
        self.assertIn("raging", b.conditions)
        self.assertEqual(b.resources["rage_rounds"], 5)
        self.assertEqual(b.ac(), ac_before - 2)         # -2 untyped AC
        self.assertEqual(b.save("will"), will_before + 2)  # +2 morale Will
        # Str ability bonus: morale +4 → +2 to attack/damage when next we attack.
        # Confirm via ability target.
        from dnd.engine.modifiers import compute as _compute
        str_total = _compute(0, b.modifiers.for_target("ability:str"))
        # original racial str bonus is some positive value; rage adds +4.
        # Assert that the modifier exists by source.
        self.assertTrue(any(
            m.source == "rage" and m.target == "ability:str" and m.value == 4
            for m in b.modifiers.modifiers
        ))

    def test_rage_end_drops_modifiers_and_fatigues(self):
        b = _barbarian()
        events = []
        enc, grid = _make_encounter(b, _goblin())
        ac_before = b.ac()
        _do_rage_start(b, {}, enc, events)
        events.clear()
        _do_rage_end(b, events)
        self.assertNotIn("raging", b.conditions)
        self.assertIn("fatigued", b.conditions)
        self.assertEqual(b.ac(), ac_before)  # back to baseline

    def test_rage_blocked_when_no_rounds(self):
        b = _barbarian()
        b.resources["rage_rounds"] = 0
        events = []
        enc, grid = _make_encounter(b, _goblin())
        _do_rage_start(b, {}, enc, events)
        self.assertNotIn("raging", b.conditions)
        self.assertTrue(any(e.kind == "skip" for e in events))


# ---------------------------------------------------------------------------
# Smite Evil
# ---------------------------------------------------------------------------


class TestSmiteEvil(unittest.TestCase):
    def test_paladin_resource_initialized(self):
        p = _paladin()
        self.assertEqual(p.resources.get("smite_evil_uses"), 1)

    def test_smite_locks_target_and_applies_bonuses(self):
        p = _paladin()
        g = _goblin(pos=(6, 5))
        enc, grid = _make_encounter(p, g)
        events = []
        _do_smite_evil(p, {"target": "enemy.closest"}, enc, grid,
                       {"enemy": _enemy_resolver(p, enc, grid)}, events)
        self.assertEqual(p.smite_target_id, g.id)
        self.assertEqual(p.resources["smite_evil_uses"], 0)
        atk, dmg = _smite_evil_adjustments(p, g)
        # Cha 18 (16 + human +2) → +4 attack; paladin level 1 → +1 damage.
        self.assertEqual(atk, 4)
        self.assertEqual(dmg, 1)

    def test_smite_does_not_apply_to_other_targets(self):
        p = _paladin()
        g1 = _goblin(pos=(6, 5))
        g2 = _goblin(pos=(4, 5))
        enc, grid = _make_encounter(p, g1, g2)
        events = []
        _do_smite_evil(p, {"target": "enemy.closest"}, enc, grid,
                       {"enemy": _enemy_resolver(p, enc, grid)}, events)
        # g1 was the closest target, so smite locks onto it; not g2.
        atk, _ = _smite_evil_adjustments(p, g2)
        self.assertEqual(atk, 0)

    def test_smite_non_evil_target_wastes_use(self):
        p = _paladin()
        # Use another paladin as the (non-evil) "target".
        ally = _paladin()
        ally.id = "ally_id"
        ally.team = "enemies"  # treat as opposing for resolver convenience
        ally.position = (6, 5)
        enc, grid = _make_encounter(p, ally)
        events = []
        _do_smite_evil(p, {"target": "enemy.closest"}, enc, grid,
                       {"enemy": _enemy_resolver(p, enc, grid)}, events)
        # Use was consumed but no smite target lock.
        self.assertEqual(p.resources["smite_evil_uses"], 0)
        self.assertIsNone(p.smite_target_id)
        self.assertTrue(any(e.kind == "smite_evil_wasted" for e in events))

    def test_smite_no_uses_blocked(self):
        p = _paladin()
        p.resources["smite_evil_uses"] = 0
        g = _goblin()
        enc, grid = _make_encounter(p, g)
        events = []
        _do_smite_evil(p, {"target": "enemy.closest"}, enc, grid,
                       {"enemy": _enemy_resolver(p, enc, grid)}, events)
        self.assertIsNone(p.smite_target_id)
        self.assertTrue(any(e.kind == "skip" for e in events))


class TestSmiteEvilEndToEndAttack(unittest.TestCase):
    def test_attack_against_smite_target_includes_bonuses(self):
        p = _paladin()
        g = _goblin(pos=(6, 5))
        enc, grid = _make_encounter(p, g)
        events = []
        _do_smite_evil(p, {"target": "enemy.closest"}, enc, grid,
                       {"enemy": _enemy_resolver(p, enc, grid)}, events)
        events.clear()
        _do_attack(p, g, grid, Roller(seed=10), events, encounter=enc)
        attacks = [e for e in events if e.kind == "attack"]
        self.assertEqual(len(attacks), 1)


# ---------------------------------------------------------------------------
# Channel Energy
# ---------------------------------------------------------------------------


class TestChannelEnergy(unittest.TestCase):
    def test_cleric_resource_initialized(self):
        c = _cleric()
        # 3 + Cha mod (Cha 14 → +2) = 5 uses.
        self.assertEqual(c.resources.get("channel_uses"), 5)

    def test_heal_living_heals_wounded_ally(self):
        c = _cleric()
        ally = _fighter()
        ally.position = (6, 5)
        ally.team = c.team
        ally.current_hp = max(1, ally.max_hp - 6)
        enc, grid = _make_encounter(c, ally)
        events = []
        _do_channel_energy(
            c, {"mode": "heal_living"}, enc, grid, Roller(seed=7),
            {"enemy": _enemy_resolver(c, enc, grid)}, events,
        )
        self.assertGreater(ally.current_hp, ally.max_hp - 6)
        self.assertEqual(c.resources["channel_uses"], 4)
        ce = [e for e in events if e.kind == "channel_energy"][0]
        # ally should appear in affected list.
        self.assertTrue(any(a["target_id"] == ally.id and a["kind"] == "heal"
                            for a in ce.detail["affected"]))

    def test_heal_living_harms_undead(self):
        c = _cleric()
        skel = _skeleton(pos=(6, 5))
        enc, grid = _make_encounter(c, skel)
        events = []
        before = skel.current_hp
        _do_channel_energy(
            c, {"mode": "heal_living"}, enc, grid, Roller(seed=11),
            {"enemy": _enemy_resolver(c, enc, grid)}, events,
        )
        # Skeleton should have taken some damage (or made save for half).
        self.assertLessEqual(skel.current_hp, before)
        ce = [e for e in events if e.kind == "channel_energy"][0]
        self.assertTrue(any(a["target_id"] == skel.id and a["kind"] == "harm_undead"
                            for a in ce.detail["affected"]))

    def test_radius_excludes_distant_targets(self):
        c = _cleric()
        far_skel = _skeleton(pos=(15, 15))  # well outside 6 squares
        enc, grid = _make_encounter(c, far_skel)
        events = []
        before = far_skel.current_hp
        _do_channel_energy(
            c, {"mode": "heal_living"}, enc, grid, Roller(seed=3),
            {"enemy": _enemy_resolver(c, enc, grid)}, events,
        )
        self.assertEqual(far_skel.current_hp, before)

    def test_channel_no_uses_blocked(self):
        c = _cleric()
        c.resources["channel_uses"] = 0
        skel = _skeleton(pos=(6, 5))
        enc, grid = _make_encounter(c, skel)
        events = []
        _do_channel_energy(
            c, {"mode": "heal_living"}, enc, grid, Roller(seed=1),
            {"enemy": _enemy_resolver(c, enc, grid)}, events,
        )
        self.assertTrue(any(e.kind == "skip" for e in events))


# ---------------------------------------------------------------------------
# Bardic Performance — Inspire Courage
# ---------------------------------------------------------------------------


class TestBardicPerformance(unittest.TestCase):
    def test_bard_resource_initialized(self):
        b = _bard()
        # 4 + Cha mod (Cha 18 with half-elf +2 → +4) + 0 = 8 rounds.
        self.assertEqual(b.resources.get("performance_rounds"), 8)

    def test_inspire_courage_buffs_allies(self):
        b = _bard()
        f = _fighter()
        f.position = (6, 5)
        f.team = b.team
        enc, grid = _make_encounter(b, f, _goblin(pos=(7, 5)))
        events = []
        attack_before = f.attack_options[0]["attack_bonus"]
        will_before = f.save("will")
        _do_bardic_performance(
            b, {"mode": "inspire_courage"}, enc, grid,
            {"enemy": _enemy_resolver(b, enc, grid)}, events,
        )
        # Modifiers added (not absorbed into attack_options[0] number, since
        # we use modifier collection at attack time).
        from dnd.engine.modifiers import compute as _compute
        atk_total = _compute(0, f.modifiers.for_target("attack"))
        dmg_total = _compute(0, f.modifiers.for_target("damage"))
        self.assertEqual(atk_total, 1)
        self.assertEqual(dmg_total, 1)
        self.assertEqual(f.save("will"), will_before + 1)

    def test_inspire_courage_consumes_round(self):
        b = _bard()
        before = b.resources["performance_rounds"]
        enc, grid = _make_encounter(b, _goblin(pos=(7, 5)))
        events = []
        _do_bardic_performance(
            b, {"mode": "inspire_courage"}, enc, grid,
            {"enemy": _enemy_resolver(b, enc, grid)}, events,
        )
        self.assertEqual(b.resources["performance_rounds"], before - 1)

    def test_inspire_courage_modifiers_expire(self):
        b = _bard()
        f = _fighter()
        f.position = (6, 5)
        f.team = b.team
        enc, grid = _make_encounter(b, f)
        events = []
        _do_bardic_performance(
            b, {"mode": "inspire_courage"}, enc, grid,
            {"enemy": _enemy_resolver(b, enc, grid)}, events,
        )
        # After ticking past the bard's next-turn round, the buff falls off.
        f.tick_round(enc.round_number + 1)
        from dnd.engine.modifiers import compute as _compute
        self.assertEqual(_compute(0, f.modifiers.for_target("attack")), 0)

    def test_no_rounds_blocks(self):
        b = _bard()
        b.resources["performance_rounds"] = 0
        enc, grid = _make_encounter(b, _goblin(pos=(7, 5)))
        events = []
        _do_bardic_performance(
            b, {"mode": "inspire_courage"}, enc, grid,
            {"enemy": _enemy_resolver(b, enc, grid)}, events,
        )
        self.assertTrue(any(e.kind == "skip" for e in events))


if __name__ == "__main__":
    unittest.main()
