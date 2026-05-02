# PF1 Rules Checklist — racial-hd

_Auto-generated from a Foundry PF1e pack snapshot. **Do not edit by hand.**_
_Items in this shard: 13._

Status legend (for the `Manual verdict:` field below):
- `[x]` verified — engine matches RAW
- `[~]` partial  — engine has some of it; gap noted
- `[-]` absent   — not in our content / engine
- `[!]` buggy    — implemented but doesn't match RAW

Update `dnd/coverage.py` with the verdict after marking a row.

---
### Aberration
*(class / racial)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `WiROthmRgcwDncDM`

> An aberration has a bizarre anatomy, strange abilities, an alien mindset, or any combination of the three.
>
> #### Features
>
> An aberration has the following features.
>
> - d8 Hit Die.
>
> - Base attack bonus equal to 3/4 total Hit Dice (medium progression).
>
> - Good *Will* Saves.
>
> - Skill points equal to 4 + Int modifier (minimum 1) per Hit Die. The following are class skills for aberrations: *Acrobatics*, *Climb*, *Escape Artist*, *Fly*, *Intimidate*, *Knowledge* (pick one), *Perception*, *Spellcraft*, *Stealth*, *Survival*, and *Swim*.
>
> #### Traits
>
> An aberration possesses the following traits (unless otherwise noted in a creature’s entry).
>
> - Darkvision 60 feet.
>
> - Proficient with its natural weapons. If generally humanoid in form, proficient with all simple weapons and any weapon it is described as using.
>
> - Proficient with whatever type of armor (light, medium, or heavy) it is described as wearing, as well as all lighter types. Aberrations not indicated as wearing armor are not proficient with armor. Aberrations are proficient with shields if they are proficient with any form of armor.
>
> - Aberrations breathe, eat, and sleep.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Animal
*(class / racial)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `WJqmmfXscPVpcISH`

> An animal is a living, nonhuman creature, usually a vertebrate with no magical abilities and no innate capacity for language or culture. Animals usually have additional information on how they can serve as companions.
>
> #### Features
>
> An animal has the following features (unless otherwise noted).
>
> - d8 Hit Die.
>
> - Base attack bonus equal to 3/4 total Hit Dice (medium progression).
>
> - Good *Fortitude* and *Reflex* saves.
>
> - Skill points equal to 2 + *Int* modifier (minimum 1) per Hit Die. The following are class skills for animals: *Acrobatics*, *Climb*, *Fly*, *Perception*, *Stealth*, and *Swim*.
>
> #### Traits
>
> An animal possesses the following traits (unless otherwise noted in a creature’s entry).
>
> - *Intelligence* score of 1 or 2 (no creature with an *Intelligence* score of 3 or higher can be an animal).
>
> - *Low-light vision*.
>
> - Alignment: Always neutral.
>
> - Treasure: None.
>
> - Proficient with its natural weapons only. A non-combative herbivore treats its natural weapons as secondary attacks. Such attacks are made with a –5 penalty on the creature’s attack rolls, and the animal receives only 1/2 its *Strength* modifier as a damage adjustment.
>
> - Proficient with no armor unless trained for war. (See *FAQ*s and *Handle Animal Skill*.)
>
> - Animals breathe, eat, and sleep.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Construct
*(class / racial)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `H8FbMUps5Z0gQdvV`

