# Character Options Inventory (PF1 Core Rulebook)

Comprehensive checklist of every character-build option from the PF1 Core
Rulebook. Tracks what's authored as content and what's mechanically wired
into the engine.

**Status legend:**
- ✓ — Implemented (data authored AND mechanical effects wired)
- ⚠ — Partial (data authored, runtime effect missing or stubbed)
- ❌ — Not yet started

---

## 1. Character Foundation

### Ability scores
- ✓ Six ability scores: STR, DEX, CON, INT, WIS, CHA
- ✓ Generation methods: 4d6kh3 rolled, point-buy 10/15/20/25, standard array
- ✓ Modifier formula: (score - 10) // 2

### Alignment
- ✓ All 9 alignments (LG/NG/CG/LN/TN/CN/LE/NE/CE)
- ⚠ Class alignment restrictions (paladin LG, monk lawful, druid neutral, barbarian non-lawful) enforced at creation; in-play alignment shifts not modeled

### Hit points
- ✓ Max HP at level 1 (HD + Con mod)
- ❌ Rolled HP for levels 2+
- ❌ Favored class +1 HP per level option
- ❌ Toughness feat bonus

### Skills (build-time)
- ✓ Skill points per level = class base + Int mod (min 1) + race bonus
- ✓ ×4 multiplier at level 1
- ✓ Max ranks per skill = character level
- ✓ Class skill +3 bonus (with at least 1 rank)

### Multiclassing
- ❌ Multi-class progression (BAB stacking, save additions, skill points across classes)
- ❌ Favored class XP penalty / favored class bonuses

### Languages
- ✓ Starting languages from race
- ✓ Bonus languages = Int mod, picked from race's bonus list

---

## 2. Races (7 core)

| Race | Status | Mechanical traits status |
|---|---|---|
| Human | ✓ data; ⚠ traits | bonus feat at L1 ✓; +1 skill rank/level ✓; +2 to chosen ability ✓ |
| Dwarf | ✓ data; ⚠ traits | ability mods ✓; speed 20 not slowed by armor ❌; defensive training (+4 vs giants) ❌; hardy (+2 vs poison/spells/SLAs) ❌; stability (+4 vs trip/bull rush) ❌; stonecunning (+2 Perception for stonework) ❌; hatred (+1 vs orcs/goblinoids) ❌; weapon familiarity ❌; darkvision 60 ⚠ (data only) |
| Elf | ✓ data; ⚠ traits | ability mods ✓; elven immunities (immune sleep, +2 vs enchantments) ❌; elven magic (+2 SR checks, +2 Spellcraft for magic items) ❌; keen senses (+2 Perception) ❌; weapon familiarity ❌; low-light vision ⚠ |
| Gnome | ✓ data; ⚠ traits | ability mods ✓; small size ✓; defensive training (+4 dodge AC vs giants) ❌; gnome magic (+1 illusion DC, SLAs) ❌; hatred (vs reptilian/goblinoid) ❌; illusion resistance (+2 saves) ❌; keen senses ❌; obsessive (+2 to a craft/profession) ❌; weapon familiarity ❌; low-light vision ⚠ |
| Half-Elf | ✓ data; ⚠ traits | adaptability (Skill Focus bonus feat) ❌; elf blood (counts as both) ❌; elven immunities ❌; keen senses ❌; multitalented ❌; low-light vision ⚠ |
| Half-Orc | ✓ data; ⚠ traits | intimidating (+2 Intimidate) ❌; orc ferocity (1/day fight on at <0 HP for 1 round) ❌; orc blood ❌; weapon familiarity (greataxe, falchion) ❌; darkvision 60 ⚠ |
| Halfling | ✓ data; ⚠ traits | ability mods ✓; small size ✓; fearless (+2 fear stacks with luck) ❌; halfling luck (+1 all saves) ❌; keen senses ❌; sure-footed (+2 Acrobatics, Climb) ❌; weapon familiarity (sling, halfling weapons) ❌ |

### Vision modes
- ⚠ Normal / Low-light / Darkvision 60 — captured on race; no light-based mechanics yet (no darkness penalty, no LL benefits)

---

## 3. Classes (11 core, level 1 → 20)

For each class: level 1 features show actual implementation status, levels 2+ are not yet started.

### Barbarian
- ✓ HD d12, full BAB, good Fort, skill points 4
- ⚠ L1: Fast Movement (+10 ft) — data only
- ⚠ L1: Rage (4+Con rounds, +4 morale Str/Con, +2 morale Will, -2 AC) — data only; no rage_start action
- ❌ L2: Uncanny Dodge; rage power
- ❌ L3: Trap Sense +1
- ❌ L4: Rage power
- ❌ L5: Improved Uncanny Dodge
- ❌ L7: Damage Reduction
- ❌ L11: Greater Rage
- ❌ L14: Indomitable Will
- ❌ L17: Tireless Rage
- ❌ L20: Mighty Rage
- ❌ Rage Powers list (~50 in CRB): Animal Fury, Clear Mind, Fearless Rage, Guarded Stance, Increased Damage Reduction, Internal Fortitude, Intimidating Glare, Knockback, Knockdown, Low-Light Vision, Mighty Swing, Moment of Clarity, Night Vision, No Escape, Powerful Blow, Quick Reflexes, Raging Climber, Raging Leaper, Raging Swimmer, Renewed Vigor, Rolling Dodge, Roused Anger, Scent, Strength Surge, Superstition, Surprise Accuracy, Swift Foot, Terrifying Howl, Unexpected Strike

### Bard
- ✓ HD d8, 3/4 BAB, good Ref + Will, skill points 6
- ⚠ L1: Bardic Knowledge (+1/2 level all Knowledge) — data only
- ⚠ L1: Bardic Performance (Countersong, Distraction, Fascinate, Inspire Courage +1) — data only
- ⚠ L1: Cantrips known — slot count tracked, specific spells not selectable
- ⚠ L1: Spontaneous casting (Cha-based) — slot count tracked
- ❌ L2: Versatile Performance, Well-Versed
- ❌ L3: Inspire Competence +2
- ❌ L5: Lore Master 1/day
- ❌ L6: Suggestion
- ❌ L8: Dirge of Doom
- ❌ L9: Inspire Greatness
- ❌ L10: Jack-of-All-Trades
- ❌ L12: Soothing Performance
- ❌ L14: Frightening Tune
- ❌ L15: Inspire Heroics
- ❌ L18: Mass Suggestion
- ❌ L20: Deadly Performance

