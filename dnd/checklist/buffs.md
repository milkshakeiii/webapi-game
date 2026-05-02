# PF1 Rules Checklist — buffs

_Auto-generated from a Foundry PF1e pack snapshot. **Do not edit by hand.**_
_Items in this shard: 207._

Status legend (for the `Manual verdict:` field below):
- `[x]` verified — engine matches RAW
- `[~]` partial  — engine has some of it; gap noted
- `[-]` absent   — not in our content / engine
- `[!]` buggy    — implemented but doesn't match RAW

Update `dnd/coverage.py` with the verdict after marking a row.

---
### Mutagen, Con
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 26
**Foundry id:** `L6gBfTUHFJMiY9Uj`

> +[[2]] natural armor bonus, +[[4]] alchemical bonus to Constitution, -2 penalty to Charisma as per @UUID[Compendium.pf1.class-abilities.Item.zrTVb83VhkFnEv6G].

**Mechanical encoding:** `changes`: 3
  - `2` → `nac`  (alchemical)
  - `-2` → `cha`  (alchemical)
  - `4` → `con`  (alchemical)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mutagen, Dex
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 26
**Foundry id:** `bleCnwZmMAOu4nE4`

> +[[2]] natural armor bonus, +[[4]] alchemical bonus to Dexterity, -2 penalty to Wisdom as per @UUID[Compendium.pf1.class-abilities.Item.zrTVb83VhkFnEv6G].

**Mechanical encoding:** `changes`: 3
  - `-2` → `wis`  (alchemical)
  - `2` → `nac`  (alchemical)
  - `4` → `dex`  (alchemical)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mutagen, Str
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 26
**Foundry id:** `a3P821aUxxJbSpVV`

> +[[2]] natural armor bonus, +[[4]] alchemical bonus to Strength, -2 penalty to Intelligence as per @UUID[Compendium.pf1.class-abilities.Item.zrTVb83VhkFnEv6G].

**Mechanical encoding:** `changes`: 3
  - `4` → `str`  (alchemical)
  - `-2` → `int`  (alchemical)
  - `2` → `nac`  (alchemical)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Alchemist
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `g1c5Qbc5VpuXHPcl`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Wooden Flesh
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9494 (PZO9494) p. 26
**Foundry id:** `OdGQWPMk0TyRnFN7`

> Grants +[[2]] natural armor bonus and DR/Slashing [[@abilities.cha.mod]] as per Wooden Flesh.

**Mechanical encoding:** `changes`: 1
  - `2` → `nac`  (base)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Arcanist
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `Fc1BH1SWKUXTkllB`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Chaos Totem, Greater
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 74
**Foundry id:** `ebyFqTewZ1K54aBX`

> Grants DR [[floor(@item.level / 2)]]/lawful as per @UUID[Compendium.pf1.class-abilities.Item.3AIFigcs4uOgzDYD].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Spirit Steed
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 77
**Foundry id:** `qmrE4n5BsnLVQV10`

> Grants DR [[floor(@item.level / 2)]]/magic as per @UUID[Compendium.pf1.class-abilities.Item.VHvomvdheVblPlA8].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Rage Powers
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `G78f2ITagA42SADz`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Rage (Unchained)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Race Guide (PZO1131) p. 8
**Foundry id:** `ciAO4KwMonUzAGY0`

> Gain +[[2]] bonus to melee attack and melee damage rolls, thrown weapon damage rolls, and Will saving throws. Additionally you suffer -2 penalty to Armor Class. You also gain 2 temporary hit points per Hit Die and are unable to use various skills. 
>
> See @UUID[Compendium.pf1.class-abilities.2Az38ZPYwjYBKZd2] for more details.

**Mechanical encoding:** `changes`: 5, has `scriptCalls`
  - `-2` → `ac`  (untyped)
  - `2 + max(0, floor((@classes.barbarianUnchained.level - 2 ) / 9))` → `mwdamage`  (untyped)
  - `2 + max(0, floor((@classes.barbarianUnchained.level - 2 ) / 9))` → `mattack`  (untyped)
  - `2 + max(0, floor((@classes.barbarianUnchained.level - 2 ) / 9))` → `twdamage`  (untyped)
  - `2 + max(0, floor((@classes.barbarianUnchained.level - 2 ) / 9))` → `will`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Rage
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 32
**Foundry id:** `UgjpRD8vtiSWRxuL`

> Gain +[[4]] morale bonus to Strength and Constitution, +[[2]] morale bonus to Will saves, and -2 penalty to Armor Class as per @UUID[Compendium.pf1.class-abilities.WSqWT9ZIshtC5vlV].

**Mechanical encoding:** `changes`: 4
  - `4 + (floor((@classes.barbarian.level - 2) / 9) * 2)` → `con`  (morale)
  - `-2` → `ac`  (untyped)
  - `4 + (floor((@classes.barbarian.level - 2) / 9) * 2)` → `str`  (morale)
  - `2 + floor((@classes.barbarian.level - 2) / 9)` → `will`  (morale)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Accurate Stance
*(buff / feat)*

**Tags:** Stance Rage Power
**Prerequisites:** —
**Source:** Advanced Race Guide (PZO1131) p. 9
**Foundry id:** `CjQ4VmDIRBb3k7Dg`

> The barbarian gains a +[[1]] competence bonus on melee attack rolls and thrown weapon attack rolls. This bonus increases by 1 for every 4 levels the barbarian has.
>
> See @UUID[Compendium.pf1.class-abilities.Item.042BafLhw5SsMsg6] for more details.

**Mechanical encoding:** `changes`: 2
  - `1 + floor(@classes.barbarianUnchained.level / 4)` → `tattack`  (competence)
  - `1 + floor(@classes.barbarianUnchained.level / 4)` → `mattack`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Calm Stance
*(buff / feat)*

**Tags:** Stance Rage Power
**Prerequisites:** —
**Source:** Advanced Race Guide (PZO1131) p. 9
**Foundry id:** `o0U6E2WvMBTectrc`

> The barbarian doesn’t gain any benefits from rage other than the temporary hit points, but she doesn’t take any of the penalties from rage (including the penalty to AC and the restriction on actions she can take).
>
> See @UUID[Compendium.pf1.class-abilities.Item.8nVgKDcPUcJBCYL7] for more details.

**Mechanical encoding:** `changes`: 5
  - `- (2 + floor((@classes.barbarianUnchained.level - 2) / 9))` → `mattack`  (untyped)
  - `- (2 + floor((@classes.barbarianUnchained.level - 2) / 9))` → `mwdamage`  (untyped)
  - `2` → `ac`  (untyped)
  - `- (2 + floor((@classes.barbarianUnchained.level - 2) / 9))` → `twdamage`  (untyped)
  - `- (2 + floor((@classes.barbarianUnchained.level - 2) / 9))` → `will`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Guarded Stance
*(buff / feat)*

**Tags:** Stance Rage Power
**Prerequisites:** —
**Source:** Advanced Race Guide (PZO1131) p. 11
**Foundry id:** `UTsRSrDTUDDEvwT5`

> The barbarian can take on a more defensive posture. This grants her a +[[1]] dodge bonus to her Armor Class for the duration of her current rage. This bonus increases by 1 for every 4 levels the barbarian has.
>
> See @UUID[Compendium.pf1.class-abilities.Item.Z0EXCnJBeBUdIb4H] for more details.

**Mechanical encoding:** `changes`: 1
  - `1 + floor(@classes.barbarianUnchained.level / 4)` → `ac`  (dodge)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Knockdown Stance
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Race Guide (PZO1131) p. 11
**Foundry id:** `fqDf4Cbv8tqRbygg`

> Adds context note and action for free trip replacement.
>
> See @UUID[Compendium.pf1.class-abilities.Item.IO2EwSxZUfTuDJ9l] for more details.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Powerful Stance
*(buff / feat)*

**Tags:** Stance Rage Power
**Prerequisites:** —
**Source:** Advanced Race Guide (PZO1131) p. 11
**Foundry id:** `HC9wMz9Ko93PgB8D`

> The barbarian gains a +[[1]] bonus on melee damage rolls and thrown weapon damage rolls. This bonus increases by 1 for every 4 levels the barbarian has.
>
> See @UUID[Compendium.pf1.class-abilities.Item.uJ4WSKQo1W8GZ9vr] for more details.

**Mechanical encoding:** `changes`: 2
  - `1 + floor(@classes.barbarianUnchained.level / 4)` → `twdamage`  (untyped)
  - `1 + floor(@classes.barbarianUnchained.level / 4)` → `mwdamage`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Reckless Stance
*(buff / feat)*

**Tags:** Stance Rage Power
**Prerequisites:** —
**Source:** Advanced Race Guide (PZO1131) p. 12
**Foundry id:** `KLUCuieSvkTD4qem`

> The barbarian can focus her ferocity. She gains a +[[1]] bonus on melee damage rolls and thrown weapon damage rolls. This bonus increases by 1 for every 4 levels the barbarian has.
>
> See @UUID[Compendium.pf1.class-abilities.Item.isntpKkbAc8v2SuT] for more details.

**Mechanical encoding:** `changes`: 2
  - `- (1 + floor(@classes.barbarianUnchained.level / 4))` → `ac`  (untyped)
  - `1 + floor(@classes.barbarianUnchained.level / 4)` → `attack`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Strength Stance
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Race Guide (PZO1131) p. 12
**Foundry id:** `aqCSTZjMKDXU0DeT`

> The barbarian gains a +[[1]] competence bonus on combat maneuvers and to her CMD. These bonuses increase by 1 for every 4 levels the barbarian has. In addition, she gains a +[[8]] competence bonus on Strength checks to lift, push, bend, or break objects (this does not apply to combat maneuvers).
>
> See @UUID[Compendium.pf1.class-abilities.Item.3c9wm12qx3pWhh79] for more details.

**Mechanical encoding:** `changes`: 3
  - `1 + floor(@classes.barbarianUnchained.level / 4)` → `cmb`  (competence)
  - `1 + floor(@classes.barbarianUnchained.level / 4)` → `cmd`  (competence)
  - `8` → `strChecks`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Stances
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `XeQ6OKTiVSI4Px09`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Barbarian
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `GoxdX8voXN2V3OVY`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Inspire Competence
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 37
**Foundry id:** `ExpWHnhptAuWwAqZ`

> Gain a +[[clamp(floor((@item.level + 5) / 4), 2, 6)]] competence bonus on skill checks with a particular skill as long as you continue to hear the bard’s performance as per @UUID[Compendium.pf1.class-abilities.Item.2M56kfIOws5yYtxq].