> A construct is an animated object or artificially created creature.
>
> #### Features
>
> A construct has the following features.
>
> - d10 Hit Die.
>
> - Base attack bonus equal to total Hit Dice (fast progression).
>
> - No good saving throws.
>
> - Skill points equal to 2 + Int modifier (minimum 1) per Hit Die. However, most constructs are mindless and gain no skill points or feats. Constructs do not have any class skills, regardless of their *Intelligence* scores.
>
> - Construct Size Bonus Hit Points Fine — Diminutive — Tiny — Small 10 Medium 20 Large 30 Huge 40 Gargantuan 60 Colossal 80
>
> #### Traits
>
> A construct possesses the following traits (unless otherwise noted in a creature’s entry).
>
> - No Constitution score. Any DCs or other statistics that rely on a Constitution score treat a construct as having a score of 10 (no bonus or penalty).
>
> - Low-light vision.
>
> - Darkvision 60 feet.
>
> - Immunity to all mind-affecting effects (charms, compulsions, morale effects, patterns, and phantasms).
>
> - Immunity to disease, death effects, necromancy effects, paralysis, poison, sleep effects, and stunning.
>
> - Cannot heal damage on its own, but often can be repaired via exposure to a certain kind of effect (see the creature’s description for details) or through the use of the *Craft Construct* feat. Constructs can also be healed through spells such as *make whole*. A construct with the fast healing special quality still benefits from that quality.
>
> - Not subject to *ability damage*, *ability drain*, fatigue, exhaustion, energy drain, or nonlethal damage.
>
> - Immunity to any effect that requires a *Fortitude* save (unless the effect also works on objects, or is harmless).
>
> - Not at risk of death from massive damage. Immediately destroyed when reduced to 0 hit points or less.
>
> - A construct cannot be raised or resurrected.
>
> - A construct is hard to destroy, and gains bonus hit points based on size, as shown on the following table.
>
> - Proficient with its natural weapons only, unless generally humanoid in form, in which case proficient with any weapon mentioned in its entry.
>
> - Proficient with no armor.
>
> - Constructs do not breathe, eat, or sleep.
>
> #### Construct Size Bonus Hit Points
>
>
>
>
>  Fine 
>  10 
>
>
>  Diminutive 
>  10 
>
>
>  Tiny 
>  10 
>
>
>  Small 
>  10 
>
>
>  Medium 
>  20 
>
>
>  Large 
>  30 
>
>
>  Huge 
>  40 
>
>
>  Gargantuan 
>  60 
>
>
>  Colossal 
>  80

**Mechanical encoding:** `changes`: 1
  - `max(0, @size - 2) * 10 + max(0, @size - 6) * 10` → `mhp`  (untypedPerm)

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Dragon
*(class / racial)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `X2WLdbFFedaah6VC`

> A dragon is a reptile-like creature, usually winged, with magical or unusual abilities.
>
> #### Features
>
> A dragon has the following features.
>
> - d12 Hit Die.
>
> - Base attack bonus equal to total Hit Dice (fast progression).
>
> - Good *Fortitude*, *Reflex*, and *Will* Saves.
>
> - Skill points equal to 6 + Int modifier (minimum 1) per Hit Die. The following are class skills for dragons: *Appraise*, *Bluff*, *Climb*, *Craft*, *Diplomacy*, *Fly*, *Heal*, *Intimidate*, *Knowledge* (all), *Linguistics*, *Perception*, *Sense Motive*, *Spellcraft*, *Stealth*, *Survival*, *Swim*, and *Use Magic Device*.
>
> #### Traits
>
> A dragon possesses the following traits (unless otherwise noted in a creature’s entry).
>
> - *Darkvision* 60 feet and *low-light vision*.
>
> - Immunity to magic sleep effects and paralysis effects.
>
> - Proficient with its natural weapons only unless humanoid in form (or capable of assuming humanoid form), in which case proficient with all simple weapons and any weapons mentioned in its entry.
>
> - Proficient with no armor.
>
> - Dragons breathe, eat, and sleep.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fey
*(class / racial)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `0jjH2XJVd6dzlaSm`

> A fey is a creature with supernatural abilities and connections to nature or to some other force or place. Fey are usually human-shaped.
>
> #### Features
>
> A fey has the following features.
>
> - d6 Hit Die.
>
> - Base attack bonus equal to 1/2 total Hit Dice (slow progression).
>
> - Good *Reflex* and *Will* Saves.
>
> - Skill points equal to 6 + Int modifier (minimum 1) per Hit Die. The following are class skills for fey: *Acrobatics*, *Bluff*, *Climb*, *Craft*, *Diplomacy*, *Disguise*, *Escape Artist*, *Fly*, *Knowledge* (geography), *Knowledge* (local), *Knowledge* (nature), *Perception*, *Perform*, *Sense Motive*, *Sleight of Hand*, *Stealth*, *Swim*, *Use Magic Device*.
>
> #### Traits
>
> A fey possesses the following traits (unless otherwise noted in a creature’s entry).
>
> - *Low-light vision*.
>
> - Proficient with all simple weapons and any weapons mentioned in its entry.
>
> - Proficient with whatever type of armor (light, medium, or heavy) it is described as wearing, as well as all lighter types. Fey not indicated as wearing armor are not proficient with armor. Fey are proficient with shields if they are proficient with any form of armor.
>
> - Fey breathe, eat, and sleep.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Humanoid
*(class / racial)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `S38eYYsK7pRhPbwg`

