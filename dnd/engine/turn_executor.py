"""Execute a TurnIntent against the live encounter state.

Walks the slot fills in PF1 order and resolves each: movement updates
positions on the grid (and triggers AoOs from leaving threatened
squares), attack actions run through ``combat.resolve_attack``, etc.

The executor returns a structured log of events that the encounter
appends to its trace.

Currently supports the actions needed for the level-1 fighter vs.
goblin demo: ``attack``, ``charge``, ``full_attack``, ``move_to``,
``move_toward``, ``move_away``, ``5ft_step``, ``withdraw``, ``hold``.
Other vocab actions (cast, drink, class abilities) raise
``NotImplementedError`` for now and will be added incrementally.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .combat import (
    AttackOutcome,
    AttackProfile,
    DefenseProfile,
    resolve_attack,
)
from .combatant import Combatant
from .dice import Roller
from .dsl import TurnIntent, evaluate
from .encounter import Encounter, aoo_triggers_for_movement
from .grid import Grid
from .modifiers import Modifier, compute as _compute_mod
from .modifiers import compute_with_context as _compute_mod_ctx


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass
class TurnEvent:
    """One event during a turn — an attack, a move, an AoO, etc."""

    actor_id: str
    kind: str             # "attack", "move", "aoo", "skip", etc.
    detail: dict


@dataclass
class TurnResult:
    actor_id: str
    rule_index: int | None
    events: list[TurnEvent]

    def to_dict(self) -> dict:
        return {
            "actor_id": self.actor_id,
            "rule_index": self.rule_index,
            "events": [{"actor_id": e.actor_id, "kind": e.kind,
                        "detail": e.detail} for e in self.events],
        }


# ---------------------------------------------------------------------------
# Top-level entry
# ---------------------------------------------------------------------------


def execute_turn(
    actor: Combatant,
    intent: TurnIntent | None,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
) -> TurnResult:
    """Execute the actor's turn against the encounter state.

    DSL v2: this is now a thin wrapper that delegates to the
    substrate-driven ``run_intent_via_substrate`` in ``actions``.
    The function lives here for import compatibility with existing
    callers — eventually patrons will hold pickers directly and call
    apply_action / enumerate_legal_actions, and execute_turn becomes
    redundant.
    """
    from .actions import run_intent_via_substrate
    return run_intent_via_substrate(
        actor, intent, encounter, grid, roller,
    )


_AURA_TRAITS: dict[str, dict] = {
    "stench": {
        "radius_squares": 6,           # 30 ft / 5 ft per square
        "save": "fort",
        "ability_for_dc": "con",
        "condition": "sickened",
        "duration_dice": "1d6",        # rounds on save fail
        "cooldown": "encounter",
        "self_immune_template_ids": ["troglodyte"],
    },
    "captivating_song": {
        "radius_squares": 60,          # 300 ft
        "save": "will",
        "ability_for_dc": "cha",
        "condition": "fascinated",
        "duration_dice": None,         # ongoing while singing
        "cooldown": "encounter",
        "self_immune_template_ids": ["harpy"],
    },
    "petrifying_gaze": {
        "radius_squares": 6,           # 30 ft
        "save": "fort",
        "ability_for_dc": "cha",       # basilisk gaze DC = Cha-based
        "condition": "petrified",
        "duration_dice": None,         # permanent until Stone to Flesh
        "cooldown": "round",           # fresh save each round
        "self_immune_template_ids": ["basilisk"],
    },
}


def _aura_save_dc(source: Combatant, trait_data: dict) -> int:
    """Standard PF1 monster save-DC formula: 10 + 1/2 HD + ability mod."""
    hd = _monster_hd(source)
    ability = trait_data.get("ability_for_dc", "cha")
    return 10 + hd // 2 + _ability_modifier(source, ability)


def _apply_aura_exposure(
    actor: Combatant, grid: Grid, roller: Roller,
    events: list[TurnEvent], *, encounter=None,
) -> None:
    """Roll any unsaved aura saves the actor is exposed to right now.

    Cooldown semantics:
      - "encounter": one save per source per encounter (stench,
        captivating_song). Both pass and fail consume the cooldown.
      - "round": fresh save every round (gazes). The cooldown key
        bakes in the round number so a new round resets it.
    """
    if grid is None:
        return
    if "dead" in actor.conditions or "unconscious" in actor.conditions:
        return
    encounter_round = (
        int(encounter.round_number) if encounter is not None else 0
    )
    for cid, source in list(grid.combatants.items()):
        if source.id == actor.id:
            continue
        if "dead" in source.conditions:
            continue
        for trait_id, data in _AURA_TRAITS.items():
            if not _has_racial_trait(source, trait_id):
                continue
            self_immune = data.get("self_immune_template_ids") or []
            if (
                actor.template_kind == "monster"
                and actor.template is not None
                and getattr(actor.template, "id", None) in self_immune
            ):
                continue
            radius = int(data.get("radius_squares", 0))
            ax, ay = actor.position
            sx, sy = source.position
            if max(abs(ax - sx), abs(ay - sy)) > radius:
                continue
            cooldown = data.get("cooldown", "encounter")
            if cooldown == "round":
                key = f"{trait_id}:{source.id}:r{encounter_round}"
            else:
                key = f"{trait_id}:{source.id}"
            if key in actor.aura_saves_taken:
                continue
            # Don't re-apply a permanent condition that's already set.
            cond = data.get("condition")
            if cond and cond in actor.conditions and not data.get("duration_dice"):
                actor.aura_saves_taken.add(key)
                continue
            from .spells import roll_save
            dc = _aura_save_dc(source, data)
            kind = data["save"]
            passed, nat, total = roll_save(actor, kind, dc, roller)
            actor.aura_saves_taken.add(key)
            event_detail: dict = {
                "trait": trait_id,
                "source_id": source.id,
                "save_kind": kind,
                "dc": dc,
                "natural": nat, "total": total, "passed": passed,
            }
            if not passed and cond:
                actor.add_condition(cond)
                duration_dice = data.get("duration_dice")
                if duration_dice:
                    dur_roll = roller.roll(duration_dice)
                    event_detail["duration"] = int(dur_roll.total)
            events.append(TurnEvent(actor.id, "aura_exposure", event_detail))


def _apply_end_of_turn_racial_effects(
    actor: Combatant, grid: Grid, roller: Roller,
    events: list[TurnEvent], *, encounter=None,
) -> None:
    """Per-round racial effects that fire at the end of the actor's turn.

    Currently:
    - Stirge blood drain: while grappling a target, drain 1d4 Con.
      Stops once the cumulative drain reaches 4 (RAW cap).
    - Lion rake: while grappling, two free claw attacks against the
      grapple target.
    - Aura exposure: when the actor ends its turn within an aura
      source's range, the actor makes the matching save (one save
      per aura per encounter; see Combatant.aura_saves_taken).
    """
    _apply_aura_exposure(actor, grid, roller, events, encounter=encounter)
    if (
        _has_racial_trait(actor, "blood_drain")
        and actor.grappling_target_id is not None
        and grid is not None
    ):
        target = grid.combatants.get(actor.grappling_target_id)
        if target is not None and "dead" not in target.conditions:
            already = int(actor.resources.get("blood_drain_dealt", 0))
            if already < 4:
                r = roller.roll("1d4")
                amount = min(int(r.total), 4 - already)
                target.apply_ability_damage("con", amount)
                actor.resources["blood_drain_dealt"] = already + amount
                events.append(TurnEvent(actor.id, "blood_drain", {
                    "target_id": target.id,
                    "amount": amount,
                    "cumulative": already + amount,
                }))
    if (
        _has_racial_trait(actor, "rake_lion")
        and actor.grappling_target_id is not None
        and grid is not None
    ):
        target = grid.combatants.get(actor.grappling_target_id)
        if target is not None and target.is_alive():
            claw_indices = [
                i for i, opt in enumerate(actor.attack_options or [])
                if str(opt.get("name", "")).lower().startswith("claw")
            ][:2]
            for idx in claw_indices:
                if not target.is_alive():
                    break
                _do_attack(actor, target, grid, roller, events,
                           label="rake", encounter=None,
                           attack_index=idx)
    # Choker constrict + strangle: while grappling, automatic 1d4+3
    # bludgeoning damage and silenced (cannot speak / V-cast).
    if (
        _has_racial_trait(actor, "constrict_strangle")
        and actor.grappling_target_id is not None
        and grid is not None
    ):
        target = grid.combatants.get(actor.grappling_target_id)
        if target is not None and target.is_alive():
            r = roller.roll("1d4")
            damage = int(r.total) + 3
            target.take_damage(damage)
            _apply_post_damage_state(target)
            if "silenced" not in target.conditions:
                target.add_condition("silenced")
                target.register_sourced_condition(
                    f"constrict_strangle:{actor.id}", "silenced",
                )
            events.append(TurnEvent(actor.id, "constrict_strangle", {
                "target_id": target.id,
                "damage": damage,
            }))
    # Gelatinous-cube engulf: any adjacent enemy that isn't already
    # engulfed by this cube makes a Reflex save (DC 10 + 1/2 HD +
    # Str mod). Failure: victim becomes engulfed (paralyzed + 1d6
    # acid this round + ongoing per-round acid via ongoing_effects).
    # An already-engulfed victim gets a per-round Reflex save to
    # escape (success → free, paralysis cleared, ongoing acid
    # removed). This wires the RAW pull-along + per-round acid;
    # the move-into-square save is approximated by end-of-turn
    # adjacency.
    if (
        _has_racial_trait(actor, "engulf")
        and grid is not None
    ):
        from .spells import roll_save
        hd = _monster_hd(actor)
        str_mod = _ability_modifier(actor, "str")
        dc = 10 + hd // 2 + str_mod
        cur_round = (
            int(encounter.round_number) if encounter is not None else 0
        )
        # Build candidates: anyone already engulfed by this cube (may
        # be off-grid) plus any adjacent enemy on the grid.
        candidates: dict[str, Combatant] = {}
        if encounter is not None:
            for ir in encounter.initiative:
                if ir.combatant.engulfed_by_id == actor.id:
                    candidates[ir.combatant.id] = ir.combatant
        for cid, victim in list(grid.combatants.items()):
            if victim.id == actor.id or victim.team == actor.team:
                continue
            if grid.is_adjacent(actor, victim):
                candidates[victim.id] = victim
        for victim in list(candidates.values()):
            if victim.team == actor.team:
                continue
            if "dead" in victim.conditions:
                continue
            already_engulfed = victim.engulfed_by_id == actor.id
            passed, nat, total = roll_save(victim, "ref", dc, roller)
            event_detail = {
                "target_id": victim.id, "dc": dc,
                "natural": nat, "total": total, "passed": passed,
                "was_engulfed": already_engulfed,
            }
            if already_engulfed and passed:
                # Escape: clear engulf state, lift paralysis, place
                # victim back on the grid at the closest free square
                # adjacent to the cube.
                victim.engulfed_by_id = None
                victim.remove_condition("paralyzed")
                _place_at_free_adjacent(victim, actor, grid)
                event_detail["effect"] = "escaped"
            elif already_engulfed and not passed:
                # Still engulfed → another 1d6 acid this round.
                acid = roller.roll("1d6")
                victim.take_damage(int(acid.total), damage_type="acid")
                _apply_post_damage_state(victim)
                event_detail["effect"] = "still_engulfed"
                event_detail["acid_damage"] = int(acid.total)
            elif not already_engulfed and not passed:
                # Newly engulfed: paralyzed + immediate 1d6 acid.
                # Pull-along: remove victim from grid (occupies the
                # cube's interior). Released on escape via the
                # already_engulfed-pass branch above.
                victim.engulfed_by_id = actor.id
                victim.add_condition("paralyzed")
                acid = roller.roll("1d6")
                victim.take_damage(int(acid.total), damage_type="acid")
                _apply_post_damage_state(victim)
                grid.remove(victim.id)
                event_detail["effect"] = "engulfed"
                event_detail["acid_damage"] = int(acid.total)
            events.append(TurnEvent(actor.id, "engulf", event_detail))


_STANDARD_ACTION_EVENT_KINDS: frozenset[str] = frozenset({
    "attack", "charge_attack", "defensive_attack", "lance_charge",
    "cast", "cast_failed", "channel_energy", "smite_evil",
    "stunning_fist", "aid_another", "total_defense",
    "trample", "coup_de_grace",
})


def _resolve_confusion(
    actor: Combatant,
    do: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    events: list[TurnEvent],
) -> dict | None:
    """Apply PF1 confusion table; return new ``do`` or ``None`` to skip.

    Returning ``None`` means the actor's turn is fully consumed by
    the confusion outcome (do-nothing or self-attack); the caller
    should bail out of further action processing.
    """
    r = roller.roll("1d100")
    val = r.terms[0].rolls[0] if r.terms else int(r.total)
    if val <= 25:
        events.append(TurnEvent(actor.id, "confused_act_normally",
                                {"roll": val}))
        return do
    if val <= 50:
        events.append(TurnEvent(actor.id, "confused_babble",
                                {"roll": val}))
        return None
    if val <= 75:
        # Self-damage: 1d8 + Str modifier with held weapon. We don't
        # track held weapons cleanly for monsters, so use 1d8 + Str.
        str_mod = _ability_modifier(actor, "str")
        dmg_roll = roller.roll("1d8")
        damage = max(1, int(dmg_roll.total) + str_mod)
        actor.take_damage(damage)
        _apply_post_damage_state(actor)
        events.append(TurnEvent(actor.id, "confused_self_attack", {
            "roll": val,
            "damage": damage,
            "die_roll": int(dmg_roll.total),
            "str_mod": str_mod,
            "hp_after": actor.current_hp,
        }))
        return None
    # 76-100: attack nearest creature (any team, friend or foe).
    nearest = _nearest_living_creature(actor, grid)
    if nearest is None:
        events.append(TurnEvent(actor.id, "confused_babble",
                                {"roll": val,
                                 "reason": "no nearest creature"}))
        return None
    events.append(TurnEvent(actor.id, "confused_attack_nearest", {
        "roll": val,
        "target_id": nearest.id,
    }))
    # Pass the Combatant object directly so _resolve_target doesn't try
    # to evaluate the id as a DSL expression.
    return {"standard": {"type": "attack", "target": nearest}}


def _nearest_living_creature(actor: Combatant, grid: Grid) -> Combatant | None:
    """Return the closest non-dead creature other than the actor.

    Used by confusion to pick the attack target. Returns ``None`` if
    no other living creature exists on the grid.
    """
    if grid is None or not getattr(grid, "combatants", None):
        return None
    best: Combatant | None = None
    best_dist = float("inf")
    ax, ay = actor.position
    for cid, other in grid.combatants.items():
        if other.id == actor.id:
            continue
        if "dead" in other.conditions:
            continue
        ox, oy = other.position
        d = max(abs(ox - ax), abs(oy - ay))  # Chebyshev (square grid)
        if d < best_dist:
            best_dist = d
            best = other
    return best


def _place_at_free_adjacent(
    victim: Combatant, anchor: Combatant, grid: Grid,
) -> None:
    """Place ``victim`` on a free square adjacent to ``anchor``'s
    footprint. Falls back to the victim's stored position if no
    adjacent free square exists. Used when an engulfed creature
    escapes the cube.
    """
    if grid is None:
        return
    ax, ay = anchor.position
    # Anchor footprint expansion: probe a 3x3 ring around the
    # anchor's anchor-square.
    candidates: list[tuple[int, int]] = []
    for dx in (-1, 0, 1, 2):
        for dy in (-1, 0, 1, 2):
            if dx == 0 and dy == 0:
                continue
            candidates.append((ax + dx, ay + dy))
    for sq in candidates:
        if not grid.in_bounds(*sq):
            continue
        if grid._occupancy.get(sq) is not None:
            continue
        victim.position = sq
        try:
            grid.place(victim)
            return
        except Exception:
            continue
    # No free square; leave victim off-grid (engulfed_by_id cleared).


def _movement_squares(actor: Combatant, encounter) -> int:
    """Compute the actor's per-action movement allowance, in squares.

    Layered on top of ``actor.speed // 5``:
    - Choker quickness: +2 squares (+10 ft) on round 1 only.
    """
    base = actor.speed // 5
    round_no = int(getattr(encounter, "round_number", 0)) if encounter else 0
    if round_no == 1 and _has_racial_trait(actor, "quickness"):
        base += 2
    return base


def _turn_used_standard_action(events: list[TurnEvent]) -> bool:
    """Heuristic: did any event indicate a standard-action effect?

    Used by the disabled-self-damage hook. A standard action that
    didn't actually fire (skipped due to invalid target, etc.) doesn't
    cost the disabled creature their 1 HP.
    """
    for e in events:
        if e.kind in _STANDARD_ACTION_EVENT_KINDS:
            return True
    return False


# ---------------------------------------------------------------------------
# Spell casting-time classification
# ---------------------------------------------------------------------------


def _classify_casting_time(ct: str) -> str:
    """Bucket a Spell.casting_time string into one of the action-slot
    categories the engine recognizes:

    - ``standard``   — single standard action (default)
    - ``swift``      — swift action (1 / round)
    - ``immediate``  — immediate action (interrupts; will be wired as a
      reactive-interrupt decision-point in DSL v2 — see
      DECISION_POINT_DSL.md)
    - ``free``       — free action (very rare, e.g. some abilities)
    - ``full_round`` — single full-round action
    - ``multi_round``— takes multiple rounds (1 round counts here per
      RAW: 'a 1-round casting time means the spell completes just
      before your next turn')

    The strings come from JSON / Foundry; we accept several common
    shapes (``1_round``, ``"1 round"``, ``"3_rounds"``).
    """
    s = (ct or "standard").strip().lower().replace(" ", "_")
    if s in ("standard", "1_standard", "1_standard_action", "standard_action"):
        return "standard"
    if s in ("swift", "1_swift", "swift_action"):
        return "swift"
    if s in ("immediate", "1_immediate", "immediate_action"):
        return "immediate"
    if s in ("free", "1_free", "free_action"):
        return "free"
    if s in ("full_round", "full-round", "1_full_round", "full"):
        return "full_round"
    if s in ("1_round", "1round"):
        return "multi_round"
    if s.endswith("_rounds") or s.endswith("rounds"):
        return "multi_round"
    if (
        "minute" in s or "hour" in s or "day" in s
    ):
        return "multi_round"  # ritual-grade casts; treat the same for v1
    return "standard"


# ---------------------------------------------------------------------------
# Movement primitives
#
# Note: the v1 dispatch entry points (``_execute_composite`` /
# ``_execute_slots`` / ``_do_standard``) were deleted in Phase 5 of
# the DSL v2 migration. The per-action helpers below
# (``_do_move_action``, ``_do_charge``, ``_do_full_attack``,
# ``_do_combat_maneuver``, ``_do_cast``, etc.) live on — they're now
# called from ``apply_action`` in ``actions.py``.
# ---------------------------------------------------------------------------


def _do_move_action(
    actor: Combatant,
    move: dict,
    encounter: Encounter,
    grid: Grid,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    mtype = move.get("type")
    speed_squares = _movement_squares(actor, encounter)
    if mtype == "move_to":
        target = _resolve_target(move.get("target"), ns)
        dest = _coerce_square(target)
        if dest is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "move_to: no destination"}))
            return
        _move_along(actor, dest, speed_squares, grid, events, encounter=encounter)
    elif mtype == "move_toward":
        target = _resolve_target(move.get("target"), ns)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "move_toward: no target"}))
            return
        dest = _square_toward(actor, target, speed_squares, grid)
        _move_along(actor, dest, speed_squares, grid, events, encounter=encounter)
    elif mtype == "move_away":
        target = _resolve_target(move.get("target"), ns)
        if target is None:
            return
        dest = _square_away(actor, target, speed_squares, grid)
        _move_along(actor, dest, speed_squares, grid, events, encounter=encounter)
    elif mtype == "stand_up":
        if "prone" in actor.conditions:
            # PF1: standing up provokes AoOs from threateners.
            from .encounter import aoo_triggers_for_provoking_action
            for threatener in aoo_triggers_for_provoking_action(
                grid, actor, "stand_up",
            ):
                _do_aoo(threatener, actor, grid, events, encounter=encounter)
                if not actor.is_alive() or actor.current_hp <= -10:
                    events.append(TurnEvent(actor.id, "skip",
                                            {"reason": "killed by AoO"}))
                    return
            actor.remove_condition("prone")
            events.append(TurnEvent(actor.id, "stand_up", {}))
    elif mtype == "draw_weapon":
        # RAW: drawing a weapon does not provoke (Action Table). The
        # BAB +1 threshold is about *combining* the draw with a regular
        # move (free vs. move action), not about AoO suppression.
        events.append(TurnEvent(actor.id, "draw_weapon",
                                {"weapon": move.get("weapon")}))
    elif mtype == "drink_potion":
        # Drinking a potion provokes AoOs from threateners.
        from .encounter import aoo_triggers_for_provoking_action
        for threatener in aoo_triggers_for_provoking_action(
            grid, actor, "drink",
        ):
            _do_aoo(threatener, actor, grid, events,
                    encounter=encounter)
            if not actor.is_alive() or actor.current_hp <= -10:
                events.append(TurnEvent(actor.id, "skip",
                                        {"reason": "killed by AoO"}))
                return
        events.append(TurnEvent(actor.id, "drink_potion",
                                {"potion": move.get("potion")}))
    elif mtype == "retrieve_stowed_item":
        # Retrieving a stowed item is a move action that provokes.
        from .encounter import aoo_triggers_for_provoking_action
        for threatener in aoo_triggers_for_provoking_action(
            grid, actor, "use_item",
        ):
            _do_aoo(threatener, actor, grid, events,
                    encounter=encounter)
            if not actor.is_alive() or actor.current_hp <= -10:
                events.append(TurnEvent(actor.id, "skip",
                                        {"reason": "killed by AoO"}))
                return
        events.append(TurnEvent(actor.id, "retrieve_stowed_item",
                                {"item": move.get("item")}))
    else:
        raise NotImplementedError(f"move action {mtype!r} not implemented")


def _do_5ft_step(
    actor: Combatant,
    target: tuple[int, int] | str,
    grid: Grid,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    if isinstance(target, str):
        # Named direction like "north", or expression evaluated to square.
        target = _coerce_square(target) or _direction_to_square(actor, target)
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "5ft_step: invalid target"}))
        return
    old = actor.position
    try:
        grid.move(actor, target)  # type: ignore[arg-type]
        events.append(TurnEvent(actor.id, "move",
                                {"kind": "5ft_step", "from": old, "to": target}))
    except Exception as e:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"5ft_step blocked: {e}"}))


def _move_along(
    actor: Combatant,
    dest: tuple[int, int] | None,
    max_squares: int,
    grid: Grid,
    events: list[TurnEvent],
    encounter=None,
    skip_aoo_first_step: bool = False,
) -> None:
    """Move along a path with AoO triggers per step.

    ``skip_aoo_first_step``: when True, the first square of movement
    doesn't provoke AoOs from threateners. Used by withdraw (PF1 RAW:
    "the square you start in is not considered threatened, and you
    do not provoke an AoO when leaving that square").
    """
    if dest is None or dest == actor.position:
        return
    cur = actor.position
    steps_taken = 0
    while steps_taken < max_squares and cur != dest:
        next_step = _step_toward_passable(cur, dest, grid)
        if next_step == cur:
            break  # truly blocked — no passable neighbor closer to dest
        # AoO check: is the actor leaving a square threatened by hostiles?
        # Skip the first step's AoO when withdrawing.
        if not (skip_aoo_first_step and steps_taken == 0):
            triggers = aoo_triggers_for_movement(grid, actor, cur)
            for threatener in triggers:
                _do_aoo(threatener, actor, grid, events, encounter=encounter)
                if not actor.is_alive() or actor.current_hp <= -10:
                    events.append(TurnEvent(actor.id, "skip",
                                            {"reason": "killed by AoO"}))
                    return
        # Commit the step.
        try:
            grid.move(actor, next_step)
        except Exception as e:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": f"move blocked: {e}"}))
            return
        events.append(TurnEvent(actor.id, "move",
                                {"kind": "step", "from": cur, "to": next_step}))
        # If this combatant carries a rider, the rider's position
        # tracks the mount's anchor.
        if actor.rider_id is not None:
            rider = grid.combatants.get(actor.rider_id)
            if rider is None:
                # Rider is off-grid (typical when mounted); update directly.
                # We can't look it up via grid; the caller (if it has a
                # reference) is expected to find this state via mount.rider_id.
                pass
            else:
                rider.position = next_step
        # Difficult terrain: cost the step at the feature's
        # movement_cost_multiplier (rounded up). PF1 RAW: each square
        # of difficult terrain counts as 2 squares of movement.
        f = grid.feature_at(*next_step)
        if f is not None and f.movement_cost_multiplier > 1.0:
            extra = int(f.movement_cost_multiplier) - 1
            steps_taken += extra
        cur = next_step
        steps_taken += 1


def _step_toward(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    """Naive step toward b — no grid awareness, no obstacle handling."""
    dx = (b[0] > a[0]) - (b[0] < a[0])
    dy = (b[1] > a[1]) - (b[1] < a[1])
    return (a[0] + dx, a[1] + dy)


def _step_toward_passable(
    a: tuple[int, int],
    b: tuple[int, int],
    grid: Grid,
    blocked: set[tuple[int, int]] | None = None,
) -> tuple[int, int]:
    """Pick the best passable adjacent square that brings us closer to b.

    Considers all 8 neighbors. Prefers the one with the smallest PF1
    grid distance to ``b``; ties broken by Euclidean distance (so true
    diagonals win when they're geometrically closer). If no neighbor is
    passable, returns ``a`` (caller should treat as blocked).

    ``blocked`` is an optional set of squares the caller wants treated
    as impassable beyond what ``grid.is_passable`` reports (useful for
    avoiding other combatants on the same path).
    """
    if a == b:
        return a
    blocked = blocked or set()
    candidates: list[tuple[int, float, tuple[int, int]]] = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = a[0] + dx, a[1] + dy
            if not grid.in_bounds(nx, ny):
                continue
            if (nx, ny) in blocked:
                continue
            if not grid.is_passable(nx, ny):
                continue
            grid_d = grid.distance_squares((nx, ny), b)
            euclid_sq = (b[0] - nx) ** 2 + (b[1] - ny) ** 2
            candidates.append((grid_d, euclid_sq, (nx, ny)))
    if not candidates:
        return a
    candidates.sort()
    return candidates[0][2]


def _square_toward(
    actor: Combatant, target: Any, max_squares: int, grid: Grid,
) -> tuple[int, int]:
    """Find a square within max_squares of actor's position, toward target.

    Uses passable-aware stepping: routes around obstacles by preferring
    the neighbor with the smallest grid-distance to the target. Stops
    when no step strictly reduces the distance (i.e., already adjacent
    or stuck), and never lands on the target square.
    """
    if hasattr(target, "position"):
        tpos = target.position
    elif isinstance(target, tuple):
        tpos = target
    else:
        return actor.position
    cur = actor.position
    cur_dist = grid.distance_squares(cur, tpos)
    for _ in range(max_squares):
        nxt = _step_toward_passable(cur, tpos, grid)
        if nxt == cur:
            break
        nxt_dist = grid.distance_squares(nxt, tpos)
        if nxt_dist >= cur_dist:
            break  # no closer than where we are
        if nxt_dist == 0:
            break  # would land on the target itself
        cur = nxt
        cur_dist = nxt_dist
    return cur


def _square_away(
    actor: Combatant, target: Any, max_squares: int, grid: Grid,
) -> tuple[int, int]:
    """Find a square within max_squares, moving away from target."""
    if hasattr(target, "position"):
        tpos = target.position
    elif isinstance(target, tuple):
        tpos = target
    else:
        return actor.position
    cur = actor.position
    for _ in range(max_squares):
        # Step in the direction opposite of target.
        dx = (cur[0] > tpos[0]) - (cur[0] < tpos[0])
        dy = (cur[1] > tpos[1]) - (cur[1] < tpos[1])
        nxt = (cur[0] + dx, cur[1] + dy)
        if nxt == cur:
            break
        if not grid.in_bounds(*nxt) or not grid.is_passable(*nxt):
            break
        cur = nxt
    return cur


def _direction_to_square(actor: Combatant, direction: str) -> tuple[int, int] | None:
    deltas = {
        "north": (0, -1), "south": (0, 1),
        "east": (1, 0),   "west": (-1, 0),
        "northeast": (1, -1), "northwest": (-1, -1),
        "southeast": (1, 1),  "southwest": (-1, 1),
    }
    d = deltas.get(direction)
    if d is None:
        return None
    return (actor.position[0] + d[0], actor.position[1] + d[1])


# ---------------------------------------------------------------------------
# Standard / full-round actions
# ---------------------------------------------------------------------------


def _do_charge(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """PF1 charge action.

    Rules enforced here:
      * Must have a valid target.
      * Must start at least 2 squares (10 ft) from the target — can't
        charge from melee.
      * Path must be a straight line along one of the 8 cardinal /
        diagonal axes (PF1 RAW: "directly toward the designated
        opponent").
      * No allies, enemies, or impassable cells in the charge lane —
        the actor walks in a straight line and stops if any cell on
        the line is blocked.
      * Must actually move at least 2 squares.
      * Must end adjacent to the target.
      * On success: +2 to attack (the -2 AC penalty is not modeled as
        a separate debuff in v1).

    Not yet enforced: difficult terrain in the lane (engine doesn't
    model terrain types yet — when it does, ``_charge_path_clear``
    will need a "no difficult cells" check).
    """
    target = _resolve_target(args.get("target"), ns)
    if target is None:
        events.append(TurnEvent(actor.id, "skip", {"reason": "charge: no target"}))
        return

    # PF1: charge requires moving at least 2 squares. If we're already
    # within 1 square of the target, charging is illegal.
    start_distance = grid.distance_between(actor, target)
    if start_distance < 2:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "charge: target too close — already in melee "
                      "(must start >= 2 squares from target)",
            "distance": start_distance,
        }))
        return

    speed_squares = _movement_squares(actor, encounter)
    # Partial charge uses 1× speed; regular charge uses 2× speed.
    if "max_squares_override" in args:
        charge_squares = int(args["max_squares_override"])
    else:
        charge_squares = speed_squares * 2  # charge = up to 2x speed

    line = _straight_line_charge_path(
        actor.position, target.position, charge_squares, grid,
    )
    if line is None:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "charge: target not on a straight line "
                      "(must be along an orthogonal or diagonal axis "
                      "within charge range)",
        }))
        return

    path_cells = line[1:]  # everything after the start position
    if not _charge_path_clear(path_cells, grid, mover=actor):
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "charge: path blocked (impassable terrain or "
                      "another combatant in the lane)",
        }))
        return

    # Walk the straight-line path one cell at a time. AoOs trigger as
    # the actor leaves each square, just like normal movement.
    start_pos = actor.position
    prev = start_pos
    for next_cell in path_cells:
        triggers = aoo_triggers_for_movement(grid, actor, prev)
        for threatener in triggers:
            _do_aoo(threatener, actor, grid, events, encounter=encounter)
            if not actor.is_alive() or actor.current_hp <= -10:
                events.append(TurnEvent(actor.id, "skip",
                                        {"reason": "killed by AoO"}))
                return
        try:
            grid.move(actor, next_cell)
        except Exception as e:
            events.append(TurnEvent(actor.id, "skip", {
                "reason": f"charge: move blocked mid-path: {e}",
            }))
            return
        events.append(TurnEvent(actor.id, "move", {
            "kind": "charge_step", "from": prev, "to": next_cell,
        }))
        prev = next_cell

    moved_squares = grid.distance_squares(start_pos, actor.position)
    if moved_squares < 2:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": f"charge: moved only {moved_squares} square(s); "
                      f"minimum 2",
            "from": list(start_pos),
            "to": list(actor.position),
        }))
        return

    if not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "charge: target not adjacent after move"}))
        return
    # Brace trigger: if the target is bracing AND has a brace-flagged
    # weapon, they get to attack the charger first with doubled
    # damage. RAW: brace deals double damage on a successful hit
    # against a charging foe. DSL v2 Phase 3.2: this is a reactive
    # interrupt — the bracer's registered Picker chooses Brace or
    # PassBrace; default is Brace (preserves v1 behavior).
    if (
        "bracing" in target.conditions
        and target.attack_options
        and encounter is not None
    ):
        brace_until = target.resources.get("bracing_until_round")
        if brace_until is None or encounter.round_number <= brace_until:
            target_main = target.held_items.get("main_hand")
            if target_main is not None:
                from .content import default_registry
                try:
                    target_w = default_registry().get_weapon(
                        target_main.item_id,
                    )
                except Exception:
                    target_w = None
                if target_w is not None and target_w.has_brace:
                    from .actions import Brace as _Brace, PassBrace as _PassBrace
                    legal: list = [
                        _Brace(actor_id=target.id, charger_id=actor.id),
                        _PassBrace(actor_id=target.id, charger_id=actor.id),
                    ]
                    bracer_picker = encounter.pickers.get(target.id)
                    if bracer_picker is None:
                        chosen = legal[0]  # Default: spring the brace.
                    else:
                        from .actions import GameState as _GameState
                        st = _GameState(encounter=encounter, grid=grid)
                        chosen = bracer_picker.pick(target, st, legal)
                    if isinstance(chosen, _Brace):
                        _do_attack(
                            target, actor, grid, roller, events,
                            label="brace_attack",
                            encounter=encounter,
                            script_options={"charge_damage_multiplier": 2},
                        )
                        target.remove_condition("bracing")
                        target.resources.pop("bracing_until_round", None)
                        if not actor.is_alive() or actor.current_hp <= -10:
                            events.append(TurnEvent(actor.id, "skip", {
                                "reason": "killed by brace attack",
                            }))
                            return
                    else:
                        # PassBrace: emit a trace event; the bracing
                        # condition stays set so a later charger may
                        # still trigger it this round.
                        events.append(TurnEvent(target.id, "brace_pass", {
                            "charger_id": actor.id,
                        }))
    # PF1 RAW: a lance wielded one-handed in the same hand as a mount's
    # reins doubles damage on a charge. Spirited Charge feat doubles
    # the multiplier (×3 total with a lance). We mark the charge so
    # _do_attack can apply the appropriate multiplier.
    chosen = actor.attack_options[0] if actor.attack_options else {}
    is_mounted = actor.mount_id is not None
    is_lance = chosen.get("weapon_id") == "lance"
    options = dict(args.get("options") or {})
    if is_mounted and is_lance:
        if _has_feat(actor, "spirited_charge"):
            options["charge_damage_multiplier"] = 3
        else:
            options["charge_damage_multiplier"] = 2
    elif is_mounted and _has_feat(actor, "spirited_charge"):
        # Spirited Charge: ×2 on any charge weapon while mounted.
        options["charge_damage_multiplier"] = 2
    # Powerful Charge: doubled damage on a designated natural attack
    # (typically gore) when charging. Modeled by routing through the
    # standard charge-damage-multiplier pathway.
    if _has_racial_trait(actor, "powerful_charge"):
        # Look for a "gore" attack or fall back to the first option.
        gore_idx = next(
            (i for i, o in enumerate(actor.attack_options or [])
             if str(o.get("name", "")).lower() == "gore"),
            0,
        )
        options.setdefault("charge_damage_multiplier", 2)
        attack_index = gore_idx
    else:
        attack_index = 0
    # Pounce: on a charge, the creature can make a full attack instead
    # of a single attack. We resolve this by issuing a follow-up
    # full_attack after the initial charge attack.
    has_pounce = _has_racial_trait(actor, "pounce")
    _do_attack(actor, target, grid, roller, events,
               attack_bonus_delta=2, label="charge_attack",
               encounter=encounter,
               script_options=options,
               attack_index=attack_index)
    if has_pounce and target.is_alive() and len(actor.attack_options or []) > 1:
        # Each remaining natural attack fires once on a charge with
        # pounce (RAW: full attack on charge). +2 charge bonus applies.
        for idx in range(1, len(actor.attack_options)):
            if not target.is_alive():
                break
            _do_attack(actor, target, grid, roller, events,
                       attack_bonus_delta=2, label="pounce_attack",
                       encounter=encounter,
                       script_options=options,
                       attack_index=idx)
    # Ride-By Attack: if the actor is mounted and has the feat AND the
    # caller requested a ride-by, continue moving along the charge line
    # past the target for the remaining squares of the actor's charge
    # capacity. The mount moves "through" the target's square — we
    # skip over it as a single step since ride-by-attack semantically
    # describes the mount continuing past the foe.
    if (
        is_mounted
        and args.get("ride_by")
        and _has_feat(actor, "ride_by_attack")
        and actor.is_alive()
    ):
        remaining = charge_squares - moved_squares
        if remaining > 0:
            # Direction = same unit vector as the charge line.
            sx, sy = start_pos
            tx, ty = target.position
            ux = (tx > sx) - (tx < sx)
            uy = (ty > sy) - (ty < sy)
            cur = actor.position
            target_pos = target.position
            for _ in range(remaining):
                next_cell = (cur[0] + ux, cur[1] + uy)
                # Skip the target's square — the mount rides through it.
                # Resolve target-passthrough before any passability/
                # occupancy checks so the target itself doesn't block.
                if next_cell == target_pos:
                    next_cell = (next_cell[0] + ux, next_cell[1] + uy)
                if not grid.in_bounds(*next_cell):
                    break
                # Use the feature check rather than is_passable, since
                # is_passable also rejects occupied squares (which we
                # already handle separately below).
                f = grid.feature_at(*next_cell)
                if f is not None and f.blocks_movement:
                    break
                if grid._occupancy.get(next_cell) is not None:
                    break
                # PF1 RAW: Ride-By Attack lets the rider continue
                # past the target without provoking AoOs from the
                # target. Other threateners' AoOs still trigger
                # normally.
                triggers = [
                    t for t in aoo_triggers_for_movement(grid, actor, cur)
                    if t.id != target.id
                ]
                for threatener in triggers:
                    _do_aoo(threatener, actor, grid, events,
                            encounter=encounter)
                    if not actor.is_alive() or actor.current_hp <= -10:
                        events.append(TurnEvent(actor.id, "skip",
                                                {"reason": "killed by AoO"}))
                        return
                try:
                    grid.move(actor, next_cell)
                except Exception:
                    break
                events.append(TurnEvent(actor.id, "move", {
                    "kind": "ride_by_step", "from": cur, "to": next_cell,
                }))
                cur = next_cell


def _straight_line_charge_path(
    start: tuple[int, int],
    target_pos: tuple[int, int],
    max_steps: int,
    grid: Grid,
) -> list[tuple[int, int]] | None:
    """Compute the straight-line cells the charger walks, or ``None``.

    PF1 charge requires the actor to move "directly toward" the target.
    We interpret that as: the displacement from the start to the
    destination square (which sits adjacent to the target) must be a
    positive integer multiple of one of the 8 unit directions
    (orthogonal or diagonal).

    Returns the full path *including* the start cell. ``path[0]`` is
    ``start``; ``path[-1]`` is the cell adjacent to ``target_pos``
    that the actor ends on. Returns ``None`` if no valid line exists
    or if the line exceeds ``max_steps``.
    """
    sx, sy = start
    tx, ty = target_pos
    dx_total = tx - sx
    dy_total = ty - sy
    if dx_total == 0 and dy_total == 0:
        return None
    # Straight-line constraint: displacement is n * (ux, uy) with
    # ux, uy ∈ {-1, 0, 1}. Equivalent: orthogonal (one of dx/dy is 0)
    # OR pure diagonal (|dx| == |dy|).
    if dx_total != 0 and dy_total != 0 and abs(dx_total) != abs(dy_total):
        return None
    ux = (dx_total > 0) - (dx_total < 0)
    uy = (dy_total > 0) - (dy_total < 0)
    # Steps to reach a cell adjacent to target along this line.
    n_steps = max(abs(dx_total), abs(dy_total)) - 1
    if n_steps < 1:
        return None
    if n_steps > max_steps:
        return None
    path: list[tuple[int, int]] = [start]
    for i in range(1, n_steps + 1):
        cell = (sx + i * ux, sy + i * uy)
        if not grid.in_bounds(*cell):
            return None
        path.append(cell)
    return path


def _charge_path_clear(
    cells: list[tuple[int, int]],
    grid: Grid,
    *,
    mover: Combatant,
) -> bool:
    """All cells in ``cells`` must be passable, unoccupied (other than
    by ``mover``), and free of difficult terrain.

    PF1 RAW: a charge cannot pass through any square that hampers
    movement (difficult terrain, water, etc.).
    """
    for cell in cells:
        if not grid.is_passable(*cell):
            return False
        f = grid.feature_at(*cell)
        if f is not None and f.movement_cost_multiplier > 1.0:
            return False  # difficult terrain blocks a charge
        for c in grid.combatants.values():
            if c.id == mover.id:
                continue
            if c.position == cell:
                return False
    return True


def _iterative_attack_count(bab: int) -> int:
    """Number of iterative attacks PF1 grants at this BAB.

    PF1 RAW: 1 attack at BAB 0-5, 2 at 6-10, 3 at 11-15, 4 at 16+.
    Always at least 1 even at BAB 0 (everyone gets a single attack).
    Each iterative beyond the first takes an additional -5 cumulative.
    """
    return max(1, (bab - 1) // 5 + 1)


def _do_full_attack(
    actor: Combatant,
    target: Combatant,
    options: dict,
    grid: Grid,
    roller: Roller,
    events: list[TurnEvent],
    encounter=None,
) -> None:
    # Adjacency only required for melee weapons. Ranged full attacks
    # (e.g., a longbow user) can fire from any range; range increments
    # apply per-attack.
    primary_is_ranged = (
        bool(actor.attack_options)
        and actor.attack_options[0].get("type") == "ranged"
    )
    if not primary_is_ranged and not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "full_attack: target not in melee"}))
        return
    # RAW: a ranged full attack provokes one AoO for the action (not per
    # iterative shot). Per-shot triggers are suppressed inside _do_attack
    # by gating on label.
    if primary_is_ranged:
        if _provoke_ranged_aoo(actor, grid, events, encounter):
            return
    bab = actor.bases.get("bab", 0)
    # Build the (delta, attack_index) sequence for this full attack.
    # Default: primary-only iteratives at 0, -5, -10, ... using
    # attack_options[0].
    #
    # Rapid Shot inserts an extra primary attack at top BAB and applies
    # -2 to every primary attack this round.
    #
    # Two-Weapon Fighting adds an off-hand attack (using the off-hand
    # attack_option, identified by ``is_offhand: True``) and applies
    # paired penalties to BOTH primary and off-hand attacks based on
    # the TWF feat and off-hand wield class.
    primary_deltas = [-5 * i for i in range(_iterative_attack_count(bab))]
    rapid_shot_active = (
        bool(options and options.get("rapid_shot"))
        and _has_feat(actor, "rapid_shot")
        and bool(actor.attack_options)
        and actor.attack_options[0].get("type") == "ranged"
    )
    if rapid_shot_active:
        primary_deltas = [0] + primary_deltas
        primary_deltas = [d - 2 for d in primary_deltas]

    # RAW (Flurry of Blows): full-attack with one extra attack at the
    # top BAB and -2 to all attack rolls (TWF-style). The monk's
    # base attack bonus from his monk class levels is treated as equal
    # to his monk level for these attacks. RAW: "These attacks can be
    # any combination of unarmed strikes and attacks with a monk
    # special weapon" — gated on _MONK_FLURRY_WEAPONS below.
    # At higher levels: 2 extra attacks at L8, 3 at L15.
    flurry_active = (
        bool(options and options.get("flurry"))
        and bool(actor.attack_options)
        and actor.attack_options[0].get("weapon_id") in _MONK_FLURRY_WEAPONS
        and actor.class_levels.get("monk", 0) > 0
    )
    flurry_substitutions: list = []
    if flurry_active:
        monk_level = actor.class_levels["monk"]
        # RAW: "the monk's base attack bonus from his monk class levels
        # is equal to his monk level" — for these attacks. The
        # attack-option's attack_bonus was computed using the actor's
        # actual BAB, so we apply a per-attack delta of (monk_level -
        # actor_bab) to swap in the flurry BAB. For pure-class monks
        # past L8 this is +0; below L8 it's a positive bump.
        flurry_bab_bonus = monk_level - bab
        primary_deltas = [
            -5 * i for i in range(_iterative_attack_count(monk_level))
        ]
        # Extra flurry attacks: 1 at L1-7, 2 at L8-14, 3 at L15+.
        if monk_level >= 15:
            extras = 3
        elif monk_level >= 8:
            extras = 2
        else:
            extras = 1
        primary_deltas = [0] * extras + primary_deltas
        # Apply the -2 TWF-style penalty + BAB swap-in to all flurry
        # attacks.
        primary_deltas = [d + flurry_bab_bonus - 2 for d in primary_deltas]
        # RAW: "A monk may substitute disarm, sunder, and trip combat
        # maneuvers for unarmed attacks as part of a flurry of blows."
        # ``options.flurry_substitutions`` is a per-position list of
        # maneuver kinds (or None for "normal attack"). Validated
        # against the RAW menu of three.
        raw_subs = list(options.get("flurry_substitutions") or [])
        for i, sub in enumerate(raw_subs):
            if sub is None:
                continue
            if sub not in _FLURRY_SUBSTITUTABLE_MANEUVERS:
                events.append(TurnEvent(actor.id, "skip", {
                    "reason": "flurry: substitution kind not in RAW "
                              "menu (trip/disarm/sunder)",
                    "kind": sub, "position": i,
                }))
                return
        flurry_substitutions = raw_subs

    twf_active = (
        bool(options and options.get("two_weapon_fighting"))
        and bool(actor.attack_options)
        and any(a.get("is_offhand") for a in actor.attack_options)
        # Off-hand attacks are melee in our v1; ranged TWF (e.g.
        # bow + buckler crossbow) isn't modeled.
        and actor.attack_options[0].get("type") == "melee"
    )
    offhand_index = -1
    twf_primary_pen = 0
    twf_offhand_pen = 0
    if twf_active:
        for i, opt in enumerate(actor.attack_options):
            if opt.get("is_offhand"):
                offhand_index = i
                break
        offhand_is_light = (
            actor.attack_options[offhand_index].get("wield") == "light"
        )
        has_twf_feat = _has_feat(actor, "two_weapon_fighting")
        if has_twf_feat and offhand_is_light:
            twf_primary_pen = -2
            twf_offhand_pen = -2
        elif has_twf_feat:
            twf_primary_pen = -4
            twf_offhand_pen = -8
        else:
            # Dual-wielding without the feat: -6 / -10 per RAW.
            twf_primary_pen = -6
            twf_offhand_pen = -10

    # Natural-attack chain: when every melee attack option is flagged
    # is_natural, each one fires once (PF1 RAW: primary at full BAB,
    # secondary at BAB-5; v1 simplification fires all at full BAB).
    # RAW (Flurry of Blows): "A monk with natural weapons cannot use
    # such weapons as part of a flurry of blows, nor can he make
    # natural attacks in addition to his flurry of blows attacks."
    # Suppress the natural-attack chain entirely when flurry is active.
    natural_indices = [
        i for i, opt in enumerate(actor.attack_options or [])
        if opt.get("type") == "melee" and opt.get("is_natural")
    ]
    if len(natural_indices) > 1 and not flurry_active:
        schedule: list[tuple[int, int]] = [(0, i) for i in natural_indices]
    else:
        schedule = [(d + twf_primary_pen, 0) for d in primary_deltas]
        if twf_active:
            # One off-hand attack at the top BAB (no -5 iterative for the
            # off-hand without Improved/Greater TWF, both deferred to v2).
            schedule.append((twf_offhand_pen, offhand_index))

    has_rend = _has_racial_trait(actor, "rend")
    # DSL v2 Phase 4: between iteratives, a sub-action decision-point
    # asks the actor's picker whether to Continue / End / Retarget.
    # Default behavior (no picker, or no matching ``sub: full_attack``
    # rule) preserves v1: continue while the target is alive, stop on
    # death/dying. Rend tracking is per-target (a dict indexed by the
    # target's id) so retargeting doesn't smear claw-hit counts across
    # creatures.
    from .actions import (
        ContinueFullAttack as _Cont, EndFullAttack as _End,
        RetargetFullAttack as _Retarget,
        GameState as _GameState,
    )
    claw_hits_by_target: dict[str, int] = {}
    for i, (delta, idx) in enumerate(schedule):
        if i > 0:
            target_alive = target.is_alive() and target.current_hp > 0
            # Build the sub-action legal list and consult the picker.
            # Retarget candidates: any other live foe legitimately
            # attackable from here. For melee primaries only adjacent
            # foes; for ranged, anyone visible.
            sub_legal: list = [
                _Cont(actor_id=actor.id, target_id=target.id),
                _End(actor_id=actor.id, target_id=target.id),
            ]
            for foe in grid.combatants.values():
                if foe.id == actor.id or foe.id == target.id:
                    continue
                if foe.team == actor.team:
                    continue
                if not foe.is_alive() or "dead" in foe.conditions:
                    continue
                if not primary_is_ranged and not grid.is_adjacent(actor, foe):
                    continue
                sub_legal.append(_Retarget(
                    actor_id=actor.id, new_target_id=foe.id,
                ))
            picker = (encounter.pickers.get(actor.id)
                      if encounter is not None else None)
            if picker is None:
                # Default: v1 break-when-target-down semantics.
                chosen = sub_legal[1] if not target_alive else sub_legal[0]
            else:
                st = _GameState(encounter=encounter, grid=grid)
                chosen = picker.pick(actor, st, sub_legal)
            if isinstance(chosen, _End):
                break
            if isinstance(chosen, _Retarget):
                new_target = grid.combatants.get(chosen.new_target_id)
                if new_target is not None:
                    target = new_target
                # Note: we do NOT reset claw_hits_by_target — the
                # original target's tally is preserved (in case the
                # picker bounces back to it later) and the new target
                # starts fresh per-target.
            # Continue: keep target as-is.
        else:
            # First iterative — no sub-decision yet (the action itself
            # was the FullAttack pick at the active-turn layer).
            if not target.is_alive() or target.current_hp <= 0:
                break
        hp_before = target.current_hp
        # RAW (Flurry of Blows): "A monk may substitute disarm, sunder,
        # and trip combat maneuvers for unarmed attacks as part of a
        # flurry of blows." When a position has a substitution, dispatch
        # _do_combat_maneuver instead of _do_attack — the same flurry
        # delta is fed in as cmb_delta so the maneuver's CMB roll
        # carries the BAB swap-in and -2 TWF penalty.
        sub_kind = (flurry_substitutions[i]
                    if (flurry_active and i < len(flurry_substitutions))
                    else None)
        if sub_kind is not None:
            _do_combat_maneuver(
                actor, sub_kind,
                {"target": target},
                encounter, grid, roller, ns={}, events=events,
                cmb_delta=delta,
            )
        else:
            _do_attack(actor, target, grid, roller, events,
                       attack_bonus_delta=delta,
                       label=f"full_attack_{i+1}",
                       encounter=encounter,
                       script_options=options,
                       attack_index=idx)
        # Track claw hits per-target for the rend rider (troll, etc.).
        # A claw is any attack option whose ``name`` starts with "claw".
        if has_rend and idx < len(actor.attack_options):
            attack_name = str(actor.attack_options[idx].get("name", "")).lower()
            if attack_name.startswith("claw") and target.current_hp < hp_before:
                claw_hits_by_target[target.id] = (
                    claw_hits_by_target.get(target.id, 0) + 1
                )
    # PF1 troll rend: +1d6+1 damage to any target this turn that took
    # 2+ claw hits and is still alive. With per-target tracking, a
    # full-attack that retargeted to a second creature can rend each
    # creature independently if it landed both claws on each.
    if has_rend:
        for tid, count in claw_hits_by_target.items():
            if count < 2:
                continue
            rend_target = grid.combatants.get(tid)
            if rend_target is None or not rend_target.is_alive():
                continue
            rend_roll = roller.roll("1d6")
            rend_damage = int(rend_roll.total) + 1
            rend_target.take_damage(rend_damage)
            _apply_post_damage_state(rend_target)
            events.append(TurnEvent(actor.id, "rend", {
                "target_id": rend_target.id,
                "damage": rend_damage,
                "die_roll": int(rend_roll.total),
            }))


_DIRECTION_DELTAS: dict[str, tuple[int, int]] = {
    "north":     (0, -1),
    "south":     (0, 1),
    "east":      (1, 0),
    "west":      (-1, 0),
    "northeast": (1, -1),
    "northwest": (-1, -1),
    "southeast": (1, 1),
    "southwest": (-1, 1),
}


def _square_in_direction(
    actor: Combatant, direction: str, distance: int,
) -> tuple[int, int] | None:
    delta = _DIRECTION_DELTAS.get(direction)
    if delta is None:
        return None
    return (
        actor.position[0] + delta[0] * distance,
        actor.position[1] + delta[1] * distance,
    )


def _do_withdraw(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    events: list[TurnEvent],
) -> None:
    direction = args.get("direction", "south")
    speed_squares = _movement_squares(actor, encounter)
    withdraw_squares = speed_squares * 2
    dest = _square_in_direction(actor, direction, withdraw_squares)
    if dest is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"withdraw: bad direction {direction!r}"}))
        return
    # Withdraw: first square of movement doesn't provoke AoOs.
    _move_along(
        actor, dest, withdraw_squares, grid, events,
        encounter=encounter, skip_aoo_first_step=True,
    )


def _do_mount(
    actor: Combatant,
    args: dict,
    grid: Grid,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Mount an adjacent creature.

    PF1 RAW: a mount must be at least one size larger than the rider
    (size restriction not enforced here in v1; callers are expected to
    pair compatible creatures). Mounting is a move action that requires
    the mount to be willing or unwilling-but-not-resisting.

    On success: the rider is removed from the grid (mount and rider
    share a square conceptually); the rider's ``position`` mirrors the
    mount's; ``mount_id`` / ``rider_id`` cross-reference is established.
    """
    if actor.mount_id is not None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "mount: already mounted"}))
        return
    target = _resolve_target(args.get("target"), ns)
    if target is None or not isinstance(target, Combatant):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "mount: no target resolved"}))
        return
    if target.rider_id is not None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "mount: target already carries a rider"}))
        return
    if not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "mount: target not adjacent"}))
        return
    actor.mount_id = target.id
    target.rider_id = actor.id
    actor.position = target.position
    # Clear the rider's occupancy without removing them from the grid's
    # combatant dict. The rider is conceptually in the mount's square;
    # they stay reachable via grid.combatants for movement-tracking but
    # don't block placement.
    for sq in [s for s, cid in grid._occupancy.items() if cid == actor.id]:
        del grid._occupancy[sq]
    events.append(TurnEvent(actor.id, "mount", {
        "mount_id": target.id, "position": list(target.position),
    }))


