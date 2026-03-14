# Shattered Archive API v1

This is a first-pass HTTP API for a playable version of *Shattered Archive*.

The API is split into two layers:

- exploration is stateful and text-heavy, so it uses one command per request
- synthesis is deterministic and optimization-heavy, so it uses one whole recipe submission per request

That split is intentional. It keeps the narrative shell simple while making the puzzle core easy to inspect, simulate, and solve through Codex or Claude Code.

## Design Choices

### 1. Sessions are the unit of play

A session stores:

- current room
- inventory
- discovered facts
- active puzzle, if any
- solved obstacles

The client does not build global state itself. It asks the server for the current authoritative session state.

### 2. Synthesis attempts are submitted all at once

The client does not send `add`, `bind`, and `distill` as separate HTTP requests.

Instead, it sends a single request containing an ordered list of actions. The server evaluates the full attempt and returns a step-by-step trace.

This is a better fit for LLM-assisted play because it is:

- less chatty
- easier to revise
- easier to compare against previous attempts
- easier for the server to score and explain

### 3. Public attempts use symbolic thread names

The internal simulator can use array indexes for threads. The public API should not.

Instead, the client gives temporary names to threads inside an attempt, for example `a`, `b`, `ab`, or `core`. Those names are local to that one request.

That avoids brittle references like “thread 1 after step 4.”

## Base Conventions

- Base path: `/v1`
- JSON request and response bodies only
- All ids are opaque strings
- Malformed requests use normal HTTP error codes
- Valid game evaluations return `200 OK`, even when the attempted recipe fails

For synthesis, that means:

- `success`: the recipe is legal and satisfies the contract
- `failure`: the recipe is legal but does not satisfy the contract
- `invalid`: the recipe contains an illegal action sequence

## Core Resources

### Session

A session is the top-level game resource.

Example:

```json
{
  "session_id": "ses_01hr3j9r3w7m0f7q1j4h5m2k5p",
  "game": "shattered_archive",
  "status": "active",
  "room": {
    "room_id": "lower_stacks_entry",
    "title": "Lower Stacks Entry",
    "description": "A broken lantern bowl hangs above a dark stair.",
    "exits": [
      {
        "exit_id": "north_stair",
        "label": "north",
        "locked": true,
        "reason": "The lantern is unlit."
      }
    ],
    "interactables": [
      {
        "id": "lantern_bowl",
        "label": "lantern bowl",
        "kind": "puzzle_anchor"
      }
    ]
  },
  "inventory": [],
  "active_puzzle": {
    "puzzle_id": "lower_stacks_lantern",
    "title": "Lantern of the Lower Stacks",
    "status": "active"
  }
}
```

### Puzzle View

A puzzle view is the full deterministic state needed to attempt a synthesis puzzle.

Example:

```json
{
  "puzzle_id": "lower_stacks_lantern",
  "title": "Lantern of the Lower Stacks",
  "status": "active",
  "puzzle_revision": 3,
  "bench_capacity": 3,
  "step_limit": 6,
  "contract": {
    "minimum_essences": {
      "lumen": 6,
      "echo": 4,
      "motive": 0,
      "veil": 0
    },
    "maximum_essences": {
      "lumen": 99,
      "echo": 99,
      "motive": 99,
      "veil": 1
    },
    "required_tags": ["relic"],
    "forbidden_tags": ["spectral"],
    "max_fray": 1
  },
  "reagents": [
    {
      "id": "archive_dust",
      "name": "Archive Dust",
      "essences": {
        "lumen": 1,
        "echo": 2,
        "motive": 0,
        "veil": 0
      },
      "tags": ["ink"],
      "cost": 2,
      "count": 1
    }
  ]
}
```

## Endpoints

### `POST /v1/sessions`

Creates a new game session.

Request:

```json
{
  "game": "shattered_archive"
}
```

Response:

