"""Decision-point substrate for the v2 DSL.

See ``dnd/DECISION_POINT_DSL.md`` for the full design. This module is
the Phase 1 deliverable: the ``Action`` hierarchy plus
``enumerate_legal_actions`` / ``apply_action``. The existing
``execute_turn`` path is untouched; we'll wire it onto this substrate
in Phase 2.

Phase 1 scope (this commit):

- Action subclasses: ``Move``, ``FiveFootStep``, ``Attack``,
  ``FullAttack``, ``Charge``, ``Withdraw``, ``TotalDefense``,
  ``EndTurn``.
- ``GameState`` wrapper carrying per-actor turn-slot accounting.
- ``enumerate_legal_actions`` and ``apply_action`` for the actions
  above. Implementation delegates to the existing ``_do_*`` helpers
  in ``turn_executor`` to avoid duplicating logic.

Out of scope (later in Phase 1 or in Phase 2+): Cast, combat
maneuvers, reactive interrupts, sub-action decision points, the
parity harness wiring into ``execute_turn``.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from .combatant import Combatant
from .dice import Roller
from .encounter import Encounter
from .grid import Grid


# ---------------------------------------------------------------------------
# Action hierarchy
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Action:
    """Base for all atomic actions surfaced at decision points.

    Each concrete subclass carries the parameters required to resolve
    it. Pickers receive a ``list[Action]`` from
    ``enumerate_legal_actions`` and select one; the engine never
    chooses for them.
    """

    actor_id: str


@dataclass(frozen=True)
class EndTurn(Action):
    """Voluntary end of turn. Always present in the legal list unless
    the actor is forced (e.g., confused-attacks-self has run its
    substituted action)."""


@dataclass(frozen=True)
class Move(Action):
    """Walk to ``destination`` along the engine's pathfinder, up to
    the actor's per-action movement allowance. Provokes AoOs from any
    threatener whose square is left along the way."""

    destination: tuple[int, int]


@dataclass(frozen=True)
class FiveFootStep(Action):
    """Take a 5-ft step to ``destination`` (must be exactly one square
    away from the actor's current position). Does not provoke. Mutually
    exclusive with movement on the same turn."""

    destination: tuple[int, int]


@dataclass(frozen=True)
class Attack(Action):
    """Single melee or ranged attack against ``target_id`` using
    ``weapon_index`` (into ``actor.attack_options``)."""

    target_id: str
    weapon_index: int = 0


@dataclass(frozen=True)
class FullAttack(Action):
    """Full-attack action: all iteratives against ``target_id``.
    Sub-action decision points between iteratives (retarget / stop)
    arrive in Phase 3; Phase 1 resolves the entire chain inline like
    the v1 executor does.

    ``options`` carries v1-style flags the executor reads — e.g.,
    ``rapid_shot``, ``two_weapon_fighting``, ``power_attack``."""

    target_id: str
    options: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Charge(Action):
    """Full-round charge to ``target_id`` along a straight line,
    ending with a single melee attack at +2 / -2 AC.

    ``options`` carries v1-style flags the executor reads — e.g.,
    ``ride_by``, ``max_squares_override``, ``power_attack``,
    ``charge_damage_multiplier``."""

    target_id: str
    options: dict = field(default_factory=dict)


@dataclass(frozen=True)
class PartialCharge(Action):
    """PF1 partial charge: a charge limited to 1x speed (vs. regular
    charge's 2x). Used when only a standard action is available
    (disabled / staggered actor) — but the v1 engine treats it as a
    full-round composite for slot accounting, which we mirror."""

    target_id: str
    options: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Withdraw(Action):
    """Full-round retreat in the cardinal/intercardinal direction,
    up to 2x speed; first square of movement does not provoke."""

    direction: str  # "north" / "south" / "east" / "west" / etc.


@dataclass(frozen=True)
class TotalDefense(Action):
    """Standard action: +4 dodge AC for one round; cannot attack."""


# ── Combat maneuvers ──────────────────────────────────────────────────


_MANEUVER_KINDS: frozenset[str] = frozenset({
    "trip", "disarm", "sunder", "bull_rush", "grapple",
    "drag", "overrun", "reposition", "steal", "dirty_trick",
})


@dataclass(frozen=True)
class Maneuver(Action):
    """One of the 10 PF1 combat maneuvers. ``kind`` is the discriminator;
    valid values in ``_MANEUVER_KINDS``. Standard action (consumes the
    standard slot). Provokes AoO from the target unless the actor has
    the matching ``improved_<kind>`` feat."""

    kind: str
    target_id: str
    options: dict = field(default_factory=dict)


@dataclass(frozen=True)
class GrappleDamage(Action):
    """Standard action while grappling: deal weapon damage to the
    grappled foe via CMB vs CMD."""


@dataclass(frozen=True)
class GrappleMove(Action):
    """Standard action while grappling: move both grappler and grappled
    up to half speed in a cardinal/intercardinal direction; CMB vs CMD."""

    direction: str


@dataclass(frozen=True)
class GrapplePin(Action):
    """Standard action while grappling: pin the foe (regular CMB vs
    CMD); pinned + helpless on success."""


@dataclass(frozen=True)
class GrappleBreakFree(Action):
    """Standard action while grappled: escape via CMB or Escape Artist
    vs the grappler's CMB."""

    use_skill: bool = False


# ── Reactive interrupts ───────────────────────────────────────────────


@dataclass(frozen=True)
class TakeAoO(Action):
    """Reactive interrupt: take an attack of opportunity against
    ``provoker_id`` with the threatener's ``weapon_index``."""

    provoker_id: str
    weapon_index: int = 0


@dataclass(frozen=True)
class PassAoO(Action):
    """Reactive interrupt: decline an AoO opportunity (e.g., to save
    it for a higher-value target later in the round, or because the
    threatener is flat-footed)."""

    provoker_id: str


@dataclass(frozen=True)
class Brace(Action):
    """Reactive interrupt: spring a readied brace against an
    incoming charger. Bracer's first hit deals doubled damage; the
    bracing condition is consumed."""

    charger_id: str


@dataclass(frozen=True)
class PassBrace(Action):
    """Reactive interrupt: decline to spring the brace, letting the
    charge resolve normally. The bracing condition stays set so the
    bracer might still spring it on a later charger this round."""

    charger_id: str


@dataclass(frozen=True)
class CleaveTo(Action):
    """Sub-action decision: continue a cleave to ``target_id`` after a
    successful primary hit. The target must be adjacent to the
    cleaver and different from the primary."""

    primary_target_id: str
    target_id: str


@dataclass(frozen=True)
class PassCleave(Action):
    """Sub-action decision: skip the cleave continuation even though
    a secondary foe is in reach (e.g., to save the swing for later
    in the round, or because all other foes are flagged 'don't
    target')."""

    primary_target_id: str


# ── Move-action grab bag ──────────────────────────────────────────────


@dataclass(frozen=True)
class DrawWeapon(Action):
    """Move action: draw a weapon. Does NOT provoke (RAW Action Table)."""

    weapon_id: str


@dataclass(frozen=True)
class StandUp(Action):
    """Move action: stand from prone. Provokes AoOs from threateners."""


@dataclass(frozen=True)
class Mount(Action):
    """Move action: mount an adjacent steed."""

    steed_id: str


@dataclass(frozen=True)
class Dismount(Action):
    """Move action: dismount the current steed."""


# ── Standard-action grab bag ──────────────────────────────────────────


@dataclass(frozen=True)
class DrinkPotion(Action):
    """Standard action: drink a potion. Provokes."""

    potion_id: str


@dataclass(frozen=True)
class AidAnother(Action):
    """Standard action: aid an adjacent ally with attack or AC."""

    ally_id: str
    mode: str = "attack"  # "attack" or "ac"


@dataclass(frozen=True)
class FightDefensively(Action):
    """Standard action: -4 attack / +2 dodge AC; single attack.

    ``options`` carries flags the executor reads on the attack
    (e.g., ``power_attack``, ``combat_expertise``)."""

    target_id: str
    options: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Cleave(Action):
    """Standard action: attack target; on hit, attack one adjacent foe.
    Phase 1 picks the secondary target hardcoded per the v1 path; the
    sub-action decision point for the secondary lands in Phase 3."""

    target_id: str


@dataclass(frozen=True)
class ChannelEnergy(Action):
    """Standard action: channel positive/negative energy in a 30-ft burst."""

    mode: str = "heal_living"


@dataclass(frozen=True)
class StunningFist(Action):
    """Standard action: declare and resolve an unarmed strike that stuns
    on a failed Fort save."""

    target_id: str


@dataclass(frozen=True)
class BardicPerformance(Action):
    """Standard action (initial; later rounds maintain via free): start
    a bardic performance. ``kind`` is the performance type."""

    kind: str = "inspire_courage"


@dataclass(frozen=True)
class DetectEvil(Action):
    """Standard action: detect alignment auras in a cone. ``target_id``
    is the focused-target form of the SLA (paladin AI's primary use
    case); empty string means no target."""

    target_id: str = ""


@dataclass(frozen=True)
class DomainPower(Action):
    """Standard action: cleric domain-granted active power. The full
    v1 args dict (``domain_id``, ``target``, etc.) lives in
    ``options`` since each domain power has its own arg shape."""

    options: dict = field(default_factory=dict)


@dataclass(frozen=True)
class EscapeWeb(Action):
    """Standard action while in webbing: Strength check or Escape
    Artist to free yourself."""


@dataclass(frozen=True)
class ReadyBrace(Action):
    """Standard action: ready a brace-flagged weapon vs an incoming
    charge. Sets the ``bracing`` condition for one round."""


@dataclass(frozen=True)
class Web(Action):
    """Standard action (spider): cast a web at a target — Reflex save
    or be entangled / restrained."""

    target_id: str


# ── Swift-action grab bag ─────────────────────────────────────────────


@dataclass(frozen=True)
class SmiteEvil(Action):
    """Swift action: declare a target; bonuses apply on attacks until
    target dies or paladin rests."""

    target_id: str


# ── Free actions ──────────────────────────────────────────────────────


@dataclass(frozen=True)
class RageStart(Action):
    """Free action: enter rage."""


@dataclass(frozen=True)
class RageEnd(Action):
    """Free action: end rage voluntarily."""


# ── Full-round grab bag ───────────────────────────────────────────────


@dataclass(frozen=True)
class Run(Action):
    """Full-round action: 4x speed in a straight line; loses Dex to AC."""

    direction: str


@dataclass(frozen=True)
class Trample(Action):
    """Full-round action: charge through one or more foes. v1 helper
    takes a target rather than a direction (the mount overruns the
    named foe); ``direction`` is preserved for the rare directional-
    overrun case."""

    target_id: str = ""
    direction: str = ""


@dataclass(frozen=True)
class CoupDeGrace(Action):
    """Full-round action vs. an adjacent helpless target: auto-hit + crit
    damage; target rolls Fort or dies."""

    target_id: str


@dataclass(frozen=True)
class TailSpikeVolley(Action):
    """Full-round action (manticore): four ranged spike attacks against
    a single target."""

    target_id: str


# ── Spellcasting ──────────────────────────────────────────────────────


@dataclass(frozen=True)
class Cast(Action):
    """Cast a spell at a target combatant or self.

    For AOE spells (fireball, sleep, etc.), the target's square is the
    AOE center. For single-creature spells, the target is the affected
    creature. For self-only spells (mage_armor, true_strike), target_id
    is the actor's own id.

    ``defensive`` triggers a concentration check (DC 15 + 2 * spell
    level) when the actor is threatened; without it, the cast provokes
    AoOs from threateners. ``metamagic`` is the list of metamagic
    feats applied to this cast; raises the slot cost per the
    metamagic_bumps table in turn_executor."""

    spell_id: str
    target_id: str
    spell_level: int
    # ``defensive``: True forces a defensive cast (concentration vs.
    # DC 15 + 2L). False forces a non-defensive cast (provokes if
    # threatened). None lets ``_do_cast`` apply its default — which
    # per v1 RAW is defensive when threatened, non-defensive
    # otherwise.
    defensive: bool | None = None
    metamagic: tuple[str, ...] = ()
    # Extra v1 args that affect cast resolution but don't fit the
    # canonical fields (spontaneous_cure for clerics, fancy override
    # flags, etc.). Passed through to _do_cast as args entries.
    options: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Per-turn slot accounting and game-state wrapper
# ---------------------------------------------------------------------------


@dataclass
class TurnSlots:
    """Per-turn action-economy tracker for one actor.

    Reset at the start of each actor's turn (the substrate's
    responsibility, not the picker's). Used by
    ``enumerate_legal_actions`` to filter out actions whose slot is
    already spent.
    """

    standard_used: bool = False
    move_used: bool = False
    swift_used: bool = False
    five_foot_step_used: bool = False
    full_round_used: bool = False
    movement_taken: bool = False  # any squares of movement consumed
    turn_ended: bool = False


@dataclass
class GameState:
    """Substrate wrapper over (encounter, grid) plus per-actor turn
    slots. The picker sees this read-only; the substrate mutates it
    inside ``apply_action``."""

    encounter: Encounter
    grid: Grid
    turn_slots: dict[str, TurnSlots] = field(default_factory=dict)

    def slots_for(self, actor: Combatant) -> TurnSlots:
        slots = self.turn_slots.get(actor.id)
        if slots is None:
            slots = TurnSlots()
            self.turn_slots[actor.id] = slots
        return slots

    def reset_turn(self, actor: Combatant) -> None:
        """Reset ``actor``'s slot tracker for a fresh turn."""
        self.turn_slots[actor.id] = TurnSlots()


@dataclass
class ApplyResult:
    """What ``apply_action`` returned: the events the action emitted.

    Phase 2 will add ``next_decision_owner`` and reactive-interrupt
    ordering. For Phase 1 the substrate produces only a flat event
    stream (matching the v1 executor's output)."""

    events: list  # list[TurnEvent], imported indirectly to avoid cycles


# ---------------------------------------------------------------------------
# enumerate_legal_actions
# ---------------------------------------------------------------------------


def enumerate_legal_actions(
    actor: Combatant,
    state: GameState,
) -> list[Action]:
    """Every action ``actor`` may take from ``state`` right now.

    ``EndTurn`` is always present (the actor can voluntarily end at
    any time). The other actions surface only when the actor's
    condition state, slot accounting, and grid permit them.

    Phase 1 covers movement / attack / full-attack / charge /
    withdraw / total-defense; later actions (Cast, maneuvers,
    reactive interrupts) will be added here as they're implemented.
    """
    actions: list[Action] = [EndTurn(actor_id=actor.id)]
    slots = state.slots_for(actor)

    if slots.turn_ended:
        return actions

    # Actor inability gates: dead / unconscious / dying / paralyzed /
    # petrified actors can't take actions. Stunned and dazed gate
    # too — see Combatant condition handling.
    if not _can_take_actions(actor):
        return actions

    grid = state.grid
    encounter = state.encounter

    # Movement options ─────────────────────────────────────────────────
    # 5-ft step: legal only when no movement has been taken yet, the
    # five_foot_step slot itself isn't spent, and the actor isn't
    # grappled / paralyzed / etc.
    if (
        not slots.movement_taken
        and not slots.five_foot_step_used
        and not slots.full_round_used
        and "grappled" not in actor.conditions
        and "pinned" not in actor.conditions
    ):
        for dest in _adjacent_legal_squares(actor, grid):
            actions.append(FiveFootStep(actor_id=actor.id, destination=dest))

    # Move: standard move action.
    if (
        not slots.move_used
        and not slots.movement_taken
        and not slots.full_round_used
        and "grappled" not in actor.conditions
    ):
        from .turn_executor import _movement_squares  # avoid cycle at import time
        budget = _movement_squares(actor, encounter)
        for dest in _reachable_squares(actor, grid, budget):
            actions.append(Move(actor_id=actor.id, destination=dest))

    # Attack options (melee + ranged) ─────────────────────────────────
    # An Attack consumes the standard slot. Surfaced for every visible
    # legal target.
    if not slots.standard_used and not slots.full_round_used:
        for target in _attackable_targets(actor, grid):
            actions.append(Attack(
                actor_id=actor.id, target_id=target.id, weapon_index=0,
            ))

    # Full-round options ──────────────────────────────────────────────
    # FullAttack / Charge / Withdraw all consume the full-round slot;
    # offered only if neither standard nor move has been used.
    if (
        not slots.standard_used
        and not slots.move_used
        and not slots.full_round_used
    ):
        for target in _attackable_targets(actor, grid):
            actions.append(FullAttack(actor_id=actor.id, target_id=target.id))
        for target in _chargeable_targets(actor, grid, encounter):
            actions.append(Charge(actor_id=actor.id, target_id=target.id))
        # Withdraw: list the cardinal/intercardinal directions where a
        # path of any length is possible; the apply step computes the
        # actual destination.
        for direction in _viable_withdraw_directions(actor, grid):
            actions.append(Withdraw(actor_id=actor.id, direction=direction))

    # Total Defense (standard action, no attack permitted) ────────────
    if not slots.standard_used and not slots.full_round_used:
        actions.append(TotalDefense(actor_id=actor.id))

    # Combat maneuvers ────────────────────────────────────────────────
    # All 10 maneuvers consume the standard slot. Each requires an
    # adjacent hostile target; ``grapple`` additionally requires the
    # actor isn't already grappling someone (RAW: you can't initiate a
    # second grapple while holding one).
    if not slots.standard_used and not slots.full_round_used:
        adj_enemies = [
            t for t in _attackable_targets(actor, grid)
            if grid.is_adjacent(actor, t)
        ]
        for kind in sorted(_MANEUVER_KINDS):
            if kind == "grapple" and actor.grappling_target_id is not None:
                continue
            for target in adj_enemies:
                actions.append(Maneuver(
                    actor_id=actor.id, kind=kind, target_id=target.id,
                ))

    # Spellcasting — enumerated per spell × per target. Defensive
    # variants are added when the actor is in a threatened square.
    # Phase 1 simplifications: no metamagic combinations enumerated
    # (patrons can construct Cast actions with metamagic manually);
    # AOE spells use the target combatant's square as the AOE center
    # rather than enumerating every reachable square.
    if not slots.standard_used and not slots.full_round_used:
        for cast in _enumerate_casts(actor, state):
            actions.append(cast)

    # Move-action grab bag: stand-up (prone only), mount/dismount, and
    # draw-weapon. DrawWeapon enumeration pulls from carried_items
    # (only weapons that aren't already held).
    if (
        not slots.move_used
        and not slots.movement_taken
        and not slots.full_round_used
    ):
        if "prone" in actor.conditions:
            actions.append(StandUp(actor_id=actor.id))
        if actor.mount_id is not None:
            actions.append(Dismount(actor_id=actor.id))
        else:
            for steed in _adjacent_mountable_steeds(actor, grid):
                actions.append(Mount(actor_id=actor.id, steed_id=steed.id))
        for weapon_id in _stowed_weapon_ids(actor):
            actions.append(DrawWeapon(
                actor_id=actor.id, weapon_id=weapon_id,
            ))

    # Standard-action grab bag.
    if not slots.standard_used and not slots.full_round_used:
        # AidAnother — any adjacent ally.
        for ally in _adjacent_allies(actor, grid):
            actions.append(AidAnother(
                actor_id=actor.id, ally_id=ally.id, mode="attack",
            ))
            actions.append(AidAnother(
                actor_id=actor.id, ally_id=ally.id, mode="ac",
            ))
        # FightDefensively / Cleave / StunningFist — need an adjacent
        # foe.
        for foe in _attackable_targets(actor, grid):
            if grid.is_adjacent(actor, foe):
                actions.append(FightDefensively(
                    actor_id=actor.id, target_id=foe.id,
                ))
                actions.append(Cleave(actor_id=actor.id, target_id=foe.id))
                if actor.resources.get("stunning_fist_uses", 0) > 0:
                    actions.append(StunningFist(
                        actor_id=actor.id, target_id=foe.id,
                    ))
        # ChannelEnergy / DetectEvil / EscapeWeb / DrinkPotion /
        # BardicPerformance / DomainPower — no target needed.
        if actor.resources.get("channel_energy_uses", 0) > 0:
            actions.append(ChannelEnergy(
                actor_id=actor.id, mode="heal_living",
            ))
            actions.append(ChannelEnergy(
                actor_id=actor.id, mode="harm_undead",
            ))
        # Detect Evil: paladins always; just emit one option.
        actions.append(DetectEvil(actor_id=actor.id))
        if "webbed" in actor.conditions or "entangled" in actor.conditions:
            actions.append(EscapeWeb(actor_id=actor.id))
        if actor.resources.get("bardic_performance_rounds", 0) > 0:
            actions.append(BardicPerformance(
                actor_id=actor.id, kind="inspire_courage",
            ))
        for power in actor.domain_spells.keys() if isinstance(
            getattr(actor, "domain_spells", None), dict,
        ) else ():
            actions.append(DomainPower(actor_id=actor.id, power=power))
        for potion_id in _carried_potion_ids(actor):
            actions.append(DrinkPotion(
                actor_id=actor.id, potion_id=potion_id,
            ))

    # Swift-action grab bag.
    if not slots.swift_used:
        if actor.resources.get("smite_evil_uses", 0) > 0:
            # Smite Evil can target any visible foe regardless of
            # melee/ranged reach (the bonuses apply to whatever attack
            # the paladin makes against them next).
            for other in grid.combatants.values():
                if other.id == actor.id or other.team == actor.team:
                    continue
                if not other.is_alive() or "dead" in other.conditions:
                    continue
                actions.append(SmiteEvil(
                    actor_id=actor.id, target_id=other.id,
                ))

    # Free-action grab bag (rage). Free actions don't consume the
    # standard/move slots; we don't track a free-action budget for
    # them. Picker can pick rage_start once per turn (apply will skip
    # if already raging).
    if actor.resources.get("rage_rounds", 0) > 0:
        if "raging" not in actor.conditions:
            actions.append(RageStart(actor_id=actor.id))
        else:
            actions.append(RageEnd(actor_id=actor.id))

    # Full-round grab bag: Run, Trample, CoupDeGrace, TailSpikeVolley.
    if (
        not slots.standard_used
        and not slots.move_used
        and not slots.full_round_used
    ):
        for direction in _viable_withdraw_directions(actor, grid):
            actions.append(Run(actor_id=actor.id, direction=direction))
        # Trample requires the trample racial trait. The v1 helper
        # takes a target (the mount overruns through it); we offer
        # one Trample per visible enemy.
        if _has_trait(actor, "trample"):
            for foe in _attackable_targets(actor, grid):
                actions.append(Trample(
                    actor_id=actor.id, target_id=foe.id,
                ))
        # CoupDeGrace: helpless adjacent foe.
        for foe in _attackable_targets(actor, grid):
            if (
                grid.is_adjacent(actor, foe)
                and "helpless" in foe.conditions
            ):
                actions.append(CoupDeGrace(
                    actor_id=actor.id, target_id=foe.id,
                ))
        # TailSpikeVolley: actor has the manticore tail_spikes trait
        # and at least one spike left.
        if (
            _has_trait(actor, "tail_spikes")
            and actor.daily_resources.get("tail_spikes", 0) > 0
        ):
            for foe in _attackable_targets(actor, grid):
                actions.append(TailSpikeVolley(
                    actor_id=actor.id, target_id=foe.id,
                ))

    # Grapple maintenance — usable only when the actor is currently
    # grappling someone (grappling_target_id set) or being grappled
    # (grappled_by_id set). All consume the standard slot.
    if not slots.standard_used and not slots.full_round_used:
        if actor.grappling_target_id is not None:
            actions.append(GrappleDamage(actor_id=actor.id))
            actions.append(GrapplePin(actor_id=actor.id))
            # GrappleMove: enumerate the eight directions; apply step
            # walks the actor + grappled foe up to half speed that way.
            for direction in _viable_withdraw_directions(actor, grid):
                actions.append(GrappleMove(
                    actor_id=actor.id, direction=direction,
                ))
        if actor.grappled_by_id is not None:
            actions.append(GrappleBreakFree(actor_id=actor.id))
            actions.append(GrappleBreakFree(
                actor_id=actor.id, use_skill=True,
            ))

    return actions


# ---------------------------------------------------------------------------
# apply_action
# ---------------------------------------------------------------------------


def apply_action(
    action: Action,
    state: GameState,
    roller: Roller,
) -> ApplyResult:
    """Resolve ``action`` against ``state``, mutating it in place.

    Delegates to the existing ``_do_*`` helpers in ``turn_executor``
    where possible to avoid duplicating logic. Returns the emitted
    event stream; Phase 2 will extend the result to carry the next
    decision-point's owner and any reactive-interrupt scheduling.
    """
    from .turn_executor import (  # local import to avoid cycle
        TurnEvent,
        _do_attack,
        _do_charge,
        _do_full_attack,
        _do_withdraw,
        _do_5ft_step,
        _move_along,
        _movement_squares,
    )
    from .modifiers import Modifier

    actor = state.grid.combatants.get(action.actor_id)
    if actor is None:
        # Defensive: the picker handed us an action whose actor isn't
        # on the grid. Treat as a no-op skip.
        evt = TurnEvent(action.actor_id, "skip", {
            "reason": "apply_action: actor not on grid",
        })
        return ApplyResult(events=[evt])

    events: list = []
    slots = state.slots_for(actor)
    grid = state.grid
    encounter = state.encounter

    if isinstance(action, EndTurn):
        slots.turn_ended = True
        return ApplyResult(events=events)

    if isinstance(action, Move):
        budget = _movement_squares(actor, encounter)
        _move_along(actor, action.destination, budget, grid, events,
                    encounter=encounter)
        slots.move_used = True
        slots.movement_taken = True
        return ApplyResult(events=events)

    if isinstance(action, FiveFootStep):
        _do_5ft_step(actor, action.destination, grid, {}, events)
        slots.five_foot_step_used = True
        slots.movement_taken = True
        return ApplyResult(events=events)

    if isinstance(action, Attack):
        target = grid.combatants.get(action.target_id)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "attack: target gone"}))
            return ApplyResult(events=events)
        _do_attack(actor, target, grid, roller, events,
                   encounter=encounter,
                   attack_index=action.weapon_index)
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, FullAttack):
        target = grid.combatants.get(action.target_id)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "full_attack: target gone"}))
            return ApplyResult(events=events)
        _do_full_attack(actor, target, dict(action.options),
                        grid, roller, events, encounter=encounter)
        slots.full_round_used = True
        return ApplyResult(events=events)

    if isinstance(action, Charge):
        target = grid.combatants.get(action.target_id)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "charge: target gone"}))
            return ApplyResult(events=events)
        args = {"target": target, **action.options}
        _do_charge(actor, args, encounter, grid, roller, {}, events)
        slots.full_round_used = True
        return ApplyResult(events=events)

    if isinstance(action, PartialCharge):
        from .turn_executor import _do_partial_charge
        target = grid.combatants.get(action.target_id)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "partial_charge: target gone"}))
            return ApplyResult(events=events)
        args = {"target": target, **action.options}
        _do_partial_charge(actor, args, encounter, grid, roller, {}, events)
        slots.full_round_used = True
        return ApplyResult(events=events)

    if isinstance(action, Withdraw):
        _do_withdraw(actor, {"direction": action.direction}, encounter,
                     grid, events)
        slots.full_round_used = True
        return ApplyResult(events=events)

    if isinstance(action, TotalDefense):
        cur_round = encounter.round_number if encounter else 1
        src = "total_defense"
        actor.modifiers.remove_by_source(src)
        actor.modifiers.add(Modifier(
            value=4, type="dodge", target="ac",
            source=src, expires_round=cur_round + 1,
        ))
        events.append(TurnEvent(actor.id, "total_defense", {
            "ac_bonus": 4, "expires_round": cur_round + 1,
        }))
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, Maneuver):
        from .turn_executor import _do_combat_maneuver
        target = grid.combatants.get(action.target_id)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": f"{action.kind}: target gone"}))
            return ApplyResult(events=events)
        args = {"target": target, **action.options}
        _do_combat_maneuver(
            actor, action.kind, args, encounter, grid, roller, {}, events,
        )
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, GrappleDamage):
        from .turn_executor import _do_grapple_damage
        _do_grapple_damage(actor, {}, encounter, grid, roller, {}, events)
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, GrappleMove):
        from .turn_executor import _do_grapple_move
        _do_grapple_move(
            actor, {"direction": action.direction},
            encounter, grid, roller, {}, events,
        )
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, GrapplePin):
        from .turn_executor import _do_grapple_pin
        _do_grapple_pin(actor, {}, encounter, grid, roller, {}, events)
        slots.standard_used = True
        return ApplyResult(events=events)

    # ── Move-action grab bag ───────────────────────────────────────
    if isinstance(action, DrawWeapon):
        from .turn_executor import _do_move_action
        _do_move_action(
            actor, {"type": "draw_weapon", "weapon": action.weapon_id},
            encounter, grid, {}, events,
        )
        slots.move_used = True
        return ApplyResult(events=events)

    if isinstance(action, StandUp):
        from .turn_executor import _do_move_action
        _do_move_action(
            actor, {"type": "stand_up"},
            encounter, grid, {}, events,
        )
        slots.move_used = True
        return ApplyResult(events=events)

    if isinstance(action, Mount):
        from .turn_executor import _do_mount
        _do_mount(actor, {"steed_id": action.steed_id},
                  grid, {}, events)
        slots.move_used = True
        return ApplyResult(events=events)

    if isinstance(action, Dismount):
        from .turn_executor import _do_dismount
        _do_dismount(actor, {}, grid, events)
        slots.move_used = True
        return ApplyResult(events=events)

    # ── Standard-action grab bag ───────────────────────────────────
    if isinstance(action, DrinkPotion):
        from .turn_executor import _do_move_action
        _do_move_action(
            actor, {"type": "drink_potion", "potion": action.potion_id},
            encounter, grid, {}, events,
        )
        slots.standard_used = True  # drink is move-action per RAW; we
        # track it as standard for simplicity until a finer slot model
        # lands.
        return ApplyResult(events=events)

    if isinstance(action, AidAnother):
        from .turn_executor import _do_aid_another
        ally = grid.combatants.get(action.ally_id)
        if ally is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "aid: ally gone"}))
            return ApplyResult(events=events)
        _do_aid_another(
            actor, {"target": ally, "mode": action.mode},
            encounter, grid, roller, {}, events,
        )
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, FightDefensively):
        from .turn_executor import _do_fight_defensively
        target = grid.combatants.get(action.target_id)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "fight_defensively: target gone"}))
            return ApplyResult(events=events)
        args = {"target": target, **action.options}
        _do_fight_defensively(
            actor, args, encounter, grid, roller, {}, events,
        )
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, Cleave):
        from .turn_executor import _do_cleave
        target = grid.combatants.get(action.target_id)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "cleave: target gone"}))
            return ApplyResult(events=events)
        _do_cleave(
            actor, {"target": target}, encounter, grid, roller, {}, events,
        )
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, ChannelEnergy):
        from .turn_executor import _do_channel_energy
        _do_channel_energy(
            actor, {"mode": action.mode},
            encounter, grid, roller, {}, events,
        )
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, StunningFist):
        from .turn_executor import _do_stunning_fist
        target = grid.combatants.get(action.target_id)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "stunning_fist: target gone"}))
            return ApplyResult(events=events)
        _do_stunning_fist(
            actor, {"target": target},
            encounter, grid, roller, {}, events,
        )
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, BardicPerformance):
        from .turn_executor import _do_bardic_performance
        _do_bardic_performance(
            actor, {"kind": action.kind},
            encounter, grid, {}, events,
        )
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, DetectEvil):
        from .turn_executor import _do_detect_evil
        args = {}
        if action.target_id:
            tgt = grid.combatants.get(action.target_id)
            if tgt is not None:
                args["target"] = tgt
        _do_detect_evil(actor, args, grid, {}, events)
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, DomainPower):
        from .turn_executor import _do_domain_power
        # The v1 args may carry a ``target`` that's been pre-resolved
        # to a Combatant (when run through the parity translator) or
        # left as a string for the helper to resolve. Either way we
        # pass the dict through.
        args = dict(action.options)
        _do_domain_power(
            actor, args, encounter, grid, roller, {}, events,
        )
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, EscapeWeb):
        from .turn_executor import _do_escape_web
        _do_escape_web(actor, {}, grid, roller, {}, events)
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, ReadyBrace):
        from .turn_executor import _do_ready_brace
        _do_ready_brace(actor, {}, encounter, events)
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, Web):
        from .turn_executor import _do_web
        target = grid.combatants.get(action.target_id)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "web: target gone"}))
            return ApplyResult(events=events)
        _do_web(actor, {"target": target},
                encounter, grid, roller, {}, events)
        slots.standard_used = True
        return ApplyResult(events=events)

    # ── Swift-action grab bag ──────────────────────────────────────
    if isinstance(action, SmiteEvil):
        from .turn_executor import _do_smite_evil
        target = grid.combatants.get(action.target_id)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "smite_evil: target gone"}))
            return ApplyResult(events=events)
        _do_smite_evil(
            actor, {"target": target}, encounter, grid, {}, events,
        )
        slots.swift_used = True
        return ApplyResult(events=events)

    # ── Free-action grab bag ───────────────────────────────────────
    if isinstance(action, RageStart):
        from .turn_executor import _do_rage_start
        _do_rage_start(actor, {}, encounter, events)
        return ApplyResult(events=events)

    if isinstance(action, RageEnd):
        from .turn_executor import _do_rage_end
        _do_rage_end(actor, events)
        return ApplyResult(events=events)

    # ── Full-round grab bag ────────────────────────────────────────
    if isinstance(action, Run):
        from .turn_executor import _do_run
        _do_run(actor, {"direction": action.direction},
                encounter, grid, events)
        slots.full_round_used = True
        return ApplyResult(events=events)

    if isinstance(action, Trample):
        from .turn_executor import _do_trample
        args: dict = {}
        if action.target_id:
            tgt = grid.combatants.get(action.target_id)
            if tgt is not None:
                args["target"] = tgt
        if action.direction:
            args["direction"] = action.direction
        _do_trample(
            actor, args, encounter, grid, roller, {}, events,
        )
        slots.full_round_used = True
        return ApplyResult(events=events)

    if isinstance(action, CoupDeGrace):
        from .turn_executor import _do_coup_de_grace
        target = grid.combatants.get(action.target_id)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "coup_de_grace: target gone"}))
            return ApplyResult(events=events)
        _do_coup_de_grace(
            actor, {"target": target},
            encounter, grid, roller, {}, events,
        )
        slots.full_round_used = True
        return ApplyResult(events=events)

    if isinstance(action, TailSpikeVolley):
        from .turn_executor import _do_tail_spike_volley
        target = grid.combatants.get(action.target_id)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "tail_spike_volley: target gone"}))
            return ApplyResult(events=events)
        _do_tail_spike_volley(
            actor, {"target": target},
            encounter, grid, roller, {}, events,
        )
        slots.full_round_used = True
        return ApplyResult(events=events)

    if isinstance(action, Cast):
        from .turn_executor import _do_cast
        target = grid.combatants.get(action.target_id)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "cast: target gone"}))
            return ApplyResult(events=events)
        args: dict = {
            "spell": action.spell_id,
            "target": target,
            "spell_level": action.spell_level,
            "metamagic": list(action.metamagic),
            **action.options,
        }
        # Only set ``defensive`` when the picker explicitly chose; None
        # means "let _do_cast apply its v1 default" (defensive when
        # threatened, non-defensive otherwise).
        if action.defensive is not None:
            args["defensive"] = action.defensive
        _do_cast(actor, args, encounter, grid, roller, {}, events)
        slots.standard_used = True
        return ApplyResult(events=events)

    if isinstance(action, GrappleBreakFree):
        from .turn_executor import _do_grapple_break_free
        # v1 helper expects ``method`` ∈ {"cmb", "escape_artist"}.
        method = "escape_artist" if action.use_skill else "cmb"
        _do_grapple_break_free(
            actor, {"method": method},
            encounter, grid, roller, {}, events,
        )
        slots.standard_used = True
        return ApplyResult(events=events)

    raise NotImplementedError(
        f"apply_action: action class {type(action).__name__} "
        f"not yet handled in Phase 1 substrate"
    )


