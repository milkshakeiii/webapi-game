#!/usr/bin/env python3
"""Submit a warrior to the Network CoreWar challenge.

Usage: python3 submit.py <your_warrior.ncw>

Your warrior faces the full field (champions + example warriors) in a
round-robin tournament across ring, grid, and star topologies. You're
rated based on where you place.
"""

import os
import sys
from collections import defaultdict
from engine.graph import Graph
from engine.loader import load_program
from engine.match import Match

BASE = os.path.dirname(os.path.abspath(__file__))
NODE_SIZE = 128
CYCLES = 2
SCORE_TARGET = 100000
MAX_TURNS = 10000

# Rating tiers based on win percentage in the tournament
TIERS = [
    (90, "Grandmaster", "Dominant. You've mastered Network CoreWar."),
    (75, "Master",      "Excellent. You outperform most champions."),
    (60, "Diamond",     "Strong. Competitive with the top warriors."),
    (45, "Gold",        "Solid. You can hold your own in battle."),
    (30, "Silver",      "Decent. You understand the basics."),
    (15, "Bronze",      "Getting there. Study the examples and SPEC."),
    (0,  "Novice",      "Keep iterating! Read SPEC.md and study examples/."),
]


# Each scenario is (label, topology, graph_factory, start_nodes)
SCENARIOS = [
    ('ring-8',      'ring',   lambda: Graph.make_ring(8, NODE_SIZE, CYCLES),             [0, 4]),
    ('ring-16',     'ring',   lambda: Graph.make_ring(16, NODE_SIZE, CYCLES),            [0, 8]),
    ('grid-4x4',    'grid',   lambda: Graph.make_grid(4, 4, NODE_SIZE, CYCLES),          [0, 10]),
    ('grid-6x6',    'grid',   lambda: Graph.make_grid(6, 6, NODE_SIZE, CYCLES),          [0, 21]),
    ('star-8',      'star',   lambda: Graph.make_star(8, NODE_SIZE, CYCLES),              [1, 5]),
    ('star-16',     'star',   lambda: Graph.make_star(16, NODE_SIZE, CYCLES),             [1, 9]),
    ('random-12-3', 'random', lambda: Graph.make_random(12, 3, NODE_SIZE, CYCLES, 42),   [0, 6]),
    ('random-16-5', 'random', lambda: Graph.make_random(16, 5, NODE_SIZE, CYCLES, 99),   [0, 8]),
    ('complete-8',  'complete', lambda: Graph.make_complete(8, NODE_SIZE, CYCLES),        [0, 4]),
]


def run_match(prog_a, prog_b, scenario):
    """Run a single match. Returns (winner_idx or None, method, scores, turns)."""
    label, topo, make_graph, starts = scenario
    graph = make_graph()

    match = Match(graph, max_turns=MAX_TURNS, score_target=SCORE_TARGET)
    match.place_program(0, prog_a[0], prog_a[1], starts[0])
    match.place_program(1, prog_b[0], prog_b[1], starts[1])
    _, results = match.run()
    return results['winner'], results['method'], results['scores'], results['turns']


def load_field():
    """Load all champions and example warriors. Returns (field, champion_names)."""
    field = []
    champion_names = set()
    for subdir in ['champions', 'examples']:
        dirpath = os.path.join(BASE, subdir)
        if not os.path.isdir(dirpath):
            continue
        for fname in sorted(os.listdir(dirpath)):
            if fname.endswith('.ncw') or fname.endswith('.ncwc'):
                path = os.path.join(dirpath, fname)
                name, cells = load_program(path, NODE_SIZE)
                field.append((name, cells))
                if subdir == 'champions':
                    champion_names.add(name)
    return field, champion_names


