# D&D Sandbox

A persistent web-API sandbox where each player runs a castle, spawns
heroes with player-authored behavior scripts and level-up plans, and
sends them out into a shared 2D world to fight, gather, craft, and
build their reputation.

The full PF1 SRD ruleset runs underneath. Heroes act on standing
orders; combat resolves with real PF1 mechanics — initiative, BAB,
iterative attacks, attacks of opportunity, the lot.

See `DESIGN_PROPOSAL.md` for the design.

## Status

Phase 1 — foundation skeleton. Implements:

- Seeded dice expression evaluator.
- Level-1 character creation for the 7 PF1 core races and 11 base
  classes.
- HTTP API for SRD content lookups and character creation.

No world, no deployments, no behavior scripts yet. That's later phases.

## Running

```bash
python3 -m dnd               # start the server on 127.0.0.1:8080
python3 -m dnd --port 9000   # alternate port
```

## Tests

```bash
python3 -m unittest discover dnd/tests
```

## Layout

```
dnd/
  server.py              HTTP routing
  engine/
    dice.py              seeded dice + expression parser
    content.py           JSON content loader
    characters.py        level-1 character creation
  content/
    races/*.json
    classes/*.json
    skills/*.json
    feats/*.json
    conditions/*.json
  tests/                 unittest suite
```

## License

Mechanical content is derived from the Pathfinder Roleplaying Game
Reference Document under the Open Game License 1.0a. See `OGL.txt`
at the repo root for the license text and Section 15 attribution chain.
