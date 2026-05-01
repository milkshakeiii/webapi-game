# D&D Sandbox Design Proposal

## Summary

A persistent web-API sandbox where each player runs a **castle**. Castles
spend **renown** to attract **heroes** — adventurers in the player's employ,
each defined by a player-authored **behavior script** and a player-authored
**level-up plan**. Heroes deploy from the castle into a shared world, where
they gather resources, craft items, fight monsters, build monster dens,
recruit monsters into their service, and (if they survive) return home
laden with loot, intel, and renown.

The full PF1 SRD ruleset runs underneath. Combat plays out tactically square
by square — initiative, iterative attacks, attacks of opportunity, full
spell lists, the works — but no human is at the controls. The hero acts on
its standing orders. Players win or lose on the quality of those orders, on
the level-up plan they committed to, and on the strategic decisions they
make at the castle level: which heroes to invest in, which dens to build,
where to send people, what to craft, what to sell.

The activity is programming. The theme is patronage. They are the same
thing: a behavior script *is* a standing order, a level-up plan *is* a
training regimen, the API *is* the channel through which a patron
communicates with their distant servants.

## The Loop

```
                ┌─────────────────────────────────────┐
                │                                     │
                ▼                                     │
       spend renown to spawn hero                     │
                │                                     │
                ▼                                     │
       attach behavior script                         │
       attach level-up plan                           │
       equip from castle stockpile                    │
                │                                     │
                ▼                                     │
       deploy → travel → adventure                    │
       (engine simulates against PF1 rules,           │
        hero acts via its script,                     │
        levels up via its plan)                       │
                │                                     │
       ┌────────┴────────┐                            │
       ▼                 ▼                            │
   hero returns      hero dies                        │
       │                 │                            │
       │                 └────► investment lost       │
       ▼                                              │
   bank: renown earned                                │
         loot deposited                               │
         intel updated                                │
         hero rests at castle                         │
                │                                     │
                └─────────────────────────────────────┘
```

The strategic question is not "what does my fighter do this turn"; the
fighter's script answers that. The strategic question is "which heroes
am I building, and to what end?"

## Theme & Framing

The player is a **patron** — a lord, a magus, an abbot, a guildmaster, a
necromancer-prince. The castle is their seat of power, persistent across
sessions and known to the world. Heroes are adventurers in their employ:
some seek the patron out drawn by reputation (renown), some are hand-raised
from squires, some are bound by debt or geas.

A behavior script is **the patron's standing orders**. A patron does not
march beside their heroes; they cannot direct them turn by turn. They write
careful instructions before deployment. A clever patron who anticipates
contingencies has heroes that survive surprises. A lazy patron writes
"attack the closest enemy" and watches their wizard get cleaved in half.

A level-up plan is **the patron's vision for the hero**. When a squire
returns and is promoted, the patron decides which feats they trained for,
which spells they studied, which path they walked.

This framing matters because it keeps the activity (programming) and the
fiction (patronage) coherent. It also opens hooks for flavor: legendary
patrons attract legendary heroes; evil patrons get necromancers and beast-
tamers; lawful patrons get paladins and inquisitors; archmage patrons can
craft geas-bound heroes who cannot disobey.

## Goals

- **Real PF1 depth.** Combat, character building, and crafting all run on
  the actual rules. Knowing PF1 should give a real edge — feat synergies,
  multiclass dips, save-or-suck spells, dispels, action economy. None of
  this is hand-waved.
- **The activity *is* the theme.** No tacked-on fiction. Writing a hero's
  behavior script is *being* the patron writing standing orders. Writing a
  level-up plan is *being* the patron training their lieutenants.
- **Deterministic, replayable simulations.** A deployment is a function of
  (world state, hero state, behavior script, level-up plan, RNG seed).
  Replays are inspectable end-to-end. Debugging a hero's death is a
  literal trace through the combat log.
- **Async-friendly.** A deployment runs as a single simulation, not a
  real-time session. Players submit their plan and check back. This suits
  a programmer audience and makes the world tolerate deep simulations
  without keeping anyone's browser open.
- **Strategic depth at the castle level.** The meta-game — which heroes
  to spawn, which dens to build, which adventures to chase — is a real
  4X-ish layer on top, not a wrapper.
- **Shared persistent world.** Other patrons' heroes and dens are part of
  the world. Indirect competition by default; direct PvP later, opt-in.

## Non-goals (for v1)

- Real-time combat. Combat resolves as part of an offline simulation.
- A graphical client. API only. Battle visualization is a returned trace.
- Direct hero piloting. Players never make a turn-by-turn decision; that's
  what the script is for.
- Player-vs-player castle warfare. v1 has *indirect* PvP (your hero might
  fight another patron's hero in a contested location, or attack their
  monster den). Direct attacks on castles are out of scope.
- 5e or 4e mechanics. PF1 SRD only.
- Adventure module-style designed dungeons. Encounters are generated from
  world state, not authored.

---

# Core Concepts

## Castles

A **castle** is the persistent identity of a player. One castle per account.
A castle has:

- **Renown** (current balance + lifetime total).
- **Treasury**: gold pieces and a stockpile of items (weapons, armor,
  potions, scrolls, raw materials, magical components).
- **Roster**: heroes currently in residence, currently deployed, and a
  graveyard of those who didn't make it back.
- **Library**: behavior scripts and level-up plans authored by the patron.
  Reusable across heroes; one script can be assigned to many heroes.
- **Crafting capacity**: artisans, workshops, magical apparatus. Determines
  what items the castle can produce given materials.
