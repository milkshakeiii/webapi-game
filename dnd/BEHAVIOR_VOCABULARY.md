# Behavior DSL Vocabulary

> **Status: live.** Active-turn rules use the v1 surface described in
> the bulk of this document. Reactive interrupts (AoO selection,
> brace, cleave continuation) and sub-action decision points
> (between full-attack iteratives) are authored via the v2 ``react:``
> / ``sub:`` clauses described in the **Reactive and sub-action
> rules** section below. Both surfaces compile to the same engine
> substrate (`actions.py` — see `DECISION_POINT_DSL.md` for the
> architecture).

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

---

# Reactive and sub-action rules (v2)

Active-turn rules above describe what a hero does **on their turn**.
The DSL also supports two additional rule kinds that fire **between**
or **outside** turns: reactive interrupts and sub-action decision
points. Both share the same `BehaviorScript` / `Rule` syntax — they
just add a `react:` or `sub:` discriminator that says when the rule
applies.

```yaml
rules:
  # Active rule (existing v1 syntax — turn-building).
  - when: enemy.closest.distance > 1
    do:
      composite: charge
      args: { target: enemy.closest }

  # Reactive rule: when an AoO opportunity comes up, take it only if
  # the provoker is bloodied; otherwise save the opportunity.
  - react: aoo
    when: provoker.hp_pct < 0.5
    do: { type: take_aoo, weapon: 0 }
  - react: aoo
    do: { type: pass_aoo }

  # Sub-action rule: between full-attack iteratives, retarget to a
  # different foe if the current one is down for the round.
  - sub: full_attack
    when: current_target.hp <= 0
    do: { type: retarget_full_attack, target: enemy.closest }
  - sub: full_attack
    do: { type: continue_full_attack }
```

## How rules dispatch

The Interpreter and the substrate cooperate:

- **Active rules** (rules with neither `react:` nor `sub:` set) feed
  `Interpreter.pick_turn` once per turn. The first matching rule's
  `do:` becomes the `TurnIntent`, which the substrate translates
  into a sequence of Actions. Same as v1.
- **Reactive rules** (`react: aoo` / `react: brace` / `react: cleave`)
  fire when the engine offers the actor a reactive interrupt. The
  rules with the matching `react:` field are walked in order; the
  first whose `when:` evaluates True picks the action via its `do:`.
- **Sub-action rules** (`sub: full_attack`) fire *between* iteratives
  in a full-attack chain (or, in future, between any other multi-
  step composite that surfaces sub-decisions).

If no reactive/sub rule matches, the engine falls back to a
v1-equivalent default — TakeAoO weapon 0, Brace springs, CleaveTo
the first adjacent foe, ContinueFullAttack while target alive. This
means scripts that don't author any reactive rules behave exactly
as they did in v1.

## Picker registration

For reactive/sub rules to fire, the script's compiled picker has to
be registered on the encounter. The sandbox tick worker does this
automatically when a deployment engages
(`register_script_pickers(hero, script, encounter)` is called inside
`_materialize_encounter`); for direct-engine tests, call the helper
yourself before the first interrupt:

```python
from dnd.engine.actions import register_script_pickers
register_script_pickers(hero, behavior_script, encounter)
```

The helper is a no-op if the script has no `react:` / `sub:` rules.

## react: aoo

Fires when the actor (the threatener) gets an attack-of-opportunity
opportunity against another combatant.

**Namespace bindings** (in addition to the active-turn base):

| Name | Type | Semantics |
|---|---|---|
| `provoker` | SelfRef | The combatant whose action provoked. Read `.hp`, `.hp_pct`, `.hp_max`, `.is_alive`, `.has_condition(name)`. |

**Allowed `do:` types:**

| Type | Fields | Effect |
|---|---|---|
| `take_aoo` | `weapon: int` (default 0) | Resolve the AoO with `actor.attack_options[weapon]`. Consumes one of the actor's per-round AoO budget. |
| `pass_aoo` | — | Decline the opportunity; no budget consumed; emits `aoo_pass` event. |

**Defaults if no rule matches:** `take_aoo` with weapon 0 (matches v1).

## react: brace

Fires when a charging foe ends adjacent to the actor and the actor
has both the `bracing` condition and a brace-flagged weapon ready.

**Namespace bindings:**

| Name | Type | Semantics |
|---|---|---|
| `charger` | SelfRef | The combatant who just charged. |

