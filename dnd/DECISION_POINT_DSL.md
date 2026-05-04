# Decision-Point DSL Redesign

**Status:** Proposal — design before code. No implementation has begun.

**Supersedes:** `BEHAVIOR_VOCABULARY.md` (the v1 turn-building DSL). The
existing behavior-script surface remains as syntactic sugar in the
final state, but it compiles down to the substrate described here —
there is **no hybrid execution path** at the end of this migration.

## 1. Why we're redesigning

The v1 model has a patron's behavior script return a `TurnIntent` —
the entire turn assembled before any of it resolves. The engine then
walks the slots in fixed order: free → swift → move → 5-ft step →
standard → end-of-turn riders.

Three things made this the wrong shape:

1. **It doesn't approximate Pathfinder play.** A real PF1 player
   attacks, sees the result, *then* decides whether to take the 5-ft
   step or stay flanking, whether to risk casting defensively or not,
   whether to follow the cleave to a different target than they were
   going to attack second. Building the turn ahead of time forces a
   commitment the actual game never asks for.

2. **Reactive abilities are hardcoded composites.** Cleave's "on hit,
   attack a second foe" lives in `_do_cleave`. Brace-vs-charge lives
   in `_do_charge`. Confused-actor table lives in
   `_resolve_confusion`. Each of these is the engine taking a
   decision the patron should be making — and the patron has no way
   to override or extend.

