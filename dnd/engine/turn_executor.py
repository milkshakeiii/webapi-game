"""Execute a TurnIntent against the live encounter state.

Walks the slot fills in PF1 order and resolves each: movement updates
positions on the grid (and triggers AoOs from leaving threatened
squares), attack actions run through ``combat.resolve_attack``, etc.

The executor returns a structured log of events that the encounter
appends to its trace.

Currently supports the actions needed for the level-1 fighter vs.
goblin demo: ``attack``, ``charge``, ``full_attack``, ``move_to``,
``move_toward``, ``move_away``, ``5ft_step``, ``withdraw``, ``hold``.
Other vocab actions (cast, drink, class abilities) raise
``NotImplementedError`` for now and will be added incrementally.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .combat import (
    AttackOutcome,
    AttackProfile,
    DefenseProfile,
    resolve_attack,
)
from .combatant import Combatant
from .dice import Roller
from .dsl import TurnIntent, evaluate
from .encounter import Encounter, aoo_triggers_for_movement
from .grid import Grid
from .modifiers import Modifier, compute as _compute_mod
from .modifiers import compute_with_context as _compute_mod_ctx


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass
class TurnEvent:
    """One event during a turn — an attack, a move, an AoO, etc."""

    actor_id: str
    kind: str             # "attack", "move", "aoo", "skip", etc.
    detail: dict


@dataclass
class TurnResult:
    actor_id: str
    rule_index: int | None
    events: list[TurnEvent]

    def to_dict(self) -> dict:
        return {
            "actor_id": self.actor_id,
            "rule_index": self.rule_index,
            "events": [{"actor_id": e.actor_id, "kind": e.kind,
                        "detail": e.detail} for e in self.events],
        }


# ---------------------------------------------------------------------------
# Top-level entry
# ---------------------------------------------------------------------------


def execute_turn(
    actor: Combatant,
    intent: TurnIntent | None,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
) -> TurnResult:
    """Execute the actor's turn against the encounter state."""
    rule_index = intent.rule_index if intent else None
    events: list[TurnEvent] = []

    if intent is None or "composite" in intent.do and intent.do["composite"] == "hold":
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "no rule matched" if intent is None else "hold"}))
        return TurnResult(actor.id, rule_index, events)

    do = intent.do
    ns = intent.namespace

    # Free actions first.
    for fa in do.get("free", []) or []:
        fa_type = fa.get("type") if isinstance(fa, dict) else None
        if fa_type == "fall_prone":
            if "prone" not in actor.conditions:
                actor.add_condition("prone")
            events.append(TurnEvent(actor.id, "fall_prone", {}))
        else:
            events.append(TurnEvent(actor.id, "free",
                                    {"action": fa}))

    # Swift action.
    swift = do.get("swift")
    if swift is not None:
        events.append(TurnEvent(actor.id, "swift",
                                {"action": swift,
                                 "note": "swift not yet implemented"}))

    # Composite or slot form?
    if "composite" in do:
        _execute_composite(actor, do["composite"], do.get("args", {}),
                           encounter, grid, roller, ns, events)
    else:
        slots = do.get("slots") or do
        _execute_slots(actor, slots, encounter, grid, roller, ns, events)

    return TurnResult(actor.id, rule_index, events)


# ---------------------------------------------------------------------------
# Composite dispatchers
# ---------------------------------------------------------------------------


def _execute_composite(
    actor: Combatant,
    composite: str,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    if composite == "hold":
        events.append(TurnEvent(actor.id, "skip", {"reason": "hold"}))
        return
    if composite == "charge":
        _do_charge(actor, args, encounter, grid, roller, ns, events)
        return
    if composite == "full_attack":
        target = _resolve_target(args.get("target"), ns)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "full_attack: no target resolved"}))
            return
        _do_full_attack(actor, target, args.get("options") or {},
                        grid, roller, events, encounter=encounter)
        return
    if composite == "withdraw":
        _do_withdraw(actor, args, encounter, grid, events)
        return
    if composite == "cast":
        _do_cast(actor, args, encounter, grid, roller, ns, events)
        return
    if composite == "cleave":
        _do_cleave(actor, args, encounter, grid, roller, ns, events)
        return
    if composite == "rage_start":
        _do_rage_start(actor, args, encounter, events)
        return
    if composite == "rage_end":
        _do_rage_end(actor, events)
        return
    if composite == "smite_evil":
        _do_smite_evil(actor, args, encounter, grid, ns, events)
        return
    if composite == "channel_energy":
        _do_channel_energy(actor, args, encounter, grid, roller, ns, events)
        return
    if composite == "bardic_performance":
        _do_bardic_performance(actor, args, encounter, grid, ns, events)
        return
    if composite == "stunning_fist":
        _do_stunning_fist(actor, args, encounter, grid, roller, ns, events)
        return
    if composite == "aid_another":
        _do_aid_another(actor, args, encounter, grid, roller, ns, events)
        return
    raise NotImplementedError(f"composite action {composite!r} not yet implemented")