# ---------------------------------------------------------------------------
# Enumeration helpers
# ---------------------------------------------------------------------------


def _can_take_actions(actor: Combatant) -> bool:
    """Conservative liveness check. Mirrors the gates that
    ``execute_turn`` applies via ``validate_turn``."""
    if not actor.is_alive():
        return False
    if "dead" in actor.conditions:
        return False
    if actor.is_unconscious():
        return False
    if "dying" in actor.conditions:
        return False
    if "paralyzed" in actor.conditions:
        return False
    if "petrified" in actor.conditions:
        return False
    if "dazed" in actor.conditions:
        return False
    if "cowering" in actor.conditions:
        return False
    if "fascinated" in actor.conditions:
        return False
    return True


def _adjacent_legal_squares(
    actor: Combatant, grid: Grid,
) -> list[tuple[int, int]]:
    """Squares one step from ``actor.position`` that are passable and
    not occupied. Used for FiveFootStep enumeration."""
    ax, ay = actor.position
    out: list[tuple[int, int]] = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            sq = (ax + dx, ay + dy)
            if not grid.in_bounds(*sq):
                continue
            f = grid.features.get(sq)
            if f is not None and f.blocks_movement:
                continue
            if grid._occupancy.get(sq) is not None:
                continue
            # Difficult terrain forbids 5-ft step (audit gap; tracked).
            # We still surface it here; apply_action delegates to
            # _do_5ft_step which will be tightened in Phase 1 cleanup.
            out.append(sq)
    return out