def _do_dismount(
    actor: Combatant,
    args: dict,
    grid: Grid,
    events: list[TurnEvent],
) -> None:
    """Step off the mount into a square adjacent to it.

    PF1 RAW: dismounting is a move action; emergency dismount with a
    Ride DC 20 check is not modeled here. Picks the first passable
    adjacent square; emits ``skip`` if no adjacent square is free.
    """
    mount_id = actor.mount_id
    if mount_id is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "dismount: not mounted"}))
        return
    mount = grid.combatants.get(mount_id)
    mount_pos = mount.position if mount is not None else actor.position
    # Find an adjacent passable square.
    chosen: tuple[int, int] | None = None
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            sq = (mount_pos[0] + dx, mount_pos[1] + dy)
            if not grid.in_bounds(*sq):
                continue
            if not grid.is_passable(*sq):
                continue
            if grid._occupancy.get(sq) is not None:
                continue
            chosen = sq
            break
        if chosen is not None:
            break
    if chosen is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "dismount: no adjacent free square"}))
        return
    actor.mount_id = None
    if mount is not None:
        mount.rider_id = None
    actor.position = chosen
    # Re-establish occupancy at the chosen square. ``place`` would also
    # re-add to combatants (already there) and validate the footprint.
    grid.place(actor)
    events.append(TurnEvent(actor.id, "dismount", {
        "mount_id": mount_id, "position": list(chosen),
    }))


def _do_coup_de_grace(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """PF1 coup de grace: full-round action against a helpless target.

    The attack auto-hits, is automatically a critical, and the target
    must make a Fortitude save (DC 10 + damage dealt) or die outright.

    Provokes AoOs from threateners (handled implicitly — the actor's
    full-round action shouldn't be triggering a movement step here, so
    we just resolve the attack).
    """
    target = _resolve_target(args.get("target"), ns)
    if target is None or not isinstance(target, Combatant):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "coup_de_grace: no target"}))
        return
    if not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "coup_de_grace: target not adjacent",
        }))
        return
    is_helpless = bool(target.conditions & {
        "helpless", "paralyzed", "sleeping", "unconscious", "pinned",
    })
    if not is_helpless:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "coup_de_grace: target not helpless",
        }))
        return
    if not actor.attack_options:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "coup_de_grace: no attack options"}))
        return
    chosen = actor.attack_options[0]
    # Roll damage as if a critical hit (apply crit multiplier).
    crit_mult = int(chosen.get("crit_multiplier", 2))
    dmg_dice = str(chosen["damage"])
    dmg_bonus = int(chosen.get("damage_bonus", 0))
    total_damage = 0
    for _ in range(crit_mult):
        r = roller.roll(dmg_dice)
        total_damage += r.total
    total_damage += dmg_bonus * crit_mult
    target.take_damage(max(0, total_damage))
    _apply_post_damage_state(target)
    # Fortitude save vs DC 10 + damage.
    save_dc = 10 + total_damage
    save_total = target.save("fort")
    sr = roller.roll("1d20")
    nat = sr.terms[0].rolls[0]
    save_passed = (nat == 20) or (nat != 1 and nat + save_total >= save_dc)
    killed_by_save = False
    if not save_passed:
        target.add_condition("dead")
        killed_by_save = True
    events.append(TurnEvent(actor.id, "coup_de_grace", {
        "target_id": target.id,
        "damage": total_damage,
        "save_dc": save_dc,
        "save_natural": nat,
        "save_total": nat + save_total,
        "save_passed": save_passed,
        "killed_by_save": killed_by_save,
    }))