### Cleric
- ✓ HD d8, 3/4 BAB, good Fort + Will, skill points 2
- ❌ Deity choice (CRB has Sarenrae, Iomedae, etc., or generic)
- ⚠ L1: Aura — data only
- ⚠ L1: Channel Energy 1d6 (3+Cha mod/day, 30-ft burst, heal/harm) — data only
- ⚠ L1: Domains (×2) — choices defined; powers/granted spells not wired
- ⚠ L1: Spontaneous casting (cure or inflict) — not wired
- ⚠ L1: Orisons — slot count tracked
- ❌ L2: (channel scaling)
- ❌ Higher-level domain powers per chosen domain

### Druid
- ✓ HD d8, 3/4 BAB, good Fort + Will, skill points 4
- ⚠ L1: Nature Bond (animal companion or domain) — data only; companion stats not generated
- ⚠ L1: Nature Sense (+2 Knowledge nature, Survival) — data only
- ⚠ L1: Wild Empathy — data only
- ⚠ L1: Orisons — slot count tracked
- ❌ L2: Woodland Stride
- ❌ L3: Trackless Step
- ❌ L4: Resist Nature's Lure
- ❌ L4: Wild Shape (huge feature; many forms)
- ❌ L9: Venom Immunity
- ❌ L13: Thousand Faces
- ❌ L15: Timeless Body
- ❌ Druid domains (subset of cleric domains): Air, Animal, Earth, Fire, Plant, Water, Weather

### Fighter
- ✓ HD d10, full BAB, good Fort, skill points 2
- ⚠ L1: Bonus Combat Feat — feat is selected and stored on character; the feat's effect isn't applied as a modifier (e.g., Weapon Focus +1 attack not added)
- ❌ L2: Bravery +1 (+1 vs fear)
- ❌ L2/4/6/8/10/12/14/16/18/20: additional combat feats
- ❌ L3: Armor Training 1 (-1 ACP, +1 max Dex)
- ❌ L5: Weapon Training 1 (+1 attack/damage with chosen group)
- ❌ L7/11/15: Armor/Weapon Training scaling
- ❌ L19: Armor Mastery (DR 5/—)
- ❌ L20: Weapon Mastery
- ❌ Weapon Groups list (~17 in CRB): Axes, Blades (heavy), Blades (light), Bows, Close, Crossbows, Double, Flails, Hammers, Monk, Natural, Polearms, Pole arms, Spears, Thrown, Tribal

### Monk
- ✓ HD d8, 3/4 BAB, all good saves (unique), skill points 4
- ❌ L1: AC Bonus (+Wis when unarmored, +1/4 levels)
- ⚠ L1: Flurry of Blows — data only; not a turn-executor option
- ⚠ L1: Stunning Fist (1+1/4 levels per day) — data only
- ⚠ L1: Unarmed Strike — weapon exists but damage scaling (1d6 medium, 1d4 small at L1, scaling by level) not wired
- ⚠ L1: Bonus Feat (one of: Catch Off-Guard, Combat Reflexes, Deflect Arrows, Dodge, Improved Grapple, Scorpion Style, Throw Anything) — selected, not effects applied
- ❌ L2: Bonus Feat, Evasion
- ❌ L3: Fast Movement (+10 ft, scaling), Maneuver Training, Still Mind
- ❌ L4: Ki Pool
- ❌ L5: High Jump, Purity of Body
- ❌ L7: Wholeness of Body
- ❌ L8: Condition Fist (additional Stunning Fist effects)
- ❌ L9: Improved Evasion
- ❌ L11: Diamond Body
- ❌ L12: Abundant Step
- ❌ L13: Diamond Soul
- ❌ L15: Quivering Palm
- ❌ L17: Timeless Body, Tongue of the Sun and Moon
- ❌ L19: Empty Body
- ❌ L20: Perfect Self

### Paladin
- ✓ HD d10, full BAB, good Fort + Will, skill points 2, alignment LG required
- ⚠ L1: Aura of Good — data only
- ⚠ L1: Detect Evil — data only
- ⚠ L1: Smite Evil 1/day — data only
- ❌ L2: Divine Grace (Cha to all saves), Lay on Hands
- ❌ L3: Aura of Courage, Divine Health, Mercy
- ❌ L4: Channel Positive Energy
- ❌ L5: Divine Bond (mount or weapon)
- ❌ L8: Aura of Resolve
- ❌ L11: Aura of Justice
- ❌ L14: Aura of Faith
- ❌ L17: Aura of Righteousness, Holy Champion
- ❌ L20: Holy Champion (final)
- ❌ Mercies list (~12 in CRB): Fatigued, Shaken, Sickened, Dazed, Diseased, Staggered, Cursed, Exhausted, Frightened, Nauseated, Poisoned, Stunned
- ❌ Spell progression (1st-level spells at L4)

### Ranger
- ✓ HD d10, full BAB, good Fort + Ref, skill points 6
- ⚠ L1: Favored Enemy (1, +2 attack/damage and skill against type) — data only
- ⚠ L1: Track (+1/2 level Survival to follow tracks) — data only
- ⚠ L1: Wild Empathy — data only
- ❌ L2: Combat Style feat (Archery or Two-Weapon Combat)
- ❌ L3: Endurance, Favored Terrain (1)
- ❌ L4: Hunter's Bond (companion or hunting team), Animal Companion option
- ❌ L4+: Spells (1st-level at L4)
- ❌ L5: Favored Enemy 2nd
- ❌ L6/10/14/18: combat style scaling
- ❌ L7: Woodland Stride
- ❌ L8: Swift Tracker
- ❌ L9: Evasion
- ❌ L11: Quarry
- ❌ L12: Camouflage
- ❌ L17: Hide in Plain Sight
- ❌ L19: Improved Quarry
- ❌ L20: Master Hunter
- ❌ Favored Terrains list: Cold, Desert, Forest, Jungle, Mountain, Plains, Planes (subset), Swamp, Underground, Urban, Water

### Rogue
- ✓ HD d8, 3/4 BAB, good Ref, skill points 8 (highest)
- ⚠ L1: Sneak Attack +1d6 — data only; precision damage not wired into combat resolution
- ⚠ L1: Trapfinding — data only; no trap mechanics
- ❌ L2: Evasion, Rogue Talent
- ❌ L3: Sneak Attack +2d6, Trap Sense +1
- ❌ L4/6/8/10/12/14/16/18/20: rogue talents
- ❌ L5/9/13/17: Sneak Attack scaling
- ❌ L8: Improved Uncanny Dodge
- ❌ L10: Advanced Talents
- ❌ L20: Master Strike
- ❌ Rogue Talents list (~30 in CRB): Bleeding Attack, Combat Trick, Fast Stealth, Finesse Rogue, Ledge Walker, Major Magic, Minor Magic, Quick Disable, Resiliency, Rogue Crawl, Slow Reactions, Stand Up, Surprise Attack, Trap Spotter, Weapon Training, Wand Use, Defensive Roll, Improved Evasion, Opportunist, Skill Mastery, Slippery Mind, Crippling Strike, Feat (advanced)

