"""2D grid for placement, distance, reach, and line of sight.

A ``Grid`` is a finite rectangle of 5-ft squares. Each square may carry a
terrain feature (wall, difficult terrain, water, etc.). Combatants are
placed at an anchor square and occupy a footprint of N×N squares
determined by their size category.

PF1 distance counting (5-10-5 alternating diagonals) is built in:

::

    distance_squares(a, b) = max(dx, dy) + min(dx, dy) // 2

Threatened squares are computed from the combatant's footprint plus its
natural reach (which depends on size and reach class — tall vs. long).

This module is purely spatial. Movement validation, path-finding, and
difficult-terrain costs are layered on by the encounter engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .combatant import Combatant
from .sizes import get_size


def _wields_reach_weapon(combatant: Combatant) -> bool:
    """True if the combatant's primary attack uses a reach weapon.

    Reads the first non-offhand attack option's ``weapon_id`` and
    looks up its ``has_reach`` field via the default registry. Returns
    False for natural-attack monsters (no weapon_id).
    """
    for opt in combatant.attack_options:
        if opt.get("is_offhand"):
            continue
        wid = opt.get("weapon_id")
        if not wid:
            return False
        from .content import default_registry
        try:
            return bool(default_registry().get_weapon(wid).has_reach)
        except Exception:
            return False
    return False


# ---------------------------------------------------------------------------
# Features
# ---------------------------------------------------------------------------


# Known feature types. Open extensible for now; the engine just looks
# at the type name.
WALL = "wall"
DIFFICULT = "difficult"
WATER = "water"
TRAP = "trap"


@dataclass(frozen=True)
class GridFeature:
    type: str
    blocks_movement: bool = False
    blocks_line_of_sight: bool = False
    movement_cost_multiplier: float = 1.0


def wall() -> GridFeature:
    return GridFeature(type=WALL, blocks_movement=True, blocks_line_of_sight=True)


def difficult() -> GridFeature:
    return GridFeature(type=DIFFICULT, movement_cost_multiplier=2.0)


def water() -> GridFeature:
    return GridFeature(type=WATER, movement_cost_multiplier=2.0)


# ---------------------------------------------------------------------------
# Grid
# ---------------------------------------------------------------------------


class PlacementError(Exception):
    """Raised when a combatant cannot be placed at the requested anchor."""


@dataclass
class Grid:
    width: int
    height: int
    features: dict[tuple[int, int], GridFeature] = field(default_factory=dict)
    combatants: dict[str, Combatant] = field(default_factory=dict)
    # square → combatant_id, for fast occupancy lookup
    _occupancy: dict[tuple[int, int], str] = field(default_factory=dict)

    # ── Bounds, terrain, basic queries ────────────────────────────────────

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def feature_at(self, x: int, y: int) -> GridFeature | None:
        return self.features.get((x, y))

    def is_wall(self, x: int, y: int) -> bool:
        f = self.feature_at(x, y)
        return f is not None and f.type == WALL

    def is_difficult(self, x: int, y: int) -> bool:
        f = self.feature_at(x, y)
        return f is not None and f.movement_cost_multiplier > 1.0

    def is_passable(self, x: int, y: int) -> bool:
        if not self.in_bounds(x, y):
            return False
        f = self.feature_at(x, y)
        if f is not None and f.blocks_movement:
            return False
        if (x, y) in self._occupancy:
            return False
        return True

    def add_feature(self, x: int, y: int, feature: GridFeature) -> None:
        if not self.in_bounds(x, y):
            raise ValueError(f"feature out of bounds at ({x}, {y})")
        self.features[(x, y)] = feature

    def occupant(self, x: int, y: int) -> str | None:
        return self._occupancy.get((x, y))

    # ── Footprint ─────────────────────────────────────────────────────────

    def footprint_squares(self, combatant: Combatant) -> list[tuple[int, int]]:
        """Squares the combatant occupies given its size and anchor."""
        size = get_size(combatant.size)
        n = size.footprint_squares
        ax, ay = combatant.position
        return [(ax + dx, ay + dy) for dx in range(n) for dy in range(n)]

    def reach_squares(self, combatant: Combatant) -> int:
        size = get_size(combatant.size)
        if combatant.reach_class == "tall":
            return size.reach_squares_tall
        return size.reach_squares_long

    # ── Placement ─────────────────────────────────────────────────────────

    def place(self, combatant: Combatant) -> None:
        squares = self.footprint_squares(combatant)
        for sq in squares:
            if not self.in_bounds(*sq):
                raise PlacementError(
                    f"footprint square {sq} out of bounds (grid {self.width}x{self.height})"
                )
            f = self.features.get(sq)
            if f is not None and f.blocks_movement:
                raise PlacementError(f"square {sq} is impassable ({f.type})")
            other = self._occupancy.get(sq)
            if other is not None and other != combatant.id:
                raise PlacementError(
                    f"square {sq} already occupied by combatant {other!r}"
                )
        # Commit: clear any prior position then mark new.
        if combatant.id in self.combatants:
            self.remove(combatant.id)
        self.combatants[combatant.id] = combatant
        for sq in squares:
            self._occupancy[sq] = combatant.id

    def remove(self, combatant_id: str) -> None:
        if combatant_id not in self.combatants:
            return
        # Sweep occupancy.
        to_drop = [sq for sq, cid in self._occupancy.items() if cid == combatant_id]
        for sq in to_drop:
            del self._occupancy[sq]
        del self.combatants[combatant_id]

    def move(self, combatant: Combatant, new_anchor: tuple[int, int]) -> None:
        old = combatant.position
        combatant.position = new_anchor
        try:
            self.place(combatant)
        except PlacementError:
            combatant.position = old
            self.place(combatant)
            raise

    # ── Distance ──────────────────────────────────────────────────────────

    @staticmethod
    def distance_squares(a: tuple[int, int], b: tuple[int, int]) -> int:
        """PF1 alternating-diagonal distance, in 5-ft squares.

        ``distance = max(dx, dy) + min(dx, dy) // 2``.
        """
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return max(dx, dy) + min(dx, dy) // 2

    @staticmethod
    def distance_feet(a: tuple[int, int], b: tuple[int, int]) -> int:
        return 5 * Grid.distance_squares(a, b)

    def distance_between(self, c1: Combatant, c2: Combatant) -> int:
        """Minimum square-distance between any squares of two combatants'
        footprints. 0 means overlap; 1 means adjacent (8-way)."""
        f1 = self.footprint_squares(c1)
        f2 = self.footprint_squares(c2)
        return min(
            self.distance_squares(s1, s2) for s1 in f1 for s2 in f2
        )

    def is_adjacent(self, c1: Combatant, c2: Combatant) -> bool:
        return self.distance_between(c1, c2) <= 1

    # ── Threatened squares & flanking ────────────────────────────────────

    def threatened_squares(self, combatant: Combatant) -> set[tuple[int, int]]:
        """Return squares the combatant threatens (eligible for AoO).

        Excludes squares occupied by the combatant itself. Includes
        squares occupied by anyone else (you threaten allies' squares
        too — friendliness matters at the AoO trigger, not here).

        With a reach weapon (lance, longspear, glaive — primary weapon
        flagged ``has_reach``), the threatened set is shifted out by
        +1 square: a Medium creature threatens distance 2 only and
        NOT adjacent. Without a reach weapon, threat covers all
        squares within ``reach_squares``.
        """
        reach = self.reach_squares(combatant)
        if reach <= 0:
            return set()
        wields_reach = _wields_reach_weapon(combatant)
        if wields_reach:
            min_d = reach + 1
            max_d = reach + 1
        else:
            min_d = 1
            max_d = reach
        own = set(self.footprint_squares(combatant))
        threatened: set[tuple[int, int]] = set()
        for sx, sy in own:
            for tx in range(sx - max_d, sx + max_d + 1):
                for ty in range(sy - max_d, sy + max_d + 1):
                    if not self.in_bounds(tx, ty):
                        continue
                    if (tx, ty) in own:
                        continue
                    d = self.distance_squares((sx, sy), (tx, ty))
                    if min_d <= d <= max_d:
                        threatened.add((tx, ty))
        return threatened

    def threatens(self, c1: Combatant, c2: Combatant) -> bool:
        """Does c1 threaten any square of c2's footprint?"""
        threats = self.threatened_squares(c1)
        return any(sq in threats for sq in self.footprint_squares(c2))

    def is_flanked_by(self, target: Combatant, a: Combatant, b: Combatant) -> bool:
        """``target`` is flanked by ``a`` and ``b`` if both threaten it
        and their footprints' centers are on opposite sides.

        Approximation: check that the line segment between the centers
        of a's and b's footprints passes through (or near) target's
        center.
        """
        if not (self.threatens(a, target) and self.threatens(b, target)):
            return False
        ac = _center(self.footprint_squares(a))
        bc = _center(self.footprint_squares(b))
        tc = _center(self.footprint_squares(target))
        # Vectors from target to each flanker.
        ax, ay = ac[0] - tc[0], ac[1] - tc[1]
        bx, by = bc[0] - tc[0], bc[1] - tc[1]
        # Opposite sides means dot product is negative and they're roughly
        # antiparallel.
        dot = ax * bx + ay * by
        return dot < 0

    # ── Line of sight (Bresenham) ─────────────────────────────────────────

    def line_of_sight(
        self,
        a: tuple[int, int],
        b: tuple[int, int],
    ) -> bool:
        """True if no LoS-blocking wall lies strictly between a and b."""
        for x, y in _bresenham(a, b):
            if (x, y) == a or (x, y) == b:
                continue
            f = self.features.get((x, y))
            if f is not None and f.blocks_line_of_sight:
                return False
        return True


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _center(squares: list[tuple[int, int]]) -> tuple[float, float]:
    if not squares:
        return (0.0, 0.0)
    sx = sum(s[0] for s in squares) / len(squares)
    sy = sum(s[1] for s in squares) / len(squares)
    return (sx, sy)


def _bresenham(a: tuple[int, int], b: tuple[int, int]) -> list[tuple[int, int]]:
    """Bresenham's line algorithm. Returns squares between a and b inclusive."""
    x0, y0 = a
    x1, y1 = b
    points: list[tuple[int, int]] = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        points.append((x, y))
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    return points