```json
{
  "session": {
    "session_id": "ses_01hr3j9r3w7m0f7q1j4h5m2k5p",
    "game": "shattered_archive",
    "status": "active"
  },
  "room": {
    "room_id": "lower_stacks_entry",
    "title": "Lower Stacks Entry",
    "description": "A broken lantern bowl hangs above a dark stair."
  },
  "active_puzzle": {
    "puzzle_id": "lower_stacks_lantern",
    "title": "Lantern of the Lower Stacks",
    "status": "active"
  }
}
```

### `GET /v1/sessions/{session_id}`

Returns the current session view, including room summary and the currently active puzzle summary if one exists.

### `POST /v1/sessions/{session_id}/commands`

Applies one exploration command.

This endpoint handles the MUD-like shell around the synthesis system.

Example requests:

```json
{ "op": "look" }
```

```json
{ "op": "move", "exit": "north" }
```

```json
{ "op": "inspect", "target": "lantern_bowl" }
```

Example response:

```json
{
  "command_id": "cmd_01hr3jf38s6wxshn0y8z5fzkj7",
  "result": "ok",
  "narration": "The lantern bowl is etched with a contract circle and three reagent slots.",
  "room": {
    "room_id": "lower_stacks_entry",
    "title": "Lower Stacks Entry"
  },
  "active_puzzle": {
    "puzzle_id": "lower_stacks_lantern",
    "title": "Lantern of the Lower Stacks",
    "status": "active"
  }
}
```

### `GET /v1/sessions/{session_id}/puzzles/{puzzle_id}`

Returns the full puzzle view for one active puzzle.

The client should read this before attempting a solution, because it contains the current `puzzle_revision`.

### `POST /v1/sessions/{session_id}/puzzles/{puzzle_id}/attempts`

Evaluates one whole synthesis attempt.

The same endpoint is used for both:

- `simulate`: test a recipe without changing world state
- `commit`: apply a successful recipe to the world

## Attempt Request Format

Example:

```json
{
  "mode": "simulate",
  "puzzle_revision": 3,
  "actions": [
    { "op": "add", "reagent_id": "archive_dust", "as": "a" },
    { "op": "add", "reagent_id": "catalogue_oil", "as": "b" },
    { "op": "add", "reagent_id": "mirror_dust", "as": "c" },
    { "op": "bind", "left": "a", "right": "b", "into": "ab", "bonus_essence": "echo" },
    { "op": "bind", "left": "ab", "right": "c", "into": "core", "bonus_essence": "lumen" },
    { "op": "distill", "thread": "core", "essence": "lumen" }
  ]
}
```

### Attempt Action Shapes

#### Add

Creates a new live thread from a reagent.

```json
{ "op": "add", "reagent_id": "archive_dust", "as": "a" }
```

Rules:

- `reagent_id` must be available in the puzzle's reagent pool
- `as` must be a new local thread name
- the bench cannot exceed `bench_capacity`

#### Bind

Consumes two live threads and creates a new live thread.

```json
{ "op": "bind", "left": "a", "right": "b", "into": "ab", "bonus_essence": "echo" }
```

Rules:

- `left` and `right` must both be live thread names
- `into` must be a new local thread name
- after the bind, `left` and `right` are retired and cannot be referenced again
- `bonus_essence` is optional
- if present, it must be positive in both input threads and the bind must be stable

#### Distill

Mutates one live thread in place.

```json
{ "op": "distill", "thread": "core", "essence": "lumen" }
```

#### Reweave

Mutates one live thread in place.

```json
{ "op": "reweave", "thread": "core", "from_essence": "motive", "to_essence": "echo", "amount": 1 }
```

#### Stabilize

Mutates one live thread in place.

```json
{ "op": "stabilize", "thread": "core", "reduce_essence": "lumen" }
```

### Alias Rules

Thread names are local to a single attempt request.

Recommended conventions:

- use short names like `a`, `b`, `c`, `ab`, `core`
- treat names as write-once for `add` and `bind`
- expect unary operations to mutate the named thread in place

This gives the client a stable symbolic language without exposing internal engine indexes.

## Attempt Response Format

Every valid attempt request returns a full evaluation result.

Example success response:

```json
{
  "attempt_id": "att_01hr3jv6x1j4n4m7h7b8qj3h9m",
  "session_id": "ses_01hr3j9r3w7m0f7q1j4h5m2k5p",
  "puzzle_id": "lower_stacks_lantern",
  "puzzle_revision": 3,
  "mode": "simulate",
  "resolution": "success",
  "summary": {
    "contract_satisfied": true,
    "steps_used": 6,
    "step_limit": 6,
    "cost_used": 7,
    "score": 646,
    "final_thread": {
      "essences": {
        "lumen": 6,
        "echo": 4,
        "motive": 0,
        "veil": 0
      },
      "tags": ["ink", "mineral", "relic"],
      "fray": 1
    },
    "violations": []
  },
  "trace": [
    {
      "step": 1,
      "action": { "op": "add", "reagent_id": "archive_dust", "as": "a" },
      "outcome": "ok",
      "live_threads": {
        "a": {
          "essences": {
            "lumen": 1,
            "echo": 2,
            "motive": 0,
            "veil": 0
          },
          "tags": ["ink"],
          "fray": 0
        }
      },
      "remaining_reagents": {
        "archive_dust": 0,
        "catalogue_oil": 1,
        "mirror_dust": 1
      }
    }
  ]
}
```

Example legal but unsuccessful response:

```json
{
  "attempt_id": "att_01hr3k5c4f7kzh7z48w3g8nssx",
  "mode": "simulate",
  "resolution": "failure",
  "summary": {
    "contract_satisfied": false,
    "steps_used": 5,
    "step_limit": 6,
    "cost_used": 6,
    "final_thread": {
      "essences": {
        "lumen": 5,
        "echo": 4,
        "motive": 1,
        "veil": 0
      },
      "tags": ["ink", "relic"],
      "fray": 1
    },
    "violations": [
      {
        "code": "minimum_essence_not_met",
        "field": "lumen",
        "expected": 6,
        "actual": 5
      }
    ]
  },
  "trace": []
}
```

Example invalid attempt response:

```json
{
  "attempt_id": "att_01hr3k8e05n6m1r5smy5xk2qwr",
  "mode": "simulate",
  "resolution": "invalid",
  "failed_step": 4,
  "error": {
    "code": "undefined_thread",
    "message": "Thread 'ab' is not live at step 4."
  },
  "trace": []
}
```

## Commit Semantics

If `mode` is `commit`:

- `resolution = success` applies the puzzle result to the session
- `resolution = failure` leaves world state unchanged
- `resolution = invalid` leaves world state unchanged

Example commit success extension:

```json
{
  "mode": "commit",
  "resolution": "success",
  "commit": {
    "applied": true,
    "puzzle_status": "solved",
    "effects": [
      {
        "type": "unlock_exit",
        "exit_id": "north_stair"
      },
      {
        "type": "room_text_change",
        "target": "lantern_bowl",
        "description": "The bowl now burns with a pale archive flame."
      }
    ]
  }
}
```

## Validation and Error Handling

### Transport and schema errors

Use standard HTTP error codes:

- `400 Bad Request`: malformed JSON or missing required fields
- `404 Not Found`: unknown session or puzzle id
- `409 Conflict`: stale `puzzle_revision`, inactive puzzle, or duplicate commit against an already solved puzzle

### Gameplay evaluation results

Use `200 OK` with semantic result fields:

- `resolution = success`
- `resolution = failure`
- `resolution = invalid`

This keeps the distinction clear:

- HTTP errors mean the client made a bad request
- `failure` and `invalid` mean the player made a bad move

## Recommended Client Flow

1. `POST /v1/sessions`
2. `GET /v1/sessions/{session_id}`
3. Explore with `POST /v1/sessions/{session_id}/commands`
4. When a puzzle is active, call `GET /v1/sessions/{session_id}/puzzles/{puzzle_id}`
5. Submit `simulate` attempts to test candidate recipes
6. Submit one `commit` attempt when satisfied
7. Continue exploration using the updated room state

## Why This Is the Right First API

This API keeps the world layer lightweight while making the synthesis layer explicit and programmable. It is easy for a normal client to call, but it is especially well suited to agent-assisted play because the hard part of the game is packaged as a structured optimization problem with a full evaluation trace.