3. **Validity is bolted on, not load-bearing.** `validate_turn` was
   added late (audit fix #2). Even with it wired, the DSL's surface
   makes illegal turns *expressible*; the engine just rejects them
   later. The audit found a half-dozen edge cases (`five_foot_step`
   in difficult terrain, paralyzed-actor turns, casting_time
   collapsing to standard, etc.) that all stem from the same root:
   the patron's API isn't constrained by what's actually legal right
   now.

A fourth motivation, future-facing:

4. **A "list the legal actions, pick one" interface is what a human
   UI, a reinforcement-learning agent, and a tree-search bot all need
   anyway.** Fixed-form turn scripts can't drive any of those without
   shimming. The decision-point model is the universal interface.

## 2. The end-state architecture

### 2.1 Core API

Two functions:

```python
def enumerate_legal_actions(
    actor: Combatant,
    state: GameState,
) -> list[Action]:
    """Every action ``actor`` can legally take from ``state`` right now.

    The list always contains at least ``EndTurn`` (unless the actor is
    forced — confused, fleeing, etc., where the table substitutes the
    decision). Includes reactive opportunities the actor currently has
    pending (an AoO they can take, a brace they can spring, etc.)."""

def apply_action(
    action: Action,
    state: GameState,
    roller: Roller,
) -> ApplyResult:
    """Resolve ``action`` against ``state``, mutating it in place.

    Returns events (the same TurnEvent stream we have today) plus a
    ``next_decision_point`` field describing whose turn it is to pick
    next, and from what list. The engine never picks an action itself
    — the caller drives the loop."""
```

`GameState` is a thin wrapper over `(encounter, grid)` plus per-actor
ephemeral state (current decision context, mid-action progress, etc.).

### 2.2 The driver loop

The simulator is a loop of:

```python
while encounter.alive():
    actor, ctx = state.next_decision_owner()
    actions = enumerate_legal_actions(actor, state)
    chosen = picker_for(actor).pick(actor, state, actions, ctx)
    apply_action(chosen, state, roller)
```

`picker_for(actor)` resolves to:
- A patron-authored `Picker` (DSL-compiled or imperative).
- The default monster AI.
- A human UI proxy (queues actions and waits).
- An RL agent's policy (later).

The engine has no "execute the actor's whole turn" function. Turns
end when the picker chooses `EndTurn` *or* when forced action
restrictions exhaust the legal list (e.g., a stunned-rider just
clears).

### 2.3 The Action type

```python
@dataclass(frozen=True)
class Action:
    """One atomic-from-the-engine's-perspective choice.

    Subclasses are concrete actions; this base just exists for typing.
    Every Action knows how to:

      - describe itself (``label``) for traces / UI
      - identify the slot it consumes (``slot_kind``)
      - validate against ``state`` at apply time (defensive, since the
        list came from the engine — but cheap to recheck)
    """
    actor_id: str
    slot_kind: str  # "standard" | "move" | "swift" | "free" | "5ft" |
                    # "full_round" | "interrupt" | "sub_action" |
                    # "end_turn"
    label: str
```

Concrete subclasses (illustrative — the full vocabulary is below):

| Action | Fields | Notes |
|---|---|---|
| `Move` | `path: list[Square]` | Single destination is sugar; engine plans paths. |
| `Attack` | `target_id, weapon_index, options` | Single attack. |
| `FullAttack` | `target_id, options` | Iteratives; the iteratives themselves still surface as decision points (see §3.3). |
| `Charge` | `target_id, options` | Standard charge. Brace defender's reaction is its own decision point. |
| `Cast` | `spell_id, target, defensive, metamagic, spell_level` | Defensive flag is now a meaningful per-cast choice. |
| `Maneuver` | `kind, target_id, options` | Bull rush, trip, disarm, … |
| `DrawWeapon` | `weapon_id` | Move action. |
| `DrinkPotion` | `potion_id` | |
| `StandUp` | — | |
| `FiveFootStep` | `destination: Square` | |
| `TotalDefense` | — | |
| `FightDefensively` | `target_id` | |
| `AidAnother` | `ally_id, mode` | |
| `Run` | `direction` | |
| `Withdraw` | `direction` | |
| `ReadyAction` | `trigger, then_action` | The "then" is itself an Action template. |
| `Concentrate` | — | Multi-round-cast continuation. |
| `EndTurn` | — | Voluntary end. |
| `TakeAoO` | `provoker_id, weapon_index` | Reactive interrupt. |
| `PassAoO` | `provoker_id` | Decline a triggered AoO. |
| `Brace` | `charger_id` | Spring the brace. |
| `PassBrace` | — | Let the charge through unbraced. |
| `CleaveTo` | `secondary_target_id` | Continuation of a cleave on hit. |

This list is open — we add a new Action subclass when we add a new
mechanic. It's deliberately verbose: a `MoveTo(square=X)` plus an
`Attack(target=Y)` is two list entries, not one composite "attack
with movement". Composition emerges from picking a sequence; the
engine doesn't know about "turn shapes".

### 2.4 Decision-point taxonomy (engine-internal)

The engine classifies decision-points into five kinds for routing
and scheduling. **The taxonomy is engine-internal — pickers don't
see it.** Pickers receive a list of legal Actions; the kind is
encoded implicitly in *what's in the list* (an interrupt offers
`TakeAoO / PassAoO`; a sub-action offers `CleaveTo / EndFullAttack`;
an active turn offers the full vocabulary). See §4.1 on why.

The five kinds:

1. **Active** — it's the actor's normal turn-step; the legal list
   covers their full action vocabulary (move/standard/swift/free/
   end_turn).
2. **Forced-substituted** — a condition substitutes the legal list.
   Confusion d% rerolls into one of {act normally, babble,
   self-attack, attack nearest} as the legal set. Panicked excludes
   offensive actions. Cowering legal list = {EndTurn} only.
3. **Sub-action** — a multi-step action surfaces an intermediate
   choice. Between iteratives in a full attack, the actor picks
   `ContinueIterative / RetargetIterative / EndFullAttack`. After
   a charge attack, a pouncer picks the next natural-attack target.
   On a successful cleave, the cleaver picks the secondary target.
4. **Reactive interrupt** — another actor's action triggered a
   reaction this actor owns: AoO, brace vs. charge, readied-action
   trigger, immediate-action interrupt. The active actor's loop
   pauses; the interrupter's picker fires; then control returns.
   The interrupted action's resolution may or may not continue
   depending on the interrupt's outcome (an AoO that kills the
   caster aborts the cast).
5. **End-of-turn** — auras, ongoing-effect ticks (poison, bleed,
   regen), and aura-cooldown resets fire automatically; no picker
   call. The next actor in initiative becomes the decision owner.