def _do_partial_charge(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """PF1 partial charge: a charge limited to the actor's normal speed
    (instead of 2× speed). Used as a standard action when a full-round
    isn't available (disabled, staggered, etc.).

    Otherwise identical to a regular charge — same target / line / lane
    rules. We delegate to ``_do_charge`` with a ``max_squares_override``
    arg.
    """
    args = dict(args)
    args["max_squares_override"] = actor.speed // 5  # 1× speed
    _do_charge(actor, args, encounter, grid, roller, ns, events)


def _resolve_grapple_partner(actor: Combatant, grid: Grid) -> Combatant | None:
    """Look up the actor's grapple partner via grappling_target_id."""
    tid = actor.grappling_target_id
    if not tid:
        return None
    return grid.combatants.get(tid)


def _resolve_grappler(actor: Combatant, grid: Grid) -> Combatant | None:
    """Look up who is grappling the actor via grappled_by_id."""
    gid = actor.grappled_by_id
    if not gid:
        return None
    return grid.combatants.get(gid)


def _do_grapple_damage(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Continue a grapple to deal damage. PF1 RAW: CMB vs grappled
    target's CMD; on success, the grappler deals weapon or natural
    damage as if making a single attack."""
    target = _resolve_grapple_partner(actor, grid)
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "grapple_damage: not grappling anyone"}))
        return
    passed, nat, total, margin = _resolve_maneuver(actor, target,
                                                   "grapple", roller)
    detail = {
        "kind": "grapple_damage", "target_id": target.id,
        "natural": nat, "total": total, "margin": margin,
        "passed": passed,
    }
    if passed and actor.attack_options:
        chosen = actor.attack_options[0]
        dmg_dice = str(chosen.get("damage", "1d4"))
        dmg_bonus = int(chosen.get("damage_bonus", 0))
        r = roller.roll(dmg_dice)
        damage = max(0, r.total + dmg_bonus)
        damage_type = str(chosen.get("damage_type", "")) or None
        target.take_damage(damage, damage_type=damage_type)
        _apply_post_damage_state(target)
        detail["damage"] = damage
    events.append(TurnEvent(actor.id, "grapple_damage", detail))


def _do_grapple_move(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Continue a grapple to move both actor and target up to half
    actor's speed. PF1 RAW: requires CMB vs CMD; the target may attempt
    to break free with a CMB / Escape Artist check."""
    target = _resolve_grapple_partner(actor, grid)
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "grapple_move: not grappling anyone"}))
        return
    passed, nat, total, margin = _resolve_maneuver(actor, target,
                                                   "grapple", roller)
    detail = {
        "kind": "grapple_move", "target_id": target.id,
        "natural": nat, "total": total, "margin": margin,
        "passed": passed,
    }
    if passed:
        direction = args.get("direction", "north")
        max_squares = max(1, (actor.speed // 5) // 2)
        dest = _square_in_direction(actor, direction, max_squares)
        if dest is not None:
            # Try to move actor to dest; if it works, drag target to
            # actor's previous position.
            old_actor_pos = actor.position
            try:
                grid.move(actor, dest)
                # Move target to where actor was.
                try:
                    grid.move(target, old_actor_pos)
                    detail["actor_to"] = list(actor.position)
                    detail["target_to"] = list(target.position)
                except Exception:
                    # Couldn't drag; revert actor.
                    grid.move(actor, old_actor_pos)
                    detail["effect"] = "move_blocked"
            except Exception:
                detail["effect"] = "move_blocked"
    events.append(TurnEvent(actor.id, "grapple_move", detail))


def _do_grapple_pin(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Continue a grapple to pin the target. PF1 RAW: pin is a parallel
    maintain-action (a regular CMB vs CMD check, no +5 DC). On success,
    target gains 'pinned' (which makes them helpless per RAW). The
    grappler's +5 circumstance bonus from holding the grapple in
    subsequent rounds is a separate accounting concern, not a pin DC
    adjustment."""
    target = _resolve_grapple_partner(actor, grid)
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "grapple_pin: not grappling anyone"}))
        return
    cmb = actor.cmb()
    cmd = target.cmd(context={"maneuver": "grapple"})
    r = roller.roll("1d20")
    nat = r.terms[0].rolls[0]
    total = nat + cmb
    passed = total >= cmd
    detail = {
        "kind": "grapple_pin", "target_id": target.id,
        "natural": nat, "total": total, "margin": total - cmd,
        "passed": passed,
    }
    if passed:
        target.add_condition("pinned")
        target.add_condition("helpless")
        detail["effect"] = "pinned"
    events.append(TurnEvent(actor.id, "grapple_pin", detail))


def _do_grapple_break_free(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """The grappled creature attempts to escape. PF1 RAW: standard
    action; the grappled creature rolls CMB or Escape Artist vs the
    grappler's CMB. On success, both lose 'grappled' (and the target
    loses 'pinned' / 'helpless' if pinned).

    The script may pass ``method='cmb'`` (default) or ``'escape_artist'``
    to choose the check. Escape Artist uses skills.skill_check.
    """
    grappler = _resolve_grappler(actor, grid)
    if grappler is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "grapple_break_free: not grappled"}))
        return
    method = args.get("method", "cmb")
    grappler_cmb = grappler.cmb()
    if method == "escape_artist":
        from .skills import skill_check
        from .content import default_registry
        result = skill_check(
            actor, "escape_artist", dc=grappler_cmb, roller=roller,
            registry=default_registry(),
        )
        passed = bool(result.success)
        nat = result.natural
        total = result.total
    else:
        r = roller.roll("1d20")
        nat = r.terms[0].rolls[0]
        total = nat + actor.cmb()
        passed = total >= grappler_cmb
    detail = {
        "kind": "grapple_break_free",
        "grappler_id": grappler.id,
        "method": method,
        "natural": nat,
        "total": total,
        "vs": grappler_cmb,
        "passed": passed,
    }
    if passed:
        # Both lose grappled; target loses pinned/helpless if pinned.
        actor.remove_condition("grappled")
        actor.remove_condition("pinned")
        actor.remove_condition("helpless")
        actor.grappled_by_id = None
        grappler.remove_condition("grappled")
        grappler.grappling_target_id = None
        detail["effect"] = "freed"
    events.append(TurnEvent(actor.id, "grapple_break_free", detail))


def _do_ready_brace(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    events: list[TurnEvent],
) -> None:
    """PF1 ready an action: brace a weapon vs a charge.

    Sets the actor's ``bracing`` condition for one round. When a
    charging foe attacks the bracing wielder, the wielder's first
    attack against that charger deals double damage (handled in
    _do_charge — when the charger ends adjacent to a bracing
    wielder, the bracing wielder gets a free attack with double
    damage).

    For v1 we just set the condition; the trigger fires on the next
    incoming charge attack against this actor. The wielder must have
    a brace-flagged weapon equipped in main_hand.
    """
    main = actor.held_items.get("main_hand")
    if main is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "ready_brace: no weapon in main_hand"}))
        return
    from .content import default_registry
    try:
        w = default_registry().get_weapon(main.item_id)
    except Exception:
        w = None
    if w is None or not getattr(w, "has_brace", False):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "ready_brace: weapon doesn't brace"}))
        return
    cur_round = encounter.round_number if encounter else 1
    # Mark the actor as bracing. Cleared at start of next round via
    # a side-channel; for v1 we just expire it heuristically when
    # _do_charge reads it.
    actor.add_condition("bracing")
    actor.resources["bracing_until_round"] = cur_round + 1
    events.append(TurnEvent(actor.id, "ready_brace", {
        "weapon_id": main.item_id,
        "expires_round": cur_round + 1,
    }))


def _do_fight_defensively(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """PF1 fight defensively: -4 attack for +2 dodge AC for one round.

    Differs from total_defense: with fight_defensively you still get
    to attack (with the -4 penalty); total_defense forfeits attacks.

    For v1: makes a single attack with -4 to-hit and grants a +2 dodge
    AC modifier expiring at the start of the actor's next turn.
    """
    target = _resolve_target(args.get("target"), ns)
    if target is None or not isinstance(target, Combatant):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "fight_defensively: no target"}))
        return
    cur_round = encounter.round_number if encounter else 1
    src = "fight_defensively"
    actor.modifiers.remove_by_source(src)
    actor.modifiers.add(Modifier(
        value=2, type="dodge", target="ac",
        source=src, expires_round=cur_round + 1,
    ))
    events.append(TurnEvent(actor.id, "fight_defensively", {
        "ac_bonus": 2, "expires_round": cur_round + 1,
    }))
    # Single attack with -4 to-hit.
    _do_attack(actor, target, grid, roller, events,
               attack_bonus_delta=-4, label="defensive_attack",
               encounter=encounter,
               script_options=args.get("options") or {})


def _do_trample(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """PF1 Trample feat: while mounted, the rider can declare overruns
    against opponents in the mount's path. Each opponent gets a Reflex
    save (DC 10 + half mount HD + mount Str mod) for half damage from
    the mount's hooves; on failure they're knocked prone.

    For v1 we model this as a single targeted overrun: the rider names
    the target, the mount makes an overrun CMB check (or auto-passes
    per RAW since trample bypasses the standard overrun avoidance),
    and the target rolls Reflex; failure → prone + hoof damage.
    Movement is the rider's responsibility (same as a charge).
    """
    if actor.mount_id is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "trample: not mounted"}))
        return
    if not _has_feat(actor, "trample"):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "trample: requires Trample feat"}))
        return
    target = _resolve_target(args.get("target"), ns)
    if target is None or not isinstance(target, Combatant):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "trample: no target resolved"}))
        return
    mount = grid.combatants.get(actor.mount_id)
    if mount is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "trample: mount not on grid"}))
        return
    if not grid.is_adjacent(mount, target):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "trample: target not adjacent to mount"}))
        return
    # Find a hoof attack on the mount.
    hoof_attack = None
    for opt in mount.attack_options:
        name = (opt.get("name") or "").lower()
        if "hoof" in name or "hooves" in name or opt.get("weapon_id") in (
            "hoof", "hooves",
        ):
            hoof_attack = opt
            break
    if hoof_attack is None and mount.attack_options:
        # Fallback to the mount's primary natural attack.
        hoof_attack = mount.attack_options[0]
    if hoof_attack is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "trample: mount has no attacks"}))
        return
    # Reflex save vs DC 10 + 1/2 mount HD + mount Str mod.
    mount_hd = 1
    if mount.template_kind == "monster" and mount.template is not None:
        hd_str = getattr(mount.template, "hit_dice", "1") or "1"
        try:
            mount_hd = max(1, int(hd_str.split("d")[0]))
        except (ValueError, IndexError):
            mount_hd = 1
    mount_str_mod = 0
    if mount.template_kind == "monster" and mount.template is not None:
        scores = getattr(mount.template, "ability_scores", None) or {}
        mount_str_mod = (int(scores.get("str", 10)) - 10) // 2
    save_dc = 10 + (mount_hd // 2) + mount_str_mod
    save_total = target.save("ref")
    sr = roller.roll("1d20")
    nat = sr.terms[0].rolls[0]
    save_passed = (nat == 20) or (nat != 1 and nat + save_total >= save_dc)
    # Roll hoof damage.
    dmg_dice = str(hoof_attack.get("damage", "1d4"))
    dmg_bonus = int(hoof_attack.get("damage_bonus", 0))
    dr = roller.roll(dmg_dice)
    raw_damage = dr.total + dmg_bonus
    final_damage = raw_damage // 2 if save_passed else raw_damage
    target.take_damage(final_damage)
    _apply_post_damage_state(target)
    if not save_passed:
        target.add_condition("prone")
    events.append(TurnEvent(actor.id, "trample", {
        "target_id": target.id,
        "mount_id": mount.id,
        "save_dc": save_dc,
        "save_natural": nat,
        "save_total": nat + save_total,
        "save_passed": save_passed,
        "damage": final_damage,
        "damage_raw": raw_damage,
        "knocked_prone": not save_passed,
    }))


def _do_run(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    events: list[TurnEvent],
) -> None:
    """PF1 Run: full-round action, 4× speed in a straight line, lose Dex
    bonus to AC until the start of the actor's next turn.

    AoOs trigger normally on each step.
    """
    direction = args.get("direction", "south")
    speed_squares = _movement_squares(actor, encounter)
    run_squares = speed_squares * 4
    dest = _square_in_direction(actor, direction, run_squares)
    if dest is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"run: bad direction {direction!r}"}))
        return

    # Lose Dex bonus to AC until the start of the actor's next turn.
    dex_to_ac = 0
    for m in actor.modifiers.for_target("ac"):
        if m.type == "ability" and "dex" in m.source.lower():
            dex_to_ac += m.value
    cur_round = encounter.round_number if encounter else 1
    src = "running"
    actor.modifiers.remove_by_source(src)
    if dex_to_ac > 0:
        actor.modifiers.add(Modifier(
            value=-dex_to_ac, type="untyped", target="ac",
            source=src, expires_round=cur_round + 1,
        ))
    events.append(TurnEvent(actor.id, "run", {
        "direction": direction,
        "max_squares": run_squares,
        "dex_ac_lost": dex_to_ac,
    }))
    _move_along(actor, dest, run_squares, grid, events, encounter=encounter)


# ---------------------------------------------------------------------------
# Attack resolution
# ---------------------------------------------------------------------------


def _provoke_ranged_aoo(
    actor: Combatant,
    grid: Grid,
    events: list[TurnEvent],
    encounter,
) -> bool:
    """Fire AoOs from threateners against ``actor`` for making a ranged
    attack action. Appends a 'skip: killed by AoO' event and returns
    True if the actor was killed by an AoO; caller should abort the
    action by returning. Returns False otherwise."""
    from .encounter import aoo_triggers_for_provoking_action
    for threatener in aoo_triggers_for_provoking_action(
        grid, actor, "ranged_attack",
    ):
        _do_aoo(threatener, actor, grid, events, encounter=encounter)
        if not actor.is_alive() or actor.current_hp <= -10:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "killed by AoO"}))
            return True
    return False


def _do_attack(
    actor: Combatant,
    target: Combatant,
    grid: Grid,
    roller: Roller,
    events: list[TurnEvent],
    *,
    attack_bonus_delta: int = 0,
    label: str = "attack",
    encounter=None,
    script_options: dict | None = None,
    attack_index: int = 0,
) -> None:
    options = actor.attack_options
    if not options:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "no attack options"}))
        return
    if attack_index < 0 or attack_index >= len(options):
        attack_index = 0
    chosen = options[attack_index]
    is_ranged = chosen.get("type") == "ranged"
    if not is_ranged and not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "attack target not in melee range"}))
        return
    # RAW (Fascinate, Foundry pack ``Fascinate``): "Any obvious threat,
    # such as someone drawing a weapon, casting a spell, or aiming a
    # weapon at the target, automatically breaks the effect." An
    # incoming attack is the canonical obvious threat — clear the
    # condition before resolution so the target isn't still penalized
    # by the -4 reactions while being attacked.
    if "fascinated" in target.conditions:
        target.remove_condition("fascinated")
        events.append(TurnEvent(target.id, "fascinate_broken",
                                {"reason": "attacked",
                                 "attacker_id": actor.id}))
    # Daily-resource gate: a ranged 'spikes' attack from a creature
    # with the tail_spikes trait consumes one of the 24/day pool.
    # When empty, the attack is skipped (the manticore is out of
    # spikes until the daily replenish ticks).
    if (
        chosen.get("type") == "ranged"
        and str(chosen.get("name", "")).lower() == "spikes"
        and _has_racial_trait(actor, "tail_spikes")
    ):
        remaining = int(actor.daily_resources.get("tail_spikes", 0))
        if remaining <= 0:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "tail_spikes: pool empty"}))
            return
        actor.daily_resources["tail_spikes"] = remaining - 1
    # Total cover blocks line of effect for ranged attacks entirely.
    if is_ranged and _total_cover_blocks_line(actor, target, grid):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "total cover blocks line of effect"}))
        return
    # Beyond max range: 5 increments for thrown, 10 for projectile.
    if _out_of_max_range(chosen, actor, target, grid, is_ranged):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "target beyond maximum range"}))
        return

    # RAW: making a ranged attack while in a threatened square provokes
    # an AoO from each threatener. Fired before the shot resolves; if
    # the AoO kills the attacker, the shot is aborted.
    #
    # Only standalone ranged attacks fire the AoO here. Wrapper actions
    # (``full_attack_<i>``, ``tail_spike_volley_<i>``) provoke ONCE for
    # the whole action and do that at the wrapper level, so we suppress
    # the per-shot trigger here.
    if is_ranged and label in ("attack", "defensive_attack"):
        if _provoke_ranged_aoo(actor, grid, events, encounter):
            return  # killed by AoO

    # Sneak attack precision damage if attacker qualifies.
    precision_dice = _sneak_attack_dice(actor, target, grid, encounter)
    # Flanking grants +2 to melee attacks (regardless of class).
    flank_bonus = _flanking_attack_bonus(
        actor, target, grid, encounter, is_ranged=is_ranged,
    )

    # Script-time attack options: power_attack, combat_expertise.
    pa_attack_pen, pa_dmg_bonus = _power_attack_adjustments(
        actor, chosen, script_options or {},
    )
    ce_attack_pen = _combat_expertise_adjustments(
        actor, chosen, script_options or {}, encounter, events,
    )
    # Smite Evil: if this target is the declared smite target, add bonuses.
    smite_atk, smite_dmg = _smite_evil_adjustments(actor, target)
    # Weapon Focus / class-specific bonuses against this weapon target.
    weapon_focus_bonus = 0
    weapon_id = chosen.get("weapon_id")
    if weapon_id:
        wf_target = f"attack:weapon:{weapon_id}"
        weapon_focus_bonus = _compute_mod(0, actor.modifiers.for_target(wf_target))

    # General-purpose attack/damage modifiers (e.g., Inspire Courage morale,
    # Point-Blank Shot for ranged). These accept any source whose target is
    # "attack" or "damage" — the modifier system enforces stacking rules.
    # Situational racial bonuses (dwarven hatred etc.) carry a qualifier
    # against the target's type/subtypes; we evaluate via the context-
    # aware compute.
    target_ctx = _target_creature_context(target)
    attack_general = _compute_mod_ctx(
        0, actor.modifiers.for_target("attack"), target_ctx,
    )
    damage_general = _compute_mod(0, actor.modifiers.for_target("damage"))
    if is_ranged:
        attack_general += _compute_mod_ctx(
            0, actor.modifiers.for_target("attack:ranged"), target_ctx,
        )
        damage_general += _compute_mod(0, actor.modifiers.for_target("damage:ranged"))

    # Range increment penalty for ranged attacks: -2 per increment
    # beyond the first. PF1 RAW caps at 5 increments (thrown) / 10
    # (projectile); for v1 we apply the penalty without enforcing a
    # hard max range — long shots are punished but not forbidden.
    range_penalty = _range_increment_penalty(chosen, actor, target, grid, is_ranged)
    # Firing into melee: -4 ranged attack vs a target engaged with
    # another combatant; negated by Precise Shot feat.
    firing_penalty = _firing_into_melee_penalty(
        actor, target, grid, encounter, is_ranged,
    )
    # Prone-position adjustments:
    #   - prone attacker: -4 to melee attack rolls
    #   - prone target:   +4 melee attacker / -4 ranged attacker
    prone_atk_penalty = 0
    if "prone" in actor.conditions and not is_ranged:
        prone_atk_penalty = -4
    prone_target_modifier = 0
    if "prone" in target.conditions:
        prone_target_modifier = -4 if is_ranged else 4
    # Helpless target (sleeping, paralyzed, unconscious, etc.):
    # attacker gets +4 to melee attack rolls. Helpless creatures also
    # treat their Dex as 0 — we approximate by switching the AC look-
    # up to flat-footed AC (the attacker's effective benefit).
    helpless_bonus = 0
    ac_situation = "normal"
    if "helpless" in target.conditions:
        helpless_bonus = 4 if not is_ranged else 0
        ac_situation = "flat_footed"
    elif _has_dex_denied(target):
        ac_situation = "flat_footed"
    # Invisible attacker: +2 attack and target denied Dex (target can't
    # see attacker absent True Seeing or pinpointing). PF1 ranged
    # invisible attackers don't get the +2 (RAW: only melee).
    # Pinpoint-by-Perception: a defender already aware of this invisible
    # attacker (via a successful Perception check on a prior round)
    # negates the Dex-denied benefit. The +2 attack bonus persists.
    invisible_bonus = 0
    if "invisible" in actor.conditions:
        if not is_ranged:
            invisible_bonus = 2
        cur_round = (
            int(encounter.round_number) if encounter is not None else 0
        )
        already_pinpointed = (
            target.pinpointed_invisible.get(actor.id, -1) >= cur_round - 1
        )
        if not already_pinpointed:
            ac_situation = "flat_footed"
    # Weapon proficiency: -4 attack if the attacker isn't proficient
    # with the weapon they're using. ``_weapon_not_proficient`` checks
    # the cached proficient categories on the combatant against the
    # chosen weapon's category (when known).
    nonprof_penalty = -4 if _weapon_not_proficient(actor, chosen) else 0
    # Armor / shield proficiency: ACP applies to attack rolls when the
    # wearer lacks proficiency with the armor or shield equipped.
    armor_nonprof_penalty = _armor_not_proficient_penalty(actor)

    # Situational AC bonuses (e.g., +4 dodge AC vs giants from
    # dwarven defensive_training): include qualifier-matched modifiers
    # for THIS attacker. We *augment* the defense_profile by computing
    # qualified-only ac modifiers separately and adding them to the
    # raw AC. (Unqualified ac modifiers are already in defense_profile
    # via the standard compute.)
    attacker_ctx = _target_creature_context(actor)
    ac_context = {
        "attacker_id": actor.id,
        "attacker_type": attacker_ctx.get("target_type"),
        "attacker_subtypes": attacker_ctx.get("target_subtypes"),
    }
    ac_situational_bonus = _compute_mod_ctx(
        0,
        [m for m in target.modifiers.for_target("ac") if m.qualifier is not None],
        ac_context,
    )
    # Positional cover. Walls between attacker and target give hard
    # cover (+4 AC); intervening combatants give soft cover (+4 AC,
    # ranged only).
    cover_bonus = _cover_ac_bonus(actor, target, grid, is_ranged)

    weapon_tags = _weapon_attack_tags(actor, chosen)

    profile = AttackProfile(
        attack_bonus=(
            int(chosen["attack_bonus"])
            + attack_bonus_delta
            + flank_bonus
            - pa_attack_pen
            - ce_attack_pen
            + smite_atk
            + weapon_focus_bonus
            + attack_general
            + range_penalty
            + firing_penalty
            + prone_atk_penalty
            + prone_target_modifier
            + helpless_bonus
            + invisible_bonus
            + nonprof_penalty
            + armor_nonprof_penalty
            - ac_situational_bonus  # subtracted because it makes the target harder to hit
            - cover_bonus
        ),
        damage_dice=str(chosen["damage"]),
        damage_bonus=(
            int(chosen.get("damage_bonus", 0))
            + pa_dmg_bonus + smite_dmg
            + damage_general
        ),
        crit_range=tuple(chosen.get("crit_range") or [20, 20]),  # type: ignore[arg-type]
        crit_multiplier=int(chosen.get("crit_multiplier", 2)),
        damage_type=str(chosen.get("damage_type", "")),
        name=str(chosen.get("name", "weapon")),
        precision_damage_dice=precision_dice,
        attack_tags=weapon_tags,
    )
    defense = target.defense_profile()
    outcome: AttackOutcome = resolve_attack(
        profile, defense, roller, situation=ac_situation,
    )
    # Discharge any single-use buffs (e.g. Guidance) on the attacker.
    actor.consume_single_use_buffs()
    # Mounted Combat feat: if the target is a mount with a rider, the
    # rider can attempt a Ride check (DC = the attack roll) to negate
    # the hit. Limited to once per round (Combat Reflexes-style
    # throttling), tracked via target.mount_id (which is set on the
    # rider, not the mount; the mount has rider_id). We use the
    # rider's per-round AoO marker as a stand-in for the once-per-round
    # restriction since the engine doesn't yet track Ride uses.
    if (
        outcome.hit
        and target.rider_id is not None
        and grid is not None
    ):
        rider = grid.combatants.get(target.rider_id)
        if rider is not None and _has_feat(rider, "mounted_combat"):
            from .skills import skill_check
            from .content import default_registry
            ride_dc = outcome.attack_total
            ride = skill_check(
                rider, "ride", dc=ride_dc, roller=roller,
                registry=default_registry(),
            )
            if ride.success:
                from dataclasses import replace as _replace
                outcome = _replace(
                    outcome,
                    hit=False, crit=False,
                    damage=0, damage_dealt_pre_dr=0, dr_absorbed=0,
                    log=outcome.log + [
                        f"mounted combat: rider {rider.name} negates hit "
                        f"(Ride d20={ride.natural}+{ride.bonus}={ride.total} "
                        f"vs DC {ride_dc})",
                    ],
                )
    # Blinded attacker: 50% miss chance against any target (PF1 RAW
    # "the creature has total concealment" applies to attacks made by
    # the blinded character).
    if outcome.hit and "blinded" in actor.conditions:
        miss_roll = roller.roll("1d100")
        if miss_roll.total <= 50:
            from dataclasses import replace as _replace
            outcome = _replace(
                outcome,
                hit=False, crit=False,
                damage=0, damage_dealt_pre_dr=0, dr_absorbed=0,
                log=outcome.log + [
                    f"blinded miss chance: rolled {miss_roll.total}/100 ≤ 50 — miss",
                ],
            )
    # Target concealment: if the target has concealment > 0 and the
    # attack would otherwise hit, roll 1d100; on a roll ≤ concealment,
    # the attack misses. Standard concealment = 20%; total concealment
    # = 50%.
    if outcome.hit and getattr(target, "concealment", 0) > 0:
        c_roll = roller.roll("1d100")
        if c_roll.total <= target.concealment:
            from dataclasses import replace as _replace
            outcome = _replace(
                outcome,
                hit=False, crit=False,
                damage=0, damage_dealt_pre_dr=0, dr_absorbed=0,
                log=outcome.log + [
                    f"concealment miss: rolled {c_roll.total}/100 ≤ "
                    f"{target.concealment} — miss",
                ],
            )
    # Rock-catching: if the target has the rock_catching trait and the
    # incoming attack is a thrown rock, the target may attempt a
    # Reflex save (DC 15 small / 20 medium / 25 large rock; based on
    # the thrower's size) to catch it instead of taking the hit. RAW
    # caps at one catch per round per target.
    if (
        outcome.hit
        and is_ranged
        and _has_racial_trait(target, "rock_catching")
        and (
            chosen.get("weapon_id") == "rock"
            or str(chosen.get("name", "")).lower() == "rock"
        )
    ):
        cur_round = (
            int(encounter.round_number) if encounter is not None else 0
        )
        last_caught = int(target.resources.get(
            "last_rock_caught_round", -1,
        ))
        if last_caught == cur_round:
            # Already caught this round; skip the save.
            pass
        else:
            from .spells import roll_save
            dc = _ROCK_CATCH_DC.get(
                str(getattr(actor, "size", "medium")).lower(), 15,
            )
            passed, nat, total = roll_save(target, "ref", dc, roller)
            if passed:
                from dataclasses import replace as _replace
                target.resources["last_rock_caught_round"] = cur_round
                outcome = _replace(
                    outcome,
                    hit=False, crit=False,
                    damage=0, damage_dealt_pre_dr=0, dr_absorbed=0,
                    log=outcome.log + [
                        f"rock caught: Ref d20={nat}+{total - nat}="
                        f"{total} ≥ {dc} — caught (thrower size "
                        f"{getattr(actor, 'size', 'medium')})",
                    ],
                )

    # Incorporeal target resolution: non-magical attacks miss outright
    # (immune); force / ghost-touch attacks pass through; any other
    # magical attack rolls a 50% miss (RAW: "50% chance to ignore
    # damage from a corporeal source"). Force damage is identified by
    # damage_type == "force" OR an explicit "force" attack tag.
    if outcome.hit and getattr(target, "incorporeal", False):
        from dataclasses import replace as _replace
        is_force = (
            "force" in weapon_tags
            or str(chosen.get("damage_type", "")).lower() == "force"
        )
        is_ghost_touch = "ghost_touch" in weapon_tags
        if is_force or is_ghost_touch:
            pass  # incorporeal lets force/ghost-touch through unchanged
        elif "magic" not in weapon_tags:
            outcome = _replace(
                outcome,
                hit=False, crit=False,
                damage=0, damage_dealt_pre_dr=0, dr_absorbed=0,
                log=outcome.log + [
                    "incorporeal: non-magical attack — full immunity",
                ],
            )
        else:
            inc_roll = roller.roll("1d100")
            if inc_roll.total <= 50:
                outcome = _replace(
                    outcome,
                    hit=False, crit=False,
                    damage=0, damage_dealt_pre_dr=0, dr_absorbed=0,
                    log=outcome.log + [
                        f"incorporeal: rolled {inc_roll.total}/100 ≤ 50 "
                        f"— magical attack ignored",
                    ],
                )
    if outcome.hit and outcome.damage > 0:
        # Mounted charge damage multiplier (lance: ×2; lance + Spirited
        # Charge: ×3; non-lance + Spirited Charge: ×2).
        mult = (script_options or {}).get("charge_damage_multiplier", 1)
        if mult > 1:
            from dataclasses import replace as _replace
            new_damage = outcome.damage * mult
            outcome = _replace(
                outcome,
                damage=new_damage,
                damage_dealt_pre_dr=outcome.damage_dealt_pre_dr * mult,
                log=outcome.log + [
                    f"mounted charge: damage ×{mult} "
                    f"({outcome.damage} → {new_damage})",
                ],
            )
        # Attack damage type is the chosen weapon's damage_type code
        # (e.g., "S", "P", "B", "P/S"). Used by Combatant.take_damage
        # to apply the regeneration non-bypass floor.
        atk_damage_type = str(chosen.get("damage_type", "")) or None
        target.take_damage(outcome.damage, damage_type=atk_damage_type)
        massive_damage_check = _check_massive_damage(
            target, outcome.damage, roller,
        )
        _apply_post_damage_state(target)
    else:
        massive_damage_check = None
    # Stunning Fist rider: if the attacker has declared a stunning_fist
    # this turn and the attack hit, the target rolls a Fort save vs the
    # cached DC; on failure, target is stunned 1 round.
    stunning_fist_event: dict | None = None
    if outcome.hit and "stunning_fist_pending" in actor.conditions:
        stunning_fist_event = _resolve_stunning_fist(
            actor, target, roller, encounter,
        )
    # Wolf-style trip-on-bite: free trip CMB after a successful melee hit
    # for creatures with the ``trip_attack`` racial trait.
    trip_event: dict | None = None
    if (
        outcome.hit and not is_ranged
        and _has_racial_trait(actor, "trip_attack")
    ):
        passed, nat, total, margin = _resolve_maneuver(
            actor, target, "trip", roller,
        )
        if passed:
            target.add_condition("prone")
        trip_event = {
            "actor_id": actor.id, "target_id": target.id,
            "natural": nat, "total": total, "margin": margin,
            "passed": passed,
        }
    # Ghoul paralysis: bite-on-hit Fort save vs paralysis (1d4+1 rounds).
    paralysis_event: dict | None = None
    if (
        outcome.hit and not is_ranged
        and _has_racial_trait(actor, "paralysis_ghoul")
    ):
        paralysis_event = _resolve_paralysis_rider(
            actor, target, roller,
        )
    # Disease on bite (ghoul fever, filth fever, etc.): the entry
    # Fort save fires; failure queues an ongoing-effect ticker that
    # re-rolls per the disease's period (typically 1 day = 14400
    # rounds at 1-round-per-6-seconds).
    disease_event: dict | None = None
    if outcome.hit and not is_ranged:
        disease_match = _matching_disease_trait(actor)
        if disease_match is not None:
            d_trait_id, d_data = disease_match
            disease_event = _resolve_disease_rider(
                actor, target, roller, d_trait_id, d_data,
                encounter=encounter,
            )
    # Grab: free grapple attempt after a successful natural-weapon hit
    # (owlbear, stirge, etc.). Stirge's blood_drain auto-grabs without
    # an opposed roll; other grabbers do an opposed CMB.
    grab_event: dict | None = None
    if (
        outcome.hit and not is_ranged
        and (
            _has_racial_trait(actor, "grab")
            or _has_racial_trait(actor, "blood_drain")
        )
    ):
        grab_event = _resolve_grab_rider(actor, target, roller)
    # Poison on bite (giant spider, viper, etc.): entry Fort save
    # fires; failure queues an ongoing poison ticker per the trait's
    # cadence.
    poison_event: dict | None = None
    if outcome.hit and not is_ranged:
        poison_match = _matching_poison_trait(actor)
        if poison_match is not None:
            p_trait_id, p_data = poison_match
            poison_event = _resolve_poison_rider(
                actor, target, roller, p_trait_id, p_data,
                encounter=encounter,
            )
    # Pinpoint check: if the attacker is invisible, the defender
    # rolls Perception (DC 20 + 1 per 10 ft of distance) to locate
    # the attacker's square. Success records the attacker_id under
    # target.pinpointed_invisible so subsequent attacks at the
    # same attacker drop the Dex-denied benefit. The +2 attack
    # bonus persists either way.
    if "invisible" in actor.conditions:
        ax, ay = actor.position
        tx, ty = target.position
        dist_squares = max(abs(ax - tx), abs(ay - ty))
        dc = 20 + (dist_squares * 5) // 10
        from .skills import skill_check
        from .content import default_registry
        result = skill_check(
            target, "perception", dc=dc, roller=roller,
            registry=default_registry(),
        )
        if result.success:
            cur_round = (
                int(encounter.round_number) if encounter is not None else 0
            )
            target.pinpointed_invisible[actor.id] = cur_round
    events.append(TurnEvent(actor.id, label, {
        "target_id": target.id,
        "weapon": profile.name,
        "hit": outcome.hit,
        "crit": outcome.crit,
        "damage": outcome.damage,
        "trace": outcome.log,
    }))
    if stunning_fist_event is not None:
        events.append(TurnEvent(actor.id, "stunning_fist_save",
                                stunning_fist_event))
    if trip_event is not None:
        events.append(TurnEvent(actor.id, "trip_on_hit", trip_event))
    if paralysis_event is not None:
        events.append(TurnEvent(actor.id, "paralysis_on_hit", paralysis_event))
    if disease_event is not None:
        events.append(TurnEvent(actor.id, "disease_on_hit", disease_event))
    if grab_event is not None:
        events.append(TurnEvent(actor.id, "grab_on_hit", grab_event))
    if poison_event is not None:
        events.append(TurnEvent(actor.id, "poison_on_hit", poison_event))
    if massive_damage_check is not None:
        events.append(TurnEvent(actor.id, "massive_damage",
                                massive_damage_check[1]))


# ---------------------------------------------------------------------------
# Active combat options: Power Attack, Combat Expertise, Smite Evil
# ---------------------------------------------------------------------------


def _has_feat(actor: Combatant, feat_id: str) -> bool:
    """True if the combatant has the feat.

    Reads from both the underlying template (``character.feats`` or
    ``monster.feats``) and the per-combatant ``extra_feats`` override
    list. Walks parametric variants (e.g. ``weapon_focus_longsword``
    for a requested ``weapon_focus``).
    """
    feats: list[str] = list(actor.extra_feats)
    if actor.template is not None:
        feats.extend(getattr(actor.template, "feats", None) or [])
    if feat_id in feats:
        return True
    prefix = feat_id + "_"
    return any(f == feat_id or f.startswith(prefix) for f in feats)


def _bab_of(actor: Combatant) -> int:
    return int(actor.bases.get("bab", 0))


def _power_attack_adjustments(
    actor: Combatant,
    chosen: dict,
    options: dict,
) -> tuple[int, int]:
    """Compute Power Attack penalty/bonus for this attack.

    ``options.power_attack`` is the patron's chosen attack-bonus penalty
    (a positive int, must be ≥ 1). PF1: -1 attack per 4 BAB step (so
    -1 at BAB 1-4, up to -2 at 5+, etc.; max = 1 + BAB // 4). Damage
    bonus depends on wield: +1 light/off-hand, +2 one-handed,
    +3 two-handed (per point of penalty).

    Returns ``(attack_pen, damage_bonus)``. (0, 0) if not requested or
    not legal (no feat, no melee, BAB < 1).
    """
    pa = options.get("power_attack")
    if not pa:
        return 0, 0
    pa_pen = int(pa)
    if pa_pen <= 0:
        return 0, 0
    if not _has_feat(actor, "power_attack"):
        return 0, 0
    bab = _bab_of(actor)
    if bab < 1:
        return 0, 0
    if chosen.get("type") != "melee":
        return 0, 0
    max_pen = 1 + bab // 4
    pa_pen = min(pa_pen, max_pen)
    wield = chosen.get("wield", "one_handed")
    if wield == "two_handed":
        dmg = pa_pen * 3
    elif wield in ("light", "off_hand"):
        dmg = pa_pen
    else:
        dmg = pa_pen * 2
    return pa_pen, dmg


def _combat_expertise_adjustments(
    actor: Combatant,
    chosen: dict,
    options: dict,
    encounter,
    events: list[TurnEvent],
) -> int:
    """Compute Combat Expertise attack penalty and apply 1-round AC bonus.

    PF1: trade up to (1 + BAB//4) attack for a dodge AC bonus of the
    same magnitude. The AC bonus lasts until the start of the actor's
    next turn (we model as expiring at current_round + 1).

    Returns the attack penalty. 0 when not requested or not legal.
    """
    ce = options.get("combat_expertise")
    if not ce:
        return 0
    ce_pen = int(ce)
    if ce_pen <= 0:
        return 0
    if not _has_feat(actor, "combat_expertise"):
        return 0
    bab = _bab_of(actor)
    if bab < 1:
        return 0
    if chosen.get("type") != "melee":
        return 0
    max_pen = 1 + bab // 4
    ce_pen = min(ce_pen, max_pen)
    cur_round = getattr(encounter, "round_number", 1) if encounter else 1
    src = "combat_expertise"
    actor.modifiers.remove_by_source(src)
    actor.modifiers.add(Modifier(
        value=ce_pen, type="dodge", target="ac",
        source=src, expires_round=cur_round + 1,
    ))
    events.append(TurnEvent(actor.id, "combat_expertise", {
        "attack_penalty": ce_pen, "ac_bonus": ce_pen,
        "expires_round": cur_round + 1,
    }))
    return ce_pen


def _ability_modifier(actor: Combatant, ability: str) -> int:
    """Read the actor's current ability modifier from the template + mods."""
    if actor.template is None:
        return 0
    base = 10
    if hasattr(actor.template, "base_ability_scores"):
        try:
            base = actor.template.base_ability_scores.get(ability)
        except Exception:
            base = 10
    total = base
    for m in actor.modifiers.for_target(f"ability:{ability}"):
        total += m.value
    return (total - 10) // 2


def _paladin_levels(actor: Combatant) -> int:
    if actor.template_kind != "character" or actor.template is None:
        return 0
    char = actor.template
    if getattr(char, "class_id", None) == "paladin":
        levels = 1
    else:
        levels = 0
    plan = getattr(char, "level_plan", None)
    if plan and isinstance(plan, dict):
        for entry in (plan.get("levels") or {}).values():
            if isinstance(entry, dict) and entry.get("class") == "paladin":
                levels += 1
    return levels


def _is_evil(target: Combatant) -> bool:
    """Best-effort alignment check for Smite Evil targets."""
    align = ""
    if target.template is not None:
        align = str(getattr(target.template, "alignment", "") or "")
    return "evil" in align.lower()


def _smite_evil_adjustments(
    actor: Combatant,
    target: Combatant,
) -> tuple[int, int]:
    """If the actor has declared this target as their smite, return
    (attack_bonus, damage_bonus). Otherwise (0, 0)."""
    if not actor.smite_target_id:
        return 0, 0
    if actor.smite_target_id != target.id:
        return 0, 0
    pal_levels = _paladin_levels(actor)
    if pal_levels <= 0:
        return 0, 0
    cha_mod = _ability_modifier(actor, "cha")
    return max(0, cha_mod), pal_levels


# ---------------------------------------------------------------------------
# Composite action handlers: Cleave, Rage, Smite Evil, Channel Energy,
# Bardic Performance
# ---------------------------------------------------------------------------


def _do_cleave(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Cleave: standard action. Attack a foe; on a hit, attack one more
    foe adjacent to actor. Both attacks at -2 to AC for 1 round."""
    if not _has_feat(actor, "cleave"):
        events.append(TurnEvent(actor.id, "skip", {"reason": "cleave: no feat"}))
        return
    primary = _resolve_target(args.get("target"), ns)
    if primary is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "cleave: no primary target"}))
        return
    if not grid.is_adjacent(actor, primary):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "cleave: primary not adjacent"}))
        return
    cur_round = encounter.round_number if encounter else 1
    src = "cleave_ac_penalty"
    actor.modifiers.remove_by_source(src)
    actor.modifiers.add(Modifier(
        value=-2, type="untyped", target="ac",
        source=src, expires_round=cur_round + 1,
    ))

    pre_hp = primary.current_hp
    _do_attack(actor, primary, grid, roller, events,
               label="cleave_primary", encounter=encounter)
    primary_hit = primary.current_hp < pre_hp
    if not primary_hit:
        events.append(TurnEvent(actor.id, "cleave_no_followup",
                                {"reason": "primary missed"}))
        return
    # DSL v2 Phase 3.3: cleave continuation is a sub-action decision
    # point. The cleaver's registered Picker chooses among CleaveTo
    # (one per adjacent foe other than primary) and PassCleave. With
    # no picker, default to the v1 behavior — first adjacent foe.
    candidates = _adjacent_enemies_excluding(actor, grid, primary)
    if not candidates:
        events.append(TurnEvent(actor.id, "cleave_no_followup",
                                {"reason": "no second foe in reach"}))
        return
    from .actions import CleaveTo as _CleaveTo, PassCleave as _PassCleave
    legal: list = [
        _CleaveTo(actor_id=actor.id, primary_target_id=primary.id,
                  target_id=c.id)
        for c in candidates
    ] + [
        _PassCleave(actor_id=actor.id, primary_target_id=primary.id),
    ]
    cleaver_picker = encounter.pickers.get(actor.id) if encounter is not None else None
    if cleaver_picker is None:
        chosen = legal[0]  # Default: first adjacent foe.
    else:
        from .actions import GameState as _GameState
        st = _GameState(encounter=encounter, grid=grid)
        chosen = cleaver_picker.pick(actor, st, legal)
    if isinstance(chosen, _PassCleave):
        events.append(TurnEvent(actor.id, "cleave_no_followup",
                                {"reason": "picker_passed"}))
        return
    secondary = grid.combatants.get(chosen.target_id)
    if secondary is None:
        events.append(TurnEvent(actor.id, "cleave_no_followup",
                                {"reason": "secondary target gone"}))
        return
    _do_attack(actor, secondary, grid, roller, events,
               label="cleave_secondary", encounter=encounter)


def _pick_adjacent_foe(
    actor: Combatant,
    encounter: Encounter,
    grid: Grid,
    exclude: Combatant | None = None,
) -> Combatant | None:
    if encounter is None:
        return None
    for ir in encounter.initiative:
        c = ir.combatant
        if c.id == actor.id or c.team == actor.team:
            continue
        if exclude is not None and c.id == exclude.id:
            continue
        if c.current_hp <= 0 or c.is_unconscious():
            continue
        if grid.is_adjacent(actor, c):
            return c
    return None


def _adjacent_enemies_excluding(
    actor: Combatant,
    grid: Grid,
    exclude: Combatant | None = None,
) -> list[Combatant]:
    """All adjacent enemies of ``actor`` (alive, conscious), in
    initiative order if encounter is available — otherwise grid-order.
    Used by the cleave continuation picker to enumerate secondary
    targets."""
    out: list[Combatant] = []
    for cid, c in grid.combatants.items():
        if c.id == actor.id or c.team == actor.team:
            continue
        if exclude is not None and c.id == exclude.id:
            continue
        if c.current_hp <= 0 or c.is_unconscious():
            continue
        if grid.is_adjacent(actor, c):
            out.append(c)
    return out


def _do_rage_start(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    events: list[TurnEvent],
) -> None:
    """Begin barbarian rage. Free action; pulls a round from the pool.

    Effects (PF1 base rage): +4 morale Str, +4 morale Con, +2 morale
    Will save, -2 untyped AC. Lasts until ended (or the pool empties).
    """
    if "raging" in actor.conditions:
        events.append(TurnEvent(actor.id, "skip", {"reason": "already raging"}))
        return
    rounds_remaining = actor.resources.get("rage_rounds", 0)
    if rounds_remaining <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "no rage rounds remaining"}))
        return
    actor.resources["rage_rounds"] = rounds_remaining - 1
    src = "rage"
    actor.modifiers.add(Modifier(value=4, type="morale",
                                 target="ability:str", source=src))
    actor.modifiers.add(Modifier(value=4, type="morale",
                                 target="ability:con", source=src))
    actor.modifiers.add(Modifier(value=2, type="morale",
                                 target="will_save", source=src))
    actor.modifiers.add(Modifier(value=-2, type="untyped",
                                 target="ac", source=src))
    actor.add_condition("raging")
    events.append(TurnEvent(actor.id, "rage_start", {
        "rounds_remaining": actor.resources["rage_rounds"],
    }))


def _do_rage_end(
    actor: Combatant,
    events: list[TurnEvent],
) -> None:
    if "raging" not in actor.conditions:
        events.append(TurnEvent(actor.id, "skip", {"reason": "not raging"}))
        return
    actor.modifiers.remove_by_source("rage")
    actor.remove_condition("raging")
    actor.add_condition("fatigued")
    events.append(TurnEvent(actor.id, "rage_end", {}))


def _do_smite_evil(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Paladin Smite Evil. Swift action; declares a target. The bonuses
    apply on attacks against that target until it dies or the paladin
    rests. This handler just consumes the use and stores the target id."""
    pal_levels = _paladin_levels(actor)
    if pal_levels <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "smite_evil: not a paladin"}))
        return
    uses = actor.resources.get("smite_evil_uses", 0)
    if uses <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "no smite_evil uses left"}))
        return
    target = _resolve_target(args.get("target"), ns)
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "smite_evil: no target"}))
        return
    if not _is_evil(target):
        # Smiting a non-evil target wastes the use (PF1 RAW).
        actor.resources["smite_evil_uses"] = uses - 1
        events.append(TurnEvent(actor.id, "smite_evil_wasted", {
            "target_id": target.id, "reason": "target not evil",
        }))
        return
    actor.resources["smite_evil_uses"] = uses - 1
    actor.smite_target_id = target.id
    cha_mod = _ability_modifier(actor, "cha")
    src = "smite_evil_deflect"
    actor.modifiers.remove_by_source(src)
    if cha_mod > 0:
        actor.modifiers.add(Modifier(
            value=cha_mod, type="deflection", target="ac", source=src,
        ))
    events.append(TurnEvent(actor.id, "smite_evil", {
        "target_id": target.id,
        "attack_bonus": max(0, cha_mod),
        "damage_bonus": pal_levels,
        "ac_bonus_vs_target": max(0, cha_mod),
        "uses_remaining": actor.resources["smite_evil_uses"],
    }))