> A humanoid usually has two arms, two legs, and one head, or a human-like torso, arms, and a head. Humanoids have few or no supernatural or extraordinary abilities, but most can speak and usually have well-developed societies. They are usually Small or Medium (with the exception of giants). Every humanoid creature also has a specific subtype to match its race, such as human, giant, goblinoid, reptilian, or tengu.
>
> Humanoids with 1 Hit Die exchange the features of their humanoid Hit Die for the class features of a PC or NPC class. Humanoids of this sort are typically presented as 1st-level warriors, which means they have average combat ability and poor saving throws. Humanoids with more than 1 Hit Die are the only humanoids who make use of the features of the humanoid type.
>
> #### Features
>
> A humanoid has the following features (unless otherwise noted in a creature’s entry).
>
> - d8 Hit Die, or by character class.
>
> - Base attack bonus equal to 3/4 total Hit Dice (medium progression).
>
> - One good save, usually *Reflex*.
>
> - Skill points equal to 2 + Int modifier (minimum 1) per Hit Die or by character class. The following are class skills for humanoids without a character class: *Climb*, *Craft*, *Handle Animal*, *Heal*, *Profession*, *Ride*, and *Survival*. Humanoids with a character class use their class’s skill list instead.
>
> #### Traits
>
> A humanoid possesses the following traits (unless otherwise noted in a creature’s entry).
>
> - Proficient with all simple weapons, or by character class.
>
> - Proficient with whatever type of armor (light, medium, or heavy) it is described as wearing, or by character class. If a humanoid does not have a class and wears *armor*, it is proficient with that type of armor and all lighter types. Humanoids not indicated as wearing armor are not proficient with armor. Humanoids are proficient with shields if they are proficient with any form of armor.
>
> - Humanoids breathe, eat, and sleep.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Magical Beast
*(class / racial)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `AjUleVwKSsSaDI4N`

> Magical beasts are similar to animals but can have *Intelligence* scores higher than 2 (in which case the magical beast knows at least one language, but can’t necessarily speak). Magical beasts usually have supernatural or extraordinary abilities, but are sometimes merely bizarre in appearance or habits.
>
> #### Features
>
> A magical beast has the following features.
>
> - d10 Hit Die.
>
> - Base attack bonus equal to total Hit Dice (fast progression).
>
> - Good *Fortitude* and *Reflex* saves.
>
> - Skill points equal to 2 + Int modifier (minimum 1) per Hit Die. The following are class skills for magical beasts: *Acrobatics*, *Climb*, *Fly*, *Perception*, *Stealth*, *Swim*.
>
> #### Traits
>
> A magical beast possesses the following traits (unless otherwise noted in a creature’s entry).
>
> - *Darkvision* 60 feet.
>
> - *Low-light vision*.
>
> - Proficient with its natural weapons only.
>
> - Proficient with no armor.
>
> - Magical beasts breathe, eat, and sleep.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Monstrous Humanoid
*(class / racial)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `6Uh8PAjR3BE7dult`

> Monstrous humanoids are similar to humanoids, but with monstrous or animalistic features. They often have magical abilities as well.
>
> #### Features
>
> A monstrous humanoid has the following features.
>
> - d10 Hit Die.
>
> - Base attack bonus equal to total Hit Dice (fast progression).
>
> - Good *Reflex* and *Will* Saves.
>
> - Skill points equal to 4 + Int modifier (minimum 1) per Hit Die. The following are class skills for monstrous humanoids: *Climb*, *Craft*, *Fly*, *Intimidate*, *Perception*, *Ride*, *Stealth*, *Survival*, and *Swim*.
>
> #### Traits
>
> A monstrous humanoid possesses the following traits (unless otherwise noted in a creature’s entry).
>
> - *Darkvision* 60 feet.
>
> - Proficient with all simple weapons and any weapons mentioned in its entry.
>
> - Proficient with whatever type of armor (light, medium, or heavy) it is described as wearing, as well as all lighter types. Monstrous humanoids not indicated as wearing armor are not proficient with armor. Monstrous humanoids are proficient with shields if they are proficient with any form of armor.
>
> - Monstrous humanoids breathe, eat, and sleep.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Ooze
*(class / racial)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `D1vugd9jeyAQrLVX`