def _reachable_squares(
    actor: Combatant, grid: Grid, budget: int,
) -> list[tuple[int, int]]:
    """BFS from ``actor.position`` over passable, unoccupied cells,
    bounded by ``budget`` step count.

    Difficult terrain doubles the cost per cell entered. Uses the
    grid's feature map (``GridFeature.movement_cost_multiplier``)."""
    if budget <= 0:
        return []
    start = actor.position
    visited: dict[tuple[int, int], int] = {start: 0}
    queue: deque[tuple[tuple[int, int], int]] = deque([(start, 0)])
    while queue:
        cell, cost = queue.popleft()
        if cost >= budget:
            continue
        cx, cy = cell
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nxt = (cx + dx, cy + dy)
                if not grid.in_bounds(*nxt):
                    continue
                if nxt == start:
                    continue
                f = grid.features.get(nxt)
                if f is not None and f.blocks_movement:
                    continue
                if grid._occupancy.get(nxt) is not None:
                    continue
                step_cost = 1
                if f is not None and f.movement_cost_multiplier > 1:
                    step_cost = int(f.movement_cost_multiplier)
                ncost = cost + step_cost
                if ncost > budget:
                    continue
                if nxt in visited and visited[nxt] <= ncost:
                    continue
                visited[nxt] = ncost
                queue.append((nxt, ncost))
    visited.pop(start, None)
    return sorted(visited.keys())