def _cleric_levels(actor: Combatant) -> int:
    if actor.template_kind != "character" or actor.template is None:
        return 0
    char = actor.template
    levels = 1 if getattr(char, "class_id", None) == "cleric" else 0
    plan = getattr(char, "level_plan", None)
    if plan and isinstance(plan, dict):
        for entry in (plan.get("levels") or {}).values():
            if isinstance(entry, dict) and entry.get("class") == "cleric":
                levels += 1
    return levels


def _do_channel_energy(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Cleric Channel Energy. 30-ft burst centered on cleric (6 squares).

    ``args.mode`` is ``"heal_living"`` or ``"harm_undead"`` (good
    cleric); the mirror options are skipped — we model the common case.
    Healing affects allies who are alive (excluding undead); harming
    affects undead enemies. 1d6 at L1, +1d6 every 2 levels. Will save
    halves harm.
    """
    cl_levels = _cleric_levels(actor)
    if cl_levels <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "channel_energy: not a cleric"}))
        return
    uses = actor.resources.get("channel_uses", 0)
    if uses <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "no channel_energy uses left"}))
        return
    actor.resources["channel_uses"] = uses - 1

    mode = args.get("mode", "heal_living")
    dice_count = 1 + (cl_levels - 1) // 2
    dice_str = f"{dice_count}d6"
    r = roller.roll(dice_str)
    base_amount = sum(r.terms[0].kept) if r.terms and r.terms[0].rolls else 0

    cha_mod = _ability_modifier(actor, "cha")
    dc = 10 + cl_levels // 2 + cha_mod

    # Find targets within 6 squares (30 ft) of the cleric.
    radius = 6
    affected: list[dict] = []
    for ir in encounter.initiative:
        c = ir.combatant
        if c.current_hp <= -10:
            continue
        if grid.distance_squares(actor.position, c.position) > radius:
            continue
        is_undead = (
            c.template_kind == "monster"
            and c.template is not None
            and "undead" in (getattr(c.template, "type", "") or "").lower()
        )
        if mode == "heal_living":
            if is_undead:
                if c.team == actor.team:
                    continue
                # Damage undead, Will save halves.
                amount = base_amount
                from .spells import roll_save
                passed, nat, total = roll_save(
                    c, "will", dc, roller,
                    context={"effect_type": "channel_energy"},
                )
                if passed:
                    amount = base_amount // 2
                c.take_damage(amount)
                _apply_post_damage_state(c)
                affected.append({
                    "target_id": c.id, "kind": "harm_undead",
                    "amount": amount, "save": passed,
                })
            else:
                # Heal living — never targets enemies.
                if c.team != actor.team and c.id != actor.id:
                    continue
                heal_amt = min(base_amount, c.max_hp - c.current_hp)
                c.heal(base_amount)
                affected.append({
                    "target_id": c.id, "kind": "heal", "amount": heal_amt,
                })
        elif mode == "harm_undead":
            if not is_undead:
                continue
            from .spells import roll_save
            amount = base_amount
            passed, nat, total = roll_save(
                c, "will", dc, roller,
                context={"effect_type": "channel_energy"},
            )
            if passed:
                amount = base_amount // 2
            c.take_damage(amount)
            _apply_post_damage_state(c)
            affected.append({
                "target_id": c.id, "kind": "harm_undead",
                "amount": amount, "save": passed,
            })

    events.append(TurnEvent(actor.id, "channel_energy", {
        "mode": mode, "dice": dice_str, "rolled": base_amount,
        "save_dc": dc, "affected": affected,
        "uses_remaining": actor.resources["channel_uses"],
    }))


def _bard_levels(actor: Combatant) -> int:
    if actor.template_kind != "character" or actor.template is None:
        return 0
    char = actor.template
    levels = 1 if getattr(char, "class_id", None) == "bard" else 0
    plan = getattr(char, "level_plan", None)
    if plan and isinstance(plan, dict):
        for entry in (plan.get("levels") or {}).values():
            if isinstance(entry, dict) and entry.get("class") == "bard":
                levels += 1
    return levels


_BARDIC_MODES = frozenset({
    "inspire_courage", "countersong", "distraction", "fascinate",
})


def _do_bardic_performance(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Bardic Performance dispatch.

    RAW (Foundry pack ``Bardic Performance``): standard action to
    start, free action to maintain. Each round consumes one round
    from ``performance_rounds``. The bard cannot have more than one
    bardic performance in effect at one time — switching modes
    requires stopping the previous one and starting a new one as a
    standard action.

    Modes implemented:
    - ``inspire_courage``: morale +attack/damage and morale +Will-vs-fear
      to all allies in earshot.
    - ``countersong``: bard rolls Perform; any creature within 30 ft
      may use the bard's Perform total in place of a save vs sonic /
      language-dependent magic that round (intercepted in
      ``roll_save`` via ``_bardic_save_intercept``).
    - ``distraction``: same shape as countersong, vs illusion (pattern)
      / illusion (figment).
    - ``fascinate``: targets within 90 ft must beat a Will save
      DC 10 + 1/2 bard level + Cha mod or be fascinated (1 target
      at L1, +1 per 3 levels above 1st).
    """
    bard_levels = _bard_levels(actor)
    if bard_levels <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "bardic_performance: not a bard"}))
        return
    rounds_left = actor.resources.get("performance_rounds", 0)
    if rounds_left <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "no bardic performance rounds left"}))
        return
    mode = args.get("mode", "inspire_courage")
    if mode not in _BARDIC_MODES:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"bardic mode {mode!r} not "
                                           f"in RAW menu"}))
        return

    actor.resources["performance_rounds"] = rounds_left - 1
    cur_round = encounter.round_number if encounter else 1

    if mode == "inspire_courage":
        _bardic_inspire_courage(actor, encounter, cur_round,
                                bard_levels, events)
        return
    if mode == "countersong":
        _bardic_countersong_distraction(
            actor, encounter, cur_round, mode,
            args, ns, events,
        )
        return
    if mode == "distraction":
        _bardic_countersong_distraction(
            actor, encounter, cur_round, mode,
            args, ns, events,
        )
        return
    if mode == "fascinate":
        _bardic_fascinate(actor, encounter, grid, cur_round,
                          bard_levels, args, ns, events)
        return


def _bardic_inspire_courage(
    actor: Combatant, encounter: Encounter, cur_round: int,
    bard_levels: int, events: list[TurnEvent],
) -> None:
    bonus = 1
    if bard_levels >= 17:
        bonus = 4
    elif bard_levels >= 11:
        bonus = 3
    elif bard_levels >= 5:
        bonus = 2

    src = f"inspire_courage:{actor.id}"
    affected_ids: list[str] = []
    for ir in encounter.initiative:
        c = ir.combatant
        if c.team != actor.team:
            continue
        if c.current_hp <= 0 or c.is_unconscious():
            continue
        # Refresh the modifier every activation so duration tracks.
        c.modifiers.remove_by_source(src)
        c.modifiers.add(Modifier(value=bonus, type="morale",
                                 target="attack", source=src,
                                 expires_round=cur_round + 1))
        c.modifiers.add(Modifier(value=bonus, type="morale",
                                 target="damage", source=src,
                                 expires_round=cur_round + 1))
        c.modifiers.add(Modifier(value=bonus, type="morale",
                                 target="will_save", source=src,
                                 expires_round=cur_round + 1))
        affected_ids.append(c.id)

    # Mark the active mode + clear any prior performance state so the
    # countersong / distraction intercept turns off when we switch
    # to inspire_courage. RAW: "A bard cannot have more than one
    # bardic performance in effect at one time."
    actor.resources["bardic_active_mode"] = "inspire_courage"
    actor.resources["bardic_active_until_round"] = cur_round + 1
    actor.resources.pop("bardic_perform_total", None)

    events.append(TurnEvent(actor.id, "bardic_performance", {
        "mode": "inspire_courage", "bonus": bonus,
        "affected_ids": affected_ids,
        "rounds_remaining": actor.resources["performance_rounds"],
    }))


# Perform skills allowed for each performance per RAW. Used to
# validate the `subskill` arg if supplied; a default is chosen if
# the patron didn't pick one.
_PERFORM_SUBSKILLS_COUNTERSONG = ("keyboard", "percussion", "wind",
                                  "string", "sing")
_PERFORM_SUBSKILLS_DISTRACTION = ("act", "comedy", "dance", "oratory")


def _bardic_countersong_distraction(
    actor: Combatant, encounter: Encounter, cur_round: int,
    mode: str, args: dict, ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Roll the bard's Perform check for the round and stash it on the
    bard's resources. ``_bardic_save_intercept`` reads it during save
    resolution for any matching effect that lands on a creature
    within 30 ft. RAW: countersong vs sonic / language-dependent;
    distraction vs illusion (pattern) / illusion (figment)."""
    if mode == "countersong":
        allowed = _PERFORM_SUBSKILLS_COUNTERSONG
    else:
        allowed = _PERFORM_SUBSKILLS_DISTRACTION
    subskill = args.get("subskill") or allowed[0]
    if subskill not in allowed:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": f"{mode}: subskill {subskill!r} not in RAW menu",
            "allowed": list(allowed),
        }))
        return

    # Roll the bard's Perform check. Use the encounter's roller so
    # the result is reproducible alongside the rest of the turn.
    # PF1 has Perform as a single skill with named subtypes; ranks
    # apply to the whole skill regardless of which subtype is rolled,
    # so we read the umbrella ``perform`` skill_total here. The
    # ``subskill`` label is preserved on the event for trace purposes
    # (it's still RAW-validated against the per-performance allowed
    # list).
    roller = getattr(encounter, "roller", None) or Roller()
    nat = roller.roll("1d20").terms[0].rolls[0]
    perform_total = nat + actor.skill_total("perform")

    actor.resources["bardic_active_mode"] = mode
    actor.resources["bardic_active_until_round"] = cur_round + 1
    actor.resources["bardic_perform_total"] = perform_total

    events.append(TurnEvent(actor.id, "bardic_performance", {
        "mode": mode,
        "subskill": subskill,
        "perform_natural": nat,
        "perform_total": perform_total,
        "rounds_remaining": actor.resources["performance_rounds"],
    }))


def _bardic_fascinate(
    actor: Combatant, encounter: Encounter, grid: Grid, cur_round: int,
    bard_levels: int, args: dict, ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Will save vs DC 10 + 1/2 bard level + Cha mod for each target
    in 90 ft. RAW: 1 target at L1, +1 per 3 levels beyond. Targets
    must be able to see and hear the bard, and the bard must be able
    to see them. On fail: ``fascinated`` condition applied."""
    from .spells import roll_save
    cha_mod = _ability_modifier(actor, "cha")
    dc = 10 + bard_levels // 2 + cha_mod
    max_targets = 1 + max(0, (bard_levels - 1) // 3)

    raw_targets = args.get("targets") or []
    resolved_targets: list[Combatant] = []
    for t_expr in raw_targets:
        t = _resolve_target(t_expr, ns)
        if t is None:
            continue
        if not t.is_alive() or t.current_hp <= 0:
            continue
        # 90 ft = 18 squares. Range gate.
        if grid.distance_squares(actor.position, t.position) > 18:
            continue
        resolved_targets.append(t)
        if len(resolved_targets) >= max_targets:
            break

    affected: list[dict] = []
    for t in resolved_targets:
        # Mind-affecting + enchantment immunities short-circuit.
        if "fascinated" in t.condition_immunities:
            affected.append({"target_id": t.id, "result": "immune"})
            continue
        passed, nat, total = roll_save(
            t, "will", dc, encounter.roller or Roller(seed=0),
            context={"effect_tags": ["enchantment", "compulsion",
                                     "mind_affecting"]},
        )
        if passed:
            affected.append({"target_id": t.id, "result": "save",
                             "natural": nat, "total": total})
        else:
            t.add_condition("fascinated")
            affected.append({"target_id": t.id, "result": "fascinated",
                             "natural": nat, "total": total})

    actor.resources["bardic_active_mode"] = "fascinate"
    actor.resources["bardic_active_until_round"] = cur_round + 1

    events.append(TurnEvent(actor.id, "bardic_performance", {
        "mode": "fascinate",
        "save_dc": dc,
        "max_targets": max_targets,
        "affected": affected,
        "rounds_remaining": actor.resources["performance_rounds"],
    }))


# RAW descriptor / school predicates for the countersong / distraction
# intercepts. Matched against the spell-save context built by
# ``_spell_save_context``.
_COUNTERSONG_DESCRIPTORS = frozenset({"sonic", "language-dependent",
                                      "language_dependent"})
_DISTRACTION_SUBSCHOOLS = frozenset({"pattern", "figment"})


def _bardic_save_intercept(
    target: Combatant, save_kind: str, save_total: int,
    context: dict, encounter, grid,
) -> int | None:
    """Returns the substituted save total (the bard's Perform total)
    if a bard within 30 ft has an active matching performance and the
    Perform total is higher than ``save_total``. ``None`` otherwise.

    Called from ``spells.roll_save`` after the natural save has been
    rolled. The Perform total was computed when the bard activated
    countersong / distraction this round and stashed in
    ``bardic_perform_total``.
    """
    if encounter is None or grid is None:
        return None
    descriptors = set(context.get("descriptors") or [])
    school = (context.get("school") or "").lower()
    subschool = (context.get("subschool") or "").lower()
    countersong_match = bool(_COUNTERSONG_DESCRIPTORS & descriptors)
    distraction_match = (school == "illusion"
                         and subschool in _DISTRACTION_SUBSCHOOLS)
    if not countersong_match and not distraction_match:
        return None
    cur_round = encounter.round_number
    best_total: int | None = None
    for ir in encounter.initiative:
        bard = ir.combatant
        if bard.id == target.id:
            # The bard themselves can also benefit from countersong
            # per RAW ("any creature within 30 feet of the bard
            # including the bard himself"). Don't skip on identity.
            pass
        mode = bard.resources.get("bardic_active_mode")
        if mode is None:
            continue
        until = bard.resources.get("bardic_active_until_round", 0)
        if until < cur_round:
            continue
        # Only the matching mode applies.
        if countersong_match and mode != "countersong":
            continue
        if distraction_match and mode != "distraction":
            continue
        # 30 ft = 6 squares.
        if grid.distance_squares(bard.position, target.position) > 6:
            continue
        # The performance must be a save-replacing kind. inspire_courage
        # / fascinate produce no Perform total.
        perform_total = bard.resources.get("bardic_perform_total")
        if perform_total is None:
            continue
        if best_total is None or perform_total > best_total:
            best_total = perform_total
    return best_total


# ---------------------------------------------------------------------------
# Wizard arcane-school L1 active powers
# ---------------------------------------------------------------------------


def _wizard_level(actor: Combatant) -> int:
    return int(actor.class_levels.get("wizard", 0))


def _intense_spells_bonus(actor: Combatant) -> int:
    """Evoker's Intense Spells passive: +max(1, wiz_lvl // 2) damage on
    an evocation hit-point-damage spell, applied once per spell."""
    if actor.template_kind != "character" or actor.template is None:
        return 0
    school = ((actor.template.class_choices or {}).get("wizard_school")
              or "universalist")
    if school != "evocation":
        return 0
    wl = _wizard_level(actor)
    if wl <= 0:
        return 0
    return max(1, wl // 2)


def _do_wizard_school_power(
    actor: Combatant,
    power_id: str,
    target: Combatant | None,
    options: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    events: list[TurnEvent],
) -> None:
    """Dispatch a wizard arcane-school L1 active power.

    All powers share the daily-pool gate (``wizard_school_<pid>_uses``
    seeded as 3 + Int mod at character build) and are standard
    actions. Per-power resolution lives in ``_WIZARD_POWER_HANDLERS``.
    """
    if _wizard_level(actor) <= 0:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "wizard_school_power: actor has no wizard levels",
        }))
        return
    res_key = f"wizard_school_{power_id}_uses"
    uses = actor.resources.get(res_key, 0)
    if uses <= 0:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "wizard_school_power: no uses remaining",
            "power_id": power_id,
        }))
        return
    handler = _WIZARD_POWER_HANDLERS.get(power_id)
    if handler is None:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "wizard_school_power: unknown power_id",
            "power_id": power_id,
        }))
        return
    # Consume one use up-front (RAW: per-day pool decrements
    # regardless of hit/miss for SLA-style abilities).
    actor.resources[res_key] = uses - 1
    handler(actor, target, options, encounter, grid, roller, events)


def _make_school_attack_profile(
    actor: Combatant,
    *,
    weapon_name: str,
    damage_dice: str,
    damage_bonus: int,
    damage_type: str,
    crit_range: tuple[int, int] = (20, 20),
    attack_bonus: int | None = None,
    attack_tags: frozenset = frozenset(),
) -> AttackProfile:
    if attack_bonus is None:
        # Default to BAB + Dex + size mod (standard ranged-touch math).
        dex_mod = _ability_modifier(actor, "dex")
        size_mod = _compute_mod(
            0, actor.modifiers.for_target("size_attack")
        )
        attack_bonus = actor.bases.get("bab", 0) + dex_mod + size_mod
    return AttackProfile(
        attack_bonus=attack_bonus,
        damage_dice=damage_dice,
        damage_bonus=damage_bonus,
        crit_range=crit_range,
        crit_multiplier=2,
        damage_type=damage_type,
        name=weapon_name,
        precision_damage_dice="0d0",
        attack_tags=attack_tags,
    )


def _power_acid_dart(
    actor: Combatant, target: Combatant | None, opts: dict,
    encounter, grid: Grid, roller: Roller, events: list[TurnEvent],
) -> None:
    """Conjuration L1: ranged touch attack within 30 ft; 1d6 acid + 1 per
    2 wizard levels. Ignores SR."""
    _ranged_touch_damage(
        actor, target, encounter, grid, roller, events,
        power_id="acid_dart", range_squares=6, dice="1d6",
        plus_per_two_levels=1, damage_type="acid",
        attack_tags=frozenset({"magic", "acid"}),
    )