### Sorcerer
- ✓ HD d6, 1/2 BAB, good Will, skill points 2
- ⚠ L1: Bloodline (one chosen) — choices defined; powers and bonus spells not wired
- ⚠ L1: Eschew Materials (auto-bonus feat) — feat in list; no material-component cost tracking
- ⚠ L1: Cantrips — slot count tracked, specific spells not selectable
- ⚠ L1: Spontaneous casting (Cha-based) — slot count tracked
- ❌ L3/9/15/20: Bloodline-specific abilities at higher levels
- ❌ Spells per day and spells known scaling

### Wizard
- ✓ HD d6, 1/2 BAB, good Will, skill points 2
- ⚠ L1: Arcane School (one of 8, or Universalist) — choice affects bonus 1st-level slot; powers not wired
- ⚠ L1: Arcane Bond (familiar or bonded object) — data only; no familiar entity created
- ⚠ L1: Scribe Scroll (auto-bonus feat) — feat in list; no scroll crafting mechanic
- ⚠ L1: Cantrips — slot count tracked
- ⚠ L1: Prepared casting from spellbook — slot count tracked; spellbook content not modeled
- ❌ L1: Starting spellbook (all 0-level + 3 + Int mod 1st-level)
- ❌ L5/10/15/20: Bonus feat from item creation/metamagic/Spell Mastery list
- ❌ Specialist school powers (per school)
- ❌ Opposed schools double-cost penalty

---

## 4. Skills (35 core)

All skills are loaded; modifiers and class-skill bonus are wired. Specific
skill checks (Diplomacy attitude shifts, Stealth opposed by Perception,
Climb DC tables, etc.) need their own action handlers.

| Skill | Loaded | Check resolution |
|---|---|---|
| Acrobatics (Dex, ACP) | ✓ | ❌ |
| Appraise (Int) | ✓ | ❌ |
| Bluff (Cha) | ✓ | ❌ |
| Climb (Str, ACP) | ✓ | ❌ |
| Craft (Int, by subtype) | ✓ | ❌ |
| Diplomacy (Cha) | ✓ | ❌ |
| Disable Device (Dex, trained, ACP) | ✓ | ❌ |
| Disguise (Cha) | ✓ | ❌ |
| Escape Artist (Dex, ACP) | ✓ | ❌ |
| Fly (Dex, ACP) | ✓ | ❌ |
| Handle Animal (Cha, trained) | ✓ | ❌ |
| Heal (Wis) | ✓ | ❌ |
| Intimidate (Cha) | ✓ | ❌ |
| Knowledge: Arcana (Int, trained) | ✓ | ❌ |
| Knowledge: Dungeoneering | ✓ | ❌ |
| Knowledge: Engineering | ✓ | ❌ |
| Knowledge: Geography | ✓ | ❌ |
| Knowledge: History | ✓ | ❌ |
| Knowledge: Local | ✓ | ❌ |
| Knowledge: Nature | ✓ | ❌ |
| Knowledge: Nobility | ✓ | ❌ |
| Knowledge: Planes | ✓ | ❌ |
| Knowledge: Religion | ✓ | ❌ |
| Linguistics (Int, trained) | ✓ | ❌ |
| Perception (Wis) | ✓ | ❌ |
| Perform (Cha, by subtype) | ✓ | ❌ |
| Profession (Wis, trained, by subtype) | ✓ | ❌ |
| Ride (Dex, ACP) | ✓ | ❌ |
| Sense Motive (Wis) | ✓ | ❌ |
| Sleight of Hand (Dex, trained, ACP) | ✓ | ❌ |
| Spellcraft (Int, trained) | ✓ | ❌ |
| Stealth (Dex, ACP) | ✓ | ❌ |
| Survival (Wis) | ✓ | ❌ |
| Swim (Str, ACP) | ✓ | ❌ |
| Use Magic Device (Cha, trained) | ✓ | ❌ |

---

## 5. Feats

CRB has roughly 200 feats. Currently ~30 are authored as data; almost
none of their mechanical effects are applied at runtime (they're picked
and validated for prerequisites, but feats like Weapon Focus don't yet
add their +1 to hit).

Authoring status: ⚠ for feats that exist in `feats.json`, ❌ for those
not yet authored. Wiring is ❌ for nearly every feat regardless of
authoring.

### Combat feats (largest category — ~100 in CRB)