> An ooze is an amorphous or mutable creature, usually mindless.
>
> #### Features
>
> An ooze has the following features.
>
> - d8 Hit Die.
>
> - Base attack bonus equal to 3/4 total Hit Dice (medium progression).
>
> - No good saving throws.
>
> - Skill points equal to 2 + Int modifier (minimum 1) per Hit Die. However, most oozes are mindless and gain no skill points or feats. Oozes do not have any class skills.
>
> #### Traits
>
> An ooze possesses the following traits (unless otherwise noted in a creature’s entry).
>
> - Mindless: No *Intelligence* score, and immunity to all mind-affecting effects (charms, compulsions, phantasms, patterns, and morale effects). An ooze with an *Intelligence* score loses this trait.
>
> - Blind (but have the blindsight special quality), with immunity to gaze attacks, visual effects, illusions, and other attack forms that rely on sight.
>
> - Immunity to poison, sleep effects, paralysis, polymorph, and stunning.
>
> - Some oozes have the ability to deal acid damage to objects. In such a case, the amount of damage is equal to 10 + 1/2 ooze’s HD + ooze’s *Con* modifier per full round of contact.
>
> - Not subject to critical hits or flanking. Does not take additional damage from precision-based attacks, such as sneak attack.
>
> - Proficient with its natural weapons only.
>
> - Proficient with no armor.
>
> - Oozes eat and breathe, but do not sleep.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Outsider
*(class / racial)*

**Tags:** —
**Prerequisites:** —
**Source:** PZO1112 (PZO1112) p. 309
**Foundry id:** `cV7yHt8i5YCV0ZTd`

> An outsider is at least partially composed of the essence (but not necessarily the material) of some plane other than the Material Plane. Some creatures start out as some other type and become outsiders when they attain a higher (or lower) state of spiritual existence.
>
> #### Features
>
> An outsider has the following features.
>
> - d10 Hit Dice.
> - Base attack bonus equal to total Hit Dice (fast progression).
> - Two good saving throws, usually *Reflex* and Will.
> - Skill points equal to 6 + Int modifier (minimum 1) per Hit Die. The following are class skills for outsiders: *Bluff*, *Craft*, *Knowledge* (planes), *Perception*, *Sense Motive*, and *Stealth*. Due to their varied nature, outsiders also receive 4 additional class skills determined by the creature’s theme.
>
> #### Traits
>
> An outsider possesses the following traits (unless otherwise noted in a creature’s entry).
>
> - Darkvision 60 feet.
> - Unlike most living creatures, an outsider does not have a dual nature—its soul and body form one unit. When an outsider is slain, no soul is set loose. Spells that restore souls to their bodies, such as *raise dead*, *reincarnate*, and *resurrection*, don’t work on an outsider. It takes a different magical effect, such as *limited wish*, *wish*, *miracle*, or *true resurrection* to restore it to life. An outsider with the native subtype can be raised, reincarnated, or resurrected just as other living creatures can be.
> - Proficient with all simple and martial weapons and any weapons mentioned in its entry.
> - Proficient with whatever type of armor (light, medium, or heavy) it is described as wearing, as well as all lighter types. Outsiders not indicated as wearing armor are not proficient with armor. Outsiders are proficient with shields if they are proficient with any form of armor.
> - Outsiders breathe, but do not need to eat or sleep (although they can do so if they wish). Native outsiders breathe, eat, and sleep.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Plant
*(class / racial)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `AbOSfjvKMqpNihdM`

> This type comprises vegetable creatures. Note that regular plants, such as one finds growing in gardens and fields, lack Wisdom and *Charisma* scores and are not creatures, but objects, even though they are alive.
>
> #### Features
>
> A plant creature has the following features.
>
> - d8 Hit Die.
>
> - Base attack bonus equal to 3/4 total Hit Dice (medium progression).
>
> - Good *Fortitude* saves.
>
> - Skill points equal to 2 + Int modifier (minimum 1) per Hit Die. Some plant creatures, however, are mindless and gain no skill points or feats. The following are class skills for plants: *Perception* and *Stealth*.
>
> #### Traits
>
> A plant creature possesses the following traits (unless otherwise noted in a creature’s entry).
>
> - Low-light vision.
>
> - Immunity to all mind-affecting effects (charms, compulsions, morale effects, patterns, and phantasms).
>
> - Immunity to paralysis, poison, polymorph, sleep effects, and stunning.
>
> - Proficient with its natural weapons only.
>
> - Not proficient with armor.
>
> - Plants breathe and eat, but do not sleep.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Undead
*(class / racial)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `mp1Zmbx0OAzSW4oW`

