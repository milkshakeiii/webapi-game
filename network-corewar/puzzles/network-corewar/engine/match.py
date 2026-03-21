"""Match runner for Network CoreWar."""

from collections import defaultdict
from .graph import Cell, Graph
from .process import Process
from .instruction import cell_to_str


class Match:
    """Runs a Network CoreWar match."""

    def __init__(self, graph, max_turns=10000, max_processes=16, score_target=None):
        self.graph = graph
        self.max_turns = max_turns
        self.max_processes = max_processes
        self.score_target = score_target  # None = no score victory, use node_count
        self.turn = 0
        # player_id -> list of Process (FIFO queue)
        self.processes = defaultdict(list)
        self.scores = defaultdict(int)  # player_id -> score points
        self.player_names = {}
        self.eliminated = set()
        self.log = []

    def place_program(self, player_id, name, cells, node_id, start_pc=0):
        """Place a program on a node and create initial process."""
        self.player_names[player_id] = name
        node = self.graph.nodes[node_id]
        for i, cell in enumerate(cells):
            c = cell.copy(new_owner=player_id)
            node.write(start_pc + i, c)
        self.processes[player_id].append(Process(player_id, node_id, start_pc))

    def resolve_address(self, node, pc, mode, value):
        """Resolve an addressing mode to an absolute address within the node."""
        if mode == '#':
            return None  # immediate - no address
        elif mode == '$':
            return (pc + value) % node.size
        elif mode == '@':
            intermediate = (pc + value) % node.size
            cell = node.read(intermediate)
            return (intermediate + cell.b_value) % node.size
        return None

    def get_value(self, node, pc, mode, value):
        """Get the numeric value for an operand."""
        if mode == '#':
            return value
        addr = self.resolve_address(node, pc, mode, value)
        if addr is not None:
            return node.read(addr).b_value
        return 0

    def execute(self, proc, verbose=False):
        """Execute one instruction for a process. Returns (alive, new_processes)."""
        node = self.graph.nodes[proc.node_id]
        cell = node.read(proc.pc)
        op = cell.opcode
        new_procs = []

        if verbose:
            print(f"  T{self.turn} P{proc.player_id} node={proc.node_id} pc={proc.pc}: {cell_to_str(cell)}")

        if op == 'DAT':
            if verbose:
                print(f"    -> DIED (executed DAT)")
            return False, []

        elif op == 'MOV':
            if cell.a_mode == '#':
                # Write a DAT with this immediate value
                dest = self.resolve_address(node, proc.pc, cell.b_mode, cell.b_value)
                if dest is not None:
                    target = node.read(dest)
                    new_cell = Cell('DAT', '#', 0, '#', cell.a_value, proc.player_id)
                    node.write(dest, new_cell)
            else:
                src_addr = self.resolve_address(node, proc.pc, cell.a_mode, cell.a_value)
                dest = self.resolve_address(node, proc.pc, cell.b_mode, cell.b_value)
                if src_addr is not None and dest is not None:
                    node.write(dest, node.read(src_addr).copy(proc.player_id))
            proc.pc = (proc.pc + 1) % node.size

        elif op == 'ADD':
            val = self.get_value(node, proc.pc, cell.a_mode, cell.a_value)
            dest = self.resolve_address(node, proc.pc, cell.b_mode, cell.b_value)
            if dest is not None:
                target = node.read(dest)
                target.b_value = (target.b_value + val) % node.size
            proc.pc = (proc.pc + 1) % node.size

        elif op == 'SUB':
            val = self.get_value(node, proc.pc, cell.a_mode, cell.a_value)
            dest = self.resolve_address(node, proc.pc, cell.b_mode, cell.b_value)
            if dest is not None:
                target = node.read(dest)
                target.b_value = (target.b_value - val) % node.size
            proc.pc = (proc.pc + 1) % node.size

        elif op == 'MOD':
            val = self.get_value(node, proc.pc, cell.a_mode, cell.a_value)
            dest = self.resolve_address(node, proc.pc, cell.b_mode, cell.b_value)
            if dest is not None and val != 0:
                target = node.read(dest)
                target.b_value = target.b_value % val
            proc.pc = (proc.pc + 1) % node.size

        elif op == 'JMP':
            addr = self.resolve_address(node, proc.pc, cell.a_mode, cell.a_value)
            if addr is not None:
                proc.pc = addr
            else:
                proc.pc = (proc.pc + 1) % node.size

        elif op == 'JMZ':
            val = self.get_value(node, proc.pc, cell.b_mode, cell.b_value)
            if val == 0:
                addr = self.resolve_address(node, proc.pc, cell.a_mode, cell.a_value)
                if addr is not None:
                    proc.pc = addr
                else:
                    proc.pc = (proc.pc + 1) % node.size
            else:
                proc.pc = (proc.pc + 1) % node.size

        elif op == 'CMP':
            val_a = self.get_value(node, proc.pc, cell.a_mode, cell.a_value)
            val_b = self.get_value(node, proc.pc, cell.b_mode, cell.b_value)
            if val_a != val_b:
                proc.pc = (proc.pc + 2) % node.size  # skip next
            else:
                proc.pc = (proc.pc + 1) % node.size

        elif op == 'SEND':
            src_addr = self.resolve_address(node, proc.pc, cell.a_mode, cell.a_value)
            edge_idx = self.get_value(node, proc.pc, cell.b_mode, cell.b_value)
            if src_addr is not None:
                src_cell = node.read(src_addr).copy(proc.player_id)
                self.graph.send_to_edge(proc.node_id, edge_idx, src_cell)
            proc.pc = (proc.pc + 1) % node.size

        elif op == 'RECV':
            edge_idx = self.get_value(node, proc.pc, cell.b_mode, cell.b_value)
            received = self.graph.recv_from_edge(proc.node_id, edge_idx)
            if received is not None:
                dest = self.resolve_address(node, proc.pc, cell.a_mode, cell.a_value)
                if dest is not None:
                    node.write(dest, received)
                proc.pc = (proc.pc + 2) % node.size  # skip next (success)
            else:
                proc.pc = (proc.pc + 1) % node.size  # no skip (nothing received)

        elif op == 'SCAN':
            # SCAN A, B — count non-DAT cells on neighbor at edge B, store count at address A.
            edge_idx = self.get_value(node, proc.pc, cell.b_mode, cell.b_value)
            neighbor_id = self.graph.neighbor(proc.node_id, edge_idx)
            dest = self.resolve_address(node, proc.pc, cell.a_mode, cell.a_value)
            if neighbor_id is not None and dest is not None:
                neighbor_node = self.graph.nodes[neighbor_id]
                count = sum(1 for c in neighbor_node.memory if c.opcode != 'DAT')
                target = node.read(dest)
                target.b_value = count % node.size
            proc.pc = (proc.pc + 1) % node.size

        elif op == 'SCORE':
            # Burns the cycle to score points equal to b_value of the referenced
            # cell. Immediate mode (#) is treated as relative ($) — SCORE always
            # reads from memory, never from a literal. This ensures all scoring
            # depends on data cells that enemies can bomb.
            mode = cell.a_mode if cell.a_mode != '#' else '$'
            addr = self.resolve_address(node, proc.pc, mode, cell.a_value)
            if addr is not None:
                points = node.read(addr).b_value
                if points > 0:
                    self.scores[proc.player_id] += points
            proc.pc = (proc.pc + 1) % node.size

        elif op == 'FORK':
            edge_idx = self.get_value(node, proc.pc, cell.a_mode, cell.a_value)
            payload_size = self.get_value(node, proc.pc, cell.b_mode, cell.b_value)
            if payload_size <= 0:
                payload_size = 1
            neighbor_id = self.graph.neighbor(proc.node_id, edge_idx)
            if neighbor_id is not None:
                # Snapshot the payload cells now (read from source node)
                payload = {}
                for i in range(payload_size):
                    addr = (proc.pc + i) % node.size
                    payload[addr] = node.read(addr).copy(proc.player_id)
                start_pc = proc.pc % self.graph.nodes[neighbor_id].size
                new_proc = Process(proc.player_id, neighbor_id, start_pc)
                # Store fork info for deferred resolution
                new_proc._fork_payload = payload
                new_proc._fork_target = neighbor_id
                new_procs.append(new_proc)
            proc.pc = (proc.pc + 1) % node.size

        return True, new_procs

    def run(self, verbose=False):
        """Run the match. Returns (winner_id or None, results_dict)."""
        player_ids = sorted(self.processes.keys())

        for turn in range(self.max_turns):
            self.turn = turn

            # Reset cycle budgets for all nodes
            for node in self.graph.nodes.values():
                node.cycles_remaining = node.cycles

            # Alternate player order each turn to reduce ordering bias
            if turn % 2 == 0:
                turn_order = player_ids
            else:
                turn_order = player_ids[::-1]

            # Collect all newly forked processes — they activate next turn
            pending = defaultdict(list)

            for pid in turn_order:
                if pid in self.eliminated:
                    continue

                surviving = []

                for proc in self.processes[pid]:
                    node = self.graph.nodes[proc.node_id]
                    if node.cycles_remaining > 0:
                        node.cycles_remaining -= 1
                        alive, new_procs = self.execute(proc, verbose=verbose)
                        if alive:
                            surviving.append(proc)
                        pending[pid].extend(new_procs)
                    else:
                        # No cycles left on this node — process skips this turn
                        surviving.append(proc)

                self.processes[pid] = surviving

                if not self.processes[pid] and not pending[pid]:
                    # Tentatively mark — may be revived if pending forks survive resolution
                    self.eliminated.add(pid)

            # Resolve fork payloads simultaneously with conflict detection
            # Group pending forks by target node
            forks_by_node = defaultdict(list)  # node_id -> [(proc, pid)]
            for pid in player_ids:
                for proc in pending[pid]:
                    if proc._fork_payload is not None:
                        forks_by_node[proc._fork_target].append((proc, pid))

            # For each target node, check if multiple players are contesting it
            contested_nodes = set()
            for node_id, forks in forks_by_node.items():
                players = set(pid for _, pid in forks)
                if len(players) > 1:
                    contested_nodes.add(node_id)

            # Apply non-contested forks, cancel contested ones
            approved = defaultdict(list)
            for pid in player_ids:
                for proc in pending[pid]:
                    if proc._fork_target in contested_nodes:
                        # Contested — fork fails, no code copy, no process
                        pass
                    else:
                        # Uncontested — apply code copy
                        if proc._fork_payload:
                            target_node = self.graph.nodes[proc._fork_target]
                            for addr, cell in proc._fork_payload.items():
                                target_node.write(addr, cell)
                        approved[pid].append(proc)
                    # Clean up fork metadata
                    proc._fork_payload = None
                    proc._fork_target = None

            # Add approved processes — they execute next turn
            for pid in player_ids:
                if approved[pid]:
                    combined = self.processes[pid] + approved[pid]
                    self.processes[pid] = combined[:self.max_processes]

            # Re-check elimination after fork resolution
            for pid in player_ids:
                if self.processes[pid]:
                    self.eliminated.discard(pid)
                elif pid not in self.eliminated:
                    self.eliminated.add(pid)
                    if verbose:
                        print(f"Turn {turn}: Player {pid} ({self.player_names.get(pid, '?')}) eliminated")

            # Check for score victory
            if self.score_target is not None:
                score_winners = [pid for pid in player_ids
                                 if self.scores[pid] >= self.score_target
                                 and pid not in self.eliminated]
                if score_winners:
                    max_score = max(self.scores[pid] for pid in score_winners)
                    top = [pid for pid in score_winners if self.scores[pid] == max_score]
                    winner = top[0] if len(top) == 1 else None
                    return winner, self._results(winner, "score")

            # Check for winner by elimination
            alive_players = [p for p in player_ids if p not in self.eliminated]
            if len(alive_players) <= 1:
                winner = alive_players[0] if alive_players else None
                return winner, self._results(winner, "elimination")

        # Turn limit reached
        if self.score_target is not None:
            # Highest score wins
            alive_scores = {pid: self.scores[pid] for pid in player_ids if pid not in self.eliminated}
            if alive_scores:
                max_score = max(alive_scores.values())
                top = [pid for pid, s in alive_scores.items() if s == max_score]
                winner = top[0] if len(top) == 1 else None
                return winner, self._results(winner, "score_timeout")
        # Fall back to node ownership
        winner = self._score_nodes(player_ids)
        return winner, self._results(winner, "node_count")

    def _score_nodes(self, player_ids):
        """Score nodes by ownership. Returns winner player_id or None for tie."""
        ownership = defaultdict(int)
        for node in self.graph.nodes.values():
            counts = defaultdict(int)
            for cell in node.memory:
                if cell.owner is not None and cell.opcode != 'DAT':
                    counts[cell.owner] += 1
            if counts:
                max_count = max(counts.values())
                winners = [pid for pid, c in counts.items() if c == max_count]
                if len(winners) == 1:
                    ownership[winners[0]] += 1

        if not ownership:
            return None
        max_nodes = max(ownership.values())
        top = [pid for pid, c in ownership.items() if c == max_nodes]
        return top[0] if len(top) == 1 else None

    def _results(self, winner, method):
        """Build results dictionary."""
        ownership = defaultdict(int)
        for node in self.graph.nodes.values():
            counts = defaultdict(int)
            for cell in node.memory:
                if cell.owner is not None and cell.opcode != 'DAT':
                    counts[cell.owner] += 1
            if counts:
                max_count = max(counts.values())
                winners = [pid for pid, c in counts.items() if c == max_count]
                if len(winners) == 1:
                    ownership[winners[0]] += 1

        return {
            'winner': winner,
            'winner_name': self.player_names.get(winner, 'None') if winner is not None else 'Draw',
            'method': method,
            'turns': self.turn,
            'node_ownership': dict(ownership),
            'processes': {pid: len(procs) for pid, procs in self.processes.items()},
            'scores': dict(self.scores),
        }