- **Reputation tags**: alignment lean, schools of magic favored, monsters
  favored or feared. Affects which heroes are willing to enlist.
- **Renown unlocks**: thresholds that gate access to higher-tier heroes,
  larger deployments, more hero slots, monster types you can attempt to
  command, etc.

A castle's shape changes slowly. Renown cycles fast.

## Renown

The meta-currency. **Earned** when heroes return having accomplished things:

- Defeating monsters (renown ~ CR overcome).
- Banking loot in the castle treasury.
- Clearing or fortifying named locations.
- Rescuing or extracting NPCs (intel networks).
- Reporting world-state intel (cartography, monster movements).
- Defeating other patrons' dens.
- A hero surviving a high-CR encounter at all (legend grows).

**Spent** at the castle to:

- Spawn new heroes (cost scales with desired starting level).
- Unlock content tiers (paladin available, druid available, dragon-tier
  monsters commandable, ...).
- Expand crafting capacity.
- Recruit named NPCs (artisans, sages, scouts) to the castle.
- Fund expeditions / contracted deployments / mercenary work.

The meta-loop is just renown in, renown out. The texture is what you spend
it *on* and how that compounds.

**Inflation/sink:** because dead heroes don't return any renown, the loop
self-regulates. A reckless patron loses heroes and stalls. A cautious one
banks small amounts but progresses slowly. A skilled one writes scripts
that survive surprises and compounds fast.

## Heroes

A hero is a PF1 character — full sheet — plus:

- **Behavior script** (a `.beh` file or equivalent — see below).
- **Level-up plan** (a `.plan` file or equivalent).
- **Status:** `at_castle` | `deployed` | `dead` | `missing`.
- **Career stats:** deployments survived, total XP earned, monsters defeated,
  signature kills, items crafted.
- **Ledger:** the trace of every deployment they've been on.

When a player wants a new hero, they:

1. Pay renown (cost ~ starting level chosen).
2. Choose a class (subject to castle unlocks).
3. Assign or write a behavior script.
4. Assign or write a level-up plan.
5. Equip from castle stockpile.
6. The engine generates the level-1 stats (ability scores rolled or pointbuy
   per castle policy), validates the level-up plan against the rules,
   accepts the hero into the roster.

Heroes start at level 1 by default. **Spawning higher-level heroes** is a
meta-progression unlock: at certain renown thresholds, the castle attracts
already-experienced adventurers (level 3, level 5, ...). Cost scales
non-linearly — a level 5 hero costs much more than five level-1s, because
the rule of D&D is that high level matters more than headcount.

### Hero death is permanent

If a hero dies on deployment, they are gone. The investment is lost. There
is no Raise Dead by default — *it exists in the rules*, and a hero with
the right spells/scrolls/spell-slots and a body to return to could be
raised by a *deployed* hero, but the castle itself doesn't have a magic
"undeath" button. This is what makes scripts matter.

(Open question: should a high-renown unlock allow castle-level Raise Dead
at exorbitant cost? See open questions.)

### Heroes can party up

A deployment can include a single hero or a party of multiple heroes from
the same castle. Their scripts must coordinate. This is where social
behaviors emerge: tank scripts that taunt, healer scripts that watch ally
HP, scout scripts that retreat to summon allies. PF1 was designed for the
4-hero party. Building a deployable party is a deep optimization problem
in itself.

(v1 may ship single-hero only and add parties in v2 — see phased plan.)

## The World

The world is a **flat 2D map** populated with static features —
inspired by *Majesty: The Fantasy Kingdom Sim*. There are no nested
dungeons in v1; "adventure sites" are points on the surface that heroes
walk to, engage, and leave. Vertical depth (multi-floor dungeons,
underdark layers) is a v2+ addition once the flat layer is fun.

### Map features

- **Castles.** Patron homes. Persistent. Each patron has one.
- **Spawn points (lairs, ruins, camps).** Sites that periodically
  generate hostile creatures or treasure. Goblin camps respawn goblins
  every few in-game hours; ancient ruins drop one-time loot when first
  cleared and then fall silent. Some are world-native; others are
  player-built (see *Monster Dens*).
- **Resource nodes.** Lumber camps, mines, herb gardens, magical
  springs. Heroes gather here. Nodes deplete over use and regenerate
  over in-game time. Limited yield-per-hour creates contention.
- **Neutral buildings.** Marketplaces (buy/sell), temples (healing,
  remove disease/curse, eventually raise dead), shrines (situational
  buffs), libraries (research, scrolls).
- **Wilderness terrain.** The space between features. Has biomes
  (forest, desert, swamp, mountain, plains). Affects movement speed
  and may trigger random encounters during travel.

A hero's "deployment" is therefore: leave castle → walk overland (with
possible random encounters along the way) → arrive at a feature →
interact (fight, gather, craft, parley, build) → walk home → bank.
Travel distance and biome difficulty are real strategic variables.

### Persistent state

The world is **shared across all patrons** and persists over time.
When patron A clears a lair, the lair stays cleared until it
regenerates. When patron A builds a goblin den, it persists until
someone clears it. When a resource node is exhausted, it stays
depleted until enough in-game time passes for it to recover.

### Discovery

Each castle starts with a small **known area** around it. Heroes
returning from deployments report what they saw, expanding the patron's
known map. Other patrons have different maps. The world *exists* in full
on the server; what each patron *knows* is a subset, evolving over time
through their heroes' eyes.

### Layout (still partly open)