def _execute_slots(
    actor: Combatant,
    slots: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Execute slot-based turn (standard + move + 5ft step)."""
    # Move first (most common for "approach and attack" patterns).
    move = slots.get("move")
    if move is not None:
        _do_move_action(actor, move, encounter, grid, ns, events)

    # 5ft step.
    five = slots.get("five_foot_step")
    if five is not None:
        _do_5ft_step(actor, five, grid, ns, events)

    # Standard action.
    std = slots.get("standard")
    if std is not None:
        _do_standard(actor, std, grid, roller, ns, events, encounter=encounter)


# ---------------------------------------------------------------------------
# Movement primitives
# ---------------------------------------------------------------------------


def _do_move_action(
    actor: Combatant,
    move: dict,
    encounter: Encounter,
    grid: Grid,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    mtype = move.get("type")
    speed_squares = actor.speed // 5
    if mtype == "move_to":
        target = _resolve_target(move.get("target"), ns)
        dest = _coerce_square(target)
        if dest is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "move_to: no destination"}))
            return
        _move_along(actor, dest, speed_squares, grid, events, encounter=encounter)
    elif mtype == "move_toward":
        target = _resolve_target(move.get("target"), ns)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "move_toward: no target"}))
            return
        dest = _square_toward(actor, target, speed_squares, grid)
        _move_along(actor, dest, speed_squares, grid, events, encounter=encounter)
    elif mtype == "move_away":
        target = _resolve_target(move.get("target"), ns)
        if target is None:
            return
        dest = _square_away(actor, target, speed_squares, grid)
        _move_along(actor, dest, speed_squares, grid, events, encounter=encounter)
    elif mtype == "stand_up":
        if "prone" in actor.conditions:
            # PF1: standing up provokes AoOs from threateners.
            from .encounter import aoo_triggers_for_provoking_action
            for threatener in aoo_triggers_for_provoking_action(
                grid, actor, "stand_up",
            ):
                _do_aoo(threatener, actor, grid, events, encounter=encounter)
                if not actor.is_alive() or actor.current_hp <= -10:
                    events.append(TurnEvent(actor.id, "skip",
                                            {"reason": "killed by AoO"}))
                    return
            actor.remove_condition("prone")
            events.append(TurnEvent(actor.id, "stand_up", {}))
    elif mtype == "draw_weapon":
        events.append(TurnEvent(actor.id, "draw_weapon",
                                {"weapon": move.get("weapon")}))
    else:
        raise NotImplementedError(f"move action {mtype!r} not implemented")


def _do_5ft_step(
    actor: Combatant,
    target: tuple[int, int] | str,
    grid: Grid,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    if isinstance(target, str):
        # Named direction like "north", or expression evaluated to square.
        target = _coerce_square(target) or _direction_to_square(actor, target)
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "5ft_step: invalid target"}))
        return
    old = actor.position
    try:
        grid.move(actor, target)  # type: ignore[arg-type]
        events.append(TurnEvent(actor.id, "move",
                                {"kind": "5ft_step", "from": old, "to": target}))
    except Exception as e:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"5ft_step blocked: {e}"}))


def _move_along(
    actor: Combatant,
    dest: tuple[int, int] | None,
    max_squares: int,
    grid: Grid,
    events: list[TurnEvent],
    encounter=None,
) -> None:
    if dest is None or dest == actor.position:
        return
    # Step-by-step movement with obstacle routing. AoO triggered when
    # leaving a threatened square.
    cur = actor.position
    steps_taken = 0
    while steps_taken < max_squares and cur != dest:
        next_step = _step_toward_passable(cur, dest, grid)
        if next_step == cur:
            break  # truly blocked — no passable neighbor closer to dest
        # AoO check: is the actor leaving a square threatened by hostiles?
        triggers = aoo_triggers_for_movement(grid, actor, cur)
        for threatener in triggers:
            _do_aoo(threatener, actor, grid, events, encounter=encounter)
            if not actor.is_alive() or actor.current_hp <= -10:
                events.append(TurnEvent(actor.id, "skip",
                                        {"reason": "killed by AoO"}))
                return
        # Commit the step.
        try:
            grid.move(actor, next_step)
        except Exception as e:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": f"move blocked: {e}"}))
            return
        events.append(TurnEvent(actor.id, "move",
                                {"kind": "step", "from": cur, "to": next_step}))
        cur = next_step
        steps_taken += 1


def _step_toward(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    """Naive step toward b — no grid awareness, no obstacle handling."""
    dx = (b[0] > a[0]) - (b[0] < a[0])
    dy = (b[1] > a[1]) - (b[1] < a[1])
    return (a[0] + dx, a[1] + dy)


def _step_toward_passable(
    a: tuple[int, int],
    b: tuple[int, int],
    grid: Grid,
    blocked: set[tuple[int, int]] | None = None,
) -> tuple[int, int]:
    """Pick the best passable adjacent square that brings us closer to b.

    Considers all 8 neighbors. Prefers the one with the smallest PF1
    grid distance to ``b``; ties broken by Euclidean distance (so true
    diagonals win when they're geometrically closer). If no neighbor is
    passable, returns ``a`` (caller should treat as blocked).

    ``blocked`` is an optional set of squares the caller wants treated
    as impassable beyond what ``grid.is_passable`` reports (useful for
    avoiding other combatants on the same path).
    """
    if a == b:
        return a
    blocked = blocked or set()
    candidates: list[tuple[int, float, tuple[int, int]]] = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = a[0] + dx, a[1] + dy
            if not grid.in_bounds(nx, ny):
                continue
            if (nx, ny) in blocked:
                continue
            if not grid.is_passable(nx, ny):
                continue
            grid_d = grid.distance_squares((nx, ny), b)
            euclid_sq = (b[0] - nx) ** 2 + (b[1] - ny) ** 2
            candidates.append((grid_d, euclid_sq, (nx, ny)))
    if not candidates:
        return a
    candidates.sort()
    return candidates[0][2]


def _square_toward(
    actor: Combatant, target: Any, max_squares: int, grid: Grid,
) -> tuple[int, int]:
    """Find a square within max_squares of actor's position, toward target.

    Uses passable-aware stepping: routes around obstacles by preferring
    the neighbor with the smallest grid-distance to the target. Stops
    when no step strictly reduces the distance (i.e., already adjacent
    or stuck), and never lands on the target square.
    """
    if hasattr(target, "position"):
        tpos = target.position
    elif isinstance(target, tuple):
        tpos = target
    else:
        return actor.position
    cur = actor.position
    cur_dist = grid.distance_squares(cur, tpos)
    for _ in range(max_squares):
        nxt = _step_toward_passable(cur, tpos, grid)
        if nxt == cur:
            break
        nxt_dist = grid.distance_squares(nxt, tpos)
        if nxt_dist >= cur_dist:
            break  # no closer than where we are
        if nxt_dist == 0:
            break  # would land on the target itself
        cur = nxt
        cur_dist = nxt_dist
    return cur


def _square_away(
    actor: Combatant, target: Any, max_squares: int, grid: Grid,
) -> tuple[int, int]:
    """Find a square within max_squares, moving away from target."""
    if hasattr(target, "position"):
        tpos = target.position
    elif isinstance(target, tuple):
        tpos = target
    else:
        return actor.position
    cur = actor.position
    for _ in range(max_squares):
        # Step in the direction opposite of target.
        dx = (cur[0] > tpos[0]) - (cur[0] < tpos[0])
        dy = (cur[1] > tpos[1]) - (cur[1] < tpos[1])
        nxt = (cur[0] + dx, cur[1] + dy)
        if nxt == cur:
            break
        if not grid.in_bounds(*nxt) or not grid.is_passable(*nxt):
            break
        cur = nxt
    return cur


def _direction_to_square(actor: Combatant, direction: str) -> tuple[int, int] | None:
    deltas = {
        "north": (0, -1), "south": (0, 1),
        "east": (1, 0),   "west": (-1, 0),
        "northeast": (1, -1), "northwest": (-1, -1),
        "southeast": (1, 1),  "southwest": (-1, 1),
    }
    d = deltas.get(direction)
    if d is None:
        return None
    return (actor.position[0] + d[0], actor.position[1] + d[1])


# ---------------------------------------------------------------------------
# Standard / full-round actions
# ---------------------------------------------------------------------------


def _do_standard(
    actor: Combatant,
    std: dict,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
    encounter=None,
) -> None:
    stype = std.get("type")
    if stype == "attack":
        target = _resolve_target(std.get("target"), ns)
        if target is None:
            events.append(TurnEvent(actor.id, "skip",
                                    {"reason": "attack: no target"}))
            return
        _do_attack(actor, target, grid, roller, events,
                   encounter=encounter,
                   script_options=std.get("options") or {})
    elif stype == "total_defense":
        # PF1 RAW: standard action; +4 dodge AC for one round; can't
        # attack. The dodge bonus expires at the start of the actor's
        # next turn (current_round + 1).
        cur_round = encounter.round_number if encounter else 1
        src = "total_defense"
        actor.modifiers.remove_by_source(src)
        actor.modifiers.add(Modifier(
            value=4, type="dodge", target="ac",
            source=src, expires_round=cur_round + 1,
        ))
        events.append(TurnEvent(actor.id, "total_defense", {
            "ac_bonus": 4, "expires_round": cur_round + 1,
        }))
    elif stype == "cast":
        _do_cast(actor, std, encounter, grid, roller, ns, events)
    else:
        raise NotImplementedError(f"standard action {stype!r} not implemented")


def _do_charge(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """PF1 charge action.

    Rules enforced here:
      * Must have a valid target.
      * Must start at least 2 squares (10 ft) from the target — can't
        charge from melee.
      * Path must be a straight line along one of the 8 cardinal /
        diagonal axes (PF1 RAW: "directly toward the designated
        opponent").
      * No allies, enemies, or impassable cells in the charge lane —
        the actor walks in a straight line and stops if any cell on
        the line is blocked.
      * Must actually move at least 2 squares.
      * Must end adjacent to the target.
      * On success: +2 to attack (the -2 AC penalty is not modeled as
        a separate debuff in v1).

    Not yet enforced: difficult terrain in the lane (engine doesn't
    model terrain types yet — when it does, ``_charge_path_clear``
    will need a "no difficult cells" check).
    """
    target = _resolve_target(args.get("target"), ns)
    if target is None:
        events.append(TurnEvent(actor.id, "skip", {"reason": "charge: no target"}))
        return

    # PF1: charge requires moving at least 2 squares. If we're already
    # within 1 square of the target, charging is illegal.
    start_distance = grid.distance_between(actor, target)
    if start_distance < 2:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "charge: target too close — already in melee "
                      "(must start >= 2 squares from target)",
            "distance": start_distance,
        }))
        return

    speed_squares = actor.speed // 5
    charge_squares = speed_squares * 2  # charge = up to 2x speed

    line = _straight_line_charge_path(
        actor.position, target.position, charge_squares, grid,
    )
    if line is None:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "charge: target not on a straight line "
                      "(must be along an orthogonal or diagonal axis "
                      "within charge range)",
        }))
        return

    path_cells = line[1:]  # everything after the start position
    if not _charge_path_clear(path_cells, grid, mover=actor):
        events.append(TurnEvent(actor.id, "skip", {
            "reason": "charge: path blocked (impassable terrain or "
                      "another combatant in the lane)",
        }))
        return

    # Walk the straight-line path one cell at a time. AoOs trigger as
    # the actor leaves each square, just like normal movement.
    start_pos = actor.position
    prev = start_pos
    for next_cell in path_cells:
        triggers = aoo_triggers_for_movement(grid, actor, prev)
        for threatener in triggers:
            _do_aoo(threatener, actor, grid, events, encounter=encounter)
            if not actor.is_alive() or actor.current_hp <= -10:
                events.append(TurnEvent(actor.id, "skip",
                                        {"reason": "killed by AoO"}))
                return
        try:
            grid.move(actor, next_cell)
        except Exception as e:
            events.append(TurnEvent(actor.id, "skip", {
                "reason": f"charge: move blocked mid-path: {e}",
            }))
            return
        events.append(TurnEvent(actor.id, "move", {
            "kind": "charge_step", "from": prev, "to": next_cell,
        }))
        prev = next_cell

    moved_squares = grid.distance_squares(start_pos, actor.position)
    if moved_squares < 2:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": f"charge: moved only {moved_squares} square(s); "
                      f"minimum 2",
            "from": list(start_pos),
            "to": list(actor.position),
        }))
        return

    if not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "charge: target not adjacent after move"}))
        return
    _do_attack(actor, target, grid, roller, events,
               attack_bonus_delta=2, label="charge_attack",
               encounter=encounter,
               script_options=args.get("options") or {})


def _straight_line_charge_path(
    start: tuple[int, int],
    target_pos: tuple[int, int],
    max_steps: int,
    grid: Grid,
) -> list[tuple[int, int]] | None:
    """Compute the straight-line cells the charger walks, or ``None``.

    PF1 charge requires the actor to move "directly toward" the target.
    We interpret that as: the displacement from the start to the
    destination square (which sits adjacent to the target) must be a
    positive integer multiple of one of the 8 unit directions
    (orthogonal or diagonal).

    Returns the full path *including* the start cell. ``path[0]`` is
    ``start``; ``path[-1]`` is the cell adjacent to ``target_pos``
    that the actor ends on. Returns ``None`` if no valid line exists
    or if the line exceeds ``max_steps``.
    """
    sx, sy = start
    tx, ty = target_pos
    dx_total = tx - sx
    dy_total = ty - sy
    if dx_total == 0 and dy_total == 0:
        return None
    # Straight-line constraint: displacement is n * (ux, uy) with
    # ux, uy ∈ {-1, 0, 1}. Equivalent: orthogonal (one of dx/dy is 0)
    # OR pure diagonal (|dx| == |dy|).
    if dx_total != 0 and dy_total != 0 and abs(dx_total) != abs(dy_total):
        return None
    ux = (dx_total > 0) - (dx_total < 0)
    uy = (dy_total > 0) - (dy_total < 0)
    # Steps to reach a cell adjacent to target along this line.
    n_steps = max(abs(dx_total), abs(dy_total)) - 1
    if n_steps < 1:
        return None
    if n_steps > max_steps:
        return None
    path: list[tuple[int, int]] = [start]
    for i in range(1, n_steps + 1):
        cell = (sx + i * ux, sy + i * uy)
        if not grid.in_bounds(*cell):
            return None
        path.append(cell)
    return path


def _charge_path_clear(
    cells: list[tuple[int, int]],
    grid: Grid,
    *,
    mover: Combatant,
) -> bool:
    """All cells in ``cells`` must be passable and unoccupied (other
    than by ``mover``).

    Difficult terrain would also disqualify a cell per PF1, but the
    engine doesn't model terrain types yet — when it does, add the
    check here.
    """
    for cell in cells:
        if not grid.is_passable(*cell):
            return False
        for c in grid.combatants.values():
            if c.id == mover.id:
                continue
            if c.position == cell:
                return False
    return True


def _iterative_attack_count(bab: int) -> int:
    """Number of iterative attacks PF1 grants at this BAB.

    PF1 RAW: 1 attack at BAB 0-5, 2 at 6-10, 3 at 11-15, 4 at 16+.
    Always at least 1 even at BAB 0 (everyone gets a single attack).
    Each iterative beyond the first takes an additional -5 cumulative.
    """
    return max(1, (bab - 1) // 5 + 1)


def _do_full_attack(
    actor: Combatant,
    target: Combatant,
    options: dict,
    grid: Grid,
    roller: Roller,
    events: list[TurnEvent],
    encounter=None,
) -> None:
    # Adjacency only required for melee weapons. Ranged full attacks
    # (e.g., a longbow user) can fire from any range; range increments
    # apply per-attack.
    primary_is_ranged = (
        bool(actor.attack_options)
        and actor.attack_options[0].get("type") == "ranged"
    )
    if not primary_is_ranged and not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "full_attack: target not in melee"}))
        return
    bab = actor.bases.get("bab", 0)
    # Per-attack delta sequence. Default iteratives are at -5, -10, etc.
    # Rapid Shot inserts an extra attack at top BAB and applies -2 to
    # every attack in this round (PF1 RAW). Only valid with ranged
    # weapons and the Rapid Shot feat.
    deltas = [-5 * i for i in range(_iterative_attack_count(bab))]
    rapid_shot_active = (
        bool(options and options.get("rapid_shot"))
        and _has_feat(actor, "rapid_shot")
        and bool(actor.attack_options)
        and actor.attack_options[0].get("type") == "ranged"
    )
    if rapid_shot_active:
        deltas = [0] + deltas
        deltas = [d - 2 for d in deltas]

    for i, delta in enumerate(deltas):
        if not target.is_alive() or target.current_hp <= 0:
            break
        _do_attack(actor, target, grid, roller, events,
                   attack_bonus_delta=delta,
                   label=f"full_attack_{i+1}",
                   encounter=encounter,
                   script_options=options)


def _do_withdraw(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    events: list[TurnEvent],
) -> None:
    direction = args.get("direction", "south")
    speed_squares = actor.speed // 5
    withdraw_squares = speed_squares * 2
    # Withdraw: first square doesn't provoke. We just move; a real impl
    # would suppress AoO from the starting square only.
    target = _direction_to_square(actor, direction)
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"withdraw: bad direction {direction!r}"}))
        return
    dest = _square_away(actor, actor.position, withdraw_squares, grid)
    _move_along(actor, dest, withdraw_squares, grid, events, encounter=encounter)


# ---------------------------------------------------------------------------
# Attack resolution
# ---------------------------------------------------------------------------


def _do_attack(
    actor: Combatant,
    target: Combatant,
    grid: Grid,
    roller: Roller,
    events: list[TurnEvent],
    *,
    attack_bonus_delta: int = 0,
    label: str = "attack",
    encounter=None,
    script_options: dict | None = None,
) -> None:
    options = actor.attack_options
    if not options:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "no attack options"}))
        return
    chosen = options[0]
    is_ranged = chosen.get("type") == "ranged"
    if not is_ranged and not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "attack target not in melee range"}))
        return

    # Sneak attack precision damage if attacker qualifies.
    precision_dice = _sneak_attack_dice(actor, target, grid, encounter)
    # Flanking grants +2 to melee attacks (regardless of class).
    flank_bonus = _flanking_attack_bonus(
        actor, target, grid, encounter, is_ranged=is_ranged,
    )

    # Script-time attack options: power_attack, combat_expertise.
    pa_attack_pen, pa_dmg_bonus = _power_attack_adjustments(
        actor, chosen, script_options or {},
    )
    ce_attack_pen = _combat_expertise_adjustments(
        actor, chosen, script_options or {}, encounter, events,
    )
    # Smite Evil: if this target is the declared smite target, add bonuses.
    smite_atk, smite_dmg = _smite_evil_adjustments(actor, target)
    # Weapon Focus / class-specific bonuses against this weapon target.
    weapon_focus_bonus = 0
    weapon_id = chosen.get("weapon_id")
    if weapon_id:
        wf_target = f"attack:weapon:{weapon_id}"
        weapon_focus_bonus = _compute_mod(0, actor.modifiers.for_target(wf_target))

    # General-purpose attack/damage modifiers (e.g., Inspire Courage morale,
    # Point-Blank Shot for ranged). These accept any source whose target is
    # "attack" or "damage" — the modifier system enforces stacking rules.
    # Situational racial bonuses (dwarven hatred etc.) carry a qualifier
    # against the target's type/subtypes; we evaluate via the context-
    # aware compute.
    target_ctx = _target_creature_context(target)
    attack_general = _compute_mod_ctx(
        0, actor.modifiers.for_target("attack"), target_ctx,
    )
    damage_general = _compute_mod(0, actor.modifiers.for_target("damage"))
    if is_ranged:
        attack_general += _compute_mod_ctx(
            0, actor.modifiers.for_target("attack:ranged"), target_ctx,
        )
        damage_general += _compute_mod(0, actor.modifiers.for_target("damage:ranged"))

    # Range increment penalty for ranged attacks: -2 per increment
    # beyond the first. PF1 RAW caps at 5 increments (thrown) / 10
    # (projectile); for v1 we apply the penalty without enforcing a
    # hard max range — long shots are punished but not forbidden.
    range_penalty = _range_increment_penalty(chosen, actor, target, grid, is_ranged)
    # Firing into melee: -4 ranged attack vs a target engaged with
    # another combatant; negated by Precise Shot feat.
    firing_penalty = _firing_into_melee_penalty(
        actor, target, grid, encounter, is_ranged,
    )
    # Prone-position adjustments:
    #   - prone attacker: -4 to melee attack rolls
    #   - prone target:   +4 melee attacker / -4 ranged attacker
    prone_atk_penalty = 0
    if "prone" in actor.conditions and not is_ranged:
        prone_atk_penalty = -4
    prone_target_modifier = 0
    if "prone" in target.conditions:
        prone_target_modifier = -4 if is_ranged else 4

    # Situational AC bonuses (e.g., +4 dodge AC vs giants from
    # dwarven defensive_training): include qualifier-matched modifiers
    # for THIS attacker. We *augment* the defense_profile by computing
    # qualified-only ac modifiers separately and adding them to the
    # raw AC. (Unqualified ac modifiers are already in defense_profile
    # via the standard compute.)
    attacker_ctx = _target_creature_context(actor)
    ac_context = {
        "attacker_type": attacker_ctx.get("target_type"),
        "attacker_subtypes": attacker_ctx.get("target_subtypes"),
    }
    ac_situational_bonus = _compute_mod_ctx(
        0,
        [m for m in target.modifiers.for_target("ac") if m.qualifier is not None],
        ac_context,
    )

    profile = AttackProfile(
        attack_bonus=(
            int(chosen["attack_bonus"])
            + attack_bonus_delta
            + flank_bonus
            - pa_attack_pen
            - ce_attack_pen
            + smite_atk
            + weapon_focus_bonus
            + attack_general
            + range_penalty
            + firing_penalty
            + prone_atk_penalty
            + prone_target_modifier
            - ac_situational_bonus  # subtracted because it makes the target harder to hit
        ),
        damage_dice=str(chosen["damage"]),
        damage_bonus=(
            int(chosen.get("damage_bonus", 0))
            + pa_dmg_bonus + smite_dmg
            + damage_general
        ),
        crit_range=tuple(chosen.get("crit_range") or [20, 20]),  # type: ignore[arg-type]
        crit_multiplier=int(chosen.get("crit_multiplier", 2)),
        damage_type=str(chosen.get("damage_type", "")),
        name=str(chosen.get("name", "weapon")),
        precision_damage_dice=precision_dice,
    )
    defense = target.defense_profile()
    outcome: AttackOutcome = resolve_attack(profile, defense, roller)
    if outcome.hit and outcome.damage > 0:
        target.take_damage(outcome.damage)
        _apply_post_damage_state(target)
    # Stunning Fist rider: if the attacker has declared a stunning_fist
    # this turn and the attack hit, the target rolls a Fort save vs the
    # cached DC; on failure, target is stunned 1 round.
    stunning_fist_event: dict | None = None
    if outcome.hit and "stunning_fist_pending" in actor.conditions:
        stunning_fist_event = _resolve_stunning_fist(
            actor, target, roller, encounter,
        )
    events.append(TurnEvent(actor.id, label, {
        "target_id": target.id,
        "weapon": profile.name,
        "hit": outcome.hit,
        "crit": outcome.crit,
        "damage": outcome.damage,
        "trace": outcome.log,
    }))
    if stunning_fist_event is not None:
        events.append(TurnEvent(actor.id, "stunning_fist_save",
                                stunning_fist_event))


# ---------------------------------------------------------------------------
# Active combat options: Power Attack, Combat Expertise, Smite Evil
# ---------------------------------------------------------------------------


def _has_feat(actor: Combatant, feat_id: str) -> bool:
    """True if the combatant has the feat.

    Reads from both the underlying template (``character.feats`` or
    ``monster.feats``) and the per-combatant ``extra_feats`` override
    list. Walks parametric variants (e.g. ``weapon_focus_longsword``
    for a requested ``weapon_focus``).
    """
    feats: list[str] = list(actor.extra_feats)
    if actor.template is not None:
        feats.extend(getattr(actor.template, "feats", None) or [])
    if feat_id in feats:
        return True
    prefix = feat_id + "_"
    return any(f == feat_id or f.startswith(prefix) for f in feats)


def _bab_of(actor: Combatant) -> int:
    return int(actor.bases.get("bab", 0))


def _power_attack_adjustments(
    actor: Combatant,
    chosen: dict,
    options: dict,
) -> tuple[int, int]:
    """Compute Power Attack penalty/bonus for this attack.

    ``options.power_attack`` is the patron's chosen attack-bonus penalty
    (a positive int, must be ≥ 1). PF1: -1 attack per 4 BAB step (so
    -1 at BAB 1-4, up to -2 at 5+, etc.; max = 1 + BAB // 4). Damage
    bonus depends on wield: +1 light/off-hand, +2 one-handed,
    +3 two-handed (per point of penalty).

    Returns ``(attack_pen, damage_bonus)``. (0, 0) if not requested or
    not legal (no feat, no melee, BAB < 1).
    """
    pa = options.get("power_attack")
    if not pa:
        return 0, 0
    pa_pen = int(pa)
    if pa_pen <= 0:
        return 0, 0
    if not _has_feat(actor, "power_attack"):
        return 0, 0
    bab = _bab_of(actor)
    if bab < 1:
        return 0, 0
    if chosen.get("type") != "melee":
        return 0, 0
    max_pen = 1 + bab // 4
    pa_pen = min(pa_pen, max_pen)
    wield = chosen.get("wield", "one_handed")
    if wield == "two_handed":
        dmg = pa_pen * 3
    elif wield in ("light", "off_hand"):
        dmg = pa_pen
    else:
        dmg = pa_pen * 2
    return pa_pen, dmg


def _combat_expertise_adjustments(
    actor: Combatant,
    chosen: dict,
    options: dict,
    encounter,
    events: list[TurnEvent],
) -> int:
    """Compute Combat Expertise attack penalty and apply 1-round AC bonus.

    PF1: trade up to (1 + BAB//4) attack for a dodge AC bonus of the
    same magnitude. The AC bonus lasts until the start of the actor's
    next turn (we model as expiring at current_round + 1).

    Returns the attack penalty. 0 when not requested or not legal.
    """
    ce = options.get("combat_expertise")
    if not ce:
        return 0
    ce_pen = int(ce)
    if ce_pen <= 0:
        return 0
    if not _has_feat(actor, "combat_expertise"):
        return 0
    bab = _bab_of(actor)
    if bab < 1:
        return 0
    if chosen.get("type") != "melee":
        return 0
    max_pen = 1 + bab // 4
    ce_pen = min(ce_pen, max_pen)
    cur_round = getattr(encounter, "round_number", 1) if encounter else 1
    src = "combat_expertise"
    actor.modifiers.remove_by_source(src)
    actor.modifiers.add(Modifier(
        value=ce_pen, type="dodge", target="ac",
        source=src, expires_round=cur_round + 1,
    ))
    events.append(TurnEvent(actor.id, "combat_expertise", {
        "attack_penalty": ce_pen, "ac_bonus": ce_pen,
        "expires_round": cur_round + 1,
    }))
    return ce_pen


def _ability_modifier(actor: Combatant, ability: str) -> int:
    """Read the actor's current ability modifier from the template + mods."""
    if actor.template is None:
        return 0
    base = 10
    if hasattr(actor.template, "base_ability_scores"):
        try:
            base = actor.template.base_ability_scores.get(ability)
        except Exception:
            base = 10
    total = base
    for m in actor.modifiers.for_target(f"ability:{ability}"):
        total += m.value
    return (total - 10) // 2


def _paladin_levels(actor: Combatant) -> int:
    if actor.template_kind != "character" or actor.template is None:
        return 0
    char = actor.template
    if getattr(char, "class_id", None) == "paladin":
        levels = 1
    else:
        levels = 0
    plan = getattr(char, "level_plan", None)
    if plan and isinstance(plan, dict):
        for entry in (plan.get("levels") or {}).values():
            if isinstance(entry, dict) and entry.get("class") == "paladin":
                levels += 1
    return levels


def _is_evil(target: Combatant) -> bool:
    """Best-effort alignment check for Smite Evil targets."""
    align = ""
    if target.template is not None:
        align = str(getattr(target.template, "alignment", "") or "")
    return "evil" in align.lower()


def _smite_evil_adjustments(
    actor: Combatant,
    target: Combatant,
) -> tuple[int, int]:
    """If the actor has declared this target as their smite, return
    (attack_bonus, damage_bonus). Otherwise (0, 0)."""
    if not actor.smite_target_id:
        return 0, 0
    if actor.smite_target_id != target.id:
        return 0, 0
    pal_levels = _paladin_levels(actor)
    if pal_levels <= 0:
        return 0, 0
    cha_mod = _ability_modifier(actor, "cha")
    return max(0, cha_mod), pal_levels


# ---------------------------------------------------------------------------
# Composite action handlers: Cleave, Rage, Smite Evil, Channel Energy,
# Bardic Performance
# ---------------------------------------------------------------------------


def _do_cleave(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Cleave: standard action. Attack a foe; on a hit, attack one more
    foe adjacent to actor. Both attacks at -2 to AC for 1 round."""
    if not _has_feat(actor, "cleave"):
        events.append(TurnEvent(actor.id, "skip", {"reason": "cleave: no feat"}))
        return
    primary = _resolve_target(args.get("target"), ns)
    if primary is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "cleave: no primary target"}))
        return
    if not grid.is_adjacent(actor, primary):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "cleave: primary not adjacent"}))
        return
    cur_round = encounter.round_number if encounter else 1
    src = "cleave_ac_penalty"
    actor.modifiers.remove_by_source(src)
    actor.modifiers.add(Modifier(
        value=-2, type="untyped", target="ac",
        source=src, expires_round=cur_round + 1,
    ))

    pre_hp = primary.current_hp
    _do_attack(actor, primary, grid, roller, events,
               label="cleave_primary", encounter=encounter)
    primary_hit = primary.current_hp < pre_hp
    if not primary_hit:
        events.append(TurnEvent(actor.id, "cleave_no_followup",
                                {"reason": "primary missed"}))
        return
    # Second swing at any other adjacent foe.
    secondary = _pick_adjacent_foe(actor, encounter, grid, exclude=primary)
    if secondary is None:
        events.append(TurnEvent(actor.id, "cleave_no_followup",
                                {"reason": "no second foe in reach"}))
        return
    _do_attack(actor, secondary, grid, roller, events,
               label="cleave_secondary", encounter=encounter)


def _pick_adjacent_foe(
    actor: Combatant,
    encounter: Encounter,
    grid: Grid,
    exclude: Combatant | None = None,
) -> Combatant | None:
    if encounter is None:
        return None
    for ir in encounter.initiative:
        c = ir.combatant
        if c.id == actor.id or c.team == actor.team:
            continue
        if exclude is not None and c.id == exclude.id:
            continue
        if c.current_hp <= 0 or c.is_unconscious():
            continue
        if grid.is_adjacent(actor, c):
            return c
    return None


def _do_rage_start(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    events: list[TurnEvent],
) -> None:
    """Begin barbarian rage. Free action; pulls a round from the pool.

    Effects (PF1 base rage): +4 morale Str, +4 morale Con, +2 morale
    Will save, -2 untyped AC. Lasts until ended (or the pool empties).
    """
    if "raging" in actor.conditions:
        events.append(TurnEvent(actor.id, "skip", {"reason": "already raging"}))
        return
    rounds_remaining = actor.resources.get("rage_rounds", 0)
    if rounds_remaining <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "no rage rounds remaining"}))
        return
    actor.resources["rage_rounds"] = rounds_remaining - 1
    src = "rage"
    actor.modifiers.add(Modifier(value=4, type="morale",
                                 target="ability:str", source=src))
    actor.modifiers.add(Modifier(value=4, type="morale",
                                 target="ability:con", source=src))
    actor.modifiers.add(Modifier(value=2, type="morale",
                                 target="will_save", source=src))
    actor.modifiers.add(Modifier(value=-2, type="untyped",
                                 target="ac", source=src))
    actor.add_condition("raging")
    events.append(TurnEvent(actor.id, "rage_start", {
        "rounds_remaining": actor.resources["rage_rounds"],
    }))


def _do_rage_end(
    actor: Combatant,
    events: list[TurnEvent],
) -> None:
    if "raging" not in actor.conditions:
        events.append(TurnEvent(actor.id, "skip", {"reason": "not raging"}))
        return
    actor.modifiers.remove_by_source("rage")
    actor.remove_condition("raging")
    actor.add_condition("fatigued")
    events.append(TurnEvent(actor.id, "rage_end", {}))


def _do_smite_evil(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Paladin Smite Evil. Swift action; declares a target. The bonuses
    apply on attacks against that target until it dies or the paladin
    rests. This handler just consumes the use and stores the target id."""
    pal_levels = _paladin_levels(actor)
    if pal_levels <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "smite_evil: not a paladin"}))
        return
    uses = actor.resources.get("smite_evil_uses", 0)
    if uses <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "no smite_evil uses left"}))
        return
    target = _resolve_target(args.get("target"), ns)
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "smite_evil: no target"}))
        return
    if not _is_evil(target):
        # Smiting a non-evil target wastes the use (PF1 RAW).
        actor.resources["smite_evil_uses"] = uses - 1
        events.append(TurnEvent(actor.id, "smite_evil_wasted", {
            "target_id": target.id, "reason": "target not evil",
        }))
        return
    actor.resources["smite_evil_uses"] = uses - 1
    actor.smite_target_id = target.id
    cha_mod = _ability_modifier(actor, "cha")
    src = "smite_evil_deflect"
    actor.modifiers.remove_by_source(src)
    if cha_mod > 0:
        actor.modifiers.add(Modifier(
            value=cha_mod, type="deflection", target="ac", source=src,
        ))
    events.append(TurnEvent(actor.id, "smite_evil", {
        "target_id": target.id,
        "attack_bonus": max(0, cha_mod),
        "damage_bonus": pal_levels,
        "ac_bonus_vs_target": max(0, cha_mod),
        "uses_remaining": actor.resources["smite_evil_uses"],
    }))