**Mechanical encoding:** `changes`: 1
  - `clamp(floor((@item.level + 5) / 4), 2, 6)` → `skill.acr`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Inspire Courage
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 37
**Foundry id:** `3p34GJemfcLdKckV`

> You gain a morale bonus on saves vs charm and fear effects, and a competence bonus on attack rolls and weapon damage rolls as per @UUID[Compendium.pf1.class-abilities.Item.h56K6HEBOItImPPL].

**Mechanical encoding:** `changes`: 2
  - `1 + max(0, floor((@item.level + 1) / 6))` → `attack`  (competence)
  - `1 + max(0, floor((@item.level + 1) / 6))` → `wdamage`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Bard
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `XabT4ksgafPj4Gm7`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Act as One
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 35
**Foundry id:** `aS8JH3Up3T0djpua`

> Grants +[[2]] dodge bonus to AC as per @UUID[Compendium.pf1.class-abilities.Item.9BDg29hecpIqySP1].

**Mechanical encoding:** `changes`: 1
  - `2` → `ac`  (dodge)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Blaze of Glory
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9447 (PZO9447) p. 7
**Foundry id:** `qYlZuBMxxuL8g8j8`

> Grants +[[10]] feet land speed and +[[4]] on attack rolls as per @UUID[Compendium.pf1.class-abilities.Item.SUIOnBzjXUMNQcak].

**Mechanical encoding:** `changes`: 2
  - `10` → `landSpeed`  (untyped)
  - `4` → `attack`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Close at Hand
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9268 (PZO9268) p. 30
**Foundry id:** `aIQ1v9zaOYTFbBcZ`

> Grants +[[1 + max(0, floor((@item.level - 8) / 4))]] morale bonus on attack rolls, damage rolls, and saving throws as per @UUID[Compendium.pf1.class-abilities.Item.ofbPltoU3YPQXPn6].

**Mechanical encoding:** `changes`: 3
  - `1 + max(0, floor((@item.level - 8) / 4))` → `attack`  (morale)
  - `1 + max(0, floor((@item.level - 8) / 4))` → `damage`  (morale)
  - `1 + max(0, floor((@item.level - 8) / 4))` → `allSavingThrows`  (morale)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Danger Ward (Fortitude)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 64
**Foundry id:** `J197dkOWtvbSpgjF`

> Allows rerolling a fortitude save with a +4 competence bonus as per @UUID[Compendium.pf1.class-abilities.Item.15IlbKFhTTuXwPU6].

**Mechanical encoding:** has `actions`, has `scriptCalls`

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Danger Ward (Reflex)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 64
**Foundry id:** `zbwheXCZgoOYOYNm`

> Allows rerolling a reflex save with a +4 competence bonus as per @UUID[Compendium.pf1.class-abilities.Item.15IlbKFhTTuXwPU6].

**Mechanical encoding:** has `actions`, has `scriptCalls`

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Danger Ward (Will)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 64
**Foundry id:** `QkPDtDGeFcWZe6i9`

> Allows rerolling a will save with a +4 competence bonus as per @UUID[Compendium.pf1.class-abilities.Item.15IlbKFhTTuXwPU6].

**Mechanical encoding:** has `actions`, has `scriptCalls`

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### For the Faith
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 37
**Foundry id:** `Z92Q2f8oUrKW5y5M`

> [[@item.level]] morale on attack rolls as per @UUID[Compendium.pf1.class-abilities.Item.jeUsQWO39LRmFbaI].

**Mechanical encoding:** `changes`: 1
  - `@item.level` → `attack`  (morale)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### For the King
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 36
**Foundry id:** `sCy51w5LtO94euQQ`

> Grants + [[@item.level]] competence on all attack and damage rolls as per @UUID[Compendium.pf1.class-abilities.Item.cMu6HFervQ41a4lD].

**Mechanical encoding:** `changes`: 2
  - `@item.level` → `attack`  (competence)
  - `@item.level` → `damage`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Inspiring Flex
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9446 (PZO9446) p. 18
**Foundry id:** `YIXC5DZ4SvDaH9pR`

> Grants +[[4]] morale on melee attack rolls, combat maneuver checks, Fortitude saves and Strength checks as per @UUID[Compendium.pf1.class-abilities.Item.U6dAFqYDRELQROy4].

**Mechanical encoding:** `changes`: 4
  - `4` → `cmb`  (morale)
  - `4` → `fort`  (morale)
  - `4` → `strChecks`  (morale)
  - `4` → `mattack`  (morale)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Inspiring Pain
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1136 (PZO1136) p. 20
**Foundry id:** `zfVy9sBSm7rLjk5k`

> Grants +[[2]] bonus on nonlethal weapon damage roll as per @UUID[Compendium.pf1.class-abilities.Item.GFYCltmhmtqA3Kk9].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Lion's Call
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 36
**Foundry id:** `VVLBWeV17x1UtP2H`

> Grants +[[0]] competence against fear effects and +[[1]] competence on attack rolls as per @UUID[Compendium.pf1.class-abilities.Item.i7Od2w9px0gmbkjU].

**Mechanical encoding:** `changes`: 1
  - `1` → `attack`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Moment of Triumph
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Bestiary (PZO1118) p. 34
**Foundry id:** `EWifq6MrCaGH6t3a`

> Adds Charisma modifier on all ability checks, attack rolls, damage rolls, saving throws, and skill checks and AC as per @UUID[Compendium.pf1.class-abilities.Item.Js2wvAGSZ1VqO7S1].

**Mechanical encoding:** `changes`: 6 (showing first 5)
  - `@abilities.cha.mod` → `ac`  (untyped)
  - `@abilities.cha.mod` → `damage`  (untyped)
  - `@abilities.cha.mod` → `skills`  (untyped)
  - `@abilities.cha.mod` → `allChecks`  (untyped)
  - `@abilities.cha.mod` → `allSavingThrows`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Poetic Inspiration
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9491 (PZO9491) p. 14
**Foundry id:** `Ql31DWosn4CcGKew`

> Grants +[[@abilities.cha.mod]] competence on attack and weapon damage rolls as per @UUID[Compendium.pf1.class-abilities.Item.nC5At2htfNHdTSZ9].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Prepared for the Journey
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9268 (PZO9268) p. 30
**Foundry id:** `l0md6rNYbCHzDaZk`

> Grants +[[2 + max(0, floor((@item.level - 2) / 6))]] bonus to initiative, knowledge (geography), perception, stealth and survival checks as per @UUID[Compendium.pf1.class-abilities.Item.zyyB1AU3s5PAuBPU].

**Mechanical encoding:** `changes`: 5
  - `2 + max(0, floor((@item.level - 2) / 6))` → `skill.sur`  (untyped)
  - `2 + max(0, floor((@item.level - 2) / 6))` → `skill.per`  (untyped)
  - `2 + max(0, floor((@item.level - 2) / 6))` → `init`  (untyped)
  - `2 + max(0, floor((@item.level - 2) / 6))` → `skill.ste`  (untyped)
  - `2 + max(0, floor((@item.level - 2) / 6))` → `skill.kge`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Protector of the People (1 Requirement)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9488 (PZO9488) p. 15
**Foundry id:** `lEwrgzT3mgwk1X4d`

> Grants + [[@item.level]] morale bonus on saving throws as per @UUID[Compendium.pf1.class-abilities.Item.1fEKSNPwGg6hB1Ui].

**Mechanical encoding:** `changes`: 1
  - `@item.level` → `allSavingThrows`  (morale)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Protector of the People (2 Requirements)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9488 (PZO9488) p. 15
**Foundry id:** `w58wV9ft9AZUxh4O`

> Grants + [[@item.level * 2]] morale bonus on saving throws as per @UUID[Compendium.pf1.class-abilities.Item.1fEKSNPwGg6hB1Ui].

**Mechanical encoding:** `changes`: 1
  - `@item.level * 2` → `allSavingThrows`  (morale)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Rally Allies
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9482 (PZO9482) p. 24
**Foundry id:** `pF2JuGqoD67yQl4k`

> Grants +[[@item.level]] competence on weapon damage rolls as per @UUID[Compendium.pf1.class-abilities.Item.a5Hd7jgzLx85l4sC].

**Mechanical encoding:** `changes`: 1
  - `@item.level` → `wdamage`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Resist Energy
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9478 (PZO9478) p. 13
**Foundry id:** `H9Qopdm0LVhvA4Pm`

> Grants energy resistance [[floor((@item.level - 4) / 4) * 5]] to on energy type as per @UUID[Compendium.pf1.class-abilities.Item.TH51moex2K8P4UjM].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Seek Retribution
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9443 (PZO9443) p. 22
**Foundry id:** `DRHyuCVDE4XW5Ayl`

> Grants +[[@abilities.cha.mod]] competence on weapon damage rolls against oathbreaking creatures as per @UUID[Compendium.pf1.class-abilities.Item.31CnioMwm6kmFt8N].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Share the Danger
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9482 (PZO9482) p. 24
**Foundry id:** `wkVghPK4yWHkoLfh`

> Grants +[[@item.level]] competence on attack rolls and saving throws when allying samurai threatens the target as per @UUID[Compendium.pf1.class-abilities.Item.k3DBzmRSzywR0sbm].

**Mechanical encoding:** `changes`: 1
  - `max(1, @item.level)` → `ac`  (deflection)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Spell Aid
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9426 (PZO9426) p. 24
**Foundry id:** `4ox2XgPppFBnW2s9`

> [[2 + floor((@item.level - 2) / 6)]] competence on next concentration, dispel or caster level check as per @UUID[Compendium.pf1.class-abilities.Item.2U4Brc6XSYEb6Azn]

**Mechanical encoding:** `changes`: 2, has `actions`
  - `1` → `concentration`  (untyped)
  - `1` → `cl`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Stampede
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9489 (PZO9489) p. 31
**Foundry id:** `mw16hzWUcPmGkN9I`

> Grants +[[4]] bonus to ac AC per @UUID[Compendium.pf1.class-abilities.Item.EAVNzT8lSiOIgTJx].

**Mechanical encoding:** `changes`: 2
  - `4` → `ac`  (untyped)
  - `@item.level` → `damage`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Strategy (AC)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 35
**Foundry id:** `GSImk5j94ry9OZIz`

> Grants +[[2]] dodge bonus to AC as per @UUID[Compendium.pf1.class-abilities.Item.fAcozS7Vmm7xLGSX]