This taxonomy is **not** an established Pathfinder framework. PF1
RAW describes individual rules (action types, the confusion table,
AoO triggers, cleave-on-hit) without a unifying schema. The five
kinds are a synthesis: PF1's natural mechanic clusters mapped onto
sequential-game-theory decision nodes (the same shape a chess
engine, MTG priority system, or MCTS framework uses). Rough mapping
to RAW:

| Kind | RAW source material |
|---|---|
| active | Action types chapter (PHB Ch. 8). |
| forced-substituted | Confusion d% table; panicked offensive ban; cowering "no actions"; nauseated "move only". |
| sub-action | Cleave's "if hit" clause; full-attack iteratives; pounce's natural-attack chain. |
| reactive interrupt | AoO triggers; brace vs. charge; readied actions; immediate actions; counterspell. |
| end-of-turn | Ongoing-effect ticks; aura cooldown resets. |

Edge cases the taxonomy will probably need to refine as we hit them:
casting defensively (parameter on Cast vs. its own sub-action point);
ready-action declaration vs. fire (active vs. interrupt — currently
treated as one of each); readied-counterspell with Spellcraft-to-
identify (a sub-action chain inside an interrupt). Refine the
schema before any phase that depends on a fix.

### 2.5 Action enumeration: templates vs. enumerations

Some action spaces are huge: every reachable square × every spell ×
every target. Two enumeration strategies, used together:

- **Concrete enumeration.** When the option set is small (every
  in-range enemy for a melee attack, every prepared spell for a
  cleric), enumerate every concrete `Action` instance.
- **Parameterized templates.** When the option set is too big to
  list (every reachable square for a Move, every legal Power Attack
  penalty), the engine returns a single `ActionTemplate` describing
  the parameter type, the legal-value predicate, and a constructor.
  The picker fills the parameter; `apply_action` re-checks legality.

Concretely:

```python
ActionTemplate(
    kind=Move,
    parameters={"destination": ParamSpec(
        type=Square,
        legal=lambda sq: sq in reachable_squares,
    )},
)
```

The picker treats the template as "for any Square in the legal set,
this Move is available". An RL agent flattens templates into
discrete actions; a human UI shows "Move..." then prompts for the
square; a patron script can declare `Move(destination=square.cover_from(enemy.closest))`
and the engine validates the produced square against the template's
predicate.

The split is per-action-kind: Move and FiveFootStep use templates;
Attack/Cast/Maneuver enumerate concretely (the target and weapon
sets are small).

### 2.6 What goes away

- `Turn` dataclass, `validate_turn`, `_intent_to_turn`.
- `_execute_slots`, the slot-walking loop in `execute_turn`.
- All `_execute_composite` branches that hardcode reactive logic
  (brace, cleave on-hit, charge → brace_attack, full_attack
  early-stop). Those become decision-point flows.
- `BehaviorScript`-as-engine-input. It survives as DSL surface but is
  parsed into a `Picker` and never reaches the executor.
- `TurnIntent` (the patron-→-engine handoff). Replaced by per-action
  `Action` instances flowing from picker to apply_action.

## 3. Mapping current behavior onto the new model

Three worked examples, to make the redesign concrete.

### 3.1 Move + attack

**v1**:
```python
do = {"slots": {
    "move": {"type": "move_toward", "target": ":enemy.closest"},
    "standard": {"type": "attack", "target": ":enemy.closest"},
}}
```
The whole turn assembled at once; executor walks slots in order.

**v2**:
```python
# Picker sees the legal-action list at decision-point 1:
#   [Move(...), Attack(...), Cast(...), TotalDefense(), Charge(...),
#    FightDefensively(...), EndTurn()]
# Patron rule: "if move available and target out of melee range, move
# toward closest enemy". Picks Move.
#
# Engine applies Move. State mutates. Next decision-point fires.
#
# Picker sees:
#   [Attack(target=closest), FiveFootStep(...), Cast(...),
#    DrawWeapon(...), EndTurn()]
# Move slot is now exhausted. Patron rule: "if attack available, take
# it on closest enemy". Picks Attack.
#
# Engine applies Attack (dice rolled, damage dealt). Next decision-
# point fires.
#
# Picker sees:
#   [FiveFootStep(...), DrawWeapon(...), DrinkPotion(...), EndTurn()]
# Standard now exhausted. No matching rule fires; default ending rule
# picks EndTurn().
```