For v1 I'm proposing a **hybrid generation approach**:

- A few **hand-authored anchor regions** at world-init: named
  geographies with character (the Whispering Wood, Ironpeak Mountains,
  the Sunken Quarry), each pre-populated with a curated selection of
  features. Makes the world feel designed rather than algorithmic.
- **Procedural fringes** filling the space between anchors with
  generated features tuned to the surrounding biome.
- **Patron-built additions** (dens, outposts) layered on top
  dynamically as the game runs.

Could simplify to fully-procedural for early-version effort. See open
questions.

## Resources & Crafting

Heroes can gather resources at locations:

- **Mundane:** wood, stone, iron, leather, herbs.
- **Magical components:** elemental essence, residuum, blood of dire wolf,
  pinch of dust from a chronomantic ruin.
- **Currency:** raw gold from monster hoards or shipwreck wrecks.
- **Reagents:** specific monster parts (dragon scale, troll regenerative
  tissue), used in feat-prereq'd crafting.

Castles craft using PF1's actual rules:

- **Craft (Wondrous Item)** with the right caster level, gold cost, time.
- **Craft Magic Arms and Armor**, **Brew Potion**, **Scribe Scroll**, etc.
- The artisan must be available at the castle (a hero with the feat, an
  NPC artisan recruited via renown, or the patron themselves if they're
  modeled as a high-level NPC).
- Magical crafting needs gold, time, **and** specific reagents the hero
  brought back — making the gather→craft loop tangible.

Crafting outputs land in the stockpile; equipped to next deployment.

This is gameable: a patron specializing in Craft Wondrous Item builds a
hero pipeline that gathers reagents, brings them home, crafts items, then
deploys those items to subsequent heroes. The crafting castle's heroes are
better-equipped than the meathead castle's, even at the same renown level.
Specialization matters.

## Monster Dens

A hero with appropriate skills (Diplomacy, Intimidate, certain spells, or
domination/charm effects) can **recruit** monsters they encounter — or
the patron can spawn a den from the castle, sending raw materials and an
escorted construction party.

A **den** is a persistent location-bound encounter:

- Inhabited by a number of NPC monsters (drawn from PF1 MM).
- The den's population grows / patrols / forages over time.
- Dens have a CR rating (combined challenge of inhabitants).
- Other patrons' heroes who visit the location encounter the den.
- A castle earns passive renown income while its dens persist (proportional
  to den CR and how contested the location is).
- A castle can recall a den (escort the monsters home — risky operation).

Dens turn the world into a player-built threat ecology. A region can be
densified with goblin tribes, troll bridges, ogre raiding parties, and a
red-dragon lair, all by patron action. Ambitious patrons turn into the
"big bad" of a region.

The cap on den building is **commanding capacity**: you can only build a
den if your castle has the renown unlock for that monster tier *and* the
escorted heroes succeeded their domination/diplomacy checks. Trying to
command a CR 12 monster with a level 4 hero is suicide.

## Monster Commanding

PF1 has explicit rules for charm, dominate, intimidate-into-surrender, and
several other forms of NPC control. We use them:

- **Diplomacy** to shift attitude and negotiate.
- **Intimidate** to force compliance under threat.
- **Handle Animal** for animals.
- **Charm Person / Charm Monster** spells for explicit magical compulsion.
- **Dominate Person / Monster** for harsher control.
- **Speak with Animals / Speak with Dead / Tongues** as communication
  prerequisites for harder targets.
- Specific class features (paladin's celestial mount, druid's animal
  companion, summoner's eidolon, witch's familiar) as built-in pets.

A "tamer" hero build is a real archetype: high-Charisma sorcerer with a
spellbook full of compulsions, plus Diplomacy and Intimidate. Such a hero
is bad at frontline combat but excellent at growing den infrastructure.

## Time & Deployments

The world runs in **real time**. One clock, advancing continuously.

- **Tick = PF1 round = 6 seconds.** Real-time : game-time ratio is 1:1
  by default, so a round takes 6 real-seconds, an hour is an hour, a
  day is a day. (Server-tunable, but no need to compress.)
- **No overland rules.** Heroes move at PF1 base speed across the flat
  2D map (a speed-30 character covers 5 ft per real-second). Continuous
  movement, like Majesty units; no quantized "travel ticks" on top.
- **Combat is real PF1 combat in real time.** When hostile units come
  into contact, they enter combat mode, initiative is rolled, and
  rounds resolve at one round per 6 real-seconds. Each character's
  turn within a round runs through their behavior script. The patron
  doesn't watch combat live (no UI for that) — the trace is appended
  to the deployment's log as it happens, readable on demand. The
  world keeps running around the combat: other units continue their
  movement and actions while the engagement plays out.

A **deployment** is just an order: "hero X (or party {X, Y, Z}), go to
location L and pursue objective O." Patron submits → unit immediately
begins moving on the map → things happen → unit either returns home,
dies, or goes "missing" (still alive but unreported, e.g., trapped or
charmed).

Typical play cadence is **daily**: patrons set their roster's orders
each day, and heroes might be out for a day or more. Sometimes less if
they get killed; sometimes longer if they're crafting on-site or
exploring far afield.

### Anti-spam

The natural pacing of a real-time world handles most spam concerns: a
hero is genuinely tied up for the duration of their deployment, so even
a heavily-staffed castle only has a handful of heroes out at once. We
layer **renown dispatch costs** on top — scaling roughly as
`level² × distance_factor × party_size` — so that low-risk grinds aren't
free. Combined with **diminishing returns** at locations (a third
clearing of the same patrol pays sharply less) and **world-state
persistence** (cleared lairs stay cleared until something repopulates
them), the result is multiple soft ceilings rather than one harsh tax.