**Mechanical encoding:** `changes`: 1
  - `2` → `ac`  (dodge)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Strategy (Attack)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 35
**Foundry id:** `GJ4CGcbf9RW7Jlqi`

> Grants +[[2]] moral bonus to attacks as per @UUID[Compendium.pf1.class-abilities.Item.fAcozS7Vmm7xLGSX]

**Mechanical encoding:** `changes`: 1
  - `2` → `attack`  (morale)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Temporary Alliance
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9482 (PZO9482) p. 24
**Foundry id:** `OCAbaLfEP5nPn6fc`

> Grants +[[@item.level]] competence on attack rolls and saving throws when allying cavalier/samurai threatens the target as per @UUID[Compendium.pf1.class-abilities.Item.k3DBzmRSzywR0sbm].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Terrain Training
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9426 (PZO9426) p. 24
**Foundry id:** `2nOppbBQqZPcwXx5`

> Grants +[[@item.level]] competence bonus to initiative, knowledge (geography), perception and survival checks as per @UUID[Compendium.pf1.class-abilities.Item.BJbgAVT6pZhML9im].

**Mechanical encoding:** `changes`: 4
  - `@item.level` → `skill.per`  (competence)
  - `@item.level` → `init`  (competence)
  - `@item.level` → `skill.sur`  (competence)
  - `@item.level` → `skill.kge`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Way of the Samurai
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Bestiary (PZO1118) p. 21
**Foundry id:** `d9bDSB4JceMd6Uq9`

> Tracks duration of @UUID[Compendium.pf1.class-abilities.Item.xzTIam3Cx9JH5GNs].

**Mechanical encoding:** has `actions`, has `scriptCalls`

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Order Abilities
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `lacW0cStFUR5cp5M`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Cavalier/Samurai
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `J8FcqAx6BAWvmgsY`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Aura of Protection
*(buff / feat)*

**Tags:** Domain Power
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 46
**Foundry id:** `7ReQuzKvSVUtwuC9`

> Grants +[[1 + floor((@item.level-8) / 4)]] deflection bonus to AC and resistance [[5 + (floor(@item.level / 14) * 5)]] against all elements (acid, cold, electricity, fire, and sonic) as per Aura of Protection (Domain Power)

**Mechanical encoding:** `changes`: 1
  - `1 + floor((@item.level - 8) / 4)` → `ac`  (deflection)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Deflection Aura
*(buff / feat)*

**Tags:** Domain Power
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 89
**Foundry id:** `GS2jJQtdIw0TlCaD`

> Grants +[[2]] deflection bonus to AC and combat maneuver defense as per @UUID[Compendium.pf1.class-abilities.Item.yDG7xVuH7oqWS4Mt].

**Mechanical encoding:** `changes`: 2
  - `2` → `ac`  (deflection)
  - `2` → `cmd`  (deflection)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Resistant Touch
*(buff / feat)*

**Tags:** Domain Power
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 46
**Foundry id:** `4gSZu1v9lw3vAD56`

> Grants a +[[1 + floor(@item.level / 5)]] resistance bonus as per Resistant Touch

**Mechanical encoding:** `changes`: 1
  - `1 + floor(@item.unlevel / 5)` → `allSavingThrows`  (resist)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Sheltering Walls
*(buff / feat)*

**Tags:** Domain Power
**Prerequisites:** —
**Source:** PZO9460 (PZO9460) p. 18
**Foundry id:** `VUSZRkECd6Qd1jGf`

> Grants +[[2]] to AC and +[[1]] to Reflex as under the effect of Cover as per @UUID[Compendium.pf1.class-abilities.Item.jlGCqPjmgNH3lUXS].

**Mechanical encoding:** `changes`: 2
  - `2` → `ac`  (untyped)
  - `1` → `ref`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Taboo
*(buff / feat)*

**Tags:** Domain Power
**Prerequisites:** —
**Source:** PZO9443 (PZO9443) p. 17
**Foundry id:** `Bw3S5PgpZWRrUqRD`

> Applies -[[(1 + floor(@item.unlevel / 5))]] penalty to saving throws as per Taboo (Domain Power)

**Mechanical encoding:** `changes`: 1
  - `-(1 + floor(@item.level / 5))` → `allSavingThrows`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Cleric
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `pGyzJLKaPKlH2k5X`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Animal Focus (Bat)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Class Guide (PZO1129) p. 27
**Foundry id:** `dHZ25yUwzmosJZbw`

> The creature gains darkvision to a range of 60 feet. At 8th level, the range increases by 30 feet. At 15th level, the creature also gains blindsense to a range of 10 feet as per @UUID[Compendium.pf1.class-abilities.Item.4r83TfLHXrRmXtIn].

**Mechanical encoding:** `changes`: 2
  - `ifelse(lte(@item.level, 8), 30, 60)` → `sensedv`  (racial)
  - `if(gte(@item.level, 15), 10)` → `sensebse`  (racial)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Animal Focus (Bear)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Class Guide (PZO1129) p. 27
**Foundry id:** `Mgi0taTxLOPN6y2V`

> The creature gains a +[[2 + floor((@item.level - 1) / 7) * 2]] enhancement bonus to Constitution as per @UUID[Compendium.pf1.class-abilities.Item.4r83TfLHXrRmXtIn].

**Mechanical encoding:** `changes`: 1
  - `2 + floor((@item.level - 1) / 7) * 2` → `con`  (enh)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Animal Focus (Bull)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Class Guide (PZO1129) p. 27
**Foundry id:** `rjnMUgUmdMU8pQwa`

> The creature gains a +[[2 + floor((@item.level - 1) / 7) * 2]] enhancement bonus to Constitution as per @UUID[Compendium.pf1.class-abilities.Item.4r83TfLHXrRmXtIn].

**Mechanical encoding:** `changes`: 1
  - `2 + floor((@item.level - 1) / 7) * 2` → `str`  (enh)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Animal Focus (Falcon)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Class Guide (PZO1129) p. 27
**Foundry id:** `30MZFYjOgu59ZoXj`

> The creature gains a +[[4 + floor((@item.level - 1) / 7) * 2]] competence bonus to Perception as per @UUID[Compendium.pf1.class-abilities.Item.4r83TfLHXrRmXtIn].

**Mechanical encoding:** `changes`: 1
  - `4 + floor((@item.level - 1) / 7) * 2` → `skill.per`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Animal Focus (Frog)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Class Guide (PZO1129) p. 27
**Foundry id:** `Yr2fjmHuiTy4J6nC`

> The creature gains a +[[4 + floor((@item.level - 1) / 7) * 2]] competence bonus on Swim checks and on Acrobatics checks to jump as per @UUID[Compendium.pf1.class-abilities.Item.4r83TfLHXrRmXtIn].

**Mechanical encoding:** `changes`: 1
  - `4 + floor((@item.level - 1) / 7) * 2` → `skill.swm`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Animal Focus (Monkey)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Class Guide (PZO1129) p. 27
**Foundry id:** `uiV6m0dNrQRIXoqQ`

> The creature gains a +[[4 + floor((@item.level - 1) / 7) * 2]] competence bonus on Climb checks as per @UUID[Compendium.pf1.class-abilities.Item.4r83TfLHXrRmXtIn].

**Mechanical encoding:** `changes`: 1
  - `4 + floor((@item.level - 1) / 7) * 2` → `skill.clm`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Animal Focus (Mouse)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Class Guide (PZO1129) p. 28
**Foundry id:** `qAb9TshwWpr5JDB2`

> The creature gains evasion, as the rogue class feature. At 12th level, this increases to improved evasion, as the rogue advanced talent as per @UUID[Compendium.pf1.class-abilities.Item.4r83TfLHXrRmXtIn].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Animal Focus (Owl)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Class Guide (PZO1129) p. 28
**Foundry id:** `LR64SMLpzgyMNNcm`

> The creature gains a +[[4 + floor((@item.level - 1) / 7) * 2]] competence bonus to Perception as per @UUID[Compendium.pf1.class-abilities.Item.4r83TfLHXrRmXtIn].

**Mechanical encoding:** `changes`: 1
  - `4 + floor((@item.level - 1) / 7) * 2` → `skill.ste`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Animal Focus (Snake)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Class Guide (PZO1129) p. 28
**Foundry id:** `wm3VB0brsAuhua0V`

> The creature gains a +[[2 + floor((@item.level - 1) / 7) * 2]] bonus on attack rolls when making attacks of opportunity and a +[[2 + floor((@item.level - 1) / 7) * 2]] dodge bonus to AC against attacks of opportunity as per @UUID[Compendium.pf1.class-abilities.Item.4r83TfLHXrRmXtIn].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Animal Focus (Stag)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Class Guide (PZO1129) p. 28
**Foundry id:** `9LKumYEPIbzb1dQB`

> The creature gains a [[5 * (1 + gte(@item.level, 8) + if(gte(@item.level, 15), 2))]]-foot enhancement bonus to its base land speed as per @UUID[Compendium.pf1.class-abilities.Item.4r83TfLHXrRmXtIn].

**Mechanical encoding:** `changes`: 1
  - `5 * (1 + gte(@item.level, 8) + if(gte(@item.level, 15), 2))` → `landSpeed`  (enh)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Animal Focus (Tiger)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Class Guide (PZO1129) p. 28
**Foundry id:** `q59pZnNa8NoW2moc`

> The creature gains a +[[2 + floor((@item.level - 1) / 7) * 2]] enhancement bonus to Constitution as per @UUID[Compendium.pf1.class-abilities.Item.4r83TfLHXrRmXtIn].

**Mechanical encoding:** `changes`: 1
  - `2 + floor((@item.level - 1) / 7) * 2` → `dex`  (enh)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Animal Focus (Wolf)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Class Guide (PZO1129) p. 28
**Foundry id:** `mZ63Rbpnk9UCwtWN`

> The creature gains the scent ability with a range of [[10 + floor((@item.level - 1) / 7) * 10]] feet. The range doubles if the opponent is upwind, and is halved if the opponent is downwind as per @UUID[Compendium.pf1.class-abilities.Item.4r83TfLHXrRmXtIn].

**Mechanical encoding:** `changes`: 1
  - `10 + floor((@item.level - 1) / 7) * 10` → `sensesc`  (racial)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Hunter
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `Ssw2Wao6TwJ300vb`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Destruction
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 39
**Foundry id:** `gBRAvqqjrLw4Cnhm`

> Grants +[[1 + floor(@item.level / 3)]] sacred / profane bonus on all weapon damage rolls as per @UUID[Compendium.pf1.class-abilities.Item.LaSR2WkVuqgG1C6L].

