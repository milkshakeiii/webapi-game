# Sandbox Layer Design (v1)

**Status:** draft for review. Lives alongside `DESIGN_PROPOSAL.md` (the
overall game design); this document is the concrete plan for the **Phase
3** sandbox layer that turns the existing combat engine into a playable
game-shaped thing.

The combat/character/spell/feat engine is built and tested (389 tests
green). What's missing: castles, the world map, deployments, persistence,
the HTTP surface that lets a patron run their castle. That's what this
doc designs.

---

## Scope of v1

In, by intent:

- **One castle per patron**, persistent across sessions.
- **Single-hero deployments**: spawn a hero, attach a behavior script,
  send to a destination, hero acts on its own, returns or dies.
- **A small flat 2D world** with hand-authored locations and one castle
  slot per patron.
- **Renown ledger**: earn from kills/loot/objectives, spend to spawn
  heroes, with history kept.
- **Persistence to JSON-on-disk** per castle and one shared world file.
- **HTTP surface** for the loop: spawn → deploy → poll → bank.

Out, deferred to later phases:

- Multi-hero parties (Phase 5).
- Crafting & gathering (Phase 4).
- Monster dens & monster commanding (Phase 7).
- PvP-flavored interactions, contested locations (Phase 8+).
- Procedural world generation (we use hand-authored locations for v1).
- Conditional level-up plans, plan refinement post-mortem.
- Web UI of any kind. The deliverable is an HTTP API.

What this v1 sandbox **must let a patron do**, end to end:

1. Create an account / castle.
2. Spawn a level-1 hero with a class, a behavior script, and a
   level-up plan (already validated by the engine).
3. Submit a deployment to a known location.
4. Get back a deployment ID and an estimated return time.
5. Poll until the deployment finishes; receive the full PF1 trace.
6. See renown banked, hero state updated (alive at castle / dead).
7. Spawn the next hero. Repeat.

---

## Big Shape Decisions

These are the load-bearing choices. Each one has a **decision** and a
**why**, plus a flag for whether it deviates from `DESIGN_PROPOSAL.md`.

### 1. Time Model: continuous tick worker (EVE-style)

**Decision:** The server runs a **background tick worker** that
advances the world by one PF1 round every `TICK_INTERVAL` real
seconds. Default `TICK_INTERVAL = 6` seconds (1:1 with PF1's
6-second round, matching `DESIGN_PROPOSAL.md`); server-tunable for
test environments.

The world has a single global clock:

```python
class WorldClock:
    started_at: datetime         # when the world first booted
    tick_number: int             # = round number; monotonic
    tick_interval_s: float       # default 6.0
```

`tick_number` IS the PF1 round number across the whole world. There is
one timeline; every hero, every encounter, every location respawn is
indexed by it.

**The tick loop** (sole writer of world state):

```python
def tick(world, registry, rng):
    # 1. Drain the order queue: requests submitted since the last tick.
    for order in world.order_queue.drain():
        apply_order(order, world)        # validates + mutates world
    # 2. For every hero with an "intent" (active deployment), advance
    #    them one round of action toward fulfilling it.
    for hero in deployed_heroes(world):
        advance_hero_one_round(hero, world, rng)
    # 3. Detect new engagements: hostile pairs newly within engagement
    #    range that weren't in combat last tick.
    for new_engagement in detect_new_engagements(world):
        materialize_encounter(world, new_engagement)
    # 4. For every active encounter, run one PF1 round.
    for enc in world.active_encounters:
        run_one_round(enc, registry, rng)
    # 5. Resolve completions (heroes who reached return target, dead
    #    heroes' bodies, location respawns).
    resolve_completions(world)
    # 6. Atomically publish the new world snapshot for HTTP readers,
    #    then persist to disk.
    world.publish_snapshot()
    save_world(world)
```

**Concurrency model: tick worker is the sole writer.**

