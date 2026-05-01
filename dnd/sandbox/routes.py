"""HTTP routes for the sandbox layer.

Read handlers deref ``world.current_snapshot`` (or read directly with
the world's write lock for short critical sections). Write handlers
do all validation up front and then submit an ``Order`` to
``world.order_queue`` — they NEVER mutate world state directly.

The actual route registration onto ``server.py`` happens in that file
when sandbox routes are wired in. This module exposes plain functions
the server's ``@route`` decorator can register.
"""

from __future__ import annotations

import uuid

from dnd.engine.characters import (
    CharacterCreationError,
    CharacterRequest,
    create_character,
)
from dnd.engine.content import ContentNotFoundError
from dnd.engine.dice import Roller
from dnd.engine.dsl import DSLError, parse_script

from .castle import RENOWN_COST_L1_HERO, new_castle
from .deployment import (
    ORDER_CREATE_CASTLE,
    ORDER_SPAWN_HERO,
    ORDER_SUBMIT_DEPLOYMENT,
    ORDER_UPLOAD_BEHAVIOR,
    ORDER_UPLOAD_PLAN,
    new_order,
)
from .hero_record import HERO_AT_CASTLE, HeroRecord
from .world import World


# ---------------------------------------------------------------------------
# Castle lifecycle
# ---------------------------------------------------------------------------


def post_castle(world: World, body: dict) -> tuple[int, dict]:
    """POST /v1/castles → create castle.

    Returns ``(status, response_dict)``.
    """
    name = body.get("name")
    email = body.get("patron_email")
    home = body.get("home_position", [10, 10])
    if not isinstance(name, str) or not name.strip():
        return 400, {"error": "missing or empty 'name'"}
    if not isinstance(email, str) or "@" not in email:
        return 400, {"error": "missing or invalid 'patron_email'"}
    if (not isinstance(home, list) or len(home) != 2
            or not all(isinstance(x, int) for x in home)):
        return 400, {"error": "'home_position' must be [int, int]"}
    if not (0 <= home[0] < world.width and 0 <= home[1] < world.height):
        return 400, {"error": "'home_position' out of world bounds"}

    castle = new_castle(name, email, (home[0], home[1]))
    world.order_queue.submit(
        new_order(None, ORDER_CREATE_CASTLE, {"castle": castle}),
    )
    return 202, {
        "id": castle.id,
        "name": castle.name,
        "patron_email": castle.patron_email,
        "home_position": list(castle.home_position),
        "renown": castle.renown,
        "status": "pending",
    }


def get_castle(world: World, castle_id: str) -> tuple[int, dict]:
    """GET /v1/castles/{cid} → castle state."""
    with world.write_lock:
        castle = world.castles.get(castle_id)
        if castle is None:
            return 404, {"error": f"castle {castle_id!r} not found"}
        return 200, castle.to_dict()


# ---------------------------------------------------------------------------
# Library
# ---------------------------------------------------------------------------


def post_castle_behavior(
    world: World, castle_id: str, body: dict,
) -> tuple[int, dict]:
    """POST /v1/castles/{cid}/library/behaviors → upload script."""
    name = body.get("name")
    text = body.get("text")
    if not isinstance(name, str) or not name.strip():
        return 400, {"error": "missing 'name'"}
    if not isinstance(text, str) or not text.strip():
        return 400, {"error": "missing 'text'"}
    # Validate the script parses before queuing the order.
    try:
        parse_script(text)
    except DSLError as e:
        return 400, {"error": f"behavior script invalid: {e}"}

    if castle_id not in world.castles:
        return 404, {"error": f"castle {castle_id!r} not found"}

    world.order_queue.submit(new_order(castle_id, ORDER_UPLOAD_BEHAVIOR, {
        "name": name, "text": text,
    }))
    return 202, {"name": name, "status": "pending"}


