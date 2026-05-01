# PF1 Mechanic Coverage

A categorized inventory of every PF1 mechanic the engine is meant to
support, with per-item status (`IMPLEMENTED`, `PARTIAL`,
`NOT_IMPLEMENTED`, `OUT_OF_SCOPE`).

**Source of truth: `dnd/coverage.py`.** This document is a narrative
view; the Python module is what `tests/test_coverage.py` checks
against. When you add or change a coverage entry, update both — they
should agree.

## How this is enforced

`tests/test_coverage.py` does three things:

1. **Completeness** — scans every content JSON (`monsters/*.json`,
   `races/*.json`, `classes/*.json`, `feats/*.json`,
   `conditions/*.json`, `spells/*.json`) and asserts that every
   declared mechanic ID has a coverage entry. New content fails the
   test until classified.
2. **No stale entries** — every coverage entry must correspond to
   live content. Removing a content ID without removing its coverage
   entry fails.
3. **Status sanity** — every entry has a recognized status and a
   non-empty note.

The test does *not* enforce that an `IMPLEMENTED` claim is actually
wired in code. That's what the rest of the suite is for. This test
just keeps the inventory honest.

## Status legend

| Status | Meaning |
|---|---|
| `IMPLEMENTED` | Wired in code, tested. |
| `PARTIAL` | Partially wired. The note describes the gap. |
| `NOT_IMPLEMENTED` | Recognized; engine ignores it for now. Land it when it bites. |
| `OUT_OF_SCOPE` | Won't implement. Reason in the note (usually: tag-only flavor trait, or mechanic too contextual to be worth modeling). |

## Roll-up

Run the suite verbosely (`python3 -m unittest dnd.tests.test_coverage
-v`) to see the current numbers. As of the latest sweep:

| Category | Total | IMPL | PARTIAL | NOT_IMPL | OOS |
|---|---:|---:|---:|---:|---:|
| Player race traits | 33 | 10 | 0 | 21 | 2 |
| Monster racial traits | 11 | 1 | 2 | 8 | 0 |
| Class features (L1) | 35 | 7 | 2 | 24 | 2 |
| Conditions | 35 | 3 | 13 | 18 | 1 |
| Feats | 30 | 19 | 0 | 11 | 0 |
| Spell effect kinds | 9 | 9 | 0 | 0 | 0 |

## What's tracked

### Player race traits

The traits PCs get from their race (declared in `races/*.json`).
Mostly small passive bonuses; some are situational (dwarven hatred,
hardy, stability) which is why they show as `NOT_IMPLEMENTED` —
implementing them requires contextual qualifiers (vs. orcs, vs.
poison, etc.) the engine doesn't yet support.

### Monster racial traits

Per-monster special qualities and attacks (DR, immunities, ferocity,
trip-on-hit, light sensitivity, etc.). Currently this is the most
underwired category for gameplay impact — DR for skeletons / zombies
and the undead immunities are the obvious next picks.

### Class features (L1)

Features each class gains at level 1. Active features (rage, smite
evil, channel energy, sneak attack, etc.) tend to be implemented;
structural features (domain selection, bloodline picks, animal
companion, school specialization) tend not to be.

### Conditions

PF1 has ~40 conditions. Many are flag-only and the engine just needs
to *honor* them when they're set (e.g., turn validation refuses
actions for unconscious / paralyzed). The richer conditions
(confused, exhausted, frightened) need rules logic the engine doesn't
have yet.

### Feats

Feats from the core rulebook. Most passive ones (Iron Will, Toughness,
Skill Focus) and the major active ones (Power Attack, Combat
Expertise, Cleave) are wired. Iterative-attack feats (Two-Weapon
Fighting, Rapid Shot) are the biggest remaining gap.

### Spell effect kinds

Internal taxonomy used in `spells.py`. A spell with effect kind
`scaling_damage` (fireball, lightning bolt) gets handled by
`_handle_scaling_damage`; a spell with `apply_condition_save`
(color spray, hold person) by `_handle_apply_condition_save`; etc.
All declared kinds currently have handlers.

## How to use this doc when fixing a bug

1. The patron reports something doesn't work — say, "skeletons take
   full damage from my fighter's longsword."
2. Look up the mechanic in `coverage.py`:
   - Skeleton has `dr_5_bludgeoning`, status `NOT_IMPLEMENTED`.
3. That's the gap. Either implement it now and flip the status to
   `IMPLEMENTED`, or note that we deliberately deferred it.

Equally, when planning a session: scan `coverage.py` for the largest
clusters of `NOT_IMPLEMENTED` items, group by what they unlock (e.g.,
"all undead defenses" — DR-by-type, energy resistance, paralysis
immunity), and land them as a coherent batch.

## When to add a new category

If you find yourself wanting to track something that doesn't fit any
existing category (e.g., per-monster *special attacks* like a ghoul's
paralysis touch, or *energy types* like cold/fire/electricity), add a
new dict to `coverage.py` and a new scanner + test in
`test_coverage.py`. The categories are intentionally additive.