| Feat | Auth | Wired |
|---|---|---|
| Agile Maneuvers | ❌ | ❌ |
| Arcane Armor Mastery | ❌ | ❌ |
| Arcane Armor Training | ❌ | ❌ |
| Arcane Strike | ❌ | ❌ |
| Bleeding Critical | ❌ | ❌ |
| Blind-Fight | ❌ | ❌ |
| Catch Off-Guard | ❌ | ❌ |
| Cleave | ⚠ | ❌ |
| Combat Casting | ❌ | ❌ |
| Combat Expertise | ⚠ | ❌ |
| Combat Reflexes | ⚠ | ❌ |
| Crippling Critical | ❌ | ❌ |
| Critical Focus | ❌ | ❌ |
| Critical Mastery | ❌ | ❌ |
| Dazzling Display | ❌ | ❌ |
| Deadly Aim | ❌ | ❌ |
| Deadly Stroke | ❌ | ❌ |
| Deafening Critical | ❌ | ❌ |
| Deflect Arrows | ❌ | ❌ |
| Disrupting Strike | ❌ | ❌ |
| Disruptive | ❌ | ❌ |
| Dodge | ⚠ | ❌ |
| Double Slice | ❌ | ❌ |
| Exhausting Critical | ❌ | ❌ |
| Far Shot | ❌ | ❌ |
| Furious Focus | ❌ | ❌ |
| Gorgon's Fist | ❌ | ❌ |
| Greater Bull Rush | ❌ | ❌ |
| Greater Disarm | ❌ | ❌ |
| Greater Feint | ❌ | ❌ |
| Greater Grapple | ❌ | ❌ |
| Greater Overrun | ❌ | ❌ |
| Greater Penetrating Strike | ❌ | ❌ |
| Greater Shield Focus | ❌ | ❌ |
| Greater Sunder | ❌ | ❌ |
| Greater Trip | ❌ | ❌ |
| Greater Two-Weapon Fighting | ❌ | ❌ |
| Greater Vital Strike | ❌ | ❌ |
| Greater Weapon Focus | ❌ | ❌ |
| Greater Weapon Specialization | ❌ | ❌ |
| Improved Bull Rush | ❌ | ❌ |
| Improved Critical | ❌ | ❌ |
| Improved Disarm | ❌ | ❌ |
| Improved Feint | ❌ | ❌ |
| Improved Grapple | ❌ | ❌ |
| Improved Initiative | ⚠ | ❌ |
| Improved Overrun | ❌ | ❌ |
| Improved Precise Shot | ❌ | ❌ |
| Improved Shield Bash | ❌ | ❌ |
| Improved Sunder | ❌ | ❌ |
| Improved Trip | ❌ | ❌ |
| Improved Two-Weapon Fighting | ❌ | ❌ |
| Improved Unarmed Strike | ⚠ | ❌ |
| Improved Vital Strike | ❌ | ❌ |
| Intimidating Prowess | ❌ | ❌ |
| Iron Will | ⚠ | ❌ |
| Lightning Reflexes | ⚠ | ❌ |
| Lightning Stance | ❌ | ❌ |
| Lunge | ❌ | ❌ |
| Manyshot | ❌ | ❌ |
| Master Craftsman | ❌ | ❌ |
| Medusa's Wrath | ❌ | ❌ |
| Mobility | ❌ | ❌ |
| Mounted Archery | ❌ | ❌ |
| Mounted Combat | ❌ | ❌ |
| Nimble Moves | ❌ | ❌ |
| Penetrating Strike | ❌ | ❌ |
| Pinpoint Targeting | ❌ | ❌ |
| Point-Blank Shot | ⚠ | ❌ |
| Power Attack | ⚠ | ❌ |
| Precise Shot | ⚠ | ❌ |
| Quick Draw | ❌ | ❌ |
| Rapid Reload | ❌ | ❌ |
| Rapid Shot | ⚠ | ❌ |
| Ride-By Attack | ❌ | ❌ |
| Run | ⚠ | ❌ |
| Scorpion Style | ❌ | ❌ |
| Shatter Defenses | ❌ | ❌ |
| Shield Focus | ❌ | ❌ |
| Shield Master | ❌ | ❌ |
| Shield Slam | ❌ | ❌ |
| Sickening Critical | ❌ | ❌ |
| Snatch Arrows | ❌ | ❌ |
| Spirited Charge | ❌ | ❌ |
| Spring Attack | ❌ | ❌ |
| Staggering Critical | ❌ | ❌ |
| Stand Still | ❌ | ❌ |
| Step Up | ❌ | ❌ |
| Stunning Critical | ❌ | ❌ |
| Stunning Fist | ❌ | ❌ |
| Throw Anything | ❌ | ❌ |
| Tiring Critical | ❌ | ❌ |
| Toughness | ⚠ | ❌ |
| Trample | ❌ | ❌ |
| Two-Weapon Defense | ❌ | ❌ |
| Two-Weapon Fighting | ⚠ | ❌ |
| Two-Weapon Rend | ❌ | ❌ |
| Unseat | ❌ | ❌ |
| Vital Strike | ❌ | ❌ |
| Weapon Finesse | ⚠ | ❌ |
| Weapon Focus | ⚠ | ❌ |
| Weapon Specialization | ❌ | ❌ |
| Whirlwind Attack | ❌ | ❌ |
| Wind Stance | ❌ | ❌ |

### Item Creation feats (8 in CRB)

| Feat | Auth | Wired |
|---|---|---|
| Brew Potion | ❌ | ❌ |
| Craft Magic Arms and Armor | ❌ | ❌ |
| Craft Rod | ❌ | ❌ |
| Craft Staff | ❌ | ❌ |
| Craft Wand | ❌ | ❌ |
| Craft Wondrous Item | ❌ | ❌ |
| Forge Ring | ❌ | ❌ |
| Scribe Scroll | ⚠ | ❌ |

### Metamagic feats (10 in CRB)

| Feat | Auth | Wired |
|---|---|---|
| Empower Spell | ⚠ | ❌ |
| Enlarge Spell | ❌ | ❌ |
| Extend Spell | ❌ | ❌ |
| Heighten Spell | ❌ | ❌ |
| Maximize Spell | ❌ | ❌ |
| Quicken Spell | ❌ | ❌ |
| Silent Spell | ❌ | ❌ |
| Still Spell | ❌ | ❌ |
| Widen Spell | ❌ | ❌ |
| Eschew Materials | ⚠ | ❌ |

### General feats (~80 in CRB; some most common)

| Feat | Auth | Wired |
|---|---|---|
| Acrobatic | ❌ | ❌ |
| Alertness | ⚠ | ❌ |
| Animal Affinity | ❌ | ❌ |
| Athletic | ⚠ | ❌ |
| Augment Summoning | ❌ | ❌ |
| Deceitful | ❌ | ❌ |
| Deft Hands | ❌ | ❌ |
| Diehard | ⚠ | ❌ |
| Endurance | ⚠ | ❌ |
| Extra Channel | ❌ | ❌ |
| Extra Ki | ❌ | ❌ |
| Extra Lay On Hands | ❌ | ❌ |
| Extra Mercy | ❌ | ❌ |
| Extra Performance | ❌ | ❌ |
| Extra Rage | ❌ | ❌ |
| Extra Rage Power | ❌ | ❌ |
| Greater Spell Focus | ❌ | ❌ |
| Greater Spell Penetration | ❌ | ❌ |
| Great Fortitude | ⚠ | ❌ |
| Improved Counterspell | ❌ | ❌ |
| Improved Familiar | ❌ | ❌ |
| Improved Great Fortitude | ❌ | ❌ |
| Improved Iron Will | ❌ | ❌ |
| Improved Lightning Reflexes | ❌ | ❌ |
| Investigator | ❌ | ❌ |
| Leadership | ❌ | ❌ |
| Magical Aptitude | ❌ | ❌ |
| Natural Spell | ❌ | ❌ |
| Nimble Moves | ❌ | ❌ |
| Persuasive | ⚠ | ❌ |
| Self-Sufficient | ❌ | ❌ |
| Skill Focus | ⚠ | ❌ |
| Spell Focus | ⚠ | ❌ |
| Spell Mastery | ❌ | ❌ |
| Spell Penetration | ⚠ | ❌ |
| Stealthy | ⚠ | ❌ |

---

## 6. Equipment

### Weapons

