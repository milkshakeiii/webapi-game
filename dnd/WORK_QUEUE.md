# Work Queue

Prioritized roll-up of pending work across the project. Three sources
feed in:

1. **Engine-mechanic gaps** — every `NOT_IMPLEMENTED` / `PARTIAL`
   entry in `coverage.py`.
2. **Sandbox-layer deferrals** — the "Deferred Scope Tracker" table
   in `SANDBOX_DESIGN.md`.
3. **Playtest finds** — bugs / fidelity gaps surfaced by hands-on
   sessions, before they get categorized into one of the above.

This file is the synthesis. When something's done, move it to the
"Recently shipped" section at the bottom (with a date) before
deleting in the next cleanup pass.

## How items get on this list

- A new playtest find → first appears here as a P0/P1 line item
  with a one-line description; if it's a coverage gap, the
  corresponding `coverage.py` entry gets updated to point at the
  initiative driving its fix.
- A new content addition → `tests/test_coverage.py` will fail until
  classified, surfacing the gap automatically.

## Priority buckets

- **P0** — snackable. <2 hours, fixes something biting *now*.
  Should clear in the next session or two.
- **P1** — medium initiative. A day or two of focused work.
  Done as a coherent batch (e.g., "all undead immunities" or
  "iterative-attack feats").
- **P2** — big rock. Multi-day or multi-week. Usually a sandbox-
  layer phase (parties, crafting, dens).

---

## DSL v2 migration (2026-05-04 — proposal stage)

Decision-point execution model replacing the turn-building DSL.
Design lives in `DECISION_POINT_DSL.md`; this is the rolled-up
phase tracker.

- **Phase 1** — substrate (`enumerate_legal_actions`, `apply_action`,
  `Action` hierarchy). New tests in isolation. Existing executor
  untouched. Parity harness verifies the substrate covers every
  state the existing engine reaches. Estimate: 2-3 days.
- **Phase 2** — `execute_turn` rewritten as the driver loop. Old
  composites become thin wrappers over `apply_action`. Reactive
  logic still hardcoded but routed through interrupt decision-points
  internally. All existing tests pass. Estimate: 2 days.
- **Phase 3** — reactive abilities (brace, cleave, AoO selection,
  confused) surface as decision-points patrons can override.
  Default pickers preserve v1 behavior so untouched scripts don't
  change. Estimate: 2 days.
- **Phase 4** — `react:` and `sub:` DSL syntax for decision-point-
  aware patron scripts. v2 vocabulary doc supersedes
  `BEHAVIOR_VOCABULARY.md`. Estimate: 1-2 days.
- **Phase 5** — delete `Turn`, `validate_turn`, `_intent_to_turn`,
  the slot dispatch, the old `_execute_composite` / `_execute_slots`.
  One execution model in the codebase. Estimate: half a day.

Open design questions in §7 of the doc need answers as each phase
begins (random-outcome reactives, continuous-tick interaction, ready
actions, determinism of multi-AoO ordering, etc.).

---

## Audit follow-ups (2026-05-04)

Five-slice audit against the d20pfsrd dumps in `dnd/checklist/rules/`
landed the four high-severity fixes (defensive cast DC, validate_turn
wiring, ranged AoO, casting_time, plus the batch-A six). The
remaining medium/low findings below are all tracked in `coverage.py`
as `PARTIAL` or `NOT_IMPLEMENTED` with explicit gap notes — this list
is just the prioritized roll-up.

### P0 — small numeric fixes (each ~30 min with a test)

- Stunned: add -2 AC modifier; drop held items on apply; +4 to attacker's
  CMB vs stunned target. `coverage.CONDITIONS["stunned"]`.
- Cowering: add -2 AC modifier. `coverage.CONDITIONS["cowering"]`.
- Pinned: add -4 AC modifier. `coverage.CONDITIONS["pinned"]`.
- Stunned action ban also via validate_turn (not just the
  stunned_until_round rider). Externally-applied stun currently
  doesn't block actions.
- Combat maneuver: Tiny-or-smaller use Dex (not Str) for CMB.
  `coverage.combat_mechanics["combat.combat_maneuver_basic"]`.
- Combat maneuver: auto-success vs immobilized/unconscious/helpless;
  +4 vs stunned. Same coverage entry.
- Bull rush: enforce one-size-larger restriction; "move with target"
  option. `coverage["combat.bull_rush"]`.
- Trip: fail-by-10 self-prone path (currently unreachable);
  flying/legless/ooze immunity. `coverage["combat.trip"]`.
- Disarm: fail-by-10 self-drop; -4 unarmed-disarm penalty.
  `coverage["combat.disarm"]`.
- Overrun: target's "avoid" choice. `coverage["combat.overrun"]`.
- 5-foot step: reject in difficult terrain.
  `coverage["combat.5_foot_step"]`.