def _power_telekinetic_fist(
    actor: Combatant, target: Combatant | None, opts: dict,
    encounter, grid: Grid, roller: Roller, events: list[TurnEvent],
) -> None:
    """Transmutation L1: ranged touch within 30 ft; 1d4 bludgeoning + 1
    per 2 wizard levels."""
    _ranged_touch_damage(
        actor, target, encounter, grid, roller, events,
        power_id="telekinetic_fist", range_squares=6, dice="1d4",
        plus_per_two_levels=1, damage_type="B",
        attack_tags=frozenset({"magic"}),
    )


def _ranged_touch_damage(
    actor: Combatant, target: Combatant | None, encounter, grid: Grid,
    roller: Roller, events: list[TurnEvent], *,
    power_id: str, range_squares: int, dice: str,
    plus_per_two_levels: int, damage_type: str,
    attack_tags: frozenset,
) -> None:
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"{power_id}: no target"}))
        return
    if grid.distance_squares(actor.position, target.position) > range_squares:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"{power_id}: target out of range"}))
        return
    wl = _wizard_level(actor)
    damage_bonus = plus_per_two_levels * (wl // 2)
    profile = _make_school_attack_profile(
        actor, weapon_name=power_id, damage_dice=dice,
        damage_bonus=damage_bonus, damage_type=damage_type,
        attack_tags=attack_tags,
    )
    outcome = resolve_attack(
        profile, target.defense_profile(), roller, situation="touch",
    )
    detail = {
        "power_id": power_id, "target_id": target.id,
        "hit": outcome.hit, "crit": outcome.crit,
        "damage": outcome.damage,
        "trace": outcome.log,
    }
    if outcome.hit:
        target.take_damage(outcome.damage)
        _apply_post_damage_state(target)
    events.append(TurnEvent(actor.id, f"wizard_power_{power_id}", detail))


def _power_force_missile(
    actor: Combatant, target: Combatant | None, opts: dict,
    encounter, grid: Grid, roller: Roller, events: list[TurnEvent],
) -> None:
    """Evocation L1: automatic-hit force missile, 1d4 + intense_spells
    bonus, force type, no save. ``As Magic Missile`` means auto-hit,
    bypasses miss chance / cover."""
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "force_missile: no target"}))
        return
    if grid.distance_squares(actor.position, target.position) > 24:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "force_missile: out of range"}))
        return
    base_roll = roller.roll("1d4")
    bonus = _intense_spells_bonus(actor)
    total = int(base_roll.total) + bonus
    target.take_damage(total)
    _apply_post_damage_state(target)
    events.append(TurnEvent(actor.id, "wizard_power_force_missile", {
        "power_id": "force_missile",
        "target_id": target.id,
        "hit": True,  # automatic
        "damage": total,
        "intense_spells_bonus": bonus,
        "die_roll": int(base_roll.total),
    }))


def _roll_touch_attack(
    actor: Combatant, target: Combatant, *,
    attack_bonus: int, roller: Roller,
) -> tuple[bool, int, int]:
    """Resolve a damage-less touch attack: d20 + attack_bonus vs touch
    AC. Returns (hit, natural, total). Nat-1 auto-misses; nat-20
    auto-hits. Used by school-power handlers that deliver only a
    condition (Blinding Ray, Dazing Touch, Grave Touch)."""
    touch_ac = target.ac("touch")
    r = roller.roll("1d20")
    nat = r.terms[0].rolls[0]
    total = nat + attack_bonus
    if nat == 1:
        return False, nat, total
    if nat == 20:
        return True, nat, total
    return total >= touch_ac, nat, total


def _power_blinding_ray(
    actor: Combatant, target: Combatant | None, opts: dict,
    encounter, grid: Grid, roller: Roller, events: list[TurnEvent],
) -> None:
    """Illusion L1: ranged touch within 30 ft. On hit, blinded for 1
    round; or dazzled for 1 round if the target has more HD than the
    wizard's level."""
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "blinding_ray: no target"}))
        return
    if grid.distance_squares(actor.position, target.position) > 6:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "blinding_ray: out of range"}))
        return
    dex_mod = _ability_modifier(actor, "dex")
    size_mod = _compute_mod(0, actor.modifiers.for_target("size_attack"))
    attack_bonus = actor.bases.get("bab", 0) + dex_mod + size_mod
    hit, nat, total = _roll_touch_attack(
        actor, target, attack_bonus=attack_bonus, roller=roller,
    )
    detail = {
        "power_id": "blinding_ray", "target_id": target.id,
        "hit": hit, "natural": nat, "total": total,
        "touch_ac": target.ac("touch"),
    }
    if hit:
        target_hd = _target_hd(target)
        wl = _wizard_level(actor)
        cur_round = encounter.round_number if encounter else 1
        condition = "dazzled" if target_hd > wl else "blinded"
        target.add_condition(condition)
        target.modifiers.add(Modifier(
            value=0, type="untyped", target="_marker",
            source=f"blinding_ray:{actor.id}",
            expires_round=cur_round + 1,
        ))
        detail["condition"] = condition
    events.append(TurnEvent(
        actor.id, "wizard_power_blinding_ray", detail,
    ))


def _target_hd(target: Combatant) -> int:
    """Total HD of ``target`` for the HD-cap comparison used by several
    school powers (dazing/grave touch, blinding ray)."""
    if target.template_kind == "character" and target.template is not None:
        return int(getattr(target.template, "level", 1))
    return _monster_hd(target)


def _power_hand_of_the_apprentice(
    actor: Combatant, target: Combatant | None, opts: dict,
    encounter, grid: Grid, roller: Roller, events: list[TurnEvent],
) -> None:
    """Universalist L1: wielded melee weapon flies and strikes a foe up
    to 30 ft away. Treated as a ranged attack with a thrown weapon, but
    to-hit uses Int (not Dex); damage uses Str. Cannot perform a
    combat maneuver."""
    if target is None:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "hand_of_the_apprentice: no target",
        }))
        return
    if grid.distance_squares(actor.position, target.position) > 6:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "hand_of_the_apprentice: target out of range",
        }))
        return
    if not actor.attack_options:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "hand_of_the_apprentice: no melee weapon wielded",
        }))
        return
    primary = actor.attack_options[0]
    if primary.get("type") != "melee":
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "hand_of_the_apprentice: primary weapon is not melee",
        }))
        return
    int_mod = _ability_modifier(actor, "int")
    size_mod = _compute_mod(
        0, actor.modifiers.for_target("size_attack")
    )
    attack_bonus = actor.bases.get("bab", 0) + int_mod + size_mod
    profile = AttackProfile(
        attack_bonus=attack_bonus,
        damage_dice=str(primary["damage"]),
        damage_bonus=int(primary.get("damage_bonus", 0)),
        crit_range=tuple(primary.get("crit_range", [20, 20])),
        crit_multiplier=int(primary.get("crit_multiplier", 2)),
        damage_type=str(primary.get("damage_type", "")),
        name=f"hand_of_the_apprentice({primary.get('name', 'weapon')})",
        precision_damage_dice="0d0",
        attack_tags=frozenset({"magic"}),
    )
    outcome = resolve_attack(
        profile, target.defense_profile(), roller, situation="normal",
    )
    detail = {
        "power_id": "hand_of_the_apprentice",
        "target_id": target.id,
        "hit": outcome.hit, "crit": outcome.crit,
        "damage": outcome.damage,
        "trace": outcome.log,
    }
    if outcome.hit:
        target.take_damage(outcome.damage)
        _apply_post_damage_state(target)
    events.append(TurnEvent(
        actor.id, "wizard_power_hand_of_the_apprentice", detail,
    ))


def _power_diviners_fortune(
    actor: Combatant, target: Combatant | None, opts: dict,
    encounter, grid: Grid, roller: Roller, events: list[TurnEvent],
) -> None:
    """Divination L1: standard-action touch (any creature). Grants
    insight +max(1, wiz_lvl // 2) on attack rolls, skill checks,
    ability checks, and saving throws for 1 round."""
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "diviners_fortune: no target"}))
        return
    if not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "diviners_fortune: target not adjacent",
        }))
        return
    wl = _wizard_level(actor)
    bonus = max(1, wl // 2)
    cur_round = encounter.round_number if encounter else 1
    src = f"diviners_fortune:{actor.id}"
    target.modifiers.remove_by_source(src)
    for tgt in ("attack", "fort_save", "ref_save", "will_save",
                "skill_check", "ability_check"):
        target.modifiers.add(Modifier(
            value=bonus, type="insight", target=tgt, source=src,
            expires_round=cur_round + 1,
        ))
    events.append(TurnEvent(actor.id, "wizard_power_diviners_fortune", {
        "power_id": "diviners_fortune",
        "target_id": target.id,
        "bonus": bonus,
        "duration_rounds": 1,
    }))


def _power_dazing_touch(
    actor: Combatant, target: Combatant | None, opts: dict,
    encounter, grid: Grid, roller: Roller, events: list[TurnEvent],
) -> None:
    """Enchantment L1: melee touch attack. On hit, target dazed for 1
    round. Creatures with more HD than wizard level are unaffected."""
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "dazing_touch: no target"}))
        return
    if not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "dazing_touch: target not adjacent",
        }))
        return
    attack_bonus = (actor.bases.get("bab", 0)
                    + _ability_modifier(actor, "str"))
    hit, nat, total = _roll_touch_attack(
        actor, target, attack_bonus=attack_bonus, roller=roller,
    )
    detail = {
        "power_id": "dazing_touch", "target_id": target.id,
        "hit": hit, "natural": nat, "total": total,
        "touch_ac": target.ac("touch"),
    }
    if hit:
        target_hd = _target_hd(target)
        wl = _wizard_level(actor)
        if target_hd > wl:
            detail["condition"] = "unaffected_hd_cap"
        else:
            cur_round = encounter.round_number if encounter else 1
            target.add_condition("dazed")
            target.modifiers.add(Modifier(
                value=0, type="untyped", target="_marker",
                source=f"dazing_touch:{actor.id}",
                expires_round=cur_round + 1,
            ))
            detail["condition"] = "dazed"
    events.append(TurnEvent(
        actor.id, "wizard_power_dazing_touch", detail,
    ))


def _power_grave_touch(
    actor: Combatant, target: Combatant | None, opts: dict,
    encounter, grid: Grid, roller: Roller, events: list[TurnEvent],
) -> None:
    """Necromancy L1: melee touch attack. On hit, target shaken for
    max(1, wiz_lvl // 2) rounds. If target was already shaken from this
    power, and has fewer HD than wizard level, it becomes frightened
    for 1 round."""
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "grave_touch: no target"}))
        return
    if not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "grave_touch: target not adjacent",
        }))
        return
    attack_bonus = (actor.bases.get("bab", 0)
                    + _ability_modifier(actor, "str"))
    hit, nat, total = _roll_touch_attack(
        actor, target, attack_bonus=attack_bonus, roller=roller,
    )
    detail = {
        "power_id": "grave_touch", "target_id": target.id,
        "hit": hit, "natural": nat, "total": total,
        "touch_ac": target.ac("touch"),
    }
    if hit:
        wl = _wizard_level(actor)
        cur_round = encounter.round_number if encounter else 1
        was_shaken = "shaken" in target.conditions
        if was_shaken and _target_hd(target) < wl:
            target.add_condition("frightened")
            target.modifiers.add(Modifier(
                value=0, type="untyped", target="_marker",
                source=f"grave_touch:{actor.id}",
                expires_round=cur_round + 1,
            ))
            detail["condition"] = "frightened"
        else:
            target.add_condition("shaken")
            duration = max(1, wl // 2)
            target.modifiers.add(Modifier(
                value=0, type="untyped", target="_marker",
                source=f"grave_touch:{actor.id}",
                expires_round=cur_round + duration,
            ))
            detail["condition"] = "shaken"
            detail["duration_rounds"] = duration
    events.append(TurnEvent(
        actor.id, "wizard_power_grave_touch", detail,
    ))


def _power_protective_ward(
    actor: Combatant, target: Combatant | None, opts: dict,
    encounter, grid: Grid, roller: Roller, events: list[TurnEvent],
) -> None:
    """Abjuration L1: 10-ft radius centered on self, lasts Int-mod
    rounds. All allies in area (including caster) gain +1 deflection
    AC, +1 per 5 wizard levels."""
    int_mod = _ability_modifier(actor, "int")
    wl = _wizard_level(actor)
    bonus = 1 + (wl // 5)
    duration = max(0, int_mod)
    cur_round = encounter.round_number if encounter else 1
    src = f"protective_ward:{actor.id}"
    affected: list[str] = []
    for ir in encounter.initiative:
        c = ir.combatant
        if c.team != actor.team:
            continue
        if grid.distance_squares(actor.position, c.position) > 2:
            continue
        c.modifiers.remove_by_source(src)
        c.modifiers.add(Modifier(
            value=bonus, type="deflection", target="ac", source=src,
            expires_round=cur_round + duration,
        ))
        affected.append(c.id)
    events.append(TurnEvent(actor.id, "wizard_power_protective_ward", {
        "power_id": "protective_ward",
        "bonus": bonus,
        "duration_rounds": duration,
        "affected_ids": affected,
    }))


_WIZARD_POWER_HANDLERS = {
    "acid_dart": _power_acid_dart,
    "telekinetic_fist": _power_telekinetic_fist,
    "force_missile": _power_force_missile,
    "blinding_ray": _power_blinding_ray,
    "hand_of_the_apprentice": _power_hand_of_the_apprentice,
    "diviners_fortune": _power_diviners_fortune,
    "dazing_touch": _power_dazing_touch,
    "grave_touch": _power_grave_touch,
    "protective_ward": _power_protective_ward,
}


# ---------------------------------------------------------------------------
# Sorcerer bloodline L1 active powers
# ---------------------------------------------------------------------------


def _sorcerer_level(actor: Combatant) -> int:
    return int(actor.class_levels.get("sorcerer", 0))


def _do_sorcerer_bloodline_power(
    actor: Combatant,
    power_id: str,
    target: Combatant | None,
    options: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    events: list[TurnEvent],
) -> None:
    """Dispatch a sorcerer bloodline L1 active power.

    Shared shape with the wizard-school dispatcher: daily-pool gate
    on ``sorcerer_bloodline_<pid>_uses`` (seeded as 3 + Cha mod at
    sheet build), per-power handler in ``_BLOODLINE_POWER_HANDLERS``.
    """
    if _sorcerer_level(actor) <= 0:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "sorcerer_bloodline_power: no sorcerer levels",
        }))
        return
    res_key = f"sorcerer_bloodline_{power_id}_uses"
    uses = actor.resources.get(res_key, 0)
    if uses <= 0:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "sorcerer_bloodline_power: no uses remaining",
            "power_id": power_id,
        }))
        return
    handler = _BLOODLINE_POWER_HANDLERS.get(power_id)
    if handler is None:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "sorcerer_bloodline_power: unknown power_id",
            "power_id": power_id,
        }))
        return
    actor.resources[res_key] = uses - 1
    handler(actor, target, options, encounter, grid, roller, events)


def _target_alignment(target: Combatant) -> str:
    """Return ``target``'s alignment string in lowercase (e.g.
    ``"lawful_evil"``). For monsters, read from the template; for
    characters, from the Character.alignment."""
    if target.template is None:
        return ""
    return str(getattr(target.template, "alignment", "") or "").lower()


def _is_evil(target: Combatant) -> bool:
    align = _target_alignment(target)
    if "evil" in align:
        return True
    # Evil-outsider / undead heuristic for monsters whose alignment
    # field isn't filled in.
    if target.template_kind == "monster":
        subtypes = set(
            getattr(target.template, "subtypes", None) or [],
        )
        if "evil" in subtypes:
            return True
    return False


def _is_good(target: Combatant) -> bool:
    align = _target_alignment(target)
    return "good" in align


def _power_heavenly_fire(
    actor: Combatant, target: Combatant | None, opts: dict,
    encounter, grid: Grid, roller: Roller, events: list[TurnEvent],
) -> None:
    """Celestial L1: ranged touch within 30 ft.
    - Evil target: 1d4 + 1/2 sorc level divine damage (no ER/immunity).
    - Good target: heals 1d4 + 1/2 sorc level (1/day per creature).
    - Neutral target: no effect."""
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "heavenly_fire: no target"}))
        return
    if grid.distance_squares(actor.position, target.position) > 6:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "heavenly_fire: out of range"}))
        return
    sl = _sorcerer_level(actor)
    bonus = sl // 2
    if _is_good(target):
        # Heal — uses/day restriction per-target. We track the daily
        # cap on the target via "heavenly_fire_received_marker".
        cur_round = encounter.round_number if encounter else 1
        marker = target.resources.get(
            "heavenly_fire_received_round", -1,
        )
        if marker >= 0:
            events.append(TurnEvent(actor.id, "wizard_power_heavenly_fire", {
                "power_id": "heavenly_fire",
                "target_id": target.id,
                "result": "good_already_benefited",
            }))
            return
        heal_roll = roller.roll("1d4")
        heal = int(heal_roll.total) + bonus
        # Clamp at max_hp.
        new_hp = min(target.max_hp, target.current_hp + heal)
        actually_healed = new_hp - target.current_hp
        target.current_hp = new_hp
        target.resources["heavenly_fire_received_round"] = cur_round
        events.append(TurnEvent(actor.id, "wizard_power_heavenly_fire", {
            "power_id": "heavenly_fire",
            "target_id": target.id,
            "result": "healed_good",
            "amount": actually_healed,
            "die_roll": int(heal_roll.total),
        }))
        return
    if _is_evil(target):
        # Damage — ranged touch attack.
        dex_mod = _ability_modifier(actor, "dex")
        size_mod = _compute_mod(0, actor.modifiers.for_target("size_attack"))
        attack_bonus = actor.bases.get("bab", 0) + dex_mod + size_mod
        hit, nat, total = _roll_touch_attack(
            actor, target, attack_bonus=attack_bonus, roller=roller,
        )
        detail = {
            "power_id": "heavenly_fire",
            "target_id": target.id,
            "result": "damage_evil",
            "hit": hit, "natural": nat, "total": total,
            "touch_ac": target.ac("touch"),
        }
        if hit:
            dmg_roll = roller.roll("1d4")
            damage = int(dmg_roll.total) + bonus
            # Divine damage bypasses ER / immunity per RAW.
            target.take_damage(damage)
            _apply_post_damage_state(target)
            detail["damage"] = damage
            detail["die_roll"] = int(dmg_roll.total)
        events.append(TurnEvent(
            actor.id, "wizard_power_heavenly_fire", detail,
        ))
        return
    # Neutral: no effect.
    events.append(TurnEvent(actor.id, "wizard_power_heavenly_fire", {
        "power_id": "heavenly_fire",
        "target_id": target.id,
        "result": "neutral_no_effect",
    }))


def _power_draconic_claws(
    actor: Combatant, target: Combatant | None, opts: dict,
    encounter, grid: Grid, roller: Roller, events: list[TurnEvent],
) -> None:
    """Draconic L1: free-action grow claws. We model the daily pool
    as rounds/day — invoking this composite "spends" one round of the
    claws being active, replacing the actor's primary attack option
    with a pair of claw natural attacks for the current round.

    RAW: 2 claws at full BAB, 1d4+Str (1d3 if Small). At L5: magic;
    at L7: 1d6 (1d4 if Small); at L11: +1d6 of matching energy. The
    attack itself is up to the patron — invoking the composite just
    sets up the claws; the actual attack happens via a normal
    full_attack or single attack in the same turn.

    For v1 we install the claw attack options on the sorcerer's
    template-side ``attack_options`` and emit a "draconic_claws_set"
    event. The claws persist for the current encounter round, then
    naturally lapse when the actor's turn ticks past the marker.
    """
    sl = _sorcerer_level(actor)
    size = (actor.size or "medium").lower()
    cur_round = encounter.round_number if encounter else 1
    # Damage scaling by size and level.
    if sl >= 7:
        damage_by_size = {"small": "1d4", "medium": "1d6", "large": "1d8"}
    else:
        damage_by_size = {"small": "1d3", "medium": "1d4", "large": "1d6"}
    damage = damage_by_size.get(size, "1d4")
    str_mod = _ability_modifier(actor, "str")
    # Build the two claw attack options.
    claw_proto = {
        "type": "melee",
        "name": "claw (draconic)",
        "weapon_id": "draconic_claw",
        "weapon_category": "natural",
        "attack_bonus": actor.bases.get("bab", 0) + str_mod,
        "damage": damage,
        "damage_bonus": str_mod,
        "damage_type": "S",
        "crit_range": [20, 20],
        "crit_multiplier": 2,
        "range_increment": 0,
        "wield": "natural",
        "is_natural": True,
    }
    # Replace any prior claw entries (idempotent on re-invocation).
    actor.attack_options = [a for a in actor.attack_options
                            if a.get("weapon_id") != "draconic_claw"]
    actor.attack_options.insert(0, dict(claw_proto))
    actor.attack_options.insert(1, dict(claw_proto))
    actor.resources["draconic_claws_active_round"] = cur_round
    events.append(TurnEvent(actor.id, "wizard_power_draconic_claws", {
        "power_id": "draconic_claws",
        "result": "claws_grown",
        "damage_dice_per_claw": damage,
        "claw_count": 2,
        "round_active": cur_round,
    }))


def _power_laughing_touch(
    actor: Combatant, target: Combatant | None, opts: dict,
    encounter, grid: Grid, roller: Roller, events: list[TurnEvent],
) -> None:
    """Fey L1: melee touch. On hit, target gets ``laughing`` for 1
    round (only move-action allowed). Mind-affecting; 24h immunity
    deferred."""
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "laughing_touch: no target"}))
        return
    if not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "laughing_touch: target not adjacent",
        }))
        return
    attack_bonus = (actor.bases.get("bab", 0)
                    + _ability_modifier(actor, "str"))
    hit, nat, total = _roll_touch_attack(
        actor, target, attack_bonus=attack_bonus, roller=roller,
    )
    detail = {
        "power_id": "laughing_touch", "target_id": target.id,
        "hit": hit, "natural": nat, "total": total,
        "touch_ac": target.ac("touch"),
    }
    if hit:
        # Mind-affecting immunity check.
        if "mindless" in target.condition_immunities:
            detail["condition"] = "mind_affecting_immune"
        else:
            cur_round = encounter.round_number if encounter else 1
            target.add_condition("laughing")
            target.modifiers.add(Modifier(
                value=0, type="untyped", target="_marker",
                source=f"laughing_touch:{actor.id}",
                expires_round=cur_round + 1,
            ))
            detail["condition"] = "laughing"
    events.append(TurnEvent(
        actor.id, "wizard_power_laughing_touch", detail,
    ))


def _power_corrupting_touch(
    actor: Combatant, target: Combatant | None, opts: dict,
    encounter, grid: Grid, roller: Roller, events: list[TurnEvent],
) -> None:
    """Infernal L1: melee touch. On hit, target gets ``shaken`` for
    max(1, sorc_lvl // 2) rounds. Multiple touches add to duration."""
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "corrupting_touch: no target"}))
        return
    if not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "corrupting_touch: target not adjacent",
        }))
        return
    attack_bonus = (actor.bases.get("bab", 0)
                    + _ability_modifier(actor, "str"))
    hit, nat, total = _roll_touch_attack(
        actor, target, attack_bonus=attack_bonus, roller=roller,
    )
    detail = {
        "power_id": "corrupting_touch", "target_id": target.id,
        "hit": hit, "natural": nat, "total": total,
        "touch_ac": target.ac("touch"),
    }
    if hit:
        sl = _sorcerer_level(actor)
        new_duration = max(1, sl // 2)
        cur_round = encounter.round_number if encounter else 1
        src = f"corrupting_touch:{actor.id}"
        # RAW: multiple touches don't stack but add to duration. Find
        # the prior marker's remaining duration before clearing.
        existing = [m for m in target.modifiers.for_target("_marker")
                    if m.source == src]
        prior_remaining = 0
        for m in existing:
            prior_remaining = max(prior_remaining,
                                  (m.expires_round or cur_round)
                                  - cur_round)
        target.modifiers.remove_by_source(src)
        total_duration = prior_remaining + new_duration
        target.add_condition("shaken")
        target.modifiers.add(Modifier(
            value=0, type="untyped", target="_marker",
            source=src, expires_round=cur_round + total_duration,
        ))
        detail["condition"] = "shaken"
        detail["duration_rounds"] = total_duration
    events.append(TurnEvent(
        actor.id, "wizard_power_corrupting_touch", detail,
    ))


_BLOODLINE_POWER_HANDLERS = {
    "heavenly_fire": _power_heavenly_fire,
    "draconic_claws": _power_draconic_claws,
    "laughing_touch": _power_laughing_touch,
    "corrupting_touch": _power_corrupting_touch,
}


def _character_level(actor: Combatant) -> int:
    """Total character level for the actor; 1 for monsters / unknowns."""
    if actor.template_kind != "character" or actor.template is None:
        return 1
    lvl = getattr(actor.template, "level", None)
    return int(lvl) if lvl else 1


def _monster_hd(actor: Combatant) -> int:
    """Parse the monster's hit-dice count (e.g. '2d8+4' → 2)."""
    if actor.template_kind != "monster" or actor.template is None:
        return 1
    hd_str = str(getattr(actor.template, "hit_dice", "") or "1")
    if "d" in hd_str:
        try:
            return int(hd_str.split("d", 1)[0])
        except ValueError:
            return 1
    try:
        return int(hd_str)
    except ValueError:
        return 1


def _do_tail_spike_volley(
    actor: Combatant,
    args: dict,
    encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Manticore tail-spike volley (RAW): a standard action that
    fires 4 spikes against a single target up to 180 ft away. Each
    consumes one spike from the daily pool; the volley stops early
    if the pool runs out.
    """
    if not _has_racial_trait(actor, "tail_spikes"):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "tail_spike_volley: actor lacks the trait"}))
        return
    target = _resolve_target(args.get("target"), ns)
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "tail_spike_volley: no target"}))
        return
    spike_idx = next(
        (i for i, opt in enumerate(actor.attack_options or [])
         if str(opt.get("name", "")).lower() == "spikes"),
        None,
    )
    if spike_idx is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "tail_spike_volley: no 'spikes' attack option"}))
        return
    # RAW: a ranged action provokes one AoO from threateners; the volley
    # is a single ranged action so we provoke once before any spike
    # fires (per-shot triggers in _do_attack are gated off for this
    # label).
    if _provoke_ranged_aoo(actor, grid, events, encounter):
        return
    fired = 0
    for i in range(4):
        if int(actor.daily_resources.get("tail_spikes", 0)) <= 0:
            break
        if not target.is_alive():
            break
        _do_attack(actor, target, grid, roller, events,
                   label=f"tail_spike_volley_{i+1}",
                   encounter=encounter,
                   attack_index=spike_idx)
        fired += 1
    events.append(TurnEvent(actor.id, "tail_spike_volley", {
        "target_id": target.id,
        "fired": fired,
        "remaining": int(actor.daily_resources.get("tail_spikes", 0)),
    }))


def _do_escape_web(
    actor: Combatant,
    args: dict,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """PF1: escape from a giant-spider's web — Strength check or
    Escape Artist check vs DC 16 (one full round to escape via
    Strength; one Escape Artist check works as a standard action).

    For v1: standard action, rolls the higher of Str check or
    Escape Artist; on success removes the entangled condition
    sourced under 'web:<spider_id>'.
    """
    if "entangled" not in actor.conditions:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "escape_web: not entangled"}))
        return
    str_score = _ability_score(actor, "str")
    str_mod = (str_score - 10) // 2 if str_score > 0 else 0
    str_roll = roller.roll("1d20")
    str_total = int(str_roll.terms[0].rolls[0]) + str_mod
    ea_total = actor.skill_total("escape_artist")
    ea_roll = roller.roll("1d20")
    ea_total += int(ea_roll.terms[0].rolls[0])
    best = max(str_total, ea_total)
    passed = best >= 16
    if passed:
        # Drop entangled if any sourced_conditions entry references it
        # under a 'web:<id>' source.
        web_sourced = [
            k for k, v in actor.sourced_conditions.items()
            if k.startswith("web:") and "entangled" in v
        ]
        for src in web_sourced:
            actor.sourced_conditions.pop(src, None)
        actor.remove_condition("entangled")
    events.append(TurnEvent(actor.id, "escape_web", {
        "str_total": str_total, "ea_total": ea_total,
        "best": best, "dc": 16, "passed": passed,
    }))


def _ability_score(actor: Combatant, ability: str) -> int:
    """Read the actor's effective ability score (post racial / bumps /
    ability damage). Falls back to 10 for missing data."""
    if actor.template_kind == "character" and actor.template is not None:
        base = (actor.template.base_ability_scores or {}).get(ability) or 10
        for m in actor.modifiers.for_target(f"ability:{ability}"):
            base += m.value
        return int(base)
    if actor.template_kind == "monster" and actor.template is not None:
        scores = getattr(actor.template, "ability_scores", None) or {}
        return int(scores.get(ability, 10) or 10)
    return 10


def _do_domain_power(
    actor: Combatant,
    args: dict,
    encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Cleric / druid domain L1 granted power.

    args.domain_id selects which of the actor's two domains to use.
    The granted power's data is loaded from the registry; per-day
    uses are tracked under ``domain_<power_id>_uses`` in resources.

    Power kinds dispatched here:
      - active_touch_heal     (Healing: Rebuke Death)
      - active_touch_buff     (War: Battle Rage; Good: Touch of Good)
      - active_touch_info     (Knowledge: Lore Keeper)
      - active_ranged_damage  (Air/Earth/Fire: ranged elemental darts)
      - active_touch_condition (Evil: Touch of Evil → sickened)
      - active_self_buff      (Trickery: Copycat → concealment)
      - active_touch_damage_bleed (Death: Bleeding Touch)
      - active_ranged_weapon_attack (Magic: Hand of the Acolyte)

    Other kinds (e.g. Law's "treat d20 as 11") are tracked in coverage
    but not yet wired.
    """
    from .content import default_registry
    domain_id = str(args.get("domain_id") or "")
    if domain_id not in actor.domains:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"domain_power: actor "
                                 f"hasn't picked domain {domain_id!r}"}))
        return
    try:
        domain = default_registry().get_domain(domain_id)
    except Exception:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"domain_power: unknown "
                                 f"domain {domain_id!r}"}))
        return
    pwr = domain.granted_power_l1 or {}
    pid = pwr.get("id")
    if not pid:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"domain_power: domain "
                                 f"{domain_id!r} has no L1 power"}))
        return
    uses_key = f"domain_{pid}_uses"
    if int(actor.resources.get(uses_key, 0)) <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"domain_power: no uses "
                                 f"left ({uses_key})"}))
        return

    # Compute caster level (cleric class levels for now).
    cl = _character_level(actor)

    kind = pwr.get("kind", "")
    detail: dict = {"domain_id": domain_id, "power_id": pid, "kind": kind}

    if kind == "active_touch_heal":
        target = _resolve_target(args.get("target"), ns)
        if target is None or not grid.is_adjacent(actor, target):
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "touch_heal: target not adjacent"}))
            return
        if pwr.get("requires_target_at_or_below_zero_hp") and target.current_hp > 0:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "rebuke_death: target above 0 HP"}))
            return
        actor.resources[uses_key] = int(actor.resources[uses_key]) - 1
        dice = str(pwr.get("heal_dice", "1d4"))
        r = roller.roll(dice)
        amount = int(r.total)
        if pwr.get("heal_plus_half_cl"):
            amount += max(1, cl // 2)
        target.heal(amount)
        if target.current_hp >= 0 and "dying" in target.conditions:
            target.remove_condition("dying")
        detail.update({"target_id": target.id, "healed": amount,
                       "uses_remaining": actor.resources[uses_key]})
        events.append(TurnEvent(actor.id, "domain_power", detail))
        return

    if kind == "active_touch_buff":
        target = _resolve_target(args.get("target"), ns)
        if target is None or not grid.is_adjacent(actor, target):
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "touch_buff: target not adjacent"}))
            return
        actor.resources[uses_key] = int(actor.resources[uses_key]) - 1
        bonus_value = max(1, cl // 2)
        cur_round = encounter.round_number if encounter else 0
        duration = int(pwr.get("buff_duration_rounds", 1))
        expires = cur_round + duration
        src = f"domain:{pid}"
        primary = pwr.get("buff_modifier") or {}
        if primary:
            target.modifiers.add(Modifier(
                value=bonus_value,
                type=str(primary.get("type", "untyped")),
                target=str(primary.get("target", "attack")),
                source=src,
                expires_round=expires,
            ))
        for extra in pwr.get("extra_modifiers") or []:
            target.modifiers.add(Modifier(
                value=bonus_value,
                type=str(extra.get("type", "untyped")),
                target=str(extra.get("target", "attack")),
                source=src,
                expires_round=expires,
            ))
        detail.update({"target_id": target.id, "bonus": bonus_value,
                       "expires_round": expires,
                       "uses_remaining": actor.resources[uses_key]})
        events.append(TurnEvent(actor.id, "domain_power", detail))
        return

    if kind == "active_touch_info":
        target = _resolve_target(args.get("target"), ns)
        if target is None or not grid.is_adjacent(actor, target):
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "touch_info: target not adjacent"}))
            return
        actor.resources[uses_key] = int(actor.resources[uses_key]) - 1
        info = {"target_id": target.id, "name": target.name}
        if target.template_kind == "monster" and target.template is not None:
            info["type"] = getattr(target.template, "type", "")
            info["cr"] = getattr(target.template, "cr", "")
            info["alignment"] = getattr(target.template, "alignment", "")
        detail.update({"info": info,
                       "uses_remaining": actor.resources[uses_key]})
        events.append(TurnEvent(actor.id, "domain_power", detail))
        return

    if kind == "active_ranged_damage":
        target = _resolve_target(args.get("target"), ns)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "ranged_damage: no target"}))
            return
        # Range gate: simple Chebyshev distance.
        ax, ay = actor.position
        tx, ty = target.position
        max_squares = int(pwr.get("range_ft", 30)) // 5
        if max(abs(ax - tx), abs(ay - ty)) > max_squares:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "ranged_damage: out of range"}))
            return
        actor.resources[uses_key] = int(actor.resources[uses_key]) - 1
        dice = str(pwr.get("damage_dice", "1d6"))
        r = roller.roll(dice)
        amount = int(r.total)
        if pwr.get("damage_plus_half_cl"):
            amount += max(1, cl // 2)
        dtype = str(pwr.get("damage_type", ""))
        # Honor energy resistance / immunity for energy-typed damage.
        from .spells import apply_typed_damage
        applied, note = apply_typed_damage(
            target, amount, dtype,
            attack_tags=frozenset({"magic"}),
            roller=roller,
        )
        _apply_post_damage_state(target)
        detail.update({"target_id": target.id, "damage": applied,
                       "damage_type": dtype, "note": note,
                       "uses_remaining": actor.resources[uses_key]})
        events.append(TurnEvent(actor.id, "domain_power", detail))
        return

    if kind == "active_touch_condition":
        target = _resolve_target(args.get("target"), ns)
        if target is None or not grid.is_adjacent(actor, target):
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "touch_condition: target not adjacent"}))
            return
        actor.resources[uses_key] = int(actor.resources[uses_key]) - 1
        cond = str(pwr.get("condition", "sickened"))
        applied = target.add_condition(cond)
        detail.update({"target_id": target.id, "condition": cond,
                       "applied": applied,
                       "uses_remaining": actor.resources[uses_key]})
        events.append(TurnEvent(actor.id, "domain_power", detail))
        return

    if kind == "active_self_buff":
        actor.resources[uses_key] = int(actor.resources[uses_key]) - 1
        cur_round = encounter.round_number if encounter else 0
        duration_formula = pwr.get("buff_duration_rounds_formula", "1")
        if duration_formula == "cl_rounds":
            duration = max(1, cl)
        else:
            duration = int(pwr.get("buff_duration_rounds", 1))
        expires = cur_round + duration
        primary = pwr.get("buff_modifier") or {}
        src = f"domain:{pid}"
        if primary:
            actor.modifiers.add(Modifier(
                value=int(primary.get("value", 1)),
                type=str(primary.get("type", "untyped")),
                target=str(primary.get("target", "ac")),
                source=src,
                expires_round=expires,
            ))
        # Concealment-style targets: also bump the field directly.
        if primary.get("target") == "concealment":
            actor.concealment = max(actor.concealment, int(primary.get("value", 0)))
        detail.update({"expires_round": expires,
                       "uses_remaining": actor.resources[uses_key]})
        events.append(TurnEvent(actor.id, "domain_power", detail))
        return

    if kind == "active_touch_damage_bleed":
        target = _resolve_target(args.get("target"), ns)
        if target is None or not grid.is_adjacent(actor, target):
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "touch_damage_bleed: target not adjacent"}))
            return
        actor.resources[uses_key] = int(actor.resources[uses_key]) - 1
        dice = str(pwr.get("damage_dice", "1d6"))
        r = roller.roll(dice)
        amount = int(r.total)
        target.take_damage(amount)
        target.apply_bleed(int(pwr.get("bleed_amount", 1)))
        _apply_post_damage_state(target)
        detail.update({"target_id": target.id, "damage": amount,
                       "uses_remaining": actor.resources[uses_key]})
        events.append(TurnEvent(actor.id, "domain_power", detail))
        return

    # Unhandled kind (Law's treat-d20-as-11, Magic's Hand of the
    # Acolyte): consume use, record event with note.
    actor.resources[uses_key] = int(actor.resources[uses_key]) - 1
    detail.update({"note": f"power kind {kind!r} not yet wired",
                   "uses_remaining": actor.resources[uses_key]})
    events.append(TurnEvent(actor.id, "domain_power", detail))