CRB has ~50 weapons. Currently ~20 authored.

#### Simple weapons
| Weapon | Auth | Notes |
|---|---|---|
| Gauntlet | ❌ | |
| Spiked Gauntlet | ❌ | |
| Unarmed Strike | ⚠ | data; needs monk size scaling |
| Dagger | ⚠ | |
| Punching Dagger | ❌ | |
| Spiked Armor | ❌ | |
| Mace, Light | ❌ | |
| Mace, Heavy | ❌ | |
| Sickle | ❌ | |
| Club | ⚠ | |
| Morningstar | ❌ | |
| Quarterstaff | ⚠ | |
| Spear | ⚠ | |
| Longspear | ❌ | reach weapon |
| Shortspear | ❌ | |
| Crossbow, Light | ⚠ | |
| Crossbow, Heavy | ⚠ | |
| Dart | ❌ | |
| Javelin | ❌ | |
| Sling | ⚠ | |

#### Martial weapons
| Weapon | Auth | Notes |
|---|---|---|
| Battleaxe | ⚠ | |
| Falchion | ⚠ | |
| Flail | ❌ | |
| Glaive | ❌ | reach |
| Greataxe | ⚠ | |
| Greatclub | ❌ | |
| Greatsword | ⚠ | |
| Guisarme | ❌ | reach, trip |
| Halberd | ⚠ | |
| Handaxe | ❌ | |
| Heavy Pick | ❌ | x4 crit |
| Lance | ❌ | reach, mounted |
| Light Hammer | ❌ | |
| Light Pick | ❌ | |
| Longsword | ⚠ | |
| Ranseur | ❌ | reach, disarm |
| Rapier | ⚠ | |
| Sap | ❌ | nonlethal |
| Scimitar | ⚠ | |
| Short Sword | ⚠ | |
| Trident | ❌ | |
| Warhammer | ⚠ | |
| Whip | ❌ | reach, finesse-like, disarm/trip |
| Longbow | ⚠ | |
| Shortbow | ⚠ | |
| Composite Longbow | ❌ | Str rating |
| Composite Shortbow | ❌ | Str rating |

#### Exotic weapons
| Weapon | Auth | Notes |
|---|---|---|
| Bastard Sword | ❌ | |
| Dwarven Waraxe | ❌ | |
| Dwarven Urgrosh | ❌ | double weapon |
| Elven Curve Blade | ❌ | finesse-eligible 2H |
| Gnome Hooked Hammer | ❌ | double weapon |
| Kama | ❌ | |
| Nunchaku | ❌ | |
| Sai | ❌ | |
| Shuriken | ❌ | |
| Siangham | ❌ | |
| Spiked Chain | ❌ | reach, finesse-eligible |
| Whip | ❌ | (also exotic) |
| Bolas | ❌ | |
| Hand Crossbow | ❌ | |
| Repeating Crossbow (light/heavy) | ❌ | |
| Net | ❌ | |
| Blowgun | ❌ | |

#### Special weapon properties / materials
- ❌ Masterwork (+1 to hit, no bonus damage)
- ❌ Special materials: Adamantine, Cold Iron, Mithral, Silver (alchemical), Darkwood
- ❌ Magical enhancement bonuses (+1 to +5)
- ❌ Magical weapon properties (Flaming, Frost, Holy, Keen, Speed, Vorpal, etc.) — see Magic Items

### Armor

| Armor | Auth | Notes |
|---|---|---|
| Padded | ⚠ | |
| Leather | ⚠ | |
| Studded Leather | ⚠ | |
| Chain Shirt | ⚠ | |
| Hide | ⚠ | |
| Scale Mail | ⚠ | |
| Chainmail | ⚠ | |
| Breastplate | ⚠ | |
| Splint Mail | ⚠ | |
| Banded Mail | ❌ | |
| Half-plate | ⚠ | |
| Full Plate | ⚠ | |

### Shields
| Shield | Auth |
|---|---|
| Buckler | ⚠ |
| Light Wooden Shield | ⚠ |
| Light Steel Shield | ⚠ |
| Heavy Wooden Shield | ⚠ |
| Heavy Steel Shield | ⚠ |
| Tower Shield | ⚠ |

### Adventuring gear (CRB ~50 items)
- ❌ Backpack, bedroll, blanket, candle, chalk, chain (10 ft), crowbar, fishhook, flint and steel, grappling hook, hammer, ink/inkpen, jug, ladder, lamp/oil, lantern (bullseye/hooded), lock (simple/average/good/superior), magnifying glass, manacles, mirror (small steel), pitons, pole (10-ft), rations (trail), rope (hempen/silk), sack, sealing wax, shovel, signal whistle, sledge, soap, spell component pouch, spyglass, tent, torch, vial, waterskin, whetstone

### Tools / kits
- ❌ Alchemist's lab, healer's kit, holy symbol (silver/wooden), spellbook, thieves' tools (regular/masterwork)

### Mounts
- ❌ Horse (light/heavy/warhorse), pony, donkey/mule, dog (riding), camel
- ❌ Mount gear: barding, bit, bridle, saddle (military/pack/riding), saddlebags

### Consumables (data only — no use mechanics yet)
- ❌ Standard alchemical: acid (flask), alchemist's fire, antitoxin, holy water, smokestick, sunrod, tanglefoot bag, thunderstone, tindertwig

---

## 7. Spells (CRB ~470)

Currently spell *slots* are computed for casters but no specific spells
are loaded as content, no spell selection mechanism, no casting
mechanics. ⚠ across the board = "slot tracked, spell content not
authored." Will need its own dedicated phase.

### By class & level (counts approximate from CRB)

| Class | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| Bard | ~12 | ~26 | ~26 | ~24 | ~22 | ~20 | ~18 | — | — | — |
| Cleric | ~13 | ~31 | ~32 | ~32 | ~24 | ~22 | ~22 | ~21 | ~19 | ~17 |
| Druid | ~13 | ~26 | ~24 | ~26 | ~24 | ~22 | ~21 | ~17 | ~14 | ~13 |
| Paladin | — | ~12 | ~10 | ~10 | ~10 | — | — | — | — | — |
| Ranger | — | ~12 | ~12 | ~12 | ~12 | — | — | — | — | — |
| Sorcerer/Wizard | ~14 | ~36 | ~38 | ~37 | ~38 | ~38 | ~36 | ~35 | ~34 | ~31 |

### Notable spells to author first (highest gameplay impact)