def _cleric_levels(actor: Combatant) -> int:
    if actor.template_kind != "character" or actor.template is None:
        return 0
    char = actor.template
    levels = 1 if getattr(char, "class_id", None) == "cleric" else 0
    plan = getattr(char, "level_plan", None)
    if plan and isinstance(plan, dict):
        for entry in (plan.get("levels") or {}).values():
            if isinstance(entry, dict) and entry.get("class") == "cleric":
                levels += 1
    return levels


def _do_channel_energy(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Cleric Channel Energy. 30-ft burst centered on cleric (6 squares).

    ``args.mode`` is ``"heal_living"`` or ``"harm_undead"`` (good
    cleric); the mirror options are skipped — we model the common case.
    Healing affects allies who are alive (excluding undead); harming
    affects undead enemies. 1d6 at L1, +1d6 every 2 levels. Will save
    halves harm.
    """
    cl_levels = _cleric_levels(actor)
    if cl_levels <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "channel_energy: not a cleric"}))
        return
    uses = actor.resources.get("channel_uses", 0)
    if uses <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "no channel_energy uses left"}))
        return
    actor.resources["channel_uses"] = uses - 1

    mode = args.get("mode", "heal_living")
    dice_count = 1 + (cl_levels - 1) // 2
    dice_str = f"{dice_count}d6"
    r = roller.roll(dice_str)
    base_amount = sum(r.terms[0].kept) if r.terms and r.terms[0].rolls else 0

    cha_mod = _ability_modifier(actor, "cha")
    dc = 10 + cl_levels // 2 + cha_mod

    # Find targets within 6 squares (30 ft) of the cleric.
    radius = 6
    affected: list[dict] = []
    for ir in encounter.initiative:
        c = ir.combatant
        if c.current_hp <= -10:
            continue
        if grid.distance_squares(actor.position, c.position) > radius:
            continue
        is_undead = (
            c.template_kind == "monster"
            and c.template is not None
            and "undead" in (getattr(c.template, "type", "") or "").lower()
        )
        if mode == "heal_living":
            if is_undead:
                if c.team == actor.team:
                    continue
                # Damage undead, Will save halves.
                amount = base_amount
                from .spells import roll_save
                passed, nat, total = roll_save(c, "will", dc, roller)
                if passed:
                    amount = base_amount // 2
                c.take_damage(amount)
                _apply_post_damage_state(c)
                affected.append({
                    "target_id": c.id, "kind": "harm_undead",
                    "amount": amount, "save": passed,
                })
            else:
                # Heal living — never targets enemies.
                if c.team != actor.team and c.id != actor.id:
                    continue
                heal_amt = min(base_amount, c.max_hp - c.current_hp)
                c.heal(base_amount)
                affected.append({
                    "target_id": c.id, "kind": "heal", "amount": heal_amt,
                })
        elif mode == "harm_undead":
            if not is_undead:
                continue
            from .spells import roll_save
            amount = base_amount
            passed, nat, total = roll_save(c, "will", dc, roller)
            if passed:
                amount = base_amount // 2
            c.take_damage(amount)
            _apply_post_damage_state(c)
            affected.append({
                "target_id": c.id, "kind": "harm_undead",
                "amount": amount, "save": passed,
            })

    events.append(TurnEvent(actor.id, "channel_energy", {
        "mode": mode, "dice": dice_str, "rolled": base_amount,
        "save_dc": dc, "affected": affected,
        "uses_remaining": actor.resources["channel_uses"],
    }))


def _bard_levels(actor: Combatant) -> int:
    if actor.template_kind != "character" or actor.template is None:
        return 0
    char = actor.template
    levels = 1 if getattr(char, "class_id", None) == "bard" else 0
    plan = getattr(char, "level_plan", None)
    if plan and isinstance(plan, dict):
        for entry in (plan.get("levels") or {}).values():
            if isinstance(entry, dict) and entry.get("class") == "bard":
                levels += 1
    return levels


def _do_bardic_performance(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Bardic Performance — Inspire Courage (only mode in v1).

    Standard action to start (free to maintain). +1 morale attack/damage
    to all allies who can hear, scaling at L5/L11/L17. Lasts 1 round
    after activation; scripts must repeat to sustain. Each round
    consumes one round from ``performance_rounds``.
    """
    bard_levels = _bard_levels(actor)
    if bard_levels <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "bardic_performance: not a bard"}))
        return
    rounds_left = actor.resources.get("performance_rounds", 0)
    if rounds_left <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "no bardic performance rounds left"}))
        return
    mode = args.get("mode", "inspire_courage")
    if mode != "inspire_courage":
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"bardic mode {mode!r} not implemented"}))
        return

    actor.resources["performance_rounds"] = rounds_left - 1
    cur_round = encounter.round_number if encounter else 1
    bonus = 1
    if bard_levels >= 17:
        bonus = 4
    elif bard_levels >= 11:
        bonus = 3
    elif bard_levels >= 5:
        bonus = 2

    src = f"inspire_courage:{actor.id}"
    affected_ids: list[str] = []
    for ir in encounter.initiative:
        c = ir.combatant
        if c.team != actor.team:
            continue
        if c.current_hp <= 0 or c.is_unconscious():
            continue
        # Refresh the modifier every activation so duration tracks.
        c.modifiers.remove_by_source(src)
        c.modifiers.add(Modifier(value=bonus, type="morale",
                                 target="attack", source=src,
                                 expires_round=cur_round + 1))
        c.modifiers.add(Modifier(value=bonus, type="morale",
                                 target="damage", source=src,
                                 expires_round=cur_round + 1))
        c.modifiers.add(Modifier(value=bonus, type="morale",
                                 target="will_save", source=src,
                                 expires_round=cur_round + 1))
        affected_ids.append(c.id)

    events.append(TurnEvent(actor.id, "bardic_performance", {
        "mode": mode, "bonus": bonus,
        "affected_ids": affected_ids,
        "rounds_remaining": actor.resources["performance_rounds"],
    }))