def _do_detect_evil(
    actor: Combatant,
    args: dict,
    grid: Grid,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Paladin Detect Evil (at-will SLA, simplified).

    PF1 RAW: paladin can use detect evil at will, concentrating up
    to 3 rounds for full information. v1 simplification: pick one
    target; reveal whether it has an evil alignment + the alignment
    string. Used by AI to inform smite-evil targeting.
    """
    if (actor.template_kind != "character"
            or getattr(actor.template, "class_id", None) != "paladin"):
        # Multiclass paladin: walk class_levels too.
        plan = getattr(actor.template, "level_plan", None) if actor.template else None
        has_paladin = False
        if plan and isinstance(plan, dict):
            for entry in (plan.get("levels") or {}).values():
                if isinstance(entry, dict) and entry.get("class") == "paladin":
                    has_paladin = True
                    break
        if not has_paladin and (
            actor.template_kind != "character"
            or getattr(actor.template, "class_id", None) != "paladin"
        ):
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "detect_evil: not a paladin"}))
            return
    target = _resolve_target(args.get("target"), ns)
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "detect_evil: no target"}))
        return
    alignment = ""
    if target.template is not None:
        alignment = str(getattr(target.template, "alignment", "") or "")
    is_evil = "evil" in alignment.lower()
    events.append(TurnEvent(actor.id, "detect_evil", {
        "target_id": target.id,
        "alignment": alignment,
        "is_evil": is_evil,
    }))


def _do_web(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Giant-spider web composite action.

    Throws a web at a creature within 50 feet (10 squares). Target
    rolls Reflex vs DC = 10 + 1/2 HD + Con mod; failure → entangled
    (and effectively rooted, in v1, by setting speed to 0 via the
    entangled-condition's speed-halving + an extra resource flag).
    PF1 RAW gives 8 webs/day; v1 doesn't enforce a per-day cap.
    """
    if not _has_racial_trait(actor, "web_giant_spider"):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "web: actor has no web racial"}))
        return
    if int(actor.daily_resources.get("web_uses", 0)) <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "web: daily pool empty"}))
        return
    target = _resolve_target(args.get("target"), ns)
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "web: no target"}))
        return
    ax, ay = actor.position
    tx, ty = target.position
    if max(abs(ax - tx), abs(ay - ty)) > 10:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "web: target beyond 50ft"}))
        return
    from .spells import roll_save
    hd = _monster_hd(actor)
    con_mod = _ability_modifier(actor, "con")
    dc = 10 + hd // 2 + con_mod
    actor.daily_resources["web_uses"] = (
        int(actor.daily_resources.get("web_uses", 0)) - 1
    )
    passed, nat, total = roll_save(target, "ref", dc, roller)
    detail = {
        "target_id": target.id, "dc": dc,
        "natural": nat, "total": total, "passed": passed,
        "uses_remaining": int(actor.daily_resources.get("web_uses", 0)),
    }
    if not passed:
        target.add_condition("entangled")
        target.register_sourced_condition(f"web:{actor.id}", "entangled")
        detail["applied"] = "entangled"
    events.append(TurnEvent(actor.id, "web", detail))


def _resolve_paralysis_rider(
    attacker: Combatant, target: Combatant, roller: Roller,
) -> dict:
    """Ghoul-bite paralysis: target Fort save vs DC 10 + 1/2 HD + Cha mod.

    Failure → paralyzed for 1d4+1 rounds. Elves are RAW-immune to ghoul
    paralysis specifically; v1 doesn't enforce that exception. The
    paralyzed condition cascades to helpless via _IMPLIES_HELPLESS.
    """
    from .spells import roll_save
    hd = _monster_hd(attacker)
    cha_mod = _ability_modifier(attacker, "cha")
    dc = 10 + hd // 2 + cha_mod
    passed, nat, total = roll_save(target, "fort", dc, roller)
    if passed:
        return {
            "target_id": target.id, "dc": dc,
            "save_natural": nat, "save_total": total,
            "passed": True,
        }
    rounds_roll = roller.roll("1d4")
    duration = int(rounds_roll.total) + 1
    target.add_condition("paralyzed")
    return {
        "target_id": target.id, "dc": dc,
        "save_natural": nat, "save_total": total,
        "passed": False, "duration": duration,
    }


def _resolve_grab_rider(
    attacker: Combatant, target: Combatant, roller: Roller,
) -> dict:
    """Free grapple attempt after a successful natural-weapon hit.

    Stirges with ``blood_drain`` auto-grab without an opposed roll
    (RAW: stirge attaches automatically on a successful touch).
    Other grabbers (owlbear) roll an opposed CMB vs the target's CMD.
    On success, both creatures gain the ``grappled`` condition; the
    attacker's ``grappling_target_id`` and target's ``grappled_by_id``
    link the pair (consumed by grapple-action handlers).
    """
    auto_grab = _has_racial_trait(attacker, "blood_drain")
    if auto_grab:
        attacker.add_condition("grappled")
        target.add_condition("grappled")
        attacker.grappling_target_id = target.id
        target.grappled_by_id = attacker.id
        return {
            "target_id": target.id,
            "passed": True,
            "auto_grab": True,
        }
    passed, nat, total, margin = _resolve_maneuver(
        attacker, target, "grapple", roller,
    )
    if passed:
        attacker.add_condition("grappled")
        target.add_condition("grappled")
        attacker.grappling_target_id = target.id
        target.grappled_by_id = attacker.id
    return {
        "target_id": target.id,
        "natural": nat, "total": total, "margin": margin,
        "passed": passed,
    }


def _resolve_disease_rider(
    attacker: Combatant, target: Combatant, roller: Roller,
    trait_id: str, data: dict, *, encounter=None,
) -> dict:
    """Generic disease-on-bite rider. The bite-Fort save is the entry
    check. Failure: applies the ``diseased`` marker AND queues an
    ongoing ticker that re-rolls every ``period_rounds`` (default
    14400 = 1 day). PF1 RAW: 2 consecutive successful saves cure.
    Undead / constructs / oozes / plants are disease-immune.
    """
    if target.is_immune_to_disease():
        return {"target_id": target.id, "immune": True, "trait": trait_id}
    from .spells import roll_save
    hd = _monster_hd(attacker)
    save_ability = data.get("save_ability", "cha")
    dc = 10 + hd // 2 + _ability_modifier(attacker, save_ability)
    passed, nat, total = roll_save(target, "fort", dc, roller)
    detail: dict = {
        "trait": trait_id,
        "target_id": target.id, "dc": dc,
        "save_natural": nat, "save_total": total,
        "passed": passed,
    }
    if not passed:
        target.add_condition("diseased")
        cur_round = encounter.round_number if encounter else 0
        target.queue_ongoing_effect(
            id=trait_id,
            type="disease",
            period_rounds=int(data.get("period_rounds", 14400)),
            onset_rounds=int(data.get("onset_rounds", 14400)),
            remaining_ticks=data.get("remaining_ticks"),
            save_kind="fort", save_dc=dc,
            ability_damage=list(data.get("ability_damage", [])),
            cure_consec=int(data.get("cure_consec", 2)),
            current_round=cur_round,
        )
        detail["ongoing_queued"] = True
    return detail


_POISON_TRAITS: dict[str, dict] = {
    "poison_giant_spider": {
        "save_ability": "con",
        "ability_damage": [("str", "1d2")],
        "period_rounds": 1,
        "remaining_ticks": 4,
        "cure_consec": 1,
    },
    "poison_viper": {
        # Small viper: 1 round / 1d2 Con / cure 1 save.
        "save_ability": "con",
        "ability_damage": [("con", "1d2")],
        "period_rounds": 1,
        "remaining_ticks": 1,
        "cure_consec": 1,
    },
}


_DISEASE_TRAITS: dict[str, dict] = {
    "diseased_bite": {
        # Ghoul fever (RAW DC 13 for a 2-HD ghoul; computed via the
        # standard 10 + 1/2 HD + Cha mod formula here).
        "save_ability": "cha",
        "ability_damage": [("con", "1d3"), ("dex", "1d3")],
        "period_rounds": 14400,   # 1 day at 1 round / 6 seconds
        "onset_rounds": 14400,    # PF1 onset 1 day
        "cure_consec": 2,
    },
    "filth_fever": {
        # Otyugh / dire-rat-style filth fever: Con-based DC, Dex+Con
        # damage, same day cadence.
        "save_ability": "con",
        "ability_damage": [("dex", "1d3"), ("con", "1d3")],
        "period_rounds": 14400,
        "onset_rounds": 14400,
        "cure_consec": 2,
    },
}


def _matching_poison_trait(actor: Combatant) -> tuple[str, dict] | None:
    for trait_id, data in _POISON_TRAITS.items():
        if _has_racial_trait(actor, trait_id):
            return trait_id, data
    return None


def _matching_disease_trait(actor: Combatant) -> tuple[str, dict] | None:
    for trait_id, data in _DISEASE_TRAITS.items():
        if _has_racial_trait(actor, trait_id):
            return trait_id, data
    return None


def _resolve_poison_rider(
    attacker: Combatant, target: Combatant, roller: Roller,
    trait_id: str, data: dict, *, encounter=None,
) -> dict:
    """Generic poison-on-bite rider. The initial Fort save is the entry
    check; failure queues an ongoing-effect ticker per ``data``.
    Poison-immune targets (vermin / undead / construct / ooze / plant)
    skip the entry entirely.
    """
    if target.is_immune_to_poison():
        return {"target_id": target.id, "immune": True, "trait": trait_id}
    from .spells import roll_save
    hd = _monster_hd(attacker)
    save_ability = data.get("save_ability", "con")
    dc = 10 + hd // 2 + _ability_modifier(attacker, save_ability)
    passed, nat, total = roll_save(target, "fort", dc, roller)
    detail: dict = {
        "trait": trait_id,
        "target_id": target.id, "dc": dc,
        "save_natural": nat, "save_total": total,
        "passed": passed,
    }
    if not passed:
        cur_round = encounter.round_number if encounter else 0
        target.queue_ongoing_effect(
            id=trait_id,
            type="poison",
            period_rounds=int(data.get("period_rounds", 1)),
            remaining_ticks=data.get("remaining_ticks"),
            save_kind="fort", save_dc=dc,
            ability_damage=list(data.get("ability_damage", [])),
            cure_consec=int(data.get("cure_consec", 1)),
            current_round=cur_round,
            onset_rounds=int(data.get("onset_rounds", 1)),
        )
        detail["ongoing_queued"] = True
    return detail


def _resolve_stunning_fist(
    attacker: Combatant,
    target: Combatant,
    roller: Roller,
    encounter,
) -> dict:
    """Apply the Stunning Fist Fort save to ``target`` on a successful
    hit. Returns an event-detail dict; the caller appends the event."""
    from .spells import roll_save
    dc = int(attacker.resources.get("stunning_fist_dc", 14))
    cur_round = encounter.round_number if encounter else 1
    passed, nat, total = roll_save(target, "fort", dc, roller)
    if passed:
        return {
            "target_id": target.id, "dc": dc,
            "save_natural": nat, "save_total": total,
            "passed": True,
        }
    # Fail: target is stunned 1 round. We use a side-channel resource
    # to track expiration, since conditions don't have built-in
    # durations. Combatant.tick_round clears it on expiry.
    target.add_condition("stunned")
    target.resources["stunned_until_round"] = cur_round + 1
    return {
        "target_id": target.id, "dc": dc,
        "save_natural": nat, "save_total": total,
        "passed": False, "stunned_until_round": cur_round + 1,
    }


def _do_stunning_fist(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Stunning Fist: declare a Fort-save rider on a melee attack.

    PF1: as part of using the feat (or monk class feature), the next
    melee attack you make this turn carries a Fort save (DC 10 + 1/2
    character level + Wis modifier). On hit, target rolls Fort or
    becomes stunned for 1 round. The use is consumed regardless of
    whether the attack hits.

    For v1 this composite bundles the declaration + the attack into
    a single action: pick a target, swing, and (on hit) the Fort
    save fires automatically.
    """
    uses = actor.resources.get("stunning_fist_uses", 0)
    if uses <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "no stunning_fist uses left"}))
        return
    target = _resolve_target(args.get("target"), ns)
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "stunning_fist: no target"}))
        return
    if not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "stunning_fist: target not adjacent"}))
        return

    # Consume the use (PF1 RAW: lost whether or not the attack lands).
    actor.resources["stunning_fist_uses"] = uses - 1

    # Compute the save DC: 10 + 1/2 char level + Wis mod.
    cur_round = encounter.round_number if encounter else 1
    char_level = _character_level(actor)
    wis_mod = _ability_modifier(actor, "wis")
    dc = 10 + char_level // 2 + wis_mod

    # Stash the DC so _do_attack can read it after rolling the attack.
    actor.add_condition("stunning_fist_pending")
    actor.resources["stunning_fist_dc"] = dc
    actor.resources["stunning_fist_round"] = cur_round

    events.append(TurnEvent(actor.id, "stunning_fist_declare", {
        "target_id": target.id, "dc": dc,
        "uses_remaining": actor.resources["stunning_fist_uses"],
    }))

    # Now run the attack; _do_attack handles the post-hit Fort save.
    _do_attack(actor, target, grid, roller, events,
               label="stunning_fist_attack", encounter=encounter,
               script_options=args.get("options") or {})

    # Clear the pending flag whether or not the attack hit.
    actor.remove_condition("stunning_fist_pending")
    actor.resources.pop("stunning_fist_dc", None)
    actor.resources.pop("stunning_fist_round", None)


def _do_coup_de_grace(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """PF1 coup-de-grace: full-round attack against a helpless target.

    Auto-hits, auto-crits (max die count, multiplied bonus), and the
    target makes a Fort save vs DC = 10 + damage dealt; failure
    instantly kills. Provokes AoO from threateners adjacent to the
    actor (PF1 RAW: "delivering a coup de grace provokes attacks of
    opportunity from threatening opponents").
    """
    target = _resolve_target(args.get("target"), ns)
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "coup_de_grace: no target"}))
        return
    if "helpless" not in target.conditions:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "coup_de_grace: target not helpless"}))
        return
    if not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "coup_de_grace: target not adjacent"}))
        return
    options = actor.attack_options
    if not options:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "coup_de_grace: actor has no weapon"}))
        return
    # Provoke AoO from each threatening enemy before the strike resolves.
    # Helpless / sleeping / dazed / fascinated / panicked / cowering /
    # nauseated creatures cannot react with an AoO.
    _CANNOT_AOO = frozenset({
        "helpless", "sleeping", "paralyzed", "petrified", "stunned",
        "unconscious", "dying", "dead", "pinned", "dazed",
        "fascinated", "panicked", "cowering", "nauseated",
    })
    if grid is not None:
        for cid, other in list(grid.combatants.items()):
            if other.id == actor.id or other.team == actor.team:
                continue
            if other.conditions & _CANNOT_AOO:
                continue
            if grid.threatens(other, actor):
                _do_aoo(other, actor, grid, events, encounter=encounter)
                if actor.current_hp <= 0:
                    return
    chosen = options[0]
    crit_mult = int(chosen.get("crit_multiplier", 2))
    damage_dice = str(chosen["damage"])
    damage_bonus = int(chosen.get("damage_bonus", 0))
    from .combat import damage_roll
    raw_damage, individual = damage_roll(
        roller, damage_dice, damage_bonus, crit_dice_count=crit_mult,
    )
    raw_damage = max(1, raw_damage)
    target.take_damage(raw_damage,
                       damage_type=str(chosen.get("damage_type", "")))
    fort_dc = 10 + raw_damage
    r_save = roller.roll("1d20")
    save_nat = r_save.terms[0].rolls[0]
    save_total = save_nat + target.save("fort")
    save_passed = save_total >= fort_dc
    died = False
    if not save_passed:
        target.add_condition("dead")
        died = True
    elif target.current_hp <= target.death_threshold:
        target.add_condition("dead")
        died = True
    events.append(TurnEvent(actor.id, "coup_de_grace", {
        "target_id": target.id,
        "weapon": chosen.get("name", "weapon"),
        "damage": raw_damage,
        "individual": individual,
        "crit_multiplier": crit_mult,
        "fort_dc": fort_dc,
        "fort_natural": save_nat,
        "fort_total": save_total,
        "fort_passed": save_passed,
        "died": died,
    }))


def _resolve_maneuver(
    actor: Combatant,
    target: Combatant,
    kind: str,
    roller: Roller,
    cmb_delta: int = 0,
) -> tuple[bool, int, int, int]:
    """Roll d20 + actor.cmb vs target.cmd(context={"maneuver": kind}).

    Returns ``(passed, natural, total, margin)`` where ``margin`` is
    ``total - cmd`` (positive on success). The maneuver kind is
    forwarded to ``cmd`` so situational bonuses (dwarven Stability
    vs trip / bullrush) qualify.

    Trip-CMB bonus from the wielded weapon (whip, scythe, flail = +2)
    is layered on for ``kind == "trip"``. The Improved-X feat for
    the matching maneuver adds +2 CMB.

    ``cmb_delta`` is a flat per-attempt bonus/penalty. Used by
    flurry-of-blows substitution to apply the monk-level BAB swap-in
    and the -2 TWF-style flurry penalty to the maneuver's CMB roll.
    """
    cmb = actor.cmb() + cmb_delta
    if kind == "trip" and actor.attack_options:
        weapon_id = actor.attack_options[0].get("weapon_id")
        if weapon_id:
            from .content import default_registry
            try:
                w = default_registry().get_weapon(weapon_id)
                cmb += w.trip_bonus
            except Exception:
                pass
    improved_feat = _IMPROVED_FEAT_FOR_MANEUVER.get(kind)
    if improved_feat and _has_feat(actor, improved_feat):
        cmb += 2
    cmd = target.cmd(context={"maneuver": kind})
    r = roller.roll("1d20")
    nat = r.terms[0].rolls[0]
    total = nat + cmb
    if nat == 20:
        passed = True
    elif nat == 1:
        passed = False
    else:
        passed = total >= cmd
    return passed, nat, total, total - cmd


_MANEUVER_KINDS = frozenset({
    "trip", "disarm", "sunder", "bull_rush", "grapple",
    "drag", "overrun", "reposition", "steal", "dirty_trick",
})

# RAW (Flurry of Blows): "A monk may substitute disarm, sunder, and
# trip combat maneuvers for unarmed attacks as part of a flurry of
# blows." Only these three kinds qualify.
_FLURRY_SUBSTITUTABLE_MANEUVERS = frozenset({"trip", "disarm", "sunder"})

# RAW: weapons usable in a flurry — unarmed strike plus the monk's
# special-weapon group (CRB monk class entry — kama, nunchaku,
# quarterstaff, sai, shuriken, siangham, temple sword). Other weapons
# the monk is proficient with (club, dagger, etc.) are NOT flurryable.
_MONK_FLURRY_WEAPONS = frozenset({
    "unarmed_strike", "kama", "nunchaku", "quarterstaff", "sai",
    "shuriken", "siangham", "temple_sword",
})

# Per-maneuver mapping to the Improved-X feat that grants:
#   - +2 CMB on this maneuver
#   - skips the AoO that the maneuver attempt would otherwise provoke
_IMPROVED_FEAT_FOR_MANEUVER: dict[str, str] = {
    "trip": "improved_trip",
    "disarm": "improved_disarm",
    "sunder": "improved_sunder",
    "bull_rush": "improved_bull_rush",
    "grapple": "improved_grapple",
    "overrun": "improved_overrun",
    "drag": "improved_drag",
    "reposition": "improved_reposition",
    "steal": "improved_steal",
    "dirty_trick": "improved_dirty_trick",
}

# Conditions a dirty-trick attacker may apply (RAW menu).
_DIRTY_TRICK_CONDITIONS: frozenset[str] = frozenset({
    "blinded", "dazzled", "deafened", "entangled", "shaken", "sickened",
})


def _do_combat_maneuver(
    actor: Combatant,
    kind: str,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
    cmb_delta: int = 0,
) -> None:
    """Standalone combat-maneuver composite.

    All maneuvers share the d20 + CMB vs CMD primitive. PF1 RAW:
    each maneuver provokes an AoO from the target unless the actor
    has the matching ``improved_<kind>`` feat. The Improved feat
    also grants +2 CMB on that maneuver (applied in _resolve_maneuver).

    Effects on success vary by kind — see ``_apply_maneuver_effect``.

    ``cmb_delta`` is forwarded to _resolve_maneuver. Used by flurry of
    blows substitution: the maneuver's CMB roll inherits the flurry's
    monk-level BAB swap-in and -2 TWF-style penalty.
    """
    if kind not in _MANEUVER_KINDS:
        raise ValueError(f"unknown maneuver kind {kind!r}")
    target = _resolve_target(args.get("target"), ns)
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"{kind}: no target"}))
        return
    if not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"{kind}: target not adjacent"}))
        return

    # AoO provocation: unless the actor has the Improved-X feat for
    # this maneuver, the target gets a free attack of opportunity
    # against the actor before the CMB roll resolves.
    improved_feat = _IMPROVED_FEAT_FOR_MANEUVER.get(kind)
    provokes = improved_feat is None or not _has_feat(actor, improved_feat)
    if provokes and not (
        target.is_unconscious()
        or target.conditions & {
            "helpless", "sleeping", "paralyzed", "petrified",
            "stunned", "dazed", "fascinated", "panicked",
            "cowering", "nauseated",
        }
    ):
        # Target retaliates with one AoO (subject to their per-round
        # AoO budget — _do_aoo respects Combat Reflexes / Dex limits).
        _do_aoo(target, actor, grid, events, encounter=encounter)
        if actor.current_hp <= 0:
            return  # actor incapacitated by AoO; skip the maneuver

    passed, nat, total, margin = _resolve_maneuver(
        actor, target, kind, roller, cmb_delta=cmb_delta,
    )
    detail = {
        "kind": kind, "target_id": target.id,
        "natural": nat, "total": total, "margin": margin,
        "passed": passed,
        "provoked_aoo": provokes,
    }
    if passed:
        _apply_maneuver_effect(
            actor, target, kind, margin, grid, detail,
            args=args, encounter=encounter, roller=roller,
        )
    events.append(TurnEvent(actor.id, f"maneuver_{kind}", detail))


def _apply_maneuver_effect(
    actor: Combatant,
    target: Combatant,
    kind: str,
    margin: int,
    grid: Grid,
    detail: dict,
    *,
    args: dict | None = None,
    encounter: object | None = None,
    roller: Roller | None = None,
) -> None:
    args = args or {}
    if kind == "trip":
        if target.add_condition("prone"):
            detail["effect"] = "prone"
        else:
            detail["effect"] = "immune"
    elif kind == "disarm":
        # PF1 RAW: success removes the held weapon. Margin ≥ 10
        # transfers it to the disarmer; otherwise the weapon falls to
        # the target's square. We model "falls to ground" as moving
        # the InventoryItem to a side-channel ``dropped_items`` list
        # on the encounter (or carried_items on the disarmer for
        # margin ≥ 10).
        item = target.held_items.pop("main_hand", None)
        if item is None:
            detail["effect"] = "no_weapon"
        else:
            # Also clear from attack_options so target can't keep
            # using the disarmed weapon.
            target.attack_options = [
                opt for opt in target.attack_options
                if not (opt.get("weapon_id") == item.item_id
                        and not opt.get("is_offhand"))
            ]
            if margin >= 10:
                # Transferred to disarmer's carried items.
                actor.carried_items.append(item)
                detail["effect"] = "disarmed_to_actor"
            else:
                # Dropped at target's square — record on the encounter
                # if it has a ``dropped_items`` dict; otherwise just
                # discard (target will need to retrieve_stowed_item to
                # pick it back up next turn).
                if hasattr(encounter, "dropped_items"):
                    sq = target.position
                    encounter.dropped_items.setdefault(sq, []).append(item)
                detail["effect"] = "disarmed_to_ground"
            detail["disarmed_item_id"] = item.item_id
    elif kind == "sunder":
        # PF1 RAW: damage the wielded weapon (or shield, optionally).
        # We default to main_hand. Damage = weapon damage roll on the
        # actor's primary attack, modified by hardness. At half max
        # HP, item gets ``broken``. At 0 HP, destroyed and removed.
        item = target.held_items.get("main_hand")
        if item is None:
            detail["effect"] = "no_target_weapon"
        else:
            # Use the actor's primary weapon damage as the sunder
            # damage roll. We don't bother re-rolling here; just
            # take the average of the dice plus damage_bonus as a
            # rough damage estimate. (Full damage roll could go in
            # later when sunder cares about crits etc.)
            actor_attack = (actor.attack_options[0]
                            if actor.attack_options else None)
            damage = 0
            if actor_attack:
                # Roll the weapon damage.
                dmg_dice = str(actor_attack.get("damage", "1d4"))
                dmg_bonus = int(actor_attack.get("damage_bonus", 0))
                r = roller.roll(dmg_dice)
                damage = r.total + dmg_bonus
            actual_loss = item.take_damage(max(0, damage))
            detail["effect"] = "sundered"
            detail["sunder_damage"] = damage
            detail["item_hp_loss"] = actual_loss
            detail["item_hp_remaining"] = item.current_hp
            detail["item_broken"] = item.broken
            if item.is_destroyed():
                target.held_items.pop("main_hand", None)
                target.attack_options = [
                    opt for opt in target.attack_options
                    if not (opt.get("weapon_id") == item.item_id
                            and not opt.get("is_offhand"))
                ]
                detail["item_destroyed"] = True
    elif kind == "grapple":
        actor.add_condition("grappled")
        target.add_condition("grappled")
        actor.grappling_target_id = target.id
        target.grappled_by_id = actor.id
        detail["effect"] = "grappled"
    elif kind == "bull_rush":
        # Push direction: from actor toward target's far side.
        dx = (target.position[0] - actor.position[0])
        dy = (target.position[1] - actor.position[1])
        ux = (dx > 0) - (dx < 0)
        uy = (dy > 0) - (dy < 0)
        squares_to_push = 1 + (margin // 5)
        new_pos = target.position
        squares_pushed = 0
        for _ in range(squares_to_push):
            cand = (new_pos[0] + ux, new_pos[1] + uy)
            if not grid.in_bounds(*cand):
                break
            if not grid.is_passable(*cand):
                break
            try:
                grid.move(target, cand)
            except Exception:
                break
            new_pos = cand
            squares_pushed += 1
        detail["effect"] = "pushed"
        detail["squares_pushed"] = squares_pushed
        detail["new_position"] = list(new_pos)
    elif kind == "drag":
        # PF1: pull target 5 ft + 5/+5 over CMD, ending each square
        # closer to the puller. Direction: opposite of the bull-rush
        # vector (toward the actor).
        dx = (actor.position[0] - target.position[0])
        dy = (actor.position[1] - target.position[1])
        ux = (dx > 0) - (dx < 0)
        uy = (dy > 0) - (dy < 0)
        squares_to_pull = 1 + (margin // 5)
        new_pos = target.position
        squares_pulled = 0
        for _ in range(squares_to_pull):
            cand = (new_pos[0] + ux, new_pos[1] + uy)
            if not grid.in_bounds(*cand):
                break
            if not grid.is_passable(*cand):
                break
            # Don't drag the target onto the actor's own square.
            if cand == actor.position:
                break
            try:
                grid.move(target, cand)
            except Exception:
                break
            new_pos = cand
            squares_pulled += 1
        detail["effect"] = "dragged"
        detail["squares_pulled"] = squares_pulled
        detail["new_position"] = list(new_pos)
    elif kind == "overrun":
        # PF1 RAW: on success move through the target's space; if
        # margin >= 5 the target is also knocked prone. We move the
        # actor through (one square past the target along the line),
        # leaving the target where they were.
        dx = (target.position[0] - actor.position[0])
        dy = (target.position[1] - actor.position[1])
        ux = (dx > 0) - (dx < 0)
        uy = (dy > 0) - (dy < 0)
        through = (target.position[0] + ux, target.position[1] + uy)
        moved = False
        if grid.in_bounds(*through) and grid.is_passable(*through):
            try:
                grid.move(actor, through)
                moved = True
            except Exception:
                moved = False
        detail["effect"] = "overran"
        detail["actor_new_position"] = list(actor.position)
        if margin >= 5:
            target.add_condition("prone")
            detail["target_prone"] = True
        if not moved:
            detail["note"] = "blocked past target"
    elif kind == "reposition":
        # Move target to any square within (1 + margin//5) of their
        # original position. The args may carry a "destination" field
        # the patron picks; otherwise we default to one square in the
        # opposite direction (a "shove off" feel).
        max_distance = 1 + (margin // 5)
        # Default: shove away from actor by one square.
        dx = (target.position[0] - actor.position[0])
        dy = (target.position[1] - actor.position[1])
        ux = (dx > 0) - (dx < 0)
        uy = (dy > 0) - (dy < 0)
        default_dest = (
            target.position[0] + ux, target.position[1] + uy,
        )
        dest = detail.get("destination") or default_dest
        # Validate distance.
        td = grid.distance_squares(target.position, dest)
        if (
            td <= max_distance
            and grid.in_bounds(*dest)
            and grid.is_passable(*dest)
        ):
            try:
                grid.move(target, dest)
            except Exception:
                pass
        detail["effect"] = "repositioned"
        detail["new_position"] = list(target.position)
        detail["max_distance"] = max_distance
    elif kind == "dirty_trick":
        # PF1 RAW: pick one of blinded / dazzled / deafened /
        # entangled / shaken / sickened. Duration = 1 round + 1
        # round per 5 by which the CMB exceeded the CMD. The condition
        # can be removed by a standard action (not modeled here — the
        # condition just sits there until tick removes it).
        cond = str(args.get("condition", "dazzled")).lower()
        if cond not in _DIRTY_TRICK_CONDITIONS:
            cond = "dazzled"
        duration = 1 + max(0, margin // 5)
        applied = target.add_condition(cond)
        detail["effect"] = "dirty_trick"
        detail["condition"] = cond
        detail["duration"] = duration
        detail["applied"] = applied
        if not applied:
            detail["note"] = "target_immune"
    elif kind == "steal":
        # PF1: take a small carried item (not held weapon — that's
        # disarm). On success, transfer one carried item from target
        # to actor. The script can specify which via args.item_id;
        # otherwise we take the first one available.
        wanted_item_id = args.get("item_id")
        chosen_idx: int | None = None
        for i, it in enumerate(target.carried_items):
            if wanted_item_id is None or it.item_id == wanted_item_id:
                chosen_idx = i
                break
        if chosen_idx is None:
            detail["effect"] = "no_carried_item"
        else:
            item = target.carried_items.pop(chosen_idx)
            actor.carried_items.append(item)
            detail["effect"] = "stolen"
            detail["stolen_item_id"] = item.item_id
            detail["stolen_instance_id"] = item.instance_id


def _do_aid_another(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Aid Another (PF1).

    Standard action. Pick an ally and a foe; roll an attack vs DC 10
    (an attack roll against an "imaginary" AC 10). On success, your
    ally gets a +2 bonus to either their next attack roll against that
    foe (mode='attack') or +2 dodge AC vs that foe (mode='ac'),
    until the start of your next turn.

    Limitations in v1:
      - The "vs that specific foe" restriction isn't modeled; the
        bonus applies universally to the ally for one round.
      - The "next attack" precision isn't modeled; uses 1-round
        duration instead.
    """
    ally = _resolve_target(args.get("ally"), ns)
    foe = _resolve_target(args.get("foe"), ns)
    mode = args.get("mode", "attack")
    if ally is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "aid_another: no ally"}))
        return
    if foe is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "aid_another: no foe"}))
        return
    if mode not in ("attack", "ac"):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"aid_another: unknown mode {mode!r}"}))
        return
    if not grid.is_adjacent(actor, foe):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "aid_another: foe not in melee reach"}))
        return

    # Roll d20 + actor's primary attack bonus vs DC 10.
    if not actor.attack_options:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "aid_another: no attack options"}))
        return
    attack_bonus = int(actor.attack_options[0].get("attack_bonus", 0))
    r = roller.roll("1d20")
    nat = r.terms[0].rolls[0]
    total = nat + attack_bonus
    success = total >= 10

    cur_round = encounter.round_number if encounter else 1
    if success:
        target_field = "attack" if mode == "attack" else "ac"
        mod_type = "circumstance" if mode == "attack" else "dodge"
        src = f"aid_another:{actor.id}:{cur_round}:{foe.id}"
        # Qualifier: bonus only applies vs the specific foe we aided
        # against. ``attack`` mode → match attacker_target_id when
        # ally attacks; ``ac`` mode → match attacker_id when foe
        # attacks ally. We use the same qualifier key on both so the
        # context plumbing is uniform.
        from .modifiers import Modifier as _Mod
        if mode == "attack":
            qualifier = (("target_id", (foe.id,)),)
        else:
            qualifier = (("attacker_id", (foe.id,)),)
        ally.modifiers.add(_Mod(
            value=2, type=mod_type, target=target_field,
            source=src, expires_round=cur_round + 1,
            qualifier=qualifier,
        ))
    events.append(TurnEvent(actor.id, "aid_another", {
        "ally_id": ally.id,
        "foe_id": foe.id,
        "mode": mode,
        "attack_natural": nat,
        "attack_total": total,
        "dc": 10,
        "passed": success,
    }))