- Charge: -2 AC penalty until next turn. `coverage["combat.charge"]`.
- Flat-footed: block AoOs unless Combat Reflexes. `coverage["combat.aoo"]`.
- Threatened squares: unarmed without Improved Unarmed Strike doesn't
  threaten. `coverage["combat.threatened_squares"]`.
- AoO trigger: unarmed-strike-vs-armed provokes from the armed
  target. `coverage["combat.aoo_provoking_actions"]`.
- Grapple: humanoid-without-2-free-hands -4 CMB.
  `coverage.CONDITIONS["grappled"]`.

### P1 — coherent batches

- **Spell Resistance for non-monsters.** Currently scoped to
  `target.template_kind == "monster"`. Drow racial SR, SR-granting
  items, and the SR buff spell are silently SR 0. Generalize the
  lookup. `coverage["magic.spell_resistance"]`.
- **Evasion / Improved Evasion / Mettle.** Class features absent
  entirely. Rogue/monk Reflex-half saves should deal zero on success
  (evasion); Improved Evasion adds half-on-fail. Mettle is the
  Fort/Will analogue. `coverage["combat.evasion"|"...improved..."|
  "...mettle"]`.
- **Broken-item penalties.** `InventoryItem.broken` flag is set but
  never consulted in attack/AC/Wand-charge math. Wire the four
  RAW-prescribed penalty paths. `coverage["combat.broken_item_penalties"]`.
- **Concentration-check broadening.** RAW-prescribed triggers
  beyond the grappled / damage-from-AoO paths: entangled cast, pinned
  cast, vigorous/violent motion, severe weather, continuous damage
  during cast. `coverage["magic.concentration_*"]`.
- **Fear behaviors.** Frightened "must flee from source"; Panicked
  "drop items + flee + cornered defaults to total defense"; Fascinated
  "obvious threat breaks effect". All currently bypassed.
  `coverage.CONDITIONS["frightened"|"panicked"|"fascinated"]`.

### P2 — structural

- **Multi-round cast deferred resolution.** Spells with casting_time
  >= 1 round currently resolve on the same turn; RAW says they
  complete "just before the caster's next turn" (or N rounds later
  for multi-round) with concentration checks on any interruption
  during the wait. `coverage["magic.cast_in_progress"]`.
- **Material / focus / divine-focus components.** Eschew Materials
  is a no-op marker today. Pouch / spellbook / holy symbol tracking,
  loss-on-disarm, etc. `coverage["magic.casting_components_m|f|df"]`.
- **Immediate actions.** No model exists. Consumes next round's swift
  per RAW. Driver: counterspells will need this; some defensive
  metamagic too. `coverage["combat.immediate_action"]`.
- **Standard-as-move substitution.** "Instead of taking a standard
  action, you may take a move action." Engine doesn't model the
  swap. `coverage["combat.action_swap_standard_to_move"]`.

---

## P0 — snackable wins

### Iterative-attack BAB sanity check

`_do_full_attack` computes `n_attacks = max(1, (bab - 1) // 5 + 1)`
which gives 1@BAB1-5, 2@BAB6-10, 3@BAB11-15, 4@BAB16+. Cross-check
against PF1 RAW (which is the same formula). Probably fine, but
hasn't been deliberately tested. Add a parametric test.

**Source:** ad-hoc audit candidate.
**Size:** S.

### Death threshold: -CON vs -10

Engine uses `current_hp <= -10` everywhere as the death threshold
(3.5e RAW). PF1 RAW is `<= -CON`. For most monsters CON 12-16 means
they should live a couple HP longer; for high-CON creatures it's
significant. Centralize the threshold in `_apply_post_damage_state`
so we change it in one place.

**Source:** noted in passing during ferocity work.
**Size:** S.

### Stunning Fist composite action

Monk gets `stunning_fist_uses` resource on level-up but no composite
action exists to spend it. Should be a swift declaration "next
attack this turn forces a Fort save vs DC 10 + 1/2 level + Wis or
target is stunned 1 round."

**Source:** `coverage.CLASS_FEATURES_L1["stunning_fist_1day"]` =
`PARTIAL`.
**Size:** S-M.

### Half-elf adaptability

Bonus Skill Focus feat at L1. Currently the feat-pick path doesn't
honor adaptability. One-line fix in `create_character` to add a
free Skill Focus when race is half-elf.

**Source:** `coverage.PLAYER_RACE_TRAITS["adaptability"]` =
`NOT_IMPLEMENTED`.
**Size:** S.

### Undead immunity to bleed