- HTTP **write handlers** (spawn hero, submit deployment, upload
  script) do not mutate world state. They construct an `Order`,
  enqueue it on `world.order_queue` (a thread-safe FIFO), and return
  immediately with a stub response. The patron's order is `phase:
  pending` until the next tick applies it (≤ `TICK_INTERVAL` of
  latency).
- HTTP **read handlers** dereference `world.current_snapshot` — a
  pointer the tick worker swaps atomically at the end of every tick.
  Readers never observe partial state and never block writers.
- The tick worker holds an exclusive write lock around its body but
  doesn't contend with HTTP requests, because HTTP threads are doing
  queue-appends and snapshot-derefs, not state mutation.

This gives:

1. **Determinism for replay.** An order's `accepted_at_tick` is the
   tick at which the queue drain absorbed it. Replays are
   `(initial state, ordered list of (order, accepted_at_tick),
   RNG seed)` → bit-identical world state at any later tick.
2. **No HTTP request blocks on a long tick body.** The worst case is
   a sub-microsecond queue append.
3. **One concurrency story** — the only place we worry about
   correctness is the tick body itself, which is single-threaded.

For v1 single-process is fine. Tick body for an empty world is well
under a millisecond.

**What the patron sees:** `GET /v1/castles/{cid}/deployments/{did}`
returns the trace as it accumulates, tick by tick. The trace is an
append-only event list keyed to `tick_number`. Polling every few
seconds gives a near-live feed; faster polling is allowed but
expensive.

**Why this and not pre-simulated deployments:** pre-simulated
deployments make cross-patron interactions feel synthetic. Henry's
vision explicitly includes two patrons' heroes converging on the same
location, fighting *each other* or fighting alongside each other in
real shared time. That's only possible with one shared clock.
The engineering cost is real (~doubles v1 work compared to the
pre-sim shortcut) but the design is load-bearing.

### 2. World Representation: integer grid, single layer

**Decision:** The world is one big integer grid (e.g., 200×200 cells of
5 ft each = a 1000 ft × 1000 ft world). Same units as the combat grid.
There is no second coordinate system.

- Hero positions: integer cell on the world grid.
- Combat: when an encounter triggers, we use a *window* of the world
  grid centered on the encounter location, plus a `Grid` object built
  from that window. Combat's existing `Grid` API stays as-is; we just
  initialize it from world cells around the encounter.
- Wilderness / impassable cells (walls, water, cliffs) live in the
  world grid.
- Locations are not extra structures; they're decorations on a
  designated world cell ("there's a goblin camp at (37, 45)").

**Why:** Reusing the integer grid we already have removes a whole
coordinate-conversion layer. PF1's combat math (range increments, AoO
threats, charge distance) is grid-native; making the world grid-native
matches.

**Why not a 2-tier "world coords + combat grid" system:** more code, more
surfaces to test, no v1 benefit. We'd need it eventually if scenes get
arbitrarily-rotated or if we render at non-grid resolutions, neither of
which is in scope.

### 3. The Deployment is a Standing Order, Advanced Tick by Tick

**Decision:** A `Deployment` is **not** an atomic simulation; it's a
**standing order** attached to a hero, processed one PF1 round per
tick. The hero is a unit on the world, advancing toward fulfilling its
order. Each tick the engine asks "what does this hero do this round?"
and runs one round of behavior.

A deployment carries a small state machine:

```
TRAVELING_OUT → AT_DESTINATION → IN_COMBAT → RETURNING → COMPLETE
                        ↘                       ↗
                         RETREATING (if hero broke off)
                        ↘
                         DEAD (terminal)
```

Each tick, depending on phase:

- `TRAVELING_OUT` / `RETURNING`: hero takes one round of movement
  toward its current waypoint. PF1 movement: a speed-30 character
  covers 6 grid cells per round (30 ft / 5 ft per cell). Wilderness
  biome may impose a multiplier later (deferred).
- `AT_DESTINATION`: hero engages the location's resident creatures
  (or another patron's hero) — transitions to `IN_COMBAT` next tick.
- `IN_COMBAT`: hero is part of an `Encounter`; one PF1 round runs
  per tick until termination.
- `RETREATING`: hero moves back toward castle; flagged so they don't
  re-engage on the way home.
- `COMPLETE`: rewards banked, hero status set to `at_castle`. No
  further ticks process this deployment.

The "atomic simulation" function from the prior design becomes a
sequence of small per-tick operations:

```python
def advance_deployment_one_round(deployment, world, registry, rng):
    if deployment.phase == TRAVELING_OUT:
        step_unit_one_round(deployment.hero, deployment.path, world)
        if reached(deployment.hero, deployment.destination):
            deployment.phase = AT_DESTINATION
    elif deployment.phase == IN_COMBAT:
        run_one_round(deployment.encounter, registry, rng)
        ...
