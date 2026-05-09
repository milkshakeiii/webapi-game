"""The tick loop. Sole writer of world state.

One call to ``tick(world, registry)`` advances the world by exactly
one PF1 round (= one tick = `world.clock.tick_interval_s` real
seconds). The body:

1. Drain the order queue and apply each via ``apply_order``.
2. Advance every active deployment one round of action toward its
   intent (move, arrive, etc.).
3. Detect new engagements: a hero who just arrived at an active
   location materializes a combat encounter.
4. Run one PF1 round of every active encounter.
5. Resolve completions and deaths.
6. Process location respawns.
7. Publish the read-snapshot for HTTP handlers.

The body holds ``world.write_lock`` for its entire duration. The
worker thread (see ``worker.py``) calls this; HTTP handlers don't.
"""

from __future__ import annotations

import uuid

from dnd.engine.combatant import (
    Combatant,
    combatant_from_hero_record,
    combatant_from_monster,
)
from dnd.engine.content import ContentRegistry
from dnd.engine.dice import Roller
from dnd.engine.dsl import (
    BehaviorScript,
    Interpreter,
    parse_script,
)
from dnd.engine.encounter import Encounter
from dnd.engine.grid import Grid
from dnd.engine.turn_executor import default_monster_intent, execute_turn

from .castle import Castle
from .deployment import (
    PHASE_AT_DESTINATION,
    PHASE_COMPLETE,
    PHASE_DEAD,
    PHASE_IN_COMBAT,
    PHASE_PENDING,
    PHASE_RETURNING,
    PHASE_TRAVELING_OUT,
    Deployment,
    WorldEncounter,
)
from .hero_record import HERO_AT_CASTLE, HeroRecord
from .orders import apply_order
from .world import LOC_ACTIVE, LOC_CLEARED, World


# ---------------------------------------------------------------------------
# Top-level tick
# ---------------------------------------------------------------------------


def tick(world: World, registry: ContentRegistry) -> None:
    """Advance the world by one PF1 round. Sole writer of world state."""
    with world.write_lock:
        # 1. Drain orders.
        for order in world.order_queue.drain():
            apply_order(order, world)

        world.clock.tick_number += 1
        cur_tick = world.clock.tick_number

        # 2. Advance every non-terminal deployment one round.
        for d in list(world.deployments.values()):
            if d.is_terminal():
                continue
            _advance_deployment(d, world, registry)

        # 3. Materialize encounters for newly-arrived heroes.
        for d in list(world.deployments.values()):
            if d.phase == PHASE_AT_DESTINATION and d.encounter_id is None:
                _materialize_encounter(d, world, registry)

        # 4. Run one round of every active encounter.
        for we in list(world.active_encounters.values()):
            _run_encounter_round(we, world, registry)

        # 5. Finalize completed encounters and resolve deployment outcomes.
        for we_id in list(world.active_encounters.keys()):
            we = world.active_encounters[we_id]
            if we.engine_encounter is not None and we.engine_encounter.is_over():
                _finalize_encounter(we, world)
                del world.active_encounters[we_id]

        # 6. Process location respawns.
        _process_respawns(world)

        # 7. Publish snapshot for HTTP readers.
        world.publish_snapshot()


# ---------------------------------------------------------------------------
# Per-deployment advancement
# ---------------------------------------------------------------------------


def _advance_deployment(
    deployment: Deployment, world: World, registry: ContentRegistry,
) -> None:
    """Advance a deployment by one tick worth of activity.

    Phase-specific logic:

    - PENDING: shouldn't really happen (apply_order promotes), but be
      defensive — leave alone.
    - TRAVELING_OUT: move along path by speed-in-cells.
    - AT_DESTINATION: handled by _materialize_encounter outside this fn.
    - IN_COMBAT: handled by _run_encounter_round outside this fn.
    - RETURNING: move along the reversed path back home.
    - DEAD / COMPLETE: terminal, no-op.
    """
    if deployment.phase == PHASE_PENDING:
        return
    if deployment.phase == PHASE_TRAVELING_OUT:
        _step_along_path(deployment, world, returning=False)
        return
    if deployment.phase == PHASE_RETURNING:
        _step_along_path(deployment, world, returning=True)
        return
    # AT_DESTINATION / IN_COMBAT / terminal — handled elsewhere.


