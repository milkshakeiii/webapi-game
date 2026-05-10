# Claude Notes — dnd sandbox

A pointer file for Claude Code sessions working in `dnd/`. Indexes the
reference dumps, design docs, engine layout, and discipline rules
that aren't obvious from the directory tree.

## Reference RAW (read before implementing)

When implementing or editing PF1 mechanics, the canonical text is in
`checklist/`, not your training data. Two scrapes:

- **Spells** — `checklist/spells/<school>.md` (3037 entries, Foundry
  PF1e snapshot). Match `### <Name>` to find the entry. Implement
  literally to the prose; don't invent durations, save types, or
  exclusions. Common pitfalls already hit: temp-HP vs `hp_max`,
  discharge-on-use vs duration, off-by-one HP thresholds.
- **Core mechanics** — `checklist/rules/<topic>.md` (d20pfsrd CRB
  scrape). Six topics: `combat`, `magic`, `conditions`,
  `special-abilities`, `skills`, `exploration-movement`. Use this
  before working on action economy, combat maneuvers, condition
  prose, save mechanics, components/SR/concentration, fast healing /
  DR / ER, etc.
- **Other content** — `checklist/{feats,races,class-abilities,
  monster-abilities,weapons-and-ammo,armors-and-shields,items,
  buffs,...}.md`. Same shape: full Foundry RAW + a `Manual verdict:`
  field per item.

`checklist/00_index.md` is the table of contents.

## Coverage tracker

`coverage.py` is the source of truth for what's implemented vs.
deferred. `tests/test_coverage.py` enforces:

1. Every content ID has an entry (no orphan content).
2. Every entry maps to live content (no stale entries).
3. Every entry has a known status + non-empty note.

Statuses: `IMPLEMENTED` / `PARTIAL` / `NOT_IMPLEMENTED` /
`OUT_OF_SCOPE`. `PF1_COVERAGE.md` is the narrative view of the same
data.

## Design docs

- `DESIGN_PROPOSAL.md` — overall sandbox design (1100 lines).
- `SANDBOX_DESIGN.md` — the live world / continuous-tick architecture.
- `CHARACTER_OPTIONS.md` — what character builds the engine supports.
- `BEHAVIOR_VOCABULARY.md` — the DSL patrons write hero scripts in. Active-turn rules (existing v1 surface) plus reactive/sub-action rules (v2 additions: `react: aoo` / `brace` / `cleave`, `sub: full_attack`).
- `DECISION_POINT_DSL.md` — design + migration tracker for the DSL/execution-model rework. All five phases closed; the substrate is the only execution path. Action-economy validation for the v1 sugar path lives in `actions._validate_intent`.
- `WORK_QUEUE.md` — pending phases and follow-ups.
- `PF1_COVERAGE.md` — narrative of `coverage.py`.
- `README.md` — public-facing overview + run/test instructions.

## Engine layout

```
engine/
  characters.py     L1 character creation (race + class + ability scores)
  combat.py         attack-roll resolution, damage, crit confirmation
  combatant.py      Combatant dataclass — HP, conditions, modifiers, resources
  content.py        JSON content loader (the registry)
  dice.py           seeded dice + expression parser
  dsl.py            BehaviorScript / Rule / Interpreter
  encounter.py      initiative, round/turn cycle
  encumbrance.py    carry capacity + speed penalties
  feat_effects.py   per-feat combat hooks
  grid.py           2D position + LoS + cover
  inventory.py      equipment slots, donning/doffing
  level_plan.py     class progression plans
  leveling.py       apply level-up
  modifiers.py      typed-bonus stacking
  progression.py    BAB / saves / class-skill tables
  racial_effects.py per-race combat hooks
  scenario.py       tournament harness
  sizes.py          size category math
  skills.py         skill_check + per-skill DC tables
  spells.py         spell handlers (effect-kind dispatch) + roll_save
  turn_executor.py  composite actions, end-of-turn dispatcher
```

Content is JSON under `content/`: `monsters/`, `races/`, `classes/`,
`feats/`, `conditions/`, `spells/`, `domains/`, `weapons/`, `armor/`,
`shields/`, `locations/`, `skills/`.

## Tools

- `tools/generate_checklist.py` — re-scrape the Foundry PF1e pack into
  `checklist/*.md`. Needs PyYAML + a local Foundry checkout.
- `tools/dump_rules.py` — re-scrape d20pfsrd into `checklist/rules/`.
  Needs a venv with `markdownify` + `beautifulsoup4`.

`tools/README.md` has run instructions for both.

## Tests

```bash
python3 -m unittest discover dnd/tests   # full suite (~1100 tests)
python3 -m unittest dnd.tests.test_coverage -v   # coverage roll-up
```

The coverage roll-up prints a per-category IMPL/PARTIAL/NOT_IMPL/OOS
table after the suite runs.

## Discipline (worked-out lessons)

- **PF1-native, not parallel mechanics.** A round is a tick, PF1 speed
  is movement, etc. Don't invent abstractions that re-implement what
  PF1 already specifies.
- **PARTIAL means real RAW gap.** Don't mark something IMPLEMENTED
  with a "but X isn't enforced" caveat — that's PARTIAL, so we know
  to revisit. IMPLEMENTED means it matches RAW.
- **Monsters: fully implemented or don't ship.** Every shipped monster
  must have all non-verticality traits wired (no "declared but
  unhandled" abilities).
- **Continuous tick world, not pre-simulated.** The world runs as a
  tick worker; deployments don't pre-resolve in isolation. Cross-
  patron interaction depends on this.
- **Track deferred scope explicitly.** When cutting v1, every
  deferred feature gets a note in `coverage.py` or `WORK_QUEUE.md` —
  nothing silently disappears.

## Things to avoid recreating

- A content scanner for `coverage.core_mechanics` — that category is
  rulebook-prose, not JSON-derived. Adding entries is manual.
- Per-skill DC tables — the per-skill prose lives in d20pfsrd's
  individual skill pages, not the dumped overview. Add slugs to
  `dump_rules.py`'s `PAGES` list if you need a specific one.
