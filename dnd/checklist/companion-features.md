# PF1 Rules Checklist — companion-features

_Auto-generated from a Foundry PF1e pack snapshot. **Do not edit by hand.**_
_Items in this shard: 11._

Status legend (for the `Manual verdict:` field below):
- `[x]` verified — engine matches RAW
- `[~]` partial  — engine has some of it; gap noted
- `[-]` absent   — not in our content / engine
- `[!]` buggy    — implemented but doesn't match RAW

Update `dnd/coverage.py` with the verdict after marking a row.

---
### Alertness
*(feat / classFeat)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 83
**Foundry id:** `iYSmTvVIXZt2uMov`

> While a familiar is within arm's reach, the master gains the Alertness feat.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Deliver Touch Spells
*(feat / classFeat)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 83
**Foundry id:** `XttM5JcGilkhdFCW`

> If the master is 3rd level or higher, a familiar can deliver touch spells for him. If the master and the familiar are in contact at the time the master casts a touch spell, he can designate his familiar as the "toucher." The familiar can then deliver the touch spell just as the master would. As usual, if the master casts another spell before the touch is delivered, the touch spell dissipates.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Empathic Link
*(feat / classFeat)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 83
**Foundry id:** `YtzidlXTKvVyiNcY`

> The master has an empathic link with his familiar to a 1 mile distance. The master can communicate emphatically with the familiar, but cannot see through its eyes. Because of the link’s limited nature, only general emotions can be shared. The master has the same connection to an item or place that his familiar does.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Evasion
*(feat / classFeat)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 83
**Foundry id:** `ooxP3ifhV6kC0wTM`

> When subjected to an attack that normally allows a Reflex saving throw for half damage, a familiar takes no damage if it makes a successful saving throw and half damage even if the saving throw fails.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Scry on Familiar
*(feat / classFeat)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 83
**Foundry id:** `mUPO7LpDVJtOoP4W`

> If the master is 13th level or higher, he may scry on his familiar (as if casting the scrying spell) once per day.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Share Spells
*(feat / classFeat)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 83
**Foundry id:** `B4tsrPOAtyEOmwAr`

> The master may cast a spell with a target of "You" on his familiar (as a touch spell) instead of on himself. The master may cast spells on his familiar even if the spells do not normally affect creatures of the familiar’s type (magical beast).

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Speak with Animals of Its Kind
*(feat / classFeat)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 83
**Foundry id:** `yNMQccEicirDocG7`

> If the master is 7th level or higher, a familiar can communicate with animals of approximately the same kind as itself (including dire varieties): bats with bats, cats with felines, hawks and owls and ravens with birds, lizards and snakes with reptiles, monkeys with other simians, rats with rodents, toads with amphibians, and weasels with ermines and minks. Such communication is limited by the Intelligence of the conversing creatures.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Speak with Master
*(feat / classFeat)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 83
**Foundry id:** `GgqfqGq8vopOdN32`

> If the master is 5th level or higher, a familiar and the master can communicate verbally as if they were using a common language. Other creatures do not understand the communication without magical help.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Spell Resistance
*(feat / classFeat)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 83
**Foundry id:** `OrbV3Q6U2BdnL8tR`

> If the master is 11th level or higher, a familiar gains spell resistance equal to the master’s level + 5. To affect the familiar with a spell, another spellcaster must get a result on a caster level check (1d20 + caster level) that equals or exceeds the familiar’s spell resistance.

**Mechanical encoding:** `changes`: 1
  - `5 + @class.level` → `spellResist`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Familiar Features
*(Item)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `NY5BdmnNcdiNt1PL`

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Familiar
*(class / base)*

**Tags:** —
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 83
**Foundry id:** `EbgtpUXqVup5iXeD`

> A familiar is an animal chosen by a spellcaster to aid him in his study of magic. It retains the appearance, Hit Dice, base attack bonus, base save bonuses, skills, and feats of the normal animal it once was, but is now a magical beast for the purpose of effects that depend on its type. Only a normal, unmodified animal may become a familiar. An animal companion cannot also function as a familiar.
>
> A familiar grants special abilities to its master, as given on the table below. These special abilities apply only when the master and familiar are within 1 mile of each other.
>
> Levels of different classes that are entitled to familiars stack for the purpose of determining any familiar abilities that depend on the master’s level.
>
> If a familiar is dismissed, lost, or dies, it can be replaced 1 week later through a specialized ritual that costs 200 gp per wizard level. The ritual takes 8 hours to complete.
>
> #### Familiar Basics
>
> Use the basic statistics for a creature of the familiar's kind, but with the following changes.
>
> **Hit Dice**: For the purpose of effects related to number of Hit Dice, use the master's character level or the familiar's normal HD total, whichever is higher.
>
> **Hit Points**: The familiar has half the master's total hit points (not including temporary hit points), rounded down, regardless of its actual Hit Dice.
>
> **Attacks**: Use the master's base attack bonus, as calculated from all his classes. Use the familiar's Dexterity or Strength modifier, whichever is greater, to calculate the familiar's melee attack bonus with natural weapons. Damage equals that of a normal creature of the familiar's kind.
>
> **Saving Throws**: For each saving throw, use either the familiar's base save bonus (Fortitude +2, Reflex +2, Will +0) or the master's (as calculated from all his classes), whichever is better. The familiar uses its own ability modifiers to saves, and it doesn't share any of the other bonuses that the master might have on saves.
>
> **Skills**: For each skill in which either the master or the familiar has ranks, use either the normal skill ranks for an animal of that type or the master's skill ranks, whichever is better. In either case, the familiar uses its own ability modifiers. Regardless of a familiar's total skill modifiers, some skills may remain beyond the familiar's ability to use. Familiars treat Acrobatics, Climb, Fly, Perception, Stealth, and Swim as class skills.
>
> **Usage**: Setup BAB, Saving Throws and Hit Points in Details tab according to familiar and master stats as mentioned above
>
> #### Familiar Ability Descriptions
>
> All familiars have special abilities (or impart abilities to their masters) depending on the master's combined level in classes that grant familiars, as shown on the table below. The abilities are cumulative.
>  Master Class Level Natural Armor Adj. Int Special 1st–2nd +1 6 Alertness, improved evasion, share spells, empathic link 3rd–4th +2 7 Deliver touch spells 5th–6th +3 8 Speak with master 7th–8th +4 9 Speak with animals of its kind 9th–10th +5 10 — 11th–12th +6 11 Spell resistance 13th–14th +7 12 Scry on familiar 15th–16th +8 13 — 17th–18th +9 14 — 19th–20th +10 15 — 
>
> **Natural Armor Adj**.: The number noted here is in addition to the familiar's existing natural armor bonus.
>
> **Int**: The familiar's Intelligence score.

**Mechanical encoding:** `changes`: 2
  - `5 + ceil(@classes.familiar.level / 2)` → `int`  (untyped)
  - `ceil(@classes.familiar.level / 2)` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

