"""Behavior DSL parser and interpreter.

A behavior script is a JSON file with this shape (YAML support is a
future add when ``PyYAML`` is in the environment):

::

    {
      "name": "aggressive_fighter",
      "party": {"hero": {}},
      "rules": [
        {
          "hero": "any",
          "when": "enemy.any and enemy.in_range(30)",
          "do": {"composite": "charge", "args": {"target": "enemy.closest"}}
        },
        {
          "hero": "any",
          "when": "enemy.any",
          "do": {"slots": {
            "standard": {"type": "attack", "target": "enemy.closest"},
            "move": {"type": "move_toward", "target": "enemy.closest"}
          }}
        },
        {"do": {"composite": "hold"}}
      ]
    }

Conditions ("when" expressions) and any nested ``target`` strings are
evaluated by a constrained AST walker that only allows: literals,
``Name`` lookups in a fixed namespace, ``Attribute`` access on the same,
``Call`` of vocabulary methods, ``BoolOp`` (and/or), ``UnaryOp`` (not /
unary minus), ``Compare`` (chained), and ``BinOp`` for simple arithmetic.

Forbidden: ``Lambda``, ``Subscript``, ``Import``, ``Yield``, list/dict
comprehensions, anything with side effects.

Vocabulary surface (initial subset; will expand to match
``BEHAVIOR_VOCABULARY.md``):

- ``self`` — the active hero. Attributes: ``hp``, ``hp_max``, ``hp_pct``,
  ``threatened_count``. Methods: ``has_condition(name)``.
- ``enemy`` — resolver. Attributes: ``any`` (bool), ``count`` (int),
  ``closest`` (Combatant), ``lowest_hp`` (Combatant),
  ``lowest_hp_pct`` (Combatant). Methods: ``in_range(r)``, ``count_in_range(r)``.
- ``ally`` — resolver. Attributes: ``any`` (bool), ``lowest_hp_pct``
  (Combatant). Method: ``role(name)``.
- ``round_number`` — int.

Any expression evaluating to a Combatant can be passed as a target. We
also support the literal string ``"self"``.
"""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .combatant import Combatant
from .encounter import Encounter
from .grid import Grid


# ---------------------------------------------------------------------------
# Behavior script
# ---------------------------------------------------------------------------


class DSLError(ValueError):
    """Raised on a parse error or vocabulary violation."""


@dataclass
class Rule:
    hero: str = "any"           # role name or "any"
    when: str | None = None     # condition expression; None = always
    do: dict = field(default_factory=dict)
    # DSL v2: ``react`` and ``sub`` discriminate non-active-turn rules.
    # When both are None, the rule applies to active-turn picking
    # (existing behavior). When ``react`` is set (e.g., "aoo", "brace",
    # "cleave"), the rule applies to that reactive-interrupt kind.
    # When ``sub`` is set (e.g., "full_attack"), the rule applies to
    # that sub-action decision-point. The ``when`` namespace is
    # context-specific (build_reactive_namespace builds it).
    react: str | None = None
    sub: str | None = None


@dataclass
class BehaviorScript:
    name: str
    party: dict[str, dict] = field(default_factory=dict)
    rules: list[Rule] = field(default_factory=list)