## Test Dungeons

The live world is meaningful but slow for iteration. Debugging a behavior
script via "deploy, wait a day, see if my fix worked" is unworkable.

So **test dungeons** exist as a separate, fast channel — a simulator
loop running outside the persistent world. A test dungeon is:

- An isolated synthetic encounter: terrain, monsters, starting
  positions, win/loss conditions, all spec'd in a small YAML file.
- Run against a *copy* of one of the patron's heroes (or a synthesized
  template — "a level 5 paladin with this script and stock equipment").
- Simulated as fast as the CPU can churn through it (a typical fight
  resolves in milliseconds), with full PF1 mechanics and a full trace.
- **No effect on the persistent world.** No renown earned or spent,
  no XP, no consumables actually consumed, no death (the hero "wakes
  up safe" if killed in the test).
- Reproducible by seed: iterate on a script, replay the same encounter,
  see exactly which line changed the outcome.
- Batch-runnable: 1000 simulations of the same encounter against a
  script tells you the *distribution* of outcomes, not just one roll.

The repo ships a **standard test library** of named encounters covering
representative challenges:

- `goblin_patrol_cr1` — solo skirmish basics.
- `ogre_solo_cr3` — single high-HP brute, sustained combat.
- `cleric_boss_cr7` — caster opponent, dispel/save logic.
- `mixed_party_cr10` — multi-monster encounter, target prioritization.
- `dragon_lair_cr15` — full party endgame coordination.
- `bandit_camp_pvp_proxy` — opponent uses a stock player-style behavior
  script, simulates inter-patron PvP texture.

Patrons author and share their own test specs. Running a script against
the standard library is a **unit-test suite for hero behavior** — easy
to wire into CI for serious patrons.

Test dungeons also serve a balance/playtest role: when we tune the
rules engine, we can batch thousands of simulations against benchmark
scripts to spot anomalies before they hit the live world.

The persistent world (real-time, shared, real stakes) and the test
bench (fast, isolated, no stakes) are clearly separated. Patrons
iterate in the bench; they commit in the world.

---

# Hero Behavior Scripts

This is the central creative interface. Getting it right matters more than
any other single decision.

## Constraints

- **Sandboxed.** Cannot run arbitrary Python on the server. Must execute
  in a deterministic, resource-bounded interpreter.
- **Expressive enough** to encode interesting tactics. "Full attack the
  closest enemy" is not a strategy; "if I can flank, full attack with
  Power Attack at -2 active; if not, withdraw to threatened-square-free
  position; if low on HP, drink potion of CLW" is a strategy.
- **Composable.** Common doctrines (e.g., "tanking", "ranged kiting",
  "buff-then-engage") should be reusable building blocks.
- **Readable.** A patron who shares a script should be able to communicate
  intent. Scripts shouldn't read like Brainfuck.
- **Inspectable on failure.** When a hero dies, the patron should be able
  to see *which rule fired*, *what state* it saw, and *why* it chose that
  action. No black boxes.

## Recommended approach: a structured behavior DSL

A YAML-style file declaring the party's reactive behavior across modes,
parsed and validated by the engine. **One script controls the whole
party** — solo deployments are just a 1-hero "party". Here's the shape,
illustrated for a classic 4-hero crew:

```yaml
name: "Standard Four v3"
party:
  tank:    { class: fighter, weapon: greatsword }
  healer:  { class: cleric,  domain: healing }
  blaster: { class: wizard,  school: evocation }
  scout:   { class: rogue,   skills: [stealth, perception] }

modes:
  travel:
    on_encounter: switch(combat)
    default: march_to_destination(formation=line, scout=scout.at_front)

  combat:
    # Rules are evaluated each turn against the active hero (the one whose
    # initiative just came up). The first matching rule whose action this
    # hero can legally take fires. Rules can reference any party member
    # by role.
    priorities:
      # ── Crisis: someone's about to die ───────────────────────────────
      - hero: healer
        if: any_member.hp_pct < 0.30 and healer.has_slot(>=2)
        do: cast(cure_serious_wounds, target=ally.lowest_hp_pct)

      - hero: any
        if: self.hp_pct < 0.20 and self.has(potion_of_cure_serious)
        do: drink(potion_of_cure_serious)

      # ── Action economy: blaster wants flanks set up ─────────────────
      - hero: scout
        if: enemy.cluster_of(>=3).exists and not blaster.cast_this_round
        do: stealth_to(enemy.cluster_flank)  # set up sneak attack next round

      - hero: blaster
        if: enemy.cluster_of(>=3).exists and blaster.has_slot(fireball)
        do: cast(fireball, target=enemy.cluster_center, exclude_allies=true)

      # ── Tank duties ─────────────────────────────────────────────────
      - hero: tank
        if: enemy.targeting(healer) or enemy.targeting(blaster)
        do: charge(target=that_enemy)

      - hero: tank
        if: can_full_attack(target=enemy.flanked or enemy.lowest_hp)
        do: full_attack(target=that, options={power_attack: 3})

      # ── Scout opportunism ───────────────────────────────────────────
      - hero: scout
        if: enemy.flat_footed or scout.flanking(enemy)
        do: full_attack(target=that, options={sneak_attack: true})

      # ── Defaults ────────────────────────────────────────────────────
      - hero: any
        default: full_attack(target=enemy.closest)

  victorious:
    do: party_loot + healer.cast_cure_until_full(if_safe)

  retreating:
    trigger: party.alive_count <= 1 or party.total_hp_pct < 0.25
    do: withdraw(towards=castle, formation=tight)
```

**Key elements**:

- **Party roles** are named slots (`tank`, `healer`, ...) that map to
  specific heroes when the party is assembled. Roles are how rules
  refer to each other (`healer.has_slot`, `ally.lowest_hp_pct`).
- **Modes** are explicit states (travel, combat, victorious, retreating,
  scavenging, crafting). The engine knows the current mode from world
  state and the script's transition rules.
- **Priorities** are an ordered list of `hero / if / do` rules. On each
  hero's turn, the engine walks rules top-to-bottom; the first whose
  `hero:` selector matches *and* `if:` evaluates true *and* whose
  action is legal-this-turn fires.
- **Conditions** use a fixed vocabulary that maps directly to PF1
  game state: `hp_pct`, `enemy.X`, `ally.X`, `has(item)`, `can_X`,
  `range_to(X)`, `threatened_squares`, `cast_this_round`, etc.
- **Actions** are PF1 actions: `move`, `charge`, `full_attack`,
  `cast_spell`, `withdraw`, `drink`, `aid_another`, etc. Each action
  takes parameters matching its rule (`charge` needs a target;
  `cast_spell` needs a spell name and target).
- **Targeting expressions** are first-class: `enemy.lowest_hp`,
  `enemy.flanked`, `enemy.weakest_spellcaster`, `ally.cleric_with_slots`,
  `position(behind=tank, away_from=enemy)`. Fixed vocabulary, rich.
- **Cross-hero references** are how coordination happens: rules for one
  hero can read another's state, and an action like `signal(role,
  message)` sets a flag another hero's rules can read on a later turn.

This is essentially a **declarative tactical AI for a 4-hero squad**,
written in a constrained vocabulary. Patrons who deeply understand PF1
write subtle, reactive scripts; novices start with stdlib templates and
modify.

### Solo heroes

The same DSL handles solo deployments — a 1-hero party with a single
role. There's no separate "solo" code path; everything is just the party
engine with N=1.

### Standard library

The engine ships a library of doctrines (`doctrines/tank.beh`,
`doctrines/healer.beh`, `doctrines/blaster.beh`, ...) and complete party
templates (`doctrines/standard_four.beh`, `doctrines/glass_cannon.beh`,
`doctrines/skirmishers.beh`) that patrons fork as starting points.
Sharing scripts becomes part of the meta-game.

## Why not arbitrary Python?

- Server-side sandbox is hard. Resource bounds (CPU, memory) are hard.
  Adversarial patrons could DoS the simulator.
- Determinism is harder: Python scripts with `random` or `time.time()`
  break replays.
- Fixed vocabulary forces patrons to think in terms of the game's actual
  primitives, which improves play.
- DSL files are *short*, parseable, and shareable. Python files diverge.

This is exactly the same reasoning that pushed network-corewar to
`.ncw` over Python.

## Why not pure HTTP polling (player runs their own bot)?

- Couples deployment time to wall clock — heroes can't run faster than
  the player's machine.
- Asymmetric: patrons with always-on servers beat patrons without.
- Replays harder (player's bot might be unavailable at replay time).
- Loses the "submit a plan, simulate fast" benefit.

Could be a v2 escape hatch for advanced patrons. Not v1.

---

# Level-Up Plans

A YAML file that pre-commits a hero's progression from level 2 to a target
level. The engine validates legality (prerequisites, restrictions) at
plan-submit time, not at level-up time, so you know upfront if your build
is impossible.

```yaml
name: "Two-Handed Hurt v2"
target_level: 12

