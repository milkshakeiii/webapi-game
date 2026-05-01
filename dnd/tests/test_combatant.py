"""Tests for dnd.engine.combatant."""

from __future__ import annotations

import unittest

from dnd.engine.characters import (
    AbilityScores,
    Character,
    CharacterRequest,
    create_character,
)
from dnd.engine.combatant import (
    Combatant,
    combatant_from_character,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.modifiers import mod


REGISTRY = default_registry()


def _basic_fighter() -> Character:
    req = CharacterRequest.from_dict({
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
    })
    return create_character(req, REGISTRY)


def _halfling_rogue() -> Character:
    # 10/14/14/13/12/14 = 0+5+5+3+2+5 = 20.
    req = CharacterRequest.from_dict({
        "name": "Pim",
        "race": "halfling",
        "class": "rogue",
        "alignment": "chaotic_good",
        "ability_scores": {
            "method": "point_buy_20",
            "scores": {"str": 10, "dex": 14, "con": 14,
                       "int": 13, "wis": 12, "cha": 14},
        },
        "feats": ["weapon_finesse"],
        "skill_ranks": {"stealth": 1, "perception": 1, "acrobatics": 1},
        "bonus_languages": ["elven"],
    })
    return create_character(req, REGISTRY)


# ---------------------------------------------------------------------------
# Monster combatant
# ---------------------------------------------------------------------------


class TestMonsterCombatant(unittest.TestCase):
    def test_goblin_basics(self):
        goblin = REGISTRY.get_monster("goblin")
        c = combatant_from_monster(goblin, position=(5, 5), team="enemies")
        self.assertEqual(c.team, "enemies")
        self.assertEqual(c.size, "small")
        self.assertEqual(c.position, (5, 5))
        self.assertEqual(c.current_hp, 6)
        self.assertEqual(c.max_hp, 6)
        # AC should match the JSON total.
        self.assertEqual(c.ac("normal"), 16)
        # Touch AC excludes armor (2) and shield (1) → 16 - 2 - 1 = 13.
        self.assertEqual(c.ac("touch"), 13)
        # Flat-footed AC excludes Dex (+2) → 16 - 2 = 14.
        self.assertEqual(c.ac("flat_footed"), 14)

    def test_goblin_attack_options(self):
        goblin = REGISTRY.get_monster("goblin")
        c = combatant_from_monster(goblin, position=(0, 0), team="enemies")
        names = {a["name"] for a in c.attack_options}
        self.assertIn("short sword", names)
        self.assertIn("shortbow", names)

    def test_goblin_saves_match_json(self):
        goblin = REGISTRY.get_monster("goblin")
        c = combatant_from_monster(goblin, position=(0, 0), team="enemies")
        self.assertEqual(c.save("fort"), 3)
        self.assertEqual(c.save("ref"), 2)
        self.assertEqual(c.save("will"), -1)

    def test_zombie_starts_staggered(self):
        z = REGISTRY.get_monster("human_zombie")
        c = combatant_from_monster(z, position=(0, 0), team="enemies")
        self.assertIn("staggered", c.conditions)


# ---------------------------------------------------------------------------
# Character combatant
# ---------------------------------------------------------------------------


class TestCharacterCombatant(unittest.TestCase):
    def test_basic_fighter_stats(self):
        char = _basic_fighter()
        c = combatant_from_character(char, REGISTRY, position=(0, 0), team="patrons")
        self.assertEqual(c.team, "patrons")
        self.assertEqual(c.size, "medium")
        # Default fighter loadout: leather (+2) + light steel shield (+1).
        # AC = 10 + Dex(2) + leather(2) + shield(1) = 15.
        self.assertEqual(c.ac("normal"), 15)
        # Touch excludes armor + shield: 10 + Dex(2) = 12.
        self.assertEqual(c.ac("touch"), 12)
        # Flat-footed drops Dex: 10 + leather(2) + shield(1) = 13.
        self.assertEqual(c.ac("flat_footed"), 13)
        # Saves: Fort = 2 base + 2 Con = 4; Ref = 0 + 2 Dex = 2; Will = 0.
        self.assertEqual(c.save("fort"), 4)
        self.assertEqual(c.save("ref"), 2)
        self.assertEqual(c.save("will"), 0)
        # Attack option: longsword (default fighter weapon).
        self.assertEqual(len(c.attack_options), 1)
        att = c.attack_options[0]
        self.assertEqual(att["weapon_id"], "longsword")
        self.assertEqual(att["type"], "melee")
        # BAB 1 + Str(4) + size(0) = 5
        self.assertEqual(att["attack_bonus"], 5)
        self.assertEqual(att["damage"], "1d8")
        self.assertEqual(att["damage_bonus"], 4)  # Str mod, 1-handed

    def test_halfling_size_mods(self):
        char = _halfling_rogue()
        c = combatant_from_character(char, REGISTRY, position=(0, 0), team="patrons")
        self.assertEqual(c.size, "small")
        # Default rogue loadout: leather armor (+2), no shield.
        # AC: 10 + Dex(3) + leather(2) + size(+1) = 16.
        self.assertEqual(c.ac("normal"), 16)
        # CMB: BAB 0 + Str -1 + size -1 = -2.
        self.assertEqual(c.cmb(), -2)
        # CMD: 10 + BAB 0 + Str -1 + Dex 3 + size -1 = 11.
        self.assertEqual(c.cmd(), 11)
        # Stealth: rank 1 + Dex 3 + class skill 3 + size 4 = 11.
        # (Leather has 0 ACP, so no penalty.)
        self.assertEqual(c.skill_total("stealth"), 11)

    def test_halfling_will_save_includes_racial(self):
        # Halfling Luck: +1 racial to ALL saves (now wired).
        # Wis 12 → +1 mod; rogue base Will 0; halfling luck +1; total 2.
        char = _halfling_rogue()
        c = combatant_from_character(char, REGISTRY, position=(0, 0), team="patrons")
        self.assertEqual(c.save("will"), 2)  # rogue base 0 + Wis +1 + halfling +1

    def test_initiative_includes_dex(self):
        char = _basic_fighter()
        c = combatant_from_character(char, REGISTRY, position=(0, 0), team="patrons")
        self.assertEqual(c.initiative_modifier(), 2)


# ---------------------------------------------------------------------------
# Mutations
# ---------------------------------------------------------------------------


class TestCombatantMutations(unittest.TestCase):
    def setUp(self) -> None:
        goblin = REGISTRY.get_monster("goblin")
        self.c = combatant_from_monster(goblin, position=(0, 0), team="x")

    def test_take_damage(self):
        self.c.take_damage(3)
        self.assertEqual(self.c.current_hp, 3)
        self.c.take_damage(10)
        self.assertEqual(self.c.current_hp, -7)

    def test_heal_caps_at_max(self):
        self.c.take_damage(4)
        self.c.heal(100)
        self.assertEqual(self.c.current_hp, self.c.max_hp)

    def test_negative_amount_raises(self):
        with self.assertRaises(ValueError):
            self.c.take_damage(-1)
        with self.assertRaises(ValueError):
            self.c.heal(-1)

    def test_conditions(self):
        self.c.add_condition("blinded")
        self.assertIn("blinded", self.c.conditions)
        self.c.remove_condition("blinded")
        self.assertNotIn("blinded", self.c.conditions)

    def test_modifiers_buff_and_expire(self):
        # Apply a +4 enhancement to AC for 5 rounds.
        m = mod(4, "enhancement", "ac", "shield_spell", expires_round=5)
        before = self.c.ac()
        self.c.add_modifier(m)
        self.assertEqual(self.c.ac() - before, 4)
        # Tick to round 5: spell expires.
        expired = self.c.tick_round(5)
        self.assertEqual(len(expired), 1)
        self.assertEqual(self.c.ac(), before)


class TestDefenseProfile(unittest.TestCase):
    def test_goblin_profile_matches_ac_dict(self):
        goblin = REGISTRY.get_monster("goblin")
        c = combatant_from_monster(goblin, position=(0, 0), team="x")
        prof = c.defense_profile()
        self.assertEqual(prof.ac, 16)
        self.assertEqual(prof.touch_ac, 13)
        self.assertEqual(prof.flat_footed_ac, 14)


if __name__ == "__main__":
    unittest.main()