def get_tier(win_pct):
    """Return (tier_name, description) for a win percentage."""
    for threshold, name, desc in TIERS:
        if win_pct >= threshold:
            return name, desc
    return TIERS[-1][1], TIERS[-1][2]


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 submit.py <your_warrior.ncw>")
        print()
        print("Write a warrior that competes in a round-robin tournament.")
        print("See README.md for the challenge and SPEC.md for the rules.")
        sys.exit(1)

    warrior_path = sys.argv[1]
    if not os.path.exists(warrior_path):
        print(f"Error: file not found: {warrior_path}")
        sys.exit(1)

    # Load the submission
    try:
        player_name, player_cells = load_program(warrior_path, NODE_SIZE)
    except Exception as e:
        print(f"Error loading {warrior_path}: {e}")
        sys.exit(1)

    if len(player_cells) > NODE_SIZE:
        print(f"Error: program has {len(player_cells)} instructions, max is {NODE_SIZE}")
        sys.exit(1)

    player = (player_name, player_cells)

    # Load the full field
    field, champion_names = load_field()
    all_programs = [player] + field
    names = [p[0] for p in all_programs]

    # Deduplicate if player name collides with a field warrior
    if names[0] in names[1:]:
        names[0] = f"{names[0]} (you)"
        player_name = names[0]

    scenario_labels = [s[0] for s in SCENARIOS]

    print(f"  Network CoreWar Challenge")
    print(f"  Warrior: {player_name} ({len(player_cells)} instructions)")
    print(f"  Field: {len(field)} opponents")
    print(f"  Scenarios: {', '.join(scenario_labels)}")
    print(f"  Settings: {NODE_SIZE} cells/node, {CYCLES} cycles/node, target {SCORE_TARGET:,}")
    print()

    # Run player vs every opponent across scenarios (both sides)
    wins = defaultdict(int)
    losses = defaultdict(int)
    draws = defaultdict(int)
    # Track head-to-head vs champions specifically
    h2h = defaultdict(lambda: {'w': 0, 'l': 0, 'd': 0})

    for scenario in SCENARIOS:
        print(f"--- {scenario[0].upper()} ---")
        for j in range(1, len(all_programs)):
            for first, second, p_pos in [(0, j, 0), (j, 0, 1)]:
                winner, method, scores, turns = run_match(
                    all_programs[first], all_programs[second], scenario
                )
                opp_name = names[j]
                s0 = scores.get(0, 0)
                s1 = scores.get(1, 0)

                is_champ = opp_name in champion_names
                if (winner == 0 and p_pos == 0) or (winner == 1 and p_pos == 1):
                    wins[opp_name] += 1
                    w_name = player_name
                    if is_champ:
                        h2h[opp_name]['w'] += 1
                elif winner is None:
                    draws[opp_name] += 1
                    w_name = "DRAW"
                    if is_champ:
                        h2h[opp_name]['d'] += 1
                else:
                    losses[opp_name] += 1
                    w_name = opp_name
                    if is_champ:
                        h2h[opp_name]['l'] += 1

                print(f"  {names[first]:>15} vs {names[second]:<15} -> {w_name:<15} ({method}, T{turns}, {s0:>7}-{s1:<7})")
        print()

    # Calculate player stats
    total_w = sum(wins.values())
    total_l = sum(losses.values())
    total_d = sum(draws.values())
    total_matches = total_w + total_l + total_d
    player_pct = (100 * total_w / total_matches) if total_matches > 0 else 0

    # Results table
    print("=== RESULTS ===")
    print(f"{'Opponent':<20} {'W':>4} {'L':>4} {'D':>4}")
    print(f"{'-'*20} {'-'*4} {'-'*4} {'-'*4}")
    for name in sorted(names[1:], key=lambda n: -(wins[n] - losses[n])):
        champ_marker = " *" if name in champion_names else ""
        print(f"{name:<20} {wins[name]:>4} {losses[name]:>4} {draws[name]:>4}{champ_marker}")
    print(f"{'-'*20} {'-'*4} {'-'*4} {'-'*4}")
    print(f"{'TOTAL':<20} {total_w:>4} {total_l:>4} {total_d:>4}")
    print()
    print("  * = champion")

    # Rating
    tier_name, tier_desc = get_tier(player_pct)
    print()
    print(f"=== RATING: {tier_name.upper()} ({player_pct:.0f}% win rate) ===")
    print(f"{tier_desc}")

    # Check head-to-head vs each champion
    beat_all = True
    print()
    print("=== vs CHAMPIONS ===")
    for cn in sorted(champion_names):
        record = h2h[cn]
        status = "AHEAD" if record['w'] > record['l'] else ("TIED" if record['w'] == record['l'] else "BEHIND")
        print(f"  vs {cn}: {record['w']}W {record['l']}L {record['d']}D  [{status}]")
        if record['w'] <= record['l']:
            beat_all = False

    print()
    if beat_all:
        print(f"CHALLENGE COMPLETE! {player_name} holds a winning record against all champions!")
    else:
        print(f"Not yet. You need a winning head-to-head record against each champion.")
        print(f"Keep iterating! See examples/ for reference and SPEC.md for the rules.")

    sys.exit(0)


if __name__ == '__main__':
    main()