def _attackable_targets(
    actor: Combatant, grid: Grid,
) -> list[Combatant]:
    """Hostile combatants the actor can plausibly attack right now.

    For melee weapons: any adjacent enemy. For ranged weapons: any
    enemy on the grid (range increments are penalty math, not legality
    gates — total cover is checked at apply time, where it can also
    skip with a clear reason)."""
    if not actor.attack_options:
        return []
    primary = actor.attack_options[0]
    is_ranged = primary.get("type") == "ranged"
    out: list[Combatant] = []
    for cid, other in grid.combatants.items():
        if other.id == actor.id:
            continue
        if other.team == actor.team:
            continue
        if not other.is_alive():
            continue
        if "dead" in other.conditions:
            continue
        if is_ranged:
            out.append(other)
        elif grid.is_adjacent(actor, other):
            out.append(other)
    return out


def _chargeable_targets(
    actor: Combatant, grid: Grid, encounter: Encounter,
) -> list[Combatant]:
    """Enemies the actor could feasibly charge to. Conservative — the
    apply step does the strict straight-line / lane-clear check, so
    here we only filter on distance and basic visibility."""
    if not actor.attack_options:
        return []
    if actor.attack_options[0].get("type") == "ranged":
        # Charge requires a melee attack at the end.
        return []
    from .turn_executor import _movement_squares
    speed = _movement_squares(actor, encounter)
    max_dist = speed * 2  # charge = up to 2x speed
    out: list[Combatant] = []
    for cid, other in grid.combatants.items():
        if other.id == actor.id:
            continue
        if other.team == actor.team:
            continue
        if not other.is_alive():
            continue
        d = grid.distance_squares(actor.position, other.position)
        # PF1 charge: minimum 2 squares (10 ft) from start.
        if d < 2 or d > max_dist:
            continue
        out.append(other)
    return out


