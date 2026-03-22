"""Graph, Node, and Cell data structures for Network CoreWar."""


class Cell:
    """A single memory cell holding one instruction."""

    __slots__ = ('opcode', 'a_mode', 'a_value', 'b_mode', 'b_value', 'owner')

    def __init__(self, opcode='DAT', a_mode='#', a_value=0, b_mode='#', b_value=0, owner=None):
        self.opcode = opcode
        self.a_mode = a_mode
        self.a_value = a_value
        self.b_mode = b_mode
        self.b_value = b_value
        self.owner = owner

    def copy(self, new_owner=None):
        return Cell(self.opcode, self.a_mode, self.a_value, self.b_mode, self.b_value,
                    new_owner if new_owner is not None else self.owner)

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        return (self.opcode == other.opcode and self.a_mode == other.a_mode and
                self.a_value == other.a_value and self.b_mode == other.b_mode and
                self.b_value == other.b_value)

    def __repr__(self):
        return f"{self.opcode} {self.a_mode}{self.a_value}, {self.b_mode}{self.b_value}"


class Node:
    """A graph node with a circular memory array."""

    def __init__(self, node_id, size=16, cycles=4):
        self.node_id = node_id
        self.size = size
        self.cycles = cycles  # max execution cycles per turn
        self.cycles_remaining = cycles  # reset each turn
        self.memory = [Cell() for _ in range(size)]
        self.edges = []  # list of neighbor_node_ids
        self.recv_buffers = {}  # edge_index -> Cell or None

    def read(self, address):
        return self.memory[address % self.size]

    def write(self, address, cell):
        self.memory[address % self.size] = cell


