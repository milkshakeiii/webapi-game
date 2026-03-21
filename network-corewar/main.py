#!/usr/bin/env python3
"""Network CoreWar - main entry point."""

import argparse
import sys
from engine.graph import Graph
from engine.loader import load_program
from engine.match import Match
from engine.instruction import cell_to_str


def dump_node(match, node_id):
    """Print the memory contents of a node."""
    node = match.graph.nodes[node_id]
    print(f"\n  Node {node_id} (edges to: {node.edges}):")
    for i in range(node.size):
        cell = node.read(i)
        owner_str = f"p{cell.owner}" if cell.owner is not None else "  "
        print(f"    [{i:2d}] {owner_str} {cell_to_str(cell)}")


def main():
    parser = argparse.ArgumentParser(description='Network CoreWar')
    parser.add_argument('programs', nargs='+', help='Program files (.ncw)')
    parser.add_argument('--nodes', type=int, default=None, help='Number of graph nodes')
    parser.add_argument('--node-size', type=int, default=16, help='Memory cells per node')
    parser.add_argument('--max-turns', type=int, default=10000, help='Maximum turns')
    parser.add_argument('--topology', choices=['ring', 'grid', 'star', 'complete'],
                        default='ring', help='Graph topology')
    parser.add_argument('--grid-rows', type=int, default=None, help='Grid rows (for grid topology)')
    parser.add_argument('--grid-cols', type=int, default=None, help='Grid cols (for grid topology)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--dump', '-d', action='store_true', help='Dump final node state')
    args = parser.parse_args()

    num_players = len(args.programs)

    # Build graph
    if args.topology == 'ring':
        num_nodes = args.nodes or (4 * num_players)
        graph = Graph.make_ring(num_nodes, args.node_size)
    elif args.topology == 'grid':
        rows = args.grid_rows or (2 * num_players)
        cols = args.grid_cols or (2 * num_players)
        graph = Graph.make_grid(rows, cols, args.node_size)
        num_nodes = rows * cols
    elif args.topology == 'star':
        num_spokes = args.nodes or (3 * num_players)
        graph = Graph.make_star(num_spokes, args.node_size)
        num_nodes = num_spokes + 1
    elif args.topology == 'complete':
        num_nodes = args.nodes or (3 * num_players)
        graph = Graph.make_complete(num_nodes, args.node_size)

    # Load programs and set up match
    match = Match(graph, max_turns=args.max_turns)

    # Determine starting nodes — spread players evenly, topology-aware
    node_ids = sorted(graph.nodes.keys())
    if args.topology == 'star':
        # Place on spokes only (skip center node 0)
        spoke_ids = [nid for nid in node_ids if nid != 0]
        start_nodes = [spoke_ids[(i * len(spoke_ids)) // num_players] for i in range(num_players)]
    elif args.topology == 'grid':
        # Place at maximally distant positions on the torus
        rows = args.grid_rows or (2 * num_players)
        cols = args.grid_cols or (2 * num_players)
        if num_players == 2:
            # Opposite positions on the torus: (0,0) and (rows//2, cols//2)
            start_nodes = [0, (rows // 2) * cols + (cols // 2)]
        else:
            start_nodes = [node_ids[(i * len(node_ids)) // num_players] for i in range(num_players)]
    else:
        start_nodes = [node_ids[(i * len(node_ids)) // num_players] for i in range(num_players)]

    for i, prog_file in enumerate(args.programs):
        name, cells = load_program(prog_file)
        if len(cells) > args.node_size:
            print(f"Error: {prog_file} has {len(cells)} instructions, max is {args.node_size}")
            sys.exit(1)
        match.place_program(i, name, cells, start_nodes[i])
        print(f"Player {i}: {name} -> node {start_nodes[i]} ({len(cells)} instructions)")

    print(f"\nGraph: {num_nodes} nodes, {args.topology} topology, {args.node_size} cells/node")
    print(f"Max turns: {args.max_turns}\n")

    # Run
    winner, results = match.run(verbose=args.verbose)

    # Results
    print(f"\n=== MATCH RESULT ===")
    print(f"Winner: {results['winner_name']} (method: {results['method']})")
    print(f"Turns: {results['turns']}")
    print(f"Node ownership: {results['node_ownership']}")
    print(f"Surviving processes: {results['processes']}")

    if args.dump:
        print(f"\n=== FINAL STATE ===")
        for nid in sorted(graph.nodes):
            dump_node(match, nid)


if __name__ == '__main__':
    main()