> Undead are once-living creatures animated by spiritual or supernatural forces.
>
> #### Features
>
> An undead creature has the following features.
>
> - d8 Hit Die.
>
> - Base attack bonus equal to 3/4 total Hit Dice (medium progression).
>
> - Good *Will* Saves.
>
> - Skill points equal to 4 + Int modifier (minimum 1) per Hit Die. Many undead, however, are mindless and gain no skill points or feats. The following are class skills for undead: *Climb*, *Disguise*, *Fly*, *Intimidate*, *Knowledge* (arcane), *Knowledge* (religion), *Perception*, *Sense Motive*, *Spellcraft*, and *Stealth*.
>
> #### Traits
>
> An undead creature possesses the following traits (unless otherwise noted in a creature’s entry).
>
> - No Constitution score. Undead use their *Charisma* score in place of their Constitution score when calculating hit points, *Fortitude* saves, and any special ability that relies on Constitution (such as when calculating a breath weapon’s DC).
>
> - *Darkvision* 60 feet.
>
> - Immunity to all mind-affecting effects (charms, compulsions, morale effects, patterns, and phantasms).
>
> - Immunity to death effects, disease, paralysis, poison, sleep effects, and stunning.
>
> - Not subject to nonlethal damage, *ability drain*, or energy drain. Immune to *damage* to its physical ability scores (Constitution, Dexterity, and *Strength*), as well as to exhaustion and fatigue effects.
>
> - Cannot heal damage on its own if it has no *Intelligence* score, although it can be healed. Negative energy (such as an inflict spell) can heal undead creatures. The fast healing special quality works regardless of the creature’s *Intelligence* score.
>
> - Immunity to any effect that requires a *Fortitude* save (unless the effect also works on objects or is harmless).
>
> - Not at risk of death from massive damage, but is immediately destroyed when reduced to 0 hit points.
>
> - Not affected by *raise dead* and *reincarnate* spells or abilities. Resurrection and *true resurrection* can affect undead creatures. These spells turn undead creatures back into the living creatures they were before becoming undead.
>
> - Proficient with its natural weapons, all simple weapons, and any weapons mentioned in its entry.
>
> - Proficient with whatever type of armor (light, medium, or heavy) it is described as wearing, as well as all lighter types. Undead not indicated as wearing armor are not proficient with armor. Undead are proficient with shields if they are proficient with any form of armor.
>
> - Undead do not breathe, eat, or sleep.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

### Vermin
*(class / racial)*

**Tags:** —
**Prerequisites:** —
**Source:** —
**Foundry id:** `g3gX00gTvJU478ju`

> This type includes insects, arachnids, other arthropods, worms, and similar invertebrates.
>
> #### Features
>
> Vermin have the following features.
>
> - d8 Hit Die.
>
> - Base attack bonus equal to 3/4 total Hit Dice (medium progression).
>
> - Good *Fortitude* saves.
>
> - Skill points equal to 2 + Int modifier (minimum 1) per Hit Die. Most vermin, however, are mindless and gain no skill points or feats. Vermin have no class skills.
>
> #### Traits
>
> Vermin possess the following traits (unless otherwise noted in a creature’s entry).
>
> - Mindless: No *Intelligence* score, and immunity to all mind-affecting effects (charms, compulsions, morale effects, patterns, and phantasms). A vermin-like creature with an *Intelligence* score is usually either an animal or a magical beast, depending on its other abilities.
>
> - *Darkvision* 60 feet.
>
> - Proficient with its natural weapons only.
>
> - Proficient with no armor.
>
> - Vermin breathe, eat, and sleep.

*No mechanical encoding — prose only.*

**In our coverage tracker:** n/a (no per-name lookup for this category)
**Manual verdict:** `[ ]`
**Notes:**

---

