"""apply_order(order, world) — the only legal entry point for state mutation.

The tick worker drains ``world.order_queue`` at the top of every tick
and feeds each ``Order`` here. HTTP routes never call this directly;
they validate input and ``world.order_queue.submit(order)``.

Each handler:

- mutates the in-memory ``World`` directly (it's running on the tick
  thread, with the write lock held);
- appends an entry to the relevant deployment's event log when
  appropriate;
- never returns a value — failure modes either set an error event on
  the related deployment or are silently dropped (validation lives in
  the HTTP layer; an order arriving here is presumed valid).
"""

from __future__ import annotations

from .castle import RENOWN_COST_L1_HERO
from .deployment import (
    ORDER_CREATE_CASTLE,
    ORDER_SPAWN_HERO,
    ORDER_SUBMIT_DEPLOYMENT,
    ORDER_UPLOAD_BEHAVIOR,
    ORDER_UPLOAD_PLAN,
    PHASE_TRAVELING_OUT,
    Deployment,
    Order,
)
from .hero_record import HERO_AT_CASTLE, HERO_DEPLOYED, HeroRecord
from .world import LOC_ACTIVE, World


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def apply_order(order: Order, world: World) -> None:
    """Apply an order to the world. Sole mutation entry point.

    Records ``accepted_at_tick`` on the order so replays can reproduce
    the exact tick at which the change took effect.
    """
    order.accepted_at_tick = world.clock.tick_number

    if order.kind == ORDER_CREATE_CASTLE:
        _apply_create_castle(order, world)
    elif order.kind == ORDER_SPAWN_HERO:
        _apply_spawn_hero(order, world)
    elif order.kind == ORDER_SUBMIT_DEPLOYMENT:
        _apply_submit_deployment(order, world)
    elif order.kind == ORDER_UPLOAD_BEHAVIOR:
        _apply_upload_behavior(order, world)
    elif order.kind == ORDER_UPLOAD_PLAN:
        _apply_upload_plan(order, world)
    else:
        # Should be unreachable; Order.__post_init__ validates kinds.
        raise ValueError(f"unhandled order kind {order.kind!r}")


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


def _apply_create_castle(order: Order, world: World) -> None:
    """Create a new castle. Payload carries the constructed Castle."""
    castle = order.payload["castle"]
    if castle.id in world.castles:
        return  # idempotent: already created
    world.castles[castle.id] = castle


def _apply_spawn_hero(order: Order, world: World) -> None:
    """Add a HeroRecord to a castle's roster, charging the renown cost."""
    castle = world.castles.get(order.castle_id) if order.castle_id else None
    if castle is None:
        return
    hero: HeroRecord = order.payload["hero"]
    cost: int = int(order.payload.get("renown_cost", RENOWN_COST_L1_HERO))
    # Re-check renown at apply time (HTTP-time check could be stale by
    # the time we drain). If insufficient, drop the order silently —
    # the order_id stub the patron got back will simply never produce
    # a hero.
    if castle.renown < cost:
        return
    if hero.id in castle.roster or hero.id in castle.graveyard:
        return  # idempotent
    castle.debit(
        cost, "spawn_hero",
        tick=world.clock.tick_number, ref=hero.id,
    )
    hero.status = HERO_AT_CASTLE
    castle.add_hero(hero)


def _apply_submit_deployment(order: Order, world: World) -> None:
    """Promote a pending deployment to TRAVELING_OUT and bind it to the hero."""
    castle = world.castles.get(order.castle_id) if order.castle_id else None
    if castle is None:
        return
    deployment_id: str = order.payload["deployment_id"]
    hero_id: str = order.payload["hero_id"]
    location_id: str = order.payload["location_id"]
    behavior_ref: str = order.payload["behavior_ref"]
    plan_ref = order.payload.get("plan_ref")
    seed: int = int(order.payload.get("seed") or _stable_seed(deployment_id))

    # Re-check world state at apply time.
    hero = castle.roster.get(hero_id)
    if hero is None or hero.status != HERO_AT_CASTLE:
        return
    location = world.locations.get(location_id)
    if location is None or location.state != LOC_ACTIVE:
        return

    path = _compute_path(castle.home_position, location.position, world)
    if not path:
        return  # no route; drop silently for v1

    deployment = Deployment(
        id=deployment_id,
        castle_id=castle.id,
        hero_id=hero.id,
        destination_location_id=location.id,
        behavior_ref=behavior_ref,
        plan_ref=plan_ref,
        submitted_at_tick=world.clock.tick_number,
        seed=seed,
        phase=PHASE_TRAVELING_OUT,
        path=path,
        path_index=0,
    )
    deployment.append_event(
        world.clock.tick_number, "depart",
        {"from": list(castle.home_position),
         "to": list(location.position),
         "path_length": len(path)},
    )
    world.deployments[deployment.id] = deployment
    hero.status = HERO_DEPLOYED
    hero.deployment_ids.append(deployment.id)


def _apply_upload_behavior(order: Order, world: World) -> None:
    castle = world.castles.get(order.castle_id) if order.castle_id else None
    if castle is None:
        return
    name: str = order.payload["name"]
    text: str = order.payload["text"]
    castle.library_behaviors[name] = text


def _apply_upload_plan(order: Order, world: World) -> None:
    castle = world.castles.get(order.castle_id) if order.castle_id else None
    if castle is None:
        return
    name: str = order.payload["name"]
    text: str = order.payload["text"]
    castle.library_plans[name] = text


# ---------------------------------------------------------------------------
# Pathfinding
# ---------------------------------------------------------------------------


def _compute_path(
    start: tuple[int, int],
    goal: tuple[int, int],
    world: World,
) -> list[tuple[int, int]]:
    """Generate a path from ``start`` to ``goal`` on the world grid.

    Greedy step-toward-goal, picking the passable 8-neighbor with
    the smallest Chebyshev distance to ``goal``. If the next chosen
    cell isn't strictly closer, we're stuck — return what we have
    plus the goal (HTTP layer should have rejected this; if we're
    still stuck at apply time, the deployment will reach the end of
    its known path and the tick worker will treat that as arrival).

    For v1 the world is sparse and this works. A* lands later if we
    need it.
    """
    if start == goal:
        return [start]

    cur = start
    path: list[tuple[int, int]] = [cur]
    visited = {cur}
    max_steps = world.width * world.height  # absolute upper bound
    for _ in range(max_steps):
        if cur == goal:
            break
        best: tuple[int, int] | None = None
        best_dist = _chebyshev(cur, goal)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = cur[0] + dx, cur[1] + dy
                if not (0 <= nx < world.width and 0 <= ny < world.height):
                    continue
                if (nx, ny) in world.impassable_cells:
                    continue
                if (nx, ny) in visited:
                    continue
                d = _chebyshev((nx, ny), goal)
                if d < best_dist:
                    best_dist = d
                    best = (nx, ny)
        if best is None:
            break
        path.append(best)
        visited.add(best)
        cur = best
    if cur != goal:
        # Couldn't reach; v1 just declares the path ends where we got.
        # Future: A*, terrain costs, etc.
        pass
    return path


def _chebyshev(a: tuple[int, int], b: tuple[int, int]) -> int:
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------


def _stable_seed(deployment_id: str) -> int:
    """Deterministic seed derived from a deployment id (31-bit hash)."""
    n = 0
    for ch in deployment_id:
        n = (n * 131 + ord(ch)) & 0x7FFFFFFF
    return n or 1
