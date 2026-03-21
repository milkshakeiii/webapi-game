# Network CoreWar

**The challenge:** Write a program that outperforms the reigning champions in a round-robin tournament.

## The Game

Programs compete on a network of nodes. Each node has 128 memory cells. Your program starts on one node with a single process and must:

1. **Spread** to other nodes using `FORK`
2. **Build scoring wells** — data cells with high values
3. **Score points** by executing `SCORE` instructions that read from your wells
4. **Fight** by bombing enemy code (overwriting their cells with zeros)

First to **100,000 points** wins. If nobody reaches the target in 10,000 turns, the highest score wins.

The catch: each node only allows **2 instruction executions per turn**, shared by all processes on that node. Spreading thin across many nodes is far more efficient than stacking processes. And your scoring wells can be destroyed by enemy bombing — so you need to defend them.

## Quick Start

```bash
cd puzzles/network-corewar

# Test your warrior against the champions
python3 submit.py my_warrior.ncw

# Run a single match to debug
python3 main.py my_warrior.ncw champions/apex.ncwc -v

# Study the examples
ls examples/
```

## Writing Your First Warrior

Warriors are written in `.ncw` files — one instruction per line, comments after `;`.

Here's a minimal warrior that builds a well and scores from it:

```
;name MyFirst
MOV #100, $4      ; write a scoring well (DAT #0, #100) at PC+4
FORK #0, #6       ; copy 6 cells to the next node
SCORE $2          ; score 100 points from the well
JMP $-1, #0       ; loop scoring forever
DAT #0, #0        ; becomes the scoring well
```

This scores ~100 points per cycle from its well, but it has no defense — an enemy can bomb the well to zero. The champions are much more sophisticated.

## Key Concepts

**Scoring wells:** `SCORE $N` reads the b_value of the cell at address PC+N. A `DAT #0, #100` earns 100 points per SCORE cycle. A bombed `DAT #0, #0` earns nothing. Build wells, protect them.

**FORK:** `FORK #edge, #payload` copies cells from your current position to an adjacent node and spawns a process there. Payload = how many cells to copy. Bigger payloads carry more code but the copy is the same speed.

**Cycle budgets:** Each node runs only 2 instructions per turn total. One process alone gets both cycles. Eight processes on the same node each get ~0.25 cycles. Spread out.

**Addressing:** `#N` = literal value, `$N` = relative to current position, `@N` = indirect (read the value at $N, then use that as a further offset).

## The Champions

Four champions, each representing a different strategic archetype:

- **Apex** (41 instructions) — Engineering. Phase-transition warrior with well-building, role divergence between commander and worker processes, and targeted bombing.
- **Scorpion** (13 instructions) — Balance. Compact fork+bomb+score with embedded wells. Efficient and resilient.
- **Swarm** (30 instructions) — Economy. Pre-embedded wells skip the setup phase. Floods nodes with scorers for maximum cycle-budget efficiency.
- **Vanguard** (39 instructions) — Aggression. Triple bomb streams, constant re-forking, and well repair under fire.

Your warrior must hold a **winning head-to-head record against each champion** across ring, grid, and star topologies.

## Full Reference

See [SPEC.md](SPEC.md) for the complete instruction set (13 instructions), addressing modes, execution model, and all game rules.

## Files

- `submit.py` — Submit your warrior and see if it beats the champions
- `main.py` — Run individual matches with full control over settings
- `SPEC.md` — Complete game specification
- `champions/` — The warriors you need to beat (compiled `.ncwc` format)
- `examples/` — Reference warriors showing different strategies
