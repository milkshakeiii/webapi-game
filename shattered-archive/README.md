# Shattered Archive

Prototype rules and test harness for the archive-synthesis puzzle layer.

The current design is intentionally small:

- One puzzle file defines a reagent pool, a contract, a bench capacity, and a step limit.
- The player turns reagents into independent `threads`, then merges and transforms them into one final spell.
- A contract is binary success or failure. Score is secondary and only used to rank valid solutions.

## Files

- `examples/lantern_puzzle.json`: starter puzzle with one known elegant solution.
- `API.md`: first-pass public HTTP API for sessions, commands, and whole-attempt synthesis.
- `MECHANICS.md`: plain-English explanation of the synthesis system.
- `schemas/*.schema.json`: machine-readable shape for puzzle, action, thread, and state data.
- `simulator.py`: deterministic local search harness with no third-party dependencies.

## State Machine

Each puzzle begins at step `0` with:

- `remaining_reagents`: a multiset of reagent ids and counts.
- `threads`: empty.
- `bench_capacity`: maximum concurrent threads on the bench.
- `step_limit`: maximum actions before the puzzle locks.

Each thread contains:

- `essences`: four integer stats: `lumen`, `echo`, `motive`, `veil`
- `tags`: a set of lowercase string tags
- `fray`: non-negative integer penalty

### Actions

`add(reagent_id)`

- Consumes one reagent from the pool.
- Creates a new thread with that reagent's essences and tags.
- Requires `len(threads) < bench_capacity`.

`bind(left_thread, right_thread, bonus_essence?)`

- Merges two threads into one.
- New essences are the elementwise sum of both threads.
- New tags are the union of both threads' tags.
- New fray is the sum of both threads' fray values.
- If the threads share at least one tag, the bind is stable.
- If the threads also share a positive value in some essence, the player may choose one such shared essence and gain `+1` there as a resonance bonus.
- If the threads share no tags, the bind still works but adds `+2 fray`.

`distill(thread, essence)`

- Adds `+2` to the chosen essence.
- Subtracts `1` from every other essence that is above `0`.
- Adds `+1 fray`.

`reweave(thread, from_essence, to_essence, amount)`

- Moves `1` or `2` points from one essence to another.
- Source essence must have at least that many points.
- Adds `+1 fray`, or `+2 fray` when moving across an opposed pair:
  - `lumen <-> veil`
  - `echo <-> motive`

`stabilize(thread, reduce_essence)`

- Subtracts `2 fray`, to a minimum of `0`.
- Subtracts `1` from one of the thread's current highest essences.
- The caller must specify which highest essence to reduce when tied.

## Contract Resolution

A puzzle is solved only when the player finishes with exactly one thread and that thread:

- Meets every minimum essence requirement.
- Does not exceed any maximum essence caps.
- Includes all required tags.
- Includes none of the forbidden tags.
- Has `fray <= max_fray`.

## Scoring

The harness ranks valid solutions with a simple prototype score:

- Fewer steps is better.
- Lower total reagent cost is better.
- Lower final fray is better.
- Lower overproduction above contract minimums is better.

This is not meant to be final economy design. It is just a stable way to compare candidate rule sets.

## Run

```bash
python3 simulator.py examples/lantern_puzzle.json --top 8
```

The script prints:

- Unique reachable states by depth
- Number of valid end states
- Top-ranked solutions with action histories and final thread stats