# ---------------------------------------------------------------------------
# Phase 2 parity harness: translate v1 TurnIntent into substrate Actions
# and run them. Drop-in replacement for ``execute_turn``.
# ---------------------------------------------------------------------------


def translate_intent(
    do: dict,
    actor: Combatant,
    encounter,
    grid: Grid,
    ns: dict | None = None,
) -> list[Action]:
    """Convert a v1 ``TurnIntent.do`` dict into a list of substrate
    Actions that produce equivalent behavior when applied in order.

    Mirrors ``execute_turn``'s slot walk: free → swift → composite OR
    (move + 5ft + standard). Each slot's intent dict is compiled into
    the matching Action subclass.

    ``ns`` is the intent's namespace dict; passing it lets the
    translator resolve string target expressions (``"enemy.closest"``,
    ``"ally.role(healer)"``) against the same namespace the v1 dispatch
    would. Pass ``intent.namespace`` from the caller.

    Returns ``[..., EndTurn]`` always — the final EndTurn closes the
    turn so the substrate's slot accounting wraps cleanly."""
    actions: list[Action] = []
    ns = ns or {}

    # Swift slot — currently only ``cast`` is supported here in v1.
    swift = do.get("swift")
    if swift is not None and swift.get("type") == "cast":
        compiled = _compile_cast_intent(swift, actor, grid, ns)
        if compiled is not None:
            actions.append(compiled)

    # Composite or slot form.
    if "composite" in do:
        compiled = _compile_composite_intent(
            do["composite"], do.get("args") or {},
            actor, encounter, grid, ns,
        )
        if compiled is not None:
            actions.append(compiled)
    else:
        slots = do.get("slots") or do
        if slots.get("move") is not None:
            compiled = _compile_move_slot_intent(
                slots["move"], actor, encounter, grid, ns,
            )
            if compiled is not None:
                actions.append(compiled)
        five = slots.get("five_foot_step")
        if five is not None:
            actions.append(FiveFootStep(
                actor_id=actor.id, destination=tuple(five),
            ))
        if slots.get("standard") is not None:
            compiled = _compile_standard_slot_intent(
                slots["standard"], actor, encounter, grid, ns,
            )
            if compiled is not None:
                actions.append(compiled)

    actions.append(EndTurn(actor_id=actor.id))
    return actions


