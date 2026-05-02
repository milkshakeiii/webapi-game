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