def get_castle_behavior(
    world: World, castle_id: str, name: str,
) -> tuple[int, dict]:
    with world.write_lock:
        castle = world.castles.get(castle_id)
        if castle is None:
            return 404, {"error": f"castle {castle_id!r} not found"}
        text = castle.library_behaviors.get(name)
        if text is None:
            return 404, {"error": f"behavior {name!r} not in library"}
        return 200, {"name": name, "text": text}


def post_castle_plan(
    world: World, castle_id: str, body: dict,
) -> tuple[int, dict]:
    name = body.get("name")
    text = body.get("text")
    if not isinstance(name, str) or not name.strip():
        return 400, {"error": "missing 'name'"}
    if not isinstance(text, str) or not text.strip():
        return 400, {"error": "missing 'text'"}
    if castle_id not in world.castles:
        return 404, {"error": f"castle {castle_id!r} not found"}
    world.order_queue.submit(new_order(castle_id, ORDER_UPLOAD_PLAN, {
        "name": name, "text": text,
    }))
    return 202, {"name": name, "status": "pending"}


def get_castle_plan(
    world: World, castle_id: str, name: str,
) -> tuple[int, dict]:
    with world.write_lock:
        castle = world.castles.get(castle_id)
        if castle is None:
            return 404, {"error": f"castle {castle_id!r} not found"}
        text = castle.library_plans.get(name)
        if text is None:
            return 404, {"error": f"plan {name!r} not in library"}
        return 200, {"name": name, "text": text}


# ---------------------------------------------------------------------------
# Heroes
# ---------------------------------------------------------------------------


def post_hero(
    world: World, castle_id: str, body: dict, registry,
) -> tuple[int, dict]:
    """POST /v1/castles/{cid}/heroes → spawn a hero.

    Validates everything synchronously (renown, character creation,
    behavior_ref present in library). Charges renown via the queued
    order on the next tick.
    """
    behavior_ref = body.get("behavior_ref")
    plan_ref = body.get("plan_ref")
    if not isinstance(behavior_ref, str) or not behavior_ref.strip():
        return 400, {"error": "missing 'behavior_ref'"}

    with world.write_lock:
        castle = world.castles.get(castle_id)
        if castle is None:
            return 404, {"error": f"castle {castle_id!r} not found"}
        if behavior_ref not in castle.library_behaviors:
            return 400, {
                "error": f"behavior_ref {behavior_ref!r} not in library — "
                         f"upload it first",
            }
        if plan_ref is not None and plan_ref not in castle.library_plans:
            return 400, {
                "error": f"plan_ref {plan_ref!r} not in library",
            }
        if castle.renown < RENOWN_COST_L1_HERO:
            return 403, {
                "error": f"insufficient renown: need "
                         f"{RENOWN_COST_L1_HERO}, have {castle.renown}",
            }

    # Build the Character synchronously so any validation error returns
    # 400 right now, not after a tick.
    try:
        request = CharacterRequest.from_dict(body)
    except CharacterCreationError as e:
        return 400, {"error": str(e)}
    except (KeyError, TypeError, ValueError) as e:
        return 400, {"error": f"bad request: {e}"}
    try:
        character = create_character(
            request, registry, roller=Roller(seed=body.get("seed")),
        )
    except CharacterCreationError as e:
        return 422, {"error": str(e)}
    except ContentNotFoundError as e:
        return 404, {"error": str(e)}

    hero_id = f"hero_{uuid.uuid4().hex[:8]}"
    hero = HeroRecord(
        id=hero_id, name=character.name, character=character,
        behavior_ref=behavior_ref, plan_ref=plan_ref,
        status=HERO_AT_CASTLE,
    )
    world.order_queue.submit(new_order(castle_id, ORDER_SPAWN_HERO, {
        "hero": hero, "renown_cost": RENOWN_COST_L1_HERO,
    }))
    return 202, {
        "id": hero_id,
        "name": hero.name,
        "status": "pending",
        "behavior_ref": behavior_ref,
        "plan_ref": plan_ref,
    }