#### Cantrips
- Detect Magic, Detect Poison, Read Magic, Light, Mending, Mage Hand, Acid Splash, Ray of Frost, Daze, Open/Close, Resistance, Guidance, Stabilize, Bleed, Spark, Virtue, Disrupt Undead, Touch of Fatigue, Prestidigitation, Arcane Mark, Flare, Ghost Sound, Message, Dancing Lights, Know Direction

#### Level 1
- Cure Light Wounds (cleric/druid/paladin/ranger/bard), Inflict Light Wounds (cleric)
- Bless, Bane (cleric)
- Magic Missile, Burning Hands, Color Spray, Sleep, Charm Person, Mage Armor, Shield, Magic Weapon (sor/wiz)
- Shield of Faith, Sanctuary, Divine Favor, Protection from Evil/etc, Command, Doom (cleric)
- Entangle, Faerie Fire, Goodberry, Produce Flame, Speak with Animals (druid)
- Cause Fear, Ray of Enfeeblement (sor/wiz)
- Grease, Obscuring Mist, Silent Image, Identify, Comprehend Languages, Enlarge Person, Reduce Person, Feather Fall, Floating Disk, Hold Portal, True Strike, Unseen Servant, Vanish (sor/wiz)
- Summon Monster I (cleric/druid/sor/wiz)

#### Level 2
- Cure Moderate Wounds, Inflict Moderate Wounds
- Hold Person, Silence, Spiritual Weapon, Sound Burst, Calm Emotions, Aid, Shield Other (cleric)
- Bear's Endurance, Bull's Strength, Cat's Grace, Eagle's Splendor, Fox's Cunning, Owl's Wisdom (universal buff line)
- Acid Arrow, Web, Glitterdust, Invisibility, Mirror Image, Scorching Ray, Flaming Sphere, Hideous Laughter (sor/wiz)
- Heat Metal, Barkskin, Flame Blade, Tree Shape, Spider Climb (druid)
- Summon Monster II
- Resist Energy, Levitate, Knock, See Invisibility

#### Level 3
- Cure Serious Wounds, Inflict Serious Wounds
- Fireball, Lightning Bolt, Fly, Haste, Slow, Dispel Magic, Stinking Cloud, Suggestion, Magic Circle vs X, Vampiric Touch, Hold Person Mass, Sleet Storm, Major Image, Tongues, Water Breathing, Wind Wall, Stone Shape (sor/wiz/cleric/druid)
- Searing Light, Daylight, Prayer, Magic Vestment (cleric)
- Call Lightning, Speak with Plants (druid)
- Animate Dead, Summon Monster III

(continues through level 9; full content authoring is a phase by itself)

### Spell mechanics required
- ❌ Spell preparation (prepared casters)
- ❌ Spells known progression (spontaneous casters)
- ❌ Spellbook for wizards
- ❌ Save DC computation (10 + spell level + key ability mod + Spell Focus)
- ❌ Spell resistance checks
- ❌ Concentration checks (cast in melee, on the defensive, etc.)
- ❌ Range/area/duration parsing
- ❌ Component requirements (V, S, M, F, DF)
- ❌ Counterspell mechanics
- ❌ Dispel magic resolution
- ❌ Spell-like abilities
- ❌ Supernatural abilities

---

## 8. Magic Items

CRB has hundreds of magic items. None authored yet.

### Categories
| Category | Status |
|---|---|
| Armor & Shield enhancements (+1 to +5, magical properties) | ❌ |
| Weapon enhancements (+1 to +5, magical properties) | ❌ |
| Potions (~15 standard) | ❌ |
| Rings (~30 in CRB) | ❌ |
| Rods (~25 in CRB) | ❌ |
| Scrolls (one per spell) | ❌ |
| Staves (~20 in CRB) | ❌ |
| Wands (one per low-level spell) | ❌ |
| Wondrous Items (~150 in CRB) | ❌ |

### Most-iconic items to author first
- Bag of Holding (I-IV)
- Belt of Giant Strength / Incredible Dexterity / Mighty Constitution (+2/+4/+6)
- Headband of Vast Intelligence / Inspired Wisdom / Alluring Charisma (+2/+4/+6)
- Cloak of Resistance (+1 to +5)
- Amulet of Natural Armor (+1 to +5)
- Ring of Protection (+1 to +5)
- Boots of Speed
- Boots of Striding and Springing
- Cloak of Elvenkind
- Boots of Elvenkind
- Eyes of the Eagle
- Gauntlets of Ogre Power
- Gloves of Arrow Snaring
- Hat of Disguise
- Heward's Handy Haversack
- Necklace of Adaptation
- Necklace of Fireballs
- Periapt of Wisdom (+1 to +6) (covered by Headband)
- Portable Hole
- Slippers of Spider Climbing
- Stone of Good Luck
- Wings of Flying

### Weapon special abilities (~30 in CRB)
- Bane, Defending, Distance, Flaming, Flaming Burst, Frost, Holy, Icy Burst, Keen, Ki Focus, Mighty Cleaving, Returning, Shock, Shocking Burst, Speed, Spell Storing, Throwing, Thundering, Unholy, Vicious, Vorpal, Wounding, Anarchic, Axiomatic

### Armor/Shield special abilities
- Animated, Arrow Catching, Arrow Deflection, Bashing, Blinding, Energy Resistance, Etherealness, Fortification (light/moderate/heavy), Ghost Touch, Glamered, Heavy Fortification, Improved Slick, Improved Shadow, Improved Silent Moves, Invulnerability, Reflecting, Shadow, Silent Moves, Slick, Spell Resistance (13/15/17/19), Wild

---

## 9. Domains (Cleric)

CRB has 27+ domains, each with a granted power and a 1st-9th level spell list.

| Domain | Auth | Power | Spells |
|---|---|---|---|
| Air | ⚠ name | ❌ | ❌ |
| Animal | ❌ | ❌ | ❌ |
| Artifice | ❌ | ❌ | ❌ |
| Chaos | ❌ | ❌ | ❌ |
| Charm | ❌ | ❌ | ❌ |
| Community | ❌ | ❌ | ❌ |
| Darkness | ❌ | ❌ | ❌ |
| Death | ⚠ name | ❌ | ❌ |
| Destruction | ❌ | ❌ | ❌ |
| Earth | ⚠ name | ❌ | ❌ |
| Evil | ⚠ name | ❌ | ❌ |
| Fire | ⚠ name | ❌ | ❌ |
| Glory | ❌ | ❌ | ❌ |
| Good | ⚠ name | ❌ | ❌ |
| Healing | ⚠ name | ❌ | ❌ |
| Knowledge | ⚠ name | ❌ | ❌ |
| Law | ⚠ name | ❌ | ❌ |
| Liberation | ❌ | ❌ | ❌ |
| Luck | ❌ | ❌ | ❌ |
| Magic | ⚠ name | ❌ | ❌ |
| Nobility | ❌ | ❌ | ❌ |
| Plant | ❌ | ❌ | ❌ |
| Protection | ❌ | ❌ | ❌ |
| Repose | ❌ | ❌ | ❌ |
| Rune | ❌ | ❌ | ❌ |
| Strength | ❌ | ❌ | ❌ |
| Sun | ❌ | ❌ | ❌ |
| Travel | ❌ | ❌ | ❌ |
| Trickery | ⚠ name | ❌ | ❌ |
| War | ⚠ name | ❌ | ❌ |
| Water | ❌ | ❌ | ❌ |
| Weather | ❌ | ❌ | ❌ |

