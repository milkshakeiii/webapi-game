"""DSL v2 substrate Slice 3: Cast.

Covers the ``Cast`` action class — enumeration over (castable spell ×
target × defensive variant) and apply (delegates to ``_do_cast``).
"""

from __future__ import annotations

import unittest

from dnd.engine.actions import (
    Cast,
    GameState,
    apply_action,
    enumerate_legal_actions,
)
from dnd.engine.characters import CharacterRequest, create_character
from dnd.engine.combatant import (
    combatant_from_character,
    combatant_from_monster,
)
from dnd.engine.content import default_registry
from dnd.engine.dice import Roller
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid


REGISTRY = default_registry()


def _wizard(pos=(5, 5), team="x"):
    req = CharacterRequest.from_dict({
        "name": "Wiz", "race": "human", "class": "wizard",
        "alignment": "true_neutral",
        "ability_scores": {"method": "point_buy_20",
            "scores": {"str": 8, "dex": 14, "con": 14,
                       "int": 16, "wis": 12, "cha": 10}},
        "free_ability_choice": "int",
        "feats": ["iron_will", "great_fortitude"],
        "skill_ranks": {"spellcraft": 1, "knowledge_arcana": 1},
        "bonus_languages": [],
    })
    char = create_character(req, REGISTRY)
    return combatant_from_character(char, REGISTRY, pos, team)


def _orc(pos, team):
    return combatant_from_monster(REGISTRY.get_monster("orc"), pos, team)


def _build_caster_vs_enemy(*, with_threatener: bool = False):
    wiz = _wizard()
    enemy = _orc((10, 5), "y")
    others = [enemy]
    if with_threatener:
        threatener = _orc((6, 5), "y")  # adjacent to wiz
        others.append(threatener)
    grid = Grid(width=20, height=10)
    grid.place(wiz)
    for o in others:
        grid.place(o)
    enc = Encounter.begin(grid, [wiz, *others], Roller(seed=1))
    state = GameState(encounter=enc, grid=grid)
    return state, wiz, others


# ---------------------------------------------------------------------------
# Enumeration
# ---------------------------------------------------------------------------


class TestEnumerateCast(unittest.TestCase):
    def test_no_casts_when_castable_spells_empty(self):
        state, wiz, _ = _build_caster_vs_enemy()
        wiz.castable_spells = set()
        actions = enumerate_legal_actions(wiz, state)
        self.assertFalse(any(isinstance(a, Cast) for a in actions))

    def test_self_only_spell_targets_self(self):
        """``shield`` has target='self'; Cast should target the actor."""
        state, wiz, _ = _build_caster_vs_enemy()
        wiz.casting_type = "spontaneous"
        wiz.castable_spells = {"shield"}
        wiz.resources["spell_slot_1"] = 1
        actions = enumerate_legal_actions(wiz, state)
        casts = [a for a in actions if isinstance(a, Cast)]
        # Just one entry — shield on self.
        self.assertEqual(len(casts), 1)
        self.assertEqual(casts[0].target_id, wiz.id)
        self.assertEqual(casts[0].spell_id, "shield")

    def test_creature_target_spell_enumerated_per_visible(self):
        """``acid_splash`` (target=one_creature) is offered against every
        visible combatant (including self — patron decides who's a foe)."""
        state, wiz, others = _build_caster_vs_enemy()
        wiz.casting_type = "spontaneous"
        wiz.castable_spells = {"acid_splash"}
        actions = enumerate_legal_actions(wiz, state)
        cast_targets = {
            a.target_id for a in actions
            if isinstance(a, Cast) and a.spell_id == "acid_splash"
        }
        # 1 wizard + 1 enemy = 2 targets.
        self.assertEqual(cast_targets, {wiz.id, others[0].id})

    def test_defensive_variant_when_threatened(self):
        state, wiz, others = _build_caster_vs_enemy(with_threatener=True)
        wiz.casting_type = "spontaneous"
        wiz.castable_spells = {"acid_splash"}
        actions = enumerate_legal_actions(wiz, state)
        casts = [a for a in actions if isinstance(a, Cast)]
        defensive = [a for a in casts if a.defensive]
        non_defensive = [a for a in casts if not a.defensive]
        self.assertEqual(len(defensive), len(non_defensive),
                         "every cast should have a defensive twin "
                         "when threatened")

    def test_no_defensive_variant_when_unthreatened(self):
        state, wiz, _ = _build_caster_vs_enemy()
        wiz.casting_type = "spontaneous"
        wiz.castable_spells = {"acid_splash"}
        actions = enumerate_legal_actions(wiz, state)
        defensive = [a for a in actions
                     if isinstance(a, Cast) and a.defensive]
        self.assertEqual(defensive, [])

    def test_spell_level_picked_up_from_class(self):
        """``magic_missile`` is wizard L1; Cast.spell_level should be 1."""
        state, wiz, _ = _build_caster_vs_enemy()
        wiz.casting_type = "spontaneous"
        wiz.castable_spells = {"magic_missile"}
        actions = enumerate_legal_actions(wiz, state)
        casts = [a for a in actions
                 if isinstance(a, Cast) and a.spell_id == "magic_missile"]
        self.assertGreater(len(casts), 0)
        self.assertTrue(all(c.spell_level == 1 for c in casts))

    def test_no_casts_when_standard_used(self):
        state, wiz, _ = _build_caster_vs_enemy()
        wiz.casting_type = "spontaneous"
        wiz.castable_spells = {"acid_splash"}
        state.slots_for(wiz).standard_used = True
        actions = enumerate_legal_actions(wiz, state)
        self.assertFalse(any(isinstance(a, Cast) for a in actions))