The `Rule(when=..., do=...)` script that produced v1's turn is sugar:
the v2 picker scans `legal_actions` for the action shape matching
each `do:` clause, in turn, until none matches and falls through to
EndTurn. Same observable behavior; semantics now per-step.

### 3.2 Cleave on hit

**v1**: `_do_cleave` calls `_do_attack` on the primary, inspects the
event stream for a hit, and if so calls `_do_attack` again on a
selected adjacent foe. The patron has no input on the secondary
target.

**v2**:
```python
# Picker picks Cleave(target=primary).
#
# apply_action resolves the primary attack. If it hit and an adjacent
# foe exists, state.next_decision_owner returns:
#   (cleaver, kind="sub_action", legal=[CleaveTo(foe1), CleaveTo(foe2),
#                                       PassCleave()])
#
# Picker chooses CleaveTo(foe2) — the *patron* picks which adjacent
# foe gets the cleave attack.
#
# Engine applies CleaveTo. Both attacks recorded. Cleave action
# complete. Next normal decision-point fires.
```

Patrons who don't care can let the default sugar pick "first adjacent
foe" — same as today's hardcoded behavior. Patrons who do care
(e.g., target the spellcaster, not the closer fighter) get the lever.

### 3.3 Iterative attacks

**v1**: `_do_full_attack` runs all iteratives in a loop with hardcoded
"stop if target dies" early-exit.

**v2**: The full-attack action surfaces as a *sequence of
decision-points*:

```
Decision 1 (active, full_round slot): picker selects FullAttack(target=X).
  → apply_action runs the first iterative. Records hit/miss/damage.
Decision 2 (sub_action): picker sees [ContinueIterative, RetargetIterative(new_target), EndFullAttack].
  → picker picks ContinueIterative.
Decision 3 (sub_action): same shape; picker picks RetargetIterative(new) because target died.
  → apply_action runs second iterative against new.
...
Decision N (sub_action): EndFullAttack (or no iteratives left).
```

Power Attack penalty also becomes a per-iterative choice (RAW: it's
declared at the start of the round, but in practice scripts commonly
want different commitments per attack — and a per-iterative choice
is a strict superset that can be locked down later if needed).

### 3.4 Reactive AoO

**v1**: `_do_aoo` is called by movement code when a threatener is
detected. The threatener auto-takes the AoO with attack_options[0].
No patron involvement.

**v2**: When actor A's movement provokes from B, the engine fires a
**reactive interrupt** decision-point owned by B before A's movement
resolves further:

```
B's picker sees [TakeAoO(provoker=A, weapon=0), TakeAoO(provoker=A, weapon=1), PassAoO(A)].
B's picker chooses TakeAoO(weapon=0).
apply_action resolves the AoO (rolls, damages A).
Control returns to A's loop. If A is still alive, movement continues;
otherwise the action aborts.
```

Patrons who want "always take AoO with main hand" (the v1 default)
get that as a one-line rule in the sugar layer. Patrons who want
"don't waste my AoO on this 1-HP straggler — save it for the wizard
who's about to cast" get the lever.

## 4. The DSL surface

### 4.1 The picker

Every patron-driven actor has a `Picker`:

```python
class Picker:
    def pick(
        self,
        actor: Combatant,
        state: GameState,
        actions: list[Action | ActionTemplate],
    ) -> Action:
        """Select one Action from ``actions``.

        ``state`` is read-only — pickers don't mutate.

        Pickers are *kind-blind*: the engine's decision-point kind
        (§2.4) is not exposed. The kind is implicit in the legal-
        actions list — an AoO opportunity surfaces as TakeAoO /
        PassAoO entries; a cleave continuation surfaces as CleaveTo;
        a confused-actor decision surfaces as the substituted four
        choices. A picker that wants kind-shaped logic pattern-matches
        on action shape (e.g., 'if any TakeAoO in actions then ...')."""
```