def _resolve_intent_target(
    target_value, actor: Combatant, grid: Grid,
    ns: dict | None = None,
) -> Combatant | None:
    """Resolve a target value from a v1 intent into a live Combatant.

    Targets in v1 intents are unevaluated expressions (e.g.,
    ``"enemy.closest"``); the v1 dispatch resolves them at execution
    time via ``_resolve_target`` against the intent's namespace. We
    do the same here so substrate behavior matches."""
    if target_value is None:
        return None
    if isinstance(target_value, Combatant):
        return target_value
    if isinstance(target_value, str):
        # Try grid lookup by id first (already-resolved), then fall back
        # to namespace expression evaluation.
        existing = grid.combatants.get(target_value)
        if existing is not None:
            return existing
        if ns is not None:
            from .turn_executor import _resolve_target
            resolved = _resolve_target(target_value, ns)
            if isinstance(resolved, Combatant):
                return resolved
    return None


_CAST_CANONICAL_KEYS = {
    "spell", "target", "spell_level", "defensive", "metamagic", "type",
}


def _compile_cast_intent(
    args: dict, actor: Combatant, grid: Grid, ns: dict | None = None,
) -> Action | None:
    """Compile a cast-shaped intent dict into a Cast action.

    Anything in ``args`` not in the canonical key set passes through
    via ``Cast.options`` so v1 extras like ``spontaneous_cure`` reach
    ``_do_cast`` unchanged."""
    spell_id = args.get("spell")
    if not spell_id:
        return None
    target = _resolve_intent_target(args.get("target"), actor, grid, ns)
    target_id = target.id if target is not None else actor.id
    extras = {k: v for k, v in args.items()
              if k not in _CAST_CANONICAL_KEYS}
    # Three-valued defensive: explicit True / False from the intent
    # passes through; absence stays None so _do_cast applies its
    # v1-default-when-threatened behavior.
    defensive: bool | None = None
    if "defensive" in args:
        defensive = bool(args["defensive"])
    return Cast(
        actor_id=actor.id, spell_id=spell_id, target_id=target_id,
        spell_level=int(args.get("spell_level", 0)),
        defensive=defensive,
        metamagic=tuple(args.get("metamagic") or ()),
        options=extras,
    )


def _compile_move_slot_intent(
    move: dict, actor: Combatant, encounter, grid: Grid,
    ns: dict | None = None,
) -> Action | None:
    """Compile a move-slot intent into a substrate Action."""
    mtype = move.get("type")
    if mtype == "move_to":
        dest = move.get("target")
        if isinstance(dest, tuple) and len(dest) == 2:
            return Move(actor_id=actor.id, destination=dest)
        return None
    if mtype in ("move_toward", "move_away"):
        target_value = move.get("target")
        target = _resolve_intent_target(target_value, actor, grid, ns)
        if target is None:
            return None
        from .turn_executor import (
            _movement_squares, _square_toward, _square_away,
        )
        speed = _movement_squares(actor, encounter)
        if mtype == "move_toward":
            dest = _square_toward(actor, target, speed, grid)
        else:
            dest = _square_away(actor, target, speed, grid)
        if dest is None:
            return None
        return Move(actor_id=actor.id, destination=dest)
    if mtype == "stand_up":
        return StandUp(actor_id=actor.id)
    if mtype == "draw_weapon":
        return DrawWeapon(
            actor_id=actor.id, weapon_id=str(move.get("weapon", "")),
        )
    if mtype == "drink_potion":
        return DrinkPotion(
            actor_id=actor.id, potion_id=str(move.get("potion", "")),
        )
    # retrieve_stowed_item: no substrate Action yet; skip.
    return None


def _compile_standard_slot_intent(
    std: dict, actor: Combatant, encounter, grid: Grid,
    ns: dict | None = None,
) -> Action | None:
    """Compile a standard-slot intent into a substrate Action."""
    stype = std.get("type")
    if stype == "attack":
        target = _resolve_intent_target(std.get("target"), actor, grid, ns)
        if target is None:
            return None
        return Attack(actor_id=actor.id, target_id=target.id)
    if stype == "total_defense":
        return TotalDefense(actor_id=actor.id)
    if stype == "cast":
        return _compile_cast_intent(std, actor, grid, ns)
    return None


def _compile_composite_intent(
    name: str, args: dict, actor: Combatant, encounter, grid: Grid,
    ns: dict | None = None,
) -> Action | None:
    """Compile a composite intent into a substrate Action.

    Returns None for ``hold`` (which becomes pure EndTurn) and for
    composites that don't yet have a substrate Action (e.g.,
    ``ready_brace``, ``web``, ``partial_charge``); the caller drops
    the unhandled action and falls through to EndTurn so the turn
    still closes cleanly."""
    target = _resolve_intent_target(args.get("target"), actor, grid, ns)
    tid = target.id if target is not None else actor.id

    if name == "hold":
        return None
    # Common helper: pull the args dict, drop the canonical keys we
    # already captured into Action fields, leave the rest in options.
    def _opts(*reserved):
        return {k: v for k, v in args.items() if k not in reserved}

    if name == "charge":
        return Charge(
            actor_id=actor.id, target_id=tid,
            options=_opts("target"),
        )
    if name == "partial_charge":
        return PartialCharge(
            actor_id=actor.id, target_id=tid,
            options=_opts("target"),
        )
    if name == "full_attack":
        # _do_full_attack takes ``options`` directly (not as a nested
        # key on args), so pull it out of the v1 intent.
        return FullAttack(
            actor_id=actor.id, target_id=tid,
            options=args.get("options") or {},
        )
    if name == "withdraw":
        return Withdraw(actor_id=actor.id,
                        direction=args.get("direction", "south"))
    if name == "run":
        return Run(actor_id=actor.id,
                   direction=args.get("direction", "south"))
    if name == "trample":
        return Trample(actor_id=actor.id, target_id=tid,
                       direction=str(args.get("direction", "")))
    if name == "coup_de_grace":
        return CoupDeGrace(actor_id=actor.id, target_id=tid)
    if name == "fight_defensively":
        return FightDefensively(
            actor_id=actor.id, target_id=tid,
            options=_opts("target"),
        )
    if name == "cleave":
        return Cleave(actor_id=actor.id, target_id=tid)
    if name == "cast":
        return _compile_cast_intent(args, actor, grid, ns)
    if name == "smite_evil":
        return SmiteEvil(actor_id=actor.id, target_id=tid)
    if name == "channel_energy":
        return ChannelEnergy(actor_id=actor.id,
                             mode=args.get("mode", "heal_living"))
    if name == "bardic_performance":
        return BardicPerformance(
            actor_id=actor.id,
            kind=args.get("kind", "inspire_courage"),
        )
    if name == "stunning_fist":
        return StunningFist(actor_id=actor.id, target_id=tid)
    if name == "detect_evil":
        return DetectEvil(actor_id=actor.id, target_id=tid)
    if name == "domain_power":
        # Resolve a target expression to a Combatant before stuffing
        # into options, so _do_domain_power doesn't need to evaluate
        # against the v1 namespace from inside our path.
        opts = dict(args)
        if target is not None:
            opts["target"] = target
        return DomainPower(actor_id=actor.id, options=opts)
    if name == "tail_spike_volley":
        return TailSpikeVolley(actor_id=actor.id, target_id=tid)
    if name == "escape_web":
        return EscapeWeb(actor_id=actor.id)
    if name == "ready_brace":
        return ReadyBrace(actor_id=actor.id)
    if name == "web":
        return Web(actor_id=actor.id, target_id=tid)
    if name == "aid_another":
        return AidAnother(actor_id=actor.id, ally_id=tid,
                          mode=args.get("mode", "attack"))
    if name == "mount":
        return Mount(actor_id=actor.id, steed_id=tid)
    if name == "dismount":
        return Dismount(actor_id=actor.id)
    if name == "rage_start":
        return RageStart(actor_id=actor.id)
    if name == "rage_end":
        return RageEnd(actor_id=actor.id)
    if name == "grapple_damage":
        return GrappleDamage(actor_id=actor.id)
    if name == "grapple_move":
        return GrappleMove(actor_id=actor.id,
                           direction=args.get("direction", "north"))
    if name == "grapple_pin":
        return GrapplePin(actor_id=actor.id)
    if name == "grapple_break_free":
        # v1 method ∈ {"cmb", "escape_artist"} ↔ substrate use_skill.
        method = args.get("method", "cmb")
        return GrappleBreakFree(
            actor_id=actor.id,
            use_skill=(method == "escape_artist"),
        )
    if name in _MANEUVER_KINDS:
        opts = {k: v for k, v in args.items() if k != "target"}
        return Maneuver(actor_id=actor.id, kind=name,
                        target_id=tid, options=opts)
    # Unhandled composites: ``ready_brace``, ``web``, ``partial_charge``,
    # and any future composite without a substrate Action yet. Phase 2
    # will fill these in as parity tests surface them.
    return None