```

The patron's behavior script is consulted **on the hero's initiative
turn within the encounter**, exactly the same way `turn_executor`
already uses it for test scenarios. The engine plumbing doesn't
change; the only new piece is "what intent does this hero have right
now" feeding into "which behavior matches".

Determinism still holds: a deployment + the world's RNG seed for the
relevant ticks → reproducible outcome. Replays use the recorded tick
sequence and the original seeds.

### 4. Concurrency: tick worker is the sole writer

**Decision:** Because all simulation runs in one tick worker, there's
only one timeline and no merge-diff problem. State changes are
immediate and observed by everyone next tick.

The split is strict:

- **HTTP read handlers** dereference `world.current_snapshot` and
  serialize from it. Lock-free.
- **HTTP write handlers** construct an `Order`, append to
  `world.order_queue` (thread-safe FIFO), and return. The handler
  never touches world state directly.
- **Tick worker** drains the queue at the top of each tick, mutates
  world state under an internal write lock, then publishes a fresh
  snapshot for readers.

This means a write handler returns *before* the order has taken
effect. The response body has just enough to let the patron poll —
e.g. `POST /v1/castles/{cid}/deployments` returns the new
`deployment_id` immediately; that deployment exists in `phase:
pending` until the next tick promotes it. From the patron's POV this
is invisible at the prod tick interval (6s) and a non-event at the
test tick interval (50ms).

- Two patrons' heroes converging on the same goblin camp on the
  same tick: both arrive together. The encounter materializes with
  three teams (patron A's hero, patron B's hero, the goblins) — or
  two if A and B are on the same side. Behavior scripts decide
  whether they help each other or treat each other as hostile.
- One hero arriving slightly later (next tick): joins the in-progress
  encounter via the existing combatant-add path or arrives to find
  an empty camp.
- Race for a resource (clear count, loot pickup) is settled by
  initiative within the actual encounter — no synthetic
  tie-breaking by submission time.

**Hostile-hero detection:** patron A's hero counts as hostile to
patron B's hero only if their patrons are in declared conflict (a
later phase). For v1 — see "What I'm NOT Building" — different
patrons' heroes are mutually-neutral; they can occupy the same
location without engaging. We materialize a shared encounter only
if at least one team contains hostile-to-everyone NPCs. This keeps
the v1 cut sane while preserving the architecture for the PvP
phase.

**Why a single lock is enough:** the tick body is short (every
deployed hero takes one round; every encounter takes one round of
combat math). Even with 50 heroes deployed, that's well under a
second per tick on a modern machine. HTTP handlers acquire the lock
between ticks, do their read/write, release. Patron-facing
operations are read-heavy (poll deployments) and trivially fast.

### 5. Persistence: JSON-on-disk, per-castle + shared world

**Decision:** All state lives under a `data/` directory at the project
root, organized as:

```
data/
  world.json                    # shared world map and location states
  castles/
    {castle_id}.json            # per-castle: roster, treasury, library, renown
  deployments/
    {deployment_id}.json        # one file per deployment, append-only result
  events/
    {YYYY-MM-DD}.jsonl          # daily append log of world events (for audit)
