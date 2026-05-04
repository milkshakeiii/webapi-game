# Behavior DSL Vocabulary (v1 Draft)

> **Status: being superseded.** This document describes the v1 turn-
> building DSL. A redesign — the decision-point DSL — is proposed in
> `DECISION_POINT_DSL.md` and supersedes the execution model here.
> The expression vocabulary (conditions, target selectors) carries
> over largely unchanged; what disappears is the `Turn` slot
> structure and the assumption that the patron commits to a whole
> turn before any of it resolves. In particular: reactive actions
> like `ready_action`, immediate actions, AoO selection, and cleave's
> secondary-target choice — which v1 either deferred or hardcoded —
> become first-class decision points in v2. Don't extend v1 in ways
> the migration would have to undo.

This is the constrained dictionary of expressions and actions a behavior
script can use. The parser ships only what's listed here; nothing else
parses.

Format:

- **Conditions / value expressions** — used inside `if:` clauses; return
  bool, int, float, or string. Conditions can be combined with `and`,
  `or`, `not`, and standard comparison operators (`==`, `!=`, `<`, `<=`,
  `>`, `>=`).
- **Target expressions** — used as the `target:`, `move_to:`, etc. value
  in actions; return a single Combatant or Square (or null if no match).
- **Actions** — used as the `do:` of a rule; describe what the active
  hero does this turn.

For each entry: `name(args)` → return-type — one-line semantics.

The vocabulary is intentionally small. **If something obvious is missing,
that's a redline candidate**; flag it. We can also cut entries that feel
overspecific.

---

## Conditions / value expressions

### Self (the hero whose turn this is)

| Expression | Returns | Semantics |
|---|---|---|
| `self.hp_pct` | float | Current HP / max HP, in [0, 1]. |
| `self.hp` | int | Current HP. |
| `self.hp_max` | int | Maximum HP. |
| `self.has_condition(c)` | bool | True if condition `c` (e.g., `prone`, `staggered`) is active. |
| `self.has(item_id)` | bool | True if at least one of `item_id` is in inventory. |
| `self.uses_left(ability_id)` | int | Remaining uses of a per-day ability (rage rounds, smite uses, channel uses, stunning fist, etc.). |
| `self.slots_left(spell_level)` | int | Spell slots remaining at this level. |
| `self.knows(spell_id)` | bool | Has the spell prepared (prepared casters) or known (spontaneous). |
| `self.threatened_count` | int | Number of hostile combatants currently threatening this hero. |
| `self.is_flanking(target)` | bool | True if hero is flanking `target` with an ally. |
| `self.is_flanked` | bool | True if two hostiles flank the hero. |
| `self.action_available(shape)` | bool | True if turn-shape `shape` (e.g., `full_round`, `standard_and_move`) is still usable this round. |

### Enemy presence (existence/count predicates)

| Expression | Returns | Semantics |
|---|---|---|
| `enemy.any` | bool | At least one enemy is visible. |
| `enemy.count` | int | Total visible enemies. |
| `enemy.count_in_range(r)` | int | Visible enemies within `r` squares of self. |
| `enemy.cluster_of(n, range=r)` | bool | At least one cluster of ≥`n` enemies all within `r` of each other. |
| `enemy.has(condition)` | bool | At least one enemy has the named condition. |

### Ally presence

| Expression | Returns | Semantics |
|---|---|---|
| `ally.any` | bool | At least one party member exists (excluding self). |
| `ally.count_in_range(r)` | int | Allies within `r` squares (subject to coordination range). |
| `ally.role_present(role)` | bool | True if the party has a hero filling `role`. |

### Combat / world state

| Expression | Returns | Semantics |
|---|---|---|
| `round_number` | int | Current round (1 on first round of combat). |
| `surprise_round` | bool | True during the surprise round only. |
| `mode` | string | Current mode: `combat`, `travel`, `scavenging`, `crafting`, `victorious`, `retreating`. |
| `signal(role, msg)` | bool | True if `role` raised signal `msg` since last cleared. |

---

## Target expressions

### Single-combatant selectors

Each returns one Combatant or null. If null, any rule whose action
requires a target falls through.

| Expression | Returns | Semantics |
|---|---|---|
| `enemy.closest` | Combatant | Nearest visible enemy. |
| `enemy.lowest_hp_pct` | Combatant | Visible enemy with lowest HP percent. |
| `enemy.lowest_hp` | Combatant | Visible enemy with lowest absolute HP. |
| `enemy.highest_threat` | Combatant | Engine's threat heuristic: recent damage dealt to allies + caster level. |
| `enemy.weakest_spellcaster` | Combatant | Lowest-CL visible spellcaster. |
| `enemy.flanked` | Combatant | Closest enemy currently flanked by allies. |
| `enemy.flat_footed` | Combatant | Closest flat-footed enemy (denied Dex). |
| `enemy.in_range(r)` | Combatant | Closest enemy within `r` squares. |
| `enemy.targeting(ally_role)` | Combatant | Closest enemy currently targeting that ally. |
| `enemy.with_condition(c)` | Combatant | Closest enemy with condition `c`. |
| `ally.role(name)` | Combatant | Party member filling that role; null if absent. |
| `ally.lowest_hp_pct` | Combatant | Ally (or self) with lowest HP percent. |
| `ally.dying` | Combatant | Closest dying ally (HP < 0). |
| `self` | Combatant | The hero whose turn this is. |