level_2:
  class: fighter
  feat_class_bonus: power_attack
  hp_method: rolled

level_3:
  class: fighter
  feat: cleave  # the per-odd-level feat
  feat_class_bonus: weapon_focus(greatsword)

level_4:
  class: fighter
  ability_bump: str
  feat_class_bonus: weapon_specialization(greatsword)

level_5:
  class: barbarian   # multiclass dip for rage
  feat: null  # no general feat at L5; barbarian gets fast movement etc.

level_6:
  class: fighter
  feat: improved_critical(greatsword)
  feat_class_bonus: greater_weapon_focus(greatsword)

# ... and so on through level 12
```

**Plans support conditional branches** (eventually):

```yaml
level_8:
  if: any_party_member.is(cleric)
  then:
    feat: combat_reflexes
  else:
    feat: extra_rage  # we need self-buff if no cleric
```

**v1: linear plans.** No branches, no in-deployment changes. The plan must
be valid as written.

**v2: conditional branches** at level-up time, evaluated against the
hero's current state and the party composition.

**v3:** plan refinement post-mortem — when a hero dies, the patron edits
the plan and the corrected plan applies to the *next* hero with that role.
(Heroes are mortal but doctrines accumulate.)

---

# The Foundation Layer (Rules Engine)

Everything above sits on top of a faithful PF1 rules engine. The previous
draft of this document focused exclusively on the rules engine; that scope
hasn't changed, just the framing. The rules engine still needs:

- Dice expression parser, seeded RNG.
- Character creation: 7 races, 11 base classes 1–20.
- Combat: initiative, action types, attacks, AoOs, conditions.
- Spells: slots, preparation, casting, save DCs.
- Skills, feats, equipment, magic items.
- Monsters: ~300–500 from MM, used for both encounters and dens.
- Conditions: full ~40 condition catalog with stacking.

Content is sourced from the PF1 SRD via the open Foundry VTT JSON dump
under OGL 1.0a. A one-time transform script normalizes it into our
schema. License obligations (OGL.txt at repo root, Section 15
attribution) are met by hand.

The rules engine is **mode-agnostic**. The sandbox is one client; future
modes (solo dungeons, programmer-vs-programmer arenas) can layer on
without changing the engine.

---

# Architectural Principles

These are load-bearing rules that apply to *every* system in the engine.
Violating them creates compounding pain, so they're captured here once and
then assumed everywhere downstream.

## Stats are computed on demand, not stored as ints

For every derived numeric value — AC, attack bonus, saves, skill totals,
ability scores after buffs, CMB, CMD, HP max-from-Con changes, etc. — the
engine **never stores the final integer**. It stores:

1. A **base** (often a constant: 10 for AC; class-table value for BAB;
   class+ability for saves).
2. A list of **typed modifiers** (each a `(value, type, target, source,
   duration)` tuple).
3. A **compute function** that walks the modifier list and applies stacking
   rules.

This means: applying a buff (`mage_armor`, `bless`, rage) is just adding
modifiers to the collection; expiring a buff is just removing them; querying
a stat is always a fresh computation. There is no "what was the AC before
the spell" bookkeeping.

## Modifier types and stacking

Each modifier carries a `type` — armor, shield, dodge, enhancement,
deflection, size, morale, sacred, profane, insight, luck, alchemical,
competence, resistance, racial, circumstance, untyped, or one of a few
others. The compute function applies stacking rules:

- **Stacking types** (`dodge`, `circumstance`, `untyped`) — every modifier
  contributes; sum them all.
- **Non-stacking types** (everything else) — for each polarity, only the
  most extreme value applies. So multiple +morale bonuses from different
  sources only contribute the highest; multiple -morale penalties only the
  worst; bonus and penalty of the same type net against each other.

In code:

```python
def compute(base: int, mods: list[Modifier]) -> int:
    total = base
    for type_, ms in group_by_type(mods).items():
        if type_ in STACKING_TYPES:
            total += sum(m.value for m in ms)
        else:
            pos = [m.value for m in ms if m.value > 0] or [0]
            neg = [m.value for m in ms if m.value < 0] or [0]
            total += max(pos) + min(neg)
    return total