class Graph:
    """A network of nodes connected by edges."""

    def __init__(self):
        self.nodes = {}  # node_id -> Node

    def add_node(self, node_id, size=16, cycles=4):
        node = Node(node_id, size, cycles)
        self.nodes[node_id] = node
        return node

    def add_edge(self, id_a, id_b):
        node_a = self.nodes[id_a]
        node_b = self.nodes[id_b]
        edge_idx_a = len(node_a.edges)
        edge_idx_b = len(node_b.edges)
        node_a.edges.append(id_b)
        node_b.edges.append(id_a)
        node_a.recv_buffers[edge_idx_a] = None
        node_b.recv_buffers[edge_idx_b] = None

    def neighbor(self, node_id, edge_index):
        """Get neighbor node ID by edge index. Returns None if invalid."""
        node = self.nodes[node_id]
        if 0 <= edge_index < len(node.edges):
            return node.edges[edge_index]
        return None

    def send_to_edge(self, from_node_id, edge_index, cell):
        """Send a cell across an edge. Writes to the neighbor's recv buffer for this edge."""
        neighbor_id = self.neighbor(from_node_id, edge_index)
        if neighbor_id is None:
            return False
        neighbor = self.nodes[neighbor_id]
        # Find which edge index on the neighbor points back to from_node_id
        for idx, nid in enumerate(neighbor.edges):
            if nid == from_node_id:
                neighbor.recv_buffers[idx] = cell
                return True
        return False

    def recv_from_edge(self, node_id, edge_index):
        """Receive a cell from an edge's buffer. Returns Cell or None. Clears buffer."""
        node = self.nodes[node_id]
        if edge_index not in node.recv_buffers:
            return None
        cell = node.recv_buffers[edge_index]
        node.recv_buffers[edge_index] = None
        return cell

    def _init_recv_buffers(self):
        """Initialize recv buffers for all nodes based on their edge count."""
        for node in self.nodes.values():
            node.recv_buffers = {i: None for i in range(len(node.edges))}

    @staticmethod
    def make_ring(num_nodes, node_size=16, cycles=4):
        """Create a ring topology with consistent edge ordering.

        Every node has edge 0 = clockwise (next) and edge 1 = counter-clockwise (prev).
        This ensures FORK #0 always means 'forward' regardless of starting position.
        """
        g = Graph()
        for i in range(num_nodes):
            g.add_node(i, node_size, cycles)
        for i in range(num_nodes):
            node = g.nodes[i]
            cw = (i + 1) % num_nodes
            ccw = (i - 1) % num_nodes
            node.edges = [cw, ccw]
        g._init_recv_buffers()
        return g

    @staticmethod
    def make_grid(rows, cols, node_size=16, cycles=4):
        """Create a toroidal grid topology.

        Wraps around both axes so every node has exactly 4 edges.
        Consistent ordering: edge 0=right, 1=down, 2=left, 3=up.
        This ensures FORK #0 always means 'right' regardless of position.
        """
        g = Graph()
        for r in range(rows):
            for c in range(cols):
                g.add_node(r * cols + c, node_size, cycles)
        for r in range(rows):
            for c in range(cols):
                nid = r * cols + c
                node = g.nodes[nid]
                right = r * cols + (c + 1) % cols
                down = ((r + 1) % rows) * cols + c
                left = r * cols + (c - 1) % cols
                up = ((r - 1) % rows) * cols + c
                node.edges = [right, down, left, up]
        g._init_recv_buffers()
        return g

    @staticmethod
    def make_star(num_spokes, node_size=16, cycles=4):
        """Create a star topology: one center node connected to all spoke nodes.

        Center is node 0. Spoke nodes are 1..num_spokes.
        Center has edges [1, 2, ..., num_spokes].
        Each spoke has one edge: [0] (back to center).
        Total nodes = num_spokes + 1.
        """
        g = Graph()
        g.add_node(0, node_size, cycles)  # center
        for i in range(1, num_spokes + 1):
            g.add_node(i, node_size, cycles)
        # Center connects to all spokes
        g.nodes[0].edges = list(range(1, num_spokes + 1))
        # Each spoke connects back to center
        for i in range(1, num_spokes + 1):
            g.nodes[i].edges = [0]
        g._init_recv_buffers()
        return g

    @staticmethod
    def make_random(num_nodes, avg_degree, node_size=16, cycles=4, seed=None):
        """Create a random connected graph with approximately avg_degree edges per node.

        Uses Erdos-Renyi model with edge probability tuned to the target average degree,
        then ensures connectivity by adding edges along a random spanning path.
        """
        import random
        rng = random.Random(seed)

        g = Graph()
        for i in range(num_nodes):
            g.add_node(i, node_size, cycles)

        # Ensure connectivity: random permutation, connect consecutive nodes
        perm = list(range(num_nodes))
        rng.shuffle(perm)
        connected_edges = set()
        for k in range(len(perm) - 1):
            a, b = min(perm[k], perm[k+1]), max(perm[k], perm[k+1])
            connected_edges.add((a, b))

        # Add random edges to reach target average degree
        # avg_degree = 2 * num_edges / num_nodes => target_edges = avg_degree * num_nodes / 2
        target_edges = int(avg_degree * num_nodes / 2)
        all_possible = [(i, j) for i in range(num_nodes) for j in range(i+1, num_nodes)]
        rng.shuffle(all_possible)
        edges = set(connected_edges)
        for a, b in all_possible:
            if len(edges) >= target_edges:
                break
            edges.add((a, b))

        # Build adjacency and shuffle edge order per node for variety
        adj = {i: [] for i in range(num_nodes)}
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        for i in range(num_nodes):
            rng.shuffle(adj[i])
            g.nodes[i].edges = adj[i]

        g._init_recv_buffers()
        return g

    @staticmethod
    def make_complete(num_nodes, node_size=16, cycles=4):
        """Create a complete graph where every node connects to every other.

        Each node's edges are ordered by node ID (excluding self).
        """
        g = Graph()
        for i in range(num_nodes):
            g.add_node(i, node_size, cycles)
        for i in range(num_nodes):
            g.nodes[i].edges = [j for j in range(num_nodes) if j != i]
        g._init_recv_buffers()
        return g