def _character_level(actor: Combatant) -> int:
    """Total character level for the actor; 1 for monsters / unknowns."""
    if actor.template_kind != "character" or actor.template is None:
        return 1
    lvl = getattr(actor.template, "level", None)
    return int(lvl) if lvl else 1


def _resolve_stunning_fist(
    attacker: Combatant,
    target: Combatant,
    roller: Roller,
    encounter,
) -> dict:
    """Apply the Stunning Fist Fort save to ``target`` on a successful
    hit. Returns an event-detail dict; the caller appends the event."""
    from .spells import roll_save
    dc = int(attacker.resources.get("stunning_fist_dc", 14))
    cur_round = encounter.round_number if encounter else 1
    passed, nat, total = roll_save(target, "fort", dc, roller)
    if passed:
        return {
            "target_id": target.id, "dc": dc,
            "save_natural": nat, "save_total": total,
            "passed": True,
        }
    # Fail: target is stunned 1 round. We use a side-channel resource
    # to track expiration, since conditions don't have built-in
    # durations. Combatant.tick_round clears it on expiry.
    target.add_condition("stunned")
    target.resources["stunned_until_round"] = cur_round + 1
    return {
        "target_id": target.id, "dc": dc,
        "save_natural": nat, "save_total": total,
        "passed": False, "stunned_until_round": cur_round + 1,
    }