# ---------------------------------------------------------------------------
# Apply
# ---------------------------------------------------------------------------


class TestApplyCast(unittest.TestCase):
    def test_cast_consumes_standard_slot(self):
        state, wiz, others = _build_caster_vs_enemy()
        wiz.casting_type = "spontaneous"
        wiz.castable_spells = {"acid_splash"}
        target = others[0]
        apply_action(
            Cast(actor_id=wiz.id, spell_id="acid_splash",
                 target_id=target.id, spell_level=0),
            state, Roller(seed=1),
        )
        self.assertTrue(state.slots_for(wiz).standard_used)

    def test_cast_emits_cast_or_resolution_event(self):
        state, wiz, others = _build_caster_vs_enemy()
        wiz.casting_type = "spontaneous"
        wiz.castable_spells = {"acid_splash"}
        target = others[0]
        result = apply_action(
            Cast(actor_id=wiz.id, spell_id="acid_splash",
                 target_id=target.id, spell_level=0),
            state, Roller(seed=1),
        )
        # cast or scaling_damage / similar should be in the events.
        kinds = [e.kind for e in result.events]
        self.assertGreater(len(kinds), 0,
                           f"expected events from cast; got {kinds}")

    def test_unknown_spell_skips_with_reason(self):
        state, wiz, others = _build_caster_vs_enemy()
        target = others[0]
        result = apply_action(
            Cast(actor_id=wiz.id, spell_id="nonexistent_spell_xyz",
                 target_id=target.id, spell_level=1),
            state, Roller(seed=1),
        )
        kinds = [e.kind for e in result.events]
        self.assertIn("skip", kinds)
        # _do_cast emits its own skip with reason starting "unknown spell".
        skip = next(e for e in result.events if e.kind == "skip")
        self.assertIn("unknown", skip.detail.get("reason", "").lower())

    def test_target_gone_skips_cast(self):
        state, wiz, others = _build_caster_vs_enemy()
        wiz.casting_type = "spontaneous"
        wiz.castable_spells = {"acid_splash"}
        result = apply_action(
            Cast(actor_id=wiz.id, spell_id="acid_splash",
                 target_id="not_a_real_id", spell_level=0),
            state, Roller(seed=1),
        )
        skip = next(e for e in result.events if e.kind == "skip")
        self.assertIn("target gone", skip.detail.get("reason", ""))

    def test_defensive_cast_runs_concentration(self):
        """A defensive cast against a threatening foe should run a
        concentration check (DC 15 + 2*spell_level). With low CL and
        low ability mod, a fixed seed should reliably surface either
        a success or failure event with the DC visible."""
        state, wiz, others = _build_caster_vs_enemy(with_threatener=True)
        wiz.casting_type = "spontaneous"
        wiz.castable_spells = {"acid_splash"}
        target = others[0]  # the far enemy
        result = apply_action(
            Cast(actor_id=wiz.id, spell_id="acid_splash",
                 target_id=target.id, spell_level=0,
                 defensive=True),
            state, Roller(seed=1),
        )
        # Concentration check should appear, either inside cast_failed
        # detail or another event.
        found_dc = False
        for e in result.events:
            check = e.detail.get("concentration_check") if e.detail else None
            if check and "dc" in check:
                # DC = 15 + 2*0 = 15 for a cantrip.
                self.assertEqual(check["dc"], 15)
                found_dc = True
        # Either we found a concentration_check (the cast was defensive
        # and rolled), or the cast resolved without one (e.g., no
        # threatener detected — but we set up a threatener so this
        # shouldn't happen).
        self.assertTrue(found_dc,
                        f"expected concentration_check; "
                        f"got events {[e.kind for e in result.events]}")


if __name__ == "__main__":
    unittest.main()
