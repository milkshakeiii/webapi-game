#!/usr/bin/env python3
"""Round-robin tournament runner for Network CoreWar."""

import os
import sys
import itertools
from collections import defaultdict
from engine.graph import Graph
from engine.loader import load_program
from engine.match import Match


NODE_SIZE = 128
CYCLES = 2
SCORE_TARGET = 100000
MAX_TURNS = 10000

SCENARIOS = [
    ('ring-8',      lambda: Graph.make_ring(8, NODE_SIZE, CYCLES),             [0, 4]),
    ('ring-16',     lambda: Graph.make_ring(16, NODE_SIZE, CYCLES),            [0, 8]),
    ('grid-4x4',    lambda: Graph.make_grid(4, 4, NODE_SIZE, CYCLES),          [0, 10]),
    ('grid-6x6',    lambda: Graph.make_grid(6, 6, NODE_SIZE, CYCLES),          [0, 21]),
    ('star-8',      lambda: Graph.make_star(8, NODE_SIZE, CYCLES),              [1, 5]),
    ('star-16',     lambda: Graph.make_star(16, NODE_SIZE, CYCLES),             [1, 9]),
    ('random-12-3', lambda: Graph.make_random(12, 3, NODE_SIZE, CYCLES, 42),   [0, 6]),
    ('random-16-5', lambda: Graph.make_random(16, 5, NODE_SIZE, CYCLES, 99),   [0, 8]),
    ('complete-8',  lambda: Graph.make_complete(8, NODE_SIZE, CYCLES),          [0, 4]),
]


def run_match(prog_a, prog_b, scenario):
    """Run a single match. Returns (winner_idx or None, method, scores, turns)."""
    label, make_graph, starts = scenario
    graph = make_graph()

    match = Match(graph, max_turns=MAX_TURNS, score_target=SCORE_TARGET)
    match.place_program(0, prog_a[0], prog_a[1], starts[0])
    match.place_program(1, prog_b[0], prog_b[1], starts[1])

    winner, results = match.run()
    return results['winner'], results['method'], results['scores'], results['turns']


def run_tournament(programs, scenario):
    """Run full round-robin (both sides) on a scenario."""
    names = [p[0] for p in programs]
    wins = defaultdict(int)
    draws = defaultdict(int)
    total_scores = defaultdict(int)
    match_results = []

    for i, j in itertools.combinations(range(len(programs)), 2):
        for first, second in [(i, j), (j, i)]:
            winner, method, scores, turns = run_match(
                programs[first], programs[second], scenario
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
    # Load all warriors from champions and examples
    base = os.path.dirname(os.path.abspath(__file__))
    programs = []
    for subdir in ['champions', 'examples']:
        dirpath = os.path.join(base, subdir)
        if not os.path.isdir(dirpath):
            continue
        for fname in sorted(os.listdir(dirpath)):
            if fname.endswith('.ncw') or fname.endswith('.ncwc'):
                try:
                    name, cells = load_program(os.path.join(dirpath, fname), NODE_SIZE)
                    programs.append((name, cells))
                except Exception as e:
                    print(f"Skipping {fname}: {e}")

    for scenario in SCENARIOS:
        print(f"\n{'='*60}")
        print(f"  SCENARIO: {scenario[0].upper()}")
        print(f"  {len(programs)} warriors, round-robin (both sides), score target {SCORE_TARGET:,}")
        print(f"{'='*60}")

        wins, draws, total_scores, match_results = run_tournament(programs, scenario)

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