```

## Inputs vs. derived

Source-of-truth state holds **only inputs** that came from the user, the
content data, or an explicit applied effect. Derived values are computed
through the modifier system on demand.

- `Character` (the static sheet) stores: race, class, level, alignment,
  base ability scores rolled or assigned, chosen feats, chosen skill
  *ranks*, language picks, class choices. It does *not* store: AC, HP max,
  BAB, saves, skill totals, post-racial ability scores, spell slots
  remaining.
- `Combatant` (the runtime, mutable) stores: current HP, active conditions,
  position, expended-resource counters (rage rounds used, smite uses, slot
  expenditures), and a `ModifierCollection` containing every active
  modifier (permanent racial/class ones, equipment-derived, buffs, debuffs,
  conditions, situational).
- A **derived view** (`CharacterSheet` for static sheets,
  `Combatant.snapshot()` for runtime) is what the API serializes. It
  includes both totals and modifier breakdowns:

  ```json
  "saves": {
    "fort": {
      "total": 4,
      "base": 2,
      "modifiers": [
        {"value": 2, "type": "ability", "source": "con_modifier"}
      ]
    }
  }
  ```

## Implications

- Every system that produces effects (spells, feats, equipment, conditions,
  class features, racial traits, sizes) declares them as **modifiers**, not
  as ad-hoc int adjustments.
- Adding a buff: `combatant.add_modifier(...)`. Removing one (or letting it
  expire): drop it from the collection.
- Tests for any stat-producing system assert against the modifier list
  *and* the computed total — both have to be right.

---

# Architecture & File Layout

```
dnd/
  __init__.py
  __main__.py            # python -m dnd → starts server
  server.py              # HTTP routing
  sessions.py            # NOT used the way astronomy uses it; see below

  # Foundation: rules engine (mode-agnostic)
  engine/
    __init__.py
    dice.py              # seeded RNG, expression parser
    characters.py        # ability scores, levels, HP, BAB, saves
    combat.py            # initiative, turns, attacks, conditions
    spells.py            # slots, casting, save DCs, SR
    skills.py            # checks, take 10/take 20
    items.py             # equipment, magic items
    conditions.py        # status effects
    monsters.py          # MM creatures, used in both encounters and dens
    crafting.py          # PF1 craft rules
    trace.py             # structured event log + serializer

  # Sandbox layer: the game on top
  sandbox/
    __init__.py
    castle.py            # castle state, treasury, library, roster
    renown.py            # renown income/spend rules
    hero.py              # hero state machine, lifecycle
    world.py             # region graph, locations, persistent state
    den.py               # monster den lifecycle and encounter generation
    deployment.py        # deploy → simulate → return pipeline
    behavior/
      parser.py          # .beh DSL parser
      validator.py       # static checks on a script
      runtime.py         # interpreter + standard library
      vocab.py           # the condition + action vocabulary
    plan/
      parser.py          # .plan DSL parser
      validator.py       # legality checker (prereqs, restrictions)
      apply.py           # take a hero from L_N to L_N+1 per the plan

  # Persistent stores (sandbox needs durability)
  storage/
    castle_store.py      # castle + library persistence
    world_store.py       # world state persistence
    hero_store.py        # hero records
    deployment_store.py  # deployment results & replays

  # Content: data files sourced from SRD
  content/
    races/*.json
    classes/*.json
    feats/*.json
    skills/*.json
    spells/*.json
    items/*.json
    monsters/*.json
    conditions/*.json
    doctrines/*.beh      # standard library of behavior scripts

  schemas/               # JSON Schemas for content + .beh + .plan
  examples/              # example castles, heroes, scripts, deployments
  tests/
    engine/              # pure rules-engine tests
    sandbox/             # sandbox-layer tests
    integration/         # end-to-end deployment tests

  OGL.txt                # at repo root, actually
  API.md
  MECHANICS.md           # detailed mechanic specs as they stabilize
  DESIGN_PROPOSAL.md     # this file
```

### Why persistent storage now (vs. astronomy's in-memory sessions)

Astronomy and Shattered Archive are session-shaped: the player connects,
plays, disconnects. The state doesn't have to outlive the session.

This is different. A castle exists across days. A deployment runs while
the player is away. The world persists between players' visits. Other
patrons' heroes change the world while you're not looking. We need
persistence — at minimum a JSON-on-disk store, ideally a SQLite db for the
world map. (Scope for v1: JSON-on-disk per castle/world. Migration to
SQLite is straightforward when needed.)

---

# API Sketch

```
# Account & castle
POST   /v1/accounts                                    → create account + castle
GET    /v1/castle                                      → my castle: roster, treasury, library, renown
GET    /v1/castle/world-map                            → my known map
PATCH  /v1/castle/policies                             → set ability-gen policy, etc.

# Library (scripts and plans authored by this patron)
POST   /v1/castle/library/behaviors                    → upload a .beh
GET    /v1/castle/library/behaviors/{name}
POST   /v1/castle/library/plans                        → upload a .plan
GET    /v1/castle/library/plans/{name}

# Heroes
POST   /v1/castle/heroes                               → spawn a new hero
       body: {class, behavior_ref, plan_ref, equipment, name, starting_level?}
GET    /v1/castle/heroes                               → roster
GET    /v1/castle/heroes/{hid}                         → full sheet + history

# Deployments
POST   /v1/castle/deployments                          → deploy hero(es) to a destination
       body: {hero_ids: [...], destination: location_id, objective: {...}}
GET    /v1/castle/deployments                          → all (in-flight + historical)
GET    /v1/castle/deployments/{did}                    → status + final result + full trace
GET    /v1/castle/deployments/{did}/log                → step-by-step combat log

# Crafting
POST   /v1/castle/crafting/orders                      → start a craft job
GET    /v1/castle/crafting/orders                      → in-flight + history

# Den management
POST   /v1/castle/dens                                 → propose to build a den
GET    /v1/castle/dens                                 → owned dens (location + status)

# Content lookups (read-only, public)
GET    /v1/content/races
GET    /v1/content/classes/{class_id}
GET    /v1/content/spells?level=3&class=wizard
GET    /v1/content/monsters?cr=5
GET    /v1/content/feats
GET    /v1/content/conditions
GET    /v1/content/doctrines              # standard library .beh files

# World (sparingly, read-only)
GET    /v1/world/locations/{id}                        → public state of a location
GET    /v1/world/regions/{id}                          → public state of a region

# Direct rules queries (stateless, useful for tooling)
POST   /v1/check                                       → resolve an arbitrary check
POST   /v1/dice                                        → roll an expression

# Validation utilities (so patrons can pre-check before submission)
POST   /v1/validate/behavior                           → static check a .beh
POST   /v1/validate/plan                               → static check a .plan against a class
POST   /v1/dryrun/deployment                           → simulate without committing
```

The deployment-result trace is the most important payload in the system.
It must include enough detail that a patron can reconstruct exactly why
their hero died — every die roll, every script branch, every action
attempt and its outcome.

---

# Decisions Locked

- **Ruleset:** Pathfinder 1e SRD (OGL 1.0a). 3.5/PF1/NWN/KOTOR family.
- **Time:** real-time, continuous, 1:1 game-time = real-time. Tick = PF1 round = 6 seconds.
- **World:** flat 2D map, Majesty-style, single region. No overland rules; PF1 movement speeds in real time. Multi-region only if/when scaling demands it.
- **Behavior scripts:** structured DSL (YAML-style), party-level. Not arbitrary Python.
- **Test dungeons:** offline fast-batch simulator, isolated from the persistent world.
- **Multi-hero parties:** yes, in v1. One script controls a party.
- **Permadeath:** default. Possible Raise-Dead unlock at high renown later.
- **Indirect PvP only in v1:** contested resources, attacking dens. No direct castle-on-castle PvP.

# Open Questions

Ranked roughly by how much they unblock implementation:

1. **World layout strategy.** Procedural-from-seed, fully hand-authored,
   or hybrid (hand-authored anchor regions + procedural fringes). I lean
   hybrid; want to confirm before committing to a generator.

2. **Behavior DSL syntax details.** The structured-tree shape is right
   (above). Specific vocabulary, the cross-hero reference syntax,
   condition language — these will need iteration once we're actually
   parsing files.

3. **Hero ability score generation policy.** Per-castle setting (each
   patron picks 4d6kh3, point-buy 20, point-buy 25, or standard array)?
   Or world-wide locked policy for fairness? I lean per-castle as a
   character-style choice.

4. **Crafting determinism.** PF1 craft rules involve dice and time.
   Keep the dice roll for fidelity, or abstract to "X gold + Y days +
   Z reagents → item" deterministically? I lean deterministic with a
   small failure rate on high-difficulty crafts.

5. **Information visibility between patrons.** Probably: lifetime
   renown, public castle name, alignment lean, owned dens (rough CR
   visible). Not heroes' builds, not the library. Espionage as a hero
   specialization could leak more.

6. **Storage backend.** JSON-on-disk vs. SQLite. JSON is enough for v1;
   switch when read latency or write contention becomes real.

7. **Combat exposure during a fight.** When a hero is in active combat,
   what does the patron see in real time? Options: nothing until the
   fight ends; a poll-able partial trace updated each round; full live
   stream. I lean "poll-able partial trace, updated each round" — not
   live-streamed, but inspectable on demand if the patron is curious.

---

# Phased Plan (revised in service of the sandbox)

### Phase 1 — Foundation skeleton (1–2 weeks)
- Project scaffold, server, dice, OGL.txt.
- A "roll a level-1 fighter" character creation API.
- The 7 core races + 11 base classes (level-1 progression only).
- Pure-engine test harness.
- Deliverable: `POST /v1/content/...` and `POST /v1/castle/heroes` work.
  No world, no deployments, no behaviors. Just rules-engine plumbing.

### Phase 2 — Combat engine + test dungeons (3–4 weeks)
- Full PF1 combat (solo hero vs. monster, no parties yet).
- A small set of monsters bulk-imported from SRD (CR ¼ to CR 3).
- Conditions, AoOs, full attack vs. standard, basic action economy.
- Behavior DSL parser + a *small* action vocabulary (move, charge,
  attack, full_attack, withdraw, drink_potion).
- **Test dungeon harness** runs first — debug scripts in seconds, not
  in a real-time world. This is what makes the rest of the project
  iterable.
- Deliverable: a level-1 fighter with a 50-line `.beh` file kills a
  goblin in a test dungeon. Reproducible via seed.

### Phase 3 — Real-time world + minimal sandbox (3–4 weeks)
- Flat 2D map. A handful of hand-authored anchor regions.
- Real-time clock, continuous unit movement at PF1 speeds.
- Castle persistence (JSON-on-disk).
- Deployment pipeline: submit order, hero walks to a destination,
  encounters the resident creature, fights, walks home (or dies).
- Patron sees the deployment trace through `/v1/castle/deployments/
  {did}` as it accumulates.
- Deliverable: a level-1 fighter deploys, kills goblins at the
  Whispering Wood, returns home, banks renown — all in real time.
  The whole sandbox loop exists, end to end, even if narrow.

### Phase 4 — Resources, crafting, equipment lifecycle (3–4 weeks)
- Resource nodes on the map, gathering as a deployment objective.
- PF1-rule-driven crafting at the castle (deterministic with failure
  rate, default).
- Stockpile management; equipment loaded onto next deployment.
- Full level progression for non-casters (fighter, barbarian, monk,
  paladin, ranger) through level 10.
- Deliverable: build divergence is real. A "gatherer" patron looks
  different from a "killer" patron at equal renown.

### Phase 5 — Multi-hero parties (3–4 weeks)
- Parties of up to 4 heroes deploy together.
- Behavior DSL extended with party roles, cross-hero conditions,
  signals.
- Initiative-aware turn execution; coordinated tactics.
- Deliverable: a fighter+cleric+wizard+rogue party deploys, the
  cleric heals when teammates are low, the wizard fireballs when
  the rogue flanks. PF1 as designed.

### Phase 6 — Spellcasting, levels 2–20, full monster catalog (4–6 weeks)
- Vancian + spontaneous casting fully implemented.
- Spell save DCs, SR, dispels, concentration.
- Bulk-import the rest of MM (CR 4 through CR 20+).
- All 11 classes leveled 1–20.
- Standard-library doctrines published for each role.
- Deliverable: level-10 parties play recognizable PF1 — buffs stacked,
  flanks set, save-or-suck spells used wisely.

### Phase 7 — Monster dens, monster commanding (3–4 weeks)
- Diplomacy/Intimidate/charm/dominate hooks in behavior DSL.
- Den construction pipeline (recruit → escort → settle).
- Den persistence and patrol behavior on the world map.
- Encounter generation: when patron B's hero crosses patron A's den,
  the den becomes the encounter.
- Renown income from active dens.
- Deliverable: a patron builds a goblin den; another patron's hero
  fights through it.

### Phase 8+ — Meta-progression, advanced patron politics
- Renown-tier unlocks, named NPC recruiting, castle upgrades.
- Conditional level-up plan branches.
- Indirect PvP via contested resources.
- Eventually: Raise-Dead unlock, sieges, alliances, formal trade.

This is multi-month work. Each phase ships something playable on its
own — the patron has a game at the end of phase 3 even though nothing
past goblins exists yet. **Every phase is a complete game, just
smaller.**

---

# Ready to Start

The big architectural decisions are locked (see *Decisions Locked* above).
Remaining open questions are calibration, not blockers — I'll default
sensibly and we'll iterate.

**Phase 1 — Foundation skeleton** is the next concrete step: project
scaffold, server, dice, OGL.txt, level-1 character creation for the 7
core races and 11 base classes, pure-engine test harness. ~1–2 weeks of
work, deliverable is a testable rules-engine foundation that everything
else builds on.

Say the word and I'll start.