def _do_stunning_fist(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Stunning Fist: declare a Fort-save rider on a melee attack.

    PF1: as part of using the feat (or monk class feature), the next
    melee attack you make this turn carries a Fort save (DC 10 + 1/2
    character level + Wis modifier). On hit, target rolls Fort or
    becomes stunned for 1 round. The use is consumed regardless of
    whether the attack hits.

    For v1 this composite bundles the declaration + the attack into
    a single action: pick a target, swing, and (on hit) the Fort
    save fires automatically.
    """
    uses = actor.resources.get("stunning_fist_uses", 0)
    if uses <= 0:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "no stunning_fist uses left"}))
        return
    target = _resolve_target(args.get("target"), ns)
    if target is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "stunning_fist: no target"}))
        return
    if not grid.is_adjacent(actor, target):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "stunning_fist: target not adjacent"}))
        return

    # Consume the use (PF1 RAW: lost whether or not the attack lands).
    actor.resources["stunning_fist_uses"] = uses - 1

    # Compute the save DC: 10 + 1/2 char level + Wis mod.
    cur_round = encounter.round_number if encounter else 1
    char_level = _character_level(actor)
    wis_mod = _ability_modifier(actor, "wis")
    dc = 10 + char_level // 2 + wis_mod

    # Stash the DC so _do_attack can read it after rolling the attack.
    actor.add_condition("stunning_fist_pending")
    actor.resources["stunning_fist_dc"] = dc
    actor.resources["stunning_fist_round"] = cur_round

    events.append(TurnEvent(actor.id, "stunning_fist_declare", {
        "target_id": target.id, "dc": dc,
        "uses_remaining": actor.resources["stunning_fist_uses"],
    }))

    # Now run the attack; _do_attack handles the post-hit Fort save.
    _do_attack(actor, target, grid, roller, events,
               label="stunning_fist_attack", encounter=encounter,
               script_options=args.get("options") or {})

    # Clear the pending flag whether or not the attack hit.
    actor.remove_condition("stunning_fist_pending")
    actor.resources.pop("stunning_fist_dc", None)
    actor.resources.pop("stunning_fist_round", None)


def _do_aid_another(
    actor: Combatant,
    args: dict,
    encounter: Encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Aid Another (PF1).

    Standard action. Pick an ally and a foe; roll an attack vs DC 10
    (an attack roll against an "imaginary" AC 10). On success, your
    ally gets a +2 bonus to either their next attack roll against that
    foe (mode='attack') or +2 dodge AC vs that foe (mode='ac'),
    until the start of your next turn.

    Limitations in v1:
      - The "vs that specific foe" restriction isn't modeled; the
        bonus applies universally to the ally for one round.
      - The "next attack" precision isn't modeled; uses 1-round
        duration instead.
    """
    ally = _resolve_target(args.get("ally"), ns)
    foe = _resolve_target(args.get("foe"), ns)
    mode = args.get("mode", "attack")
    if ally is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "aid_another: no ally"}))
        return
    if foe is None:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "aid_another: no foe"}))
        return
    if mode not in ("attack", "ac"):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"aid_another: unknown mode {mode!r}"}))
        return
    if not grid.is_adjacent(actor, foe):
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "aid_another: foe not in melee reach"}))
        return

    # Roll d20 + actor's primary attack bonus vs DC 10.
    if not actor.attack_options:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": "aid_another: no attack options"}))
        return
    attack_bonus = int(actor.attack_options[0].get("attack_bonus", 0))
    r = roller.roll("1d20")
    nat = r.terms[0].rolls[0]
    total = nat + attack_bonus
    success = total >= 10

    cur_round = encounter.round_number if encounter else 1
    if success:
        target_field = "attack" if mode == "attack" else "ac"
        mod_type = "circumstance" if mode == "attack" else "dodge"
        src = f"aid_another:{actor.id}:{cur_round}"
        ally.modifiers.add(Modifier(
            value=2, type=mod_type, target=target_field,
            source=src, expires_round=cur_round + 1,
        ))
    events.append(TurnEvent(actor.id, "aid_another", {
        "ally_id": ally.id,
        "foe_id": foe.id,
        "mode": mode,
        "attack_natural": nat,
        "attack_total": total,
        "dc": 10,
        "passed": success,
    }))


