#!/usr/bin/env python3
"""Round-robin tournament runner for Network CoreWar."""

import os
import sys
import itertools
from collections import defaultdict
from engine.graph import Graph
from engine.loader import load_program
from engine.match import Match


def run_match(prog_a, prog_b, topology, node_size=128, cycles=2, score_target=100000, max_turns=10000):
    """Run a single match. Returns (winner_idx or None, method, scores, turns)."""
    if topology == 'ring':
        graph = Graph.make_ring(8, node_size, cycles)
        starts = [0, 4]
    elif topology == 'grid':
        graph = Graph.make_grid(4, 4, node_size, cycles)
        starts = [0, 10]
    elif topology == 'star':
        graph = Graph.make_star(8, node_size, cycles)
        starts = [1, 5]
    elif topology == 'complete':
        graph = Graph.make_complete(6, node_size, cycles)
        starts = [0, 3]

    match = Match(graph, max_turns=max_turns, score_target=score_target)

    name_a, cells_a = prog_a
    name_b, cells_b = prog_b
    match.place_program(0, name_a, cells_a, starts[0])
    match.place_program(1, name_b, cells_b, starts[1])

    winner, results = match.run()
    return results['winner'], results['method'], results['scores'], results['turns']


def run_tournament(programs, topology, node_size=128):
    """Run full round-robin (both sides) on a topology."""
    names = [p[0] for p in programs]
    wins = defaultdict(int)
    draws = defaultdict(int)
    total_scores = defaultdict(int)
    match_results = []

    for i, j in itertools.combinations(range(len(programs)), 2):
        for first, second in [(i, j), (j, i)]:
            winner, method, scores, turns = run_match(
                programs[first], programs[second], topology
            )
            if winner == 0:
                wins[names[first]] += 1
                result_str = f"{names[first]} beats {names[second]}"
            elif winner == 1:
                wins[names[second]] += 1
                result_str = f"{names[second]} beats {names[first]}"
            else:
                draws[names[first]] += 1
                draws[names[second]] += 1
                result_str = f"{names[first]} vs {names[second]} DRAW"

            total_scores[names[first]] += scores.get(0, 0)
            total_scores[names[second]] += scores.get(1, 0)
            match_results.append((result_str, method, turns, scores))

    return wins, draws, total_scores, match_results


def main():
    # Select representative warriors (mix of strategies and sizes)
    base = os.path.dirname(os.path.abspath(__file__))
    warrior_files = [
        os.path.join(base, 'champions', 'apex.ncw'),
        os.path.join(base, 'champions', 'scorpion.ncw'),
        os.path.join(base, 'examples', 'harvester.ncw'),
        os.path.join(base, 'examples', 'warrior.ncw'),
        os.path.join(base, 'examples', 'colonizer.ncw'),
        os.path.join(base, 'examples', 'dwarf.ncw'),
        os.path.join(base, 'examples', 'imp.ncw'),
    ]

    # Load all programs
    programs = []
    for f in warrior_files:
        try:
            name, cells = load_program(f, 128)
            programs.append((name, cells))
        except Exception as e:
            print(f"Skipping {f}: {e}")

    topologies = ['ring', 'grid', 'star', 'complete']

    for topo in topologies:
        print(f"\n{'='*60}")
        print(f"  TOPOLOGY: {topo.upper()}")
        print(f"  8 warriors, round-robin (both sides), score target 100K")
        print(f"{'='*60}")

        wins, draws, total_scores, match_results = run_tournament(programs, topo)

        # Sort by wins descending
        all_names = sorted(set(p[0] for p in programs),
                          key=lambda n: (-wins[n], -total_scores[n]))

        print(f"\n{'Program':<20} {'Size':>5} {'Wins':>5} {'Draws':>6} {'TotalScore':>12}")
        print(f"{'-'*20} {'-'*5} {'-'*5} {'-'*6} {'-'*12}")
        for name in all_names:
            size = len([c for n, c in programs if n == name][0])
            print(f"{name:<20} {size:>5} {wins[name]:>5} {draws[name]:>6} {total_scores[name]:>12}")

        # Show individual match results
        print(f"\nMatch details:")
        for result, method, turns, scores in match_results:
            score_str = f"({scores.get(0,0)} vs {scores.get(1,0)})"
            print(f"  {result:<45} {method:<15} T{turns:<6} {score_str}")


if __name__ == '__main__':
    main()
