# PF1 Rules Checklist — monster-templates

_Auto-generated from a Foundry PF1e pack snapshot. **Do not edit by hand.**_
_Items in this shard: 198._

Status legend (for the `Manual verdict:` field below):
- `[x]` verified — engine matches RAW
- `[~]` partial  — engine has some of it; gap noted
- `[-]` absent   — not in our content / engine
- `[!]` buggy    — implemented but doesn't match RAW

Update `dnd/coverage.py` with the verdict after marking a row.

---
### Advanced (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 294
**Foundry id:** `0EZPEkeiIiU2ZkBh`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> Creatures with the advanced template are fiercer and more powerful than their ordinary cousins.
>
> **Quick Rules**: +2 on all rolls (including damage rolls) and special ability DCs; +4 to AC and CMD; +2 hp/HD.
>
> **Rebuild Rules**: **AC** increase natural armor by +2; **Ability Scores** +4 to all ability scores (except Int scores of 2 or less).

**Mechanical encoding:** `changes`: 10 (showing first 5)
  - `2` → `attack`  (untyped)
  - `2` → `init`  (untyped)
  - `4` → `nac`  (untyped)
  - `2` → `damage`  (untyped)
  - `4` → `cmd`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Advanced (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 294
**Foundry id:** `68lE3FXyBY9P6I7o`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> Creatures with the advanced template are fiercer and more powerful than their ordinary cousins.
>
> **Quick Rules**: +2 on all rolls (including damage rolls) and special ability DCs; +4 to AC and CMD; +2 hp/HD.
>
> **Rebuild Rules**: **AC** increase natural armor by +2; **Ability Scores** +4 to all ability scores (except Int scores of 2 or less).

**Mechanical encoding:** `changes`: 7 (showing first 5)
  - `4` → `cha`  (untypedPerm)
  - `2` → `nac`  (untypedPerm)
  - `if(gt(@abilities.int.total, 2), 4)` → `int`  (untypedPerm)
  - `4` → `str`  (untypedPerm)
  - `4` → `wis`  (untypedPerm)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Aerial
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9458 (PZO9458) p. 18
**Foundry id:** `Ovo97rjBymtgkjdH`

> **Usable with Summons** Yes - Requires the feat @UUID[Compendium.pf1.feats.Item.ezNxW33BtSafLl0J] or @UUID[Compendium.pf1.feats.Item.R5nnb83RW7qHkVmA]
>
> Aerial creatures are native denizens of the Elemental Planes of Air, and they possess unique adaptations to help them survive there. This template can be applied only to a non-outsider with none of the subtypes that follow: air, cold, earth, fire, or water. An aerial creature's CR increases by 1 only if the base creature has 5 or more HD.
>
> **Rebuild Rules:** **Type** gains the air subtype; **Senses** gains darkvision 60 ft.; **Defensive Abilities** gains DR and resistance to electricity as noted on the table below; **Speed** gains a fly speed equal to its highest speed with perfect maneuverability (maximum fly speed of 10 feet per HD); **Attacks** gains bonus electricity damage as noted on the table below on attacks with natural weapons and metal weapons.
>
>
> **Hit Dice**
>
>
> **DR**
>
>
> **Resist Electricity**
>
>
> **Electricity Damage**
>
>
> 1-4
>
>
> -
>
>
> 10
>
>
> 1 point
>
>
> 5-10
>
>
> 3/-
>
>
> 15
>
>
> 1d6
>
>
> 11+
>
>
> 5/-
>
>
> 20
>
>
> 2d6

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Alebrije
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `AE4zG8c0mrTDrsv4`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Alebrijes travel through dreams, visiting creatures as they sleep in hopes of answering questions, jogging memories, or providing inspiration. Alebrijes can take the shape of any animal or magical beast found throughout the Material Plane, though they have unique colorations and patterns all over their bodies, and some grow wings. These colorations typically include bright, vibrant hues and decorative patterns like spirals and stripes.
>
> "Alebrije" is an acquired template that can be added to any animal or magical beast (referred to hereafter as the base creature). An alebrije uses the base creature’s statistics and special abilities except as noted here.
>
> **Challenge Rating:** Base creature’s CR + 2.
>
> **Size:** An alebrije with 8 Hit Dice or more increases in size by one category.
>
> **Type**: The creature’s type changes to magical beast (extraplanar). Do not recalculate its base attack bonus, saves, or skill ranks.
>
> **Senses:** The creature gains darkvision with a range of 120 feet, dreamsight, and scent.
>
> **Dreamsight (Su):** Alebrijes are able to notice and locate sleeping creatures within 500 feet, as well as creatures engaged in similar rest, such as meditation or resting trances.
>
> **Armor Class:** Natural armor bonus increases by 2.
>
> **Hit Dice:** Change all the creature’s racial Hit Dice to d10s. Hit Dice derived from class levels remain unchanged.
>
> **Defensive Abilities:** An alebrije with 5 Hit Dice or more gains DR 5/magic (or DR 10/magic if it has 11 Hit Dice or more) and SR equal to its new CR + 6 (or SR equal to its new CR + 11 if it has 11 Hit Dice or more). In addition, an alebrije gains cold resistance 5 and fire resistance 5 (or cold resistance 10 and fire resistance 10 if it has 11 Hit Dice or more). Finally, an alebrije gains light fortification, as the fortification armor special ability.
>
> **Speed:** An alebrije with 5 Hit Dice or more grows wings and gains a fly speed of 20 feet (average). If the alebrije has 11 Hit Dice or more, it gains a fly speed of 40 feet (average) instead. An alebrije that already has a fly speed improves its maneuverability by one step instead.
>
> **Melee:** An alebrije’s natural attacks grow mighty and fantastical. Increase the damage die of the base creature’s primary natural attacks by one step. An alebrije’s natural attacks are considered magical for the purposes of damage reduction.
>
> **Spell-like Abilities:** An alebrije gains the following spell-like abilities, using its Charisma modifier to determine any save DCs: 3/day—dream, nightmare; 1/day— dream council, dream travel, mind thrust III, plane shift (self plus 50 lbs. of objects only). The caster level equals the creature’s HD (or the caster level of the base creature’s spell-like abilities, whichever is higher).
>
> **Ability Scores:** Str +4, Dex +6, Con +4, Int +4, Wis +6, Cha +4.
>
> **Skills:** Alebrijes have a +8 racial bonus on Knowledge (arcana) and Knowledge (planes) checks. They always treat these skills as class skills. Otherwise,their skills are the same as the base creatures’.
>
> **Languages:** An alebrije gains telepathy (100 ft.) and can speak one language of its choice.

**Mechanical encoding:** `changes`: 11 (showing first 5)
  - `6` → `dex`  (untyped)
  - `6` → `wis`  (untyped)
  - `4` → `cha`  (untyped)
  - `8` → `skill.kar`  (untyped)
  - `4` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Alter Ego
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** Bestiary 5 (PZO1137) p. 9
**Foundry id:** `STjPrfTnTtkpYRI1`

> "Alter ego" is an acquired template that can be added to any corporeal creature that has an Int score of 3 or higher (referred to hereafter as the base creature). An alter ego uses all of the base creature's statistics and special abilities except as noted here.
>
> **Challenge Rating:** Same as base creature.
>
> **Alignment:** Usually neutral.
>
> **Type:** The creature's type changes to construct. It retains all subtypes except for alignment subtypes and subtypes that indicate kind.
>
> **Armor Class:** Though it appears identical to its progenitor, an alter ego is formed from a solidified ectoplasm that is more yielding than flesh. Reduce the creature's natural armor bonus by 2 (minimum +0).
>
> **Hit Dice:** Change all the creature's racial Hit Dice to d10s. All Hit Dice derived from class levels remain unchanged. As a construct, an alter ego doesn't have a Constitution score, but as a construct it gains bonus hit points based on its size.
>
> **Defensive Abilities:** An alter ego gains fast healing 1 (or fast healing 3 if it has 11 Hit Dice or more), DR 5/adamantine (or DR 10/adamantine if it has 11 Hit Dice or more), and the standard construct immunities and traits.
>
> **Attacks:** An alter ego retains all the natural weapons, manufactured weapon attacks, and weapon proficiencies of the base creature. It also gains a slam attack that deals damage based on the alter ego's size, but as if it were one size category larger than its actual size.
>
> **Ability Scores:** Dex +4. As a construct, an alter ego has no Constitution score; treat it as having a Constitution score of 10 when determining hit points, save DCs, and other statistics that rely on a Constitution score.
>
> **Feats:** An alter ego gains Toughness as a bonus feat.
>
> **Skills:** An alter ego can confuse onlookers into believing it is its progenitor. An alter ego gains a +4 racial bonus on Disguise checks to appear as its progenitor.
>
> **Special Qualities:** An alter ego gains the following special qualities.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.eBclJmWWG1VwVadt inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.4N1msV5R8pNWpR5s inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.vUgD8OJ9fAMalD3d inline=true]

**Mechanical encoding:** `changes`: 3
  - `4` → `dex`  (untyped)
  - `-min(@ac.natural.total, 2)` → `nac`  (untyped)
  - `1` → `bonusFeats`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Animal Lord
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1120 (PZO1120) p. 14-15
**Foundry id:** `0EQrL4heBcvh7TUk`

> When the gods of nature or powerful spirits desire a champion to defend the animal world, they invest a token of their power in a chosen vessel—be it animal or humanoid. Traditionally, only one animal lord for a specific animal species is active on a world at any one time, although sometimes, when an extant animal lord strays from its charge or otherwise fails, the force that created it might create a replacement to send against the fallen animal lord to challenge it in a combat to the death, with the victor claiming the right to rule or a chance at redemption.
>
> An animal lord does not dwell among humanity—the wild is its domain. How an animal lord interacts with a humanoid society largely depends on how that society treats the animals of that lord's affinity. Societies that honor and respect those animals, even if they use the animals as a food source, earn the animal lord's (sometimes grudging) respect, but those who abuse or otherwise harm animals of that lord's species find a powerful and ardent enemy in the lord.
>
> The cat lord above uses a leopard as the base animal—this particular cat lord represents a newly created animal lord. The longer an animal lord exists, the higher its level should be.
>
> "Animal Lord" is an inherited template that can be added to any humanoid of 10 Hit Dice or more, referred to hereafter as the base creature. The animal lord also gains the characteristics of one type of animal (of a size no larger than one step larger than the base creature's size), referred to hereafter as the base animal.
>
> **CR:** Same as the base creature or the base animal (whichever is higher) +2.
>
> **Alignment:** Any neutral.
>
> **Type:** The base creature's type changes to outsider (native, shapechanger). Do not recalculate class Hit Dice, BAB, or saves.
>
> **Senses:** An animal lord gains the senses of both the base creature and the base animal in both of its forms.
>
> **AC:** An animal lord gains the base animal or base creature's natural armor bonus, whichever is higher, in both of its forms—this bonus is increased by +2 to determine the animal lord's actual natural armor bonus.
>
> **Defensive Abilities:** An animal lord gains DR 10/silver. It also gains all of the base animal's defensive abilities in both of its forms.
>
> **Speed:** An animal lord's base speed is that of its base creature form or its base animal form, whichever is greater. Animal lords whose base animal has a burrow, climb, fly, or swim speed can use that mode of movement even in humanoid form, instantly growing the necessary appendages as necessary.
>
> **Melee:** An animal lord in humanoid form can instantaneously transform parts of its body to make all of the natural attacks possessed by the base animal. An animal lord typically prefers to use its natural attacks in melee combat, but often carries manufactured ranged weapons to diversify its combat options as well.
>
> **Special Attacks:** An animal lord gains all of the special attacks possessed by the base animal and can employ them in both humanoid and animal form. It also gains abilities determined by its species affinity (see below).
>
> **Ability Scores:** Animal lords use the higher ability score between the base creature and the base animal as their base ability scores, then increase all of these ability scores by +4.
>
> **Skills:** An animal lord gains all of the base animal's racial modifiers to skill checks.
>
> **Special Qualities:** An animal lord gains the following special qualities.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.tF4zvrr6K89kUR5A inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.dQHMSJgnd7riv2JD inline=true]
>
> #### Species Affinity
>
> Animal lords can be made from almost any creature of the animal type, but most are grouped into larger categories known as species affinities. The most common animal lord kingdom affinities are detailed below, but many others exist. Animals listed in parenthesis list typical base animals for that lord.
>
> **Bear Lord (Grizzly Bear):** Bear lords have broad shoulders, sharp teeth, and thick fingers. Bear lords gain the following additional ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.nl3W3WJZL8fYa0Mt inline=true]
>
> **Canine Lord (Dog, Hyena, Wolf):** Canine lords are hirsute, have pronounced canines, and have slightly pointed ears. Canine lords gain the following additional ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.rwQFthvLAAYprW4z inline=true]
>
> **Cat Lord (Leopard, Lion, Tiger):** Cat lords move with a fluid agility, and have slender bodies and catlike eyes. Cat lords gain the following additional ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.KOEo37F2obKPDseP inline=true]
>
> **Crocodile Lord (Crocodile):** Crocodile lords have reptilian eyes, sharp teeth, and a scaly ridge along the spine. Crocodile lords gain the following additional ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.TNPqQoQDYilAFIZw inline=true]
>
> **Dinosaur Lord (Deinonychus, Tyrannosaurus):** A dinosaur lord tends to have sharp teeth, scaly skin, and a booming voice. Dinosaur lords gain the following additional ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.upwqIwpoP2I16Ro8 inline=true]
>
> **Raptor Lord (Eagle, Falcon):** Raptor lords have feathery-looking and brightly colored hair, wide searching eyes, and aquiline noses. Raptor lords gain the following additional ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.3ih3AiDeM2yTpA7F inline=true]
>
> **Rat Lord (Giant Rat):** Rat lords have pointed chins and pointed ears, and move with quick, jittery motions. Rat lords gain the following additional ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.3cIYvKaT6y5TuktW inline=true]
>
> **Shark Lord (Shark):** Shark lords have black eyes, pale skin, sharp teeth, and little to no body hair. They gain the following additional ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.GdX506twDl0aLS1j inline=true]
>
> **Serpent Lord (Snake):** Serpent lords tend to have unusual skin colors, often with stripes or other patterns), snakelike eyes, and forked tongues. Serpent lords gain the following ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.uh1AGvs2abnp9ANR inline=true]

**Mechanical encoding:** `changes`: 7 (showing first 5)
  - `4` → `str`  (untyped)
  - `4` → `dex`  (untyped)
  - `4` → `int`  (untyped)
  - `4` → `con`  (untyped)
  - `4` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Animus Shade
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** Bestiary 5 (PZO1137) p. 11
**Foundry id:** `RUxd9Jm0DXTUsNZR`

> "Animus shade" is an acquired template that can be added to any living creature that has a Charisma score of at least 6 and an Intelligence score of at least 8. An animus shade retains all the base creature's statistics and special abilities except as noted here.
>
> **Challenge Rating:** Base creature's CR + 2.
>
> **Alignment:** Any evil.
>
> **Type:** The creature's type changes to undead. Do not recalculate the creature's base attack bonus, saves, or skill points. It gains the incorporeal subtype.
>
> **Senses:** An animus shade gains darkvision with a range of 60 feet.
>
> **Aura:** The animus shade gains a mental static aura.
>
> **Armor Class:** The animus shade gains a deflection bonus to its Armor Class equal to its Charisma modifier from the incorporeal subtype. It loses the base creature's natural armor bonus, as well as all armor and shield bonuses not from force effects or the ghost touch special ability.
>
> **Hit Dice:** Change the base creature's racial Hit Dice to d8s. Its class Hit Dice are unaffected. As an undead, an animus shade uses its Charisma modifier to determine its bonus hit points (instead of its Constitution modifier).
>
> **Defensive Abilities:** An animus shade retains all of the defensive abilities of the base creature that don't rely on a corporeal form to function. It gains channel resistance +4, the incorporeal ability, and all of the immunities granted by its undead traits. An animus shade also gains the following defensive ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.mTXwy22RE0LXt4JT inline=true]
>
> **Speed:** An animus shade loses its previous speeds and gains a fly speed of 30 feet (perfect), unless the base creature has a better fly speed.
>
> **Attacks:** An animus shade loses all of the base creature's natural and unarmed attacks.
>
> **Special Attacks:** An animus shade retains all special attacks of the original creature that do not require a corporeal body to function. In addition, it gains the following special attacks. The save DC of an animus shade's special attacks is equal to 10 + half the animus shade's Hit Dice + the animus shade's Charisma modifier. These are mind-affecting effects.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.JuP9zPXUJ1B31X2F inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.a2onQfehBz8zEtJb inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.61zlWQsYOBvxzQIX inline=true]
>
> **Ability Scores:** Cha +4. In addition, as an incorporeal creature, an animus shade has no Strength or Constitution score.
>
> **Skills:** An animus shade gains a +8 racial bonus on Intimidate and Perception checks (which stacks with other racial bonuses). An animus shade treats Climb, Disguise, Fly, Intimidate, Knowledge (arcana), Knowledge (religion), Perception, Sense Motive, Spellcraft, and Stealth as class skills. Otherwise, its skills are the same as those of the base creature.

**Mechanical encoding:** `changes`: 9 (showing first 5)
  - `8` → `skill.per`  (untyped)
  - `max(@attributes.speed.fly.base, 30)` → `flySpeed`  (untyped)
  - `0` → `landSpeed`  (untyped)
  - `0` → `burrowSpeed`  (untyped)
  - `0` → `swimSpeed`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Aqueous
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9458 (PZO9458) p. 18
**Foundry id:** `xXxuV1C3GQrAgvE9`

> **Usable with Summons** Yes - Requires the feat @UUID[Compendium.pf1.feats.Item.ezNxW33BtSafLl0J] or @UUID[Compendium.pf1.feats.Item.R5nnb83RW7qHkVmA]
>
> Aqueous creatures are native denizens of the Elemental Planes of Water, and they move with a unique grace underwater. This template can be applied only to a non-outsider that has none of the following subtypes: air, cold, earth, fire, or water. An aqueous creature’s CR increases by 1 only if the base creature has 5 or more HD.
>
> **Rebuild Rules:** **Type** gains the water subtype; **Senses** gains darkvision 60 ft.; **Defensive Abilities** gains DR and resistance to cold as noted on the table below; **Speed** gains a swim speed equal to its highest speed + 10 ft.; **Attacks** gains bonus cold damage as noted on the table below on attacks with natural weapons and metal weapons.
>
>
> **Hit Dice**
>
>
> **DR**
>
>
> **Resist Cold**
>
>
> **Cold Damage**
>
>
> 1-4
>
>
> -
>
>
> 10
>
>
> 1 point
>
>
> 5-10
>
>
> 3/-
>
>
> 15
>
>
> 1d6
>
>
> 11+
>
>
> 5/-
>
>
> 20
>
>
> 2d6

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Barbarian (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 246
**Foundry id:** `QYHoLcZmc7ad1A1z`

> A barbarian creature can fly into a rage, granting it numerous bonuses in combat. It also gains additional hit points and a few valuable defensive abilities. A barbarian creature's CR increases by 3 if the creature has 10 or more HD. A barbarian creature must be chaotic.
>
> **Quick Rules:** +2 on all rolls based on Str; can @UUID[Compendium.pf1.class-abilities.Item.WSqWT9ZIshtC5vlV] for a number of rounds per day equal to 4 + its HD + its Con modifier (this functions as @UUID[Compendium.pf1.class-abilities.Item.IWNz5tJCnpig4UtX] if the creature has 10 or more HD); gains DR 1/— and @UUID[Compendium.pf1.class-abilities.Item.7WaQxnVaaoL4AGr8] (DR 3/— and @UUID[Compendium.pf1.class-abilities.Item.ZfnHhhTFQVo0Lj4P] if the creature has 10 or more HD).
>
> **Rebuild Rules:** **Defensive Abilities** @UUID[Compendium.pf1.class-abilities.Item.7WaQxnVaaoL4AGr8] (@UUID[Compendium.pf1.class-abilities.Item.ZfnHhhTFQVo0Lj4P] if the creature has 10 or more HD; DR 1/— (3/— if the creature has 10 or more HD); **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.WSqWT9ZIshtC5vlV] (can be used a number of rounds per day equal to 4 + its HD + its Con modifier, functions as the @UUID[Compendium.pf1.class-abilities.Item.IWNz5tJCnpig4UtX] class feature if the creature has 10 or more HD); **Ability Scores** +4 Strength.

**Mechanical encoding:** `changes`: 4
  - `2` → `wdamage`  (untyped)
  - `2` → `mattack`  (untyped)
  - `2` → `strChecks`  (untyped)
  - `2` → `strSkills`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Barbarian (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 246
**Foundry id:** `HOCayRF6siZgzNmr`

> A barbarian creature can fly into a rage, granting it numerous bonuses in combat. It also gains additional hit points and a few valuable defensive abilities. A barbarian creature's CR increases by 3 if the creature has 10 or more HD. A barbarian creature must be chaotic.
>
> **Quick Rules:** +2 on all rolls based on Str; can @UUID[Compendium.pf1.class-abilities.Item.WSqWT9ZIshtC5vlV] for a number of rounds per day equal to 4 + its HD + its Con modifier (this functions as @UUID[Compendium.pf1.class-abilities.Item.IWNz5tJCnpig4UtX] if the creature has 10 or more HD); gains DR 1/— and @UUID[Compendium.pf1.class-abilities.Item.7WaQxnVaaoL4AGr8] (DR 3/— and @UUID[Compendium.pf1.class-abilities.Item.ZfnHhhTFQVo0Lj4P] if the creature has 10 or more HD).
>
> **Rebuild Rules:** **Defensive Abilities** @UUID[Compendium.pf1.class-abilities.Item.7WaQxnVaaoL4AGr8] (@UUID[Compendium.pf1.class-abilities.Item.ZfnHhhTFQVo0Lj4P] if the creature has 10 or more HD; DR 1/— (3/— if the creature has 10 or more HD); **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.WSqWT9ZIshtC5vlV] (can be used a number of rounds per day equal to 4 + its HD + its Con modifier, functions as the @UUID[Compendium.pf1.class-abilities.Item.IWNz5tJCnpig4UtX] class feature if the creature has 10 or more HD); **Ability Scores** +4 Strength.

**Mechanical encoding:** `changes`: 1
  - `4` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Bard (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 246
**Foundry id:** `JuIM2J4m5c2hsmAk`

> Capable of inspiring its companions to accomplish great things, a bard creature is most effective when surrounded by allies. It also gains some limited spellcasting. A bard creature's CR increases by 2 if the creature has 10 or more HD.
>
> **Quick Rules:** +2 on all rolls based on Cha; can use @UUID[Compendium.pf1.class-abilities.Item.ZfCUTi1MiLgR4T7I] for a number of rounds per day equal to 4 + its HD + its Cha modifier (using its HD as its bard level to determine the bonuses and types of performance); can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.S4VHXq1asXBwaRwo] (see the Bard Spells Known table, below) using its HD as its CL and gaining two spell slots of each level for every level of spells known.
>
> **Rebuild Rules:** **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.ZfCUTi1MiLgR4T7I] (can be used a number of rounds per day equal to 4 + the creature's HD + its Cha modifier, using its HD as its bard level to determine bonuses and types of performance); **Bard Spells** can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.S4VHXq1asXBwaRwo] (see the Bard Spells Known table below) using its HD as its CL and gaining two spell slots of each level for every level of spells known; **Ability Scores** +4 Charisma.
>
> #### Bard Spells Known
>
>
>
> **HD**
>
>
> **0**
>
>
> **1**
>
>
> **2**
>
>
> **3**
>
>
> **4**
>
>
> **5**
>
>
> **6**
>
>
> 1-4
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 5-8
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 9-12
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> 13-16
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> 17-20
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> 21+
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1

**Mechanical encoding:** `changes`: 2
  - `2` → `chaSkills`  (untyped)
  - `2` → `chaChecks`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Bard (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 246
**Foundry id:** `Mzd7VOaRHy5ne6nW`

> Capable of inspiring its companions to accomplish great things, a bard creature is most effective when surrounded by allies. It also gains some limited spellcasting. A bard creature's CR increases by 2 if the creature has 10 or more HD.
>
> **Quick Rules:** +2 on all rolls based on Cha; can use @UUID[Compendium.pf1.class-abilities.Item.ZfCUTi1MiLgR4T7I] for a number of rounds per day equal to 4 + its HD + its Cha modifier (using its HD as its bard level to determine the bonuses and types of performance); can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.S4VHXq1asXBwaRwo] (see the Bard Spells Known table, below) using its HD as its CL and gaining two spell slots of each level for every level of spells known.
>
> **Rebuild Rules:** **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.ZfCUTi1MiLgR4T7I] (can be used a number of rounds per day equal to 4 + the creature's HD + its Cha modifier, using its HD as its bard level to determine bonuses and types of performance); **Bard Spells** can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.S4VHXq1asXBwaRwo] (see the Bard Spells Known table below) using its HD as its CL and gaining two spell slots of each level for every level of spells known; **Ability Scores** +4 Charisma.
>
> #### Bard Spells Known
>
>
>
> **HD**
>
>
> **0**
>
>
> **1**
>
>
> **2**
>
>
> **3**
>
>
> **4**
>
>
> **5**
>
>
> **6**
>
>
> 1-4
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 5-8
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 9-12
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> 13-16
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> 17-20
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> 21+
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1

**Mechanical encoding:** `changes`: 1
  - `4` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Black-Blooded (3.5)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `7IJ0di9rH8cAMKIN`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> None can claim to fully understand all of the properties of the black blood that courses through the depths of the Darklands. Freezing regardless of temperature and fundamentally charged with deadly negative energies, the viscous ooze empowers the magic of the dead while it fouls and destroys nearly every living thing it touches. Yet not everything is destroyed by the profane substance’s corruptive touch. Some rare beings refuse to be drained of life, and for their tenacity the black blood disfigures them as if by some cruel whim.
>
> Black-blooded creatures are monstrosities warped by exposure to the vile fluids that pervade the Land of Black Blood. Sometimes born of creatures living on the shores of the Caltherium or those subjected to the necromantic fluids as part of cruel experiments, such beings prove exceedingly rare. Those that do exist, however, are crazed and physically warped abominations, living manifestations of the destructive black blood, their paths tainted by endless secretions of the freezing pollution and the ruined lifeless forms of all they encounter. Fortunately, most mutated by the black blood don’t live for long, as no mortal form can suffer the negatively charged. But, in the depths of the Darklands—to the fright of the inhabitants of those already deadly realms—there are known to be some terrifying exceptions.
>
> "Black-blooded" is an acquired template that can be added to any corporeal aberration, animal, dragon, fey, giant, humanoid, magical beast, monstrous humanoid, ooze, plant, or vermin (referred to hereafter as the base creature).
>
> A black-blooded creature uses all the base creaturefs statistics and abilities except as noted here.
>
> **Size and Type:** The creature’s type changes to aberration and it gains the aquatic subtype. Do not recalculate Hit Dice, base attack bonus, or saves. Size is unchanged.
>
> **Speed:** A black-blooded creature gains a swim speed equal to its base movement speed. If it can already swim, use the higher of the two swim speeds.
>
> **Armor Class:** Natural armor increases by +2 (this stacks with any natural armor bonus the base creature has).
>
> **Damage:** A black-blooded creature retains all of the attacks and damage of the base creature, but deals an additional 1d6 points of cold damage on all attacks.
>
> **Special Attacks:** A black-blooded creature retains all the special attacks of the base creature and gains the following special attack.
>
> *Breath Weapon (Su):* 30-foot cone of black blood, once every 1d4 rounds, damage 6d6 cold. A successful Reflex save (DC 10 + 1.2 black-blooded creature's racial HD + black-blooded creature's Con modifier) reduces damage by half.
>
> **Special Qualities:** A black-blooded creature has all the special qualities of the base creature, plus darkvision out to 120 feet, low-light vision, and the amphibious quality. A black-blooded creature has immunity to ability drain, cold, energy drain, and poison.
>
> *Blood Rain (Su):* Black-blooded creatures constantly leak and spray bursts of freezing black blood. Any creature within 15 feet of a black-blooded creature takes an amount of cold damage equal to the black-blooded creature’s Constitution modifier.
>
> *Tainted Life (Ex):* The black blood is antithetical to all life and consumes all but the heartiest hosts. Any creature with the black-blooded template must make a DC 15 Fortitude save every day or take 1d4 points of Constitution damage.
>
> **Abilities:** Increase from the base creature as follows: Str +2, Dex +2, Con +4, Int –4, Cha +2.
>
> **Skills:** A black-blooded creature has a +8 racial bonus on any Swim check to perform some special action or avoid a hazard. It can always choose to take 10 on a Swim check, even if distracted or endangered.
>
> **Environment:** The Land of Black Blood.
>
> **Challenge Rating:** Same as base creature +1.
>
> **Alignment:** Always chaotic evil.
>
> **Level Adjustment:** Same as base creature +3.

**Mechanical encoding:** `changes`: 6 (showing first 5)
  - `4` → `con`  (untyped)
  - `2` → `str`  (untyped)
  - `2` → `dex`  (untyped)
  - `-4` → `int`  (untyped)
  - `2` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Blighted Fey
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** Bestiary 5 (PZO1137) p. 46-47
**Foundry id:** `29X7GiKNBgbc5cxT`

> "Blighted fey" is an acquired template that can be added to any fey creature with 2 or more Hit Dice, referred to hereafter as the base creature. A blighted fey uses the base creature's statistics and abilities except as noted here.
>
> **CR:** Base creature's CR + 2.
>
> **Alignment:** Chaotic evil.
>
> **Senses:** A blighted fey gains darkvision to a range of 60 feet if the base creature did not already have it. If the base creature already has darkvision, the ability is extended by an additional 30 feet.
>
> **Armor Class:** Natural armor improves by 2.
>
> **Defensive Abilities:** A blighted fey gains DR 10/cold iron and good; immunity to disease, paralysis, poison, and polymorph; and resistance to cold 10 and electricity 10. A blighted fey also gains spell resistance equal to 11 + its newly adjusted CR.
>
> Additionally, a blighted fey gains the following ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.PpTqLo0DvrJBJTcC inline=true]
>
> **Special Attacks:** A blighted fey gains the following special attacks. Unless otherwise noted, save DCs are equal to 10 + half the blighted fey's Hit Dice + the blighted fey's Constitution modifier.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.oxCP28AAdPER7l3D inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.LT4HY34hTxLd2Fq0 inline=true]
>
> **Special Qualities:** A blighted fey gains the following special qualities.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.NHQevbJKqM6BKKQt inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.7JXzAkDvUXAsRIcN inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.qFQxsgSMVE79zE9k inline=true]
>
> **Ability Scores:** Str +4, Con +4, Cha +2.
>
> **Feats:** Blighted fey gain @UUID[Compendium.pf1.feats.Item.8snLqsJN4LLL00Nq] as a bonus feat.
>
> **Skills:** A blighted fey gains a +2 racial bonus on Knowledge (nature), Perception, and Stealth checks.

**Mechanical encoding:** `changes`: 9 (showing first 5)
  - `2` → `cha`  (untyped)
  - `4` → `con`  (untyped)
  - `2` → `skill.kna`  (racial)
  - `2` → `skill.per`  (racial)
  - `11 + @details.cr.total` → `spellResist`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Boreal
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `4Xa5IWETHCVLmnyd`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** Yes
>
> In realms where the icy hand of winter seldom (or never) releases its frigid grasp, some particularly hardy creatures have evolved to better survive in these harsh environments, becoming stronger and much more dangerous. These boreal creatures mostly resemble members of their kind that dwell in more temperate climates, but their fur and skin are much paler, and it is not uncommon for parts of these creatures to be cloaked in frost.
>
> **Challenge Rating:** Same as the base creature +1.
>
> **Type:** The creature gains the cold subtype. If this subtype is applied to a creature with the animal or vermin type, the creature’s type changes to magical beast. Do not recalculate its Hit Dice, base attack bonus, saves, or skill points.
>
> **Attacks:** A boreal creature’s natural attacks deal an additional 1d6 points of cold damage.
>
> **Abilities:** Str +2, Con +2.
>
> **Skills:** The creature receives a +4 bonus on Stealth and Survival checks in snow. An aquatic boreal creature receives a +4 racial bonus on Stealth and Survival checks at all times in frigid waters (its natural habit), instead of in snow.
>
> **Environment:** The creature’s natural environment changes to a cold climate.
>
> **Special Qualities:** A boreal creature gains the following special quality.
>
> *Trackless Step (Ex):* A boreal creature does not leave a trail in snow and cannot be tracked. It can choose to leave a trail, if it so desires. This special quality does not apply to aquatic boreal creatures.

**Mechanical encoding:** `changes`: 2
  - `2` → `con`  (untyped)
  - `2` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Broken Soul
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 24-25
**Foundry id:** `8I0XKl38jZIaokAf`

> A broken soul is torment and pain made manifest. Tortured to the extremes of both physical and mental endurance, and then taken beyond those barriers, a broken soul gains extraordinary reserves of fortitude and resilience as well as the ability to inflict a measure of its own terrible suffering on others.
>
> Each broken soul has a unique appearance, the torture it has endured plainly visible on its body. Its skin is a mass of scar tissue, marred with bruises that do not fade and scored with countless scars. In some cases, a broken soul's flesh has been flayed away, revealing the musculature and bone underneath. Weeping sores and open cuts cover a broken soul's body, wounds that never fully heal. Its limbs are often twisted, the result of broken bones that were never set properly, and it might be missing fingers, toes, ears, or other appendages. A broken soul's existence is one of unending suffering, and the constant pain often drives the creature irrevocably mad. In their insanity, these unfortunates hate all other creatures and seek to inflict their wounds and their agony on all they encounter.
>
> The creation of a broken soul can happen in a number of ways. Some broken souls arise spontaneously, the result of horrific treatment at the hands of cruel abusers. With no way to escape their torment, these creatures embrace the pain and anguish and transcend them, making them a part of their very being. In so doing, they become something both more and less than they were. Other broken souls are purposefully created out of helpless prisoners by sadistic torturers through a harrowing gauntlet of mental and physical torments. By breaking a creature's mind and body, these torturers hope to create guardians or servants whose loyalty is ensured by the constant pain they must endure. Even more harrowing, some broken souls take it upon themselves to create more of their kind, fashioning gruesome works of living, mutilated art in an effort to share their suffering. These "artists" often turn on their own torturers first, perfecting their skills on those who created them before turning their attention to any other unfortunate creatures they can find.
>
> "Broken soul" is an acquired template that can be added to any living creature with an Intelligence score of 3 or higher (referred to hereafter as the base creature). A broken soul uses all the base creature's statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature +2.
>
> **Alignment:** Usually chaotic evil.
>
> **Armor Class:** A mass of scar tissue covers every inch of the broken soul's body, increasing the base creature's natural armor bonus by +4.
>
> **Defensive Abilities:** Inured to pain and abuse, a broken soul gains damage reduction 5/— and acid, cold, electricity, fire, and sonic resistance 5.
>
> **Speed:** Because a broken soul is in constant agony, reduce each of its speeds by 10 feet (minimum speed of 5 feet).
>
> **Special Attacks:** A broken soul gains the following special attacks. Save DCs are equal to 10 + 1/2 the broken soul's Hit Dice + the broken soul's Charisma modifier unless otherwise noted.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.VsssQaINzYsRKjxk inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.ljdRSNZRFdr25jDd inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.fwdVN17CK9Ok3vAL inline=true]
>
> **Abilities:** Con +6, Wis –2 (minimum 1). In addition, a broken soul gains a +2 bonus to one ability score of its choice and a –6 penalty to another ability score of its choice (minimum 1), which can apply to the ability scores modified by this template.
>
> **Feats:** A broken soul gains Diehard, Endurance, Great Fortitude, and Toughness as bonus feats.
>
> **Skills:** A broken soul gains a +8 racial bonus on Intimidate checks, but takes a –10 racial penalty on Concentration checks because of its constant pain.
>
> **Organization:** Solitary.

**Mechanical encoding:** `changes`: 11 (showing first 5)
  - `-(10 - max(0, 5 - (@attributes.speed.land.base - 10)))` → `landSpeed`  (untyped)
  - `8` → `skill.int`  (racial)
  - `-10` → `concentration`  (racial)
  - `-(10 - max(0, 5 - (@attributes.speed.climb.base - 10)))` → `climbSpeed`  (untyped)
  - `4` → `bonusFeats`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Calcified
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `kmhlTruhYgDtSDDz`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> A creature with the calcified template is preserved by the toxic fluids pumped into its body by an incutilis lord. Though the creature’s identity is lost and its life soon fades, the incutilis lord retains use of the creature’s feats, physical skills, extraordinary abilities, spell-like abilities, and supernatural abilities. This template can be applied to any living corporeal creature.
>
> **Rebuild Rules:** Senses darkvision 60 ft.; AC increase natural armor by 4; Immune mind-affecting effects; Ability Scores +4 Str and Con. A calcified creature has no Intelligence score, but can use its physical skills as directed by the incutilis lord that created it and does not lose any skill ranks. Skills: +8 racial bonus on Stealth checks in dim or no light.

**Mechanical encoding:** `changes`: 3
  - `4` → `str`  (untyped)
  - `4` → `nac`  (untyped)
  - `4` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Celestial
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 294
**Foundry id:** `8kHcvgFNoGObDhQ8`

> Celestial creatures dwell in the higher planes, but can be summoned using spells such as summon monster and planar ally. A celestial creature's CR increases by +1 only if the base creature has 5 or more HD. A celestial creature's quick and rebuild rules are the same.
>
> **Rebuild Rules:** **Senses** gains darkvision 60 ft.; **Defensive Abilities** gains DR and energy resistance as noted on the table; **SR** gains SR equal to new CR +5; **Special Attacks** @UUID[Compendium.pf1.template-abilities.Item.y1wyWYIpRmchAFO6] 1/day as a swift action (adds Cha bonus to attack rolls and damage bonus equal to HD against evil foes; smite persists until target is dead or the celestial creature rests).
>
> **Celestial Creature Defenses**
>
>
> **Hit Dice**
>
>
> **Resist Acid, Cold, and Electricity**
>
>
> **DR**
>
>
> 1-4
>
>
> 5
>
>
> —
>
>
> 5-10
>
>
> 10
>
>
> 5/evil
>
>
> 11+
>
>
> 15
>
>
> 10/evil

**Mechanical encoding:** `changes`: 1
  - `@details.cr.total + 5` → `spellResist`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Child of Yog-Sothoth
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `9ARmxRrYxvt0MJTo`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** No
>
> Creatures born of mortal flesh infused with the essence of the outer god Yog-Sothoth, these deviant children are often tasked with preparing the world for further incursions from other dimensions or agents of the Elder Mythos. Traditionally, the process of creating a child of Yog-Sothoth involves a blasphemous ritual that uses a mortal creature (typically a human) as an incubator. For the purpose of this ritual, gender is irrelevant. Giving birth to a child of Yog-Sothoth is always fatal. In most cases, the ritual results in the birth of twins—one a child of Yog-Sothoth, which can pass for a time as a member of the race of the creature in which it incubated, and one that cannot. Those twins that inherit a monstrous appearance take more after the Outer God itself in form, and are known as the spawn of Yog-Sothoth (Pathfinder RPG Bestiary 4 251).
>
> "Child of Yog-Sothoth" is an inherited template that can be added to any living corporeal creature (referred to hereafter as the base creature), but typically, humanoids and animals are those chosen by the cult of Yog-Sothoth to carry the Outer God’s gifts. A child of Yog-Sothoth retains all of the base creature’s statistics and special abilities, except as listed below.
>
> **Challenge Rating:** Base creature’s CR + 1.
>
> **Alignment:** Any chaotic. The vast majority of the children of Yog-Sothoth are chaotic evil. While a good-aligned child of Yog-Sothoth is theoretically possible, such a creature would be significantly unusual in that it would need to have been separated at an early age from the cult that caused its creation, and allowed to mature with the strong guidance of a good-aligned mentor or parental figure.
>
> **Type:** The creature’s type changes to aberration (augmented). Do not recalculate its base attack bonus, saves, or skill ranks.
>
> **Senses:** The creature gains all-around vision and low-light vision.
>
> **Armor Class:** A child of Yog-Sothoth has either a +1 natural armor bonus for every 2 Hit Dice it has or the base creature’s natural armor bonus, whichever of the two leads to a higher result.
>
> **Hit Dice:** Change the creature’s racial Hit Dice to d8s. All Hit Dice derived from class levels remain unchanged.
>
> **Defensive Abilities:** A child of Yog-Sothoth gains cold resistance 10 and fire resistance 10. It has spell resistance equal to its CR + 11, and has a +4 racial bonus on saving throws against mind-affecting effects. A child of Yog-Sothoth is immune to disease and poison.
>
> **Attacks:** While the abdominal tentacles of a child of Yog-Sothoth are merely unsightly sensory organs, the sucker-shaped mouth at the tip of its tail is a primary attack that the child can use as long as it is not concealing its features (see Special Qualities below). A hit with the tail deals bite damage as normal for a creature of the child’s size (1d6 points of damage for a Medium child).
>
> **Special Attacks:** A child of Yog-Sothoth gains the following special attacks.
>
> *Blood Drain (Ex): *A child of Yog-Sothoth can drain blood from a grappled or helpless foe via its tail mouth, dealing 1d2 points of Constitution damage per round it does so.
>
> **Spell-Like Abilities:** A child of Yog-Sothoth gains the following spell-like abilities (the save DCs of these abilities are calculated using the child’s Intelligence score as a result of its magic savant special quality, and its caster level equals its Hit Dice): 3/day comprehend languages, detect thoughts, hypnotism; 1/day invisibility; 1/week contact entity I. A child of Yog-Sothoth with 5 Hit Dice adds contact entity II to its 1/week spell-like abilities. A child of Yog-Sothoth with 9 Hit Dice adds contact entity III to its 1/week spell-like abilities. A child of Yog-Sothoth with 13 Hit Dice adds contact entity IV to its 1/week spell-like abilities. A child of Yog-Sothoth with 17 Hit Dice adds gate to its 1/week spell-like abilities.
>
> *Stench (Su):* A child of Yog-Sothoth always exudes an unpleasant scent. As a swift action, the child can intensify this scent, causing it to become truly nauseating. All living creatures within 30 feet must succeed at a Fortitude saving throw (DC = 10 + 1/2 the child’s HD + the child’s Constitution modifier) or become nauseated for 1 round. The child can exude this nauseating stench for a number of rounds per day equal to its total Hit Dice, but these rounds need not be consecutive. Each round the child wishes to maintain the stench, it must use a swift action to do so. The stench is a poison effect.
>
> **Special Qualities:** A child of Yog-Sothoth gains the following special quality.
>
> **Conceal Features:** A child of Yog-Sothoth gains a +8 racial bonus on checks to disguise itself as a typical member of the base creature’s species (although it always appears as a particularly sizable member of that race) if it takes the time to don clothing or armor to hide its monstrous qualities. When it does so, it loses access to all-around vision and can’t make its tail attack.
>
> **Magic Savant:** A child of Yog-Sothoth’s intrinsic understanding of magic allows it to modify the concentration checks and save DCs of its racial spell-like abilities (whether from the base creature or from this template) that are normally affected by Charisma to be modified instead by the child’s Intelligence modifier. This doesn’t affect actual spellcasting ability, such as that granted by sorcerer levels.
>
> **Weaknesses:** A child of Yog-Sothoth gains the following weakness.
>
> **Loathed:** Children of Yog-Sothoth are loathed by animals and psychopomps. Both types of creatures gain a +4 bonus on Perception checks and Sense Motive checks against a child of Yog-Sothoth, and receive a +2 morale bonus on attack rolls and weapon damage rolls against such targets.
>
> **Ability Scores:** Str +2, Con +4, Int +4, Cha –2.
>
> **Feats:** A child of Yog-Sothoth gains Toughness as a bonus feat.
>
> **Skills:** A child of Yog-Sothoth gains a +8 racial bonus on Disguise checks to appear as a typical specimen of the base creature when it is using its conceal features ability. All Knowledge skills and Spellcraft are class skills for a child of Yog-Sothoth; a child of Yog-Sothoth gains a +4 racial bonus on Knowledge (arcana) and Spellcraft checks.

**Mechanical encoding:** `changes`: 7 (showing first 5)
  - `2` → `str`  (untyped)
  - `4` → `skill.spl`  (untyped)
  - `4` → `skill.kar`  (untyped)
  - `4` → `con`  (untyped)
  - `4` → `int`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Chthonic
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9458 (PZO9458) p. 19
**Foundry id:** `TIsuPNyZbmvj0Jdx`

> **Usable with Summons** Yes - Requires the feat @UUID[Compendium.pf1.feats.Item.ezNxW33BtSafLl0J] or @UUID[Compendium.pf1.feats.Item.R5nnb83RW7qHkVmA]
>
> Chthonic creatures are native denizens of the Elemental Planes of Earth. They produce acid, which they use to help them burrow quickly through the dense rock of their homes. This template can be applied only to a non-outsider that has none of the following subtypes: air, cold, earth, fire, or water. A chthonic creature’s CR increases by 1 only if the base creature has 5 or more HD.
>
> **Rebuild Rules:** **Type** The creature gains the earth subtype; **Senses** gains darkvision 60 ft.; **Defensive Abilities** gains DR and resistance to acid as noted on the table below; **Speed** gains a burrow speed equal to half its highest speed (its tunnels always collapse behind it, and never leave behind a usable passage); **Attacks** gains bonus acid damage as noted on the table below on attacks with natural weapons.
>
>
> **Hit Dice**
>
>
> **DR**
>
>
> **Resist Acid**
>
>
> **Acid Damage**
>
>
> 1-4
>
>
> -
>
>
> 10
>
>
> 1 point
>
>
> 5-10
>
>
> 3/-
>
>
> 15
>
>
> 1d6
>
>
> 11+
>
>
> 5/-
>
>
> 20
>
>
> 2d6

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Cleric (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 246-247
**Foundry id:** `1JyzDvOVL6t9uw2K`

> As a conduit of divine power, a cleric creature is often viewed with great respect by its community. A cleric creature's CR increases by 2 if the creature has 7 or more HD, and it increases by 3 if the creature has 13 or more HD. A cleric creature must worship a deity (which must be determined when the template is added) and its alignment must be within one step of that deity's.
>
> **Quick Rules:** +2 on all rolls based on Wis; can @UUID[Compendium.pf1.class-abilities.Item.kXXz1lO4i7CibHJ9] a number of times per day equal to 3 + its Cha modifier (positive if good, negative if evil, choose if neutral; using its HD – 2 as its cleric level to determine the effect and DC, minimum 1); can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.W4PGylYL7ghRfy5G] (see the Cleric, Druid, and Wizard Spell Slots table on @Source[PZO1130;pages=251]) using its HD as its CL.
>
> **Rebuild Rules:** **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.kXXz1lO4i7CibHJ9] (can be used a number of times per day equal to 3 + is Cha modifier—positive if good, negative if evil, choose if neutral—using its HD – 2 as its cleric level to determine effect and DC, minimum 1); **Cleric Spells** can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.W4PGylYL7ghRfy5G] (see the Cleric, Druid, and Wizard Spell Slots table on @Source[PZO1130;pages=251]) using its HD as its CL; **Ability Scores** +4 Wisdom.
>
> **Cleric, Druid, and Wizard Spells Slots**
>
>
> **HD**
>
>
> **0**
>
>
> **1**
>
>
> **2**
>
>
> **3**
>
>
> **4**
>
>
> **5**
>
>
> **6**
>
>
> **7**
>
>
> **8**
>
>
> **9**
>
>
> 1-3
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 4-6
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 7-9
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 10-12
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 13-15
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 16-18
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> 19-21
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> 22-24
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> 25+
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1

**Mechanical encoding:** `changes`: 3
  - `2` → `wisSkills`  (untyped)
  - `2` → `will`  (untyped)
  - `2` → `wisChecks`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Cleric (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 246-247
**Foundry id:** `wrOqo5s22hCwZJzo`

> As a conduit of divine power, a cleric creature is often viewed with great respect by its community. A cleric creature's CR increases by 2 if the creature has 7 or more HD, and it increases by 3 if the creature has 13 or more HD. A cleric creature must worship a deity (which must be determined when the template is added) and its alignment must be within one step of that deity's.
>
> **Quick Rules:** +2 on all rolls based on Wis; can @UUID[Compendium.pf1.class-abilities.Item.kXXz1lO4i7CibHJ9] a number of times per day equal to 3 + its Cha modifier (positive if good, negative if evil, choose if neutral; using its HD – 2 as its cleric level to determine the effect and DC, minimum 1); can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.W4PGylYL7ghRfy5G] (see the Cleric, Druid, and Wizard Spell Slots table on @Source[PZO1130;pages=251]) using its HD as its CL.
>
> **Rebuild Rules:** **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.kXXz1lO4i7CibHJ9] (can be used a number of times per day equal to 3 + is Cha modifier—positive if good, negative if evil, choose if neutral—using its HD – 2 as its cleric level to determine effect and DC, minimum 1); **Cleric Spells** can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.W4PGylYL7ghRfy5G] (see the Cleric, Druid, and Wizard Spell Slots table on @Source[PZO1130;pages=251]) using its HD as its CL; **Ability Scores** +4 Wisdom.
>
> **Cleric, Druid, and Wizard Spells Slots**
>
>
> **HD**
>
>
> **0**
>
>
> **1**
>
>
> **2**
>
>
> **3**
>
>
> **4**
>
>
> **5**
>
>
> **6**
>
>
> **7**
>
>
> **8**
>
>
> **9**
>
>
> 1-3
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 4-6
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 7-9
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 10-12
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 13-15
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 16-18
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> 19-21
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> 22-24
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> 25+
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1

**Mechanical encoding:** `changes`: 1
  - `4` → `wis`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Colour-Blighted
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 39
**Foundry id:** `LuYsx4C0NbXm79WU`

> A creature with the colour-blighted simple template appears hideously deformed and glows with the same unnamable color as the creature that blighted it. A colour-blighted creature's quick and rebuild rules are the same.
>
> **Rebuild Rules:** A colour-blighted creature's ability scores suffer drain as a result of being fed upon by a colour out of space, but once a creature gains this template, it becomes immune to further feed attacks from colours out of space until it loses the colour-blighted simple template. A Charisma score drained to 0 by a colour out of space's feed attack is raised to 1; other ability scores are not altered. In order to remove this simple template from a creature, one need only restore all of its drained ability scores to normal. As long as a creature suffers the colour-blighted template, it becomes strangely aggressive toward creatures that do not exude the colors of a colour out of space, and gains a +1 bonus on attack rolls and weapon damage rolls against such targets. Every 24 hours, a creature suffering from this simple template must make a DC 12 Fortitude save to resist crumbling into fine white ash—such a doom means instant death and, for many color-blighted creatures, their only chance at escape from a life filled with pain.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Commando Construct
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `EAB0ehDcASqXl5J6`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Commando constructs are elite fighting machines that often operate alone or in small squads. Although they are skilled combatants, these constructs can handle a variety of clandestine activities, including assassination, infiltration, kidnapping, and sabotage. They are most often found wandering the plains of Numeria, or under the service of a local warlord.
>
> "Commando construct" is an acquired template that can be added to any construct, referred to hereafter as the base creature.
>
> **Challenge Rating:** If the base creature has 9 or fewer HD, base creature’s CR + 1; if base creature has 10 or more HD, base creature’s CR + 2.
>
> **Type:** A commando construct gains the augmented subtype. It uses all the base creature’s statistics and special abilities except as noted here.
>
> **Armor Class:** A commando construct’s natural armor bonus increases by 4.
>
> **Hit Dice:** Change the commando construct’s Hit Dice to d12s. Additionally, a commando construct gains 1-1/2 times the normal bonus hit points for a construct of its size.
>
> **Special Attacks:** A commando construct gains special attacks chosen from the list below. A commando construct with 8 HD or fewer selects one option, a commando construct with 9–12 HD selects two options, and a commando construct with 13 HD or more selects three options. Each option can be selected only once.
>
> *Brutal Attacks (Ex):* When a commando construct makes two successful melee attacks against the same target in 1 round, its attacks either rend flesh or crush bones. This deals an additional amount of damage equal to the damage dealt by its highest-damage successful melee attack plus twice the commando construct’s Strength modifier.
>
> *Energy Attacks (Su):* Pick one energy type: acid, cold, electricity, or fire. Each of the commando construct’s melee attacks deals 1d6 points of energy damage of the chosen type on a hit.
>
> *Extra Attack (Ex):* When using the full-attack action, a commando construct can make one extra attack per round at its highest base attack bonus.
>
> *Knockdown Strike (Ex): *When a commando construct makes a successful melee attack, it can forgo dealing its normal damage to its target and instead attempt a free combat maneuver check. If the construct is successful, the target takes damage equal to the commando construct’s Strength modifier and is knocked prone. This is treated as a trip attack for the purpose of creatures that can’t be tripped or that have bonuses or weaknesses against trip combat maneuvers. On a failed combat maneuver check, the commando construct is not tripped in return. This ability works only on creatures of a size equal to or smaller than the commando construct.
>
> *Knockout Strike (Ex):* As a full-attack action, a commando construct can unleash a devastating strike with one of its melee attacks that can instantly knock a target unconscious. If a commando construct hits and the target takes damage from the attack, the target must succeed at a Fortitude save (DC = 10 + half the commando construct’s HD + the commando construct’s Strength modifier) or fall unconscious for 1d6 rounds. Each round on its turn, the unconscious target can attempt a new saving throw to regain consciousness. Creatures immune to critical hits or nonlethal damage are immune to this ability.
>
> *Precision (Ex):* A commando construct rolls twice to confirm critical hits, taking the more favorable result.
>
> *Reach (Ex):* The reach of all of a commando construct’s melee attacks increases by 5 feet.
>
> *Retaliatory Strike (Ex): *Whenever an enemy makes a successful melee attack against a commando construct or an adjacent ally, the enemy provokes an attack of opportunity from the commando construct.
>
> *Sneak Attack (Ex):* As per the rogue class feature. The number of additional sneak attack dice is based on the commando creature’s Hit Dice.
>
> *Sundering Blows (Ex):* Whenever a commando construct confirms a critical hit with a melee attack, it deals an amount of damage to the target’s armor or shield equal to the melee damage as if it had also succeeded at a sunder combat maneuver.
>
> **Ability Scores:** Str +4, Dex +4.
>
> **Feats:** A commando construct gains one bonus combat feat, plus an additional combat feat for every 4 HD (to a maximum of 10 feats from this ability).
>
> **Special Qualities:** A commando construct gains following special abilities.
>
> *Energized Alacrity (Su):* Once per minute as a swift action, a commando construct can draw power from special energizing transmitters attached to its body. When doing so, the commando construct gains a +30-foot bonus to all of its speeds for 1 round. Additionally, when making a full attack during this round, the commando construct can move up to its speed either before or after it attacks. This movement provokes attacks of opportunity as normal.
>
> *Tactical Awareness (Ex): *A commando construct gains a +2 bonus on initiative checks. This bonus increases by 1 for every 5 HD the commando construct has (to a maximum of +6 at 20 HD). Additionally, a commando construct is never considered an unaware combatant and is always able to act in the surprise round. A commando construct is still flat-footed in the surprise round until it acts.
>
> #### Construction
>
> A commando construct’s materials cost an additional 10,000 gp above the base creature’s cost. The Craft check required to make the body has a DC 4 higher than normal for the base construct’s kind. The construct is animated using a special laboratory or workroom that costs 1,000 gp to establish. If the creator is personally constructing the creature’s body, the crafting and the ritual can be performed simultaneously. The creator must have a minimum caster level 1 higher than the base creature’s minimum required caster level. In addition, the following spells must be cast during the ritual: bull’s strength, greater heroism, and limited wish.

**Mechanical encoding:** `changes`: 3
  - `4` → `str`  (untyped)
  - `4` → `nac`  (untyped)
  - `4` → `dex`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Counterpoised
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `M8xes1clRb7IzKfE`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** Yes - Requires the feat Summon Neutral Monster
>
> Counterpoised creatures dwell in the Outer Planes where balance between elements or ideologies is paramount, but they can be summoned using spells such as summon monster and planar ally. A counterpoised creature’s CR increases by 1 only if the base creature has 5 or more Hit Dice. A counterpoised creature’s quick and rebuild rules are the same.
>
> **Rebuild Rules:** Senses gains darkvision 60 ft.; Defensive Abilities gains DR and energy resistance as noted on the table; SR gains SR equal to new CR +5; Special Attacks smite bias 1/day as a swift action (adds Cha bonus to attack rolls and damage bonus equal to HD against a foe that is chaotic evil, chaotic good, lawful evil, or lawful good; smite persists until the target is dead or the counterpoised creature rests).
>
>
>
>
>  **Hit Dice** 
>  **Resist Cold, Electricity, and Fire** 
>  **DR** 
>
>
>  1-4 
>  5 
>  — 
>
>
>  5-10 
>  10 
>  5/adamantine 
>
>
>  11+ 
>  15 
>  10/adamantine

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Cytillesh Zombie
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `TSLnxMdrpIU98IFm`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** Yes
>
> The cytillesh zombies presented here use a hybrid monster template that is easy to duplicate. The base creature gains the fast zombie template presented on page 289 of the Pathfinder RPG Bestiary. It also gains +4 Turn Resistance and Cytillesh Symbiosis (see the Cytillesh Zombie stat block). The cytillesh zombie template increases a zombie’s challenge rating by 1. In the context of this adventure, this template can only be added to a creature suffering the effects of exposure to cytillesh fungus that imbibes concentrated cytillesh with caphorite and lazurite granules (see area B12).

**Mechanical encoding:** `changes`: 2
  - `2` → `dex`  (untyped)
  - `10` → `landSpeed`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Dark Ice (3.5)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `Wnb8EezV7vfJMJjh`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Under the influence of the cold rider, the frigid clutch of winter’s malice entered the hearts of Syntira’s fey and transformed them to ice. Now, empowered by the cold hate of the Witch Queen, her former companions are ready to exact a brutal vengeance against the people of Falcon’s Hollow.
>
> "Dark ice creature" is an acquired template that can be added to any fey without the fire subtype (hereafter referred to as the base creature). A dark ice creature uses all of the base creature’s statistics except as noted here.
>
> **Size and Type:** The creature’s type is unchanged, but it gains the cold subtype. Its size is unchanged.
>
> **AC:** A dark ice creature’s natural armor bonus improves by +4, as a layer of thick permafrost toughens its now leathery skin and coats its body with a thin but durable shell of ice.
>
> **Defensive Abilities:** A dark ice creature retains the base creature’s defensive abilities and gains the following.
>
> *Fast Healing (Su): *As long as a dark ice creature is in contact with ice or snow it heals 3 hit points per round.
>
> *Immunity to Cold (Ex):* A dark ice creature is immune to cold.
>
> **Weaknesses:** A dark ice creature retains the base creature’s weaknesses and gains the following.
>
> *Fire vulnerability (Ex)* A dark ice creature takes 1-1/2 times as much damage from fire.
>
> **Attack:** A dark ice creature grows jagged oversized icicle talons in place of fingers, paws, or hooves, and it gains two vicious claw attacks if it did not already have them.
>
> **Damage:** Use the damage below or the base creature’s claw damage, whichever is better.
>
>
>
>
>  **Size** 
>  **Claw Damage** 
>
>
>  Fine 
>  1 
>
>
>  Diminutive 
>  1d2 
>
>
>  Tiny 
>  1d3 
>
>
>  Small 
>  1d4 
>
>
>  Medium 
>  1d6 
>
>
>  Large 
>  1d8 
>
>
>  Huge 
>  2d6 
>
>
>  Gargantuan 
>  3d6 
>
>
>  Colossal 
>  4d6 
>
>
>
>
> **Special Attacks:** A dark ice creature retains the base creature’s special attacks and gains the ones listed below:
>
> *Frigid Touch (Su)* Once per day, a dark ice creature may make a touch attack against a foe to deal 1d6 points of Dexterity damage by freezing its blood in its veins and numbing its bones.
>
> *Frosty Grasp (Su)* A dark ice creature’s natural attacks, as well as any weapons it wields, deal an additional 1d6 points of cold damage.
>
> **Abilities:** A dark ice creature’s ability scores are modified as follows: Str +2, Con +2.
>
> **Environment:** Any cold.
>
> **Challenge Rating:** As base creature +1.
>
> **Alignment:** Always evil (any).

**Mechanical encoding:** `changes`: 3
  - `4` → `nac`  (untyped)
  - `2` → `str`  (untyped)
  - `2` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Dark
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9458 (PZO9458) p. 19
**Foundry id:** `8wcgAdUOucEtYJcD`

> **Usable with Summons** Yes - Requires the feat @UUID[Compendium.pf1.feats.Item.ezNxW33BtSafLl0J] or @UUID[Compendium.pf1.feats.Item.R5nnb83RW7qHkVmA]
>
> Dark creatures are native denizens of the Plane of Shadow, and generally have a dark gray or deep purple coloration. This template can be applied only to a non-outsider that has none of the following subtypes: air, cold, earth, fire, or water. A dark creature’s CR increases by 1 only if the base creature has 5 or more HD.
>
> **Rebuild Rules:** **Senses** gain darkvision 60 ft. and low-light vision; **Defensive Abilities** gains DR and resistance to cold and electricity based on its Hit Dice, as noted on the table below; **SR** gains SR equal to its new CR + 5.
>
>
> **Hit Dice**
>
>
> **DR**
>
>
> **Resist Cold and Electricity**
>
>
> 1-4
>
>
> -
>
>
> 5
>
>
> 5-10
>
>
> 5/Magic
>
>
> 10
>
>
> 11+
>
>
> 10/magic
>
>
> 15
>
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.n9WbBGBZn808WtfE inline=true]

**Mechanical encoding:** `changes`: 1
  - `@details.cr.total + 5` → `spellResist`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Deep Creature (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `sFoAenfeqwUBbc67`

> **Acquired/Inherited Template** Acquired
>
> **Simple Template** Yes**Usable with Summons** No
>
> Deep creatures have been twisted by the deep ones, whether through interbreeding or foul rituals.
>
> **Quick Rules:** +8 on Swim checks and can always take 10 on Swim checks; swim speed equal to base land speed; +1 to AC; +1 on rolls based on Con or Wis; +1 hp/HD; two claw attacks that each deal 1d4 points of damage (for Medium creatures); amphibious.
>
> **Rebuild Rules:** Type gain the aquatic and deep one subtypes; AC natural armor increases by 1; Speed swim speed equal to base land speed; Melee two claw attacks that each deal 1d4 points of damage (for Medium creatures); Special Qualities amphibious; Ability Scores +2 Str, +2 Con, +2 Wis.

**Mechanical encoding:** `changes`: 9 (showing first 5)
  - `1` → `wisChecks`  (untyped)
  - `8` → `skill.swm`  (untyped)
  - `1` → `conChecks`  (untyped)
  - `1` → `wisSkills`  (untyped)
  - `1` → `fort`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Deep Creature (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `c33Zy5DJAhatfl1D`

> **Acquired/Inherited Template** Acquired
>
> **Simple Template** Yes**Usable with Summons** No
>
> Deep creatures have been twisted by the deep ones, whether through interbreeding or foul rituals.
>
> **Quick Rules:** +8 on Swim checks and can always take 10 on Swim checks; swim speed equal to base land speed; +1 to AC; +1 on rolls based on Con or Wis; +1 hp/HD; two claw attacks that each deal 1d4 points of damage (for Medium creatures); amphibious.
>
> **Rebuild Rules:** Type gain the aquatic and deep one subtypes; AC natural armor increases by 1; Speed swim speed equal to base land speed; Melee two claw attacks that each deal 1d4 points of damage (for Medium creatures); Special Qualities amphibious; Ability Scores +2 Str, +2 Con, +2 Wis.

**Mechanical encoding:** `changes`: 4
  - `2` → `wis`  (untyped)
  - `2` → `str`  (untyped)
  - `1` → `nac`  (untyped)
  - `2` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Degenerate (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `zfZ7M3PGgvWeolOz`

> **Acquired/Inherited Template** Acquired
>
> **Simple Template** Yes**Usable with Summons** No
>
> Degenerate creatures are weaker than their ordinary cousins.
>
> **Quick Rules:** -2 on all rolls (including damage rolls) and to special ability DCs; -2 to AC and CMD; -2 hp/HD.
>
> **Rebuild Rules:** Ability Scores -4 to all ability scores (minimum 1).

**Mechanical encoding:** `changes`: 8 (showing first 5)
  - `-2` → `wdamage`  (untyped)
  - `-2` → `allSavingThrows`  (untyped)
  - `-2` → `attack`  (untyped)
  - `-2` → `ac`  (untyped)
  - `-2` → `allChecks`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Degenerate (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `EPXBZkhH1VrHetJX`

> **Acquired/Inherited Template** Acquired
>
> **Simple Template** Yes**Usable with Summons** No
>
> Degenerate creatures are weaker than their ordinary cousins.
>
> **Quick Rules:** -2 on all rolls (including damage rolls) and to special ability DCs; -2 to AC and CMD; -2 hp/HD.
>
> **Rebuild Rules:** Ability Scores -4 to all ability scores (minimum 1).

**Mechanical encoding:** `changes`: 6 (showing first 5)
  - `-4` → `con`  (untyped)
  - `-4` → `str`  (untyped)
  - `-4` → `wis`  (untyped)
  - `-4` → `cha`  (untyped)
  - `-4` → `dex`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Demonic Vermin
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `NP6VVchHAFS75Eh5`

> **Acquired/Inherited Template** Both**Simple Template** No**Usable with Summons** No
>
> Deskari’s influence upon the Worldwound’s verminous life cannot be ignored for long by visitors to this tainted land. While some giant vermin have resisted Deskari’s influence, most have succumbed to it. Such creatures are almost always encountered along the Worldwound’s periphery. As one travels deeper into the blighted land, the immense insects, spiders, and other vermin encountered in the canyons and rivers take on an increasingly unsettling intelligence and demonic features. In many ways, these demonic vermin are no longer true denizens of the Material Plane—they are, after a fact, what happens when the chaos and evil of the Abyss infuse a mindless creature. They are the unholy spawn of vermin—and mortal sins.
>
> Countless variations of demonic vermin exist in the forbidding wasteland that is the Worldwound. When a nest of similar monsters is encountered, they all typically share the same demonic powers and traits, but another nest of the same species could exhibit entirely different abilities, depending on the nature of the Abyssal energies that have corrupted and transformed them. Uncorrupted giant vermin that wander into or are otherwise brought into the Worldwound do not immediately fall victim to this vile transformation, but several months of exposure can, at the GM’s whim, cause such creatures to spontaneously transform into one of these hideous monstrosities.
>
> "Demonic vermin" is an inherited or acquired template that can be added to any vermin (hereafter referred to as the base creature). A demonic vermin retains all the base creature’s statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature +1.
>
> **Alignment:** Chaotic evil.
>
> **Type:** The creature’s type changes to magical beast. Do not recalculate HD, BAB, or saves. While a demonic vermin is not an outsider, it is treated as if it had the demon subtype for the purposes of resolving all effects relating to that subtype.
>
> **Armor Class:** Natural armor improves by +2.
>
> **Special Qualities and Defenses:** A demonic vermin gains immunity to electricity and poison and resistance to acid 10, cold 10, and fire 10. It also gains DR 5/cold iron (if 11 HD or less) or DR 10/cold iron (if 12 HD or more). As demonic vermin are intelligent, they lose the mindless trait.
>
> **Melee:** A demonic vermin’s natural weapons are unchanged, but they are treated as chaotic and evil for the purpose of resolving damage reduction.
>
> **Special Attacks:** A demonic vermin retains all the special attacks of the base creature. In addition, it gains one of the following special abilities of your choosing— you can, of course, invent different abilities of your own as well. The save DC for any of these attacks is equal to 10 + 1/2 the demonic vermin’s HD + the demonic vermin’s Constitution modifier.
>
> *Abyssal Energy (Su): *Choose one of the following energy types—acid, fire, or cold. The demonic vermin gains immunity to that energy type, and also gains a breath weapon that inflicts that type of energy damage. This breath weapon is a 60-foot-line, and deals 1d6 points of damage per CR point possessed by the demonic vermin (Reflex save halves). It can be used once every 1d4 rounds.
>
> *Additional Senses (Ex):* The vermin has a large number of extra eyes and other sensory organs. It gains all-around vision, scent, and a +8 racial bonus on Perception checks.
>
> *Death Throes (Su): *When the vermin is slain, it can make a single melee attack (using any one of its natural attacks) as an immediate action. It then explodes into acid, fire, electricity, or cold (your choice), dealing 1d6 points of damage per CR point possessed by the demonic vermin (Reflex save halves).
>
> *Diseased (Su): *The demonic vermin is immune to disease, and its natural attacks inflict demonplague (see page 29) on a hit (Fortitude save negates).
>
> *Drone (Su): *By rubbing its wings or limbs together as a standard action, the demonic vermin produces a loud, discordant drone that causes those within 30 feet of it to become sickened (if the vermin is CR 8 or less) or confused (if the vermin is CR 9 or higher) for 1d6 rounds (Will save negates). This is a sonic mind-affecting effect.
>
> *Skitter (Ex): *The creature has uncanny speed and erratic movements. The vermin’s speeds all increase by 10 feet, it gains Mobility and Spring Attack as bonus feats, and it gains a +4 racial bonus on Initiative checks.
>
> **Spell-Like Abilities:** In addition to gaining one of the special attacks listed here, all demonic vermin gain access to a limited number of spell-like abilities, depending on its Hit Dice. Each ability is usable once per day. Caster level equals the creature’s CR.
>
>
>
>
>  **CR** 
>  **Abilities** 
>
>
>  1–4 
>  *darkness* 
>
>
>  5–8 
>  *vomit swarm*APG 
>
>
>  9–12 
>  *insect plague* 
>
>
>  13–16 
>  *greater teleport* (self plus 50 lbs. of objects only) 
>
>
>  17–20 
>  *earthquake* 
>
>
>
>
> **Abilities:** Str +4, Con +2. A demonic vermin’s Intelligence becomes 10 and its Charisma becomes 15 (unless the base creature has higher values, in which case they remain unchanged).**Feats: A demonic vermin gains feats as appropriate for its Hit Dice, and gains Toughness as a bonus feat.
>
> Skills:** A demonic vermin has skill points per racial Hit Die equal to 4 + its Intelligence modifier. The following are class skills for demonic vermin: Acrobatics, Bluff, Climb, Fly, Knowledge (planes), Perception, Sense Motive, and Stealth.
>
> **Languages:** A demonic vermin speaks Abyssal, Celestial, and Draconic. It also gains telepathy to a distance of 100 feet.

**Mechanical encoding:** `changes`: 3
  - `2` → `con`  (untyped)
  - `2` → `nac`  (untyped)
  - `4` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Devilbound (Accuser)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 56-57
**Foundry id:** `Qw1reTTMiymJbFt6`

> A devilbound creature has made a bargain with a devil, promising a service and its soul in exchange for infernal power. The specific service depends on the devil's type and motivations, but always furthers the interests of Hell.
>
> "Devilbound creature" is an acquired template that can be added to any creature with 5 or more Hit Dice and Intelligence, Wisdom, and Charisma scores of 3 or higher (referred to hereafter as the base creature). The creature retains all the base creature's statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature +1.
>
> **Alignment:** Any evil. A devilbound creature radiates an evil aura as if it were an evil outsider.
>
> **Senses:** A devilbound creature gains darkvision 60 ft. and the see in darkness ability.
>
> **Armor Class:** Natural armor improves by +4.
>
> **Defensive Abilities:** A devilbound creature gains a +4 bonus on saving throws against poison, resist fire 30, and regeneration 5 (good spells, good weapons).
>
> **Weaknesses:** The devil-bound creature gains the following weakness.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.nuAhCqqdWT8H45r5 inline=true]
>
> **Special Attacks:** The creature gains the summon universal monster ability and can summon a devil once per day with a 100% chance of success. The devil remains for 1 hour. The creature's caster level or Hit Dice, whichever is higher, determines the most powerful kind of devil it can summon and the effective spell level of this ability, according to the following table.**
>
>
>
> Caster Level**
>
>
> **Devil**
>
>
> **Spell Level**
>
>
> 3rd
>
>
> Lemure
>
>
> 2nd
>
>
> 9th
>
>
> Bearded devil
>
>
> 5th
>
>
> 11th
>
>
> Erinyes
>
>
> 6th
>
>
> 13th
>
>
> Bone devil
>
>
> 7th
>
>
> 15th
>
>
> Barbed devil
>
>
> 8th
>
>
> 17th
>
>
> Ice devil
>
>
> 9th
>
>
> **Spell-Like Abilities:** The creature gains the following spell-like abilities, depending on the kind of devil it is bound to. The creature uses its Hit Dice or caster level, whichever is higher, as the caster level for its spell-like abilities. Save DCs are based on the creature's Intelligence, Wisdom, or Charisma, whichever is highest.
>
> *Accuser*: 3/day—@UUID[Compendium.pf1.spells.Item.6kmkxepwgsbta6ui], @UUID[Compendium.pf1.spells.Item.oylikodnyku2zewu] (self only), @UUID[Compendium.pf1.spells.Item.vxi9c3xwa83xthka]
>
> **Abilities:** Adjust the base creature's ability scores according to the kind of devil it is bound to.
>
>
> **Devil**
>
>
> **Str**
>
>
> **Dex**
>
>
> **Con**
>
>
> **Int**
>
>
> **Wis**
>
>
> **Cha**
>
>
> Accuser
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> Barbed, bearded, host
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> Belier
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Bone, ice
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> Contract, handmaiden
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Drowning, horned
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> Erinyes
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Immolation
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Imp
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> Nemesis, pit fiend
>
>
> +2 to any three different ability scores

**Mechanical encoding:** `changes`: 4
  - `2` → `con`  (untyped)
  - `2` → `dex`  (untyped)
  - `4` → `nac`  (untyped)
  - `2` → `wis`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Devilbound (Barbed, Bearded, Host)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 56-57
**Foundry id:** `2lQeCSOS4Jivf65m`

> A devilbound creature has made a bargain with a devil, promising a service and its soul in exchange for infernal power. The specific service depends on the devil's type and motivations, but always furthers the interests of Hell.
>
> "Devilbound creature" is an acquired template that can be added to any creature with 5 or more Hit Dice and Intelligence, Wisdom, and Charisma scores of 3 or higher (referred to hereafter as the base creature). The creature retains all the base creature's statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature +1.
>
> **Alignment:** Any evil. A devilbound creature radiates an evil aura as if it were an evil outsider.
>
> **Senses:** A devilbound creature gains darkvision 60 ft. and the see in darkness ability.
>
> **Armor Class:** Natural armor improves by +4.
>
> **Defensive Abilities:** A devilbound creature gains a +4 bonus on saving throws against poison, resist fire 30, and regeneration 5 (good spells, good weapons).
>
> **Weaknesses:** The devil-bound creature gains the following weakness.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.nuAhCqqdWT8H45r5 inline=true]
>
> **Special Attacks:** The creature gains the summon universal monster ability and can summon a devil once per day with a 100% chance of success. The devil remains for 1 hour. The creature's caster level or Hit Dice, whichever is higher, determines the most powerful kind of devil it can summon and the effective spell level of this ability, according to the following table.**
>
>
>
> Caster Level**
>
>
> **Devil**
>
>
> **Spell Level**
>
>
> 3rd
>
>
> Lemure
>
>
> 2nd
>
>
> 9th
>
>
> Bearded devil
>
>
> 5th
>
>
> 11th
>
>
> Erinyes
>
>
> 6th
>
>
> 13th
>
>
> Bone devil
>
>
> 7th
>
>
> 15th
>
>
> Barbed devil
>
>
> 8th
>
>
> 17th
>
>
> Ice devil
>
>
> 9th
>
>
> **Spell-Like Abilities:** The creature gains the following spell-like abilities, depending on the kind of devil it is bound to. The creature uses its Hit Dice or caster level, whichever is higher, as the caster level for its spell-like abilities. Save DCs are based on the creature's Intelligence, Wisdom, or Charisma, whichever is highest.
>
> *Barbed*: 3/day—@UUID[Compendium.pf1.spells.Item.d8hypv6zdyan3rzr]
>
> *Bearded*: 3/day—@UUID[Compendium.pf1.spells.Item.ojwg1ki98tq8xyh9], @UUID[Compendium.pf1.spells.Item.8u1xa5javcxc6szk]
>
> *Host*: 3/day—@UUID[Compendium.pf1.spells.Item.ojwg1ki98tq8xyh9], @UUID[Compendium.pf1.spells.Item.7d6sv5ecvi7kho3m]
>
> **Abilities:** Adjust the base creature's ability scores according to the kind of devil it is bound to.
>
>
> **Devil**
>
>
> **Str**
>
>
> **Dex**
>
>
> **Con**
>
>
> **Int**
>
>
> **Wis**
>
>
> **Cha**
>
>
> Accuser
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> Barbed, bearded, host
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> Belier
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Bone, ice
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> Contract, handmaiden
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Drowning, horned
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> Erinyes
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Immolation
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Imp
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> Nemesis, pit fiend
>
>
> +2 to any three different ability scores

**Mechanical encoding:** `changes`: 4
  - `2` → `con`  (untyped)
  - `2` → `str`  (untyped)
  - `4` → `nac`  (untyped)
  - `2` → `dex`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Devilbound (Belier, Contract, Handmaiden)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 56-57
**Foundry id:** `CyYvckGaQFUB5NkU`

> A devilbound creature has made a bargain with a devil, promising a service and its soul in exchange for infernal power. The specific service depends on the devil's type and motivations, but always furthers the interests of Hell.
>
> "Devilbound creature" is an acquired template that can be added to any creature with 5 or more Hit Dice and Intelligence, Wisdom, and Charisma scores of 3 or higher (referred to hereafter as the base creature). The creature retains all the base creature's statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature +1.
>
> **Alignment:** Any evil. A devilbound creature radiates an evil aura as if it were an evil outsider.
>
> **Senses:** A devilbound creature gains darkvision 60 ft. and the see in darkness ability.
>
> **Armor Class:** Natural armor improves by +4.
>
> **Defensive Abilities:** A devilbound creature gains a +4 bonus on saving throws against poison, resist fire 30, and regeneration 5 (good spells, good weapons).
>
> **Weaknesses:** The devil-bound creature gains the following weakness.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.nuAhCqqdWT8H45r5 inline=true]
>
> **Special Attacks:** The creature gains the summon universal monster ability and can summon a devil once per day with a 100% chance of success. The devil remains for 1 hour. The creature's caster level or Hit Dice, whichever is higher, determines the most powerful kind of devil it can summon and the effective spell level of this ability, according to the following table.
>
>
> **Caster Level**
>
>
> **Devil**
>
>
> **Spell Level**
>
>
> 3rd
>
>
> Lemure
>
>
> 2nd
>
>
> 9th
>
>
> Bearded devil
>
>
> 5th
>
>
> 11th
>
>
> Erinyes
>
>
> 6th
>
>
> 13th
>
>
> Bone devil
>
>
> 7th
>
>
> 15th
>
>
> Barbed devil
>
>
> 8th
>
>
> 17th
>
>
> Ice devil
>
>
> 9th
>
>
> **Spell-Like Abilities:** The creature gains the following spell-like abilities, depending on the kind of devil it is bound to. The creature uses its Hit Dice or caster level, whichever is higher, as the caster level for its spell-like abilities. Save DCs are based on the creature's Intelligence, Wisdom, or Charisma, whichever is highest.
>
> *Belier*: 3/day—@UUID[Compendium.pf1.spells.Item.smbkd2yobhshbpqf]
>
> *Contract*: 3/day—@UUID[Compendium.pf1.spells.Item.lsboosfk26m0ycqv], @UUID[Compendium.pf1.spells.Item.xllxylvvqr82o2d5], @UUID[Compendium.pf1.spells.Item.vl2mznu91c3efcam]
>
> *Handmaiden*: 3/day—@UUID[Compendium.pf1.spells.Item.wralcmyi4tdcai24]; 1/day—@UUID[Compendium.pf1.spells.Item.jbqo4o2b2tmdz7wv]
>
> **Abilities:** Adjust the base creature's ability scores according to the kind of devil it is bound to.
>
>
> **Devil**
>
>
> **Str**
>
>
> **Dex**
>
>
> **Con**
>
>
> **Int**
>
>
> **Wis**
>
>
> **Cha**
>
>
> Accuser
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> Barbed, bearded, host
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> Belier
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Bone, ice
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> Contract, handmaiden
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Drowning, horned
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> Erinyes
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Immolation
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Imp
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> Nemesis, pit fiend
>
>
> +2 to any three different ability scores

**Mechanical encoding:** `changes`: 4
  - `2` → `cha`  (untyped)
  - `2` → `wis`  (untyped)
  - `4` → `nac`  (untyped)
  - `2` → `int`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Devilbound (Bone, Ice)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 56-57
**Foundry id:** `770YBD41hLiYnQsi`

> A devilbound creature has made a bargain with a devil, promising a service and its soul in exchange for infernal power. The specific service depends on the devil's type and motivations, but always furthers the interests of Hell.
>
> "Devilbound creature" is an acquired template that can be added to any creature with 5 or more Hit Dice and Intelligence, Wisdom, and Charisma scores of 3 or higher (referred to hereafter as the base creature). The creature retains all the base creature's statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature +1.
>
> **Alignment:** Any evil. A devilbound creature radiates an evil aura as if it were an evil outsider.
>
> **Senses:** A devilbound creature gains darkvision 60 ft. and the see in darkness ability.
>
> **Armor Class:** Natural armor improves by +4.
>
> **Defensive Abilities:** A devilbound creature gains a +4 bonus on saving throws against poison, resist fire 30, and regeneration 5 (good spells, good weapons).
>
> **Weaknesses:** The devil-bound creature gains the following weakness.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.nuAhCqqdWT8H45r5 inline=true]
>
> **Special Attacks:** The creature gains the summon universal monster ability and can summon a devil once per day with a 100% chance of success. The devil remains for 1 hour. The creature's caster level or Hit Dice, whichever is higher, determines the most powerful kind of devil it can summon and the effective spell level of this ability, according to the following table.
>
>
> **Caster Level**
>
>
> **Devil**
>
>
> **Spell Level**
>
>
> 3rd
>
>
> Lemure
>
>
> 2nd
>
>
> 9th
>
>
> Bearded devil
>
>
> 5th
>
>
> 11th
>
>
> Erinyes
>
>
> 6th
>
>
> 13th
>
>
> Bone devil
>
>
> 7th
>
>
> 15th
>
>
> Barbed devil
>
>
> 8th
>
>
> 17th
>
>
> Ice devil
>
>
> 9th
>
>
> **Spell-Like Abilities:** The creature gains the following spell-like abilities, depending on the kind of devil it is bound to. The creature uses its Hit Dice or caster level, whichever is higher, as the caster level for its spell-like abilities. Save DCs are based on the creature's Intelligence, Wisdom, or Charisma, whichever is highest.
>
> *Bone*: 3/day—@UUID[Compendium.pf1.spells.Item.7d6sv5ecvi7kho3m], @UUID[Compendium.pf1.spells.Item.oylikodnyku2zewu] (self only)
>
> *Ice*: 3/day—@UUID[Compendium.pf1.spells.Item.pkm8um5t1cxsn6jh], @UUID[Compendium.pf1.spells.Item.t1uhggjfimtabp4v]
>
> **Abilities:** Adjust the base creature's ability scores according to the kind of devil it is bound to.
>
>
> **Devil**
>
>
> **Str**
>
>
> **Dex**
>
>
> **Con**
>
>
> **Int**
>
>
> **Wis**
>
>
> **Cha**
>
>
> Accuser
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> Barbed, bearded, host
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> Belier
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Bone, ice
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> Contract, handmaiden
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Drowning, horned
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> Erinyes
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Immolation
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Imp
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> Nemesis, pit fiend
>
>
> +2 to any three different ability scores

**Mechanical encoding:** `changes`: 4
  - `4` → `nac`  (untyped)
  - `2` → `int`  (untyped)
  - `2` → `con`  (untyped)
  - `2` → `wis`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Devilbound (Drowning, Horned)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 56-57
**Foundry id:** `mZjb8U31UXiJNYZt`

> A devilbound creature has made a bargain with a devil, promising a service and its soul in exchange for infernal power. The specific service depends on the devil's type and motivations, but always furthers the interests of Hell.
>
> "Devilbound creature" is an acquired template that can be added to any creature with 5 or more Hit Dice and Intelligence, Wisdom, and Charisma scores of 3 or higher (referred to hereafter as the base creature). The creature retains all the base creature's statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature +1.
>
> **Alignment:** Any evil. A devilbound creature radiates an evil aura as if it were an evil outsider.
>
> **Senses:** A devilbound creature gains darkvision 60 ft. and the see in darkness ability.
>
> **Armor Class:** Natural armor improves by +4.
>
> **Defensive Abilities:** A devilbound creature gains a +4 bonus on saving throws against poison, resist fire 30, and regeneration 5 (good spells, good weapons).
>
> **Weaknesses:** The devil-bound creature gains the following weakness.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.nuAhCqqdWT8H45r5 inline=true]
>
> **Special Attacks:** The creature gains the summon universal monster ability and can summon a devil once per day with a 100% chance of success. The devil remains for 1 hour. The creature's caster level or Hit Dice, whichever is higher, determines the most powerful kind of devil it can summon and the effective spell level of this ability, according to the following table.
>
>
> **Caster Level**
>
>
> **Devil**
>
>
> **Spell Level**
>
>
> 3rd
>
>
> Lemure
>
>
> 2nd
>
>
> 9th
>
>
> Bearded devil
>
>
> 5th
>
>
> 11th
>
>
> Erinyes
>
>
> 6th
>
>
> 13th
>
>
> Bone devil
>
>
> 7th
>
>
> 15th
>
>
> Barbed devil
>
>
> 8th
>
>
> 17th
>
>
> Ice devil
>
>
> 9th
>
>
> **Spell-Like Abilities:** The creature gains the following spell-like abilities, depending on the kind of devil it is bound to. The creature uses its Hit Dice or caster level, whichever is higher, as the caster level for its spell-like abilities. Save DCs are based on the creature's Intelligence, Wisdom, or Charisma, whichever is highest.
>
> *Drowning*: 3/day—@UUID[Compendium.pf1.spells.Item.ohy0ty2dawfaaqwd], @UUID[Compendium.pf1.spells.Item.7m5us8d4a9lwh1ap]
>
> *Horned*: 3/day—@UUID[Compendium.pf1.spells.Item.xgv1e2ayf1e0br9j], @UUID[Compendium.pf1.spells.Item.6oq1wcryviik9ice]
>
> **Abilities:** Adjust the base creature's ability scores according to the kind of devil it is bound to.
>
>
> **Devil**
>
>
> **Str**
>
>
> **Dex**
>
>
> **Con**
>
>
> **Int**
>
>
> **Wis**
>
>
> **Cha**
>
>
> Accuser
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> Barbed, bearded, host
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> Belier
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Bone, ice
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> Contract, handmaiden
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Drowning, horned
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> Erinyes
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Immolation
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Imp
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> Nemesis, pit fiend
>
>
> +2 to any three different ability scores

**Mechanical encoding:** `changes`: 4
  - `2` → `str`  (untyped)
  - `2` → `cha`  (untyped)
  - `2` → `dex`  (untyped)
  - `4` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Devilbound (Erinyes)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 56-57
**Foundry id:** `tqyI7Jpf14w5pIOf`

> A devilbound creature has made a bargain with a devil, promising a service and its soul in exchange for infernal power. The specific service depends on the devil's type and motivations, but always furthers the interests of Hell.
>
> "Devilbound creature" is an acquired template that can be added to any creature with 5 or more Hit Dice and Intelligence, Wisdom, and Charisma scores of 3 or higher (referred to hereafter as the base creature). The creature retains all the base creature's statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature +1.
>
> **Alignment:** Any evil. A devilbound creature radiates an evil aura as if it were an evil outsider.
>
> **Senses:** A devilbound creature gains darkvision 60 ft. and the see in darkness ability.
>
> **Armor Class:** Natural armor improves by +4.
>
> **Defensive Abilities:** A devilbound creature gains a +4 bonus on saving throws against poison, resist fire 30, and regeneration 5 (good spells, good weapons).
>
> **Weaknesses:** The devil-bound creature gains the following weakness.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.nuAhCqqdWT8H45r5 inline=true]
>
> **Special Attacks:** The creature gains the summon universal monster ability and can summon a devil once per day with a 100% chance of success. The devil remains for 1 hour. The creature's caster level or Hit Dice, whichever is higher, determines the most powerful kind of devil it can summon and the effective spell level of this ability, according to the following table.
>
>
> **Caster Level**
>
>
> **Devil**
>
>
> **Spell Level**
>
>
> 3rd
>
>
> Lemure
>
>
> 2nd
>
>
> 9th
>
>
> Bearded devil
>
>
> 5th
>
>
> 11th
>
>
> Erinyes
>
>
> 6th
>
>
> 13th
>
>
> Bone devil
>
>
> 7th
>
>
> 15th
>
>
> Barbed devil
>
>
> 8th
>
>
> 17th
>
>
> Ice devil
>
>
> 9th
>
>
> **Spell-Like Abilities:** The creature gains the following spell-like abilities, depending on the kind of devil it is bound to. The creature uses its Hit Dice or caster level, whichever is higher, as the caster level for its spell-like abilities. Save DCs are based on the creature's Intelligence, Wisdom, or Charisma, whichever is highest.
>
> *Erinyes*: 3/day—@UUID[Compendium.pf1.spells.Item.be88e90guqbi1q1z] (single target), @UUID[Compendium.pf1.spells.Item.okui7mft5bquqfrg]
>
> **Abilities:** Adjust the base creature's ability scores according to the kind of devil it is bound to.
>
>
> **Devil**
>
>
> **Str**
>
>
> **Dex**
>
>
> **Con**
>
>
> **Int**
>
>
> **Wis**
>
>
> **Cha**
>
>
> Accuser
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> Barbed, bearded, host
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> Belier
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Bone, ice
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> Contract, handmaiden
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Drowning, horned
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> Erinyes
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Immolation
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Imp
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> Nemesis, pit fiend
>
>
> +2 to any three different ability scores

**Mechanical encoding:** `changes`: 4
  - `2` → `cha`  (untyped)
  - `2` → `dex`  (untyped)
  - `2` → `con`  (untyped)
  - `4` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Devilbound (Immolation)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 56-57
**Foundry id:** `PNmCjvE1r1OTNEkh`

> A devilbound creature has made a bargain with a devil, promising a service and its soul in exchange for infernal power. The specific service depends on the devil's type and motivations, but always furthers the interests of Hell.
>
> "Devilbound creature" is an acquired template that can be added to any creature with 5 or more Hit Dice and Intelligence, Wisdom, and Charisma scores of 3 or higher (referred to hereafter as the base creature). The creature retains all the base creature's statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature +1.
>
> **Alignment:** Any evil. A devilbound creature radiates an evil aura as if it were an evil outsider.
>
> **Senses:** A devilbound creature gains darkvision 60 ft. and the see in darkness ability.
>
> **Armor Class:** Natural armor improves by +4.
>
> **Defensive Abilities:** A devilbound creature gains a +4 bonus on saving throws against poison, resist fire 30, and regeneration 5 (good spells, good weapons).
>
> **Weaknesses:** The devil-bound creature gains the following weakness.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.nuAhCqqdWT8H45r5 inline=true]
>
> **Special Attacks:** The creature gains the summon universal monster ability and can summon a devil once per day with a 100% chance of success. The devil remains for 1 hour. The creature's caster level or Hit Dice, whichever is higher, determines the most powerful kind of devil it can summon and the effective spell level of this ability, according to the following table.
>
>
> **Caster Level**
>
>
> **Devil**
>
>
> **Spell Level**
>
>
> 3rd
>
>
> Lemure
>
>
> 2nd
>
>
> 9th
>
>
> Bearded devil
>
>
> 5th
>
>
> 11th
>
>
> Erinyes
>
>
> 6th
>
>
> 13th
>
>
> Bone devil
>
>
> 7th
>
>
> 15th
>
>
> Barbed devil
>
>
> 8th
>
>
> 17th
>
>
> Ice devil
>
>
> 9th
>
>
> **Spell-Like Abilities:** The creature gains the following spell-like abilities, depending on the kind of devil it is bound to. The creature uses its Hit Dice or caster level, whichever is higher, as the caster level for its spell-like abilities. Save DCs are based on the creature's Intelligence, Wisdom, or Charisma, whichever is highest.
>
> *Immolation*: 3/day—@UUID[Compendium.pf1.spells.Item.nfm6i9z9r3n2fku7], @UUID[Compendium.pf1.spells.Item.6oq1wcryviik9ice]
>
> **Abilities:** Adjust the base creature's ability scores according to the kind of devil it is bound to.
>
>
> **Devil**
>
>
> **Str**
>
>
> **Dex**
>
>
> **Con**
>
>
> **Int**
>
>
> **Wis**
>
>
> **Cha**
>
>
> Accuser
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> Barbed, bearded, host
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> Belier
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Bone, ice
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> Contract, handmaiden
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Drowning, horned
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> Erinyes
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Immolation
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Imp
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> Nemesis, pit fiend
>
>
> +2 to any three different ability scores

**Mechanical encoding:** `changes`: 4
  - `2` → `cha`  (untyped)
  - `2` → `con`  (untyped)
  - `4` → `nac`  (untyped)
  - `2` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Devilbound (Imp)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 56-57
**Foundry id:** `3tJMY2yN1wqO2unK`

> A devilbound creature has made a bargain with a devil, promising a service and its soul in exchange for infernal power. The specific service depends on the devil's type and motivations, but always furthers the interests of Hell.
>
> "Devilbound creature" is an acquired template that can be added to any creature with 5 or more Hit Dice and Intelligence, Wisdom, and Charisma scores of 3 or higher (referred to hereafter as the base creature). The creature retains all the base creature's statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature +1.
>
> **Alignment:** Any evil. A devilbound creature radiates an evil aura as if it were an evil outsider.
>
> **Senses:** A devilbound creature gains darkvision 60 ft. and the see in darkness ability.
>
> **Armor Class:** Natural armor improves by +4.
>
> **Defensive Abilities:** A devilbound creature gains a +4 bonus on saving throws against poison, resist fire 30, and regeneration 5 (good spells, good weapons).
>
> **Weaknesses:** The devil-bound creature gains the following weakness.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.nuAhCqqdWT8H45r5 inline=true]
>
> **Special Attacks:** The creature gains the summon universal monster ability and can summon a devil once per day with a 100% chance of success. The devil remains for 1 hour. The creature's caster level or Hit Dice, whichever is higher, determines the most powerful kind of devil it can summon and the effective spell level of this ability, according to the following table.
>
>
> **Caster Level**
>
>
> **Devil**
>
>
> **Spell Level**
>
>
> 3rd
>
>
> Lemure
>
>
> 2nd
>
>
> 9th
>
>
> Bearded devil
>
>
> 5th
>
>
> 11th
>
>
> Erinyes
>
>
> 6th
>
>
> 13th
>
>
> Bone devil
>
>
> 7th
>
>
> 15th
>
>
> Barbed devil
>
>
> 8th
>
>
> 17th
>
>
> Ice devil
>
>
> 9th
>
>
> **Spell-Like Abilities:** The creature gains the following spell-like abilities, depending on the kind of devil it is bound to. The creature uses its Hit Dice or caster level, whichever is higher, as the caster level for its spell-like abilities. Save DCs are based on the creature's Intelligence, Wisdom, or Charisma, whichever is highest.
>
> *Imp*: 3/day—@UUID[Compendium.pf1.spells.Item.oylikodnyku2zewu] (self only), @UUID[Compendium.pf1.spells.Item.d40ia71c2eljm91k] (self only, same size as base creature)
>
> **Abilities:** Adjust the base creature's ability scores according to the kind of devil it is bound to.
>
>
> **Devil**
>
>
> **Str**
>
>
> **Dex**
>
>
> **Con**
>
>
> **Int**
>
>
> **Wis**
>
>
> **Cha**
>
>
> Accuser
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> Barbed, bearded, host
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> Belier
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Bone, ice
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> Contract, handmaiden
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Drowning, horned
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> Erinyes
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Immolation
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Imp
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> Nemesis, pit fiend
>
>
> +2 to any three different ability scores

**Mechanical encoding:** `changes`: 4
  - `2` → `cha`  (untyped)
  - `2` → `int`  (untyped)
  - `4` → `nac`  (untyped)
  - `2` → `dex`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Devilbound (Nemesis, Pit Fiend)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 56-57
**Foundry id:** `QmtVihVH2pUFMsCC`

> A devilbound creature has made a bargain with a devil, promising a service and its soul in exchange for infernal power. The specific service depends on the devil's type and motivations, but always furthers the interests of Hell.
>
> "Devilbound creature" is an acquired template that can be added to any creature with 5 or more Hit Dice and Intelligence, Wisdom, and Charisma scores of 3 or higher (referred to hereafter as the base creature). The creature retains all the base creature's statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature +1.
>
> **Alignment:** Any evil. A devilbound creature radiates an evil aura as if it were an evil outsider.
>
> **Senses:** A devilbound creature gains darkvision 60 ft. and the see in darkness ability.
>
> **Armor Class:** Natural armor improves by +4.
>
> **Defensive Abilities:** A devilbound creature gains a +4 bonus on saving throws against poison, resist fire 30, and regeneration 5 (good spells, good weapons).
>
> **Weaknesses:** The devil-bound creature gains the following weakness.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.nuAhCqqdWT8H45r5 inline=true]
>
> **Special Attacks:** The creature gains the summon universal monster ability and can summon a devil once per day with a 100% chance of success. The devil remains for 1 hour. The creature's caster level or Hit Dice, whichever is higher, determines the most powerful kind of devil it can summon and the effective spell level of this ability, according to the following table.
>
>
> **Caster Level**
>
>
> **Devil**
>
>
> **Spell Level**
>
>
> 3rd
>
>
> Lemure
>
>
> 2nd
>
>
> 9th
>
>
> Bearded devil
>
>
> 5th
>
>
> 11th
>
>
> Erinyes
>
>
> 6th
>
>
> 13th
>
>
> Bone devil
>
>
> 7th
>
>
> 15th
>
>
> Barbed devil
>
>
> 8th
>
>
> 17th
>
>
> Ice devil
>
>
> 9th
>
>
> **Spell-Like Abilities:** The creature gains the following spell-like abilities, depending on the kind of devil it is bound to. The creature uses its Hit Dice or caster level, whichever is higher, as the caster level for its spell-like abilities. Save DCs are based on the creature's Intelligence, Wisdom, or Charisma, whichever is highest.
>
> *Nemesis*: 3/day — @UUID[Compendium.pf1.spells.Item.oylikodnyku2zewu], @UUID[Compendium.pf1.spells.Item.q4ixxjb4v281g2xv]; 1/day — @UUID[Compendium.pf1.spells.Item.baocube6vvey9zlc]
>
> *Pit Fiend*: 3/day — quickened @UUID[Compendium.pf1.spells.Item.6oq1wcryviik9ice], @UUID[Compendium.pf1.spells.Item.oylikodnyku2zewu]; 1/day — @UUID[Compendium.pf1.spells.Item.baocube6vvey9zlc]
>
> **Abilities:** Adjust the base creature's ability scores according to the kind of devil it is bound to. (For Nemesis and Pit Fiend, go to the "Changes" tab to set the appropriate stats)
>
>
> **Devil**
>
>
> **Str**
>
>
> **Dex**
>
>
> **Con**
>
>
> **Int**
>
>
> **Wis**
>
>
> **Cha**
>
>
> Accuser
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> Barbed, bearded, host
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> Belier
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Bone, ice
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> —
>
>
> Contract, handmaiden
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> 2
>
>
> 2
>
>
> Drowning, horned
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> —
>
>
> 2
>
>
> Erinyes
>
>
> —
>
>
> 2
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Immolation
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> —
>
>
> 2
>
>
> Imp
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> —
>
>
> 2
>
>
> Nemesis, pit fiend
>
>
> +2 to any three different ability scores

**Mechanical encoding:** `changes`: 4
  - `2` → `str`  (untyped)
  - `2` → `str`  (untyped)
  - `4` → `nac`  (untyped)
  - `2` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Divine Guardian
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 60-61
**Foundry id:** `IGBwcBQf8DBC7CtG`

> A divine guardian is a creature chosen by the gods to guard a sacred site of the faith. Blessed with eternal life (or damned, some might say), a divine guardian spends untold centuries in the service of its deity, tirelessly and deathlessly defending its charge from any who would seek to desecrate it.
>
> Typically such a creature is transformed into a form more regal than its mortal one, setting it apart from a typical member of its race or species. A divine guardian is spiritually connected to the one site that it must guard for eternity. As long as a divine guardian remains within that site, it does not hunger, thirst, get sick, or even age. Within the bounds of its sacred site, a divine guardian possesses numerous defensive powers to ward it from intruders, but it can never leave the area or the long years of its service will finally catch up to it. A divine guardian must weigh the power and prestige of its endless responsibility against the freedom death might inevitably bring.
>
> Most divine guardians are chosen servants who agree to willingly serve their gods for all eternity, but some have been cursed with their duty in response for some harm to the god's faithful or as atonement for some great sin. Whatever the nature of its creation, a divine guardian is still beholden to the god that granted it its powers, and to the followers of that god as well.
>
> A cleric or paladin of the deity that created a divine guardian can issue the guardian commands. This does not give the cleric or paladin complete control over the creature, but the guardian does respond favorably to those requests. For example, a cleric could ask it to not attack her companions, or to help her defend the guardian's sacred site from attackers. A cleric or paladin of the same faith must win an opposed Charisma check to convince a divine guardian to do anything it wouldn't ordinarily do. A divine guardian can never be ordered to leave its sacred site or to go against the tenets of its deity's faith.
>
> The divine guardian hydra presented here is built using a hydra from the Pathfinder RPG Bestiary. See page 178 of the Bestiary for rules on this creature's hydra traits and regenerate head abilities. This divine guardian hydra is a divine guardian of the god of nature and the weather, thus giving it the air and water subtypes.
>
> "Divine guardian" is an acquired template that can be added to any creature (referred to hereafter as the base creature). A divine guardian uses all the base creature's statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature +1.
>
> **Alignment:** Usually, the alignment of a divine guardian matches that of the god who invested it with power. Sometimes, however, a god punishes a wayward worshiper or an enemy of the faith by making it a divine guardian.
>
> **Type:** The creature's type does not change, but the creature might gain one or more alignment or elemental subtypes, depending on the alignment and portfolio of the deity that granted it the template. Possible subtypes include air, chaotic, cold, earth, evil, fire, good, lawful, and water. For instance, a lawful good deity's divine guardian would have the lawful and good subtypes, even if it were actually of some other alignment. Similarly, a neutral god of water and ice would grant its divine guardian the water and cold subtypes.
>
> **Senses:** A divine guardian gains darkvision 60 feet and low-light vision.
>
> **Defensive Abilities:** A divine guardian is immune to disease, poison, and all mind-affecting effects. It also gains fast healing 5. In addition, it gains the following defensive ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.aSFG2qpQsyjVG1T8 inline=true]
>
> **Special Attacks:** A divine guardian gains the following.
>
> **Spell-Like Abilities:** A divine guardian has a cumulative number of spell-like abilities depending on its Hit Dice. Unless otherwise noted, these abilities are usable 1/day. CL is equal to the divine guardian's HD or the CL of the base creature's spell-like abilities, whichever is higher.
>
>
> **HD**
>
>
> **Abilities**
>
>
> 1–2
>
>
> @UUID[Compendium.pf1.spells.Item.nee6cxpoekp3aklq] 3/day, @UUID[Compendium.pf1.spells.Item.ojwg1ki98tq8xyh9]* *at will (within sacred site only), @UUID[Compendium.pf1.spells.Item.2ubwr3811rn9jvop]
>
>
> 3–4
>
>
> @UUID[Compendium.pf1.spells.Item.cqhabnit3b7l5ezm], @UUID[Compendium.pf1.spells.Item.2o9tacbz7tbrlhvv]* *3/day
>
>
> 5–6
>
>
> @UUID[Compendium.pf1.spells.Item.d1wxnax51cecplm4], @UUID[Compendium.pf1.spells.Item.6kmkxepwgsbta6ui]
>
>
> 7–8
>
>
> @UUID[Compendium.pf1.spells.Item.k3zn13pbr5tr9zac]
>
>
> 9–10
>
>
> @UUID[Compendium.pf1.spells.Item.p2kosvizylhy8vfa]
>
>
> 11–12
>
>
> @UUID[Compendium.pf1.spells.Item.8z4tlk1fojr9t9yb]
>
>
> 13–14
>
>
> @UUID[Compendium.pf1.spells.Item.odel1qsctfkp8rdm]
>
>
> 15–16
>
>
> @UUID[Compendium.pf1.spells.Item.trl849bibbe760xo]
>
>
> 17–18
>
>
> @UUID[Compendium.pf1.spells.Item.5w1zrztwbvd6xkgj]
>
>
> 19–20
>
>
> @UUID[Compendium.pf1.spells.Item.dsondqy4ngf1yzf3]
>
>
> 21+
>
>
> @UUID[Compendium.pf1.spells.Item.1mi4y3g4n8adtfl3]
>
>
> **Special Qualities:** A divine guardian gains the following.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.sl3K8MzsL9cJ7xH7 inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.1GhDRENe7E1UQFzP inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.nDEDfbhO6fIX0h3O inline=true]
>
> **Abilities:** Wis +4, Cha +4. If the base creature has an Intelligence score of 2 or lower, it also gains Int +4.
>
> **Skills:** A divine guardian gains a +5 racial bonus on Perception and Sense Motive checks.
>
> **Organization:** Solitary.

**Mechanical encoding:** `changes`: 5
  - `if(lte(@abilities.int.total, 2), 1) * 4` → `int`  (untyped)
  - `5` → `skill.sen`  (racial)
  - `4` → `cha`  (untyped)
  - `5` → `skill.per`  (racial)
  - `4` → `wis`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Dread Lord
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `y06ja9U29UYqCOYx`

> **Acquired/Inherited Template** Both**Simple Template** No**Usable with Summons** No
>
> Dread lords are intrinsically tied to the territories they inhabit, either through ancestry or by claiming them in costly battle. Ambitious and cunning in their pursuit of land and glory, once dread lords attain their goals of conquest, they transition into tragic figures. They might find themselves hollow once their dreams are fulfilled, having nothing else to strive for, or could becoming heartless toward their charges, seeing them as ungrateful for all the lord sacrificed.
>
> Some lords come into power through vile deeds and become targets of powerful curses wreaked by people they wronged or powerful divine entities that demand retribution. These despicable creatures are transformed into brooding immortals known as cursed lords. Regardless of how they rose to rule over their lands, their dark domains are dangerous and haunted places, as described beginning on page 159.
>
> "Dread lord" is an acquired or inherited template that can be added to any creature with Intelligence and Charisma scores of at least 6 (referred to hereafter as the base creature). A dread lord uses the base creature’s statistics and abilities except as noted here. If the creature is imprisoned within its domain as the result of a powerful curse, it instead becomes a cursed lord (see page 235).
>
> **Challenge Rating:** Base creature’s CR + 1.
>
> **Alignment:** Any evil.
>
> **Senses:** A dread lord gains darkvision 120 feet. Defensive Abilities: A dread lord gains DR 5/good or silver. A dread lord gains fast healing 5 if it has fewer than 10 Hit Dice, or fast healing 10 if it has 10 or more Hit Dice.
>
> **Weaknesses:** A dread lord gains the following weakness.
>
> *Landlocked (Ex):* A dread lord’s power is drawn directly from its domain, which has a radius of 5 miles per Hit Die of the dread lord, centered on a fixed point of some significance to the dread lord. The dread lord loses all benefits of this template when not within its domain.
>
> **Special Attacks:** A dread lord gains several special attacks. For every 3 Hit Dice the dread lord has, it chooses a special attack from those listed below. Unless otherwise noted, the saving throw DCs for these abilities are equal to 10 + 1/2 the dread lord’s Hit Dice + its Charisma modifier. The dread lord’s caster level is equal to its total Hit Dice (or the caster level of its existing spell-like abilities, whichever is higher).
>
> *All-Seeing (Sp):* Nothing happens in the dread lord’s realm without the dread lord becoming aware. It can use speak with animals, speak with plants, and stone tell as spell-like abilities each three times per day. If it has a CR of 5 or higher, it can use clairaudience/clairvoyance as a spell-like ability three times per day, and the spell’s range extends to any place in its domain.
>
> *Dream Dominion (Su):* The dread lord has dominion over even the dreams of its subjects. It can use dream and nightmare as spell-like abilities, each once per day, but targeting only creatures within its domain. If it has a CR of 9 or higher, then once per week it can attempt to gain control of a creature whose dreams it affects in this way. If the target fails a secondary Will saving throw, the dread lord enslaves it, as per dominate monster, in addition to the dream or nightmare spell-like ability’s normal effects.
>
> *Fear Aura (Su): *The dread lord is terrifying to behold. Any creature within a 60-foot radius that sees or hears the dread lord must succeed at a Will save or be shaken for as long as it is within the aura, and for 1 minute thereafter. Whether or not the save is successful, that creature cannot be affected again by the same dread lord’s fear aura for 24 hours. This is a mind-affecting fear effect.
>
> *Magical Mastery (Su):* The dread lord draws magical power from its domain. It treats its caster level as 2 higher for the purposes of spells and spell-like abilities it casts, and the saving throw DCs of such spells and spell-like abilities increase by 1.
>
> *Master of the Four Winds (Sp):* The dread lord can control the weather within its domain. It can use fog cloud and gust of wind as spell-like abilities each three times per day. If it has a CR of 5 or higher, it can use control weather as a spell-like ability once per day. If it has a CR of 8 or higher, it can use control winds as a spell-like ability once per day.
>
> *Physical Mastery (Su):* The dread lord draws strength and deftness from its domain. It gains a +4 profane bonus to its Strength, Dexterity, and Constitution scores.
>
> *Plant Affinity (Sp): *The dread lord’s control over its lands extends to the very plants. It can use entangle as a spell-like ability at will, and plant growth as a spell-like ability once per day. If it has a CR of 5 or higher, it can use tree stride as a spell-like ability at will. If it has a CR of 10 or higher, it can use liveoak as a spell-like ability once per day.
>
> *Unquestioned Ruler (Sp):* The dread lord’s subjects naturally bend to its will. It can use charm animal, charm person, and detect thoughts as spell-like abilities at will. If it has a CR of 10 or higher, it can use dominate animal, dominate person, and mass suggestion as spell-like abilities three times per day.
>
> **Special Qualities:** A dread lord gains the following special ability.
>
> *One with the Land (Su):* A dread lord can shape the hazardous landscapes formed as a consequence of its domain’s creation to its will. It can replace any normal or supernatural hazard present in its domain with another hazard, but the process takes 24 hours, during which time neither hazard functions. The combined CR of all hazards found within a lord’s domain (that is, the CR of a hypothetical encounter with all of the hazards at once) can’t exceed twice its Hit Dice, and it cannot create any hazards whose CR exceeds its own. A dread lord’s affinity with the land grants it a +2 bonus on all Will saves.
>
> **Ability Scores:** Intelligence +4, Charisma +4.

**Mechanical encoding:** `changes`: 3
  - `4` → `int`  (untyped)
  - `4` → `cha`  (untyped)
  - `2` → `will`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Dream Eater
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `7I686h03hecJF9T4`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** Yes
>
> An endless variety of beings exist within and below the Pyramid of Kamaria. Among the most unique denizens of the pyramid, however, are the dream eaters. Created by the Gem of Dreams (see page 43), these onetime humans have been warped by nightmares into deformed creatures. The Rovagug cultists themselves have built a strange mythology for themselves around this practice—they believe the Gem of Dreams to be a gift sent them by their god. According to their myths, once the Rough Beast emerges from the Dead Vault and destroys Golarion, the corpse world left behind would be populated only by those Rovagug has chosen for survival. It is through this magical gem’s capacity to transform dreamers into monsters that they believe they are being so selected.
>
> "Dream Eater" is an acquired template that can be added to any living intelligent creature through contact with the artifact known as the Gem of Dreams—but once a creature becomes a dream eater, it cannot gain this template again. CR: Same as base creature +2.
>
> **CR:** Same as base creature +2.
>
> **Alignment:** Chaotic evil—most dream eaters become worshipers of Rovagug, demon lords, or other chaotic evil deities.
>
> **Senses:** The base creature gains darkvision 60 ft.; if the base creature already possesses darkvision, the range of that ability increases by 60 ft.
>
> **Immunity:** The base creature becomes immune to mind-affecting effects.
>
> **Special Attacks:** A dream eater gains two special attacks, as detailed below. Both of these special attacks have save DCs equal to 10 + 1/2 the dream eater’s Hit Dice + the dream eater’s Charisma modifier.
>
> *Dream Eating (Su): *As a full-round action that provokes attacks of opportunity, a dream eater can consume a creature’s subconscious dreams if the victim fails to resist with a Will save. A sleeping victim takes a –2 penalty on saving throws against this ability, but automatically wakens if the save is successful. On a failed save, the victim takes 1d4 points of Charisma damage, and the dream eater gains a number of psychic points equal to the Charisma drained, to a maximum amount of psychic points equal to the dream eater’s Hit Dice.
>
> *Psychic Assault (Su): *As a swift action, a dream eater can imbue any melee attack he makes with a psychic assault, infusing the mind of the creature struck with hideous nightmare visions and hallucinations. The magnitude of the effect depends on how many psychic points the dream eater spends in the assault. By expending 1 point, the dream eater can cause the victim to become dazzled for 1d6 rounds. By expending 3 points, he can make a victim become staggered for 1d6 rounds. By expending 5 points, he can make the victim nauseated for 1d6 rounds. By expending 7 points, he can make the victim confused for 1d6 rounds. And by expending 9 points, he can stun the victim for 1d6 rounds. The victim can resist the psychic assault entirely by making a Will saving throw.
>
> **Special Abilities:** A dream eater gains telepathy with other dream eaters to a range of 30 feet.
>
> **Ability Scores:** Str +6, Dex +2, Con +4, Int +2, Wis +2, Cha +4.
>
> **Skills:** A dream eater gains a +4 racial bonus on Perception and Stealth checks. He also gains a +8 racial bonus on Knowledge (religion) and Knowledge (planes) checks, and these two skills are now always considered class skills for the creature.

**Mechanical encoding:** `changes`: 10 (showing first 5)
  - `8` → `skill.kpl`  (racial)
  - `4` → `skill.ste`  (racial)
  - `2` → `dex`  (untyped)
  - `4` → `skill.per`  (racial)
  - `4` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Dreamspawn
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `3FTK3cF6l1hSewSP`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Dreamspawn creatures are created when the lucid bodies of dreamers are killed in certain correupted areas of the Dimension of Dreams, their nightmarish final moments resulting in true death in the waking world. On some rare occasions, the creature or creatures responsible for the death of the dreamer are intrinsically bound to that dreamer’s death throes, their etheric forms dragged along with the victim’s fleeing soul and stranded somewhere between the sleeping and waking worlds. These creatures soon emerge on the Material Plane, bursting forth from their victim’s corpse as nightmarish spectres of the dream-thing they once were.
>
> Dreamspawn creatures are always linked by ectoplasmic strands to the corpse of the dreamer that created them. They drain the corpse of fluids and essence in order to manifest, desiccating the remains in the process. Their initial manifestation usually disfigures the corpse in some horrifying manner. Dreamspawn creatures are forced to drag the remains of dead dreamers behind them, motivate to experience the Material Plane but shackled to their creator’s rotting body.
>
> These otherworldly creatures seek out new host bodies to replace the original rotting corpses that first brought them into the world. This effort allows them to extend their lives as their host body rots beyond repair. Those who hunt these escaped nightmares and seek to silence them have learned to sense the eerie vibrations that accompany the dreamspawn’s violation of planar physics, and use it to their advantage to locate and destroy the creatures.
>
> "Dreamspawn creature" is an acquired template that can be added to any corporeal creature (referred to hereafter as the base creature). Dreamspawn creatures are typically at least one size category larger than their hosts. A dreamspawn creature uses all the base creature’s statistics and special abilities except as noted here.
>
> **Challenge Rating:** Same as the base creature’s CR + 1.
>
> **Alignment:** Usually evil.
>
> **Type:** The creature’s type changes to outsider (extraplanar). Do not recalculate base class Hit Dice, BAB, saves, or skill points.
>
> **Senses:** A dreamspawn creature gains thoughtsense 60 feet.
>
> *Thoughtsense (Su): *A dreamspawn creature can automatically detect and locate conscious creatures within the specified range (usually 60 feet). This functions similarly to the blindsight ability. Nondetection, mind blank, and similar effects can block thoughtsense. Thoughtsense can distinguish between sentient (Intelligence 3 or greater) and non-sentient (Intelligence 1–2) creatures, but otherwise provides no information about the creatures it detects.
>
> **Aura:** A dreamspawn creature has the following aura.
>
> *Discordant Feedback (Su): *The dreamspawn creature’s psychic energy creates an eerie, shrieking feedback in the minds of living creatures in a 10-foot radius. Creatures within the aura take a –2 penalty on all attack rolls, skill checks, and saving throws while in the area, and must make a successful Will save or take 1d2 points of Charisma damage. Spellcasters who attempt to cast spells in the aura’s radius must make a concentration check with a DC equal to 10 + 1/2 the dreamspawn creature’s Hit Dice + the dreamspawn creature’s Charisma modifier. If the character fails, the spell is expended but does not function. This is a mind-affecting effect.
>
> **Defensive Abilities:** A dreamspawn creature gains DR 5/good or silver, immunity to mind-affecting effects, and the following defensive ability.
>
> *Span Planes (Su): *Dreamspawn creatures exist partially on the Material Plane and partially in the Dimension of Dreams. Dreamspawn creatures take half damage (50%) from all nonmagical attack forms, and full damage from magical weapons, spells, spell-like effects, supernatural effects, incorporeal creatures and effects, and force effects.
>
> **Speed:** Same as the base creature. If the base creature does not have a fly speed, the dreamspawn creature gains a fly speed of 10 (perfect maneuverability) as a supernatural ability.
>
> **Attacks:** A dreamspawn creature retains all the natural weapons, manufactured weapon attacks, and weapon proficiencies of the base creature. If the base creature has no other natural attacks, the dreamspawn creature gains a slam attack that deals damage based on the dreamspawn creature’s size.
>
> **Special Qualities:** A dreamspawn creature gains the following special quality.
>
> *Sleepwalker (Su): *A dreamspawn creature is tethered to the corpse of the dreamer whose death birthed it, using it as a conduit between one world and the next. Typically, the desiccated corpse is dragged lifelessly along with the materialized dreamspawn creature, occupying an adjacent square and moving along with it. As a move action, the dreamspawn creature can also withdraw wholly into the corpse where it can control the movements of its host. While inhabiting the corpse, it can attack foes with a slam attack. Any attack against the host deals half damage to the dreamspawn creature as well, although its DR, resistances, and immunities may negate some or all of this damage. The dreamspawn creature can materialize from the corpse as a free action. If a dreamspawn creature kills another corporeal target, it can discard its tethered corpse and attach itself to the newly killed victim.
>
> **Abilities:** Dex +4, Cha +2.

**Mechanical encoding:** `changes`: 3
  - `2` → `cha`  (untyped)
  - `4` → `dex`  (untyped)
  - `10` → `flySpeed`  (base)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Druid (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 247
**Foundry id:** `QVVNIlAXUhNuEbth`

> Drawn to the raw might and power of nature, a druid creature gains the ability to change shape and cast druid spells. A druid creature's CR increases by 2 if the creature has 7 or more HD, and it increases by 3 if the creature has 13 or more HD.
>
> **Quick Rules:** +2 on all rolls based on Wis; can use @UUID[Compendium.pf1.class-abilities.Item.sJdBOE9lwz5XAkUi] if it has 7 or more HD (using its HD – 3 as its druid level to determine the effect of the wild shape); can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.YGxrR8krrZAviojA] (see the Cleric, Druid, and Wizard Spell Slots table) using its HD as its CL; @UUID[Compendium.pf1.class-abilities.Item.5iXq1igb1Cq0qobT].
>
> **Rebuild Rules:** **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.sJdBOE9lwz5XAkUi] (if it has 7 or more HD, using its HD – 3 as its druid level to determine the effect of the wild shape); **Druid Spells** can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.YGxrR8krrZAviojA] (see the Cleric, Druid, and Wizard Spell Slots table above) using its HD as its CL; **Ability Scores** +4 Wisdom; **SQ** @UUID[Compendium.pf1.class-abilities.Item.5iXq1igb1Cq0qobT].
>
> **Animal Companion:** These rules assume the druid creature doesn't have an @UUID[Compendium.pf1.class-abilities.Item.1jMb1iCiNjS5yfwe]. If you want to add one, select a creature from the list of a summon nature's ally spell. The spell must have a level no higher than 1/2 the creature's CR. Treat the companion as an additional creature in the encounter, awarding XP for defeating it as if it was not an animal companion.
>
> **Cleric, Druid, and Wizard Spells Slots**
>
>
> **HD**
>
>
> **0**
>
>
> **1**
>
>
> **2**
>
>
> **3**
>
>
> **4**
>
>
> **5**
>
>
> **6**
>
>
> **7**
>
>
> **8**
>
>
> **9**
>
>
> 1-3
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 4-6
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 7-9
>
>
> †
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 10-12
>
>
> †
>
>
> †
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 13-15
>
>
> †
>
>
> †
>
>
> †
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 16-18
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> 19-21
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> 22-24
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> 25+
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> 2
>
>
> 2
>
>
> 1

**Mechanical encoding:** `changes`: 3
  - `2` → `wisChecks`  (untyped)
  - `2` → `wisSkills`  (untyped)
  - `2` → `will`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Druid (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 247
**Foundry id:** `3K1uexLg6lGMugaI`

> Drawn to the raw might and power of nature, a druid creature gains the ability to change shape and cast druid spells. A druid creature's CR increases by 2 if the creature has 7 or more HD, and it increases by 3 if the creature has 13 or more HD.
>
> **Quick Rules:** +2 on all rolls based on Wis; can use @UUID[Compendium.pf1.class-abilities.Item.sJdBOE9lwz5XAkUi] if it has 7 or more HD (using its HD – 3 as its druid level to determine the effect of the wild shape); can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.YGxrR8krrZAviojA] (see the Cleric, Druid, and Wizard Spell Slots table) using its HD as its CL; @UUID[Compendium.pf1.class-abilities.Item.5iXq1igb1Cq0qobT].
>
> **Rebuild Rules:** **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.sJdBOE9lwz5XAkUi] (if it has 7 or more HD, using its HD – 3 as its druid level to determine the effect of the wild shape); **Druid Spells** can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.YGxrR8krrZAviojA] (see the Cleric, Druid, and Wizard Spell Slots table above) using its HD as its CL; **Ability Scores** +4 Wisdom; **SQ** @UUID[Compendium.pf1.class-abilities.Item.5iXq1igb1Cq0qobT].
>
> **Animal Companion:** These rules assume the druid creature doesn't have an @UUID[Compendium.pf1.class-abilities.Item.1jMb1iCiNjS5yfwe]. If you want to add one, select a creature from the list of a summon nature's ally spell. The spell must have a level no higher than 1/2 the creature's CR. Treat the companion as an additional creature in the encounter, awarding XP for defeating it as if it was not an animal companion.
>
> **Cleric, Druid, and Wizard Spells Slots**
>
>
> **HD**
>
>
> **0**
>
>
> **1**
>
>
> **2**
>
>
> **3**
>
>
> **4**
>
>
> **5**
>
>
> **6**
>
>
> **7**
>
>
> **8**
>
>
> **9**
>
>
> 1-3
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 4-6
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 7-9
>
>
> †
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 10-12
>
>
> †
>
>
> †
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 13-15
>
>
> †
>
>
> †
>
>
> †
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 16-18
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> 19-21
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> 22-24
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> 25+
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> †
>
>
> 2
>
>
> 2
>
>
> 1

**Mechanical encoding:** `changes`: 1
  - `4` → `wis`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Echohusk
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `7lLKIZNFvU5i3zfk`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Echohusks are the walking corpses of creatures slain by powerful psychic attacks and animated by the mental energies that caused their deaths. The mind and soul of an echohusk are erased from its being, leaving nothing but the psychic echo of the creature that scoured its mind.
>
> Left unattended, echohusks do little other than attack creatures that disturb them. However, anyone who creates an echohusk possesses an innate mental link to the undead creature, and is able to command the echohusk to perform whatever gruesome tasks she desires.
>
> Echohusks are common in and around Geb, where death from the powerful mental attacks of psychic spellcasters—even liches—is an all too common occurrence. In such areas, echohusks are found in groups, obeying the commands of their dark masters. In the deep reaches of the underworld, where lost travelers or wayward patrols might encounter psychic horrors like neothelids, masterless echohusks are more common; the ancient and terrible creatures that happen to spawn them typically have little use for mindless servants.
>
> Many psychic creatures have attempted to perfect the technique of creating echohusks, but only the attacks of the incorporeal undead known as psychic stalkers (see page 45) can create echohusks without fail. The horrific nature of psychic stalkers is likely the reason for this phenomenon.
>
> "Echohusk" is an acquired template that can be added to any living, intelligent corporeal creature, referred to hereafter as the base creature.
>
> **Challenge Rating:** This depends on the creature’s new total number of Hit Dice, as given below.**
>
>
>
>
>  HD** 
>  **CR** 
>  **XP** 
>
>
>  1 
>  1/4 
>  100 
>
>
>  2 
>  1/2 
>  200 
>
>
>  3–4 
>  1 
>  400 
>
>
>  5–6 
>  2 
>  600 
>
>
>  7–8 
>  3 
>  800 
>
>
>  9–10 
>  4 
>  1,200 
>
>
>  11–12 
>  5 
>  1,600 
>
>
>  13–15 
>  6 
>  2,400 
>
>
>  16–17 
>  7 
>  3,200 
>
>
>  18–20 
>  8 
>  4,800 
>
>
>  21–24 
>  9 
>  6,400 
>
>
>  25–28 
>  10 
>  9,600 
>
>
>
>
> **Alignment:** Always neutral evil.
>
> **Type:** The creature’s type changes to undead. It retains any subtypes except for alignment subtypes (such as good) and subtypes that indicate kind (such as giant). It doesn’t gain the augmented subtype. It uses all the base creature’s statistics and special abilities except as noted here.
>
> **Armor Class:** The creature’s natural armor bonus is based on the echohusk’s size, indicated below.**
>
>
>
>
>  Echohusk Size** 
>  **Natural Armor Bonus** 
>
>
>  Small or smaller 
>  +0 
>
>
>  Medium 
>  +1 
>
>
>  Large 
>  +2 
>
>
>  Huge 
>  +3 
>
>
>  Gargantuan 
>  +6 
>
>
>  Colossal 
>  +10 
>
>
>
>
> **Hit Dice:** An echohusk retains the number of HD the base creature possessed (except those from class levels), and gains a number of additional Hit Dice given on the following table. An echohusk uses its Charisma modifier (instead of its Constitution modifier) to determine bonus hit points.**
>
>
>
>
>  Echohusk Size** 
>  **Bonus Hit Dice** 
>
>
>  Medium or smaller 
>  — 
>
>
>  Large 
>  +1 
>
>
>  Huge 
>  +2 
>
>
>  Gargantuan 
>  +4 
>
>
>  Colossal 
>  +6 
>
>
>
>
> **Saves:** Base save bonuses are Fortitude +1/3 Hit Dice, Reflex +1/3 Hit Dice, and Will +1/2 Hit Dice + 2.
>
> **Defensive Abilities:** Echohusks lose their defensive abilities and gain all of the qualities and immunities granted by the undead type.
>
> **Weaknesses:** Echohusks gain the following weakness.
>
> *Vulnerable to Psychic Magic (Ex):* Echohusks are particularly susceptible to psychic spells and attacks, as the entire force that animates them is composed of psychic energy. They take a –4 penalty on saving throws against psychic spells and effects.
>
> **Speed:** An echohusk retains all of the base creature’s movement speeds. However, its maneuverability for flight drops to clumsy.
>
> **Attacks:** An echohusk retains all the natural weapons, manufactured weapon attacks, and weapon proficiencies of the base creature. It gains a slam attack that deals damage as if it were one size category larger than its actual size.
>
> **Special Attacks:** An echohusk retains none of the base creature’s special attacks.
>
> **Ability Scores:** An echohusk’s Strength score increases by 2. An echohusk has neither a Constitution score or an Intelligence score, its Wisdom score changes to 10, and its Charisma score changes to 14.
>
> **BAB:** An echohusk’s base attack bonus is equal to 3/4 of its Hit Dice.
>
> **Skills:** An echohusk has no skill ranks and loses any racial bonuses to skills that the base creature possessed.
>
> **Feats:** An echohusk loses all feats possessed by the base creature, and doesn’t gain feats as its Hit Dice increase.
>
> **Special Qualities:** An echohusk loses most special qualities of the base creature, but it retains any extraordinary special qualities that improve its melee or ranged attacks. An echohusk gains the following special qualities.
>
> *Psychic Servitude (Su):* Echohusks are animated not by typical necromantic energies, but rather by the mental energies of a powerful psychic creature. They cannot be commanded or created by animate dead, command undead, control undead, and similar necromancy spells and effects. However, any creature that creates an echohusk with its psychic attacks can command that echohusk as if it had animated it using the animate dead spell (up to 4 HD of echohusks per HD of the animating creature, and no one echohusk can possess more than twice the HD of the animating creature). Echohusks under a creature’s control don’t count against the number of other undead that the creature can control with the animate dead spell, the Command Undead feat, or other similar effects.
>
> *Shattered Psyche (Ex):* Psychic attacks that are powerful enough to destroy minds leave behind a powerful but unstable force that lashes out at those nearby. When an echohusk takes damage from a melee attack, a ranged attack from within 30 feet, or a psychic spell or effect from any distance, the creature that initiated the attack must succeed at a Will saving throw (DC = 10 + 1/2 the echohusk’s Hit Dice + the echohusk’s Charisma modifier) or take 1 point of Charisma damage and be dazed for 1 round as the psychic energies in the echohusk shatter once more.

**Mechanical encoding:** `changes`: 1
  - `2` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Ectoplasmic
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 83
**Foundry id:** `BitIbt8z4RR1wqzM`

> Drawn from energies of the Ethereal Plane, ectoplasm is a vile substance resembling thick tangles of slimy linen or dripping goo. It shapes itself into the form of an undead creature, creating a host for a soul unfortunate enough to be confined within it. The existence of an ectoplasmic being is a cruel one, and few souls willingly choose this painful form of undeath.
>
> An ectoplasmic creature is approximately the same size as the body it inhabited in life, though it weighs nearly twice as much, as the ropes of undead matter that compose its body are significantly heavier than most living flesh.
>
> Even more so than most undead beings, creatures born of ectoplasm live hateful existences, filled with nothing but a lust for destruction and suffering. They have no bodily needs and require no sustenance; the only thing an ectoplasmic creature feeds upon is its own hatred of the living.
>
> Once a spirit has passed to the afterlife, it seldom wishes to return at all, let alone in a disfigured ectoplasmic body. Spirits that aren't powerful enough to come back as ghosts or spectres sometimes return as ectoplasmic monsters, particularly when there are no remains of the creature's original body for its soul to inhabit in the form of a skeleton or zombie. Sometimes, ghosts and other strong undead purposefully draw upon ectoplasm from the ethereal realm, yearning for even more power in their ectoplasmic hosts.
>
> Those who suffer this sorrowful fate, by misfortune or choice, are usually stuck in their ectoplasmic prisons until death grants them sweet release from this unlife. The transition from death to ectoplasmic undeath is a torturous ordeal, as is retaining the horrid form into which the creature is reborn. Often, this persistent agony drives these beings beyond mad, creating within an insatiable rage akin to that experienced by frustrated ghosts and other haunted souls.
>
> An ectoplasmic creature's burning desperation and embitterment often pushes it toward violence: most such beings fling themselves into battle willingly, killing to satiate their natural hunger for the suffering of others, while simultaneously hoping to be killed and thus freed of their own suffering own.
>
> Whenever in contact with surfaces (including walls they pass through), ectoplasmic creatures leave a trail of a silvery substance that resembles a slug's mucus—a trait almost exclusive to these undead. This slippery secretion dries within moments, so if its encountered, there is surely such a creature lurking nearby.
>
> Ectoplasmic beings can inhabit any location, regardless of environment or climate. The horrors tend to prowl the areas in which they died, and rarely venture outside these areas, as though they were anchored there.
>
> Though these entities rarely coordinate complicated actions with others of their kind, they seem to do so unintentionally at times. Their unnatural strength makes ectoplasmic creatures formidable combatants, which those not familiar with fighting ectoplasmic creatures would expect by looking at them. Fortunately for the wary, the sticky ectoplasm that trails behind these undead monsters is a clear indicator of their presence, and most experienced clerics can identify the substance at a glance.
>
> "Ectoplasmic" is an acquired template that can be added to any corporeal creature (other than an undead), referred to hereafter as the base creature.
>
> **Challenge Rating:** Same as the base creature +1.
>
> **Alignment:** Usually chaotic evil.
>
> **Type:** The creature's type changes to undead. It retains any subtype except for alignment subtypes (such as evil) and subtypes that indicate kind (such as giant). It does not gain the augmented subtype. It uses all the base creature's statistics and special abilities except as noted in the following sections.
>
> **Armor Class:** The creature's natural armor bonus changes as follows:
>
>
> **Ectoplasm Size**
>
>
> **Natural Armor Bonus**
>
>
> Tiny or smaller
>
>
> +0
>
>
> Small
>
>
> +1
>
>
> Medium
>
>
> +2
>
>
> Large
>
>
> +3
>
>
> Huge
>
>
> +4
>
>
> Gargantuan
>
>
> +6
>
>
> Colossal
>
>
> +8
>
>
> **Hit Dice:** Drop HD gained from class levels (to a minimum of 1 HD) and change racial Hit Dice to d8s. Ectoplasmic creatures use their Charisma modifiers to determine bonus hit points (instead of Constitution).
>
> **Saves:** Base save bonuses for racial Hit Dice are Fort +1/3 HD, Ref +1/3 HD, and Will +1/2 HD + 2.
>
> **Defensive Abilities:** An ectoplasmic creature loses the base creature's defensive abilities, and gains DR 5/ slashing as well as all of the standard immunities and traits possessed by undead creatures.
>
> **Speed:** Winged ectoplasmic creatures can still fly, but their maneuverability drops to poor if it was initially any better. If the base creature flew magically, so can the ectoplasmic creature. Retain all other movement types. An ectoplasmic creature gains the ability to traverse the air (as the @UUID[Compendium.pf1.spells.Item.e4v1uv8hexeu9sxj] spell) as a constant effect.
>
> **Attacks:** An ectoplasmic creature retains all natural weapons of the base creature. It gains a slam attack that deals damage based on the ectoplasmic creature's size.
>
> **Special Attacks:** An ectoplasmic creature retains all of the special attacks of the base creature. In addition, an ectoplasmic creature gains the following special attack.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.DmmdujI8ZsQtwIgt inline=true]
>
> **Abilities:** An ectoplasmic creature receives a +2 bonus to Strength and a +2 bonus to Charisma. An ectoplasmic creature has no Constitution or Intelligence score, and its Wisdom score becomes 10.
>
> **BAB:** An ectoplasmic creature's base attack bonus is equal to 3/4 its Hit Dice.
>
> **Feats:** An ectoplasmic creature loses all feats possessed by the base creature, and gains Toughness as a bonus feat.
>
> **Special Abilities:** An ectoplasmic creature loses most special qualities of the base creature. It retains any extraordinary special qualities that improve its melee or ranged attacks. An ectoplasmic creature gains the following special ability:
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.hHILPC00xJsM9jhm inline=true]

**Mechanical encoding:** `changes`: 4
  - `2` → `cha`  (untyped)
  - `2` → `str`  (untyped)
  - `1` → `bonusFeats`  (untyped)
  - `lookup(@size, 0, 0, 0, 1, 2, 3, 4, 6, 8)` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Elemental-Infused Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `kiplszYa0tEMMei1`

> **Acquired/Inherited Template** Both**Simple Template** No**Usable with Summons** No
>
> Sometimes unpredictable elemental events cause planar energies to infuse mundane creatures with otherworldly power, transforming them into element-infused creatures.
>
> "Element-infused" is an inherited or acquired template that can be added to any living, corporeal creature. An element-infused creature retains the base creature’s statistics and special abilities except as noted here. An element-infused creature has a strong connection to one or two of the elemental planes. Unlike most templates, the element-infused template grants few universal abilities; rather, it grants the creature a choice of several different defensive, offensive, and movement-based abilities that match its particular element or elements. In this way, not all water-infused creatures are necessarily identical. In order to select an ability, at least one of an elementinfused creature’s elements must match one of those listed in parentheses after the ability’s name. For abilities that reference an energy type, the energy type chosen must be associated with one of the creature’s elements: acid (earth), cold (water), electricity (air), or fire (fire).
>
> An element-infused creature can select a number of movement abilities (see the Speed section), defensive abilities, and offensive abilities (see the Special Attacks section) based on its Hit Dice, as shown in the chart below. In addition, an element-infused creature with 4 or more Hit Dice gains one or more bonus abilities that it can use to select additional abilities from any of these three categories. A creature infused with only one element gains one additional bonus ability.
>
>
>
>
>  **HD** 
>  **Movement** 
>  **Defensive** 
>  **Offensive** 
>  **Bonus** 
>
>
>  1-3 
>  1 
>  1 
>  1 
>  0 
>
>
>  4-6 
>  1 
>  1 
>  1 
>  1 
>
>
>  7-9 
>  1 
>  2 
>  1 
>  1 
>
>
>  10-12 
>  1 
>  2 
>  1 
>  2 
>
>
>  13-15 
>  1 
>  2 
>  2 
>  2 
>
>
>  16-18 
>  1 
>  2 
>  2 
>  3 
>
>
>  19+ 
>  1 
>  3 
>  2 
>  3 
>
>
>
>
> **CR:** If 9 HD or fewer, base creature’s CR + 1; if 10 HD or more, base creature’s + 2.
>
> **Type:** The creature’s type chances to outsider (native). In addition, the creature gains the air, earth, fire, or water subtypes corresponding to its element or elements. Do not recalculate HD, BAB, or saves.
>
> **Senses:** An element-infused creature gains darkvision with a range of up to 60 feet.
>
> **Defensive Abilities:** An element-infused creature can choose one or more of the following extraordinary abilities.
>
> *Damage Reduction (any): *The creature gains DR 2/—. If the creature has 10 or more HD, this ability can be selected one additional time, increasing the damage reduction to 5/—.
>
> *Energy Immunity (any):* The creature gains immunity to one of its associated energy types, chosen when it gains this ability. The creature must already have energy resistance 10 or higher for that energy in order to select this ability.
>
> *Energy Resistance (any):* The creature ignores the first 10 points of damage that it takes from one of its associated energy types, chosen when it gains this ability. A fire-infused creature that selects this ability also ignores the damage dealt by the fire-dominant planar trait.
>
> *Evasion (air or fire):* The creature gains the ability to avoid damage as if it had the evasion rogue class ability.
>
> *Fiery Blood (fire):* Anyone who damages the creature with a slashing or piercing melee weapon is sprayed with boiling blood that deals 1d4 points of fire damage. This damage increases by 1d4 for every 5 HD the creature has. Creatures using reach weapons are not subject to this damage.
>
> *Fortification (any): *The creature has a 50% chance to negate a critical hit or sneak attack, taking only the normal amount of damage from the attack.
>
> *Improved Natural Armor (earth): *The creature’s natural armor bonus improves by 2. If the creature has 10 or more HD, this bonus increases to 3.
>
> *Indistinct Form (air or water)*: The creature benefits from a 20% miss chance as if it had concealment.
>
> *Stability (earth or water):* The creature receives a +4 racial bonus to its CMD when resisting bull rush, drag, overrun, or trip combat maneuvers.
>
> **Speed:** An element-infused creature can choose one or more of the following abilities. Except where noted, these are extraordinary abilities.
>
> *Burrow (earth):* The creature gains a burrow speed equal to half its highest speed. Tunnels it creates always collapse behind it and never leave behind a usable passage.
>
> *Earth Glide (earth):* The creature gains the earth glide ability of an earth elemental (Pathfinder RPG Bestiary 122), though it can use this ability for only 1 minute per HD it has. This duration does not need to be consecutive, but it must be spent in 1-minute increments. The creature must have a burrow speed in order to use this ability. It can select this ability a second time in order to use this power at will.
>
> *Flight (air):* The creature gains a fly speed equal to its highest speed with average maneuverability (maximum fly speed of 10 feet per HD).
>
> *Improved Quickness (Su, fire): *Three times per day as a swift action, the creature can take an extra move action. The creature must already have quickness to select this ability.
>
> *Puddle Form (Su, water): *Once per day, the creature can turn into an animate puddle of water for up to 10 minutes. This functions as gaseous form, but the creature instead has both a base speed and swim speed of 10 feet.
>
> *Quickness (fire): *The creature’s base movement speed increases by 10, and it gains a +1 bonus on initiative checks. For every 5 HD the creature has, its base speed increases by an additional 10 feet (maximum = double its base speed), and its initiative bonus increases by 1 (maximum +5).
>
> *Swim (water): *The creature gains a swim speed equal to its highest speed (maximum 100 feet). The creature also gains the amphibious and aquatic subtypes.
>
> **Special Attacks:** An element-infused creature can choose one or more of the following abilities.
>
> *Breath Weapon (Su, any):* The creature gains a breath weapon (15-foot cone or 30-foot line) that it can use as a standard action once every minute. The breath weapon deals 1d6 points of damage of one of its associated energy types (Reflex half, DC = 10 + 1/2 creature’s HD + Con modifier). The damage increases by 1d6 for every 3 HD the creature has. If the creature has 10 or more HD, the size of the breath weapon doubles.
>
> *Burn (Ex, fire): *The creature can set creatures it strikes on fire, as per the burn ability (Bestiary 298), though only with attacks augmented by its energy attacks ability.
>
> *Energy Attacks (Ex, any):* One of the creature’s natural attacks deals an additional 1d6 points of its corresponding energy’s damage, selected when the creature gains this ability. This damage increases by 1d6 for every 10 HD the creature has. An element-infused creature can select this ability multiple times, applying its benefits to an additional two natural attacks each time.
>
> *Gusting Strike (Ex, air):* Once per round when the creature hits with a melee attack, it can attempt a bull rush combat maneuver check against the target of its melee attack as a free action. This bull rush does not provoke an attack of opportunity.
>
> *Toppling Strike (Ex, earth or water): *The element-infused creature gains the trip special ability (Bestiary: 305) with one of its natural attacks.
>
> **Abilities:** An element-infused creature gains a +4 bonus to two ability scores of its choice, a +2 bonus to two other ability scores of its choice, and a –2 penalty to one ability score of its choice. (Go to the "Changes" tab to set these modifiers)
>
> **Skills:** An element-infused creature with racial Hit Dice has a number of skill points per racial Hit Die equal to 6 + Intelligence mod. Racial class skills are unchanged, and class level skill ranks are unaffected.
>
> **Languages:** The creature gains an elemental language or languages associated with its elemental type as long as it has an Intelligence score of 3 or higher: Aquan (water), Auran (air), Ignan (fire), or Terran (earth). If the base creature is unable to speak, it can instead understand the acquired languages.

**Mechanical encoding:** `changes`: 5
  - `4` → `str`  (untyped)
  - `-2` → `str`  (untyped)
  - `4` → `str`  (untyped)
  - `2` → `str`  (untyped)
  - `2` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Energized (Air, Fire)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `bpuEOM70Dt5UfNIP`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Most golems are animated by an elemental spirit bound within a constructed body, but some creators build their golems with a greater purpose in mind. An energized golem is infused with the raw elemental energy of the elemental spirit used to animate it, granting it increased strength and agility and a host of supernatural powers.
>
> "Energized" is an acquired template that can be added to any golem (referred to hereafter as the base creature). An energized golem uses all the base creature’s statistics and special abilities except as noted here. Save DCs are equal to 10 + half the energized golem’s Hit Dice + the energized golem’s Constitution modifier.
>
> **Challenge Rating:** Base creature’s CR + 2.
>
> *Aura (Su): *An energized golem radiates one of the elemental energy auras described below. All creatures within 5 feet of the energized golem take 1d6 points of energy damage at the beginning of the golem’s turn. Each type of elemental aura generates an additional effect within this range, as is described below. For every 10 Hit Dice the energized golem has, the range of the aura extends by 5 feet and it deals an additional 1d6 points of energy damage. The type of energy damage and any additional effects of the aura are determined by the elemental overcharge special quality.
>
> *Blizzard:* The frigid temperatures surrounding the energized golem deal an additional amount of nonlethal damage equal to the damage dice of its elemental aura to all creatures within range each round. A creature can attempt a Fortitude save to negate this additional nonlethal damage. Creatures that take any amount of nonlethal damage from this effect are fatigued. If a target is already fatigued, it is instead exhausted. The fatigued or exhaustion condition persists until the creature recovers from the nonlethal damage.
>
> *Caustic Mist:* A poisonous miasma emanates from the energized golem, afflicting those within range each round with a deadly toxin that rapidly destroys flesh, muscle, and organs alike. Poison (Ex): Aura—inhaled; save Fort; frequency 1/round for 6 rounds; effect 1 Str, 1 Dex, and 1 Con damage; cure 2 saves.
>
> *Immolation:* The extreme heat surrounding the energized golem causes each creature and unattended object within range to catch fire unless it succeeds at a Reflex save. Each affected creature or item takes an additional amount of fire damage equal to the number of damage dice for the energized golem’s elemental aura immediately and each round thereafter as long as it remains within the aura. A creature or object that has caught on fire but moves outside of the aura instead takes 1d6 points of fire damage each round and can attempt another Reflex save each round to extinguish the flames.
>
> *Swirling Winds:* Powerful winds surround the energized golem, buffeting creatures within range and dealing an additional amount of bludgeoning damage equal to the damage dice of its elemental aura. These winds otherwise function as a gust of wind spell. An affected creature can attempt a Reflex save to negate this additional damage, but a successful Fortitude save is required to negate the *gust of wind* effect. If the energized golem has 10 or more Hit Dice, the DC of Fly or Strength checks to resist the effects of the winds increases by 5.
>
> **Armor Class:** Natural armor improves by 3.
>
> **Hit Points:** An energized golem receives double the bonus hit points based on its size granted by the construct creature type.
>
> **Defensive Abilities:** An energized golem’s body is infused with elemental energy, granting it immunity to a single energy type. Refer to the elemental overcharge special quality below.
>
> **Special Attacks:** An energized golem retains all of the base creature’s special abilities and gains the following special attack.
>
> *Energy Discharge (Su):* Once per hour, an energized golem can discharge a pulse of energy from its body as a standard action, affecting all targets within a 20-foot burst. This burst deals 1d8 points of energy damage for every 2 Hit Dice the energized golem has (Reflex half ). Each creature damaged by this ability must succeed at a second saving throw or suffer an additional effect. The type of energy damage, the additional effect, and the type of save to avoid this additional effect are determined by the elemental overcharge special quality.
>
> **Ability Scores:** An energized golem gains ability scores based on the base creature’s Hit Dice and the type of elemental spirit used in its creation. If the elemental spirit used is an air or fire elemental spirit, the energized golem gains a +2 bonus to Strength and +4 bonus to Dexterity. If the elemental spirit used is an earth or water elemental spirit, the energized golem gains a +4 bonus to Strength and +2 bonus to Dexterity. If the base creature has 10 or more Hit Dice, these ability score bonuses increase to +8 and +4.
>
> **Special Qualities:** An energized golem retains all of the base creature’s special qualities and gains the following special quality.
>
> *Elemental Overcharge (Su):* An energized golem is augmented by the elemental spirit that is bound to it during its creation. Its natural attacks deal 1d6 points of energy damage for every 6 Hit Dice the golem has. The type of damage dealt, the golem’s immunity, and its aura are based on the elemental spirit bound to the golem during its creation, as listed on the table below.**
>
>
>
> Elemental**
>
>
> **Energy**
>
>
> **Aura**
>
>
> **Discharge Effect (Saving Throw Type)**
>
>
> Air
>
>
> Electricity
>
>
> Swirling winds
>
>
> Stunned for 1 round (Fortitude)
>
>
> Earth
>
>
> Acid
>
>
> Caustic mist
>
>
> Acid clings to targets, dealing half damage next round (Reflex)
>
>
> Fire
>
>
> Fire
>
>
> Immolation
>
>
> Knocked prone (Fortitude)
>
>
> Water
>
>
> Cold
>
>
> Blizzard
>
>
> Entangled for 1d4+1 rounds (Reflex)

**Mechanical encoding:** `changes`: 3
  - `4 + if(gt(@attributes.hd.total, 9), 4)` → `dex`  (untyped)
  - `3` → `nac`  (untyped)
  - `2 + if(gt(@attributes.hd.total, 9), 2)` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Energized (Earth, Water)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `7NmE4uSQYw3nsRAN`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Most golems are animated by an elemental spirit bound within a constructed body, but some creators build their golems with a greater purpose in mind. An energized golem is infused with the raw elemental energy of the elemental spirit used to animate it, granting it increased strength and agility and a host of supernatural powers.
>
> "Energized" is an acquired template that can be added to any golem (referred to hereafter as the base creature). An energized golem uses all the base creature’s statistics and special abilities except as noted here. Save DCs are equal to 10 + half the energized golem’s Hit Dice + the energized golem’s Constitution modifier.
>
> **Challenge Rating:** Base creature’s CR + 2.
>
> *Aura (Su): *An energized golem radiates one of the elemental energy auras described below. All creatures within 5 feet of the energized golem take 1d6 points of energy damage at the beginning of the golem’s turn. Each type of elemental aura generates an additional effect within this range, as is described below. For every 10 Hit Dice the energized golem has, the range of the aura extends by 5 feet and it deals an additional 1d6 points of energy damage. The type of energy damage and any additional effects of the aura are determined by the elemental overcharge special quality.
>
> *Blizzard:* The frigid temperatures surrounding the energized golem deal an additional amount of nonlethal damage equal to the damage dice of its elemental aura to all creatures within range each round. A creature can attempt a Fortitude save to negate this additional nonlethal damage. Creatures that take any amount of nonlethal damage from this effect are fatigued. If a target is already fatigued, it is instead exhausted. The fatigued or exhaustion condition persists until the creature recovers from the nonlethal damage.
>
> *Caustic Mist:* A poisonous miasma emanates from the energized golem, afflicting those within range each round with a deadly toxin that rapidly destroys flesh, muscle, and organs alike. Poison (Ex): Aura—inhaled; save Fort; frequency 1/round for 6 rounds; effect 1 Str, 1 Dex, and 1 Con damage; cure 2 saves.
>
> *Immolation:* The extreme heat surrounding the energized golem causes each creature and unattended object within range to catch fire unless it succeeds at a Reflex save. Each affected creature or item takes an additional amount of fire damage equal to the number of damage dice for the energized golem’s elemental aura immediately and each round thereafter as long as it remains within the aura. A creature or object that has caught on fire but moves outside of the aura instead takes 1d6 points of fire damage each round and can attempt another Reflex save each round to extinguish the flames.
>
> *Swirling Winds:* Powerful winds surround the energized golem, buffeting creatures within range and dealing an additional amount of bludgeoning damage equal to the damage dice of its elemental aura. These winds otherwise function as a gust of wind spell. An affected creature can attempt a Reflex save to negate this additional damage, but a successful Fortitude save is required to negate the *gust of wind* effect. If the energized golem has 10 or more Hit Dice, the DC of Fly or Strength checks to resist the effects of the winds increases by 5.
>
> **Armor Class:** Natural armor improves by 3.
>
> **Hit Points:** An energized golem receives double the bonus hit points based on its size granted by the construct creature type.
>
> **Defensive Abilities:** An energized golem’s body is infused with elemental energy, granting it immunity to a single energy type. Refer to the elemental overcharge special quality below.
>
> **Special Attacks:** An energized golem retains all of the base creature’s special abilities and gains the following special attack.
>
> *Energy Discharge (Su):* Once per hour, an energized golem can discharge a pulse of energy from its body as a standard action, affecting all targets within a 20-foot burst. This burst deals 1d8 points of energy damage for every 2 Hit Dice the energized golem has (Reflex half ). Each creature damaged by this ability must succeed at a second saving throw or suffer an additional effect. The type of energy damage, the additional effect, and the type of save to avoid this additional effect are determined by the elemental overcharge special quality.
>
> **Ability Scores:** An energized golem gains ability scores based on the base creature’s Hit Dice and the type of elemental spirit used in its creation. If the elemental spirit used is an air or fire elemental spirit, the energized golem gains a +2 bonus to Strength and +4 bonus to Dexterity. If the elemental spirit used is an earth or water elemental spirit, the energized golem gains a +4 bonus to Strength and +2 bonus to Dexterity. If the base creature has 10 or more Hit Dice, these ability score bonuses increase to +8 and +4.
>
> **Special Qualities:** An energized golem retains all of the base creature’s special qualities and gains the following special quality.
>
> *Elemental Overcharge (Su):* An energized golem is augmented by the elemental spirit that is bound to it during its creation. Its natural attacks deal 1d6 points of energy damage for every 6 Hit Dice the golem has. The type of damage dealt, the golem’s immunity, and its aura are based on the elemental spirit bound to the golem during its creation, as listed on the table below.**
>
>
>
> Elemental**
>
>
> **Energy**
>
>
> **Aura**
>
>
> **Discharge Effect (Saving Throw Type)**
>
>
> Air
>
>
> Electricity
>
>
> Swirling winds
>
>
> Stunned for 1 round (Fortitude)
>
>
> Earth
>
>
> Acid
>
>
> Caustic mist
>
>
> Acid clings to targets, dealing half damage next round (Reflex)
>
>
> Fire
>
>
> Fire
>
>
> Immolation
>
>
> Knocked prone (Fortitude)
>
>
> Water
>
>
> Cold
>
>
> Blizzard
>
>
> Entangled for 1d4+1 rounds (Reflex)

**Mechanical encoding:** `changes`: 3
  - `3` → `nac`  (untyped)
  - `2 + if(gt(@attributes.hd.total, 9), 2)` → `dex`  (untyped)
  - `4 + if(gt(@attributes.hd.total, 9), 4)` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Enlightened Construct
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `U7WoBCEG5FBftSnI`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Infused with powerful psychic energy, enlightened constructs have access to strange and deadly mental powers. Highly intelligent and secretive, these constructs typically serve as henchmen to powerful psychics or sorcerous cabals.
>
> "Enlightened construct" is an acquired template that can be added to any construct, referred to hereafter as the base creature. An enlightened construct retains all the base creature’s statistics and special abilities except as noted here.
>
> **Challenge Rating:** If the base creature had 4 or fewer HD, base creature’s CR + 1; HD 5–10, base creature’s CR + 2; HD 11 or more, base creature’s CR + 3.
>
> **Alignment:** An enlightened construct’s alignment is no more than one step away from that of its creator.
>
> **Type:** An enlightened construct gains the augmented subtype.
>
> **Senses:** An enlightened construct gains lifesense out to 60 feet.
>
> **Weaknesses:** An enlightened construct gains the following weakness.
>
> *Susceptible to Mind-Affecting Effects (Ex):* An enlightened construct is susceptible to mind-affecting effects, even though it is a construct. Although they can be magically charmed or compelled, enlightened constructs are particularly resistant to enchantments and receive a +4 bonus on Will saves to resist these effects.
>
> **Special Attacks:** An enlightened construct gains the following special abilities.
>
> *Mind Thrust (Sp):* An enlightened construct can use *mind thrust* as a spell-like ability a number of times per day equal to 2 + the enlightened construct’s Intelligence modifier. The version of *mind thrust* available to an enlightened construct is determined by its Hit Dice: HD Spell
>
>
> **HD**
>
>
> **Spell**
>
>
> 1-2
>
>
> Mind thrust I
>
>
> 3-4
>
>
> Mind thrust II
>
>
> 5-7
>
>
> Mind thrust III
>
>
> 8-10
>
>
> Mind thrust IV
>
>
> 11-15
>
>
> Mind thrust V
>
>
> 16-20
>
>
> Mind thrust VI
>
>
> **Spell-Like Abilities (Sp):** An enlightened construct gains a number of spell-like abilities set by its Hit Dice. It gains the spell-like abilities listed in the entry for its Hit Dice on the table below, as well as all listed spell-like abilities for prior entries. Unless otherwise noted, each ability is usable 1/day. The caster level for these abilities is equal to the enlightened construct’s Hit Dice (or the caster level of the base construct’s spell-like abilities, whichever is higher). The DC for a saving throw against the enlightened construct’s spell-like ability is equal to 10 + the spell’s level + the enlightened construct’s Intelligence modifier.
>
>
> **HD**
>
>
> **Spell-Like Abilities**
>
>
> 1-2
>
>
> Mindlink 3/day
>
>
> 3-4
>
>
> Mental block
>
>
> 5-6
>
>
> Mind probe 3/day
>
>
> 7-8
>
>
> Telekinesis 3/day
>
>
> 9-10
>
>
> Dimensional lock 3/day
>
>
> 11-12
>
>
> Dimension door 3/day
>
>
> 13-14
>
>
> Mass synesthesia
>
>
> 15-16
>
>
> Antimagic field
>
>
> 17-18
>
>
> Telekinetic storm
>
>
> 19-20
>
>
> Power word kill
>
>
> **Ability Scores:** If the base creature had an Intelligence score of 9 or less, roll 2d6+4 to determine the enlightened construct’s new Intelligence score. If the base creature had an Intelligence score of 10 or greater, increase its Intelligence score by 6. Additionally, increase the enlightened construct’s Charisma score by 2d6.
>
> **Feats:** Since it has an Intelligence score, an enlightened construct gains feats as normal for a creature of its Hit Dice.
>
> **Skills:** An enlightened construct gains skill points according to its new Intelligence score, which are assigned appropriately for its function, as determined by the GM.
>
> **Languages:** An enlightened construct speaks one language that its creator spoke, plus a number of additional languages that its creator knew equal to the enlightened construct’s Intelligence bonus (if any). The enlightened construct can also communicate by telepathy up to a range of 100 feet.
>
> **Special Qualities:** An enlightened construct gains the following special qualities.
>
> *Artificial Soul (Su):* Though not the true soul of a living creature, the enlightened construct’s artificial soul provides it with a unique personality and a spark of sentience. Unlike most constructs, the enlightened construct is not immune to necromantic effects. Enlightened constructs are still immune to death effects and they cannot be raised or resurrected. Enlightened construct golems are still immune to magic as described in their entries.
>
> *Phrenic Stone (Su):* An enlightened construct has a stone infused with supernatural mental energy embedded into its head or chest that is the source of its awakened intellect. If an enlightened construct is destroyed but this phrenic stone remains intact, it can be used to create another enlightened construct, using the same cost as augmenting a new enlightened construct (see Construction below). When a phrenic stone is used to create a new enlightened construct, the personality and memories of the previous enlightened construct are lost. A phrenic stone has hardness 10, 20 hit points, and a break DC of 30.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Entothrope
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** Bestiary 5 (PZO1137) p. 116
**Foundry id:** `1Jseq3I2ksUppiSQ`

> Entothropes are humanoids with the ability to turn into large insects and insect-humanoid hybrids.
>
> "Entothrope" is an inherited (for natural entothropes) or acquired (for afflicted entothropes) template that can be added to any humanoid.
>
> **Challenge Rating:** Base humanoid's or base vermin's CR (whichever is higher) + 1.
>
> **Size and Type:** The humanoid (referred to as the base creature) gains the shapechanger subtype. The entothrope takes on the characteristics of a type of vermin (referred to as the base vermin) within one size category of the base creature's size. An entothrope's hybrid form is the same size as the base creature or base vermin, whichever is larger.
>
> **Armor Class:** In hybrid or vermin form, the entothrope uses the base vermin's natural armor bonus or gains a +2 natural armor bonus, whichever is higher.
>
> **Defensive Abilities:** A natural entothrope gains DR 10/ silver in hybrid or vermin form. An afflicted entothrope gains DR 5/silver in hybrid or vermin form.
>
> **Speed:** Same as the base creature's or base vermin's speed, depending on which form the entothrope is using. Hybrids use the base creature's speed, unless the entothrope has a CR of 5 or higher, in which case it gains all of the base vermin's additional speeds (such as a climb or fly speed) in hybrid form.
>
> **Melee:** An entothrope gains natural attacks in hybrid and vermin forms according to the base vermin.
>
> **Special Abilities:** An entothrope retains all the special attacks, qualities, and abilities of the base creature. In hybrid or vermin form, it gains the special attacks, qualities, and abilities of the base vermin. An entothrope also gains darkvision 60 feet and the following abilities.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.6eg1Ty9OTGAwsg3l inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.9vBKx5YXJgz6QIM7 inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.afr4ozW3FnCJz5Le inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.ogoetILszkI0IOHb inline=true]
>
> **Ability Scores:** Int –2 and Wis +2 in all forms; Dex +2 and Con +2 in hybrid and vermin forms. Entothropes are observant, but their minds work in inefficient ways. In addition to these adjustments to the base creature's stats, an entothrope's ability scores change when she assumes hybrid or insect form. In human form, the entothrope's ability scores are unchanged from the base creature's form. In hybrid and insect form, the entothrope's ability scores are the same as the base creature's or the base vermin's, whichever ability score is higher.

**Mechanical encoding:** `changes`: 3
  - `2` → `wis`  (untyped)
  - `2` → `nac`  (base)
  - `-2` → `int`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Entropic
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1116 (PZO1116) p. 292
**Foundry id:** `pF1B9lqYMsFF7mie`

> Creatures with the entropic template live in planes where chaos is paramount. They can be summoned using spells such as summon monster and planar ally. An entropic creature's CR increases by +1 only if the base creature has 5 or more HD. An entropic creature's quick and rebuild rules are the same.
>
> **Rebuild Rules**: **Senses** gains darkvision 60 ft.; **Defensive Abilities** gains DR and energy resistance as noted on the table; **SR** gains SR equal to new CR +5; **Special Attacks** @UUID[Compendium.pf1.template-abilities.Item.2mN1Ufe2zie7P1iM] 1/day as a swift action (adds Cha bonus to attack rolls and damage bonus equal to HD against lawful foes; smite persists until the target is dead or the entropic creature rests).
>
> **Entropic Creature Defenses**
>
>
> **Hit Dice**
>
>
> **Resist Acid and Fire**
>
>
> **DR**
>
>
> 1-4
>
>
> 5
>
>
> —
>
>
> 5-10
>
>
> 10
>
>
> 5/lawful
>
>
> 11+
>
>
> 15
>
>
> 10/lawful

**Mechanical encoding:** `changes`: 1
  - `@details.cr.total + 5` → `spellResist`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Eruphyte
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `7A0hhL9d0DhoJJX7`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> The Astral Plane, the realm of thought and higher consciousness, hosts two vulnerable sources of information: astral bodies connected to spellcasters’ physical forms by invisible silver cords, and souls bound for the Boneyard. When either vessel is disrupted or destroyed, there is a small chance that the victim’s fragmented intellect will pass along a fraying silver cord or through a weakened planar barrier. Mixed with the Astral Plane’s raw cognitive force, this tumultuous information vents into the Material Plane. For esoteric reasons not fully understood by scholars, sentient plants make ideal vessels for these proto-intellects, where they either instill a rudimentary mind in a formerly thoughtless plant or bolster existing mental capabilities. These eruphyte creatures become conduits for raw thought and vast stores of knowledge.
>
> "Eruphyte" is an acquired template that can be added to any plant creature, referred to hereafter as the base creature. An eruphyte creature uses the base creature’s statistics and abilities except as noted here.
>
> **Challenge Rating:** The base creature’s CR + 1.
>
> **Senses:** An eruphyte creature gains the following sense.
>
> *Thoughtsense (Su): *An eruphyte creature notices and locates living, conscious creatures within 60 feet as if it possessed the blindsight ability. Spells such as nondetection or mind blank make a creature undetectable by this sense.
>
> **Special Attacks:** An eruphyte creature gains the following special attack.
>
> *Thoughtspear (Su):* Once per hour as a standard action, an eruphyte creature can direct a blast of disorienting mental energy at a creature within 120 feet. This attack deals 1d8 damage for every 2 Hit Dice the eruphyte creature has (rounded down, minimum 1d8), and the target cannot attempt Knowledge skill checks for 1 minute afterwards. A target that succeeds at a Will saving throw (DC = 10 + half the eruphyte creature’s HD + its Intelligence modifier) reduces the damage by half and negates the skill disruption. This is a mind-affecting effect.
>
> **Languages:** An eruphyte creature gains telepathy (60 ft.).
>
> **Special Qualities:** An eruphyte creature gains the bardic knowledge ability with an effective bard level equal to half its HD, rounded down.
>
> **Abilities:** Int +6. An eruphyte creature gains feats and skill points according to its new Intelligence score. Eruphyte creatures typically receive feats that enhance their preexisting behavior patterns or enable new means of achieving the same goals. Eruphyte creatures with Intelligence scores of 10 or higher may receive feats that enable more advanced behaviors, tactics, or even social patterns, as befits their situation. They typically gain skill ranks in Knowledge or other Intelligence-based skills.

**Mechanical encoding:** `changes`: 1
  - `6` → `int`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Exoskeleton
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** Bestiary 5 (PZO1137) p. 124-125
**Foundry id:** `055IbpMbY3yfbwPb`

> "Exoskeleton" is an acquired template that can be added to any corporeal vermin that has an exoskeleton (referred to hereafter as the base creature).
>
> **Challenge Rating:** Depends on Hit Dice, as follows.
>
>
> **Hit Dice**
>
>
> **CR**
>
>
> **XP**
>
>
> 1
>
>
> 1/4
>
>
> 100
>
>
> 2
>
>
> 1/2
>
>
> 200
>
>
> 3-4
>
>
> 1
>
>
> 400
>
>
> 5-6
>
>
> 2
>
>
> 600
>
>
> 7-8
>
>
> 3
>
>
> 800
>
>
> 9-10
>
>
> 4
>
>
> 1,200
>
>
> 11-12
>
>
> 5
>
>
> 1,600
>
>
> 13-15
>
>
> 6
>
>
> 2,400
>
>
> 16-17
>
>
> 7
>
>
> 3,200
>
>
> 18-20
>
>
> 8
>
>
> 4,800
>
>
> 21-24
>
>
> 9
>
>
> 6,400
>
>
> 25-28
>
>
> 10
>
>
> 9,600
>
>
> **Alignment:** Always neutral evil.
>
> **Type:** The creature's type changes to undead. It retains any subtype except for alignment subtypes and subtypes that indicate kind. It does not gain the augmented subtype. It uses the base creature's abilities except as noted below.
>
> **Armor Class:** The base creature's natural armor changes as follows.
>
>
> **Exoskeleton Size**
>
>
> **Natural Armor Bonus**
>
>
> Tiny or smaller
>
>
> +0
>
>
> Small
>
>
> +1
>
>
> Medium
>
>
> +2
>
>
> Large
>
>
> +3
>
>
> Huge
>
>
> +4
>
>
> Gargantuan
>
>
> +7
>
>
> Colossal
>
>
> +11
>
>
> **Hit Dice:** An exoskeleton retains the number of Hit Dice the base creature had, and gains a number of additional Hit Dice as noted on the following table. If the base creature has more than 20 Hit Dice, it can't be made into an exoskeleton by the @UUID[Compendium.pf1.spells.Item.8uwmrygxgih1fb57] spell. An exoskeleton uses its Charisma modifier (instead of its Constitution modifier) to determine bonus hit points.
>
>
> **Exoskelton Size**
>
>
> **Bonus Hit Dice**
>
>
> Tiny or smaller
>
>
> —
>
>
> Small or Medium
>
>
> +1
>
>
> Large
>
>
> +2
>
>
> Huge
>
>
> +4
>
>
> Gargantuan
>
>
> +6
>
>
> Colossal
>
>
> +10
>
>
> **Saves:** Base save bonuses are Fort +1/3 Hit Dice, Ref +1/3 Hit Dice, and Will +1/2 Hit Dice + 2.
>
> **Defensive Abilities:** Exoskeletons lose their defensive abilities and gain all of the qualities and immunities granted by the undead type. In addition, exoskeletons gain DR 5/bludgeoning.
>
> **Speed:** Exoskeletons retain all movement speeds. They can still fly but their maneuverability drops to clumsy.
>
> **Attacks:** An exoskeleton retains all of its natural weapons. If the base creature didn't have any natural weapons, it gains a @UUID[Compendium.pf1.monster-abilities.Item.GrbQIXcmp5VXxYA7] attack that deals damage as if it were one size category larger than its actual size.
>
> **Special Attacks:** An exoskeleton loses all of its special attacks that rely on a living biology (such as @UUID[Compendium.pf1.monster-abilities.Item.R4HTn8pmyiBaMTC5]), but it retains any others.
>
> **Abilities:** An exoskeleton's Strength increases by 2. The exoskeleton has no Constitution or Intelligence score, and its Wisdom and Charisma scores change to 10.
>
> **BAB:** An exoskeleton's base attack bonus is equal to 3/4 of its Hit Dice.
>
> **Skills:** Though most vermin are mindless and have no skill ranks, the exoskeleton loses all skill ranks if it had any, and it doesn't retain any racial bonuses it had.
>
> **Feats:** An exoskeleton loses all feats that the base creature had and doesn't gain feats as its Hit Dice increase, but it does gain Toughness as a bonus feat.
>
> **Special Qualities:** An exoskeleton loses most special qualities of the base creature. It retains any extraordinary special qualities that improve its melee or ranged attacks. An exoskeleton gains the following special quality.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.tMpw0Jcn5d3jmmWc inline=true]

**Mechanical encoding:** `changes`: 5
  - `1` → `bonusFeats`  (untyped)
  - `10` → `wis`  (untyped)
  - `10` → `cha`  (untyped)
  - `2` → `str`  (untyped)
  - `lookup(@size, 0, 0, 0, 1, 2, 3, 4, 7, 11)` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Failed Prophet
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `UDLZNEeVb4DWar2e`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> When a Kalistocrat performs the final rites to create her idealized afterlife, the likelihood of success depends on how stringently she adhered to Kalistrade’s teachings and how much wealth she sacrificed to serve as an occult anchor for her will. It’s not always apparent which prophets succeed, and mere weeks after death, the mindscapes of those prophets who failed begin to collapse. For most, their souls become untethered and join the River of Souls, but others cling tenaciously to their failed dream, and their consciousness escapes into and animates their gold-veined bodies.
>
> Some of these so-called failed prophets eventually slip out of their shells and accept Pharasma’s judgment. Others refuse to accept their own failure and attempt to perform the ritual again after accumulating far more wealth than before. These failed prophets often break out of their mausoleums to hunt down the wealthy and steal their treasure—or worse, dismantle the precious bodies of other Kalistocrats for scrap, sending the mindscapes of their onetime allies hurtling to the Astral Plane to be torn apart by predators or astral weather.
>
> "Failed prophet" is an acquired template that can be added to any living creature with 5 or more Hit Dice. A failed prophet retains all the base creature’s statistics and special abilities except as noted here.
>
> **CR:** The base creature’s CR + 2.
>
> **Type:** The creature’s type changes to construct with the augmented subtype. The failed prophet retains all subtypes except alignment subtypes (such as good). Do not recalculate BAB, saves, or skill ranks.
>
> **Senses:** A failed prophet gains darkvision 60 feet as well the following ability.
>
> *Silver Scent (Ex)*: A failed prophet can sense valuable materials as if using the scent universal monster rule. A failed prophet can attempt a DC 20 Appraise check as a free action to identify the relative values of detected wealth.
>
> **Armor Class:** A failed prophet has a +5 natural armor bonus or the base creature’s natural armor bonus, whichever is better.
>
> **Hit Dice:** Change all of the base creature’s racial Hit Dice to d10s. All Hit Dice derived from class levels remain unchanged. As constructs, failed prophets gain bonus hit points based on their size.
>
> **Defensive Abilities:** A failed prophet gains DR 10/ bludgeoning and magic, a +4 bonus on saving throws against mind-affecting effects, and immunity to cold and electricity. The failed prophet also gains the immunities normally granted by her construct traits, except for the construct type’s immunity to mind-affecting effects. Failed prophets also gain the following defensive ability.
>
> *Revel in Wealth (Ex):* A failed prophet gains fast healing equal to her Hit Dice so long as she has wealth stored in her personal vault (see below) worth at least 1,000 gp. Melee Attack: A failed prophet gains two claw attacks if the base creature didn’t already have them. These claws have a reach equal to the base creature’s natural reach plus 5 feet and deal damage as if the prophet were one size larger than she actually is. In place of making a claw attack, a failed prophet can instead attempt a touch attack that deals no damage but allows her to use her greedy grab special attack. The failed prophet’s natural weapons are treated as magic weapons for the purpose of overcoming damage reduction. Special Attacks: A failed prophet gains the following special attacks.
>
> *Aurokinesis:* A failed prophet can hurl shards of her body, gaining the gather power and kinetic blast abilities of a kineticist with a level equal to the prophet’s CR – 2. She also gains the earth blast kinetic blast and a number of infusions equal to 1/3 the prophet’s CR (rounded up). A failed prophet of CR 10 or higher also gains the metal blast composite blast. If a failed prophet already has the kinetic blast class ability, she can instead either gain the internal buffer class ability of a kineticist whose level is equal to the prophet’s CR or increase the number of points her internal buffer can store by 2; in either case, she restores her buffer to its maximum capacity every 24 hours.
>
> For the purpose of calculating the save DCs and damage for her kineticist abilities, the prophet chooses either her Intelligence, Wisdom, or Charisma score and uses that in place of her Constitution score. Once this choice is made, it cannot be changed.
>
> *Greedy Grab (Ex):* When a failed prophet hits a creature with her claw attack or a touch attack, she can attempt a free steal combat maneuver with a +4 racial bonus to steal the target’s wealth; this does not provoke an attack of opportunity. If successful, the prophet grabs mundane valuables from the target equal to 100 gp × the failed prophet’s Hit Dice, shoveling them into her personal vault (see below). A failed prophet cannot steal more wealth than her target has.
>
> *Personal Vault (Ex): *A failed prophet can stow small objects and mundane valuables within her body, up to 500 gp × her Hit Dice. Creatures can steal individual objects from this extradimensional space with a successful steal combat maneuver or Sleight of Hand check, though either of these checks takes a –5 penalty.
>
> *Plutophage (Ex):* A failed prophet can siphon the value from the valuables in her personal vault equal to 100 gp × her Hit Dice to negate 1 point of burn whenever she would accept burn from her aurokinesis. Ability Scores: Str +6, Dex +2, Int +2, Wis +4, Cha +2. A failed prophet has no Constitution score. Skills: Failed prophets have a +4 racial bonus on Appraise, Knowledge (arcana), Knowledge (religion), Perception, Sense Motive, and Stealth checks. A failed prophet’s skills are the same as those of the base creature, except she treats Knowledge (arcana) and Knowledge (religion) as class skills as well.

**Mechanical encoding:** `changes`: 1
  - `5` → `nac`  (base)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fey Animal
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `y6WppzM6841RW6a0`

> **Acquired/Inherited Template** Both**Simple Template** No**Usable with Summons** Yes
>
> "Fey animal" is an inherited or acquired template that can be added to a living, corporeal animal (referred to hereafter as the base creature). A fey animal uses all the base creature’s statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature +1.
>
> **Type:** Creature type changes to fey. It gains the augmented subtype. Do not recalculate Hit Dice, Base Attack Bonus, skills, or saves.
>
> **Alignment:** Any chaotic.
>
> **Armor Class:** A fey creature’s natural armor bonus increases by +1.
>
> **Special Qualities and Defenses:** A fey animal gains darkvision 60 feet and low-light vision if it didn’t already possess it. It also gains DR 5/cold iron (DR 10/cold iron if it has 11 or more Hit Dice) and SR equal to its CR + 11.
>
> **Speed:** All of the fey creature’s movement speeds increase by 10 feet.
>
> **Special Attacks:** A fey animal gains the special attack described below. Save DCs are equal to 10 + 1/2 the fey animal’s Hit Dice + the fey animal’s Charisma modifier.
>
> *Death Curse (Su):* When a creature slays a fey animal, the slayer is cursed with ill luck unless it makes a successful Will saving throw to resist the curse. If it fails to resist, the victim takes a –2 penalty on all attack rolls, ability checks, skill checks, and saving throws until the curse is removed. The total penalty from multiple fey animal death curses stacks, but the multiple death curses count as a single curse overall for the purposes of removing its effects. A fey creature can see this curse on a creature as an angry red halo around the victim’s head.
>
> **Spell-Like Abilities:** A fey animal has a cumulative number of spell-like abilities set by its HD. Unless otherwise noted, an ability is usable 1/day. The CL equals the fey animal’s CR.
>
> **Abilities:** Dex +4, Int +10 (to a maximum score of 12), Wis +2, Cha +4.
>
> **Skills:** A fey animal gains a +4 racial bonus on Bluff and Stealth checks, and has skill points per racial Hit Die equal to 6 + its Intelligence modifier. Its racial class skills are Acrobatics, Bluff, Climb, Diplomacy, Fly, Knowledge (nature), Perception, Sense Motive, Stealth, and Swim.
>
> **Languages:** Fey animals speak Sylvan plus one other language common to the region.
>
>
>
>
>  **HD Spell-Like Abilities** 
>
>
>  1–3 
>  *charm person*, *faerie fire* 
>
>
>  4–6 
>  *fly *(3/day), *tree shape* 
>
>
>  7–9 
>  *charm monster*, *hallucinatory terrain* 
>
>
>  10–13 
>  *polymorph *(3/day), *summon nature’s ally IV* 
>
>
>  14–16 
>  *feeblemind*, *transport via plants* 
>
>
>  17 or higher 
>  *mass charm monster*, *summon nature’s ally VIII*

**Mechanical encoding:** `changes`: 6 (showing first 5)
  - `10` → `allSpeeds`  (untyped)
  - `2` → `wis`  (untyped)
  - `4` → `dex`  (untyped)
  - `1` → `nac`  (untyped)
  - `10` → `int`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fey Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1120 (PZO1120) p. 116-117
**Foundry id:** `aTUEmCxUcbdAqgRO`

> Fey creatures resemble the mundane creatures they derive from, but with brighter colors, delicate features, and elegant wings such as those of a pixie or sprite. Despite their fragile-seeming appearance, fey creatures are every bit as hardy as their non-fey relations, though they sacrifice raw might for grace and the ability to fly. They live long lives, barring death by misadventure, and rarely show outward signs of age.
>
> Some fey creatures owe their nature to fey ancestors interbreeding with mortal beings, while others are races in their own right. Still others began life as ordinary creatures and were infused with fey essence through the magic of learned spellcasters or the influence of ancient powers of nature. As a rule, fey creatures rarely dwell in civilized lands, both by preference and because the conditions that give rise to the fey rarely occur in urban surroundings. If not already born into realms of primeval wild or areas touched by great fey powers, fey creatures soon seek them out.
>
> Though more prone to mischief than mayhem, fey creatures run the gamut from inimical to sprightly in behavior. Those inclined toward play and jest take a dim view of interlopers lacking in good humor. Such foul-tempered intruders risk humiliation at best if they insult the fey, and much worse if they raise arms against them. More aggressive fey still possess a well-developed though sadistic sense of humor. Such wicked fey use their inborn powers to lure outsiders to their doom, rather than into mere inconvenience.
>
> Fey creatures generally have cordial relationships with animals, allies of nature such as druids, and other fey. Exceptions exist where rival communities of fey dwell in proximity to one another. In these cases, any fey creatures in the vicinity ally with one side or the other according to their own inclinations, only rarely standing outside such conflicts. Fey creatures derived from horses and the like often serve as mounts, though only to other fey or to allies of nature who acknowledge them as at least near-equals, if not full partners.
>
> "Fey Creature" is an inherited or acquired template that can be added to any living, corporeal creature. A fey creature retains the base creature's statistics and special abilities except as noted here.
>
> **CR:** 9 HD or less, as base creature +1; 10 HD or more, as base creature +2.
>
> **Alignment:** Any non-lawful.
>
> **Type:** The creature's type changes to fey. Do not recalculate HD, BAB, or saves.
>
> **Senses:** A fey creature gains low-light vision.
>
> **Armor Class:** Reduce the creature's natural armor, if any, by 1 (minimum of 0).
>
> **Defensive Abilities:** A fey creature gains a +4 bonus on saves against mind-affecting effects, resist cold and electricity 10, and DR 5/cold iron (if 11 HD or less) or DR 10/cold iron (if 12 HD or more).
>
> **Speed:** Unless the base creature flies better, the fey creature flies at 1-1/2 times the base creature's land speed (good maneuverability), rounded down to the nearest multiple of 5 feet. If the creature already has flight with a maneuverability of good, it increases to perfect.
>
> **Special Abilities:** A fey creature gains one of the following abilities for every 4 HD or fraction thereof.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.cTwDHFgLZzCfNZBt inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.FX7luSAlUPL0zDHs inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.Y59t64yKUD2y6z3f inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.5Pg6n2hbi6r3F80Z inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.FXVYkFXwY1nBM5a9 inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.mVBeF0wnBk6xcORi inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.1bzfZmr8EfJ1iyPg inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.d3XNifdnQXOK3wul inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.hAlJoAofhar5Eps2 inline=true]
>
> **Spell-Like Abilities:** A fey creature with an Intelligence or Wisdom score of 8 or more has a cumulative number of spell-like abilities depending on its Hit Dice. Unless otherwise noted, an ability is usable once per day. Caster level equals the creature's HD (or the caster level of the base creature's spell-like abilities, whichever is higher).
>
>
> 1–2
>
>
> @UUID[Compendium.pf1.spells.Item.zymaptg3vmnvfvxl]* *3/day, @UUID[Compendium.pf1.spells.Item.bl71og1gklwncmt7]
>
>
> 3–4
>
>
> @UUID[Compendium.pf1.spells.Item.2nn2tshkn4p7k25l], @UUID[Compendium.pf1.spells.Item.ec2zmvdzi4m3puh4]
>
>
> 5–6
>
>
> @UUID[Compendium.pf1.spells.Item.qgmlu83z2l84kjde]
>
>
> 7–8
>
>
> @UUID[Compendium.pf1.spells.Item.7rx66m98dwo18fy8]
>
>
> 9–10
>
>
> @UUID[Compendium.pf1.spells.Item.n0bsyxchnigkkuqo]
>
>
> 11–12
>
>
> @UUID[Compendium.pf1.spells.Item.66vvhyiy5q8yzbq2]
>
>
> 13–14
>
>
> @UUID[Compendium.pf1.spells.Item.446vcsetq4ny904e]
>
>
> 15–16
>
>
> @UUID[Compendium.pf1.spells.Item.0w3hvcp3gb2bhtv5]
>
>
> 17–18
>
>
> @UUID[Compendium.pf1.spells.Item.oq3mqv5vovjkoa2p]
>
>
> 19–20
>
>
> @UUID[Compendium.pf1.spells.Item.34jyuvdflia4goib]
>
>
> **Abilities:** A fey creature gains a +4 bonus to Dexterity and a +2 bonus to Intelligence and Charisma. A fey creature receives a –2 penalty to Strength. Fey creatures derived from creatures without an Intelligence score gain an Intelligence of 3.
>
> **Skills:** A fey creature with racial Hit Dice has skill points per racial Hit Die equal to 6 + its Intelligence modifier. It gains Acrobatics, Bluff, Fly, and Stealth as class skills.
>
> **Languages:** Fey creatures speak Sylvan as well as any languages spoken by the base creature.

**Mechanical encoding:** `changes`: 7 (showing first 5)
  - `2` → `int`  (untyped)
  - `4` → `dex`  (untyped)
  - `if(gte(@ac.natural.total, 1), -1)` → `nac`  (untyped)
  - `-2` → `str`  (untyped)
  - `ifelse(not(@abilities.int.total), 3, @abilities.int.total)` → `int`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fey-Touched Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `VBHPKsaj8qPHd6Rs`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** Yes - Spellcasters with ties to the fey (such as sorcerers with the fey bloodline) can summon fey-touched creatures with summon monster spells
>
> Fey-touched creatures are descended from inhabitants of the First World and often possess striking features compared to their normal counterparts, such as bright coloration or a cunning visage. The fey-touched creature's First World ancestor needn't be a fey specifically, and even magical beasts, First World gnomes, and other non-fey inhabitants of the fecund, magical plane can produce fey-touched heirs generations after their initial dalliance with residents of other planes. Some fey-touched creatures thus claim to be descended from the legendary Tane and even the godlike Eldest, though these claims are likely unfounded — such claims themselves intentional or accidental manifestations of the creature's hereditary First World influence.
>
> A fey-touched creature's CR increases by 1 only if the base creature has 5 or more Hit Dice. The fey-touched creature template can be applied only to living creatures. A fey-touched creature's quick and rebuild rules are the same. Spellcasters with ties to the fey (such as sorcerers with the fey bloodline) can summon fey-touched creatures with summon monster spells and take fey-touched creatures as improved familiars at 3rd level, similar to selecting celestial or infernal familiars.
>
> **Rebuild Rules:** Senses gains low-light vision;
>
> **Defensive Abilities** gains +2 bonus on Will saves and DR as noted on the table; SR gains SR equal to new CR +5;
>
> **Special Qualities** change shape (a single fixed Small or Medium humanoid form, alter self), woodland stride (as the druid ability).
>
> **Fey-touched Creature Defenses**
>
>
> **Hit Dice**
>
>
> **DR**
>
>
> 1-4
>
>
> —
>
>
> 5-10
>
>
> 5/cold iron
>
>
> 11+
>
>
> 10/cold iron

**Mechanical encoding:** `changes`: 1
  - `2` → `will`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fiend-Infused
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `KYvuUMQ7YxV95pBN`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** No
>
> Although most golems are animated by the spirits of elementals, certain reckless or daring golem crafters instead bind evil outsiders such as daemons, demons, and devils to power golems. This fiend does not inhabit or control the golem in the usual manner of fiendish possession; instead, the outsider is subjugated within the golem to act as a mere engine. Although a fiend-infused golem has more self-awareness and cunning than a typical golem, it possesses only a brute, primitive intellect, lacking the animating fiend’s personality beyond a base desire to destroy goodness. The fiend’s rage at being imprisoned in such a manner manifests as ever-burning hellfire, which the fiend-infused golem uses as a weapon against its foes.
>
> As with ordinary golems, fiend-infused golems primarily serve as guards or defenders. However, a fiend-infused golem’s marginally improved intellect means it can be given more complex instructions, such as evaluating an intruder’s intent, activating or deactivating traps, acting in disguise, or patrolling a convoluted territory. Although fiend-infused golems are obligated to follow their creators’ commands in the same manner as regular golems, they sometimes do so with sullenness or frustrated defiance.
>
> The foremost golem crafters of antiquity served the Jistka Imperium many thousands of years ago, and that empire’s golem foundries at Rachikan experimented extensively with fiend-bound golems. Using evil outsiders as an animating force came with an inherent drawback that Rachikan’s golem crafters could never fully overcome: the fiend’s seething anger at serving within a golem increases the chance that the fiend-infused golem will break free of its command and run amok. Ultimately, the golem crafters of Rachikan succeeded only by increasing the size of their golems: Rachikan’s enormous behemoth golems (Pathfinder Campaign Setting: Lost Kingdoms 40) are the only fiendinfused golems that do not risk the bound fiend going berserk. Although the Jistka Imperium is long gone, fiend-infused golems still guard its ancient factories and treasure vaults, particularly in the ruins of Rachikan and in other hidden sites along the Chelish coast.
>
> With renewed interest in the Jistka Imperium among such organizations as the Pathfinder Society and Egorian’s prestigious Athenaeum, ancient secrets of fiend-infused golems have leaked to several modern golem crafters. Some of these crafters had already developed their own techniques for creating fiend-infused golems, and use the unearthed Jistkan lore to confirm or supplement their own designs. The artificers of House Thrune are particularly interested in harnessing and improving upon the Jistkan methods, both because the golems promise to be very powerful additions to the Thrune arsenal and because they are always looking for new ways to bind the spirits of Hell.
>
> A fiend-infused golem is the same size and weight as an ordinary golem of its type.
>
> "Fiend-infused" is a template that can be added to any golem that is not vulnerable to fire (referred to hereafter as the base creature). The fiend-infused template must be applied when the golem is created; an existing golem can’t later acquire this template. A fiend-infused golem uses all of the base creature’s statistics and special abilities except as noted here.
>
> **CR:** Base creature’s CR + 2.
>
> **Alignment:** Always neutral evil.
>
> **Defensive Abilities:** Fiend-infused golems gain fast healing 5 and immunity to fire. If the base creature already has damage reduction, it adds good to the qualities needed to bypass that reduction. If the base creature has the immunity to magic defensive ability, it adds susceptibility to banishment and dismissal (see the immunity to magic ability above).
>
> **Special Attacks:** A fiend-infused golem gains the berserk liberation special attack described above and loses any berserk special attack of the base creature. The amount of damage dealt when the fiend-infused golem goes berserk is equal to 1d6 × its CR (Reflex half; DC = 10 + 1/2 the golem’s Hit Dice + the golem’s Constitution modifier). A fiend-infused golem also gains the hellfire touch special attack described above.
>
> **Abilities:** A fiend-infused golem’s Intelligence score changes to 4 and its Charisma score changes to 10.**Feats: A fiend-infused golem has feats appropriate for its Hit Dice. The golem’s creator determines the golem’s feats as part of the process of creating the construct. Fiend-infused golems can be assigned any feats they are physically capable of using, although most feats are assigned from the following: Blind-Fight, Combat Reflexes, Intimidating Prowess, Power Attack, Skill Focus (Intimidate), Toughness, and Weapon Focus.
>
> Skills:** A fiend-infused golem gains ranks in Intimidate equal to its Hit Dice.
>
> **Languages:** A fiend-infused golem understands Abyssal and Infernal, but it cannot speak.
>
> **Construction:** A fiend-infused golem’s base materials cost an additional 25,000 gp above the base creature’s cost to account for the materials that are needed to bind the fiend within the golem. Add the spells dimensional anchor, magic circle against evil, and either planar ally or planar binding to the base creature’s requirements.
>
> The DC of the Craft check required to make the fiend-infused golem’s body is 4 higher than the base creature’s construct skill DC, and the creator must have a minimum caster level 4 higher than the base creature’s minimum required caster level. The increase to the DC of the Craft check and to the caster level are halved (to 2 higher) if the creator possesses at least 10 ranks in Knowledge (planes).

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fiendish
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 294
**Foundry id:** `kDaBd3zlTauG2f9n`

> Creatures with the fiendish template live in the Lower Planes, such as the Abyss and Hell, but can be summoned using spells such as summon monster and planar ally. A fiendish creature's CR increases by +1 only if the base creature has 5 or more HD. A fiendish creature's quick and rebuild rules are the same.
>
> **Rebuild Rules:** **Senses** gains darkvision 60 ft.; **Defensive Abilities** gains DR and energy resistance as noted on the table; **SR** gains SR equal to new CR +5; **Special Attacks** @UUID[Compendium.pf1.template-abilities.Item.3XEQ0B8GADTxGKKD] 1/day as a swift action (adds Cha bonus to attack rolls and damage bonus equal to HD against good foes; smite persists until target is dead or the fiendish creature rests).
>
> **Fiendish Creature Defenses**
>
>
> **Hit Dice**
>
>
> **Resist Cold and Fire**
>
>
> **DR**
>
>
> 1-4
>
>
> 5
>
>
> —
>
>
> 5-10
>
>
> 10
>
>
> 5/good
>
>
> 11+
>
>
> 15
>
>
> 10/good

**Mechanical encoding:** `changes`: 1
  - `@details.cr.total + 5` → `spellResist`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fiery
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9458 (PZO9458) p. 19
**Foundry id:** `ubKX7esqMFnhbExt`

> **Usable with Summons** Yes - Requires the feat @UUID[Compendium.pf1.feats.Item.ezNxW33BtSafLl0J] or @UUID[Compendium.pf1.feats.Item.R5nnb83RW7qHkVmA]
>
> Fiery creatures are native denizens of the Elemental Planes of Fire, and act as conduits to the burning energies of their home plane. This template can be applied only to a non-outsider that has none of the following subtypes: air, cold, earth, fire, or water. Creatures with a swim speed can’t be fiery creatures. A fiery creature’s CR increases by 1 only if the base creature has 5 or more HD.
>
> **Rebuild Rules:** **Type** gains the fire subtype; **Senses** gains darkvision 60 ft.; **Defensive Abilities** gains DR as noted on the table below; **Attacks** gains bonus fire damage as noted on the table below on attacks with natural weapons and metal weapons.
>
>
> **Hit Dice**
>
>
> **DR**
>
>
> **Fire Damage**
>
>
> 1-4
>
>
> -
>
>
> 1 point
>
>
> 5-10
>
>
> 3/-
>
>
> 1d6
>
>
> 11+
>
>
> 5/-
>
>
> 2d6

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fighter (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 247
**Foundry id:** `N2fasf8I2icC7JTI`

> A fighter creature gains bonus combat feats, and both armor and weapon training. A fighter creature's CR increases by 2 if the creature has 10 or more HD.
>
> **Quick Rules:** +2 on all rolls based on Str; gains a bonus combat feat and an additional bonus combat feat for every 4 HD (to a maximum of 10 feats; a fighter creature is considered a fighter with a level equal to its HD for the purpose of qualifying for combat feats). If the creature has 3 or more HD, it gains @UUID[Compendium.pf1.class-abilities.Item.5JFfSqLMCpbRmERa] (the bonus increases and penalty decreases for every 4 HD the creature possesses thereafter, to the class feature's normal maximums). If the creature has 5 or more HD, it gains @UUID[Compendium.pf1.class-abilities.Item.RzEzudurxQFirFoF] (the creature gains only one weapon group, and its bonuses increase by 1 every 4 HD thereafter, to a maximum of +4).
>
> **Rebuild Rules:** **Special Attacks** If the creature has 5 or more HD, it gains @UUID[Compendium.pf1.class-abilities.Item.RzEzudurxQFirFoF] (the creature gains only one weapon group, and its bonuses increase by 1 every 4 HD thereafter, to a maximum of +4); **Special Abilities** If the creature has 3 or more HD, it gains @UUID[Compendium.pf1.class-abilities.Item.5JFfSqLMCpbRmERa] (the bonus increases and penalty decreases for every 4 HD it possesses thereafter, to the class feature's normal maximums); **Ability Scores** +4 Strength; **Feats** The creature gains a bonus combat feat and an additional combat feat for every 4 HD (to a maximum of 10 feats from this ability).

**Mechanical encoding:** `changes`: 5
  - `2` → `strSkills`  (untyped)
  - `2` → `strChecks`  (untyped)
  - `2` → `wdamage`  (untyped)
  - `2` → `mattack`  (untyped)
  - `min(10, 1 + floor(@attributes.hd.total / 4))` → `bonusFeats`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fighter (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 247
**Foundry id:** `Vx8af8Biu7abYsDm`

> A fighter creature gains bonus combat feats, and both armor and weapon training. A fighter creature's CR increases by 2 if the creature has 10 or more HD.
>
> **Quick Rules:** +2 on all rolls based on Str; gains a bonus combat feat and an additional bonus combat feat for every 4 HD (to a maximum of 10 feats; a fighter creature is considered a fighter with a level equal to its HD for the purpose of qualifying for combat feats). If the creature has 3 or more HD, it gains @UUID[Compendium.pf1.class-abilities.Item.5JFfSqLMCpbRmERa] (the bonus increases and penalty decreases for every 4 HD the creature possesses thereafter, to the class feature's normal maximums). If the creature has 5 or more HD, it gains @UUID[Compendium.pf1.class-abilities.Item.RzEzudurxQFirFoF] (the creature gains only one weapon group, and its bonuses increase by 1 every 4 HD thereafter, to a maximum of +4).
>
> **Rebuild Rules:** **Special Attacks** If the creature has 5 or more HD, it gains @UUID[Compendium.pf1.class-abilities.Item.RzEzudurxQFirFoF] (the creature gains only one weapon group, and its bonuses increase by 1 every 4 HD thereafter, to a maximum of +4); **Special Abilities** If the creature has 3 or more HD, it gains @UUID[Compendium.pf1.class-abilities.Item.5JFfSqLMCpbRmERa] (the bonus increases and penalty decreases for every 4 HD it possesses thereafter, to the class feature's normal maximums); **Ability Scores** +4 Strength; **Feats** The creature gains a bonus combat feat and an additional combat feat for every 4 HD (to a maximum of 10 feats from this ability).

**Mechanical encoding:** `changes`: 2
  - `min(10, 1 + floor(@attributes.hd.total / 4))` → `bonusFeats`  (untyped)
  - `4` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fleshwarped Creature (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `r4JTr4PeaaMmNOoM`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> These creatures are twisted by fleshwarping, grants horrific abilities by perverting creatures’ original forms. This template can be applied only to corporeal living creatures.
>
> **Quick Rules:** +2 to AC and CMD; +2 to attack rolls and damage rolls; +2 hp/HD; +2 on rolls based on Str and Dex; –2 on rolls based on Int and Cha; the creature gains a new movement mode (climb, burrow, fly [clumsy], or swim) with a speed of 30 ft.
>
> **Rebuild Rules:** AC increase natural armor bonus by 2; Movement The creature gains a movement new movement mode (climb, burrow, fly [clumsy], or swim) with a speed of 30 ft.; Ability Scores +4 Str, +4 Con, –4 Int, –4 Cha.

**Mechanical encoding:** `changes`: 13 (showing first 5)
  - `2` → `ac`  (untyped)
  - `-2` → `chaChecks`  (untyped)
  - `-2` → `intSkills`  (untyped)
  - `-2` → `chaSkills`  (untyped)
  - `2` → `damage`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fleshwarped Creature (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `OeUX6hPFCspymTnV`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> These creatures are twisted by fleshwarping, grants horrific abilities by perverting creatures’ original forms. This template can be applied only to corporeal living creatures.
>
> **Quick Rules:** +2 to AC and CMD; +2 to attack rolls and damage rolls; +2 hp/HD; +2 on rolls based on Str and Dex; –2 on rolls based on Int and Cha; the creature gains a new movement mode (climb, burrow, fly [clumsy], or swim) with a speed of 30 ft.
>
> **Rebuild Rules:** AC increase natural armor bonus by 2; Movement The creature gains a movement new movement mode (climb, burrow, fly [clumsy], or swim) with a speed of 30 ft.; Ability Scores +4 Str, +4 Con, –4 Int, –4 Cha.

**Mechanical encoding:** `changes`: 5
  - `-4` → `int`  (untyped)
  - `-4` → `cha`  (untyped)
  - `2` → `nac`  (untyped)
  - `4` → `str`  (untyped)
  - `4` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Floodslain
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `8sJxllkGBnqqUgu5`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Collectively known as "the after-storm" by Belkzen natives, floodslain are victims of flash floods that have risen as undead. They’re creatures of panic and despair, driven by anger, fear, and a yearning to drag others into the waters. Long after the floodwaters recede, floodslain continue spreading the miserable death that claimed them.
>
> Floodslain are similar in appearance to their original living forms, and are recognizable even in their waterlogged state. Many were gruesomely damaged by the floods that took their lives, though, their bodies battered and broken by rushing water and debris. The one feature common among all floodslain is wild, panicked eyes—a telltale sign of a death mired in shock and fear. Floodslain tend to drift toward lower ground, as if seeking the very water that transformed them. While this habitual migration makes them a contained threat in some areas, the relatively flat floodplains of Belkzen offer little resistance to the wandering undead. They can be found floating in major rivers, trapped in ravines and valleys, and staggering across flatlands, sometimes in large numbers. Floodslain that come close to living creatures try to drown them, and relentlessly follow those who flee. Targets who escape often draw the attention of yet more floodslain, eventually leading the undead to their homes. In great numbers, floodslain can slaughter small settlements.
>
> While many find the possibility of undead born from purely natural disasters to be disturbing in and of itself, theories from druids and scholars in Lastwall hold even more chilling implications. Given that floodslain are most common in eastern Belkzen yet are little known outside that region, it is suspected that the floodwater itself was cursed even before falling as snow, perhaps by the dark influence of Gallowspire. If the Whispering Tyrant’s insidious reach could extend so far using only passing clouds, the crusaders of Lastwall might be facing a threat even more dire than they realize.
>
> "Floodslain" is an acquired template that can be added to any non-aquatic living creature. A floodslain uses the base creature’s stats and abilities except as noted here.
>
> **CR:** Same as base creature + 1.
>
> **Alignment:** Chaotic evil.
>
> **Type:** The creature’s type changes to undead (augmented). Do not recalculate class BAB or saves.
>
> **Armor Class:** Natural armor increases by 2.
>
> **Hit Dice:** Change all racial Hit Dice to d8s. Class Hit Dice are unaffected. As undead, floodslain creatures use their Charisma modifiers to determine bonus hit points (instead of their Constitution modifiers).
>
> **Defensive Abilities:** A floodslain creature gains channel resistance +2, DR 5/magic, and cold resistance 10 in addition to other defensive abilities granted by the undead type.
>
> **Speed:** A floodslain creature gains a swim speed of 30 feet unless it already possesses a swim speed.
>
> **Melee:** A floodslain creature gains a slam attack based on its size, if the base creature doesn’t have one. Its slam attack also delivers the drowning touch effect (see below). Its natural attacks are treated as magic weapons for the purpose of overcoming damage reduction.
>
> **Special Attacks:** Floodslain creatures gain several special attacks. The save DCs are equal to 10 + 1/2 the base creature’s HD + its Charisma modifier unless otherwise noted.
>
> *Crashing Waters (Su): *Once per day, a floodslain creature can instinctively summon a spectral echo of the rushing waters that created it. This mass of phantom water slams the floodslain creature from behind, carrying it forward at up to three times its normal speed and enabling it to charge a single target. These waters also impact all creatures near the end of the floodslain creature’s movement, pushing them back. This acts as a bull rush; the floodslain creature attempts a single combat maneuver check against the CMD of each creature within 10 feet of the end of its charge. This bull rush attempt doesn’t provoke attacks of opportunity.
>
> *Create Spawn (Su): *Any creature killed by a floodslain creature rises as a floodslain creature if it’s left immersed in water for 24 hours. These spawn aren’t under the control of their creators.**Drowning Touch (Su): The slam attack of a floodslain creature partially fills a living victim’s lungs with water. The victim must succeed at a Fortitude saving throw in order to cough up this water or become fatigued for 1d4 rounds. A fatigued creature that fails this save becomes exhausted instead. An exhausted creature that fails this save is staggered and falls to 0 hp. A creature at 0 hp that fails this save drops to –1 hp and begins dying. A creature killed in this fashion appears to have drowned.
>
> *Panic (Su): *The dead eyes of a floodslain creature are frozen with shock and fear. The floodslain creature can induce fear in a living victim as a standard action. Targets must succeed at a Will saving throw or become shaken for 1d6 rounds. A creature can be affected by the same floodslain creature’s panic attack only once every 24 hours.
>
> Special Qualities:** A floodslain creature gains the following special quality.
>
> *Flash Flood (Su): *A floodslain creature is constantly surrounded by an echo of the disaster that originally took its life. Water streams from the floodslain creature’s body, forming a 30-foot-radius pool that renders the ground in that area slick and muddy and increases the DCs of Acrobatics checks made in the area by 5.
>
> **Ability Scores:** Str +2, Dex –2, Int +0, Wis +2, Cha +2 (minimum 14). Waterlogged and ruined, floodslain creatures are driven to cling to life by maddened fear and confusion. As undead, floodslain creatures have no Constitution scores.
>
> **Feats:** Floodslain creatures gain Toughness as a bonus feat.

**Mechanical encoding:** `changes`: 5
  - `2` → `str`  (untyped)
  - `-2` → `dex`  (untyped)
  - `2` → `cha`  (untyped)
  - `2` → `nac`  (untyped)
  - `2` → `wis`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Foo Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1120 (PZO1120) p. 120-121
**Foundry id:** `2aWJH1E2ubfojBmx`

> Foo creatures are benevolent guardian spirits that hail originally from the Outer Plane of Nirvana, where they spend their days cavorting in the idyllic wilds or aiding that realm's inhabitants, particularly the agathions, in their work. Yet while they come from Nirvana, foo creatures are often encountered on the Material Plane as well, for they are favorite conjurations of many cultures and religions.
>
> Countless species of foo creatures exist—for if an animal dwells upon the Material Plane, it is certain that somewhere in the vast wilds of Nirvana its spiritual double frolics and plays. Nonetheless, certain foo creatures are more common than others, and the most often encountered of all are dogs and lions.
>
> A foo creature can be called to the Material Plane for any reason a conjurer can imagine—these monsters are generally much more intelligent than their mundane counterparts, and can not only follow complex orders but can speak and converse as well. Typically, a foo creature is contacted to serve for a time as a guardian—by adopting its statue form using its freeze ability, a foo creature can appear as little more than an ornate decoration astride the facade of a building or standing guard over a fountain in a city plaza. They are not as often called upon to serve as soldiers in armies, for foo creatures detest war. They generally dislike serving as mounts as well, although for particularly pious and kindly folk, they have been known to make exceptions.
>
> "Foo Creature" is an inherited template that can be added to any animal, referred to hereafter as the base creature. A foo creature retains all the base creature's statistics and abilities except as noted here.
>
> **Challenge Rating:** Same as the base creature +1.
>
> **Alignment:** Any good.
>
> **Type:** The base creature's type changes to outsider with the good subtype. It gains the augmented subtype. Do not recalculate BAB, saves, or skill ranks.
>
> **Senses:** As the base creature, plus darkvision 60 feet.
>
> **AC:** A foo creature's natural armor bonus increases by +2.
>
> **Hit Dice:** The base creature's racial Hit Dice change to d10s.
>
> **Defensive Abilities:** A foo creature retains all of the base creature's defensive abilities and special qualities. It also gains the following.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.Xh0VWNsmO5Gm7U5E inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.sY8RqBBoh6bH3QRy inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.WwcG2s4Tf2yiFgLs inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.YrOCTRVwjxSWVhmr inline=true]
>
> **Special Abilities:** A foo creature retains all of the base creature's special attacks and special abilities. It also gains the following special quality.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.7bilKrHuDzEp67rH inline=true]
>
> **Abilities:** +2 Strength, +2 Constitution, +4 Intelligence.
>
> **Feats:** All foo creatures gain @UUID[Compendium.pf1.feats.Item.iAbIGhm7T2OK9Brt] as a bonus feat.
>
> **Languages:** All foo creatures speak Common and Celestial.

**Mechanical encoding:** `changes`: 5
  - `1` → `bonusFeats`  (untyped)
  - `2` → `str`  (untyped)
  - `4` → `int`  (untyped)
  - `2` → `con`  (untyped)
  - `2` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fungal Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 116-117
**Foundry id:** `JwUAifKIprk1G8mO`

> A fungal creature is an animate plant with the appearance of a living creature. It grows from spores implanted in the dead body of a host creature, and takes on the host creature's basic form and many of that creature's abilities. It retains none of the memories of the creature it grew from, yet it instinctively knows how to use the abilities it inherited from its host. How exactly this is possible is a question that continues to befuddle scholars. The leading theory is that the spores' precise modeling of their host succeeds in capturing some of the creature's physiology—essentially copying its mind—but that for some reason the departure of the creature's spirit or soul upon death prevents the spores from copying the memories as well.
>
> Fungal creatures are often content to sit in quiet contemplation, absorbing the nutrients they require from the life-giving earth. But when faced with living creatures, the overwhelming biological need to reproduce takes over, and the fungal creatures try to seed their spores into new hosts to spawn the next generation of fungal creatures.
>
> Fungal creatures have the general appearance of the base creatures from which they spawned, but their skin is pale fungus rather than flesh and blood. Mushroom caps and shelf fungi sprout from a fungal creature's body, along with fungal gills to deliver the fungal creature's spores. As with many types of fungi, a fungal creature's flesh is poisonous, and any creature that ingests any part of a fungal creature's body risks infection by its spores (as described in the create spawn ability and fungal spores poison on the facing page).
>
> The fungal nymph presented here is built using the nymph from the Pathfinder RPG Bestiary. See page 217 of the Bestiary for rules on this creature's blinding beauty, inspiration, spells, stunning glance, unearthly grace, and wild empathy abilities.
>
> “Fungal creature” is an inherited template that can be added to any corporeal, living creature susceptible to Constitution damage (referred to hereafter as the base creature). A fungal creature uses all the base creature's statistics and special abilities except as noted here.
>
> **CR**: Same as the base creature +1.
>
> **Type**: The creature's type changes to plant (augmented). Do not recalculate base class Hit Dice, BAB, saves, or skill points.
>
> **Senses**: A fungal creature gains darkvision 60 feet.
>
> **Armor Class**: The fungal growths that appear on a fungal creature's body increase the base creature's natural armor bonus by 2.
>
> **Hit Dice**: Change all racial Hit Dice to d8s. Class Hit Dice are unaffected.
>
> **Defensive Abilities**: A fungal creature gains immunity to disease in addition to all of the standard plant traits.
>
> **Speed**: Each of a fungal creature's speeds decreases by 10 feet from those of the base creature (minimum 5 feet).
>
> **Attacks**: A fungal creature retains all the natural weapons, manufactured weapon attacks, and weapon proficiencies of the base creature. If the base creature has no other natural attacks, the fungal creature gains a slam attack that deals damage based on the fungal creature's size.
>
> **Special Attacks**: A fungal creature gains the following.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.N4KxLX1cqoQvSflU inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.bf3EBXbwhT85Qq16 inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.Qro9B56QDRTww4or inline=true]
>
> **Special Qualities**: A fungal creature gains the following.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.ACL0mkNk1NsiIYah inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.bArhYgudJyN9HB0S inline=true]
>
> **Abilities**: Str +4, Dex –2 (minimum 1), Con +4.
>
> **Languages**: If a fungal creature is able to speak, it gains the ability to speak Sylvan in addition to any other languages the base creature knows.

**Mechanical encoding:** `changes`: 9 (showing first 5)
  - `2` → `nac`  (untyped)
  - `max(1, @abilities.dex.total - 2)` → `dex`  (untyped)
  - `if(@attributes.speed.swim.total, max(5, @attributes.speed.swim.total - 10))` → `swimSpeed`  (untyped)
  - `if(@attributes.speed.burrow.total, max(5, @attributes.speed.burrow.total - 10))` → `burrowSpeed`  (untyped)
  - `if(@attributes.speed.land.total, max(5, @attributes.speed.land.total - 10))` → `landSpeed`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fungoid Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** Bestiary 5 (PZO1137) p. 131
**Foundry id:** `JijLUMbU0f062mnv`

> Creatures with the fungoid template appear as they did in life, save that their flesh is pallid and moist, and mushrooms and mold cake their bodies. This template can be applied to any living, non-plant creature. A fungoid creature's quick and rebuild rules are the same.
>
> **Rebuild Rules:** The creature's type changes to plant, and it gains all of the traits of the plant type. The creature gains telepathy 100 ft. with other fungoid creatures. Its alignment changes to chaotic evil.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Ghost
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 144
**Foundry id:** `718KMxAaTejfY2co`

> "Ghost" is an acquired template that can be added to any living creature that has a Charisma score of at least 6. A ghost retains all the base creature's statistics and special abilities except as noted here.
>
> **Challenge Rating:** Same as the base creature +2.
>
> **Type:** The creature's type changes to undead. Do not recalculate the creature's base attack bonus, saves, or skill points. It gains the incorporeal subtype.
>
> **Armor Class:** A ghost gains a deflection bonus equal to its Charisma modifier. It loses the base creature's natural armor bonus, as well as all armor and shield bonuses not from force effects or ghost touch items.
>
> **Hit Dice:** Change all of the creature's racial Hit Dice to d8s. All Hit Dice derived from class levels remain unchanged. Ghosts use their Charisma modifiers to determine bonus hit points (instead of Constitution).
>
> **Defensive Abilities:** A ghost retains all of the defensive abilities of the base creature save those that rely on a corporeal form to function. Ghosts gain channel resistance +4, darkvision 60 ft., the incorporeal ability, and all of the immunities granted by its undead traits. Ghosts also gain the @UUID[Compendium.pf1.template-abilities.Item.07oHIjzqmAhroY6y] ability.
>
> **Speed:** Ghosts lose their previous speeds and gain a fly speed of 30 feet (perfect), unless the base creature has a higher fly speed.
>
> **Melee and Ranged Attacks:** A ghost loses all of the base creature's attacks. If it could wield weapons in life, it can wield ghost touch weapons as a ghost.
>
> **Special Attacks:** A ghost retains all the special attacks of the base creature, but any relying on physical contact do not function. In addition, a ghost gains one ghost special attack from the list below for every 3 points of CR (minimum 1—the first ability chosen must always be *corrupting touch*). The save DC against a ghost's special attack is equal to 10 + 1/2 ghost's HD + ghost's Charisma modifier unless otherwise noted. Additional ghost abilities beyond these can be designed at the GM's discretion.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.pOEFIy4STD3Rcokx inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.FsbKN8sAOmcUvF1f inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.6Ixo1uICjdRLDFaY inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.qL3lKcBF2jJjcf55 inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.ra4nVjZDEAZgu5JW inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.pNbKBq0ewMnYlXhu inline=true]
>
> **Abilities:** Cha +4; as an incorporeal undead creature, a ghost has no Strength or Constitution score.
>
> **Skills:** Ghosts have a +8 racial bonus on Perception and Stealth skill checks. A ghost always treats Climb, Disguise, Fly, Intimidate, Knowledge (arcana), Knowledge (religion), Perception, Sense Motive, Spellcraft, and Stealth as class skills. Otherwise, skills are the same as the base creature.

**Mechanical encoding:** `changes`: 7 (showing first 5)
  - `@abilities.cha.mod` → `ac`  (deflection)
  - `30` → `flySpeed`  (base)
  - `8` → `skill.ste`  (racial)
  - `0` → `landSpeed`  (untypedPerm)
  - `4` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Ghoulish Creature (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `HvWmQrf74ihtyms1`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> Ghoulish creatures have succumbed to ghoul fever and transformed into cannibalistic undead versions of their previous selves.
>
> **Quick Rules:** Counts as undead; darkvision 60 ft.; undead immunities; +1 to AC; +1 on rolls based on Str and Cha; two claw attacks that deal each 1d4 points of damage (for Medium creatures) plus paralysis and one bite attack that deals 1d6 points of damage (for Medium creatures) plus paralysis and disease; disease (Ghoul Fever: Bite—injury; save Fort DC = 10 + 1/2 HD + Cha modifier; onset 1 day; frequency 1/day; effect 1d3 points of Con damage and 1d3 points of Dex damage; cure 2 consecutive saves); paralysis (1d4+1 rounds, DC = 10 + 1/2 HD + Cha modifier, elves are immune).
>
> **Rebuild Rules:** Type change to undead; Senses darkvision 60 ft.; AC natural armor bonus increases by 1; Melee two claw attacks that each deal 1d4 points of damage (for Medium creatures) plus paralysis and one bite attack that deals 1d6 points of damage (for Medium creatures) plus paralysis and disease; Special Attacks disease (Ghoul Fever: Bite—injury; save Fort DC = 10 + 1/2 HD + Cha modifier; onset 1 day; frequency 1/day; effect 1d3 points of Con damage and 1d3 points of Dex damage; cure 2 consecutive saves), paralysis (1d4+1 rounds, DC = 10 + 1/2 HD + Cha modifier, elves are immune); Ability Scores +2 Str, +2 Cha.

**Mechanical encoding:** `changes`: 7 (showing first 5)
  - `1` → `strChecks`  (untyped)
  - `1` → `strSkills`  (untyped)
  - `1` → `chaSkills`  (untyped)
  - `1` → `mattack`  (untyped)
  - `1` → `ac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Ghoulish Creature (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `LWdSzfPmNavAsJBe`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> Ghoulish creatures have succumbed to ghoul fever and transformed into cannibalistic undead versions of their previous selves.
>
> **Quick Rules:** Counts as undead; darkvision 60 ft.; undead immunities; +1 to AC; +1 on rolls based on Str and Cha; two claw attacks that deal each 1d4 points of damage (for Medium creatures) plus paralysis and one bite attack that deals 1d6 points of damage (for Medium creatures) plus paralysis and disease; disease (Ghoul Fever: Bite—injury; save Fort DC = 10 + 1/2 HD + Cha modifier; onset 1 day; frequency 1/day; effect 1d3 points of Con damage and 1d3 points of Dex damage; cure 2 consecutive saves); paralysis (1d4+1 rounds, DC = 10 + 1/2 HD + Cha modifier, elves are immune).
>
> **Rebuild Rules:** Type change to undead; Senses darkvision 60 ft.; AC natural armor bonus increases by 1; Melee two claw attacks that each deal 1d4 points of damage (for Medium creatures) plus paralysis and one bite attack that deals 1d6 points of damage (for Medium creatures) plus paralysis and disease; Special Attacks disease (Ghoul Fever: Bite—injury; save Fort DC = 10 + 1/2 HD + Cha modifier; onset 1 day; frequency 1/day; effect 1d3 points of Con damage and 1d3 points of Dex damage; cure 2 consecutive saves), paralysis (1d4+1 rounds, DC = 10 + 1/2 HD + Cha modifier, elves are immune); Ability Scores +2 Str, +2 Cha.

**Mechanical encoding:** `changes`: 3
  - `2` → `cha`  (untyped)
  - `2` → `str`  (untyped)
  - `1` → `ac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Giant (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 295
**Foundry id:** `bBZEesM8WLIGPhKw`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> Creatures with the giant template are larger and stronger than their normal-sized kin. This template cannot be applied to creatures that are Colossal.
>
> **Quick Rules:** +2 to all rolls based on Str or Con, +2 hp/ HD, –1 penalty on all rolls based on Dex.
>
> **Rebuild Rules**: Size increase by one category; AC increase natural armor by +3; Attacks increase dice rolled by 1 step; Ability Scores +4 size bonus to Str and Con, –2 Dex.

**Mechanical encoding:** `changes`: 13 (showing first 5)
  - `-1` → `dexChecks`  (untyped)
  - `2` → `strChecks`  (untyped)
  - `2` → `strSkills`  (untyped)
  - `2` → `mattack`  (untyped)
  - `-1` → `rattack`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Giant (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 295
**Foundry id:** `Q2RyiEsoCOuqwKO4`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> Creatures with the giant template are larger and stronger than their normal-sized kin. This template cannot be applied to creatures that are Colossal.
>
> **Quick Rules:** +2 to all rolls based on Str or Con, +2 hp/ HD, –1 penalty on all rolls based on Dex.
>
> **Rebuild Rules**: Size increase by one category; AC increase natural armor by +3; Attacks increase dice rolled by 1 step; Ability Scores +4 size bonus to Str and Con, –2 Dex.

**Mechanical encoding:** `changes`: 5
  - `1` → `size`  (untyped)
  - `4` → `str`  (size)
  - `4` → `con`  (size)
  - `-2` → `dex`  (untyped)
  - `3` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Giantkin Ogre
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `yDRhZid8sMuCiN0q`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** No
>
> Ogres sometimes interbreed with other giants. The result of such crossbreeding is a giantkin ogre, which gains some abilities from its non-ogre parents. In areas where ogre clans live near large populations of giants, interbreeding can be so common that entire ogre clans consist solely of giantkin.
>
> Blessed with the blood of greater giants, giantkin ogres are larger and stronger than their normal ogre relatives and gain abilities from their giant progenitors.
>
> **Rebuild Rules:** Hit points +10 hit points; Saving Throws +1 racial bonus to all saving throws; Ability Scores +4 Strength, +4 Constitution; Special Attacks rock throwing (1d6, 90 ft.), Special see table.
>
>
>
>
>  **Crossbreed** 
>  **Special Abilities** 
>
>
>  Fireblood 
>  Resist fire 10 
>
>
>  Frostblood 
>  Resist cold 10 
>
>
>  Hillblood 
>  Increase natural armor by 2 
>
>
>  Stoneblood 
>  Rock catching, rock throwing (1d8, 120 ft.)

**Mechanical encoding:** `changes`: 4
  - `1` → `allSavingThrows`  (untyped)
  - `10` → `mhp`  (untyped)
  - `4` → `str`  (untyped)
  - `4` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Gnarled Creature (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `kZD3bdHeImDGDvIo`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** Yes
>
> Creatures who have been "blessed" with the demon lord Kostchtchie’s attention may acquire this template, which leaves them hunched and knotted with corded muscles and awkwardly formed limbs. Though slower and clumsier than their fellows, gnarled creatures are much stronger and hardier and have thick, horny skin. "Gnarled" is an acquired template that can be applied to any creature of the animal, dragon, fey, humanoid, magical beast, monstrous humanoid, outsider, undead, or vermin type.
>
> **Quick Rules:** +1 on all rolls based on Str or Con, +1 hp/HD, –1 penalty on all rolls based on Dex, –2 penalty on all rolls based on Cha, gains Diehard as a bonus feat.
>
> **Rebuild Rules:** AC increase natural armor by +3; Speed reduce base speed by 10 ft. (cannot be lower than 10 ft.); Defensive Abilities gains the ferocity ability; Ability Scores +2 Str, +2 Con, –2 Dex, –4 Cha.

**Mechanical encoding:** `changes`: 13 (showing first 5)
  - `-2` → `chaChecks`  (untyped)
  - `-1` → `dexSkills`  (untyped)
  - `-2` → `chaSkills`  (untyped)
  - `1` → `conChecks`  (untyped)
  - `1` → `strChecks`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Gnarled Creature (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `hmysSEOYPAXWV19Z`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** Yes
>
> Creatures who have been "blessed" with the demon lord Kostchtchie’s attention may acquire this template, which leaves them hunched and knotted with corded muscles and awkwardly formed limbs. Though slower and clumsier than their fellows, gnarled creatures are much stronger and hardier and have thick, horny skin. "Gnarled" is an acquired template that can be applied to any creature of the animal, dragon, fey, humanoid, magical beast, monstrous humanoid, outsider, undead, or vermin type.
>
> **Quick Rules:** +1 on all rolls based on Str or Con, +1 hp/HD, –1 penalty on all rolls based on Dex, –2 penalty on all rolls based on Cha, gains Diehard as a bonus feat.
>
> **Rebuild Rules:** AC increase natural armor by +3; Speed reduce base speed by 10 ft. (cannot be lower than 10 ft.); Defensive Abilities gains the ferocity ability; Ability Scores +2 Str, +2 Con, –2 Dex, –4 Cha.

**Mechanical encoding:** `changes`: 5
  - `3` → `nac`  (untyped)
  - `-4` → `cha`  (untyped)
  - `2` → `con`  (untyped)
  - `2` → `str`  (untyped)
  - `-2` → `dex`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Granule Construct Host
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `7PhXmtFADZBHiiRG`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Granule construct swarms are the product of powerful artificers pushing the boundaries of their craft. Alone, each individual is a barely sentient construct so tiny as to be practically invisible, a speck of dust that moves under its own power. Brought together by the thousands into a swarm, however, the complex linking of simple systems creates an emergent consciousness of humanlike intelligence, although alien enough to make communication nearly impossible. Granule construct swarms exist solely to infest larger living organisms and reproduce in the relative safety and comfort provided by their bodies. Capable of repairing and replicating out of the raw elements around them, granule constructs within a host are almost unstoppable through physical means, burrowing their way into flesh and sending signals through the bloodstream. Once safely ensconced, granule construct swarms modify their hosts to maximize survival potential, a trait that leads certain people to intentionally cultivate granule construct swarms inside themselves, despite the resulting deformities. Energy damage to a host damages the granule construct swarm equally, but normal weapon damage does not. Granule constructs can vacate dead or dying creatures whenever they so choose, emerging as a standard swarm.
>
> **Environment:** Although created in arcane laboratories, granule construct swawrms can travel anywhere safe to their host creatures.
>
> **Typical Physical Characteristics:** Up close, each microscopic granule construct appears as a silver sphere with an all-purpose orifice at one end that it uses to gather information, take in nutrients, and focus the electromagnetic charges that propel it through the air. At the opposite end emerges a single manipulator claw. In a swarm, they appear as a dense cloud, somewhere between dust and a shadow, that constantly shifts shape and emits a faint hum. Once inside a host's body, a granule construct swarm makes a number of modifications which it finds beneficial, toughening it and making it more aware to ensure maximum survival.
>
> "Granule construct host" is an acquired template that can be added to any corporeal aberration, animal, dragon, fey, giant, humanoid, magical beast, monstrous humanoid, or vermin (referred to hereafter as the base creature). Granule construct hosts use all of the base creature's statistics except as noted below.
>
> **Armor Class:** Creatures with this template gain +2 to their natural armor bonus as their skin thickens and toughens.
>
> **Attack:** A granule construct host retains all the attacks of the base creature and also gains a claw attack if it didn't already have one. if the base creature can use weapons, the granule construct host retains this ability. A creature with natural weapons retains those natural weapons. A granule construct host fighting without weapons uses either its claw attack or its primary natural weapon (if it has any). A granule construct host armed with a weapon uses its claw or a weapon, as it desires.
>
> **Damage:** Granule construct hosts have 2 claw attacks. If the base creatue does not have this attack form, use the appropriate damage value from the table below according to the granule construct host's size. Creatures that have other kinds of natural weapons retain their old damage values or use the appropriate value from the table below, whichever is better.
>
>
>
>
>  **Size** 
>  **Damage** 
>
>
>  Fine 
>  1 
>
>
>  Diminutive 
>  1d2 
>
>
>  Tiny 
>  1d3 
>
>
>  Small 
>  1d4 
>
>
>  Medium 
>  1d6 
>
>
>  Large 
>  1d8 
>
>
>  Huge 
>  2d6 
>
>
>  Gargantuan 
>  2d8 
>
>
>  Colossal 
>  4d6 
>
>
>
>
> **Special Attack:** A granule construct host retains all the special attacks of the base creature and gains infest.
>
> *Infest (Ex):* Once per week, a granule construct host may make a touch attack to allow the swarm inhabiting it to split and infest another creature. If it succeeds, both creatures become infested, otherwise the granule constructs remain in the pre-existing host.
>
> **Special Qualities:** A granule construct host retains all the special qualities of the base creature and gains those described below.
>
> *Uncanny Dodge (Ex):* Granule construct swarms retain an awareness of their surroundings even while inhabiting a body, and as a result granule construct hosts retain their Dexterity bonus to AC even if caught flat-footed or attacked by an invisible opponent, although they still lose their Dexterity bonus if immobilized.
>
> *Blindsight: *To a range of 100 feet.
>
> *Hive Mind (Ex):* While a creature hosting a granule construct swarm normally maintains free will, the swarm living inside maintains contact with any other granule construct swarms or hosts within 100 feet and shares this link in brief, painful flashes. As long as one of the connected creatures is not flanked, none of them are, and if one is aware of a foe, all are.
>
> In addition, if at any point a granule construct swarm infesting a host body feels threatened, it may attempt to take over control of the host's body. At that point, the host must make a DC 15 Will save or obey the swarm's commands for 1d10 rounds, which normally translates to attacking or fleeing from the source of the overwhelming threat.
>
> **Abilities:** Modify from the base creature as follows: +2 Con, -6 Cha (minimum of 1). A granule construct host's body twists into a monsterous mockery of its former shape, all bulging veins and dark shadows moving beneath their skin.
>
> **Challenge Rating:** As base creature.

**Mechanical encoding:** `changes`: 3
  - `-6` → `cha`  (untyped)
  - `2` → `con`  (untyped)
  - `2` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Graveknight
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1120 (PZO1120) p. 138-189
**Foundry id:** `IAocAOv9UKqcxa7u`

> Undying tyrants and eternal champions of the undead, graveknights arise from the corpses of the most nefarious warlords and disgraced heroes—villains too merciless to submit to the shackles of death. They bear the same weapons and regalia they did in life, though warped or empowered by their profane resurrection. The legions they once held also flock to them in death, ready to serve their wicked ambitions once more. A graveknight's essence is fundamentally tied to its armor, the bloodstained trappings of its battle lust. This armor becomes an icon of its perverse natures, transforming into a monstrous second skin over the husk of desiccated flesh and scarred bone locked within.
>
> "Graveknight" is an acquired template that can be added to any living creature with 5 or more Hit Dice (referred to hereafter as the base creature). Most graveknights were once humanoids. A graveknight uses the base creature's statistics and abilities except as noted here.
>
> **CR:** Same as base creature +2.
>
> **Alignment:** Any evil.
>
> **Type:** The graveknight's type changes to undead (augmented). Do not recalculate class Hit Dice, BAB, or saves.
>
> **Senses:** A graveknight gains darkvision 60 ft.
>
> **Aura:** A graveknight emanates the following aura.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.1wwC4ILbhAfTmGgR inline=true]
>
> **Armor Class:** Natural armor improves by +4.
>
> **Hit Dice:** Change all racial Hit Dice to d8s. Class Hit Dice are unaffected. As an undead, a graveknight uses its Charisma modifier to determine bonus hit points.
>
> **Defensive Abilities:** A graveknight gains channel resistance +4; DR 10/magic; and immunity to cold, electricity, and any additional energy type noted by its ruinous revivification special quality. A graveknight also gains spell resistance equal to its augmented CR + 11.**The graveknight also gains the following ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.YBursVLw25ljmNkQ inline=true]
>
> Attacks:** A graveknight gains a slam attack if the base creature didn't have one. Damage for the slam depends on the graveknight's size (see Bestiary 302).
>
> **Special Attacks:** A graveknight gains the following special attacks. Save DCs are equal to 10 + 1/2 the graveknight's HD + the graveknight's Charisma modifier unless otherwise noted.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.FJLHvyEm3jwRsk1s inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.WzYNTBfCynXtyCrT inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.bCocwpXqTDm9Rx8e inline=true]
>
> **Special Qualities:** A graveknight gains the following.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.q2bSNNOBakB7P4vC inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.TFjyMpWJvw6NgmzQ inline=true]
>
> **Ability Scores:** Str +6, Int +2, Wis +4, Cha +4. As an undead creature, a graveknight has no Constitution score.
>
> **Skills:** Graveknights gain a +8 racial bonus on Intimidate, Perception, and Ride checks.
>
> **Feats:** Graveknights gain Improved Initiative, Mounted Combat, Ride-By Attack, and Toughness as bonus feats.

**Mechanical encoding:** `changes`: 10 (showing first 5)
  - `8` → `skill.rid`  (racial)
  - `@details.cr.total + 11` → `spellResist`  (untyped)
  - `6` → `str`  (untyped)
  - `8` → `skill.int`  (racial)
  - `4` → `wis`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Guardian Spirit
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `xVZlhotkGUaKriMi`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> A guardian spirit is bound to the fate of a mortal being (called its "ward"). This bond may be formed by any number of beings or events carrying the weight of destiny, such as deities, the Eldest, norns, and mythic creatures and magic. A spirit can bind itself willingly if it believes that doing so is likely to further its agenda, give it more power, or allow it access to the world of mortals. Mortals can generally invoke a guardian spirit only with summoning and calling spells.
>
> "Guardian spirit" is an acquired template that can be added to any fey or outsider that qualifies to become a familiar through the Improved Familiar feat (this template does not make it a familiar, however). A guardian spirit uses all the base creature’s statistics and special abilities except as noted here. A guardian spirit has a rune on its forehead similar to that on an eidolon (though its ward does not gain a matching rune).
>
>
>
>
>  **Conjuration Spell Level** 
>  **CR** 
>  **Armor Class** 
>  **Hit Dice** 
>  **Ability Scores** 
>  **Special** 
>
>
>  3 
>  +0 
>  +0 
>  +0 
>  +2 
>  Smite threat 1/day, spell-like abilities 
>
>
>  4 
>  +2 
>  +2 
>  +2 
>  +2 
>  Fated guardian, spell-like ability 
>
>
>  5 
>  +4 
>  +4 
>  +4 
>  +4 
>  Spell-like ability 
>
>
>  6 
>  +6 
>  +6 
>  +6 
>  +4 
>  Smite threat 2/day, spell-like ability 
>
>
>  7 
>  +8 
>  +8 
>  +8 
>  +6 
>  Spell-like ability 
>
>
>  8 
>  +10 
>  +10 
>  +10 
>  +6 
>  Co-walker, spell-like ability 
>
>
>  9 
>  +12 
>  +12 
>  +12 
>  +8 
>  Smite threat 3/day, spell-like ability 
>
>
>
>
> **CR:** The guardian spirit’s CR increases based on the level of spell used to summon it, as noted on the Conjured Guardian table on page 27.
>
> **Armor Class:** The guardian spirit’s natural armor bonus increases based on the level of spell used to summon it, as noted on the Conjured Guardian table.
>
> **Hit Dice:** The guardian spirit’s Hit Dice increase based on the level of spell used to summon it, as noted on the Conjured Guardian table. It gains appropriate skill points, feats, ability score increases, base attack bonus, and base saving throw advancements for its increased Hit Dice.
>
> **Defensive Abilities:** The guardian spirit has an amount of spell resistance equal to 11 + its CR unless the base creature’s SR was higher.
>
> **Ability Scores:** The guardian spirit’s Charisma score becomes 18 unless the base creature’s Charisma score was higher. Each of the guardian spirit’s ability scores increases when it’s summoned by higher-level spells, as noted on the Conjured Guardian table above.
>
> **Special Attacks:** If the guardian spirit has extraordinary or supernatural abilities that deal hit point damage measured in dice, the number of dice increases by an amount equal to the level of spell used to conjure it – 3. If the ability requires at least a standard action to activate and has an instantaneous duration, the damage increases by an additional die.
>
> **Special:** The guardian spirit gains a smite and additional special abilities as noted on the table.
>
> *Smite Threat (Su):* Once per day as a swift action, the guardian spirit can add its Charisma bonus on attack rolls and its HD on damage rolls against a foe that currently threatens its ward or has attacked the ward within the past 24 hours; this smite persists until the target is dead or the summoning of the guardian spirit ends. If the spirit is summoned by a 6th-level spell, it can use smite threat an additional time per day, and if the spirit is summoned by a 9th-level spell, it can use smite threat a third time per day.
>
> **Spell-Like Abilities:** A guardian spirit’s caster level for its spell-like abilities is equal to its Challenge Rating + 1, or to the base creature’s caster level, whichever is higher. It can cast guidance at will. For every spell level of the conjuration spell used to call or summon it (such as planar ally, planar binding, or summon monster if the summoner has the Summon Guardian Spirit feat), the guardian spirit gains access to one additional spell-like ability of the ward’s choice from the following list:
>
> *Spell Level 3: *Chill touch, ill omenAPG, protection from chaos/evil/good/law (choose one; its alignment descriptor must oppose the guardian spirit’s alignment).
> *Spell Level 4:* Call lightning, detect thoughts, invisibility.
> *Spell Level 5:* Cure serious wounds, dispel magic, shout.
> *Spell Level 6:* Call lightning storm, death ward, freedom of movement.
> *Spell Level 7:* Break enchantment, breath of life, contagious flameAPG.
> *Spell Level 8: *Cloak of dreamsAPG, greater heroism, sunbeam.
> *Spell Level 9:* Greater shout, power word blind, regenerate.
>
> Each chosen spell-like ability is available once per day.
>
> *Fated Guardian (Su): *When conjured by a 4th-level or higher spell, a guardian spirit can protect the destiny of another creature within 30 feet as a standard action once per day. For 1 round, any time the creature makes an attack or attempts a saving throw, it rolls twice and takes the better result.
>
> *Co-Walker (Sp):* When conjured by an 8th-level or higher spell, a guardian spirit can assume the shape of its ward as if with alter self, except it can appear to be only the ward (even if the ward is not of a creature type or size that can normally be assumed with alter self) and it gains a +10 bonus on Disguise checks to appear to be the ward.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Half-Celestial
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 169
**Foundry id:** `j7IZqYzTZKa8xmSb`

> "Half-celestial" is an inherited or acquired template that can be added to any living, corporeal creature with an Intelligence score of 4 or more. A half-celestial creature retains the base creature's statistics and special abilities except as noted here.
>
> **CR:** HD 5 or less, as base creature + 1; HD 6–10, as base creature + 2; HD 11 or more, as base creature + 3.
>
> **Alignment:** Any good.
>
> **Type:** The creature's type changes to outsider (native). Do not recalculate HD, BAB, or saves.
>
> **Armor Class:** Natural armor improves by +1.
>
> **Defenses/Qualities:** It gains darkvision 60 feet; immunity to disease; +4 racial bonus on saves vs. poison; acid, cold, and electricity resist 10; DR 5/magic (if HD 11 or less) or 10/magic (if HD 12 or more); and SR equal to CR + 11 (maximum 35).
>
> **Speed:** Unless the base creature flies better, the half-celestial flies at twice the base creature's land speed (good maneuverability).
>
> **Special Abilities:** A half-celestial gains the following.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.y1wyWYIpRmchAFO6 inline=true]
>
> **Spell-Like Abilities:** A half-celestial with an Int or Wis score of 8 or higher has a cumulative number of spell-like abilities depending on its Hit Dice. Unless otherwise noted, an ability is usable once per day. Caster level equals the creature's HD (or the caster evel of the base creature's spell-like abilities, whichever is higher).
>
>
> **HD**
>
>
> **Abilities**
>
>
> 1–2
>
>
> @UUID[Compendium.pf1.spells.Item.skgjjub1hng29nwo]* *3/day, @UUID[Compendium.pf1.spells.Item.wa0zb2pncesmm9lz]
>
>
> 3–4
>
>
> @UUID[Compendium.pf1.spells.Item.ibk7jrc5rwubpia6], @UUID[Compendium.pf1.spells.Item.tr7m97npkbgm4wp7]
>
>
> 5–6
>
>
> @UUID[Compendium.pf1.spells.Item.norn02g8zdsspf2j], @UUID[Compendium.pf1.spells.Item.6l904edkt8jv9jor]
>
>
> 7–8
>
>
> @UUID[Compendium.pf1.spells.Item.erndkoe44rgj0lob], @UUID[Compendium.pf1.spells.Item.ocbjt6z7amc3yn8w]
>
>
> 9–10
>
>
> @UUID[Compendium.pf1.spells.Item.sg3eq6xpsum65fgm]
>
>
> 11–12
>
>
> @UUID[Compendium.pf1.spells.Item.odcyzsuexods8ek9]
>
>
> 13–14
>
>
> @UUID[Compendium.pf1.spells.Item.n0vm6or4nwaylpfa]* *3/day, @UUID[Compendium.pf1.spells.Item.vxmp5prgw5fj4h6f]
>
>
> 15–16
>
>
> @UUID[Compendium.pf1.spells.Item.q2r6jrgsbwjgssdg]
>
>
> 17–18
>
>
> @UUID[Compendium.pf1.spells.Item.mi52crelhwuy6bmp]* *(celestials only)
>
>
> 19–20
>
>
> @UUID[Compendium.pf1.spells.Item.thh46ghi51lrl3cl]
>
>
> **Abilities:** A half-celestial gains a +4 bonus on three ability scores of its choice and a +2 bonus on the other three.
>
> **Skills:** A half-celestial with racial Hit Dice has skill points per racial Hit Die equal to 6 + its Intelligence modifier. Racial class skills are unchanged from the base creature's. Skill ranks from class levels are unaffected.

**Mechanical encoding:** `changes`: 9 (showing first 5)
  - `4` → `str`  (untyped)
  - `4` → `dex`  (untyped)
  - `max(@attributes.speed.fly.total, 2 * @attributes.speed.land.total)` → `flySpeed`  (base)
  - `4` → `con`  (untyped)
  - `min(35, @details.cr.total + 11)` → `spellResist`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Half-Dragon
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 170
**Foundry id:** `gaTNMYfwYbFcqtEA`

> "Half-dragon" is an inherited or acquired template that can be added to any living, corporeal creature (referred to hereafter as the base creature). A half-dragon retains all the base creature's statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature + 2 (minimum 3).
>
> **Type:** Creature type changes to dragon. Do not recalculate HD, BAB, or saves.
>
> **Armor Class:** Nat. armor improves by +4.
>
> **Special Qualities and Defenses:** A half-dragon gains darkvision 60 feet; low-light vision; and immunity to sleep, paralysis, and energy of the same type as its breath weapon.
>
> **Speed:** A half-dragon has wings. Unless the base creature has a better fly speed, the half-dragon can fly at twice the creature's base land speed (average maneuverability).
>
> **Melee:** A half-dragon has two claw attacks and a bite attack. If the base creature can use manufactured weapons, the half-dragon can as well. A new claw or bite attack deals damage as appropriate for the half-dragon's size (see Natural Attacks.)
>
> **Special Abilities:** A half-dragon retains all the special attacks of the base creature and gains a @UUID[Compendium.pf1.monster-abilities.Item.bg2m81Euc7kGdiKN] usable once per day based on the dragon variety (see below). The breath weapon deals 1d6 hit points of damage per racial HD possessed by the half-dragon (Reflex half; DC 10 + 1/2 creature's racial HD + creature's Con modifier).
>
>
> **Dragon Variety**
>
>
> **Breath Weapon**
>
>
> Black or copper
>
>
> 60–foot line of acid
>
>
> Brass
>
>
> 60–foot line of fire
>
>
> Blue or bronze
>
>
> 60–foot line of electricity
>
>
> Gold or red
>
>
> 30–foot cone of fire
>
>
> Green
>
>
> 30–foot cone of acid
>
>
> Silver or white
>
>
> 30–foot cone of cold
>
>
> **Abilities:** Increase from the base creature as follows: Str +8, Con +6, Int +2, Cha +2.
>
> **Skills:** A half-dragon with racial Hit Dice has skill points per racial Hit Die equal to 6 + its Intelligence modifier. Racial class skills are unchanged from the base creature's.

**Mechanical encoding:** `changes`: 6 (showing first 5)
  - `4` → `nac`  (untyped)
  - `2` → `int`  (untyped)
  - `6` → `con`  (untyped)
  - `max(@attributes.speed.fly.total, 2 * @attributes.speed.land.total)` → `flySpeed`  (base)
  - `8` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Half-Fiend
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 171
**Foundry id:** `34W9MgjhRXCWiKmO`

> "Half-fiend" is an inherited or acquired template that can be added to a living, corporeal creature with an Int score of 4 or more. A half-fiend uses all the base creature's statistics and special abilities except as noted here.
>
> **CR:** HD 4 or less, as base creature + 1; HD 5 to 10, as base creature + 2; HD 11 or more, as base creature + 3.
>
> **Alignment:** Any evil.
>
> **Type:** The creature's type changes to outsider (native). Do not recalculate HD, BAB, or saves.
>
> **Armor Class:** Natural armor improves by +1.
>
> **Defenses/Qualities:** Gains darkvision 60 feet; immunity to poison; acid, cold, electricity, and fire resistance 10; DR 5/magic (if HD 11 or less) or 10/magic (if HD 12 or more); and SR equal to creature's CR + 11 (maximum 35).
>
> **Speed:** Unless the base creature flies better, the half-fiend flies at twice the base creature's land speed (good).
>
> **Melee:** A half-fiend gains two claw attacks and a bite attack. Damage depends on its size.
>
> **Special Attacks:** A half-fiend gains the following.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.3XEQ0B8GADTxGKKD inline=true]
>
> **Spell-Like Abilities:** A half-fiend with an Int or Wis score of 8 or higher has a cumulative number of spell-like abilities set by its HD. Unless otherwise noted, an ability is usable 1/day. CL equals the creature's HD (or the CL of the base creature's spell-like abilities, whichever is higher).
>
>
> **HD**
>
>
> **Abilities**
>
>
> 1–2
>
>
> @UUID[Compendium.pf1.spells.Item.tsndfcfijmgxs37p] 3/day
>
>
> 3–4
>
>
> @UUID[Compendium.pf1.spells.Item.ffsr22oaciurke4e]
>
>
> 5–6
>
>
> @UUID[Compendium.pf1.spells.Item.okui7mft5bquqfrg]
>
>
> 7–8
>
>
> @UUID[Compendium.pf1.spells.Item.vdh0yuzpjwhky6kr]3/day
>
>
> 9–10
>
>
> @UUID[Compendium.pf1.spells.Item.ppeb97nxg1rmdpme]
>
>
> 11–12
>
>
> @UUID[Compendium.pf1.spells.Item.baocube6vvey9zlc]
>
>
> 13–14
>
>
> @UUID[Compendium.pf1.spells.Item.flrn1xmm2wfrxbkf]* *3/day, @UUID[Compendium.pf1.spells.Item.u01yelxlhrd85181]
>
>
> 15–16
>
>
> @UUID[Compendium.pf1.spells.Item.e8zen5nzixnt7bde]
>
>
> 17–18
>
>
> @UUID[Compendium.pf1.spells.Item.mi52crelhwuy6bmp]* *(fiends only)
>
>
> 19–20
>
>
> @UUID[Compendium.pf1.spells.Item.rlfd7f64wgjfvg6e]
>
>
> **Abilities:** A half-fiend gains a +4 bonus on three ability scores of its choice and a +2 bonus on the other three.
>
> **Skills:** A half-fiend with racial HD has skill points per racial HD equal to 6 + Int mod. Racial class skills are unchanged, and class level skill ranks are unaffected.

**Mechanical encoding:** `changes`: 9 (showing first 5)
  - `max(@attributes.speed.fly.total, 2 * @attributes.speed.land.total)` → `flySpeed`  (base)
  - `4` → `con`  (untyped)
  - `min(35, @details.cr.total + 11)` → `spellResist`  (untyped)
  - `1` → `nac`  (untyped)
  - `4` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Half-Janni
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `u06GtvHIQJHttw28`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** Yes
>
> Jann are the kind of genie closest to humans in interests and temperament, and are drawn to mingle with mortals. Sometimes these associations result in the birth of halfjanni children. Beautiful and exotic, the elemental power that resides in these half-jann mixes with the unique potential of the human parent, sometimes rivaling or even exceeding that of their genie parent.
>
> Half-jann often seek to sequester themselves on the edge of Keleshite civilizations, capable of observing their human kin without getting deeply involved in mortal affairs. Like their genie ancestors, however, the half-jann are fascinated by true humans, and often take them as mates, leading to generations of suli-jann (see below).
>
> No matter their human ancestry, half-jann are lovely to look upon, possessing deeply tanned bronze skin and intense eyes that sometimes seem to be swirling pools of elemental power.
>
> #### Creating a Half-Janni
>
> "Half-janni" is an inherited template that can be added to any human (referred to hereafter as the "base creature").
>
> A half-janni uses all the base creature’s statistics and special abilities except as noted here.
>
> **Size and Type:** The creature’s type changes to outsider (augmented humanoid, human, native). Do not recalculate the base creature’s Hit Dice, base attack bonus, or saves. Size is unchanged.
>
> **Speed:** A half-janni gains the ability to fly, with a speed of 20 feet (good maneuverability).
>
> **Armor Class:** The half-janni’s natural armor improves by +1 (this stacks with any natural armor bonus the base creature has).
>
> **Spell-Like Abilities:** A half-janni with an Intelligence or Wisdom score of 8 or higher has spell-like abilities, depending on its level, as indicated on the table below. The abilities are cumulative.
>
> Caster level equals the creature’s level, and the save DC is Charisma-based.
>
>
>
>
>  **Level** 
>  **Abilities** 
>
>
>  1-2 
>  *Speak with animals* 3/day 
>
>
>  3-6 
>  *Enlarge person* or *reduce person* 2/day in any combination 
>
>
>  7-8 
>  *Invisibility* (self only) 3/day 
>
>
>  9-14 
>  *Create food and water* 1/day 
>
>
>  15-16 
>  *Ethereal jaunt* 1/day 
>
>
>
>
> **Special Qualities:** A half-janni has all the special qualities of the base creature, plus the following special qualities.
>
> - Darkvision out to 60 feet
>
> - Immunity to disease
>
> - Fire resistance 10
>
> **Abilities:** Increase from the base creature as follows: Str +2, Dex +2, Int +2, Wis +4, Cha +4
>
> **Challenge Rating:** Same as base creature +2

**Mechanical encoding:** `changes`: 6 (showing first 5)
  - `4` → `cha`  (untyped)
  - `4` → `wis`  (untyped)
  - `2` → `dex`  (untyped)
  - `2` → `int`  (untyped)
  - `2` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Haunted Construct
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `Au8SQCFtLfSv3u9Y`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> On the border between Xa Hoi and Nagajor, near the caldera of Mount Kumijinja, a cave system leads deep into the Darklands. The locals call it the Clicking Caverns, for scouts report seeing strange clockwork warriors creeping out of the caves at night in search of living creatures. Deep beneath those caves is the clockwork necropolis of Pan Majang, a constantly transforming edifice that houses the sadistic, flesh-eating spirits of a forgotten race. These spirits now possess and haunt the constructs they once used as slaves.
>
> A haunted construct is formed when a soul does not continue to Pharasma’s Spire and is instead drawn to an existing construct in a desperate attempt to continue living. Often malevolent and cruel, these souls seek to inflict harm on the living and invite them to join in their tortured existence.
>
> "Haunted construct" is an acquired template that can be added to any construct (referred to hereafter as the base creature). A haunted construct retains all the base creature’s statistics and special abilities except as noted here.
>
> **Challenge Rating:** Base creature’s CR + 1.
>
> **Alignment:** Any evil, most commonly neutral evil.
>
> **Armor Class:** A haunted construct gains a +1 deflection bonus to AC.
>
> **Defensive Abilities:** Haunted constructs gain channel resistance +4.
>
> **Special Qualities:** A haunted construct gains the following special qualities.
>
> *Infused Soul (Su):* A haunted construct is infused with the soul of a creature who died nearby. The soul provides the haunted construct a semblance of unlife as a ghostly apparition surrounds its body and controls its actions. This allows the haunted construct to apply its Charisma modifier as a bonus on Fortitude saves, and it gains a number of bonus hit points per Hit Die equal to its Charisma bonus. A haunted construct is healed by negative energy and harmed by positive energy as if it were an undead creature. It reacts to magical and supernatural effects, such as *detect undead* and *searing light*, as if it were an undead creature.
>
> *Unholy Beacon (Su): *Haunted constructs act as a focal point for negative energy, exuding a constant 20-foot aura that functions as the spell desecrate. Additionally, undead creatures within the aura gain the benefits of the haunted construct’s damage resistance or hardness, if any.
>
> **Special Attacks:** Each haunted construct gains one of the following haunts tied to its artificial body. This haunt functions until the haunted construct is destroyed but acts on initiative count 10, as usual for haunts, affecting each creature within 30 feet. The Perception DC to notice the haunt is equal to 15 + the haunted construct’s CR. The save DC against a haunted construct’s special attack is equal to 10 + half the haunted construct’s Hit Dice, and the caster level is equal to the haunted construct’s CR. A creature can attempt the listed saving throw at the end of its turn each round to negate the haunt’s ongoing effect; once a creature successfully saves against the effect, it is immune to that effect for 24 hours. Additional haunted construct abilities beyond these can be designed at the GM’s discretion.
>
> *Burned Alive (Su):* The spirit inhabiting this haunted construct perished in a blaze; notice the smell of smoke; effect a screech erupts as affected creatures catch on fire; destruction flood the area with water for at least 24 hours.
>
> *Eaten Alive (Su):* The spirit inhabiting this haunted construct was torn apart by wild animals; notice the sound of gnashing teeth; effect an invisible force bites and tears the flesh of all living targets, dealing 1d6 points of force damage per 4 Hit Dice the haunted construct has (minimum 1d6) each round and inflicting the shaken condition (Will negates); this is a mind-affecting effect; destruction a good-aligned creature must remain in the haunted area for 3 days while fasting.
>
> *Frozen Bones (Su):* The spirit inhabiting this haunted construct froze to death; notice frost begins to appear on the ground and any clothing or objects; effect a sudden chill fills the air, and creatures take 1d6 points of cold damage per 2 Hit Dice the haunted construct has (minimum 1d6) and are staggered for 1d4 rounds; on a successful Fortitude save, a creature takes half the damage and negates the staggered condition; destruction burn the area in magical fire with a caster level equal to or greater than that of the haunt.
>
> *Insane Ramblings (Su): *The spirit inhabiting this haunted construct wasted away from madness; notice a discordant chorus of whispers; effect yammering voices fill the heads of all affected creatures, affecting them as per the spell confusion (Will negates); destruction a creature shouts a hidden truth or previously kept secret.
>
> *Isolation (Su):* The spirit inhabiting this haunted construct died trapped and alone; notice ambient sound disappears and other sounds are quieted; effect each target believes it is alone in the world; it cannot perceive, target, nor interact with anyone it considers an ally (Will negates); this is a mind-affecting effect; destruction a boisterous celebration of friendship lasting at least 1 hour at the site of the haunt.
>
> *Loss of Limbs (Su):* The spirit inhabiting this haunted construct bled out after being dismembered; notice targets’ arms all start to tingle; effect each target believes its arms have been ripped off; the creature drops whatever it is holding and cannot use its arms in any way (Will negates); this is a mind-affecting effect; destruction a creature must willfully offer the strength of its own arms to the vengeful spirits, accepting 2 points of Strength and Dexterity drain.
>
> *Mutilation (Su):* The spirit inhabiting this haunted construct was murdered in a gruesome fashion; notice the creature’s muscles begin to spasm; effect the creature’s arms and legs spasm and twist into hideous angles, reducing its base speed to 5 feet and imposing a –4 penalty on attack rolls (Will negates); destruction the source must be targeted by a heal or regeneration spell.
>
> **Ability Scores:** If the base creature’s Charisma score is less than 10, then its Charisma score changes to 14; otherwise a haunted construct receives a +4 bonus to Charisma. A haunted construct receives a +4 bonus to its Intelligence score and generally has the same skills the soul had in life. If the base creature lacked an Intelligence score, it gains an Intelligence score of 4 and generally selects the same feats its soul had in life.

**Mechanical encoding:** `changes`: 3
  - `4` → `int`  (untyped)
  - `1` → `ac`  (deflection)
  - `4` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Haunted One
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `3HySvC8pHcanyB3H`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Haunted ones are mortals who share their bodies with strange intelligences of supernatural origin. While technically undead, these disembodied intellects exist only as thought—they cannot directly interact with the world until they find a host willing to share both body and mind.
>
> In essence, a haunted one is two creatures—a living host (almost always a humanoid with at least a modicum of intelligence) and its rider (the unbodied entity). The term "haunted one" specifically refers to the host as influenced by its rider.
>
> While all riders possess their own intelligence and have unique goals and motivations, they are similar enough to present them as related entities. Riders attempt to influence their hosts by disseminating cryptic ideas and motivations among the host’s own thoughts and memories. A rider’s methods of influencing its host are subtle yet effective, though ultimately it has no ability to override the host creature. It cannot take control of the host’s body, and throughout the "possession" the host retains its free will. Instead, the rider can strong-arm its host, much like when casting geas/quest—a host who fails to act upon the rider’s "requests" suffers increasingly adverse physical and mental ailments. These effects can, at their most potent, cause the host permanent damage or even death. Typically, the rider departs after its host perishes, though it is unclear whether the adverse effects are produced to attempt to further sway the host, or as a result of the rider choosing to depart because the host continually disregards its suggestions.
>
> Still, being a haunted one is not without some benefits. Haunted ones possess the uncanny ability to recall fantastic amounts of knowledge in areas of study previously unknown to them, often including information beyond the scope of the greatest scholars. Typically, this knowledge concerns something ancient and occult, forbidden things that most would find horrifying and maddening, which the host feels compelled to seek out and explore. Similarly, riders inherently sense the presence of others like themselves, and often use the host to track their rivals down. While these urges are not inherently beneficial, hosts who appease them begin to develop stronger connections with their riders. As a result, the rider becomes more efficient at transferring greater amounts of lost knowledge to the host.
>
> The circumstances by which a creature can be exposed to an unbodied entity capable of transforming it into a haunted one are numerous, but if the targeted creature wishes to resist the attempt by the rider to invade its mind, the host-to-be can attempt a DC 15 Will save. If the save is successful, the unbodied entity fails to possess the host, and may not try again for 24 hours.
>
> "Haunted one" is an acquired template that can be added to any corporeal creature of average intellect or better (Intelligence 10 or higher). Typically, the base creature is a humanoid—although other creatures are not unheard of.
>
> **Challenge Rating:** As base creature +1.
>
> **Alignment:** All riders have an alignment—most are chaotic, evil, or both. When a host becomes a haunted one, its alignment changes to match the rider’s. Typically, when a host attempts an act out of keeping with this alignment, the rider punishes the host (see "Weaknesses" below).
>
> **Weaknesses:** A haunted one gains the following weakness.
>
> *Haunted (Ex): *If at any point a haunted one’s rider spirit feels the haunted one needs "persuasion" to follow its demands, the spirit can inflict 1d6 points of Constitution damage upon the haunted one as a free action, up to once per round. The haunted one can resist this Constitution damage by making a DC 20 Fortitude save—with a successful save, the spirit cannot attempt to harm the haunted one in this manner again for 24 hours.
>
> **Special Abilities:** A haunted one gains the following four special abilities.
>
> *True Lore (Su):* Once per day, a haunted one can gain a +20 insight bonus on any Knowledge skill check that it makes, provided that the haunted one possesses at least one skill rank in that Knowledge skill. Every 5 HD possessed by the haunted one grants an additional daily use of this ability.
>
> *Vision (Sp):* Once a day, a haunted one can use vision as a spell-like ability (Caster Level equals the haunted one’s HD). Every 5 HD possessed by the haunted one grants an additional daily use of this ability.
>
> **Skills:** Knowledge skills are always class skills for a haunted one.
>
> **Abilities:** Con +4, Int +2, Wis +2, Cha +2.
>
> **Languages:** A haunted one gains a bonus language possessed by the rider—unless otherwise specified, this bonus language is Aklo. Additionally, haunted ones possess telepathy with other haunted ones, to a range of 100 feet.

**Mechanical encoding:** `changes`: 4
  - `2` → `cha`  (untyped)
  - `2` → `wis`  (untyped)
  - `2` → `int`  (untyped)
  - `4` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Hell Engine
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `YE9x2cUVGiNibXuu`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> A hell engine is a construct fueled by an infernal contract, bypassing the complex magic and craftsmanship needed to animate a golem or similar engine of destruction. Artificers who lack the skill or magical aptitude to craft constructs on their own may be tempted to use the power of Hell to make up for their shortcomings, surrendering their souls for the chance to see their masterpieces brought to horrifying life.
>
> Although a hell engine lacks the creativity and cunning of a true devil, contracting an infernal construct grants certain advantages over a bound outsider. A hell engine’s mindless neutrality renders it resistant to anarchic or holy attacks that would cripple a devil, making it a valuable tool against celestial and chaotic forces. Combined with the construct’s ability to banish hostile outsiders and replace them with additional devils, these war machines earn a distinguished place as shock troops in infernal armies and guardians of Hell’s most secure vaults.
>
> "Hell engine" is an acquired template that can be added to any nonchaotic, nongood construct with no Intelligence score. A hell engine uses all the base creature’s statistics and special abilities except as noted here.
>
> **Challenge Rating:** Base creature’s CR + 1.
>
> **Alignment:** Always neutral. However, a hell engine radiates a moderate aura of law and evil as if it were a lawful evil outsider.
>
> **Senses:** A hell engine gains the see in darkness ability. In addition, the hell engine can see through the hellfire cloud created by its breath weapon without penalty, ignoring any cover or concealment bonuses it provides.
>
> **Defensive Abilities:** A hell engine gains fire resistance 30. If the base creature has immunity to magic, it gains the following change:
>
> - Dispel evil or dispel law drives the hell engine back 30 feet and deals 2d12 points of damage to it (no save).
>
> **Weaknesses:** A hell engine gains the following weakness.
>
> *Contract Powered (Ex):* A hell engine draws power from the infernal contract that animates it. A hell engine cannot attack the devil that drafted its contract, the mortal who signed it, or any creature holding an original copy of the contract. Spells cast by the devil that wrote the contract or its mortal signatory automatically bypass any spell resistance or immunity to magic the hell engine has. If both copies of the contract are destroyed, the hell engine ceases to function until a new one is created.
>
> **Special Attacks:** A hell engine gains the following.
>
> *Breath Weapon (Su)*: As a standard action once every 1d4+1 rounds, a hell engine can exhale a churning cloud of hellfire in an adjacent space equal to its own size. This hellfire persists for 1 round; each creature within the area when the hell engine creates it (as well as any creature that passes through the cloud until the start of the hell engine’s next turn) takes 1d6 points of fire damage and 1d6 points of unholy damage per 2 Hit Dice of the base creature. A creature can attempt a Reflex save (DC 10 + half the base creature’s HD) for half damage. The hellfire cloud also provides concealment as if from a fog cloud spell.
>
> The hell engine can use this breath weapon in addition to any breath weapon the base creature has, and it can use up to two breath weapons simultaneously as a full-round action. Simultaneous breath weapons both fill the area of either the hellfire breath weapon or base creature’s breath weapon (hell engine’s choice). If the base creature’s breath weapon deals fire damage, a simultaneous breath weapon converts half of that damage into unholy damage.
>
> *Banishing Strike (Su):* Three times per day as an immediate action, the hell engine can force an extraplanar or summoned creature it hits to attempt a Will save (DC = 10 + half the base creature’s HD); on a failure, the target is forced back to its original plane as if by a dismissal spell.
>
> *Redirect Summons (Sp): *Within 1 minute of successfully using its banishing strike ability, a hell engine can redirect its planar energy to summon a devil as an immediate action with a 100% chance of success. The summoned devil remains for 1 hour. A hell engine can have only one summoned devil at a time. The hell engine’s Hit Dice determines the most powerful kind of devil it can summon and the effective spell level of this ability, according to the following table.**
>
>
>
> HD**
>
>
> **Devil**
>
>
> **Spell Level**
>
>
> 5
>
>
> Lemure
>
>
> 2nd
>
>
> 10
>
>
> Bearded devil
>
>
> 5th
>
>
> 15
>
>
> Erinyes
>
>
> 6th
>
>
> 20
>
>
> Bone devil
>
>
> 7th
>
>
> 25
>
>
> Barbed devil
>
>
> 8th
>
>
> 30+
>
>
> Ice devil
>
>
> 9th

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Hellbound Creature (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `CjtaI9O7kMVpmvpK`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> Hellbound creatures have consigned their souls to Hell in exchange for infernal power. A hellbound creature’s Hit Dice determine what type of devil it can summon with its summon spell-like ability and the summon ability’s spell level. It can instead choose to summon 1d3 devils of the next weaker category, or 1d4+1 devils of two categories weaker.
>
> **Quick Rules:** Darkvision; see in darkness; +1 to AC; +1 on rolls based on Str and Cha; contract bound*; gore attack that deals 1d4 points of damage (for Medium creatures); summon (see table; 100%).
>
> **Rebuild Rules:** Senses darkvision, see in darkness; AC natural armor bonus increases by 1; Weaknesses contract bound*; Melee gore attack that deals 1d4 points of damage (for Medium creatures); Spell-like Abilities summon (see table; 100%); Ability Scores +2 Str, +2 Cha.
>
> **Hellbound Summon**
>
>
>
>
>  **Hellbound Creature HD** 
>  **Devil** 
>  **Spell Level** 
>
>
>  8 or fewer 
>  Lemure 
>  2nd 
>
>
>  9-10 
>  Bearded devil 
>  5th 
>
>
>  11-12 
>  Erinyes 
>  6th 
>
>
>  13-14 
>  Bone devil 
>  7th 
>
>
>  15-16 
>  Barbed devil 
>  8th 
>
>
>  17 or more 
>  Ice devil 
>  9th

**Mechanical encoding:** `changes`: 7 (showing first 5)
  - `1` → `chaSkills`  (racial)
  - `1` → `mattack`  (untyped)
  - `1` → `strSkills`  (racial)
  - `1` → `wdamage`  (untyped)
  - `1` → `strChecks`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Hellbound Creature (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `D990b7fgSno1y1sA`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> Hellbound creatures have consigned their souls to Hell in exchange for infernal power. A hellbound creature’s Hit Dice determine what type of devil it can summon with its summon spell-like ability and the summon ability’s spell level. It can instead choose to summon 1d3 devils of the next weaker category, or 1d4+1 devils of two categories weaker.
>
> **Quick Rules:** Darkvision; see in darkness; +1 to AC; +1 on rolls based on Str and Cha; contract bound*; gore attack that deals 1d4 points of damage (for Medium creatures); summon (see table; 100%).
>
> **Rebuild Rules:** Senses darkvision, see in darkness; AC natural armor bonus increases by 1; Weaknesses contract bound*; Melee gore attack that deals 1d4 points of damage (for Medium creatures); Spell-like Abilities summon (see table; 100%); Ability Scores +2 Str, +2 Cha.
>
> **Hellbound Summon**
>
>
>
>
>  **Hellbound Creature HD** 
>  **Devil** 
>  **Spell Level** 
>
>
>  8 or fewer 
>  Lemure 
>  2nd 
>
>
>  9-10 
>  Bearded devil 
>  5th 
>
>
>  11-12 
>  Erinyes 
>  6th 
>
>
>  13-14 
>  Bone devil 
>  7th 
>
>
>  15-16 
>  Barbed devil 
>  8th 
>
>
>  17 or more 
>  Ice devil 
>  9th

**Mechanical encoding:** `changes`: 3
  - `2` → `cha`  (untyped)
  - `2` → `str`  (untyped)
  - `1` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Hive Creature (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `fkdhZBKmlJcLH3dU`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> While a creature infested by a hive corruption usually becomes a warrior, mutations can create hive creatures that retain the capabilities of the original creatures.
>
> **Quick Rules:** +3 to AC; +1 on rolls based on Str, Dex, and Con; –3 on rolls based on Cha; +1 hp/ HD; two claw attacks that each deal 1d4 points of damage (for Medium creatures) and one bite attack that deals 1d6 points of damage (for Medium creatures); immunity to acid; blind; blindsense 60 ft.; blindsight 10 ft.; corrosive blood*; hive mind*.
>
> **Rebuild Rules:** Type gain the hive subtype and all the corresponding abilities; AC natural armor bonus increases by 2; Melee two claw attacks that each deal 1d4 points of damage (for Medium creatures) and one bite attack that deals 1d6 points of damage (for Medium creatures); Ability Scores +2 Str, +2 Dex, +2 Con, –6 Cha.

**Mechanical encoding:** `changes`: 13 (showing first 5)
  - `1` → `conChecks`  (untyped)
  - `1` → `dexSkills`  (untyped)
  - `@attributes.hd.total` → `mhp`  (untyped)
  - `1` → `dexChecks`  (untyped)
  - `-3` → `chaSkills`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Hive Creature (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `0B6iOkMz64GCIzdO`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> While a creature infested by a hive corruption usually becomes a warrior, mutations can create hive creatures that retain the capabilities of the original creatures.
>
> **Quick Rules:** +3 to AC; +1 on rolls based on Str, Dex, and Con; –3 on rolls based on Cha; +1 hp/ HD; two claw attacks that each deal 1d4 points of damage (for Medium creatures) and one bite attack that deals 1d6 points of damage (for Medium creatures); immunity to acid; blind; blindsense 60 ft.; blindsight 10 ft.; corrosive blood*; hive mind*.
>
> **Rebuild Rules:** Type gain the hive subtype and all the corresponding abilities; AC natural armor bonus increases by 2; Melee two claw attacks that each deal 1d4 points of damage (for Medium creatures) and one bite attack that deals 1d6 points of damage (for Medium creatures); Ability Scores +2 Str, +2 Dex, +2 Con, –6 Cha.

**Mechanical encoding:** `changes`: 5
  - `2` → `dex`  (untyped)
  - `2` → `con`  (untyped)
  - `2` → `str`  (untyped)
  - `2` → `nac`  (untyped)
  - `-6` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Hivemind Swarm
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** Bestiary 5 (PZO1137) p. 156-157
**Foundry id:** `RDbGRXtfMeVnDcT2`

> "Hivemind swarm" is an acquired or inherited template that can be added to any creature with the swarm subtype (referred to hereafter as the base creature). The hivemind template allows a swarm to increase in power and abilities, much like a class—when you create a hivemind swarm, you can customize its CR as needed by adjusting the number of additional Hit Dice (and thus associated statistics). A hivemind swarm uses the base creature's statistics and special abilities except as noted here.
>
> **Challenge Rating:** +1 for each additional Hit Die gained above the base creature's Hit Dice.
>
> **Type:** A hivemind swarm's type remains unchanged unless the base creature was an animal or vermin. In this case, its type changes to magical beast.
>
> **Senses:** A hivemind swarm gains thoughtsense to a range of 60 feet.
>
> **Armor Class:** A hivemind swarm gains a +1 insight bonus to its AC per additional Hit Die.
>
> **Hit Dice:** A hivemind swarm gains at least one racial Hit Die in addition to the Hit Dice of the base creature. The type of racial Hit Die the hivemind swarm gains is the same as that of the base creature. A hivemind swarm can never gain more than 20 racial Hit Dice in this manner.
>
> **Saves:** The hivemind swarm's base saves increase as appropriate for a creature of its type as the hivemind swarm gains racial Hit Dice.
>
> **Defensive Abilities:** A hivemind creature retains all of the base creature's defensive abilities and special qualities, including all swarm traits. Due to its increased Intelligence score, a hivemind swarm is not immune to mind-affecting effects; since a hivemind swarm has a single mind, mind-affecting effects treat it as a single target despite its numerous separate bodies.
>
> **Attacks:** A hivemind creature retains its swarm attack, and continues to deal automatic damage to any creature whose space it occupies at the end of its move, with no attack roll needed. The swarm base damage is based on the hivemind's Hit Dice, starting at 1d6 for 1 Hit Die and increasing by 1d6 for every additional 5 Hit Dice beyond the first.
>
> **Special Attacks:** A hivemind creature retains all of the base creature's special abilities and gains the following special ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.9YsTT3kqnej4W0Fi inline=true]
>
> **Ability Scores:** If a base creature's Intelligence score is 10 or lower, the hivemind swarm gains a base Intelligence score of 11. A hivemind swarm's Intelligence score increases by 1 point for every Hit Die it gains beyond the base creature's Hit Dice. If the base creature's Charisma is lower than 10, the hivemind swarm gains a base Charisma score of 10. For every 4 Hit Dice the hivemind swarm gains beyond the base creature's Hit Dice, it gains a +1 bonus to an ability score of its choice (this bonus can be applied to Intelligence, and it stacks with the bonus to Intelligence that a hivemind swarm gains for every Hit Die it attains).
>
> **BAB:** A swarm's base attack bonus increases as it gains racial Hit Dice as appropriate for a creature of its type.
>
> **Feats:** A hivemind swarm loses all feats that the base creature had but gains a number of feats as normal for a creature of its Hit Dice (as presented on Table 1–6 @Source[PZO1112;pages=293]).
>
> **Skills:** A hivemind swarm loses all skill ranks that the base creature had but has skill ranks per racial Hit Die as defined by its creature type. A hivemind swarm's class skills are the same as those that its creature type had and also include all Knowledge skills and Spellcraft.
>
> **Languages:** A hivemind creature gains telepathy (100 ft.) and can speak a number of languages of its choice equal to 1 + its Intelligence modifier.
>
> **Special Qualities:** A hivemind gains the following.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.O99tATglvlozDgXI inline=true]

**Mechanical encoding:** `changes`: 2
  - `ifelse(gt(10, @abilities.int.total), 0, 11 - @abilities.int.base)` → `int`  (untyped)
  - `ifelse(gte(10, @abilities.cha.total), 0, 10 - @abilities.cha.base)` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Id Mutant
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `NnsKur4FhOsxb5ci`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** Yes
>
> Scholars of the mind have many names for the part of the psyche that controls unconscious and animalistic urges— be it the primal brain, instinct, or simply the id. Some scholars believe that, were this underlying mind to seize control, a normally mild-mannered person would revert to a savage, bestial state; some even theorize that when a barbarian enters a rage, he is in fact tapping into the id to empower his wrath. But what would happen if powerful magic were to act upon the id and make it transform not only a person's mind, but his physical being as well? One such method by which this can occur is via the curse of bestial dreams, an affliction that arises when the wishcraft of a vespergaunt interacts with powerful magical crystals infused with mortal dreams and memories—an affliction that, in time, transforms its victims into a deformed and bestial creature known as an id mutant.
>
> An id mutant loses its identity almost entirely, changing into an animalistic version of its previous self. If its adjusted Intelligence score remains above 3, it can still speak and understand language, but it does not retain any societal affiliations it had prior to devolving. Survival becomes the paramount concern for an id mutant, and it focuses more on base animalistic desires—the thrill of the hunt, securing a safe lair, and procreation. An id mutant's personality is entirely new—one based on fulfilling base needs, and as such an id mutant's alignment changes to chaotic neutral.
>
> When a humanoid becomes an id mutant, its physical deformations almost always result in a resemblance to a specific animal. Some believe this animal to be a sort of spirit animal, but in fact the animal associated with the mutation is somewhat arbitrary, influenced in part by the original creature's temperament and personality. For up to 10 days after a humanoid transforms into an id mutant, break enchantment or remove curse can remove the template. After this window of time closes, the condition becomes much more difficult to reverse. Both miracle and wish can restore an id mutant to its previous life. Likewise, an id mutant that dies and is then brought back from death sheds the template and is restored to its previous life.
>
> #### Creating an Id Mutant
>
> "Id mutant" is an acquired template that can be added to any humanoid (referred to hereafter as the base creature). An id mutant retains all the base creature's statistics and special abilities except as noted here. Statistics for several example id mutants can be found throughout this adventure.
>
> **CR:** Same as the base creature +1.
>
> **Alignment:** Chaotic neutral.
>
> **Senses:** An id mutant gains low-light vision.
>
> **AC:** An id mutant's natural armor bonus increases by 2.
>
> **Speed:** An id mutant's base speed increases by 10 feet. Some id mutants gain an additional movement type as well (see Special Qualities, below).
>
> **Melee:** An id mutant gains a single natural attack. This can be a bite, a claw, a gore, a slam, or a talon. Damage caused by this natural attack depends on the id mutant's size (see Table 3–1 on page 302 of the Pathfinder RPG Bestiary).
>
> **Feats:** An id mutant gains one of the following as a bonus feat: Great Fortitude, Iron Will, Lightning Reflexes, or Toughness.
>
> **Skills:** Id mutants gain a +4 racial bonus on Perception, Stealth, and Survival checks.
>
> **Ability Scores:** Str +4, Con +4, Int –6 (minimum 1), Cha –4 (minimum 1).
>
> **Special Qualities:** An id mutant gains one mutation from the list below for every 3 points of the base creature's adjusted CR (minimum 1). Additional mutations beyond these can be designed at the GM's discretion (although id mutants never gain supernatural or spell-like abilities in this manner, with the exception of the infectious mutation, described below).
>
> *Additional Movement (Ex): *The id mutant gains a burrow, climb, or fly speed (average maneuverability) equal to the base creature's unmodified speed. This mutation can be selected up to three times—each time, a different form of movement must be chosen.
>
> *Additional Natural Attack (Ex): *The id mutant gains an additional natural attack chosen from the Melee entry above. This mutation can be selected multiple times.
>
> *Aquatic (Ex): *The id mutant gains the aquatic subtype, a swim speed equal to its base land speed, and the amphibious special quality.
>
> *Blindsense (Ex): *The id mutant gains blindsense to a range of 30 feet. This mutation may be selected multiple times— each time it is selected, the range increases by 30 feet.
>
> *Ferocious (Ex): *The id mutant gains ferocity.
>
> *Infectious (Su): *Whenever an infectious id mutant damages a humanoid with one of its natural attacks, that humanoid must succeed at a Fortitude save (DC = 10 + 1/2 the id mutant's HD + the id mutant's Constitution modifier) or be afflicted by the curse of bestial dreams (see page 4).
>
> *Scent (Ex): *The id mutant gains the scent ability.
>
> *Swift (Ex): *The id mutant's base speed increases by an additional 20 feet.
>
> *Tentacled (Ex): *The id mutant gains a number of tentacle attacks equal to its adjusted CR divided by 5 (minimum 2). Each tentacle also has the grab and constrict special attack (constrict damage equals the tentacle's damage). This mutation can only be selected by id mutants of CR 10 or higher.
>
> *Thick Hide (Ex): *The id mutant's thick hide grants it DR 2/piercing. This mutation can be selected multiple times—each time it is selected, the DR increases by 2.

**Mechanical encoding:** `changes`: 9 (showing first 5)
  - `4` → `skill.sur`  (racial)
  - `-4` → `cha`  (untyped)
  - `10` → `landSpeed`  (untyped)
  - `4` → `skill.ste`  (racial)
  - `2` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Implacable Stalker
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `ev0AaPdPSSjI7Hew`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Implacable stalkers embody murderous predation. They not only revel in hunting down and killing their victims in gory, brutal fashion, but they draw supernatural strength and power from their victims’ fear and terror. They look similar to other creatures of their kind, but are often covered in gruesome scars and exude an aura of menace.
>
> "Implacable stalker" is an acquired template that can be added to any creature with an Intelligence score of 3 or higher. Most implacable stalkers are humanoids, monstrous humanoids, or outsiders. An implacable stalker uses the base creature’s stats and abilities except as noted here.
>
> **Challenge Rating:** Base creature’s CR + 2.
>
> **Alignment:** Any evil.
>
> **Senses:** An implacable stalker gains the following.
>
> *Sense Fear (Su):* An implacable stalker is able to sense the fear of nearby living creatures. This functions similarly to blindsight, with a range of 120 feet, except it only allows the implacable stalker to detect creatures that are currently experiencing any level of fear ranging from spooked to horrified (see page 10). Additionally, this ability allows the implacable stalker to detect such creatures even through solid barriers, but 1 foot of stone, 1 inch of common metal, a thin sheet of lead, or 3 feet of wood or dirt blocks it.
>
> **Armor Class:** Natural armor bonus increases by 6.
>
> **Defensive Abilities:** An implacable stalker gains DR 5/—, and resistance to acid, cold, electricity, fire, and sonic 10. The implacable stalker also gains the following defensive ability.
>
> *Terrifying Inevitability (Su):* An implacable stalker is even more difficult to kill when in the presence of fear. As long as the implacable stalker is able to see or hear a creature currently experiencing any level of fear ranging from spooked to horrified (see page 10), it gains fast healing equal to its Hit Dice, its damage reduction increases to 10/—, and it gains spell resistance equal to 16 + its CR.
>
> **Speed:** An implacable stalker’s base land speed is reduced by 10 feet if its base speed is 20 feet or higher.
>
> **Special Attacks:** An implacable stalker gains the following special attacks.
>
> *Fear Aura (Su): *Creatures that have at least 5 fewer Hit Dice than the implacable stalker must succeed at a Will save or become frightened for 1 minute if they come within 60 feet of it. Even if they succeed at their saves, they gain the shaken condition for as long as they remain within 60 feet of the implacable stalker, and for 1 round thereafter. All other creatures within this radius must succeed at a Will save or become shaken for as long as they remain within 60 feet of the implacable stalker, and for 1 round thereafter. A creature that successfully saves cannot be affected again by the same implacable stalker’s aura until the creature has left the aura and reentered it. This is a mind-affecting fear effect.
>
> *Gory Display (Ex):* Whenever an implacable stalker kills a sentient living creature, as a swift action, it can revel in the kill, shredding its victim’s corpse in a gruesome display of power. If it does, it chooses one of the following benefits: gain a +4 morale bonus to Strength and Dexterity for 1 minute, regain a single use of a spell-like ability that it can normally use three or more times per day, or immediately heal a number of hit points equal to its Hit Dice.
>
> Alternatively, instead of any of these benefits, the implacable stalker can cause a single creature within 60 feet to become more vulnerable to fear. Creatures affected in this way lose any immunity to fear they may have. If the creature did not possess immunity to fear, it takes a –4 penalty on saving throws to resist fear effects, and all Intimidate checks attempted against it receive a +4 circumstance bonus. These effects last for 10 minutes. Finally, if the creature is currently immune to the implacable stalker’s fear aura because it succeeded at a previous saving throw, it loses that immunity.
>
> **Special Qualities:** An implacable stalker gains the following special qualities.
>
> *Nightmare Resurrection (Su):* When an implacable stalker dies, it creates a psychic imprint on the mind of each intelligent creature within 60 feet that witnessed its death. Each week, such creatures are subject to a nightmare effect (DC = 10 + 1/2 the implacable stalker’s Hit Dice + the implacable stalker’s Charisma modifier; the normal modifiers for nightmare based on knowledge and connection do not apply). In this nightmare, the creature is hunted and slain by the implacable stalker (for GMs using the nightmare dreamscape rules on page 162, these nightmares always have the "being chased" nightmare feature). A creature that succeeds at three consecutive saving throws to resist the effect is freed from it. If any creature fails at three consecutive saving throws to resist the nightmare, the implacable stalker returns to life, as per true resurrection. If its corpse has been completely destroyed, it returns to life in a random location within 5 miles of the creature that failed to resist the nightmare effects. Once the implacable stalker is returned to life, the psychic imprint fades from all creatures still affected by it. Right Behind You (Sp): As a swift action, an implacable stalker can teleport to an unoccupied space, which must be adjacent to a creature the stalker is aware of that has the shaken, frightened, or panicked condition. The implacable stalker can travel a maximum distance of 480 feet with each use of this ability, and must wait 1d6 rounds between each use. Additionally, if the implacable stalker travels at least 40 feet, any shaken, frightened, or panicked creature it arrives adjacent to is denied its Dexterity bonus to AC against the implacable stalker’s attacks until the beginning of the implacable stalker’s next turn.
>
> **Ability Scores:** Strength +4, Constitution +6 (if the implacable stalker is an undead creature, it gains Charisma +6, instead).
>
> **Skills:** Implacable stalkers gain a +8 racial bonus on Intimidate checks, and a +6 racial bonus on Stealth checks and Survival checks to follow tracks.
>
> **Feats:** Implacable stalkers gain Diehard, Endurance, Intimidating Prowess, and Toughness as bonus feats.

**Mechanical encoding:** `changes`: 5
  - `6` → `con`  (untyped)
  - `8` → `skill.int`  (racial)
  - `4` → `str`  (untyped)
  - `6` → `nac`  (untyped)
  - `6` → `skill.ste`  (racial)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Jiang-Shi
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1120 (PZO1120) p. 278-279
**Foundry id:** `VGwEIJd4FAQVr6DR`

> Jiang-shis (often known as "hopping vampires") are undead humanoid creatures that feed on the exhaled life energy of the living. A jiang-shi's appearance is based on the state of the creature's corpse at the time of its reanimation. Regardless of the state of decay, most jiang-shis wear clothing or armor that is at least one generation out of style. Additionally, each has a short parchment prayer scroll affixed to its brow by stitches; originally intended to protect the body from restless spirits, this scroll grants a jiang-shi immunity to magical effects unleashed by items like scrolls and wands.
>
> A jiang-shi is created when a restless spirit does not leave its corpse at the time of death, and is instead allowed to fester and putrefy within. At some point during the body's decomposition, the thing rises in its grotesque form and seeks living creatures to feed upon.
>
> "Jiang-shi" is an acquired template that can be added to any living creature with 5 or more Hit Dice (referred to hereafter as the base creature). Most jiang-shis were once humans, but any creature that undergoes specific rites can acquire the template. A jiang-shi uses the base creature's stats and abilities except as noted here.
>
> **CR:** Same as the base creature +2.
>
> **Alignment:** Any evil.
>
> **Type:** The creature's type changes to undead (augmented). Do not recalculate class Hit Dice, BAB, or saves.
>
> **Senses:** A jiang-shi vampire gains darkvision 60 feet. It also gains the ability to sense the breathing of living creatures—a jiang-shi has blindsight to a range of 60 feet against creatures that breathe. A creature may hold its breath to prevent a jiang-shi from noticing it in this manner.
>
> **Armor Class:** Natural armor improves by +2.
>
> **Hit Dice:** Change all racial Hit Dice to d8s. Class Hit Dice are unaffected. As undead, jiang-shis use their Charisma modifier to determine bonus hit points (instead of Constitution).
>
> **Defensive Abilities:** A jiang-shi gains channel resistance +4, DR 10/magic and slashing, and resistance to cold 20, in addition to all of the defensive abilities granted by the undead type. A jiang-shi also gains fast healing 5. In addition, all jiang-shis gain the following defensive ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.NtJrBCMl4UCuuqDW inline=true]
>
> **Weaknesses:** Jiang-shis recoil from mirrors or the sound of handbells rung within 10 feet of them. Cooked rice, which to jiang-shis mocks the fundamental fact that they no longer eat food, shames them into recoiling as well. These things don't harm a jiang-shi vampire—they merely keep it at bay for a period of time. A recoiling jiang-shi vampire must stay at least 5 feet away from the object of its revulsion, and cannot touch or make melee attacks against a creature brandishing the object during that round. Holding a jiang-shi vampire at bay takes a standard action. After being held at bay for 1 round, a jiang-shi vampire can attempt to overcome its revulsion of the object and function normally each round it makes a @Save[will;dc=20] save at the start of its turn.
>
> *Destroying a Jiang-Shi*: If reduced to 0 hit points, a jiang-shi vampire crumbles to dust but is not destroyed. It reforms in 1 minute with 1 hit point in the same space, or the nearest unoccupied space. Scattering the dust before the jiang-shi reforms destroys it permanently, as does mixing rice into the dust with a dose of holy water. Jiang-shi vampires are also susceptible to wooden weapons carved from peach trees, as such weapons represent the unity of all elements and life to these creatures. A wooden weapon carved from a peach tree automatically bypasses a jiang-shi vampire's damage reduction. Additionally, any successful hit from such a weapon that reduces a jiang-shi to 0 hit points immediately destroys the creature. Although they normally retreat from daylight, jiang-shi vampires are not destroyed by sunlight like regular vampires and can move around during the day without harm.
>
> **Speed:** A jiang-shi moves only by hopping. This mode of movement is somewhat less swift than regular movement, and thus a jiang-shi's base speed is reduced by 10 feet from the base creature's speed, to a minimum of 10 feet. This unusual mode of movement allows the jiang-shi to ignore the effects of difficult terrain on movement, and makes it impossible to trip. Other speeds (like fly or swim speeds) are not affected by this reduction.
>
> **Melee:** A jiang-shi gains a bite attack and 2 claw attacks if the base creature didn't have them. Damage for the bite attack depends on the jiang-shi's size, but its claw attacks do damage as a creature two size categories larger. For a Medium jiang-shi, a bite attack deals 1d6 points of damage and a claw attack deals 1d8 points of damage. A jiang-shi's claws are even more dangerous than this, though—see the @UUID[Compendium.pf1.template-abilities.Item.FuxJPnq1cUpHoUHn] special attack below. A jiang-shi's natural weapons are treated as magic weapons for the purpose of overcoming damage reduction.
>
> **Special Attacks:** A jiang-shi gains several special attacks. Save DCs are equal to 10 + 1/2 the jiang-shi's Hit Dice + the jiang-shi's Charisma modifier unless otherwise noted.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.FuxJPnq1cUpHoUHn inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.XCuxIeOyCiCQAvdR inline=true]
>
> **Ability Scores:** Str +4, Dex +6, Int +2, Wis +4, Cha +2. As an undead creature, a jiang-shi has no Constitution score.
>
> **Feats**: Jiang-shis gain Alertness, Dodge, Mobility, Skill Focus (Acrobatics), and Spring Attack as bonus feats.
>
> **Skills:** Jiang-shis gain a +8 racial bonus on Acrobatics, Perception, and Stealth checks.

**Mechanical encoding:** `changes`: 11 (showing first 5)
  - `8` → `skill.per`  (racial)
  - `4` → `wis`  (untyped)
  - `5` → `bonusFeats`  (untyped)
  - `min(@attributes.speed.land.total, max(10, @attributes.speed.land.base - 10))` → `landSpeed`  (untyped)
  - `2` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Juju Zombie
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1116 (PZO1116) p. 291
**Foundry id:** `AqTrfwmoBJUsVnNq`

> A juju zombie is an animated corpse of a creature, created to serve as an undead minion, that retains the skills and abilities it possessed in life.
>
> "Juju zombie" is an acquired template that can be added to any living corporeal creature, referred to hereafter as the base creature.
>
> **CR:** As base creature +1.
>
> **Alignment:** Any evil.
>
> **Type:** The creature's type changes to undead. It retains any subtype except for alignment subtypes and subtypes that indicate kind.
>
> **Armor Class:** A juju zombie gains a +3 bonus to its natural armor over the base creature's natural armor bonus.
>
> **Hit Dice:** Change all the creature's racial Hit Dice to d8s. All Hit Dice derived from class levels remain unchanged. As undead, juju zombies use their Charisma modifiers to determine bonus hit points (instead of Constitution).
>
> **Defensive Abilities:** Juju zombies gain channel resistance +4, DR 5/magic and slashing (or DR 10/magic and slashing if it has 11 HD or more), and fire resistance 10. They are immune to cold, electricity, and @UUID[Compendium.pf1.spells.Item.49yc9dpr4kvgki2s].
>
> **Speed:** A winged juju zombie's maneuverability drops to clumsy. If the base creature flew magically, its fly speed is unchanged. Retain all other movement types.
>
> **Attacks:** A juju zombie retains all the natural weapons, manufactured weapon attacks, and weapon proficiencies of the base creature. It also gains a slam attack that deals damage based on the juju zombie's size, but as if it were one size category larger than its actual size.
>
> **Abilities:** Increase from the base creature as follows: Str +4, Dex +2. A juju zombie has no Con score; as an undead, it uses its Charisma in place of Constitution when calculating hit points, Fortitude saves, or any special ability that relies on Constitution.
>
> **Feats:** A juju zombie gains @UUID[Compendium.pf1.feats.Item.Uuiu3p982omhMEPj] and @UUID[Compendium.pf1.feats.Item.8snLqsJN4LLL00Nq] as bonus feats.
>
> **Skills:** A juju zombie gains a +8 racial bonus on all Climb checks.

**Mechanical encoding:** `changes`: 5
  - `3` → `nac`  (untyped)
  - `4` → `str`  (untyped)
  - `2` → `dex`  (untyped)
  - `2` → `bonusFeats`  (untyped)
  - `8` → `skill.clm`  (racial)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Kanabo
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `QcWu43ghd0dQslRo`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** No
>
> Within Kaoling, those oni that take the form of hobgoblins—known as ja noi—are treated as honored champions. While ja noi have an overwhelming need to engage in regular battle and command troops, and can be dangerous if too much time passes between fights, this drive is easily met by Kaoling’s regular military operations, and most hobgoblin soldiers are only too willing to fight at a ja noi’s command. While other oni are respected for their size and strength, they are generally treated as valued allies rather than members of Kaoling society. Ja noi, by contrast, are embraced as revered cousins, and closely integrated into Kaoling communities.
>
> Though rare, sometimes such close association leads to children being born with one ja noi and one hobgoblin parent. These half-ja noi offspring are known as kanabo, a term that can also be used to refer to an iron club or translated as meaning "the strongest," which is how the hobgoblins of Kaoling view the oni-kin among them. Kanabo inherit much of their oni parent’s vitality, mystic power, and cunning, but lack the ja noi drive to fight even when no foe is present.
>
> Kanabo is an inherited template that can be added to a living, corporeal humanoid of the goblinoid subtype. A kanabo uses all the base creature’s statistics and special abilities except as noted here.
>
> **CR:** HD 10 or less, as base creature + 1; HD 11 or more, as base creature + 2.
>
> **Alignment:** Lawful evil.
>
> **Type:** The creature’s type changes to outsider (native). Do not recalculate HD, BAB, or saves.
>
> **Armor Class:** Natural armor improves by +1.
>
> **Defenses/Qualities:** HD 11 or less, gains regeneration 1 (acid and fire); HD 12 or more, gains regeneration 5 (acid and fire).
>
> **Spell-Like Abilities:** A kanabo with an Intelligence or Wisdom score of 8 or higher has a cumulative number of spell-like abilities set by its HD. Unless otherwise noted, an ability is usable 1/day. Caster level equals the creature’s HD (or the CL of the base creature’s spell-like abilities, whichever is higher).
>
>
>
>
>  **HD** 
>  **Abilities** 
>
>
>  1–2 
>  *Doom* 3/day, *magic weapon* 3/day 
>
>
>  3–4 
>  *Bull’s strength*, *command* 3/day 
>
>
>  6–8 
>  *Fly* 3/day 
>
>
>  9+ 
>  *Alter self* (at will), *monstrous physique I* (at will, *Pathfinder RPG Ultimate Magic*) 
>
>
>
>
> **Abilities:** A kanabo gains a +4 bonus to Strength and Constitution, and a +2 bonus to Dexterity, Intelligence, Wisdom, and Charisma.
>
> **Skills:** A kanabo with racial HD has skill ranks equal to 6 + its Intelligence modifier for each racial HD. Racial class skills are unchanged, and class level skill ranks are unaffected.

**Mechanical encoding:** `changes`: 7 (showing first 5)
  - `2` → `int`  (untyped)
  - `2` → `wis`  (untyped)
  - `2` → `cha`  (untyped)
  - `1` → `nac`  (untyped)
  - `2` → `dex`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Lich Creature (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `dOa4aQoSdHOtplkp`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> While it might not have followed the traditional path to lichdom, which requires a strong aptitude for magic, a lich creature’s connection to an object allows it to survive as an undead indefinitely, returning each time its foes destroy it unless they can destroy the lich creature’s phylactery (Bestiary 188).
>
> **Quick Rules:** Counts as undead; darkvision 60 ft.; rejuvenation*; immune to cold and electricity; undead immunities; +1 on rolls based on Int, Wis, and Cha; touch attack deals 1d8 + 1/2 HD points of damage plus paralyzing touch*; fear aura*.
>
> **Rebuild Rules:** Type change to undead; Senses darkvision 60 ft.; Defensive Abilities rejuvenation*; Immune cold, electricity; Melee touch attack deals 1d8 + 1/2 HD points of damage plus paralyzing touch*; Special Attacks fear aura*, paralyzing touch*; Ability Scores +2 Int, +2 Wis, +2 Cha.

**Mechanical encoding:** `changes`: 7 (showing first 5)
  - `1` → `chaSkills`  (untyped)
  - `1` → `wisChecks`  (untyped)
  - `1` → `wisSkills`  (untyped)
  - `1` → `intChecks`  (untyped)
  - `1` → `chaChecks`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Lich Creature (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `BbSctxbenUZvX9T9`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> While it might not have followed the traditional path to lichdom, which requires a strong aptitude for magic, a lich creature’s connection to an object allows it to survive as an undead indefinitely, returning each time its foes destroy it unless they can destroy the lich creature’s phylactery (Bestiary 188).
>
> **Quick Rules:** Counts as undead; darkvision 60 ft.; rejuvenation*; immune to cold and electricity; undead immunities; +1 on rolls based on Int, Wis, and Cha; touch attack deals 1d8 + 1/2 HD points of damage plus paralyzing touch*; fear aura*.
>
> **Rebuild Rules:** Type change to undead; Senses darkvision 60 ft.; Defensive Abilities rejuvenation*; Immune cold, electricity; Melee touch attack deals 1d8 + 1/2 HD points of damage plus paralyzing touch*; Special Attacks fear aura*, paralyzing touch*; Ability Scores +2 Int, +2 Wis, +2 Cha.

**Mechanical encoding:** `changes`: 3
  - `2` → `int`  (untyped)
  - `2` → `wis`  (untyped)
  - `2` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Lich
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 188-189
**Foundry id:** `honQfTrmEEvFQ3hp`

> "Lich" is an acquired template that can be added to any living creature (referred to hereafter as the base creature), provided it can create the required phylactery. A lich retains all the base creature's statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature + 2.
>
> **Alignment:** Any evil.
>
> **Type:** The creature's type changes to undead. Do not recalculate BAB, saves, or skill ranks.
>
> **Senses:** A lich gains darkvision 60 ft.
>
> **Armor Class:** A lich has a +5 natural armor bonus or the base creature's natural armor bonus, whichever is better.
>
> **Hit Dice:** Change all of the creature's racial Hit Dice to d8s. All Hit Dice derived from class levels remain unchanged. As undead, liches use their Charisma modifiers to determine bonus hit points (instead of Constitution).
>
> **Defensive Abilities:** A lich gains channel resistance +4, DR 15/bludgeoning and magic, and immunity to cold and electricity (in addition to those granted by its undead traits). The lich also gains the following defensive ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.G4kaLOlyrNrKK0AS inline=true]
>
> **Melee Attack:** A lich has a touch attack that it can use once per round as a natural weapon. A lich fighting without weapons uses its natural weapons (if it has any) in addition to its touch attack (which is treated as a primary natural weapon that replaces one claw or slam attack, if the creature has any). A lich armed with a weapon uses its weapons normally, and can use its touch attack as a secondary natural weapon.
>
> **Damage:** A lich's touch attack uses negative energy to deal 1d8 points of damage to living creatures + 1 point of damage per 2 Hit Dice possessed by the lich. As negative energy, this damage can be used to heal undead creatures. A lich can take a full-round action to infuse itself with this energy, healing damage as if it had used its touch attack against itself.
>
> **Special Attacks:** A lich gains the two special attacks described below. Save DCs are equal to 10 + 1/2 lich's HD + lich's Cha modifier unless otherwise noted.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.7oahBi33JdZ1DjAn inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.FFUzHo7zlM6B0Xsw inline=true]
>
> **Abilities:** Int +2, Wis +2, Cha +2. Being undead, a lich has no Constitution score.
>
> **Skills:** Liches have a +8 racial bonus on Perception, Sense Motive, and Stealth checks. A lich always treats Climb, Disguise, Fly, Intimidate, Knowledge (arcana), Knowledge (religion), Perception, Sense Motive, Spellcraft, and Stealth as class skills. Otherwise, skills are the same as the base creature.

**Mechanical encoding:** `changes`: 7 (showing first 5)
  - `max(@ac.natural.total, 5)` → `nac`  (untyped)
  - `2` → `int`  (untyped)
  - `2` → `cha`  (untyped)
  - `8` → `skill.ste`  (racial)
  - `2` → `wis`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Lycanthrope
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 196
**Foundry id:** `IpQhYuRgQJDACRr9`

> Lycanthropes are humanoids with the ability to turn into animals and animal-humanoid hybrid shapes. Natural lycanthropes are born with this ability and have perfect control over their shapechanging. Afflicted lycanthropes contract this ability like a curse or disease from another lycanthrope; they sometimes change form involuntarily.
>
> "Lycanthrope" is an inherited (for natural lycanthropes) or acquired (for afflicted lycanthropes) template that can be added to any humanoid.
>
> **Challenge Rating:** Same as base creature or base animal (whichever is higher) + 1.
>
> **Size and Type:** The creature (referred to hereafter as the base creature) gains the shapechanger subtype. The lycanthrope takes on the characteristics of some type of animal (referred to hereafter as the base animal) within one size category of the base creature's size. A lycanthrope's hybrid form is the same size as the base animal or the base creature, whichever is larger.
>
> **AC:** In hybrid or animal form the lycanthrope has the natural armor bonus of the base animal increased by +2.
>
> **Defensive Abilities:** A natural lycanthrope gains DR 10/silver in animal or hybrid form. An afflicted lycanthrope gains DR 5/silver in animal or hybrid form.
>
> **Speed:** Same as the base creature or base animal, depending on which form the lycanthrope is using. Hybrids use the base creature's speed.
>
> **Melee:** A lycanthrope gains natural attacks in animal and hybrid forms according to the base animal.
>
> **Special Attacks:** A lycanthrope retains all the special attacks, qualities, and abilities of the base creature. In hybrid or animal form it gains the special attacks, qualities, and abilities of the base animal. A lycanthrope also gains low-light vision, scent, and the following:
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.cR3nXvyFgdohIkLd inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.1BTw6p0EgMD2PZHQ inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.RKGxk0cxmMNByCle inline=true]
>
> **Ability Scores:** +2 Wis, –2 Cha in all forms; +2 Str, +2 Con in hybrid and animal forms. Lycanthropes have enhanced senses but are not fully in control of their emotions and animalistic urges. In addition to these adjustments to the base creature's stats, a lycanthrope's ability scores change when he assumes hybrid or animal form. In human form, the lycanthrope's ability scores are unchanged from the base creature's form. In animal and hybrid form, the lycanthrope's ability scores are the same as the base creature's or the base animal's, whichever ability score is higher.

**Mechanical encoding:** `changes`: 2
  - `2` → `wis`  (untyped)
  - `-2` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Lycanthropic Creature (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `QzzviyFKJkv2v1kK`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> Lycanthropic creatures can act as simpler variants of any sort of lycanthrope in hybrid form, but the default is for a werewolf-like creature, so if the base lycanthrope has different features, adjust the creature accordingly (for instance, a wereshark can swim). This simple template reflects the creature's hybrid form. The creature can't take full animal form, and when it's in its ordinary form, remove this template with the exceptions of change shape, low-light vision, and scent. Lycanthropic creatures don't have to be humanoids, and at your discretion, a lycanthropic creature can afflict creatures of its own type with lycanthropy, in addition to humanoids.
>
> **Quick Rules:** +1 to AC; DR 5/silver; +1 on rolls based on Str, Dex, and Con; +1 hp/HD; bite attack that deals 1d6 points of damage (for Medium creatures) plus curse of lycanthropy*; change shape (normal or hybrid form; polymorph); lycanthropic empathy* (as appropriate for the lycanthrope).
>
> **Rebuild Rules:** Type gain the shapechanger subtype; DR 5/ silver; Senses low-light vision, scent; AC natural armor bonus increases by 1; Melee bite attack that deals 1d6 points of damage (for Medium creatures) plus curse of lycanthropy*; Special Attacks curse of lycanthropy*; Special Qualities change shape (normal or hybrid form; polymorph), lycanthropic empathy* (as appropriate for the lycanthrope); Ability Scores +2 Str, +2 Dex, +2 Con.

**Mechanical encoding:** `changes`: 12 (showing first 5)
  - `1` → `dexChecks`  (untyped)
  - `1` → `strSkills`  (untyped)
  - `1` → `dexSkills`  (untyped)
  - `1` → `ref`  (untyped)
  - `1` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Lycanthropic Creature (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `vaa3bb2DjxcGx0KU`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> Lycanthropic creatures can act as simpler variants of any sort of lycanthrope in hybrid form, but the default is for a werewolf-like creature, so if the base lycanthrope has different features, adjust the creature accordingly (for instance, a wereshark can swim). This simple template reflects the creature’s hybrid form. The creature can’t take full animal form, and when it’s in its ordinary form, remove this template with the exceptions of change shape, low-light vision, and scent. Lycanthropic creatures don’t have to be humanoids, and at your discretion, a lycanthropic creature can afflict creatures of its own type with lycanthropy, in addition to humanoids.
>
> **Quick Rules:** +1 to AC; DR 5/silver; +1 on rolls based on Str, Dex, and Con; +1 hp/HD; bite attack that deals 1d6 points of damage (for Medium creatures) plus curse of lycanthropy*; change shape (normal or hybrid form; polymorph); lycanthropic empathy* (as appropriate for the lycanthrope).
>
> **Rebuild Rules:** Type gain the shapechanger subtype; DR 5/ silver; Senses low-light vision, scent; AC natural armor bonus increases by 1; Melee bite attack that deals 1d6 points of damage (for Medium creatures) plus curse of lycanthropy*; Special Attacks curse of lycanthropy*; Special Qualities change shape (normal or hybrid form; polymorph), lycanthropic empathy* (as appropriate for the lycanthrope); Ability Scores +2 Str, +2 Dex, +2 Con.

**Mechanical encoding:** `changes`: 4
  - `2` → `dex`  (untyped)
  - `2` → `str`  (untyped)
  - `2` → `con`  (untyped)
  - `1` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Man-Eating Animal
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `Uaz02FMkVRqx017e`

> **Acquired/Inherited Template** Both**Simple Template** No**Usable with Summons** No
>
> Scholars will explain that though many animals fight to defend their territory and their young, only a few apex predators hunt humanoids for food. Yet any villager across the Inner Sea region can recount tales about maneating beasts that once lurked in the local wilderness (and might still). Any sort of animal can become a man-eater, from known predators to seemingly harmless herbivores. Though the creatures and locations may change, certain elements remain the same in tales of man-eating animals. Having tasted human flesh, these animals can’t be sated by any other type of food. Man-eaters have terrible bites, and hunters’ arrows bounce off their hides. Man-eaters are unusually bold, no longer frightened by human presence like their kin. Yet they are also canny, employing tactics no mere animal could conceive. Man-eaters appear able to understand human speech, and some of the more fanciful stories even claim the animals can speak.
>
> A man-eating animal can be distinguished from its common relatives by its carnivorous teeth, enlarged jaws, and the glint of intelligence in its eyes.
>
> ### Ecology
>
> Most tales of man-eating animals are sparked by rabid or starving (but otherwise normal) animals, but true man-eaters do exist. Such abominations are the result of a fiendish spirit fusing with that of a mundane animal. Though not wholly fiendish in nature, the beast gains limited sentience, increased resilience, and unnatural appetites. Despite popular belief, eating humanoid flesh isn’t enough to turn an animal into a maneater. The creature must be exposed to chaotic and evil influences, whether from a planar gate, demonic altar, or transformative elixir (such as the blood of Baphomet). Man-eating animals can also result from botched summonings and incomplete exorcisms. A fiendish spark set loose might inhabit an animal’s form so that the foul spirit can continue to spread suffering.
>
> Man-eating animals are no longer part of the natural ecology. They hunt almost ceaselessly, preferring intelligent prey above all else. They rarely die of natural causes, almost always meeting their ends in bloody conflict. These creatures can and do mate with members of their original species. In cases of multiple births, only one of the litter inherits this corruption, and it soon devours its siblings.
>
> ### Habitat & Society
>
> Individual man-eaters might be found anywhere—the freak results of black magic and vicious natures—but they’re encountered in numbers only where fiendish influence is strong. Man-eating animals are most common in the blasted landscape of the Worldwound, where they nearly outnumber their natural counterparts. In Kyonin, maneaters have been born to otherwise normal animals, a sign to the elves that Tanglebriar’s corruption is expanding.
>
> Man-eating animals, especially large bovines such as aurochs and bison, are sacred to the followers of Baphomet, demon lord of beasts. Away from civilized lands, cults of Baphomet raise small herds of these carnivorous cattle, feeding them on corpses when live victims are unavailable. Man-eating animals serve as guards and pets for dark cultists and the demons they worship. Though too intelligent and willful to be trained like normal animals, man-eaters gladly serve those who encourage their bloodlust. A dissatisfied man-eater, however, is likely to turn on its so-called master the second its master displays a moment of weakness.
>
> With their rudimentary intelligence, man-eating animals are able to understand the guttural tongue of the Abyss, and to learn common words in the language of those they hunt. Many take advantage of hunters who assume they are dumb animals.
>
> Man-eaters’ combination of animal instinct and demonic cunning allows them to more easily hunt their preferred prey: humanoids. Man-eating animals are known to track victims over long distances, their enhanced senses and great endurance allowing them to continue the chase long after their prey becomes fatigued. An innate sense of direction sometimes allows a man-eater to anticipate (or overhear) its victim’s destination and reach it before the creature. Even latched gates and animal traps prove ineffective against the man-eater’s cunning.
>
> "Man-Eating" is an inherited or acquired template that can be added to a creature of the animal type. A maneating animal uses all the base creature’s statistics and special abilities except as noted here.
>
> **CR:** HD 4 or fewer, as base creature + 1; HD 5 to 10, as base creature + 2; HD 11 or more, as base creature + 3.
>
> **Alignment:** Chaotic evil.
>
> **Type:** A man-eating animal’s type changes to magical beast. It retains any subtypes except for alignment subtypes.
>
> **Armor Class:** A man-eating animal’s natural armor improves by +2.
>
> **Hit Dice:** A man-eating animal’s racial HD change to d10s.
>
> **Defenses/Qualities:** A man-eating animal gains darkvision 60 feet, and DR 5/slashing (if HD 11 or fewer) or 10/slashing (if HD 12 or more).
>
> **Melee:** A man-eating animal gains a bite attack. Damage from the bite attack depends on the creature’s size (Pathfinder RPG Bestiary 301–302). If the base creature already has a bite attack, it gains Improved Natural Attack (bite) and Improved Critical (bite) as bonus feats. It also adds 1-1/2 times its Str bonus to the damage (or twice its Str bonus if a bite is its only natural attack).
>
> **Abilities:** Con +4, Int +2, Wis +4, Cha +4.
>
> **BAB:** A man-eating animal’s base attack bonus is equal to its Hit Dice.
>
> **Skills:** A man-eating animal gains a +4 racial bonus on Survival checks to follow tracks.
>
> **Languages:** A man-eating animal understands Abyssal and Common, but cannot speak.

**Mechanical encoding:** `changes`: 6 (showing first 5)
  - `4` → `wis`  (untyped)
  - `2` → `int`  (untyped)
  - `4` → `con`  (untyped)
  - `@attributes.hd.total` → `mhp`  (untyped)
  - `4` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mana Wastes Mutant
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `zAm6hRD11BS0r7xl`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> The magic-warping effects of the Mana Wastes often extend to the very life force of creatures who wander the trackless deserts. The dangerous radiations of magic gone afoul infuse the bodies and essences of these wanderers. Those who spend too much time in the Spellscar Desert or the wasteland's other treacherous environs occasionally fall prey to the deadly energies that persist in these regions, and their bodies gradually decay more and more until they are so far removed from their original forms that they can be described only as mutants. These twisted and degenerate creatures roam in packs throughout the Mana Wastes.
>
> Because those who succumb to the Mana Wastes' mutagenic effects often hail from the Grand Duchy of Alkenstar or one of its smaller holdings in the region, numerous humanoid mutants are proficient in the use of firearms, having learned to wield the weapons in place of the unpredictable forces of magic. Those who manage to actually secure a powerful weapon from one of the dwarven arms factories in the Wastes often garner the respect of other mutants. Such firearm wielders invariably rise to positions of power, becoming known as wasteland lords by their envious peers, who all squabble and fight for the same honor.
>
> Most Mana Wastes mutants collaborate in small tribal groups with other mutants, since those who wander the battered desert alone risk attack from the resident mutated vermin or violent bands of lawless gnolls, giants, or goblins. The civilized people of Alkenstar shun mutants for the most part, regarding transformed humans and other wanderers of the Mana Wastes as no better than monsters. The border guards of neighboring Nex keep a stringent lookout for such wasteland travelers and attack them on sight. The necromancers of Geb, however, see potential in the mutated peoples of the Spellscar Desert, and occasionally entreat them to leave their blasted home and relocate to the heart of Geb in Yled by promising a life of comfort and acceptance. In actuality, such mutants are taken to the infamous Mortuarium, where Geb's cruelest wizards perform unholy experiments on Alkenstar's deformed expatriates and turn them into undead abominations to serve in Geb's lurching army.
>
> "Mana Wastes Mutant" is an acquired template that can be added to any living, corporeal creature. A Mana Wastes mutant retains the base creature's statistics and special abilities except as noted here.
>
> **CR:** As base creature +1.
>
> **Alignment:** Any non-lawful.
>
> **Type:** The creature's type changes to aberration. Do not recalculate HD, BAB, or saves.
>
> **Armor Class:** A Mana Wastes mutant gains a +2 bonus to its natural armor over the base creature's natural armor bonus.
>
> **Defensive Abilities:** A Mana Wastes mutant gains a +4 bonus on saves against mind-affecting effects, DR 5/cold iron (or DR 10/cold iron if the base creature has 11 HD or more), and spell resistance equal to 11 + its adjusted CR. Mana Wastes mutants are immune to disease and poison.
>
> **Speed:** A winged Mana Wastes mutant's maneuverability drops to clumsy. If the base creature flew magically, it loses this ability.
>
> **Melee:** A Mana Wastes mutant retains all the natural weapons, manufactured weapon attacks, and weapon proficiencies of the base creature. It also gains a slam attack that deals damage based on the mutant's size.
>
> **Spell-Like Abilities:** A Mana Wastes mutant loses access to any spell-like abilities the base creature may have had. Any spellcasting abilities gained from class levels remain unchanged.
>
> **Special Abilities:** A Mana Wastes mutant retains any extraordinary and supernatural special qualities of the base creature. A Mana Wastes mutant gains one of the following abilities for every 4 HD or fraction thereof (minimum 1— the first ability chosen must always be disease).
>
> *Acid Resistance (Su): *A Mana Wastes mutant gains resistance to acid 10. This ability can be taken more than once. Each time it is taken, the Mana Wastes mutant increases its resistance to acid by an additional 10. A Mana Wastes mutant that gains acid resistance in excess of 30 becomes immune to acid instead.
>
> *Acidic Pustules (Ex):* Mana Wastes mutants are often covered in necrotic pustules that burst at the slightest touch. Whenever a creature deals piercing or slashing damage to a Mana Wastes mutant, all creatures adjacent to the Mana Wastes mutant must succeed at a Reflex save (DC = 10 + 1/2 the Mana Wastes mutant's Hit Dice + the Mana Wastes mutant's Constitution modifier) or take acid damage as its boils and blisters pop and spray about. A Mana Wastes mutant deals an amount of acid damage in this way based on its size (1d4 points of acid damage for a Medium Mana Wastes mutant, 1d6 for a Large mutant, and so on).
>
> *Breath Weapon (Ex): *A Mana Wastes mutant can spray a 30-foot cone of acidic bile from its mouth as a standard action once every 1d4 rounds. The acid damage caused by this attack is equal to 1d6 per two Hit Dice the mutant possesses. A successful Reflex save (DC = 10 + 1/2 the Mana Waste mutant's Hit Dice + the Mana Waste mutant's Constitution modifier) halves any damage taken from this attack.
>
> *Disease (Su): *Even though Mana Wastes mutants are immune to disease, they carry a deadly magical contagion that they spread with their slam attacks. Mana fever: injury; save Fort DC = 10 + 1/2 the Mana Wastes mutant's Hit Dice + the Mana Wastes mutant's Constitution modifier; onset 1d4 minutes; frequency 1/day; effect 1d2 Con damage, 1d2 Cha drain (or 1d3 Con damage, 1d3 Cha drain if the base creature has 8 HD or more); cure 2 consecutive saves. Anyone who lives with mana fever for a week straight without dying becomes immune to the disease, but also becomes a Mana Wastes mutant.
>
> *Increased Speed (Ex):* Some Mana Wastes mutants are transformed in such a way that their base speed increases by 10 feet.
>
> **Deformities:** In addition to its special abilities listed above, a Mana Wastes mutant gains one of the following deformities from its transformation (roll a 1d4 to randomly determine the deformity).**
>
>
>
>
>  d%** 
>  **Effect** 
>
>
>  1 
>  *Deformed Arm*: One hand can't wield weapons, but the mutant's slam attack deals damage as if it were two size categories larger than its actual size. 
>
>
>  2 
>  *Deformed Leg*: The mutant's base speed is reduced by 10 feet (minimum base speed of 5 feet), but it gains a +4 racial bonus to its CMD. 
>
>
>  3 
>  *Shattered Mind*: The mutant takes a –2 penalty to Intelligence, but gains a +2 racial bonus on Will saves. 
>
>
>  4 
>  *Warped Hide*: The mutant loses its +2 racial bonus to Con, but gains an additional +2 bonus to its natural armor. 
>
>
>
>
> **Abilities:** Increase from the base creature as follows: Str +2, Con +2, Cha –2.
>
> **Skills:** A Mana Wastes mutant gains Climb, Intimidate, Stealth, and Survival as class skills.

**Mechanical encoding:** `changes`: 4
  - `2` → `str`  (untyped)
  - `-2` → `cha`  (untyped)
  - `2` → `con`  (untyped)
  - `2` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Middle Age (Age Category)
*(feat / misc)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `gHAQp2ABmWxcrFAM`

> You suffer a -1 penalty to your physical ability scores, and gain a +1 to your mental ability scores, due to your age category.

**Mechanical encoding:** `changes`: 6 (showing first 5)
  - `-1` → `con`  (untypedPerm)
  - `1` → `int`  (untypedPerm)
  - `1` → `wis`  (untypedPerm)
  - `1` → `cha`  (untypedPerm)
  - `-1` → `dex`  (untypedPerm)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mongrel Giant (Ash, Frost, River, Taiga)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `NtPmk8KGtG7Y3HSF`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** No
>
> While most giants have the physical features of the type of giant of their immediate ancestors, occasionally a giant gives birth to a child who has physical traits associated with one of the other types of giants. Hill giants are the one type of giant whose traits don’t arise in other giants.
>
> "Mongrel giant" is an inherited template that can be added to any creature with the giant subtype (referred to hereafter as the base creature). A mongrel giant retains all the base creature’s statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature’s CR + 1.
>
> **Special Qualities:** A mongrel giant retains all the special attacks, qualities, and abilities of the base creature and gains the following special quality.
>
> *Giant Ancestry (Ex):* A mongrel giant has traits and features of another variety of giant and gains additional abilities based on this ancestry (see Giant Ancestry Traits below).
>
> **Abilities:** Con +2. Most mongrel giants gain an additional ability score increase as determined by their giant ancestry; if an ancestry grants a bonus to Constitution higher than +2, that higher bonus replaces this standard +2 bonus.
>
> #### Giant Ancestry Traits
>
> A mongrel giant gains additional traits based on his ancestry. For spell-like abilities, the mongrel giant’s caster level is equal to the base creature’s HD or the caster level of the base creature’s spell-like abilities, whichever is higher.
>
> Ash Giant: Ash mongrels are deformed and covered in open sores and tumors. They gain immunity to disease and the ash giant’s disease (ash leprosy) ability. Constitution +4.
>
> Cave Giant: Cave mongrels have prominent teeth and gray-green skin. They gain the cave giant’s axe wielder ability and the ferocity universal monster ability. Strength +2.
>
> Cliff Giant: Cliff mongrels have red-brown skin shot through with streaks of shimmering color. They gain tremorsense 30 feet when in contact with unworked stone or natural earth, and they can use the following spell-like abilities once per day: cure moderate wounds, speak with animals, and stone shape. Wisdom +2.
>
> Cloud Giant: Cloud mongrels have fine features and pale blue or white skin. They can use the following spell-like abilities once per day: fog cloud, levitate (self plus 2,000 pounds), and obscuring mist. They also gain the oversized weapon ability (the giant can wield a weapon of one size category larger than his size would normally allow without penalty). Wisdom +2.
>
> Desert Giant: Desert mongrels have roughly textured tan or orange skin. They gain immunity to fire and Martial Weapon Proficiency (scimitar) as a bonus feat. Dexterity +2.
>
> Eclipse Giant: Eclipse mongrels have dark gray skin and appear somewhat overweight. They gain immunity to death effects and can use the following spell-like abilities once per day: daylight or deeper darkness (choose one) and heal or harm (choose one). Wisdom +2.
>
> Fire Giant: Fire mongrels have orange hair and red or black skin. They gain the fire subtype (including immunity to fire and vulnerability to cold), and gain Martial Weapon Proficiency (greatsword) as a bonus feat. Strength +2.
>
> Frost Giant: Frost mongrels have light blue skin and dirty yellow hair. They gain the cold subtype (including immunity to cold and vulnerability to fire), and gain Martial Weapon Proficiency (greataxe) as a bonus feat. Constitution +4.
>
> Jungle Giant: Jungle mongrels have brown and green skin that is textured like fibrous plant material or tree bark. They gain immunity to poison and gain the jungle giant’s archery expert ability. Dexterity +2.
>
> Marsh Giant: Marsh mongrels have pale green skin and hairless bodies. They gain a swim speed of 20 feet and can use the following spell-like abilities once per day: augury, bestow curse, and fog cloud. Strength +2.
>
> Moon Giant: Moon giant mongrels have pale gray skin that sparkles faintly in dim light. They gain cold resistance 10 and fire resistance 10, and can use the following spell-like abilities once per day: clairaudience/clairvoyance, dancing lights, and true seeing. Wisdom +2.
>
> Mountain Giant: Mountain mongrels have warty skin. They gain immunity to fear and can use the following spell-like abilities once per day: deeper darkness, dimension door, and invisibility. Strength +2.
>
> Ocean Giant: Ocean mongrels have blue skin. They gain the amphibious special quality, the aquatic subtype, cold resistance 10, and electricity resistance 10. Strength +2.
>
> Plague Giant: Plague mongrels are thin and their skin looks diseased. They gain immunity to disease and can use the following spell-like abilities once per day: contagion, death knell, and wither limb. Wisdom +2.
>
> River Giant: River mongrels have green skin marked with swirling patterns. They gain the hold breath universal monster ability and a +4 racial bonus on Swim checks. Constitution +4.
>
> Rune Giant: Rune giant mongrels are among the rarest of all mongrel giants. They have black skin through which red runes shimmer, almost like faintly glowing tattoos. A rune mongrel’s CR is the same as the base creature’s CR + 2. They gain immunity to cold, electricity, and fire; gain the runes ability that rune giants have; and can use the following spell-like abilities once per day: air walk, charm person, demand, mass charm monster, and suggestion. Strength +6, Constitution +8, Wisdom +4, Charisma +4.
>
> Shadow Giant: Shadow mongrels have dark gray skin. They gain the shadow giant’s militant special ability and darkvision 60 feet. Wisdom +2.
>
> Slag Giant: Slag mongrels have rust-colored skin. They gain fire resistance 10 and the slag giant’s shattering blow ability. Strength +2.
>
> Stone Giant: Stone mongrels have elongated heads and brown or gray skin that resembles rock. They gain the stone giant’s improved rock catching ability, and increase the range of their rock throwing ability by 40 feet. If the base creature doesn’t have rock throwing, it gains that ability with a range increment of 120 feet. Natural armor bonus increases by 2.
>
> Storm Giant: Storm mongrels gain immunity to electricity and the following spell-like abilities usable once per day: call lightning, control weather, and levitate. Strength +2.
>
> Sun Giant: Sun mongrels have golden skin and faintly glowing flame-colored hair. They are immune to fire and blindness, and can use the following spell-like abilities once per day: daylight and flame strike. Wisdom +2.
>
> Taiga Giant: Taiga mongrels have dark gray skin, red hair, and a strong lower jaw. They gain a +4 deflection bonus to their Armor Class from protective spirits and are immune to illusions. Constitution +4.
>
> Tomb Giant: Tomb mongrels have milky-white, hairless flesh. They gain immunity to death effects and paralysis, gain the negative energy affinity defensive ability, and can use control undead once per day as a spell-like ability. Wisdom +2.
>
> Wood Giant: Wood mongrels have pale pink skin and prominent brows. They can use the following spell-like abilities once per day: charm animal, enlarge person (self only), pass without trace, quench, speak with animals, spike growth, and tree shape. Dexterity +2.

**Mechanical encoding:** `changes`: 1
  - `4` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mongrel Giant (Cave, Fire, Marsh, Mountain, Ocean, Slag, Storm)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `RHpVcF3tGmzrbZ9i`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** No
>
> While most giants have the physical features of the type of giant of their immediate ancestors, occasionally a giant gives birth to a child who has physical traits associated with one of the other types of giants. Hill giants are the one type of giant whose traits don’t arise in other giants.
>
> "Mongrel giant" is an inherited template that can be added to any creature with the giant subtype (referred to hereafter as the base creature). A mongrel giant retains all the base creature’s statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature’s CR + 1.
>
> **Special Qualities:** A mongrel giant retains all the special attacks, qualities, and abilities of the base creature and gains the following special quality.
>
> *Giant Ancestry (Ex):* A mongrel giant has traits and features of another variety of giant and gains additional abilities based on this ancestry (see Giant Ancestry Traits below).
>
> **Abilities:** Con +2. Most mongrel giants gain an additional ability score increase as determined by their giant ancestry; if an ancestry grants a bonus to Constitution higher than +2, that higher bonus replaces this standard +2 bonus.
>
> #### Giant Ancestry Traits
>
> A mongrel giant gains additional traits based on his ancestry. For spell-like abilities, the mongrel giant’s caster level is equal to the base creature’s HD or the caster level of the base creature’s spell-like abilities, whichever is higher.
>
> Ash Giant: Ash mongrels are deformed and covered in open sores and tumors. They gain immunity to disease and the ash giant’s disease (ash leprosy) ability. Constitution +4.
>
> Cave Giant: Cave mongrels have prominent teeth and gray-green skin. They gain the cave giant’s axe wielder ability and the ferocity universal monster ability. Strength +2.
>
> Cliff Giant: Cliff mongrels have red-brown skin shot through with streaks of shimmering color. They gain tremorsense 30 feet when in contact with unworked stone or natural earth, and they can use the following spell-like abilities once per day: cure moderate wounds, speak with animals, and stone shape. Wisdom +2.
>
> Cloud Giant: Cloud mongrels have fine features and pale blue or white skin. They can use the following spell-like abilities once per day: fog cloud, levitate (self plus 2,000 pounds), and obscuring mist. They also gain the oversized weapon ability (the giant can wield a weapon of one size category larger than his size would normally allow without penalty). Wisdom +2.
>
> Desert Giant: Desert mongrels have roughly textured tan or orange skin. They gain immunity to fire and Martial Weapon Proficiency (scimitar) as a bonus feat. Dexterity +2.
>
> Eclipse Giant: Eclipse mongrels have dark gray skin and appear somewhat overweight. They gain immunity to death effects and can use the following spell-like abilities once per day: daylight or deeper darkness (choose one) and heal or harm (choose one). Wisdom +2.
>
> Fire Giant: Fire mongrels have orange hair and red or black skin. They gain the fire subtype (including immunity to fire and vulnerability to cold), and gain Martial Weapon Proficiency (greatsword) as a bonus feat. Strength +2.
>
> Frost Giant: Frost mongrels have light blue skin and dirty yellow hair. They gain the cold subtype (including immunity to cold and vulnerability to fire), and gain Martial Weapon Proficiency (greataxe) as a bonus feat. Constitution +4.
>
> Jungle Giant: Jungle mongrels have brown and green skin that is textured like fibrous plant material or tree bark. They gain immunity to poison and gain the jungle giant’s archery expert ability. Dexterity +2.
>
> Marsh Giant: Marsh mongrels have pale green skin and hairless bodies. They gain a swim speed of 20 feet and can use the following spell-like abilities once per day: augury, bestow curse, and fog cloud. Strength +2.
>
> Moon Giant: Moon giant mongrels have pale gray skin that sparkles faintly in dim light. They gain cold resistance 10 and fire resistance 10, and can use the following spell-like abilities once per day: clairaudience/clairvoyance, dancing lights, and true seeing. Wisdom +2.
>
> Mountain Giant: Mountain mongrels have warty skin. They gain immunity to fear and can use the following spell-like abilities once per day: deeper darkness, dimension door, and invisibility. Strength +2.
>
> Ocean Giant: Ocean mongrels have blue skin. They gain the amphibious special quality, the aquatic subtype, cold resistance 10, and electricity resistance 10. Strength +2.
>
> Plague Giant: Plague mongrels are thin and their skin looks diseased. They gain immunity to disease and can use the following spell-like abilities once per day: contagion, death knell, and wither limb. Wisdom +2.
>
> River Giant: River mongrels have green skin marked with swirling patterns. They gain the hold breath universal monster ability and a +4 racial bonus on Swim checks. Constitution +4.
>
> Rune Giant: Rune giant mongrels are among the rarest of all mongrel giants. They have black skin through which red runes shimmer, almost like faintly glowing tattoos. A rune mongrel’s CR is the same as the base creature’s CR + 2. They gain immunity to cold, electricity, and fire; gain the runes ability that rune giants have; and can use the following spell-like abilities once per day: air walk, charm person, demand, mass charm monster, and suggestion. Strength +6, Constitution +8, Wisdom +4, Charisma +4.
>
> Shadow Giant: Shadow mongrels have dark gray skin. They gain the shadow giant’s militant special ability and darkvision 60 feet. Wisdom +2.
>
> Slag Giant: Slag mongrels have rust-colored skin. They gain fire resistance 10 and the slag giant’s shattering blow ability. Strength +2.
>
> Stone Giant: Stone mongrels have elongated heads and brown or gray skin that resembles rock. They gain the stone giant’s improved rock catching ability, and increase the range of their rock throwing ability by 40 feet. If the base creature doesn’t have rock throwing, it gains that ability with a range increment of 120 feet. Natural armor bonus increases by 2.
>
> Storm Giant: Storm mongrels gain immunity to electricity and the following spell-like abilities usable once per day: call lightning, control weather, and levitate. Strength +2.
>
> Sun Giant: Sun mongrels have golden skin and faintly glowing flame-colored hair. They are immune to fire and blindness, and can use the following spell-like abilities once per day: daylight and flame strike. Wisdom +2.
>
> Taiga Giant: Taiga mongrels have dark gray skin, red hair, and a strong lower jaw. They gain a +4 deflection bonus to their Armor Class from protective spirits and are immune to illusions. Constitution +4.
>
> Tomb Giant: Tomb mongrels have milky-white, hairless flesh. They gain immunity to death effects and paralysis, gain the negative energy affinity defensive ability, and can use control undead once per day as a spell-like ability. Wisdom +2.
>
> Wood Giant: Wood mongrels have pale pink skin and prominent brows. They can use the following spell-like abilities once per day: charm animal, enlarge person (self only), pass without trace, quench, speak with animals, spike growth, and tree shape. Dexterity +2.

**Mechanical encoding:** `changes`: 2
  - `2` → `str`  (untyped)
  - `2` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mongrel Giant (Cliff, Cloud, Eclipse, Moon, Plague, Shadow, Sun, Tomb)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `lLfibK8joy58pHaF`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** No
>
> While most giants have the physical features of the type of giant of their immediate ancestors, occasionally a giant gives birth to a child who has physical traits associated with one of the other types of giants. Hill giants are the one type of giant whose traits don’t arise in other giants.
>
> "Mongrel giant" is an inherited template that can be added to any creature with the giant subtype (referred to hereafter as the base creature). A mongrel giant retains all the base creature’s statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature’s CR + 1.
>
> **Special Qualities:** A mongrel giant retains all the special attacks, qualities, and abilities of the base creature and gains the following special quality.
>
> *Giant Ancestry (Ex):* A mongrel giant has traits and features of another variety of giant and gains additional abilities based on this ancestry (see Giant Ancestry Traits below).
>
> **Abilities:** Con +2. Most mongrel giants gain an additional ability score increase as determined by their giant ancestry; if an ancestry grants a bonus to Constitution higher than +2, that higher bonus replaces this standard +2 bonus.
>
> #### Giant Ancestry Traits
>
> A mongrel giant gains additional traits based on his ancestry. For spell-like abilities, the mongrel giant’s caster level is equal to the base creature’s HD or the caster level of the base creature’s spell-like abilities, whichever is higher.
>
> Ash Giant: Ash mongrels are deformed and covered in open sores and tumors. They gain immunity to disease and the ash giant’s disease (ash leprosy) ability. Constitution +4.
>
> Cave Giant: Cave mongrels have prominent teeth and gray-green skin. They gain the cave giant’s axe wielder ability and the ferocity universal monster ability. Strength +2.
>
> Cliff Giant: Cliff mongrels have red-brown skin shot through with streaks of shimmering color. They gain tremorsense 30 feet when in contact with unworked stone or natural earth, and they can use the following spell-like abilities once per day: cure moderate wounds, speak with animals, and stone shape. Wisdom +2.
>
> Cloud Giant: Cloud mongrels have fine features and pale blue or white skin. They can use the following spell-like abilities once per day: fog cloud, levitate (self plus 2,000 pounds), and obscuring mist. They also gain the oversized weapon ability (the giant can wield a weapon of one size category larger than his size would normally allow without penalty). Wisdom +2.
>
> Desert Giant: Desert mongrels have roughly textured tan or orange skin. They gain immunity to fire and Martial Weapon Proficiency (scimitar) as a bonus feat. Dexterity +2.
>
> Eclipse Giant: Eclipse mongrels have dark gray skin and appear somewhat overweight. They gain immunity to death effects and can use the following spell-like abilities once per day: daylight or deeper darkness (choose one) and heal or harm (choose one). Wisdom +2.
>
> Fire Giant: Fire mongrels have orange hair and red or black skin. They gain the fire subtype (including immunity to fire and vulnerability to cold), and gain Martial Weapon Proficiency (greatsword) as a bonus feat. Strength +2.
>
> Frost Giant: Frost mongrels have light blue skin and dirty yellow hair. They gain the cold subtype (including immunity to cold and vulnerability to fire), and gain Martial Weapon Proficiency (greataxe) as a bonus feat. Constitution +4.
>
> Jungle Giant: Jungle mongrels have brown and green skin that is textured like fibrous plant material or tree bark. They gain immunity to poison and gain the jungle giant’s archery expert ability. Dexterity +2.
>
> Marsh Giant: Marsh mongrels have pale green skin and hairless bodies. They gain a swim speed of 20 feet and can use the following spell-like abilities once per day: augury, bestow curse, and fog cloud. Strength +2.
>
> Moon Giant: Moon giant mongrels have pale gray skin that sparkles faintly in dim light. They gain cold resistance 10 and fire resistance 10, and can use the following spell-like abilities once per day: clairaudience/clairvoyance, dancing lights, and true seeing. Wisdom +2.
>
> Mountain Giant: Mountain mongrels have warty skin. They gain immunity to fear and can use the following spell-like abilities once per day: deeper darkness, dimension door, and invisibility. Strength +2.
>
> Ocean Giant: Ocean mongrels have blue skin. They gain the amphibious special quality, the aquatic subtype, cold resistance 10, and electricity resistance 10. Strength +2.
>
> Plague Giant: Plague mongrels are thin and their skin looks diseased. They gain immunity to disease and can use the following spell-like abilities once per day: contagion, death knell, and wither limb. Wisdom +2.
>
> River Giant: River mongrels have green skin marked with swirling patterns. They gain the hold breath universal monster ability and a +4 racial bonus on Swim checks. Constitution +4.
>
> Rune Giant: Rune giant mongrels are among the rarest of all mongrel giants. They have black skin through which red runes shimmer, almost like faintly glowing tattoos. A rune mongrel’s CR is the same as the base creature’s CR + 2. They gain immunity to cold, electricity, and fire; gain the runes ability that rune giants have; and can use the following spell-like abilities once per day: air walk, charm person, demand, mass charm monster, and suggestion. Strength +6, Constitution +8, Wisdom +4, Charisma +4.
>
> Shadow Giant: Shadow mongrels have dark gray skin. They gain the shadow giant’s militant special ability and darkvision 60 feet. Wisdom +2.
>
> Slag Giant: Slag mongrels have rust-colored skin. They gain fire resistance 10 and the slag giant’s shattering blow ability. Strength +2.
>
> Stone Giant: Stone mongrels have elongated heads and brown or gray skin that resembles rock. They gain the stone giant’s improved rock catching ability, and increase the range of their rock throwing ability by 40 feet. If the base creature doesn’t have rock throwing, it gains that ability with a range increment of 120 feet. Natural armor bonus increases by 2.
>
> Storm Giant: Storm mongrels gain immunity to electricity and the following spell-like abilities usable once per day: call lightning, control weather, and levitate. Strength +2.
>
> Sun Giant: Sun mongrels have golden skin and faintly glowing flame-colored hair. They are immune to fire and blindness, and can use the following spell-like abilities once per day: daylight and flame strike. Wisdom +2.
>
> Taiga Giant: Taiga mongrels have dark gray skin, red hair, and a strong lower jaw. They gain a +4 deflection bonus to their Armor Class from protective spirits and are immune to illusions. Constitution +4.
>
> Tomb Giant: Tomb mongrels have milky-white, hairless flesh. They gain immunity to death effects and paralysis, gain the negative energy affinity defensive ability, and can use control undead once per day as a spell-like ability. Wisdom +2.
>
> Wood Giant: Wood mongrels have pale pink skin and prominent brows. They can use the following spell-like abilities once per day: charm animal, enlarge person (self only), pass without trace, quench, speak with animals, spike growth, and tree shape. Dexterity +2.

**Mechanical encoding:** `changes`: 2
  - `2` → `wis`  (untyped)
  - `2` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mongrel Giant (Desert, Jungle, Wood)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `7Vbnueieo9aNwBCt`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** No
>
> While most giants have the physical features of the type of giant of their immediate ancestors, occasionally a giant gives birth to a child who has physical traits associated with one of the other types of giants. Hill giants are the one type of giant whose traits don’t arise in other giants.
>
> "Mongrel giant" is an inherited template that can be added to any creature with the giant subtype (referred to hereafter as the base creature). A mongrel giant retains all the base creature’s statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature’s CR + 1.
>
> **Special Qualities:** A mongrel giant retains all the special attacks, qualities, and abilities of the base creature and gains the following special quality.
>
> *Giant Ancestry (Ex):* A mongrel giant has traits and features of another variety of giant and gains additional abilities based on this ancestry (see Giant Ancestry Traits below).
>
> **Abilities:** Con +2. Most mongrel giants gain an additional ability score increase as determined by their giant ancestry; if an ancestry grants a bonus to Constitution higher than +2, that higher bonus replaces this standard +2 bonus.
>
> #### Giant Ancestry Traits
>
> A mongrel giant gains additional traits based on his ancestry. For spell-like abilities, the mongrel giant’s caster level is equal to the base creature’s HD or the caster level of the base creature’s spell-like abilities, whichever is higher.
>
> Ash Giant: Ash mongrels are deformed and covered in open sores and tumors. They gain immunity to disease and the ash giant’s disease (ash leprosy) ability. Constitution +4.
>
> Cave Giant: Cave mongrels have prominent teeth and gray-green skin. They gain the cave giant’s axe wielder ability and the ferocity universal monster ability. Strength +2.
>
> Cliff Giant: Cliff mongrels have red-brown skin shot through with streaks of shimmering color. They gain tremorsense 30 feet when in contact with unworked stone or natural earth, and they can use the following spell-like abilities once per day: cure moderate wounds, speak with animals, and stone shape. Wisdom +2.
>
> Cloud Giant: Cloud mongrels have fine features and pale blue or white skin. They can use the following spell-like abilities once per day: fog cloud, levitate (self plus 2,000 pounds), and obscuring mist. They also gain the oversized weapon ability (the giant can wield a weapon of one size category larger than his size would normally allow without penalty). Wisdom +2.
>
> Desert Giant: Desert mongrels have roughly textured tan or orange skin. They gain immunity to fire and Martial Weapon Proficiency (scimitar) as a bonus feat. Dexterity +2.
>
> Eclipse Giant: Eclipse mongrels have dark gray skin and appear somewhat overweight. They gain immunity to death effects and can use the following spell-like abilities once per day: daylight or deeper darkness (choose one) and heal or harm (choose one). Wisdom +2.
>
> Fire Giant: Fire mongrels have orange hair and red or black skin. They gain the fire subtype (including immunity to fire and vulnerability to cold), and gain Martial Weapon Proficiency (greatsword) as a bonus feat. Strength +2.
>
> Frost Giant: Frost mongrels have light blue skin and dirty yellow hair. They gain the cold subtype (including immunity to cold and vulnerability to fire), and gain Martial Weapon Proficiency (greataxe) as a bonus feat. Constitution +4.
>
> Jungle Giant: Jungle mongrels have brown and green skin that is textured like fibrous plant material or tree bark. They gain immunity to poison and gain the jungle giant’s archery expert ability. Dexterity +2.
>
> Marsh Giant: Marsh mongrels have pale green skin and hairless bodies. They gain a swim speed of 20 feet and can use the following spell-like abilities once per day: augury, bestow curse, and fog cloud. Strength +2.
>
> Moon Giant: Moon giant mongrels have pale gray skin that sparkles faintly in dim light. They gain cold resistance 10 and fire resistance 10, and can use the following spell-like abilities once per day: clairaudience/clairvoyance, dancing lights, and true seeing. Wisdom +2.
>
> Mountain Giant: Mountain mongrels have warty skin. They gain immunity to fear and can use the following spell-like abilities once per day: deeper darkness, dimension door, and invisibility. Strength +2.
>
> Ocean Giant: Ocean mongrels have blue skin. They gain the amphibious special quality, the aquatic subtype, cold resistance 10, and electricity resistance 10. Strength +2.
>
> Plague Giant: Plague mongrels are thin and their skin looks diseased. They gain immunity to disease and can use the following spell-like abilities once per day: contagion, death knell, and wither limb. Wisdom +2.
>
> River Giant: River mongrels have green skin marked with swirling patterns. They gain the hold breath universal monster ability and a +4 racial bonus on Swim checks. Constitution +4.
>
> Rune Giant: Rune giant mongrels are among the rarest of all mongrel giants. They have black skin through which red runes shimmer, almost like faintly glowing tattoos. A rune mongrel’s CR is the same as the base creature’s CR + 2. They gain immunity to cold, electricity, and fire; gain the runes ability that rune giants have; and can use the following spell-like abilities once per day: air walk, charm person, demand, mass charm monster, and suggestion. Strength +6, Constitution +8, Wisdom +4, Charisma +4.
>
> Shadow Giant: Shadow mongrels have dark gray skin. They gain the shadow giant’s militant special ability and darkvision 60 feet. Wisdom +2.
>
> Slag Giant: Slag mongrels have rust-colored skin. They gain fire resistance 10 and the slag giant’s shattering blow ability. Strength +2.
>
> Stone Giant: Stone mongrels have elongated heads and brown or gray skin that resembles rock. They gain the stone giant’s improved rock catching ability, and increase the range of their rock throwing ability by 40 feet. If the base creature doesn’t have rock throwing, it gains that ability with a range increment of 120 feet. Natural armor bonus increases by 2.
>
> Storm Giant: Storm mongrels gain immunity to electricity and the following spell-like abilities usable once per day: call lightning, control weather, and levitate. Strength +2.
>
> Sun Giant: Sun mongrels have golden skin and faintly glowing flame-colored hair. They are immune to fire and blindness, and can use the following spell-like abilities once per day: daylight and flame strike. Wisdom +2.
>
> Taiga Giant: Taiga mongrels have dark gray skin, red hair, and a strong lower jaw. They gain a +4 deflection bonus to their Armor Class from protective spirits and are immune to illusions. Constitution +4.
>
> Tomb Giant: Tomb mongrels have milky-white, hairless flesh. They gain immunity to death effects and paralysis, gain the negative energy affinity defensive ability, and can use control undead once per day as a spell-like ability. Wisdom +2.
>
> Wood Giant: Wood mongrels have pale pink skin and prominent brows. They can use the following spell-like abilities once per day: charm animal, enlarge person (self only), pass without trace, quench, speak with animals, spike growth, and tree shape. Dexterity +2.

**Mechanical encoding:** `changes`: 2
  - `2` → `dex`  (untyped)
  - `2` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mongrel Giant (Rune)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `xOO0VWAVs2cnrYW0`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** No
>
> While most giants have the physical features of the type of giant of their immediate ancestors, occasionally a giant gives birth to a child who has physical traits associated with one of the other types of giants. Hill giants are the one type of giant whose traits don’t arise in other giants.
>
> "Mongrel giant" is an inherited template that can be added to any creature with the giant subtype (referred to hereafter as the base creature). A mongrel giant retains all the base creature’s statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature’s CR + 1.
>
> **Special Qualities:** A mongrel giant retains all the special attacks, qualities, and abilities of the base creature and gains the following special quality.
>
> *Giant Ancestry (Ex):* A mongrel giant has traits and features of another variety of giant and gains additional abilities based on this ancestry (see Giant Ancestry Traits below).
>
> **Abilities:** Con +2. Most mongrel giants gain an additional ability score increase as determined by their giant ancestry; if an ancestry grants a bonus to Constitution higher than +2, that higher bonus replaces this standard +2 bonus.
>
> #### Giant Ancestry Traits
>
> A mongrel giant gains additional traits based on his ancestry. For spell-like abilities, the mongrel giant’s caster level is equal to the base creature’s HD or the caster level of the base creature’s spell-like abilities, whichever is higher.
>
> Ash Giant: Ash mongrels are deformed and covered in open sores and tumors. They gain immunity to disease and the ash giant’s disease (ash leprosy) ability. Constitution +4.
>
> Cave Giant: Cave mongrels have prominent teeth and gray-green skin. They gain the cave giant’s axe wielder ability and the ferocity universal monster ability. Strength +2.
>
> Cliff Giant: Cliff mongrels have red-brown skin shot through with streaks of shimmering color. They gain tremorsense 30 feet when in contact with unworked stone or natural earth, and they can use the following spell-like abilities once per day: cure moderate wounds, speak with animals, and stone shape. Wisdom +2.
>
> Cloud Giant: Cloud mongrels have fine features and pale blue or white skin. They can use the following spell-like abilities once per day: fog cloud, levitate (self plus 2,000 pounds), and obscuring mist. They also gain the oversized weapon ability (the giant can wield a weapon of one size category larger than his size would normally allow without penalty). Wisdom +2.
>
> Desert Giant: Desert mongrels have roughly textured tan or orange skin. They gain immunity to fire and Martial Weapon Proficiency (scimitar) as a bonus feat. Dexterity +2.
>
> Eclipse Giant: Eclipse mongrels have dark gray skin and appear somewhat overweight. They gain immunity to death effects and can use the following spell-like abilities once per day: daylight or deeper darkness (choose one) and heal or harm (choose one). Wisdom +2.
>
> Fire Giant: Fire mongrels have orange hair and red or black skin. They gain the fire subtype (including immunity to fire and vulnerability to cold), and gain Martial Weapon Proficiency (greatsword) as a bonus feat. Strength +2.
>
> Frost Giant: Frost mongrels have light blue skin and dirty yellow hair. They gain the cold subtype (including immunity to cold and vulnerability to fire), and gain Martial Weapon Proficiency (greataxe) as a bonus feat. Constitution +4.
>
> Jungle Giant: Jungle mongrels have brown and green skin that is textured like fibrous plant material or tree bark. They gain immunity to poison and gain the jungle giant’s archery expert ability. Dexterity +2.
>
> Marsh Giant: Marsh mongrels have pale green skin and hairless bodies. They gain a swim speed of 20 feet and can use the following spell-like abilities once per day: augury, bestow curse, and fog cloud. Strength +2.
>
> Moon Giant: Moon giant mongrels have pale gray skin that sparkles faintly in dim light. They gain cold resistance 10 and fire resistance 10, and can use the following spell-like abilities once per day: clairaudience/clairvoyance, dancing lights, and true seeing. Wisdom +2.
>
> Mountain Giant: Mountain mongrels have warty skin. They gain immunity to fear and can use the following spell-like abilities once per day: deeper darkness, dimension door, and invisibility. Strength +2.
>
> Ocean Giant: Ocean mongrels have blue skin. They gain the amphibious special quality, the aquatic subtype, cold resistance 10, and electricity resistance 10. Strength +2.
>
> Plague Giant: Plague mongrels are thin and their skin looks diseased. They gain immunity to disease and can use the following spell-like abilities once per day: contagion, death knell, and wither limb. Wisdom +2.
>
> River Giant: River mongrels have green skin marked with swirling patterns. They gain the hold breath universal monster ability and a +4 racial bonus on Swim checks. Constitution +4.
>
> Rune Giant: Rune giant mongrels are among the rarest of all mongrel giants. They have black skin through which red runes shimmer, almost like faintly glowing tattoos. A rune mongrel’s CR is the same as the base creature’s CR + 2. They gain immunity to cold, electricity, and fire; gain the runes ability that rune giants have; and can use the following spell-like abilities once per day: air walk, charm person, demand, mass charm monster, and suggestion. Strength +6, Constitution +8, Wisdom +4, Charisma +4.
>
> Shadow Giant: Shadow mongrels have dark gray skin. They gain the shadow giant’s militant special ability and darkvision 60 feet. Wisdom +2.
>
> Slag Giant: Slag mongrels have rust-colored skin. They gain fire resistance 10 and the slag giant’s shattering blow ability. Strength +2.
>
> Stone Giant: Stone mongrels have elongated heads and brown or gray skin that resembles rock. They gain the stone giant’s improved rock catching ability, and increase the range of their rock throwing ability by 40 feet. If the base creature doesn’t have rock throwing, it gains that ability with a range increment of 120 feet. Natural armor bonus increases by 2.
>
> Storm Giant: Storm mongrels gain immunity to electricity and the following spell-like abilities usable once per day: call lightning, control weather, and levitate. Strength +2.
>
> Sun Giant: Sun mongrels have golden skin and faintly glowing flame-colored hair. They are immune to fire and blindness, and can use the following spell-like abilities once per day: daylight and flame strike. Wisdom +2.
>
> Taiga Giant: Taiga mongrels have dark gray skin, red hair, and a strong lower jaw. They gain a +4 deflection bonus to their Armor Class from protective spirits and are immune to illusions. Constitution +4.
>
> Tomb Giant: Tomb mongrels have milky-white, hairless flesh. They gain immunity to death effects and paralysis, gain the negative energy affinity defensive ability, and can use control undead once per day as a spell-like ability. Wisdom +2.
>
> Wood Giant: Wood mongrels have pale pink skin and prominent brows. They can use the following spell-like abilities once per day: charm animal, enlarge person (self only), pass without trace, quench, speak with animals, spike growth, and tree shape. Dexterity +2.

**Mechanical encoding:** `changes`: 4
  - `4` → `cha`  (untyped)
  - `4` → `wis`  (untyped)
  - `6` → `str`  (untyped)
  - `8` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mongrel Giant (Stone)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `wUosWb4K2f4nvRYj`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** No
>
> While most giants have the physical features of the type of giant of their immediate ancestors, occasionally a giant gives birth to a child who has physical traits associated with one of the other types of giants. Hill giants are the one type of giant whose traits don’t arise in other giants.
>
> "Mongrel giant" is an inherited template that can be added to any creature with the giant subtype (referred to hereafter as the base creature). A mongrel giant retains all the base creature’s statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature’s CR + 1.
>
> **Special Qualities:** A mongrel giant retains all the special attacks, qualities, and abilities of the base creature and gains the following special quality.
>
> *Giant Ancestry (Ex):* A mongrel giant has traits and features of another variety of giant and gains additional abilities based on this ancestry (see Giant Ancestry Traits below).
>
> **Abilities:** Con +2. Most mongrel giants gain an additional ability score increase as determined by their giant ancestry; if an ancestry grants a bonus to Constitution higher than +2, that higher bonus replaces this standard +2 bonus.
>
> #### Giant Ancestry Traits
>
> A mongrel giant gains additional traits based on his ancestry. For spell-like abilities, the mongrel giant’s caster level is equal to the base creature’s HD or the caster level of the base creature’s spell-like abilities, whichever is higher.
>
> Ash Giant: Ash mongrels are deformed and covered in open sores and tumors. They gain immunity to disease and the ash giant’s disease (ash leprosy) ability. Constitution +4.
>
> Cave Giant: Cave mongrels have prominent teeth and gray-green skin. They gain the cave giant’s axe wielder ability and the ferocity universal monster ability. Strength +2.
>
> Cliff Giant: Cliff mongrels have red-brown skin shot through with streaks of shimmering color. They gain tremorsense 30 feet when in contact with unworked stone or natural earth, and they can use the following spell-like abilities once per day: cure moderate wounds, speak with animals, and stone shape. Wisdom +2.
>
> Cloud Giant: Cloud mongrels have fine features and pale blue or white skin. They can use the following spell-like abilities once per day: fog cloud, levitate (self plus 2,000 pounds), and obscuring mist. They also gain the oversized weapon ability (the giant can wield a weapon of one size category larger than his size would normally allow without penalty). Wisdom +2.
>
> Desert Giant: Desert mongrels have roughly textured tan or orange skin. They gain immunity to fire and Martial Weapon Proficiency (scimitar) as a bonus feat. Dexterity +2.
>
> Eclipse Giant: Eclipse mongrels have dark gray skin and appear somewhat overweight. They gain immunity to death effects and can use the following spell-like abilities once per day: daylight or deeper darkness (choose one) and heal or harm (choose one). Wisdom +2.
>
> Fire Giant: Fire mongrels have orange hair and red or black skin. They gain the fire subtype (including immunity to fire and vulnerability to cold), and gain Martial Weapon Proficiency (greatsword) as a bonus feat. Strength +2.
>
> Frost Giant: Frost mongrels have light blue skin and dirty yellow hair. They gain the cold subtype (including immunity to cold and vulnerability to fire), and gain Martial Weapon Proficiency (greataxe) as a bonus feat. Constitution +4.
>
> Jungle Giant: Jungle mongrels have brown and green skin that is textured like fibrous plant material or tree bark. They gain immunity to poison and gain the jungle giant’s archery expert ability. Dexterity +2.
>
> Marsh Giant: Marsh mongrels have pale green skin and hairless bodies. They gain a swim speed of 20 feet and can use the following spell-like abilities once per day: augury, bestow curse, and fog cloud. Strength +2.
>
> Moon Giant: Moon giant mongrels have pale gray skin that sparkles faintly in dim light. They gain cold resistance 10 and fire resistance 10, and can use the following spell-like abilities once per day: clairaudience/clairvoyance, dancing lights, and true seeing. Wisdom +2.
>
> Mountain Giant: Mountain mongrels have warty skin. They gain immunity to fear and can use the following spell-like abilities once per day: deeper darkness, dimension door, and invisibility. Strength +2.
>
> Ocean Giant: Ocean mongrels have blue skin. They gain the amphibious special quality, the aquatic subtype, cold resistance 10, and electricity resistance 10. Strength +2.
>
> Plague Giant: Plague mongrels are thin and their skin looks diseased. They gain immunity to disease and can use the following spell-like abilities once per day: contagion, death knell, and wither limb. Wisdom +2.
>
> River Giant: River mongrels have green skin marked with swirling patterns. They gain the hold breath universal monster ability and a +4 racial bonus on Swim checks. Constitution +4.
>
> Rune Giant: Rune giant mongrels are among the rarest of all mongrel giants. They have black skin through which red runes shimmer, almost like faintly glowing tattoos. A rune mongrel’s CR is the same as the base creature’s CR + 2. They gain immunity to cold, electricity, and fire; gain the runes ability that rune giants have; and can use the following spell-like abilities once per day: air walk, charm person, demand, mass charm monster, and suggestion. Strength +6, Constitution +8, Wisdom +4, Charisma +4.
>
> Shadow Giant: Shadow mongrels have dark gray skin. They gain the shadow giant’s militant special ability and darkvision 60 feet. Wisdom +2.
>
> Slag Giant: Slag mongrels have rust-colored skin. They gain fire resistance 10 and the slag giant’s shattering blow ability. Strength +2.
>
> Stone Giant: Stone mongrels have elongated heads and brown or gray skin that resembles rock. They gain the stone giant’s improved rock catching ability, and increase the range of their rock throwing ability by 40 feet. If the base creature doesn’t have rock throwing, it gains that ability with a range increment of 120 feet. Natural armor bonus increases by 2.
>
> Storm Giant: Storm mongrels gain immunity to electricity and the following spell-like abilities usable once per day: call lightning, control weather, and levitate. Strength +2.
>
> Sun Giant: Sun mongrels have golden skin and faintly glowing flame-colored hair. They are immune to fire and blindness, and can use the following spell-like abilities once per day: daylight and flame strike. Wisdom +2.
>
> Taiga Giant: Taiga mongrels have dark gray skin, red hair, and a strong lower jaw. They gain a +4 deflection bonus to their Armor Class from protective spirits and are immune to illusions. Constitution +4.
>
> Tomb Giant: Tomb mongrels have milky-white, hairless flesh. They gain immunity to death effects and paralysis, gain the negative energy affinity defensive ability, and can use control undead once per day as a spell-like ability. Wisdom +2.
>
> Wood Giant: Wood mongrels have pale pink skin and prominent brows. They can use the following spell-like abilities once per day: charm animal, enlarge person (self only), pass without trace, quench, speak with animals, spike growth, and tree shape. Dexterity +2.

**Mechanical encoding:** `changes`: 2
  - `2` → `con`  (untyped)
  - `2` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Monk (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 247-248
**Foundry id:** `iwW67ugGGuhJrTHu`

> A monk creature gains extra attacks with unarmed strikes or natural attacks, an increase in damage with those attacks, and defensive abilities. A monk creature's CR increases by 3 if the creature has 10 or more HD. A monk creature must be lawful.
>
> **Quick Rules:** +2 on all rolls based on Dex and Wis; gains the @UUID[Compendium.pf1.feats.Item.2aTFNMs3pW6nUBlr] feat. When the creature makes a full attack with unarmed strikes or natural attacks, it can make an extra attack of the same type (of its choice) with a –5 penalty. If the creature uses unarmed strikes, it deals damage as if it were a monk of a level equal to its HD (maximum 20 HD). A creature with 10 or more HD that uses natural attacks instead increases the damage dealt by all of its natural attacks by one die step. If the creature is wearing no armor, it gains a bonus to AC equal to 2 + its Wis modifier. This bonus to AC increases by 1 for every 4 HD it possesses (to a maximum of +5 at 20 HD). The creature gains @UUID[Compendium.pf1.class-abilities.Item.KQYCRLEdD4bGA5ak] (@UUID[Compendium.pf1.class-abilities.Item.Cc2eFfhJYlClCGEH] if the creature has 10 or more HD).
>
> **Rebuild Rules:** **Defensive Abilities** @UUID[Compendium.pf1.class-abilities.Item.KQYCRLEdD4bGA5ak] (@UUID[Compendium.pf1.class-abilities.Item.Cc2eFfhJYlClCGEH] if the creature has 10 or more HD), and if the creature is wearing no armor, it gains a bonus to AC equal its Wis modifier. This bonus to AC increases by 1 for every 4 HD (to a maximum of +5 at 20 HD); **Special Attacks** when the creature makes a full attack with unarmed strikes or natural attacks, it can make an extra attack of the same type with a –5 penalty. If the creature uses unarmed strikes, it deals damage as if it were a monk with a level equal to its HD (maximum 20 HD). A creature with 10 or more HD that uses natural attacks increases the damage dealt by all of its natural attacks by one die step instead; **Ability Scores** +4 Dexterity and Wisdom; **Feats** @UUID[Compendium.pf1.feats.Item.2aTFNMs3pW6nUBlr].

**Mechanical encoding:** `changes`: 8 (showing first 5)
  - `2` → `dexSkills`  (untyped)
  - `2` → `ref`  (untyped)
  - `2` → `dexChecks`  (untyped)
  - `2` → `wisChecks`  (untyped)
  - `@abilities.wis.mod + (2 + floor(@attributes.hd.total / 4))` → `ac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Monk (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 247-248
**Foundry id:** `BI0MvUb9zxGT8Nd9`

> A monk creature gains extra attacks with unarmed strikes or natural attacks, an increase in damage with those attacks, and defensive abilities. A monk creature's CR increases by 3 if the creature has 10 or more HD. A monk creature must be lawful.
>
> **Quick Rules:** +2 on all rolls based on Dex and Wis; gains the @UUID[Compendium.pf1.feats.Item.2aTFNMs3pW6nUBlr] feat. When the creature makes a full attack with unarmed strikes or natural attacks, it can make an extra attack of the same type (of its choice) with a –5 penalty. If the creature uses unarmed strikes, it deals damage as if it were a monk of a level equal to its HD (maximum 20 HD). A creature with 10 or more HD that uses natural attacks instead increases the damage dealt by all of its natural attacks by one die step. If the creature is wearing no armor, it gains a bonus to AC equal to 2 + its Wis modifier. This bonus to AC increases by 1 for every 4 HD it possesses (to a maximum of +5 at 20 HD). The creature gains @UUID[Compendium.pf1.class-abilities.Item.KQYCRLEdD4bGA5ak] (@UUID[Compendium.pf1.class-abilities.Item.Cc2eFfhJYlClCGEH] if the creature has 10 or more HD).
>
> **Rebuild Rules:** **Defensive Abilities** @UUID[Compendium.pf1.class-abilities.Item.KQYCRLEdD4bGA5ak] (@UUID[Compendium.pf1.class-abilities.Item.Cc2eFfhJYlClCGEH] if the creature has 10 or more HD), and if the creature is wearing no armor, it gains a bonus to AC equal its Wis modifier. This bonus to AC increases by 1 for every 4 HD (to a maximum of +5 at 20 HD); **Special Attacks** when the creature makes a full attack with unarmed strikes or natural attacks, it can make an extra attack of the same type with a –5 penalty. If the creature uses unarmed strikes, it deals damage as if it were a monk with a level equal to its HD (maximum 20 HD). A creature with 10 or more HD that uses natural attacks increases the damage dealt by all of its natural attacks by one die step instead; **Ability Scores** +4 Dexterity and Wisdom; **Feats** @UUID[Compendium.pf1.feats.Item.2aTFNMs3pW6nUBlr].

**Mechanical encoding:** `changes`: 4
  - `4` → `wis`  (untyped)
  - `4` → `dex`  (untyped)
  - `1` → `bonusFeats`  (untyped)
  - `@abilities.wis.mod + (2 + floor(@attributes.hd.total / 4))` → `ac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mummified Animal
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `Y9xguBsk7keAdj7T`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> When explorers find tombs housing the mummified remains of important and powerful beings, they often find those mummies accompanied by animals—ones that the interred found significant or that represented their ideals in life. Some of these mummified animals were created and placed in the tombs as guardians. Below are common examples of mummified animals, as well as the mummified animal template.
>
> "Mummified animal" is an acquired template that can be added to a creature of the animal type. A mummified animal uses all the base creature’s statistics and special abilities except as noted here.
>
> **Challenge Rating:** HD 4 or fewer, as base creature; HD 5 to 10, as base creature +1; HD 11 or more, as base creature +2.
>
> **Alignment:** Neutral evil.
>
> **Type:** The creature’s type changes to undead. Do not recalculate BAB, saves, or skills.
>
> **Senses:** A mummified animal gains darkvision 60 ft.
>
> **Defensive Abilities:** A mummified animal gains damage reduction based on its Hit Dice: one with 5 or fewer Hit Dice gains DR 2/—, one with 6–10 Hit Dice gains DR 5/—, and one with 11–20 Hit Dice gains DR 10/—.
>
> **Speed:** Winged mummified animals can still fly, but their maneuverability drops to clumsy. Retain all other movement types.
>
> **Special Attacks:** A mummified animal retains all special attacks except those dependent on a living body to function, such as a snake’s poison or a skunk’s revolting musk. A mummified animal also gains the following special attack.
>
> *Servant’s Curse (Su): *Once per day, a mummified animal can touch a creature or hit a creature with one of its natural attacks to deliver a curse. Any living creature struck by this attack must succeed at a Will save or take 1d3 points of Dex and Wis damage. The save DC is equal to 10 + 1/2 the mummified animal’s Hit Dice + the mummified animal’s Charisma modifier.
>
> **Abilities:** A mummified animal loses its Constitution score, and its Charisma score becomes 14.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mummified Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 197
**Foundry id:** `lLsRXE3PooNQvEBX`

> Many ancient cultures mummify their dead, preserving the bodies of the deceased through lengthy and complex funerary and embalming processes. While the vast majority of these corpses are mummified simply to preserve the bodies in the tombs where they are interred, some are mummified with the help of magic to live on after death as mummified creatures. A mummified creature appears much as other mummies do—a dusty corpse, desiccated and withered, swathed in a funeral shroud of linen wrappings adorned with hieroglyphs—but a spark of malign intelligence gleams in its unliving eyes.
>
> Mummified creatures differ from the standard mummy presented in the Pathfinder RPG Bestiary with regard to how and why they are created. Most standard mummies are created as simple tomb guardians; they gain abilities such as an aura of despair and mummy rot, but they usually lose their free will, much of their intelligence, and the abilities they possessed in life. A mummified creature, on the other hand, retains its intelligence, memories, and many of its other abilities. A mummified creature does not spread the curse of mummy rot, nor does the sight of it paralyze the living with fear, but its touch can reduce a living creature to dust and its very presence is frightening. Though slow and clumsy in undeath, a mummified creature is nonetheless capable of surprising bursts of speed and ferocity. Because of its creation process, however, a mummified creature is susceptible to energy damage, though determining an individual mummified creature's vulnerability is not always easy.
>
> Many mummified creatures are created to guard the tombs of important figures, but some powerful beings—rulers, high priests, mighty wizards, or even wealthy aristocrats—arrange to be transformed into mummified creatures upon their deaths. Unwilling to give up their lives and knowledge to the whims of fate, these people bind their souls to the dried husks of their dead bodies, trading oblivion for endless centuries of unlife. The truly wealthy sometimes arrange for their most favored spouses, concubines, servants, or guards to be mummified with them, enabling them to hold court in dusty tombs in an undead mockery of their old lives centuries after they perished.
>
> To create a mummified creature, a corpse must be prepared through embalming, with its internal organs replaced with dried herbs and flowers and its dead skin preserved through the application of sacred oils. Unlike with standard mummies, a mummified creature's brain is not removed from its skull after death. Injected with strange chemicals and tattooed with mystical hieroglyphs, a mummified creature's brain retains the base creature's mind and abilities, though the process does result in the loss of some mental faculties. Once this process is complete, the body is wrapped in special purified linens marked with hieroglyphs that grant the mummified creature its new abilities (as well as its weakness). Finally, the creator must cast a create greater undead spell to give the mummified creature its unlife.
>
> "Mummified creature" is an acquired template that can be added to any living corporeal creature (hereafter referred to as the base creature). A mummified creature uses all of the base creature's statistics except as noted here.
>
> **CR:** Same as the base creature +1.
>
> **Alignment:** Any evil.
>
> **Type:** The creature's type changes to undead (augmented). It retains any other subtypes as well, except for alignment subtypes and subtypes that indicate kind. Do not recalculate class HD, BAB, saves, or skill points.
>
> **Senses:** A mummified creature gains darkvision 60 feet.
>
> **Aura:** A mummified creature gains a frightful presence aura with a range of 30 feet and a duration of 1d6 rounds.
>
> **Armor Class:** Natural armor improves by +4.
>
> **Hit Dice:** Change all racial Hit Dice to d8s. Class Hit Dice are unaffected. As an undead, a mummified creature uses its Charisma modifier to determine bonus hit points (instead of Constitution).
>
> **Defensive Abilities:** A mummified creature gains DR 5/— and the defensive abilities granted by the undead type.
>
> **Weaknesses:** The mummification process leaves a mummified creature vulnerable to a single energy type. Choose or determine randomly from the following list.
>
>
> **[[/r d10]]**
>
>
> **Energy**
>
>
> 1
>
>
> Electricity
>
>
> 2–3
>
>
> Acid
>
>
> 4–7
>
>
> Fire
>
>
> 8–9
>
>
> Cold
>
>
> 10
>
>
> Sonic
>
>
> **As a fail-safe in case of rebellion, a mummified creature is subtly marked during the ritual process with a hieroglyph someplace inconspicuous on its body or wrappings that identifies the particular energy type to which it is vulnerable. A successful @Skill[per;dc=20] check is needed to find the mark, but a successful @Skill[lin;dc=25] check is still required to decipher the hieroglyph's meaning.
>
> Speed:** Decrease all speeds by 10 feet (to a minimum of 5 feet). If the base creature has a flight speed, its maneuverability changes to clumsy.
>
> **Attacks:** The mummification process hardens the mummified creature's bones to a stone-like density, granting the mummified creature a powerful slam attack if the base creature has no other natural attacks. This slam attack deals damage based on the mummified creature's size (Bestiary 302), treating the creature as if it were one size category larger.
>
> **Special Attacks:** A mummified creature gains the following special attacks.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.CEsXikv4dxo03vFK inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.ZnmqBjh69PUHd8Uf inline=true]
>
> **Abilities:** Str +4, Int –2 (minimum 1). As an undead creature, a mummified creature has no Constitution score.
>
> **Feats:** A mummified creature gains Toughness as a bonus feat, and Improved Natural Attack as a bonus feat for each of the base creature's natural attacks.
>
> **Skills:** A mummified creature gains a +4 racial bonus on Stealth checks.

**Mechanical encoding:** `changes`: 10 (showing first 5)
  - `-2` → `int`  (untyped)
  - `4` → `nac`  (untyped)
  - `4` → `skill.ste`  (racial)
  - `2` → `bonusFeats`  (untyped)
  - `-(10 - max(0, 5 - (@attributes.speed.fly.base - 10)))` → `flySpeed`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mummy Lord
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1133 (PZO1133) p. 176-177
**Foundry id:** `GSHBFW0jtaRf5Kjv`

> Many cultures practice the sacred art of mummification, though the sinister magical techniques used to imbue corpses with undead vitality are far less widespread. In certain ancient lands, such blasphemous techniques have been refined through centuries of ceremony and countless deaths, giving rise to mummies of terrible power. On rare occasions, if the deceased was of great rank and exceeding malevolence, he might undergo such elaborate rituals, rising from his tomb as a fearful mummy lord. Similarly, a ruler known for his malice or who died in a moment of great rage might spontaneously arise as such a vengeful despot. Regardless of the exact circumstances of his resurrection, a mummy lord retains the abilities he had in life, becoming a creature consumed by the desire to restore his rule and dominate both the living and dead.
>
> "Mummy lord" is an acquired template that can be added to any living corporeal creature (referred to hereafter as the base creature) that has at least 8 Hit Dice. The process of creating a mummy lord requires 50,000 gp worth of rare herbs, oils, and other mummification materials. The mummy lord retains all of the base creature's statistics and special abilities, except as listed below.
>
> **Challenge Rating:** Base creature's CR + 2.
>
> **Alignment:** Any evil alignment.
>
> **Type:** The creature's type changes to undead (augmented). Do not recalculate its base attack bonus, saves, or skill ranks.
>
> **Senses:** A mummy lord gains darkvision with a range of 60 feet.
>
> **Aura:** A mummy lord gains the following aura.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.HVHlePfAvQH8v3LH inline=true]
>
> **Armor Class:** A mummy lord has either a +1 natural armor bonus for every 2 Hit Dice it possesses or the base creature's natural armor bonus, whichever of the two leads to a higher result.
>
> **Hit Dice:** Change the creature's racial Hit Dice to d8s. All Hit Dice derived from class levels remain unchanged. As undead, mummy lords use their Charisma modifiers to determine bonus hit points.
>
> **Defensive Abilities:** A mummy lord gains channel resistance +4, DR 10/—, immunity to cold and electricity (in addition to the immunities granted by its undead traits), and the following defensive ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.JyAo9uRz3QFWyKLz inline=true]
>
> **Attacks:** The mummification process hardens the mummy lord's bones to a stone-like density, granting it a powerful slam attack if the base creature has no other natural attacks. This slam attack deals damage based on the mummy lord's size, treating the creature as if it were one size category larger. Those hit by a mummy lord's slam attack also run the risk of succumbing to insidious mummy rot (see Special Attacks below).
>
> **Special Attacks:** A mummy lord gains the following special attacks. The attacks' save DCs are equal to 10 + 1/2 the mummy lord's Hit Dice + the mummy lord's Charisma modifier unless otherwise noted.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.ZE82qt7AVCZP8dbr inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.dsz4asyww19G7bAA inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.SjZwLarX0B0yhUUT inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.4bUnNnNJyEO6UyuU inline=true]
>
> **Ability Scores:** Strength +8, Charisma +6. As an undead creature, a mummy lord has no Constitution score.
>
> **Skills:** A mummy lord gains a +8 racial bonus on Intimidate, Sense Motive, and Stealth checks. It always treats Climb, Disguise, Fly, Intimidate, Knowledge (arcana), Knowledge (religion), Perception, Sense Motive, Spellcraft, and Stealth as class skills. Otherwise, its skills are the same as those of the base creature.
>
> **Feats**: A mummy lord gains Toughness as a bonus feat.

**Mechanical encoding:** `changes`: 7 (showing first 5)
  - `8` → `skill.sen`  (untyped)
  - `8` → `skill.ste`  (untyped)
  - `if(lte(@ac.natural.total, @attributes.hd.total / 2), floor(@attributes.hd.total / 2))` → `nac`  (untyped)
  - `1` → `bonusFeats`  (untyped)
  - `6` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mutant Goblin
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `F4glao5wCxrNEsw4`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> No description provided.
>
> "Mutant goblin" is an acquired template that can be added to a goblin (referred to hereafter as the base creature). A mutant goblin uses the base creature's statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature + 1.
>
> **Armor Class:** Natural armor bonus increases by 4.
>
> **Mutations:** A mutant goblin gains four of the following mutations, determined randomly when it gains the template. For every 5 Hit Dice it has (5, 10, and so on), it gains another random mutation. (Other possible mutations include tusks, a spiked tail, and gills.)
>
> *Breath Weapon (Su): *The goblin can spew a line of foul acidic blood from its mouth (20-foot line, Reflex DC = 10 + 1/2 Hit Die + its Constitution modifier for half damage, 1d4 points of acid damage per HD, usable every 1d4 rounds). If it has 5 or more HD, the range increases to 30 feet and the damage increases to 1d6 points of acid damage per HD.
>
> *Claws (Ex): *The goblin's hands become claws. It gains a natural claw attack for each hand that deals damage appropriate to its size, and gains the grab ability with its claws.
>
> *Extra Arm (Ex): *The goblin gains an extra arm with a functional hand, as the vestigial arm discovery. If it gains this mutation again, it gains another arm.
>
> *Fast Healing (Ex): *The goblin gains fast healing 1. If it has 5 Hit Dice or more, this increases to fast healing 2. If the creature has 10 HD or more, this increases to fast healing 5.
>
> *Venomous Bite (Ex): *The mutant goblin grows large fangs, gaining a poisonous bite as a natural attack that deals damage appropriate to its size. The poison functions like wyvern poison, except its DC is 10 + 1/2 HD + its Constitution modifier.
>
> *Wings (Ex): *The goblin gains dragonfly wings, granting it a fly speed of 30 feet with clumsy maneuverability.
>
> **Abilities:** Str +4, Int –2.

**Mechanical encoding:** `changes`: 3
  - `4` → `nac`  (untyped)
  - `-2` → `int`  (untyped)
  - `4` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mutant
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1133 (PZO1133) p. 180-181
**Foundry id:** `4pbHKe1aYEcjBEs4`

> When long-term exposure to radiation or bizarre magical fields doesn't result in a creature's death, it might mutate the creature into a twisted version of itself. Some of these mutations can be advantageous, while others are unquestionably a hindrance. Mutants often band together into roving bands of loosely affiliated marauders, traveling the land in search of food, shelter, or whatever else motivates their fractured minds.
>
> "Mutant" is an acquired template that can be added to any living, corporeal creature. A mutant retains the base creature's statistics and special abilities except as noted here.
>
> **Challenge Rating:** Base creature's CR + 1.
>
> **Type:** The creature's type changes to aberration (augmented). Do not recalculate its Hit Dice, base attack bonus, or saves.
>
> **Attacks:** A mutant retains all the natural weapons, manufactured weapon attacks, and weapon and armor proficiencies of the base creature.
>
> **Special Abilities:** A mutant retains any extraordinary and supernatural abilities of the base creature.
>
> **Abilities:** A mutant gains a +4 bonus to two ability scores of its choice and takes a –2 penalty to two ability scores of its choice (These can be selected under the "Changes" tab of this window).
>
> **Skills:** A mutant gains Climb, Intimidate, Knowledge (any one), Perception, Sense Motive, Survival, and Swim as class skills.
>
> **Deformities:** Each mutant has one of the following deformities. It can take a second deformity to gain a mutation as detailed in Mutations. A deformity can't be taken if it wouldn't disadvantage the mutant.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.EFr1vhIFgZUFhEmo inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.A6UQXYB7fk2AF7YG inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.lZW7kBFcP8N9dQrQ inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.gXLtwKKh0mvYcdMo inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.Ng7WnEilFZAhSlq6 inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.rzKpL9UotRN27zPq inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.E4qnwk1TZGx9QsBO inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.Sf6qF1Y4mtdmAgmp inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.w5gjd7H55p62mjMb inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.f32aL8qJWGC7hBMG inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.woBZTw0FkmtXcUqq inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.z5JMJmvUVhcwdGmU inline=true]
>
> **Mutations:** A mutant gains one of the beneficial mutations below when it acquires this template, plus an additional mutation for every 4 Hit Dice it possesses. By taking an extra deformity (see above), a mutant can add an additional mutation. Only the first extra deformity provides this benefit. A mutant that gains additional Hit Dice after acquiring this template does not gain additional mutations.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.KscgG1V5RUdCbbhH inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.jPtoDPAqJrzhMpyk inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.gbSfXmwZjoOBq9K2 inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.1m9Mj5LqXWAuQbES inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.pIAB9ppo769IAnvO inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.wN8gymG8t0p2RPqG inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.eXqZbDT1zut7ihG4 inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.QXXOi5gHDzfyCfMb inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.HBN2iJanfuBQ3mo9 inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.BT0Ka35TvXbVIsnd inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.614MhYJZ0nTGQxY6 inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.vez4ZB6yAPbkvAJa inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.e1nNtvVohIowUCSB inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.tAELNqFfCFjrLhdf inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.kKB3oHzs4FPoQRrp inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.zLRcwOeKt3UfwRul inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.vM3SQ0a4M75Bbxop inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.GIcp4eug70nYUTRC inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.0JDYwOSTyB6wASHK inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.Bo9I3rLVZRxeElJM inline=true]

**Mechanical encoding:** `changes`: 4
  - `-2` → `str`  (untyped)
  - `4` → `str`  (untyped)
  - `4` → `str`  (untyped)
  - `-2` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Nightmare Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 204-205
**Foundry id:** `31gYYBIdKKvV51Vr`

> Nightmare creatures have an unnatural link to the most terrifying parts of the Dimension of Dreams, allowing them to turn others' dreams into nightmares and sow fear even in the waking world. Corrupted by their power, they become evil and use their abilities to torment their enemies and abuse creatures weaker than themselves. Eventually this dream connection corrupts the creature's appearance into a bizarre caricature of its original form.
>
> A nightmare creature uses its ability to control dreams to confuse and frighten its target with horrendous imagery— visions of failure or betrayal and horrific scenes of murder and death. A nightmare creature may even allow the target to think it is in control of the dream or has awakened from a nightmare, only to snatch away that hope and send its target into a downward spiral of misery and self-doubt. The most wicked nightmare creatures tend to become ghosts if slain, returning again and again to haunt their chosen victims.
>
> "Nightmare creature" is an acquired or inherited template that can be added to any creature with Intelligence and Charisma scores of at least 6 (referred to hereafter as the base creature). Most nightmare creatures were once aberrations, fey, humanoids, or outsiders. A nightmare creature uses the base creature's statistics and abilities except as noted here. If the base creature has 10 or more Hit Dice, it instead becomes a nightmare lord (see below).
>
> **CR:** Same as the base creature +1.
>
> **Alignment:** Any evil.
>
> **Type:** If the base creature is an outsider, it gains the evil subtype.
>
> **Senses:** A nightmare creature gains darkvision 120 feet.**Defensive Abilities: A nightmare creature gains DR 5/good or silver and the following defensive abilities.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.SWiSBL5OiQbWcl60 inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.cM2KKcMpvyJxK49U inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.8sYuX0IAxlWe52pY inline=true]
>
> Speed:** Same as the base creature. If the base creature does not have a fly speed, the nightmare creature gains a fly speed of 10 (perfect maneuverability) as a supernatural ability.
>
> **Special Attacks:** A nightmare creature gains several special attacks. Save DCs are equal to 10 + 1/2 the nightmare creature's Hit Dice + its Charisma modifier unless otherwise noted. The nightmare creature's caster level is equal to its total Hit Dice (or the caster level of the base creature's spell-like abilities, whichever is higher).
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.qX4GXcNxcEHMA0zq inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.Q10tRa6OLKYQ7WIi inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.HT9aXJi9lyyPArF5 inline=true]
>
> **Spell-Like Abilities:** A nightmare creature gains the following spell-like abilities: Constant—@UUID[Compendium.pf1.spells.Item.71g6nmvy8qnodwyz]; 3/day—@UUID[Compendium.pf1.spells.Item.xllxylvvqr82o2d5], @UUID[Compendium.pf1.spells.Item.ifcnx1yyw6e7ousm], @UUID[Compendium.pf1.spells.Item.siv3ub7hbmcklf8c], @UUID[Compendium.pf1.spells.Item.zqj5qzyl46af27v0]; 1/day—@UUID[Compendium.pf1.spells.Item.btoow6tyv39443gh].
>
> **Ability Scores:** Dex +4, Int +2, Cha +4.
>
> **Skills:** A nightmare creature gains a +4 racial bonus on Intimidate and Stealth checks.

**Mechanical encoding:** `changes`: 6 (showing first 5)
  - `4` → `skill.ste`  (racial)
  - `4` → `skill.int`  (racial)
  - `4` → `dex`  (untyped)
  - `4` → `cha`  (untyped)
  - `if(@attributes.speed.fly.total, 0, 10)` → `flySpeed`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Nosferatu
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 268-269
**Foundry id:** `APWjD9OEpFnukZm1`

> Nosferatu are savage undead who may be the progenitors of the common, more refined vampires. The curse of the nosferatu lacks the elegance and romance of its modern form, harkening to a forgotten age of verminous hunger and eerie powers. Granted immortal life but not immortal youth, nosferatu are withered, embittered creatures unable to create others of their kind, as they somehow lost that ability long ago.
>
> Their ancient sensibilities still reflect the cruelty of epochs past, and their age-spanning plots are untethered by the modern affliction of morality. Nosferatu resent common vampires (which they call "moroi," an ancient term from a lost language) for their beauty, whereas those vampires scorn the nosferatu as bestial relics of an earlier age, best hidden away in remote ruins so as not to sully the charismatic reputation of "true" vampires.
>
> Because nosferatu can't create spawn, any nosferatu in existence are very old—created long ago in a time before they lost the ability to infect others with their undead curse. Most nosferatu live in isolated places with few visitors, and a nosferatu could be a thousand years old and yet have fewer than a dozen character levels because it lacks sufficient foes to challenge it or the initiative to train itself.
>
> "Nosferatu" is an acquired template that can be added to any living creature with 5 or more Hit Dice (referred to hereafter as the base creature). Most nosferatu were once humanoids, fey, or monstrous humanoids. A nosferatu uses the base creature's stats and abilities except as noted here.
>
> **CR:** Same as the base creature +2.
>
> **Alignment:** Any evil.
>
> **Type:** The creature's type changes to undead (augmented). Do not recalculate class Hit Dice, BAB, or saves.
>
> **Senses:** A nosferatu gains darkvision 60 ft., low-light vision, and scent.
>
> **Armor Class:** Natural armor improves by 8.
>
> **Hit Dice:** Change all racial Hit Dice to d8s. Class Hit Dice are unaffected. As an undead, a nosferatu uses its Charisma modifier to determine its bonus hit points (instead of Constitution).
>
> **Defensive Abilities:** A nosferatu gains channel resistance +4 and DR 5/wood and piercing (this includes all wood-shafted weapons such as arrows, crossbow bolts, spears, and javelins, even if the weapon's actual head is made of another material). It also gains resistance 10 to cold, electricity, and sonic.
>
> A nosferatu gains fast healing 5. If reduced to 0 hit points in combat, a nosferatu assumes its swarm form (see below) and attempts to escape. It must reach its coffin within 1 hour or be utterly destroyed. (In swarm form, it can normally travel up to 5 miles in 1 hour.) Additional damage dealt to a nosferatu forced into swarm form has no effect. Once at rest, the nosferatu is helpless. It regains 1 hit point after 1 hour, then is no longer helpless and resumes healing at the rate of 5 hit points per round.
>
> **Weaknesses:** A nosferatu can't tolerate the strong odor of garlic, and won't enter an area laced with it. Similarly, it recoils from mirrors or strongly presented holy symbols. These things don't harm the nosferatu—they merely keep it at bay. A recoiling nosferatu must stay at least 5 feet away from the mirror or holy symbol and can't touch or make melee attacks against that creature. Holding a nosferatu at bay takes a standard action. After 1 round, a nosferatu can overcome its revulsion of the object and function normally each round it succeeds at a @Save[will;dc=25] save.
>
> A nosferatu cannot enter a private home or dwelling unless invited in by someone with the authority to do so.
>
> Reducing a nosferatu's hit points to 0 incapacitates it but doesn't always destroy it (see fast healing). However, certain attacks can slay nosferatu. Exposing any nosferatu to direct sunlight staggers it on the first round of exposure and destroys it utterly on the second consecutive round of exposure if it does not escape. Each round of immersion in running water deals an amount of damage to a nosferatu equal to one-third of its full normal hit points—a nosferatu reduced to 0 hit points in this manner is destroyed. Driving a wooden stake through a helpless nosferatu's heart instantly slays it (this is a full-round action). However, it returns to life if the stake is removed, unless its head is also severed and anointed with holy water.
>
> **Speed:** Same as the base creature. If the base creature has a swim speed, the nosferatu is not harmed by running water.
>
> **Melee:** A nosferatu gains two claw attacks if the base creature didn't have any (1d4 points of damage for a Small nosferatu, 1d6 points of damage for a Medium one).
>
> **Special Attacks:** A nosferatu gains several special attacks. Its save DCs are equal to 10 + 1/2 the nosferatu's Hit Dice + the nosferatu's Cha modifier unless otherwise noted.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.ikY1FVxTljVTG4TW inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.A1z1J1gYafgERGIp inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.9iBtBhHF1wCuRuVK inline=true]
>
> **Special Qualities:** A nosferatu gains the following.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.m535hEt4n0SZLig6 inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.gLyruUZty3GZ96SM inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.YmPMfKGDgHCuc6XJ inline=true]
>
> **Ability Scores:** Str +2, Dex +4, Int +2, Wis +6, Cha +4. As an undead creature, a nosferatu has no Constitution score.
>
> **Skills:** A nosferatu gains a +8 racial bonus on Perception, Sense Motive, and Stealth checks.
>
> **Feats:** A nosferatu gains Alertness, Improved Initiative, Lightning Reflexes, and Skill Focus (in two different skills) as bonus feats.

**Mechanical encoding:** `changes`: 10 (showing first 5)
  - `4` → `dex`  (untyped)
  - `8` → `nac`  (untyped)
  - `8` → `skill.ste`  (racial)
  - `8` → `skill.per`  (racial)
  - `6` → `wis`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Old (Age Category)
*(feat / misc)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `NtQDu5p8IXfyJnKa`

> You suffer a -3 penalty to your physical ability scores, and gain a +2 to your mental ability scores, due to your age category.

**Mechanical encoding:** `changes`: 6 (showing first 5)
  - `-3` → `con`  (untypedPerm)
  - `2` → `int`  (untypedPerm)
  - `2` → `wis`  (untypedPerm)
  - `2` → `cha`  (untypedPerm)
  - `-3` → `dex`  (untypedPerm)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Osirion Mummy
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `wVpQnwScicfnKl1l`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> The mummification process of ancient Osirion results in a variant mummy. Although the Osirion mummy appears very similar to normal mummies-a desiccated husklike creature, draped in embalming wrap adorned with hieroglyphics-the Osirion mummy differs slightly in ability. Osirion mummies do not spread the curse of mummy rot through touch, nor does the very sight of them give rise to paralysis. They are still, however, resilient killing machines.
>
> "Osirion mummy" is an acquired template that can be added to any living, corporeal creature (hereafter referred to as the base creature). An Osirion mummy uses all of the base creature's statistics except as noted here.
>
> **Size and Type:** The creature's type changes to undead, and it gains the augmented subtype. It retains any other subtypes as well, except for alignment subtypes (such as good). Do not recalculate base attack bonuses, saves, or skill points. Size is unchanged.
>
> **Hit Dice:** Increase all current and future Hit Dice to d12.
>
> **AC:** An Osirion mummy's natural armor bonus increases by +5.
>
> **Defensive Abilities:** An Osirion mummy retains the base creature's defensive abilities and gains damage reduction.
>
> *Damage Reduction (Ex) *An Osirion mummy's body is resilient, providing it with damage reduction 5/-.
>
> **Weaknesses:** An Osirion mummy retains the base creature's weaknesses and gains energy vulnerability.
>
> *Energy vulnerability (Ex)* The mummification process leaves the mummy vulnerable to a single energy type, from which it takes half again as much damage (+50%) as normal. Choose or determine randomly from the following list:
>
>
>
>
>  **d10** 
>  **Energy** 
>
>
>  1-4 
>  Fire 
>
>
>  5-6 
>  Acid 
>
>
>  7-8 
>  Cold 
>
>
>  9 
>  Electricity 
>
>
>  10 
>  Sonic 
>
>
>
>
> As an emergency safeguard, it was common for the necromantic embalmers of ancient Osirion to subtly mark the particular energy type to which the mummy would be vulnerable with a separate hieroglyph someplace inconspicuously on the mummy's body or wrappings. A DC 20 Spot check uncovers the mark, but unless the viewer is capable of comprehending its meaning a DC 20 Decipher Script check is required to unlock its secret.
>
> **Speed:** An Osirion mummy's speeds all decrease by 10 feet (minimum 5 feet). If the base creature has a flight speed its maneuverability class worsenes by one step, to a minimum of clumsy.
>
> **Attack:** An Osirion mummy retains all the attacks of the base creature and also gains a slam attack if it did not already have one. If the base creature can use weapons, the Osirion mummy retains that ability. In addition, all of an Osirion mummy's attacks are treated as magical for the purpose of overcoming damage reduction.
>
> **Damage:** The mummification process hardens the mummy's bones to a stonelike density, granting the mummy a powerful slam attack. The creature's slam attack deals damage according to its size as listed below.
>
>
>
>
>  **Size** 
>  **Damage** 
>
>
>  Fine 
>  1 
>
>
>  Diminutive 
>  1d2 
>
>
>  Tiny 
>  1d3 
>
>
>  Small 
>  1d4 
>
>
>  Medium 
>  1d6 
>
>
>  Large 
>  1d8 
>
>
>  Huge 
>  2d6 
>
>
>  Gargantuan 
>  2d8 
>
>
>  Colossal 
>  4d6 
>
>
>
>
> **Special Attacks:** An Osirion mummy retains the base creature's special attacks and also gains the following.
>
> *Dust Stroke (Su) *A successful natural or slam attack by an Osirion mummy that drops its victim's hit points to below -9 does more than just kill the victim, it also disintegrates the victim's body into a cloud of dust and ash. A raise dead spell cannot bring back the victim, but a resurrection still works.
>
> *Sudden Burst of Vengeance (Su) *Despite its slow lumbering nature, an Osirion mummy is capable of lurching forward to attack with a short but surprising, explosion of speed. Twice per day, as a free action, an Osirion mummy may act as though augmented by a haste spell. The effect lasts for a single round.
>
> **Abilities:** An Osirion mummy's ability scores are modified as follows: Str +4, Int -2 (minimum 1). As an undead creature, an Osmon mummy has no Constitution score.
>
> **Feats:** The creature gains Improved Natural Attack for each natural attack form as a bonus feat. If the creature previously had a slam attack before adding the template. the creature's new slam attack also gains the Improved Natural Attack feat.
>
> **Environment:** Any.
>
> **Challenge Rating:** As base creature +1.
>
> **Alignment:** Usually lawful evil.

**Mechanical encoding:** `changes`: 4
  - `5` → `nac`  (untyped)
  - `-10` → `allSpeeds`  (base)
  - `4` → `str`  (untyped)
  - `-2` → `int`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Paladin (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 248
**Foundry id:** `DxKzgjuvqHZMjKz0`

> paladin creatures can battle evil using smite evil and heal using lay on hands, and they possesses some defensive abilities as well. A paladin creature's CR increases by 3 if the creature has 10 or more HD. A paladin creature must be lawful good.
>
> **Quick Rules:** +2 on all rolls based on Str and Cha; can @UUID[Compendium.pf1.class-abilities.Item.2TsDfK0SKC8IGVx4] once per day (treating its HD as its paladin level for the purposes of damage); can use @UUID[Compendium.pf1.class-abilities.Item.WhE4j0Jc82npdMCP] once per day (healing 1d6 hit points for every 2 HD it possesses instead of using its paladin level); gains @UUID[Compendium.pf1.class-abilities.Item.2YqtYAfLcV7KWkpJ] and @UUID[Compendium.pf1.class-abilities.Item.eYuNS8kf9Z3V6kjO] (if the creature has 10 or more HD, it also gains @UUID[Compendium.pf1.class-abilities.Item.jiBCmy0kP1Uwaz0D]).
>
> **Rebuild Rules:** **Defensive Abilities** @UUID[Compendium.pf1.class-abilities.Item.eYuNS8kf9Z3V6kjO] (if the creature has 10 or more HD, it also gains @UUID[Compendium.pf1.class-abilities.Item.jiBCmy0kP1Uwaz0D]); **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.2TsDfK0SKC8IGVx4] ability once per day (treating its HD as its paladin level for the purposes of damage); **Special Qualities** @UUID[Compendium.pf1.class-abilities.Item.2YqtYAfLcV7KWkpJ] as the paladin class feature, @UUID[Compendium.pf1.class-abilities.Item.WhE4j0Jc82npdMCP] once per day (healing 1d6 hit points for every 2 HD the creature possesses instead of using its paladin level); **Ability Scores** +4 Strength and Charisma.

**Mechanical encoding:** `changes`: 6 (showing first 5)
  - `2` → `chaChecks`  (untyped)
  - `2` → `strSkills`  (untyped)
  - `2` → `wdamage`  (untyped)
  - `2` → `chaSkills`  (untyped)
  - `2` → `strChecks`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Paladin (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 248
**Foundry id:** `Zf0dy41vkqU4fcl7`

> paladin creatures can battle evil using smite evil and heal using lay on hands, and they possesses some defensive abilities as well. A paladin creature's CR increases by 3 if the creature has 10 or more HD. A paladin creature must be lawful good.
>
> **Quick Rules:** +2 on all rolls based on Str and Cha; can @UUID[Compendium.pf1.class-abilities.Item.2TsDfK0SKC8IGVx4] once per day (treating its HD as its paladin level for the purposes of damage); can use @UUID[Compendium.pf1.class-abilities.Item.WhE4j0Jc82npdMCP] once per day (healing 1d6 hit points for every 2 HD it possesses instead of using its paladin level); gains @UUID[Compendium.pf1.class-abilities.Item.2YqtYAfLcV7KWkpJ] and @UUID[Compendium.pf1.class-abilities.Item.eYuNS8kf9Z3V6kjO] (if the creature has 10 or more HD, it also gains @UUID[Compendium.pf1.class-abilities.Item.jiBCmy0kP1Uwaz0D]).
>
> **Rebuild Rules:** **Defensive Abilities** @UUID[Compendium.pf1.class-abilities.Item.eYuNS8kf9Z3V6kjO] (if the creature has 10 or more HD, it also gains @UUID[Compendium.pf1.class-abilities.Item.jiBCmy0kP1Uwaz0D]); **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.2TsDfK0SKC8IGVx4] ability once per day (treating its HD as its paladin level for the purposes of damage); **Special Qualities** @UUID[Compendium.pf1.class-abilities.Item.2YqtYAfLcV7KWkpJ] as the paladin class feature, @UUID[Compendium.pf1.class-abilities.Item.WhE4j0Jc82npdMCP] once per day (healing 1d6 hit points for every 2 HD the creature possesses instead of using its paladin level); **Ability Scores** +4 Strength and Charisma.

**Mechanical encoding:** `changes`: 2
  - `4` → `str`  (untyped)
  - `4` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Pallid Vector
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `uUzjnQRvgITL4zri`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Followers of Urgathoa revere all sicknesses as worldly expressions of her divine will, but none more so than the pallid gift, which opens its victims’ fevered minds to the glory of the Pallid Princess. Creatures that die while afflicted with the disease rise as undead, but some creatures form a symbiotic bond with it and become pallid vectors.
>
> "Pallid vector" is an acquired template that can be added to a corporeal, living creature not immune to disease. A pallid vector retains all the base creature’s statistics and special abilities except as noted.
>
> **CR:** Base creature’s CR + 2.
>
> **Alignment:** Any evil.
>
> **Armor Class:** The creature’s natural armor bonus increases by 3.
>
> **Defensive Abilities:** A pallid vector is treated as undead for the purposes of negative and positive energy, and it gains immunity to disease, exhaustion, fatigue, poison, and stunning. Additionally, it gains the following ability.
>
> *Pale Rebirth (Su): *When a pallid vector dies, it rises as a plague zombie (Pathfinder RPG Bestiary 289) 1 round later. Instead of zombie rot, it spreads pallid gift (see Disease below). Sprinkling holy water on the body (a standard action) before it rises prevents this. A humanoid pallid vector that kills itself ritualistically or dies within a desecrate effect or other area that promotes undeath rises as a more powerful undead instead, as if it had died from pallid gift (see table below).
>
> **Special Attacks:** A pallid vector gains stench (Bestiary 304; 10 rounds) and disease. The DCs are Constitution-based.
>
> *Disease (Su):* All of a pallid vector’s melee attacks, even with manufactured weapons, carry the pallid gift disease. Pallid Gift: melee attacks; save Fort DC = 10 + 1/2 the pallid vector’s Hit Dice + its Con modifier; >onset immediate; frequency 1/day; effect 1d6 Constitution damage and 1d6 Wisdom damage, the infected creature is fatigued, the ability damage can’t be healed, and the fatigue can’t be removed while the creature is infected; cure 2 consecutive saves. A nonhumanoid infected creature that dies rises as a plague zombie in 2d6 hours, and spreads pallid curse instead of zombie rot. A humanoid infected creature that dies rises as an undead according to its HD. Plague zombieGhastWight
>
>
>
>
>  **Hit Dice** 
>  **Monster** 
>
>
>  1-3 
>
>
>
>  4-5 
>
>
>
>  6-7 
>
>
>
>  8+ 
>  Vampire 
>
>
>
>
> **Ability Scores:** Str +2, Con +4, Wis +2.

**Mechanical encoding:** `changes`: 4
  - `2` → `str`  (untyped)
  - `2` → `wis`  (untyped)
  - `3` → `nac`  (untyped)
  - `4` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Penanggalen
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1120 (PZO1120) p. 216-217
**Foundry id:** `3N4wtjtVH8MFA5aI`

> The hideous penanggalen is one of the most horrific vampiric monstrosities. By day, a penanggalen appears to be a normal humanoid, but at night or when provoked, the creature's head rips free from the rest of her body, coils of viscera and entrails dangling from her throat as she launches into the air, seeking blood to sate her unholy thirst.
>
> Unlike most undead, the penanggalen is more akin to the lich in that she willfully abandons both her mortality and morality to become a hideous undead monster. While penanggalens are traditionally female spellcasters, any creature capable of performing the vile ritual of transformation can become one.
>
> Similar to a lich, a creature works toward becoming a penanggalen. More than one such transformation ritual exists, but all require heinous acts that symbolize the casting aside of kindness, benevolence, and any semblance of feelings other than cruelty. Many of these rituals call for the repeated consumption of blood, bile, tears, and other fluids drawn from captured and tortured innocents.
>
> A penanggalen keeps a vat of vinegar in her lair. When returning from a night of feeding, a penanggalen's organs are swollen with blood. In order to fit back into her body, the penanggalen must soak for 1 hour in this vat of vinegar. Once reduced, a penanggalen slides back into her body. If a penanggalen is slain away from her body, the body rapidly deteriorates into foul-smelling grit.
>
> The penanggalen presented above was a witch in life. The witch class is presented in full in the Advanced Player's Guide.
>
> "Penanggalen" is an acquired template that can be added to any living creature with 5 or more Hit Dice (referred to hereafter as the base creature). Most penanggalens were once humanoids or monstrous humanoids and nearly every penanggalen is female. A penanggalen uses the base creature's stats and abilities except as noted here.
>
> **CR:** Same as base creature +1.
>
> **Alignment:** Any evil.
>
> **Type:** The creature's type changes to undead (augmented). Do not recalculate class Hit Dice, BAB, or saves.
>
> **Senses:** A penanggalen gains darkvision 60 ft.
>
> **Armor Class:** Natural armor improves by +6.
>
> **Hit Dice:** Change the base creature's racial HD to d8s. All HD derived from class levels remain unchanged. As undead, a penanggalen uses her Charisma modifier to determine bonus hit points (instead of Constitution).
>
> **Defensive Abilities:** A penanggalen gains channel resistance +4, DR 5/silver and slashing, resistance to cold 10 and fire 10, and all of the defensive abilities granted by the undead type. A penanggalen also gains fast healing 5.
>
> **Weaknesses:** A penanggalen gains light sensitivity. In addition, a penanggalen is staggered while outside of her human body and exposed to direct sunlight.
>
> **Speed:** When a penanggalen is attached to her body, she retains the same base speed as the base creature. When a penanggalen is separated from her body, she has only a fly speed of 60 feet with good maneuverability.
>
> **Melee:** A penanggalen gains a bite attack and a slam attack when she is detached from her body. Damage is standard for attacks of these types for the penanggalen's size. Both natural attacks are treated as magic for the purpose of overcoming damage reduction.
>
> **Special Attacks:** A penanggalen retains all of the base creature's special attacks. She also gains the following additional special attacks. Save DCs are equal to 10 + 1/2 the penanggalen's HD + the penanggalen's Charisma modifier unless otherwise noted.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.XSiJrGbdLmSS58Rf inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.Rk7DNDyGZLvBvEUe inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.k5psPXh04L1bk9iG inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.teLPTDiCre1N1iYM inline=true]
>
> **Ability Scores:** Str +6, Dex +4, Int +2, Wis +2, Cha +4. As an undead creature, a penanggalen has no Constitution score.
>
> **Skills:** A penanggalen gains a +8 racial bonus on Bluff, Fly, Knowledge (arcana), Perception, Sense Motive, and Stealth checks.
>
> **Special Qualities:** A penanggalen gains the following special quality.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.ZMuovlXYwwZkXpzt inline=true]

**Mechanical encoding:** `changes`: 12 (showing first 5)
  - `8` → `skill.blf`  (racial)
  - `2` → `int`  (untyped)
  - `8` → `skill.per`  (racial)
  - `8` → `skill.kar`  (racial)
  - `6` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Petitioner
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1116 (PZO1116) p. 208-209
**Foundry id:** `pftwaky9o6qa4Q1q`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Petitioners are the souls of mortals brought to the Outer Planes after death in order to experience their ultimate punishment, reward, or fate. A petitioner retains fragments of its memories from life, and its appearance depends not only upon the shape it held in life but also upon the nature of the Outer Plane to which it has come. The stat block detailed above presents a typical petitioner formed from the soul of an average human—it does not include any of the plane-specific abilities or features a petitioner gains, and should be modified as appropriate depending on the plane to which the petitioner is assigned.
>
> Creatures who die, become petitioners, and then return to life retain no memories of the time they spent as petitioners in the afterlife. A petitioner who dies is gone forever—its "life force" has either returned to the Positive Energy Plane or, in some cases, provided the energy to trigger the creation of another outsider. Petitioners who please a deity or another powerful outsider can be granted rewards—the most common such reward manifests as a transformation into a different outsider, such as an archon, azata, demon, or devil, depending upon the petitioner’s alignment. In rare cases, a creature can retain its personality from life all the way through its existence as a petitioner and into its third "life" as an outsider, although such events are rare indeed.
>
> "Petitioner" is an acquired template that can be added to any creature whose soul migrates to one of the Outer Planes following its death (henceforth referred to as the base creature). The petitioner uses all of the base creature’s statistics and abilities except as noted below.
>
> **CR:** A petitioner’s CR is 1. In some cases, at the GM’s discretion, particularly large or unusual petitioners with higher than normal ability scores may begin with a higher CR; compare the petitioner’s statistics to the values on Table 1–1 on page 293 to help determine an unusual petitioner’s starting CR.
>
> **Alignment:** A petitioner’s alignment is identical to that of its home plane.
>
> **Size and Type:** The creature’s type changes to outsider. It loses all subtypes. Its size does not change.
>
> **Senses:** Petitioners lose any unusual senses they had, but gain darkvision 60 feet.
>
> **Armor Class:** The petitioner loses all racial bonuses to its Armor Class.
>
> **Hit Dice:** Petitioners lose all racial and class-based Hit Dice and gain 2d10 racial Hit Dice as outsiders.
>
> **Saves:** Petitioners have good Fortitude and Reflex saves; a petitioner’s base saves are Fort +3, Ref +3, Will +0.
>
> **Defensive Abilities:** Petitioners lose all the defensive abilities of the base creature. Petitioners are immune to mind-affecting effects.
>
> **Attacks:** The creature’s BAB is +2, subject to modification for size and Strength. It loses all natural attacks and gains a slam attack as appropriate for a creature of its size.
>
> **Special Attacks:** Petitioners lose all special attacks.
>
> **Abilities:** Same as the base creature.
>
> **Feats:** Petitioners lose all feats. As a 2 HD outsider, a petitioner gains one feat—typically Toughness.
>
> **Skills:** Petitioners lose all skill ranks they possessed as mortals. As a 2 HD outsider, a petitioner has 12 skill ranks it can spend on skills (with a maximum of 2 ranks in any one skill), and gains bonus skill ranks as appropriate for its Intelligence. Unlike most outsiders, petitioners do not gain an additional 4 class skills beyond those available to all outsiders.
>
> **Special Qualities:** Petitioners lose all special qualities, along with all abilities granted by class levels (including increases on saving throws and to HD and BAB).
>
> #### Petitioner Traits
>
> A petitioner gains additional traits based on its home plane.
>
> **Abaddon (Neutral Evil):** The "hunted" have bodies that are identical to what they had in life—these petitioners are doomed to be stalked and eventually consumed by the daemons that lust for souls. A hunted that survives long enough eventually warps and twists into a daemon. The hunted gain DR 5/— and fast healing 1 so that they provide a slightly more robust hunt for their daemonic predators.
>
> **Abyss (Chaotic Evil):** "Larvae" are perhaps the most hideous of petitioners—they appear as pallid, maggot-like creatures with heads similar to those they possessed in life. Larvae that feed long enough on Abyssal filth eventually transform into demons. They have cold, electricity, and fire resistance 10, and instead of a slam attack gain a bite attack as appropriate for their size.
>
> **Elysium (Chaotic Good):** The "chosen" have idealized versions of their mortal bodies. In time, after experiencing the pleasures Elysium has to offer, the chosen become azatas. The chosen gain resistance to cold and fire 10 and a +2 bonus to Charisma.
>
> **Heaven (Lawful Good):** The "elect" appear similar to their mortal forms, save that they possess a golden halo and feathered wings. After spending enough time aiding heavenly tasks, the elect become archons. They gain a fly speed equal to their base speed (average mobility).
>
> **Hell (Lawful Evil):** The "damned" retain their mortal forms, but are heavily scarred by various tortures. Those who endure the torments of Hell long enough may eventually be approved for transformation into devils. The damned gain immunity to fire (but not immunity to the pain caused by fire—whenever one of the damned takes fire damage, it must make a DC 15 Fortitude save to resist being stunned by the pain for 1d4 rounds).
>
> **Limbo (Chaotic Neutral):** The "shapeless" retain their basic forms, but these forms constantly waver and shimmer, as if they were ghosts in peril of dissolving away. After wallowing in the chaos of Limbo for long enough, they can transform into proteans. The shapeless have the incorporeal subtype, an incorporeal touch attack, and all advantages granted by that defensive ability.
>
> **Nirvana (Neutral Good):** The "cleansed" take on the forms of animals that closely approximate their personalities. Upon achieving true enlightenment, they transform into agathions. The cleansed gain cold and sonic resistance 10 and a +2 bonus to Wisdom.
>
> **Purgatory (Neutral):** The "dead" appear as animated skeletons but are not undead—in time, they can earn the right to become aeons. They gain DR 10/bludgeoning and immunity to cold.
>
> **Utopia (Lawful Neutral):** The "remade" retain the same body shape but have milky white skin covered in dense black script, as if some strange scribe had used them for parchment. Upon deciphering the riddles posed by these complex lines of script, one of the remade can enter an axiomite forge to be transformed into an inevitable. The remade are immune to hostile transmutation effects and gain a +2 bonus to Intelligence.

**Mechanical encoding:** `changes`: 1
  - `2` → `bab`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Pickin Ogre
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `gPbMkJvP49tgVSqX`

> **Acquired/Inherited Template** Inherited**Simple Template** Yes**Usable with Summons** No
>
> Ogres with the thicken template have huge, oversized heads and razor-sharp teeth.
>
> **Quick Rules:** –1 to AC, ranged attack rolls, initiative, and Dexterity-based skills; gains a bite attack (1d8).
>
> **Rebuild Rules:** Ability Scores –2 Dexterity; Attacks gains a bite attack (1d8) .

**Mechanical encoding:** `changes`: 1
  - `-2` → `dex`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Plagued Beast
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1133 (PZO1133) p. 194
**Foundry id:** `TC0MAD0u4Dpc9m2T`

> When animals are stricken with demon plague, they may arise as undead and further spread the disease. Some demons and cultists are fond of using plagued horses as mounts.
>
> "Plagued beast" is an acquired template that can be added to a living, corporeal creature with an Intelligence score of 1 or 2. A plagued beast uses all of the creature's statistics and special abilities except as noted here.
>
> **Challenge Rating:** Base creature's CR + 1.
>
> **Alignment:** Neutral evil.
>
> **Type:** The creature's type changes to undead (augmented). It retains all subtypes except alignment subtypes and subtypes that indicate kind. Do not recalculate its saves, BAB, or skill ranks.
>
> **Armor Class:** Increase the base creature's AC by 2.
>
> **Hit Dice:** Change all of the creature's racial Hit Dice to d8s. As undead, plagued beasts use their Charisma modifiers to determine bonus hit points.
>
> **Defensive Abilities:** Plagued beasts gain darkvision 60 feet, channel resistance +2, and DR 5/slashing. They are immune to cold, and gain all of the standard undead traits.
>
> **Melee:** A plagued beast gains a bite attack that deals damage based on the plagued beast's size. If the beast already has a bite attack, the bite's damage increases by one step, as if it had increased one size category.
>
> **Special Attacks:** A plagued beast inflicts demon plague with each successful bite attack (DC = 10 + 1/2 the plagued beast's Hit Dice + the plagued beast's Charisma modifier).
>
> **Ability Scores:** +4 Strength, +2 Dexterity. A plagued beast has a minimum Charisma score of 15—if the base creature's Charisma score is lower, increase it to 15. A plagued beast has no Constitution score; as an undead, it uses its Charisma when calculating its hit points, Fortitude saves, and any special abilities that rely on Constitution.
>
> **Feats:** A plagued beast gains Toughness as a bonus feat.

**Mechanical encoding:** `changes`: 5
  - `4` → `str`  (untyped)
  - `2` → `dex`  (untyped)
  - `ifelse(gte(@abilities.cha.total, 15), 0, 15 - @abilities.cha.total)` → `cha`  (untyped)
  - `1` → `bonusFeats`  (untyped)
  - `2` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Pod-Spawned
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 21
**Foundry id:** `PVYC3drphaVss858`

> A creature with the pod-spawned template is a duplicate created by the bodythief. It resembles the original and has all its memories, but can't exhibit sincere emotion.**Pod-spawned creatures can't reproduce and remain the same apparent age as their original at the time of replacement.
>
> "Pod-spawned" is an acquired template that can be added to any living creature (referred to hereafter as the base creature).
>
> CR:** For creatures with no class levels or only NPC class levels, this is the same as that of the base creature. For creatures with PC class levels, this is the same as that of the base creature –1. Creatures with a significant number of spells, spell-like abilities, or supernatural abilities have their CR further reduced by 1.
>
> **Type:** Type changes to plant. Do not recalculate BAB, hit points, saves, or skill ranks.
>
> **Alignment:** Alignment changes to lawful evil.
>
> **Senses:** A pod-spawned creature gains low-light vision.
>
> **Defensive Abilities:** A pod-spawned creature gains plant traits.
>
> **Special Abilities:** The pod-spawned creature gains the mimic ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.cvgqKtDW4GbLdsC3 inline=true]
>
> **Ability Scores:** Cha –4.
>
> **Feats:** All feats are retained, even if the pod-spawned creature no longer qualifies for their prerequisites.
>
> **Special Abilities:** The creature loses any spellcasting ability and all spell-like and supernatural abilities.

**Mechanical encoding:** `changes`: 1
  - `-4` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Possessed Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `h8j7cYUozTuPOgUj`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> While there are rules in Pathfinder RPG Occult Adventures for when a creature is possessed and totally controlled by a specific spell, sometimes a creature is possessed by a vague entity (hereafter called a spirit) that acts as a second personality within the creature’s mind, sharing control and providing the creature some symbiotic benefits.
>
> **Quick Rules:** +2 on rolls based on Cha; +4 on Will saves; after failing a save against a mind-affecting effect, reroll the save, but the spirit takes control if the second save succeeds; always acts on the surprise round.
>
> **Rebuild Rules:** Defensive Abilities +4 on Will saves; after failing a save against a mind-affecting effect, reroll the save, but the spirit takes control if the second save succeeds; Special Qualities always acts on the surprise round; Ability Scores +4 Cha.

**Mechanical encoding:** `changes`: 2
  - `4` → `cha`  (untyped)
  - `4` → `will`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Prana Ghost
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `royN1TrSR8rN2Qgu`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> The typical ghost is a nightmarish creature of dark emotion, with an undying thirst for justice or vengeance. These ghosts are often warped by deep emotional turmoil, madness, or contact with the dark radiations of the Negative Energy Plane—sometimes all three. But such twisted, tormented creatures are not the only spirits that cling to traces of their former lives on the Material Plane. There is another kind of ghost, just as dedicated, but more rational and often more subtle.
>
> As a soul departs a body, it joins the great River of Souls winding its way through the Astral Plane and passes on to judgment in the Outer Planes. Sometimes such a soul, through force of will or an unquenchable desire to accomplish one last act, forces its way back to the Material Plane as a prana ghost. Formed entirely of vital life essence, or prana, this manifest spirit is not an undead creature, but rather something entirely different, though undead that gorge on life energy are drawn to the glut of prana that composes a prana ghost like scavengers to a fresh corpse. Though easily mistaken for the undead spirits they resemble, prana ghosts function very differently from normal ghosts, haunts, and other incorporeal undead.
>
> Unlike the raging etheric ghost, a prana ghost tends to avoid worldly affairs when it can. It acts as mentor and guide to the living rather than acting overtly. These ghosts exude a supernatural calm and exhibit great control over their emotions and desires, wishing only to accomplish the task at hand, and to do so as quickly and as safely as possible. Even so, when victory (or failure) looms, a reckless prana ghost may attempt to take matters into its own hands. Such an intervention can be a great surprise to those who had no idea a supernatural entity was pulling the strings of their agents and allies. Among virtuous creatures who were unaware of the aid they were receiving, the prana ghost’s appearance might lead to violence if the prana ghost can’t convince them it isn’t undead.
>
> Once a prana ghost succeeds at its task, or its failure becomes clear, it dissipates from the world and reenters the Astral Plane. Many prana ghosts then resume their passage toward the Outer Planes, but a few dwell on the Astral Plane for centuries, if not millennia. Such prana ghosts often plot a reversal of personal fortunes, or the fortunes of their progeny or those of friends and allies. Others linger because they are not yet ready to reach their final fate.
>
> Usually, prana ghosts are more helpful and less malicious than their ethereal cousins, but not always. A creature doesn’t need to have led a virtuous or enlightened life to achieve the state—it needs only the necessary force of will to slip the chains of death, and a willingness to accept whatever consequences its soul might have to endure for refusing to face judgment at the appointed time. The souls of evil creatures seeking final vengeance can be just as willful as those with righteous goals, for selfishness can drive a soul to cling to mortal existence as strongly as more noble motivations.
>
> "Prana ghost" is an acquired template that can be added to any living creature with Intelligence and Wisdom scores of at least 6 (referred to hereafter as the base creature). A prana ghost retains all of the base creature’s statistics and special abilities except as noted here.
>
> **Challenge Rating:** Base creature’s CR + 1.
>
> **Type:** The creature’s type changes to outsider, and it gains the augmented, extraplanar, and incorporeal subtypes. Do not recalculate the creature’s base attack bonus, saves, or skill points.
>
> **Armor Class:** A prana ghost gains a deflection bonus to AC equal to its Wisdom modifier instead of the Charisma-based bonus the incorporeal ability normally provides. It loses the base creature’s armor bonus, as well as all armor and shield bonuses that don’t come from force effects or ghost touch items.
>
> **Hit Dice:** Change all of the creature’s racial Hit Dice to d10s. All Hit Dice derived from class levels remain unchanged.
>
> **Defensive Abilities:** A prana ghost retains all of the defensive abilities of the base creature save those that rely on a corporeal form to function. Prana ghosts gain darkvision to a range of 60 feet, the incorporeal ability, and the rejuvenation ability.
>
> Prana ghosts are immune to dazing, disease, exhaustion, fatigue, paralysis, poison, sleep effects, and stunning, as well as all effects that require a corporeal body. They are not subject to nonlethal damage.
>
> A prana ghost doesn’t risk death from damage, but instead immediately dissipates when its hit point total drops to a negative amount equal to its Constitution score. Prana ghosts are not affected by raise dead, resurrection, or true resurrection, but can be affected by reincarnate.
>
> *Rejuvenation (Su):* In most cases, it is difficult to dissipate a prana ghost through simple combat; the prana ghost restores itself in 2d4 days. Generally, the only way to permanently dissipate a prana ghost is to help it complete its mission or to make the mission impossible to complete, after which the prana ghost continues its path to the afterlife.
>
> **Weaknesses:** A prana ghost gains the following weakness. Living
>
> *Prana (Ex): *A prana ghost is made entirely of life essence, so it is vulnerable to effects that snuff life essence out. A prana ghost takes half again as much damage (+50%) from negative energy effects and death effects that deal damage, half again as many negative levels from negative energy effects that inflict negative levels, and half again as much Constitution damage and drain from negative energy effects (such as a wraith’s touch). If a prana ghost dissipates from such an effect, it takes twice as long for it to restore itself via rejuvenation.
>
> **Speed:** Prana ghosts lose their previous speeds and gain a fly speed of 30 feet (perfect) unless the base creature has a higher fly speed. They also gain the astral step ability.
>
> *Astral Step (Su):* As a standard action a number of times per day equal to its Wisdom bonus, a prana ghost can teleport to a space within 60 feet that it can see. This is a teleportation effect.
>
> **Attacks:** A prana ghost keeps the base creature’s natural and unarmed attacks. These attacks automatically count as if they had the ghost touch property and add the prana ghost’s Wisdom bonus to damage rolls (or 1/2 its Wisdom bonus for off-hand attacks and secondary weapons, but no additional damage for single primary natural attacks or the like). If the creature could wield weapons in life, it can wield ghost touch weapons as a prana ghost.
>
> **Special Attacks:** A prana ghost gains the following melee attack.
>
> *Dazing Touch (Su):* With a touch, a prana ghost can deal 1d6 points of damage, and the creature touched must succeed at a Will saving throw (DC = 10 + 1/2 the prana ghost’s Hit Dice + the prana ghost’s Wisdom modifier) or be dazed for 1 round.
>
> **Ability Scores:** Dex +4, Con +4, Wis +2. As incorporeal creatures, prana ghosts have no Strength score.
>
> **Skills:** Prana ghosts have a +8 racial bonus on Perception, Sense Motive, and Stealth skill checks. A prana ghost always treats Acrobatics, Bluff, Craft, Diplomacy, Intimidate, Knowledge (planes), Perception, Sense Motive, Stealth, and Use Magic Device as class skills. Otherwise, class skills are the same as the base creature.
>
> **Feats:** Prana ghosts gain Alertness, Improved Initiative, and Toughness as bonus feats.

**Mechanical encoding:** `changes`: 8 (showing first 5)
  - `2` → `wis`  (untyped)
  - `8` → `skill.sen`  (racial)
  - `30` → `flySpeed`  (base)
  - `8` → `skill.per`  (racial)
  - `4` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Primordial
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO9458 (PZO9458) p. 19
**Foundry id:** `gMtxmfemM0rZFyZO`

> **Usable with Summons** Yes - Requires the feat @UUID[Compendium.pf1.feats.Item.ezNxW33BtSafLl0J] or @UUID[Compendium.pf1.feats.Item.R5nnb83RW7qHkVmA]
>
> Primordial creatures are magical precursors or echoes of creatures from the Material Plane. A primordial creature’s CR increases by 1 only if the base creature has 5 or more HD.
>
> **Rebuild Rules:**
>
> **Defensive Abilities** gains DR as noted on the table below;
>
> **SR** gains SR equal to its new CR + 6;
>
> **Speed** gains a +10-ft. bonus to all speeds;
>
> **Attacks** the damage dice for one primary natural weapon increases as if the creature were one size larger (if the creature has more than one primary attack, the increased damage is applied to the first attack type it has from this list: bite, claw, slam, gore, talon, sting);
>
> **Spell-Like Abilities** gains spell-like abilities listed on the table below according to its Hit Dice (including all the spell-like abilities of lower-Hit Die primordial creatures), each available 1/day. The DCs of any saves against these abilities are equal to 10 + the primordial creature’s Charisma bonus + spell level.
>
>
> **Hit Dice**
>
>
> **DR**
>
>
> **Spell-Like Abilities**
>
>
> 1-4
>
>
> -
>
>
> @UUID[Compendium.pf1.spells.Item.zymaptg3vmnvfvxl]
>
>
> 5-10
>
>
> 5/cold iron
>
>
> @UUID[Compendium.pf1.spells.Item.bl71og1gklwncmt7]
>
>
> 11+
>
>
> 10/cold iron
>
>
> @UUID[Compendium.pf1.spells.Item.ud4xukzhan89qhm4]

**Mechanical encoding:** `changes`: 2
  - `10` → `allSpeeds`  (untyped)
  - `@details.cr.total + 6` → `spellResist`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Promethean Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `q1qyzlzQOF1I2hB5`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> A promethean creature has had some of its body replaced by golem parts.
>
> **Quick Rules:** +4 to AC; +2 on rolls based on Str; slam attack that deals 1d6 points of damage (for Medium creatures); +4 on saving throws vs. poison and disease; immune to emotion effects except those that produce rage, hatred, or anger; automatically stabilize when below 0 hp.
>
> **Rebuild Rules:** AC natural armor bonus increases by 4; Defensive Abilities +4 on saving throws vs. poison and disease, immune to emotion effects except those that produce rage, hatred, or anger; automatically stabilize when below 0 hp; Melee slam attack that deals 1d6 points of damage (for Medium creatures); Special Qualities doesn’t need to eat, sleep, or drink; Ability Scores +4 Str.

**Mechanical encoding:** `changes`: 2
  - `4` → `nac`  (untyped)
  - `4` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Prophecy-Addled Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `dxZIW17lbOVHmIuK`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Prophecy-addled creatures receive powerful oracular insights, but they cannot easily distinguish between these flashes of mystical insight and reality. A prophecy-addled creature’s quick and rebuild rules are the same.
>
> **Rebuild Rules:** 
>
> **AC** increase insight bonus by +2;
>
> **Saves** +2 insight bonus on Fortitude and Reflex saves, –4 penalty on saves against confusion effects;
>
> **Special Qualities** If the creature has flash of brutality, flash of insight, or another special quality that allows it to reroll a d20 roll a certain number of times each day, it can use that ability two additional times each day. If not, the creature gains the following special quality.
>
> *Prophetic Insight (Su): *Three times per day as an immediate action, the prophecy-addled creature can reroll any one d20 roll that it has just made before the results of the roll are revealed. It must take the result of the reroll, even if it’s worse than the original rol

**Mechanical encoding:** `changes`: 2
  - `2` → `fort`  (untyped)
  - `2` → `ref`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Psychic Lich
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `cNOJIofo8ZPzwpCs`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> While some liches prefer to spend undeath’s eternity in seclusion, a psychic lich sustains its life force by embracing its personal accomplishments to create a powerful astral echo of itself. Even more megalomaniacal than most liches, psychic liches resemble ordinary liches for the most part, but their every moment is attended by ghostly images of past cruelties, a constantly rotating illusory display of the evil deeds that brought them their power. Most psychic liches are humans, or come from other races renowned for their psychic abilities.
>
> ### A Psychic Lich’s Memoir and Legend
>
> To become a psychic lich, one must create and infuse a memoir, which serves a similar function to an ordinary lich’s phylactery. This memoir projects the lich’s personal legend into the Astral Plane, which is tethered through the planes to a physical object, typically a magically strengthened book or scroll (10 hit points, hardness 1, break DC 15). The only way to destroy the lich is to destroy his astral legend, which almost always requires the memoir as a special focus. Unless the astral legend is erased, the lich can rejuvenate after it is killed (see Creating a Psychic Lich, below).
>
> Each psychic lich must create its own memoir by using the Craft Wondrous Item feat. The character must be able to cast psychic spells at a caster level of 11th or higher. The memoir costs 120,000 gp to create and has a caster level equal to that of its creator at the time of creation.
>
> If the physical memoir is destroyed while the psychic lich’s astral legend survives, the physical memoir gradually reforms over the course of 1d10 days at a site central to its creator’s history (such as the library where he first studied magic or the battlefield where he vanquished a powerful rival). It typically reappears hidden among other books or treasures, where an unwitting dupe might begin reading the text and hasten the psychic lich’s return.
>
> "Psychic lich" is an acquired template that can be added to any living creature (referred to hereafter as the base creature), provided it can create the required astral memoir. A psychic lich retains all the base creature’s statistics and special abilities except as noted here.
>
> **Challenge Rating:** Base creature’s CR + 2.
>
> **Alignment:** Any evil.
>
> **Type:** The creature’s type changes to undead. Do not recalculate BAB, saves, or skill ranks.
>
> **Senses:** A psychic lich gains darkvision 60 ft.
>
> **Armor Class:** A psychic lich has a +5 natural armor bonus or the base creature’s natural armor bonus, whichever is higher.
>
> **Hit Dice:** Change all of the creature’s racial Hit Dice to d8s. All Hit Dice derived from class levels remain unchanged. As undead, psychic liches use their Charisma modifier to determine bonus hit points (instead of Constitution).
>
> **Defensive Abilities:** A psychic lich gains channel resistance +4, DR 15/bludgeoning and magic, and immunity to cold and electricity (in addition to those abilities granted by its undead traits). The lich also gains the following two defensive abilities.
>
> *Psychic Feast (Ex):* If a psychic lich succeeds at a Will saving throw against an attack that has a reduced effect on a successful save, it instead avoids the effect entirely. If the effect was a spell with the mind-affecting descriptor, the psychic lich also heals an amount of damage equal to 1d8 plus the spell’s caster level if it succeeds at its save. A psychic lich may automatically succeed on any Will save against a spell it casts that targets only itself.
>
> *Rejuvenation (Su):* When a psychic lich is destroyed, its body reforms near its astral memoir 10d10 days later. If a creature reads the psychic lich’s memoir, the total time is reduced to one tenth the original result, which could result in the psychic lich’s immediate restoration in a new body. Once the time elapses, the lich wakens fully healed (albeit without any gear it left behind on its old body).
>
> The only way to ensure that a psychic lich does not rejuvenate is to target its memoir with the spell instigate psychic duel or mindscape door or use it as a special focus when casting plane shift or similar magic. This allows one creature to instigate a psychic duel (Pathfinder RPG Occult Adventures 202) on a veiled, harmful mindscape with a self-contained shape inhabited by the lich’s astral legend. The legend has the statistics of the lich, can’t leave the mindscape by any means, and is permanently destroyed if reduced to 0 or fewer hit points. An astral legend can’t be destroyed unless the psychic lich’s physical body has also been destroyed and has not yet rejuvenated.
>
> **Weaknesses:** A psychic lich doesn’t gain immunity to mind-affecting effects as a result of becoming undead. If the base creature is immune to any mind-affecting effects, it loses those immunities and instead gains a +4 bonus on saving throws against such effects.
>
> **Attacks:** A psychic lich has a melee touch attack that it can use once per round as a natural weapon. A lich fighting without weapons uses its natural weapons (if it has any) in addition to its touch attack (which is treated as a primary natural weapon that replaces one claw or slam attack, if the creature has any). A lich armed with a weapon uses its weapons normally, and can use its touch attack as a secondary natural weapon.
>
> **Damage:** A psychic lich’s touch attack uses psychic energy to deal 1d8 points of damage to a target + 1 point of damage per 2 Hit Dice possessed by the lich. This energy has no effect on a creature immune to mind-affecting effects.
>
> **Special Attacks:** A psychic lich gains the special attacks described below. Save DCs are equal to 10 + 1/2 the lich’s HD + the lich’s Charisma modifier unless otherwise noted.
>
> *Bewildering Touch (Su): *Any living creature a psychic lich hits with its touch attack must succeed at a Fortitude saving throw or be permanently confused as its nervous system continuously sends false signals. The creature doesn’t automatically attack the psychic lich if it is targeted by further attacks. Calm emotions or any spell that can remove a curse can free the victim (see the bestow curse spell description) with a DC equal to the bewildering touch’s save DC. As a full-round action, a creature that rolls a result of "act normally" can attempt a new saving throw to end this effect.
>
> **Ability Scores:** Int +2, Wis +2, Cha +2. Being undead, a psychic lich has no Constitution score.
>
> **Skills:** Psychic liches have a +8 racial bonus on Perception, Sense Motive, and Stealth checks. A lich always treats Climb, Disguise, Fly, Intimidate, Knowledge (arcana), Knowledge (religion), Perception, Sense Motive, Spellcraft, and Stealth as class skills. Otherwise, skills are the same as the base creature.
>
> **Feats:** A psychic lich gains Psychic Combatant, and Psychic Defender as bonus feats, even if it does not meet the prerequisites.

**Mechanical encoding:** `changes`: 7 (showing first 5)
  - `8` → `skill.sen`  (racial)
  - `2` → `wis`  (untyped)
  - `2` → `cha`  (untyped)
  - `8` → `skill.ste`  (racial)
  - `2` → `int`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Psychic Vampire
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `PyRquowxdB6eSxmI`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Much like their more bestial cousins, psychic vampires are undead abominations driven by a terrible hunger. However, unlike vampires and nosferatu, who feed on blood, psychic vampires hunger for the occult energy that fuels the spells of psychic spellcasters. Some scholars confuse psychic vampires with the rare vetala breed of vampires or call them "vetalaranas," as they steal a more refined form of spiritual energy. For their part, psychic vampires consider vetalas a dying bloodline, and as their own influence increases, they strike against their corpse-possessing kin with impunity.
>
> A psychic vampire is usually born when a creature with psychic potential dies in a state of denial, stubbornly clinging to the material world through sheer willpower. As it dies, the creature attempts to draw on its own psychic energy and that of any living beings around it in order to cling to its mortal existence. It inevitably fails, but if its will is strong enough, it rises again. No longer able to sustain itself using its own mental energy, it hungers for the energy of others. Psychic vampires can’t create spawn, and thus their numbers remain relatively small.
>
> A hungry psychic vampire appears in shades of gray, but when it has gorged on psychic energy, it becomes flushed with natural colors once again, and if it’s careful, it might pass for a living creature. Although sunlight doesn’t harm psychic vampires, they avoid it because their unnatural grayness gives away their true nature. Religious mantras and superstitious antics have no effect on psychic vampires other than to amuse them greatly, although psychic vampires who were religious in life might expect those practices to hold power over them in their undead state and react with fear until they realize the mantras can’t harm them. The only thing that can give a psychic vampire pause is lack of fear in its victims.
>
> The home of a psychic vampire looks deceptively normal, holding fresh food and other supplies that undead creatures don’t need in abundant supply. The fresh food is more than a facade, however; the psychic vampires have it fed to their captives to keep these captives fit for use as possessed bodies and reserves of psychic energy.
>
> "Psychic vampire" is an acquired template that can be added to any living creature with 5 or more Hit Dice (referred to hereafter as the base creature). Most psychic vampires were once humanoids, fey, or monstrous humanoids. A psychic vampire uses the base creature’s statistics and abilities except as noted here.
>
> **Challenge Rating:** Base creature’s CR + 2.
>
> **Alignment:** Any evil.
>
> **Type:** The creature’s type changes to undead (augmented). Do not recalculate class Hit Dice, BAB, or saves.
>
> **Senses:** A psychic vampire gains darkvision to a range of 60 feet and thoughtsense.
>
> **Armor Class:** Natural armor improves by 4.
>
> **Hit Dice:** Change all racial Hit Dice to d8s. Class Hit Dice are unaffected. As undead, psychic vampires use their Charisma modifiers to determine bonus hit points (instead of their Constitution modifiers).
>
> **Defensive Abilities:** A psychic vampire gains channel resistance +4, DR 10/cold iron and magic, and resistance to cold 10 and fire 10, in addition to all of the defensive abilities granted by the undead type. A psychic vampire also gains fast healing 5. If the psychic vampire is reduced to 0 hit points in combat, its fast healing ceases to function, and it must possess an object (see Weaknesses below) as an immediate action or be utterly destroyed. While possessing the object, it can’t use any of its supernatural abilities or exit the object. If the possessed object is destroyed while the psychic vampire possesses it, the psychic vampire is permanently destroyed. After 1 hour, the psychic vampire can exit the possessed object, regain 1 hit point, and resume healing at the rate of 5 hit points per round.
>
> **Weaknesses:** A psychic vampire has difficulty tolerating any vocal expressions that deny its power or authority. Any character can force a psychic vampire to recoil by dramatically defying it verbally as a standard action. This doesn’t harm the psychic vampire—it merely keeps the psychic vampire at bay. A recoiling psychic vampire must stay at least 5 feet away from an openly defiant character and can’t touch or make melee attacks against it. After 1 round, a psychic vampire can fight past its revulsion and function normally each round it succeeds at a DC 25 Will save.
>
> Reducing a psychic vampire’s hit points to 0 or lower incapacitates it but doesn’t always destroy it (see Defensive Abilities above). However, destroying an object possessed by a psychic vampire whose fast healing isn’t functioning destroys the psychic vampire forever. Repairing the object does not restore the psychic vampire.
>
> **Attacks:** A psychic vampire gains a slam attack if the base creature didn’t have one. Its natural weapons are treated as magic weapons for the purpose of overcoming damage reduction.
>
> **Special Attacks:** A psychic vampire gains the following special attacks. The save DCs are equal to 10 + 1/2 the psychic vampire’s Hit Dice + the psychic vampire’s Charisma modifier unless otherwise noted.
>
> *Drain Psychic Energy (Su):* A creature hit by a psychic vampire’s slam attack (or other natural weapon) takes 1d4 points of ability drain to the highest of its mental ability scores (Intelligence, Wisdom, or Charisma), and the psychic vampire gains a like number of temporary points of psychic energy (PE). These PE points are in addition to the psychic vampire’s current PE total, and any PE expended is subtracted from these PE points first. These temporary PE points don’t stack with any previously gained temporary PE points. The temporary PE points disappear 1 hour later. The psychic vampire’s attack also drains the target’s memories, as per mindwipe. If a creature that takes ability damage from this attack has the ability to cast psychic spells, it is treated as though it were under the effects of a negative emotion effect for the purposes of the emotion component to its spellcasting. A successful Will saving throw negates all the effects of drain psychic energy.
>
> This ability triggers only once per round, regardless of the number of attacks a psychic vampire makes.
>
> *Possession (Su): *As a full-round action, a psychic vampire can attempt to take control of a helpless living creature’s body, as per the spell possession (the CL is 10th or equal to the psychic vampire’s HD, whichever is higher). A creature that successfully saves against this ability is immune to that same psychic vampire’s possession for 24 hours.
>
> **Special Qualities:** A psychic vampire gains the following special qualities.
>
> *Possess Object (Su):* As a full-round action, a psychic vampire can possess an object and animate it, as per object possessionOA, except the psychic vampire’s body vanishes while it’s possessing an object, as per greater possession. The psychic vampire can remain in control of an object indefinitely. The vampire’s presence in an object can be determined via divination spells such as detect evil and detect undead.
>
> *Psychic Magic (Su): *A psychic vampire gains the psychic magic universal monster rule (see page 2). The psychic vampire has a cumulative number of spells it can cast determined by its HD, with a CL equal to the psychic vampire’s HD. The psychic vampire’s PE pool is equal to its HD.
>
>
>
>
>  **HD** 
>  **Spells** 
>
>
>  5–8 
>  *Burst of adrenaline*OA (1 PE), *haste* (3 PE), *mental block*OA (2 PE), *spider climb* (2 PE) 
>
>
>  9–12 
>  *Emotive block*OA (3 PE), *mind thrust IV*OA (4 PE), *riding possession*OA (4 PE), *synaptic scramble*OA (4 PE) 
>
>
>  13–16 
>  *Synapse overload*OA (5 PE), *telepathy*OA (5 PE) 
>
>
>  17–20 
>  *Ego whip IV*OA (6 PE), *mass inflict pain*OA (6 PE) 
>
>
>
>
> **Ability Scores:** Str +2, Dex +2, Int +4, Wis +4, Cha +6. As an undead creature, a psychic vampire has no Constitution score.
>
> **Feats:** Psychic vampires gain Alertness, Combat Expertise, Dodge, Improved Initiative, and Iron Will as bonus feats.
>
> **Skills:** Psychic vampires gain a +8 racial bonus on Bluff, Perception, Sense Motive, and Stealth checks.

**Mechanical encoding:** `changes`: 10 (showing first 5)
  - `2` → `str`  (untyped)
  - `4` → `nac`  (untyped)
  - `8` → `skill.per`  (racial)
  - `8` → `skill.blf`  (racial)
  - `2` → `dex`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Psychoplasmic
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `JQfhDh7WlfOq9cbo`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> While nearly all spirits experience the Astral Plane at some point in their cosmic journeys, it is still one of the least understood planes in the multiverse. Some say it is merely a dream of the gods, while others contend it is the realm of thought itself. Though it is a seemingly endless realm of celestial desert, creatures still roam and hunt on its infinite expanse.
>
> Among the strangest are the psychoplasmic creatures that spontaneously form on the Astral Plane in no perceivable pattern. It could be that when a soul gets caught up in some form of astral eddy, its essence and the strange energies of the Astral Plane fuse to create this bizarre form of life. Some suggest that the passage of souls through the plane leaves impressions behind, the most powerful of which manifest as beings unto themselves. The most outlandish philosophies theorize that since the Astral Plane is a plane of thought, maybe a great thinker exists somewhere beyond the expanse, and these creatures are physical embodiments of its will.
>
> Whatever the nature of a psychoplasmic creature’s genesis, it retains much of its knowledge of its former life, if any, but is extremely emotionally dulled. It cares nothing for its past, and instead takes on a mission or a task that it must complete, but usually without knowing why. Those who believe that the Astral Plane is both the incarnation of thought and also a thinker believe that these creatures always do the bidding of that astral mind. The evidence is scant, as there seems to be little rhyme or reason to individual psychoplasmic creatures’ actions. Instead, they seem inexplicably fixated on random things; while a few eventually change the nature of their obsessions, such refocusing is rare. Some of the most common tasks that psychoplasmic creatures propel themselves toward include hunting down beasts or beings that they never could have bested in life, exploring or drawing other creatures toward areas of the Astral Planes where few have ever tread, and giving themselves over to the service of psychic masters to whom they are inexplicably attuned.
>
> The one common thread between all psychoplasmic creatures is their substance and appearance. Though they keep the forms they once held (or were molded to resemble), they seem to be composed of a large, constantly shifting clump of silvery dust. This dust continuously drifts from a psychoplasmic creature’s form, dissipating into nothing. Yet as fast as it falls, it is replaced, leaving the creature’s size unchanged even after decades or centuries of such evaporation. The strange dust of a psychoplasmic creature’s form completely disappears only after the creature fulfills its inscrutable objective.
>
> Psychoplasmic creatures come in many forms. Many are large, hulking brutes that stalk those who invade or defile the Astral Plane, sometimes tracking trespassers to the Material Plane (though their mobility is diminished there). Others are more intelligent and serve as advisors and companions to shulsagas (*Pathfinder RPG Bestiary 4* 245). These beings might be treated as anything from valued members of a shulsaga community to embodiments of heroes or entire shulsaga tribes lost and reborn. Others, however, wage war on shulsagas, and are widely perceived as the psychic vengeance of deadly foes or mighty beasts from their mythology. In any case, the known power of psychoplasmic creatures has impacted shulsagas’ culture and art, and they dust many of their most sacred sites and most impressive pieces of statuary in silvery powder, to suggest suggesting the adaptability and might of psychoplasmic creatures.
>
> A select few psychoplasmic creatures serve the interests of the Boneyard—though it can be difficult to tell whether that is intentional or incidental. Psychopomps keep these astral denizens at arm’s length, but nonetheless welcome their aid in their eternal vigil over the River of Souls. Many psychopomps remain skeptical of the strange creatures’ agenda, though, suspecting that these psychoplasmic allies are spying on or undermining their comrades. Regardless, no accounts tell of psychoplasmic creatures serving predators of souls, such as daemons.
>
> Still other psychoplasmic creatures wander the planes, fixated on whatever was embedded in their minds when they came into being. A strange few seem to be born without any ambition beyond a nameless urge to wander the multiverse in search of adventure before they finally dissipate back into the silvery void of the Astral Plane.
>
> "Psychoplasmic" is an acquired template that can be added to any corporeal creature (other than an undead), referred to hereafter as the base creature.
>
> **Challenge Rating**: Base creature’s CR + 1.
>
> **Alignment**: Usually neutral.
>
> **Type**: The creature’s type changes to outsider. Do not recalculate the base creature’s base attack bonus, saves, or skill points. It retains any subtype and gains the augmented subtype. It uses all the base creature’s statistics and special abilities except as noted in the following sections.
>
> **Armor Class**: A psychoplasmic creature gains a natural armor bonus of +2. If it already has a natural armor bonus, that bonus increases by 2.
>
> **Hit Dice**: Change all of the creature’s racial Hit Dice to d10s. All Hit Dice derived from class levels remain unchanged.
>
> **Defensive Abilities**: A psychoplasmic creature gains an amount of spell resistance equal to its CR + 5. Psychic spells bypass this spell resistance.
>
> **Damage Reduction and Energy Resistance**: A psychoplasmic creature gains damage reduction and energy resistance based on its Hit Dice, as given in the table below.
>
>
>
>
>  **Hit Dice** 
>  **Resist Cold, Electricity, and Fire** 
>  **DR** 
>
>
>  1–4 
>  5 
>  — 
>
>
>  5–10 
>  10 
>  5/magic or adamantine 
>
>
>  11+ 
>  15 
>  10/magic and adamantine 
>
>
>
>
> **Speed:** Psychoplasmic creatures gain a fly speed of 60 feet (perfect) while on the Astral Plane.
>
> **Attacks:** A psychoplasmic creature retains all natural weapons of the base creature. It gains a slam attack that deals damage based on the ectoplasmic creature’s size.
>
> **Special Attacks:** A psychoplasmic creature retains all of the special attacks of the base creature. In addition, a psychoplasmic creature gains the following special attack.
>
> *Mindlock (Su):* Upon successfully making an unarmed strike or natural attack against a creature with an Intelligence score of 3 or higher, a psychoplasmic creature can attempt to impose a mindlock on that creature as a free action. The target of the mindlock must succeed at a Will saving throw (DC = 10 + 1/2 the psychoplasmic creature’s Hit Dice + its Intelligence modifier). If the target fails, it cannot cast spells, speak, or use Intelligence checks or Intelligence-based skill checks for 1 round (or 1d4 rounds, if the psychoplasmic creature has 11 Hit Dice or more).
>
> **Ability Scores:** Dex +4, Int +4.
>
> **Skills:** Survival is always a class skill for psychoplasmic creatures, and they gain a +5 racial bonus on Survival check when following tracks.
>
> **Special Abilities:** The flexible body of a psychoplasmic creature grants it the compression ability.

**Mechanical encoding:** `changes`: 3
  - `2` → `nac`  (untyped)
  - `4` → `dex`  (untyped)
  - `4` → `int`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Rampant
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `UeYPclKF36SDgECy`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> The Positive Energy Plane is a font of growth, life, and souls, and metaphysical currents bear these resources through the hearts of stars and onto the Material Plane. Especially potent bursts of positive energy or partially developed souls can wind their way through the Material Plane to quicken plant life in particular. Only hardy plant creatures can foster this extraplanar force and be transformed into fonts of unchecked growth. Such rampant creatures rapidly change their local environments, turning mundane plants into tangled masses of competing foliage that slowly develop into new creatures all their own.
>
> "Rampant" is an acquired template that can be added to any plant creature with at least 8 Hit Dice, referred to hereafter as the base creature. A rampant creature uses the base creature’s statistics and special abilities except as noted here.
>
> **Challenge Rating:** The base creature’s CR + 1.
>
> **Aura:** A rampant creature has the following aura.
>
> *Aura of Growth (Su): *Living plants (but not plant creatures) within 1 mile of a rampant creature grow at triple their normal rate, and plants within 100 feet are affected as by the overgrowth function of plant growth. Overgrown plants return to normal after spending 1 hour outside the rampant creature’s presence, or immediately if the rampant creature takes negative energy damage.
>
> **Regeneration:** A rampant creature gains regeneration 5 (negative energy).
>
> **Weaknesses:** A rampant creature gains vulnerability to negative energy, and taking any negative energy damage disables the creature’s aura of growth for 1 minute.
>
> **Abilities:** Con +4.
>
> **Special Quality:** A rampant creatures gain the following special quality.
>
> *Verdant Genesis (Su): *Every week, a group of living plants within 1 mile of the rampant creature grows into new plant creatures with total combined Hit Dice no higher than the rampant creature’s total Hit Dice. For instance, a rampant quickwood with 10 HD could create two 4 HD assassin vines and two 1 HD vegepygmies. These new creatures are not under the rampant creature’s command. These new creatures each take 1 permanent negative level for each full day they spend more than 1 mile from the rampant creature that spawned them. A rampant creature cannot suppress its verdant genesis ability.

**Mechanical encoding:** `changes`: 1
  - `4` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Ranger (Quick, Dex)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 248
**Foundry id:** `3snzuCXL24e4aiOC`

> A ranger creature gains a favored enemy. It also gains a basic combat style, tracking, and some defensive abilities. A ranger creature's CR increases by 2 if the creature has 10 or more HD.
>
> **Quick Rules:** Choose either Str or Dex. The creature gains +2 on all rolls based on the chosen ability score (and +2 to AC if Dex is chosen). The creature gains either @UUID[Compendium.pf1.feats.Item.8rsFtye3PwM6CKli] or @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs] as a bonus feat (if the creature has 10 or more HD, choose two more bonus feats from the lists in combat style class feature—from @UUID[Compendium.pf1.class-abilities.Item.KKGYpoGUDT4wkglu] if the creature took @UUID[Compendium.pf1.feats.Item.8rsFtye3PwM6CKli], or from @UUID[Compendium.pf1.class-abilities.Item.AU5RcfC63ZBOFIx8] if the creature took @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs]). The creature also gains @UUID[Compendium.pf1.class-abilities.Item.XmALhWqXdN9yOmtd] (choosing only one favored enemy; the favored enemy bonus increases by 2 at 5 HD and every 5 HD thereafter, to a maximum of +10 at 20 HD). Lastly, the creature gains @UUID[Compendium.pf1.class-abilities.Item.r8wPs0bB3WhOLxbX] (and @UUID[Compendium.pf1.class-abilities.Item.KQYCRLEdD4bGA5ak] if the creature has 10 or more HD).
>
> **Rebuild Rules: Defensive Abilities** @UUID[Compendium.pf1.class-abilities.Item.KQYCRLEdD4bGA5ak] (if the creature has 10 or more HD); **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.XmALhWqXdN9yOmtd] (choosing only one favored enemy; the favored enemy bonus increases by 2 at 5 HD and every 5 HD thereafter, to a maximum of +10 at 20 HD); **Special Qualities** @UUID[Compendium.pf1.class-abilities.Item.r8wPs0bB3WhOLxbX]; **Ability Scores** +4 Strength or Dexterity; **Feats** either @UUID[Compendium.pf1.feats.Item.8rsFtye3PwM6CKli] or @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs] as a bonus feat (if the creature has 10 or more HD, choose two more bonus feats from the lists in the combat style ranger class feature—either from @UUID[Compendium.pf1.class-abilities.Item.KKGYpoGUDT4wkglu] if the creature took @UUID[Compendium.pf1.feats.Item.8rsFtye3PwM6CKli], or from @UUID[Compendium.pf1.class-abilities.Item.AU5RcfC63ZBOFIx8] if the creature took @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs]).

**Mechanical encoding:** `changes`: 5
  - `2` → `rattack`  (untyped)
  - `2` → `dexSkills`  (untyped)
  - `2` → `ac`  (untyped)
  - `2` → `tattack`  (untyped)
  - `2` → `dexChecks`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Ranger (Quick, Str)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 248
**Foundry id:** `bXmCFt7toGfodmok`

> A ranger creature gains a favored enemy. It also gains a basic combat style, tracking, and some defensive abilities. A ranger creature's CR increases by 2 if the creature has 10 or more HD.
>
> **Quick Rules:** Choose either Str or Dex. The creature gains +2 on all rolls based on the chosen ability score (and +2 to AC if Dex is chosen). The creature gains either @UUID[Compendium.pf1.feats.Item.8rsFtye3PwM6CKli] or @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs] as a bonus feat (if the creature has 10 or more HD, choose two more bonus feats from the lists in combat style class feature—from @UUID[Compendium.pf1.class-abilities.Item.KKGYpoGUDT4wkglu] if the creature took @UUID[Compendium.pf1.feats.Item.8rsFtye3PwM6CKli], or from @UUID[Compendium.pf1.class-abilities.Item.AU5RcfC63ZBOFIx8] if the creature took @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs]). The creature also gains @UUID[Compendium.pf1.class-abilities.Item.XmALhWqXdN9yOmtd] (choosing only one favored enemy; the favored enemy bonus increases by 2 at 5 HD and every 5 HD thereafter, to a maximum of +10 at 20 HD). Lastly, the creature gains @UUID[Compendium.pf1.class-abilities.Item.r8wPs0bB3WhOLxbX] (and @UUID[Compendium.pf1.class-abilities.Item.KQYCRLEdD4bGA5ak] if the creature has 10 or more HD).
>
> **Rebuild Rules: Defensive Abilities** @UUID[Compendium.pf1.class-abilities.Item.KQYCRLEdD4bGA5ak] (if the creature has 10 or more HD); **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.XmALhWqXdN9yOmtd] (choosing only one favored enemy; the favored enemy bonus increases by 2 at 5 HD and every 5 HD thereafter, to a maximum of +10 at 20 HD); **Special Qualities** @UUID[Compendium.pf1.class-abilities.Item.r8wPs0bB3WhOLxbX]; **Ability Scores** +4 Strength or Dexterity; **Feats** either @UUID[Compendium.pf1.feats.Item.8rsFtye3PwM6CKli] or @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs] as a bonus feat (if the creature has 10 or more HD, choose two more bonus feats from the lists in the combat style ranger class feature—either from @UUID[Compendium.pf1.class-abilities.Item.KKGYpoGUDT4wkglu] if the creature took @UUID[Compendium.pf1.feats.Item.8rsFtye3PwM6CKli], or from @UUID[Compendium.pf1.class-abilities.Item.AU5RcfC63ZBOFIx8] if the creature took @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs]).

**Mechanical encoding:** `changes`: 7 (showing first 5)
  - `2` → `mdamage`  (untyped)
  - `2` → `mattack`  (untyped)
  - `2` → `strSkills`  (untyped)
  - `2` → `nattack`  (untyped)
  - `2` → `cmb`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Ranger (Rebuild, Dex)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 248
**Foundry id:** `smuVQX108OShSniw`

> A ranger creature gains a favored enemy. It also gains a basic combat style, tracking, and some defensive abilities. A ranger creature's CR increases by 2 if the creature has 10 or more HD.
>
> **Quick Rules:** Choose either Str or Dex. The creature gains +2 on all rolls based on the chosen ability score (and +2 to AC if Dex is chosen). The creature gains either @UUID[Compendium.pf1.feats.Item.8rsFtye3PwM6CKli] or @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs] as a bonus feat (if the creature has 10 or more HD, choose two more bonus feats from the lists in combat style class feature—from @UUID[Compendium.pf1.class-abilities.Item.KKGYpoGUDT4wkglu] if the creature took @UUID[Compendium.pf1.feats.Item.8rsFtye3PwM6CKli], or from @UUID[Compendium.pf1.class-abilities.Item.AU5RcfC63ZBOFIx8] if the creature took @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs]). The creature also gains @UUID[Compendium.pf1.class-abilities.Item.XmALhWqXdN9yOmtd] (choosing only one favored enemy; the favored enemy bonus increases by 2 at 5 HD and every 5 HD thereafter, to a maximum of +10 at 20 HD). Lastly, the creature gains @UUID[Compendium.pf1.class-abilities.Item.r8wPs0bB3WhOLxbX] (and @UUID[Compendium.pf1.class-abilities.Item.KQYCRLEdD4bGA5ak] if the creature has 10 or more HD).
>
> **Rebuild Rules: Defensive Abilities** @UUID[Compendium.pf1.class-abilities.Item.KQYCRLEdD4bGA5ak] (if the creature has 10 or more HD); **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.XmALhWqXdN9yOmtd] (choosing only one favored enemy; the favored enemy bonus increases by 2 at 5 HD and every 5 HD thereafter, to a maximum of +10 at 20 HD); **Special Qualities** @UUID[Compendium.pf1.class-abilities.Item.r8wPs0bB3WhOLxbX]; **Ability Scores** +4 Strength or Dexterity; **Feats** either @UUID[Compendium.pf1.feats.Item.8rsFtye3PwM6CKli] or @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs] as a bonus feat (if the creature has 10 or more HD, choose two more bonus feats from the lists in the combat style ranger class feature—either from @UUID[Compendium.pf1.class-abilities.Item.KKGYpoGUDT4wkglu] if the creature took @UUID[Compendium.pf1.feats.Item.8rsFtye3PwM6CKli], or from @UUID[Compendium.pf1.class-abilities.Item.AU5RcfC63ZBOFIx8] if the creature took @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs]).

**Mechanical encoding:** `changes`: 1
  - `4` → `dex`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Ranger (Rebuild, Str)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 248
**Foundry id:** `ayzAmEJOSJKImKdu`

> A ranger creature gains a favored enemy. It also gains a basic combat style, tracking, and some defensive abilities. A ranger creature's CR increases by 2 if the creature has 10 or more HD.
>
> **Quick Rules:** Choose either Str or Dex. The creature gains +2 on all rolls based on the chosen ability score (and +2 to AC if Dex is chosen). The creature gains either @UUID[Compendium.pf1.feats.Item.8rsFtye3PwM6CKli] or @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs] as a bonus feat (if the creature has 10 or more HD, choose two more bonus feats from the lists in combat style class feature—from @UUID[Compendium.pf1.class-abilities.Item.KKGYpoGUDT4wkglu] if the creature took @UUID[Compendium.pf1.feats.Item.8rsFtye3PwM6CKli], or from @UUID[Compendium.pf1.class-abilities.Item.AU5RcfC63ZBOFIx8] if the creature took @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs]). The creature also gains @UUID[Compendium.pf1.class-abilities.Item.XmALhWqXdN9yOmtd] (choosing only one favored enemy; the favored enemy bonus increases by 2 at 5 HD and every 5 HD thereafter, to a maximum of +10 at 20 HD). Lastly, the creature gains @UUID[Compendium.pf1.class-abilities.Item.r8wPs0bB3WhOLxbX] (and @UUID[Compendium.pf1.class-abilities.Item.KQYCRLEdD4bGA5ak] if the creature has 10 or more HD).
>
> **Rebuild Rules: Defensive Abilities** @UUID[Compendium.pf1.class-abilities.Item.KQYCRLEdD4bGA5ak] (if the creature has 10 or more HD); **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.XmALhWqXdN9yOmtd] (choosing only one favored enemy; the favored enemy bonus increases by 2 at 5 HD and every 5 HD thereafter, to a maximum of +10 at 20 HD); **Special Qualities** @UUID[Compendium.pf1.class-abilities.Item.r8wPs0bB3WhOLxbX]; **Ability Scores** +4 Strength or Dexterity; **Feats** either @UUID[Compendium.pf1.feats.Item.8rsFtye3PwM6CKli] or @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs] as a bonus feat (if the creature has 10 or more HD, choose two more bonus feats from the lists in the combat style ranger class feature—either from @UUID[Compendium.pf1.class-abilities.Item.KKGYpoGUDT4wkglu] if the creature took @UUID[Compendium.pf1.feats.Item.8rsFtye3PwM6CKli], or from @UUID[Compendium.pf1.class-abilities.Item.AU5RcfC63ZBOFIx8] if the creature took @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs]).

**Mechanical encoding:** `changes`: 1
  - `4` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Ravener
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1116 (PZO1116) p. 230-231
**Foundry id:** `u9sTYTt9G8qyWbAg`

> Most evil dragons spend their lifetimes coveting and amassing wealth, but when the end draws near, some come to realize that all the wealth in the world cannot forestall death. Faced with this truth, most dragons vent their frustration on the countryside, ravaging the world before their passing. Yet some seek a greater solution to the problem and decide instead to linger on, hoarding life as they once hoarded gold. These foul wyrms attract the attention of dark powers, and through the blackest of necromantic rituals are transformed into undead dragons known as raveners.
>
> Although its body quickly rots away, a ravener does not care for the needs of the flesh. It seeks only to consume life, be it from wild animals, would-be dragonslayers, or even other dragons. A ravener is often on the move, changing lairs frequently as its territories become devoid of life.
>
> The ravener presented here is built from a red dragon wyrm.
>
> "Ravener" is an acquired template that can be added to any evil true dragon of an age category of ancient or older (referred to hereafter as the base creature). A ravener retains all the base creature's statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature +2.
>
> **Alignment:** Any evil.
>
> **Type:** The creature's type changes to undead. Do not recalculate BAB, saves, or skill ranks. It keeps any subtypes possessed by the base creature.
>
> **Senses:** A ravener's darkvision increases to 240 feet, and its blindsense increases to 120 feet.
>
> **Armor Class:** A ravener gains a deflection bonus to its AC equal to half its Charisma bonus (minimum +1).
>
> **Hit Dice:** Change all of the base creature's racial Hit Dice to d8s. All Hit Dice derived from class levels remain unchanged. As an undead, a ravener uses its Charisma to determine bonus hit points instead of its Constitution.
>
> **Saving Throws:** As undead, a ravener uses its Charisma modifier on Fortitude saves (instead of Constitution).
>
> **Defensive Abilities:** A ravener gains channel resistance +4 and all of the immunities derived from undead traits. Its damage reduction changes from DR/magic to DR/good. A ravener also gains the following ability.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.ShmSmPqR8V2mcver inline=true]
>
> **Attacks:** A ravener retains all of the natural attacks of the base creature, but each of these attacks threatens a critical hit on a 19 or 20. Feats like Improved Critical can increase this range further. If the ravener scores a critical hit with a natural weapon, the target gains 1 negative level. The DC to remove this negative level is equal to 10 + 1/2 the ravener's Hit Dice + the ravener's Charisma modifier. Whenever a creature gains a negative level in this way, the ravener adds 5 points to its soul ward.
>
> **Special Attacks:** A ravener retains all of the special attacks of the base creature and gains the following special attacks as described below. All save DCs are equal to 10 + 1/2 the ravener's HD + the ravener's Charisma modifier.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.AC4OJ8KUjWOmR9AB inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.ambL7m669puVDCH1 inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.UVNAs1atF6WGoy2P inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.wex4REzhPY9keumz inline=true]
>
> **Abilities:** Str +4, Int +4, Wis +4, Cha +6. Being undead, a ravener has no Constitution score.
>
> **Skills:** A ravener has a +8 racial bonus on Intimidate, Perception, and Stealth checks. The ravener's class skills are otherwise the same as those of the base creature.

**Mechanical encoding:** `changes`: 8 (showing first 5)
  - `8` → `skill.int`  (racial)
  - `max(1, floor(@abilities.cha.mod / 2))` → `ac`  (deflection)
  - `8` → `skill.per`  (racial)
  - `6` → `cha`  (untyped)
  - `4` → `int`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Recycled Construct
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `rhqQSn51sbKynq7Z`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> A skilled artificer can revitalize a ruined construct by jury-rigging the pieces left intact. The patchwork nature of a recycled construct renders it fragile and leaves key circuitry exposed. reducing its bonus hit points by 5.
>
> "Recycled construct" is an acquired template that can be added to a construct with 3 or more Hit Dice made predominantly of solid material. A recycled construct uses all the base creature’s statistics and special abilities except as noted here.
>
> **Challenge Rating:** Base creature’s CR – 1.
>
> **Defensive Abilities:** Reduce any damage reduction or hardness by 5. Replace any immunity to magic with spell resistance equal to the base creature’s CR + 11. Any exceptions to the base creature’s immunity to magic automatically bypass the recycled construct’s spell resistance and function as described for the base creature.
>
> **Weaknesses:** A recycled construct gains the following weakness.
>
> *Malfunction (Ex):* A recycled construct that takes precision damage or extra damage from a critical hit becomes staggered for 1 round and immediately triggers a malfunction. To determine the nature of this malfunction, roll 1d10 and consult the table on page 52 (CL = the base creature’s HD; save DC = 10 + the base creature’s HD). A creature can use a move action to attempt a special Disable Device check before dealing precision damage to a recycled construct (DC = 20 + the base creature’s HD). On a success, the attacking creature can roll twice and choose the malfunction result.
>
>
>
>
>  **d10** 
>  **Malfunction** 
>
>
>  1 
>  No additional effect 
>
>
>  2 
>  Sparks fly from the construct, dazzling each adjacent creature that can see it (Fortitude negates). 
>
>
>  3 
>  The construct flails wildly, making one melee attack against each adjacent creature. If the construct is wielding only a ranged weapon, it uses that weapon as an improvised bludgeoning weapon. 
>
>
>  4 
>  The construct leaks lubricant, affecting itself and all adjacent squares as if with a *grease* spell for 1d4+1 rounds. 
>
>
>  5 
>  The attack causes the construct to seize violently, functioning as a free disarm combat maneuver check against the weapon that triggered the malfunction. On a success, the weapon is thrown 1d4×10 feet in a random direction. A natural weapon instead provokes a free grapple combat maneuver attempt against the attacking creature for 1 round. This malfunction has no effect on ammunition. 
>
>
>  6 
>  Acrid smoke, steam, or mist pours from the construct, as if from a *pyrotechnics* smoke cloud. 
>
>
>  7 
>  Shrapnel explodes from the construct in all directions, dealing 1d6 points of slashing damage per Hit Die of the construct to each creature within 20 feet (Reflex half). 
>
>
>  8 
>  The construct emits an earsplitting screech, deafening all creatures within 20 feet (Fortitude negates). 
>
>
>  9 
>  Disruptive energy pulses from the construct, functioning as *dispel magic* targeting every creature within 20 feet. 
>
>
>  10 
>  The construct goes berserk, as a clay golem. 
>
>
>
>
> **Attacks:** If the base creature has more than one natural attack, remove one natural attack. The creator can replace the lost attack with a light, one-handed, or ranged weapon of at least masterwork quality and a size appropriate for the base creature.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Resolute
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1116 (PZO1116) p. 293
**Foundry id:** `cNJjgY50ypSjk2zk`

> Creatures with the resolute template live in planes where law is paramount. They can be summoned using spells such as summon monster and planar ally. A resolute creature's CR increases by +1 only if the base creature has 5 or more HD. A resolute creature's quick and rebuild rules are the same.
>
> **Rebuild Rules:**
>
> **Senses** gains darkvision 60 ft.;
>
> **Defensive Abilities** gains DR and energy resistance as noted on the table; SR gains SR equal to new CR +5;
>
> **Special Attacks** @UUID[Compendium.pf1.template-abilities.Item.7F8NhzCPExC1bQUF] 1/day as a swift action (adds Cha bonus to attack rolls and damage bonus equal to HD against chaotic foes; smite persists until target is dead or the resolute creature rests).
>
> **Resolute Creature Defenses**
>
>
> **Hit Dice**
>
>
> **Resist Acid, Cold, and Fire**
>
>
> **DR**
>
>
> 1-4
>
>
> 5
>
>
> —
>
>
> 5-10
>
>
> 10
>
>
> 5/chaotic
>
>
> 11+
>
>
> 15
>
>
> 10/chaotic

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Rogue (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 248
**Foundry id:** `srT6zEa0pmwlh72n`

> A rogue creature gains sneak attack. It also gains defensive abilities and rogue talents if it has 10 or more Hit Dice. A rogue creature's CR increases by 2 if the creature has 10 or more HD.
>
> **Quick Rules:** +2 to AC and on all rolls based on Dex; gains @UUID[Compendium.pf1.class-abilities.Item.6pjr8jMFSKqXkBKk] with a number of sneak attack dice equal to 1/2 its HD (maximum 10d6 at 20 HD); gains @UUID[Compendium.pf1.class-abilities.Item.KQYCRLEdD4bGA5ak] and @UUID[Compendium.pf1.class-abilities.Item.7WaQxnVaaoL4AGr8] (if the creature has 10 or more HD, it also gains @UUID[Compendium.pf1.class-abilities.Item.ZfnHhhTFQVo0Lj4P] and two @UUID[Compendium.pf1.class-abilities.Item.iBTrvPtn3jczInbn], one of which can be an @UUID[Compendium.pf1.class-abilities.Item.EQ7JGo4P1XirLO46]).
>
> **Rebuild Rules:** **Defensive abilities** @UUID[Compendium.pf1.class-abilities.Item.KQYCRLEdD4bGA5ak], @UUID[Compendium.pf1.class-abilities.Item.7WaQxnVaaoL4AGr8] (@UUID[Compendium.pf1.class-abilities.Item.ZfnHhhTFQVo0Lj4P] if the creature has 10 or more HD); **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.6pjr8jMFSKqXkBKk] (with a number of sneak attack dice equal to 1/2 the creature's HD, to a maximum of 10d6 at 20 HD); **Special Qualities** if the creature has 10 or more HD, it gains two @UUID[Compendium.pf1.class-abilities.Item.iBTrvPtn3jczInbn], one of which can be an @UUID[Compendium.pf1.class-abilities.Item.EQ7JGo4P1XirLO46]; **Ability Scores** +4 Dexterity.

**Mechanical encoding:** `changes`: 5
  - `2` → `dexChecks`  (untyped)
  - `2` → `dexSkills`  (untyped)
  - `2` → `rattack`  (untyped)
  - `2` → `tattack`  (untyped)
  - `2` → `ac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Rogue (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 248
**Foundry id:** `cVE48is5NiDMEg8O`

> A rogue creature gains sneak attack. It also gains defensive abilities and rogue talents if it has 10 or more Hit Dice. A rogue creature's CR increases by 2 if the creature has 10 or more HD.
>
> **Quick Rules:** +2 to AC and on all rolls based on Dex; gains @UUID[Compendium.pf1.class-abilities.Item.6pjr8jMFSKqXkBKk] with a number of sneak attack dice equal to 1/2 its HD (maximum 10d6 at 20 HD); gains @UUID[Compendium.pf1.class-abilities.Item.KQYCRLEdD4bGA5ak] and @UUID[Compendium.pf1.class-abilities.Item.7WaQxnVaaoL4AGr8] (if the creature has 10 or more HD, it also gains @UUID[Compendium.pf1.class-abilities.Item.ZfnHhhTFQVo0Lj4P] and two @UUID[Compendium.pf1.class-abilities.Item.iBTrvPtn3jczInbn], one of which can be an @UUID[Compendium.pf1.class-abilities.Item.EQ7JGo4P1XirLO46]).
>
> **Rebuild Rules:** **Defensive abilities** @UUID[Compendium.pf1.class-abilities.Item.KQYCRLEdD4bGA5ak], @UUID[Compendium.pf1.class-abilities.Item.7WaQxnVaaoL4AGr8] (@UUID[Compendium.pf1.class-abilities.Item.ZfnHhhTFQVo0Lj4P] if the creature has 10 or more HD); **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.6pjr8jMFSKqXkBKk] (with a number of sneak attack dice equal to 1/2 the creature's HD, to a maximum of 10d6 at 20 HD); **Special Qualities** if the creature has 10 or more HD, it gains two @UUID[Compendium.pf1.class-abilities.Item.iBTrvPtn3jczInbn], one of which can be an @UUID[Compendium.pf1.class-abilities.Item.EQ7JGo4P1XirLO46]; **Ability Scores** +4 Dexterity.

**Mechanical encoding:** `changes`: 1
  - `4` → `dex`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Runeplated Construct
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `EHLA9tNCRxoR8moQ`

> **Acquired/Inherited Template** Both**Simple Template** No**Usable with Summons** No
>
> Wizards in ancient Thassilon each specialized in one of seven schools of magic, a practice that carried over to their production of magical constructs.
>
> "Runeplated construct" is an acquired or inherited template that can be added to any creature with the construct type (referred to hereafter as the base creature). A runeplated construct retains all the base creature’s statistics and special abilities except as noted here.
>
> **Challenge Rating:** Base creature’s CR + 1.
>
> **Defensive Abilities:** A runeplated construct retains all the defenses of the base creature and gains the following defensive ability.
>
> *Opposition School Resistance (Su): *A runeplated construct gains a +2 bonus on saving throws against spells and spell-like abilities from the schools of magic to which its school is opposed (see Runeplated Construct Traits below).
>
> **Special Attacks:** A runeplated construct retains all the special attacks of the base creature and gains the following special attack.
>
> *Infused Attack (Su): *By drawing upon the magical energy of the school that created it, a runeplated construct can add additional effects or damage to its melee attacks (see Runeplated Construct Traits below). The save DC against these abilities is 10 + half the construct’s CR + the construct’s Strength modifier.
>
> **Special Qualities:** A runeplated construct retains all the special qualities and abilities of the base creature and gains the following special quality.
>
> *Runeplated (Su):* A runeplated construct cannot cast spells or use spell-like abilities, even those granted to the base creature, from schools opposed to the one in which it is runeplated. If the base creature has spells or spell-like abilities from the school in which it is runeplated, its gains one additional use of each such ability during the normal frequency period (3/day becomes 4/day, for example).
>
> #### Runeplated Construct Traits
>
> A runeplated construct gains additional traits based on the school of Thassilonian sin magic used to enhance it.
>
> **Envy (Abjuration):** Envyplated constructs gain the following attack.
>
> *Envy-Infused Attack (Su):* An envyplated construct’s melee attacks are infused with abjuration magic that disrupts and suppresses the protective magic of its foe. Once per round as a free action upon hitting an opponent, an envyplated construct can lower the total deflection bonus (if any) of that foe by 2 (Reflex negates). Multiple applications of this ability stack until the target’s deflection bonus is reduced to 0. If the target has deflection bonuses from multiple sources, the highest bonus is lowered first. This ability does not render magical items nonmagical, nor does it end spell durations. After 1 minute, the effect ends and the deflection bonuses return to normal.
>
> *Opposition Schools:* Evocation and necromancy.
>
> **Gluttony (Necromancy):** Gluttonyplated constructs gain the following attack.
>
> *Gluttony-Infused Attack (Su):* A gluttonyplated construct can infuse its melee attacks with necromantic energy that steals the target’s life force, adding it to the golem’s own. Once per round as a free action upon hitting an opponent with a melee attack, a gluttonyplated construct can impose 1 temporary negative level on that foe (Fortitude negates).
>
> *Opposition Schools:* Abjuration and enchantment.
>
> **Greed (Transmutation):** Greedplated constructs gain the following attack.
>
> *Greed-Infused Attack (Su):* A greedplated construct can infuse its melee attacks with transmutation magic. As a free action once per round upon hitting an opponent with a melee attack, it can polymorph that opponent into a tiny animal for 1d3 rounds, as per the baleful polymorph spell (Fortitude negates). Unlike for the spell, however, none of the changes are permanent, and the target returns to its normal form and mind at the end of the duration.
>
> *Opposition Schools:* Enchantment and illusion.
>
> **Lust (Enchantment):** Lustplated constructs gain the following attack.
>
> *Lust-Infused Attack (Su): *Able to lower inhibitions and willpower with a mere touch, a lustplated construct can infuse its melee attacks with enchantment magic. Once per round as a free action upon hitting an opponent with a melee attack, a lustplated construct can deal 1d4 points of Wisdom damage (Will negates).
>
> *Opposition Schools:* Necromancy and transmutation.
>
> **Pride (Illusion):** Prideplated constructs gain the following attack.
>
> *Pride-Infused Attack (Su):* A prideplated construct can infuse its melee attacks with illusion magic. Once per round as a free action upon hitting an opponent, a prideplated construct can cause the target to become fascinated for 1d4+1 rounds as it is surrounded by interwoven, scintillating colors (Will negates).
>
> *Opposition Schools:* Conjuration and transmutation.
>
> **Sloth (Conjuration):** Slothplated constructs gain the following attack.
>
> *Sloth-Infused Attack (Su):* A slothplated construct can infuse its melee attacks with conjuration magic. Once per round as a free action upon hitting an opponent, a slothplated construct can cause that opponent, along with all its worn and held gear, to instantaneously teleport to any other available, visible space of the construct’s choosing within 100 feet (Will negates). Opponents thus teleported cannot be sent into the ground or into the air, and if the arrival area is dangerous (on fire, for instance), the opponent gains a +4 bonus on the saving throw to resist the effect.
>
> *Opposition Schools:* Evocation and illusion.
>
> **Wrath (Evocation):** Wrathplated constructs gain the following attack.
>
> *Wrath-Infused Attack (Su):* A wrathplated construct can infuse its melee attacks with evocation magic. Melee attacks made by a wrathplated construct deal an additional 2d6 points of fire or electricity damage (no save). The type of energy damage is chosen when the construct becomes runeplated and can’t be changed.
>
> *Opposition Schools:* Abjuration and conjuration.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Runeslave
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `AXuljvWINi0KJ4QF`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> The ageless monuments and awesome cities of Thassilon rose upon the backs of countless slaves, but none bore the sin-poisoned civilization’s burden more than the giants. Able to perform the work of dozens of human slaves, Thassilon’s titanic servants—hill giants, stone giants, taiga giants, and others—crafted marvels nigh unparalleled in any era before or since, and shaped the face of what is now modern Varisia. Yet as viciously as the runelords worked their slaves and for all they demanded, the giant-crafted marvels were not enough. And thus, working the corrupt rune magic that was theirs alone, the runelords manufactured a damning curse and laid it over their most tireless and effective workers, and in so doing created a new breed of servant: the runeslave.
>
> Numerous severe-looking runes spark and flicker upon a runeslave’s body, seemingly seared into the creature’s flesh. One of the runes is larger and more prominent than the others—this is always one of the runes of Thassilonian magic. Although a runeslave’s mind is dulled, its muscles bulge grotesquely, as if barely contained beneath a thin layer of skin, and such behemoths move with unnatural agility for creatures of their ponderous size.
>
> Note that while the runeslave template does make a giant more powerful (and thus increases its CR), few, if any giants would seek to gain a runeslave’s powers. Despite the advantages the runeslave gains, what it loses in free will and longevity typically vastly outweigh the benefits. In combat, a runeslave is deadly and terrifying, but in life, the condition is rightly feared among giants as a devastating and debilitating curse.
>
> "Runeslave" is an acquired template that can be added to any giant (referred to hereafter as the base creature). A runeslave uses all the base creature’s statistics and special abilities except as noted here.
>
> **CR:** Same as the base creature +1.
>
> **Defensive Abilities:** A runeslave becomes immune to fear effects, exhaustion, and fatigue. In addition, all runeslaves gain the following additional defensive ability.
>
> *Resist Pain (Ex): *Runeslaves can continue to function even after taking great punishment. They are immune to nonlethal damage. Against effects that inflict pain (such as a symbol of pain spell), a runeslave gains a +4 bonus on all saving throws.**Weaknesses: Runeslaves gain the following weakness.
>
> *Arcane Decay (Su): *The symbols etched upon a runeslave’s body put great stress on its physical form, choking its mind and ultimately killing the giant in time. Each runeslave has a predominant Thassilonian rune associated with one school of magic inscribed on its body. Traditionally, this rune is of a school of magic directly opposed to the runelord the runeslave serves— all of the runeslaves encountered in this adventure bear the sign of wrath upon their bodies as a sort of brand of shame. The slow decay of a runeslave’s mental faculties manifests as a gradual loss of life and sanity, represented by the accumulation of rune-shaped scars all over the body. The disease has no additional physical or mental effect until these magical runescars completely overwhelm their host, at which point the accumulated pain the giant has endured since becoming a runeslave is released in a fatal surge of unleashed suffering. All runeslaves are "infected" with this disease. Only limited wish, miracle, or wish can prevent or cure arcane decay, but in so doing removes the entire template, reverting the runeslave back to the base creature. Multiple successful Fortitude saves only delay the decay and do not cure the creature of the disease.
>
> Arcane Decay: Inherited—non-contagious; save Fortitude DC 15; frequency 1/week; effect gain one runescar; cure none (but see above). When a runeslave’s number of runescars equals its Hit Dice, it dies.
>
> Speed:** A runeslave’s base land speed is 20 feet faster than the base creature’s. Other forms of movement, such as flying or swim speeds, are unaffected.
>
> **Special Attacks:** A runeslave gains the following special attack.
>
> *Arcane Surge (Su): *Once per day as a swift action, a runeslave can gain the benefits of the spell haste for 6 rounds. Using this ability forces the giant to make an additional Fortitude save against arcane decay, even if it has already made its weekly save to resist the disease.
>
> **Abilities:** Change from the base creature as follows: Str +4, Dex +2, Int –2, Wis –2, Cha –2.
>
> **Feats:** Runeslaves gain Diehard and Toughness as bonus feats.

**Mechanical encoding:** `changes`: 6 (showing first 5)
  - `-2` → `cha`  (untyped)
  - `4` → `str`  (untyped)
  - `-2` → `int`  (untyped)
  - `2` → `dex`  (untyped)
  - `20` → `landSpeed`  (base)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Runewarped Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `wKvKDnbOARyx1BGr`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Before Alaznist created the first sinspawn through the use of her runewell, she experimented with several techniques to create sin-twisted servants. One foundation of the complex magical technique used to create sinspawn was known as runewarping. Through the use of runewarping, Alaznist and other powerful mages created horribly twisted creatures from their slaves and prisoners. These creators valued ability over aesthetics, so runewarped creatures were transformed by powerful magic into horrid mockeries of their previous forms. Runewarped creatures seek out sources of magic to consume, trying in vain to complete their transformation. Although a runewarped creature is recognizable as the creature it once was, the creature bears altered or additional limb joints, elongated fingers, and a massive jaw capable of delivering a powerful bite.
>
> "Runewarped creature" is an acquired template that can be added to any animal, humanoid, or monstrous humanoid (referred to hereafter as the base creature). A runewarped creature uses the base creature’s statistics and special abilities except as noted here.
>
> **Challenge Rating:** Base creature’s CR + 1.
>
> **Alignment:** Any evil.
>
> **Type:** The creature’s type changes to aberration. Do not recalculate its base attack bonus, saves, or skill ranks.
>
> **Senses:** The creature gains darkvision with a range of 60 feet, low-light vision, and magic-scent.
>
> *Magic-Scent (Su): *Runewarped creatures have scent that detects only creatures with the ability to cast spells. This scent allows the runewarped creature to know the location and power of all magic auras within range of its scent. Magic-scent always detects magic auras in a range of 60 feet and is not affected by wind.
>
> **Armor Class:** Natural armor bonus increases by 2.
>
> **Hit Dice:** Change all the creature’s racial Hit Dice to d8s. Hit Dice derived from class levels remain unchanged.
>
> **Defensive Abilities:** A runewarped creature with 5 Hit Dice or more gains DR 5/magic (or DR 10/magic if it has 11 Hit Dice or more) and SR equal to its new CR + 6 (or SR equal to its new CR + 11 if it has 11 Hit Dice or more).
>
> **Melee:** A runewarped creature gains a bite attack that deals damage based on the runewarped creature’s size but as if it were one size category larger than its actual size. If the runewarped creature already has a bite attack, the bite’s damage increases by one step, as if it had increased one size category.
>
> **Special Attacks:** A runewarped creature loses any spells or spell-like abilities, but it retains all other special attacks and abilities of the base creature. A runewarped creature gains the following special attack.
>
> *Consume Magic (Su):* A runewarped creature’s bite drains magical ability from creatures capable of casting spells or using spell-like abilities. The struck creature loses its highest-level prepared spell, spell slot, or spell-like ability unless it succeeds at a Will save to negate the effect. A creature can be affected by this ability only once per round, even if attacked multiple times or by multiple runewarped creatures. The save DC is Constitution-based.
>
> **Ability Scores:** Str +4, Con +2, Int –4 (minimum 1), Cha –2.

**Mechanical encoding:** `changes`: 5
  - `2` → `con`  (untyped)
  - `-4` → `int`  (untyped)
  - `-2` → `cha`  (untyped)
  - `4` → `str`  (untyped)
  - `2` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Sea-Sworn (3.5)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `KNfhdjpOycaZ4uJC`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** Yes
>
> This creature stares with cold, black eyes, its bluish-green skin slick with moisture and stinking of brine and the muck of the tidal flats. Its hands and feet are webbed, and its facial features are blunted by the smooth, frog-like skin that covers them. It makes no sound as it marches out of the shallows, water and seaweed streaming from its unkempt hair and barnacle-encrusted armor. It merely approaches with cold menace, sword raised and sharp beneath a crusting of salt.
>
> During the troubled times following Andoran’s break with Cheliax, Chelish necromancers created the sea-sworn to fill the need for ruthless and overpowering marines who would serve the navy tirelessly. "Volunteered" by their captains, these sailors and warriors were forced to undergo hideous rites culminating in their dying and being reborn as undead monstrosities uniquely suited to making war at sea. Powerful swimmers without the need to breathe or eat, and nearly impossible to destroy in their natural element, these crack teams were the bane of Andoren ships, with just a handful of the fast-healing horrors capable of overrunning the mightiest frigates. Concerned that such effective troops might reach too far, the Chelish government ordered them anchored to their role with the "curse of the sea-sworn," rendering them incapable of abandoning their ships or the sea. As further protection, the Chelish leaders frequently placed geas spells on the sea-sworn leaders, tasking them with policing their own and making sure that the undead sailors never strove to become more than what they were intended as: cold, heartless tools of Chelish ambition.
>
> #### Creating a Sea-Sworn
>
> "Sea-sworn" is an acquired template that can be added to any corporeal creature that does not possess the aquatic sub-type. A sea-sworn uses all of the base creature’s statistics except as noted here.
>
> **Size and Type:** The creature’s type changes to undead and it gains the augmented and aquatic sub-types. It retains any other subtypes except alignment subtypes. Do not recalculate base attack bonus, saves, or skill points. Size is unchanged.
>
> **Hit Dice:** Increase all current and future Hit Dice to d12s.
>
> **Armor Class:** The base creature’s natural armor bonus improves by +3. Sea-sworn often wear the armor they wore in life.
>
> **Defensive Abilities:** A sea-sworn retains the base creature’s defensive abilities and gains damage reduction.
>
> *Damage Reduction (Ex): *A sea-sworn has damage reduction 5/piercing. Their skin is incredibly tough, but deep stabs allow their salt water essence to seep out.
>
> **Weaknesses:** A sea-sworn retains the base creature’s weaknesses and gains the curse of the sea-sworn.
>
> *Curse of the Sea-Sworn (Ex): *Sea-sworn function normally whenever in contact with salt water or aboard a vessel floating (or sunken) in salt water. A sea-sworn taken outside these conditions by any means quickly withers away, taking 2d6 points of damage per round.
>
> **Speed:** The creature gains a swim speed equal to its land speed, or retains its original swim speed if it is faster than its land speed.
>
> **Attacks:** A sea-sworn retains all the natural weapons, manufactured weapon attacks, and weapon proficiencies of the base creature. A sea-sworn also gains a slam attack that also inflicts its drowning touch.
>
> **Damage:** Natural and manufactured weapons deal damage normally. A slam attack deals damage depending on the sea-sworn’s size. (Use the base creature’s slam damage if it’s better.)
>
> **Special Attacks:** A sea-sworn retains the base creature’s special attacks and also gains the following.
>
> *Drowning Touch (Ex): *The touch of a sea-sworn causes the lungs of a living creature to fill with salt water dealing 1 point of Constitution damage. Creatures with the aquatic or water sub-types, creatures that do not need to breathe, and creatures which can breathe water are all immune to this special attack.
>
> **Special Qualities:** A sea-sworn loses most special qualities of the base creature. It retains any extraordinary special qualities that improve its melee or ranged attacks. A sea-sworn gains the following special quality.
>
> *Fast Healing (Ex): *A sea-sworn gains fast healing 2 whenever it is immersed in salt water to a depth of at least one-quarter of the creature’s height.
>
> **Abilities:** A sea-sworn’s Strength score increases by +4, it has no Constitution score, and its Charisma score decreases by 2.
>
> **Feats:** Same as the base creature.
>
> **Skills:** A sea-sworn has a +8 racial bonus on any Swim check to perform some special action or avoid a hazard. It can always choose to take 10 on a Swim check, even if distracted or endangered. It can use the run action while swimming, provided it swims in a straight line. Otherwise same as the base creature.
>
> **Environment:** In contact with salt water or aboard a vessel in salt water.
>
> **Challenge Rating:** As base creature +1.
>
> **Alignment:** Usually neutral evil.
>
>
>
>
>  **Sea-Sworn Size** 
>  **Slam Damage** 
>
>
>  Fine 
>  1 
>
>
>  Diminutive 
>  1d2 
>
>
>  Tiny 
>  1d3 
>
>
>  Small 
>  1d4 
>
>
>  Medium 
>  1d6 
>
>
>  Large 
>  1d8 
>
>
>  Huge 
>  2d6 
>
>
>  Gargantuan 
>  2d8 
>
>
>  Colossal 
>  4d6

**Mechanical encoding:** `changes`: 3
  - `-2` → `cha`  (untyped)
  - `4` → `str`  (untyped)
  - `3` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Seeded
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `3LzewfL1XvkI88xR`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** No
>
> Though the Great Old One Xhamen-Dor lies halfdormant where its bloated body crashed millennia ago, virtually nothing can prevent it from seeking new hosts to infect. The most common means by which one might contract this infestation is through nightmares that brush against Xhamen-Dor’s influence in the Dimension of Dreams, after which the Inmost Blot can track victims and infest their thoughts, slowly and painfully driving them mad. Less common is direct exposure to one of the Great Old One’s vine-choked thralls: the seeded.
>
> Xhamen-Dor feeds upon a victim’s force of personality, and as a result, only a select few who meet its inscrutable criteria are even able to contract the seedborne consumption disease that turns one into a seeded. Those infected first become sickly and withdrawn. Weeks later, the germinating evil within begins sending fibrous feelers throughout the victim’s body. When the host finally slips into a catatonic coma, these fibers quickly digest the organs and portions of the flesh before animating the corpse from within like a puppet. Most victims maintain painful recollections of their former lives, yet they are driven to hear and obey the commands of Xhamen-Dor and find new victims to spread their plague.
>
> "Seeded creature" is an inherited template that can be added to any corporeal, living creature with a Charisma score of 12 or higher. A seeded creature uses the base creature’s stats and abilities except as noted here.
>
> **CR:** Base creature’s CR + 1.
>
> **Alignment:** Always neutral evil.
>
> **Type:** The creature’s type changes to undead (augmented). Do not recalculate class Hit Dice, Base Attack Bonus, or saves.
>
> **Senses:** A seeded creature gains darkvision with a range of 60 feet.
>
> **Armor Class:** The fungal growths that appear on a seeded creature’s body increase the base creature’s natural armor bonus by 2.
>
> **Hit Dice:** Change all racial Hit Dice to d8s. Class Hit Dice are unaffected. As undead, seeded creatures use their Charisma modifiers to determine bonus hit points (instead of their Constitution modifiers).
>
> **Defensive Abilities:** A seeded creature gains channel resistance +4, damage reduction 5/bludgeoning or slashing, a +4 bonus on saving throws against mindaffecting effects, cold resistance 10, and electricity resistance 10, in addition to the defensive abilities granted by the undead type. A seeded creature also gains fast healing 5.
>
> **Weaknesses:** A seeded creature has the following weakness.
>
> **Transformed:** Although seeded creatures are undead, their bodies pulse with alien plant life. For the purposes of effects targeting creatures by type (such as a ranger’s favored enemy and bane weapons), seeded creatures count as both undead and plants.
>
> Seeded creatures are not immune to charms, compulsions, and mind-affecting effects from psychic sources, such as psychic spells or a creature’s psychic magic ability. However, such effects have a chance to harm the source due to seeded creatures’ insidious mind special attack (see below).
>
> Speed: A seeded creature retains all movement types and gains a climb speed equal to its base speed.
>
> **Melee:** A seeded creature gains two tendril attacks that each deal damage as per a tentacle of a creature one size category larger than the base creature’s size. These tendrils are secondary attacks and also have the grab universal monster ability, and the seeded creature’s reach with these attacks increases by 5 feet. Its natural weapons are treated as magic and evil weapons for the purpose of overcoming damage reduction.
>
> **Special Attacks:** A seeded creature gains several special attacks. The save DCs are equal to 10 + 1/2 the seeded creature’s HD + the seeded creature’s Charisma modifier unless otherwise noted.
>
> *Death Burst (Ex):* When a seeded creature dies, it releases psychic spores. All creatures adjacent to the seeded creature are exposed to its seedborne consumption infestation (see below). Due to the spores’ psychic nature, any effect that would completely deflect gases and similar airborne hazards grants protected creatures only a +5 bonus on saving throws against exposure.
>
> *Entrapping Tendrils (Ex): *When a seeded creature succeeds at a combat maneuver check to pin a foe, it can attempt a second combat maneuver check to tie up the foe with a tendril as a swift action. Doing so causes it to lose one of its tendril attacks as long as it is keeping a creature tied up in this way, and a seeded creature can tie up only two creatures in this way before it runs out of spare vines. Each round that a creature remains tied up in this way, it is exposed to the seeded one’s seedborne consumption until it is affected. In addition, every full day a victim remains tied up in this way is instead treated as though a month had passed for the purpose of the seedborne consumption disease. The tendrils each have hardness 5 and 10 hit points. If a creature tears free or destroys a tendril, the seeded creature regrows enough of the vines that make up its tendrils to regain its lost tendril attack after 1 minute.
>
> *Insidious Mind (Su): *When a seeded one succeeds at a saving throw against a psychic charm, a compulsion, or another mind-affecting spell or spell-like ability that would otherwise affect it, its dreams infect the spellcaster’s mind, exposing him to seedborne consumption.
>
> *Seedborne Consumption (Su):* natural or touch attack; save Fort DC = 10 + 1/2 the seeded one’s HD + the seeded one’s Charisma modifier; onset 1 month; frequency 1/month; effect 1d2 Charisma damage (this damage cannot be healed while the creature is infected); cure 3 consecutive saves. When a creature’s Charisma is reduced to 0, instead of becoming unconscious it falls into a feverish mental state where its mind is scattered and inattentive. The creature can still move and perform actions, but it can concentrate on only a single action, and for only a few moments. It takes a –4 penalty on saving throws; Intelligence-, Wisdom-, and Charisma-based checks; and skill checks. Within 24 hours of a creature’s Charisma score reaching 0, it dies and rises as a seeded creature.
>
> **Ability Scores:** Str +4, Wis +2, Cha +4. As an undead creature, a seeded creature has no Constitution score.
>
> **Language:** A seeded creature gains telepathy with a range of 100 feet, but only with other seeded creatures. Seeded creatures benefit from the morale bonuses granted by other seeded creatures within range of their telepathy.

**Mechanical encoding:** `changes`: 4
  - `2` → `nac`  (untyped)
  - `4` → `cha`  (untyped)
  - `2` → `wis`  (untyped)
  - `4` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shadow Animal
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `VWsM44QuzCrRDw65`

> **Acquired/Inherited Template** Both**Simple Template** No**Usable with Summons** No
>
> Dread energies from the Plane of Shadow have leaked into the countryside of Nidal for thousands of years, pooling in shadowed groves and along darkened hillsides. Although normal animals shun these shadow-haunted regions, hunger or adversity sometimes compels a creature to enter them. Some animals who do so are wholly transformed by these energies, becoming shadow animals.
>
> Shadow animals are more than mere animals, becoming hunters bleached of bright colors and commanding unusual predatory powers. Even herbivores that undergo this transformation become short tempered and dangerous.
>
> Shadow animals have the brute cunning to understand spoken language, but they generally cannot speak.
>
> The shadow animal template is inherited or acquired and can be added to any living, corporeal animal (referred to hereafter as the base creature). A shadow animal uses all the base creature’s statistics and special abilities except as noted.
>
> **CR:** If 9 HD or fewer, base creature’s CR + 1; if 10 HD or more, base creature’s CR + 2.
>
> **Type:** The creature’s type changes to outsider (native). Do not recalculate HD, BAB, or saves.
>
> **Alignment:** Any (usually nongood).
>
> **Armor Class:** Reduce the creature’s natural armor, if any, by 1 (to a minimum of 0).
>
> **Senses:** A shadow animal gains darkvision with a range up to 60 feet and low-light vision if it didn’t already have it.
>
> **Defensive Abilities:** A shadow animal gains the following defensive ability.
>
> **Shadow Blend (Su):** In any illumination other than bright light, a shadow animal blends into the shadows, giving it concealment (20% miss chance). A shadow animal can suspend or resume this ability as a free action.
>
> **Speed:** All of the shadow animal’s movement speeds increase by 10 feet.
>
> **Special Abilities:** A shadow animal gains one of the following abilities for every 3 HD it has (round up).
>
> *Blinding Savagery (Ex):* Choose the rake, rend, or trample ability. Whenever the shadow animal creature uses the selected ability to deal damage to a creature, the damaged creature must succeed at a Fortitude saving throw or become blinded for 1 round. The save DC is equal to 10 + half the shadow animal’s Hit Dice + the shadow animal’s Wisdom modifier. This ability can be selected up to three times, applying it to a different ability each time.
>
> *Energy Resistance (Ex):* The shadow animal gains cold resistance 10 or increases its existing cold resistance of 10 or greater to immunity to cold. This ability can be selected up to two times.
>
> *Evasion (Ex):* The shadow animal gains evasion, as per the rogue ability of the same name.
>
> *Fear Aura (Su):* Any creature within a 60-foot radius of the shadow animal that can see or hear it must succeed at a Will saving throw (DC = 10 + half the shadow animal’s HD + the shadow animal’s Charisma modifier) or be shaken for as long as it remains within the aura. Whether or not it succeeds at its save, that creature cannot be affected again by the same shadow animal’s fear aura for 24 hours. This is a mind-affecting fear effect.
>
> *Frightful Presence (Su): *The shadow animal gains the frightful presence universal monster ability, which activates as a free action when the shadow animal charges, attacks during a surprise round, or succeeds at a DC 15 Intimidate check. Its frightful presence has a range of 30 feet and a duration of 5d6 rounds.
>
> *Hide in Plain Sight (Su): *The shadow animal can use Stealth even while being observed. As long as it is within 10 feet of a shadow other than its own, a shadow animal can attempt to use Stealth to hide itself from view even if it does not have cover or concealment.
>
> *See in Darkness (Su):* The shadow animal can see perfectly in darkness of any kind, including that created by deeper darkness.
>
> *Shadow Bite (Su):* The shadow animal can make one of its natural attacks through its shadow. Its reach with the selected natural attack increases by 5 feet, and a creature damaged by this natural attack must succeed at a Fortitude save (DC = 10 + half the shadow animal’s HD + the shadow animal’s Charisma modifier) or take 1 point of Strength damage in addition to the normal damage dealt.
>
> *Shadow Form (Su):* Once per day as a standard action, the shadow animal can turn into an animate pool of darkness for up to 10 minutes. This duration need not be used at all once, but it must be used in 1-minute increments. This ability functions as per gaseous form.
>
> *Shadow Spirit (Su): *The shadow animal gains a +4 racial bonus on saving throws against energy drain and death effects. This ability can be selected up to two times; if this ability is selected a second time, the shadow animal instead gains immunity to energy drain and death effects.
>
> *Shadow Step (Su): *The shadow animal can teleport up to 10 feet per Hit Die as a move action, so long as the creature starts and ends this travel in dim light or darkness. It can use this ability once every 1d4 rounds.
>
> *Spectral Attacks (Su):* The shadow animal’s natural attacks affect incorporeal creatures as if they had the ghost touch weapon special ability.
>
> *Spell Resistance (Ex):* The shadow animal gains SR equal to 11 + its CR. This does not stack with any SR the base creature has.
>
> *Umbral Fast Healing (Ex):* The shadow animal gains fast healing 1 when in areas of dim light or darkness. A shadow animal must have at least 10 HD to select this ability.
>
> *Vanish (Su): *As a swift action, the shadow animal can vanish for 1 round as if affected by invisibility. Each day, it can use this ability for 1 round per Hit Die. This ability’s duration need not be used all at once, but it must be used in 1-round increments.
>
> **Abilities:** A shadow animal gains a +4 bonus to Dexterity and Charisma and a +2 bonus to Intelligence and Wisdom.
>
> **Skills:** A shadow animal gains a +4 racial bonus on Intimidate and Stealth checks, which does not stack with any racial bonuses the base creature has. A shadow animal has a number of skill points per racial Hit Dice equal to 6 + its Intelligence modifier. Its racial class skills are Acrobatics, Climb, Fly, Intimidate, Perception, Stealth, and Swim.
>
> **Languages:** Shadow animals gain Common and Infernal, but if the base creature is unable to speak, it can only understand these languages.

**Mechanical encoding:** `changes`: 8 (showing first 5)
  - `4` → `skill.int`  (racial)
  - `2` → `wis`  (untyped)
  - `4` → `skill.ste`  (racial)
  - `2` → `int`  (untyped)
  - `4` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shadow Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** Ultimate Combat (PZO1121) p. 1
**Foundry id:** `yvYkW2QIxFIvStcu`

> Creatures with the shadow creature template dwell on the Shadow Plane, only rarely venturing onto other, brighter planes, and can be summoned by shadow callers. A shadow creature's CR increases by +1. A shadow creature's quick and rebuild rules are the same.
>
> **Senses** gains darkvision 60 ft. and low-light vision;
>
> **Defensive Abilities** gains energy resistance and DR as noted on the table below; SR gains SR equal to new CR + 6;
>
>
> **Hit Dice**
>
>
> **Resist Cold and Electricity**
>
>
> **DR**
>
>
> 1–4
>
>
> 5
>
>
> —
>
>
> 5–10
>
>
> 10
>
>
> 5/magic
>
>
> 11+
>
>
> 15
>
>
> 10/magic
>
>
> **Special Abilities** @Embed[Compendium.pf1.template-abilities.Item.5h5eg7TxHk9QqZrR inline=true]

**Mechanical encoding:** `changes`: 1
  - `@details.cr.total + 6` → `spellResist`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shadow Lord
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 238-239
**Foundry id:** `8skkLkLDQaVELQQK`

> "Shadow lord" is an acquired template that can be added to any shadow creature with 5 or more Hit Dice (referred to hereafter as the base creature). Most shadow lords were originally humanoids. A shadow lord retains all the base creature's statistics and abilities (including those granted by the shadow creature template) except as noted here.
>
> **Challenge Rating**: Same as the base creature +2.
>
> **Alignment**: Any evil.
>
> **Senses**: A shadow lord gains the see in darkness ability.
>
> **Armor Class**: Same as the base creature (see also the incorporeal step ability).
>
> **Defensive Abilities**: A shadow lord gains the following defensive abilities.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.N6phN54CSyfxWDGE inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.So7ITiyAEuINBETo inline=true]
>
> **Attacks**: A shadow lord gains a melee touch attack that deals 1d6 points of damage (Fortitude negates). The save DC is equal to 10 + 1/2 the shadow lord's Hit Dice + the shadow lord's Charisma modifier. On a critical hit, the shadow lord's touch attack also deals 1 point of Constitution damage (also negated by the saving throw).
>
> **Special Attacks**: A shadow lord gains the following special attacks. Their saving throw DCs for these attacks are equal to 10 + 1/2 the shadow lord's Hit Dice + the shadow lord's Charisma modifier, unless otherwise noted.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.izOLrpaR7daioVgm inline=true]
>
> **Spell-Like Abilities**: A shadow lord gains the following spell-like abilities, with a caster level equal to its Hit Dice: at will—@UUID[Compendium.pf1.spells.Item.c3iz720zjv922b6j]; 3/day—@UUID[Compendium.pf1.spells.Item.ed7fvzc2p4m6n7a2], @UUID[Compendium.pf1.spells.Item.cmwcavfyc1vbehy8]; 1/day— @UUID[Compendium.pf1.spells.Item.44nj6jzo81o9mng9] (if the shadow lord has 11 or more Hit Dice), @UUID[Compendium.pf1.spells.Item.btoow6tyv39443gh].
>
> A creature created with @UUID[Compendium.pf1.spells.Item.ed7fvzc2p4m6n7a2] or @UUID[Compendium.pf1.spells.Item.44nj6jzo81o9mng9] that would normally have a @UUID[Compendium.pf1.monster-templates.Item.8kHcvgFNoGObDhQ8] or @UUID[Compendium.pf1.monster-templates.Item.kDaBd3zlTauG2f9n] template (such as a bear) instead gains the shadow creature template.
>
> **Special Qualities**: A shadow lord gains the following special quality.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.QWeiwOLntur04Bbu inline=true]
>
> **Ability Scores**: Dex +4, Cha +4.
>
> **Skills**: A shadow lord gains a +8 racial bonus on all Stealth checks.

**Mechanical encoding:** `changes`: 3
  - `4` → `dex`  (untyped)
  - `8` → `skill.ste`  (racial)
  - `4` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shadow
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 238
**Foundry id:** `mAGorlufp4G4ElbH`

> "Shadow creature" is an inherited template that can be added to any living creature, referred to hereafter as the base creature. A shadow creature retains all the base creature's statistics and abilities except as noted here.
>
> **Challenge Rating**: Same as the base creature +1.
>
> **Alignment**: Any (usually nongood).
>
> **Type**: The base creature's type changes to outsider, and it gains the augmented subtype. Do not recalculate BAB, saves, or skill ranks.
>
> **Senses**: As the base creature plus darkvision 60 feet and low-light vision.
>
> **Defensive Abilities**: A shadow creature gains DR and resistance to cold and electricity based on its Hit Dice, as noted on the following table.
>
>
> **Hit Dice**
>
>
> **Resist Cold and Electricity**
>
>
> **DR**
>
>
> 1–4
>
>
> 5
>
>
> —
>
>
> 5–10
>
>
> 10
>
>
> 5/magic
>
>
> 11+
>
>
> 15
>
>
> 10/magic
>
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.5h5eg7TxHk9QqZrR inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.RJiH37Y3Ckb2O9yx inline=true]

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shadowbound Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `9CyU0311Ga0lFkDr`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> A shadowbound creature has lost its color and capacity for joy and pleasure. Quick Rules: darkvision 120 ft.; +1 to AC; +2 on rolls based on Con; +2 hp/HD; light blindness; can’t gain morale bonuses; regretful gaze (shaken 1 round, 30 ft., Will save negates, DC = 10 + 1/2 HD + Cha modifier); after taking 3 points of damage per HD in a single attack, gain a +2 profane bonus on attack rolls, damage rolls, saving throws, and skill checks for 1 round.
>
> **Rebuild Rules:**
>
> **Senses** darkvision 120 ft.;
>
> **AC** gain a deflection bonus to AC equal to 1/4 CR (minimum 1);
>
> **Weaknesses** light blindness, can’t gain morale bonuses;
>
> **Special Attacks** regretful gaze (shaken 1 round, 30 ft., Will negates, DC = 10 + 1/2 HD + Cha modifier); after taking 3 points of damage per HD in a single attack, gain a +2 profane bonus on attack rolls, damage rolls, saving throws, and skill checks for 1 round;
>
> **Ability Scores** +4 Con.

**Mechanical encoding:** `changes`: 2
  - `4` → `con`  (untyped)
  - `max(1, floor(@details.cr.total / 4))` → `ac`  (deflection)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shadowfire Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `MVbXYal4w0UE5RR5`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** No
>
> Created through rituals that suffused elemental fire with the dark corruption of shadow, shadowfire creatures were spawned from the evil cult led by Yarrix (see page 103). Cruelly transformed from their true forms by their ancient creators, they flicker between existence and nothingness, reality and oblivion, feeding on pain and flame and the screams of those who dare stand against them.
>
> "Shadowfire creature" is an inherited template that can be applied to any creature that has the shadow creature template (Pathfinder RPG Bestiary 4 238) and 5 or more Hit Dice, referred to hereafter as the base creature. It retains all the special abilities of the base creature, except as noted here.
>
> **CR:** Same as the base creature + 1.
>
> **Type:** The shadowfire creature gains the elemental and fire subtypes if it does not already have them. Do not recalculate the creature’s base attack bonus, saves, or skill ranks.
>
> **Defensive Abilities:** A shadowfire creature gains immunity to fire and cold, and loses any vulnerability it has to fire or cold. In addition, a shadowfire creature gains the following defensive abilities.
>
> *Fire Absorption (Su): *A shadowfire creature regains 1 hit point for each point of fire damage it would take from normal fire, a flaming weapon, or magical fire were it not immune. Any hit points gained above the shadowfire creature’s full normal hit point total are temporary hit points that disappear after 5 minutes.
>
> *Incorporeal Step (Su):* When a shadowfire creature moves, it gains the incorporeal subtype and special ability, including a deflection bonus to AC equal to its Charisma bonus. It loses the incorporeal subtype and special ability when it stops moving.
>
> **Special Attacks:** A shadowfire creature gains the following special attack.
>
> *Shadow Touch (Su): *A shadowfire creature’s touch chills the target and saps away its life energy. All of a shadowfire creature’s slam attacks and attacks with natural weapons deal an additional 1d6 points of negative energy damage to living creatures.
>
> **Spell-Like Abilities:** A shadowfire creature can use the shadow step spell (Pathfinder RPG Ultimate Magic 237) as a spell-like ability once per day, with a caster level equal to its Hit Dice. If it has 11 or more Hit Dice, it can instead use this ability three times per day.
>
> **Ability Scores:** Str +2, Dex +2, Cha +4.

**Mechanical encoding:** `changes`: 3
  - `2` → `str`  (untyped)
  - `4` → `cha`  (untyped)
  - `2` → `dex`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shaggra Ogre
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `d9NwazitKj1cmH6f`

> **Acquired/Inherited Template** Inherited**Simple Template** Yes**Usable with Summons** No
>
> Ogres with the shaggra template are covered in long, matted fur, and have stunted legs and massive oversized arms, similar to apes. They move on all fours and smash enemies with their giant fists.
>
> **Quick Rules:** +2 on all attack rolls, damage rolls, and Strength checks; gains two slam attacks (1d6); gains the grab and constrict monster special abilities.
>
> **Rebuild Rules:** Ability Scores +4 Strength; Attacks gains 2 slam attacks (1d6, grab, constrict); Special Abilities grab, constrict.

**Mechanical encoding:** `changes`: 1
  - `4` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Siabrae
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `2FTfKnrHp20G4j8l`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> When druids are faced with threats to the natural world, they are steadfast and, at times, relentless in their defense of the land. Even in the face of overwhelming odds—an incursion of demons from the Abyss, a creeping plague of necromantic corruption, an unstoppable blight of magical radiation, or a similar supernatural threat to the natural world—some sects of druids refuse to give up or abandon their duties. In these tragic cases, the desperate druids adopt the blasphemous tactic of accepting the corruption into themselves and becoming powerful undead guardians. They fight on not only against the original source of the corruption, but against all living creatures, for these druids become siabraes, and are filled with bitterness and hatred for all others—particularly other druids, whom they regard as cowards. Siabraes do not form spontaneously; they arise only as the result of the horrific Welcome the Blighted Soul ritual.
>
> "Siabrae" is an acquired template that can be added to any druid who successfully performs the welcome the blighted soul ritual (hereafter referred to as the base creature). A siabrae can’t have the blight druid archetype. A siabrae retains all the base creature’s statistics and special abilities except as noted here.
>
> **CR:** Base creature’s CR + 2.
>
> **Alignment:** Neutral evil.
>
> **Type:** The creature’s type changes to undead with the earth subtype. Do not recalculate BAB, saves, or skill ranks.
>
> **Senses:** A siabrae gains darkvision and tremorsense, both with a range of 60 feet.
>
> **Armor Class:** A siabrae has a +10 natural armor bonus or the creature’s normal bonus, whichever is better.
>
> **Hit Dice:** Change the creature’s racial Hit Dice to d8s. All Hit Dice derived from class levels are unchanged. As an undead, a siabrae uses its Charisma modifier to determine its bonus hit points (rather than using its Constitution modifier).
>
> **Defensive Abilities:** In addition to all the abilities granted by its undead traits, a siabrae gains channel resistance +4, DR 10/ adamantine and bludgeoning, and immunity to fire. A siabrae also gains the following defensive ability.
>
> *Blighted Rebirth (Su):* When a siabrae is destroyed, it can attempt a DC 20 Fortitude save in order to avoid this end. The siabrae automatically succeeds at this saving throw if it is in contact with blighted or diseased terrain. On a successful save, the siabrae’s body crumbles to dust as the blighted earth absorbs its essence. Its enduring essence begins forming a new body in a random location within 1d10 miles (this new location must contain a mass of unworked stone large enough for the siabrae’s body to form within). This process takes 1d10 days, after which the siabrae emerges from the stone with a peal of thunder, though without any of its gear.
>
> **Speed:** A siabrae gains a burrow speed equal to its land speed, as well as the earth glide ability.
>
> **Attacks:** A siabrae grows a pair of stony antlers from its skull, granting it a gore attack that deals damage based on the siabrae’s size, but as if it were one size category larger than its actual size. This gore attack is always a primary attack, even when the siabrae also uses weapons. If the siabrae wishes, it can retain these antlers in any form it assumes via wild shape. Shards of the stony antlers break off in wounds—a siabrae’s antlers constantly replenish themselves as these shards break off. A creature damaged by a siabrae’s gore attack must succeed at a Fortitude save (DC = 10 + 1/2 the siabrae’s HD + the siabrae’s Charisma modifier) or turn to stone permanently.
>
> **Special Attacks and Abilities:** A siabrae retains all the special attacks and abilities of the base creature. If it had the ability to use wild shape, it retains this ability, but it can assume only the form of creatures that cannot fly. Any form it assumes (via wild shape or polymorph effects) and any creature it summons appears diseased, malnourished, or even in an advanced state of decay, although these are cosmetic effects; they do not impact actual game statistics. In addition, a siabrae gains the following special attacks.
>
> *Blight Mastery (Su):* Any of a siabrae’s spells or effects that would normally be restricted to affecting animals can also affect undead animals.
>
> *Blightbond (Ex):* A siabrae has an unholy bond with the blighted earth. It loses any animal companion or access to domains it had from its druidic nature bond ability. In place of nature bond, the siabrae’s close ties to the blighted landscape grant it one of the following cleric domains: Animal, Death, Destruction, Earth, Madness, or Repose. The blightbond ability otherwise functions the same as nature bond.
>
> **Ability Scores:** Str +2, Wis +2, Cha +2. Being undead, a siabrae has no Constitution score.
>
> **Skills:** A siabrae gains a +8 racial bonus on Perception, Sense Motive, and Stealth checks. A siabrae always treats Intimidate, Knowledge (planes), Knowledge (religion), Sense Motive, and Stealth as class skills. Otherwise, a siabrae’s skills are the same as those of the base creature. Feats: A siabrae gains Toughness as a bonus feat.

**Mechanical encoding:** `changes`: 7 (showing first 5)
  - `2` → `str`  (untyped)
  - `2` → `cha`  (untyped)
  - `2` → `wis`  (untyped)
  - `8` → `skill.sen`  (racial)
  - `8` → `skill.ste`  (racial)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Silverblood Lycanthrope
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `f74QNc7i96Pn4vbM`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Silverblood werewolves are a rare type of lycanthrope found almost exclusively in the Arthfell Forest. They are the survivors of an experimental process conceived by jeweler-turned-werewolf Garrick Argentum, and developed by his allies in the Shadow Pack, a group of werewolf druids in the forest. The Shadow Pack conducted an eldritch ritual involving successive exposures to pure silver under the light of the full moon in an attempt to desensitize the werewolves to the deadly touch of silver (in theory, this process could also produce other types of silverblood lycanthropes). The experiment was a success, and the werewolves lost their vulnerability. Swollen with pride at their new ability, the Shadow Pack joined forces with the hobgoblins of the wood and attacked the town of Olfden. Turned back after a savage battle known as the Night of Silver Blood, the werewolves sought to regroup and prepare a new assault, but on the night of the next new moon they discovered a fatal flaw in their blasphemous rite. Tied now more than ever to the lunar cycle, most of the silverblood werewolves wasted away and died when the moon darkened. Even those few that survived are greatly weakened when each new moon comes, though the surge of power when the moon waxes full still earns them great respect, and many have found positions of leadership among the werewolves of the wood.
>
> Though the Night of Silver Blood was a failure, many hobgoblins and werewolves within the Arthfell Forest believe it is proof that major towns and even small cities could be totally ravaged by a somewhat larger, betterprepared force spearheaded by silverblood werewolves. Some groups of silverblood werewolves continue to maintain close connections to the local hobgoblins, forming war parties with them that raid farther and farther from the woods during the nights of the full moon. If one such band were to have a noteworthy success, its leaders might be able to gather a much larger force that could once again threaten Olfden or similarly sized settlements.
>
> "Silverblood lycanthrope" is an acquired lycanthrope template (Pathfinder RPG Bestiary 196) that can be added to any humanoid or lycanthrope. If added to a creature that already has the lycanthrope template, it replaces that template.
>
> **Challenge Rating:** Same as base creature +2 (this includes the +1 increase for being a natural lycanthrope).
>
> **Size and Type:** The creature (referred to hereafter as the base creature) gains the shapechanger subtype. The silverblood lycanthrope takes on the characteristics of the base animal. Its hybrid form is the same size as the base animal or the base creature, whichever is larger.
>
> **AC:** In animal or hybrid form the silverblood lycanthrope gains a +4 natural armor bonus to AC.
>
> **Defensive Abilities:** A silverblood lycanthrope gains DR 1/- in animal or hybrid form. When the moon is at least half full, this increases to DR 3/-, and during the nights of the full moon the silverblood lycanthrope gains DR 10/-.
>
> **Speed:** Same as the base creature or base animal, depending on which form the lycanthrope is using. Hybrids use the base creature's speed.
>
> **Melee:** A lycanthrope gains a bite attack in animal and hybrid forms according to the base animal.
>
> **Special Attacks:** A silverblood lycanthrope retains all the special attacks, qualities, and abilities of the base creature. In animal or hybrid form it gains any special attacks associated with its natural weapons. A silverblood lycanthrope also gains low-light vision, scent, and the following abilities.
>
> *Change Shape (Su):* All silverblood lycanthropes have three forms: a humanoid form, an animal form, and a hybrid form. Equipment does not meld with the new form when changing between humanoid and hybrid form, but does when changing between those forms and animal form. A silverblood lycanthrope can shift to any of its three forms as a move action. A slain silverblood lycanthrope reverts to its humanoid form, although it remains dead.
>
> *Curse of Lycanthropy (Su): *A silverblood lycanthrope's bite attack in animal or hybrid form infects a humanoid target with lycanthropy (Fortitude DC 15 negates). If the victim's size is not within one size category of the silverblood lycanthrope, this ability has no effect. Creatures that become lycanthropes as a result of this curse become standard afflicted lycanthropes rather than silverblood lycanthropes.
>
> *Lunar Sympathy (Su):* A silverblood lycanthrope is filled with enthusiastic vigor when the light of the moon is strongest. When the moon is at least half full, a silverblood lycanthrope gains the benefit of bless whenever it is outdoors at night. On nights of the full moon, a silverblood lycanthrope gains the effect of heroism rather than bless, and retains the benefit indoors.
>
> When the moon is less than half full, a silverblood lycanthrope becomes fatigued during the night. On nights of the new moon, a silverblood lycanthrope becomes fatigued during the day and each night becomes exhausted and takes 1d4 points of Constitution damage. A successful DC 20 Fortitude save reduces the Constitution damage by half.
>
> *Lycanthropic Empathy (Ex):* In any form, silverblood lycanthropes can communicate and empathize with animals of the same species as the base animal. They can use Diplomacy to alter such an animal's attitude, and when so doing gain a +4 racial bonus on the check. Due to their near-legendary reputation, silverblood lycanthropes gain a +8 racial bonus on Diplomacy and Intimidate checks against standard lycanthropes of the same base creature.
>
> **Ability Scores:** +2 Wis, -2 Cha in all forms; +2 Str, +2 Con in hybrid and animal forms. Silverblood lycanthropes have enhanced senses but are not fully in control of their emotions and animalistic urges. In addition to these adjustments to the base creature's statistics, a silverblood lycanthrope's ability scores change when she assumes animal or hybrid form. In human form, the silverblood lycanthrope's ability scores are unchanged from the base creature's form. In animal and hybrid forms, the silverblood lycanthrope's ability scores are the same as the base creature's or the base animal's, whichever ability score is higher.

**Mechanical encoding:** `changes`: 5
  - `4` → `nac`  (untyped)
  - `2` → `str`  (untyped)
  - `2` → `wis`  (untyped)
  - `2` → `con`  (untyped)
  - `-2` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Skeletal Champion
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 252
**Foundry id:** `4BOuZZKzHQ8FdVEG`

> Some skeletons retain their intelligence and cunning, making them formidable warriors. These undead are far more powerful than their mindless kin, and many gain class levels.
>
> "Skeletal Champion" is an acquired template that can be added to any corporeal creature (other than an undead) that has a skeletal system (referred to hereafter as the base creature) and a minimum Intelligence of 3.
>
> **CR:** A skeletal champion's CR is +1 higher than a normal skeleton with the same HD.
>
> **Type:** The creature's type becomes undead. It keeps subtypes save for alignment subtypes and subtypes that indicate kind.
>
> **Alignment:** Any evil.
>
> **Armor Class:** Natural armor as per skeleton.
>
> **Hit Dice:** Change all of the creature's racial HD to d8s, then add 2 racial Hit Dice to this total (creatures without racial HD gain 2). HD from class levels are unchanged.
>
> **Defensive Abilities:** A skeletal champion gains DR 5/bludgeoning, channel resistance +4, and immunity to cold. It also gains all of the standard undead traits.
>
> **Speed:** As standard skeleton.
>
> **Attacks:** As standard skeleton.
>
> **Abilities:** Str +2, Dex +2. As undead, it has no Constitution score.
>
> **BAB:** Its BAB for racial HD equals 3/4 of its HD.
>
> **Skills:** Gains skill ranks per racial Hit Die equal to 4 + its Int modifier. Class skills for racial HD are Climb, Disguise, Fly, Intimidate, Knowledge (arcana), Knowledge (religion), Perception, Sense Motive, Spellcraft, and Stealth. Skills gained from class levels remain unchanged.
>
> **Feats:** A skeletal champion gains Improved Initiative as a bonus feat.
>
> **Saves:** Base save bonuses for racial Hit Dice are Fort +1/3 HD, Ref +1/3 HD, and Will +1/2 HD + 2.

**Mechanical encoding:** `changes`: 4
  - `1` → `bonusFeats`  (untypedPerm)
  - `lookup(@size, 0, 0, 0, 1, 2, 2, 3, 6, 10)` → `nac`  (untyped)
  - `2` → `dex`  (untyped)
  - `2` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Skeleton
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 250-251
**Foundry id:** `pnAOF0zWjd0rrYzC`

> Skeletons are the animated bones of the dead, brought to unlife through foul magic. While most skeletons are mindless automatons, they still possess an evil cunning imparted to them by their animating force—a cunning that allows them to wield weapons and wear armor.
>
> "Skeleton" is an acquired template that can be added to any corporeal creature (other than an undead) that has a skeletal system (referred to hereafter as the base creature).
>
> **Challenge Rating:** Depends on Hit Dice, as follows:
>
>
> **HD**
>
>
> **CR**
>
>
> **XP**
>
>
> 1/2
>
>
> 1/6
>
>
> 65
>
>
> 1
>
>
> 1/3
>
>
> 135
>
>
> 2–3
>
>
> 1
>
>
> 400
>
>
> 4–5
>
>
> 2
>
>
> 600
>
>
> 6–7
>
>
> 3
>
>
> 800
>
>
> 8–9
>
>
> 4
>
>
> 1,200
>
>
> 10–11
>
>
> 5
>
>
> 1,600
>
>
> 12–14
>
>
> 6
>
>
> 2,400
>
>
> 15–17
>
>
> 7
>
>
> 3,200
>
>
> 18–20
>
>
> 8
>
>
> 4,800
>
>
> **Alignment:** Always neutral evil.
>
> **Type:** The creature's type changes to undead. It retains any subtype except for alignment subtypes (such as good) and subtypes that indicate kind (such as giant). It does not gain the augmented subtype. It uses all the base creature's statistics and special abilities except as noted here.
>
> **Armor Class:** Natural armor bonus changes as follows:
>
>
> **Skeleton Size**
>
>
> **Natural Armor Bonus**
>
>
> Tiny or smaller
>
>
> +0
>
>
> Small
>
>
> +1
>
>
> Medium or Large
>
>
> +2
>
>
> Huge
>
>
> +3
>
>
> Gargantuan
>
>
> +6
>
>
> Colossal
>
>
> +10
>
>
> **Hit Dice:** A skeleton drops any HD gained from class levels and changes racial HD to d8s. Creatures without racial HD are treated as if they have 1 racial HD. If the creature has more than 20 Hit Dice, it can't be made into a skeleton by the animate dead spell. A skeleton uses its Cha modifier (instead of its Con modifier) to determine bonus hit points.
>
> **Saves:** Base save bonuses are Fort +1/3 HD, Ref +1/3 HD, and Will +1/2 HD + 2.
>
> **Defensive Abilities:** A skeleton loses the base creature's defensive abilities and gains DR 5/bludgeoning and immunity to cold. It also gains all of the standard immunities and traits possessed by undead creatures.
>
> **Speed:** A winged skeleton can't use its wings to fly. If the base creature flew magically, so can the skeleton. All other movement types are retained.
>
> **Attacks:** A skeleton retains all the natural weapons, manufactured weapon attacks, and weapon proficiencies of the base creature, except for attacks that can't work without flesh. A creature with hands gains one claw attack per hand; the skeleton can strike with each of its claw attacks at its full attack bonus. A claw attack deals damage depending on the skeleton's size (see Natural Attacks). If the base creature already had claw attacks with its hands, use the skeleton claw damage only if it's better.
>
> **Special Attacks:** A skeleton retains none of the base creature's special attacks.
>
> **Abilities:** A skeleton's Dexterity increases by +2. It has no Constitution or Intelligence score, and its Wisdom and Charisma scores change to 10.
>
> **BAB:** A skeleton's base attack bonus is equal to 3/4 of its Hit Dice.
>
> **Skills:** A skeleton loses all skill ranks possessed by the base creature and gains none of its own.
>
> **Feats:** A skeleton loses all feats possessed by the base creature and gains @UUID[Compendium.pf1.feats.Item.Uuiu3p982omhMEPj] as a bonus feat.
>
> **Special Qualities:** A skeleton loses most special qualities of the base creature. It retains any extraordinary special qualities that improve its melee or ranged attacks.

**Mechanical encoding:** `changes`: 5
  - `lookup(@size, 0, 0, 0, 1, 2, 2, 3, 6, 10)` → `nac`  (untyped)
  - `1` → `bonusFeats`  (untypedPerm)
  - `2` → `dex`  (racial)
  - `10` → `wis`  (base)
  - `10` → `cha`  (base)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Sorcerer (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 248-249
**Foundry id:** `BQXwnVCbFR0UgDhH`

> Sorcerer creatures can use a variety of powerful spells and abilities to devastate their foes. Select a sorcerer creature's bloodline when the template is added. A sorcerer creature's CR increases by 2 if the creature has 8 or more HD, and it increases by 3 if the creature has 14 or more HD.
>
> **Quick Rules:** +2 on all rolls based on Cha; gains the bloodline arcana and bloodline powers of its chosen bloodline (using its HD – 2 as its sorcerer level to determine the effect and DC [minimum 1]); can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.yaL9DS7Eu5OmsxnV] (see the Sorcerer Spells Known table below) using its HD as its CL and gaining two spell slots for every level of spells known.
>
> **Rebuild Rules: Special Attacks** bloodline arcana, bloodline powers (using its HD – 2 as its sorcerer level to determine the effect and DC [minimum 1]); **Sorcerer Spells** can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.yaL9DS7Eu5OmsxnV] (see the Sorcerer Spells Known table below) using its HD as its CL and gaining two spell slots for every spell level known; **Ability Scores** +4 Charisma.
>
> #### Sorcerer Spells Known
>
>
>
> **HD**
>
>
> **0**
>
>
> **1**
>
>
> **2**
>
>
> **3**
>
>
> **4**
>
>
> **5**
>
>
> **6**
>
>
> **7**
>
>
> **8**
>
>
> **9**
>
>
> 1-4
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 5-7
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 8-10
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 11-13
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 14--16
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 17-19
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> 20-22
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> 23-25
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> 26+
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1

**Mechanical encoding:** `changes`: 2
  - `2` → `chaSkills`  (untyped)
  - `2` → `chaChecks`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Sorcerer (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 248-249
**Foundry id:** `TpzJ6KRAGlpGvPNx`

> Sorcerer creatures can use a variety of powerful spells and abilities to devastate their foes. Select a sorcerer creature's bloodline when the template is added. A sorcerer creature's CR increases by 2 if the creature has 8 or more HD, and it increases by 3 if the creature has 14 or more HD.
>
> **Quick Rules:** +2 on all rolls based on Cha; gains the bloodline arcana and bloodline powers of its chosen bloodline (using its HD – 2 as its sorcerer level to determine the effect and DC [minimum 1]); can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.yaL9DS7Eu5OmsxnV] (see the Sorcerer Spells Known table below) using its HD as its CL and gaining two spell slots for every level of spells known.
>
> **Rebuild Rules: Special Attacks** bloodline arcana, bloodline powers (using its HD – 2 as its sorcerer level to determine the effect and DC [minimum 1]); **Sorcerer Spells** can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.yaL9DS7Eu5OmsxnV] (see the Sorcerer Spells Known table below) using its HD as its CL and gaining two spell slots for every spell level known; **Ability Scores** +4 Charisma.
>
> #### Sorcerer Spells Known
>
>
>
> **HD**
>
>
> **0**
>
>
> **1**
>
>
> **2**
>
>
> **3**
>
>
> **4**
>
>
> **5**
>
>
> **6**
>
>
> **7**
>
>
> **8**
>
>
> **9**
>
>
> 1-4
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 5-7
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 8-10
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 11-13
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 14--16
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 17-19
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> 20-22
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> 23-25
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> 26+
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1

**Mechanical encoding:** `changes`: 1
  - `4` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Soulbound Construct
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `cF55FLZJSJV9PvU4`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> A soulbound construct is a once-living creature that has had its soul bound to a construct host that serves as its new body.
>
> "Soulbound construct" is an acquired template that can be applied to a construct (referred to hereafter as the host construct); this construct draws several of its statistics from a living corporeal creature with an Intelligence score of 4 or more (referred to hereafter as the base creature) whose soul is contained within a soul focus. A soulbound construct uses all the host construct’s statistics and special abilities except as noted here.
>
> **Challenge Rating:** If the base creature has 10 or fewer Hit Dice, host construct’s CR + 1; if the base creature has 11 or more Hit Dice, host construct’s CR + 2.
>
> **Alignment:** As per base creature.
>
> **Type:** A soulbound construct gains any alignment subtypes that the base creature had.
>
> **Armor Class:** A host construct gains a deflection bonus to AC equal to the base creature’s Charisma modifier.
>
> **Weakness:** A soulbound construct retains all the weaknesses of the host construct and gains the following additional weakness.
>
> *Susceptible to Mind-Affecting Effects (Ex):* A soulbound construct is not immune to mind-affecting effects.
>
> **Special Attacks:** A soulbound construct gains the following special attack.
>
> *Spell-Like Abilities (Ex):* A soulbound construct has one or more alignment-based spell-like abilities, based upon the base creature’s HD. If the base creature has 1–4 HD, the soulbound construct can cast the first spell-like ability listed in the table below for its alignment once per day. If the base creature has 5–10 HD, it can cast the first listed spell-like ability three times per day and the second ability once per day. If the base creature has 11–16 HD, it can cast the first listed spell-like ability at will, the second ability three times per day, and the third ability once per day. If the base creature has 17–20 HD, it can cast the first and second listed spell-like abilities at will and the third ability three times per day. The caster level for these abilities is equal to the base creature’s Hit Dice. The save DC for these abilities is based on the base creature’s Intelligence, Wisdom, or Charisma, whichever is highest.
>
>
>
>
>  **Alignment** 
>  **First Ability** 
>  **Second Ability** 
>  **Third Ability** 
>
>
>  Lawful good 
>  *Hold person* 
>  *Dimensional anchor* 
>  *Repulsion* 
>
>
>  Neutral good 
>  *Heroism* 
>  *Greater invisibility* 
>  *Heal* 
>
>
>  Chaotic good 
>  *Blink* 
>  *Shout* 
>  *Prismatic spray* 
>
>
>  Lawful neutral 
>  *Suggestion* 
>  *Lesser globe of invulnerability* 
>  *Blade barrier* 
>
>
>  Neutral 
>  *Deep slumber* 
>  *Hold monster* 
>  *Greater dispel magic* 
>
>
>  Chaotic neutral 
>  *Rage* 
>  *Confusion* 
>  *Disintegrate* 
>
>
>  Lawful evil 
>  *Minor image* 
>  *Crushing despair* 
>  *Antilife shell* 
>
>
>  Neutral evil 
>  *Inflict moderate wounds* 
>  *Enervation* 
>  *Harm* 
>
>
>  Chaotic evil 
>  *Stinking cloud* 
>  *Contagion* 
>  *Eyebite* 
>
>
>
>
> **Ability Scores:** The host construct replaces its Intelligence, Wisdom, and Charisma scores with those of the base creature.
>
> **Skills:** A soulbound construct gains the Intelligence-, Wisdom-, and Charisma-based skills of the soul held in the soul focus. If the host construct already has any of these skills, select the higher total bonus between that of the base creature and that of the host construct.
>
> **Feats:** A soulbound construct gains the base creature’s feats as bonus feats. Feats that can’t be used by the host construct are not added in this way.
>
> **Special Qualities:** A soulbound construct gains the following special qualities.
>
> *Bind Soul (Su):* The process to bind the soul focus to the construct body takes 1d10 days of continual concentration, and the target construct can attempt a Will save (DC = 10 + half the base creature’s Hit Dice + the base creature’s Intelligence, Wisdom, or Charisma modifier, whichever is highest) to negate the effect. Mindless constructs receive no save against this effect.
>
> *Soul Focus (Su):* The base creature’s soul lives within a gem called a soul focus. As long as the soul focus remains intact, a soulbound construct gains the abilities granted by this template, and it retains the base creature’s personality, memories, and thoughts, as well as its alignment, mental ability scores, feats, and skills that are based on mental ability scores. It does not retain racial modifiers to those skills (if any). A soul focus has hardness 8, 12 hit points, and a break DC of 20.

**Mechanical encoding:** `changes`: 1
  - `@abilities.cha.mod` → `ac`  (deflection)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Spore Zombie
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `1kpZeLHXJWe988Oh`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> There are certain evil fungal creatures (such as fungus queens, but also rare fungal growths or extraplanar blights upon the wild) that can infest vermin with spores that have been infused with sinister power and negative energy. These foul spores grow quickly in the body of a dead vermin, eventually bursting from its head to form disturbing, antler-like growths. At the same time, the spores animate the vermin as an intelligent undead creature.
>
> These are then known as spore zombies.
>
> "Spore zombie" is an acquired template that can be added to any vermin, which is referred to hereafter as the base creature.
>
> **Challenge Rating:** The base creature’s CR + 1.
>
> **Alignment:** Always chaotic evil.
>
> **Type:** The creature’s type changes to undead. It retains any subtypes and gains the augmented subtype.
>
> **Armor Class:** A spore zombie gains a +2 bonus to the base creature’s natural armor.
>
> **Hit Dice:** The base creature’s Hit Dice + 2.
>
> **Saves:** The creature’s base save bonuses are Fort +1/3 Hit Dice, Ref +1/3 Hit Dice, and Will +1/2 Hit Dice + 2.
>
> **Defensive Abilities:** Spore zombies gain all of the qualities and immunities granted by the undead type, and retain all defensive abilities that the base creature had.
>
> **Attacks:** A spore zombie retains all of the base creature’s natural attacks.
>
> **Special Attacks:** A spore zombie retains all of the base creature’s special attacks, plus the following (any special attack save DCs that are Constitution-based are now Charisma-based).
>
> *Spore Burst (Ex):* Once per day as a swift action, a spore zombie can spray a cloud of spores through the area. This deals 2d6 points of damage to the spore zombie and creates a cloud of spores that fills an area equal to the spore zombie’s reach. Any creature in this area must succeed at a Fortitude save or be nauseated by the spores for 1d6 rounds. Vermin that fail this save become infested for 24 hours. If an infested vermin dies during this time, it rises as a spore zombie 1d6 rounds after its death.
>
> **Abilities:** Strength +4. A spore zombie gains an Intelligence score of 10 and a Charisma score equal to the base creature’s Constitution score. They do not have a Con score.
>
> **Feats:** A spore zombie gains feats as appropriate for its Hit Dice, and gains Toughness as a bonus feat.
>
> **Skills:** A spore zombie gains skill points equal to 4 + Int modifier per Hit Die (4 points per HD for most). Climb, Fly, Perception, and Stealth are class skills.
>
> **Languages:** A spore zombie can understand Abyssal but can’t speak.

**Mechanical encoding:** `changes`: 2
  - `2` → `nac`  (untyped)
  - `4` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Steam-Powered Construct
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `ZFhMSVXrakOKSiYv`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** No
>
> Though some scholars may argue about who exactly created the first steam-powered clockwork, the secret of their manufacture is now out. Savvy engineers have started to create faster and more powerful clockwork contraptions in the form of marvels blending arcane heat sources with large boilers to create pressured steam that powers the complex constructs.
>
> "Steam-powered clockwork" is an inherited template that can be added to any construct (referred to hereafter as the base creature). A steam-powered clockwork retains all the base creature’s statistics and special abilities except as noted here. Creating a steam-powered clockwork increases the skill check DC to craft the construct by 5.
>
> **Challenge Rating:** Base creature’s CR + 2.
>
> **Type:** The base creature gains the augmented and clockwork subtypes. If the base creature did not have the clockwork subtype, add the vulnerable to electricity, swift reactions, and difficult to create special qualities from that subtype.
>
> **Hit Points:** Double the bonus hit points based on size granted by the construct creature type (if any).
>
> **Defensive Abilities:** Engineers design steam-powered clockworks’ mechanisms to withstand the heat and pressure of the steam that powers it. As such, steam-powered clockworks gain fortification and fire resistance based on their Hit Dice.
>
>
>
>
>  **Hit Dice** 
>  **Fortification** 
>  **Fire Resistance** 
>
>
>  1-4 
>  25% 
>  5 
>
>
>  5-8 
>  25% 
>  10 
>
>
>  9-12 
>  50% 
>  10 
>
>
>  13-16 
>  50% 
>  20 
>
>
>  17-20 
>  75% 
>  20 
>
>
>  20+ 
>  75% 
>  30 
>
>
>
>
> **Attacks:** A steam-powered construct diverts excess heat to its melee weapon systems, dealing 1d6 points of additional fire damage with natural attacks and with any metal weapons it wields.
>
> **Special Attacks:** Engineers utilize a steam-powered clockwork’s pressurized steam to further enhance its capabilities. A steam-powered clockwork gains steam blast plus one additional special attack from the list below. The save DC against a steam-powered construct’s special attack is equal to 10 + half the steam-powered construct’s Hit Dice.
>
> *Self-Destruction (Ex):* When a steam-powered clockwork’s hit points are reduced to 10% of its total or fewer but are still above 0, the creature self-destructs on its next turn. It bursts into an explosion of metal scraps and steam that deals 1d6 points of fire and slashing damage per Hit Die the steam-powered clockwork has to creatures within the steam-powered clockwork’s natural reach (minimum 5 feet). A target can attempt a Reflex save for half damage.
>
> *Steam Blast (Ex):* As a standard action, the steam-powered construct can release a jet of steam at a target within 30 feet. If the construct succeeds at a ranged touch attack, the jet deals 1d6 points of fire damage for every 2 Hit Dice the steam-powered construct has (minimum 1d6).
>
> *Steam Horn (Ex): *As a standard action, the steam-powered construct can unleash a loud blast of sound and a cone of steam that deafens targets and deals 1d6 points of fire damage for every 2 Hit Dice the steam-powered construct has (minimum 1d6). A target can attempt a Fortitude save to take half damage and negate the deafened condition. Medium and smaller constructs release a 15-foot cone, Large and Huge constructs release a 30-foot cone, and Gargantuan and Colossal constructs release a 60-foot cone. This ability is usable once every 1d4 rounds.
>
> **Special Qualities:** A steam-powered clockwork loses the winding and efficient winding special qualities and gains a steam engine with a boiler instead of a clockwork winding mechanism that requires a special key. To power and move the construct, valves collect and release pressurized steam from the boiling water.
>
> *Heat Management (Ex): *When a steam-powered clockwork ignores any amount of fire damage due to its fire resistance, the steam-powered clockwork gains the benefits of haste, increases the additional fire damage applied to melee attacks to 2d6, and loses its fortification ability for 1 round. Whenever a steam-powered clockwork takes cold damage, it gains the effects of slow and loses the extra fire damage applied to melee attacks for 1 round. A steam-powered construct can negate either effect with a successful Fortitude save (DC = 10 + the amount of energy damage taken). Steam-powered clockwork golems are affected by magical fire and cold spells, which bypass their immunity to magic special ability.
>
> *Increased Locomotion (Ex):* Steam-powered clockworks increase all movement speeds by 10 feet and gain Run as a bonus feat.
>
> *Steam Engine (Ex):* An alchemically treated boiler contains the superheated water that supplies power to a steam engine. A steam-powered clockwork can remain active for 1 week per Hit Die with a full boiler. Anytime the steam-powered clockwork uses a special attack granted by this template, reduce the remaining duration of activity by 1 day (to a minimum of 1 day).
>
> **Ability Scores:** Str +4, Dex +4.

**Mechanical encoding:** `changes`: 2
  - `4` → `str`  (untyped)
  - `4` → `dex`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Sunbaked Zombie
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `dFfB1SnoXFEqOBwM`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> Sun-baked zombies most often rise near pyramids and other burial sites in hot deserts, where latent necromantic energy lingers from countless arcane rituals and restless spirits. As such, sunbaked zombies are primarily found among the dunes of Osirion and the other nations that make up northern Garund. Typically animated in isolation, sunbaked zombies rarely form hordes like normal zombies, but when entire caravans fall to thirst and the desert sun, all of its members might rise as these terrible undead.
>
> When one intentionally raises a sunbaked zombie using animate dead, the body to be raised must be left out in the sun’s rays for a full 12 hours and must be salted every hour during this time to hasten its desiccation. Spell effects that produce light work for this purpose only if they count as actual sunlight, and even then they must be combined with desecrate. Casting the animating spell at night always fails; the sun must be out and directly beating down on the corpse. Without the intense magical focus of a spell, it takes many days for the corpse to absorb enough sun and necromantic energy to rise spontaneously.
>
> "Sunbaked zombie" is an acquired template that can be added to any corporeal creature (other than undead), referred to hereafter as the base creature.
>
> **CR:** This depends on the creature’s new total number of Hit Dice, as follows.
>
>
>
>
>  **HD** 
>  **CR** 
>  **XP** 
>
>
>  1 
>  1/2 
>  200 
>
>
>  2 
>  1 
>  400 
>
>
>  3–4 
>  2 
>  600 
>
>
>  5–6 
>  3 
>  800 
>
>
>  7–8 
>  4 
>  1,200 
>
>
>  9–10 
>  5 
>  1,600 
>
>
>  11–12 
>  6 
>  2,400 
>
>
>  13–16 
>  7 
>  3,200 
>
>
>  17–20 
>  8 
>  4,800 
>
>
>  21–24 
>  9 
>  6,400 
>
>
>  25–28 
>  10 
>  9,600 
>
>
>
>
> **Alignment:** Always neutral evil.
>
> **Type:** The creature’s type changes to undead. It retains any subtypes except for alignment subtypes (such as good) and subtypes that indicate kind (such as giant). It does not gain the augmented subtype.
>
> **Armor Class**: The natural armor bonus is based on the creature’s size.
>
>
>
>
>  **Sunbaked Zombie Size** 
>  **Natural Armor Bonus** 
>
>
>  Tiny or smaller 
>  +0 
>
>
>  Small 
>  +1 
>
>
>  Medium 
>  +2 
>
>
>  Large 
>  +3 
>
>
>  Huge 
>  +4 
>
>
>  Gargantuan 
>  +7 
>
>
>  Colossal 
>  +11 
>
>
>
>
> **Hit Dice:** Drop Hit Dice gained from class levels (to a minimum of 1) and change racial HD to d8s. Sunbaked zombies gain additional HD as noted on the following table. Sunbaked zombies use their Charisma modifiers to determine bonus hit points (instead of Constitution).
>
>
>
>
>  **Sunbaked Zombie Size** 
>  **Bonus Hit Dice** 
>
>
>  Tiny or smaller 
>  — 
>
>
>  Small or Medium 
>  +1 HD 
>
>
>  Large 
>  +2 HD 
>
>
>  Huge 
>  +4 HD 
>
>
>  Gargantuan 
>  +6 HD 
>
>
>  Colossal 
>  +10 HD 
>
>
>
>
> **Saves:** A sunbaked zombie’s base save bonuses are Fort +1/3 HD, Ref +1/3 HD, and Will +1/2 HD + 2.
>
> **Defensive Abilities:** A sunbaked zombie loses the base creature’s defensive abilities and gains DR 5/slashing and resist fire 10 (or immunity to fire if it has 11 HD or more), as well as all of the standard immunities and traits granted by the undead type.
>
> **Speed:** Winged sunbaked zombies can still fly, but their maneuverability drops to clumsy. If the base creature flew magically, so can the sunbaked zombie. Retain all other movement types.
>
> **Attacks:** A sunbaked zombie retains all natural weapons, manufactured weapon attacks, and weapon proficiencies of the base creature. It also gains a slam attack that deals damage based on the sunbaked zombie’s size, but as if it were one size category larger than its actual size (Pathfinder RPG Bestiary 301–302).
>
> **Special Attacks:** A sunbaked zombie retains none of the base creature’s special attacks, but gains the following.
>
> *Death Throes (Su): *When a sunbaked zombie is destroyed, its body explodes in a burst of stale dust. Adjacent creatures must succeed at a Fortitude save or be staggered for 1d4+1 rounds. The DC is equal to 10 + 1/2 the sunbaked zombie’s Hit Dice + the sunbaked zombie’s Cha modifier. Creatures that don’t breathe are immune to this effect.
>
> *Fiery Gaze (Su):* A sunbaked zombie’s eye sockets flicker with a small flame that gives light equivalent to that of a candle. As a standard action, a sunbaked zombie can direct its gaze against a single creature within 30 feet of it. A creature targeted must succeed at a Fortitude save or take 1d6 points of fire damage. If the sunbaked zombie has 5 or more Hit Dice, its fiery gaze deals 2d6 points of fire damage, and this damage increases by an additional 1d6 points of fire damage for every 4 additional Hit Dice the sunbaked zombie possesses. A creature damaged by this effect must succeed at a Reflex save or catch fire. Each round, a burning creature can attempt a Reflex save to quench the flames; failure results in another 1d6 points of fire damage. Flammable items worn by a creature must also save or take the same damage as the creature. If a creature is already on fire, it suffers no additional effects from a fiery gaze. The save DC is Charisma-based.
>
> **Abilities:** Str +2. A sunbaked zombie has no Con or Int score, and its Wis and Cha become 10.
>
> **BAB:** A sunbaked zombie’s base attack bonus is equal to 3/4 of its Hit Dice.
>
> **Skills:** A sunbaked zombie has no skill ranks.
>
> **Feats:** A sunbaked zombie loses all feats possessed by the base creature and gains Toughness as a bonus feat.
>
> **Special Qualities:** A sunbaked zombie loses most special qualities of the base creature. It retains any extraordinary special qualities that improve its melee or ranged attacks.

**Mechanical encoding:** `changes`: 1
  - `2` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Taxidermic Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1133 (PZO1133) p. 240-241
**Foundry id:** `qoHQEdnaA5CdZEkn`

> Taxidermic creatures are the work of obsessed individuals seeking to use their alchemical or occult talents to preserve and reanimate lifeless beings. The abilities of taxidermic creatures often pale in comparison to those of their living counterparts, as they are bereft of intelligence or an animate life force to guide them. Instead, taxidermic creatures possess a rudimentary form of instinct, though they are still able to follow basic instructions from their creators.
>
> Less refined than the magic used to animate undead, golems, and other constructs, the creation of a taxidermic creature is at best an inaccurate science. There is no one method of crafting a taxidermic creature, so each result is different. Every creature crafted in such a manner is prone to inherent defects based on the materials used or shortcuts taken during the process, and may or may not be able to obey its creators commands in a satisfactory manner. Because of taxidermic creatures' limited mental faculties, their creators must be extremely careful and literal when commanding them.
>
> Left unattended, taxidermic creatures stand in place, having no need to drink, eat, or sleep. Unless given specific commands, the actions of these creatures are unpredictable. Each taxidermic creature behaves differently, depending on the quirks of its individual construction. Some taxidermic creatures move and act like prowling animals, while others move with the rigidity and unerring purpose of animated objects. Some twisted taxidermists have gone so far as to create taxidermic humanoids, aberrations, and even fey.
>
> "Taxidermic creature" is an acquired template that can be added to any corporeal creature (other than constructs or undead), referred to hereafter as the base creature.
>
> **Challenge Rating:** This depends on the creature's original number of Hit Dice, as noted on the following table, and is further adjusted based on its size, as noted in the Hit Dice entry below.
>
>
> **Hit Dice**
>
>
> **CR**
>
>
> 1
>
>
> 1/4
>
>
> 2
>
>
> 1/2
>
>
> 3-4
>
>
> 1
>
>
> 5-6
>
>
> 2
>
>
> 7-8
>
>
> 3
>
>
> 9-10
>
>
> 4
>
>
> 11-12
>
>
> 5
>
>
> 13-16
>
>
> 6
>
>
> 17-20
>
>
> 7
>
>
> 21-24
>
>
> 8
>
>
> 25-28
>
>
> 9
>
>
> **Alignment:** Always neutral.
>
> **Type:** The creature's type changes to construct. It retains all subtypes except for alignment subtypes (such as good) and subtypes that indicate kind. It does not gain the augmented subtype. It uses all the base creature's statistics and special abilities except as noted here.
>
> **Senses:** The creature gains darkvision 60 feet and lowlight vision if it does not already possess them.
>
> **Armor Class:** The taxidermic creature's natural armor bonus is based on its size.
>
>
> **Size**
>
>
> **Natural Armor Bonus**
>
>
> Tiny or smaller
>
>
> +0
>
>
> Small
>
>
> +1
>
>
> Medium
>
>
> +2
>
>
> Large
>
>
> +3
>
>
> Huge
>
>
> +4
>
>
> Gargantuan
>
>
> +7
>
>
> Colossal
>
>
> +11
>
>
> **Hit Dice:** Remove Hit Dice gained from class levels (minimum of 1) and change all racial Hit Dice to d10s. As constructs, taxidermic creatures gain a number of bonus hit points based on their size. This information is repeated in the table below. Taxidermic creatures also gain bonus Hit Dice based on their size, as noted on the following table.
>
>
> **Size**
>
>
> **Bonus Hit Dice**
>
>
> **Bonus Construct hp**
>
>
> **CR Increase**
>
>
> Tiny or smaller
>
>
> —
>
>
> —
>
>
> —
>
>
> Small
>
>
> —
>
>
> +10
>
>
> —
>
>
> Medium
>
>
> —
>
>
> +20
>
>
> —
>
>
> Large
>
>
> +1 HD
>
>
> +30
>
>
> +1
>
>
> Huge
>
>
> +2 HD
>
>
> +40
>
>
> +1
>
>
> Gargantuan
>
>
> +3 HD
>
>
> +60
>
>
> +1
>
>
> Colossal
>
>
> +4 HD
>
>
> +80
>
>
> +2
>
>
> **Saves:** The creature's base save bonuses are Fortitude +1/3 Hit Dice, Reflex +1/3 Hit Dice, and Will +1/3 Hit Dice.
>
> **Defensive Abilities:** Taxidermic creatures lose their defensive abilities and gain all the qualities and immunities granted by the construct type.
>
> **Weaknesses:** A taxidermic creature gains the following weakness.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.EK6ehTRvcfkAyYUC inline=true]
>
> **Speed:** Reduce the base speed of a taxidermic creature by 10 feet, to a minimum of 20 feet. Winged taxidermic creatures can fly, but their maneuverability drops to clumsy. If the base creature flew magically, the taxidermic creature loses this ability. Retain all other movement types.
>
> **Attacks:** A taxidermic creature retains all natural weapons, manufactured weapon attacks, and weapon proficiencies of the base creature. It also gains a slam attack that deals damage based on the taxidermic creature's size.
>
> **Special Attacks:** A taxidermic creature retains none of the base creature's special attacks.
>
> **Ability Scores:** Strength –2, Dexterity –2. A taxidermic creature has no Constitution or Intelligence score. Its Wisdom becomes 10 and Charisma becomes 3.
>
> **Base Attack Bonus:** A taxidermic creature's base attack bonus is equal to 3/4 of its Hit Dice, even though most constructs have base attack bonuses equal to their Hit Dice.
>
> **Skills:** A taxidermic creature has no skill ranks. It loses all racial bonuses on skill checks that are not directly related to its physical form.
>
> **Feats:** A taxidermic creature loses all feats possessed by the base creature, and does not gain feats as its Hit Dice increase.
>
> **Special Qualities:** A taxidermic creature loses most special qualities of the base creature. It retains any extraordinary special qualities that improve its melee or ranged attacks.

**Mechanical encoding:** `changes`: 7 (showing first 5)
  - `-2` → `str`  (untyped)
  - `lookup(@size, 0, 0, 0, 1, 2, 3, 4, 7, 11)` → `nac`  (untyped)
  - `3` → `cha`  (untyped)
  - `lookup(@size, 0, 0, 0, 10, 20, 30, 40, 60, 80)` → `mhp`  (untyped)
  - `-ifelse(lte(@attributes.speed.land.base - 10, 20), @attributes.speed.land.base - 20, 10)` → `landSpeed`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Terror Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `XRIfX0iS6TRzs5Ov`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** Yes
>
> Creatures with the terror template are warped by prolonged contact with the Negative Energy Plane. They are terrifying to behold and have developed special resistances and attacks. A terror creature’s quick and rebuild rules are the same.
>
> **Rebuild Rules:**
>
> **Alignment** changes to NE;
>
> **Senses** gains darkvision 60 ft.;
>
> **Aura** fear (as fear spell, 20 ft., Will save DC 10 + 1/2 terror creature’s racial HD + creature’s Charisma modifier);
>
> **Defensive Abilities** negative energy absorption (Su; heals 1 hit point for every 3 points of damage that negative energy attacks would otherwise deal; a terror creature gets no saving throw against negative energy effects);
>
> **Immune** fear effects

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Thicken Ogre
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `b95YEbR3GE3mLuoJ`

> **Acquired/Inherited Template** Inherited**Simple Template** Yes**Usable with Summons** No
>
> These tall, bone-thin ogres have thick, bark-like skin and spiked growths all over their bodies, and their hands end in sharp, thorn-like claws.
>
> **Quick Rules:** +2 on AC, –1 hp/HD, and –1 on Fortitude saves and Constitution checks; gains 2 claw attacks (1d6); +4 racial bonus on Stealth checks in forests.
>
> **Rebuild Rules:** Ability Scores –2 Constitution, +2 natural armor bonus; Attacks gains 2 claw attacks (1d6); Special +4 racial bonus on Stealth checks in forests.

**Mechanical encoding:** `changes`: 2
  - `2` → `nac`  (untyped)
  - `-2` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Trompe l'Oleil
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `es3RMR9PqdUJfoxn`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** No
>
> Trompe l’oeil creatures are life-sized portraits animated by powerful magic or occult phenomena. Able to move and talk, these constructs can also step out of their frames to become three-dimensional beings. Born from artistic masterpieces, trompe l’oeils can easily pass for their original models, though close examination reveals that they are not flesh and blood, but only layers of paint. Trompe l’oeils can be created to act as guardians and spies, or on occasion, a painting will animate spontaneously. Rarely, a portrait is so lifelike, a nascent spirit is able to inhabit it. Believing itself to be as good as or better than the original, such a trompe l’oeil seeks to eliminate and replace the painting’s subject.
>
> "Trompe l’oeil" is an inherited template that can be added to any corporeal creature that has an Intelligence score (referred to hereafter as the base creature).
>
> **Challenge Rating:** Base creature’s CR + 1.
>
> **Alignment:** A trompe l’oeil usually has the same alignment as its creator or the base creature. A trompe l’oeil that seeks to destroy its original model, however, has an evil alignment (but the same alignment on the chaotic/lawful axis).
>
> **Type:** The creature’s type changes to construct. Do not recalculate BAB, saves, or skill ranks.
>
> **Armor Class:** A trompe l’oeil gains a bonus to AC based on its HD, as noted in the following table. If it is depicted wearing armor or a shield, these items are masterwork and gain an enhancement bonus (or equivalent armor special abilities) when worn by the trompe l’oeil, as indicated in the table. If the trompe l’oeil is depicted without armor, add the armor enhancement bonus to its natural armor bonus instead. Armor and shields equipped by a trompe l’oeil melt into puddles of nonmagical paint when the creature is destroyed.
>
>
>
>
>  **Trompe l'Oeil HD** 
>  **Armor Enhancement Bonus** 
>  **Shield Enhancement Bonus** 
>
>
>  1-4 
>  — 
>  — 
>
>
>  5-8 
>  +1 
>  — 
>
>
>  9-12 
>  +2 
>  +1 
>
>
>  13-16 
>  +3 
>  +1 
>
>
>  17+ 
>  +4 
>  +2 
>
>
>
>
> **Hit Dice:** Change all of the creature’s racial Hit Dice to d10s. All Hit Dice derived from class levels remain unchanged. As constructs, trompe l’oeils gain a number of additional hit points as noted in the following table.
>
>
>
>
>  **Tromp l'Oeil Size** 
>  **Bonus Hit Points** 
>
>
>  Tiny or smaller 
>  — 
>
>
>  Small 
>  +10 
>
>
>  Medium 
>  +20 
>
>
>  Large 
>  +30 
>
>
>  Huge 
>  +40 
>
>
>  Gargantuan 
>  +60 
>
>
>  Colossal 
>  +80 
>
>
>
>
> **Defensive Abilities:** A trompe l’oeil gains the standard immunities and traits of construct creatures. In addition, it gains rejuvenation.
>
> *Rejuvenation (Su):* When a trompe l’oeil is destroyed, it reforms 2d4 days later on its original canvas (see page 243). The only way to permanently destroy a trompe l’oeil is to destroy the original canvas before the creature reforms.
>
> **Attacks:** A trompe l’oeil retains all weapon proficiencies and natural weapons. If it’s depicted wielding any manufactured weapons, the weapons are masterwork and gain an enhancement bonus (or equivalent weapon special abilities) when wielded by it. The bonus is based on its HD, as noted in the following table. A trompe l’oeil’s weapons melt into puddles of nonmagical paint when the creature is destroyed.
>
>
>
>
>  **Trompe l'Oeil HD** 
>  **Weapon Enhancement Bonus** 
>
>
>  1-3 
>  — 
>
>
>  4-6 
>  +1 
>
>
>  7-9 
>  +2 
>
>
>  10-12 
>  +3 
>
>
>  13-15 
>  +4 
>
>
>  16+ 
>  +5 
>
>
>
>
> **Abilities:** A trompe l’oeil has no Constitution score.
>
> **Skills:** A trompe l’oeil gains a +10 racial bonus on Disguise checks to appear as the base creature. It also receives a +5 bonus on Bluff checks to pretend to be the base creature and a +5 bonus on Stealth checks to appear as part of a painting.
>
> **Special Qualities:** A trompe l’oeil gains the following special qualities.
>
> *Autotelic (Ex):* A trompe l’oeil uses its Charisma score in place of its Constitution score when calculating hit points, Fortitude saves, and any special ability that relies on Constitution (such as when calculating a breath weapon’s DC).
>
> *Enter Painting (Su):* As a standard action, a trompe l’oeil can enter a painting it touches. When it does so, its physical body disappears, and its image appears in the painting. The trompe l’oeil can use its normal senses and attempt Perception checks to notice anything occurring near the painting. While within a painting, the trompe l’oeil can talk and move anywhere within the picture or even temporarily alter it (such as by picking a flower in the painting). It cannot use any spells or other abilities while within an image. In addition, the trompe l’oeil gains the freeze universal monster ability to appear as part of the painting. The trompe l’oeil can leave the painting as a move action. Once it leaves the painting, the image immediately reverts to the appearance it had before the trompe l’oeil entered. If someone destroys or damages the painting, the trompe l’oeil is unharmed, but exits the image.

**Mechanical encoding:** `changes`: 2
  - `if(gte(@attributes.hd.total, 9), 1) + if(gte(@attributes.hd.total, 17), 1)` → `sac`  (untyped)
  - `ceil(@attributes.hd.total / 4 - 1)` → `aac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Tsukumogami
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1133 (PZO1133) p. 253
**Foundry id:** `HrbdB5h8EiWyMHo5`

> When an object reaches the 100-year anniversary of its crafting, sometimes it forms an amalgam with a kami, creating a creature known as a tsukumogami. Tsukumogami run the gamut in personality, outlook, and function. Objects that are well kept and cared for often form curious and helpful tsukumogami. Most commonly, tsukumogami are mischievous and frightening but not actually malign. Tsukumogami formed from objects that have been abandoned, neglected, or misused are dangerous both to the humans around and to themselves, as their uncontrolled rage might eventually transform them into oni.
>
> Tsukumogami is an acquired template that can be added to any animated object (referred to hereafter as the base creature). A tsukumogami retains all the base creature's statistics and special abilities except as noted here.
>
> **Challenge Rating:** Base creature's CR + 2.
>
> **Alignment:** Any.
>
> **Type:** The creature's type changes to outsider (kami, native). Tsukumogami have good Reflex and Will saves, so increase the base creature's Reflex and Will saves to 2 + 1/2 its Hit Dice + the relevant ability modifier.
>
> **Armor Class:** A tsukumogami's natural armor bonus increases by 2.
>
> **Hit Dice:** Retain the base creature's construct bonus hit points from size (if any). As outsiders, tsukumogami gain bonus hit points from high Constitution scores.
>
> **Spell-Like Abilities:** Tsukumogami gain spell-like abilities based on their size, usable at will. The caster level is equal to the tsukumogami's Hit Dice.
>
>
> **Size**
>
>
> **Abilities**
>
>
> Tiny+
>
>
> @UUID[Compendium.pf1.spells.Item.7u45op4znvtkvgv3] (self only), @UUID[Compendium.pf1.spells.Item.mtxqp85izkb20djq], @UUID[Compendium.pf1.spells.Item.24zg8a05hqum3e6j], @UUID[Compendium.pf1.spells.Item.pumqlg17ixbjp6s3] (self only)
>
>
> Small+
>
>
> @UUID[Compendium.pf1.spells.Item.oylikodnyku2zewu] (self only), @UUID[Compendium.pf1.spells.Item.0onqjy8gfgop1xsi]
>
>
> Medium+
>
>
> @UUID[Compendium.pf1.spells.Item.plou8h168bfn5hq6], @UUID[Compendium.pf1.spells.Item.kq916lznxo0ig68v]
>
>
> Large+
>
>
> @UUID[Compendium.pf1.spells.Item.7d6sv5ecvi7kho3m], @UUID[Compendium.pf1.spells.Item.x23pz2agjub1eh89]
>
>
> Huge+
>
>
> @UUID[Compendium.pf1.spells.Item.x5hunybxpzhd3gcm] (self only), @UUID[Compendium.pf1.spells.Item.gvfrhibwwuar2rcf] (self only, no volume limit)
>
>
> Gargantuan+
>
>
> @UUID[Compendium.pf1.spells.Item.k9iu3d82hlo7coct] (each casting ends any previous castings)
>
>
> Colossal
>
>
> @UUID[Compendium.pf1.spells.Item.7wcosqq4v4x0bvep] (self only)
>
>
> **Special Qualities and Defensive Abilities:** Because it grows additional features such as a tongue, arms, or legs, a tsukumogami gains the additional attack animated object quality without spending Construction Points, and all its attacks increase their damage dice by one step. A tsukumogami can gain 10 bonus hit points as an additional option costing 1 CP. It gains the freeze special quality. As kami, tsukumogami gain immunity to petrification and polymorph effects; resist acid 10, electricity 10, and fire 10; telepathy 100 feet; fast healing 5; merge with ward; and ward. Though a tsukumogami loses its construct type, it keeps its hardness, low-light vision, and all its construct immunities. It can still be affected by spells that affect objects or constructs. A tsukumogami is always merged with its ward, and unlike most kami, it forms an amalgam with its ward, so it can move and communicate while merged.
>
> **Ability Scores:** A tsukumogami has a 15 Intelligence, 17 Wisdom, and 14 Charisma. A Medium tsukumogami receives a +4 bonus to Strength, a +4 bonus to Dexterity, and a Constitution score of 19. These ability scores are adjusted for size.
>
> **Skills:** A tsukumogami has a number of skill points per racial Hit Die equal to 6 + its Intelligence modifier. Its racial class skills are the base outsider class skills plus Disguise, Knowledge (history), Perform (any one), and Sleight of Hand.

**Mechanical encoding:** `changes`: 7 (showing first 5)
  - `17` → `wis`  (untyped)
  - `2` → `nac`  (untyped)
  - `14` → `cha`  (untyped)
  - `ifelse(gte(@size, 4), 4, 0)` → `dex`  (untyped)
  - `15` → `int`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Tulpa
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1133 (PZO1133) p. 254-255
**Foundry id:** `ebelkwSiOkbnwHiT`

> Tulpas are constructed of ideas and imagination. Beings of pure thought (some theorize that they are made of the same mysterious substance as the Astral Plane), tulpas are made physical by a powerful mind that is either psychically attuned or has some amount of latent psychic power.
>
> The exact process that creates a tulpa is not well understood. Sometimes such beings come about after years of practice and meditation followed by an occult ritual. Other times they seem to appear spontaneously, often after their creators suffer traumatic experiences. More often than not, in these latter cases, the creators are children. Such a child witnesses something horrific or far too strange for her nascent imagination to comprehend, and ends up creating an imaginary friend to help her sort through the event and protect her from other potential dangers. While most of these imaginary friends are nothing more than figments of her mind, every so often they manifest as tulpas. Some such tulpas are noble creatures that protect the child who created them, but just as many are malicious entities that subtly torment the child or lead her astray.
>
> While a tulpa is a creature of thought created by the imagination of another being, it has a will and a mind of its own. This often leads to conflict between a tulpa and its creator. In order to protect itself from banishment or worse, a tulpa often attempts to compel others to think and concentrate on its existence. This allows the tulpa to create havens of other "creators" in case its original creator forgets about the tulpa or becomes incapacitated. Nonetheless, even a sadistic tulpa or a tulpa with an actively belligerent creator must protect its creator's life in order to preserve its own existence.
>
> "Tulpa" is an inherited template that can be added to any corporeal creature, referred to hereafter as the base creature. Most tulpas take the form of humanoids, and most of those take the form of their creator, but these creatures can be nearly anything their creator imagines. Tulpas have a strangely parallel existence with unfettered eidolons (@Source[PZO1120;pages=110]), and tulpas with a particularly bizarre form not based on an original creature can be represented as unfettered eidolons instead. A tulpa uses the base creature's stats and abilities except as noted here. A tulpa can be created either intentionally or unintentionally, and this distinction affects the way the template applies to the base creature.
>
> **Challenge Rating:** Base creature's CR + 2.
>
> **Alignment:** Tulpas can have any alignment, and their alignments vary wildly. An intentionally created tulpa's creator can choose the tulpa's alignment. Unintentionally created tulpas can be of any alignment, though in general an unintentionally created tulpa's alignment is in opposition to that of the creature who created it. Tulpas often have alignments that are different from the base creature they resemble—they may manifest as a friendly red dragon, a nightmarishly evil unicorn, or a fun-loving prankster inevitable.
>
> **Type:** The creature's type changes to outsider with the augmented subtype. Do not recalculate the creature's Hit Dice, BAB, or saves.
>
> **Defensive Abilities:** As a being of mental energy, tulpas naturally resist mental attacks. It gains a +4 racial bonus on saving throws to resist mind-affecting effects.
>
> **Psychic Magic:** A tulpa is able to use a limited amount of psychic magic, though only to affect itself or its creator. The tulpa can store a maximum amount of psychic energy equal to 3 + its Hit Dice. The tulpa can use @UUID[Compendium.pf1.spells.Item.0vi272dchokb72pf] (1 PE), @UUID[Compendium.pf1.spells.Item.ndvks6ztnxhj6oxh] (1 PE), @UUID[Compendium.pf1.spells.Item.z6xg1ckozmmx2s3q] (3 PE), @UUID[Compendium.pf1.spells.Item.plou8h168bfn5hq6] (2 PE), and @UUID[Compendium.pf1.spells.Item.91rt7847dbgccbjk] (2 PE) as psychic magic spells. If the tulpa has at least 9 Hit Dice, it can also use @UUID[Compendium.pf1.spells.Item.nn4gjuby3uovsv78] (5 PE), @UUID[Compendium.pf1.spells.Item.iqamm8pyipsnfw96] (5 PE), @UUID[Compendium.pf1.spells.Item.vrzgrnmiz8kmz6di] (4 PE), and @UUID[Compendium.pf1.spells.Item.4mw83czf7b62rar3] (5 PE). A tulpa's caster level equals its Hit Dice.
>
> **Special Qualities:** A tulpa gains the following special qualities.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.8OZeyv2et79LhypP inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.Ycz1qa8O5r7ciFyh inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.hpIEaS3Jnna2fMBR inline=true]
>
> **Skills:** Tulpas know their creators' minds extremely well and are adept at manipulating them. They gain a +8 racial bonus on Bluff, Diplomacy, Intimidate, and Sense Motive checks against their creators.
>
> **Ability Scores:** When a tulpa comes into being intentionally, its creator chooses two of the tulpa's ability scores to increase by 4, and two of its ability scores to increase by 2 (These can be chosen under the "Changes" tab of this window). Otherwise, the ability scores increase randomly. Either way, the tulpa's Intelligence score cannot exceed the Intelligence score of its creator, so if its Intelligence score would be higher than its creator's, reduce its Intelligence to be the same as its creator's instead (an unintentionally created tulpa already at maximum Intelligence never randomly gains an ability score increase to its Intelligence score).

**Mechanical encoding:** `changes`: 4
  - `4` → `str`  (untyped)
  - `4` → `str`  (untyped)
  - `2` → `str`  (untyped)
  - `2` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Unknown
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `FiaLbtxlYdKfg0xi`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> The unknown are terrifying fey creatures that feed off the mental energies of other creatures. Scholars studying the behavior and organization of the unknown speculate they may have originally been fey creatures that somehow reached the Dimension of Dreams and became trapped there, remade by other minds likewise lost in ephemeral dreamscapes. The unknown propagate more of their own kind by eroding humanoids’ psyches until the victims transform into new unknown. Unknown typically choose to victimize those who are already relatively helpless, especially children, but when they transform an accomplished adventurer into one of their own, the result can be truly terrifying.
>
> "Unknown" is an acquired template for any humanoid. Unknown use the base creature abilities, except as noted.
>
> **Challenge Rating:** Base creature’s CR + 2.
>
> **Alignment:** Neutral evil.
>
> **Type:** The creature’s type changes to fey (augmented humanoid). Do not recalculate HD, BAB, or saves.
>
> **Senses:** An unknown gains low-light vision.
>
> **Armor Class:** Natural armor bonus improves by 2.
>
> **Defensive Abilities:** An unknown gains DR 10/cold iron.
>
> **Melee**: An unknown gains two claw attacks (assuming the base creature has two hands). These claws deal 1d6 points of damage if the unknown is Medium (1d4 if Small).
>
> **Special Attacks:** An unknown gains the following special attacks.
>
> *Psyche Erosion (Su):* Once per day, a target affected by an unknown’s victimize ability that sees the unknown’s true appearance must succeed at a Will save (DC = 10 + 1/2 the unknown’s total Hit Dice + the unknown’s Charisma modifier) or take 1d6 points of Charisma damage. A successful save negates the Charisma damage and also ends the unknown’s victimize effect on that target. As long as a creature is the target of an unknown’s victimize ability, it can’t recover the ability damage from psyche erosion, even through magic. If the Charisma damage from psyche erosion is equal to the target’s Charisma score, that creature doesn’t recover ability score damage naturally even if it ceases being the target of victimize. Only magic can fully heal this ability damage.
>
> When its Charisma damage is equal to its Charisma score, the target falls into a nightmare-filled catatonia where it continues to be followed by an unknown. This dream state lasts for 1d4 days, and at the end, the character awakes if its Charisma damage has been reduced to less than its Charisma score. If not, the creature immediately loses all sense of self, becoming an unknown thrall. It replaces its Charisma score with the unknown’s Charisma score, and no longer takes Charisma damage from exposure to the unknown. Over time, typically 1 to 2 weeks, the thrall becomes a new unknown, gaining this template.
>
> The unknown can share its senses with any of its thralls (even if it changes the target of its victimize ability), and as a full-round action, it can assume control of a thrall’s body, as per possessionOA. Typically, an unknown uses this ability to keep the thrall close by until it becomes an unknown. Unknowns often use thralls to lure new victims to its lair.
>
> Psyche erosion is a mind-affecting effect. If your game uses the sanity system (see page 12), the erosion deals 2d6 points of sanity damage instead of Charisma damage, and triggers the catatonia and the transformation into a thrall if the victim’s sanity damage is equal to or exceeds the target’s sanity.
>
> *Victimize (Su):* As a swift action, an unknown can target a single creature within line of sight with this ability. After designating a target, the unknown can’t change the target of this ability for 24 hours, or until the target dies or succeeds at its save against the unknown’s psyche erosion ability. An unknown always knows the exact location of a victimized creature and the shortest route to reach it, even if it is on another plane (similar to a combined discern location and find the path); this is a divination effect and can only be prevented by mind blank and similar effects. A creature can be the target of only one unknown’s victimize ability at a time, and an unknown can victimize only one creature at a time.
>
> **Spell-Like Abilities:** An unknown can use blur, ghost sound, ventriloquism, and vocal alteration (self only) as spell-like abilities at will, with a caster level equal to its Hit Dice.
>
> **Languages:** An unknown gains Aklo as a bonus language. It can’t speak except by using its ventriloquism spell-like ability.
>
> **Special Qualities:** An unknown gains the following.
>
> *Assume Likeness (Su)*: As a standard action while using hallucinatory camouflage, an unknown is able to disguise itself as a specific creature known to the target of its victimize ability. If the victimized creature succeeds at a Will save (at the same DC as in psyche erosion) it negates this effect, and the unknown can’t use this ability again for 24 hours or until it changes victims, whichever comes first. Otherwise, the unknown’s features and mannerisms change to match the creature known to its victim, granting it a +20 circumstance bonus on Disguise checks to impersonate this creature. Unlike hallucinatory camouflage, this ability works against the target of victimize. This is a mind-affecting illusion (glamer) effect.
>
> *Dream Movements (Su): *To the unknown, all worlds are tinted with the shades of nightmares from the Dimension of Dreams, allowing them to defy the laws of physics as they move as if in a dream. An unknown gains an insight bonus to AC equal to its Charisma bonus. It can travel as if by dimension door as a move action at will, but only to enter or leave an area within line of sight of the target of its victimize ability. The victimized creature and the intended destination must both be within long range of the unknown.
>
> *Hallucinatory Camouflage (Su):* As long as an unknown is targeting a creature with its victimize ability, it hides its appearance behind a veil of illusions, appearing to be an unremarkable member of the victimized creature’s race to everyone except the target of victimize. A successful Will save (at the same DC as psyche erosion) allows a creature that interacts with the illusion to disbelieve the effect. This is a mind-affecting illusion (glamer) effect.
>
> **Ability Scores:** +2 Dexterity, +2 Constitution, +2 Intelligence, +4 Charisma.

**Mechanical encoding:** `changes`: 5
  - `4` → `cha`  (untyped)
  - `2` → `int`  (untyped)
  - `2` → `con`  (untyped)
  - `2` → `dex`  (untyped)
  - `2` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Vahana
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1133 (PZO1133) p. 262
**Foundry id:** `kCnCPAaNfB0HPheV`

> Vahanas are steeds of legend, created by the gods. Deities gift vahanas to faithful servants to help them accomplish great deeds or as rewards for the same. Makaras, elephants with crocodile features, are one of the common types of vahana.
>
> Vahana is an acquired template that can be added to any living creature of the animal type. A vahana retains the base creature's statistics and special abilities except as noted here.
>
> **CR:** Base creature's CR + 2.
>
> **Alignment:** Within one step of the vahana's creator deity.
>
> **Type:** The creature's type changes to magical beast, and it gains darkvision 60 feet. Don't recalculate HD, BAB, or saves.
>
> **Armor Class:** Natural armor improves by 3.
>
> **Defensive Abilities:** A vahana gains acid, cold, electricity, and fire resistance 10; DR 10/magic, and spell resistance equal to CR + 11 (maximum 35).
>
> **Speed:** +30 feet for all movement types (up to double the creature's base movement speed).
>
> **Special Abilities:** A vahana gains the following.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.VwKG1tO2k0jDJFpt inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.eEWZY0diX2je9krb inline=true]
>
> **Abilities:** Increase from the base creature as follows: Str +4, Dex +4, Con +4, Int +10, Wis +2, Cha +2.

**Mechanical encoding:** `changes`: 13 (showing first 5)
  - `min(@attributes.speed.fly.base, 30)` → `flySpeed`  (untyped)
  - `min(@attributes.speed.land.base, 30)` → `landSpeed`  (untyped)
  - `10` → `int`  (untyped)
  - `min(@attributes.speed.climb.base, 30)` → `climbSpeed`  (untyped)
  - `2` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Vampire Spawn
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `O6PQCcUIQLwgEKiH`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> The following template can be used to create unique vampire spawn with class levels.
>
> "Vampire spawn" is an acquired template that can be added to any living creature with 4 or more Hit Dice (referred to hereafter as the base creature). A vampire spawn uses the base creature’s stats and abilities except as noted here.
>
> **CR:** Same as the base creature + 1.
>
> **Alignment:** Any evil.
>
> **Type:** The creature’s type changes to undead. Do not recalculate class Hit Dice, BAB, or saves.
>
> **Senses:** A vampire spawn gains darkvision to 60 feet.
>
> **Armor Class:** Natural armor increases to +4, unless the base creature’s natural armor is already +4 or higher.
>
> **Hit Dice:** Change all racial Hit Dice to d8s. Class Hit Dice are unaffected. As undead, vampire spawn use their Cha modifier to determine bonus hit points (instead of Con).
>
> **Defensive Abilities:** A vampire spawn gains channel resistance +2, DR 5/silver, resistance 10 against cold and electricity, and fast healing 2.
>
> **Weaknesses:** A vampire spawn has the same weaknesses of the vampire that created it.
>
> *Resurrection Vulnerability (Su): *A raise dead or similar spell cast on a vampire spawn destroys it (Will negates). Using the spell in this way does not require a material component.
>
> **Melee:** A vampire spawn gains a slam attack if the base creature didn’t have one. Damage for the slam depends on the vampire spawn’s size (see Bestiary 301).
>
> **Special Attacks:** A vampire spawn gains a vampire’s blood drain and dominate special attacks. The vampire who created the spawn can influence a spawn’s dominated creature as if she had dominated it herself.
>
> *Energy Drain (Su): *A creature hit by a vampire spawn’s slam (or other natural weapon) gains 1 negative level. This ability only triggers only once per round.
>
> **Special Qualities:** A vampire spawn gains the gaseous form, shadowless, and spider climb abilities of a vampire.
>
> **Ability Scores:** Cha +2.
>
> **Skills:** Spawn gain a +8 racial bonus on Acrobatics and Stealth checks.
>
> **Feats:** Spawn gain Skill Focus (Perception) as a bonus feat.

**Mechanical encoding:** `changes`: 4
  - `8` → `skill.ste`  (racial)
  - `2` → `cha`  (untyped)
  - `8` → `skill.acr`  (racial)
  - `4` → `nac`  (base)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Vampire
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 270-271
**Foundry id:** `FFZV078TgqxA5GvX`

> "Vampire" is an acquired template that can be added to any living creature with 5 or more Hit Dice (referred to hereafter as the base creature). Most vampires were once humanoids, fey, or monstrous humanoids. A vampire uses the base creature's stats and abilities except as noted here.
>
> **CR:** Same as the base creature + 2.
>
> **AL:** Any evil.
>
> **Type:** The creature's type changes to undead (augmented). Do not recalculate class Hit Dice, BAB, or saves.
>
> **Senses:** A vampire gains darkvision 60 ft.
>
> **Armor Class:** Natural armor improves by +6.
>
> **Hit Dice:** Change all racial Hit Dice to d8s. Class Hit Dice are unaffected. As undead, vampires use their Charisma modifier to determine bonus hit points (instead of Constitution).
>
> **Defensive Abilities:** A vampire gains channel resistance +4, DR 10/magic and silver, and resistance to cold 10 and electricity 10, in addition to all of the defensive abilities granted by the undead type. A vampire also gains fast healing 5. If reduced to 0 hit points in combat, a vampire assumes gaseous form (see below) and attempts to escape. It must reach its coffin home within 2 hours or be utterly destroyed. (It can normally travel up to 9 miles in 2 hours.) Additional damage dealt to a vampire forced into gaseous form has no effect. Once at rest, the vampire is @Condition[helpless;info]. It regains 1 hit point after 1 hour, then is no longer helpless and resumes healing at the rate of 5 hit points per round.
>
> **Weaknesses:** Vampires cannot tolerate the strong odor of garlic and will not enter an area laced with it. Similarly, they recoil from mirrors or strongly presented holy symbols. These things don't harm the vampire—they merely keep it at bay. A recoiling vampire must stay at least 5 feet away from the mirror or holy symbol and cannot touch or make melee attacks against that creature. Holding a vampire at bay takes a standard action. After 1 round, a vampire can overcome its revulsion of the object and function normally each round it makes a DC 25 Will save.
>
> Vampires cannot enter a private home or dwelling unless invited in by someone with the authority to do so.
>
> Reducing a vampire's hit points to 0 or lower incapacitates it but doesn't always destroy it (see fast healing). However, certain attacks can slay vampires. Exposing any vampire to direct sunlight staggers it on the first round of exposure and destroys it utterly on the second consecutive round of exposure if it does not escape. Each round of immersion in running water inflicts damage on a vampire equal to one-third of its maximum hit points—a vampire reduced to 0 hit points in this manner is destroyed. Driving a wooden stake through a helpless vampire's heart instantly slays it (this is a full-round action). However, it returns to life if the stake is removed, unless the head is also severed and anointed with holy water.
>
> **Speed:** Same as the base creature. If the base creature has a swim speed, the vampire is not unduly harmed by running water.
>
> **Melee:** A vampire gains a slam attack if the base creature didn't have one. Damage for the slam depends on the vampire's size (see Natural Attacks). Its slam also causes energy drain (see below). Its natural weapons are treated as magic weapons for the purpose of overcoming damage reduction.
>
> **Special Attacks:** A vampire gains several special attacks. Save DCs are equal to 10 + 1/2 vampire's HD + vampire's Cha modifier unless otherwise noted.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.JRzJ1KADTQyp5Pwt inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.zrZtiRzEMZjGFAOf inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.qSN6gwPwk1bzZ5kU inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.hhVHkuMmR9qs2sHe inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.L68llMM0tJPeSNlS inline=true]
>
> **Special Qualities:** A vampire gains the following.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.pVrzlP0nPShbuPmR inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.8ORQD37xwCGLwxe0 inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.ug9244fDjTiA30ot inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.WrNTjJtIVSNRgnTC inline=true]
>
> **Ability Scores** Str +6, Dex +4, Int +2, Wis +2, Cha +4. As an undead creature, a vampire has no Constitution score.
>
> **Skills** Vampires gain a +8 racial bonus on Bluff, Perception, Sense Motive, and Stealth checks.
>
> **Feats** Vampires gain @UUID[Compendium.pf1.feats.Item.Q1cY8r0Pvb66pMG0], @UUID[Compendium.pf1.feats.Item.h9nHYLxXvIXBTmup], @UUID[Compendium.pf1.feats.Item.JreaiTHdyWFNj3Tb], @UUID[Compendium.pf1.feats.Item.Uuiu3p982omhMEPj], @UUID[Compendium.pf1.feats.Item.0bZf3SDkvVOe2ujH], and @UUID[Compendium.pf1.feats.Item.8snLqsJN4LLL00Nq] as bonus feats.

**Mechanical encoding:** `changes`: 11 (showing first 5)
  - `8` → `skill.blf`  (racial)
  - `8` → `skill.sen`  (racial)
  - `6` → `nac`  (untyped)
  - `2` → `int`  (untyped)
  - `4` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Vampiric Creature
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `aZeRFZvgLbgW3vO0`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** No
>
> Vampiric creatures have been transformed into vampires, and they don’t have to be humanoids. At your discretion, a vampiric creature might have the create spawn ability and could create spawn of its own creature type in addition to humanoid spawn. Non-humanoid vampiric creatures likely have unusual "coffins" that befit their nature.
>
> **Quick Rules:** Counts as undead; darkvision 60 ft.; +1 to AC; +1 on rolls based on Str, Dex, and Cha; undead immunities; fast healing 1* (this includes the ability to escape to its coffin in gaseous form at 0 hp); vampire weaknesses*; slam attack that deals 1d6 points of damage (for Medium creatures) plus energy drain; blood drain*; energy drain (1 level, DC = 10 + 1/2 HD + Charisma modifier); gaseous form*, shadowless*, spider climb*.
>
> **Rebuild Rules:**
>
> **Type** change to undead;
>
> **Senses** darkvision 60 ft.;
>
> **AC** natural armor bonus increases by 1;
>
> **Defensive Abilities** fast healing 1* (this includes the ability to escape to its coffin in gaseous form at 0 hp);
>
> **Weaknesses** vampire weaknesses*;
>
> **Melee** slam attack that deals 1d6 points of damage (for Medium creatures) plus energy drain; Special Attacks blood drain*, energy drain (1 level, DC = 10 + 1/2 HD + Charisma modifier);
>
> **Special Qualities** gaseous form*, shadowless*, spider climb*;
>
> **Ability Scores** +2 Str, +2 Dex, +2 Cha.

**Mechanical encoding:** `changes`: 4
  - `1` → `nac`  (untyped)
  - `2` → `dex`  (untyped)
  - `2` → `str`  (untyped)
  - `2` → `cha`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Venerable (Age Category)
*(feat / misc)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `Bt4NFHWKPeoW0ZfQ`

> You suffer a -6 penalty to your physical ability scores, and gain a +3 to your mental ability scores, due to your age category.

**Mechanical encoding:** `changes`: 6 (showing first 5)
  - `-6` → `con`  (untypedPerm)
  - `3` → `int`  (untypedPerm)
  - `3` → `wis`  (untypedPerm)
  - `3` → `cha`  (untypedPerm)
  - `-6` → `dex`  (untypedPerm)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Vetala
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `bia5VqeoI7mffgSK`

> **Acquired/Inherited Template** Acquired**Simple Template** No**Usable with Summons** No
>
> While most of the Inner Sea’s vampires lust for living blood, the mysterious vetalas hunger for a more intangible force: the energy that infuses mortal minds. Referred to as consciousness or psyche by some, the academics of Vudra— from where most vetalas hail—call this fundamental vital force prana. Regardless of their desire’s name, vetalas prey upon those who show creative promise, possess potent force of will, or seem destined for greatness, draining the most brilliant sources of mortal light to fuel their own unnatural embers. Their dark mastery of life force allows vetalas to possess corpses or even overwhelm the minds of living creatures. With these stolen masks and the resources of abducted lives, they work their foul wills.
>
> Vetalas are said to be the spirits of children "born evil," who never received burial rites upon their deaths. Sometimes one of these evil spirits takes hold of a corpse— not necessarily its own—which becomes its anchor to the mortal world. Such young souls seek out experiences and life energy, becoming as wicked as any other vampire as they endlessly indulge their profane, deathless desires.
>
> "Vetala" is an acquired template that can be added to any living creature with 5 or more Hit Dice (referred to hereafter as the base creature). Most vetalas were once humanoids, fey, or monstrous humanoids. A vetala uses the base creature’s stats and abilities except as noted here.
>
> **CR:** Same as the base creature + 2.
>
> **AL:** Any evil.
>
> **Type:** The creature’s type changes to undead (augmented). Do not recalculate class Hit Dice, BAB, or saves.
>
> **Senses:** A vetala gains darkvision 60 ft.
>
> **Armor Class:** Natural armor improves by +4.
>
> **Hit Dice:** Change all racial Hit Dice to d8s. Class Hit Dice are unaffected. As undead, vetalas use their Charisma modifiers to determine bonus hit points (instead of Constitution).
>
> **Defensive Abilities:** A vetala gains channel resistance +4, DR 10/magic and good, and resistance to fire 10 and electricity 10, in addition to all of the defensive abilities granted by the undead type. A vetala also gains fast healing 5. If reduced to 0 hit points in combat, a vetala is helpless and its fast healing ceases to function for 1 hour. Additional damage dealt to the vetala has no effect. Its body might be subjected to any method of dismemberment or desecration, but after 1 hour—regardless of the state of its remains—it regains 1 hit point, is no longer helpless, and resumes healing at the rate of 5 hit points per round.
>
> **Weaknesses:** Vetalas cannot tolerate the sound of prayers or religious mantras recited by those truly faithful to a good deity. Any character with a good-aligned deity can force a vetala to recoil by dramatically praying as a standard action. Praying doesn’t harm a vetala; it merely keeps the creature at bay. A recoiling vetala must stay at least 5 feet away from a praying character and cannot touch or make melee attacks against it. After 1 round, a vetala can fight past its revulsion and function normally each round it succeeds at a DC 25 Will save. The prayers of those who worship non-good deities or worship no deity have no effect on a vetala.
>
> Reducing a vetala’s hit points to 0 or lower incapacitates it but doesn’t always destroy it (see fast healing). However, consecrating the vetala’s remains and burying the body destroys it forever. A vetala’s body is considered consecrated if it is doused with a vial of holy water and buried, if it is buried in earth affected by the spell consecrate, or if bless, prayer, or a similar divine spell is cast upon it as it is being buried. Digging up a vetala’s corpse or profaning the area where it’s buried does not restore a buried vetala.
>
> **Speed:** Same as the base creature. A vetala also gains a climb speed equal to its base land speed.
>
> **Melee:** A vetala gains two claw attacks if the base creature didn’t have them. A vetala’s claw attacks do damage as a creature once size category larger (for example, a Medium vetala’s claw attack deals 1d6 points of damage). A vetala’s natural weapons are treated as magic weapons for the purpose of overcoming damage reduction.
>
> **Special Attacks:** A vetala gains several special attacks. Save DCs are equal to 10 + 1/2 the vetala’s Hit Dice + the vetala’s Cha modifier unless otherwise noted.
>
> *Drain Prana (Su):* A vetala can drain the mental vitality of a grappled opponent. If the vetala establishes or maintains a pin, it drains this energy, dealing 1d4 points of Charisma damage. Additionally, the victim is affected by the spell modify memory, as if the vetala had spent 5 minutes concentrating. The vetala gains perfect knowledge of any memory it chooses to eliminate using this ability. Vetalas often use this ability to prevent victims from remembering they’ve been attacked.
>
> *Malevolence (Su):* As a full-round action, a vetala can attempt to take control of a helpless living creature’s body, as the spell magic jar (caster level 10th or the vetala’s Hit Dice, whichever is higher), except that it does not require a receptacle. The target can resist the attack with a successful Will save. A creature that successfully saves is immune to that same vetala’s possession for 24 hours. If a creature fails its save, its consciousness and control of its body are subsumed as the vetala takes command of its body. The vetala can remain in control for a number of hours equal to its Charisma modifier or until it decides to end the possession. Whenever the possession ends or the host body is killed, the vetala’s consciousness instantly returns to its body, regardless of distance, so long as it remains on the same plane. If the vetala’s body has been destroyed or moved to another plane, the vetala’s consciousness is destroyed when the possession ends. While possessing another creature, the vetala’s body is empty and vulnerable, though it is instantly aware if its body is disturbed or takes damage.
>
> *Paralysis (Ex): *Any creature struck by a vetala’s claws must make a successful Will save or be paralyzed for 1d4+1 rounds. Elves are immune to this effect.
>
> *Possess Corpse (Su): *As a full-round action, a vetala can possess a Large or smaller corpse just as it can a living body. The vetala’s consciousness leaves its body and takes control of the corpse, animating it as either a skeleton or zombie (depending on its state of decay). The vetala can remain in control of a corpse indefinitely, and can communicate through the body, but cannot use any of its other special abilities. This ability otherwise functions just as malevolence.
>
> **Ability Scores:** Str +4, Dex +2, Int +4, Wis +2, Cha +6. As an undead creature, a vetala has no Constitution score.
>
> **Feats:** Vetalas gain Alertness, Blind-Fight, Deceitful, Improved Initiative, and Skill Focus (Disguise) as bonus feats.
>
> **Skills:** Vetalas gain a +8 racial bonus on Disguise, Perception, Sense Motive, and Stealth checks.

**Mechanical encoding:** `changes`: 10 (showing first 5)
  - `2` → `wis`  (untyped)
  - `6` → `cha`  (untyped)
  - `4` → `str`  (untyped)
  - `2` → `dex`  (untyped)
  - `8` → `skill.sen`  (racial)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Waxwork
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `DrNBs1L4eGk3PGBD`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** No
>
> The practice of making sculptures from wax dates back to the earliest humanoid civilizations. Only the medium of wax can so closely duplicate the transparency of skin. Often, creators use powerful magic to house an animating spirit within the wax model. A created waxwork creature obeys the commands of its creator. Rarely, a wax sculpture animates of it own accord—the result of nearby magic suffusing the wax or a lost spirit in search of a corporeal form. Such waxwork creatures are uncontrolled.
>
> A waxwork creature is the same size as the creature it duplicates, but weighs only half as much.
>
> "Waxwork" is an inherited template that can be added to any Tiny or larger corporeal creature (other than a construct or ooze), referred to hereafter as the base creature.
>
> **Challenge Rating:** Depends on Hit Dice, as follows.
>
>
>
>
>  **Waxwork HD** 
>  **CR** 
>
>
>  1 
>  2 
>
>
>  2-3 
>  3 
>
>
>  4-5 
>  4 
>
>
>  6-7 
>  5 
>
>
>  8-10 
>  6 
>
>
>  11-13 
>  7 
>
>
>  14-16 
>  8 
>
>
>  17-19 
>  9 
>
>
>  20 
>  10 
>
>
>
>
> If the creature is larger or smaller than Medium, adjust the CR according to the table below.
>
>
>
>
>  **Waxwork Size** 
>  **CR** 
>  **Natural Armor Bonus** 
>  **Bonus Hit points** 
>
>
>  Tiny or smaller 
>  -2 
>  +0 
>  — 
>
>
>  Small 
>  -1 
>  +1 
>  +10 
>
>
>  Medium 
>  +0 
>  +2 
>  +20 
>
>
>  Large 
>  +1 
>  +3 
>  +30 
>
>
>  Huge 
>  +2 
>  +4 
>  +40 
>
>
>  Gargantuan 
>  +3 
>  +7 
>  +60 
>
>
>  Colossal 
>  +4 
>  +11 
>  +80 
>
>
>
>
> **Alignment:** Always neutral.
>
> **Type:** The creature’s type changes to construct. It doesn’t retain any subtypes, nor does it gain the augmented subtype. It uses all the base creature’s statistics and special abilities except as noted here.
>
> **Armor Class:** The waxwork creature’s natural armor bonus is based on its size.
>
> **Hit Dice:** Remove HD gained from class levels and change racial HD to d10s. Creatures without racial HD are treated as if they have 1 racial HD. As constructs, waxwork creatures gain additional hit points as noted in the following table.
>
> **Saves:** The creature’s base save bonuses are Fortitude +1/3 HD, Reflex +1/3 HD, and Will +1/3 HD.
>
> **Defensive Abilities:** A waxwork creature loses the base creature’s defensive abilities. It gains waxen regeneration 5 (fire) and immunity to cold. If it has 11 or more HD, the waxen regeneration increases to 10 (fire). It also gains all of the standard immunities and traits possessed by constructs.
>
> *Waxen Regeneration (Su): *This ability functions like regeneration, except the waxwork creature has it without a Constitution score. A waxwork creature reduced to 0 hit points is staggered instead of destroyed while its waxen regeneration is active; it ignores all damage dealt to it that would reduce its hit points below 0. Fire damage causes the waxwork creature’s regeneration to stop functioning on the round following the attack.
>
> **Weaknesses:** A waxwork creature is vulnerable to fire.
>
> **Speed:** A waxwork creature retains movement types, except as follows: It loses burrow and magical flight speeds. Winged waxwork creatures can fly, but maneuverability drops to clumsy. A waxwork creature floats and must succeed at a DC 20 Swim check each round to stay underwater.
>
> **Attacks:** A waxwork creature retains all the natural weapons and weapon proficiencies of the base creature. It also gains a slam attack that deals damage based on the waxwork creature’s size, but as if it were one size category larger than its actual size.
>
> **Special Attacks:** A waxwork creature retains none of the base creature’s special attacks.
>
> **Abilities:** A waxwork creature has no Constitution or Intelligence score, and its Wisdom and Charisma scores change to 10.
>
> **BAB:** A waxwork creature’s base attack bonus is equal to its Hit Dice.
>
> **Skills:** A waxwork creature loses all of the base creature’s skills and gains none of its own.
>
> **Feats:** A waxwork creature loses all of the base creature’s feats and gains Improved Initiative as a bonus feat.
>
> **Special Qualities:** A waxwork creature loses most special qualities of the base creature. It retains any extraordinary special qualities that improve its melee or ranged attacks. A waxwork creature gains the freeze universal monster ability to appear as a wax sculpture.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Winter Fey
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `9HhBrM5RbDURSxeM`

> **Acquired/Inherited Template** Inherited**Simple Template** No**Usable with Summons** Yes
>
> "Winter fey" is an inherited template that can be added to any fey creature without the fire subtype, referred to hereafter as the base creature. A winter fey uses all the base creature’s statistics and special abilities except as noted here.
>
> **CR:** As base creature +1.
>
> **Alignment:** Any evil.
>
> **Type:** The base creature’s type remains fey, but it gains the cold subtype.
>
> **AC:** Natural armor improves by +2.
>
> **Defensive Abilities:** A winter fey retains the base creature’s defensive abilities, and gains the following ability.
>
> *Fast Healing (Su): *A winter fey gains fast healing 3 when in contact with ice or snow.
>
> **Speed:** A winter fey retains the base creature’s normal movement and gains the following.
>
> *Ice Walking (Ex): *A winter fey takes no penalty to speed or on Acrobatics, Climb, or Stealth checks in snowy or icy terrain or weather conditions and can walk across snow crusts or thin ice without breaking through.
>
> **Attacks:** A winter fey retains all the natural weapons, manufactured weapon attacks, and weapon proficiencies of the base creature. A creature with hands gains one claw attack per hand; the winter fey can strike with each of its claw attacks at its full attack bonus. A claw attack deals damage as if the winter fey were one size category larger than its actual size (Pathfinder RPG Bestiary 301–302). If the base creature already had claw attacks with its hands, use the winter fey claw damage only if it’s better.
>
> **Special Attacks:** A winter fey retains the base creature’s special attacks and gains the ones listed below.
>
> *Frigid Touch (Su): *Once per day, a winter fey may attempt a touch attack against a foe; if successful, it deals 1d6 points of Dexterity damage by freezing the blood in its victim’s veins and numbing its victim to the bone.
>
> *Frosty Grasp (Su): *A winter fey’s natural attacks, as well as any weapons it wields, deal an additional 1d6 points of cold damage.
>
> **Abilities:** A winter fey’s Strength and Constitution increase by +2.
>
> **Skills:** A winter fey gains a +4 racial bonus on Survival checks when in cold environments.

**Mechanical encoding:** `changes`: 3
  - `2` → `str`  (untyped)
  - `2` → `con`  (untyped)
  - `2` → `nac`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Winter-Touched Fey
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `pjGvAwhOPtXSIoUy`

> **Acquired/Inherited Template** Acquired**Simple Template** Yes**Usable with Summons** Yes
>
> Chief among the allies of Baba Yaga and the White Witches of Irrisen are the winter-touched, a special breed of fey immune to the harsh weather and low temperatures of the frozen north. Willingly pledging themselves to a wholly evil life, these creatures undergo a complex ritual called the Winter Rite, in which they accept a sliver of ice into their hearts that infuses their bodies with the same supernatural winter perpetuated by the White Witches of Irrisen. The resulting transformation gives the fey’s skin a sickly bluish cast marked with spidery white veins like hoarfrost on glass. These evil fey can channel the power of winter into their attacks, slowing their victims with numbing cold. The winter-touched universally delight in spreading the influence of the White Witches, carrying out the wills of the witches who performed their Winter Rites. The winter-touched display a chilling loyalty that borders on fanaticism—a devotion all but guaranteed given the White Witches’ ability to fatally pierce the hearts of those who fail them with the same slivers of ice the fey so willingly accepted.
>
> #### Winter-Touched Fey
>
> The winter-touched fey simple template can be applied to any creature of the fey type. This template cannot be applied to a creature with the fire subtype. A winter-touched fey’s quick and rebuild rules are the same.
>
> **Rebuild Rules:** The creature’s alignment changes to evil and it gains the cold subtype;
>
> **Special Attacks:** *Numbing Cold (Su) *Any creature hit by a winter-touched creature’s attacks (natural or weapon) must succeed at a Fortitude save or be staggered for 1 round. The save DC is Constitution-based.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Wizard (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 249
**Foundry id:** `h6RJAmL7C9bC0aem`

> A wizard creature is skilled in the ways of arcane magic, and its spellcasting ability is unmatched. Beyond casting damaging spells, a wizard creature can call upon mighty forces to serve the will of the creature and its allies. Select a wizard creature's arcane school when the template is added. A wizard creature's CR increases by 2 if the creature has 7 or more HD, and it increases by 3 if the creature has 13 or more HD.
>
> **Quick Rules:** +2 on all rolls based on Int; gains the @UUID[Compendium.pf1.class-abilities.Item.20JWTam2dn7jjZFV] abilities of its chosen school (using its HD – 2 as its wizard level to determine the effect and DC [minimum 1]); can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.LrjNAKP05lZq2tZZ] (see the Cleric, Druid, and Wizard Spell Slots table on @Source[PZO1130;pages=251]) using its HD as its CL; can designate one item as its @UUID[Compendium.pf1.class-abilities.Item.pW1PNlDcdGl7KuEa] and use that item to cast any one spell it knows once per day.
>
> **Rebuild Rules:** **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.pW1PNlDcdGl7KuEa], @UUID[Compendium.pf1.class-abilities.Item.20JWTam2dn7jjZFV] abilities (using its HD – 2 as its wizard level to determine the effect and DC [minimum 1]); **Wizard Spells** can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.LrjNAKP05lZq2tZZ] (see the Cleric, Druid, and Wizard Spell Slots table on @Source[PZO1130;pages=251]) using its HD as its CL; **Ability Scores** +4 Intelligence.
>
> #### Cleric, Druid, and Wizard Spells Slots
>
>
>
> **HD**
>
>
> **0**
>
>
> **1**
>
>
> **2**
>
>
> **3**
>
>
> **4**
>
>
> **5**
>
>
> **6**
>
>
> **7**
>
>
> **8**
>
>
> **9**
>
>
> 1-3
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 4-6
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 7-9
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 10-12
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 13-15
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 16-18
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> 19-21
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> 22-24
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> 25+
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1

**Mechanical encoding:** `changes`: 2
  - `2` → `intSkills`  (untyped)
  - `2` → `intChecks`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Wizard (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1130 (PZO1130) p. 249
**Foundry id:** `qAh5A72Ufgl2U8Gg`

> A wizard creature is skilled in the ways of arcane magic, and its spellcasting ability is unmatched. Beyond casting damaging spells, a wizard creature can call upon mighty forces to serve the will of the creature and its allies. Select a wizard creature's arcane school when the template is added. A wizard creature's CR increases by 2 if the creature has 7 or more HD, and it increases by 3 if the creature has 13 or more HD.
>
> **Quick Rules:** +2 on all rolls based on Int; gains the @UUID[Compendium.pf1.class-abilities.Item.20JWTam2dn7jjZFV] abilities of its chosen school (using its HD – 2 as its wizard level to determine the effect and DC [minimum 1]); can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.LrjNAKP05lZq2tZZ] (see the Cleric, Druid, and Wizard Spell Slots table on @Source[PZO1130;pages=251]) using its HD as its CL; can designate one item as its @UUID[Compendium.pf1.class-abilities.Item.pW1PNlDcdGl7KuEa] and use that item to cast any one spell it knows once per day.
>
> **Rebuild Rules:** **Special Attacks** @UUID[Compendium.pf1.class-abilities.Item.pW1PNlDcdGl7KuEa], @UUID[Compendium.pf1.class-abilities.Item.20JWTam2dn7jjZFV] abilities (using its HD – 2 as its wizard level to determine the effect and DC [minimum 1]); **Wizard Spells** can cast a small number of @UUID[Compendium.pf1.class-abilities.Item.LrjNAKP05lZq2tZZ] (see the Cleric, Druid, and Wizard Spell Slots table on @Source[PZO1130;pages=251]) using its HD as its CL; **Ability Scores** +4 Intelligence.
>
> #### Cleric, Druid, and Wizard Spells Slots
>
>
>
> **HD**
>
>
> **0**
>
>
> **1**
>
>
> **2**
>
>
> **3**
>
>
> **4**
>
>
> **5**
>
>
> **6**
>
>
> **7**
>
>
> **8**
>
>
> **9**
>
>
> 1-3
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 4-6
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 7-9
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 10-12
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 13-15
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> —
>
>
> 16-18
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> —
>
>
> 19-21
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> —
>
>
> 22-24
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1
>
>
> —
>
>
> 25+
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> ‡
>
>
> 2
>
>
> 2
>
>
> 1

**Mechanical encoding:** `changes`: 1
  - `4` → `int`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Worm that Walks
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1116 (PZO1116) p. 286-287
**Foundry id:** `JBPqanXaxNsVfPJ4`

> When a powerful spellcaster with a strong personality, a lust for life, and a remorselessly evil soul dies and is buried in a graveyard infused with eldritch magic, a strange phenomenon sometimes occurs. The flesh of the decaying body fats and instructs the very worms that gnaw, and these graveworms quicken not only on corruption but upon the spellcaster's memories and magical power. The spellcaster's very soul is consumed in this vile process, only to be split apart to inhabit each of the individual chewing worms in so many fragments. The result is a hideous hive mind of slithering life known as a worm that walks—a mass of worms that clings to the vague shape of the body that granted it this new existence, and can wield the powers and magic the spellcaster had in life. A worm that walks retains memories of its life as a spellcaster before its death, but is not undead—it is a hideous new form of undulant life.
>
> "Worm that walks" is a template that can be added to any evil spellcasting creature. A worm that walks retains all the base creature's statistics and abilities except as noted here.
>
> **CR:** Same as the base creature +2.
>
> **Alignment:** Any evil.
>
> **Type:** The base creature's type changes to vermin. It gains the augmented subtype. Do not recalculate BAB, saves, or skill ranks. Worms that walk are intelligent and do not possess the standard mindless trait of most vermin. Note that while a worm that walks has the ability to discorperate into a swarm, and while its body is made up of countless wriggling worms, it does not itself gain the swarm subtype.
>
> **Size:** Although the worms that make up the worm that walks's body are Fine creatures, the worm that walks is treated as a creature the same size as the base creature.
>
> **Senses:** As the base creature, plus darkvision 60 feet and blindsight 30 feet.
>
> **AC:** The worm that walks loses any natural armor bonus the base creature may have had, but gains an insight bonus to its AC equal to its Wisdom bonus (minimum of +2).
>
> **Hit Dice:** Change the base creature's racial HD to d8s. All HD derived from class levels remain unchanged.
>
> **Defensive Abilities:** A worm that walks retains all of the base creature's defensive abilities and special qualities. It also gains the following additional defensive abilities.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.79AXq4OmataZHDe8 inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.7OTFbD9OXXSdFd3Y inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.mbbVZLwIlTfJ5cmR inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.eTPO2n4gTtAX1MQK inline=true]
>
> **Melee Attacks:** A worm that walks loses any natural attacks the base creature had, but gains a slam attack that deals damage based on its size (see Table 3–1: Natural Attacks by Size, on page 299). This slam has the grab ability and affects creatures up to one size larger than the worm that walks. A worm that walks retains any weapon proficiencies the base creature had.
>
> **Special Attacks:** A worm that walks retains all of the base creature's special attacks. It also gains the following additional special attacks.
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.3gD2efmQPCsQhO0f inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.AXuoptq4z2QazV79 inline=true]
>
> - 
>
> @Embed[Compendium.pf1.template-abilities.Item.psj2v8c5MXmTNNEj inline=true]
>
> **Abilities:** Dex +4, Con +4.
>
> **Skills:** Worms that walk gain a +8 racial bonus on Perception, Sense Motive, and Stealth checks.
>
> **Feats:** Worms that walk gain @UUID[Compendium.pf1.feats.Item.O0e0UCim27GPKFuW] as a bonus feat.

**Mechanical encoding:** `changes`: 8 (showing first 5)
  - `max(2, @abilities.wis.mod)` → `ac`  (insight)
  - `8` → `skill.sen`  (racial)
  - `-(@ac.natural.total)` → `nac`  (untyped)
  - `1` → `bonusFeats`  (untyped)
  - `4` → `dex`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Young (Quick)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 295
**Foundry id:** `44qA5JCwx2Cii3hx`

> Creatures with the young template are immature specimens of the base creature. You can also use this simple template to easily create a smaller variant of a monster. This template cannot be applied to creatures that increase in power through aging or feeding (such as dragons or barghests) or creatures that are Fine-sized.
>
> **Quick Rules:** +2 to all Dex-based rolls, –2 to all other rolls, –2 hp/HD.
>
> **Rebuild Rules:** Size decrease by one category; AC reduce natural armor by –2 (minimum +0); Attacks decrease damage dice by 1 step; Ability Scores –4 Strength, –4 Con, +4 size bonus to Dex.

**Mechanical encoding:** `changes`: 24 (showing first 5)
  - `-2` → `intChecks`  (untyped)
  - `-2` → `sattack`  (untyped)
  - `-2` → `nattack`  (untyped)
  - `-2` → `chaSkills`  (untyped)
  - `-2` → `conSkills`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Young (Rebuild)
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 295
**Foundry id:** `OSt0Qkjh4F8O4ymC`

> Creatures with the young template are immature specimens of the base creature. You can also use this simple template to easily create a smaller variant of a monster. This template cannot be applied to creatures that increase in power through aging or feeding (such as dragons or barghests) or creatures that are Fine-sized.
>
> **Quick Rules:** +2 to all Dex-based rolls, –2 to all other rolls, –2 hp/HD.
>
> **Rebuild Rules:** Size decrease by one category; AC reduce natural armor by –2 (minimum +0); Attacks decrease damage dice by 1 step; Ability Scores –4 Strength, –4 Con, +4 size bonus to Dex.

**Mechanical encoding:** `changes`: 5
  - `-1` → `size`  (untyped)
  - `-min(2, @ac.natural.total)` → `nac`  (untyped)
  - `-4` → `str`  (untyped)
  - `4` → `dex`  (size)
  - `-4` → `con`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Zombie Lord
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1127 (PZO1127) p. 286
**Foundry id:** `m1YCxlSsoQZM75C6`

> Zombie lords are the fleshy counterparts of skeletal champions—intelligent, cunning, and envious of creatures whose bodies aren't rotting away. Despite their decaying flesh, they are not slow like common zombies, and can easily pursue fleeing prey. Zombie lords are more powerful than common zombies and retain their class levels.
>
> "Zombie lord" is an acquired template that can be added to any corporeal creature (other than undead) that has a minimum Intelligence of 3. This corporeal creature is referred to hereafter as the base creature.
>
> **CR**: A zombie lord's CR is 1 higher than that of a normal zombie with the same Hit Dice, plus the normal CR increase for class levels (if any).
>
> **Type**: The creature's type becomes undead. It keeps subtypes except for alignment subtypes and subtypes that indicate kind.
>
> **Alignment**: Any evil.
>
> **Armor Class**: Natural armor as per @UUID[Compendium.pf1.monster-templates.Item.nLoeB640GSsAUWYm].
>
> **Hit Dice**: Change all of the creature's racial Hit Dice to d8s, then add 2 racial Hit Dice to this total (creatures without racial HD gain 2 undead HD). Hit Dice from class levels are unchanged.
>
> **Saving Throws**: Base save bonuses for racial Hit Dice are Fort +1/3 HD, Ref +1/3 HD, and Will +1/2 HD + 2.
>
> **Defensive Abilities**: A zombie lord gains DR 5/slashing and channel resistance +4, in addition to undead traits.
>
> **Speed**: As @UUID[Compendium.pf1.monster-templates.Item.nLoeB640GSsAUWYm].
>
> **Attacks**: As @UUID[Compendium.pf1.monster-templates.Item.nLoeB640GSsAUWYm].
>
> **Abilities**: Str +2, Dex +2. As an undead, it has no Constitution score.
>
> **BAB**: A zombie lord's BAB for its racial HD is equal to 3/4 its HD.
>
> **Skills**: A zombie lord gains skill ranks per racial Hit Die equal to 4 + its Int modifier (class skills as the undead type). Skills gained from class levels remain unchanged.
>
> **Feats**: A zombie lord gains Toughness as a bonus feat.
>
> **Special Qualities**: Unlike a common @UUID[Compendium.pf1.monster-templates.Item.nLoeB640GSsAUWYm], a zombie lord does not gain the @UUID[Compendium.pf1.template-abilities.Item.Ld4w9QurQancak8a] special quality.

**Mechanical encoding:** `changes`: 4
  - `2` → `str`  (untyped)
  - `(4 + @abilities.int.mod) * @attributes.hd.total` → `bonusSkillRanks`  (untyped)
  - `lookup(@size - 2, 0, 1, 2, 3, 4, 7, 11)` → `nac`  (untyped)
  - `2` → `dex`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Zombie
*(feat / template)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 288-289
**Foundry id:** `nLoeB640GSsAUWYm`

> Zombies are the animated corpses of dead creatures, forced into foul unlife via necromantic magic like animate dead. While the most commonly encountered zombies are slow and tough, others possess a variety of traits, allowing them to spread disease or move with increased speed.
>
> Zombies are unthinking automatons, and can do little more than follow orders. When left unattended, zombies tend to mill about in search of living creatures to slaughter and devour. Zombies attack until destroyed, having no regard for their own safety.
>
> Although capable of following orders, zombies are more often unleashed into an area with no command other than to kill living creatures. As a result, zombies are often encountered in packs, wandering around places the living frequent, looking for victims. Most zombies are created using animate dead. Such zombies are always of the standard type, unless the creator also casts haste or remove paralysis to create fast zombies, or contagion to create plague zombies.
>
> "Zombie" is an acquired template that can be added to any corporeal creature (other than an undead), referred to hereafter as the base creature.
>
> **Challenge Rating:** This depends on the creature's new total number of Hit Dice, as follows:
>
>
> **HD**
>
>
> **CR**
>
>
> **XP**
>
>
> 1/2
>
>
> 1/8
>
>
> 50
>
>
> 1
>
>
> 1/4
>
>
> 100
>
>
> 2
>
>
> 1/2
>
>
> 200
>
>
> 3–4
>
>
> 1
>
>
> 400
>
>
> 5–6
>
>
> 2
>
>
> 600
>
>
> 7–8
>
>
> 3
>
>
> 800
>
>
> 9–10
>
>
> 4
>
>
> 1,200
>
>
> 11–12
>
>
> 5
>
>
> 1,600
>
>
> 13–16
>
>
> 6
>
>
> 2,400
>
>
> 17–20
>
>
> 7
>
>
> 3,200
>
>
> 21–24
>
>
> 8
>
>
> 4,800
>
>
> 25–28
>
>
> 9
>
>
> 6,400
>
>
> **Alignment:** Always neutral evil.
>
> **Type:** The creature's type changes to undead. It retains any subtype except for alignment subtypes (such as good) and subtypes that indicate kind. It does not gain the augmented subtype. It uses all the base creature's statistics and special abilities except as noted here.
>
> **Armor Class:** Natural armor is based on the zombie's size:
>
>
> **Zombie Size**
>
>
> **Natural Armor Bonus**
>
>
> Tiny or smaller
>
>
> +0
>
>
> Small
>
>
> +1
>
>
> Medium
>
>
> +2
>
>
> Large
>
>
> +3
>
>
> Huge
>
>
> +4
>
>
> Gargantuan
>
>
> +7
>
>
> Colossal
>
>
> +11
>
>
> **Hit Dice:** Drop HD gained from class levels (minimum of 1) and change racial HD to d8s. Zombies gain a number of additional HD as noted on the following table.
>
>
> **Zombie Size**
>
>
> **Bonus Hit Dice**
>
>
> Tiny or smaller
>
>
> —
>
>
> Small or Medium
>
>
> +1 HD
>
>
> Large
>
>
> +2 HD
>
>
> Huge
>
>
> +4 HD
>
>
> Gargantuan
>
>
> +6 HD
>
>
> Colossal
>
>
> +10 HD
>
>
> **Zombies use their Charisma modifiers to determine bonus hit points (instead of Constitution).
>
> Saves:** Base save bonuses are Fort +1/3 HD, Ref +1/3 HD, and Will +1/2 HD + 2.
>
> **Defensive Abilities:** Zombies lose their defensive abilities and gain all of the qualities and immunities granted by the undead type. Zombies gain DR 5/slashing.
>
> **Speed:** Winged zombies can still fly, but maneuverability drops to clumsy. If the base creature flew magically, so can the zombie. Retain all other movement types.
>
> **Attacks:** A zombie retains all the natural weapons, manufactured weapon attacks, and weapon proficiencies of the base creature. It also gains a slam attack that deals damage based on the zombie's size, but as if it were one size category larger than its actual size (see Natural Attacks).
>
> **Special Attacks:** A zombie retains none of the base creature's special attacks.
>
> **Abilities:** Str +2, Dex –2. A zombie has no Con or Int score, and its Wis and Cha become 10.
>
> **BAB:** A zombie's base attack is equal to 3/4 its Hit Dice.
>
> **Skills:** A zombie has no skill ranks.
>
> **Feats:** A zombie loses all feats possessed by the base creature, and does not gain feats as its Hit Dice increase, but it does gain Toughness as a bonus feat.
>
> **Special Qualities:** A zombie loses most special qualities of the base creature. It retains any extraordinary special qualities that improve its melee or ranged attacks. A zombie gains the following special quality.
>
> - 
>
> @UUID[Compendium.pf1.template-abilities.Item.Ld4w9QurQancak8a]

**Mechanical encoding:** `changes`: 6 (showing first 5)
  - `1` → `bonusFeats`  (untypedPerm)
  - `10` → `wis`  (untypedPerm)
  - `lookup(@size - 2, 0, 1, 2, 3, 4, 7, 11)` → `nac`  (untyped)
  - `10` → `cha`  (untypedPerm)
  - `2` → `str`  (untyped)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