def _do_cast(
    actor: Combatant,
    args: dict,
    encounter,
    grid: Grid,
    roller: Roller,
    ns: dict[str, Any],
    events: list[TurnEvent],
) -> None:
    """Cast a spell. ``args`` has ``spell``, ``target``, ``spell_level``,
    optional ``defensive`` flag."""
    spell_id = args.get("spell")
    if not spell_id:
        events.append(TurnEvent(actor.id, "skip", {"reason": "cast: no spell"}))
        return
    # Resolve registry.
    from .content import default_registry
    registry = default_registry()
    try:
        spell = registry.get_spell(spell_id)
    except Exception as e:
        events.append(TurnEvent(actor.id, "skip",
                                {"reason": f"unknown spell {spell_id!r}: {e}"}))
        return

    # Knowledge / preparation check.
    if actor.castable_spells and spell_id not in actor.castable_spells:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": f"actor cannot cast {spell_id!r} (not on class spell list "
                      f"or above castable level)",
        }))
        return

    spell_level = int(args.get("spell_level", 1))
    slot_key = f"spell_slot_{spell_level}"
    remaining = actor.resources.get(slot_key, 0)
    if remaining <= 0:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": f"no spell slots remaining at level {spell_level}",
        }))
        return

    # ── Concentration check if threatened (cast on the defensive). ──
    threatened_by = []
    if grid is not None:
        for cid, other in grid.combatants.items():
            if other.id == actor.id or other.team == actor.team:
                continue
            if other.is_unconscious() or "paralyzed" in other.conditions:
                continue
            if grid.threatens(other, actor):
                threatened_by.append(other)
    if threatened_by:
        defensive = bool(args.get("defensive", True))   # default to defensive
        if defensive:
            from .spells import key_ability_for, caster_level as _cl
            cl = _cl(actor)
            key = key_ability_for(actor)
            ab_mod = 0
            if key and actor.template is not None and hasattr(actor.template, "base_ability_scores"):
                base = actor.template.base_ability_scores.get(key)
                ab_mod = (base - 10) // 2
                # Add modifiers
                for m in actor.modifiers.for_target(f"ability:{key}"):
                    ab_mod += m.value
            conc_dc = 15 + spell_level
            r = roller.roll("1d20")
            nat = r.terms[0].rolls[0]
            total = nat + cl + ab_mod
            passed = total >= conc_dc
            # Slot is consumed regardless of success.
            actor.resources[slot_key] = remaining - 1
            if not passed:
                events.append(TurnEvent(actor.id, "cast_failed", {
                    "spell_id": spell_id,
                    "reason": "concentration_failed",
                    "concentration_check": {
                        "natural": nat, "modifier": cl + ab_mod,
                        "total": total, "dc": conc_dc,
                    },
                    "threatened_by": [t.id for t in threatened_by],
                }))
                return
            events.append(TurnEvent(actor.id, "concentration", {
                "natural": nat, "modifier": cl + ab_mod,
                "total": total, "dc": conc_dc, "passed": True,
            }))
        else:
            # Casting non-defensively while threatened provokes AoOs.
            for threatener in threatened_by:
                _do_aoo(threatener, actor, grid, events, encounter=encounter)
                if actor.current_hp <= 0:
                    events.append(TurnEvent(actor.id, "cast_failed", {
                        "spell_id": spell_id,
                        "reason": "killed_by_aoo_during_cast",
                    }))
                    actor.resources[slot_key] = remaining - 1
                    return
            actor.resources[slot_key] = remaining - 1
    else:
        actor.resources[slot_key] = remaining - 1

    # ── Resolve targets, expanding for buff_party / AoE. ──
    targets = _expand_cast_targets(actor, spell, args, encounter, grid, ns)
    if not targets:
        events.append(TurnEvent(actor.id, "skip", {
            "reason": f"cast {spell_id}: no target resolved",
        }))
        return

    from .spells import cast_spell
    cur_round = encounter.round_number if encounter is not None else 1
    outcome = cast_spell(
        actor, spell, targets, spell_level, registry, roller,
        current_round=cur_round,
    )
    events.append(TurnEvent(actor.id, "cast", outcome.to_dict()))