def _step_along_path(
    deployment: Deployment, world: World, *, returning: bool,
) -> None:
    """Move the hero forward (or backward) along the path."""
    castle = world.castles.get(deployment.castle_id)
    if castle is None:
        return
    hero = castle.get_hero(deployment.hero_id)
    if hero is None:
        return
    speed_cells = max(1, hero.character.race_id and 6 or 6)  # placeholder; use 6
    speed_cells = _hero_speed_cells(hero, world)

    cur_tick = world.clock.tick_number
    if not returning:
        # Advance forward toward the end of the path.
        target_index = min(
            len(deployment.path) - 1, deployment.path_index + speed_cells,
        )
        if target_index > deployment.path_index:
            deployment.path_index = target_index
            deployment.append_event(cur_tick, "step", {
                "to": list(deployment.path[target_index]),
            })
        if deployment.path_index >= len(deployment.path) - 1:
            deployment.phase = PHASE_AT_DESTINATION
            deployment.append_event(cur_tick, "arrive", {
                "location_id": deployment.destination_location_id,
            })
    else:
        # Returning: walk path indices back toward 0.
        target_index = max(0, deployment.path_index - speed_cells)
        if target_index < deployment.path_index:
            deployment.path_index = target_index
            deployment.append_event(cur_tick, "step", {
                "to": list(deployment.path[target_index]),
            })
        if deployment.path_index <= 0:
            _finalize_deployment_complete(deployment, world)


def _hero_speed_cells(hero: HeroRecord, world: World) -> int:
    """Return how many cells the hero moves per tick (= per PF1 round).

    Speed in feet / 5 ft per cell. Default 6 cells (= 30 ft) for most races.
    """
    # The character object encodes race; race speed comes from the registry
    # at materialization time and isn't stored on HeroRecord. We approximate
    # here using a default; this is fine for v1 since most characters are
    # speed 30. A future enhancement loads race + computes precisely.
    return 6


# ---------------------------------------------------------------------------
# Encounter materialization
# ---------------------------------------------------------------------------