def parse_script(text: str) -> BehaviorScript:
    """Parse a JSON behavior script."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise DSLError(f"behavior script is not valid JSON: {e}") from e
    return script_from_dict(data)


def load_script(path: str | Path) -> BehaviorScript:
    p = Path(path)
    return parse_script(p.read_text(encoding="utf-8"))


def script_from_dict(data: dict) -> BehaviorScript:
    if not isinstance(data, dict):
        raise DSLError(f"script must be an object, got {type(data).__name__}")
    name = str(data.get("name", "<unnamed>"))
    party = dict(data.get("party") or {"hero": {}})
    raw_rules = data.get("rules")
    if not isinstance(raw_rules, list):
        raise DSLError("'rules' must be a list")
    rules: list[Rule] = []
    for i, r in enumerate(raw_rules):
        if not isinstance(r, dict):
            raise DSLError(f"rule {i} must be an object, got {type(r).__name__}")
        rules.append(Rule(
            hero=str(r.get("hero", "any")),
            when=r.get("when"),
            do=dict(r.get("do") or {}),
            react=r.get("react"),
            sub=r.get("sub"),
        ))
    return BehaviorScript(name=name, party=party, rules=rules)


# ---------------------------------------------------------------------------
# Safe AST evaluator
# ---------------------------------------------------------------------------


_ALLOWED_NODES: tuple[type[ast.AST], ...] = (
    ast.Expression,
    ast.BoolOp, ast.And, ast.Or,
    ast.UnaryOp, ast.Not, ast.USub, ast.UAdd,
    ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.Is, ast.IsNot, ast.In, ast.NotIn,
    ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod,
    ast.Constant,
    ast.Name, ast.Attribute,
    ast.Call, ast.keyword,
    ast.Load,
)


def _validate_ast(tree: ast.AST) -> None:
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise DSLError(
                f"disallowed expression node: {type(node).__name__}"
            )


def evaluate(expression: str, namespace: dict[str, Any]) -> Any:
    """Parse and evaluate ``expression`` in ``namespace``.

    Only the constrained AST node types are allowed.
    """
    if not expression or not expression.strip():
        raise DSLError("empty expression")
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as e:
        raise DSLError(f"syntax error in expression {expression!r}: {e}") from e
    _validate_ast(tree)
    return _eval_node(tree.body, namespace)


def _eval_node(node: ast.AST, ns: dict[str, Any]) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id not in ns:
            raise DSLError(f"unknown identifier {node.id!r}")
        return ns[node.id]
    if isinstance(node, ast.Attribute):
        value = _eval_node(node.value, ns)
        if not hasattr(value, node.attr):
            raise DSLError(f"unknown attribute {node.attr!r} on {value!r}")
        return getattr(value, node.attr)
    if isinstance(node, ast.Call):
        func = _eval_node(node.func, ns)
        args = [_eval_node(a, ns) for a in node.args]
        kwargs = {kw.arg: _eval_node(kw.value, ns) for kw in node.keywords if kw.arg}
        return func(*args, **kwargs)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, ns)
        if isinstance(node.op, ast.Not):
            return not operand
        if isinstance(node.op, ast.USub):
            return -operand
        if isinstance(node.op, ast.UAdd):
            return +operand
    if isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            for v in node.values:
                r = _eval_node(v, ns)
                if not r:
                    return r
            return r
        if isinstance(node.op, ast.Or):
            for v in node.values:
                r = _eval_node(v, ns)
                if r:
                    return r
            return r
    if isinstance(node, ast.Compare):
        left = _eval_node(node.left, ns)
        for op, comp_node in zip(node.ops, node.comparators):
            right = _eval_node(comp_node, ns)
            if not _compare(left, op, right):
                return False
            left = right
        return True
    if isinstance(node, ast.BinOp):
        l = _eval_node(node.left, ns)
        r = _eval_node(node.right, ns)
        if isinstance(node.op, ast.Add):
            return l + r
        if isinstance(node.op, ast.Sub):
            return l - r
        if isinstance(node.op, ast.Mult):
            return l * r
        if isinstance(node.op, ast.Div):
            return l / r
        if isinstance(node.op, ast.FloorDiv):
            return l // r
        if isinstance(node.op, ast.Mod):
            return l % r
    raise DSLError(f"unsupported node {type(node).__name__}")


def _compare(left: Any, op: ast.cmpop, right: Any) -> bool:
    if isinstance(op, ast.Eq):    return left == right
    if isinstance(op, ast.NotEq): return left != right
    if isinstance(op, ast.Lt):    return left < right
    if isinstance(op, ast.LtE):   return left <= right
    if isinstance(op, ast.Gt):    return left > right
    if isinstance(op, ast.GtE):   return left >= right
    if isinstance(op, ast.Is):    return left is right
    if isinstance(op, ast.IsNot): return left is not right
    if isinstance(op, ast.In):    return left in right
    if isinstance(op, ast.NotIn): return left not in right
    raise DSLError(f"unsupported comparison op {type(op).__name__}")


# ---------------------------------------------------------------------------
# Vocabulary objects passed into the evaluator namespace
# ---------------------------------------------------------------------------


class SelfRef:
    """Wraps the active combatant for ``self.X`` access."""
    def __init__(self, c: Combatant):
        self._c = c

    @property
    def hp(self) -> int: return self._c.current_hp
    @property
    def hp_max(self) -> int: return self._c.max_hp
    @property
    def hp_pct(self) -> float:
        return self._c.current_hp / self._c.max_hp if self._c.max_hp else 0.0
    @property
    def threatened_count(self) -> int:
        # Lookup hostile threateners against our position; expensive but
        # only one combatant.
        return 0  # placeholder until we have the encounter / grid context

    def has_condition(self, name: str) -> bool:
        return name in self._c.conditions


class EnemyResolver:
    """Wraps `enemy.*` selectors against the encounter and grid."""

    def __init__(self, actor: Combatant, encounter: Encounter, grid: Grid):
        self._actor = actor
        self._enc = encounter
        self._grid = grid

    def _enemies(self) -> list[Combatant]:
        return [
            ir.combatant for ir in self._enc.initiative
            if ir.combatant.team != self._actor.team
            and ir.combatant.current_hp > 0
            and not ir.combatant.is_unconscious()
        ]

    @property
    def any(self) -> bool: return bool(self._enemies())

    @property
    def count(self) -> int: return len(self._enemies())

    @property
    def closest(self) -> Combatant | None:
        en = self._enemies()
        if not en: return None
        return min(en, key=lambda e: self._grid.distance_between(self._actor, e))

    @property
    def lowest_hp(self) -> Combatant | None:
        en = self._enemies()
        if not en: return None
        return min(en, key=lambda e: e.current_hp)

    @property
    def lowest_hp_pct(self) -> Combatant | None:
        en = self._enemies()
        if not en: return None
        return min(en, key=lambda e: (e.current_hp / e.max_hp) if e.max_hp else 0)

    def in_range(self, r: int) -> Combatant | None:
        """Closest enemy within r squares; None if none."""
        en = self._enemies()
        if not en: return None
        c = min(en, key=lambda e: self._grid.distance_between(self._actor, e))
        if self._grid.distance_between(self._actor, c) <= r:
            return c
        return None

    def count_in_range(self, r: int) -> int:
        return sum(
            1 for e in self._enemies()
            if self._grid.distance_between(self._actor, e) <= r
        )


class AllyResolver:
    def __init__(self, actor: Combatant, encounter: Encounter, grid: Grid):
        self._actor = actor
        self._enc = encounter
        self._grid = grid

    def _allies(self) -> list[Combatant]:
        return [
            ir.combatant for ir in self._enc.initiative
            if ir.combatant.team == self._actor.team
            and ir.combatant.id != self._actor.id
            and ir.combatant.current_hp > 0
        ]

    @property
    def any(self) -> bool: return bool(self._allies())

    @property
    def lowest_hp_pct(self) -> Combatant | None:
        al = self._allies()
        if not al: return None
        return min(al, key=lambda c: (c.current_hp / c.max_hp) if c.max_hp else 0)

    @property
    def dying(self) -> Combatant | None:
        """Closest dying ally (HP < 0, not yet dead). None if none."""
        candidates = [
            ir.combatant for ir in self._enc.initiative
            if ir.combatant.team == self._actor.team
            and ir.combatant.id != self._actor.id
            and ir.combatant.current_hp <= 0
            and "dead" not in ir.combatant.conditions
        ]
        if not candidates:
            return None
        return min(
            candidates,
            key=lambda c: self._grid.distance_between(self._actor, c),
        )


def build_namespace(
    actor: Combatant,
    encounter: Encounter,
    grid: Grid,
) -> dict[str, Any]:
    return {
        "self":         SelfRef(actor),
        "enemy":        EnemyResolver(actor, encounter, grid),
        "ally":         AllyResolver(actor, encounter, grid),
        "round_number": encounter.round_number,
        "True": True, "False": False, "None": None,
    }


def build_reactive_namespace(
    actor: Combatant,
    encounter: Encounter,
    grid: Grid,
    *,
    kind: str,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Namespace for a reactive-interrupt or sub-action ``when`` clause.

    Inherits the base namespace (``self``, ``enemy``, ``ally``,
    ``round_number``) and overlays kind-specific bindings:

    - ``react: aoo``   — ``provoker`` (Combatant), ``weapon`` index list
      (the threatener's attack_options), ``aoos_left`` (per-round budget
      remaining).
    - ``react: brace`` — ``charger`` (Combatant), ``charger.distance``,
      etc.
    - ``react: cleave`` — ``primary`` (Combatant), ``candidates`` (list
      of adjacent enemies).
    - ``sub: full_attack`` — ``current_target``, ``iteration``,
      ``remaining_iteratives``.

    Phase 4 first slice ships the ``aoo`` namespace; the others land
    in subsequent slices.
    """
    ns = build_namespace(actor, encounter, grid)
    ctx = context or {}
    if kind == "aoo":
        provoker = ctx.get("provoker")
        ns["provoker"] = SelfRef(provoker) if provoker is not None else None
    elif kind == "brace":
        charger = ctx.get("charger")
        ns["charger"] = SelfRef(charger) if charger is not None else None
    elif kind == "cleave":
        primary = ctx.get("primary")
        ns["primary"] = SelfRef(primary) if primary is not None else None
        ns["candidates"] = ctx.get("candidates") or []
    elif kind == "full_attack":
        current = ctx.get("current_target")
        ns["current_target"] = (
            SelfRef(current) if current is not None else None
        )
        ns["iteration"] = ctx.get("iteration", 0)
    return ns


# ---------------------------------------------------------------------------
# Interpreter
# ---------------------------------------------------------------------------


@dataclass
class TurnIntent:
    """The interpreter's choice of action this turn — not yet executed.

    ``do`` is a copy of the matching rule's ``do`` block, with target
    expressions still as strings; the executor will resolve them against
    the namespace at execution time. ``rule_index`` indicates which rule
    fired (for traces).
    """

    rule_index: int
    do: dict
    namespace: dict[str, Any]


class Interpreter:
    def __init__(self, script: BehaviorScript):
        self.script = script

    def pick_turn(
        self,
        actor: Combatant,
        encounter: Encounter,
        grid: Grid,
    ) -> TurnIntent | None:
        ns = build_namespace(actor, encounter, grid)
        for i, rule in enumerate(self.script.rules):
            if rule.hero not in ("any",):
                # Future: role-based selection. For v1 'any' covers solo.
                pass
            if rule.when is not None:
                try:
                    matched = bool(evaluate(rule.when, ns))
                except DSLError:
                    raise
                if not matched:
                    continue
            return TurnIntent(rule_index=i, do=dict(rule.do), namespace=ns)
        return None