```

- Read on each request that needs the data. Write atomically via
  `os.replace` after a tempfile write.
- Single-process server; no cross-process locking is needed in v1.
- A simple `lock.json` next to each file documents the in-flight
  request count for human debugging only.

**Why JSON-on-disk:** the proposal already accepts this. It's enough
for v1 traffic levels (single-digit patrons, dozens of deployments).
Migration to SQLite is a future drop-in replacement.

**What we will write down to:** `Castle`, `World`, `Deployment`. NOT
`Hero` separately — heroes are nested inside castles. Deployments are
the only thing that benefits from being its own file (large traces,
write-once-then-read).

### 6. Out-of-scope tradeoff: hero death is forever, no Raise Dead in v1

**Decision:** When a hero dies, they're gone. The hero record moves to
the castle's graveyard with the deployment trace attached. No castle-
side Raise Dead at v1. (A *deployed* hero with the spell could
hypothetically raise an ally mid-deployment; this requires party
support so it's also out of scope until Phase 5.)

**Why:** Permadeath is what makes scripts matter. The proposal locks
this; I'm restating it because it's load-bearing for the data model.

---

## Data Model

The new dataclasses live in `dnd/sandbox/`. The engine layer is
untouched except for one or two integration points (see Integration
Points below).

### Castle

```python
@dataclass
class Castle:
    id: str                          # uuid
    name: str
    patron_email: str                # auth tie-in (out of scope but recorded)
    created_at: datetime
    home_position: tuple[int, int]   # cell on the world grid

    renown: int                      # current balance
    lifetime_renown: int             # all-time earned (informational)

    treasury_gold: int

    roster: list[HeroRecord]         # heroes currently at castle or out
    graveyard: list[HeroRecord]      # dead heroes, kept for history

    library_behaviors: dict[str, BehaviorScript]
    library_plans: dict[str, LevelUpPlan]

    renown_ledger: list[RenownEntry] # append-only history
```

### HeroRecord

A hero "record" is the persistent piece. The combat-time `Combatant` is
constructed from this on demand for each deployment.

```python
@dataclass
class HeroRecord:
    id: str
    name: str
    character: Character             # the engine's static character sheet
    behavior_ref: str                # name of a behavior script in the library
    plan_ref: str | None             # name of a level-up plan in the library
    status: HeroStatus               # AT_CASTLE | DEPLOYED | DEAD
    current_hp: int                  # carries between deployments
    current_xp: int
    deployments: list[str]           # deployment IDs, oldest first
    spawned_at: datetime
    died_at: datetime | None
```

### World

```python
@dataclass
class World:
    width: int
    height: int
    impassable_cells: set[tuple[int, int]]   # walls, deep water, cliffs
    locations: list[Location]
    revision: int                            # bumped on every WorldDiff merge
```

### Location

```python
@dataclass
class Location:
    id: str
    name: str
    position: tuple[int, int]
    kind: str                        # "lair" | "ruins" | "camp" | ...
    description: str
    resident_template: str           # references a content/encounters/*.json
    state: LocationState             # ACTIVE | CLEARED | RESPAWNING
    last_cleared_at: datetime | None
    cleared_by_castle: str | None
    base_renown: int                 # what clearing the location is worth
```

A location is "active" until cleared. While cleared, no encounter
materializes there. After a respawn cooldown (proposal says "every few
in-game hours"; we'll probably just track in deployment-count or a
simple wall-clock TTL), it returns to active.

### Deployment

```python
@dataclass
class Deployment:
    id: str
    castle_id: str
    hero_id: str
    destination_location_id: str
    behavior_ref: str
    plan_ref: str | None

    submitted_at_tick: int           # world tick at which order applied
    completed_at_tick: int | None    # filled when phase reaches COMPLETE / DEAD

    phase: DeploymentPhase           # see state machine in section 3
    path: list[tuple[int, int]]      # current pathing waypoints
    encounter_id: str | None         # set while phase == IN_COMBAT

    # Append-only event log. Each entry is keyed to a tick number so
    # patrons polling can stream just the new ones.
    events: list[DeploymentEvent]

    # Running totals updated as the deployment progresses.
    renown_earned: int
    gold_earned: int
    items_earned: list[str]

    seed: int                        # determinism anchor used by encounters
                                     # spawned by this deployment