(`⚠ name` = listed in `cleric.json`'s domain_choices but no implementation.)

---

## 10. Bloodlines (Sorcerer)

CRB has 10 bloodlines. Each grants: bonus class skill, bloodline arcana,
1st/3rd/9th/15th/20th-level powers, and bonus spells per bloodline level.

| Bloodline | Auth | Powers | Spells |
|---|---|---|---|
| Aberrant | ❌ | ❌ | ❌ |
| Abyssal | ❌ | ❌ | ❌ |
| Arcane | ⚠ name | ❌ | ❌ |
| Celestial | ⚠ name | ❌ | ❌ |
| Destined | ❌ | ❌ | ❌ |
| Draconic (10 chromatic/metallic options) | ⚠ name | ❌ | ❌ |
| Elemental (Air/Earth/Fire/Water variants) | ❌ | ❌ | ❌ |
| Fey | ⚠ name | ❌ | ❌ |
| Infernal | ⚠ name | ❌ | ❌ |
| Undead | ❌ | ❌ | ❌ |

---

## 11. Arcane Schools (Wizard)

| School | Auth | Powers | Subschools |
|---|---|---|---|
| Universalist | ⚠ choice | ❌ | n/a (no opposed) |
| Abjuration | ⚠ choice | ❌ | ❌ |
| Conjuration | ⚠ choice | ❌ | Summoner / Teleportation |
| Divination | ⚠ choice | ❌ | Foresight / Scrying |
| Enchantment | ⚠ choice | ❌ | Controller / Manipulator |
| Evocation | ⚠ choice | ❌ | Admixture / Force |
| Illusion | ⚠ choice | ❌ | Phantasmagorist / Shadow |
| Necromancy | ⚠ choice | ❌ | Lich / Undead |
| Transmutation | ⚠ choice | ❌ | Enhancement / Shapechange |

(`⚠ choice` = listed in `wizard.json`'s school_choices but powers/opposed schools/subschools not implemented.)

---

## 12. Animal Companions & Familiars

### Animal companions (Druid, Ranger, Paladin)
None authored. CRB has roughly 30 companion options:
- Bird (eagle, hawk, raven, owl)
- Dog (riding/wolf-style)
- Cat (small / leopard / cheetah)
- Constrictor / Viper
- Crocodile
- Dinosaur (Compsognathus / Deinonychus / Velociraptor / Pteranodon)
- Eidolon (summoner only)
- Horse
- Pony
- Mule / Donkey
- Boar
- Camel
- Elephant
- Wolverine / Badger
- Tiger
- Bear (black / brown)
- Ape / Orangutan
- Lizard (giant gecko / monitor)
- Pig
- Shark (animal companion?)
- Whale (?)

### Familiars (Wizard, Sorcerer w/ Arcane bloodline, Witch)
None authored. CRB has ~10 standard familiars:
- Bat (+3 Fly)
- Cat (+3 Stealth)
- Hawk (+3 Perception in light)
- Lizard (+3 Climb)
- Monkey (+3 Acrobatics)
- Owl (+3 Perception at night)
- Rat (+2 Fort saves)
- Raven (+3 Appraise; speaks one language)
- Toad (+3 HP)
- Weasel (+2 Reflex saves)

### Improved Familiars (require Improved Familiar feat + alignment + caster level)
- Pseudodragon (CL 5, Neutral Good)
- Imp (CL 7, Lawful Evil)
- Quasit (CL 7, Chaotic Evil)
- Mephit (various, CL 7, varying alignment)
- Stirge (CL 5)
- and others

---

## 13. Combat Maneuvers (CRB)

All resolved via CMB vs CMD. Currently `Combatant.cmb()` and `cmd()` are
wired; specific maneuvers are not action handlers yet.

| Maneuver | Authored | Action handler |
|---|---|---|
| Bull Rush | ❌ | ❌ |
| Disarm | ❌ | ❌ |
| Grapple | ❌ | ❌ |
| Overrun | ❌ | ❌ |
| Sunder | ❌ | ❌ |
| Trip | ❌ | ❌ |

(Drag, Reposition, Steal, Dirty Trick are APG, not CRB.)

---

## 14. Conditions

35 conditions authored in `conditions.json`. Mechanical enforcement is partial:

| Condition | Authored | Enforced in combat |
|---|---|---|
| Bleed | ⚠ | ❌ |
| Blinded | ⚠ | ❌ (no flat-footed AC, no miss chance) |
| Confused | ⚠ | ❌ |
| Cowering | ⚠ | ❌ |
| Dazed | ⚠ | ⚠ (validated as no-action in turn) |
| Dazzled | ⚠ | ❌ |
| Deafened | ⚠ | ❌ |
| Dead | ⚠ | ✓ (combatant excluded from combat) |
| Disabled | ⚠ | ❌ |
| Dying | ⚠ | ⚠ (set when HP ≤ 0; no ongoing 1 HP loss) |
| Energy Drained | ⚠ | ❌ |
| Entangled | ⚠ | ❌ |
| Exhausted | ⚠ | ❌ |
| Fascinated | ⚠ | ❌ |
| Fatigued | ⚠ | ❌ |
| Flat-Footed | ⚠ | ✓ (used by AC computation) |
| Frightened | ⚠ | ❌ |
| Grappled | ⚠ | ⚠ (validated for some actions like drink) |
| Helpless | ⚠ | ❌ |
| Incorporeal | ⚠ | ❌ |
| Invisible | ⚠ | ❌ |
| Nauseated | ⚠ | ❌ |
| Panicked | ⚠ | ❌ |
| Paralyzed | ⚠ | ⚠ (validated as no-physical-action in turn) |
| Petrified | ⚠ | ⚠ (validated as no-physical-action in turn) |
| Pinned | ⚠ | ❌ |
| Prone | ⚠ | ❌ (no AC modifier or attack penalty) |
| Shaken | ⚠ | ❌ |
| Sickened | ⚠ | ❌ |
| Sleeping | ⚠ | ❌ |
| Squeezing | ⚠ | ❌ |
| Stable | ⚠ | ❌ |
| Staggered | ⚠ | ⚠ (validated as single-action in turn) |
| Stunned | ⚠ | ❌ |
| Unconscious | ⚠ | ⚠ (excluded from acting) |

---

## 15. Languages (CRB)

| Language | Source |
|---|---|
| Common | universal |
| Aklo | (APG, skip) |
| Aquan | elemental plane / monsters |
| Auran | elemental plane / monsters |
| Celestial | outer planes |
| Draconic | dragons |
| Druidic | druid-only |
| Dwarven | dwarven |
| Elven | elven |
| Giant | giants |
| Gnoll | gnolls |
| Gnome | gnomish |
| Goblin | goblinoids |
| Halfling | halflings |
| Ignan | elemental plane |
| Infernal | hell |
| Orc | orcs |
| Sylvan | fey |
| Terran | elemental plane |
| Undercommon | underdark |
| Abyssal | demons |

---

## 16. Deities (CRB)

CRB describes ~20 core deities (Sarenrae, Iomedae, Erastil, Cayden Cailean,
Desna, Shelyn, Torag, Pharasma, Abadar, Asmodeus, Calistria, Gorum, Gozreh,
Lamashtu, Nethys, Norgorber, Rovagug, Urgathoa, Zon-Kuthon, Irori, Sarenrae).
None authored — used by paladin (alignment requirement), cleric (domain
selection), and players for flavor.

| Deity | Alignment | Domains |
|---|---|---|
| Sarenrae | NG | Glory, Good, Healing, Sun, Fire |
| Iomedae | LG | Glory, Good, Law, Sun, War |
| Erastil | LG | Animal, Community, Good, Law, Plant |
| Cayden Cailean | CG | Chaos, Charm, Good, Strength, Travel |
| Desna | CG | Chaos, Good, Liberation, Luck, Travel |
| Shelyn | NG | Air, Charm, Good, Luck, Protection |
| Torag | LG | Artifice, Earth, Good, Law, Protection |
| Pharasma | N | Death, Healing, Knowledge, Repose, Water |
| Abadar | LN | Earth, Law, Nobility, Protection, Travel |
| Asmodeus | LE | Evil, Fire, Law, Magic, Trickery |
| Calistria | CN | Chaos, Charm, Knowledge, Luck, Trickery |
| Gorum | CN | Chaos, Destruction, Glory, Strength, War |
| Gozreh | N | Air, Animal, Plant, Water, Weather |
| Lamashtu | CE | Chaos, Evil, Madness, Strength, Trickery |
| Nethys | N | Destruction, Knowledge, Magic, Protection, Rune |
| Norgorber | NE | Charm, Death, Evil, Knowledge, Trickery |
| Rovagug | CE | Chaos, Destruction, Evil, War, Weather |
| Urgathoa | NE | Death, Evil, Magic, Strength, War |
| Zon-Kuthon | LE | Darkness, Death, Destruction, Evil, Law |
| Irori | LN | Healing, Knowledge, Law, Rune, Strength |

---

## 17. Other Systems Touched by Character Build

### Encumbrance & carrying capacity
- ❌ Light/Medium/Heavy load by Strength
- ❌ Carry capacity multipliers by size

### Movement & speed
- ✓ Base speed by race
- ❌ Armor speed reduction (e.g., medium/heavy from 30 → 20)
- ❌ Encumbrance speed reduction
- ❌ Burrow / Climb / Fly / Swim speeds
- ❌ Maneuverability for Fly speed (clumsy/poor/average/good/perfect)

### Saves & resistances
- ✓ Fort/Ref/Will base + ability mod
- ❌ Energy resistance (acid/cold/electricity/fire/sonic), specific amounts
- ❌ Damage reduction (X/material, X/alignment, X/—)
- ❌ Spell resistance
- ❌ Immunities (fire / sleep / charm / etc.)
- ❌ Vulnerabilities

### Action types (turn slots)
- ✓ Standard, Move, Full-Round, Swift, Five-Foot Step, Free
- ⚠ Immediate action (counts against next round's swift; not yet enforced)
- ❌ Readied actions (data structure exists in Turn but no resolution)
- ❌ Delayed initiative

### Death & dying
- ⚠ HP ≤ 0 sets dying condition; ≤ -Con sets dead — currently uses -10 hard cap
- ❌ Stabilization rolls (Constitution check vs DC 10 + injuries)
- ❌ Massive damage rule (50+ dmg in one hit → Fort save or instant death)
- ❌ Coup de grace
- ❌ Raise Dead / Resurrection / True Resurrection mechanics

### Critical hits
- ✓ Threat range, confirmation roll, damage multiplier
- ❌ Precision damage (sneak attack) doesn't multiply on crit — needs separate channel

### Special qualities (creature traits)
- ❌ Scent, Tremorsense, Blindsense, Blindsight
- ❌ Regeneration (X/material)
- ❌ Fast Healing X
- ❌ Construct/Undead/Outsider type traits
- ❌ Subtypes (cold/fire/etc.)

### Encounter timing & XP
- ❌ XP awards (encounter CR vs party APL)
- ❌ Treasure rolls
- ❌ Wealth-by-level guidelines

---

## Implementation priority suggestion

If we work through this in priority of "make existing characters mechanically real," I'd order it:

1. **Wire feat effects** for the ~30 already-authored feats (Power Attack, Weapon Focus, Improved Initiative, Toughness, Dodge, +2-save trio). Most are 1-3 lines of modifier additions.
2. **Wire racial traits** (Halfling Luck +1 saves, Dwarf Hardy, Elven Immunities, Half-Orc Ferocity, etc.).
3. **Wire core class features**: Sneak Attack precision channel; Rage as buff w/ duration; Smite Evil; Fighter weapon training.
4. **Author + wire ~50 core spells** with the spell-resolution machinery (slot consumption, save DCs, SR, concentration, charm faction-flip, simple summons).
5. **Author + wire combat maneuvers** (Trip, Grapple, Disarm, Bull Rush, Sunder, Overrun) as action handlers.
6. **Expand feats** to the rest of CRB (~150 more authored).
7. **Expand classes to L20 progression**.
8. **Expand monster catalog** beyond the starter 7.
9. **Magic items** as a content+mechanic layer.
10. **Domain / bloodline / school powers** to fill out caster build space.

Each is a discrete chunk; we can tackle them in any order.