def _do_cast(
    actor: Combatant,
    args: dict,
    encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Cast a spell. ``args`` has ``spell``, ``target``, ``spell_level``,
    optional ``defensive`` flag."""
    spell_id = args.get("spell")
    if not spell_id:
        events.append(TurnEvent(actor.id, "skip", {"reason": "cast: no spell"}))
        return
    # Resolve registry.
    from .content import default_registry
    registry = default_registry()
    try:
        spell = registry.get_spell(spell_id)
    except Exception as e:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"unknown spell {spell_id!r}: {e}"}))
        return

    # Casting-time classification. Emit a structured event so callers
    # can see what the spell's RAW casting time was (the engine still
    # resolves multi-round casts on the same turn — proper deferral to
    # 'just before the caster's next turn' is a separate, larger
    # change). Standard / swift casts pass through silently.
    ct_class = _classify_casting_time(spell.casting_time)
    if ct_class in ("multi_round", "full_round"):
        events.append(TurnEvent(actor.id, "cast_long_casting_time", {
            "spell_id": spell_id,
            "casting_time": spell.casting_time,
            "classification": ct_class,
            "note": (
                "RAW: spell completes 'just before the caster's next "
                "turn' (or N rounds later); engine resolves on the "
                "current turn for now."
            ),
        }))

    # Knowledge / preparation check.
    if actor.castable_spells and spell_id not in actor.castable_spells:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": f"actor cannot cast {spell_id!r} (not on class spell list "
                      f"or above castable level)",
        }))
        return

    base_spell_level = int(args.get("spell_level", 1))
    # Metamagic level adjustment: each applied feat raises the slot
    # cost by a fixed amount (PF1 RAW). The save-DC stays at the base
    # level — we don't pass the bumped level into save_dc_for.
    metamagic = list(args.get("metamagic") or [])
    metamagic_bump = 0
    metamagic_bumps = {
        "empower_spell": 2,
        "maximize_spell": 3,
        "quicken_spell": 4,
        "still_spell": 1,
        "silent_spell": 1,
        "extend_spell": 1,
        "heighten_spell": 0,  # variable; caller specifies effective_spell_level
    }
    for mm in metamagic:
        metamagic_bump += metamagic_bumps.get(mm, 0)
        # Validate the caster has the feat.
        if not _has_feat(actor, mm):
            events.append(TurnEvent(actor.id, "skip", {
                "reason": f"metamagic {mm!r} requires the feat",
            }))
            return
    spell_level = base_spell_level + metamagic_bump

    # RAW (Arcane Bond, Foundry pack ``Arcane Bond``): "A bonded
    # object can be used once per day to cast any one spell that the
    # wizard has in his spellbook and is capable of casting, even if
    # the spell is not prepared. ... This spell cannot be modified
    # by metamagic feats or other abilities. The bonded object
    # cannot be used to cast spells from the wizard's opposition
    # schools." Gate first so the metamagic / opposition / use-pool
    # rejections fire before the slot-count check.
    use_bond = bool(args.get("use_arcane_bond"))
    if use_bond:
        if actor.template_kind != "character" or actor.template is None:
            events.append(TurnEvent(actor.id, "skip", {
                "reason": "use_arcane_bond: actor is not a player character",
            }))
            return
        if int(actor.class_levels.get("wizard", 0)) <= 0:
            events.append(TurnEvent(actor.id, "skip", {
                "reason": "use_arcane_bond: actor has no wizard levels",
            }))
            return
        if metamagic:
            events.append(TurnEvent(actor.id, "skip", {
                "reason": "use_arcane_bond: spell cannot be modified "
                          "by metamagic per RAW",
                "metamagic": metamagic,
            }))
            return
        opposition = tuple(
            (actor.template.class_choices or {}).get(
                "wizard_opposition_schools",
            ) or ()
        )
        if (spell.school or "").lower() in opposition:
            events.append(TurnEvent(actor.id, "skip", {
                "reason": "use_arcane_bond: cannot cast spells from "
                          "opposition schools per RAW",
                "spell_school": spell.school,
                "opposition_schools": list(opposition),
            }))
            return
        if actor.resources.get("arcane_bond_uses", 0) <= 0:
            events.append(TurnEvent(actor.id, "skip", {
                "reason": "use_arcane_bond: 1/day already spent",
            }))
            return
        actor.resources["arcane_bond_uses"] = (
            actor.resources.get("arcane_bond_uses", 0) - 1
        )
        # The bonded cast still consumes a slot (RAW: "treated like any
        # other spell"). Falls through to the slot check below.

    slot_key = f"spell_slot_{spell_level}"
    remaining = actor.resources.get(slot_key, 0)
    # Cleric domain bonus slot: if the spell qualifies (cast at base
    # level, no metamagic bump above base, and spell_id is in this
    # cleric's domain_spells set for that level), the bonus
    # ``domain_slot_<L>`` counts as available.
    domain_slot_remaining = 0
    if (
        metamagic_bump == 0
        and spell_id in (actor.domain_spells.get(base_spell_level) or set())
    ):
        domain_slot_remaining = int(
            actor.resources.get(f"domain_slot_{base_spell_level}", 0),
        )
    if remaining <= 0 and domain_slot_remaining <= 0:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": f"no spell slots remaining at level {spell_level}"
                      f" (base {base_spell_level} + {metamagic_bump} metamagic)",
        }))
        return

    # ── Prepared casters: spell must be in prepared_spells ──────────
    # Prepared casters consume one entry from prepared_spells[level]
    # in addition to the slot. Spontaneous casters skip this check —
    # any spell in castable_spells of legal level is fair game. The
    # prepared list may have duplicates (a wizard who prepared
    # magic_missile twice can cast it twice).
    #
    # Permissive fallback: if a prepared caster's prepared_spells is
    # entirely empty (no prep for any level), we treat the actor as
    # if spontaneous. This keeps the "default-dispatch hero with no
    # prep specified" path working — castable_spells is the gate.
    # As soon as ANY prep exists for ANY level, the prepared-caster
    # rules apply at every level (an empty list at a specific level
    # = nothing prepared at that level).
    has_any_prep = bool(actor.prepared_spells) and any(
        actor.prepared_spells.values()
    )
    # Cleric / druid spontaneous casting: at cast time, the actor can
    # sacrifice any prepared spell of the same level to cast a cure
    # (cleric: good-aligned) or summon-nature's-ally (druid) instead.
    # We support cleric cure-swap via an explicit args.spontaneous_cure
    # flag — any prep at the same level can be consumed, and the cast
    # spell must be a cure_X variant.
    spontaneous_cure = bool(args.get("spontaneous_cure"))
    if spontaneous_cure:
        if not _is_cleric_class(actor):
            events.append(TurnEvent(actor.id, "skip", {
                "reason": "spontaneous_cure: actor is not a cleric",
            }))
            return
        if not spell_id.startswith("cure_"):
            events.append(TurnEvent(actor.id, "skip", {
                "reason": "spontaneous_cure: target spell must be a cure_X",
            }))
            return
    use_bond = bool(args.get("use_arcane_bond"))

    if (
        actor.casting_type == "prepared"
        and has_any_prep
        and not spontaneous_cure
        and not use_bond
    ):
        prep_list = actor.prepared_spells.get(base_spell_level, [])
        if spell_id not in prep_list:
            events.append(TurnEvent(actor.id, "skip", {
                "reason": f"spell {spell_id!r} not prepared at level "
                          f"{base_spell_level} (prepared casters must "
                          f"have it in their daily prep)",
                "prepared_at_level": list(prep_list),
            }))
            return

    def _consume_slot() -> None:
        """Decrement the spell slot and (for prepared casters with
        an active prep) remove one matching entry from
        prepared_spells. Called once per cast-attempt that gets past
        the prepared-spell check, even if the cast subsequently
        fails (RAW: ASF / concentration failure still consumes the
        slot AND the prep).

        Cantrips/orisons (level-0 spells) are at-will per RAW —
        prepared casters keep them in prepared_spells but neither
        slot nor prep entry is consumed. Spontaneous casters can
        cast known cantrips freely too. So spell_level == 0 is
        a no-op here.

        Cleric bonus domain slot: when the spell being cast is one
        of the cleric's domain spells at this level AND the
        ``domain_slot_<L>`` pool has a use available, that slot is
        consumed in preference to the regular spell_slot_<L>. The
        prep-entry burn still happens normally (the domain spell is
        prepped in the bonus slot).
        """
        if base_spell_level == 0:
            return
        # Prefer the bonus domain slot when applicable.
        domain_set = actor.domain_spells.get(base_spell_level) or set()
        domain_slot_key = f"domain_slot_{base_spell_level}"
        if (
            spell_id in domain_set
            and int(actor.resources.get(domain_slot_key, 0)) > 0
        ):
            actor.resources[domain_slot_key] = (
                int(actor.resources[domain_slot_key]) - 1
            )
        else:
            actor.resources[slot_key] = max(
                0, actor.resources.get(slot_key, 0) - 1,
            )
        if actor.casting_type == "prepared" and has_any_prep:
            prep_list = actor.prepared_spells.get(base_spell_level, [])
            if spontaneous_cure:
                # Spontaneous cure: any prep entry at this level burns
                # in place of the cure spell. Take the first available.
                if prep_list:
                    prep_list.pop(0)
                    actor.prepared_spells[base_spell_level] = prep_list
            elif spell_id in prep_list:
                prep_list.remove(spell_id)
                actor.prepared_spells[base_spell_level] = prep_list

    # ── Arcane spell failure from armor ─────────────────────────────
    # Arcane casters wearing armor / shields with non-zero
    # arcane_spell_failure roll a d100 per cast; failure consumes the
    # slot. Still Spell removes the somatic component and skips this
    # check (RAW). Only S-component spells trigger ASF (V-only or
    # M-only spells aren't affected; in practice almost everything
    # arcane has S).
    asf_pct = _arcane_spell_failure_pct(actor)
    is_arcane = _is_arcane_caster(actor)
    has_s_for_asf = "S" in (spell.components or []) and (
        "still_spell" not in metamagic
    )
    if is_arcane and has_s_for_asf and asf_pct > 0:
        asf_roll = roller.roll("1d100")
        if asf_roll.total <= asf_pct:
            events.append(TurnEvent(actor.id, "cast_failed", {
                "spell_id": spell_id,
                "reason": "arcane_spell_failure",
                "asf_pct": asf_pct,
                "roll": asf_roll.total,
            }))
            _consume_slot()
            return

    # ── Spell components check ──────────────────────────────────────
    components = list(spell.components or [])
    has_v = "V" in components and "silent_spell" not in metamagic
    has_s = "S" in components and "still_spell" not in metamagic
    if has_v and "silenced" in actor.conditions:
        events.append(TurnEvent(actor.id, "cast_failed", {
            "spell_id": spell_id,
            "reason": "verbal_component_blocked",
            "detail": "silenced",
        }))
        return
    if has_v and "deafened" in actor.conditions:
        # PF1 RAW: 20% chance of spell failure on V-component spells.
        miss = roller.roll("1d100")
        if miss.total <= 20:
            events.append(TurnEvent(actor.id, "cast_failed", {
                "spell_id": spell_id,
                "reason": "verbal_component_failed_deafened",
                "roll": miss.total,
            }))
            return
    # PF1 RAW: a two-handed weapon in your main hand denies you a
    # free hand for somatic components. Pragmatic exception (matches
    # tabletop convention): wizards / sorcerers / etc. with a single
    # two-handed weapon (typical: quarterstaff in main_hand, off_hand
    # empty) are presumed to free a hand to cast and re-grip after.
    # Only block S when BOTH main_hand and off_hand are filled, leaving
    # no free hand at all.
    if has_s and "grappled" not in actor.conditions:
        main_weapon = actor.held_items.get("main_hand")
        off_weapon = actor.held_items.get("off_hand")
        if main_weapon is not None and off_weapon is not None:
            from .content import default_registry
            try:
                w = default_registry().get_weapon(main_weapon.item_id)
                if w.wield == "two_handed":
                    events.append(TurnEvent(actor.id, "cast_failed", {
                        "spell_id": spell_id,
                        "reason": "somatic_blocked_no_free_hand",
                    }))
                    return
            except Exception:
                pass
    if has_s and "grappled" in actor.conditions:
        # RAW: somatic spells while grappled require a concentration check
        # (DC 10 + grappler's CMB + spell level).
        from .spells import key_ability_for, caster_level as _cl
        cl_g = _cl(actor)
        key_g = key_ability_for(actor)
        ab_g = 0
        if key_g and actor.template is not None and hasattr(actor.template, "base_ability_scores"):
            base = actor.template.base_ability_scores.get(key_g)
            ab_g = (base - 10) // 2
            for m in actor.modifiers.for_target(f"ability:{key_g}"):
                ab_g += m.value
        grappler = _resolve_grappler(actor, grid)
        grappler_cmb = grappler.cmb() if grappler is not None else 0
        grapple_dc = 10 + grappler_cmb + spell_level
        r_g = roller.roll("1d20")
        nat_g = r_g.terms[0].rolls[0]
        total_g = nat_g + cl_g + ab_g
        if total_g < grapple_dc:
            events.append(TurnEvent(actor.id, "cast_failed", {
                "spell_id": spell_id,
                "reason": "somatic_grappled_concentration_failed",
                "concentration_check": {
                    "natural": nat_g, "modifier": cl_g + ab_g,
                    "total": total_g, "dc": grapple_dc,
                },
            }))
            _consume_slot()
            return

    # ── Concentration check if threatened (cast on the defensive). ──
    threatened_by = []
    if grid is not None:
        for cid, other in grid.combatants.items():
            if other.id == actor.id or other.team == actor.team:
                continue
            if other.is_unconscious() or "paralyzed" in other.conditions:
                continue
            if grid.threatens(other, actor):
                threatened_by.append(other)
    if threatened_by:
        defensive = bool(args.get("defensive", True))   # default to defensive
        if defensive:
            from .spells import key_ability_for, caster_level as _cl
            cl = _cl(actor)
            key = key_ability_for(actor)
            ab_mod = 0
            if key and actor.template is not None and hasattr(actor.template, "base_ability_scores"):
                base = actor.template.base_ability_scores.get(key)
                ab_mod = (base - 10) // 2
                # Add modifiers
                for m in actor.modifiers.for_target(f"ability:{key}"):
                    ab_mod += m.value
            conc_dc = 15 + 2 * spell_level
            r = roller.roll("1d20")
            nat = r.terms[0].rolls[0]
            total = nat + cl + ab_mod
            passed = total >= conc_dc
            # Slot is consumed regardless of success.
            _consume_slot()
            if not passed:
                events.append(TurnEvent(actor.id, "cast_failed", {
                    "spell_id": spell_id,
                    "reason": "concentration_failed",
                    "concentration_check": {
                        "natural": nat, "modifier": cl + ab_mod,
                        "total": total, "dc": conc_dc,
                    },
                    "threatened_by": [t.id for t in threatened_by],
                }))
                return
            events.append(TurnEvent(actor.id, "concentration", {
                "natural": nat, "modifier": cl + ab_mod,
                "total": total, "dc": conc_dc, "passed": True,
            }))
        else:
            # Casting non-defensively while threatened provokes AoOs.
            # Track total damage taken for the concentration check below.
            hp_before_aoos = actor.current_hp
            for threatener in threatened_by:
                _do_aoo(threatener, actor, grid, events, encounter=encounter)
                if actor.current_hp <= 0:
                    events.append(TurnEvent(actor.id, "cast_failed", {
                        "spell_id": spell_id,
                        "reason": "killed_by_aoo_during_cast",
                    }))
                    _consume_slot()
                    return
            damage_taken = max(0, hp_before_aoos - actor.current_hp)
            if damage_taken > 0:
                # PF1 RAW: damage during a cast → concentration check
                # DC 10 + damage + spell level. Failure → spell lost.
                from .spells import key_ability_for, caster_level as _cl
                cl_d = _cl(actor)
                key_d = key_ability_for(actor)
                ab_d = 0
                if key_d and actor.template is not None and hasattr(actor.template, "base_ability_scores"):
                    base = actor.template.base_ability_scores.get(key_d)
                    ab_d = (base - 10) // 2
                    for m in actor.modifiers.for_target(f"ability:{key_d}"):
                        ab_d += m.value
                dmg_dc = 10 + damage_taken + spell_level
                r_d = roller.roll("1d20")
                nat_d = r_d.terms[0].rolls[0]
                total_d = nat_d + cl_d + ab_d
                if total_d < dmg_dc:
                    events.append(TurnEvent(actor.id, "cast_failed", {
                        "spell_id": spell_id,
                        "reason": "concentration_failed_damage",
                        "concentration_check": {
                            "natural": nat_d, "modifier": cl_d + ab_d,
                            "total": total_d, "dc": dmg_dc,
                        },
                        "damage_taken": damage_taken,
                    }))
                    _consume_slot()
                    return
            _consume_slot()
    else:
        _consume_slot()

    # ── Resolve targets, expanding for buff_party / AoE. ──
    targets = _expand_cast_targets(actor, spell, args, encounter, grid, ns)
    if not targets:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": f"cast {spell_id}: no target resolved",
        }))
        return

    from .spells import cast_spell
    cur_round = encounter.round_number if encounter is not None else 1
    outcome = cast_spell(
        actor, spell, targets, base_spell_level, registry, roller,
        current_round=cur_round, metamagic=metamagic, grid=grid,
        encounter=encounter,
    )
    events.append(TurnEvent(actor.id, "cast", outcome.to_dict()))


def _expand_cast_targets(
    actor: Combatant,
    spell,
    args: dict,
    encounter,
    grid,
    ns: dict[str, Any],
) -> list[Combatant]:
    """Multi-target / friend-or-foe expansion based on the spell's effect."""
    kind = spell.effect.get("kind", "")
    # Party buffs: target all allies in 50 ft (10 squares) of caster.
    if kind == "buff_party":
        if encounter is None:
            return [actor]
        out: list[Combatant] = []
        for ir in encounter.initiative:
            c = ir.combatant
            if c.team != actor.team:
                continue
            if c.current_hp <= 0:
                continue
            if grid is None or grid.distance_between(actor, c) <= 10:
                out.append(c)
        return out

    # AoE shapes — burst, cone, line, spread, emanation.
    area = spell.effect.get("area") or {}
    shape = area.get("shape", "")
    if shape == "burst":
        return _expand_aoe_burst(actor, spell, args, ns, encounter, grid)
    if shape == "cone":
        return _expand_aoe_cone(actor, spell, args, ns, encounter, grid)
    if shape == "line":
        return _expand_aoe_line(actor, spell, args, ns, encounter, grid)
    if shape == "spread":
        return _expand_aoe_spread(actor, spell, args, ns, encounter, grid)
    if shape == "emanation":
        return _expand_aoe_emanation(actor, spell, args, ns, encounter, grid)

    # Single-target default: resolve from the args.target expression.
    target_expr = args.get("target")
    target = _resolve_target(target_expr, ns)
    return [target] if target is not None else []


def _expand_aoe_burst(
    actor: Combatant,
    spell,
    args: dict,
    ns: dict[str, Any],
    encounter,
    grid,
) -> list[Combatant]:
    """All combatants whose anchor is within R squares of the burst center.

    Burst center is determined by the script's ``target`` arg: a
    Combatant (use its position) or a literal square.
    """
    if encounter is None or grid is None:
        return []
    eff = spell.effect
    area = eff.get("area") or {}
    radius_squares = int(area.get("size_ft", 0)) // 5
    target_expr = args.get("target")
    target_obj = _resolve_target(target_expr, ns)
    if hasattr(target_obj, "position"):
        center = target_obj.position
    elif (isinstance(target_obj, tuple)
          and len(target_obj) == 2
          and all(isinstance(c, int) for c in target_obj)):
        center = target_obj
    else:
        return []
    out: list[Combatant] = []
    for ir in encounter.initiative:
        c = ir.combatant
        if c.current_hp <= -10:
            continue
        if grid.distance_squares(c.position, center) <= radius_squares:
            out.append(c)
    return out


def _expand_aoe_cone(
    actor: Combatant,
    spell,
    args: dict,
    ns: dict[str, Any],
    encounter,
    grid,
) -> list[Combatant]:
    """All combatants in a 90-degree cone emanating from the caster.

    Cone direction = from caster toward the script's ``target``. Cone
    length = ``area.size_ft``. Squares within ±45° of the direction
    vector and within range are inside.
    """
    if encounter is None or grid is None:
        return []
    eff = spell.effect
    area = eff.get("area") or {}
    range_squares = int(area.get("size_ft", 0)) // 5
    target_expr = args.get("target")
    target_obj = _resolve_target(target_expr, ns)
    if hasattr(target_obj, "position"):
        target_pos = target_obj.position
    elif (isinstance(target_obj, tuple)
          and len(target_obj) == 2
          and all(isinstance(c, int) for c in target_obj)):
        target_pos = target_obj
    else:
        return []
    cx, cy = actor.position
    tx, ty = target_pos
    vx, vy = tx - cx, ty - cy
    if vx == 0 and vy == 0:
        return []
    out: list[Combatant] = []
    for ir in encounter.initiative:
        c = ir.combatant
        if c.id == actor.id:
            continue  # caster's own square is the cone origin
        if c.current_hp <= -10:
            continue
        sx, sy = c.position
        dx, dy = sx - cx, sy - cy
        if dx == 0 and dy == 0:
            continue
        if grid.distance_squares(actor.position, c.position) > range_squares:
            continue
        # In-cone test: angle between (dx,dy) and (vx,vy) must be ≤ 45°.
        # Equivalently: dot > 0 AND 2 * dot² ≥ |d|² · |v|².
        dot = dx * vx + dy * vy
        if dot <= 0:
            continue
        if 2 * dot * dot < (dx * dx + dy * dy) * (vx * vx + vy * vy):
            continue
        out.append(c)
    return out


def _expand_aoe_line(
    actor: Combatant,
    spell,
    args: dict,
    ns: dict[str, Any],
    encounter,
    grid,
) -> list[Combatant]:
    """All combatants on a straight line from the caster to a target
    point, up to ``area.size_ft`` distance.

    Direction = unit vector from caster toward args.target. The line is
    a single-cell-wide path along the Bresenham line. Walls block the
    line at their cell (lightning bolt stops at the first wall).
    """
    if encounter is None or grid is None:
        return []
    eff = spell.effect
    area = eff.get("area") or {}
    length_squares = int(area.get("size_ft", 0)) // 5
    target_expr = args.get("target")
    target_obj = _resolve_target(target_expr, ns)
    if hasattr(target_obj, "position"):
        target_pos = target_obj.position
    elif (isinstance(target_obj, tuple)
          and len(target_obj) == 2
          and all(isinstance(c, int) for c in target_obj)):
        target_pos = target_obj
    else:
        return []
    cx, cy = actor.position
    tx, ty = target_pos
    if (tx, ty) == (cx, cy):
        return []
    # Step direction: unit vector along the strongest axis.
    ux = (tx > cx) - (tx < cx)
    uy = (ty > cy) - (ty < cy)
    # Walk cells along the line up to length_squares; stop at first wall.
    line_cells: set[tuple[int, int]] = set()
    cur = (cx, cy)
    for _ in range(length_squares):
        nxt = (cur[0] + ux, cur[1] + uy)
        if not grid.in_bounds(*nxt):
            break
        f = grid.features.get(nxt)
        if f is not None and f.blocks_line_of_sight:
            break
        line_cells.add(nxt)
        cur = nxt
    out: list[Combatant] = []
    for ir in encounter.initiative:
        c = ir.combatant
        if c.id == actor.id:
            continue
        if c.current_hp <= -10:
            continue
        if c.position in line_cells:
            out.append(c)
    return out


def _expand_aoe_spread(
    actor: Combatant,
    spell,
    args: dict,
    ns: dict[str, Any],
    encounter,
    grid,
) -> list[Combatant]:
    """Burst that follows corners — BFS from the spread origin to all
    cells within ``area.size_ft``, treating walls as impassable.

    Used for fireball / cloudkill / similar PF1 "spread" spells. The
    distinction vs ``burst`` is path-based: a spread fills around
    obstacles instead of going through them.
    """
    if encounter is None or grid is None:
        return []
    eff = spell.effect
    area = eff.get("area") or {}
    radius_squares = int(area.get("size_ft", 0)) // 5
    target_expr = args.get("target")
    target_obj = _resolve_target(target_expr, ns)
    if hasattr(target_obj, "position"):
        center = target_obj.position
    elif (isinstance(target_obj, tuple)
          and len(target_obj) == 2
          and all(isinstance(c, int) for c in target_obj)):
        center = target_obj
    else:
        return []
    # BFS by actual path distance through unblocked cells. Each step
    # costs 1 (orthogonal) or 1 (first diagonal) — we don't track the
    # PF1 5-10-5 alternating diagonal cost in spread expansion since
    # the spread radius is in feet/5 and the wave fills cell-by-cell.
    # Walls block expansion entirely.
    visited: dict[tuple[int, int], int] = {center: 0}
    frontier: list[tuple[int, int]] = [center]
    while frontier:
        next_frontier: list[tuple[int, int]] = []
        for cell in frontier:
            cur_d = visited[cell]
            if cur_d >= radius_squares:
                continue
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nb = (cell[0] + dx, cell[1] + dy)
                    if nb in visited:
                        continue
                    if not grid.in_bounds(*nb):
                        continue
                    f = grid.features.get(nb)
                    if f is not None and f.blocks_line_of_sight:
                        continue
                    visited[nb] = cur_d + 1
                    next_frontier.append(nb)
        frontier = next_frontier
    out: list[Combatant] = []
    for ir in encounter.initiative:
        c = ir.combatant
        if c.current_hp <= -10:
            continue
        if c.position in visited:
            out.append(c)
    return out


def _expand_aoe_emanation(
    actor: Combatant,
    spell,
    args: dict,
    ns: dict[str, Any],
    encounter,
    grid,
) -> list[Combatant]:
    """Lasting aura from the caster outward to ``area.size_ft``.

    For instantaneous-cast purposes we expand to all combatants within
    range right now (the emanation continues to follow the caster
    across rounds via the modifier expiration system; this expansion
    is the on-cast snapshot of who's affected).

    PF1 RAW: the caster is the center; an emanation moves with them.
    Walls don't block (line of effect required for spell targeting,
    but the emanation itself fills space around the caster — for v1
    we just pick combatants by distance).
    """
    if encounter is None or grid is None:
        return [actor]
    eff = spell.effect
    area = eff.get("area") or {}
    radius_squares = int(area.get("size_ft", 0)) // 5
    out: list[Combatant] = []
    for ir in encounter.initiative:
        c = ir.combatant
        if c.current_hp <= -10:
            continue
        if grid.distance_squares(actor.position, c.position) <= radius_squares:
            out.append(c)
    return out


_SNEAK_ATTACK_DENY_DEX_CONDITIONS = frozenset({
    "flat_footed", "prone", "paralyzed", "helpless",
    "stunned", "sleeping", "pinned", "cowering", "blinded",
})


def _is_flanking(
    actor: Combatant,
    target: Combatant,
    grid: Grid | None,
    encounter,
) -> bool:
    """True if any conscious ally + the actor flank the target."""
    if grid is None or encounter is None:
        return False
    if not grid.is_adjacent(actor, target):
        return False
    for ir in encounter.initiative:
        ally = ir.combatant
        if ally.id == actor.id or ally.team != actor.team:
            continue
        if ally.current_hp <= 0 or ally.is_unconscious():
            continue
        if grid.is_flanked_by(target, actor, ally):
            return True
    return False


def _cover_ac_bonus(
    attacker: Combatant,
    target: Combatant,
    grid: Grid | None,
    is_ranged: bool,
) -> int:
    """Return the cover bonus to ``target``'s AC vs ``attacker``.

    PF1 cover tiers (simplified for the grid-and-Bresenham model):
      - No walls in line: no hard cover. Soft cover (+4) applies if a
        non-attacker non-target combatant stands on the line AND the
        attack is ranged.
      - Exactly one wall on the line: hard cover (+4 AC, +2 Reflex —
        the Reflex piece is read by callers via ``_cover_reflex_bonus``).
      - Two or more walls on the line: greater cover (+8 AC, +4
        Reflex). Models "the cover is more than half" from RAW.
      - Total cover (line of effect fully blocked) is rejected at the
        attack-validity stage by ``_total_cover_blocks_line``, not
        here — this function only returns AC bonuses for attacks
        that are still resolvable.

    Hard / greater cover trumps soft cover; we don't stack them.
    """
    if grid is None:
        return 0
    from .grid import _bresenham
    line = _bresenham(attacker.position, target.position)
    wall_count = 0
    has_soft = False
    for cell in line:
        if cell == attacker.position or cell == target.position:
            continue
        # Hard cover from a wall on the line.
        f = grid.features.get(cell)
        if f is not None and f.blocks_line_of_sight:
            wall_count += 1
            continue
        # Soft cover from any other combatant standing in the way.
        for cid, occupant in grid.combatants.items():
            if occupant.id in (attacker.id, target.id):
                continue
            if occupant.position == cell:
                has_soft = True
                break
    if wall_count >= 2:
        return 8  # greater cover
    if wall_count == 1:
        return 4  # hard cover
    if has_soft and is_ranged:
        return 4  # soft cover (ranged only)
    return 0


def _cover_reflex_bonus(
    attacker: Combatant,
    target: Combatant,
    grid: Grid | None,
) -> int:
    """Return the Reflex-save bonus from cover.

    PF1 RAW: hard cover grants +2 Reflex (against effects originating
    on the far side of the cover); greater cover grants +4. Soft
    cover (intervening combatants) does NOT grant Reflex bonuses
    per RAW. We mirror the wall-count logic in _cover_ac_bonus.
    """
    if grid is None:
        return 0
    from .grid import _bresenham
    line = _bresenham(attacker.position, target.position)
    walls = 0
    for cell in line:
        if cell == attacker.position or cell == target.position:
            continue
        f = grid.features.get(cell)
        if f is not None and f.blocks_line_of_sight:
            walls += 1
    if walls >= 2:
        return 4
    if walls == 1:
        return 2
    return 0


def _total_cover_blocks_line(
    attacker: Combatant,
    target: Combatant,
    grid: Grid | None,
) -> bool:
    """True when the line of effect from attacker to target is fully
    blocked — ranged attacks and most spells fail entirely (PF1 'total
    cover'). We treat 3+ walls in the line as total cover.
    """
    if grid is None:
        return False
    from .grid import _bresenham
    line = _bresenham(attacker.position, target.position)
    walls = 0
    for cell in line:
        if cell == attacker.position or cell == target.position:
            continue
        f = grid.features.get(cell)
        if f is not None and f.blocks_line_of_sight:
            walls += 1
    return walls >= 3


def _firing_into_melee_penalty(
    actor: Combatant,
    target: Combatant,
    grid: Grid | None,
    encounter,
    is_ranged: bool,
) -> int:
    """PF1 RAW: ranged attacks against a target engaged in melee suffer
    a -4 penalty unless the attacker has the Precise Shot feat.

    "Engaged in melee" is approximated as "another combatant is
    adjacent to the target" — sufficient for 5-ft reach. Reach
    weapons (10-ft) are deferred.
    """
    if not is_ranged or grid is None or encounter is None:
        return 0
    if _has_feat(actor, "precise_shot"):
        return 0
    for ir in encounter.initiative:
        c = ir.combatant
        if c.id == actor.id or c.id == target.id:
            continue
        if c.current_hp <= 0 or c.is_unconscious():
            continue
        if grid.is_adjacent(c, target):
            return -4
    return 0


_DEX_DENIED_CONDITIONS = frozenset({
    "flat_footed", "helpless", "paralyzed", "stunned", "pinned",
    "cowering", "blinded", "prone", "sleeping", "petrified",
})


# Reflex DC for catching a thrown rock, indexed by the thrower's
# size. PF1 RAW: small rock DC 15, medium 20, large 25, huge 30,
# gargantuan 35, colossal 40. Rocks scale with the thrower's size.
_ROCK_CATCH_DC: dict[str, int] = {
    "small": 15,
    "medium": 20,
    "large": 25,
    "huge": 30,
    "gargantuan": 35,
    "colossal": 40,
}


def _weapon_attack_tags(actor: Combatant, chosen: dict) -> frozenset[str]:
    """Compute PF1 attack tags for a weapon attack.

    Tags drive DR bypass and incorporeal/special-defense interactions.
    Sources, in order:
      1. ``chosen.get("attack_tags")`` — explicit tag list on the
         attack option (used by natural attacks that are inherently
         magical, e.g., outsider claws).
      2. Held-item ``properties``: ``enhancement_bonus`` > 0 implies
         "magic"; ``special_abilities`` (e.g. ghost_touch, holy,
         flaming) each become tags AND imply "magic"; ``material``
         (silver / cold_iron / adamantine) becomes a tag.
    """
    tags: set[str] = set(t.lower() for t in (chosen.get("attack_tags") or []))
    weapon = actor.held_items.get("main_hand")
    if weapon is not None:
        props = getattr(weapon, "properties", None) or {}
        if int(props.get("enhancement_bonus", 0) or 0) > 0:
            tags.add("magic")
        for sa in props.get("special_abilities") or []:
            sa_str = str(sa).lower()
            tags.add(sa_str)
            tags.add("magic")  # any special ability is by definition a magical weapon
        material = props.get("material")
        if material:
            tags.add(str(material).lower())
    return frozenset(tags)


def _has_dex_denied(target: Combatant) -> bool:
    """Whether the target is denied its Dex bonus to AC."""
    return bool(target.conditions & _DEX_DENIED_CONDITIONS)


_ARCANE_CASTER_CLASSES: frozenset[str] = frozenset({
    "wizard", "sorcerer", "bard", "magus", "summoner", "witch",
    "bloodrager", "skald",
})


def _is_cleric_class(actor: Combatant) -> bool:
    """True if the actor has any cleric levels (spontaneous cure-swap
    eligible). Walks the level plan for multiclass clerics."""
    if actor.template_kind != "character" or actor.template is None:
        return False
    char = actor.template
    if getattr(char, "class_id", None) == "cleric":
        return True
    plan = getattr(char, "level_plan", None)
    if plan and isinstance(plan, dict):
        for entry in (plan.get("levels") or {}).values():
            if isinstance(entry, dict) and entry.get("class") == "cleric":
                return True
    return False


def _is_arcane_caster(actor: Combatant) -> bool:
    """True if the actor has any levels in an arcane casting class."""
    if actor.template_kind != "character" or actor.template is None:
        return False
    char = actor.template
    if getattr(char, "class_id", None) in _ARCANE_CASTER_CLASSES:
        return True
    plan = getattr(char, "level_plan", None) or {}
    levels = plan.get("levels") if isinstance(plan, dict) else None
    if levels:
        for entry in levels.values():
            if isinstance(entry, dict) and entry.get("class") in _ARCANE_CASTER_CLASSES:
                return True
    return False


def _arcane_spell_failure_pct(actor: Combatant) -> int:
    """Sum the arcane spell failure % from equipped armor + shield."""
    if actor.template_kind != "character" or actor.template is None:
        return 0
    from .content import default_registry
    registry = default_registry()
    pct = 0
    armor_id = getattr(actor.template, "equipped_armor", None)
    if armor_id and armor_id != "none":
        try:
            pct += int(registry.get_armor(armor_id).arcane_spell_failure)
        except Exception:
            pass
    shield_id = getattr(actor.template, "equipped_shield", None)
    if shield_id:
        try:
            pct += int(registry.get_shield(shield_id).arcane_spell_failure)
        except Exception:
            pass
    return pct


def _armor_not_proficient_penalty(actor: Combatant) -> int:
    """Return the attack-roll penalty from wearing armor / shield the
    actor isn't proficient with.

    PF1 RAW: a non-proficient wearer takes the armor-check penalty
    (ACP) on attack rolls and on Strength/Dex-based skill checks.
    Skill ACP is already applied via combatant_from_character; this
    helper layers the same penalty onto attack rolls.
    """
    if actor.template_kind != "character" or actor.template is None:
        return 0
    profs = actor.armor_proficiency_categories
    if not profs:
        return 0  # not modeled — no penalty
    from .content import default_registry
    registry = default_registry()
    penalty = 0
    armor_id = getattr(actor.template, "equipped_armor", None)
    if armor_id and armor_id != "none":
        try:
            armor = registry.get_armor(armor_id)
        except Exception:
            armor = None
        if armor is not None and armor.category not in ("none",) and \
                armor.category not in profs:
            penalty += int(armor.armor_check_penalty)  # negative or zero
    shield_id = getattr(actor.template, "equipped_shield", None)
    if shield_id:
        try:
            shield = registry.get_shield(shield_id)
        except Exception:
            shield = None
        if shield is not None:
            shield_token = (
                "shield_tower" if shield.is_tower else "shields_normal"
            )
            if shield_token not in profs:
                penalty += int(shield.armor_check_penalty)
    return penalty


def _weapon_not_proficient(actor: Combatant, chosen: dict) -> bool:
    """True if the actor lacks proficiency with the weapon being used.

    Uses the cached ``Combatant.weapon_proficiency_categories`` set
    (populated at construction). When the cache is empty we assume
    the actor is proficient (e.g., monsters with natural attacks
    don't need a category lookup; their attack_options come from a
    template with built-in proficiency).

    Proficiency matches either the weapon's category ("simple",
    "martial", "exotic") or its specific weapon ID — class data may
    grant a narrow list of weapons (e.g. wizard with quarterstaff)
    that don't translate to whole-category proficiency.
    """
    weapon_cat = chosen.get("weapon_category")
    if not weapon_cat:
        return False  # natural / template-supplied attack — always proficient
    profs = getattr(actor, "weapon_proficiency_categories", None) or set()
    if not profs:
        return False  # no cached proficiencies — assume proficient
    if weapon_cat in profs:
        return False
    weapon_id = chosen.get("weapon_id")
    if weapon_id and weapon_id in profs:
        return False
    return True


def _target_creature_context(target: Combatant) -> dict:
    """Build the qualifier-matching context dict for ``target``.

    Used by situational racial traits (dwarven hatred vs orcs etc.).
    Reads ``target_type`` and ``target_subtypes`` from the underlying
    monster template; characters get a ``humanoid`` type with their
    race id as a subtype (so dwarven hatred recognizes a "goblinoid"
    PC etc., should one ever exist). Also includes ``target_id`` so
    qualifier predicates can match a specific combatant — used by the
    aid-another "vs that foe" restriction.
    """
    if target.template is None:
        return {"target_id": target.id, "target_type": "",
                "target_subtypes": []}
    if target.template_kind == "monster":
        ttype = (getattr(target.template, "type", "") or "").lower()
        subs = [s.lower() for s in
                (getattr(target.template, "subtypes", None) or [])]
        return {"target_id": target.id, "target_type": ttype,
                "target_subtypes": subs}
    if target.template_kind == "character":
        race_id = (getattr(target.template, "race_id", "") or "").lower()
        return {"target_id": target.id, "target_type": "humanoid",
                "target_subtypes": [race_id]}
    return {"target_id": target.id, "target_type": "",
            "target_subtypes": []}


def _range_increment_penalty(
    chosen: dict,
    actor: Combatant,
    target: Combatant,
    grid: Grid | None,
    is_ranged: bool,
) -> int:
    """PF1 RAW: ranged attacks take -2 per range increment beyond the
    first.

    ``range_increment`` on the attack option is in feet; we convert to
    feet via ``5 * grid.distance_between(actor, target)``. A weapon
    with no ``range_increment`` (purely melee) gets no penalty.
    """
    if not is_ranged or grid is None:
        return 0
    rinc_ft = int(chosen.get("range_increment") or 0)
    if rinc_ft <= 0:
        return 0
    distance_ft = grid.distance_between(actor, target) * 5
    if distance_ft <= 0:
        return 0
    # Number of increments used: ceil(distance / rinc).
    increments = (distance_ft + rinc_ft - 1) // rinc_ft
    return -2 * max(0, increments - 1)


def _out_of_max_range(
    chosen: dict,
    actor: Combatant,
    target: Combatant,
    grid: Grid | None,
    is_ranged: bool,
) -> bool:
    """True when the target is beyond the weapon's maximum range.

    PF1 RAW: thrown weapons cap at 5 range increments; projectile
    weapons (bows, crossbows, slings) at 10 increments. We
    distinguish via ``can_throw`` on the underlying Weapon (default to
    10 for projectiles, 5 for thrown).
    """
    if not is_ranged or grid is None:
        return False
    rinc_ft = int(chosen.get("range_increment") or 0)
    if rinc_ft <= 0:
        return False
    distance_ft = grid.distance_between(actor, target) * 5
    weapon_id = chosen.get("weapon_id")
    max_increments = 10  # default to projectile cap
    if weapon_id:
        from .content import default_registry
        try:
            w = default_registry().get_weapon(weapon_id)
            if w.can_throw:
                max_increments = 5
        except Exception:
            pass
    return distance_ft > rinc_ft * max_increments


def _flanking_attack_bonus(
    actor: Combatant,
    target: Combatant,
    grid: Grid | None,
    encounter,
    *,
    is_ranged: bool,
) -> int:
    """+2 to attack when flanking a target in melee (PF1 RAW)."""
    if is_ranged:
        return 0
    return 2 if _is_flanking(actor, target, grid, encounter) else 0


def _sneak_attack_dice(
    actor: Combatant,
    target: Combatant,
    grid: Grid | None,
    encounter,
) -> str:
    """Return precision damage dice (e.g. ``"2d6"``) if attacker qualifies.

    PF1 sneak attack triggers when the target is denied its Dex bonus to
    AC OR the attacker is flanking. Multiclass rogues use only their
    rogue level for sneak attack progression.
    """
    if actor.template_kind != "character":
        return ""
    char = actor.template
    if char is None:
        return ""

    # Cumulative rogue levels (from level plan).
    rogue_levels = 1 if getattr(char, "class_id", None) == "rogue" else 0
    plan = getattr(char, "level_plan", None)
    if plan and isinstance(plan, dict):
        for entry in (plan.get("levels") or {}).values():
            if isinstance(entry, dict) and entry.get("class") == "rogue":
                rogue_levels += 1
    if rogue_levels < 1:
        return ""

    # Qualifies via flat-footed / denied Dex, or via flanking.
    denies_dex = bool(target.conditions & _SNEAK_ATTACK_DENY_DEX_CONDITIONS)
    if not denies_dex and not _is_flanking(actor, target, grid, encounter):
        return ""

    # Sneak attack scales: +1d6 at L1, +1d6 every 2 levels (L1=1, L3=2, ...).
    sa_dice = (rogue_levels + 1) // 2
    return f"{sa_dice}d6"


def _has_racial_trait(target: Combatant, trait_id: str) -> bool:
    """True if the monster template carries the named racial trait."""
    if target.template_kind != "monster" or target.template is None:
        return False
    traits = getattr(target.template, "racial_traits", None) or []
    return any(
        isinstance(t, dict) and t.get("id") == trait_id for t in traits
    )


def _check_massive_damage(
    target: Combatant, damage: int, roller: Roller,
) -> tuple[bool, dict] | None:
    """PF1 massive damage rule: 50+ damage from a single source forces
    a Fortitude save (DC 15). Failure = death; the dying-threshold
    rules are bypassed.

    Returns ``None`` if the threshold isn't met. Otherwise returns
    ``(saved, detail)`` where ``saved`` is True/False and ``detail``
    is a trace dict.
    """
    if damage < 50:
        return None
    if "dead" in target.conditions:
        return None  # already dead — skip
    save_total = target.save("fort")
    r = roller.roll("1d20")
    nat = r.terms[0].rolls[0]
    save_passed = (nat == 20) or (nat != 1 and nat + save_total >= 15)
    detail = {
        "damage": damage, "save_dc": 15,
        "save_natural": nat, "save_total": nat + save_total,
        "save_passed": save_passed,
    }
    if not save_passed:
        target.add_condition("dead")
    return save_passed, detail


def _apply_post_damage_state(target: Combatant) -> None:
    """Centralized HP-threshold transitions after damage.

    All damage sites must call this *after* ``target.take_damage(...)``.
    It handles four transitions, by HP threshold:

    * HP <= ``target.death_threshold`` → dead. PF1 RAW: -CON for living
      creatures; 0 for undead/constructs.
    * HP <= 0 (but above death threshold) with ferocity → stay
      conscious + ``ferocity_active`` + ``staggered``. Tick_round
      bleeds 1 HP/round until killed outright.
    * HP < 0 (negative but above death threshold) without ferocity →
      ``dying``. Tick_round bleeds 1 HP/round.
    * HP exactly 0 → ``disabled`` (PF1 distinction): conscious, can
      take 1 standard or 1 move (not both); standard actions deal 1
      HP back to self (not yet modeled — PARTIAL).
    """
    threshold = target.death_threshold
    if target.current_hp <= threshold:
        target.add_condition("dead")
        target.remove_condition("dying")
        target.remove_condition("disabled")
        target.remove_condition("ferocity_active")
        target.remove_condition("staggered")
        return
    if target.current_hp == 0:
        target.add_condition("disabled")
        target.remove_condition("dying")
        return
    if target.current_hp < 0:
        if _has_racial_trait(target, "ferocity"):
            # Stay conscious and keep fighting; suppress dying.
            target.add_condition("ferocity_active")
            target.add_condition("staggered")
            target.remove_condition("dying")
            target.remove_condition("disabled")
        else:
            target.add_condition("dying")
            target.remove_condition("disabled")


def _aoo_limit(actor: Combatant) -> int:
    """Maximum AoOs per round. PF1: 1 by default; Combat Reflexes adds
    the combatant's Dex modifier (minimum total 1)."""
    if not _has_feat(actor, "combat_reflexes"):
        return 1
    dex_mod = _ability_modifier(actor, "dex")
    return max(1, 1 + dex_mod)


def _can_take_aoo(threatener: Combatant, current_round: int) -> bool:
    """Throttle AoOs per the threatener's per-round limit."""
    if threatener.aoos_used_round_marker != current_round:
        threatener.aoos_used_round_marker = current_round
        threatener.aoos_used_this_round = 0
    return threatener.aoos_used_this_round < _aoo_limit(threatener)


def _do_aoo(
    threatener: Combatant,
    target: Combatant,
    grid: Grid,
    events: list[TurnEvent],
    encounter=None,
) -> None:
    """Resolve a triggered AoO opportunity. DSL v2 Phase 3.1: this
    becomes a reactive-interrupt decision point — the threatener's
    registered Picker (if any) chooses a weapon or declines. With no
    picker registered, the default is "take with weapon 0", matching
    v1 behavior so untouched scripts/tests don't change."""
    # Throttle AoOs by the per-round limit (1 + Dex if Combat Reflexes).
    if encounter is not None:
        if not _can_take_aoo(threatener, encounter.round_number):
            return
    if not threatener.attack_options:
        return

    # Build the picker's legal-actions list: one TakeAoO per available
    # weapon plus a PassAoO entry. The picker sees only the actions —
    # not the kind of decision-point — per the kind-blind contract
    # (DECISION_POINT_DSL.md §4.1).
    from .actions import TakeAoO as _TakeAoO, PassAoO as _PassAoO
    legal_actions: list = [
        _TakeAoO(
            actor_id=threatener.id, provoker_id=target.id,
            weapon_index=i,
        )
        for i in range(len(threatener.attack_options))
    ] + [
        _PassAoO(actor_id=threatener.id, provoker_id=target.id),
    ]

    picker = None
    if encounter is not None and encounter.pickers:
        picker = encounter.pickers.get(threatener.id)

    if picker is None:
        # Default behavior: TakeAoO with weapon 0. Preserves v1.
        chosen = legal_actions[0]
    else:
        from .actions import GameState as _GameState
        state = _GameState(encounter=encounter, grid=grid)
        chosen = picker.pick(threatener, state, legal_actions)

    # PassAoO: no budget consumed, emit a trace event, done.
    if isinstance(chosen, _PassAoO):
        events.append(TurnEvent(threatener.id, "aoo_pass", {
            "provoker_id": target.id,
        }))
        return

    # TakeAoO: consume the per-round budget and resolve the attack.
    if encounter is not None:
        threatener.aoos_used_this_round += 1
    weapon_index = (
        chosen.weapon_index if isinstance(chosen, _TakeAoO) else 0
    )
    if weapon_index < 0 or weapon_index >= len(threatener.attack_options):
        weapon_index = 0
    chosen_weapon = threatener.attack_options[weapon_index]
    profile = AttackProfile(
        attack_bonus=int(chosen_weapon["attack_bonus"]),
        damage_dice=str(chosen_weapon["damage"]),
        damage_bonus=int(chosen_weapon.get("damage_bonus", 0)),
        crit_range=tuple(chosen_weapon.get("crit_range") or [20, 20]),  # type: ignore[arg-type]
        crit_multiplier=int(chosen_weapon.get("crit_multiplier", 2)),
        damage_type=str(chosen_weapon.get("damage_type", "")),
        name=str(chosen_weapon.get("name", "weapon")),
    )
    # AoO uses the encounter's RNG sequence so seeded simulations stay
    # deterministic.
    if encounter is not None and encounter.roller is not None:
        aoo_roller = encounter.roller
    else:
        from .dice import Roller as _R
        aoo_roller = _R(seed=0)
    outcome = resolve_attack(profile, target.defense_profile(), aoo_roller)
    if outcome.hit and outcome.damage > 0:
        target.take_damage(outcome.damage)
        _apply_post_damage_state(target)
    events.append(TurnEvent(threatener.id, "aoo", {
        "target_id": target.id,
        "hit": outcome.hit,
        "crit": outcome.crit,
        "damage": outcome.damage,
        "weapon_index": weapon_index,
        "trace": outcome.log,
    }))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _resolve_target(target: Any, ns: dict[str, Any]) -> Any:
    """Resolve a target spec to a Python object (Combatant, square, etc.)."""
    if target is None:
        return None
    if isinstance(target, str):
        # Treat as expression to evaluate against the namespace.
        try:
            return evaluate(target, ns)
        except Exception:
            return None
    return target


def _coerce_square(target: Any) -> tuple[int, int] | None:
    if target is None:
        return None
    if isinstance(target, tuple) and len(target) == 2:
        return (int(target[0]), int(target[1]))
    if hasattr(target, "position"):
        return target.position
    if isinstance(target, list) and len(target) == 2:
        return (int(target[0]), int(target[1]))
    return None


# ---------------------------------------------------------------------------
# Default monster AI (no script)
# ---------------------------------------------------------------------------


def default_monster_intent(
    actor: Combatant,
    encounter: Encounter,
    grid: Grid,
) -> TurnIntent:
    """Hardcoded aggressive-melee AI for monsters that don't have scripts.

    Logic: if a hostile is in melee range, full_attack closest. Otherwise
    if enemies exist, charge the closest. Otherwise hold.
    """
    from .dsl import build_namespace
    ns = build_namespace(actor, encounter, grid)
    enemies = [
        ir.combatant for ir in encounter.initiative
        if ir.combatant.team != actor.team
        and ir.combatant.current_hp > 0
        and not ir.combatant.is_unconscious()
    ]
    if not enemies:
        return TurnIntent(rule_index=-1,
                          do={"composite": "hold"},
                          namespace=ns)
    closest = min(enemies, key=lambda e: grid.distance_between(actor, e))
    if grid.is_adjacent(actor, closest):
        return TurnIntent(
            rule_index=-1,
            do={"composite": "full_attack",
                "args": {"target": "enemy.closest"}},
            namespace=ns,
        )
    # Charge if within charge range (2x speed) AND a straight-line
    # PF1-legal charge path exists. If the geometry isn't right
    # (target off-axis, lane blocked) the AI falls back to
    # move_toward so the monster doesn't waste its turn declaring an
    # illegal charge.
    charge_range = (actor.speed // 5) * 2
    if grid.distance_between(actor, closest) <= charge_range:
        line = _straight_line_charge_path(
            actor.position, closest.position, charge_range, grid,
        )
        if line is not None and _charge_path_clear(
            line[1:], grid, mover=actor,
        ):
            return TurnIntent(
                rule_index=-1,
                do={"composite": "charge",
                    "args": {"target": "enemy.closest"}},
                namespace=ns,
            )
    # Otherwise approach.
    return TurnIntent(
        rule_index=-1,
        do={"slots": {
            "move": {"type": "move_toward", "target": "enemy.closest"},
        }},
        namespace=ns,
    )