**Mechanical encoding:** `changes`: 1
  - `1 + floor(@item.level / 3)` → `wdamage`  (sacred)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Healing
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 39
**Foundry id:** `hzu5SyhALN2TBoAe`

> This buff acts as a placeholder to track buff state but currently does not modify any values on the actor.
>
> Tracks Healing Judgement state.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Justice
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 39
**Foundry id:** `QAL8jtr7BkTSVpXK`

> Grants +[[1 + floor(@item.level / 5)]] sacred / profane bonus on all attack rolls which is doubled to confirm critical hits at level 10 as per @UUID[Compendium.pf1.class-abilities.Item.j6ZSm23YrshsdfBt].

**Mechanical encoding:** `changes`: 2
  - `1 + floor(@item.level / 5)` → `attack`  (sacred)
  - `if(gte(@item.level, 10), (1 + floor(@item.level / 5)) * 2)` → `critConfirm`  (sacred)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Piercing
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 39
**Foundry id:** `yqdRqkADURTHBvVH`

> Grants +[[1 + floor(@item.level / 3)]] sacred / profane bonus on concentration checks and caster level checks to overcome spell resistance as per@UUID[Compendium.pf1.class-abilities.Item.Po86Ft2nHRNpNogi].

**Mechanical encoding:** `changes`: 1
  - `1 + floor(@item.level / 3)` → `concentration`  (sacred)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Protection
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 39
**Foundry id:** `WrxSFJ9MJvFO3Mmu`

> Grants +[[1 + floor(@item.level / 5)]] sacred / profane bonus to armor class as per @UUID[Compendium.pf1.class-abilities.Item.APjE7Cvu9fQFYKca].

**Mechanical encoding:** `changes`: 1
  - `1 + floor(@item.level / 5)` → `ac`  (sacred)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Purity
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 39
**Foundry id:** `mKqlvosmPK2iAxL4`

> Grants +[[1 + floor(@item.level / 5)]] sacred / profane bonus on saving throws which is doubled against curses, diseases, and poisons at level 10 as per @UUID[Compendium.pf1.class-abilities.Item.asMZBthOLKiIF4bM].

**Mechanical encoding:** `changes`: 1
  - `1 + floor(@item.level / 5)` → `allSavingThrows`  (sacred)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Resiliency
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 39
**Foundry id:** `cA2R9j90XCY3mRvl`

> Grants DR [[1 + floor(@item.level / 5)]]/magic (or alignment at level 10) as per Resiliency.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Resistance
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 39
**Foundry id:** `W9TR1oh1KpDxOKr1`

> Grants ER [[(1 + floor(@item.level / 3)) * 2]] against one energy type as per Resistance.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Smiting
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 39
**Foundry id:** `kFYQF6YT5GIO5EdP`

> This buff acts as a placeholder to track buff state but currently does not modify any values on the actor.
>
> Tracks Smiting Judgement state.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Inquisitor
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `4THjOTxrpTjQqNiL`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Spell Deflection
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9286 (PZO9286) p. 8
**Foundry id:** `8AEPlLbeiTbQBJbV`

> Allows to track consumed spell levels via charges and duration as per Spell Deflection.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Utility Wild Talents
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `1ckPAo0nLTEdZPgk`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Kineticist
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `a9BPEnh9ilSLjqhs`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Broken Taboo
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Bestiary 4 (PZO1132) p. 30
**Foundry id:** `ueH9tRS3YLwRgJ9e`

> Applies [[-2]] penalty on attack rolls, damage rolls, ability checks, skill checks, and saving throws as per Taboo class feature.

**Mechanical encoding:** `changes`: 4
  - `-2` → `damage`  (untyped)
  - `-2` → `skills`  (untyped)
  - `-2` → `allChecks`  (untyped)
  - `-2` → `attack`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Medium
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `8SCL6FyTrBfYtua6`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Debilitating Injury (Bewildered)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Race Guide (PZO1131) p. 22
**Foundry id:** `YX0ZXFOGqZXu57AN`

> The target takes a –2 penalty to AC. The target takes an additional –[[floor((@item.level + 2) / 6) * 2]] penalty to AC against all attacks made by the rogue as per @UUID[Compendium.pf1.class-abilities.Item.nL9Ds9nflmID84vo].

**Mechanical encoding:** `changes`: 1
  - `-2` → `ac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Debilitating Injury (Disoriented)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Race Guide (PZO1131) p. 22
**Foundry id:** `3V4SKStquBCW8grU`

> The target takes a –2 penalty on attack rolls. The target takes an additional –[[floor((@item.level + 2) / 6) * 2]] penalty to attack rolls against the rogue as per @UUID[Compendium.pf1.class-abilities.Item.nL9Ds9nflmID84vo].

**Mechanical encoding:** `changes`: 1
  - `-2` → `attack`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Debilitating Injury (Hampered)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Race Guide (PZO1131) p. 22
**Foundry id:** `0Ec3mH1ddh76cvYU`

> All of the target’s speeds are reduced by half (to a minimum of 5 feet). In addition, the target cannot take a 5-foot step as per @UUID[Compendium.pf1.class-abilities.Item.nL9Ds9nflmID84vo] .

**Mechanical encoding:** `changes`: 5
  - `max(5, floor(@attributes.speed.burrow.total / 2))` → `burrowSpeed`  (untyped)
  - `max(5, floor(@attributes.speed.fly.total / 2))` → `flySpeed`  (untyped)
  - `max(5, floor(@attributes.speed.climb.total / 2))` → `climbSpeed`  (untyped)
  - `max(5, floor(@attributes.speed.land.total / 2))` → `landSpeed`  (untyped)
  - `max(5, floor(@attributes.speed.swim.total / 2))` → `swimSpeed`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Rogue
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `W0lDQynHK8L9tptK`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Dire Prophecy
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Ultimate Magic (PZO1117) p. 82
**Foundry id:** `B1lq0g41olpQMfzK`

> You suffer -4 penalty to AC, attack rolls, saves, ability checks and skill checks as per @UUID[Compendium.pf1.class-abilities.Item.KPauZdmqDDxXj6OU].

**Mechanical encoding:** `changes`: 5
  - `-4` → `ac`  (untyped)
  - `-4` → `skills`  (untyped)
  - `-4` → `allSavingThrows`  (untyped)
  - `-4` → `attack`  (untyped)
  - `-4` → `allChecks`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Evil Eye (Ability)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 66
**Foundry id:** `vRHG0qhHPsWgFkAl`

> The target takes a -[[ifelse(gte(@item.level, 8), 4, 2)]] penalty on ability checks as per @UUID[Compendium.pf1.class-abilities.Item.U4o5YunSfhiWoZi8]

**Mechanical encoding:** `changes`: 1
  - `ifelse(gte(@item.level, 8), -4, -2)` → `allChecks`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Evil Eye (AC)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 66
**Foundry id:** `5CWQRKQxsM14G93h`

> The target takes a -[[ifelse(gte(@item.level, 8), 4, 2)]] penalty on AC as per @UUID[Compendium.pf1.class-abilities.Item.U4o5YunSfhiWoZi8]

**Mechanical encoding:** `changes`: 1
  - `ifelse(gte(@item.level, 8), -4, -2)` → `ac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Evil Eye (Atk)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 66
**Foundry id:** `mDv3xY2HllJpjqe2`

> The target takes a -[[ifelse(gte(@item.level, 8), 4, 2)]] penalty on attack rolls as per @UUID[Compendium.pf1.class-abilities.Item.U4o5YunSfhiWoZi8].

**Mechanical encoding:** `changes`: 1
  - `ifelse(gte(@item.level, 8), -4, -2)` → `attack`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Evil Eye (Saves)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 66
**Foundry id:** `2Ob3MdeFHK2wLkyu`

> The target takes a -[[ifelse(gte(@item.level, 8), 4, 2)]] penalty on saving throws as per @UUID[Compendium.pf1.class-abilities.Item.U4o5YunSfhiWoZi8].

**Mechanical encoding:** `changes`: 1
  - `ifelse(gte(@item.level, 8), -4, -2)` → `allSavingThrows`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Evil Eye (Skill)
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 66
**Foundry id:** `XBjEZImaTvGXh6Gq`

> The target takes a -[[ifelse(gte(@item.level, 8), 4, 2)]] penalty on skill checks as per @UUID[Compendium.pf1.class-abilities.Item.U4o5YunSfhiWoZi8]

**Mechanical encoding:** `changes`: 1
  - `ifelse(gte(@item.level, 8), -4, -2)` → `skills`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Ward
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 67; Advanced Class Guide (PZO1129) p. 37
**Foundry id:** `e6LhyzMnHZc5Vlni`

> Gain +[[2]] deflection bonus to AC and +[[2]] resistance bonus to saving throws.
>
> This lasts until you are hit or you fail a saving throw.
>
> See @UUID[Compendium.pf1.class-abilities.Item.etzfM5q6bFFSnRjU] for more details.

**Mechanical encoding:** `changes`: 2
  - `2 + clamp(floor(@item.level / 8), 0, 2)` → `ac`  (deflection)
  - `2 + clamp(floor(@item.level / 8), 0, 2)` → `allSavingThrows`  (resist)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Witch
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `pWAnXIA75Y5ZNsCL`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Class Abilities
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `ws0RqS477A2LHCan`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Lunge
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 115, 130
**Foundry id:** `7DtG0pydiheVvIS8`

> Applies a -[[2]] penalty to your Armor Class until your next turn as per @UUID[Compendium.pf1.feats.Item.xq2TFr7bsYBBHOi5].