Undead are immune to bleed in PF1. Currently no general bleed
system, but ferocity-bleed exists. If we ever apply ferocity-style
bleed to anything that an undead could be (we don't today), we'd
double-bug it. Add a guard in `_apply_post_damage_state` and/or
`tick_round`: undead don't get ferocity-active state.

**Source:** `coverage.MONSTER_RACIAL_TRAITS["undead_traits"]` =
`PARTIAL`.
**Size:** S.

---

## P1 — coherent batches

### Iterative-attack feats (combat_reflexes, two_weapon_fighting, rapid_shot, precise_shot)

Currently the only way to get extra attacks per round is via BAB
iteratives. Combat Reflexes is the worst gap (only 1 AoO/round
modeled). TWF and Rapid Shot need off-hand / extra-ranged-shot
plumbing in `_do_attack` and `_do_full_attack`. Precise Shot
removes the -4 penalty for firing into melee — needs the penalty
to exist first.

**Source:** `coverage.FEATS["combat_reflexes" / "two_weapon_fighting"
/ "rapid_shot" / "precise_shot"]` = all `NOT_IMPLEMENTED`.
**Size:** M.

### Undead trait cluster

Wire the meaningful immunities for undead: immune to mind-affecting
(charm, hold, sleep, fear), immune to paralysis/sleep/stun, immune
to bleed, no nonlethal damage. Most are condition-immunity flags;
the gnarly one is "no Con score" semantics for HP / Fort saves
(currently masked by precomputed monster stats).

**Source:** `coverage.MONSTER_RACIAL_TRAITS["undead_traits" /
"undead_traits_zombie"]`.
**Size:** M.

### Situational racial-trait cluster

Implements the "vs creature type X" / "vs effect Y" qualifier
system: dwarven hatred (+1 attack vs orcs/goblinoids), hardy
(+2 vs poison/spells/SLAs), stability (+4 CMD vs trip/bullrush),
defensive_training (+4 dodge AC vs giants). Plus gnome equivalents.
The hard part is the contextual qualifier framework, not any one
trait — once it exists, all of them are 1 line each.

**Source:** `coverage.PLAYER_RACE_TRAITS` — about 8 traits in this
cluster.
**Size:** M.

### Combat maneuvers (trip, disarm, sunder, bull-rush, grapple)

Currently completely absent. Wolf trip-on-bite is a `NOT_IMPLEMENTED`
that wants this. Needs CMB/CMD checks (the core math is in the
engine), a dispatcher in `turn_executor`, and condition application
on success (prone for trip, disarmed for disarm, grappled for
grapple).

**Source:** `coverage.MONSTER_RACIAL_TRAITS["trip_attack"]`,
multiple class features, generic combat option.
**Size:** L.

---

## Engine-level "future" items (when their consumers land)

These are real engine gaps but aren't useful to land before something
exercises them. Leave them parked here so we remember to build the
infra alongside the first consumer.

- **Energy resistance / immunity infrastructure.** Generic mechanism
  for cold/fire/electricity/acid/sonic. Latent until cold/fire/etc.
  damage spells exist (currently they don't). Build alongside the
  first cold-damage spell. Driver: `cold_immunity` (skeleton).
- **Daylight context (for light sensitivity).** Encounters have no
  notion of indoor / outdoor / time-of-day. Add either a per-encounter
  `bright_light: bool` flag or per-location metadata, and apply
  `dazzled` automatically. Low gameplay impact today. Driver:
  `light_sensitivity` (kobold, orc).

## Phase 4+ work

Sandbox-layer initiatives (multi-hero parties, crafting, monster dens,
direct PvP, etc.) live in `SANDBOX_DESIGN.md`'s "Deferred Scope
Tracker" — that's the source of truth for them. **Don't duplicate
those entries here.** This file stays scoped to engine fidelity +
in-flight bug-fix work.

---

## Recently shipped

(Move items here when they land. Keep ~10 most recent; trim older
entries as they age out.)

- 2026-05-01 — Skeleton/zombie DR by type. (`coverage.py`)
- 2026-05-01 — Orc ferocity (PF1 RAW: stay conscious + 1 HP/round
  bleed). Centralized via `_apply_post_damage_state`; fixed latent
  bug where `_do_aoo` never set `dying`. (`coverage.py`)
- 2026-05-01 — PF1 coverage tracker: `coverage.py`, `PF1_COVERAGE.md`,
  `tests/test_coverage.py`. Six categories, 153 entries pre-classified
  by sweeping current content.
- 2026-04-30 — Charge: PF1 straight-line + path-clear + min-distance
  enforcement (deviation, not regression — old code was too lenient).
  AI fallback in `default_monster_intent` so off-axis charges become
  move_toward instead of wasted skips.
- 2026-04-30 — Phase 3 sandbox layer: castles, world, deployments,
  tick worker as sole writer, queue-based decoupling, HTTP API.
- 2026-04-30 — Active class abilities: Power Attack, Combat Expertise,
  Cleave, Rage, Smite Evil, Channel Energy, Inspire Courage.