```

### DeploymentEvent

```python
@dataclass
class DeploymentEvent:
    tick: int                        # world tick number
    kind: str                        # "depart" | "step" | "engage" | "round" | "loot" | "return" | "death"
    detail: dict                     # kind-specific payload (positions, attack outcomes, …)
```

The event list is the patron's window into the deployment. It grows
tick by tick. There is no separate "result object" — when phase
becomes `COMPLETE` or `DEAD`, the final tally is the sum of all
events plus the hero's final HP.

### Order (the queued write)

Every state-mutating HTTP request becomes an `Order` posted to the
tick worker. Orders carry the validated request data, the originating
castle, the timestamp the request arrived, and (after the worker
drains them) the tick at which they took effect.

```python
@dataclass
class Order:
    id: str                          # uuid; doubles as the response stub key
    castle_id: str
    kind: str                        # "spawn_hero" | "submit_deployment" | "upload_behavior" | ...
    payload: dict                    # kind-specific validated data
    received_at: datetime            # wall-clock arrival
    accepted_at_tick: int | None     # filled when worker drains the queue
```

For each `kind`, the order's `payload` is the request body after
schema and content-engine validation (e.g., a `spawn_hero` order's
payload includes a fully-formed `Character` produced by
`create_character`, so the worker doesn't re-parse content). HTTP
handlers do all the *validation* work; the worker does all the
*mutation* work. Validation failures return `400` synchronously
before any order is enqueued.

### Encounter (sandbox-side wrapper)

The combat engine has its own `Encounter` class. The sandbox keeps a
thin wrapper that ties an in-progress encounter to its location and
participating deployments:

```python
@dataclass
class WorldEncounter:
    id: str
    location_id: str | None            # None for ad-hoc field battles
    deployment_ids: list[str]          # deployments whose heroes are in this fight
    engine_encounter: Encounter        # the combat engine's encounter object
    started_at_tick: int
    ended_at_tick: int | None
```

The tick worker maps `tick → run one round of every WorldEncounter`,
appends results to the relevant deployments' event lists.

---

## Simulation Pipeline

The pipeline is the **tick loop** introduced in the Time Model section.
Here it is at the next level of detail:

```python
def tick(world, registry):
    with world.lock:
        world.clock.tick_number += 1
        rng = world.rng_for_tick(world.clock.tick_number)

        # 1. Drain the orders queue: deployments submitted between ticks.
        for order in world.pending_orders.drain():
            accept_order(order, world)

        # 2. Per-deployment one-round advancement (movement, phase change).
        for d in world.active_deployments():
            advance_deployment_one_round(d, world, rng)

        # 3. Detect new engagements among units that just moved.
        for engagement in detect_new_engagements(world):
            we = materialize_world_encounter(engagement, world, rng)
            world.active_encounters[we.id] = we

        # 4. Run one PF1 round of every active encounter.
        for we in list(world.active_encounters.values()):
            run_one_round_of_encounter(we, world, registry, rng)
            if we.engine_encounter.is_over():
                finalize_encounter(we, world)

        # 5. Resolve completions & deaths.
        for d in world.active_deployments():
            if d.phase == COMPLETE or d.phase == DEAD:
                finalize_deployment(d, world)

        # 6. Maintenance: respawns, ledger entries, etc.
        process_respawns(world)

        # 7. Persist.
        save_world(world)