def run_intent_via_substrate(
    actor: Combatant,
    intent,  # TurnIntent | None
    encounter,
    grid: Grid,
    roller: Roller,
):
    """Drop-in substrate-based replacement for ``execute_turn``.

    Takes the same arguments and produces an equivalent ``TurnResult``
    by translating the intent into substrate Actions and applying
    them. Behavior is intended to match ``execute_turn`` for every
    intent shape the v1 dispatch supports — that's the parity
    contract Phase 2 must achieve before Phase 5 can delete the v1
    executor.

    Mirrored from execute_turn:
      - hold / no rule matched → skip with reason; still tick aura
        end-of-turn riders.
      - validate_turn before dispatch; on error skip with
        ``invalid_turn`` reason.
      - confusion d% substitutes the do-block.
      - free actions emitted as ``free`` events (or ``fall_prone``).
      - then the slot walk via ``translate_intent`` + ``apply_action``.
      - end-of-turn racial-effect riders fired after.
    """
    from .turn_executor import (
        TurnEvent,
        _apply_end_of_turn_racial_effects,
        _apply_post_damage_state,
        _intent_to_turn,
        _resolve_confusion,
        _turn_used_standard_action,
    )
    from .dsl import TurnIntent  # noqa: F401 — typing only
    from .encounter import (
        Turn as _Turn,  # noqa: F401
        TurnValidationError,
        validate_turn,
    )

    # Local import of TurnResult to avoid a top-level cycle.
    from .turn_executor import TurnResult

    rule_index = intent.rule_index if intent else None
    events: list = []

    if intent is None or (
        "composite" in intent.do
        and intent.do["composite"] == "hold"
    ):
        events.append(TurnEvent(
            actor.id, "skip",
            {"reason": "no rule matched" if intent is None else "hold"},
        ))
        _apply_end_of_turn_racial_effects(
            actor, grid, roller, events, encounter=encounter,
        )
        return TurnResult(actor.id, rule_index, events)

    # Action-economy validation (same as execute_turn).
    try:
        validate_turn(_intent_to_turn(intent.do), actor, grid)
    except TurnValidationError as exc:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "invalid_turn",
            "detail": str(exc),
        }))
        _apply_end_of_turn_racial_effects(
            actor, grid, roller, events, encounter=encounter,
        )
        return TurnResult(actor.id, rule_index, events)

    do = intent.do

    # Confusion d% (forced-substituted in v2 terms; v1 mutates do
    # in-place — we mirror that here).
    if "confused" in actor.conditions:
        do = _resolve_confusion(actor, do, encounter, grid, roller, events)
        if do is None:
            return TurnResult(actor.id, rule_index, events)

    # Free actions — these don't have substrate Actions yet, so we
    # mirror execute_turn's emit-only handling.
    for fa in do.get("free", []) or []:
        fa_type = fa.get("type") if isinstance(fa, dict) else None
        if fa_type == "fall_prone":
            if "prone" not in actor.conditions:
                actor.add_condition("prone")
            events.append(TurnEvent(actor.id, "fall_prone", {}))
        else:
            events.append(TurnEvent(actor.id, "free",
                                    {"action": fa}))

    # Swift cast gate: matches the check in execute_turn. A swift-slot
    # cast requires either a native-swift-time spell or the
    # quicken_spell metamagic; reject otherwise with the exact same
    # event the v1 path emits, before the slot walk.
    swift = do.get("swift")
    if swift is not None and swift.get("type") == "cast":
        from .turn_executor import _classify_casting_time
        from .content import default_registry
        mm = list(swift.get("metamagic") or [])
        native_swift = False
        spell_id = swift.get("spell")
        if spell_id:
            try:
                s = default_registry().get_spell(spell_id)
                native_swift = (
                    _classify_casting_time(s.casting_time) == "swift"
                )
            except Exception:
                pass
        if "quicken_spell" not in mm and not native_swift:
            events.append(TurnEvent(actor.id, "skip", {
                "reason": "swift cast requires either a native swift-time "
                          "spell or the quicken_spell metamagic",
                "spell": spell_id,
            }))
            do = dict(do)
            do.pop("swift", None)

    # Translate the rest of the intent into substrate Actions and run
    # them via the substrate.
    state = GameState(encounter=encounter, grid=grid)
    state.reset_turn(actor)
    ns = intent.namespace if intent is not None else None
    actions_to_run = translate_intent(do, actor, encounter, grid, ns)
    for action in actions_to_run:
        result = apply_action(action, state, roller)
        events.extend(result.events)
        if not actor.is_alive():
            break

    # Disabled self-damage (matches execute_turn).
    if "disabled" in actor.conditions and actor.current_hp == 0:
        if _turn_used_standard_action(events):
            actor.take_damage(1)
            _apply_post_damage_state(actor)
            events.append(TurnEvent(actor.id, "disabled_self_damage", {
                "amount": 1,
            }))

    # End-of-turn aura / ongoing-effect riders.
    _apply_end_of_turn_racial_effects(
        actor, grid, roller, events, encounter=encounter,
    )

    return TurnResult(actor.id, rule_index, events)


# ---------------------------------------------------------------------------
# Picker (patron-facing) and driver loop (engine-internal)
#
# These are demo-grade for Phase 1 — enough to run a small simulation
# end-to-end and validate the substrate. The real picker compilation
# from BehaviorScript / DSL lives in dsl.py and lands in Phase 4; the
# real driver loop integrates with the sandbox tick worker in Phase 2.
# ---------------------------------------------------------------------------


class Picker:
    """Patron-facing behavior interface. Replaces ``BehaviorScript`` /
    ``TurnIntent`` in the v2 model.

    A picker is called many times per turn — once per decision point.
    Each call receives the actor, the read-only game state, and the
    legal-actions list; it returns one chosen action. The picker is
    *kind-blind*: see ``DECISION_POINT_DSL.md`` §4.1 for why."""

    def pick(
        self,
        actor: Combatant,
        state: GameState,
        actions: list[Action],
    ) -> Action:
        raise NotImplementedError


class ClosestEnemyPicker(Picker):
    """Demo behavior: a melee fighter who walks toward the closest
    enemy and attacks. Preference order:

      1. FullAttack on the closest enemy if offered.
      2. Charge to the closest enemy if offered.
      3. Single Attack on the closest enemy if offered.
      4. Move toward the closest enemy.
      5. EndTurn.

    Demonstrates the per-decision picker shape; not a real DSL-
    compiled picker."""

    def pick(
        self,
        actor: Combatant,
        state: GameState,
        actions: list[Action],
    ) -> Action:
        enemy = self._closest_enemy(actor, state)
        if enemy is None:
            return _first(actions, EndTurn)

        for a in actions:
            if isinstance(a, FullAttack) and a.target_id == enemy.id:
                return a
        for a in actions:
            if isinstance(a, Charge) and a.target_id == enemy.id:
                return a
        for a in actions:
            if isinstance(a, Attack) and a.target_id == enemy.id:
                return a

        moves = [a for a in actions if isinstance(a, Move)]
        if moves:
            return min(moves, key=lambda m: state.grid.distance_squares(
                m.destination, enemy.position,
            ))
        return _first(actions, EndTurn)

    @staticmethod
    def _closest_enemy(
        actor: Combatant, state: GameState,
    ) -> Combatant | None:
        candidates = [
            o for o in state.grid.combatants.values()
            if o.team != actor.team
            and o.is_alive()
            and "dead" not in o.conditions
        ]
        if not candidates:
            return None
        return min(
            candidates,
            key=lambda c: state.grid.distance_squares(
                actor.position, c.position,
            ),
        )