def _expand_cast_targets(
    actor: Combatant,
    spell,
    args: dict,
    encounter,
    grid,
    ns: dict[str, Any],
) -> list[Combatant]:
    """Multi-target / friend-or-foe expansion based on the spell's effect."""
    kind = spell.effect.get("kind", "")
    # Party buffs: target all allies in 50 ft (10 squares) of caster.
    if kind == "buff_party":
        if encounter is None:
            return [actor]
        out: list[Combatant] = []
        for ir in encounter.initiative:
            c = ir.combatant
            if c.team != actor.team:
                continue
            if c.current_hp <= 0:
                continue
            if grid is None or grid.distance_between(actor, c) <= 10:
                out.append(c)
        return out

    # AoE shapes — burst, cone.
    area = spell.effect.get("area") or {}
    shape = area.get("shape", "")
    if shape == "burst":
        return _expand_aoe_burst(actor, spell, args, ns, encounter, grid)
    if shape == "cone":
        return _expand_aoe_cone(actor, spell, args, ns, encounter, grid)

    # Single-target default: resolve from the args.target expression.
    target_expr = args.get("target")
    target = _resolve_target(target_expr, ns)
    return [target] if target is not None else []


def _expand_aoe_burst(
    actor: Combatant,
    spell,
    args: dict,
    ns: dict[str, Any],
    encounter,
    grid,
) -> list[Combatant]:
    """All combatants whose anchor is within R squares of the burst center.

    Burst center is determined by the script's ``target`` arg: a
    Combatant (use its position) or a literal square.
    """
    if encounter is None or grid is None:
        return []
    eff = spell.effect
    area = eff.get("area") or {}
    radius_squares = int(area.get("size_ft", 0)) // 5
    target_expr = args.get("target")
    target_obj = _resolve_target(target_expr, ns)
    if hasattr(target_obj, "position"):
        center = target_obj.position
    elif (isinstance(target_obj, tuple)
          and len(target_obj) == 2
          and all(isinstance(c, int) for c in target_obj)):
        center = target_obj
    else:
        return []
    out: list[Combatant] = []
    for ir in encounter.initiative:
        c = ir.combatant
        if c.current_hp <= -10:
            continue
        if grid.distance_squares(c.position, center) <= radius_squares:
            out.append(c)
    return out


def _expand_aoe_cone(
    actor: Combatant,
    spell,
    args: dict,
    ns: dict[str, Any],
    encounter,
    grid,
) -> list[Combatant]:
    """All combatants in a 90-degree cone emanating from the caster.

    Cone direction = from caster toward the script's ``target``. Cone
    length = ``area.size_ft``. Squares within ±45° of the direction
    vector and within range are inside.
    """
    if encounter is None or grid is None:
        return []
    eff = spell.effect
    area = eff.get("area") or {}
    range_squares = int(area.get("size_ft", 0)) // 5
    target_expr = args.get("target")
    target_obj = _resolve_target(target_expr, ns)
    if hasattr(target_obj, "position"):
        target_pos = target_obj.position
    elif (isinstance(target_obj, tuple)
          and len(target_obj) == 2
          and all(isinstance(c, int) for c in target_obj)):
        target_pos = target_obj
    else:
        return []
    cx, cy = actor.position
    tx, ty = target_pos
    vx, vy = tx - cx, ty - cy
    if vx == 0 and vy == 0:
        return []
    out: list[Combatant] = []
    for ir in encounter.initiative:
        c = ir.combatant
        if c.id == actor.id:
            continue  # caster's own square is the cone origin
        if c.current_hp <= -10:
            continue
        sx, sy = c.position
        dx, dy = sx - cx, sy - cy
        if dx == 0 and dy == 0:
            continue
        if grid.distance_squares(actor.position, c.position) > range_squares:
            continue
        # In-cone test: angle between (dx,dy) and (vx,vy) must be ≤ 45°.
        # Equivalently: dot > 0 AND 2 * dot² ≥ |d|² · |v|².
        dot = dx * vx + dy * vy
        if dot <= 0:
            continue
        if 2 * dot * dot < (dx * dx + dy * dy) * (vx * vx + vy * vy):
            continue
        out.append(c)
    return out


_SNEAK_ATTACK_DENY_DEX_CONDITIONS = frozenset({
    "flat_footed", "prone", "paralyzed", "helpless",
    "stunned", "sleeping", "pinned", "cowering", "blinded",
})


def _is_flanking(
    actor: Combatant,
    target: Combatant,
    grid: Grid | None,
    encounter,
) -> bool:
    """True if any conscious ally + the actor flank the target."""
    if grid is None or encounter is None:
        return False
    if not grid.is_adjacent(actor, target):
        return False
    for ir in encounter.initiative:
        ally = ir.combatant
        if ally.id == actor.id or ally.team != actor.team:
            continue
        if ally.current_hp <= 0 or ally.is_unconscious():
            continue
        if grid.is_flanked_by(target, actor, ally):
            return True
    return False


def _firing_into_melee_penalty(
    actor: Combatant,
    target: Combatant,
    grid: Grid | None,
    encounter,
    is_ranged: bool,
) -> int:
    """PF1 RAW: ranged attacks against a target engaged in melee suffer
    a -4 penalty unless the attacker has the Precise Shot feat.

    "Engaged in melee" is approximated as "another combatant is
    adjacent to the target" — sufficient for 5-ft reach. Reach
    weapons (10-ft) are deferred.
    """
    if not is_ranged or grid is None or encounter is None:
        return 0
    if _has_feat(actor, "precise_shot"):
        return 0
    for ir in encounter.initiative:
        c = ir.combatant
        if c.id == actor.id or c.id == target.id:
            continue
        if c.current_hp <= 0 or c.is_unconscious():
            continue
        if grid.is_adjacent(c, target):
            return -4
    return 0


def _target_creature_context(target: Combatant) -> dict:
    """Build the qualifier-matching context dict for ``target``.

    Used by situational racial traits (dwarven hatred vs orcs etc.).
    Reads ``target_type`` and ``target_subtypes`` from the underlying
    monster template; characters get a ``humanoid`` type with their
    race id as a subtype (so dwarven hatred recognizes a "goblinoid"
    PC etc., should one ever exist).
    """
    if target.template is None:
        return {"target_type": "", "target_subtypes": []}
    if target.template_kind == "monster":
        ttype = (getattr(target.template, "type", "") or "").lower()
        subs = [s.lower() for s in
                (getattr(target.template, "subtypes", None) or [])]
        return {"target_type": ttype, "target_subtypes": subs}
    if target.template_kind == "character":
        race_id = (getattr(target.template, "race_id", "") or "").lower()
        return {"target_type": "humanoid", "target_subtypes": [race_id]}
    return {"target_type": "", "target_subtypes": []}


def _range_increment_penalty(
    chosen: dict,
    actor: Combatant,
    target: Combatant,
    grid: Grid | None,
    is_ranged: bool,
) -> int:
    """PF1 RAW: ranged attacks take -2 per range increment beyond the
    first.

    ``range_increment`` on the attack option is in feet; we convert to
    feet via ``5 * grid.distance_between(actor, target)``. A weapon
    with no ``range_increment`` (purely melee) gets no penalty.
    """
    if not is_ranged or grid is None:
        return 0
    rinc_ft = int(chosen.get("range_increment") or 0)
    if rinc_ft <= 0:
        return 0
    distance_ft = grid.distance_between(actor, target) * 5
    if distance_ft <= 0:
        return 0
    # Number of increments used: ceil(distance / rinc).
    increments = (distance_ft + rinc_ft - 1) // rinc_ft
    return -2 * max(0, increments - 1)