def _materialize_encounter(
    deployment: Deployment, world: World, registry: ContentRegistry,
) -> None:
    """Spawn a fresh combat encounter at the location and bind it to the
    deployment. Transitions the deployment to IN_COMBAT.

    For v1: one resident monster per location, one hero per encounter.
    Multi-monster locations and multi-hero shared encounters land later.
    """
    castle = world.castles.get(deployment.castle_id)
    if castle is None:
        return
    location = world.locations.get(deployment.destination_location_id)
    if location is None:
        return
    hero = castle.get_hero(deployment.hero_id)
    if hero is None:
        return

    # If the location is already cleared (someone else got there
    # first), skip combat and start returning home.
    if location.state != LOC_ACTIVE:
        deployment.phase = PHASE_RETURNING
        deployment.append_event(
            world.clock.tick_number, "empty_location",
            {"location_id": location.id, "state": location.state},
        )
        return

    # Build a small combat grid centered on the location.
    grid_size = 12
    grid = Grid(width=grid_size, height=grid_size)
    hero_pos = (1, grid_size // 2)
    monster_pos = (grid_size - 2, grid_size // 2)

    hero_combatant = combatant_from_hero_record(
        hero, registry, hero_pos, "patrons",
    )
    grid.place(hero_combatant)

    monster_template = registry.get_monster(location.resident_template)
    monster_combatant = combatant_from_monster(
        monster_template, monster_pos, "enemies",
    )
    grid.place(monster_combatant)

    roller = Roller(seed=deployment.seed + world.clock.tick_number)
    encounter = Encounter.begin(
        grid, [hero_combatant, monster_combatant], roller,
    )

    we_id = f"enc_{uuid.uuid4().hex[:8]}"
    we = WorldEncounter(
        id=we_id,
        location_id=location.id,
        deployment_ids=[deployment.id],
        started_at_tick=world.clock.tick_number,
        engine_encounter=encounter,
        grid=grid,
    )
    we.engine_encounter.roller = roller  # type: ignore[attr-defined]
    # Persist participants on WE (the engine Encounter doesn't keep these).
    we._hero = hero_combatant            # type: ignore[attr-defined]
    we._monsters = [monster_combatant]   # type: ignore[attr-defined]
    we._roller = roller                  # type: ignore[attr-defined]
    we._behavior = _load_behavior_script(castle, deployment)  # type: ignore[attr-defined]
    # DSL v2 Phase 4: if the hero's behavior script has any reactive
    # rules (``react: aoo``, ``react: brace``, ``react: cleave``,
    # ``sub: full_attack``), compile and register a picker on the
    # encounter so those rules fire when interrupts land. Active-turn
    # picking still flows through Interpreter.pick_turn → TurnIntent
    # below; only reactive interrupts route through the picker.
    if we._behavior is not None:  # type: ignore[attr-defined]
        from dnd.engine.actions import register_script_pickers
        register_script_pickers(hero_combatant, we._behavior, encounter)  # type: ignore[attr-defined]
    world.active_encounters[we_id] = we

    deployment.phase = PHASE_IN_COMBAT
    deployment.encounter_id = we_id
    deployment.append_event(
        world.clock.tick_number, "engage",
        {"location_id": location.id,
         "encounter_id": we_id,
         "hero_hp": hero_combatant.current_hp,
         "monster_id": monster_combatant.id,
         "monster_kind": location.resident_template,
         "monster_hp": monster_combatant.current_hp},
    )


def _load_behavior_script(
    castle: Castle, deployment: Deployment,
) -> BehaviorScript | None:
    """Look up the behavior script in the castle library and parse it.

    Returns ``None`` if the script ref isn't in the library — falls
    back to default_monster_intent for the hero too in that case
    (which is a sane "charge nearest enemy" fallback).
    """
    text = castle.library_behaviors.get(deployment.behavior_ref)
    if not text:
        return None
    try:
        return parse_script(text)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Encounter rounds
# ---------------------------------------------------------------------------


def _run_encounter_round(
    we: WorldEncounter, world: World, registry: ContentRegistry,
) -> None:
    """Run one PF1 round of an active encounter.

    Each combatant whose initiative falls in this round takes their
    turn. We do NOT use Encounter.advance_turn's wrap detection
    because we want exactly one full round per tick.
    """
    enc = we.engine_encounter
    if enc is None or enc.is_over():
        return
    grid = we.grid
    roller: Roller = we._roller       # type: ignore[attr-defined]
    behavior: BehaviorScript | None = we._behavior  # type: ignore[attr-defined]
    hero: Combatant = we._hero        # type: ignore[attr-defined]

    cur_tick = world.clock.tick_number
    n_initiative = len(enc.initiative)

    # Run exactly one turn per initiative slot to make one round.
    for _ in range(n_initiative):
        if enc.is_over():
            break
        actor = enc.current_actor()
        if actor is None:
            break
        if actor.current_hp <= -10 or "dead" in actor.conditions:
            enc.advance_turn()
            continue
        if actor.is_unconscious():
            enc.advance_turn()
            continue

        if actor.team == hero.team:
            # Hero's turn — use script if present, otherwise the same
            # default-aggressive AI as monsters.
            intent = None
            if behavior is not None:
                try:
                    intent = Interpreter(behavior).pick_turn(actor, enc, grid)
                except Exception:
                    intent = None
            if intent is None:
                intent = default_monster_intent(actor, enc, grid)
            result = execute_turn(actor, intent, enc, grid, roller)
        else:
            intent = default_monster_intent(actor, enc, grid)
            result = execute_turn(actor, intent, enc, grid, roller)

        # Append a per-actor turn event to the deployment(s).
        for d_id in we.deployment_ids:
            d = world.deployments.get(d_id)
            if d is not None:
                d.append_event(cur_tick, "round", {
                    "actor_id": actor.id,
                    "actor_name": actor.name,
                    "events": [
                        {"kind": ev.kind, "detail": ev.detail}
                        for ev in result.events
                    ],
                    "actor_hp": actor.current_hp,
                })
        enc.advance_turn()


def _finalize_encounter(we: WorldEncounter, world: World) -> None:
    """Clean up after a finished encounter: bank rewards, mark location,
    transition deployment(s) to RETURNING or DEAD."""
    cur_tick = world.clock.tick_number
    we.ended_at_tick = cur_tick
    enc = we.engine_encounter
    hero: Combatant = we._hero       # type: ignore[attr-defined]
    monsters: list[Combatant] = we._monsters  # type: ignore[attr-defined]

    hero_alive = hero.is_alive() and hero.current_hp > -10
    winner_team = enc.winner_team() if enc is not None else None

    for d_id in we.deployment_ids:
        d = world.deployments.get(d_id)
        if d is None:
            continue
        castle = world.castles.get(d.castle_id)
        if castle is None:
            continue
        hero_record = castle.get_hero(d.hero_id)
        if hero_record is None:
            continue

        if not hero_alive or winner_team != hero.team:
            # Hero died.
            castle.bury(hero_record.id, died_at_tick=cur_tick)
            d.phase = PHASE_DEAD
            d.completed_at_tick = cur_tick
            d.append_event(cur_tick, "death", {
                "encounter_id": we.id,
                "final_hp": hero.current_hp,
            })
            continue

        # Hero won. Carry combat-end HP back to the record.
        hero_record.current_hp = max(1, hero.current_hp)

        # Bank rewards. Renown = location.base_renown for v1.
        if we.location_id is not None:
            location = world.locations.get(we.location_id)
            if location is not None and location.state == LOC_ACTIVE:
                d.renown_earned += location.base_renown
                castle.credit(
                    location.base_renown, "deployment_reward",
                    tick=cur_tick, ref=d.id,
                )
                location.state = LOC_CLEARED
                location.cleared_at_tick = cur_tick
                location.cleared_by_castle = castle.id

        d.phase = PHASE_RETURNING
        d.append_event(cur_tick, "victory", {
            "encounter_id": we.id,
            "renown_earned": d.renown_earned,
            "hero_hp": hero.current_hp,
        })


def _finalize_deployment_complete(deployment: Deployment, world: World) -> None:
    """Hero made it home. Set hero back to AT_CASTLE; mark deployment done."""
    cur_tick = world.clock.tick_number
    castle = world.castles.get(deployment.castle_id)
    if castle is None:
        return
    hero = castle.get_hero(deployment.hero_id)
    if hero is not None:
        hero.status = HERO_AT_CASTLE
    deployment.phase = PHASE_COMPLETE
    deployment.completed_at_tick = cur_tick
    deployment.append_event(cur_tick, "complete", {
        "renown_earned": deployment.renown_earned,
    })


# ---------------------------------------------------------------------------
# Respawns
# ---------------------------------------------------------------------------


def _process_respawns(world: World) -> None:
    """Reactivate locations whose respawn delay has elapsed."""
    cur = world.clock.tick_number
    for loc in world.locations.values():
        if loc.state != LOC_CLEARED:
            continue
        if loc.cleared_at_tick is None:
            continue
        if cur - loc.cleared_at_tick >= loc.respawn_ticks:
            loc.state = LOC_ACTIVE
            loc.cleared_at_tick = None
            loc.cleared_by_castle = None