def _first(actions: list[Action], cls: type) -> Action:
    for a in actions:
        if isinstance(a, cls):
            return a
    raise RuntimeError(f"no {cls.__name__} in legal actions")


def run_encounter(
    state: GameState,
    pickers: dict[str, Picker],
    roller: Roller,
    *,
    max_rounds: int = 50,
) -> list:
    """Drive the encounter to completion (one team standing) or until
    ``max_rounds`` is reached. Returns the flat event log.

    Walks the existing ``Encounter`` initiative order, resets each
    actor's slots at start-of-turn, and loops the picker → apply
    cycle until the picker returns ``EndTurn`` (or the actor hits a
    safety bound on decisions per turn).

    Phase 1 demo. Phase 2 will replace ``execute_turn`` with this
    loop; Phase 3 adds reactive-interrupt handling so the loop
    coordinates B's picker when A's action provokes."""
    from .turn_executor import _apply_end_of_turn_racial_effects
    enc = state.encounter
    log: list = []
    decision_cap = 50  # safety bound per turn
    for _ in range(max_rounds):
        for ir in enc.initiative:
            actor = ir.combatant
            if not actor.is_alive() or "dead" in actor.conditions:
                continue
            picker = pickers.get(actor.id)
            if picker is None:
                continue
            state.reset_turn(actor)
            steps = 0
            while not state.slots_for(actor).turn_ended:
                steps += 1
                if steps > decision_cap:
                    raise RuntimeError(
                        f"actor {actor.id} hit decision cap of "
                        f"{decision_cap} — picker likely looping",
                    )
                actions = enumerate_legal_actions(actor, state)
                chosen = picker.pick(actor, state, actions)
                result = apply_action(chosen, state, roller)
                log.extend(result.events)
                if not actor.is_alive():
                    break
            # End-of-turn riders (auras, rake, etc.) — same pass the
            # v1 executor makes.
            if actor.is_alive() and "dead" not in actor.conditions:
                _apply_end_of_turn_racial_effects(
                    actor, state.grid, roller, log, encounter=enc,
                )
        # Round wrap: tick every combatant (ferocity bleed, dying
        # 1-HP/round loss, ongoing effects, daily refresh, etc.).
        enc.round_number += 1
        for ir in enc.initiative:
            ir.combatant.tick_round(enc.round_number, roller=enc.roller)
        # Victory check.
        teams_alive = {
            ir.combatant.team for ir in enc.initiative
            if ir.combatant.is_alive()
            and "dead" not in ir.combatant.conditions
        }
        if len(teams_alive) <= 1:
            return log
    return log


def _adjacent_allies(
    actor: Combatant, grid: Grid,
) -> list[Combatant]:
    """Combatants on the actor's team within melee reach (excl. self)."""
    out: list[Combatant] = []
    for cid, other in grid.combatants.items():
        if other.id == actor.id:
            continue
        if other.team != actor.team:
            continue
        if not other.is_alive() or "dead" in other.conditions:
            continue
        if grid.is_adjacent(actor, other):
            out.append(other)
    return out


def _adjacent_mountable_steeds(
    actor: Combatant, grid: Grid,
) -> list[Combatant]:
    """Adjacent allies that look like rideable steeds. Conservative: any
    same-team Large+ creature with no rider. Phase 1 stub — refine when
    Mount has more callers."""
    out: list[Combatant] = []
    for cid, other in grid.combatants.items():
        if other.id == actor.id or other.team != actor.team:
            continue
        if other.rider_id is not None:
            continue
        if not grid.is_adjacent(actor, other):
            continue
        if other.size in ("large", "huge", "gargantuan", "colossal"):
            out.append(other)
    return out


def _stowed_weapon_ids(actor: Combatant) -> list[str]:
    """Weapons in carried_items that aren't currently held. Phase 1
    stub: doesn't distinguish weapon vs. non-weapon items because
    InventoryItem doesn't carry a kind discriminator at this layer."""
    held_ids = {
        item.item_id for item in actor.held_items.values()
        if item is not None
    }
    return sorted({
        item.item_id for item in actor.carried_items
        if item.item_id not in held_ids
    })


def _carried_potion_ids(actor: Combatant) -> list[str]:
    """Items in carried_items whose id begins with 'potion_'. Phase 1
    placeholder — once an Item.kind exists we filter on that."""
    return sorted({
        item.item_id for item in actor.carried_items
        if str(item.item_id).startswith("potion_")
    })


def _has_trait(actor: Combatant, trait_id: str) -> bool:
    """Does ``actor`` carry the named racial trait? Mirrors the
    turn_executor helper without the import cycle."""
    if actor.template_kind != "monster" or actor.template is None:
        return False
    for trait in getattr(actor.template, "racial_traits", ()) or ():
        if isinstance(trait, dict) and trait.get("id") == trait_id:
            return True
    return False


# Spell.target prefixes that mean "self only". Anything starting with
# any of these resolves to a Cast targeting the actor's own id, with
# no enemy/ally enumeration. Other target shapes (creature_touched,
# one_creature, area-shaped, etc.) enumerate per visible combatant.
_SELF_TARGET_PREFIXES: tuple[str, ...] = ("self",)


def _enumerate_casts(
    actor: Combatant, state: GameState,
) -> list[Cast]:
    """Enumerate every (spell, target, defensive) Cast available to
    ``actor`` right now.

    Phase 1 scope:

    - Spell pool comes from ``actor.castable_spells`` (set by both the
      prepared and spontaneous casting models — prepared casters
      populate it with their currently-prepared spells).
    - For each spell, the level is read from ``spell.level_by_class``
      using the actor's class id (when known); falls back to 0.
    - Targets:
        * spells whose ``target`` field starts with "self" → just
          Cast(target=actor.id)
        * everything else → one Cast(target=visible_combatant.id) per
          visible combatant on the grid (allies and enemies both —
          fireball / cure / etc. all share the same enumeration shape;
          the picker chooses friend or foe)
    - When the actor is in a threatened square (some hostile threatens
      them), every Cast is also offered with ``defensive=True``.
    - Metamagic combinations are not enumerated; patrons can construct
      Cast actions with their own ``metamagic`` tuple.
    """
    if not actor.castable_spells:
        return []

    from .content import default_registry
    registry = default_registry()

    grid = state.grid
    threatened = any(
        other.team != actor.team
        and other.is_alive()
        and "dead" not in other.conditions
        and grid.threatens(other, actor)
        for other in grid.combatants.values()
        if other.id != actor.id
    )

    class_id = None
    if actor.template_kind == "character" and actor.template is not None:
        class_id = getattr(actor.template, "class_id", None)

    visible_targets = [
        c for c in grid.combatants.values()
        if c.is_alive() and "dead" not in c.conditions
    ]

    out: list[Cast] = []
    for spell_id in sorted(actor.castable_spells):
        try:
            spell = registry.get_spell(spell_id)
        except Exception:
            continue
        spell_level = 0
        if class_id is not None and class_id in spell.level_by_class:
            spell_level = int(spell.level_by_class[class_id])
        target_field = (spell.target or "").lower()
        is_self_only = any(
            target_field.startswith(p) for p in _SELF_TARGET_PREFIXES
        )
        if is_self_only:
            target_ids = [actor.id]
        else:
            target_ids = [c.id for c in visible_targets]
        for target_id in target_ids:
            out.append(Cast(
                actor_id=actor.id, spell_id=spell_id,
                target_id=target_id, spell_level=spell_level,
                defensive=False,
            ))
            if threatened:
                out.append(Cast(
                    actor_id=actor.id, spell_id=spell_id,
                    target_id=target_id, spell_level=spell_level,
                    defensive=True,
                ))
    return out


def _viable_withdraw_directions(
    actor: Combatant, grid: Grid,
) -> list[str]:
    """Cardinal/intercardinal directions where the first step out of
    the actor's square is into a passable, unoccupied cell. Coarse —
    the apply step walks the full path."""
    deltas = {
        "north": (0, -1), "south": (0, 1),
        "east": (1, 0), "west": (-1, 0),
        "northeast": (1, -1), "northwest": (-1, -1),
        "southeast": (1, 1), "southwest": (-1, 1),
    }
    out: list[str] = []
    ax, ay = actor.position
    for name, (dx, dy) in deltas.items():
        sq = (ax + dx, ay + dy)
        if not grid.in_bounds(*sq):
            continue
        f = grid.features.get(sq)
        if f is not None and f.blocks_movement:
            continue
        if grid._occupancy.get(sq) is not None:
            continue
        out.append(name)
    return out