def _flanking_attack_bonus(
    actor: Combatant,
    target: Combatant,
    grid: Grid | None,
    encounter,
    *,
    is_ranged: bool,
) -> int:
    """+2 to attack when flanking a target in melee (PF1 RAW)."""
    if is_ranged:
        return 0
    return 2 if _is_flanking(actor, target, grid, encounter) else 0


def _sneak_attack_dice(
    actor: Combatant,
    target: Combatant,
    grid: Grid | None,
    encounter,
) -> str:
    """Return precision damage dice (e.g. ``"2d6"``) if attacker qualifies.

    PF1 sneak attack triggers when the target is denied its Dex bonus to
    AC OR the attacker is flanking. Multiclass rogues use only their
    rogue level for sneak attack progression.
    """
    if actor.template_kind != "character":
        return ""
    char = actor.template
    if char is None:
        return ""

    # Cumulative rogue levels (from level plan).
    rogue_levels = 1 if getattr(char, "class_id", None) == "rogue" else 0
    plan = getattr(char, "level_plan", None)
    if plan and isinstance(plan, dict):
        for entry in (plan.get("levels") or {}).values():
            if isinstance(entry, dict) and entry.get("class") == "rogue":
                rogue_levels += 1
    if rogue_levels < 1:
        return ""

    # Qualifies via flat-footed / denied Dex, or via flanking.
    denies_dex = bool(target.conditions & _SNEAK_ATTACK_DENY_DEX_CONDITIONS)
    if not denies_dex and not _is_flanking(actor, target, grid, encounter):
        return ""

    # Sneak attack scales: +1d6 at L1, +1d6 every 2 levels (L1=1, L3=2, ...).
    sa_dice = (rogue_levels + 1) // 2
    return f"{sa_dice}d6"


def _has_racial_trait(target: Combatant, trait_id: str) -> bool:
    """True if the monster template carries the named racial trait."""
    if target.template_kind != "monster" or target.template is None:
        return False
    traits = getattr(target.template, "racial_traits", None) or []
    return any(
        isinstance(t, dict) and t.get("id") == trait_id for t in traits
    )


def _apply_post_damage_state(target: Combatant) -> None:
    """Centralized HP-threshold transitions after damage.

    All damage sites must call this *after* ``target.take_damage(...)``.
    It handles four transitions, by HP threshold:

    * HP <= ``target.death_threshold`` → dead. PF1 RAW: -CON for living
      creatures; 0 for undead/constructs.
    * HP <= 0 (but above death threshold) with ferocity → stay
      conscious + ``ferocity_active`` + ``staggered``. Tick_round
      bleeds 1 HP/round until killed outright.
    * HP < 0 (negative but above death threshold) without ferocity →
      ``dying``. Tick_round bleeds 1 HP/round.
    * HP exactly 0 → ``disabled`` (PF1 distinction): conscious, can
      take 1 standard or 1 move (not both); standard actions deal 1
      HP back to self (not yet modeled — PARTIAL).
    """
    threshold = target.death_threshold
    if target.current_hp <= threshold:
        target.add_condition("dead")
        target.remove_condition("dying")
        target.remove_condition("disabled")
        target.remove_condition("ferocity_active")
        target.remove_condition("staggered")
        return
    if target.current_hp == 0:
        target.add_condition("disabled")
        target.remove_condition("dying")
        return
    if target.current_hp < 0:
        if _has_racial_trait(target, "ferocity"):
            # Stay conscious and keep fighting; suppress dying.
            target.add_condition("ferocity_active")
            target.add_condition("staggered")
            target.remove_condition("dying")
            target.remove_condition("disabled")
        else:
            target.add_condition("dying")
            target.remove_condition("disabled")


def _aoo_limit(actor: Combatant) -> int:
    """Maximum AoOs per round. PF1: 1 by default; Combat Reflexes adds
    the combatant's Dex modifier (minimum total 1)."""
    if not _has_feat(actor, "combat_reflexes"):
        return 1
    dex_mod = _ability_modifier(actor, "dex")
    return max(1, 1 + dex_mod)


def _can_take_aoo(threatener: Combatant, current_round: int) -> bool:
    """Throttle AoOs per the threatener's per-round limit."""
    if threatener.aoos_used_round_marker != current_round:
        threatener.aoos_used_round_marker = current_round
        threatener.aoos_used_this_round = 0
    return threatener.aoos_used_this_round < _aoo_limit(threatener)


def _do_aoo(
    threatener: Combatant,
    target: Combatant,
    grid: Grid,
    events: list[TurnEvent],
    encounter=None,
) -> None:
    # Throttle AoOs by the per-round limit (1 + Dex if Combat Reflexes).
    if encounter is not None:
        if not _can_take_aoo(threatener, encounter.round_number):
            return
        threatener.aoos_used_this_round += 1
    # Use the threatener's first attack option as their AoO weapon.
    if not threatener.attack_options:
        return
    chosen = threatener.attack_options[0]
    profile = AttackProfile(
        attack_bonus=int(chosen["attack_bonus"]),
        damage_dice=str(chosen["damage"]),
        damage_bonus=int(chosen.get("damage_bonus", 0)),
        crit_range=tuple(chosen.get("crit_range") or [20, 20]),  # type: ignore[arg-type]
        crit_multiplier=int(chosen.get("crit_multiplier", 2)),
        damage_type=str(chosen.get("damage_type", "")),
        name=str(chosen.get("name", "weapon")),
    )
    # AoO uses a fresh d20 in the encounter's RNG sequence.
    from .dice import Roller as _R
    aoo_roller = _R()  # not deterministic — TODO route encounter RNG.
    outcome = resolve_attack(profile, target.defense_profile(), aoo_roller)
    if outcome.hit and outcome.damage > 0:
        target.take_damage(outcome.damage)
        _apply_post_damage_state(target)
    events.append(TurnEvent(threatener.id, "aoo", {
        "target_id": target.id,
        "hit": outcome.hit,
        "crit": outcome.crit,
        "damage": outcome.damage,
        "trace": outcome.log,
    }))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _resolve_target(target: Any, ns: dict[str, Any]) -> Any:
    """Resolve a target spec to a Python object (Combatant, square, etc.)."""
    if target is None:
        return None
    if isinstance(target, str):
        # Treat as expression to evaluate against the namespace.
        try:
            return evaluate(target, ns)
        except Exception:
            return None
    return target


def _coerce_square(target: Any) -> tuple[int, int] | None:
    if target is None:
        return None
    if isinstance(target, tuple) and len(target) == 2:
        return (int(target[0]), int(target[1]))
    if hasattr(target, "position"):
        return target.position
    if isinstance(target, list) and len(target) == 2:
        return (int(target[0]), int(target[1]))
    return None


# ---------------------------------------------------------------------------
# Default monster AI (no script)
# ---------------------------------------------------------------------------


def default_monster_intent(
    actor: Combatant,
    encounter: Encounter,
    grid: Grid,
) -> TurnIntent:
    """Hardcoded aggressive-melee AI for monsters that don't have scripts.

    Logic: if a hostile is in melee range, full_attack closest. Otherwise
    if enemies exist, charge the closest. Otherwise hold.
    """
    from .dsl import build_namespace
    ns = build_namespace(actor, encounter, grid)
    enemies = [
        ir.combatant for ir in encounter.initiative
        if ir.combatant.team != actor.team
        and ir.combatant.current_hp > 0
        and not ir.combatant.is_unconscious()
    ]
    if not enemies:
        return TurnIntent(rule_index=-1,
                          do={"composite": "hold"},
                          namespace=ns)
    closest = min(enemies, key=lambda e: grid.distance_between(actor, e))
    if grid.is_adjacent(actor, closest):
        return TurnIntent(
            rule_index=-1,
            do={"composite": "full_attack",
                "args": {"target": "enemy.closest"}},
            namespace=ns,
        )
    # Charge if within charge range (2x speed) AND a straight-line
    # PF1-legal charge path exists. If the geometry isn't right
    # (target off-axis, lane blocked) the AI falls back to
    # move_toward so the monster doesn't waste its turn declaring an
    # illegal charge.
    charge_range = (actor.speed // 5) * 2
    if grid.distance_between(actor, closest) <= charge_range:
        line = _straight_line_charge_path(
            actor.position, closest.position, charge_range, grid,
        )
        if line is not None and _charge_path_clear(
            line[1:], grid, mover=actor,
        ):
            return TurnIntent(
                rule_index=-1,
                do={"composite": "charge",
                    "args": {"target": "enemy.closest"}},
                namespace=ns,
            )
    # Otherwise approach.
    return TurnIntent(
        rule_index=-1,
        do={"slots": {
            "move": {"type": "move_toward", "target": "enemy.closest"},
        }},
        namespace=ns,
    )