The default monster AI is a `Picker` subclass. Patron-authored DSL
scripts compile to a `Picker`. An RL agent's policy is a `Picker`.

Why kind-blind:

- **Smaller surface.** No ``DecisionContext`` to spec, version, or
  document. Three arguments instead of four.
- **The actions encode the context.** Anything the picker would want
  from the kind is already in the action shape (an AoO has a
  ``provoker_id``; a cleave has a ``primary_target_id``; a
  confused-actor's choices have their own labels).
- **Future-proof.** Adding a new decision-point kind doesn't break
  existing pickers; they just see new Action subclasses they can
  ignore (or pattern-match on if they care).
- **The DSL keywords compile to action-shape matches.** ``react: aoo``
  in §4.3 is sugar for "fire when TakeAoO is in legal_actions" — not
  for "check ctx.kind".

### 4.2 Compiled-from-rules sugar

The current `BehaviorScript(rules=[Rule(when, do)])` syntax stays.
Compilation produces a `Picker` whose `pick` walks the rules in
order; for each rule:

1. Evaluate `when` against the actor + state namespace (current
   semantics — same expression vocabulary, same allowed AST).
2. If `when` evaluates True, scan `actions` for an entry matching the
   `do` shape (action kind + target + slot kind). If found, return
   it. The `do` block's parameter expressions resolve against the
   namespace and feed into `ActionTemplate` parameters.
3. If `when` is True but no matching action is in `actions` (e.g.,
   the script said `attack` but the actor's standard slot is
   already used), fall through to the next rule.
4. If no rule matches, the picker emits `EndTurn`.

This means existing scripts behave the same in v2 as in v1 *for the
cases where v1 was correct*. Cases where v1 silently flattened intra-
turn structure (cleave secondary, AoO target, post-attack 5-ft step
adjustment) now have decision-points the script doesn't speak to;
defaults take over.

### 4.3 Decision-point-aware syntax (post-Phase 4)

Once the substrate is in place, scripts can opt into the richer model
by adding `react:` and `sub:` rule clauses:

```yaml
rules:
  - when: enemy.closest.distance > 1
    do: move_toward(enemy.closest)
  - when: self.hp_pct >= 0.5
    do: full_attack(enemy.closest)
  - sub: full_attack
    when: target.is_dead
    do: retarget(enemy.closest)        # next iterative goes here
  - react: aoo
    when: provoker.is_caster
    do: take_aoo(weapon=0)             # always interrupt casters
  - react: aoo
    when: true
    do: pass_aoo                       # otherwise save the AoO
  - react: cleave
    do: cleave_to(enemy.weakest_spellcaster)
```

The `do:` vocabulary is the same as v1 (so the sugar path keeps
working), with new entries (`retarget`, `take_aoo`, `pass_aoo`,
`cleave_to`, `concentrate`, …) for the actions that v1 couldn't
express.

### 4.4 What the DSL no longer has

- `Turn` slots. Patrons write per-decision actions, not assembled
  turns.
- `delay` / explicit init manipulation in `do:`. (Re-introduced as
  `Delay` action if needed.)
- The "five_foot_step exclusivity" worry — the engine doesn't offer
  a 5-ft step in the legal list when movement was already taken.
- Validation errors at parse time about action-economy combinations.
  The engine's enumeration is the validity check.

## 5. Migration plan

The migration runs in five phases. **The end state has exactly one
execution model** — the substrate of §2. Old DSL syntax is
preserved as a compile target into pickers; there is no second path
through the engine.

### Phase 1 — substrate, no behavior change

Build `enumerate_legal_actions`, `apply_action`, and the `Action`
hierarchy. Cover *all* current functionality:

- Every existing composite (charge, full_attack, cast, all maneuvers,
  rage start/end, cleave, brace, etc.) gets an Action class.
- Every slot type representable.
- Reactive interrupts (AoO, brace, cleave continuation) modeled as
  `interrupt` decision points.

The existing `execute_turn` is untouched. New substrate is tested in
isolation:

- `test_enumerate_legal_actions.py` — for each interesting state,
  the legal list is what we expect.
- `test_apply_action.py` — for each Action, applying it produces the
  right events and state.

No existing test changes. **Exit criterion**: the new substrate
covers every state the existing engine reaches, and a parity test
(see §6) shows the two models produce identical event streams for
the existing test fixtures.

### Phase 2 — `execute_turn` reuses the substrate

Rewrite `execute_turn` as the driver loop of §2.2, with the
existing rule-matching logic compiled into a `Picker`. The old
composite functions get progressively dismantled:

- `_do_charge`, `_do_full_attack`, `_do_cleave`, etc. become thin
  wrappers around `apply_action` for their respective Action class.
- The reactive logic inside them (brace trigger, cleave on-hit,
  full-attack early-exit) becomes interrupt decision-points handled
  by the loop.

The patron-facing API doesn't change yet. Tests still pass.
**Exit criterion**: `_execute_composite` is empty (just a dispatch
to `apply_action`); `_execute_slots` is gone; all 1100+ existing
tests pass on the new internals.

### Phase 3 — reactive abilities surface as decision points

Brace, cleave, AoO selection, confused-actor sub-list — each gets
its own `interrupt` or `forced_substituted` decision point in the
new model, with patron pickers able to override defaults. The
default picker maintains current behavior (so a patron who hasn't
touched their script keeps getting the v1 outcome).

Tests for reactive behaviors get split: one set verifies the default
picker produces the v1 outcome (parity); another set exercises
patron overrides. **Exit criterion**: the engine no longer makes any
reactive choice silently — every choice flows through a Picker.

### Phase 4 — patron-authored decision-point syntax

Add `react:` and `sub:` rule clauses (§4.3). Update parser,
namespace builder for the new contexts, vocabulary doc. Existing
scripts unchanged; new scripts can use the richer surface.

Add documentation: a successor to `BEHAVIOR_VOCABULARY.md` covering
the v2 vocabulary in full. The v1 doc is marked superseded.

**Exit criterion**: every reactive behavior our existing tests cover
is also expressible in patron-authored DSL.

### Phase 5 — turn-building infrastructure removed

Delete:

- `Turn` dataclass and its imports.
- `validate_turn`, `TurnValidationError`, `_intent_to_turn`,
  `_FULL_ROUND_COMPOSITES` / `_FREE_COMPOSITES` mappings.
- The `Turn`-based legality checks scattered through condition hooks
  (those become legality predicates inside `enumerate_legal_actions`).

The old DSL syntax stays — but now it provably has *no separate
execution path*; it's just sugar that compiles to pickers. Verify by
removing the old executor module entirely and checking nothing
imports it outside of test fixtures.

**Exit criterion**: `git grep` for `validate_turn` returns zero
hits. The engine has one execution model.

## 6. Test strategy

The migration is high-risk for regressions. Three protections:

### 6.1 Parity harness (Phase 1 → Phase 2)

A `test_parity.py` runs every existing turn-script test through both
models and asserts identical event streams. Built in Phase 1, kept
green throughout Phase 2. Dropped at the end of Phase 2 (the old
model is gone).

### 6.2 Substrate exhaustiveness (Phase 1 onward)

A property-style test sweeps states (combinations of conditions,
positions, equipment) and asserts:

- `enumerate_legal_actions` contains exactly the actions matching a
  hand-coded reference predicate.
- `apply_action` is total: applied to any (action, state) pair from
  the enumeration, it doesn't raise.
- `apply_action` round-trips with `enumerate_legal_actions`: the
  next-decision-point's `legal_actions` is non-empty unless the
  encounter ended.

### 6.3 Coverage roll-up still applies

`coverage.py` keys are mostly orthogonal to the execution model
change — they're about which mechanics resolve correctly, not how
the executor walks them. A few entries get retired (`combat.5_foot_step`'s
"validate_turn enforces exclusivity" wording becomes "engine doesn't
offer the 5-ft step in the legal list"); the test_coverage.py
roll-up keeps the inventory honest.

## 7. Open design questions

These are flagged for resolution before each phase begins. None block
the doc; all need an answer before code lands.

1. **Random outcomes inside an action.** When `Attack` resolves, the
   d20 + damage roll happens inside `apply_action` and the result is
   visible in the events. The picker sees the result before its next
   decision. **Question**: do we ever want the picker to choose
   between *outcomes* (e.g., reroll as part of a feat)? Probably yes
   for Lucky / fortune-teller-style — model as another reactive
   interrupt at the moment of the roll. Out of scope for Phase 1-3,
   but the architecture must allow it.

2. **Continuous-tick world interaction.** The sandbox has a tick
   worker that advances the world while patrons are remote. When an
   actor reaches a decision point, who blocks? Proposal: the actor's
   **own** clock pauses while their picker thinks; the world-clock
   keeps moving, but other actors' clocks pause if they're waiting on
   this actor's resolution (initiative ordering). Cross-encounter
   pauses are unaffected. Needs validation against `SANDBOX_DESIGN.md`.

3. **Ready actions.** `ReadyAction(trigger, then)` is itself a
   delayed decision-point — the trigger fires, the actor's picker
   fires *then* against the trigger context. Cleaner than v1's
   "store a partial intent" approach. Land in Phase 3 alongside
   reactive interrupts.

4. **Action bundles for performance.** Some patrons (and bots) will
   pick the same action class repeatedly with parameter sweeps
   (e.g., Move-then-Attack). If per-decision-point overhead matters,
   we can let the engine batch a sequence into one apply_action call
   when the picker pre-commits. **Defer until measured** — premature.

5. **Determinism.** The order of interrupt resolution matters when
   multiple AoOs fire from the same provocation. RAW is silent;
   v1 fires them in `grid.combatants.items()` iteration order.
   **Resolved (2026-05-04):** initiative order among threateners,
   highest first; ties broken by combatant id, lexicographic. Stable
   across runs and replay-safe.

6. **Forced movement and "no decision".** Bull-rushed targets get
   shoved per RAW with no choice on direction. We model these as
   apply_action effects that mutate state without a decision point —
   the recipient doesn't pick. Same with confused-attacks-self
   (engine picks the target via the d% table, then a normal attack
   action runs against the chosen target with no further patron
   input).
   **Resolved (2026-05-04):** confirmed. The d% table substitutes
   *for* the picker call (forced-substituted kind), not as a
   sub-decision; the resulting attack runs as a continuation inside
   the same apply_action. Bull-rushed motion mutates state with no
   picker call.

7. **DSL backwards compat completeness.** Phase 4 must demonstrate
   parity for every existing patron script we care about. Today
   that's the contents of `dnd/sandbox/` test scripts and the
   internal monster AI. Confirm the list is exhaustive before
   Phase 5 deletion.

## 8. Why this isn't a hybrid at the end

A skeptic could read §4.2 ("compiled-from-rules sugar") and say the
old DSL still exists, so there's a hybrid. To be precise:

- The old **syntax** (`BehaviorScript`, `Rule`, `when`/`do`) survives.
- The old **execution model** (`Turn`, `validate_turn`, slot dispatch,
  `_execute_composite`, `_execute_slots`) is **deleted** in Phase 5.

What remains is one engine — the decision-point loop — with two
front-end syntaxes for authoring pickers (legacy compiled and
v2-native). Both produce identical `Picker` objects. There's exactly
one code path through `apply_action`. Removing the legacy syntax at
some future date is a straightforward DSL deprecation, not an engine
change.

## 9. Cross-references

- Supersedes: `BEHAVIOR_VOCABULARY.md` (v1 vocabulary; v2 successor
  to be written in Phase 4).
- Sandbox-layer integration: `SANDBOX_DESIGN.md` (continuous-tick
  worker; question 7.2 above).
- Mechanic correctness baseline: `coverage.py` and the rules dumps
  in `checklist/rules/` — most entries are unaffected; a handful
  re-word during Phase 5.
- Migration tracking: add a "DSL v2 migration" section to
  `WORK_QUEUE.md` once Phase 1 begins, with one item per phase.