**Mechanical encoding:** `changes`: 1
  - `-2` → `ac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Feats
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `Rmfd3hAApWG8yfmJ`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fighting Defensively
*(buff / temp)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 184
**Foundry id:** `V8cRFtOQA6ltklEl`

> You can choose to fight defensively when attacking. If you do so, you take a –4 penalty on all attacks in a round to gain a +[[2]] dodge bonus to AC until the start of your next turn.

**Mechanical encoding:** `changes`: 2
  - `-4` → `attack`  (untyped)
  - `if(gte(@skills.acr.rank, 3), 1) + 2` → `ac`  (dodge)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Armor of the Tireless Warrior
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9053 (PZO9053) p. 60
**Foundry id:** `XYly5prMmLVsLT1l`

> Grants immunity to fatigued and exhausted for 10 minutes as per Armor of the Tireless Warrior

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Daikyu of Commanding Presence
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9053 (PZO9053) p. 60
**Foundry id:** `lnC5Qmk5FwJvFjvE`

> Grants +[[2]] morale bonus on saves against fear and +[[1]] morale on attack rolls when charging.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Karyukai Tea Set
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9053 (PZO9053) p. 60
**Foundry id:** `jcwfjt5FwoJcMlyL`

> gains a +[[4]] morale bonus on saving throws against poison and fear effects for 12 hours as per @UUID[Compendium.pf1.items.Item.sIXmHL2dR2cQpA3Z].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Otherworldly Kimono
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9054 (PZO9054) p. 60; Bestiary 3 (PZO1123) p. 216
**Foundry id:** `Cl3NcY8raqcmeP7x`

> Grants +[[6]] resistance to saves and +[[2]] to Caster Level checks as long as someone is trapped inside the Kimono as per @UUID[Compendium.pf1.buffs.Item.Cl3NcY8raqcmeP7x].

**Mechanical encoding:** `changes`: 2
  - `6` → `allSavingThrows`  (resist)
  - `2` → `cl`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Seishinru, Spirit Elixir
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9054 (PZO9054) p. 61
**Foundry id:** `FzUOIQgvjpzeNnnt`

> Tracks duration and allows heal when dropped to 0 HP as per @UUID[Compendium.pf1.items.Item.z1Wf1DqtJQoVzbI9].

**Mechanical encoding:** has `actions`

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Sunblock Kohl
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1138 (PZO1138) p. 15
**Foundry id:** `Uc5GpPwgJcxwfnVa`

> Grants +[[2]] circumstance bonus on saves against light-based effects that would dazzle or blind as per @UUID[Compendium.pf1.items.Item.Pg5aON2QSqZB9aYj]

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Chameleon Suit
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 30
**Foundry id:** `0MmlqFG4XodHOIzn`

> +[[10]] competence bonus on Stealth checks as per @UUID[Compendium.pf1.technology.Item.Nnrom1FPNcjBJRK8].

**Mechanical encoding:** `changes`: 1
  - `10` → `skill.ste`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Filter Mask
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 44
**Foundry id:** `EaNmiARTiepLXfcV`

> Adds context note that target is immune to inhaled toxins or diseases as per @UUID[Compendium.pf1.technology.Item.3SHwrxfV7GG51ajY].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Force Field
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 45
**Foundry id:** `EDreDkg4ESQIwmEd`

> Grants Temporary HP as per Force Field.

**Mechanical encoding:** has `scriptCalls`

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Hard Light Shield
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 30
**Foundry id:** `0AfEoAsDnhvMUW2D`

> +[[2]] shield AC [force effect] as per @UUID[Compendium.pf1.technology.Item.alQVMlHc89hMxK2M].

**Mechanical encoding:** `changes`: 1
  - `2` → `sac`  (base)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Jetpack
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 48
**Foundry id:** `aRpdBq0hSvter9wi`

> Grants a fly speed of 60 feet as per @UUID[Compendium.pf1.technology.Item.4FRBfHoD1W9SsrDr].

**Mechanical encoding:** `changes`: 1
  - `60` → `flySpeed`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Magboots
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 49
**Foundry id:** `eKiKTrSBNLubVI6g`

> +[[10]] circumstance bonus while climbing metal surfaces as per @UUID[Compendium.pf1.technology.Item.nK3XfCurRf9nRZiD].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Neraplast Armor
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9085 (PZO9085) p. 60
**Foundry id:** `AclErIDcanB7Kd8D`

> +[[3]] competence bonus on Stealth checks in current terrain as per @UUID[Compendium.pf1.technology.Item.tYUaP6Yx45ekrOdR].

**Mechanical encoding:** `changes`: 1
  - `3` → `skill.ste`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Powered Armor
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 61
**Foundry id:** `iy10UP3d0lEgwy2i`

> Grants:
>
> - +[[2]] to strength checks
> - +[[6]] enh. to strength
> - +[[6]] enh. to dexterity
> - +[[10]] ft. land speed
> - 20 ft. fly speed
>
> See @UUID[Compendium.pf1.technology.Item.eecEg8w7FECEclV5] for more details.

**Mechanical encoding:** `changes`: 5
  - `2` → `strChecks`  (circumstance)
  - `20` → `flySpeed`  (untyped)
  - `6` → `str`  (enh)
  - `6` → `dex`  (enh)
  - `10` → `landSpeed`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Scatterlight suit
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 30
**Foundry id:** `pDKUOiA1UuKAoAX5`

> Grants touch AC against beam weapons and rays as per various @UUID[Compendium.pf1.technology.Item.gTyNHqZf2jkmtTbC].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Veemod (Black)
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 53
**Foundry id:** `G4KDVMpA5nH0r9sF`

> Grants +[[2]] competence bonus on Perception checks while active as per @UUID[Compendium.pf1.technology.Item.0BtaS9u6bxDBaKhH] with @UUID[Compendium.pf1.technology.Item.jhIfmOlvPbwZwCq1].

**Mechanical encoding:** `changes`: 1
  - `10` → `skill.per`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Veemod (Blue)
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 53
**Foundry id:** `8e8Iqdi721djMcSi`

> Grants all-around vision (cannot be flanked) while active as per @UUID[Compendium.pf1.technology.Item.0BtaS9u6bxDBaKhH] with @UUID[Compendium.pf1.technology.Item.vbJhd1aeLHgPsA6e].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Veemod (Brown)
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 53
**Foundry id:** `64LMZn1hx4DeI08O`

> Grants +[[1]] circumstance bonus on all saving throws against bright light effects that cause dazzling or blindness while active as per @UUID[Compendium.pf1.technology.Item.0BtaS9u6bxDBaKhH] with @UUID[Compendium.pf1.technology.Item.jJfwLVduz8FtcgEg].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Veemod (Gray)
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 53
**Foundry id:** `l9l2uKTWEAuTqXVq`

> Grants Low-Light Vision while active as per @UUID[Compendium.pf1.technology.Item.0BtaS9u6bxDBaKhH] with @UUID[Compendium.pf1.technology.Item.djUaPaLmCemzz8eu].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Veemod (Green)
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 53
**Foundry id:** `1MspZVYeg3IMlGVL`

> Grants +[[10]] competence bonus on Perception checks while active as per @UUID[Compendium.pf1.technology.Item.0BtaS9u6bxDBaKhH] with @UUID[Compendium.pf1.technology.Item.9dvLuZUA2Wy1TBht].

**Mechanical encoding:** `changes`: 1
  - `10` → `skill.per`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Veemod (Orange)
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 53
**Foundry id:** `YUrObSwqLffrici4`

> Grants see in darkness while active as per @UUID[Compendium.pf1.technology.Item.0BtaS9u6bxDBaKhH] with @UUID[Compendium.pf1.technology.Item.eyohSXJlccmDl3Ve].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Veemod (Powered Armor)
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 61
**Foundry id:** `WRwcMIspQq9acUQW`

> Grants +[[10]] competence bonus on Perception checks, Low-Light Vision and Darkvision 120 ft. while active as per @UUID[Compendium.pf1.technology.Item.eecEg8w7FECEclV5].

**Mechanical encoding:** `changes`: 2
  - `120` → `sensedv`  (untyped)
  - `5` → `skill.per`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Veemod (Prismatic)
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 53
**Foundry id:** `pbyW9fpqSA3qAwmI`

> Grants X-ray vision while active as per @UUID[Compendium.pf1.technology.Item.0BtaS9u6bxDBaKhH] with @UUID[Compendium.pf1.technology.Item.s7otjXVeYmKuS1ra].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Veemod (Red)
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 53
**Foundry id:** `4pD4QNKhhbbGuY6i`

> Grants Darkvision 60 ft. while active as per @UUID[Compendium.pf1.technology.Item.0BtaS9u6bxDBaKhH] with @UUID[Compendium.pf1.technology.Item.dNF5qq8D1cSJHsEA].

**Mechanical encoding:** `changes`: 1
  - `60` → `sensedv`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Veemod (White)
*(buff / item)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 53
**Foundry id:** `FA4nPvdBteR2pzqK`

> Grants +[[5]] competence bonus on Perception checks while active as per @UUID[Compendium.pf1.technology.Item.0BtaS9u6bxDBaKhH] with @UUID[Compendium.pf1.technology.Item.CgwAhfGBEFSqA9Lo].

**Mechanical encoding:** `changes`: 1
  - `5` → `skill.per`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Technology
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `HKTsCi1OUug346MZ`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Items
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `qSOEcB1IUucbWDCA`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Elemental Stance
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Race Guide (PZO1131) p. 10
**Foundry id:** `v9JaHLaVkP9O36TS`

> This buff acts as a placeholder to track buff state but currently does not modify any values on the actor.
>
> See @UUID[Compendium.pf1.class-abilities.Item.EKF5SHvuXhOjf2K6] for more details.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Regenerative Stance
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Race Guide (PZO1131) p. 12
**Foundry id:** `HdNb6j7U9qA2tnr1`

> This buff acts as a placeholder to track buff state but currently does not modify any values on the actor.
>
> See @UUID[Compendium.pf1.class-abilities.Item.3wRZrnb7itCksfhP] for more details.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Taunting Stance
*(buff / feat)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Race Guide (PZO1131) p. 12
**Foundry id:** `43eVSSa6rSTl7ieD`

> This buff acts as a placeholder to track buff state but currently does not modify any values on the actor.
>
> See @UUID[Compendium.pf1.class-abilities.Item.uAI3k87VtkTt8hcw] for more details.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Placeholder Buffs
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `H4f7Rs5PFd3IA3ey`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Acute Senses
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Ultimate Magic (PZO1117) p. 205
**Foundry id:** `3cimRYgdw7AiOVci`

> You gain a +[[min(30, (10 + (floor(@item.level / 8) * 10)))]] enhancement bonus on Perception checks as per @UUID[Compendium.pf1.spells.Item.f9adpo6szijchpva].

**Mechanical encoding:** `changes`: 1
  - `min(30, (10 + (floor(@item.level / 8) * 10)))` → `skill.per`  (enh)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Age Resistance, Greater
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Ultimate Magic (PZO1117) p. 205
**Foundry id:** `U067K8fH1HcnJhI1`

> You ignore the physical detriments of being venerable, old or middle-aged as per @UUID[Compendium.pf1.spells.Item.eqrqv2ofspk574d3].

**Mechanical encoding:** `changes`: 3
  - `min(@abilities.dex.base, lookup(@ageCategory.physical, 0, 0, 1, 3, 6))` → `dex`  (untyped)
  - `min(@abilities.str.base, lookup(@ageCategory.physical, 0, 0, 1, 3, 6))` → `str`  (untyped)
  - `min(@abilities.con.base, lookup(@ageCategory.physical, 0, 0, 1, 3, 6))` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Age Resistance, Lesser
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Ultimate Magic (PZO1117) p. 205
**Foundry id:** `8MI2BpO4ewblrCvp`

> You ignore the physical detriments of being middle-aged as per @UUID[Compendium.pf1.spells.Item.li8zwqjorsww6o82].

**Mechanical encoding:** `changes`: 3
  - `min(@abilities.dex.base, lookup(@ageCategory.physical, 0, 0, 1, 1, 1))` → `dex`  (untyped)
  - `min(@abilities.con.base, lookup(@ageCategory.physical, 0, 0, 1, 1, 1))` → `con`  (untyped)
  - `min(@abilities.str.base, lookup(@ageCategory.physical, 0, 0, 1, 1, 1))` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Age Resistance
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Ultimate Magic (PZO1117) p. 205
**Foundry id:** `6PwPlGZVTqg3VUEd`

> You ignore the physical detriments of being old or middle-aged as per @UUID[Compendium.pf1.spells.Item.li8zwqjorsww6o82].

**Mechanical encoding:** `changes`: 3
  - `min(@abilities.con.base, lookup(@ageCategory.physical, 0, 0, 1, 3, 3))` → `con`  (untyped)
  - `min(@abilities.str.base, lookup(@ageCategory.physical, 0, 0, 1, 3, 3))` → `str`  (untyped)
  - `min(@abilities.dex.base, lookup(@ageCategory.physical, 0, 0, 1, 3, 3))` → `dex`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Aid
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 239
**Foundry id:** `qmwVJUZ7ZuvF3tAB`

> You have a +[[1]] morale bonus to attack rolls and saves against fear effects as per @UUID[Compendium.pf1.spells.Item.ibk7jrc5rwubpia6] spell.

**Mechanical encoding:** `changes`: 1
  - `1` → `attack`  (morale)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Angelic Aspect, Greater
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9431 (PZO9431) p. 28
**Foundry id:** `wgnn6S8tN2o5lYtM`

> Grants low-light vision; darkvision 60 feet; DR 10/evil; immunity to acid, cold, and petrification; resistance to electricity 10 and fire 10; a +[[4]] racial bonus on saves against poison; and protective aura and truespeech as supernatural abilities for the duration of the spell. Also, your wings give you a fly speed of 60 feet with good maneuverability.
>
> Protective aura provides a +[[4]] deflection bonus to AC and a +[[4]] resistance bonus on saving throws against attacks made or effects created by evil creatures to anyone within 20 feet. Otherwise, it functions as a magic circle against evil and a lesser globe of invulnerability, both with a radius of 20 feet.
>
> Truespeech allows you to speak with any creature that has a language, as though using the tongues spell as per @UUID[Compendium.pf1.spells.Item.ujykn701inq3hm2n].

**Mechanical encoding:** `changes`: 2
  - `60` → `flySpeed`  (untyped)
  - `60` → `sensedv`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Angelic Aspect, Lesser
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9431 (PZO9431) p. 28
**Foundry id:** `SQNQcS6VOXlF7vJx`

> Grants low-light vision, resistance to acid 5, resistance to cold 5, and the benefits of Protection from Evil as per @UUID[Compendium.pf1.spells.Item.4ratngmltr3z4om5].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Angelic Aspect
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9431 (PZO9431) p. 28
**Foundry id:** `vIB8zWUZ11j4OFKS`

> Grants low-light vision, darkvision of 60 feet, resistance to acid 10, resistance to cold 10, DR 5/evil, and fly speed of 30 feet with average maneuverability. In addition, your natural weapons and any weapons you wield are considered good-aligned for the purpose of overcoming damage reduction as per @UUID[Compendium.pf1.spells.Item.8jrtvmhydudy7fks].

**Mechanical encoding:** `changes`: 2
  - `30` → `flySpeed`  (untyped)
  - `60` → `sensedv`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Ant Haul
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 201
**Foundry id:** `CgyclqlZAD1HCtjv`

> Triples the target's carrying capacity as per @Compendium[pf1.spells.ngcx59msygjom4h2].

**Mechanical encoding:** `changes`: 1
  - `2` → `carryMult`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Ape Walk
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9412 (PZO9412) p. 28
**Foundry id:** `klGH5FlCy3d7lydy`

> Grants climb speed of 30 feet as per @UUID[Compendium.pf1.spells.Item.p6irfohhgss1iod5].

**Mechanical encoding:** `changes`: 1
  - `30` → `climbSpeed`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Bane
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 346
**Foundry id:** `D2huasedfGMSetP7`

> You take a -1 penalty on attack rolls and saving throws vs fear effects as per @UUID[Compendium.pf1.spells.Item.3etxlex8u32g0hrx] spell.

**Mechanical encoding:** `changes`: 1
  - `-1` → `attack`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Barkskin
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 246
**Foundry id:** `kG8EriOOSJmDmYZd`

> Your skin is toughened, granting you an enhancement bonus to your natural armor as per the @UUID[Compendium.pf1.spells.Item.la7kuehewu85ybnt] spell.

**Mechanical encoding:** `changes`: 1
  - `clamp(2 + floor((@item.level - 3) / 3), 2, 5)` → `nac`  (enh)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Bear's Endurance
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 246, 247
**Foundry id:** `lV9zpEnZrArmfEFZ`

> The subject has a +[[4]] enhancement bonus to Constitution as per @UUID[Compendium.pf1.spells.Item.usdv1eqvibmxun6x] spell.

**Mechanical encoding:** `changes`: 1
  - `4` → `con`  (enh)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Bless
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 249
**Foundry id:** `QYVZS8MfOKzjpCm1`

> You have a +[[1]] morale bonus to attack rolls and saves against fear effects as per @UUID[Compendium.pf1.spells.Item.wa0zb2pncesmm9lz] spell.

**Mechanical encoding:** `changes`: 1
  - `1` → `attack`  (morale)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Blessing of the Mole
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Ultimate Magic (PZO1117) p. 208
**Foundry id:** `KkpKycN7WMwnjlxU`

> Grants darkvision 30 feet and a +[[2]] competence bonus on Stealth as per @UUID[Compendium.pf1.spells.Item.mnsqk035k4hr8vjs] spell.

**Mechanical encoding:** `changes`: 2
  - `30` → `sensedv`  (untyped)
  - `2` → `skill.ste`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Blood Rage (Spell)
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9413 (PZO9413) p. 28
**Foundry id:** `Rh3wrAV3ZfgSviyN`

> The subject has a bonus to Strength and malus to AC based on it's current hp as per @UUID[Compendium.pf1.spells.Item.g09p4w3w8enp5tki] spell.

**Mechanical encoding:** `changes`: 2
  - `max(-5, ceil(min(0, (@attributes.hp.value - @item.uses.value) / 5)))` → `ac`  (untyped)
  - `min(10, floor(max(0, (@item.uses.value - @attributes.hp.value)) / 5) * 2)` → `str`  (morale)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Bull's Strength
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 251
**Foundry id:** `ClOy4KHJFDdt0ALh`

> The subject has a +[[4]] enhancement bonus to Strength as per @UUID[Compendium.pf1.spells.Item.05i5rxwim12hwktu].

**Mechanical encoding:** `changes`: 1
  - `4` → `str`  (enh)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Burst of Glory
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9267 (PZO9267) p. 230; PZO9202 (PZO9202) p. 21
**Foundry id:** `EmavEsO0Mv42N03v`

> You gain a +[[1]] sacred bonus on attack rolls and saves against fear effects, plus [[@item.level]] temporary hit point as per @UUID[Compendium.pf1.spells.Item.8wspht4k8tiugz6u].

**Mechanical encoding:** `changes`: 1, has `scriptCalls`
  - `1` → `attack`  (sacred)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Cat's Grace
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 252
**Foundry id:** `dVqLY99ECYnLeoB5`

> The subject has a +[[4]] enhancement bonus to Dexterity as per @UUID[Compendium.pf1.spells.Item.ns8jbp0ilbvbvuif] spell.

**Mechanical encoding:** `changes`: 1
  - `4` → `dex`  (enh)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Certain Grip
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Bestiary (PZO1118) p. 225
**Foundry id:** `iYm4uOJ9j9kv5IiM`

> Grants a +[[4]] competence bonus on Climb checks, on Acrobatics checks to balance, and to CMD against bull rush, drag, reposition, and trip attempts. While affected by this spell, the target is also immune to the disarm combat maneuver as per @UUID[Compendium.pf1.spells.Item.lmnwhrqgxf9cm9jq].

**Mechanical encoding:** `changes`: 1
  - `4` → `skill.clm`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Darkvision, Greater
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Ultimate Magic (PZO1117) p. 216
**Foundry id:** `IwthEw2sCUq4GfxY`

> Grants darkvision 120 ft. for 1 Hour per item level as per @UUID[Compendium.pf1.spells.Item.nntvnla4qnawr0xn] spell.

**Mechanical encoding:** `changes`: 1
  - `120` → `sensedv`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Darkvision
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 264
**Foundry id:** `fKqcMkjlkUL70WJ0`

> Grants darkvision 60 ft. for 1 Hour per item level as per @UUID[Compendium.pf1.spells.Item.mz9yr5yhr0f3oqtp] spell.

**Mechanical encoding:** `changes`: 1
  - `60` → `sensedv`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Deadeye's Lore
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Bestiary (PZO1118) p. 226; PZO9416 (PZO9416) p. 28
**Foundry id:** `l42Gtrj8QGjdyRfd`

> You gain a +[[4]] sacred bonus on all Survival checks for the duration of the spell, and you do not have to move at half your speed while traveling through the wilderness or while tracking as per @UUID[Compendium.pf1.spells.Item.ilcdn4jmdj3g0wac].

**Mechanical encoding:** `changes`: 1
  - `4` → `skill.sur`  (sacred)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Death Ward
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 264
**Foundry id:** `rYSQfpzeKIfUOR1G`

> Grants +[[4]] morale bonus on saves against all death spells and magical death effects. You are granted a save to negate such effects even if one is not normally allowed. You are immune to energy drain and any negative energy effects, including channeled negative energy as per @UUID[Compendium.pf1.spells.Item.e0rlki4hwu76l5ya].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Delay Poison
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 265
**Foundry id:** `FxGQVAP3ep7xiAC4`

> Grants immunity to poison as per @UUID[Compendium.pf1.spells.Item.l7e01shgg8c44zfg].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Divine Favor
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 273
**Foundry id:** `3czZB6whbQo9WhxR`

> You have a luck bonus to attack rolls and weapon damage rolls as per @UUID[Compendium.pf1.spells.Item.21bxbzdaawjrnvyo] spell.

**Mechanical encoding:** `changes`: 2
  - `clamp(floor(@item.level / 3), 1, 3)` → `wdamage`  (luck)
  - `clamp(floor(@item.level / 3), 1, 3)` → `attack`  (luck)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Divine Power
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 273
**Foundry id:** `0hRYCva2hdwUNFh6`

> You gain a +[[(min(6, floor(@item.level / 3)))]] luck bonus on attack rolls, weapon damage rolls, Strength checks, and Strength-based skill checks and also gains [[@item.level]] temp. HP as per @UUID[Compendium.pf1.spells.Item.0yvwyclhkf76veo1].

**Mechanical encoding:** `changes`: 4, has `scriptCalls`
  - `(min(6, floor(@item.level / 3)))` → `attack`  (luck)
  - `(min(6, floor(@item.level / 3)))` → `strChecks`  (luck)
  - `(min(6, floor(@item.level / 3)))` → `strSkills`  (luck)
  - `(min(6, floor(@item.level / 3)))` → `wdamage`  (luck)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Divine Transfer
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 216
**Foundry id:** `l6s6haw5PHdNi9YD`

> Grants DR/Evil as per @UUID[Compendium.pf1.spells.Item.dq65gtj0phmasj87].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Eagle's Splendor
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 275
**Foundry id:** `KsgdOd5vzGu7UDBe`

> The subject has a +[[4]] enhancement bonus to Charisma as per @UUID[Compendium.pf1.spells.Item.d4oubr5bdoo8w1ev] spell.

**Mechanical encoding:** `changes`: 1
  - `4` → `cha`  (enh)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Endure Elements
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 277
**Foundry id:** `N9I7rqVRxAi96UBn`

> Tracks duration of the spell Endure Elements.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Enlarge Person
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 277, 278
**Foundry id:** `1ovEWVzSp5yZXeVm`

> Adjusts:
>
> - +[[2]] Size bonus to Strength
> - -2 Size penalty to Dexterity
> - +[[1]] Size
>
> Includes carry capacity adjustments partially accounting for your gear not changing in size.
>
> See @UUID[Compendium.pf1.spells.jnlr9cuepka1l26e] for more details.

**Mechanical encoding:** `changes`: 5
  - `-2` → `dex`  (size)
  - `-2` → `carryStr`  (untyped)
  - `-0.5` → `carryMult`  (untyped)
  - `1` → `size`  (untyped)
  - `2` → `str`  (size)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fly
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 284
**Foundry id:** `sfmKrukx8vFoXLBf`

> Grants fly speed as per @UUID[Compendium.pf1.spells.Item.7d6sv5ecvi7kho3m] spell.

**Mechanical encoding:** `changes`: 2
  - `floor(@item.level / 2)` → `skill.fly`  (untyped)
  - `ifelse(or(gt(@attributes.encumbrance.level, 0), gt(@armor.type, 1)), 40, 60)` → `flySpeed`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fox's Cunning
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 286
**Foundry id:** `1z7euBqoJ1ZDCRW4`

> The subject has a +[[4]] enhancement bonus to Intelligence as per @UUID[Compendium.pf1.spells.Item.743anqr1ahefv8zd] spell.

**Mechanical encoding:** `changes`: 1
  - `4` → `int`  (enh)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Freedom of Movement
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 287
**Foundry id:** `wdZ9dbMnPF0nlMoK`

> Grants immunity to paralysed condition as per @UUID[Compendium.pf1.spells.Item.lvzq2mwkqmozolpl].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Haste
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 293
**Foundry id:** `NWImcWGTjCtw1Zf0`

> When making a full attack action, you may make one extra attack with one natural or manufactured weapon at your highest base attack bonus. This effect is not cumulative with similar effects, such as that provided by a *speed* weapon.
>
> You also gain a +[[1]] bonus on attack rolls, dodge AC and Reflex saves.
>
> All your modes of movement (including land, fly, burrow, climb and swim) increase by 30ft, to a maximum of twice your normal speed using that form of movement. This increase counts as an enhancement bonus, and it affects the creature’s jumping distance as normal for increased speed.
>
> See @UUID[Compendium.pf1.spells.Item.s9amdo5398alb5p0] for more details.

**Mechanical encoding:** `changes`: 8 (showing first 5)
  - `min(@attributes.speed.burrow.base, 30)` → `burrowSpeed`  (enh)
  - `min(@attributes.speed.climb.base, 30)` → `climbSpeed`  (enh)
  - `1` → `ac`  (haste)
  - `1` → `attack`  (haste)
  - `min(@attributes.speed.swim.base, 30)` → `swimSpeed`  (enh)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Heightened Awareness
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Class Guide (PZO1129) p. 183
**Foundry id:** `ora1YS0VXYjJIQkh`

> Grants +[[2]] competence bonus on Perception checks and on all Knowledge checks that you are trained in as per @UUID[Compendium.pf1.spells.Item.r8bhei88g6h26fp0].

**Mechanical encoding:** `changes`: 11 (showing first 5), has `actions`
  - `if(@skills.kno.rank, 2)` → `skill.kno`  (competence)
  - `if(@skills.kge.rank, 2)` → `skill.kge`  (competence)
  - `if(@skills.kpl.rank, 2)` → `skill.kpl`  (competence)
  - `if(@skills.klo.rank, 2)` → `skill.klo`  (competence)
  - `if(@skills.kna.rank, 2)` → `skill.kna`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Heroism, Greater
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 295
**Foundry id:** `T2j3SnpatLbS32O1`

> You gain a +[[4]] morale bonus on attack rolls, saves, and skill checks as per @UUID[Compendium.pf1.spells.Item.z0duc2v2n3ioynta].

**Mechanical encoding:** `changes`: 3
  - `4` → `attack`  (morale)
  - `4` → `allSavingThrows`  (morale)
  - `4` → `skills`  (morale)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Heroism
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 295
**Foundry id:** `ulvEcJsFba6Fg4g9`

> You gain a +[[2]] morale bonus on attack rolls, saves, and skill checks as per @UUID[Compendium.pf1.spells.Item.vqfrp8t0c1lw1jna].

**Mechanical encoding:** `changes`: 3
  - `2` → `attack`  (morale)
  - `2` → `allSavingThrows`  (morale)
  - `2` → `skills`  (morale)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Invisibility, Greater
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 301
**Foundry id:** `a7hnzLkLPrqRti14`

> Grants invisibility as per @UUID[Compendium.pf1.spells.Item.cxgi0ub77t6aink1].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Invisibility
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 301
**Foundry id:** `sIogsaNU2T2Qe3l9`

> Grants invisibility as per @UUID[Compendium.pf1.spells.Item.oylikodnyku2zewu].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Jump
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 303
**Foundry id:** `AgqXOB4RbAi5QHnR`

> Grants +[[clamp((floor((@item.level + 3) / 4) * 10), 10, 30)]] enhancement bonus on Acrobatics checks made to attempt high jumps or long jumps as per @UUID[Compendium.pf1.spells.Item.ns2zo6qgd9co02uf].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Keen Senses
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 230
**Foundry id:** `F9HgMbfh0AHe4zCP`

> Grants +[[2]] competence bonus on Perception checks and low-light vision as per @UUID[Compendium.pf1.spells.Item.54x9nw6ni4rpphcn].

**Mechanical encoding:** `changes`: 1
  - `2` → `skill.per`  (competence)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Long Arm
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Class Guide (PZO1129) p. 186
**Foundry id:** `GLQo0kv6iZEvBGto`

> Increases natural reach by 5 feet as per @UUID[Compendium.pf1.spells.Item.steozrynqopyxiua] spell.

**Mechanical encoding:** `changes`: 1
  - `5` → `reach`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Longstrider, Greater
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Class Guide (PZO1129) p. 186
**Foundry id:** `aXNBwNX1qgp8GqzM`

> Grants +[[20]]-foot enhancement bonus to your base speed and a +[[10]]-foot enhancement bonus to your other modes of movement (burrow, climb, fly, swim, and so on) as per @UUID[Compendium.pf1.spells.Item.k78qs00yp7uybprw].

**Mechanical encoding:** `changes`: 5
  - `if(@attributes.speed.fly.total, 10)` → `flySpeed`  (enh)
  - `20` → `landSpeed`  (enh)
  - `if(@attributes.speed.climb.total, 10)` → `climbSpeed`  (enh)
  - `if(@attributes.speed.swim.total, 10)` → `swimSpeed`  (enh)
  - `if(@attributes.speed.burrow.total, 10)` → `burrowSpeed`  (enh)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Longstrider
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 305
**Foundry id:** `qmHamauveVs3q6F0`

> Grants +[[10]] foot enhancement bonus to your base speed as per @UUID[Compendium.pf1.spells.Item.hosf489xyoexmp57].

**Mechanical encoding:** `changes`: 1
  - `10` → `landSpeed`  (enh)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mage Armor
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 306
**Foundry id:** `IlO0CNpAIKZtNYu8`

> Grants +[[4]] armor bonus to AC which also applies against incorporeal touch attacks as per @UUID[Compendium.pf1.spells.Item.ucc0a31d1y86oleh].

**Mechanical encoding:** `changes`: 1
  - `4` → `aac`  (base)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Magic Vestment
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 310
**Foundry id:** `Qqo3DLdlbnXhXe7G`

> Grants an enhancement bonus of +[[min(5, floor(@item.level / 4))]] to your armor class or shield ac as per @UUID[Compendium.pf1.spells.Item.73han2zqxg59u18g].

**Mechanical encoding:** `changes`: 1
  - `min(5, floor(@item.level / 4))` → `aac`  (enh)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Monkey Fish
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Class Guide (PZO1129) p. 188
**Foundry id:** `DbgVlKyMojx8L3gR`

> Grants 10 foot climb speed and swim speed as per @UUID[Compendium.pf1.spells.Item.wijuvnfmtmq83jef]. This buff has no effect if you are wearing medium or heavy armor or carrying a medium or heavy load.

**Mechanical encoding:** `changes`: 2
  - `if(and(lt(@armor.type, 2), lt(@attributes.encumbrance.level, 1)), 10)` → `climbSpeed`  (racial)
  - `if(and(lt(@armor.type, 2), lt(@attributes.encumbrance.level, 1)), 10)` → `swimSpeed`  (racial)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Owl's Wisdom
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 318
**Foundry id:** `1W9YmqCqawLmMXmf`

> The subject has a +[[4]] enhancement bonus to Wisdom as per @UUID[Compendium.pf1.spells.Item.b9ggsagifzk4fwut] spell.

**Mechanical encoding:** `changes`: 1
  - `4` → `wis`  (enh)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Prayer (Negative)
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 324
**Foundry id:** `MFogxSkB5dBmUI5i`

> You have a -1 luck penalty on attack rolls, weapon damage rolls, saves and skill checks as per @UUID[Compendium.pf1.spells.Item.hu8179fdqfkl0bqj].

**Mechanical encoding:** `changes`: 4
  - `-1` → `allSavingThrows`  (untyped)
  - `-1` → `skills`  (untyped)
  - `-1` → `attack`  (untyped)
  - `-1` → `wdamage`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Prayer (Positive)
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 324
**Foundry id:** `kXvipUvebDtVfxEv`

> You have a +[[1]] luck bonus on attack rolls, weapon damage rolls, saves and skill checks as per @UUID[Compendium.pf1.spells.Item.hu8179fdqfkl0bqj].

**Mechanical encoding:** `changes`: 4
  - `1` → `allSavingThrows`  (luck)
  - `1` → `wdamage`  (luck)
  - `1` → `attack`  (luck)
  - `1` → `skills`  (luck)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Protection From Energy
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 327
**Foundry id:** `p2JgcKLVXMawO3uL`

> Grants [[min(120, @item.level * 10)]] charges to track the amout of energy damage that can be absorbed as per @UUID[Compendium.pf1.spells.Item.1vh2ewwvzvxunoxk].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Rage (Spell)
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 329
**Foundry id:** `nRHD11ZwDWlRyT8c`

> Grants a +[[2]] morale bonus to Strength and Constitution, a +[[1]] morale bonus on Will saves, and a -2 penalty to AC as per Rage (Spell).

**Mechanical encoding:** `changes`: 4
  - `-2` → `ac`  (untyped)
  - `2` → `con`  (morale)
  - `2` → `str`  (morale)
  - `1` → `will`  (morale)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Reduce Person
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 330, 331
**Foundry id:** `Z140LMTwEKHQXdW5`

> Adjusts:
>
> - -2 Size penalty to Strength
> - +[[2]] Size bonus to Dexterity
> - -1 Size
>
> Included carry capacity adjustments partially account for your gear not changing in size.
>
> See @UUID[Compendium.pf1.spells.2y9e1l6zso9tdg0a] spell for more details.

**Mechanical encoding:** `changes`: 5
  - `2` → `dex`  (size)
  - `-2` → `str`  (size)
  - `1` → `carryStr`  (untyped)
  - `-1` → `size`  (untyped)
  - `0.5` → `carryMult`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Remove Fear
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 332
**Foundry id:** `lpBAgRhDew61Vmzo`

> Grants +[[4]] morale bonus against fear effects as per @UUID[Compendium.pf1.spells.Item.eu4u4mr1naoiqohz].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Resist Energy (Acid)
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 334
**Foundry id:** `efd99dVtQUUSoz5Z`

> Grants [[10 * clamp(ceil((@item.level + 1) / 4), 1, 3)]] resistance against acid as per @UUID[Compendium.pf1.spells.Item.tkjnm3lw7ni82tag].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Resist Energy (Cold)
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 334
**Foundry id:** `u2g0irnJ5BeNvh0R`

> Grants [[10 * clamp(ceil((@item.level + 1) / 4), 1, 3)]] resistance against cold as per @UUID[Compendium.pf1.spells.Item.tkjnm3lw7ni82tag].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Resist Energy (Electricity)
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 334
**Foundry id:** `p8gZ2WaceSCWT4LK`

> Grants [[10 * clamp(ceil((@item.level + 1) / 4), 1, 3)]] resistance against electricity as per @UUID[Compendium.pf1.spells.Item.tkjnm3lw7ni82tag].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Resist Energy (Fire)
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 334
**Foundry id:** `OEPLhd4m46A6QA31`

> Grants [[10 * clamp(ceil((@item.level + 1) / 4), 1, 3)]] resistance against fire as per @UUID[Compendium.pf1.spells.Item.tkjnm3lw7ni82tag].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Resist Energy (Sonic)
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 334
**Foundry id:** `tV3x332iNS0WpFf3`

> Grants [[10 * clamp(ceil((@item.level + 1) / 4), 1, 3)]] resistance against sonic as per @UUID[Compendium.pf1.spells.Item.tkjnm3lw7ni82tag].

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Resistance
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 334
**Foundry id:** `GdU6Xlwn2phRnfc6`

> You are imbued with a +[[1]] resistance bonus on saves as per @UUID[Compendium.pf1.spells.Item.g8j278xcu2s1zlwy].

**Mechanical encoding:** `changes`: 1
  - `1` → `allSavingThrows`  (resist)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### See Invisibility
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 339
**Foundry id:** `U7fqIfaTpWEcpamb`

> Grants see invisibility for 10 Minutes per item level as per @UUID[Compendium.pf1.spells.Item.nokru6mxk9p3r513] spell.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shield of Faith
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 342
**Foundry id:** `WgCWQxR53UdVSGPB`

> Grants deflection bonus to AC as per @UUID[Compendium.pf1.spells.Item.y2uhoqr4itdbw5g4] spell.

**Mechanical encoding:** `changes`: 1
  - `2 + min(3, floor(@item.level / 6))` → `ac`  (deflection)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shield Other
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 342
**Foundry id:** `DTQBBe9QaeqI4jFp`

> Grants +[[1]] deflection bonus to AC and a +[[1]] resistance bonus on saves as per @UUID[Compendium.pf1.spells.Item.menqakfoa1ftvi3f].

**Mechanical encoding:** `changes`: 2
  - `1` → `allSavingThrows`  (resist)
  - `1` → `ac`  (deflection)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shield
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 342
**Foundry id:** `olTpyao476hOEzzm`

> Grants +[[4]] Shield Bonus to AC which also applies to incorporeal touch attacks as per @UUID[Compendium.pf1.spells.Item.sz7j540uypmqqvti].

**Mechanical encoding:** `changes`: 1
  - `4` → `sac`  (base)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Slow
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 344
**Foundry id:** `OQQYaNxXsb974T8j`

> You are @Condition[staggered], and you have a -1 penalty to attack rolls, AC and Reflex saves.
>
> In addition, you move at half speed (round down to the next 5-foot increment).
>
> See @UUID[Compendium.pf1.spells.Item.jcr72piqo6g549e1] for more details.

**Mechanical encoding:** `changes`: 8 (showing first 5)
  - `if(gt(@attributes.speed.swim.total, 0), max(1, floor(@attributes.speed.swim.total / 5 / 2)) * 5)` → `swimSpeed`  (untyped)
  - `if(gt(@attributes.speed.land.total, 0), max(1, floor(@attributes.speed.land.total / 5 / 2)) * 5)` → `landSpeed`  (untyped)
  - `if(gt(@attributes.speed.burrow.total, 0), max(1, floor(@attributes.speed.burrow.total / 5 / 2)) * 5)` → `burrowSpeed`  (untyped)
  - `if(gt(@attributes.speed.climb.total, 0), max(1, floor(@attributes.speed.climb.total / 5 / 2)) * 5)` → `climbSpeed`  (untyped)
  - `-1` → `ref`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Spell Resistance
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 347
**Foundry id:** `GTSxlSYtfXk5a0Oj`

> Grants spell resistance [[12 + @item.level]] as per @UUID[Compendium.pf1.spells.Item.4k9bh8ny1il2oner].

**Mechanical encoding:** `changes`: 1
  - `12 + @item.level` → `spellResist`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Spider Climb
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 347
**Foundry id:** `0KISG8qU22ncv72d`

> Grants 20 feet climb speed as per @UUID[Compendium.pf1.spells.Item.3mfmhx8avu7h3iom].

**Mechanical encoding:** `changes`: 1
  - `20` → `climbSpeed`  (racial)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Stoneskin
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 350
**Foundry id:** `dYMrU01t5FNMgNra`

> You gain DR 10/adamantine. You ignore the first 10 points of damage each time you take damage from a weapon, though an adamantine weapon bypasses the reduction. Once the spell has prevented a total of [[min(@item.level, 15) * 10]] points of damage, it is discharged as per Stoneskin.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Touch of the Sea
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 250
**Foundry id:** `9HlefpSamj4Qme3p`

> Grants swim speed of [[30]] feet along and the ability to take 10 even if distracted or endangered as per @UUID[Compendium.pf1.spells.Item.ts50hpvkdgerfp1a].

**Mechanical encoding:** `changes`: 1
  - `30` → `swimSpeed`  (racial)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### True Seeing
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 363
**Foundry id:** `hiSHFDTHqBYTvsaR`

> Grants true seeing 120 ft. for 1 Minute per item level as per @UUID[Compendium.pf1.spells.Item.jbqo4o2b2tmdz7wv] spell.

**Mechanical encoding:** `changes`: 1
  - `120` → `sensetr`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Wrathful Mantle
*(buff / spell)*

**Tags:** —
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 257
**Foundry id:** `bU5ry2F5WAKhacZI`

> Grants a +[[min(5, floor(@item.level / 4))]] resistance bonus on all saving throws. You can end the effect at any time as a swift action to deal 2d8 points of force damage to all creatures within 5 feet as per @UUID[Compendium.pf1.spells.Item.1gz3zdpxu7uic5ky].

**Mechanical encoding:** `changes`: 1, has `actions`
  - `min(5, floor(@item.level / 4))` → `allSavingThrows`  (resist)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Spells
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `abSp08elNrsecBYc`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Total Defense
*(buff / temp)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 186
**Foundry id:** `DvcRWaWndZ1s2tB4`

> You can defend yourself as a standard action. You get a +[[4]] dodge bonus to your AC for 1 round. Your AC improves at the start of this action. You can’t combine total defense with fighting defensively or with the benefit of the Combat Expertise feat. You can’t make attacks of opportunity while using total defense.

**Mechanical encoding:** `changes`: 1
  - `4 + if(gte(@skills.acr.rank, 3), 2)` → `ac`  (dodge)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