**Allowed `do:` types:**

| Type | Fields | Effect |
|---|---|---|
| `brace` | — | Spring the brace. Triggers a free attack at the charger with double damage; consumes the `bracing` condition. |
| `pass_brace` | — | Decline. Charger's attack resolves normally; `bracing` stays set so a later charger this round may still trigger it. |

**Defaults:** `brace` (matches v1's unconditional trigger).

## react: cleave

Fires when the actor's primary cleave attack hits and at least one
adjacent foe other than the primary is in reach.

**Namespace bindings:**

| Name | Type | Semantics |
|---|---|---|
| `primary` | SelfRef | The primary target (the one the cleave hit). |
| `candidates` | list[Combatant] | Adjacent foes other than the primary. |

**Allowed `do:` types:**

| Type | Fields | Effect |
|---|---|---|
| `cleave_to` | `target: <expr>` or `target_id: <id>` | Continue the cleave against the resolved combatant. The `target:` expression evaluates against the namespace (so `target: enemy.lowest_hp` works); the resolved combatant must be in `candidates` or the rule falls through. |
| `pass_cleave` | — | Skip the continuation. |

**Defaults:** `cleave_to` against the first candidate (matches v1).

## sub: full_attack

Fires *between* iteratives in a full-attack chain. The first
iterative always runs (it was the active-turn pick that brought us
here); the picker is consulted before each subsequent iterative.

**Namespace bindings:**

| Name | Type | Semantics |
|---|---|---|
| `current_target` | SelfRef | The actor's current target for the iterative chain (changes if a previous rule chose `retarget_full_attack`). |
| `candidates` | list[Combatant] | Other foes the actor could legally retarget to (adjacent for melee primaries; any visible for ranged). |
| `iteration` | int | Which iterative is about to fire (0-indexed). 0 means the first iterative — the picker isn't actually called there. |

**Allowed `do:` types:**

| Type | Fields | Effect |
|---|---|---|
| `continue_full_attack` | — | Take the next iterative against `current_target`. |
| `end_full_attack` | — | Stop the chain. Skip remaining iteratives. |
| `retarget_full_attack` | `target: <expr>` or `new_target_id: <id>` | Switch `current_target` to the resolved combatant; the next iterative swings at them. |

**Defaults:** `continue_full_attack` while `current_target` is alive
and at HP > 0; otherwise `end_full_attack`. The default never
retargets — patrons must opt in.

A note on rend (troll): the engine tracks claw hits per-target. If
the patron retargets mid-chain, the original target's tally is
preserved; if claws connect on the new target, that target also
becomes eligible for rend. Both rends fire if both reach 2+ claw
hits.

## A note on `is_alive` vs `hp <= 0`

`SelfRef.is_alive` returns True unless the `dead` condition is set.
For most creatures that's a clean "is this thing actually dead"
check. For orcs (and other creatures with the `ferocity` racial
trait) it's misleading: ferocity keeps `is_alive` True even at
negative HP — the creature is staggered and bleeding out, not dead.

For "this target is down for the round, time to switch", use
`current_target.hp <= 0` rather than `not current_target.is_alive`.

## Migration notes from v1

If you wrote v1 scripts:

- Active rules need no changes — the v1 turn-building syntax
  (`composite:` / `slots:` / `do.standard:` / etc.) is preserved
  end-to-end through `translate_intent` into substrate Actions.
- Reactive behaviors that v1 hardcoded (auto-take AoO with weapon
  0, auto-spring brace, auto-cleave-to-first-adjacent) now happen
  *because no rule overrode the default*. To keep v1 behavior, do
  nothing. To customize, add `react:` / `sub:` rules.

## Open future work

Tracked in `DECISION_POINT_DSL.md` and `WORK_QUEUE.md`:

- More reactive kinds: `react: counterspell`, `react: immediate_action`,
  `react: ready_action_trigger`. The plumbing pattern is in place;
  each just needs its own legal-actions enumeration + namespace.
- `sub:` for other composites that have natural mid-action choices
  (cleave already has `react: cleave`; charge could surface a
  sub-action point if/when partial-charge variants land).
- Continuous-tick world integration: when the actor is paused at a
  picker call but their patron is remote, who blocks the world
  clock? See `DECISION_POINT_DSL.md` §7.2 for the design proposal.
