# dnd/tools

One-off scripts for working with the project. Not part of the runtime.

## generate_checklist.py

Walks a local checkout of [Foundry PF1e]
(https://gitlab.com/foundryvtt_pathfinder1e/foundryvtt-pathfinder1)
and emits `dnd/checklist/*.md` — a per-category coverage checklist.

For each PF1 item (feat, spell, monster ability, class feature, …)
the script extracts:

- name, type, sub-type, tags
- structured prerequisites (when present) or a regex pull from the
  prose `Prerequisites:` line
- source rulebook + page numbers (Paizo product code → readable name
  via a small lookup table inside the script)
- the rules-text prose, HTML-stripped to markdown
- a one-line summary of their mechanical encoding (`changes` count,
  presence of `actions` / `scriptCalls`, or `prose only`)
- our coverage-tracker status if `dnd/coverage.py` has a matching
  entry
- a blank `[ ]` for the manual fidelity verdict + a `Notes:` line

The output is a manual checklist. The script never claims an item is
implemented faithfully — it just compiles the list a human can walk.

### Running

Their data isn't vendored; clone it fresh whenever you want an updated
snapshot:

```bash
git clone --depth 1 \
    https://gitlab.com/foundryvtt_pathfinder1e/foundryvtt-pathfinder1.git \
    /tmp/foundry-pf1

python3 -m dnd.tools.generate_checklist \
    --foundry /tmp/foundry-pf1 \
    --out dnd/checklist
```

Requires PyYAML (`pip3 install --user --break-system-packages pyyaml`
on Homebrew Python).

### Updating coverage.py from the checklist

When you tick a row, copy the verdict over to `dnd/coverage.py` so
`tests/test_coverage.py` reflects the engine's actual coverage. The
checklist file is the *to-read* surface; `coverage.py` is the
*verdict log*.

### Categories included

| Pack | What's in it |
|---|---|
| feats | Every feat (Combat, Metamagic, Skill, Item Creation, etc.) |
| classes | All player classes (49 — core + APG + ACG + Occult + Unchained + NPC) |
| class-abilities | Sub-options on every class (bloodlines, domains, talents, hexes, deeds, …) |
| races | Player races (105 between core + others) |
| racial-hd | Racial Hit Dice for monstrous PCs |
| companion-features | Animal companion / familiar abilities |
| monster-abilities | Universal monster abilities (e.g., gaze attacks, regeneration) |
| monster-templates | Templates that modify a base creature |
| template-abilities | Abilities granted by templates |
| mythic-paths | Mythic tier features |
| buffs | Toggleable buff items (rage, bless, haste, …) |
| rules | Conditions and other rules-appendix entries |
| basic-monsters | Bestiary stat blocks (small set in this pack) |
| weapons-and-ammo | Weapon stats |
| armors-and-shields | Armor / shield stats |
| ultimate-equipment | Ultimate Equipment book |
| items | Magic items (rings, wondrous items, etc.) |
| spells | All spells, sharded by school (`spells/abj.md`, `spells/con.md`, …) |

Skipped: `technology` (sci-fi gear), `macros` (JS scripts), `roll-tables`
(random tables — not rules content).

### Re-running

The script is idempotent. Re-running overwrites every shard. You can
`git diff` to see what changed in their dataset between snapshots.

## dump_rules.py

Scrapes core-mechanic rules pages from d20pfsrd.com into
`dnd/checklist/rules/<slug>.md`. Companion to `generate_checklist.py`:
the Foundry pack covers content but its `rules` shard is empty, so
this fills the gap with full RAW prose for combat, magic, conditions,
skills, special abilities, and movement.

### Running

`markdownify` and `beautifulsoup4` aren't in stdlib. Use a venv:

```bash
python3 -m venv /tmp/rulesenv
/tmp/rulesenv/bin/pip install markdownify beautifulsoup4
/tmp/rulesenv/bin/python -m dnd.tools.dump_rules \
    --out dnd/checklist/rules
```

The pages don't change often, so the dumps are committed and the
script is mainly there to refresh if a page moves or you want to add
more chapters. Edit the `PAGES` list at the top to add slugs.
