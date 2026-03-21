# Network CoreWar Specification

## Overview

Programs compete on a network graph. Each node has a circular memory array of cells. Programs spread across nodes using FORK and SEND/RECV. Last program running (or most nodes controlled) wins.

## Graph

- **Node**: circular memory of N cells (default 16). Empty cells are `DAT #0, #0`.
- **Edge**: bidirectional connection between nodes. Each node's edges are numbered 0, 1, 2, ... in a consistent order.
- **Topologies**:
  - `ring`: edge 0 = clockwise, edge 1 = counter-clockwise. 2 edges per node.
  - `grid`: toroidal grid, edge 0 = right, 1 = down, 2 = left, 3 = up. 4 edges per node.
  - `star`: center node 0 connected to all spokes. Center has N edges, spokes have 1.
  - `complete`: every node connected to every other.

## Cells

Each cell has:
- `opcode`: instruction (DAT, MOV, ADD, SUB, JMP, JMZ, CMP, SEND, RECV, FORK, SCAN)
- `a_mode`, `a_value`: operand A (mode + integer value)
- `b_mode`, `b_value`: operand B (mode + integer value)
- `owner`: player ID who last wrote this cell (used for scoring)

## Addressing Modes

All addressing is intra-node (within the current node's memory, mod node_size).

| Symbol | Name      | Meaning                                                    |
|--------|-----------|------------------------------------------------------------|
| `#`    | Immediate | The literal value. No memory reference.                    |
| `$`    | Relative  | Offset from current PC. Default if no sigil.               |
| `@`    | Indirect  | Value at relative address is used as further offset from that address. |

For `@`: resolve `(PC + value) % size` to get intermediate address, then read that cell's b_value and add it to the intermediate address to get the final address.

## Instructions

| Opcode | Operands | Description |
|--------|----------|-------------|
| `DAT`  | A, B     | Data. Process dies if it executes this. |
| `MOV`  | A, B     | If A is `#` (immediate): write `DAT #0, #A` to address B. Otherwise: copy entire cell at A to address B. |
| `ADD`  | A, B     | Add value of A to b_value of cell at B. Result wraps mod node_size. |
| `SUB`  | A, B     | Subtract value of A from b_value of cell at B. Result wraps mod node_size. |
| `MOD`  | A, B     | Set b_value of cell at B to `b_value % A`. Useful for wrapping computed edge indices (e.g., `MOD #2, $3` to cycle edge 0,1,0,1,...). No-op if A is 0. |
| `JMP`  | A, _     | Set PC to address A. B is ignored. |
| `JMZ`  | A, B     | If b_value of cell at B is zero, jump to A. Otherwise advance PC. |
| `CMP`  | A, B     | If value of A != value of B, skip next instruction (PC += 2). Otherwise PC += 1. **Note:** this is inverted from traditional CoreWar's CMP/SEQ (which skips if equal). |
| `SEND` | A, B     | Copy cell at address A to the RECV buffer of the neighbor at edge B. Edge index is resolved via B's addressing mode (use `#` for literal, `$` or `@` for computed). |
| `RECV` | A, B     | Check RECV buffer from edge B (resolved via addressing mode). If data present: write it to address A, skip next (PC += 2). If empty: PC += 1. Clears the buffer on read. |
| `FORK` | A, B     | Copy B cells starting from PC to neighbor at edge A. Both A (edge) and B (payload size) are resolved via their addressing modes — use `$` or `@` to compute targets dynamically. Spawn a new process at PC on that node. Code copy and process activation are **deferred to end of turn**. If multiple players fork to the same node in the same turn, all contested forks are cancelled. |
| `SCAN` | A, B     | Count non-DAT cells on neighbor at edge B (resolved via addressing mode). Store count in b_value of cell at address A. |

### Value resolution

`get_value(mode, value)`:
- `#`: returns `value` directly
- `$` or `@`: returns b_value of the cell at the resolved address

## Execution Model

### Processes

A process is a program counter (PC) on a specific node, belonging to a player. Each process executes one instruction per turn.

### Turn Structure

1. **Alternate player order**: even turns P0 first, odd turns P1 first.
2. For each player (in turn order):
   - Execute each process in FIFO order (oldest first).
   - Surviving processes kept; dead processes (executed DAT) removed.
   - New processes from FORK go into a pending queue.
3. **Resolve pending forks** (all players simultaneously):
   - Group forks by target node.
   - If only one player targets a node: code is copied, process is spawned.
   - If multiple players target the same node: all forks to that node are cancelled.
4. Add approved pending processes to player queues (capped at max_processes, default 16).
5. Check elimination.

### Process Cap

Each player has a maximum of 16 processes. Excess processes are truncated (oldest kept).

## Win Conditions

1. **Elimination**: only one player has processes remaining.
2. **Turn limit** (default 10,000): score by node ownership.

### Node Ownership

A node is owned by the player with the most non-DAT cells on that node. Ties = no owner. Player with most owned nodes wins. Equal nodes = draw.

## Program Format (.ncw)

```
;name ProgramName
;author AuthorName
MOV $0, $1       ; comments after semicolon
ADD #4, $3
JMP $-2, #0
DAT #0, #4
```

- One instruction per line. Comments start with `;`.
- `;name` and `;author` are metadata directives.
- Default addressing mode is `$` (relative) if no sigil given.
- Program must fit within node_size cells.

## CLI Usage

```
python3 main.py prog1.ncw prog2.ncw [options]

Options:
  --nodes N          Number of graph nodes
  --node-size N      Memory cells per node (default: 16)
  --max-turns N      Maximum turns (default: 10000)
  --topology TYPE    ring, grid, star, complete (default: ring)
  --grid-rows N      Grid rows (grid topology)
  --grid-cols N      Grid cols (grid topology)
  -v, --verbose      Per-instruction execution trace
  -d, --dump         Dump final node memory state
```

Supports 2+ players. Players are placed at maximally distant positions on the graph.