```

Step 2's `advance_deployment_one_round` is the only place hero-level
state evolves outside of combat. For v1:

- `TRAVELING_OUT` / `RETURNING`: move along path by
  `(speed // 5)` cells per tick. Pre-computed path; recompute only if
  blocked.
- `AT_DESTINATION`: transition to `IN_COMBAT` if hostiles are present;
  otherwise transition to `RETURNING` (empty location).
- `IN_COMBAT`: nothing to do here at the deployment layer; step 4
  drives this.
- `RETREATING`: same as `RETURNING` but flagged so that re-engagement
  detection skips this hero on the way home.

### Travel encounters (deferred)

For v1, the only encounters are at locations. Wilderness travel
encounters (random ambushes en route) are explicitly deferred — see
the Deferred Scope tracker below.

### Combat is the existing engine

Inside `run_one_round_of_encounter`, we call into the existing
`turn_executor` for every combatant whose initiative is on this round.
The engine doesn't know it's part of a real-time tick — it just runs
one round of the encounter. The sandbox owns the "do one round per
tick" pacing.

---

## HTTP Surface (v1)

Endpoints, scoped to v1 only. Header conventions and auth are stub
(an `X-Castle-Id` header for dev; replace with real auth later).

```
# Castle lifecycle
POST   /v1/castles                 # create castle (idempotent on patron_email)
GET    /v1/castles/{cid}           # full castle state
PATCH  /v1/castles/{cid}           # rename, change settings

# Library
POST   /v1/castles/{cid}/library/behaviors    # upload a behavior script
GET    /v1/castles/{cid}/library/behaviors/{name}
POST   /v1/castles/{cid}/library/plans
GET    /v1/castles/{cid}/library/plans/{name}

# Heroes
POST   /v1/castles/{cid}/heroes    # spawn (cost: renown)
GET    /v1/castles/{cid}/heroes
GET    /v1/castles/{cid}/heroes/{hid}

# Deployments
POST   /v1/castles/{cid}/deployments
GET    /v1/castles/{cid}/deployments
GET    /v1/castles/{cid}/deployments/{did}    # status + (partial) trace
GET    /v1/castles/{cid}/deployments/{did}/log

# World (read-only)
GET    /v1/world                                # map + active locations
GET    /v1/world/locations/{lid}                # one location
```

All existing `/v1/content/*` routes stay where they are.

### Request/response shapes

```json
// POST /v1/castles
{
  "name": "Hill of the Hawk",
  "patron_email": "henry@example.com"
}
// → 201
{
  "id": "castle_a1b2c3",
  "name": "Hill of the Hawk",
  "renown": 100,
  "home_position": [10, 10],
  ...
}

// POST /v1/castles/{cid}/heroes
{
  "name": "Edric",
  "race": "human",
  "class": "fighter",
  "alignment": "lawful_good",
  "ability_scores": { "method": "point_buy_20", "scores": {...} },
  "feats": ["power_attack", "weapon_focus"],
  "skill_ranks": {"climb": 1, "swim": 1},
  "behavior_ref": "doctrines/melee_aggressive",
  "plan_ref": "plans/two_handed_hurt",
  "free_ability_choice": "str",
  "class_choices": {"fighter_bonus_feat": "cleave"},
  "bonus_languages": []
}
// → 201
{
  "id": "hero_xyz",
  "name": "Edric",
  "status": "at_castle",
  "current_hp": 12,
  ...
}

// POST /v1/castles/{cid}/deployments
{
  "hero_id": "hero_xyz",
  "destination_location_id": "loc_goblin_camp_north",
  "seed": 42                                // optional; server picks if omitted
}
// → 202 (immediately, before the order is processed)
{
  "id": "deploy_abc123",
  "phase": "pending",                       // becomes "traveling_out" on next tick
  "order_id": "ord_q9z7",
  "received_at_tick": 1842
}

// GET /v1/castles/{cid}/deployments/{did}?since_tick=1842
// → returns events whose tick > since_tick. Patron polls with the
// last tick they've seen to get only the new tail.
{
  "id": "deploy_abc123",
  "phase": "in_combat",
  "current_tick": 1851,
  "events": [
    {"tick": 1842, "kind": "depart", "detail": {"from": [10, 10]}},
    {"tick": 1843, "kind": "step",   "detail": {"to":   [11, 11]}},
    ...
    {"tick": 1850, "kind": "engage", "detail": {"location": "loc_goblin_camp_north", "encounter_id": "enc_123"}},
    {"tick": 1851, "kind": "round",  "detail": {"round": 1, "log": [...]}}
  ]
}

// GET /v1/castles/{cid}/deployments/{did}  (after phase = complete)
{
  "id": "deploy_abc123",
  "phase": "complete",
  "completed_at_tick": 1872,
  "renown_earned": 50,
  "gold_earned": 12,
  "items_earned": [],
  "hero_alive": true,
  "hero_final_hp": 7,
  "events": [ ... full event log ... ]
}

// GET /v1/world
// Snapshot of the live world. Includes the current tick number so the
// client knows how to interpret `since_tick` queries.
{
  "tick": 1851,
  "tick_interval_s": 6.0,
  "width": 200,
  "height": 200,
  "locations": [
    {"id": "loc_goblin_camp_north", "name": "Goblin Camp", "position": [37, 45], "state": "active"},
    ...
  ]
}
```

### Error shapes

`400` for malformed input (unknown class, invalid ability scores).
`403` for renown insufficient. `404` for missing castle/hero/location.
`409` if a deployment references a hero who's currently deployed.

---

## Integration Points with the Engine

Almost everything in the engine layer is reusable as-is. The few
changes needed:

1. **`Combatant.from_hero_record(record, registry)`** — a factory
   that builds a Combatant from a `HeroRecord` (so deployments don't
   re-create characters from scratch each time). Sits in
   `combatant.py` next to the existing factories.

2. **Behavior script library** — current `dsl.parse_script` parses
   from a string or file. The library API needs to wrap that with
   storage, but the parser doesn't change.

3. **Encounter trace serialization** — already in
   `TurnResult.to_dict`. We just collect trace events into the
   `DeploymentResult.encounter_traces` list.

4. **Default monster AI** — already exists as `default_monster_intent`.
   Deployment encounters use it for the resident creatures unless the
   location specifies a behavior script (out of scope for v1; all
   monsters use the default AI).

5. **No changes to the modifier system, no changes to combat math, no
   changes to characters/leveling.** The sandbox layer sits cleanly
   on top.

---

## File Layout for the Sandbox Code

```
dnd/sandbox/
  __init__.py
  castle.py            # Castle dataclass + persistence
  hero_record.py       # HeroRecord dataclass + factory
  world.py             # World, Location dataclasses, persistence
  deployment.py        # Deployment, DeploymentResult, WorldDiff
  simulation.py        # run_deployment(...) — the pipeline
  storage.py           # JSON-on-disk read/write helpers
  routes.py            # HTTP routes for the sandbox endpoints
```

`server.py` imports `routes.py` to register the new endpoints alongside
the existing content/character routes.

`tests/test_sandbox_*.py` for new tests; integration test runs through
the full HTTP pipeline.

---

## Deferred Scope Tracker

This is the running list of features cut from v1 — what's deferred,
where it lands, and what's needed to build it. Henry asked that we
keep this explicit and not silently drop anything; this section is the
canonical record. **Update this list whenever scope shifts.**

| Feature | Promised phase | Status | Notes |
|---|---|---|---|
| Multi-hero parties | Phase 5 | deferred | Needs DSL extensions for party roles, cross-hero conditions, signal mechanism. Engine support already partially in place via `enemy.*` / `ally.*` resolvers. |
| Crafting (PF1 craft rules) | Phase 4 | deferred | Self-contained subsystem: recipe content, gather→craft→equip pipeline, gold/time/reagent accounting. Item content already exists. |
| Monster dens | Phase 7 | deferred | Requires patron-built world structures, periodic renown income, den-vs-deployment encounter generation. Diplomacy/Intimidate/charm hooks needed first. |
| Direct PvP (cross-patron hostility) | Phase 8+ | deferred | Architecture supports it (mutual-neutral default, can flip to hostile per patron-pair). Needs explicit conflict-declaration endpoint and renown-stake rules. |
| Procedural world generation | Phase 8+ | deferred | Hand-authored locations are faster for v1. Add a generator only when content scaling demands it. |
| Conditional level-up plans (branches) | Phase 8+ | deferred | Linear plans (current `LevelUpPlan`) cover the common case. Branches need an `if/then/else` extension to plan parsing. |
| Wilderness travel encounters | Phase 4 sub | deferred | Needs encounter tables tied to biome + travel-leg length. Architecture-compatible; just no content yet. |
| Hero raise-dead at castle | Phase 8+ | deferred | Permadeath is a v1 design choice. May relax at very-high renown later. |
| Patron espionage / map intel | Phase 8+ | deferred | Per-patron "known map" view. v1: every patron sees the full world. |
| Stockpile / equipment lifecycle (carryover between deployments) | Phase 4 | deferred | v1 hero carries equipment they were spawned with; lost on death. No castle-side stockpile or re-equip. |
| Web UI / visualization | Phase 8+ | deferred | API only for v1. Patrons curl/script their way around. |
| SQLite migration from JSON-on-disk | when needed | deferred | JSON-on-disk works at single-digit-patron scale. Switch when read latency or write contention is a real problem. |

If a v1 deliverable would be empty without one of these, pull it in
and update this table. The rule is "small but complete loop", not
"complete but tiny demo."

---

## Defaults Locked

All previously-open questions have been resolved with these defaults
(easy to revisit later — none of them are architecturally load-bearing).

| # | Setting | Value |
|---|---|---|
| 1 | `TICK_INTERVAL` | 6.0s prod, 0.05s test; server CLI flag |
| 2 | World grid size | 200×200 cells (1000 ft × 1000 ft) |
| 3 | Renown costs | L1 hero = 10; new castle starts with 100 |
| 4 | Location respawn | 14,400 ticks after clearing (per-location overridable) |
| 5 | Auth | `X-Castle-Id` header stub |
| 6 | Location content layout | `dnd/content/locations/*.json` → baked into `data/world.json` on first boot |
| 7 | Cross-patron hostility | Mutually-neutral by default; shared encounter only via common NPC enemy |

---

## Implementation Order

With the tick worker as sole writer and an order queue between HTTP
and the worker, the build order is:

1. `dnd/sandbox/storage.py` — atomic JSON read/write helpers.
2. `dnd/sandbox/world.py` — `World`, `Location`, `WorldClock`
   dataclasses; the `current_snapshot` pointer + `publish_snapshot()`
   primitive; the `OrderQueue` (a thin wrapper around
   `queue.Queue` or a `deque` + `Lock` that exposes `submit()` and
   `drain()`). Hand-authored `data/world.json` with 3–5 locations.
3. `dnd/sandbox/hero_record.py` + a `Combatant.from_hero_record`
   factory in `combatant.py`.
4. `dnd/sandbox/castle.py` — castle dataclass, persistence, renown
   ledger.
5. `dnd/sandbox/deployment.py` — `Deployment` + `DeploymentEvent` +
   `WorldEncounter` + `Order` dataclasses.
6. `dnd/sandbox/orders.py` — the `apply_order(order, world)`
   dispatch: one handler per `kind` (`spawn_hero`,
   `submit_deployment`, `upload_behavior`, …). All mutation lives
   here; HTTP handlers never call this directly.
7. `dnd/sandbox/tick.py` — the tick loop (drain queue, advance
   deployments, detect engagements, run encounter rounds, finalize,
   publish snapshot). **The largest single piece of new code.**
   Tests run a few hand-driven ticks against a world with 1 hero +
   1 location.
8. `dnd/sandbox/worker.py` — the background thread that calls
   `tick()` at `TICK_INTERVAL`. Owns the worker's exclusive write
   lock; nothing else touches it.
9. `dnd/sandbox/routes.py` — HTTP routes. Read handlers deref
   `world.current_snapshot`; write handlers validate and submit an
   `Order`. **Routes never call `apply_order` directly.**
10. Wire into `server.py` (start tick worker on server start; route
    registration). HTTP server stays `ThreadingHTTPServer` (request
    threads only enqueue or read snapshots, so threading is safe and
    cheap).
11. `tests/test_sandbox_*.py` — unit tests per module, plus an
    integration test that boots a server with a fast tick interval
    (e.g., 0.05s), submits a deployment, polls until complete, and
    asserts the trace. Also a determinism test: same orders +
    same seed → bit-identical world state.

Each step is one focused commit. Estimated size: ~2k LOC including
tests. Estimated wall-clock work: ~2 weeks of focused effort
(roughly double the pre-sim cut, as flagged when we made the
trade).