def list_heroes(world: World, castle_id: str) -> tuple[int, dict]:
    with world.write_lock:
        castle = world.castles.get(castle_id)
        if castle is None:
            return 404, {"error": f"castle {castle_id!r} not found"}
        return 200, {
            "roster": [h.to_dict() for h in castle.roster.values()],
            "graveyard": [h.to_dict() for h in castle.graveyard.values()],
        }


def get_hero(
    world: World, castle_id: str, hero_id: str,
) -> tuple[int, dict]:
    with world.write_lock:
        castle = world.castles.get(castle_id)
        if castle is None:
            return 404, {"error": f"castle {castle_id!r} not found"}
        hero = castle.get_hero(hero_id)
        if hero is None:
            return 404, {"error": f"hero {hero_id!r} not found"}
        return 200, hero.to_dict()


# ---------------------------------------------------------------------------
# Deployments
# ---------------------------------------------------------------------------


def post_deployment(
    world: World, castle_id: str, body: dict,
) -> tuple[int, dict]:
    hero_id = body.get("hero_id")
    location_id = body.get("destination_location_id")
    seed = body.get("seed")
    if not isinstance(hero_id, str):
        return 400, {"error": "missing 'hero_id'"}
    if not isinstance(location_id, str):
        return 400, {"error": "missing 'destination_location_id'"}
    if seed is not None and not isinstance(seed, int):
        return 400, {"error": "'seed' must be an integer if provided"}

    with world.write_lock:
        castle = world.castles.get(castle_id)
        if castle is None:
            return 404, {"error": f"castle {castle_id!r} not found"}
        hero = castle.roster.get(hero_id)
        if hero is None:
            return 404, {"error": f"hero {hero_id!r} not in roster"}
        if hero.status != HERO_AT_CASTLE:
            return 409, {"error": f"hero {hero_id!r} not available "
                                  f"(status={hero.status})"}
        location = world.locations.get(location_id)
        if location is None:
            return 404, {"error": f"location {location_id!r} not found"}
        behavior_ref = hero.behavior_ref
        plan_ref = hero.plan_ref

    deployment_id = f"deploy_{uuid.uuid4().hex[:8]}"
    world.order_queue.submit(new_order(castle_id, ORDER_SUBMIT_DEPLOYMENT, {
        "deployment_id": deployment_id,
        "hero_id": hero_id,
        "location_id": location_id,
        "behavior_ref": behavior_ref,
        "plan_ref": plan_ref,
        "seed": seed,
    }))
    return 202, {
        "id": deployment_id,
        "phase": "pending",
        "received_at_tick": world.clock.tick_number,
    }


def list_deployments(world: World, castle_id: str) -> tuple[int, dict]:
    with world.write_lock:
        if castle_id not in world.castles:
            return 404, {"error": f"castle {castle_id!r} not found"}
        out = [
            d.to_dict() for d in world.deployments.values()
            if d.castle_id == castle_id
        ]
        return 200, {"deployments": out}


def get_deployment(
    world: World, castle_id: str, deployment_id: str,
    *, since_tick: int | None = None,
) -> tuple[int, dict]:
    """GET /v1/castles/{cid}/deployments/{did}?since_tick=N

    With ``since_tick``, returns only events with tick > since_tick.
    Without it, returns the full deployment dict.
    """
    with world.write_lock:
        if castle_id not in world.castles:
            return 404, {"error": f"castle {castle_id!r} not found"}
        d = world.deployments.get(deployment_id)
        if d is None:
            return 404, {"error": f"deployment {deployment_id!r} not found"}
        if d.castle_id != castle_id:
            return 404, {"error": "deployment not in this castle"}
        full = d.to_dict()
        if since_tick is not None:
            full["events"] = [
                e for e in full["events"] if e["tick"] > since_tick
            ]
        full["current_tick"] = world.clock.tick_number
        return 200, full


# ---------------------------------------------------------------------------
# World
# ---------------------------------------------------------------------------


def get_world(world: World) -> tuple[int, dict]:
    """GET /v1/world → snapshot of the live world."""
    return 200, world.current_snapshot