### Position selectors

Each returns a Square (an `(x, y)` tuple) or null.

| Expression | Returns | Semantics |
|---|---|---|
| `square.behind(combatant)` | Square | Empty square such that `combatant` is between self and the nearest enemy. |
| `square.adjacent_to(combatant)` | Square | Empty square adjacent to that combatant. |
| `square.flanking(target=e, with=a)` | Square | Square that creates a flank on `e` together with ally `a`. |
| `square.cover_from(combatant)` | Square | Closest empty square providing cover from that combatant. |
| `square.cluster_center(of=enemy_filter)` | Square | Geometric center of an enemy cluster (for AoE targeting). |

---

## Actions

A rule's `do:` is a **Turn**: a structured object with the slots PF1's
action economy actually defines. The parser builds the Turn slot by slot
and validates at parse time, so invalid turns are unrepresentable.

### Turn slots

| Slot | Type | Notes |
|---|---|---|
| `full_round` | full-round action | If set, consumes both `standard` and `move` slots. |
| `standard` | standard action | At most one. |
| `move` | move action OR move-equivalent | At most one. May contain a movement action (`move_to`, `5ft_step` no — see below) or a non-movement move-equivalent (`draw_weapon`, `stand_up`, `manipulate_item`). May also be filled with another standard action (taking a second standard-action's worth of effect, with the standard slot left empty). |
| `swift` | swift action | At most one per turn. |
| `five_foot_step` | direction or square | Allowed only if no other slot provides movement. |
| `free` | list of free actions | Any number; each must be on the legal-as-free list. |

### Validation rules

Enforced at parse time. A turn that violates any rule is rejected with a
specific error message naming the conflict.

1. **Action exclusivity.** If `full_round` is set, `standard` and `move`
   must both be null.
2. **Five-foot-step exclusivity.** If `five_foot_step` is set, no other
   slot can provide movement (no `move_to`/`move_toward`/`move_away`
   in `move`; no `charge`/`withdraw`/`run` in `full_round`).
3. **Swift uniqueness.** At most one swift action. Setting `swift` also
   counts against the *next* round's immediate-action allowance, but
   that's tracked at runtime, not at parse time.
4. **Free-action legality.** Every entry in `free` must be on the
   legal-as-free list (drop_item, fall_prone, speak, signal,
   end_concentration, drop_held_charge).
5. **Actor legality.** The actor must be able to legally take each
   filled action given current state — e.g., can't `drink` while
   grappled, can't `cast` while silenced for verbal-component spells.

### Examples — explicit slot form

```yaml
# Cast and 5-ft step
do:
  standard: cast(spell=cure_light_wounds, target=ally.lowest_hp_pct)
  five_foot_step: north
  swift: null

# Draw weapon and attack (move slot fills with a non-movement equivalent)
do:
  standard: attack(target=enemy.closest)
  move: draw_weapon(longsword)
  five_foot_step: north   # legal: move slot has no movement

# Two move actions, no standard
do:
  move: stand_up()
  # standard left empty, second move action would go in 'standard' slot if needed

# Total defense, still using move
do:
  standard: total_defense
  move: move_to(square=square.cover_from(enemy.closest))

# Free-action coordination
do:
  standard: full_attack(target=enemy.flanked)
  free:
    - signal(role=healer, message="i'm flanking, watch my back")
```

### Named composites (v1 shipped list)

Sugar for the common patterns. Each compiles to a specific slot fill —
the parser produces the same `Turn` object either way.

| Composite | Slot expansion |
|---|---|
| `charge(target, swift?, free?)` | `full_round: charge(target)` |
| `full_attack(target, options?, swift?, free?)` | `full_round: full_attack(target, options)` |
| `withdraw(direction, swift?, free?)` | `full_round: withdraw(direction)` |
| `run(direction, free?)` | `full_round: run(direction)` (swift not allowed; running doesn't leave one) |
| `total_defense(move?, swift?, free?)` | `standard: total_defense_action` |
| `attack_and_step(target, step, swift?, free?)` | `standard: attack(target)`, `five_foot_step: step` |
| `attack_and_move(target, move_to, swift?, free?)` | `standard: attack(target)`, `move: move_to(square)` |
| `cast(spell, target, options?, swift?, free?)` | `standard: cast(spell, target, options)` (engine derives whether full-round needed from spell entry) |
| `cast_and_step(spell, target, step, swift?, free?)` | `standard: cast(...)`, `five_foot_step: step` |
| `cast_and_move(spell, target, move_to, swift?, free?)` | `standard: cast(...)`, `move: move_to(square)` |
| `cast_defensive(spell, target, swift?, free?)` | `standard: cast_defensive(...)` (rolls concentration vs DC 15 + spell level) |
| `delay(swift?, free?)` | special — postpones initiative this round |
| `ready_action(trigger, then, swift?, free?)` | `standard: ready_action(trigger, then)` |
| `hold(swift?, free?)` | all action slots null; only `free`/`swift` allowed |

Anything not in the composite list is written in explicit slot form. The
slot form is always available; composites are convenience.

### Movement actions (fill `move:` or `move_to:` slot)

| Action | Args | Semantics |
|---|---|---|
| `move_to(target)` | square | Pathfind to a square, up to speed. |
| `move_toward(target)` | combatant | Move up to speed toward `target`. |
| `move_away(target)` | combatant | Move up to speed away from `target`. |
| `5ft_step(direction or target)` | direction or square | Take a 5-ft step. |
| `stand_up` | — | Stand from prone (move action; provokes AoO). |
| `draw_weapon(id)` | weapon id | Draw a stowed weapon (move action; or free with high BAB). |
| `sheathe_weapon(id)` | weapon id | Stow a weapon. |

### Attack actions (fill `standard:` or `full_round:` slot)

| Action | Args | Semantics |
|---|---|---|
| `attack(target, weapon=?)` | combatant | Single standard attack. |
| `full_attack(target, options=?)` | combatant + opts | All iterative attacks; options like `power_attack: N`. |
| `charge(target)` | combatant | Full-round straight-line move + single attack at +2/-2 AC. |
| `aid_another(ally, type=attack/ac)` | ally + flag | Standard action; +2 to ally's next attack or +2 AC vs next attack. |
| `combat_maneuver(type, target)` | type + combatant | Trip, grapple, disarm, sunder, bull_rush, overrun. |
| `cleave(target)` | combatant | If hit, makes a follow-up attack on adjacent foe. |

### Spell actions (fill `standard:` or `full_round:` slot)

| Action | Args | Semantics |
|---|---|---|
| `cast(spell, target, options=?)` | spell id, target, opts | Cast a spell; engine derives action type from spell entry. |
| `cast_defensive(spell, target)` | spell id, target | Cast on the defensive (concentration check vs DC 15+spell level). |
| `concentrate(spell_id)` | spell id | Maintain a concentration-required spell. |

### Item actions

| Action | Args | Semantics |
|---|---|---|
| `drink(item_id)` | potion id | Move action: drink a potion (target self by default). |
| `apply_oil(item_id, target=ally)` | item, ally | Standard action: apply oil to ally. |
| `use_item(item_id, target?)` | item, target | Generic use of a magic item / scroll. |

### Class ability actions

| Action | Args | Semantics |
|---|---|---|
| `rage_start` | — | Swift action: enter rage (barbarian). |
| `rage_end` | — | Free action: end rage. |
| `bardic_performance(type)` | type | Standard (start) / free (sustain): Inspire Courage, Countersong, Distraction, Fascinate. |
| `smite_evil(target)` | combatant | Swift: declare a target evil for smite (paladin). |
| `channel_energy(positive_or_negative)` | flag | Standard action: 30-ft burst heal/harm. |
| `stunning_fist(target)` | combatant | Modify a melee attack into a Stunning Fist (monk). |

### Reactive / coordination actions

| Action | Args | Semantics |
|---|---|---|
| `signal(role, message)` | role, str | Free: raise a signal that another rule can read. |
| `ready_action(trigger, then=action)` | trigger spec, action | Standard: prepare an action triggered by a future event. |
| `delay()` | — | Move self later in initiative this round. |

### Free actions

| Action | Args | Semantics |
|---|---|---|
| `drop_item(item_id)` | item | Drop a held item. |
| `fall_prone` | — | Drop prone deliberately. |
| `speak(message)` | str | Narrative; appears in the deployment trace. |

### Defensive / pass

These are slot fillers (typically for `standard:`):

| Action | Slot | Semantics |
|---|---|---|
| `total_defense` | standard | +4 dodge AC; cannot make AoOs this round. (Move slot still available.) |
| `total_defense_full` | full_round | Same +4 dodge AC, but commits the whole turn. |
| `hold` | — | Pass: all action slots null. (Use the `hold()` composite; produces an empty turn.) |

---

## What's deliberately not here (yet)

These exist in PF1 but are out of scope for v1 vocabulary. Flag if you
want any in:

- **Polymorph** and shape-changing actions. (Phase 4+.)
- **Metamagic** application (Empower, Maximize, Quicken). (Phase 4+.)
- **Counterspell** / dispel-on-cast. (Phase 4+.)
- **Combat reflexes mid-flow tweaks** beyond passive auto-AoOs.
- **Two-weapon attacks** as a separate action shape (folded into
  `full_attack` with options).
- **Mounted combat** actions.
- **Grapple maintenance** beyond `combat_maneuver(grapple, target)`.
- **User-defined predicates / macros**. (Constrained vocabulary; v1 ships
  exactly this list.)

---

## Total

- 33 conditions / value expressions
- 19 target expressions (14 combatant selectors, 5 square selectors)
- 6 turn slots + 5 validation rules + 14 named composites + ~30 slot-filler
  actions across movement/attack/spell/item/class/reactive/free/defensive
  categories.

Redline freely. After your sign-off I wire up the parser + interpreter.
