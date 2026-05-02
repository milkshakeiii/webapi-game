# PF1 Rules Checklist — feats

_Auto-generated from a Foundry PF1e pack snapshot. **Do not edit by hand.**_
_Items in this shard: 390._

Status legend (for the `Manual verdict:` field below):
- `[x]` verified — engine matches RAW
- `[~]` partial  — engine has some of it; gap noted
- `[-]` absent   — not in our content / engine
- `[!]` buggy    — implemented but doesn't match RAW

Update `dnd/coverage.py` with the verdict after marking a row.

---
### Ability Focus
*(feat)*

**Tags:** Monster
**Prerequisites:** Special attack
**Source:** PZO1112 (PZO1112) p. 314
**Foundry id:** `QWQH2kZgd1xZicuX`

> *One of this creature's special attacks is particularly difficult to resist.*
>
> **Prerequisites**: Special attack.
>
> **Benefits**: Choose one of the creature's special attacks. Add +2 to the DC for all saving throws against the special attack on which the creature focuses.
>
> **Special**: A creature can gain this feat multiple times. Its effects do not stack. Each time the creature takes the feat, it applies to a different special attack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `ability_focus` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Acrobatic Steps
*(feat)*

**Tags:** General, Movement
**Prerequisites:** Dex 15, Nimble Moves
**Source:** Core Rulebook (PZO1110) p. 113, 115
**Foundry id:** `B6wEQOUMv2ifm2Nj`

> *You can easily move over and through obstacles.*
>
> **Prerequisites**: Dex 15, Nimble Moves.
>
> **Benefits**: Whenever you move, you may move through up to 15 feet of difficult terrain each round as if it were normal terrain. The effects of this feat stack with those provided by Nimble Moves (allowing you to move normally through a total of 20 feet of difficult terrain each round).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `acrobatic_steps` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Acrobatic
*(feat)*

**Tags:** General
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 113, 114
**Foundry id:** `jCxcObXJfdDrx4WS`

> *You are skilled at leaping, jumping, and flying.*
>
> **Benefits**: You get a +2 bonus on all Acrobatics and Fly skill checks. If you have 10 or more ranks in one of these skills, the bonus increases to +4 for that skill.

**Mechanical encoding:** `changes`: 2
  - `2 + if(gte(@skills.fly.rank, 10), 2)` → `skill.fly`  (untyped)
  - `2 + if(gte(@skills.acr.rank, 10), 2)` → `skill.acr`  (untyped)

**In our coverage tracker:** absent (slug `acrobatic` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Agile Maneuvers
*(feat)*

**Tags:** Combat
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 114, 117
**Foundry id:** `lxDJhpqwtR3J4UXx`

> *You've learned to use your quickness in place of brute force when performing combat maneuvers.*
>
> **Benefits**: You add your Dexterity bonus to your base attack bonus and size bonus when determining your Combat Maneuver Bonus (see Combat) instead of your Strength bonus.
>
> **Normal**: You add your Strength bonus to your base attack bonus and size bonus when determining your Combat Maneuver Bonus.

**Mechanical encoding:** `changes`: 1
  - `if(gt(@abilities.dex.mod, @abilities.str.mod), @abilities.dex.mod - @abilities.str.mod)` → `cmb`  (untyped)

**In our coverage tracker:** absent (slug `agile_maneuvers` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Alertness
*(feat)*

**Tags:** General, Skill
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 114, 117
**Foundry id:** `Q1cY8r0Pvb66pMG0`

> *You often notice things that others might miss.*
>
> **Benefits**: You get a +2 bonus on Perception and Sense Motive skill checks. If you have 10 or more ranks in one of these skills, the bonus increases to +4 for that skill.

**Mechanical encoding:** `changes`: 2
  - `2 + if(gte(@skills.per.rank, 10), 2)` → `skill.per`  (untyped)
  - `2 + if(gte(@skills.sen.rank, 10), 2)` → `skill.sen`  (untyped)

**In our coverage tracker:** `IMPLEMENTED` — +2 perception/sense_motive
**Manual verdict:** `[ ]`
**Notes:**

---

### Aligned Crafting
*(feat)*

**Tags:** Item Creation
**Prerequisites:** Craft Magic Arms and Armor or Craft Wondrous Item
**Source:** PZO9486 (PZO9486) p. 26
**Foundry id:** `UqQk2exo5s8hL71s`

> *Your magical creations reject those you oppose.*
>
> **Prerequisites**: Craft Magic Arms and Armor or Craft Wondrous Item.
>
> **Benefit**: When you craft a magic weapon, magic armor, a magic shield, or a wondrous item, you can infuse it with a bit of your convictions. Creatures that are more than one alignment step away from you are sickened while using or wearing this item. An item that has been infused with your alignment can never have an opposing special ability added to it later (for example, a longsword infused with your lawful good alignment cannot later gain the anarchic weapon special ability). Infusing the item with your alignment in this way increases the items total construction cost by 10%.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `aligned_crafting` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Alignment Channel
*(feat)*

**Tags:** Channeling
**Prerequisites:** Ability to channel energy
**Source:** Core Rulebook (PZO1110) p. 114, 117
**Foundry id:** `ieww7CP6JK5pwtpg`

> Choose chaos, evil, good, or law. You can channel divine energy to affect outsiders that possess this subtype.
>
> **Prerequisites**: Ability to channel energy.
>
> **Benefits**: Instead of its normal effect, you can choose to have your ability to channel energy heal or harm outsiders of the chosen alignment subtype. You must make this choice each time you channel energy. If you choose to heal or harm creatures of the chosen alignment subtype, your channel energy has no effect on other creatures. The amount of damage healed or dealt and the DC to halve the damage is otherwise unchanged.
>
> **Special**: You can gain this feat multiple times. Its effects do not stack. Each time you take this feat, it applies to a new alignment subtype. Whenever you channel energy, you must choose which type to effect.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `alignment_channel` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Amateur Gunslinger
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** —
**Source:** Bestiary (PZO1118) p. 89
**Foundry id:** `nxfb1Cxl628nYR3L`

> *Although you are not a gunslinger, you have and can use grit.*
>
> **Prerequisites:** You have no levels in a class that has the grit class feature.
>
> **Benefit:** You gain a small amount of grit and the ability to perform a single 1st-level deed from the gunslinger deed class feature. At the start of the day, you gain 1 grit point, though throughout the day you can gain grit points up to a maximum of your Wisdom modifier (minimum 1). You can regain grit using the rules for the gunslinger’s grit class feature. You can spend this grit to perform the 1st-level deed you chose upon taking this feat, and any other deed you have gained through feats or magic items.
>
> **Special:** If you gain levels in a class that grants the grit class feature, you can immediately trade this feat for the Extra Grit feat.
>
> ##### Combat Trick
>
> Choose a second 1st-level gunslinger deed. You can spend grit to use this deed, or you can spend 5 stamina points to use either of your deeds in place of grit. If you gain levels in a class that grants the grit class feature, you retain the ability to spend 5 stamina points in place of grit when using any of your 1st-level deeds, and this becomes a combat trick of the Extra GritUC feat (even though that feat is not a combat feat).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `amateur_gunslinger` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Amateur Investigator
*(feat)*

**Tags:** General
**Prerequisites:** Int 13, 1 rank in at least one Knowledge skill, no levels in a class that has the inspiration class feature
**Source:** Advanced Class Guide (PZO1129) p. 141
**Foundry id:** `SS99IHuvIvzQ1v92`

> *Your knowledge is more than plain smarts—it’s inspired.*
>
> **Prerequisites**: Int 13, 1 rank in at least one Knowledge skill, no levels in a class that has the inspiration class feature.
>
> **Benefit**: Like an investigator, you have the ability to augment your Knowledge, Linguistics, and Spellcraft skill checks. You gain a pool of inspiration equal to your Intelligence modifier. You can expend one use of inspiration as a free action to add 1d6 to the result of a Knowledge, Linguistics, or Spellcraft check, as long as you are trained in that skill (even if you take 10 or 20 on that check). You make this choice after the check is rolled and before the results of the roll are revealed. You can use inspiration only once per skill check. Your pool of inspiration refreshes each day, typically after you get a restful night’s sleep.
>
> **Special**: If you gain levels in a class that has the inspiration class feature, you can immediately trade this feat for the Extra Inspiration feat.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `amateur_investigator` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Amateur Swashbuckler
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** No levels in a class that has the panache class feature
**Source:** Advanced Class Guide (PZO1129) p. 141; Advanced Race Guide (PZO1131) p. 113
**Foundry id:** `Vov43JkBzhtPn2T9`

> *Though not a swashbuckler, you have and can use panache.*
>
> **Prerequisites**: No levels in a class that has the panache class feature.
>
> **Benefit**: You gain a small amount of panache and the ability to perform a single 1st-level swashbuckler deed. Choose a 1st-level deed from the swashbuckler’s deeds class feature (see page 56; you can't select opportune parry and riposte). Once chosen, this deed cannot be changed.
>
> At the start of each day, you gain 1 panache point. Throughout the day, you can gain a number of panache points up to a maximum of your Charisma modifier (minimum 1). You can regain panache points as the swashbuckler’s panache class feature. You can spend these panache points to perform the 1st-level deed you chose upon taking this feat as well as any other deeds you have gained through feats or magic items.
>
> **Special**: If you gain levels in a class that has the panache class feature, you can immediately trade this feat for the Extra Panache feat.
>
>
> ##### Combat Trick
>
> Choose a second 1st-level swashbuckler deed. You can spend panacheACG to use this deed, or you can spend 5 stamina points to use either of your deeds in place of panache. If you gain levels in a class that grants the panache class feature, you retain the ability to spend 5 stamina points in place of panache when using any of your 1st-level deeds, and this becomes a combat trick of the Extra Panache feat (even though that feat is not a combat feat).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `amateur_swashbuckler` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Animal Affinity
*(feat)*

**Tags:** General
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 114, 118
**Foundry id:** `bqoIfsrF8BF1GC28`

> *You are skilled at working with animals and mounts.*
>
> **Benefits**: You get a +2 bonus on all Handle Animal and Ride skill checks. If you have 10 or more ranks in one of these skills, the bonus increases to +4 for that skill.

**Mechanical encoding:** `changes`: 2
  - `2 + if(gte(@skills.rid.rank, 10), 2)` → `skill.rid`  (untyped)
  - `2 + if(gte(@skills.han.rank, 10), 2)` → `skill.han`  (untyped)

**In our coverage tracker:** absent (slug `animal_affinity` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Aquadynamic Focus
*(feat)*

**Tags:** Combat
**Prerequisites:** Weapon Focus, base attack bonus +1
**Source:** PZO92102 (PZO92102) p. 57
**Foundry id:** `Ta1GLdnipoC2qpCO`

> *Your skill with your chosen weapons is so great that you can use them underwater without impediment.*
>
> **Prerequisites**: Weapon Focus, base attack bonus +1.
>
> **Benefits**: You don't take additional penalties on attack and damage rolls for fighting underwater with bludgeoning and slashing melee weapons for which you have taken the Weapon Focus feat.
>
> **Normal**: When using bludgeoning and slashing melee weapons underwater, you take a -2 penalty on attack rolls and deal half damage.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `aquadynamic_focus` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Aquadynamic Shot
*(feat)*

**Tags:** Combat
**Prerequisites:** Far Shot, Point-Blank Shot, base attack bonus +4
**Source:** PZO92102 (PZO92102) p. 57
**Foundry id:** `5X0iLon184CkZ1sI`

> *You use projectiles and special trick shots that lose less accuracy when underwater.*
>
> **Prerequisites**: Far Shot, Point-Blank Shot, base attack bonus +4.
>
> **Benefits**: Your projectile attacks take a -1 penalty per 5 feet of water between you and the target. You still can't use thrown weapons effectively underwater except in special circumstances (Aquatic Adventures 44).
>
> **Normal**: Projectile attacks underwater take a -2 penalty per 5 feet of water between the shooter and the target.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `aquadynamic_shot` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Arcane Armor Mastery
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Arcane Armor Training, Medium Armor Proficiency, caster level 7th
**Source:** Core Rulebook (PZO1110) p. 114, 118
**Foundry id:** `aUYSiYrtVHkgfHD6`

> *You have mastered the ability to cast spells while wearing armor.*
>
> **Prerequisites**: Arcane Armor Training, Medium Armor Proficiency, caster level 7th.
>
> **Benefits**: As a swift action, reduce the arcane spell failure chance due to the armor you are wearing by 20% for any spells you cast this round. This bonus replaces, and does not stack with, the bonus granted by Arcane Armor Training.
>
> ##### Combat Trick
>
> When casting a spell while wearing armor, you can spend 1 stamina point to activate Arcane Armor Mastery as a free action, or spend a number of stamina points equal to the spell's level (minimum 1) to ignore your armor's arcane spell failure chance entirely for that casting.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `arcane_armor_mastery` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Arcane Armor Training
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Light Armor Proficiency, caster level 3rd
**Source:** Core Rulebook (PZO1110) p. 114, 118
**Foundry id:** `3v85ul6tGGBZbtBg`

> *You have learned how to cast spells while wearing armor.*
>
> **Prerequisites**: Light Armor Proficiency, caster level 3rd.
>
> **Benefits**: As a swift action, reduce the arcane spell failure chance due to the armor you are wearing by 10% for any spells you cast this round.
>
> ##### Combat Trick
>
> When casting a spell while wearing armor, you can spend 1 stamina point to activate Arcane Armor Training as a free action.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `arcane_armor_training` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Arcane Strike
*(feat)*

**Tags:** Combat, Weapon, Magic, Offensive
**Prerequisites:** Ability to cast arcane spells
**Source:** Core Rulebook (PZO1110) p. 114, 118
**Foundry id:** `QvlxYVVsBDlykPKe`

> *You draw upon your arcane power to enhance your weapons with magical energy.*
>
> **Prerequisites**: Ability to cast arcane spells.
>
> **Benefits**: As a swift action, you can imbue your weapons with a fraction of your power. For 1 round, your weapons deal +1 damage and are treated as magic for the purpose of overcoming damage reduction. For every five caster levels you possess, this bonus increases by +1, to a maximum of +5 at 20th level.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `arcane_strike` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Armor Proficiency, Heavy
*(feat)*

**Tags:** Combat
**Prerequisites:** Light Armor Proficiency, Medium Armor Proficiency
**Source:** Core Rulebook (PZO1110) p. 114, 118
**Foundry id:** `3MqcLuZfUJB8xMby`

> *You are skilled at wearing heavy armor.*
>
> **Prerequisites**: Light Armor Proficiency, Medium Armor Proficiency.
>
> **Benefits**: See Armor Proficiency, Light.
>
> **Normal**: See Armor Proficiency, Light.
>
> **Special**: Fighters and paladins automatically have Heavy Armor Proficiency as a bonus feat. They need not select it.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `armor_proficiency_heavy` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Armor Proficiency, Light
*(feat)*

**Tags:** Combat
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 114, 118
**Foundry id:** `FszchlqR39lnNduC`

> *You are skilled at wearing light armor.*
>
> **Benefits**: When you wear a type of armor with which you are proficient, the armor check penalty for that armor applies only to Dexterity- and Strength-based skill checks.
>
> **Normal**: A character who is wearing armor with which he is not proficient applies its armor check penalty to attack rolls and to all skill checks that involve moving.
>
> **Special**: All characters except monks, sorcerers, and wizards automatically have Light Armor Proficiency as a bonus feat. They need not select it.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `armor_proficiency_light` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Armor Proficiency, Medium
*(feat)*

**Tags:** Combat
**Prerequisites:** Light Armor Proficiency
**Source:** Core Rulebook (PZO1110) p. 114, 118
**Foundry id:** `qQCgBVieojhmMuHL`

> *You are skilled at wearing medium armor.*
>
> **Prerequisites**: Light Armor Proficiency.
>
> **Benefits**: See Armor Proficiency, Light.
>
> **Normal**: See Armor Proficiency, Light.
>
> **Special**: Barbarians, clerics, druids, fighters, paladins, and rangers automatically have Medium Armor Proficiency as a bonus feat. They need not select it.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `armor_proficiency_medium` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Aspect of the Beast
*(feat)*

**Tags:** General
**Prerequisites:** wild shape class feature, see Special
**Source:** Advanced Player's Guide (PZO1115) p. 151
**Foundry id:** `dPLj98GIzbwcoOjn`

> *Whether by magic or a curse of your blood, some part of you is more beast than man.*
>
> **Prerequisites**: wild shape class feature, see Special.
>
> **Benefit**: Your bestial nature manifests itself in one of the following ways. You choose the manifestation when you choose the feat, and then you cannot change it.
>
> - 
>
> **Night Senses** (Ex): If your base race has normal vision, you gain low-light vision. If your base race has low-light vision, you gain darkvision out to a range of 30 feet. If your base race has darkvision, the range of your darkvision increases by 30 feet.
>
> - 
>
> **Claws of the Beast** (Ex): You grow a pair of claws. These claws are primary attacks that deal 1d4 points of damage (1d3 if you are Small).
>
> - 
>
> **Predator's Leap** (Ex): You can make a running jump without needing to run 10 feet before you jump.
>
> - 
>
> **Wild Instinct** (Ex): You gain a +2 bonus on initiative checks and a +2 bonus on Survival skill checks.
>
> **Special**: A character that has contracted lycanthropy can take this feat without having to meet the prerequisites. A ranger who selects the natural weapon combat style can take this feat without having to meet the prerequisites (even if he does not select Aspect of the Beast as a bonus feat).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `aspect_of_the_beast` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Athletic
*(feat)*

**Tags:** General
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 114, 118
**Foundry id:** `rMR6ahXEfYqASE7D`

> *You possess inherent physical prowess.*
>
> **Benefits**: You get a +2 bonus on Climb and Swim skill checks. If you have 10 or more ranks in one of these skills, the bonus increases to +4 for that skill.

**Mechanical encoding:** `changes`: 2
  - `2 + if(gte(@skills.clm.rank, 10), 2)` → `skill.clm`  (untyped)
  - `2 + if(gte(@skills.swm.rank, 10), 2)` → `skill.swm`  (untyped)

**In our coverage tracker:** `IMPLEMENTED` — +2 climb/swim
**Manual verdict:** `[ ]`
**Notes:**

---

### Augment Summoning
*(feat)*

**Tags:** General
**Prerequisites:** Spell Focus (conjuration)
**Source:** Core Rulebook (PZO1110) p. 114, 118
**Foundry id:** `7bJjKqNRrvpXJ4L3`

> *Your summoned creatures are more powerful and robust.*
>
> **Prerequisites**: Spell Focus (conjuration).
>
> **Benefits**: Each creature you conjure with any summon spell gains a +4 enhancement bonus to Strength and Constitution for the duration of the spell that summoned it.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `augment_summoning` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Awesome Blow
*(feat)*

**Tags:** Combat, Monster
**Prerequisites:** Str 25, Power Attack, Improved Bull Rush, size Large or larger
**Source:** PZO1112 (PZO1112) p. 314
**Foundry id:** `KPaC3H6EQGG4sXLT`

> *This creature can send opponents flying.*
>
> **Prerequisites**: Str 25, Power Attack, Improved Bull Rush, size Large or larger.
>
> **Benefits**: As a standard action, the creature may perform an awesome blow combat maneuver. If the creature's maneuver succeeds against a corporeal opponent smaller than itself, its opponent takes damage (typically slam damage plus Strength bonus) and is knocked flying 10 feet in a direction of the attacking creature's choice and falls prone. The attacking creature can only push the opponent in a straight line, and the opponent can't move closer to the attacking creature than the square it started in. If an obstacle prevents the completion of the opponent's move, the opponent and the obstacle each take 1d6 points of damage, and the opponent is knocked prone in the space adjacent to the obstacle.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `awesome_blow` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Bashing Finish
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Improved Shield Bash, Shield Master, Two-Weapon Fighting, base attack bonus +11
**Source:** Advanced Race Guide (PZO1131) p. 114; Advanced Player's Guide (PZO1115) p. 151
**Foundry id:** `DUg7ErlHBmdhlh8n`

> *You follow a powerful blow from your weapon with an opportunistic bash from your shield.*
>
> **Prerequisites**: Improved Shield Bash, Shield Master, Two-Weapon Fighting, base attack bonus +11.
>
> **Benefits**: Whenever you score a critical hit with a melee weapon, you can make a shield bash attack against the same target using the same bonus as a free action.
>
> ##### Combat Trick
>
> When you fail to confirm a critical hit with a melee weapon attack, you can spend 5 stamina points to make a shield bash attack against the target anyway. You still can't make the attack if the target is immune to critical hits.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `bashing_finish` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Blazing Aura
*(feat)*

**Tags:** Combat, Conduit
**Prerequisites:** Knowledge (planes) 3 ranks
**Source:** Bestiary 6 (PZO1141) p. 26
**Foundry id:** `SKStYsOqcnZPzytA`

> *You cover yourself in coils of flame drawn from the Plane of Fire.*
>
> **Prerequisites**: Knowledge (planes) 3 ranks.
>
> **Benefits**: As a standard action, you can shroud yourself in fire. Until the end of your turn, whenever a creature makes a successful melee attack against you, that creature takes a number of points of fire damage equal to 1d6 plus half your ranks in Knowledge (planes); attacks made using reach weapons ignore this effect. A creature can halve this fire damage with a successful Reflex save (DC = 10 + half your level + your Constitution modifier).
>
> You can use this feat's benefit a number of times per day equal to your ranks in Knowledge (planes). If you have at least 9 ranks in Knowledge (planes), activating this ability is a move action. If you have at least 15 ranks in Knowledge (planes), you can activate this ability as a move action or a swift action.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `blazing_aura` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Bleeding Critical
*(feat)*

**Tags:** Combat, Critical, Combat Trick
**Prerequisites:** Critical Focus, base attack bonus +11
**Source:** Core Rulebook (PZO1110) p. 114, 118
**Foundry id:** `K1BvVIrp30BUKQB5`

> *Your critical hits cause opponents to bleed profusely.*
>
> **Prerequisites**: Critical Focus, base attack bonus +11.
>
> **Benefits**: Whenever you score a critical hit with a slashing or piercing weapon, your opponent takes 2d6 points of bleed damage (see Conditions) each round on his turn, in addition to the damage dealt by the critical hit. Bleed damage can be stopped by a DC 15 Heal skill check or through any magical healing. The effects of this feat stack.
>
> **Special**: You can only apply the effects of one critical feat to a given critical hit unless you possess Critical Mastery.
>
> ##### Combat Trick
>
> When you deal bleed damage with this feat, you can spend up to 3 stamina points to increase the amount of bleed damage dealt by double the number of stamina points you spent.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `bleeding_critical` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Blind-Fight
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 114, 118
**Foundry id:** `pmAO1Sni8xx71pLF`

> *You are skilled at attacking opponents that you cannot clearly perceive.*
>
> **Benefits**: In melee, every time you miss because of concealment (see Combat), you can reroll your miss chance percentile roll one time to see if you actually hit.
>
> An invisible attacker gets no advantages related to hitting you in melee. That is, you don't lose your Dexterity bonus to Armor Class, and the attacker doesn't get the usual +2 bonus for being invisible. The invisible attacker's bonuses do still apply for ranged attacks, however.
>
> You do not need to make Acrobatics skill checks to move at full speed while blinded.
>
> **Normal**: Regular attack roll modifiers for invisible attackers trying to hit you apply, and you lose your Dexterity bonus to AC. The speed reduction for darkness and poor visibility also applies.
>
> **Special**: The Blind-Fight feat is of no use against a character who is the subject of a blink spell.
>
> ##### Combat Trick
>
> Once per round, when you hit a creature that benefits from concealment, you can spend 2 stamina points to ignore the miss chance from that creature's concealment until the end of your next turn.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `blind_fight` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Blinding Critical
*(feat)*

**Tags:** Combat, Critical, Combat Trick
**Prerequisites:** Critical Focus, base attack bonus +15
**Source:** Core Rulebook (PZO1110) p. 114, 119
**Foundry id:** `2Gd0V8lDe6BkG7nl`

> *Your critical hits blind your opponents.*
>
> **Prerequisites**: Critical Focus, base attack bonus +15.
>
> **Benefits**: Whenever you score a critical hit, your opponent is permanently blinded. A successful Fortitude save reduces this to dazzled for 1d4 rounds. The DC of this Fortitude save is equal to 10 + your base attack bonus. This feat has no effect on creatures that do not rely on eyes for sight or creatures with more than two eyes (although multiple critical hits might cause blindness, at the GM's discretion). Blindness can be cured by heal, regeneration, remove blindness, or similar abilities.
>
> **Special**: You can only apply the effects of one critical feat to a given critical hit unless you possess Critical Mastery.
>
> ##### Combat Trick
>
> When you confirm a critical hit and attempt to blind an opponent with this feat, you can spend up to 5 stamina points to increase the DC of this feat's saving throw by an amount equal to the number of stamina points you spent.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `blinding_critical` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Block Chakras
*(feat)*

**Tags:** General
**Prerequisites:** Psychic Sensitivity or levels in an occult class, brawler’s flurry or flurry of blows class feature, ki pool
**Source:** PZO9493 (PZO9493) p. 28
**Foundry id:** `Ak0uWIHfOROMnywq`

> *You’ve learned how to block the lower chakras of your foes.*
>
> **Prerequisites**: Psychic Sensitivity or levels in an occult class, brawler’s flurry or flurry of blows class feature, ki pool.
>
> **Benefit**: As a standard action, you can spend 1 ki point to make a single unarmed strike that attempts to block one of the target’s chakras. If you hit the target and deal damage, you can select either the root, sacral, or navel chakra, as long as you can open that chakra yourself. The target suffers a specific effect based on the chosen chakra (see below), though it can reduce these effects with a successful Fortitude save (DC = 10 + half your character level + the ability modifier you use to calculate your ki pool).
>
> - 
>
> Root: The target’s DR is reduced by 10 for 1 minute. If the target has multiple forms of DR, you choose which DR is reduced. On a successful save, the target’s DR is instead reduced by 5 for 1 round.
>
> - 
>
> Sacral: The target can’t use any of its speeds except its land speed (or swim speed for an aquatic creature) for 1 round, and it moves at half speed for 1 minute. If it was flying, the target can attempt a Fly check to fall safely. On a successful save, the target instead moves at half speed for 1 round.
>
> - 
>
> Navel: The target takes a –2 penalty on attack rolls and damage rolls, and it reduces the DCs of its spells and abilities by 2 for 1 minute. On a successful save, the penalty and reduction is halved and lasts for 1 round.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `block_chakras` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Block Upper Chakras
*(feat)*

**Tags:** General
**Prerequisites:** Block Chakras, Psychic Sensitivity or levels in an occult class, brawler’s flurry or flurry of blows class feature, ki pool, character level 8th
**Source:** PZO9493 (PZO9493) p. 28
**Foundry id:** `jMGCqF0DGOVqyYUt`

> *You can block additional chakras.*
>
> **Prerequisites**: Block Chakras, Psychic Sensitivity or levels in an occult class, brawler’s flurry or flurry of blows class feature, ki pool, character level 8th.
>
> **Benefit**: When you use Block Chakras, you can also select from the heart, throat, brow, and crown chakras, as long as you can open the chosen chakra yourself, with the following effects.
>
> - 
>
> Heart: The target can’t recover hit points from any source for 1 minute. This prevents hit point recovery from fast healing and regeneration but doesn’t deactivate regeneration altogether, so it does not allow a creature with regeneration to be killed through hit point damage. On a successful save, the target recovers only half as many hit points for 1 round.
>
> - 
>
> Throat: The target can’t speak or cast spells with a thought component for 1 round, and for 1 minute, actions that require speaking or thought components have a 20% chance to fail. On a successful save, actions that require speaking or thought components have a 50% chance to fail for 1 round.
>
> - 
>
> Brow: The target is blinded for 1 minute. On a successful save, the target loses all special forms of vision (such as lowlight vision, see in darkness, and true seeing) for 1 round; this doesn’t affect nonvisual senses like blindsight and blindsense.
>
> - 
>
> Crown: The target must roll twice and take the lower result on all d20 rolls for 1 round and on its first attack roll or caster level check each round for 1 minute. On a successful save, the target must roll twice and take the lower result on its next d20 roll.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `block_upper_chakras` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Bloody Assault
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Str 13, Power Attack, base attack bonus +6
**Source:** Advanced Race Guide (PZO1131) p. 114; Advanced Player's Guide (PZO1115) p. 151
**Foundry id:** `xKJhMF8gS9c53RGl`

> *Sacrificing accuracy, you can inflict bloody wounds that are slow to heal.*
>
> **Prerequisites**: Str 13, Power Attack, base attack bonus +6.
>
> **Benefits**: You can choose to take a -5 penalty on all melee attack rolls and combat maneuver checks to inflict 1d4 points of bleed damage with your weapon melee attacks, in addition to the normal damage dealt by the weapon. A creature continues to take bleed damage every round at the start of its turn. Bleed damage can be stopped by a DC 15 Heal check or through any magical healing. Bleed damage from this feat does not stack with itself. You must choose to use this feat before making the attack roll, and its effects last until your next turn (although the bleeding lasts until healed, as normal).
>
> ##### Combat Trick
>
> Each round you use this feat, you can spend up to 5 stamina points. If you do, until the end of your next turn, you reduce the penalty on all your attack rolls by an amount equal to the number of stamina points you spent.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `bloody_assault` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Bludgeoner
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** —
**Source:** Bestiary (PZO1118) p. 90; Advanced Race Guide (PZO1131) p. 114
**Foundry id:** `pTPorNenRhXAtdYg`

> *You can knock foes out cold with just about any blunt instrument.*
>
> **Benefits**: You take no penalty on attack rolls for using a lethal bludgeoning weapon to deal nonlethal damage.
>
> **Normal**: You take a -4 penalty on attack rolls when using a lethal weapon to deal nonlethal damage. You cannot use a lethal weapon to deal nonlethal damage in a sneak attack.
>
> **Special**: A rogue with this feat can use a lethal bludgeoning weapon to deal nonlethal damage with a sneak attack.
>
> ##### Combat Trick
>
> When you make an attack with a lethal bludgeoning weapon to deal nonlethal damage, you can spend 2 stamina points to treat the weapon's damage as if the weapon were one size category larger. This does not stack with any other effects that treat the weapon's damage as if the weapon were a larger size.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `bludgeoner` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Bodyguard
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Combat Reflexes
**Source:** Advanced Player's Guide (PZO1115) p. 151
**Foundry id:** `JSPFo2fBkNlrtVqi`

> *Your swift strikes ward off enemies attacking nearby allies.*
>
> **Prerequisites**: Combat Reflexes.
>
> **Benefit**: When an adjacent ally is attacked, you may use an attack of opportunity to attempt the aid another action to improve your ally’s AC. You may not use the aid another action to improve your ally’s attack roll with this attack.
>
> **Normal**: Aid another is a standard action.
>
> ##### Combat Trick
>
> When you use an attack of opportunity to use an aid another action to improve an adjacent ally’s Armor Class, you can spend 1 or 2 stamina points. Increase the bonus to the ally’s AC by an amount equal to the number of stamina points you spent.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `bodyguard` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Breadth of Experience
*(feat)*

**Tags:** Gnome, Elf, Dwarf
**Prerequisites:** Dwarf, elf, or gnome; 100+ years old
**Source:** Advanced Player's Guide (PZO1115) p. 151
**Foundry id:** `bkw0OuBdByzeWF0N`

> *Although still young for your kind, you have a lifetime of knowledge and training.*
>
> **Prerequisites**: Dwarf, elf, or gnome; 100+ years old.
>
> **Benefits**: You get a +2 bonus on all Knowledge and Profession skill checks, and can make checks with those skills untrained.

**Mechanical encoding:** `changes`: 2
  - `2` → `skill.knowledge`  (untyped)
  - `2` → `skill.pro`  (untyped)

**In our coverage tracker:** absent (slug `breadth_of_experience` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Brew Potion
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Caster level 3rd
**Source:** Core Rulebook (PZO1110) p. 117, 119
**Foundry id:** `nNVFVFRBCT4O2ab9`

> *You can create magic potions.*
>
> **Prerequisites**: Caster level 3rd.
>
> **Benefits**: You can create a potion of any 3rd-level or lower spell that you know and that targets one or more creatures or objects. Brewing a potion takes 2 hours if its base price is 250 gp or less, otherwise brewing a potion takes 1 day for each 1,000 gp in its base price. When you create a potion, you set the caster level, which must be sufficient to cast the spell in question and no higher than your own level. To brew a potion, you must use up raw materials costing one half this base price. See the magic item creation rules in Magic Items for more information.
>
> When you create a potion, you make any choices that you would normally make when casting the spell. Whoever drinks the potion is the target of the spell.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `brew_potion` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Brilliant Planner
*(feat)*

**Tags:** General
**Prerequisites:** Int 13, character level 5th
**Source:** PZO1134 (PZO1134) p. 75
**Foundry id:** `lcBEHycuiTEcCof4`

> *Your experience and intellect enable you to create prescient plans and contingencies.*
>
> **Prerequisites**: Int 13, character level 5th.
>
> **Benefit**: You can prepare for future contingencies without defining what those preparations are until they are relevant. As a part of this preparation, while in a settlement for at least 24 hours, you can take 8 hours and spend up to 50 gp per character level, which becomes your brilliant plan fund. While you have a brilliant plan pending, you are always treated as carrying 20 additional pounds of weight, even before you define your brilliant plan.
>
> Once per day, you can take 10 minutes to enact a brilliant plan, withdrawing an item that would have been available in a settlement you visited or procuring a mundane service that your character planned ahead of time. Once you enact the plan, subtract the price of the item or service from this feat’s fund. Any item procured must weigh 10 pounds or less. Likewise, the GM must approve any nonmagical service you gain by using this feat as being appropriate for the location selected.
>
> Once you have spent all the money in your brilliant plan fund or procured 20 pounds of objects with this feat, you cannot use the feat again until you replenish your brilliant plan fund.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `brilliant_planner` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Caster's Champion
*(feat)*

**Tags:** Combat
**Prerequisites:** —
**Source:** PZO9293 (PZO9293) p. 21
**Foundry id:** `XhGkCdqvLjdyET0n`

> *You draw upon the power of an allied arcane spellcaster to enhance your weapons with magical energy.*
>
> **Benefit**: Three times per day as a swift action, when you are within 30 feet of an ally who is an arcane spellcaster, you can channel a portion of her arcane power into your weapons. For 1 round, you gain a +1 bonus on all weapon damage rolls, and your weapons are treated as magic for the purpose of overcoming damage reduction. When your base attack bonus reaches +4 and every 4 points thereafter, this bonus increases by 1, to a maximum of +5 at 16th level.
>
> **Special**: This feat counts as Arcane Strike for the purposes of prerequisites.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `caster_s_champion` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Catch Off-Guard
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 114, 119
**Foundry id:** `bZ1YdzkT8NtRIEJ4`

> *Foes are surprised by your skilled use of unorthodox and improvised weapons.*
>
> **Benefits**: You do not suffer any penalties for using an improvised melee weapon. Unarmed opponents are flat-footed against any attacks you make with an improvised melee weapon.
>
> **Normal**: You take a -4 penalty on attack rolls made with an improvised weapon.
>
> ##### Combat Trick
>
> When making an attack with an improvised weapon against an armed opponent, you can spend 5 stamina points. If you do, the target is considered flat-footed during that attack. An opponent who recognizes you and has seen you use Catch Off-Guard in this way is immune to this effect.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `catch_off_guard` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Channel Smite
*(feat)*

**Tags:** Combat, Channeling, Combat Trick
**Prerequisites:** Channel energy class feature
**Source:** Core Rulebook (PZO1110) p. 114, 119
**Foundry id:** `ftBTltVkin3Ko3NJ`

> *You can channel your divine energy through a melee weapon you wield.*
>
> **Prerequisites**: Channel energy class feature.
>
> **Benefits**: Before you make a melee attack roll, you can choose to spend one use of your channel energy ability as a swift action. If you channel positive energy and you hit an undead creature, that creature takes an amount of additional damage equal to the damage dealt by your channel positive energy ability. If you channel negative energy and you hit a living creature, that creature takes an amount of additional damage equal to the damage dealt by your channel negative energy ability. Your target can make a Will save, as normal, to halve this additional damage. If your attack misses, the channel energy ability is still expended with no effect.
>
> ##### Combat Trick
>
> When making an attack using this feat, you can spend a number of stamina points up to the number of dice in your channel energy. For each stamina point you spend in this way, add an additional 1d6 points of positive or negative energy damage to your Channel Smite attack. This damage is also halved if the target succeeds at its Will save against the Channel Smite attack.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `channel_smite` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Charging Hurler
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Point-Blank Shot
**Source:** Advanced Race Guide (PZO1131) p. 115; Bestiary (PZO1118) p. 92
**Foundry id:** `RADDhLqKsKxEROeZ`

> *You know how to use your momentum to enhance your thrown weapon attacks.*
>
> **Prerequisites**: Point-Blank Shot.
>
> **Benefits**: You can use the charge rules to make a thrown weapon attack. All the parameters of a charge apply, except that you must only move closer to your opponent, and you must end your movement within 30 feet of that opponent. If you do, you can make a single thrown weapon attack against that opponent, gaining the +2 bonus on the attack roll and taking a -2 penalty to your AC until the start of your next turn.
>
> ##### Combat Trick
>
> When using this feat, you can spend 2 stamina points to end your movement within 50 feet of your target instead of 30 feet.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `charging_hurler` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Chokehold
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Improved Grapple, Improved Unarmed Strike, base attack bonus +6 or monk level 5th
**Source:** Bestiary (PZO1118) p. 92
**Foundry id:** `fCn7TNdREiH7fzuv`

> *While grappling, you can cut off an opponent's air and blood supply.*
>
> **Prerequisites**: Improved Grapple, Improved Unarmed Strike, base attack bonus +6 or monk level 5th.
>
> **Benefits**: While you have an opponent up to one size category larger than you grappled, you can attempt a grapple combat maneuver with a -5 penalty on the check. If you succeed, you have pinned your opponent and hold the opponent in a chokehold. When you maintain the grapple, you also maintain the chokehold. A creature in a chokehold cannot breathe or speak, and thus cannot cast spells that have a verbal component. An opponent you have in a chokehold has to hold his breath or begin suffocating. Any creature that does not breathe, is immune to bleed damage, or is immune to critical hits is immune to the effects of your chokehold. When the grapple is ended, so is the chokehold.
>
> ##### Combat Trick
>
> When you attempt a chokehold, you can spend 2 stamina points to reduce the penalty to -1.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `chokehold` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Cleave
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Str 13, Power Attack, base attack bonus +1
**Source:** Core Rulebook (PZO1110) p. 116, 119
**Foundry id:** `Zeq6RWYv5otvg8q7`

> *You can strike two adjacent foes with a single swing.*
>
> **Prerequisites**: Str 13, Power Attack, base attack bonus +1.
>
> **Benefits**: As a standard action, you can make a single attack at your full base attack bonus against a foe within reach. If you hit, you deal damage normally and can make an additional attack (using your full base attack bonus) against a foe that is adjacent to the first and also within reach. You can only make one additional attack per round with this feat. When you use this feat, you take a -2 penalty to your Armor Class until your next turn.
>
> ##### Combat Trick
>
> When using the Cleave or Great Cleave feat, you can spend 4 stamina points to negate the -2 penalty to Armor Class until your next turn.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** `IMPLEMENTED` — composite action; -2 AC for the round
**Manual verdict:** `[ ]`
**Notes:**

---

### Cleaving Finish
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Str 13, Cleave, Power Attack
**Source:** Advanced Race Guide (PZO1131) p. 115; Bestiary (PZO1118) p. 92
**Foundry id:** `HdLIUDhskAwWcRBZ`

> *When you strike down an opponent, you can continue your swing into another target.*
>
> **Prerequisites**: Str 13, Cleave, Power Attack.
>
> **Benefits**: If you make a melee attack, and your target drops to 0 or fewer hit points as a result of your attack, you can make another melee attack using your highest base attack bonus against another opponent within reach. You can make only one extra attack per round with this feat.
>
> ##### Combat Trick
>
> After making a Cleaving Finish attack, if you bring another target below 0 hit points in the same round, you can spend 5 stamina points to make another Cleaving Finish attack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `cleaving_finish` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Close-Quarters Thrower
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Dex 13, Dodge, Weapon Focus with selected thrown weapon
**Source:** Bestiary (PZO1118) p. 92; Advanced Race Guide (PZO1131) p. 115
**Foundry id:** `WtVQV3QZvm2VHIAX`

> *You are agile enough to avoid melee attacks while throwing weapons or bombs.*
>
> **Prerequisites**: Dex 13, Dodge, Weapon Focus with selected thrown weapon.
>
> **Benefits**: Choose a type of thrown weapon. You do not provoke attacks of opportunity for making ranged attacks using the selected weapon. If you are an alchemist, and you select this feat and choose alchemist bombs, you do not provoke attacks of opportunity for the process of drawing components of, creating, and throwing a bomb.
>
> **Normal**: Making a ranged attack provokes attacks of opportunity.
>
> ##### Combat Trick
>
> When throwing any thrown weapon, you can spend 2 stamina points. If you do, you do not provoke attacks of opportunity for that throw.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `close_quarters_thrower` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Clustered Shots
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Point-Blank Shot, Precise Shot, base attack bonus +6
**Source:** Bestiary (PZO1118) p. 92; Advanced Race Guide (PZO1131) p. 115
**Foundry id:** `6b29HYy9MgWVO7oW`

> *You take a moment to carefully aim your shots, causing them all to strike nearly the same spot.*
>
> **Prerequisites**: Point-Blank Shot, Precise Shot, base attack bonus +6.
>
> **Benefits**: When you use a full-attack action to make multiple ranged weapon attacks against the same opponent, total the damage from all hits before applying that opponent's damage reduction.
>
> **Special**: If the massive damage optional rule is being used (Core Rulebook 189), that rule applies if the total damage you deal with this feat is equal to or exceeds half the opponent's full normal hit points (minimum 50 points of damage).
>
> ##### Combat Trick
>
> When using this feat, you can spend up to 2 stamina points for each attack that hit the same target. Increase the damage pooled by this feat by an amount equal to the number of stamina points you spent.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `clustered_shots` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Combat Casting
*(feat)*

**Tags:** General, Magic, Defensive
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 114, 119
**Foundry id:** `u7rGDZUL296QIuA0`

> *You are adept at spellcasting when threatened or distracted.*
>
> **Benefits**: You get a +4 bonus on concentration checks made to cast a spell or use a spell-like ability when casting on the defensive or while grappled.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `combat_casting` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Combat Expertise
*(feat)*

**Tags:** Combat, Defensive
**Prerequisites:** Int 13
**Source:** Core Rulebook (PZO1110) p. 114, 119
**Foundry id:** `NFxHebU1XhEs5WJh`

> *You can increase your defense at the expense of your accuracy.*
>
> **Prerequisites**: Int 13.
>
> **Benefits**: You can choose to take a -1 penalty on melee attack rolls and combat maneuver checks to gain a +1 dodge bonus to your Armor Class. When your base attack bonus reaches +4, and every +4 thereafter, the penalty increases by -1 and the dodge bonus increases by +1. You can only choose to use this feat when you declare that you are making an attack or a full-attack action with a melee weapon. The effects of this feat last until your next turn.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `IMPLEMENTED` — attack-time tradeoff; 1-round dodge AC
**Manual verdict:** `[ ]`
**Notes:**

---

### Combat Reflexes
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 114, 119-120
**Foundry id:** `h9nHYLxXvIXBTmup`

> *You can make additional attacks of opportunity.*
>
> **Benefits**: You may make a number of additional attacks of opportunity per round equal to your Dexterity bonus. With this feat, you may also make attacks of opportunity while flat-footed.
>
> **Normal**: A character without this feat can make only one attack of opportunity per round and can't make attacks of opportunity while flat-footed.
>
> **Special**: The Combat Reflexes feat does not allow a rogue to use her opportunist ability more than once per round.
>
> ##### Combat Trick
>
> When you miss with an attack of opportunity, you can spend 5 stamina points to make a second attack for the same provoking action. That second attack of opportunity takes a -5 penalty on the attack roll and costs one of your attacks of opportunity for the round.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** `NOT_IMPLEMENTED` — extra AoOs/round = Dex mod; only 1 AoO/round modeled
**Manual verdict:** `[ ]`
**Notes:**

---

### Combat Vigor
*(feat)*

**Tags:** Combat
**Prerequisites:** Con 13
**Source:** PZO9475 (PZO9475) p. 14
**Foundry id:** `LVycOywOAhOFqp5A`

> *You can quickly recuperate from devastating attacks without divine assistance.*
>
> **Prerequisites**: Con 13.
>
> **Benefit**: You gain a vigor pool with a maximum number of points equal to your Constitution bonus. As a standard action, you can spend up to 1 vigor point per 3 Hit Dice you have (minimum 1) to regain 1d6 hit points per vigor point spent (maximum 7d6). Each time you spend vigor points, you become fatigued for 1 minute. You cannot spend vigor points while fatigued or exhausted. Spending vigor points doesn’t provoke attacks of opportunity. The points in your vigor pool are replenished to their maximum after you rest for 8 hours.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `combat_vigor` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Command Undead
*(feat)*

**Tags:** General
**Prerequisites:** Channel negative energy class feature
**Source:** Core Rulebook (PZO1110) p. 114, 120
**Foundry id:** `CjLNTqNGz4zU4zpp`

> *Using foul powers of necromancy, you can command undead creatures, making them into your servants.*
>
> **Prerequisites**: Channel negative energy class feature.
>
> **Benefits**: As a standard action, you can use one of your uses of channel negative energy to enslave undead within 30 feet. Undead receive a Will save to negate the effect. The DC for this Will save is equal to 10 + 1/2 your cleric level + your Charisma modifier. Undead that fail their saves fall under your control, obeying your commands to the best of their ability, as if under the effects of control undead. Intelligent undead receive a new saving throw each day to resist your command. You can control any number of undead, so long as their total Hit Dice do not exceed your cleric level. If you use channel energy in this way, it has no other effect (it does not heal or harm nearby creatures). If an undead creature is under the control of another creature, you must make an opposed Charisma check whenever your orders conflict.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `command_undead` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Conceal Spell
*(feat)*

**Tags:** General
**Prerequisites:** Deceitful, Bluff 1 rank, Disguise 1 rank, Sleight of Hand 1 rank
**Source:** PZO1134 (PZO1134) p. 80
**Foundry id:** `1Uk54nyzdK9Yfjt4`

> *You can hide the evidence of spells you cast.*
>
> **Prerequisites**: Deceitful, Bluff 1 rank, Disguise 1 rank, Sleight of Hand 1 rank.
>
> **Benefits**: When you cast a spell or use a spell-like ability, you can attempt to conceal verbal and somatic components among other speech and gestures, and to conceal the manifestation of casting the spell, so others don't realize you're casting a spell or using a spell-like ability until it is too late. The attempt to hide the spell slows your casting slightly, such that spells that normally take a standard action to cast now take a full-round action, and spells that normally take longer than a standard action take twice as long. (Swift action spells still take a swift action.) To discover your ruse, a creature must succeed at a Perception, Sense Motive, or Spellcraft check (the creature receives an automatic check with whichever of those skills has the highest bonus) against a DC equal to 15 + your number of ranks in Bluff or Disguise (whichever is higher) + your Charisma modifier; the creature gains a bonus on its check equal to the level of the spell or spelllike ability you are concealing.
>
> If your spell has a somatic component, any creature that can see you receives a Perception or Spellcraft check (whichever has the highest bonus) against a DC equal to 15 + your number of ranks in Sleight of Hand + your Dexterity modifier; the creature gains a bonus on its check equal to the level of the spell or spell-like ability you are concealing. Since you are concealing the spell's manifestation through other actions, others observing you realize you're doing something, even if they don't realize you're casting a spell. If there is a verbal component, they still hear your loud, clear voice but don't notice the spell woven within. If an opponent fails its check, your casting also does not provoke attacks of opportunity, and an opponent that fails its check can't use readied actions that depend on realizing that you're casting a spell or using a spell-like ability, or readied actions such as counterspelling that require identifying the spell you're casting. Spells such as fireball that create an additional obvious effect (aside from the manifestation of casting that all spells and spell-like abilities share) still create that effect, though it might not be obvious who cast the spell unless it emanates from you.
>
> If a character interacts with you long enough to attempt a Sense Motive check without realizing you have been casting spells, that character can use Sense Motive to gain a hunch that you're behaving unusually.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `conceal_spell` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Craft Construct
*(feat)*

**Tags:** General, Item Creation, Monster
**Prerequisites:** Caster level 5th, Craft Magic Arms and Armor, Craft Wondrous Item
**Source:** PZO1112 (PZO1112) p. 314
**Foundry id:** `DMSYzt5jD9vk0DGy`

> *You can create construct creatures like golems.*
>
> **Prerequisites**: Caster level 5th, Craft Magic Arms and Armor, Craft Wondrous Item.
>
> **Benefit**: You can create any construct whose prerequisites you meet. The act of animating a construct takes one day for each 1,000 gp in its market price. To create a construct, you must use up raw materials costing half of its base price, plus the full cost of the basic body created for the construct. Each construct has a special section that summarizes its costs and other prerequisites. A newly created construct has average hit points for its Hit Dice.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `craft_construct` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Craft Cybernetics
*(feat)*

**Tags:** General
**Prerequisites:** Technologist, Heal 9 ranks, Knowledge (engineering) 9 ranks
**Source:** PZO9272 (PZO9272) p. 6
**Foundry id:** `0yDBOWqCLugDCUeW`

> *You can build cyberware and install it in a creature's body.*
>
> **Prerequisites**: Technologist, Heal 9 ranks, Knowledge (engineering) 9 ranks
>
> **Benefits**: You can create cybernetic items. Creating a cybernetic item takes 1 day for every 1,000 gp in the item's price. To create the object, you must use up raw materials costing half of this total price. See Crafting High-Tech Items on page 16 for more information.
>
> You can repair a broken cybernetic item if it is one that you could make. Doing so costs half the raw materials and half the time it would take to craft that item from scratch. You can also install a cybernetic item in a creature's body.
>
> See the Cybertech section on page 35 for more information on installing cyberware.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `craft_cybernetics` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Craft Magic Arms and Armor
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Caster level 5th
**Source:** Core Rulebook (PZO1110) p. 117, 120
**Foundry id:** `4hNO4OAWYF5vXphH`

> *You can create magic armor, shields, and weapons.*
>
> **Prerequisites**: Caster level 5th.
>
> **Benefits**: You can create magic weapons, armor, or shields. Enhancing a weapon, suit of armor, or shield takes 1 day for each 1,000 gp in the price of its magical features. To enhance a weapon, suit of armor, or shield, you must use up raw materials costing half of this total price. See the magic item creation rules in Magic Items for more information.
>
> The weapon, armor, or shield to be enhanced must be a masterwork item that you provide. Its cost is not included in the above cost.
>
> You can also mend a broken magic weapon, suit of armor, or shield if it is one that you could make. Doing so costs half the raw materials and half the time it would take to craft that item in the first place.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `craft_magic_arms_and_armor` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Craft Ooze
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Brew Potion, Craft Wondrous Item, Craft (alchemy) 3 ranks, caster level 5th
**Source:** PZO9445 (PZO9445) p. 22
**Foundry id:** `hmIyhTP9CuKD1E5X`

> *You can use alchemy to create dangerous ooze creatures.*
>
> **Prerequisites**: Brew Potion, Craft Wondrous Item, Craft (alchemy) 3 ranks, caster level 5th.
>
> **Benefit**: You can create living oozes as though they were magical items. Creating an ooze creature takes 1 day for each 500 gp in its construction cost. To create an ooze, you must have access to an oozing vat (see below), you must use up raw materials worth the construction cost of the ooze, and you must succeed at a Craft (alchemy) check (DC 10 + 2 × the ooze’s CR). A failed check ruins the materials used, while a check that fails by 5 or more also results in an ooze that attacks its creator for 1d4 rounds before dissipating into useless waste material. A newly created ooze has average hit points for its Hit Dice. Oozes created with this feat are mindless and uncontrolled, and even normally intelligent oozes like slithering trackers that are created this way have no Intelligence score—nor any loyalty to their creator.
>
> While ooze creatures cannot normally be purchased in traditional marketplaces, GMs who wish to include such an option in their games—perhaps with oozes sold as black market commodities— need only double the construction cost of a specific ooze creature in order to figure out a fair market price.
>
> The following table lists some of the most commonly crafted oozes and their creation requirements. At the GM’s discretion, other types of ooze creatures can be created with this feat. Creatures from Pathfinder RPG Bestiary 2, 3, or 4 are marked with a matching superscript.
>
>
> Ooze
>
>
> Construction Cost
>
>
> Craft DC
>
>
> Gelatinous cube
>
>
> 1,600 GP
>
>
> 16
>
>
> Gray ooze
>
>
> 3,600 GP
>
>
> 18
>
>
> Slithering trackerB2
>
>
> 3,600 GP
>
>
> 18
>
>
> Ochre jelly
>
>
> 4,900 GP
>
>
> 20
>
>
> Black pudding
>
>
> 8,100 GP
>
>
> 24
>
>
> Magma oozeB2
>
>
> 8,100 GP
>
>
> 24
>
>
> Deathtrap oozeB3
>
>
> 8,100 GP
>
>
> 26
>
>
> Carnivorous crystalB3
>
>
> 16,900 GP
>
>
> 32

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `craft_ooze` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Craft Pharmaceutical
*(feat)*

**Tags:** General
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 6
**Foundry id:** `9SLkAHfOX4UEnkmS`

> *You can craft pharmaceuticals.*
>
> **Prerequisites: **Technologist, Heal 9 ranks, Knowledge (nature) 9 ranks
>
> **Benefits**: You can create any pharmaceutical or poison. Creating a pharmaceutical takes 2 hours if its base price is 250 gp or less; otherwise, the creation of the pharmaceutical takes 1 day for every 1,000 gp in its price. To create the pharmaceutical or poison, you must use up raw materials costing half of this total price. See Crafting High-Tech Items on page 16 for more information.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `craft_pharmaceutical` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Craft Poppet
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Caster level 1st
**Source:** PZO9481 (PZO9481) p. 31
**Foundry id:** `EdcHghQAYBIDao3s`

> *Some construct builders learn their art by creating poppets.*
>
> **Prerequisites**: Caster level 1st.
>
> **Benefit**: You can craft poppets and add augmentations to existing poppets that you control. You are treated as having both Craft Arms and Armor and Craft Wondrous Item for the purpose of fulfilling the prerequisites for Craft Construct.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `craft_poppet` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Craft Robot
*(feat)*

**Tags:** General
**Prerequisites:** Craft Technological Arms and Armor, Craft Technological Item, Technologist, Craft (mechanical) 9 ranks, Knowledge (engineering) 9 ranks
**Source:** PZO9090 (PZO9090) p. 71
**Foundry id:** `XEe84rVBLzlDq7Ae`

> *You can build robots.*
>
> **Prerequisites**: Craft Technological Arms and Armor, Craft Technological Item, Technologist, Craft (mechanical) 9 ranks, Knowledge (engineering) 9 ranks.
>
> **Benefits**: You can create robots, provided you have access to a robotics lab and the necessary materials. A robot's price is equal to its CR x 20,000 gp, and the cost to create one is half this amount. Creating a robot takes 1 day for every 1,000 gp of its price. At the end of the process you must attempt a single Craft (mechanical) skill check to finish the robot. Failing this check means that the robot doesn't function and the materials and time are wasted. The DC for this skill check is equal to 20 + the robot's CR (minimum 21). A newly created robot has average hit points for its Hit Dice.
>
> **Special**: A robotics lab is required to craft robots and uses 200 charges each day it is in operation. See page 16 of Pathfinder Campaign Setting: Technology Guide for more information on technological laboratories.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `craft_robot` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Craft Rod
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Caster level 9th
**Source:** Core Rulebook (PZO1110) p. 117, 120
**Foundry id:** `rt2cBQvEU0ANE3z4`

> *You can create magic rods.*
>
> **Prerequisites**: Caster level 9th.
>
> **Benefits**: You can create magic rods. Crafting a rod takes 1 day for each 1,000 gp in its base price. To craft a rod, you must use up raw materials costing half of its base price. See the magic item creation rules in Magic Items for more information.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `craft_rod` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Craft Shadow Piercing
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Craft (jewelry) 5 ranks, caster level 5th
**Source:** PZO9450 (PZO9450) p. 28
**Foundry id:** `ecPbtSHMr6hCIjrt`

> *You can craft magical piercings infused with the power of shadow.*
>
> **Prerequisites**: Craft (jewelry) 5 ranks, caster level 5th.
>
> **Benefit**: You can create special wondrous items—typically barbs, hooks, rings, and spikes—that adorn piercings in the wearer’s flesh and grant magical abilities. Both you and the recipient of the piercing (if not yourself) must be present for the entire piercing process.
>
> Shadow piercings must be placed in a part of the body normally associated with a magic item slot, but they do not take up a slot on the body, nor interfere with other magic items that use those slots. A single slot can only hold one shadow piercing (nonmagical piercings do not count against this limit). Shadow piercings can be applied to the following slots: belt, body, chest, eyes, feet, hands, head, neck, shoulder, and wrist.
>
> A single slot can hold multiple physical piercings, though the pieces of jewelry operate as a single item and must be created for that purpose. Shadow piercings have different levels of power: minor, major, and greater. Minor shadow piercings usually include one piece of jewelry, while major and greater shadow piercings often are made up of multiple rings and spikes that cover the entire area of the piercing’s slot (but are still considered a single item). A creature can only use a number of shadow piercings equal its Constitution modifier plus its Wisdom modifier.
>
> Carefully inserting or removing a shadow piercing takes a full-round action and deals no damage. Alternatively, a shadow piercing may be pulled out of a creature using the steal maneuver as a standard action that deals 1d6 points of damage. Only a creature with the Craft Shadow Piercing feat may create or insert a shadow piercing, but any creature may remove one. Inserting a shadow piercing is impossible unless the target is willing or helpless. After being removed, a shadow piercing may be inserted into another creature by someone with this feat. Since they are treated as magic items, they are affected by dispel magic.
>
> Shadow piercings follow the rules for magic item creation, except the creator can use the Craft (jewelry) skill instead of Spellcraft. New shadow piercings can be researched and designed using the rules for pricing new magic items. Shadow piercing powers for a specific slot must be thematically similar or linked. Since shadow piercings don’t interfere with other magic items in the same slot, but can only have one piercing per slot, the base price is multiplied by 1.5 instead of doubled as if they had no space limitation.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `craft_shadow_piercing` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Craft Staff
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Caster level 11th
**Source:** Core Rulebook (PZO1110) p. 117, 120
**Foundry id:** `lIlQnrRkC3YJ1V6t`

> *You can create magic staves.*
>
> **Prerequisites**: Caster level 11th.
>
> **Benefits**: You can create any staff whose prerequisites you meet. Crafting a staff takes 1 day for each 1,000 gp in its base price. To craft a staff, you must use up raw materials costing half of its base price. A newly created staff has 10 charges. See the magic item creation rules in Magic Items for more information.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `craft_staff` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Craft Technological Arms and Armor
*(feat)*

**Tags:** General
**Prerequisites:** Technologist, Craft (mechanical) 7 ranks, Knowledge (engineering) 7 ranks
**Source:** PZO9272 (PZO9272) p. 6
**Foundry id:** `SkiZsGPMlsMNeBhf`

> *You can build technological weapons and armor.*
>
> **Prerequisites**: Technologist, Craft (mechanical) 7 ranks, Knowledge (engineering) 7 ranks
>
> **Benefits**: You can create technological weapons or armor. Creating a technological weapon or suit of armor takes 1 day for every 1,000 gp in the item's price. To create the object, you must use up raw materials costing half of this total price. See Crafting High-Tech Items on page 16 for more information.
>
> You can also repair a broken technological weapon or suit of armor if it is one that you could make. Doing so costs half the raw materials and half the time it would take to craft that item from scratch.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `craft_technological_arms_and_armor` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Craft Technological Item
*(feat)*

**Tags:** General
**Prerequisites:** Technologist, Craft (mechanical) 5 ranks, Knowledge (engineering) 5 ranks
**Source:** PZO9272 (PZO9272) p. 6
**Foundry id:** `u9wRB7bsYgX0jCdk`

> *You can craft technological gear and items.*
>
> **Prerequisites**: Technologist, Craft (mechanical) 5 ranks, Knowledge (engineering) 5 ranks
>
> **Benefits**: You can create technological gear. Creating a piece of technological gear takes 1 day for every 1,000 gp in the item's price. To create the object, you must use up raw materials costing half of this total price. See Crafting High- Tech Items on page 16 for more information.
>
> You can also repair a broken technological item if it is one that you could make. Doing so costs half the raw materials and half the time it would take to craft that item from scratch.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `craft_technological_item` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Craft Wand
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Caster level 5th
**Source:** Core Rulebook (PZO1110) p. 117, 120
**Foundry id:** `V6du9lXESc2spA7B`

> *You can create magic wands.*
>
> **Prerequisites**: Caster level 5th.
>
> **Benefits**: You can create a wand of any 4th-level or lower spell that you know. Crafting a wand takes 1 day for each 1,000 gp in its base price. To craft a wand, you must use up raw materials costing half of this base price. A newly created wand has 50 charges. See the magic item creation rules in Magic Items for more information.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `craft_wand` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Craft Wondrous Item
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Caster level 3rd
**Source:** Core Rulebook (PZO1110) p. 117, 120
**Foundry id:** `tD76K8QGco9scT0r`

> *You can create wondrous items, a type of magic item.*
>
> **Prerequisites**: Caster level 3rd.
>
> **Benefits**: You can create a wide variety of magic wondrous items. Crafting a wondrous item takes 1 day for each 1,000 gp in its price. To create a wondrous item, you must use up raw materials costing half of its base price. See the magic item creation rules in Magic Items for more information.
>
> You can also mend a broken wondrous item if it is one that you could make. Doing so costs half the raw materials and half the time it would take to craft that item.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `craft_wondrous_item` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Create Enhanced Firearm
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Craft Magic Arms and Armor; Craft (weapons) 1 rank or Gunsmithing
**Source:** PZO9486 (PZO9486) p. 26
**Foundry id:** `WmXRmJIpmK9nejvC`

> *You can craft superior firearms.*
>
> **Prerequisites**: Craft Magic Arms and Armor; Craft (weapons) 1 rank or Gunsmithing.
>
> **Benefit**: When you craft a firearm or magical firearm, you can use reinforced components to make the weapon more reliable. This increases the item’s total construction cost by 10%. The misfire chance of the weapon is reduced by 1. This can never reduce a firearm’s misfire chance by more than 1.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `create_enhanced_firearm` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Critical Focus
*(feat)*

**Tags:** Combat, Critical, Combat Trick
**Prerequisites:** Base attack bonus +9
**Source:** Core Rulebook (PZO1110) p. 114, 120
**Foundry id:** `JNlMhMhcDO8wkXiw`

> *You are trained in the art of causing pain.*
>
> **Prerequisites**: Base attack bonus +9.
>
> **Benefits**: You receive a +4 circumstance bonus on attack rolls made to confirm critical hits.
>
> ##### Combat Trick
>
> If your successful critical confirmation roll is a natural 19 or 20, you can spend 2 stamina points to roll another confirmation roll. If this confirmation roll also succeeds, increase your critical multiplier by 1 for this attack, and you can roll again. If you continue to roll 19 or 20, you can continue to spend stamina points for additional rolls, and the increases to the critical multiplier stack.

**Mechanical encoding:** `changes`: 1
  - `4` → `critConfirm`  (circumstance)

**In our coverage tracker:** absent (slug `critical_focus` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Critical Mastery
*(feat)*

**Tags:** Combat, Critical
**Prerequisites:** Critical Focus, any two critical feats, 14th-level fighter
**Source:** Core Rulebook (PZO1110) p. 114, 120
**Foundry id:** `lRWXptGqGabk1vfH`

> *Your critical hits cause two additional effects.*
>
> **Prerequisites**: Critical Focus, any two critical feats, 14th-level fighter.
>
> **Benefits**: When you score a critical hit, you can apply the effects of two critical feats in addition to the damage dealt.
>
> **Normal**: You can only apply the effects of one critical feat to a given critical hit in addition to the damage dealt.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `critical_mastery` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Crossbow Mastery
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Dex 15, Point-Blank Shot, Rapid Reload, Rapid Shot
**Source:** Advanced Player's Guide (PZO1115) p. 157; PZO9000-2S (PZO9000-2S) p. 10; Advanced Race Guide (PZO1131) p. 116; PZO1111 (PZO1111) p. 218
**Foundry id:** `cKthdANSm9kgKc29`

> *You can load crossbows with blinding speed and even fire them in melee with little fear of reprisal.*
>
> **Prerequisites**: Dex 15, Point-Blank Shot, Rapid Reload, Rapid Shot.
>
> **Benefits**: The time required for you to reload any type of crossbow is reduced to a free action, regardless of the type of crossbow used. You can fire a crossbow as many times in a full attack action as you could attack if you were using a bow. Reloading a crossbow for the type of crossbow you chose when you took Rapid Reload no longer provokes attacks of opportunity.
>
> **Special**: Starting at 6th level, a ranger with the archery combat style may select Crossbow Mastery as a combat style feat.
>
> ##### Combat Trick
>
> As long as you have at least 1 stamina point in your stamina pool, reloading any kind of crossbow no longer provokes attacks of opportunity.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `crossbow_mastery` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Crushing Impact
*(feat)*

**Tags:** Combat
**Prerequisites:** Str 13, Improved Bull Rush, Improved Unarmed Strike, Power Attack
**Source:** PZO9493 (PZO9493) p. 24
**Foundry id:** `PjyRS3MdzvsVPyN8`

> *You slam into your foes with brute strength as unyielding as a wall.*
>
> **Prerequisites**: Str 13, Improved Bull Rush, Improved Unarmed Strike, Power Attack.
>
> **Benefit**: Whenever you successfully bull rush an enemy and its movement is stopped by a solid object or barrier, you deal your unarmed strike damage to the foe, as long as it’s within your threatened area. If you performed your bull rush as part of a charge, you gain a +2 bonus on your damage roll.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `crushing_impact` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Cultivate Magic Plants
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Brew Potion, Craft Wondrous Item, Knowledge (nature) 1 rank
**Source:** Occult Adventures (PZO1140) p. 109
**Foundry id:** `57ELWypg7Rq3XBwG`

> *You combine a natural green thumb and knowledge of magic in order to grow magic plants.*
>
> **Prerequisites**: Brew Potion, Craft Wondrous Item, Knowledge (nature) 1 rank.
>
> **Benefit**: You can cultivate magic plants. Cultivating a magic plant takes 1 week per 1,000 gp in its base price. When you create a magic plant, you make the same choices that you would normally make when casting the spell. Whoever consumes the fruit of the magic plant is the target of the spell.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `cultivate_magic_plants` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Dazzling Display
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Weapon Focus, proficiency with the selected weapon
**Source:** Core Rulebook (PZO1110) p. 117, 120
**Foundry id:** `3cq9YbgcMrAXC76j`

> *Your skill with your favored weapon can frighten enemies.*
>
> **Prerequisites**: Weapon Focus, proficiency with the selected weapon.
>
> **Benefits**: While wielding the weapon in which you have Weapon Focus, you can perform a bewildering show of prowess as a full-round action. Make an Intimidate check to demoralize all foes within 30 feet who can see your display.
>
> ##### Combat Trick
>
> When wielding a melee weapon with which you have Weapon Focus, you can make a single melee attack as a standard action against a foe. If the attack hits, you can select any number of foes within 30 feet who saw the attack, including that foe. Spend 2 stamina points per foe you have selected, then attempt an Intimidate check to demoralize those foes.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `dazzling_display` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Deadly Aim
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Dex 13, base attack bonus +1
**Source:** Core Rulebook (PZO1110) p. 114, 121
**Foundry id:** `K4FEFu94JKOP2l51`

> *You can make exceptionally deadly ranged attacks by pinpointing a foe's weak spot, at the expense of making the attack less likely to succeed.*
>
> **Prerequisites**: Dex 13, base attack bonus +1.
>
> **Benefits**: You can choose to take a -1 penalty on all ranged attack rolls to gain a +2 bonus on all ranged damage rolls. When your base attack bonus reaches +4, and every +4 thereafter, the penalty increases by -1 and the bonus to damage increases by +2. You must choose to use this feat before making an attack roll and its effects last until your next turn. The bonus damage does not apply to touch attacks or effects that do not deal hit point damage.
>
> ##### Combat Trick
>
> When using this feat, you can spend 4 stamina points to reduce the penalty to attack rolls imposed by the feat by 1 until the beginning of your next turn. You can't reduce the penalty below 0.
>
> **Usage**: select Conditional Modifier when performing a ranged attack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `deadly_aim` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Deadly Finish
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Base attack bonus +11
**Source:** Bestiary (PZO1118) p. 94; Advanced Race Guide (PZO1131) p. 116
**Foundry id:** `sWnRp7fvHlK2egrw`

> *Your attacks don't just fell your opponents--they kill them outright.*
>
> **Prerequisites**: Base attack bonus +11.
>
> **Benefits**: When you hit with a melee attack and reduce your opponent to -1 or fewer hit points, you can force that opponent to succeed at a Fortitude save (DC 15 + the damage your attack dealt) or die.
>
> ##### Combat Trick
>
> When you reduce an opponent to 0 hit points, you can spend 2 stamina points to force the creature to succeed at the saving throw for Deadly Finish or die.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `deadly_finish` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Deadly Stroke
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Dazzling Display, Greater Weapon Focus, Shatter Defenses, Weapon Focus, proficiency with the selected weapon, base attack bonus +11
**Source:** Core Rulebook (PZO1110) p. 117, 121
**Foundry id:** `en3iH9cxZtYQNd08`

> *With a well-placed strike, you can bring a swift and painful end to most foes.*
>
> **Prerequisites**: Dazzling Display, Greater Weapon Focus, Shatter Defenses, Weapon Focus, proficiency with the selected weapon, base attack bonus +11.
>
> **Benefits**: As a standard action, make a single attack with the weapon for which you have Greater Weapon Focus against a stunned or flat-footed opponent. If you hit, you deal double the normal damage and the target takes 1 point of Constitution bleed (see Conditions). The additional damage and bleed is not multiplied on a critical hit.
>
> ##### Combat Trick
>
> You can spend 5 stamina points to make a Deadly Stroke attack against a dazed opponent, or 10 stamina points to make a Deadly Stroke against an opponent you are flanking.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `deadly_stroke` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Deafening Critical
*(feat)*

**Tags:** Combat, Critical, Combat Trick
**Prerequisites:** Critical Focus, base attack bonus +13
**Source:** Core Rulebook (PZO1110) p. 114, 121
**Foundry id:** `RE14LhYMDTcjAyHd`

> *Your critical hits cause enemies to lose their hearing.*
>
> **Prerequisites**: Critical Focus, base attack bonus +13.
>
> **Benefits**: Whenever you score a critical hit against an opponent, the victim is permanently deafened. A successful Fortitude save reduces the deafness to 1 round. The DC of this Fortitude save is equal to 10 + your base attack bonus. This feat has no effect on deaf creatures. This deafness can be cured by heal, regeneration, remove deafness, or a similar ability.
>
> **Special**: You can only apply the effects of one critical feat to a given critical hit unless you possess Critical Mastery.
>
> ##### Combat Trick
>
> When you confirm a critical hit and attempt to deafen an opponent with this feat, you can spend up to 5 stamina points to increase the DC of this feat's saving throw by an amount equal to the number of stamina points you spent.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `deafening_critical` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Death or Glory
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Str 13, Power Attack, base attack bonus +6
**Source:** Advanced Race Guide (PZO1131) p. 117; Bestiary (PZO1118) p. 94
**Foundry id:** `B3D3sXpydYZrgAuB`

> *Even when facing a larger foe, you aren't afraid to take great risks in order to finish the fight.*
>
> **Prerequisites**: Str 13, Power Attack, base attack bonus +6.
>
> **Benefits**: Against a creature of size Large or larger, you can make a single melee attack as a full-round action, gaining a +4 bonus on the attack roll, damage roll, and critical confirmation roll. You gain an additional +1 on this bonus at base attack bonus +11, +16, and +20 (for a maximum of +7 at base attack +20). After you resolve your attack, the opponent you attack can spend an immediate action to make a single melee attack against you with the same bonuses.
>
> **Special**: You can combine the full-round action attack this feat allows with the benefit of Vital Strike, Improved Vital Strike, or Greater Vital Strike.
>
> ##### Combat Trick
>
> When you make a Death or Glory attack, you can spend 5 stamina points to automatically negate the opponent's immediate-action attack against you after it takes the action but before it rolls the attack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `death_or_glory` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Deceitful
*(feat)*

**Tags:** General
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 114, 121
**Foundry id:** `SUACufUXl12sUvnQ`

> *You are skilled at deceiving others, both with the spoken word and with physical disguises.*
>
> **Benefits**: You get a +2 bonus on all Bluff and Disguise skill checks. If you have 10 or more ranks in one of these skills, the bonus increases to +4 for that skill.

**Mechanical encoding:** `changes`: 2
  - `2 + if(gte(@skills.blf.rank, 10), 2)` → `skill.blf`  (untyped)
  - `2 + if(gte(@skills.dis.rank, 10), 2)` → `skill.dis`  (untyped)

**In our coverage tracker:** absent (slug `deceitful` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Defensive Combat Training
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 114, 121
**Foundry id:** `F9mKy0SmRo4bTdni`

> *You excel at defending yourself from all manner of combat maneuvers.*
>
> **Benefits**: You treat your total Hit Dice as your base attack bonus when calculating your Combat Maneuver Defense (see Combat).
>
> ##### Combat Trick
>
> When targeted with a combat maneuver, you can spend any number of stamina points to gain a bonus to your CMD equal to the number of stamina points you spent.

**Mechanical encoding:** `changes`: 1
  - `@attributes.hd.total - @attributes.bab.total` → `cmd`  (untyped)

**In our coverage tracker:** absent (slug `defensive_combat_training` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Deflect Arrows
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Dex 13, Improved Unarmed Strike
**Source:** Core Rulebook (PZO1110) p. 115, 121
**Foundry id:** `ACEQfonKVqh0fwkK`

> *You can knock arrows and other projectiles off course, preventing them from hitting you.*
>
> **Prerequisites**: Dex 13, Improved Unarmed Strike.
>
> **Benefits**: You must have at least one hand free (holding nothing) to use this feat. Once per round when you would normally be hit with an attack from a ranged weapon, you may deflect it so that you take no damage from it. You must be aware of the attack and not flat-footed. Attempting to deflect a ranged attack doesn't count as an action. Unusually massive ranged weapons (such as boulders or ballista bolts) and ranged attacks generated by natural attacks or spell effects can't be deflected.
>
> ##### Combat Trick
>
> You can spend 5 stamina points to deflect an arrow while you're flat-footed. You must still be aware of the attack.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `deflect_arrows` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Deft Hands
*(feat)*

**Tags:** General, Skill
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 114, 121
**Foundry id:** `SMyexRzOm5PfjT5I`

> *You have exceptional manual dexterity.*
>
> **Benefits**: You get a +2 bonus on Disable Device and Sleight of Hand skill checks. If you have 10 or more ranks in one of these skills, the bonus increases to +4 for that skill.

**Mechanical encoding:** `changes`: 2
  - `2 + if(gte(@skills.slt.rank, 10), 2)` → `skill.slt`  (untyped)
  - `2 + if(gte(@skills.dev.rank, 10), 2)` → `skill.dev`  (untyped)

**In our coverage tracker:** absent (slug `deft_hands` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Deific Obedience
*(feat)*

**Tags:** General
**Prerequisites:** Knowledge (religion) 3 ranks, must worship a deity
**Source:** PZO92112 (PZO92112) p. 4; PZO9267 (PZO9267) p. 210; PZO9290 (PZO9290) p. 3
**Foundry id:** `FoH6mHqWlkYnWLF6`

> *Your reverence for a deity is so great that daily prayer and minor sacrifices grant you special boons.*
>
> **Prerequisites**: Knowledge (religion) 3 ranks, must worship a deity.
>
> **Benefits**: Each deity requires a different daily obedience, but all obediences take no more than 1 hour per day to perform. Once you've performed the obedience, you gain the benefit of a special ability or resistance as indicated in the Obedience entry for the god to whom you performed the obedience.
>
> If you have at least 12 Hit Dice, you also gain the first boon granted by your deity upon undertaking your obedience. If you have at least 16 Hit Dice, you also gain the second boon. If you have 20 Hit Dice or more, you also gain the third boon. Unless a specific duration or number of uses per day is listed, a boons effects are constant. If you have levels in the evangelist, exalted, or sentinel prestige classes, you gain access to these boons at lower levels as a benefit of your prestige class. If you have no levels in one of these prestige classes, you gain the boons marked as exalted boons. If you later take levels in sentinel or evangelist, you lose access to the exalted boons and gain access to the new boons appropriate to your class.
>
> If you ever fail to perform a daily obedience, you lose all access to the benefits and boons granted by this feat until you next perform the obedience.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `deific_obedience` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Diehard
*(feat)*

**Tags:** General
**Prerequisites:** Endurance
**Source:** Core Rulebook (PZO1110) p. 115, 122
**Foundry id:** `O0e0UCim27GPKFuW`

> *You are especially hard to kill. Not only do your wounds automatically stabilize when grievously injured, but you can remain conscious and continue to act even at death's door.*
>
> **Prerequisites**: Endurance.
>
> **Benefits**: When your hit point total is below 0, but you are not dead, you automatically stabilize. You do not need to make a Constitution check each round to avoid losing additional hit points. You may choose to act as if you were disabled, rather than dying. You must make this decision as soon as you are reduced to negative hit points (even if it isn't your turn). If you do not choose to act as if you were disabled, you immediately fall unconscious.
>
> When using this feat, you are staggered. You can take a move action without further injuring yourself, but if you perform any standard action (or any other action deemed as strenuous, including some swift actions, such as casting a quickened spell) you take 1 point of damage after completing the act. If your negative hit points are equal to or greater than your Constitution score, you immediately die.
>
> **Normal**: A character without this feat who is reduced to negative hit points is unconscious and dying.
>
> Usage: apply Staggered condition.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `NOT_IMPLEMENTED` — act normally while dying
**Manual verdict:** `[ ]`
**Notes:**

---

### Dirty Fighting
*(feat)*

**Tags:** Combat
**Prerequisites:** —
**Source:** PZO9459 (PZO9459) p. 14
**Foundry id:** `KSc5UH9Os4iqzK3M`

> *You can take advantage of a distracted foe.*
>
> **Benefit**: When you attempt a combat maneuver check against a foe you are flanking, you can forgo the +2 bonus on your attack roll for flanking to instead have the combat maneuver not provoke an attack of opportunity. If you have a feat or ability that allows you to attempt the combat maneuver without provoking an attack of opportunity, you can instead increase the bonus on your attack roll for flanking to +4 for the combat maneuver check.
>
> **Special**: This feat counts as having Dex 13, Int 13, Combat Expertise, and Improved Unarmed Strike for the purposes of meeting the prerequisites of the various improved combat maneuver feats, as well as feats that require those improved combat maneuver feats as prerequisites.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `dirty_fighting` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Disarming Strike
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Int 13, Combat Expertise, Improved Disarm, base attack bonus +9
**Source:** Advanced Player's Guide (PZO1115) p. 157; Advanced Race Guide (PZO1131) p. 117
**Foundry id:** `7pQ5ew0XWvQaT826`

> *Your critical hits can disarm your foes.*
>
> **Prerequisites**: Int 13, Combat Expertise, Improved Disarm, base attack bonus +9.
>
> **Benefits**: Whenever you score a critical hit with a melee attack, you can disarm your opponent, in addition to the normal damage dealt by the attack. If your confirmation roll exceeds your opponent's CMD, you may disarm your opponent as if from the disarm combat maneuver. This does not provoke an attack of opportunity.
>
> **Normal**: You must perform a disarm combat maneuver to disarm an opponent.
>
> **Special**: You can only apply the effects of one of the following feats to a given critical hit
>
> ##### Combat Trick
>
> When you fail to confirm a critical hit with a melee attack, you can spend 2 stamina points to attempt to disarm the target anyway. When you do, reroll the confirmation roll and use it to determine if the disarm attempt exceeds the opponent's CMD. This reroll is used only for the disarm combat maneuver; it can't cause the critical to be confirmed. You still can't make the attempt if the target is immune to critical hits.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `disarming_strike` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Disengaging Feint
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Int 13, Combat Expertise, Improved Feint
**Source:** Advanced Race Guide (PZO1131) p. 117; Bestiary (PZO1118) p. 96
**Foundry id:** `86WJUgilNgbeQXBH`

> *You can feint to disengage from combat.*
>
> **Prerequisites**: Int 13, Combat Expertise, Improved Feint.
>
> **Benefits**: As a standard action, use Bluff to feint against an opponent. Instead of denying that opponent his Dexterity bonus to AC, a successful feint allows you to move up to your speed without provoking an attack of opportunity from the opponent you feinted for leaving the square you start in.
>
> ##### Combat Trick
>
> You can select this feat even if you don't meet the ability score prerequisite (Intelligence 13). You gain the benefits of this feat only as long as you have at least 1 stamina point in your stamina pool. You can spend 5 stamina points to attempt a Disengaging Feint as a move action instead of a standard action.

**Mechanical encoding:** has `actions`, has `scriptCalls`

**In our coverage tracker:** absent (slug `disengaging_feint` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Disengaging Flourish
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Int 13, Combat Expertise, Disengaging Feint, Improved Feint
**Source:** Bestiary (PZO1118) p. 96; Advanced Race Guide (PZO1131) p. 118
**Foundry id:** `PehrgtZkD4jn5PUV`

> *Distracting your opponents gives you the opportunity to make a swift retreat.*
>
> **Prerequisites**: Int 13, Combat Expertise, Disengaging Feint, Improved Feint.
>
> **Benefits**: As a standard action, make a Bluff check against each opponent that currently threatens you. If you succeed against at least one opponent, you can move up to your speed. This movement does not provoke attacks of opportunity from any opponent you succeeded at feinting against.
>
> ##### Combat Trick
>
> You can select this feat even if you don't meet the ability score prerequisite (Intelligence 13). You gain the benefits of this feat only as long as you have at least 1 stamina point in your stamina pool. You can spend 5 stamina points to make a Disengaging Flourish attempt as a move action instead of a standard action.

**Mechanical encoding:** has `actions`, has `scriptCalls`

**In our coverage tracker:** absent (slug `disengaging_flourish` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Disengaging Shot
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Int 13, Combat Expertise, Disengaging Feint, Dodge, Improved Feint, Mobility
**Source:** Bestiary (PZO1118) p. 96; Advanced Race Guide (PZO1131) p. 118
**Foundry id:** `Fir5fuh0SqWX6wtw`

> *You make one last attack before beating a hasty retreat.*
>
> **Prerequisites**: Int 13, Combat Expertise, Disengaging Feint, Dodge, Improved Feint, Mobility.
>
> **Benefits**: Whenever you use Disengaging Feint or Disengaging Flourish, you can make a single melee attack against one opponent you succeeded at feinting against. That opponent is denied his Dexterity bonus to AC against this attack.
>
> ##### Combat Trick
>
> You can select this feat even if you don't meet the ability score prerequisite (Intelligence 13). You gain the benefit of this feat only as long as you have at least 1 stamina point in your stamina pool. Just before you attempt your free melee attack with Disengaging Shot, you can spend up to 5 stamina points. If you do, increase the attack's damage by 2 points for each stamina point you spent.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `disengaging_shot` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Disruptive
*(feat)*

**Tags:** Combat, Offensive
**Prerequisites:** 6th-level fighter
**Source:** Core Rulebook (PZO1110) p. 114, 122
**Foundry id:** `QaMwiDFQdDwycTUO`

> *Your training makes it difficult for enemy spellcasters to safely cast spells near you.*
>
> **Prerequisites**: 6th-level fighter.
>
> **Benefits**: The DC to cast spells defensively increases by +4 for all enemies that are within your threatened area. This increase to casting spells defensively only applies if you are aware of the enemy's location and are capable of taking an attack of opportunity. If you can only take one attack of opportunity per round and have already used that attack, this increase does not apply.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `disruptive` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Distance Thrower
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Str 13
**Source:** Advanced Race Guide (PZO1131) p. 118; Bestiary (PZO1118) p. 97
**Foundry id:** `vRjWh9GGi2iUzmsF`

> *You are accurate with thrown weapons at longer ranges than normal.*
>
> **Prerequisites**: Str 13.
>
> **Benefits**: With a thrown weapon, you reduce your penalty on ranged attack rolls due to range by 2.
>
> ##### Combat Trick
>
> Thrown weapons wielded by you have twice their normal range.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `distance_thrower` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Dodge
*(feat)*

**Tags:** Combat, Defensive
**Prerequisites:** Dex 13
**Source:** Core Rulebook (PZO1110) p. 114, 122
**Foundry id:** `JreaiTHdyWFNj3Tb`

> *Your training and reflexes allow you to react swiftly to avoid an opponents' attacks.*
>
> **Prerequisites**: Dex 13.
>
> **Benefits**: You gain a +1 dodge bonus to your AC. A condition that makes you lose your Dex bonus to AC also makes you lose the benefits of this feat.

**Mechanical encoding:** `changes`: 1
  - `1` → `ac`  (dodge)

**In our coverage tracker:** `IMPLEMENTED` — +1 dodge AC
**Manual verdict:** `[ ]`
**Notes:**

---

### Dolphin Circle
*(feat)*

**Tags:** Combat
**Prerequisites:** Dolphin Dart, Dolphin Style, Improved Unarmed Strike, Swim 10 ranks, base attack bonus +10 or monk level 10th
**Source:** PZO92102 (PZO92102) p. 57-58
**Foundry id:** `TF9tm6ls38bkwqij`

> *You circle your foes like dolphins, forcing them to play into your attacks.*
>
> **Prerequisites**: Dolphin Dart, Dolphin Style, Improved Unarmed Strike, Swim 10 ranks, base attack bonus +10 or monk level 10th.
>
> **Benefits**: While in Dolphin Style, as a full-round action underwater you can choose a circular path starting and ending in your current space whose length is no longer than you could swim with a single move action. You circle around that path until your next turn, and this movement doesn't provoke attacks of opportunity. You are considered to be in every space along the path for the purpose of threatening squares and providing flanking for other allies (but not yourself ), as well as whether you are in the area of an area effect. Other creatures can attack you (and touch you with beneficial touch spells) as if you were in every space along the path. However, you don't count as being in any of the spaces for the purpose of other creatures moving through an occupied space. At the beginning of your next turn, choose any space along the path to stop circling.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `dolphin_circle` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Dolphin Dart
*(feat)*

**Tags:** Combat
**Prerequisites:** Dolphin Style, Improved Unarmed Strike, Swim 6 ranks, base attack bonus +6 or monk level 6th
**Source:** PZO92102 (PZO92102) p. 58
**Foundry id:** `W5w7Az6CbDm6bgpE`

> *Like a dolphin, you can quickly dart at a foe and retreat.*
>
> **Prerequisites**: Dolphin Style, Improved Unarmed Strike, Swim 6 ranks, base attack bonus +6 or monk level 6th.
>
> **Benefits**: While in Dolphin Style, as a standard action underwater you can move up to half your swim speed, make a single melee attack against a creature within your reach, and then retreat back to your previous position. Your movement and attack don't provoke attacks of opportunity, even if your foe has an ability that allows attacks of opportunity with triggers other than moving out of a threatened area.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `dolphin_dart` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Dolphin Style
*(feat)*

**Tags:** Combat, Style
**Prerequisites:** Improved Unarmed Strike, Swim 3 ranks, base attack bonus +3 or monk level 3rd
**Source:** PZO92102 (PZO92102) p. 58
**Foundry id:** `tFWADj9sdIRLjdOY`

> *You fight like a dolphin, bunching your enemies up together to make it easier to pick them off.*
>
> **Prerequisites**: Improved Unarmed Strike, Swim 3 ranks, base attack bonus +3 or monk level 3rd.
>
> **Benefits**: You gain a +1 bonus on melee attack rolls against any creature adjacent to at least two of its other allies as long as you aren't flanking that creature, and your melee attacks ignore any bonus to AC gained by use of the aid another action.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `dolphin_style` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Double Slice
*(feat)*

**Tags:** Combat, Offensive, Two Weapons, Weapon
**Prerequisites:** Dex 15, Two-Weapon Fighting
**Source:** Core Rulebook (PZO1110) p. 116, 122
**Foundry id:** `VK8TgwfjeomMwGjd`

> *Your off-hand weapon while dual-wielding strikes with greater power.*
>
> **Prerequisites**: Dex 15, Two-Weapon Fighting.
>
> **Benefits**: Add your Strength bonus to damage rolls made with your off-hand weapon.
>
> **Normal**: You normally add only half of your Strength modifier to damage rolls made with a weapon wielded in your off-hand.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `double_slice` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Dreadful Carnage
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 158; Advanced Race Guide (PZO1131) p. 118
**Foundry id:** `8w8oazSjfoqLMCR1`

> *Slaying an enemy demoralizes your other nearby foes.*
>
> **Prerequisites:** Str 15, Power Attack, Furious Focus, base attack bonus +11.
>
> **Benefit:** Whenever you reduce an enemy to 0 or fewer hit points, you can make an Intimidate check to demoralize all enemies within 30 feet as a free action. Enemies that cannot see both you and the enemy you reduced to 0 or fewer hit points are unaffected.
>
> ##### Combat Trick
>
> When you reduce an enemy to 0 or fewer hit points, you can spend up to 6 stamina points to increase the radius of this feat’s effect by 5 feet for each stamina point you spent (to a maximum of 60 feet).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `dreadful_carnage` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Eldritch Claws
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Str 15, natural weapons, base attack bonus +6
**Source:** Advanced Race Guide (PZO1131) p. 119; Advanced Player's Guide (PZO1115) p. 158
**Foundry id:** `eZ1aqBIrR5L8sVu8`

> *Who needs magic weapons? Eldritch tricks are no match for your bestial ferocity.*
>
> **Prerequisites**: Str 15, natural weapons, base attack bonus +6.
>
> **Benefits**: Your natural weapons are considered both magic and silver for purpose of overcoming damage reduction.
>
> ##### Combat Trick
>
> As long as you have 1 stamina point in your stamina pool, your claws are also considered to be cold iron weapons for the purpose of overcoming damage reduction.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `eldritch_claws` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Elemental Channel
*(feat)*

**Tags:** Channeling
**Prerequisites:** Channel energy class feature
**Source:** Core Rulebook (PZO1110) p. 115, 122
**Foundry id:** `f5rgOsdDlseGr4o5`

> *Choose one elemental subtype, such as air, earth, fire, or water. You can channel your divine energy to harm or heal outsiders that possess your chosen elemental subtype.*
>
> **Prerequisites**: Channel energy class feature.
>
> **Benefits**: Instead of its normal effect, you can choose to have your ability to channel energy heal or harm outsiders of your chosen elemental subtype. You must make this choice each time you channel energy. If you choose to heal or harm creatures of your elemental subtype, your channel energy has no affect on other creatures. The amount of damage healed or dealt and the DC to halve the damage is otherwise unchanged.
>
> **Special**: You can gain this feat multiple times. Its effects do not stack. Each time you take this feat, it applies to a new elemental subtype.
>
> **Usage**: link this feat to Channel Energy charges. Change damage type to negative if you channel negative energy. Copy this feature and change Action Type to Healing if you plan to heal.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `elemental_channel` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Empower Spell-Like Ability
*(feat)*

**Tags:** Monster
**Prerequisites:** Spell-like ability at caster level 6th or higher
**Source:** PZO1112 (PZO1112) p. 314
**Foundry id:** `NJoSHKbpJj9aD84E`

> *One of this creature's spell-like abilities is particularly potent and powerful.*
>
> **Prerequisites**: Spell-like ability at caster level 6th or higher.
>
> **Benefits**: Choose one of the creature's spell-like abilities, subject to the restrictions below. The creature can use that ability as an empowered spell-like ability three times per day (or less, if the ability is normally usable only once or twice per day).
>
> When a creature uses an empowered spell-like ability, all variable, numeric effects of the spell-like ability are increased by half (+50%). Saving throws and opposed rolls are not affected. Spell-like abilities without random variables are not affected.
>
> The creature can only select a spell-like ability duplicating a spell with a level less than or equal to 1/2 its caster level (round down) - 2. For a summary, see the table in the description of the Quicken Spell-Like Ability.**
>
>
> Spell Level**
>
>
> **Caster Level to Empower**
>
>
> 0
>
>
> 4th
>
>
> 1st
>
>
> 6th
>
>
> 2nd
>
>
> 8th
>
>
> 3rd
>
>
> 10th
>
>
> 4th
>
>
> 12th
>
>
> 5th
>
>
> 14th
>
>
> 6th
>
>
> 16th
>
>
> 7th
>
>
> 18th
>
>
> 8th
>
>
> 20th
>
>
> 9th
>
>
> -
>
>
> **Special**: This feat can be taken multiple times. Each time it is taken, the creature can apply it to a different spell-like ability.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `empower_spell_like_ability` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Empower Spell
*(feat)*

**Tags:** Metamagic, Magic
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 117, 122
**Foundry id:** `77gXSucrxfrE9yWk`

> *You can increase the power of your spells, causing them to deal more damage.*
>
> **Benefits**: All variable, numeric effects of an empowered spell are increased by half, including bonuses to those dice rolls.
>
> Saving throws and opposed rolls are not affected, nor are spells without random variables. An empowered spell uses up a spell slot two levels higher than the spell’s actual level.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `NOT_IMPLEMENTED` — metamagic: +50% damage/heal at +2 spell level
**Manual verdict:** `[ ]`
**Notes:**

---

### Endurance
*(feat)*

**Tags:** General
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 115, 122
**Foundry id:** `ehqx8txNRGMaNOPt`

> *Harsh conditions or long exertions do not easily tire you.*
>
> **Benefits**: You gain a +4 bonus on the following checks and saves: Swim checks made to resist nonlethal damage from exhaustion; Constitution checks made to continue running; Constitution checks made to avoid nonlethal damage from a forced march; Constitution checks made to hold your breath; Constitution checks made to avoid nonlethal damage from starvation or thirst; Fortitude saves made to avoid nonlethal damage from hot or cold environments; and Fortitude saves made to resist damage from suffocation.
>
> You may sleep in light or medium armor without becoming fatigued.
>
> **Normal**: A character without this feat who sleeps in medium or heavier armor is fatigued the next day.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `NOT_IMPLEMENTED` — +4 to various endurance-related checks
**Manual verdict:** `[ ]`
**Notes:**

---

### Enforcer
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Intimidate 1 rank
**Source:** Advanced Race Guide (PZO1131) p. 119; PZO1111 (PZO1111) p. 125; Advanced Player's Guide (PZO1115) p. 159
**Foundry id:** `R351L670WEKmPCFW`

> *You are skilled at causing fear in those you brutalize.*
>
> **Prerequisites**: Intimidate 1 rank.
>
> **Benefits**: Whenever you deal nonlethal damage with a melee weapon, you can make an Intimidate check to demoralize your target as a free action. If you are successful, the target is shaken for a number of rounds equal to the damage dealt. If your attack was a critical hit, your target is frightened for 1 round with a successful Intimidate check, as well as being shaken for a number of rounds equal to the damage dealt.
>
> ##### Combat Trick
>
> When you score a critical hit with a weapon dealing nonlethal damage, you can spend 5 stamina points to frighten the target for 1d4 rounds instead of 1 round.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `enforcer` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Enlarge Spell
*(feat)*

**Tags:** Metamagic
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 117, 123-124
**Foundry id:** `9mcYid7xJY9NiySx`

> *You can increase the range of your spells.*
>
> **Benefits**: You can alter a spell with a range of close, medium, or long to increase its range by 100%. An enlarged spell with a range of close now has a range of 50 ft. + 5 ft./level, while medium-range spells have a range of 200 ft. + 20 ft./level and long-range spells have a range of 800 ft. + 80 ft./level. An enlarged spell uses up a spell slot one level higher than the spell's actual level.
>
> Spells whose ranges are not defined by distance, as well as spells whose ranges are not close, medium, or long, do not benefit from this feat.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `enlarge_spell` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Eschew Materials
*(feat)*

**Tags:** General, Magic
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 115, 123
**Foundry id:** `ElqchQT5WB625HPg`

> *You can cast many spells without needing to utilize minor material components.*
>
> **Benefits**: You can cast any spell with a material component costing 1 gp or less without needing that component. The casting of the spell still provokes attacks of opportunity as normal. If the spell requires a material component that costs more than 1 gp, you must have the material component on hand to cast the spell, as normal.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `NOT_IMPLEMENTED` — skip cheap material components
**Manual verdict:** `[ ]`
**Notes:**

---

### Exhausting Critical
*(feat)*

**Tags:** Combat, Critical, Combat Trick
**Prerequisites:** Critical Focus, Tiring Critical, base attack bonus +15
**Source:** Core Rulebook (PZO1110) p. 114, 123
**Foundry id:** `dyTsGfZBwrXNfdH9`

> *Your critical hits cause opponents to become exhausted.*
>
> **Prerequisites**: Critical Focus, Tiring Critical, base attack bonus +15.
>
> **Benefits**: When you score a critical hit on a foe, your target immediately becomes exhausted. This feat has no effect on exhausted creatures.
>
> **Special**: You can only apply the effects of one critical feat to a given critical hit unless you possess the Critical Mastery feat.
>
> ##### Combat Trick
>
> When you threaten a critical hit against an exhausted target and choose to use Exhausting Critical, you can spend up to 5 stamina points. If you do, you gain a +2 bonus on the confirmation roll for each stamina point you spent.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `exhausting_critical` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Exotic Weapon Proficiency
*(feat)*

**Tags:** Combat, Proficiency, Weapon
**Prerequisites:** Base attack bonus +1
**Source:** Core Rulebook (PZO1110) p. 115, 123
**Foundry id:** `BJBC4lbo7xGWPsKJ`

> *Choose one type of exotic weapon, such as the spiked chain or whip. You understand how to use that type of exotic weapon in combat, and can utilize any special tricks or qualities that exotic weapon might allow.*
>
> **Prerequisites**: Base attack bonus +1.
>
> **Benefits**: You make attack rolls with the weapon normally.
>
> **Normal**: A character who uses a weapon with which he is not proficient takes a -4 penalty on attack rolls.
>
> **Special**: You can gain Exotic Weapon Proficiency multiple times. Each time you take the feat, it applies to a new type of exotic weapon.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `exotic_weapon_proficiency` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extend Spell
*(feat)*

**Tags:** Metamagic, Magic
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 117, 124
**Foundry id:** `btXWioB3SKJv8YEG`

> *You can make your spells last twice as long.*
>
> **Benefits**: An extended spell lasts twice as long as normal. A spell with a duration of concentration, instantaneous, or permanent is not affected by this feat. An extended spell uses up a spell slot one level higher than the spell's actual level.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extend_spell` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Amplification
*(feat)*

**Tags:** General
**Prerequisites:** Phrenic amplification class feature
**Source:** Bestiary 4 (PZO1132) p. 133
**Foundry id:** `MWbOlWeXOxxsBacw`

> *You are a master at manipulating your mental energies to produce amplified effects.*
>
> **Prerequisites**: Phrenic amplification class feature.
>
> **Benefit**: You gain one additional phrenic amplification. This can’t be a major amplification.
>
> **Special**: You can take this feat multiple times. Each time you do, you gain another phrenic amplification.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_amplification` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Arcana
*(feat)*

**Tags:** General
**Prerequisites:** Magus arcana class feature
**Source:** Ultimate Magic (PZO1117) p. 149
**Foundry id:** `aakJ9PeaLxE6qluW`

> *You have unlocked the secret of a new magus arcana.*
>
> **Prerequisites**: Magus arcana class feature.
>
> **Benefit**: You gain one additional magus arcana. You must meet all the prerequisites for this magus arcana.
>
> **Special**: You can gain this feat multiple times. Its effects stack, granting a new arcana each time you gain this feat.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_arcana` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Arcane Pool
*(feat)*

**Tags:** General
**Prerequisites:** Arcane pool class feature
**Source:** Ultimate Magic (PZO1117) p. 150
**Foundry id:** `3lfNiysSNv1ahV4F`

> *You have learned how to draw more power from your arcane pool.*
>
> **Prerequisites**: Arcane pool class feature.
>
> **Benefit**: Your arcane pool increases by 2.
>
> **Special**: You can gain this feat multiple times. Its effects stack, granting you an increase to your arcane pool each time you take this feat.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_arcane_pool` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Arcanist Exploit
*(feat)*

**Tags:** General
**Prerequisites:** Arcanist exploit class feature
**Source:** Advanced Class Guide (PZO1129) p. 146
**Foundry id:** `oY7COqEz5J61AX7C`

> *Your repertoire of arcanist exploits expands.*
>
> **Prerequisites**: Arcanist exploit class feature.
>
> **Benefit**: You gain one additional arcanist exploit. You must meet the prerequisites for this arcanist exploit.
>
> **Special**: You can take this feat multiple times. Each time you do, you gain another arcanist exploit.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_arcanist_exploit` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Bane
*(feat)*

**Tags:** General
**Prerequisites:** Bane class feature
**Source:** Bestiary (PZO1118) p. 100
**Foundry id:** `DaedlCctLlmtUbrT`

> *You can use your bane ability more often than normal.*
>
> **Prerequisites**: Bane class feature.
>
> **Benefit**: You can use your bane ability for 3 additional rounds per day.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_bane` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Bombs
*(feat)*

**Tags:** General
**Prerequisites:** Bomb class feature
**Source:** Advanced Player's Guide (PZO1115) p. 159
**Foundry id:** `ViwAwl9iKWgh77pP`

> *You can throw more bombs per day.*
>
> **Prerequisites**: Bomb class feature.
>
> **Benefit**: You can throw two additional bombs per day.
>
> **Special**: You can gain Extra Bombs multiple times. Its effects stack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_bombs` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Cantrips or Orisons
*(feat)*

**Tags:** —
**Prerequisites:** Ability to cast cantrips or orisons
**Source:** Ultimate Magic (PZO1117) p. 150
**Foundry id:** `QlfQpoqFeSTC9AAT`

> *You are a master of minor spells.*
>
> **Prerequisites**: Ability to cast cantrips or orisons.
>
> **Benefit**: Add two cantrips to your cantrips known or two orisons to your orisons known.
>
> **Special**: You can take this feat multiple times. Each time you do, add two cantrips or orisons to your spells known.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_cantrips_or_orisons` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Channel
*(feat)*

**Tags:** Channeling
**Prerequisites:** Channel energy class feature
**Source:** Core Rulebook (PZO1110) p. 115, 123-124
**Foundry id:** `pgRX4VpFemwv9R0E`

> *You can channel divine energy more often.*
>
> **Prerequisites**: Channel energy class feature.
>
> **Benefits**: You can channel energy two additional times per day.
>
> **Special**: If a paladin with the ability to channel positive energy takes this feat, she can use lay on hands four additional times per day, but only to channel positive energy. If a warpriest with the ability to channel energy takes this feat, he gains four additional uses of fervor per day, but can use them only to channel energy.
>
> **Usage**: add additional charges to respective feature Maximum Usage Formula manually.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_channel` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Discovery
*(feat)*

**Tags:** —
**Prerequisites:** Discovery class feature
**Source:** Advanced Player's Guide (PZO1115) p. 160
**Foundry id:** `WYuwfu2h0LWNkU4Y`

> *You have made a new alchemical discovery.*
>
> **Prerequisites**: Discovery class feature.
>
> **Benefit**: You gain one additional discovery. You must meet all of the prerequisites for this discovery.
>
> **Special**: You can gain Extra Discovery multiple times.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_discovery` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Evolution
*(feat)*

**Tags:** —
**Prerequisites:** Eidolon class feature
**Source:** Ultimate Magic (PZO1117) p. 150
**Foundry id:** `bPu6oC4wfuadvMOp`

> Your eidolon has more evolutions.
>
> **Prerequisites**: Eidolon class feature.
>
> **Benefit**: Your eidolon’s evolution pool increases by 1.
>
> **Special**: This evolution can be taken once at 1st level, and again at 5th, 10th, 15th and 20th.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_evolution` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Feature
*(feat)*

**Tags:** General, Skinwalker
**Prerequisites:** Con 13, skinwalker
**Source:** PZO9439 (PZO9439) p. 7
**Foundry id:** `3KKtUz4ayCMaHeXQ`

> You are an exceptional shapechanger.
>
> **Prerequisites**: Con 13, skinwalker.
>
> **Benefit**: When you change shape to your bestial form, you may choose one additional feature from those listed in your shapechange ability and gain that benefit while in bestial form.
>
> **Special**: You can gain this feat multiple times. Its effects stack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_feature` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Focus Power
*(feat)*

**Tags:** General
**Prerequisites:** Focus power class feature
**Source:** Bestiary 4 (PZO1132) p. 133
**Foundry id:** `TN4EcG5WwQQPzl51`

> *You gain an additional focus power from your implements.*
>
> **Prerequisites**: Focus power class feature.
>
> **Benefit**: You gain one additional focus power from among those available from your chosen implement schools. You must select a power for which you normally qualify.
>
> **Special**: You can choose this feat once for every implement school you know, up to a maximum of seven times at 18th level. Each time you do, you must choose a different focus power. If you have selected the same implement school more than once, you can select a focus power from that school once for each time you selected that school.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_focus_power` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Gnome Magic
*(feat)*

**Tags:** General
**Prerequisites:** Cha 13, Gnome
**Source:** PZO9411 (PZO9411) p. 26
**Foundry id:** `yQ06clVxFV6dOjc1`

> *The raw magic that flows through your gnome blood is stronger than normal.*
>
> **Prerequisites**: Cha 13, Gnome.
>
> **Benefit**: You gain an additional three uses per day of your gnome spell-like abilities (dancing lights, ghost sound, prestidigitation). You can use these in any combination; for example, you can use dancing lights four times in one day (taking all three additional uses for the same spell), or you can cast ghost sound twice, prestidigitation twice, speak with animals twice, and dancing lights once. If you have a feat, trait, or other ability that changes your racial 0-level spell-like abilities to other 0-level spells, this feat applies to them instead.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_gnome_magic` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Grit
*(feat)*

**Tags:** Grit
**Prerequisites:** Grit class feature or the Amateur Gunslinger feat
**Source:** Bestiary (PZO1118) p. 100
**Foundry id:** `dahncmkl8bFmFlmi`

> *You have more grit than the ordinary gunslinger.*
>
> **Prerequisites**: Grit class feature or the Amateur Gunslinger feat.
>
> **Benefit**: You gain 2 extra grit points at the start of each day, and your maximum grit increases by 2.
>
> **Normal**: If you are a gunslinger, you gain your Wisdom modifier in grit points at the start of each day, which is also your maximum grit. If you have the Amateur Gunslinger feat, you gain 1 grit point at the start of each day, and your maximum grit is equal to your Wisdom modifier.
>
> **Special**: If you possess levels in the gunslinger class, you can take this feat multiple times.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_grit` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Hex
*(feat)*

**Tags:** General
**Prerequisites:** Hex class feature
**Source:** Advanced Player's Guide (PZO1115) p. 160; Advanced Class Guide (PZO1129) p. 147
**Foundry id:** `Wyg5K1Y72Jf5Yehb`

> *You have learned the secrets of a new hex.*
>
> **Prerequisites**: Hex class feature.
>
> **Benefit**: You gain one additional hex. You must meet the prerequisites for this hex. If you are a shaman, it must be a hex granted by your spirit rather than one from a wandering spirit.
>
> **Special**: You can take this feat multiple times. Each time you do, you gain another hex.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_hex` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Inspiration
*(feat)*

**Tags:** General
**Prerequisites:** Amateur Investigator or inspiration class feature
**Source:** Advanced Class Guide (PZO1129) p. 147
**Foundry id:** `4VUSgCTR3kUUtKxp`

> *You are more able to draw upon inspiration than most.*
>
> **Prerequisites**: Amateur Investigator or inspiration class feature.
>
> **Benefit**: You gain three extra use per day of inspiration in your inspiration pool.
>
> **Special**: If you have levels in the investigator class, you can take this feat multiple times. Each time you do, you gain three extra uses of inspiration per day.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_inspiration` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Investigator Talent
*(feat)*

**Tags:** General
**Prerequisites:** Investigator talent class feature
**Source:** Advanced Class Guide (PZO1129) p. 147
**Foundry id:** `91lGWgfmuQFUQit5`

> *You learn a new way to use your training and inspiration.*
>
> **Prerequisites**: Investigator talent class feature.
>
> **Benefit**: You gain one additional investigator talent. You must meet the prerequisites for this investigator talent.
>
> **Special**: You can take this feat multiple times. Each time you do, you gain another investigator talent.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_investigator_talent` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Item Slot
*(feat)*

**Tags:** General
**Prerequisites:** Non-humanoid body shape
**Source:** PZO9429 (PZO9429) p. 18
**Foundry id:** `AuzOXSPSI7Q3iNK8`

> *You are able to wear magic items more easily than other creatures of your kind.*
>
> **Prerequisites**: Non-humanoid body shape.
>
> **Benefit**: Choose one magic item slot not normally available to creatures with your shape. You can now use magic items in that slot.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_item_slot` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Ki
*(feat)*

**Tags:** General
**Prerequisites:** Ki pool class feature
**Source:** Core Rulebook (PZO1110) p. 115, 124
**Foundry id:** `PGTjF7uoFx7wP1WO`

> *You can use your ki pool more times per day than most.*
>
> **Prerequisites**: Ki pool class feature.
>
> **Benefits**: Your ki pool increases by 2.
>
> **Special**: You can gain Extra Ki multiple times. Its effects stack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_ki` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Lay On Hands
*(feat)*

**Tags:** General
**Prerequisites:** Lay on hands class feature
**Source:** Core Rulebook (PZO1110) p. 115, 124
**Foundry id:** `RDgJ7awoKBhacWsu`

> *You can use your lay on hands ability more often.*
>
> **Prerequisites**: Lay on hands class feature.
>
> **Benefits**: You can use your lay on hands ability two additional times per day.
>
> **Special**: You can gain Extra Lay On Hands multiple times. Its effects stack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_lay_on_hands` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Martial Flexibility
*(feat)*

**Tags:** General
**Prerequisites:** Martial flexibility class feature
**Source:** Advanced Class Guide (PZO1129) p. 147
**Foundry id:** `rd6l1sioW9ecVcSm`

> *You are extremely versatile in a fight.*
>
> **Prerequisites**: Martial flexibility class feature.
>
> **Benefit**: You can use your martial flexibility ability three additional times per day.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_martial_flexibility` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Mental Focus
*(feat)*

**Tags:** General
**Prerequisites:** Mental focus class feature
**Source:** Bestiary 4 (PZO1132) p. 133
**Foundry id:** `AZoNxM18sC74qeo9`

> *You possess increased mental focus.*
>
> **Prerequisites**: Mental focus class feature.
>
> **Benefit**: You gain 2 additional points of mental focus.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_mental_focus` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Mercy
*(feat)*

**Tags:** General
**Prerequisites:** Lay on hands class feature, mercy class feature
**Source:** Core Rulebook (PZO1110) p. 115, 124
**Foundry id:** `GCAaufQOqpQagrSk`

> *Your lay on hands ability adds an additional mercy.*
>
> **Prerequisites**: Lay on hands class feature, mercy class feature.
>
> **Benefits**: Select one additional mercy for which you qualify. When you use lay on hands to heal damage to one target, it also receives the additional effects of this mercy.
>
> **Special**: You can gain this feat multiple times. Its effects do not stack. Each time you take this feat, select a new mercy.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_mercy` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Mesmerist Tricks
*(feat)*

**Tags:** General
**Prerequisites:** Mesmerist trick class feature
**Source:** Bestiary 4 (PZO1132) p. 133
**Foundry id:** `54QWaanZra9hi7LV`

> *You can use your mesmerist tricks more often.*
>
> **Prerequisites**: Mesmerist trick class feature.
>
> **Benefit**: You can implant two additional mesmerist tricks per day.
>
> **Special**: You can gain Extra Mesmerist Tricks multiple times. Its effects stack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_mesmerist_tricks` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Ninja Trick
*(feat)*

**Tags:** General
**Prerequisites:** Ninja trick class feature
**Source:** PZO9466 (PZO9466) p. 25
**Foundry id:** `SxJ3UUccsCHjI6WN`

> *You have honed your shadowy skills further than most.*
>
> **Prerequisites**: Ninja trick class feature.
>
> **Benefit**: You gain one additional ninja trick. You must meet all of the prerequisites for this ninja trick.
>
> **Special**: You can gain Extra Ninja Trick multiple times.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_ninja_trick` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Panache
*(feat)*

**Tags:** Panache
**Prerequisites:** Amateur Swashbuckler or panache class feature
**Source:** Advanced Class Guide (PZO1129) p. 147
**Foundry id:** `vxDz1Rt1XKfFvWBV`

> *You have more panache than the ordinary swashbuckler.*
>
> **Prerequisites**: Amateur Swashbuckler or panache class feature.
>
> **Benefit**: You gain two more panache points at the start of each day, and your maximum panache increases by two.
>
> **Special**: If you have levels in the swashbuckler class, you can take this feat multiple times. Its effects stack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_panache` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Performance
*(feat)*

**Tags:** General
**Prerequisites:** Bardic performance class feature
**Source:** Core Rulebook (PZO1110) p. 115, 124
**Foundry id:** `6yGoL82RidBHmXPb`

> *You can use your bardic performance ability more often than normal.*
>
> **Prerequisites**: Bardic performance class feature.
>
> **Benefits**: You can use bardic performance for 6 additional rounds per day.
>
> **Special**: You can gain Extra Performance multiple times. Its effects stack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_performance` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Rage Power
*(feat)*

**Tags:** General
**Prerequisites:** Rage power class feature
**Source:** Advanced Player's Guide (PZO1115) p. 160
**Foundry id:** `7P84frgqSmscfkUC`

> *You have unlocked a new ability to use while raging.*
>
> **Prerequisites**: Rage power class feature.
>
> **Benefit**: You gain one additional rage power. You must meet all of the prerequisites for this rage power.
>
> **Special**: You can gain Extra Rage Power multiple times.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_rage_power` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Rage
*(feat)*

**Tags:** General
**Prerequisites:** Rage class feature
**Source:** Core Rulebook (PZO1110) p. 115, 124
**Foundry id:** `oP4Srsuk0dF2Zf9F`

> *You can use your rage ability more than normal.*
>
> **Prerequisites**: Rage class feature.
>
> **Benefits**: You can rage for 6 additional rounds per day.
>
> **Special**: You can gain Extra Rage multiple times. Its effects stack.
>
> **Usage**: add additional charges to Rage feature Maximum Usage Formula manually.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_rage` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Reservoir
*(feat)*

**Tags:** General
**Prerequisites:** Arcane reservoir class feature
**Source:** Advanced Class Guide (PZO1129) p. 147
**Foundry id:** `XMQRJ6eGKu3KILKe`

> *Your reservoir of arcane energy is greater than others’.*
>
> **Prerequisites**: Arcane reservoir class feature.
>
> **Benefit**: You gain three more points in your arcane reservoir, and the maximum number of points in your arcane reservoir increases by that amount.
>
> **Special**: You can take this feat multiple times. Its effects stack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_reservoir` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Revelation
*(feat)*

**Tags:** General
**Prerequisites:** Revelation class feature
**Source:** Advanced Player's Guide (PZO1115) p. 160
**Foundry id:** `VHsCghfyT6J43b5G`

> *You have discovered a new aspect of your mystery.*
>
> **Prerequisites**: Revelation class feature.
>
> **Benefit**: You gain one additional revelation. You must meet all of the prerequisites for this revelation.
>
> **Special**: You can gain Extra Revelation multiple times.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_revelation` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Rogue Talent
*(feat)*

**Tags:** General
**Prerequisites:** Rogue talent class feature
**Source:** Advanced Player's Guide (PZO1115) p. 160
**Foundry id:** `jGYtflqD2m71KaEg`

> *Through constant practice, you have learned how to perform a special trick.*
>
> **Prerequisite**: Rogue talent class feature.
>
> **Benefit**: You gain one additional rogue talent. You must meet all of the prerequisites for this rogue talent.
>
> **Special**: You can gain Extra Rogue Talent multiple times.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_rogue_talent` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Slayer Talent
*(feat)*

**Tags:** General
**Prerequisites:** Slayer talent class feature
**Source:** Advanced Class Guide (PZO1129) p. 147
**Foundry id:** `xEiu70gtsZsq4eSo`

> *Through long practice, you have learned how to perform a special talent.*
>
> **Prerequisites**: Slayer talent class feature.
>
> **Benefit**: You gain one additional slayer talent. You must meet the prerequisites for this slayer talent.
>
> **Special**: You can take this feat multiple times. Each time you do, you gain another slayer talent.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_slayer_talent` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Extra Surge
*(feat)*

**Tags:** General, Android
**Prerequisites:** Con 13, nanite surge ability
**Source:** PZO9085 (PZO9085) p. 72; PZO9449 (PZO9449) p. 7
**Foundry id:** `gtvBVEKBRF2SzfeJ`

> *You can use your nanite surge ability more often than normal.*
>
> **Prerequisites**: Con 13, nanite surge ability.
>
> **Benefit**: You can use your nanite surge ability one additional time per day.
>
> **Special**: You can gain Extra Surge multiple times. Its effects stack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `extra_surge` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### False Opening
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Dex 13, Dodge, Close Quarters Thrower or Point-Blank Master, Weapon Focus with selected ranged weapon
**Source:** Advanced Race Guide (PZO1131) p. 119; Bestiary (PZO1118) p. 100
**Foundry id:** `Av67GzsPJ0qjipZ1`

> *When you make a ranged attack while threatened, you can fool your opponent into thinking he has an opening.*
>
> **Prerequisites**: Dex 13, Dodge, Close Quarters Thrower or Point-Blank Master, Weapon Focus with selected ranged weapon.
>
> **Benefits**: Choose a ranged weapon or a thrown weapon. When you make a ranged attack using that weapon, you can choose to provoke an attack of opportunity from one or more opponents who threaten you. You gain a +4 dodge bonus against such attacks. An opponent that makes such an attack and misses you loses his Dexterity bonus to AC against you until the end of your turn.
>
> ##### Combat Trick
>
> When you use this feat, you can spend 5 stamina points to make an attack of opportunity against an opponent who misses you with the provoked attack (after it loses its Dexterity bonus to AC against you).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `false_opening` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Far Shot
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Point-Blank Shot
**Source:** Core Rulebook (PZO1110) p. 116, 124
**Foundry id:** `HMCAM3Zyo77kG8Yg`

> *You are more accurate at longer ranges.*
>
> **Prerequisites**: Point-Blank Shot.
>
> **Benefits**: You only suffer a -1 penalty per full range increment between you and your target when using a ranged weapon.
>
> **Normal**: You suffer a -2 penalty per full range increment between you and your target.
>
> ##### Combat Trick
>
> When making a single ranged attack as a standard action, you can spend 5 stamina points to ignore all range penalties on that attack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `far_shot` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Felling Smash
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Int 13, Str 13, Combat Expertise, Improved Trip, Power Attack, base attack bonus +6
**Source:** Advanced Race Guide (PZO1131) p. 119; Bestiary (PZO1118) p. 101
**Foundry id:** `HvYZ9O5dhlfkFjDq`

> *You commit all your focus to a devastating blow, trying to crush your opponent to the ground.*
>
> **Prerequisites**: Int 13, Str 13, Combat Expertise, Improved Trip, Power Attack, base attack bonus +6.
>
> **Benefits**: If you use the attack action to make a single melee attack at your highest base attack bonus while using Power Attack and you hit an opponent, you can spend a swift action to attempt a trip combat maneuver against that opponent.
>
> ##### Combat Trick
>
> You can select this feat even if you don't meet the ability score prerequisite (Intelligence 13). You gain the benefit of this feat only as long as you have at least 1 stamina point in your stamina pool. You can spend 5 stamina points to make the trip attempt from this feat as a free action instead of a swift action.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `felling_smash` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fleet
*(feat)*

**Tags:** General, Movement
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 115, 124
**Foundry id:** `BkKYCzEGNTzZRiTz`

> *You are faster than most.*
>
> **Benefits**: While you are wearing light or no armor, your base speed increases by 5 feet. You lose the benefits of this feat if you carry a medium or heavy load.
>
> **Special**: You can take this feat multiple times. The effects stack.

**Mechanical encoding:** `changes`: 1
  - `if(and(lt(@armor.type, 2), lt(@attributes.encumbrance.level, 1)), 5)` → `landSpeed`  (base)

**In our coverage tracker:** absent (slug `fleet` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Fleshwarper
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Craft (alchemy) 5 ranks, Heal 5 ranks, evil alignment
**Source:** Ultimate Intrigue (PZO1135) p. 87
**Foundry id:** `9jvLagEYC2EAJ6lJ`

> *You can create creatures through an abominable alchemical process.*
>
> **Prerequisites**: Craft (alchemy) 5 ranks, Heal 5 ranks, evil alignment.
>
> **Benefit**: You can create fleshwarped creatures and fleshcraft grafts (see Fleshwarping for full details). A newly created fleshwarped creature has average hit points for its Hit Dice.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `fleshwarper` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Flyby Attack
*(feat)*

**Tags:** —
**Prerequisites:** Fly speed
**Source:** PZO1112 (PZO1112) p. 315
**Foundry id:** `PlCHtwe6e3f7pZYR`

> *This creature can make an attack before and after it moves while flying.* 
>
> **Prerequisites**: Fly speed.
>
> **Benefit**: When flying, the creature can take a move action and another standard action at any point during the move. The creature cannot take a second move action during a round when it makes a flyby attack.
>
> **Normal**: Without this feat, the creature takes a standard action either before or after its move.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `flyby_attack` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Focused Shot
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Int 13, Point-Blank Shot, Precise Shot
**Source:** Advanced Race Guide (PZO1131) p. 120; Advanced Player's Guide (PZO1115) p. 160
**Foundry id:** `dNmpRd9N0eyEJuUw`

> *Your anatomical insight adds deadliness to your shots.*
>
> **Prerequisites**: Int 13, Point-Blank Shot, Precise Shot.
>
> **Benefits**: As a standard action, you may make an attack with a bow or crossbow and add your Intelligence modifier on the damage roll. You must be within 30 feet of your target to deal this extra damage. Creatures immune to critical hits and sneak attacks are immune to this extra damage.
>
> **Special**: Starting at 2nd level, a ranger with the archery combat style may select Focused Shot as a combat style feat.
>
> ##### Combat Trick
>
> You can spend 2 stamina points to make a Focused Shot attack against a target anywhere within your weapon's first range increment.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `focused_shot` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Following Step
*(feat)*

**Tags:** Combat, Movement, Offensive, Combat Trick
**Prerequisites:** Dex 13, Step Up
**Source:** Advanced Player's Guide (PZO1115) p. 160; Advanced Race Guide (PZO1131) p. 120
**Foundry id:** `QvfsBWvx7Rfb9Wb7`

> *You can repeatedly close the distance when foes try to move away, without impeding your normal movement.*
>
> **Prerequisites**: Dex 13, Step Up.
>
> **Benefit**: When using the Step Up feat to follow an adjacent foe, you may move up to 10 feet. You may still take a 5-foot step during your next turn, and any movement you make using this feat does not subtract any distance from your movement during your next turn.
>
> **Normal**: You can only take a 5-foot step to follow an opponent using Step Up.
>
> ##### Combat Trick
>
> When you use this feat to move, you can spend 2 stamina points to increase your movement to 15 feet.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `following_step` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Forge Ring
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Caster level 7th
**Source:** Core Rulebook (PZO1110) p. 117, 124
**Foundry id:** `HVu9JzllWoLzKKqH`

> *You can create magic rings.*
>
> **Prerequisites**: Caster level 7th.
>
> **Benefits**: You can create magic rings. Crafting a ring takes 1 day for each 1,000 gp in its base price. To craft a ring, you must use up raw materials costing half of the base price. See the magic item creation rules in Magic Items for more information.
>
> You can also mend a broken ring if it is one that you could make. Doing so costs half the raw materials and half the time it would take to forge that ring in the first place.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `forge_ring` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Furious Focus
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Str 13, Power Attack, base attack bonus +1
**Source:** Advanced Player's Guide (PZO1115) p. 161
**Foundry id:** `UcEIgufLJlIfhHmu`

> *Even in the midst of fierce and furious blows, you can find focus in the carnage and your seemingly wild blows strike home.*
>
> **Prerequisites**: Str 13, Power Attack, base attack bonus +1.
>
> **Benefit**: When you are wielding a two-handed weapon or a one-handed weapon with two hands, and using the Power Attack feat, you do not suffer Power Attack’s penalty on melee attack rolls on the first attack you make each turn. You still suffer the penalty on any additional attacks, including attacks of opportunity.
>
> ##### Combat Trick
>
> When using the Power Attack feat and wielding a two-handed melee weapon or a onehanded melee weapon with two hands, you can spend 5 stamina points. If you do, each successful attack you make against a target reduces your Power Attack penalty against that target by 1 (to a minimum of 0) until the beginning of your next turn.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `furious_focus` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Gorgon's Fist
*(feat)*

**Tags:** Combat, Offensive, Unarmed
**Prerequisites:** Improved Unarmed Strike, Scorpion Style, base attack bonus +6
**Source:** Core Rulebook (PZO1110) p. 115, 124
**Foundry id:** `nhUawPP4jfED3CYV`

> *With one well-placed blow, you leave your target reeling.*
>
> **Prerequisites**: Improved Unarmed Strike, Scorpion Style, base attack bonus +6.
>
> **Benefits**: As a standard action, make a single unarmed melee attack against a foe whose speed is reduced (such as from Scorpion Style). If the attack hits, you deal damage normally and the target is staggered until the end of your next turn unless it makes a Fortitude saving throw (DC 10 + 1/2 your character level + your Wis modifier). This feat has no effect on targets that are staggered.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `gorgon_s_fist` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Gory Finish
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Dazzling Display, Weapon Focus
**Source:** Bestiary (PZO1118) p. 102; Advanced Race Guide (PZO1131) p. 120
**Foundry id:** `bSvHafwjbsYsXeoW`

> *By drawing upon wells of savagery, you can slay your foe in creative and horrifyingly gruesome manners, intimidating nearby foes.*
>
> **Prerequisites**: Dazzling Display, Weapon Focus.
>
> **Benefits**: When you use the attack action, you can use a weapon with which you have Weapon Focus to make a single attack at your highest base attack bonus. If you reduce your target to negative hit points, you can spend a swift action to make an Intimidate check to demoralize all foes within 30 feet who could see your attack.
>
> ##### Combat Trick
>
> You can spend 5 stamina points when confirming a critical on a Gory Finish attack to attempt an Intimidate check to demoralize all foes within 30 feet of you who can see your attack.

**Mechanical encoding:** has `actions`, has `scriptCalls`

**In our coverage tracker:** absent (slug `gory_finish` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Great Cleave
*(feat)*

**Tags:** Combat, Offensive
**Prerequisites:** Str 13, Cleave, Power Attack, base attack bonus +4
**Source:** Core Rulebook (PZO1110) p. 116, 124
**Foundry id:** `6HSMdwX1VS6nZ6Zf`

> *You can strike many adjacent foes with a single blow.*
>
> **Prerequisites**: Str 13, Cleave, Power Attack, base attack bonus +4.
>
> **Benefits**: As a standard action, you can make a single attack at your full base attack bonus against a foe within reach. If you hit, you deal damage normally and can make an additional attack (using your full base attack bonus) against a foe that is adjacent to the previous foe and also within reach. If you hit, you can continue to make attacks against foes adjacent to the previous foe, so long as they are within your reach. You cannot attack an individual foe more than once during this attack action. When you use this feat, you take a -2 penalty to your Armor Class until your next turn.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `great_cleave` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Great Fortitude
*(feat)*

**Tags:** General, Saving Throw, Defensive
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 115, 124
**Foundry id:** `fVRnBIHR4Jq6btvm`

> *You are resistant to poisons, diseases, and other maladies.*
>
> **Benefits**
>
> You get a +2 bonus on all Fortitude saving throws.

**Mechanical encoding:** `changes`: 1
  - `2` → `fort`  (untyped)

**In our coverage tracker:** `IMPLEMENTED` — +2 fort save
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Blind-Fight
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Perception 15 ranks, Improved Blind-Fight
**Source:** Advanced Race Guide (PZO1131) p. 120; Advanced Player's Guide (PZO1115) p. 161
**Foundry id:** `IOPS4W1mVH76IgxX`

> *Your enemies cannot hide from you.*
>
> **Prerequisites**: Perception 15 ranks, Improved Blind-Fight.
>
> **Benefits**: Your melee attacks ignore the miss chance for less than total concealment, and you treat opponents with total concealment as if they had normal concealment (20% miss chance instead of 50%). You may still reroll a miss chance percentile roll as normal.
>
> If you successfully pinpoint an invisible or hidden attacker, that attacker gets no advantages related to hitting you with ranged attacks, regardless of the range. That is, you don't lose your Dexterity bonus to Armor Class, and the attacker doesn't get the usual +2 bonus for being invisible.
>
> **Special**: The Greater Blind-Fight feat is of no use against a character who is the subject of a blink spell.
>
> ##### Combat Trick
>
> When you attack a creature subject to the blink spell, you can spend 5 stamina points. If you do, your Greater Blind-Fight feat works against that creature until the beginning of your next turn, either treating the blink miss chance as 20% and allowing a reroll or ignoring the blink miss chance if you have a way to see or strike ethereal creatures.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `greater_blind_fight` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Bull Rush
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** Improved Bull Rush, Power Attack, base attack bonus +6, Str 13
**Source:** Core Rulebook (PZO1110) p. 125; Advanced Race Guide (PZO1131) p. 120
**Foundry id:** `XGvS0hHv58XAeQij`

> *Your bull rush attacks throw enemies off balance.*
>
> **Prerequisites**: Improved Bull Rush, Power Attack, base attack bonus +6, Str 13.
>
> **Benefits**: You receive a +2 bonus on checks made to bull rush a foe. This bonus stacks with the bonus granted by Improved Bull Rush. Whenever you bull rush an opponent, his movement provokes attacks of opportunity from all of your allies (but not you).
>
> **Normal**: Creatures moved by bull rush do not provoke attacks of opportunity.
>
> ##### Combat Trick
>
> When you bull rush an opponent, you can spend 5 stamina points to have the opponent’s movement from the bull rush provoke an attack of opportunity from you as well.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.bullRush`  (untyped)

**In our coverage tracker:** absent (slug `greater_bull_rush` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Dirty Trick
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 161; Advanced Race Guide (PZO1131) p. 120
**Foundry id:** `mY29nl8eCF5GjchB`

> *When you pull a dirty trick, your foe is truly hindered.*
>
> **Prerequisites:** Int 13, Combat Expertise, Improved Dirty Trick, base attack bonus +6.
>
> **Benefit:** You receive a +2 bonus on checks made to attempt a dirty trick. This bonus stacks with the bonus granted by Improved Dirty Trick. Whenever you successfully perform a dirty trick, the penalty lasts for 1d4 rounds, plus 1 round for every 5 by which your attack exceeds the target’s CMD. In addition, removing the condition requires the target to spend a standard action.
>
> **Normal:** The condition imposed by a dirty trick lasts for 1 round plus 1 round for every 5 by which your attack exceeds the target’s CMD. Removing the condition requires the target to spend a move action.
>
> ##### Combat Trick
>
> You can select this feat even if you don’t meet the ability score prerequisite (Intelligence 13). You gain the benefits of this feat only as long as you have at least 1 stamina point in your stamina pool. When you successfully complete a dirty trick combat maneuver, you can spend 5 stamina points to make the condition you inflicted with that maneuver require a full-round action to remove (instead of a standard action).

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.dirtyTrick`  (untyped)

**In our coverage tracker:** absent (slug `greater_dirty_trick` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Disarm
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** Combat Expertise, Improved Disarm, base attack bonus +6, Int 13
**Source:** Core Rulebook (PZO1110) p. 125; Advanced Race Guide (PZO1131) p. 120
**Foundry id:** `1AY9Xjbg109TsnVl`

> *You can knock weapons far from an enemy's grasp.*
>
> **Prerequisites**: Combat Expertise, Improved Disarm, base attack bonus +6, Int 13.
>
> **Benefits**: You receive a +2 bonus on checks made to disarm a foe. This bonus stacks with the bonus granted by Improved Disarm. Whenever you successfully disarm an opponent, the weapon lands 15 feet away from its previous wielder, in a random direction.
>
> **Normal**: Disarmed weapons and gear land at the feet of the disarmed creature.
>
> ##### Combat Trick
>
> You can select this feat even if you don’t meet the ability score prerequisite (Intelligence 13). You gain the benefits of this feat only as long as you have at least 1 stamina point in your stamina pool. When you successfully disarm a foe, you can spend 5 stamina points to select where the weapon lands by choosing a square within 15 feet of the disarmed foe. If you choose a square in your space and have at least one hand free, you can grab the weapon as part of the disarm attempt.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.disarm`  (untyped)

**In our coverage tracker:** absent (slug `greater_disarm` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Drag
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 161; Advanced Race Guide (PZO1131) p. 121
**Foundry id:** `0X4q0Ypx3L05Sqzg`

> *Foes that you drag are thrown out of balance.*
>
> **Prerequisites:** Str 13, Improved Drag, Power Attack, base attack bonus +6.
>
> **Benefit:** You receive a +2 bonus on checks made to drag a foe. This bonus stacks with the bonus granted by Improved Drag. Whenever you drag a foe, his movement provokes attacks of opportunity from all of your allies (but not you).
>
> **Normal:** Creatures moved by drag do not provoke attacks of opportunity.
>
> ##### Combat Trick
>
> When you succeed at a drag combat maneuver check, you can spend 5 stamina points to gain up to 10 feet of movement for your drag. You can use this movement in place of your normal movement, but only to drag an opponent.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.drag`  (untyped)

**In our coverage tracker:** absent (slug `greater_drag` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Feint
*(feat)*

**Tags:** Combat, Combat Maneuver, Offensive
**Prerequisites:** Combat Expertise, Improved Feint, base attack bonus +6, Int 13
**Source:** Core Rulebook (PZO1110) p. 114, 125
**Foundry id:** `0VM8AdwP25nHWnV8`

> *You are skilled at making foes overreact to your attacks.*
>
> **Prerequisites**: Combat Expertise, Improved Feint, base attack bonus +6, Int 13.
>
> **Benefits**: Whenever you use feint to cause an opponent to lose his Dexterity bonus, he loses that bonus until the beginning of your next turn, in addition to losing his Dexterity bonus against your next attack.
>
> **Normal**: A creature you feint loses its Dexterity bonus against your next attack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `greater_feint` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Grapple
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** Improved Grapple, Improved Unarmed Strike, base attack bonus +6, Dex 13
**Source:** Core Rulebook (PZO1110) p. 125; Advanced Race Guide (PZO1131) p. 121
**Foundry id:** `hc7CRKHvhmKRzNKb`

> *Maintaining a grapple is second nature to you.*
>
> **Prerequisites**: Improved Grapple, Improved Unarmed Strike, base attack bonus +6, Dex 13.
>
> **Benefits**: You receive a +2 bonus on checks made to grapple a foe. This bonus stacks with the bonus granted by Improved Grapple. Once you have grappled a creature, maintaining the grapple is a move action. This feat allows you to make two grapple checks each round (to move, harm, or pin your opponent), but you are not required to make two checks. You only need to succeed at one of these checks to maintain the grapple.
>
> **Normal**: Maintaining a grapple is a standard action.
>
> ##### Combat Trick
>
> After you take a move action to successfully maintain a grapple, you can spend 5 stamina points before the end of your turn to maintain that grapple as a swift action. This allows you to make up to three grapple checks to maintain a grapple during a round, but you still can’t maintain a grapple until the round after you initiate it.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.grapple`  (untyped)

**In our coverage tracker:** absent (slug `greater_grapple` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Overrun
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** Improved Overrun, Power Attack, base attack bonus +6, Str 13
**Source:** Core Rulebook (PZO1110) p. 125; Advanced Race Guide (PZO1131) p. 121
**Foundry id:** `tkWfEP1fD7CZt8Kw`

> *Enemies must dive to avoid your dangerous move.*
>
> **Prerequisites**: Improved Overrun, Power Attack, base attack bonus +6, Str 13.
>
> **Benefits**: You receive a +2 bonus on checks made to overrun a foe. This bonus stacks with the bonus granted by Improved Overrun. Whenever you overrun opponents, they provoke attacks of opportunity if they are knocked prone by your overrun.
>
> **Normal**: Creatures knocked prone by your overrun do not provoke an attack of opportunity.
>
> ##### Combat Trick
>
> If you succeed at a combat maneuver check to overrun an opponent, but do not exceed your opponent’s CMD by 5 or more, you can spend 2 stamina points to knock the target prone anyway.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.overrun`  (untyped)

**In our coverage tracker:** absent (slug `greater_overrun` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Penetrating Strike
*(feat)*

**Tags:** Combat, Weapon, Offensive
**Prerequisites:** Penetrating Strike, Weapon Focus, 16th-level fighter
**Source:** Core Rulebook (PZO1110) p. 117, 125
**Foundry id:** `FSDatwC1s6GoV1Sf`

> *Your attacks penetrate the defenses of most foes.*
>
> **Prerequisites**: Penetrating Strike, Weapon Focus, 16th-level fighter.
>
> **Benefits**: Your attacks with weapons selected with Weapon Focus ignore up to 10 points of damage reduction. This amount is reduced to 5 points for damage reduction without a type (such as DR 10/ — ).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `greater_penetrating_strike` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Reposition
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 161; Advanced Race Guide (PZO1131) p. 121
**Foundry id:** `HbfpROYGuhT2OLIQ`

> *When you reposition foes, they are left vulnerable to the attacks of your allies.*
>
> **Prerequisites:** Int 13, Combat Expertise, Improved Reposition, base attack bonus +6.
>
> **Benefit:** You receive a +2 bonus on checks made to reposition a foe. This bonus stacks with the bonus granted by Improved Reposition. Whenever you reposition a foe, his movement provokes attacks of opportunity from all of your allies (but not you).
>
> **Normal:** Creatures moved by reposition do not provoke attacks of opportunity.
>
> ##### Combat Trick
>
> You can select this feat even if you don’t meet the ability score prerequisite (Intelligence 13). You gain the benefits of this feat only as long as you have at least 1 stamina point in your stamina pool. When attempting to reposition a foe, you can spend 5 stamina points to increase your melee reach by 5 feet for the purpose of determining where you can move the foe.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.reposition`  (untyped)

**In our coverage tracker:** absent (slug `greater_reposition` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Shield Focus
*(feat)*

**Tags:** Combat, Combat Trick, Defensive
**Prerequisites:** Shield Focus, Shield Proficiency, base attack bonus +1, 8th-level fighter
**Source:** Core Rulebook (PZO1110) p. 116, 125
**Foundry id:** `XRPuApgE1Ltz4YHN`

> *You are skilled at deflecting blows with your shield.*
>
> **Prerequisites**: Shield Focus, Shield Proficiency, base attack bonus +1, 8th-level fighter.
>
> **Benefits**: Increase the AC bonus granted by any shield you are using by 1. This bonus stacks with the bonus granted by Shield Focus.
>
> ##### Combat Trick
>
> When an attack is made against you while you are using a shield, you can spend up to 4 stamina points. For that attack, your shield bonus increases by an amount equal to the number of stamina points you spent. This increase does not stack with any gained from the Shield Focus combat trick.

**Mechanical encoding:** `changes`: 1
  - `if(@shield.type, 1)` → `sac`  (untyped)

**In our coverage tracker:** absent (slug `greater_shield_focus` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Spell Focus
*(feat)*

**Tags:** General, Magic
**Prerequisites:** Spell Focus
**Source:** Core Rulebook (PZO1110) p. 116, 125
**Foundry id:** `LSykiaxYWzva2boF`

> *Choose a school of magic to which you have already applied the Spell Focus feat. Any spells you cast of this school are very hard to resist.*
>
> **Prerequisites**: Spell Focus.
>
> **Benefits**: Add +1 to the Difficulty Class for all saving throws against spells from the school of magic you select. This bonus stacks with the bonus from Spell Focus.
>
> **Special**: You can gain this feat multiple times. Its effects do not stack. Each time you take the feat, it applies to a new school to which you already have applied the Spell Focus feat.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `greater_spell_focus` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Spell Penetration
*(feat)*

**Tags:** General, Magic
**Prerequisites:** Spell Penetration
**Source:** Core Rulebook (PZO1110) p. 114, 125
**Foundry id:** `3HjwKckDBDDPcY2c`

> *Your spells break through spell resistance much more easily than most.*
>
> **Prerequisites**: Spell Penetration.
>
> **Benefits**: You get a +2 bonus on caster level checks (1d20 + caster level) made to overcome a creature's spell resistance. This bonus stacks with the one from Spell Penetration.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `greater_spell_penetration` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Spring Attack
*(feat)*

**Tags:** Combat, Offensive, Movement
**Prerequisites:** Dex 17, Acrobatic Steps, Dodge, Improved Spring Attack, Mobility, Nimble Moves, Spring Attack, base attack bonus +16
**Source:** Occult Adventures (PZO1140) p. 114
**Foundry id:** `6wPjZJNZpTfGJjTR`

> *You are a scything wind cutting through the battlefield as you topple your foes.*
>
> **Prerequisites**: Dex 17, Acrobatic Steps, Dodge, Improved Spring Attack, Mobility, Nimble Moves, Spring Attack, base attack bonus +16.
>
> **Benefit**: When you use Spring Attack, you can select three targets to attack during your movement instead of one. The second attack made this way is made at your full base attack bonus – 5, and the third attack made this way is made at your full base attack bonus – 10. All restrictions of Spring Attack apply to each target, and your movement does not provoke attacks of opportunity from any of your targets. You can’t target the same creature more than once.
>
> **Special**: A monk of at least 18th level can select this feat as a monk bonus feat, but only if he has Improved Spring attack and Spring Attack.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `greater_spring_attack` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Steal
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** Int 13, Combat Expertise, Improved Steal, base attack bonus +6
**Source:** Advanced Player's Guide (PZO1115) p. 162; Advanced Race Guide (PZO1131) p. 121
**Foundry id:** `XxZgIRc2UMLXHtZh`

> *You have a knack for snatching items from your opponents in combat.*
>
> **Prerequisites**: Int 13, Combat Expertise, Improved Steal, base attack bonus +6.
>
> **Benefits**: You receive a +2 bonus on checks made to steal an item from a foe. This bonus stacks with the bonus granted by Improved Steal. If you successfully steal an item from a foe during combat, it does not notice the theft until after combat is over or if it attempts to use the missing item.
>
> **Normal**: Creatures automatically notice items taken from them through the steal combat maneuver.
>
> ##### Combat Trick
>
> You can select this feat even if you don’t meet the ability score prerequisite (Intelligence 13). You gain the benefits of this feat only as long as you have at least 1 stamina point in your stamina pool. When attempting a stealAPG combat maneuver with a whip, you can spend 2 stamina points to negate the –4 penalty on the check.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.steal`  (untyped)

**In our coverage tracker:** absent (slug `greater_steal` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Sunder
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** Improved Sunder, Power Attack, base attack bonus +6, Str 13
**Source:** Core Rulebook (PZO1110) p. 125-126; Advanced Race Guide (PZO1131) p. 121
**Foundry id:** `wJNggbGTZBx7BW9W`

> *Your devastating strikes cleave through weapons and armor and into their wielders, damaging both item and wielder alike in a single terrific strike.*
>
> **Prerequisites**: Improved Sunder, Power Attack, base attack bonus +6, Str 13.
>
> **Benefits**: You receive a +2 bonus on checks made to sunder an item. This bonus stacks with the bonus granted by Improved Sunder. Whenever you sunder to destroy a weapon, shield, or suit of armor, any excess damage is applied to the item's wielder. No damage is transferred if you decide to leave the item with 1 hit point.
>
> ##### Combat Trick
>
> When you succeed at a sunder combat maneuver check, you can spend a number of stamina points up to your Strength bonus to deal an amount of extra damage to the target equal to double the number of stamina points you spent. The damage type is the same as that of the weapon you used to attempt the maneuver.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.sunder`  (untyped)

**In our coverage tracker:** absent (slug `greater_sunder` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Trip
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** Combat Expertise, Improved Trip, base attack bonus +6, Int 13
**Source:** Core Rulebook (PZO1110) p. 126; Advanced Race Guide (PZO1131) p. 122
**Foundry id:** `lNyMFFQaOxxTOW7M`

> *You can make free attacks on foes that you knock down.*
>
> **Prerequisites**: Combat Expertise, Improved Trip, base attack bonus +6, Int 13.
>
> **Benefits**: You receive a +2 bonus on checks made to trip a foe. This bonus stacks with the bonus granted by Improved Trip. Whenever you successfully trip an opponent, that opponent provokes attacks of opportunity.
>
> **Normal**: Creatures do not provoke attacks of opportunity from being tripped.
>
> ##### Combat Trick
>
> You can select this feat even if you don’t meet the ability score prerequisite (Intelligence 13). You gain the benefits of this feat only as long as you have at least 1 stamina point in your stamina pool. You can spend 2 stamina points after you successfully trip an opponent to deal 1d6 points of falling damage to the target.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.trip`  (untyped)

**In our coverage tracker:** absent (slug `greater_trip` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Two-Weapon Fighting
*(feat)*

**Tags:** Combat, Two Weapons, Weapon, Offensive
**Prerequisites:** Dex 19, Improved Two-Weapon Fighting, Two-Weapon Fighting, base attack bonus +11
**Source:** Core Rulebook (PZO1110) p. 116, 126
**Foundry id:** `ieltigobtFrlTXIt`

> *You are incredibly skilled at fighting with two weapons at the same time.*
>
> **Prerequisites**: Dex 19, Improved Two-Weapon Fighting, Two-Weapon Fighting, base attack bonus +11.
>
> **Benefits**: You get a third attack with your off-hand weapon, albeit at a -10 penalty.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `greater_two_weapon_fighting` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Vital Strike
*(feat)*

**Tags:** Combat, Offensive
**Prerequisites:** Improved Vital Strike, Vital Strike, base attack bonus +16
**Source:** Core Rulebook (PZO1110) p. 117, 126
**Foundry id:** `zKNk7a4XxXsygJ67`

> *You can make a single attack that deals incredible damage.*
>
> **Prerequisites**: Improved Vital Strike, Vital Strike, base attack bonus +16.
>
> **Benefits**: When you use the attack action, you can make one attack at your highest base attack bonus that deals additional damage. Roll the weapon's damage dice for the attack four times and add the results together before adding bonuses from Strength, weapon abilities (such as *flaming*), precision based damage, and other damage bonuses. These extra weapon damage dice are not multiplied on a critical hit, but are added to the total.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `greater_vital_strike` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Weapon Focus
*(feat)*

**Tags:** Combat, Offensive, Weapon
**Prerequisites:** Proficiency with selected weapon, Weapon Focus with selected weapon, base attack bonus +1, 8th-level fighter
**Source:** Core Rulebook (PZO1110) p. 117, 126
**Foundry id:** `IER2MzJrjSvxMlNS`

> *Choose one type of weapon (including unarmed strike or grapple) for which you have already selected Weapon Focus. You are a master at your chosen weapon.*
>
> **Prerequisites**: Proficiency with selected weapon, Weapon Focus with selected weapon, base attack bonus +1, 8th-level fighter.
>
> **Benefits**: You gain a +1 bonus on attack rolls you make using the selected weapon. This bonus stacks with other bonuses on attack rolls, including those from Weapon Focus.
>
> **Special**: You can gain Greater Weapon Focus multiple times. Its effects do not stack. Each time you take the feat, it applies to a new type of weapon.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `greater_weapon_focus` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Weapon Specialization
*(feat)*

**Tags:** Combat, Offensive, Weapon
**Prerequisites:** Proficiency with selected weapon, Greater Weapon Focus with selected weapon, Weapon Focus with selected weapon, Weapon Specialization with selected weapon, 12th-level fighter
**Source:** Core Rulebook (PZO1110) p. 117, 126
**Foundry id:** `asmQDyDYTtuXg8b4`

> *Choose one type of weapon (including unarmed strike or grapple) for which you possess the Weapon Specialization feat. Your attacks with the chosen weapon are more devastating than normal.*
>
> **Prerequisites**: Proficiency with selected weapon, Greater Weapon Focus with selected weapon, Weapon Focus with selected weapon, Weapon Specialization with selected weapon, 12th-level fighter.
>
> **Benefits**: You gain a +2 bonus on all damage rolls you make using the selected weapon. This bonus to damage stacks with other damage roll bonuses, including any you gain from Weapon Specialization.
>
> **Special**: You can gain Greater Weapon Specialization multiple times. Its effects do not stack. Each time you take the feat, it applies to a new type of weapon.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `greater_weapon_specialization` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Greater Whip Mastery
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Improved Whip Mastery, Weapon Focus (whip), Whip Mastery, base attack bonus +8
**Source:** Advanced Race Guide (PZO1131) p. 122; Bestiary (PZO1118) p. 103
**Foundry id:** `ypozx6qcx3ilwH9B`

> *You can use a whip to make combat maneuvers with ease.*
>
> **Prerequisites**: Improved Whip Mastery, Weapon Focus (whip), Whip Mastery, base attack bonus +8.
>
> **Benefits**: You are so quick with your whip that you never drop it due to a failed disarm or trip combat maneuver attempt. Further, you gain the ability to grapple using your whip. To do so, use the normal grapple rules with the following changes.
>
> *Attack:* You cannot use your whip to attack while you are using it to grapple an opponent.
>
> *Damage: *When dealing damage to your grappled opponent, you deal your whip's weapon damage rather than your unarmed strike damage.
>
> *Free Hands: *You take no penalty on your combat maneuver check for having fewer than two hands free when you use your whip to grapple.
>
> *Reach: *Rather than pulling your grappled opponent adjacent to you when you successfully grapple and when you move the grapple, you must keep him within your whip's reach minus his own reach to maintain the grapple. If the difference in reach is less than 0, such as is the case for a Medium whip wielder and a Gargantuan creature, you cannot grapple that opponent with your whip. If you have to pull a creature adjacent to you to grapple it with your whip, you still provoke an attack of opportunity from that opponent unless you have the Improved Grapple feat.
>
> *Tie Up: *While adjacent to your opponent, you can attempt to use your whip to tie him up. If you do so to an opponent you have grappled rather than pinned, you take only a -5 penalty on the combat maneuver check rather than the normal -10.
>
> ##### Combat Trick
>
> When you initiate a grapple with a whip, you can spend 5 stamina points to attempt a second grapple check as a swift action to either move or damage the creature you are grappling. This is not a check to maintain the grapple.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `greater_whip_mastery` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Grisly Ornament
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Harvest Parts
**Source:** PZO9478 (PZO9478) p. 24
**Foundry id:** `WOny1lHnaikwNDzH`

> *You adorn your gear with mementos from your foes.*
>
> **Prerequisites**: Harvest Parts.
>
> **Benefit**: You can attempt a Craft or Heal check to craft a special type of trophy called an ornament from part of a creature that’s been dead for less than an hour. You take a –4 penalty on this check if you or an ally didn’t slay the creature. You can craft one ornament per character level per day. Each corpse provides enough material for one ornament plus one additional ornament per size category above Medium. You can wear one ornament in each magic item slot not already occupied by another item. When you craft an ornament, you choose whether it affects Armor Class, attack rolls, CMB, CMD, saving throws, or skill checks. The ornament provides a morale bonus equal to the monster’s CR divided by 4 (round down, minimum 1) to the selected statistic against creatures of the same creature type as the source of the ornament. This bonus increases by 1 against creatures of the exact same variety (so a red dragon’s talon provides the increased bonus against red dragons but not all dragons). An ornament remains effective for 1 day, plus 1 additional day for every 5 by which you exceed the DC to craft it. You can give ornaments to others, but gifted ornaments have a morale bonus equal to the monster’s CR divided by 6 (round down, minimum 0) and remain effective for only 24 hours.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `grisly_ornament` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Harvest Parts
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Craft (any) 1 rank or Heal 1 rank
**Source:** PZO9478 (PZO9478) p. 24
**Foundry id:** `rpsKqlUNGhqRV97z`

> You can extract the choicest parts from a monster’s carcass to use as resources when crafting items.
>
> **Prerequisites**: Craft (any) 1 rank or Heal 1 rank.
>
> **Benefit**: You can attempt a Craft or Heal check, as though making a trophy, to gain usable resources from a creature that has been dead for less than an hour. Only creatures with a CR of 1 or higher yield usable parts. The value of the parts you harvest is equal to the creature’s CR squared × 10 gp (increases to CR derived from class levels or templates do not contribute to this value). This value can be used only as raw materials for crafting alchemical, masterwork, mundane, or magic items. Items crafted using creature parts must be made of a suitable material—typically bone or hide, with metal only in extraordinary cases. No more than a quarter of a crafted item’s cost can be supplied with harvested parts. Harvested parts remain usable for 2 days before they rot (unless used to craft objects or somehow preserved). Creature parts that are harvested in this manner can’t be bought or sold in most settlements.
>
> ##### Crafting Trophies
>
> Although any character can take trophies from fallen creatures for cosmetic or roleplaying purposes, the following feats allow characters to derive functionality from items they salvage from monstrous corpses. These feats work similarly to item creation feats, except trophies are created using a single Craft or Heal check, they are nonmagical, and the benefits they provide are typically temporary. The DC of such a check is equal to 15 + the creature’s CR, and creating a trophy takes a number of minutes equal to the creature’s CR.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `harvest_parts` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Haunt Scavenger
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Any one item creation feat or Craft (alchemy) 3 ranks
**Source:** PZO9471 (PZO9471) p. 30
**Foundry id:** `MaBR8MFF9sibtF4z`

> *You can use spiritual essence to craft magic items.*
>
> **Prerequisites**: Any one item creation feat or Craft (alchemy) 3 ranks.
>
> **Benefit**: You can harvest the ectoplasmic remains of haunts, incorporeal undead, or the like to craft magic items. Whenever you encounter a recently neutralized haunt, the remains of an incorporeal undead creature, or the remains of a creature that has the ability to possess another creature using a racial spell-like ability or supernatural ability (such as a ghost or a shadow demon), you can attempt to extract material components from those remains that are suitable for crafting magic items. You must have access to an alchemist’s lab (Pathfinder RPG Ultimate Equipment 76) in order to extract components from a haunt or creature, and you must begin extracting these components within 10 minutes of the haunt or creature’s death or destruction. After 10 minutes, the components have degraded too much to be of any use to you.
>
> Harvesting components with this feat can take several hours. Performing at least 1 minute of work extracting components from a haunt or creature prevents its material components from degrading further for 24 hours, allowing you to safely suspend and resume harvesting these components without fear of subsequent degradation. This ectoplasmic residue is portable once the extraction work begins, provided you have a vial to contain the source residue (the actual amount of residue is never much, physically, but the value of the components you can extract from the residue increases with the power of the original haunt or creature).
>
> Each hour, attempt a Craft (alchemy) or a Knowledge (religion) check to successfully handle the residue and extract useful material. The DC for this check is equal to 15 + the CR of the haunt or creature being harvested. If you succeed at the check, you harvest 50 gp worth of components. If you fail the check by 4 or less, you can attempt to harvest those components again. If you fail the check by 5 or more, the residue spoils and you cannot scavenge any more from that particular source. A single source can yield an amount of components up to a maximum value of 50 gp per point of CR before it is depleted.
>
> Material components harvested with Haunt Scavenger can be used in place of the material components of enchantment or necromancy spells and extracts, provided they are of equal or greater value compared to the spell’s normal material components. Additionally, they can be used in place of actual gold to fund the construction of a magic item with an enchantment or necromancy aura.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `haunt_scavenger` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Heighten Spell
*(feat)*

**Tags:** Metamagic, Magic
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 117, 126
**Foundry id:** `O109YFcItBFUDHvu`

> *You can cast spells as if they were a higher level.*
>
> **Benefits**: A heightened spell has a higher spell level than normal (up to a maximum of 9th level). Unlike other metamagic feats, Heighten Spell actually increases the effective level of the spell that it modifies. All effects dependent on spell level (such as saving throw DCs and ability to penetrate a *lesser globe of invulnerability*) are calculated according to the heightened level. The heightened spell is as difficult to prepare and cast as a spell of its effective level.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `heighten_spell` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Hover
*(feat)*

**Tags:** Monster
**Prerequisites:** Fly speed
**Source:** PZO1112 (PZO1112) p. 315
**Foundry id:** `6lqGh0NvprZpUUwV`

> *This creature can hover in place with ease and can kick up clouds of dust and debris.*
>
> **Prerequisites**: Fly speed.
>
> **Benefits**: A creature with this feat can halt its movement while flying, allowing it to hover without needing to make a Fly skill check.
>
> If a creature of size Large or larger with this feat hovers within 20 feet of the ground in an area with lots of loose debris, the draft from its wings creates a hemispherical cloud with a radius of 60 feet. The winds generated can snuff torches, small campfires, exposed lanterns, and other small, open flames of non-magical origin. Clear vision within the cloud is limited to 10 feet. Creatures have concealment at 15 to 20 feet (20% miss chance). At 25 feet or more, creatures have total concealment (50% miss chance, and opponents cannot use sight to locate the creature).
>
> **Normal**: Without this feat, a creature must make a Fly skill check to hover and the creature does not create a cloud of debris while hovering.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `hover` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Hurricane Punch
*(feat)*

**Tags:** Combat
**Prerequisites:** Str 13, Improved Bull Rush, Improved Unarmed Strike, Power Attack
**Source:** PZO9483 (PZO9483) p. 19
**Foundry id:** `SI5S8eZGMOwIDkiq`

> *Your fast strikes hit with the force of a hurricane, pushing your foes away.*
>
> **Prerequisites**: Str 13, Improved Bull Rush, Improved Unarmed Strike, Power Attack.
>
> **Benefit**: When you hit the same creature with unarmed strikes at least twice in the same round, you can attempt a bull rush combat maneuver against that creature as a swift action. You can also move with the target even if you have no movement remaining, but the distance you move can’t exceed half your speed.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `hurricane_punch` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Impaling Critical
*(feat)*

**Tags:** Combat, Critical, Combat Trick
**Prerequisites:** Critical Focus, Weapon Specialization with selected piercing melee weapon, base attack bonus +11
**Source:** Bestiary (PZO1118) p. 105; Advanced Race Guide (PZO1131) p. 122
**Foundry id:** `ecb9SMCyYPaPLCSy`

> *Your critical hits can skewer your foes.*
>
> **Prerequisites**: Critical Focus, Weapon Specialization with selected piercing melee weapon, base attack bonus +11.
>
> **Benefits**: Whenever you score a critical hit with the selected piercing melee weapon, you can impale your opponent on your weapon. While your opponent is impaled in this way, each time he starts his turn, you deal damage equal to your weapon's damage dice plus the extra damage dice from your weapon's properties. As an immediate action, you can pull your weapon out of your opponent. If your opponent is ever outside your reach, you must spend a free action to let go of your weapon or pull it out of him. Your opponent can also spend a move action to pull your weapon out. When the weapon comes out, your opponent takes damage as if starting his turn impaled. While you impale your opponent with your weapon, you cannot use it to attack, and you must hold on to it.
>
> ##### Combat Trick
>
> When you impale a foe with this feat, you can spend 5 stamina points to make the weapon require a standard action to remove (rather than a move action).

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `impaling_critical` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Bull Rush
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** Str 13, Power Attack, base attack bonus +1
**Source:** Core Rulebook (PZO1110) p. 126; Advanced Race Guide (PZO1131) p. 122
**Foundry id:** `dn2KgHFQRbuoNRx0`

> *You are skilled at pushing your foes around.*
>
> **Prerequisites**: Str 13, Power Attack, base attack bonus +1.
>
> **Benefits**: You do not provoke an attack of opportunity when performing a bull rush combat maneuver. In addition, you receive a +2 bonus on checks made to bull rush a foe. You also receive a +2 bonus to your Combat Maneuver Defense whenever an opponent tries to bull rush you.
>
> **Normal**: You provoke an attack of opportunity when performing a bull rush combat maneuver.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.bullRush`  (untyped)

**In our coverage tracker:** absent (slug `improved_bull_rush` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Channel
*(feat)*

**Tags:** Channeling
**Prerequisites:** Channel energy class feature
**Source:** Core Rulebook (PZO1110) p. 115, 126
**Foundry id:** `1HfwfBOSWtdxFQ2s`

> *Your channeled energy is harder to resist.*
>
> **Prerequisites**: Channel energy class feature.
>
> **Benefits**: Add 2 to the DC of saving throws made to resist the effects of your channel energy ability.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improved_channel` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Charging Hurler
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Charging Hurler, Point-Blank Shot
**Source:** Bestiary (PZO1118) p. 105; Advanced Race Guide (PZO1131) p. 122
**Foundry id:** `5r33SwOguzVDBb3m`

> *Every muscle in your body adds its force to your thrown weapons.*
>
> **Prerequisites**: Charging Hurler, Point-Blank Shot.
>
> **Benefits**: When you use Charging Hurler, your target can be at any range up to your weapon's maximum range. If your target is within 30 feet, you gain a +2 bonus on damage rolls.
>
> **Normal**: Using Charging Hurler requires you to end your movement within 30 feet of your opponent.
>
> ##### Combat Trick
>
> When using Charging Hurler against a target within 30 feet, you can spend up to 2 stamina points. When you do, the bonus on your damage roll for that attack increases by double the number of stamina points you spent.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improved_charging_hurler` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Counterspell
*(feat)*

**Tags:** General, Magic
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 115, 127-128
**Foundry id:** `V8GIvVaAofyw9xIl`

> *You are skilled at countering the spells of others using similar spells.*
>
> **Benefits**: When counterspelling, you may use a spell of the same school that is one or more spell levels higher than the target spell.
>
> **Normal**: Without this feat, you may counter a spell only with the same spell or with a spell specifically designated as countering the target spell.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improved_counterspell` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Critical
*(feat)*

**Tags:** Combat, Critical, Offensive
**Prerequisites:** Proficient with weapon, base attack bonus +8
**Source:** Core Rulebook (PZO1110) p. 115, 127
**Foundry id:** `TbOPtIL8Fv8obXtP`

> *Attacks made with your chosen weapon are quite deadly.*
>
> **Prerequisites**: Proficient with weapon, base attack bonus +8.
>
> **Benefits**: When using the weapon you selected, your threat range is doubled.
>
> **Special**: You can gain Improved Critical multiple times. The effects do not stack. Each time you take the feat, it applies to a new type of weapon.
>
> This effect doesn't stack with any other effect that expands the threat range of a weapon.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improved_critical` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Dirty Trick
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 162; Advanced Race Guide (PZO1131) p. 123
**Foundry id:** `LUOETW7Fm0oPKKWj`

> *You are skilled at pulling dirty tricks on your foes.*
>
> **Prerequisites:** Int 13, Combat Expertise.
>
> **Benefit:** You do not provoke an attack of opportunity when performing a dirty trick combat maneuver. In addition, you receive a +2 bonus on checks made to attempt a dirty trick. You also receive a +2 bonus to your Combat Maneuver Defense when an opponent tries a dirty trick on you.
>
> **Normal:** You provoke an attack of opportunity when performing a dirty trick combat maneuver.
>
> ##### Combat Trick
>
> You can select this feat even if you don’t meet the ability score prerequisite (Intelligence 13). You gain the benefits of this feat only as long as you have at least 1 stamina point in your stamina pool. When you are the target of a dirty trick combat maneuver, you can spend a number of stamina points up to your Strength or Dexterity bonus, whichever is greater. Your CMD against that dirty trick attempt increases by that number.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.dirtyTrick`  (untyped)

**In our coverage tracker:** absent (slug `improved_dirty_trick` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Disarm
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** Int 13, Combat Expertise
**Source:** Core Rulebook (PZO1110) p. 127; Advanced Race Guide (PZO1131) p. 123
**Foundry id:** `711B9WNFgpdDKKf2`

> *You are skilled at knocking weapons from a foe's grasp.*
>
> **Prerequisites**: Int 13, Combat Expertise.
>
> **Benefits**: You do not provoke an attack of opportunity when performing a disarm combat maneuver. In addition, you receive a +2 bonus on checks made to disarm a foe. You also receive a +2 bonus to your Combat Maneuver Defense whenever an opponent tries to disarm you.
>
> **Normal**: You provoke an attack of opportunity when performing a disarm combat maneuver.
>
> ##### Combat Trick
>
> You can select this feat even if you don't meet the ability score prerequisite (Intelligence 13). You gain the benefit of this feat only as long as you have at least 1 stamina point in your stamina pool. When you are the target of a disarm combat maneuver, you can spend a number of stamina points up to your Strength or Dexterity bonus, whichever is greater. Your CMD against that disarm attempt increases by that number.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.disarm`  (untyped)

**In our coverage tracker:** absent (slug `improved_disarm` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Drag
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 162; Advanced Race Guide (PZO1131) p. 123
**Foundry id:** `e1zIVW9AcrmRrYvx`

> *You are skilled at dragging foes around the battlefield.*
>
> **Prerequisites:** Str 13, Power Attack, base attack bonus +1.
>
> **Benefit:** You do not provoke an attack of opportunity when performing a drag combat maneuver. In addition, you receive a +2 bonus on checks made to drag a foe. You also receive a +2 bonus to your Combat Maneuver Defense when an opponent tries to drag you.
>
> **Normal:** You provoke an attack of opportunity when performing a drag combat maneuver.
>
> ##### Combat Trick
>
> When you are the target of a drag combat maneuver, you can spend a number of stamina points up to your Strength or Dexterity bonus, whichever is greater. Your CMD against that drag attempt increases by that number.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.drag`  (untyped)

**In our coverage tracker:** absent (slug `improved_drag` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Familiar
*(feat)*

**Tags:** Magic
**Prerequisites:** Ability to acquire a new familiar, compatible alignment, sufficiently high level (see below)
**Source:** Core Rulebook (PZO1110) p. 115, 127
**Foundry id:** `oRJlgRLS32fmoQpy`

> *This feat allows you to acquire a powerful familiar, but only when you could normally acquire a new familiar.*
>
> **Prerequisites**: Ability to acquire a new familiar, compatible alignment, sufficiently high level (see below).
>
> **Benefits**: When choosing a familiar, the creatures listed below are also available to you. You may choose a familiar with an alignment up to one step away on each alignment axis (lawful through chaotic, good through evil).
>  Familiar Alignment Arcane Spellcaster Level Celestial hawk1 Neutral good 3rd Dire rat Neutral 3rd Fiendish viper2 Neutral evil 3rd Elemental, Small (any type) Neutral 5th Stirge Neutral 5th Homunculus3 Any 7th Imp Lawful evil 7th Mephit (any type) Neutral 7th Pseudodragon Neutral good 7th Quasit Chaotic evil 7th 1 Or other celestial animal from the standard familiar list. 2 Or other fiendish animal from the standard familiar list. 3 The master must first create the homunculus. 
>
> Improved familiars otherwise use the rules for regular familiars, with two exceptions: if the creature's type is something other than animal, its type does not change; and improved familiars do not gain the ability to speak with other creatures of their kind (although many of them already have the ability to communicate).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improved_familiar` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Feint
*(feat)*

**Tags:** Combat, Combat Maneuver, Offensive
**Prerequisites:** Int 13, Combat Expertise
**Source:** Core Rulebook (PZO1110) p. 114, 127
**Foundry id:** `tocde3sKG1O3GKgd`

> *You are skilled at fooling your opponents in combat.*
>
> **Prerequisites**: Int 13, Combat Expertise.
>
> **Benefits**: You can make a Bluff check to feint in combat as a move action.
>
> **Normal**: Feinting in combat is a standard action.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improved_feint` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Grapple
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** Dex 13, Improved Unarmed Strike
**Source:** Core Rulebook (PZO1110) p. 127; Advanced Race Guide (PZO1131) p. 123
**Foundry id:** `ZmQkRk93nbHxsQSt`

> *You are skilled at grappling opponents.*
>
> **Prerequisites**: Dex 13, Improved Unarmed Strike.
>
> **Benefits**: You do not provoke an attack of opportunity when performing a grapple combat maneuver. In addition, you receive a +2 bonus on checks made to grapple a foe. You also receive a +2 bonus to your Combat Maneuver Defense whenever an opponent tries to grapple you.
>
> **Normal**: You provoke an attack of opportunity when performing a grapple combat maneuver.
>
> ##### Combat Trick
>
> When you are the target of a grapple combat maneuver to initiate or maintain a grapple, you can spend a number of stamina points up to your Strength or Dexterity bonus, whichever is greater. Your CMD against that grapple attempt increases by that number.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.grapple`  (untyped)

**In our coverage tracker:** absent (slug `improved_grapple` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Great Fortitude
*(feat)*

**Tags:** General, Saving Throw
**Prerequisites:** Great Fortitude
**Source:** Core Rulebook (PZO1110) p. 115, 127
**Foundry id:** `1hxjrJ68yWsiCCFD`

> *You can draw upon an inner reserve to resist diseases, poisons, and other grievous harm.*
>
> **Prerequisites**: Great Fortitude.
>
> **Benefits**: Once per day, you may reroll a Fortitude save. You must decide to use this ability before the results are revealed. You must take the second roll, even if it is worse.

**Mechanical encoding:** has `scriptCalls`

**In our coverage tracker:** absent (slug `improved_great_fortitude` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Initiative
*(feat)*

**Tags:** Combat
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 115, 127
**Foundry id:** `Uuiu3p982omhMEPj`

> *Your quick reflexes allow you to react rapidly to danger.*
>
> **Benefits**: You get a +4 bonus on initiative checks.

**Mechanical encoding:** `changes`: 1
  - `4` → `init`  (untyped)

**In our coverage tracker:** `IMPLEMENTED` — +4 initiative
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Iron Will
*(feat)*

**Tags:** General, Saving Throw
**Prerequisites:** Iron Will
**Source:** Core Rulebook (PZO1110) p. 115, 127
**Foundry id:** `cKxfEL5XOWuzLhfO`

> *Your clarity of thought allows you to resist mental attacks.*
>
> **Prerequisites**: Iron Will.
>
> **Benefits**: Once per day, you may reroll a Will save. You must decide to use this ability before the results are revealed. You must take the second roll, even if it is worse.

**Mechanical encoding:** has `scriptCalls`

**In our coverage tracker:** absent (slug `improved_iron_will` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Ki Throw
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Improved Bull Rush, Ki Throw
**Source:** Advanced Player's Guide (PZO1115) p. 163
**Foundry id:** `GUN1ISsoORAqxNOM`

> *Your enemies are living weapons in your hands.*
>
> **Prerequisites**: Improved Bull Rush, Ki Throw.
>
> **Benefit**: When using the Ki Throw feat, you may throw your target into any square you threaten that is occupied by another creature. Make a bull rush combat maneuver check with a –4 penalty against the secondary target. If this check succeeds, the thrown creature lands prone in the secondary target’s square, while the secondary target is pushed back and knocked prone in an adjacent square. If the check fails, the thrown creature lands prone in the nearest square you threaten adjacent to the secondary target.
>
> If you throw a Large or larger creature into an area containing multiple secondary targets, you take an additional penalty of –4 on your combat maneuver check for each target after the first.
>
> **Special**: A monk may take this as a bonus feat at 14th level.
>
> ##### Combat Trick
>
> When using this feat to throw a target into another creature’s space, you can spend up to 6 stamina points to reduce the penalty on the bull rush attempt against the secondary target by an amount equal to the number of stamina points you spent.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improved_ki_throw` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Lightning Reflexes
*(feat)*

**Tags:** General, Saving Throw
**Prerequisites:** Lightning Reflexes
**Source:** Core Rulebook (PZO1110) p. 115, 127
**Foundry id:** `PrthT5jZl4t3znqR`

> *You have a knack for avoiding danger all around you.*
>
> **Prerequisites**: Lightning Reflexes.
>
> **Benefits**: Once per day, you may reroll a Reflex save. You must decide to use this ability before the results are revealed. You must take the second roll, even if it is worse.

**Mechanical encoding:** has `scriptCalls`

**In our coverage tracker:** absent (slug `improved_lightning_reflexes` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Natural Armor
*(feat)*

**Tags:** Monster
**Prerequisites:** Natural armor, Con 13
**Source:** PZO1112 (PZO1112) p. 315
**Foundry id:** `n1wLrcwaqOSDqrOo`

> *This creature's hide is tougher than most.*
>
> **Prerequisites**: Natural armor, Con 13.
>
> **Benefits**: The creature's natural armor bonus increases by +1.
>
> **Special**: A creature can gain this feat multiple times. Each time the creature takes the feat, its natural armor bonus increases by another point.

**Mechanical encoding:** `changes`: 1
  - `1` → `nac`  (untyped)

**In our coverage tracker:** absent (slug `improved_natural_armor` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Natural Attack
*(feat)*

**Tags:** Monster
**Prerequisites:** Natural weapon, base attack bonus +4
**Source:** PZO1112 (PZO1112) p. 315
**Foundry id:** `8viuSwNbDvZZaiak`

> *Attacks made by one of this creature’s natural attacks leave vicious wounds.*
>
> **Prerequisites**: Natural weapon, base attack bonus +4.
>
> **Benefit**: Choose one of the creature’s natural attack forms (not an unarmed strike). The damage for this natural attack increases by one step on the following list, as if the creature’s size had increased by one category. Damage dice increase as follows: 1d2, 1d3, 1d4, 1d6, 1d8, 2d6, 3d6, 4d6, 6d6, 8d6, 12d6.
>
> A weapon or attack that deals 1d10 points of damage increases as follows: 1d10, 2d8, 3d8, 4d8, 6d8, 8d8, 12d8.
>
> **Special**: This feat can be taken multiple times. Each time it is taken, it applies to a different natural attack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improved_natural_attack` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Overrun
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** Str 13, Power Attack, base attack bonus +1
**Source:** Core Rulebook (PZO1110) p. 127; Advanced Race Guide (PZO1131) p. 123
**Foundry id:** `go4xOiSUP8R1QJ5N`

> *You are skilled at running down your foes.*
>
> **Prerequisites**: Str 13, Power Attack, base attack bonus +1.
>
> **Benefits**: You do not provoke an attack of opportunity when performing an overrun combat maneuver. In addition, you receive a +2 bonus on checks made to overrrun a foe. You also receive a +2 bonus to your Combat Maneuver Defense whenever an opponent tries to overrun you. Targets of your overrun attempt may not chose to avoid you.
>
> **Normal**: You provoke an attack of opportunity when performing an overrun combat maneuver.
>
> ##### Combat Trick
>
> When you are the target of an overrun combat maneuver, you can spend a number of stamina points up to your Strength or Dexterity bonus, whichever is greater. Your CMD against that overrun attempt increases by that number.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.overrun`  (untyped)

**In our coverage tracker:** absent (slug `improved_overrun` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Precise Shot
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Dex 19, Point-Blank Shot, Precise Shot, base attack bonus +11
**Source:** Core Rulebook (PZO1110) p. 116, 128
**Foundry id:** `h1vqUG9Kh3f7oKWK`

> *Your ranged attacks ignore anything but total concealment and cover.*
>
> **Prerequisites**: Dex 19, Point-Blank Shot, Precise Shot, base attack bonus +11.
>
> **Benefits**: Your ranged attacks ignore the AC bonus granted to targets by anything less than total cover, and the miss chance granted to targets by anything less than total concealment. Total cover and total concealment provide their normal benefits against your ranged attacks.
>
> **Normal**: See the normal rules on the effects of cover and concealment in Combat.
>
> ##### Combat Trick
>
> When you use the ability of the Precise Shot combat trick, the bonuses increase to +4.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improved_precise_shot` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Reposition
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 163; Advanced Race Guide (PZO1131) p. 123
**Foundry id:** `CYHloH6aEnfgdxAV`

> *You have learned how to force your enemies to move around the battlefield.*
>
> **Prerequisites:** Int 13, Combat Expertise.
>
> **Benefit:** You do not provoke an attack of opportunity when performing a reposition combat maneuver. In addition, you receive a +2 bonus on checks made to reposition a foe. You also receive a +2 bonus to your Combat Maneuver Defense when an opponent tries to reposition you.
>
> **Normal:** You provoke an attack of opportunity when performing a reposition combat maneuver.
>
> ##### Combat Trick
>
> You can select this feat even if you don’t meet the ability score prerequisite (Intelligence 13). You gain the benefits of this feat only as long as you have at least 1 stamina point in your stamina pool. When you are the target of a reposition combat maneuver, you can spend a number of stamina points up to your Strength or Dexterity bonus, whichever is greater. Your CMD against that reposition attempt increases by that number.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.reposition`  (untyped)

**In our coverage tracker:** absent (slug `improved_reposition` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Shield Bash
*(feat)*

**Tags:** Combat, Offensive
**Prerequisites:** Shield Proficiency
**Source:** Core Rulebook (PZO1110) p. 116, 128
**Foundry id:** `qYv70Ch9RQfi1LQQ`

> *You can protect yourself with your shield, even if you use it to attack.*
>
> **Prerequisites**: Shield Proficiency.
>
> **Benefits**: When you perform a shield bash, you may still apply the shield's shield bonus to your AC.
>
> **Normal**: Without this feat, a character that performs a shield bash loses the shield's shield bonus to AC until his next turn (see Equipment).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improved_shield_bash` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Snap Shot
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Dex 15, Point-Blank Shot, Rapid Shot, Snap Shot, Weapon Focus, base attack bonus +9
**Source:** Advanced Race Guide (PZO1131) p. 123; Bestiary (PZO1118) p. 106
**Foundry id:** `EiSKVmyOAd6mGdEb`

> *You can take advantage of your opponent's vulnerabilities from a greater distance, and without exposing yourself.*
>
> **Prerequisites**: Dex 15, Point-Blank Shot, Rapid Shot, Snap Shot, Weapon Focus, base attack bonus +9.
>
> **Benefits**: You threaten an additional 5 feet with Snap Shot.
>
> **Normal**: Making a ranged attack provokes attacks of opportunity.
>
> ##### Combat Trick
>
> At the end of your turn, you can spend 5 stamina points to threaten an additional 15 feet with Snap Shot (instead of an additional 10 feet) until you take an attack of opportunity against an opponent in the expanded threat range or the beginning of your next turn, whichever comes first.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improved_snap_shot` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Spring Attack
*(feat)*

**Tags:** Combat, Offensive, Movement
**Prerequisites:** Dex 15, Dodge, Mobility, Nimble Moves, Spring Attack, base attack bonus +9
**Source:** Occult Adventures (PZO1140) p. 114
**Foundry id:** `D5VflgZupUiegFAY`

> *You dart through the press of battle like a breeze, assaulting foes as you pass.*
>
> **Prerequisites**: Dex 15, Dodge, Mobility, Nimble Moves, Spring Attack, base attack bonus +9.
>
> **Benefit**: When you use Spring Attack, you can select two targets to attack during your movement instead of one. The second attack made this way is made at your full base attack bonus – 5. All restrictions of Spring Attack apply to both targets, and your movement does not provoke attacks of opportunity from either target. You can’t target the same creature twice.
>
> **Special**: A monk of at least 14th level can select this feat as a monk bonus feat, but only if he has Spring Attack.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `improved_spring_attack` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Steal
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** Int 13, Combat Expertise
**Source:** Advanced Player's Guide (PZO1115) p. 163; Advanced Race Guide (PZO1131) p. 124
**Foundry id:** `Kbuy0bkPlOYz5yaO`

> *You have a knack for snatching items from your opponents.*
>
> **Prerequisites**: Int 13, Combat Expertise.
>
> **Benefits**: You do not provoke an attack of opportunity when performing a steal combat maneuver. In addition, you receive a +2 bonus on checks made to steal an item from a foe. You also receive a +2 bonus to your Combat Maneuver Defense when an opponent tries to steal an item from you.
>
> **Normal**: You provoke an attack of opportunity when performing a steal combat maneuver.
>
> ##### Combat Trick
>
> You can select this feat even if you don’t meet the ability score prerequisite (Intelligence 13). You gain the benefits of this feat only as long as you have at least 1 stamina point in your stamina pool. When you are the target of a steal combat maneuver, you can spend a number of stamina points up to your Strength or Dexterity bonus, whichever is greater. Your CMD against that steal attempt increases by that number.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.steal`  (untyped)

**In our coverage tracker:** absent (slug `improved_steal` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Sunder
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** Str 13, Power Attack, base attack bonus +1
**Source:** Core Rulebook (PZO1110) p. 128; Advanced Race Guide (PZO1131) p. 124
**Foundry id:** `lpXdFoT6OqS5vi2X`

> *You are skilled at damaging your foes' weapons and armor.*
>
> **Prerequisites**: Str 13, Power Attack, base attack bonus +1.
>
> **Benefits**: You do not provoke an attack of opportunity when performing a sunder combat maneuver. In addition, you receive a +2 bonus on checks made to sunder an item. You also receive a +2 bonus to your Combat Maneuver Defense whenever an opponent tries to sunder your gear.
>
> **Normal**: You provoke an attack of opportunity when performing a sunder combat maneuver.
>
> ##### Combat Trick
>
> When you are the target of a sunder combat maneuver, you can spend a number of stamina points up to your Strength or Dexterity bonus, whichever is greater. Your CMD increases by that number for that sunder attempt.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.sunder`  (untyped)

**In our coverage tracker:** absent (slug `improved_sunder` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Swap Places
*(feat)*

**Tags:** Combat, Teamwork, Combat Trick
**Prerequisites:** Swap Places
**Source:** Advanced Class Guide (PZO1129) p. 150
**Foundry id:** `9j6OM2njOSADu8H9`

> *When you switch places with your comrade, your sizes don’t matter.*
>
> **Prerequisites**: Swap Places.
>
> **Benefit**: When you and your ally use Swap Places, your ally can be up to one size larger or smaller than you, and your movement into the ally’s square does not provoke an attack of opportunity. If your ally cannot fit into the space you had been occupying and there are no available adjacent squares to accommodate the rest of the ally’s space, the ally must squeeze. Alternatively, as part of its movement, the ally can attempt a bull rush combat maneuver against a creature that occupies a space your ally would occupy, but this bull rush cannot move the creature more than 5 feet.
>
> **Normal**: Using Swap Places requires you and your ally to be the same size, and your movement into the ally’s square provokes attacks of opportunity.
>
> ##### Combat Trick
>
> When you attempt a bull rush when using this feat, you can spend 2 stamina points to gain the ability to move the target of that combat maneuver more than 5 feet if necessary to create space for your ally (you must still roll high enough on the bull rush attempt to move the target an extra distance, as normal).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improved_swap_places` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Trip
*(feat)*

**Tags:** Combat, Offensive, Combat Maneuver, Combat Trick
**Prerequisites:** Int 13, Combat Expertise
**Source:** Core Rulebook (PZO1110) p. 128; Advanced Race Guide (PZO1131) p. 124
**Foundry id:** `gTrGPxzN054GfpkM`

> *You are skilled at sending your opponents to the ground.*
>
> **Prerequisites**: Int 13, Combat Expertise.
>
> **Benefits**: You do not provoke an attack of opportunity when performing a trip combat maneuver. In addition, you receive a +2 bonus on checks made to trip a foe. You also receive a +2 bonus to your Combat Maneuver Defense whenever an opponent tries to trip you.
>
> **Normal**: You provoke an attack of opportunity when performing a trip combat maneuver.
>
> ##### Combat Trick
>
> You can select this feat even if you don't meet the ability score prerequisite (Intelligence 13). You gain the benefits of this feat only as long as you have at least 1 stamina point in your stamina pool. When you are the target of a trip combat maneuver, you can spend a number of stamina points up to your Strength or Dexterity bonus, whichever is greater. Your CMD against that trip attempt increases by that number.

**Mechanical encoding:** `changes`: 1
  - `2` → `cmb.trip`  (untyped)

**In our coverage tracker:** absent (slug `improved_trip` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Two-Weapon Feint
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Dex 17, Int 13, Combat Expertise, Improved Two-Weapon Fighting, Two-Weapon Feint, Two-Weapon Fighting, base attack bonus +6
**Source:** Bestiary (PZO1118) p. 106; Advanced Race Guide (PZO1131) p. 124
**Foundry id:** `SNLBrZVKytb0S3tS`

> *Your primary weapon keeps a foe off balance, allowing you to slip your off-hand weapon past his defenses.*
>
> **Prerequisites**: Dex 17, Int 13, Combat Expertise, Improved Two-Weapon Fighting, Two-Weapon Feint, Two-Weapon Fighting, base attack bonus +6.
>
> **Benefits**: While using Two-Weapon Fighting to make melee attacks, you can forgo your first primary-hand melee attack to make a Bluff check to feint an opponent. If you successfully feint, that opponent is denied his Dexterity bonus to AC until the end of your turn.
>
> ##### Combat Trick
>
> You can select this feat even if you don't meet the ability score prerequisite (Intelligence 13). You gain the benefits of this feat only as long as you have at least 1 stamina point in your stamina pool. You can spend 5 stamina points to increase the duration for which the opponent is denied its Dexterity bonus until the start of your next turn.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improved_two_weapon_feint` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Two-Weapon Fighting
*(feat)*

**Tags:** Combat, Weapon, Two Weapons, Offensive
**Prerequisites:** Dex 17, Two-Weapon Fighting, base attack bonus +6
**Source:** Core Rulebook (PZO1110) p. 116, 128
**Foundry id:** `3fNdl7eIUJ5d5fwg`

> *You are skilled at fighting with two weapons.*
>
> **Prerequisites**: Dex 17, Two-Weapon Fighting, base attack bonus +6.
>
> **Benefits**: In addition to the standard single extra attack you get with an off-hand weapon, you get a second attack with it, albeit at a -5 penalty.
>
> **Normal**: Without this feat, you can only get a single extra attack with an off-hand weapon.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improved_two_weapon_fighting` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Unarmed Strike
*(feat)*

**Tags:** Combat, Unarmed, Offensive
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 115, 128
**Foundry id:** `2aTFNMs3pW6nUBlr`

> *You are skilled at fighting while unarmed.*
>
> **Benefits**: You are considered to be armed even when unarmed — you do not provoke attacks of opportunity when you attack foes while unarmed. Your unarmed strikes can deal lethal or nonlethal damage, at your choice.
>
> **Normal**: Without this feat, you are considered unarmed when attacking with an unarmed strike, and you can deal only nonlethal damage with such an attack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `NOT_IMPLEMENTED` — treats unarmed as armed; lethal damage option
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Vital Strike
*(feat)*

**Tags:** Combat, Offensive
**Prerequisites:** Vital Strike, base attack bonus +11
**Source:** Core Rulebook (PZO1110) p. 117, 128
**Foundry id:** `DorPGQ2mifJbMKH8`

> *You can make a single attack that deals a large amount of damage.*
>
> **Prerequisites**: Vital Strike, base attack bonus +11.
>
> **Benefits**: When you use the attack action, you can make one attack at your highest base attack bonus that deals additional damage. Roll the weapon's damage dice for the attack three times and add the results together before adding bonuses from Strength, weapon special abilities (such as *flaming*), precision based damage, and other damage bonuses. These extra weapon damage dice are not multiplied on a critical hit, but are added to the total.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improved_vital_strike` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improved Whip Mastery
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Weapon Focus (whip), Whip Mastery, base attack bonus +5
**Source:** Advanced Race Guide (PZO1131) p. 124; Bestiary (PZO1118) p. 106
**Foundry id:** `pDzBCnBZXHydBPJx`

> *You are able to entangle opponents with the coils of your whip.*
>
> **Prerequisites**: Weapon Focus (whip), Whip Mastery, base attack bonus +5.
>
> **Benefits**: While wielding a whip, you threaten the area of your natural reach plus 5 feet. You can also use a whip to grasp an unattended Small or Tiny object within your whip's reach and pull that object into your square. To do so, you must hit AC 10 with a melee touch attack. Further, you can use the whip to grasp onto an object within your whip's reach, using 5 feet of your whip as if it were a grappling hook, allowing you to use the rest of your whip to swing on like a rope. As a free action, you can release the object your whip is grasping, but you cannot use the whip to attack while the whip is grasping an object.
>
> ##### Combat Trick
>
> At the start of your turn, you can spend 5 stamina points to increase the radius of the area you threaten while wielding a whip by an additional 5 feet until you make an attack against an opponent in the expanded reach or the beginning of your next turn, whichever comes first.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improved_whip_mastery` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Improvised Weapon Mastery
*(feat)*

**Tags:** Combat, Offensive
**Prerequisites:** Catch Off-Guard or Throw Anything, base attack bonus +8
**Source:** Core Rulebook (PZO1110) p. 115, 128
**Foundry id:** `z5G64ZSUDNdgeICT`

> *You can turn nearly any object into a deadly weapon, from a razor-sharp chair leg to a sack of flour.*
>
> **Prerequisites**: Catch Off-Guard or Throw Anything, base attack bonus +8.
>
> **Benefits**: You do not suffer any penalties for using an improvised weapon. Increase the amount of damage dealt by the improvised weapon by one step (for example, 1d4 becomes 1d6) to a maximum of 1d8 (2d6 if the improvised weapon is two-handed). The improvised weapon has a critical threat range of 19–20, with a critical multiplier of ×2.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `improvised_weapon_mastery` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### In Harm’s Way
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 164
**Foundry id:** `nW2GUYlGhZ2bmgdz`

> *You put yourself in danger’s path to save your allies.*
>
> **Prerequisites:** Bodyguard.
>
> **Benefit:** While using the aid another action to improve an adjacent ally’s AC, you can intercept a successful attack against that ally as an immediate action, taking full damage from that attack and any associated effects (bleed, poison, etc.). A creature cannot benefit from this feat more than once per attack.
>
> ##### Combat Trick
>
> When using this feat’s benefit, you can spend up to 5 stamina points to reduce the damage from the intercepted attack by an amount equal to double the number of stamina points you spent this way. This does not alter other effects from that attack (such as bleed, poison, etc.), even if the damage is reduced to 0.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `in_harm_s_way` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Infuse Poison
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Brew Potion, Craft (alchemy) 5 ranks, caster level 3rd
**Source:** PZO9462 (PZO9462) p. 12
**Foundry id:** `FtAXizfqhTNauRYh`

> You can infuse a poison with a magical effect.
>
> **Prerequisites**: Brew Potion, Craft (alchemy) 5 ranks, caster level 3rd.
>
> **Benefit**: You can infuse an ingested poison with any spell of 3rd level or lower that you know and that targets one or more creatures and has a casting time of less than 1 minute. Infusing a poison takes 2 hours if its base price is 250 gp or less; otherwise, infusing a poison takes 1 day for each 1,000 gp in its base price. When you infuse a poison, you set the caster level, which must be sufficient to cast the spell in question and no higher than your own caster level. To infuse a poison, you must use up raw materials costing half of its base price.
>
> When you create an infused poison, you make any choices that you would normally make when casting the spell.
>
> Whoever ingests the infused poison is the target of the spell.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `infuse_poison` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Inner Flame
*(feat)*

**Tags:** Combat, Ifrit, Combat Trick
**Prerequisites:** Scorching Weapons, character level 7th, ifrit
**Source:** Ultimate Combat (PZO1121) p. 130; Advanced Race Guide (PZO1131) p. 124
**Foundry id:** `DAC7m76dINHq2liy`

> *Your body generates so much heat that your mere touch scorches your enemies.*
>
> **Prerequisites**: Scorching Weapons, character level 7th, ifrit.
>
> **Benefits**: Your bonus on saves against fire attacks and spells with the fire descriptor or light descriptor increases to +4. When you use Scorching Weapons, the affected weapons deal an additional 1d6 points of fire damage instead of 1, and when you are grappling, you deal this damage to your grappling opponent on your turn.
>
> ##### Combat Trick
>
> When you fail a saving throw against an effect that has the fire or light descriptor, you can spend 5 stamina points to reroll the saving throw. You must take the second result, even if it is worse.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `inner_flame` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Inscribe Magical Tattoo
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Craft (calligraphy, paintings, or tattoos) 5 ranks, caster level 5th
**Source:** PZO9237 (PZO9237) p. 16
**Foundry id:** `6dfwJL4eOK4J0oK5`

> *You can craft magical tattoos.*
>
> **Prerequisites**: Craft (calligraphy, paintings, or tattoos) 5 ranks, caster level 5th
>
> **Benefit**: You can create magical tattoos, magic items inked directly into the flesh of a willing or helpless creature. Both you and the recipient of the tattoo (if the recipient is not yourself) must be present during the entire tattooing process. Magic tattoos must be placed on a part of the body normally able to hold a magic item slot, but they do not count against or interfere with magic items worn on those slots. A single slot can only hold one magical tattoo (nonmagical tattoos and tattoos acquired from the tattooed sorcerer archetype do not count against this limit). Tattoos may be inscribed on the following slots: belt, body, chest, feet, hands, head, neck, shoulder, ring (up to two), or wrist. They cannot be inscribed on armor, eye, headband, or shield slots.
>
> Magical tattoos are difficult to destroy, though they count as magic items for the purposes of dispel magic. The spell erase can permanently destroy a magical tattoo, but the bearer of the tattoo can resist the spell with a Will save, in addition to the caster needing to make a successful caster level check to erase the tattoo. Physically removing a magical tattoo with a sharp instrument or defacing it with fire or acid can destroy it as well. Doing so is a full-round action that not only requires the target to be willing or helpless, but also provokes attacks of opportunity. At least 2 points of damage per caster level of the tattoo must be dealt to destroy a magical tattoo in this manner.
>
> Magical tattoos follow the rules for magic item creation as though they were wondrous items, except that they can use the Craft (calligraphy, paintings, tattoos) skill. New magical tattoos can be researched and designed using the guidelines for pricing new magic items. Magical tattoos are treated as slotless magical items for pricing purposes.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `inscribe_magical_tattoo` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Intimidating Prowess
*(feat)*

**Tags:** General, Skill
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 115, 128
**Foundry id:** `O0jbkTJcIji9BNiF`

> *Your physical might is intimidating to others.*
>
> **Benefits**: Add your Strength modifier to Intimidate skill checks in addition to your Charisma modifier.

**Mechanical encoding:** `changes`: 1
  - `max(0, @abilities.str.mod)` → `skill.int`  (untyped)

**In our coverage tracker:** absent (slug `intimidating_prowess` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Iron Will
*(feat)*

**Tags:** General, Saving Throw
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 115, 129
**Foundry id:** `iAbIGhm7T2OK9Brt`

> *You are more resistant to mental effects.*
>
> **Benefits**: You get a +2 bonus on all Will saving throws.

**Mechanical encoding:** `changes`: 1
  - `2` → `will`  (untyped)

**In our coverage tracker:** `IMPLEMENTED` — +2 will save
**Manual verdict:** `[ ]`
**Notes:**

---

### Ki Throw
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Improved Trip, Improved Unarmed Strike
**Source:** Advanced Player's Guide (PZO1115) p. 164
**Foundry id:** `IWcbDa0ITsDdiHjo`

> Your physical control and mastery of momentum allows you to throw enemies.
>
> **Prerequisites**: Improved Trip, Improved Unarmed Strike.
>
> **Benefit**: On a successful unarmed trip attack against a target your size or smaller, you may throw the target prone in any square you threaten rather than its own square. This movement does not provoke attacks of opportunity, and you cannot throw the creature into a space occupied by other creatures.
>
> **Special**: A monk may gain Ki Throw as a bonus feat at 10th level. A monk with this feat can affect creatures larger than his own size by spending 1 ki point per size category difference.
>
> ##### Combat Trick
>
> You can spend 5 stamina points to throw a creature one size category larger than you.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `ki_throw` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Leadership
*(feat)*

**Tags:** General
**Prerequisites:** Character level 7th
**Source:** Core Rulebook (PZO1110) p. 115, 129
**Foundry id:** `R3a1OV18RwDJftvq`

> *You attract followers to your cause and a companion to join you on your adventures.*
>
> **Prerequisites**: Character level 7th.
>
> **Benefits**: This feat enables you to attract a loyal cohort and a number of devoted subordinates who assist you. A cohort is generally an NPC with class levels, while followers are typically lower level NPCs. See Table below for what level of cohort and how many followers you can recruit.
>  Leadership Score Cohort Level Number of Followers by Level 1st 2nd 3rd 4th 5th 6th 1 or lower — — — — — — — 2 1st — — — — — — 3 2nd — — — — — — 4 3rd — — — — — — 5 3rd — — — — — — 6 4th — — — — — — 7 5th — — — — — — 8 5th — — — — — — 9 6th — — — — — — 10 7th 5 — — — — — 11 7th 6 — — — — — 12 8th 8 — — — — — 13 9th 10 1 — — — — 14 10th 15 1 — — — — 15 10th 20 2 1 — — — 16 11th 25 2 1 — — — 17 12th 30 3 1 1 — — 18 12th 35 3 1 1 — — 19 13th 40 4 2 1 1 — 20 14th 50 5 3 2 1 — 21 15th 60 6 3 2 1 1 22 15th 75 7 4 2 2 1 23 16th 90 9 5 3 2 1 24 17th 110 11 6 3 2 1 25 or higher 17th 135 13 7 4 2 2 
>
> **Leadership Modifiers**: Several factors can affect your Leadership score, causing it to vary from the base score (character level + Cha modifier). Your reputation (from the point of view of the cohort or follower you are trying to attract) raises or lowers your Leadership score:
>  Leader's Reputation Modifier Great renown +2 Fairness and generosity +1 Special power +1 Failure -1 Aloofness -1 Cruelty -2 
>
> Other modifiers may apply when you try to attract a cohort, as listed below.
>  The Leader... Modifier Has a familiar, special mount, or animal companion -2 Recruits a cohort of a different alignment -1 Caused the death of a cohort -2* *Cumulative per cohort killed. 
>
> Followers have different priorities from cohorts. When you try to attract a follower, use the following modifiers.
>  The Leader... Modifier Has a stronghold, base of operations, guildhouse, etc. +2 Moves around a lot -1 Caused the death of other followers -1 
>
> **Leadership Score**: Your base Leadership score equals your level plus your Charisma modifier. In order to take into account negative Charisma modifiers, this table allows for very low Leadership scores, but you must still be 7th level or higher in order to gain the Leadership feat. Outside factors can affect your Leadership score, as detailed above.
>
> **Cohort Level**: You can attract a cohort of up to this level. Regardless of your Leadership score, you can only recruit a cohort who is two or more levels lower than yourself. The cohort should be equipped with gear appropriate for its level (see Creating NPCs). A cohort can be of any race or class. The cohort's alignment may not be opposed to your alignment on either the law/chaos or good/evil axis, and you take a -1 penalty to your Leadership score if you recruit a cohort of an alignment different from your own.
>
> A cohort does not count as a party member when determining the party's XP. Instead, divide the cohort's level by your level. Multiply this result by the total XP awarded to you, then add that number of experience points to the cohort's total.
>
> If a cohort gains enough XP to bring it to a level one lower than your level, the cohort does not gain the new level — its new XP total is 1 less than the amount needed to attain the next level.
>
> **Number of Followers by Level**: You can lead up to the indicated number of characters of each level. Followers are similar to cohorts, except they're generally low-level NPCs. Because they're usually 5 or more levels behind you, they're rarely effective in combat.
>
> Followers don't earn experience and thus don't gain levels. When you gain a new level, consult Table: Leadership to determine if you acquire more followers, some of whom may be higher level than the existing followers. Don't consult the table to see if your cohort gains levels, however, because cohorts earn experience on their own.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `leadership` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Lifecrafting
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Craft Construct, Leadership, wyrwood
**Source:** PZO9495 (PZO9495) p. 7
**Foundry id:** `HoN8pq9Q72T8WbOX`

> *Your crafting skill and the secret knowledge of your people allows you to create new wyrwoods.*
>
> **Prerequisites**: Craft Construct, Leadership, wyrwood.
>
> **Benefit**: By completing a unique ritual, you can create a wyrwood. While you can use any Small wooden construct to create the base of a wyrwood, infusing it with life and consciousness requires a specific process. The process requires a flawless ioun stone worth at least 10,000 gp. For the ritual to succeed, you must spend 1 month in complete isolation with the construct that will become a wyrwood. Each week, you must succeed at a DC 30 Craft (carpentry) or Craft (sculpture) check. Failure requires you to start again, although the materials can be reused. Over this time, the construct reshapes itself around the ioun stone until it finds the form it will take permanently— thus even non-humanoid constructs become humanoid as they become wyrwoods. While wyrwoods are born as fully formed adults, they lack any skill or training, so they have only 1 level in the commoner class.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `lifecrafting` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Lightning Reflexes
*(feat)*

**Tags:** General, Saving Throw
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 115, 130
**Foundry id:** `0bZf3SDkvVOe2ujH`

> *You have faster reflexes than normal.*
>
> **Benefits**: You get a +2 bonus on all Reflex saving throws.

**Mechanical encoding:** `changes`: 1
  - `2` → `ref`  (untyped)

**In our coverage tracker:** `IMPLEMENTED` — +2 ref save
**Manual verdict:** `[ ]`
**Notes:**

---

### Lightning Stance
*(feat)*

**Tags:** Combat, Movement, Defensive
**Prerequisites:** Dex 17, Dodge, Wind Stance, base attack bonus +11
**Source:** Core Rulebook (PZO1110) p. 114, 130
**Foundry id:** `jbvXxHpu7BVbCpwr`

> *The speed at which you move makes it nearly impossible for opponents to strike you.*
>
> **Prerequisites**: Dex 17, Dodge, Wind Stance, base attack bonus +11.
>
> **Benefits**: If you take two actions to move or a withdraw action in a turn, you gain 50% concealment for 1 round.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `lightning_stance` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Lingering Performance
*(feat)*

**Tags:** —
**Prerequisites:** Bardic performance class feature
**Source:** —
**Foundry id:** `F2GJXemdlPolvx4D`

> *The effects of your bardic performance carry on, even after you have stopped performing.*
>
> **Prerequisites**: Bardic performance class feature.
>
> **Benefit**: The bonuses and penalties from your bardic performance continue for 2 rounds after you cease performing. Any other requirement, such as range or specific conditions, must still be met for the effect to continue. If you begin a new bardic performance during this time, the effects of the previous performance immediately cease.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `lingering_performance` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Lunge
*(feat)*

**Tags:** Combat, Offensive
**Prerequisites:** Base attack bonus +6
**Source:** Core Rulebook (PZO1110) p. 115, 130
**Foundry id:** `xq2TFr7bsYBBHOi5`

> *You can strike foes that would normally be out of reach.*
>
> **Prerequisites**: Base attack bonus +6.
>
> **Benefits**: You can increase the reach of your melee attacks by 5 feet until the end of your turn by taking a -2 penalty to your AC until your next turn. You must decide to use this ability before any attacks are made.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `lunge` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Magical Aptitude
*(feat)*

**Tags:** General
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 115, 130
**Foundry id:** `CLSsMyNmdcNAOUKC`

> *You are skilled at spellcasting and using magic items.*
>
> **Benefits**: You get a +2 bonus on all Spellcraft checks and Use Magic Device checks. If you have 10 or more ranks in one of these skills, the bonus increases to +4 for that skill.

**Mechanical encoding:** `changes`: 2
  - `2 + if(gte(@skills.umd.rank, 10), 2)` → `skill.umd`  (untyped)
  - `2 + if(gte(@skills.spl.rank, 10), 2)` → `skill.spl`  (untyped)

**In our coverage tracker:** absent (slug `magical_aptitude` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Magical Tail
*(feat)*

**Tags:** General, Kitsune
**Prerequisites:** Kitsune
**Source:** Ultimate Combat (PZO1121) p. 193
**Foundry id:** `fnAVlh0TXLt5XbNJ`

> *You grow an extra tail that represents your growing magical powers.*
>
> **Prerequisites**: Kitsune.
>
> **Benefit**: You gain a new spell-like ability, each usable twice per day, from the following list, in order: disguise self, charm person, misdirection, invisibility, suggestion, displacement, confusion, dominate person.
>
> For example, the first time you select this feat, you gain disguise self 2/day; the second time you select this feat, you gain charm person 2/day. Your caster level for these spells is equal to your Hit Dice. The DCs for these abilities are Charisma-based.
>
> **Special**: You may select this feat up to eight times. Each time you take it, you gain an additional ability as described above.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `magical_tail` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Manyshot
*(feat)*

**Tags:** Combat, Ranged, Weapon, Offensive
**Prerequisites:** Dex 17, Point-Blank Shot, Rapid Shot, base attack bonus +6
**Source:** Core Rulebook (PZO1110) p. 116, 130
**Foundry id:** `w23dO02t0poRrno0`

> *You can fire multiple arrows at a single target.*
>
> **Prerequisites**: Dex 17, Point-Blank Shot, Rapid Shot, base attack bonus +6.
>
> **Benefits**: When making a full-attack action with a bow, your first attack fires two arrows. If the attack hits, both arrows hit. Apply precision-based damage (such as sneak attack) and critical hit damage only once for this attack. Damage bonuses from using a composite bow with a high Strength bonus apply to each arrow, as do other damage bonuses, such as a ranger's favored enemy bonus. Damage reduction and resistances apply separately to each arrow.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `manyshot` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Martial Dominance
*(feat)*

**Tags:** Combat
**Prerequisites:** Base attack bonus +5, Intimidate 1 rank
**Source:** PZO1134 (PZO1134) p. 86
**Foundry id:** `gGx5DrPAWiFc0WOt`

> *Your skill at arms intimidates your foes.*
>
> **Prerequisites**: Base attack bonus +5, Intimidate 1 rank.
>
> **Benefits**: You can use your base attack bonus in place of your ranks in Intimidate to determine your Intimidate skill bonus. When you confirm a critical hit against a creature, you can attempt an Intimidate check to demoralize that creature as an immediate action.

**Mechanical encoding:** `changes`: 1, has `actions`
  - `max(@attributes.bab.total - @skill.int.rank, 0)` → `skill.int`  (untyped)

**In our coverage tracker:** absent (slug `martial_dominance` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Martial Weapon Proficiency
*(feat)*

**Tags:** Combat, Weapon, Proficiency
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 115, 130
**Foundry id:** `IPfsLy9sWXF6IBP1`

> *Choose a type of martial weapon. You understand how to use that type of martial weapon in combat.*
>
> **Benefits**: You make attack rolls with the selected weapon normally (without the non-proficient penalty).
>
> **Normal**: When using a weapon with which you are not proficient, you take a -4 penalty on attack rolls.
>
> **Special**: Barbarians, fighters, paladins, and rangers are proficient with all martial weapons. They need not select this feat.
>
> You can gain Martial Weapon Proficiency multiple times. Each time you take the feat, it applies to a new type of weapon.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `martial_weapon_proficiency` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Master Craftsman
*(feat)*

**Tags:** General, Skill, Item Creation
**Prerequisites:** 5 ranks in any Craft or Profession skill
**Source:** Core Rulebook (PZO1110) p. 115, 130
**Foundry id:** `6hmIs98sJoJzzIq0`

> *Your superior crafting skills allow you to create simple magic items.*
>
> **Prerequisites**: 5 ranks in any Craft or Profession skill.
>
> **Benefits**: Choose one Craft or Profession skill in which you possess at least 5 ranks. You receive a +2 bonus on your chosen Craft or Profession skill. Ranks in your chosen skill count as your caster level for the purposes of qualifying for the Craft Magic Arms and Armor and Craft Wondrous Item feats. You can create magic items using these feats, substituting your ranks in the chosen skill for your total caster level. You must use the chosen skill for the check to create the item. The DC to create the item still increases for any necessary spell requirements (see the magic item creation rules in Magic Items). You cannot use this feat to create any spell-trigger or spell-activation item.
>
> **Normal**: Only spellcasters can qualify for the Craft Magic Arms and Armor and Craft Wondrous Item feats.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `master_craftsman` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Maximize Spell
*(feat)*

**Tags:** Metamagic, Magic
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 117, 130
**Foundry id:** `J1yi4hFKYdXqZE3h`

> *Your spells have the maximum possible effect.*
>
> **Benefits**: All variable, numeric effects of a spell modified by this feat are maximized. Saving throws and opposed rolls are not affected, nor are spells without random variables. A maximized spell uses up a spell slot three levels higher than the spell's actual level.
>
> An empowered, maximized spell gains the separate benefits of each feat: the maximum result plus half the normally rolled result.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `maximize_spell` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Medusa's Wrath
*(feat)*

**Tags:** Combat, Unarmed, Offensive
**Prerequisites:** Improved Unarmed Strike, Gorgon's Fist, Scorpion Style, base attack bonus +11
**Source:** Core Rulebook (PZO1110) p. 115, 130
**Foundry id:** `sOCyCmNxe2MBbEaI`

> *You can take advantage of your opponent's confusion, delivering multiple blows.*
>
> **Prerequisites**: Improved Unarmed Strike, Gorgon's Fist, Scorpion Style, base attack bonus +11.
>
> **Benefits**: Whenever you use the full-attack action and make at least one unarmed strike, you can make two additional unarmed strikes at your highest base attack bonus. These bonus attacks must be made against a dazed, flat-footed, paralyzed, staggered, stunned, or unconscious foe.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `medusa_s_wrath` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Misdirection Attack
*(feat)*

**Tags:** Combat
**Prerequisites:** Int 13, Combat Expertise, Deceitful, Misdirection Redirection, Misdirection Tactics, Bluff 10 ranks
**Source:** PZO1134 (PZO1134) p. 87
**Foundry id:** `VtTtf8P02AhoumaB`

> *After misdirecting your opponent's weapon attack, you leave your opponent open to further violence.*
>
> **Prerequisites**: Int 13, Combat Expertise, Deceitful, Misdirection Redirection, Misdirection Tactics, Bluff 10 ranks.
>
> **Benefits**: When you successfully use the Misdirection Tactics feat to negate a melee weapon attack, the opponent whose attack you negated provokes an attack of opportunity from you, even though you normally can't take attacks of opportunity while using the total defense action. This effect is in addition to the effect gained from Misdirection Redirection.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `misdirection_attack` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Misdirection Redirection
*(feat)*

**Tags:** Combat
**Prerequisites:** Int 13, Combat Expertise, Misdirection Tactics, Deceitful, Bluff 10 ranks
**Source:** PZO1134 (PZO1134) p. 87
**Foundry id:** `6RmcdXzrNGEWDT0h`

> *After misdirecting your opponent's weapon attack, you trick it into striking someone else.*
>
> **Prerequisites**: Int 13, Combat Expertise, Misdirection Tactics, Deceitful, Bluff 10 ranks.
>
> **Benefits**: When you successfully use the Misdirection Tactics feat to negate a melee weapon attack, you redirect your foe's attack and trick your foe into striking another creature of your choice within the foe's melee reach. To resolve this attack, your foe must make a new attack roll against the new target.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `misdirection_redirection` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Misdirection Tactics
*(feat)*

**Tags:** Combat
**Prerequisites:** Int 13, Combat Expertise, Deceitful, Bluff 4 ranks
**Source:** PZO1134 (PZO1134) p. 87
**Foundry id:** `lcsiFYTpkBpIGeeF`

> *You have learned to use deception and trickery to misdirect your opponent's weapon attack.*
>
> **Prerequisites**: Int 13, Combat Expertise, Deceitful, Bluff 4 ranks.
>
> **Benefits**: While you are using the total defense action, if a melee attack would still hit your AC, you can attempt a Bluff check with a DC equal to the foe's attack roll as an immediate action. If you succeed at the check, you negate the attack (treat it as a miss). If the attack still hits, you cannot use this feat against the same opponent for 24 hours.

**Mechanical encoding:** has `actions`, has `scriptCalls`

**In our coverage tracker:** absent (slug `misdirection_tactics` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mobility
*(feat)*

**Tags:** Combat, Movement, Defensive
**Prerequisites:** Dex 13, Dodge
**Source:** Core Rulebook (PZO1110) p. 114, 130
**Foundry id:** `R7L4SlGRlnThqFrP`

> *You can easily move through a dangerous melee.*
>
> **Prerequisites**: Dex 13, Dodge.
>
> **Benefits**: You get a +4 dodge bonus to Armor Class against attacks of opportunity caused when you move out of or within a threatened area. A condition that makes you lose your Dexterity bonus to Armor Class (if any) also makes you lose dodge bonuses.
>
> Dodge bonuses stack with each other, unlike most types of bonuses.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `mobility` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Monastic Legacy
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Still mind class feature, Improved Unarmed Strike
**Source:** Advanced Race Guide (PZO1131) p. 127; Bestiary (PZO1118) p. 109
**Foundry id:** `lrm4C05AtgTksHYU`

> *Your formal unarmed training continues to bolster your training in other areas.*
>
> **Prerequisites**: Still mind class feature, Improved Unarmed Strike.
>
> **Benefits**: Add half the levels you have in classes other than monk to your monk level to determine your effective monk level for your base unarmed strike damage. This feat does not make levels in classes other than monk count toward any other monk class features.
>
> ##### Combat Trick
>
> At the start of your turn, you can spend 5 stamina points to use your full character level to determine your effective monk level for your unarmed strike damage. This increase lasts until the start of your next turn.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `monastic_legacy` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Monstrous Crafter
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Craft Wondrous Item, Grisly Ornament, Harvest Parts
**Source:** PZO9478 (PZO9478) p. 24
**Foundry id:** `laMCsQj0tA1t0eWr`

> *You can weave pieces of beasts into your magic items.*
>
> **Prerequisites**: Craft Wondrous Item, Grisly Ornament, Harvest Parts.
>
> **Benefit**: Whenever you use the Grisly Ornament feat, you are able to permanently integrate one ornament you have crafted using the harvested creature parts into a wondrous item. The ornament grants no ongoing benefits, but once per day you can activate an integrated ornament as a free action to gain its full benefits for 1 minute. You can integrate an ornament into a wondrous item (or replace an item’s existing ornament) by spending 8 hours of work and 100 gp × the creature’s CR.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `monstrous_crafter` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mounted Archery
*(feat)*

**Tags:** Combat, Mount, Ranged, Offensive, Weapon
**Prerequisites:** Ride 1 rank, Mounted Combat
**Source:** Core Rulebook (PZO1110) p. 115, 131
**Foundry id:** `rp9HV7wYcMb333si`

> *You are skilled at making ranged attacks while mounted.*
>
> **Prerequisites**: Ride 1 rank, Mounted Combat.
>
> **Benefits**: The penalty you take when using a ranged weapon while mounted is halved: -2 instead of -4 if your mount is taking a double move, and -4 instead of -8 if your mount is running.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `mounted_archery` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mounted Combat
*(feat)*

**Tags:** Combat, Defensive, Mount
**Prerequisites:** Ride 1 rank
**Source:** Core Rulebook (PZO1110) p. 115, 131
**Foundry id:** `0spsP9ylE3goD3jc`

> *You are adept at guiding your mount through combat.*
>
> **Prerequisites**: Ride 1 rank.
>
> **Benefits**: Once per round when your mount is hit in combat, you may attempt a Ride check (as an immediate action) to negate the hit. The hit is negated if your Ride check result is greater than the opponent's attack roll.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `mounted_combat` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mounted Shield
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Mounted Combat, Shield Focus
**Source:** Advanced Race Guide (PZO1131) p. 127; Advanced Player's Guide (PZO1115) p. 165
**Foundry id:** `zrxZvMHYH2QHKH8f`

> *Your defensive tactics defend both you and your mount.*
>
> **Prerequisites**: Mounted Combat, Shield Focus.
>
> **Benefits**: You may add your base shield bonus (including the bonus from Shield Focus but not including enhancement bonuses) to your mount's AC. In addition, you may add this bonus when making a Ride check to negate a hit against your mount using the Mounted Combat feat.
>
> ##### Combat Trick
>
> As long as you have at least 1 stamina point in your stamina pool, you can add your shield's enhancement bonus to your mount's Armor Class.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `mounted_shield` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Mounted Skirmisher
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Ride rank 14, Mounted Combat, Trick Riding
**Source:** Advanced Race Guide (PZO1131) p. 127; Advanced Player's Guide (PZO1115) p. 165
**Foundry id:** `N2utLmu8WBxNWo5y`

> *You are adept at attacking from upon a swift moving steed.*
>
> **Prerequisites**: Ride rank 14, Mounted Combat, Trick Riding.
>
> **Benefits**: If your mount moves its speed or less, you can still take a full-attack action.
>
> **Normal**: If your mount moves more than 5 feet, you can only take an attack action.
>
> ##### Combat Trick
>
> When your mount moves its speed or less, you can spend 5 stamina points to spur it on 10 additional feet. This is bonus movement, and you can still make a full attack when your mount takes this bonus movement.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `mounted_skirmisher` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Multiattack
*(feat)*

**Tags:** Combat, Monster
**Prerequisites:** Three or more natural attacks
**Source:** PZO1112 (PZO1112) p. 315
**Foundry id:** `RmhtvELGu73iR8yh`

> *This creature is particularly skilled at making attacks with its natural weapons.*
>
> **Prerequisites**: Three or more natural attacks.
>
> **Benefits**: The creature's secondary attacks with natural weapons take only a -2 penalty.
>
> **Normal**: Without this feat, the creature’s secondary attacks with natural weapons take a –5 penalty.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `multiattack` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Multiweapon Fighting
*(feat)*

**Tags:** Combat, Monster
**Prerequisites:** Dex 13, three or more hands
**Source:** PZO1112 (PZO1112) p. 315
**Foundry id:** `vhN413T0ASvOxBL1`

> This multi-armed creature is skilled at making attacks with multiple weapons.
>
> **Prerequisites**: Dex 13, three or more hands.
>
> **Benefit**: Penalties for fighting with multiple weapons are reduced by –2 with the primary hand and by –6 with off hands.
>
> **Normal**: A creature without this feat takes a –6 penalty on attacks made with its primary hand and a –10 penalty on attacks made with all of its off hands. (It has one primary hand, and all the others are off hands.) See @UUID[Compendium.pf1.feats.Item.Ee7JHADKEK37tTHs].
>
> **Special**: This feat replaces the Two-Weapon Fighting feat for creatures with more than two arms.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `multiweapon_fighting` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Natural Spell
*(feat)*

**Tags:** General, Magic
**Prerequisites:** Wis 13, wild shape class feature
**Source:** Core Rulebook (PZO1110) p. 115, 131
**Foundry id:** `JUBqOpBA3agQwNvu`

> *You can cast spells even while in a form that cannot normally cast spells.*
>
> **Prerequisites**: Wis 13, wild shape class feature.
>
> **Benefits**: You can complete the verbal and somatic components of spells while using wild shape. You substitute various noises and gestures for the normal verbal and somatic components of a spell.
>
> You can also use any material components or focuses you possess, even if such items are melded within your current form. This feat does not permit the use of magic items while you are in a form that could not ordinarily use them, and you do not gain the ability to speak while using wild shape.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `natural_spell` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Nimble Moves
*(feat)*

**Tags:** General, Movement
**Prerequisites:** Dex 13
**Source:** Core Rulebook (PZO1110) p. 115, 131
**Foundry id:** `VMVAqGze4cs3naya`

> *You can move across a single obstacle with ease.*
>
> **Prerequisites**: Dex 13.
>
> **Benefits**: Whenever you move, you may move through 5 feet of difficult terrain each round as if it were normal terrain. This feat allows you to take a 5-foot step into difficult terrain.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `nimble_moves` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Opening Volley
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** —
**Source:** Advanced Race Guide (PZO1131) p. 127-128; Bestiary (PZO1118) p. 112
**Foundry id:** `IsGNUF8XmxwTkxmI`

> *Your ranged assault leaves your foe disoriented and vulnerable to your melee attack.*
>
> **Benefits**: Whenever you deal damage with a ranged attack, you gain a +4 circumstance bonus on the next melee attack roll you make against the opponent. This attack must occur before the end of your next turn.
>
> ##### Combat Trick
>
> When you deal damage with a ranged attack, you can spend 2 stamina points to gain a +4 circumstance bonus on the next two melee attack rolls you make against that opponent until the end of your next turn, instead of on only the next melee attack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `opening_volley` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Outflank
*(feat)*

**Tags:** Combat, Teamwork, Combat Trick
**Prerequisites:** Base attack bonus +4
**Source:** Advanced Player's Guide (PZO1115) p. 165
**Foundry id:** `ln2Dhw97Fol1BCxU`

> *You look for every edge when flanking an enemy.*
>
> **Prerequisites**: Base attack bonus +4.
>
> **Benefit**: Whenever you and an ally who also has this feat are flanking the same creature, your flanking bonus on attack rolls increases to +4. In addition, whenever you score a critical hit against the flanked creature, it provokes an attack of opportunity from your ally.
>
> ##### Combat Trick
>
> When you threaten but fail to confirm a critical hit against a creature you are flanking, you can spend 5 stamina points. If you do, that creature provokes an attack of opportunity from each ally with this feat who is flanking the creature, even though you didn’t confirm the critical hit. You still can’t use this ability against targets immune to critical hits.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `outflank` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Pack Attack
*(feat)*

**Tags:** Combat, Teamwork
**Prerequisites:** Base attack bonus +1
**Source:** Bestiary (PZO1118) p. 118
**Foundry id:** `XfdKpTa4w1wuhJKU`

> *You are skilled at surrounding your enemies.*
>
> **Prerequisites**: Base attack bonus +1.
>
> **Benefit**: When you are adjacent to an ally with this feat, the first time you melee attack an opponent, you can spend an immediate action to take a 5-foot step, even if you have otherwise moved this round.
>
> **Normal**: You can take a 5-foot step only if you have not otherwise moved in a round.
> Combat Trick
>
> When you are adjacent to an ally that also has this feat, you can spend 2 stamina points to take a 5-foot step as a free action instead of an immediate action. You can still use this feat’s ability only once per round.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `pack_attack` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Painful Collision
*(feat)*

**Tags:** Combat
**Prerequisites:** Str 13, Improved Bull Rush, Power Attack
**Source:** PZO9493 (PZO9493) p. 24
**Foundry id:** `VPruDiNTrlRVlJRA`

> *You shove your opponents into each other, causing painful and damaging collisions.*
>
> **Prerequisites**: Str 13, Improved Bull Rush, Power Attack.
>
> **Benefit**: When you bull rush an enemy into another creature, both creatures take 1d6 points of bludgeoning damage, plus an additional 1d6 points of bludgeoning damage for every 5 feet your original target has moved as a result of your bull rush. For instance, if you successfully bull rush a goblin 10 feet and it then collides with another goblin, both creatures would take 3d6 points of bludgeoning damage.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `painful_collision` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Paired Opportunists
*(feat)*

**Tags:** Combat, Teamwork, Combat Trick
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 166
**Foundry id:** `yW1RFRSh4Ma2uYc9`

> *You know how to make an enemy pay for lax defenses.*
>
> **Benefit**: Whenever you are adjacent to an ally who also has this feat, you receive a +4 circumstance bonus on attacks of opportunity against creatures that you both threaten. Enemies that provoke attacks of opportunity from your ally also provoke attacks of opportunity from you so long as you threaten them (even if the situation or an ability would normally deny you the attack of opportunity). This does not allow you to take more than one attack of opportunity against a creature for a given action.
>
> ##### Combat Trick
>
> As long as an ally that also has this feat is within your melee reach, you can spend 2 stamina points to gain this feat’s benefits until the end of your next turn.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `paired_opportunists` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Passing Trick
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Int 13, Combat Expertise, Dodge, Improved Feint, Mobility, size Small or smaller
**Source:** Advanced Race Guide (PZO1131) p. 128; Bestiary (PZO1118) p. 112
**Foundry id:** `tZEAN61G7WEFHD4J`

> *Slipping past a foe gives you the chance to feint.*
>
> **Prerequisites**: Int 13, Combat Expertise, Dodge, Improved Feint, Mobility, size Small or smaller.
>
> **Benefits**: Whenever you make a successful Acrobatics check to move through an opponent's space, you can spend a swift action to make a Bluff check against that opponent to feint in combat.
>
> **Special**: If you have the Underfoot feat and the opponent is larger than you, you gain a +2 bonus on the Bluff check this feat allows.
>
> ##### Combat Trick
>
> You can spend 5 stamina points to attempt a Bluff check as a free action instead of a swift action when using this feat.

**Mechanical encoding:** has `actions`, has `scriptCalls`

**In our coverage tracker:** absent (slug `passing_trick` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Penetrating Strike
*(feat)*

**Tags:** Combat, Offensive
**Prerequisites:** Weapon Focus, base attack bonus +1, 12th-level fighter, proficiency with weapon
**Source:** Core Rulebook (PZO1110) p. 117, 131
**Foundry id:** `TGmNCGtnHf0icozK`

> *Your attacks are capable of penetrating the defenses of some creatures.*
>
> **Prerequisites**: Weapon Focus, base attack bonus +1, 12th-level fighter, proficiency with weapon.
>
> **Benefits**: Your attacks with weapons selected with Weapon Focus ignore up to 5 points of damage reduction. This feat does not apply to damage reduction without a type (such as DR 10/ — ).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `penetrating_strike` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Persuasive
*(feat)*

**Tags:** General, Skill
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 115, 131
**Foundry id:** `L10V7jTzmMYz62zz`

> *You are skilled at swaying attitudes and intimidating others into your way of thinking.*
>
> **Benefits**: You get a +2 bonus on Diplomacy and Intimidate skill checks. If you have 10 or more ranks in one of these skills, the bonus increases to +4 for that skill.

**Mechanical encoding:** `changes`: 2
  - `2 + if(gte(@skills.dip.rank, 10), 2)` → `skill.dip`  (untyped)
  - `2 + if(gte(@skills.int.rank, 10), 2)` → `skill.int`  (untyped)

**In our coverage tracker:** `IMPLEMENTED` — +2 diplomacy/intimidate
**Manual verdict:** `[ ]`
**Notes:**

---

### Pin Down
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Combat Reflexes, fighter level 11th
**Source:** Advanced Race Guide (PZO1131) p. 129; Bestiary (PZO1118) p. 113
**Foundry id:** `JYp3KC5jVI9sgsSL`

> *You easily block enemy escapes.*
>
> **Prerequisites**: Combat Reflexes, fighter level 11th.
>
> **Benefits**: Whenever an opponent you threaten takes a 5-foot step or uses the withdraw action, that opponent provokes an attack of opportunity from you. If the attack hits, you deal no damage, but the targeted creature is prevented from making the move action that granted a 5-foot step or the withdraw action and does not move.
>
> ##### Combat Trick
>
> When using this feat, you can spend 5 stamina points to gain its benefits and still deal damage with the attack of opportunity.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `pin_down` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Pinning Knockout
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Dex 13, Greater Grapple, Improved Grapple, Improved Unarmed Strike, base attack bonus +9 or monk level 9th
**Source:** Advanced Race Guide (PZO1131) p. 129; Bestiary (PZO1118) p. 113
**Foundry id:** `QSMKp6riDytO2ajn`

> *An opponent you have pinned is easy for you to knock out.*
>
> **Prerequisites**: Dex 13, Greater Grapple, Improved Grapple, Improved Unarmed Strike, base attack bonus +9 or monk level 9th.
>
> **Benefits**: While you have an opponent pinned, when you succeed at a grapple combat maneuver check to deal an opponent nonlethal damage using an unarmed strike or a light or one-handed weapon, double your damage result. Any creature that is immune to critical hits is immune to the effects of this feat.
>
> ##### Combat Trick
>
> When using an unarmed strike or a light or one-handed weapon to deal nonlethal damage to a pinned opponent with this feat, you can spend 5 stamina points to triple the damage instead of doubling it.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `pinning_knockout` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Pinpoint Targeting
*(feat)*

**Tags:** Combat, Ranged, Offensive, Weapon
**Prerequisites:** Dex 19, Improved Precise Shot, Point-Blank Shot, Precise Shot, base attack bonus +16
**Source:** Core Rulebook (PZO1110) p. 116, 131
**Foundry id:** `ztV5oURW9cFsLdXT`

> *You can target the weak points in your opponent's armor.*
>
> **Prerequisites**: Dex 19, Improved Precise Shot, Point-Blank Shot, Precise Shot, base attack bonus +16.
>
> **Benefits**: As a standard action, make a single ranged attack. The target does not gain any armor, natural armor, or shield bonuses to its Armor Class. You do not gain the benefit of this feat if you move this round.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `pinpoint_targeting` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Piranha Strike
*(feat)*

**Tags:** —
**Prerequisites:** Weapon Finesse, base attack bonus +1
**Source:** —
**Foundry id:** `5xhMBEM8iB0xrE3X`

> *You make a combination of quick strikes, sacrificing accuracy for multiple, minor wounds that prove exceptionally deadly.*
>
> **Prerequisites**: Weapon Finesse, base attack bonus +1.
>
> **Benefit**: When wielding a light weapon, you can choose to take a –1 penalty on all melee attack rolls and combat maneuver checks to gain a +2 bonus on all melee damage rolls. This bonus to damage is halved (–50%) if you are making an attack with an off-hand weapon or secondary natural weapon. When your base attack bonus reaches +4, and for every 4 points thereafter, the penalty increases by –1 and the bonus on damage rolls increases by +2. You must choose to use this feat before the attack roll, and its effects last until your next turn. The bonus damage does not apply to touch attacks or effects that do not deal hit point damage. This feat cannot be used in conjunction with the Power Attack feat.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `piranha_strike` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Point-Blank Shot
*(feat)*

**Tags:** Combat
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 116, 131
**Foundry id:** `8rsFtye3PwM6CKli`

> *You are especially accurate when making ranged attacks against close targets.*
>
> **Benefits**: You get a +1 bonus on attack and damage rolls with ranged weapons at ranges of up to 30 feet.
>
> **Combat Trick**
> You can spend up to 6 stamina points to increase this feat's range by 5 feet for each stamina point you spent.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `IMPLEMENTED` — +1 attack/damage with ranged
**Manual verdict:** `[ ]`
**Notes:**

---

### Power Attack
*(feat)*

**Tags:** Combat, Offensive
**Prerequisites:** Str 13, base attack bonus +1
**Source:** Core Rulebook (PZO1110) p. 116, 131
**Foundry id:** `FUW5mIXHNBBIQ1Sq`

> *You can make exceptionally deadly melee attacks by sacrificing accuracy for strength.*
>
> **Prerequisites**: Str 13, base attack bonus +1.
>
> **Benefits**: You can choose to take a -1 penalty on all melee attack rolls and combat maneuver checks to gain a +2 bonus on all melee damage rolls. This bonus to damage is increased by half (+50%) if you are making an attack with a two-handed weapon, a one handed weapon using two hands, or a primary natural weapon that adds 1-1/2 times your Strength modifier on damage rolls. This bonus to damage is halved (-50%) if you are making an attack with an off-hand weapon or secondary natural weapon. When your base attack bonus reaches +4, and every 4 points thereafter, the penalty increases by -1 and the bonus to damage increases by +2. You must choose to use this feat before making an attack roll, and its effects last until your next turn. The bonus damage does not apply to touch attacks or effects that do not deal hit point damage.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `IMPLEMENTED` — attack-time tradeoff; wield-scaled damage bonus
**Manual verdict:** `[ ]`
**Notes:**

---

### Precise Shot
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Point-Blank Shot
**Source:** Core Rulebook (PZO1110) p. 116, 131
**Foundry id:** `53urYIbYYpQuoSLd`

> *You are adept at firing ranged attacks into melee.*
>
> **Prerequisites**: Point-Blank Shot.
>
> **Benefits**: You can shoot or throw ranged weapons at an opponent engaged in melee without taking the standard -4 penalty on your attack roll.
>
> ##### Combat Trick
>
> As a standard action, you can spend 2 stamina points and make a ranged attack against a foe engaged in melee with an ally. If the attack hits, it deals no damage, but your ally gains your choice of either a +2 bonus on her next attack roll against that opponent or a +2 bonus to AC against that opponent's next attack. This bonus lasts until the start of your next turn.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `NOT_IMPLEMENTED` — no -4 firing into melee
**Manual verdict:** `[ ]`
**Notes:**

---

### Precise Strike
*(feat)*

**Tags:** Combat, Teamwork, Combat Trick
**Prerequisites:** Dex 13, base attack bonus +1
**Source:** Advanced Player's Guide (PZO1115) p. 167
**Foundry id:** `NdrNsfFKYGy3VXDF`

> *You are skilled at striking where it counts, as long as an ally distracts your foe.*
>
> **Prerequisites**: Dex 13, base attack bonus +1.
>
> **Benefit**: Whenever you and an ally who also has this feat are flanking the same the creature, you deal an additional 1d6 points of precision damage with each successful melee attack. This bonus damage stacks with other sources of precision damage, such as sneak attack. This bonus damage is not multiplied on a critical hit.
>
> #### Combat Trick
>
> When dealing precision damage with this feat, you can spend 2 stamina points to increase that precision damage to 2d6.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `precise_strike` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Pressure Adept
*(feat)*

**Tags:** General
**Prerequisites:** Swim 5 ranks
**Source:** PZO92102 (PZO92102) p. 58
**Foundry id:** `Bl0fVCqJaXS7tXvn`

> *You've spent so much time at unusual pressures that you've extended your native range beyond the norms of your species.*
>
> **Prerequisites**: Swim 5 ranks.
>
> **Benefits**: Add one oceanic zone to your native range when calculating pressure (meaning that you don't take pressure damage in that range unless instantaneously transported up or down, and even then you adapt to the change all at once rather than 100 feet at a time). Surfacedwellers taking this feat must select the sunlight zone, and aquatic creatures can select any zone either directly above or directly below their native range.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `pressure_adept` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Psychic Sensitivity
*(feat)*

**Tags:** General
**Prerequisites:** —
**Source:** Bestiary 4 (PZO1132) p. 138
**Foundry id:** `3owNW4QoIZK6Pwm5`

> *You unlock the secrets of the occult world.*
>
> **Benefit**: You gain access to *occult skill unlocks* for any skills in which you have ranks. If you have no ranks in the appropriate skill, you can’t use the occult skill unlock, even if that skill can be used untrained.
>
> **Normal**: You must have the ability to cast psychic spells in order to use occult skill unlocks.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `psychic_sensitivity` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Pushing Assault
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Str 15, Power Attack, base attack bonus +1
**Source:** Advanced Race Guide (PZO1131) p. 129; Advanced Player's Guide (PZO1115) p. 167
**Foundry id:** `MpecI8kzg7WFzwwS`

> *A strike made with a two-handed weapon can push a similar sized opponent backward.*
>
> **Prerequisites**: Str 15, Power Attack, base attack bonus +1.
>
> **Benefits**: When you hit a creature your size or smaller with a two-handed weapon attack modified by the Power Attack feat, you can choose to push the target 5 feet directly away from you instead of dealing the extra damage from Power Attack. If you score a critical hit, you can instead push the target 10 feet directly away from you. This movement does not provoke attacks of opportunities, and the target must end this move in a safe space it can stand in. You choose which effect to apply after the attack roll has been made, but before the damage is rolled.
>
> ##### Combat Trick
>
> You can spend 5 stamina points to gain the effects of this feat and still deal the extra damage from Power Attack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `pushing_assault` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Quick Dirty Trick
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Int 13, Combat Expertise, Improved Dirty Trick, base attack bonus +6
**Source:** Advanced Race Guide (PZO1131) p. 129; Bestiary (PZO1118) p. 114
**Foundry id:** `MCHLkpm99e5wbTbB`

> *You can perpetrate a dirty trick and deliver an attack before your opponent is the wiser.*
>
> **Prerequisites**: Int 13, Combat Expertise, Improved Dirty Trick, base attack bonus +6.
>
> **Benefits**: On your turn, you can perform a single dirty trick combat maneuver (Dirty Trick) in place of one of your melee attacks. You must choose the melee attack with the highest base attack bonus to make the dirty trick combat maneuver.
>
> **Normal**: A dirty trick combat maneuver is a standard action.
>
> ##### Combat Trick
>
> You can select this feat even if you don't meet the ability score prerequisite (Intelligence 13). You gain the benefits of this feat only as long as you have at least 1 stamina point in your stamina pool. You can spend 2 stamina points to change an attack that does not have your highest base attack bonus into a dirty trick combat maneuver. You can use this combat trick only once per round, but you can use it even if you already used your attack at the highest base attack bonus for a dirty trick.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `quick_dirty_trick` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Quick Draw
*(feat)*

**Tags:** Combat, Weapon
**Prerequisites:** Base attack bonus +1
**Source:** Core Rulebook (PZO1110) p. 116, 131-132
**Foundry id:** `WKIVfdosc5SqYzmP`

> *You can draw weapons faster than most.*
>
> **Prerequisites**: Base attack bonus +1.
>
> **Benefits**: You can draw a weapon as a free action instead of as a move action. You can draw a hidden weapon (see the Sleight of Hand skill) as a move action.
>
> A character who has selected this feat may throw weapons at his full normal rate of attacks (much like a character with a bow).
>
> Alchemical items, potions, scrolls, and wands cannot be drawn quickly using this feat.
>
> **Normal**: Without this feat, you may draw a weapon as a move action, or (if your base attack bonus is +1 or higher) as a free action as part of movement. Without this feat, you can draw a hidden weapon as a standard action.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `quick_draw` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Quick Steal
*(feat)*

**Tags:** Combat, Combat Trick, Combat Maneuver
**Prerequisites:** Int 13, Combat Expertise, Improved Steal, base attack bonus +6
**Source:** Bestiary (PZO1118) p. 114; Advanced Race Guide (PZO1131) p. 130
**Foundry id:** `f8BDCG8XvJlfGfFG`

> *You are adept at relieving foes of their belongings even while you strike.*
>
> **Prerequisites**: Int 13, Combat Expertise, Improved Steal, base attack bonus +6.
>
> **Benefits**: On your turn, you can perform a single steal combat maneuver (Steal) in place of one of your melee attacks. You must choose the melee attack with the highest base attack bonus to make the steal.
>
> **Normal**: A steal combat maneuver is a standard action.
>
> ##### Combat Trick
>
> You can select this feat even if you don't meet the ability score prerequisite (Intelligence 13). You gain the benefit of this feat only as long as you have at least 1 stamina point in your stamina pool. You can spend 2 stamina points to change an attack that does not have your highest base attack bonus into a steal combat maneuver. You can use this combat trick only once per round, but you can use it even if you already used your attack at the highest base attack bonus to steal.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `quick_steal` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Quick Stow
*(feat)*

**Tags:** Combat
**Prerequisites:** Quick Draw, base attack bonus +1
**Source:** —
**Foundry id:** `QQE5EGIh7KDABnv2`

> *You effortlessly stow items and sheathe weapons.*
>
> **Prerequisites**: Quick Draw, base attack bonus +1.
>
> **Benefits**: You do not provoke an attack of opportunity when sheathing a weapon, and you can combine a move action to sheathe a weapon with a regular move action. (You can both stow and draw a weapon as part of the same move action in this way.) If you have the Two-Weapon Fighting feat, you can sheathe two light or one-handed weapons in the time it would normally take to sheathe one.
>
> You can also quickly stow items in a backpack or other container that you are wearing or carrying. When you successfully use an action to pick up an item (including when you steal an item with a successful Sleight of Hand check or steal combat maneuver check), you can stow the item as part of the same action used to acquire it. You can try to hide this object by attempting a Sleight of Hand check with a -20 penalty, opposed by the Perception check results of all opponents.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `quick_stow` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Quicken Spell-Like Ability
*(feat)*

**Tags:** Monster
**Prerequisites:** Spell-like ability at CL 10th or higher
**Source:** PZO1112 (PZO1112) p. 315
**Foundry id:** `P4tmHYQVGowcstjO`

> *This creature can use one of its spell-like abilities with next to no effort.*
>
> **Prerequisites**: Spell-like ability at CL 10th or higher.
>
> **Benefits**: Choose one of the creature's spell-like abilities, subject to the restrictions described in this feat. The creature can use the chosen spell-like ability as a quickened spell-like ability three times per day (or less, if the ability is normally usable only once or twice per day).
>
> Using a quickened spell-like ability is a swift action that does not provoke an attack of opportunity. The creature can perform another action--including the use of another spell-like ability (but not another swift action)--in the same round that it uses a quickened spell-like ability. The creature may use only one quickened spell-like ability per round.
>
> The creature can only select a spell-like ability duplicating a spell with a level less than or equal to 1/2 its caster level (round down) - 4. For a summary, see the table below.
>
> A spell-like ability that duplicates a spell with a casting time greater than 1 full round cannot be quickened.**
>
>
> Spell Level**
>
>
> **Caster Level to Quicken**
>
>
> 0
>
>
> 8th
>
>
> 1st
>
>
> 10th
>
>
> 2nd
>
>
> 12th
>
>
> 3rd
>
>
> 14th
>
>
> 4th
>
>
> 16th
>
>
> 5th
>
>
> 18th
>
>
> 6th
>
>
> 20th
>
>
> 7th
>
>
> --
>
>
> 8th
>
>
> --
>
>
> 9th
>
>
> --
>
>
> **Normal**: The use of a spell-like ability normally requires a standard action (at the very least) and provokes an attack of opportunity.
>
> **Special**: This feat can be taken multiple times. Each time it is taken, the creature can apply it to a different one of its spell-like abilities.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `quicken_spell_like_ability` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Quicken Spell
*(feat)*

**Tags:** Metamagic, Magic
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 117, 132
**Foundry id:** `wFoLrh5FeeqBXsQ8`

> *You can cast spells in a fraction of the normal time.*
>
> **Benefits**: Casting a quickened spell is a swift action. You can perform another action, even casting another spell, in the same round as you cast a quickened spell. A spell whose casting time is more than 1 round or 1 full-round action cannot be quickened.
>
> A quickened spell uses up a spell slot four levels higher than the spell's actual level. Casting a quickened spell doesn't provoke an attack of opportunity.
>
> **Special**: You can apply the effects of this feat to a spell cast spontaneously, so long as it has a casting time that is not more than 1 full-round action, without increasing the spell's casting time.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `quicken_spell` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Ranged Feint
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Base attack bonus +2, Bluff 3 ranks
**Source:** PZO1134 (PZO1134) p. 89
**Foundry id:** `LJgvLlAoX4FHf93G`

> *You can mislead foes about your aim with ranged attacks.*
>
> **Prerequisites**: Base attack bonus +2, Bluff 3 ranks.
>
> **Benefits**: You can feint with a ranged weapon by throwing a thrown weapon or firing one arrow, bolt, bullet, or other piece of ammunition; this feint takes the same action as normal to feint, but depending on your weapon, you might have to reload or draw another weapon afterward. When you successfully use a ranged feint, you deny that enemy its Dexterity bonus to AC against your ranged attacks as well as your melee attacks for the same duration as normal. If your feints normally deny a foe its Dexterity bonus to AC against attacks other than your own, this applies only against others' melee attacks.
>
> **Normal**: You can feint only with a melee weapon, and only against a creature you threaten with that weapon.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `ranged_feint` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Rapid Reload
*(feat)*

**Tags:** Combat, Ranged, Weapon, Offensive
**Prerequisites:** Weapon Proficiency (crossbow type chosen)
**Source:** Core Rulebook (PZO1110) p. 116, 132
**Foundry id:** `11ClnanF4PdEPd9g`

> *Choose a type of crossbow (hand, light, or heavy). You can reload such weapons quickly.*
>
> **Prerequisite**: Weapon Proficiency (crossbow type chosen).
>
> **Benefit**: The time required for you to reload your chosen type of crossbow is reduced to a free action (for a hand or light crossbow) or a move action (for a heavy crossbow). Reloading a crossbow still provokes an attack of opportunity.
>
> If you have selected this feat for hand crossbow or light crossbow, you may fire that weapon as many times in a full-attack action as you could attack if you were using a bow.
>
> **Normal**: A character without this feat needs a move action to reload a hand or light crossbow, or a full-round action to reload a heavy crossbow.
>
> **Special**: You can gain Rapid Reload multiple times. Each time you take the feat, it applies to a new type of crossbow.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `rapid_reload` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Rapid Shot
*(feat)*

**Tags:** Combat, Ranged, Weapon, Offensive
**Prerequisites:** Dex 13, Point-Blank Shot
**Source:** Core Rulebook (PZO1110) p. 116, 132
**Foundry id:** `NABgOSBRECIREaha`

> *You can make an additional ranged attack.*
>
> **Prerequisites**: Dex 13, Point-Blank Shot.
>
> **Benefits**: When making a full-attack action with a ranged weapon, you can fire one additional time this round. All of your attack rolls take a -2 penalty when using Rapid Shot.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `NOT_IMPLEMENTED` — extra ranged attack at -2/-2
**Manual verdict:** `[ ]`
**Notes:**

---

### Reach Spell
*(feat)*

**Tags:** Metamagic
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 168
**Foundry id:** `KxoxorctRlefGwil`

> *Your spells go farther than normal.*
>
> **Benefits**: You can alter a spell with a range of touch, close, or medium to increase its range to a higher range category, using the following order: touch, close, medium, and long. A reach spell uses up a spell slot one level higher than the spell's actual level for each increase in range category. For example, a spell with a range of touch increased to long range uses up a spell slot three levels higher. Spells modified by this feat that require melee touch attacks instead require ranged touch attacks.
>
> Spells that do not have a range of touch, close, or medium do not benefit from this feat.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `reach_spell` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Reinforced Crafting
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Craft Magic Arms and Armor, ability to cast make whole or mending
**Source:** PZO9486 (PZO9486) p. 27
**Foundry id:** `h0pRzRlCHFtMmbJC`

> *Your magical creations are hardier than most.*
>
> **Prerequisites**: Craft Magic Arms and Armor, ability to cast make whole or mending.
>
> **Benefit**: When you craft a magic weapon, magic armor, or magic shield, you can add a fortifying element to the item. This increases the item’s total construction cost by 10%. If it’s a weapon, when it becomes broken, the penalty to attack and damage rolls is reduced to –1 (this can never reduce a broken weapon’s penalty to attack and damage to 0 or a positive number). If it’s a suit of armor or a shield, when it becomes broken, the bonus it grants to AC is reduced by one-quarter, rounding down. Other drawbacks of the broken condition to weapons, armor, and shields still apply as normal. Normal: A broken weapon imposes a –2 penalty on attack and damage rolls. The bonus a broken suit of armor or a broken shield grants to AC is halved.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `reinforced_crafting` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Rending Claws
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Str 13, two claw natural weapon attacks, base attack bonus +6
**Source:** Advanced Race Guide (PZO1131) p. 130; Advanced Player's Guide (PZO1115) p. 168
**Foundry id:** `NS0DdgEs4bxZm9Gx`

> *Your claw attacks do greater harm to your enemy.*
>
> **Prerequisites**: Str 13, two claw natural weapon attacks, base attack bonus +6.
>
> **Benefits**: If you hit a creature with two claw attacks in the same turn, the second claw attack deals an additional 1d6 points of damage. This damage is precision damage and is not multiplied on a critical hit. You can use this feat once per round.
>
> ##### Combat Trick
>
> When you make two claw attacks but hit with only one, you can spend 5 stamina points to deal the precision damage granted by this feat anyway.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `rending_claws` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Ride-By Attack
*(feat)*

**Tags:** Combat, Mount, Offensive, Movement
**Prerequisites:** Ride 1 rank, Mounted Combat
**Source:** Core Rulebook (PZO1110) p. 115, 132
**Foundry id:** `liPAO5urMI9chctT`

> *While mounted and charging, you can move, strike at a foe, and then continue moving.*
>
> **Prerequisites**: Ride 1 rank, Mounted Combat.
>
> **Benefits**: When you are mounted and use the charge action, you may move and attack as if with a standard charge and then move again (continuing the straight line of the charge). Your total movement for the round can't exceed double your mounted speed. You and your mount do not provoke an attack of opportunity from the opponent that you attack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `ride_by_attack` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Robot's Bane
*(feat)*

**Tags:** General
**Prerequisites:** —
**Source:** PZO9272 (PZO9272) p. 6
**Foundry id:** `mKrQhQAd4Xr3tB8Q`

> *You have trained to avoid the attacks and effects employed by robots and technology and to combat them effectively.*
>
> **Prerequisites****Knowledge (engineering) 5 ranks
>
> Benefits**: You gain a +1 bonus on attack and damage rolls against creatures with the robot subtype. Additionally, you gain a +1 dodge bonus to your AC and a +1 bonus on saving throws against attacks and effects from robots. If you have at least 11 ranks in Knowledge (engineering), these bonuses increase to +2. If you have at least 17 ranks in Knowledge (engineering), these bonuses increase to +3.
>
> **Special**: If you have constructs as a favored enemy, you can use your favored enemy bonus toward constructs in place of the bonus granted by this feat if it's larger. These bonuses do not stack with those granted by other abilities that allow you to add your favored enemy bonus to AC or on saving throws.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `robot_s_bane` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Run
*(feat)*

**Tags:** General
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 116, 132
**Foundry id:** `bXeW4kLCErPBFpNB`

> *You are swift of foot.*
>
> **Benefits**: When running, you move five times your normal speed (if wearing medium, light, or no armor and carrying no more than a medium load) or four times your speed (if wearing heavy armor or carrying a heavy load). If you make a jump after a running start (see the Acrobatics skill description), you gain a +4 bonus on your Acrobatics check. While running, you retain your Dexterity bonus to your Armor Class.
>
> **Normal**: You move four times your speed while running (if wearing medium, light, or no armor and carrying no more than a medium load) or three times your speed (if wearing heavy armor or carrying a heavy load), and you lose your Dexterity bonus to AC.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `NOT_IMPLEMENTED` — x4 speed for run action
**Manual verdict:** `[ ]`
**Notes:**

---

### Saving Shield
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Shield Proficiency
**Source:** Advanced Race Guide (PZO1131) p. 130; Advanced Player's Guide (PZO1115) p. 168
**Foundry id:** `7wKFKyTQ97nci84x`

> *You deflect attacks that could mean your ally's death.*
>
> **Prerequisites**: Shield Proficiency.
>
> **Benefits**: Whenever an adjacent ally is the target of an attack, you can, as an immediate action, grant that adjacent ally a +2 shield bonus to AC. You must be wielding a light shield, heavy shield, or tower shield to use this feat.
>
> ##### Combat Trick
>
> When you use this feat, you can spend 2 stamina points to increase the shield bonus granted to your ally by an amount equal to the enhancement bonus of the shield you are using.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `saving_shield` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Scavenger's Luck
*(feat)*

**Tags:** General
**Prerequisites:** Knowledge (engineering) 1 rank
**Source:** PZO9272 (PZO9272) p. 7
**Foundry id:** `0KZvBoqEfb1AUZ64`

> *You coax better behavior out of timeworn technology.*
>
> **Prerequisites**: Knowledge (engineering) 1 rank
>
> **Benefits**: When your check for using a piece of timeworn technology results in a glitch, you can roll again. You must choose to reroll before determining the specific glitch, and must take the second result, even if it's worse. When you use timeworn technology, it doesn't automatically glitch on a natural 1.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `scavenger_s_luck` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Scorching Weapons
*(feat)*

**Tags:** Combat, Ifrit, Combat Trick
**Prerequisites:** Ifrit
**Source:** Advanced Race Guide (PZO1131) p. 130; Ultimate Combat (PZO1121) p. 130
**Foundry id:** `vZI5uTnmKJuEXPnu`

> *Elemental fire stirs within your body, boiling your blood and rendering you resistant to flame.*
>
> **Prerequisites**: Ifrit.
>
> **Benefits**: You gain a +2 bonus on saving throws against fire attacks and spells with the fire descriptor or light descriptor. As a swift action, you can make up to two held manufactured metallic weapons become red-hot for 1 round, dealing 1 additional point of fire damage with a successful hit. This does not stack with other effects that add fire damage to weapons, such as the flaming weapon special ability.
>
> ##### Combat Trick
>
> When you use this feat to make one or more metallic weapons red hot for 1 round, you can spend 2 stamina points to increase the additional fire damage to 2 points, and have that damage stack with other effects that add fire damage to a weapon (such as the flaming weapon special ability).

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `scorching_weapons` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Scorpion Style
*(feat)*

**Tags:** Combat, Unarmed, Offensive
**Prerequisites:** Improved Unarmed Strike
**Source:** Core Rulebook (PZO1110) p. 115, 132
**Foundry id:** `2AfSIVge3bg8r6wr`

> *You can perform an unarmed strike that greatly hampers your target's movement.*
>
> **Prerequisites**: Improved Unarmed Strike.
>
> **Benefits**: To use this feat, you must make a single unarmed attack as a standard action. If this unarmed attack hits, you deal damage normally, and the target's base land speed is reduced to 5 feet for a number of rounds equal to your Wisdom modifier unless it makes a Fortitude saving throw (DC 10 + 1/2 your character level + your Wis modifier).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `scorpion_style` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Scribe Scroll
*(feat)*

**Tags:** General, Item Creation
**Prerequisites:** Caster level 1st
**Source:** Core Rulebook (PZO1110) p. 117, 133
**Foundry id:** `tlRu8SYjzA7WCHN7`

> *You can create magic scrolls.*
>
> **Prerequisites**: Caster level 1st.
>
> **Benefits**: You can create a scroll of any spell that you know. Scribing a scroll takes 2 hours if its base price is 250 gp or less, otherwise scribing a scroll takes 1 day for each 1,000 gp in its base price. To scribe a scroll, you must use up raw materials costing half of this base price. See the magic item creation rules in Magic Items for more information.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `NOT_IMPLEMENTED` — crafting feat — deferred to Phase 4
**Manual verdict:** `[ ]`
**Notes:**

---

### Selective Channeling
*(feat)*

**Tags:** Channeling
**Prerequisites:** Cha 13, channel energy class feature
**Source:** Core Rulebook (PZO1110) p. 116, 133-134
**Foundry id:** `WnWRcte0jppClLpz`

> *You can choose whom to affect when you channel energy.*
>
> **Prerequisites**: Cha 13, channel energy class feature.
>
> **Benefits**: When you channel energy, you can choose a number of targets in the area up to your Charisma modifier. These targets are not affected by your channeled energy.
>
> **Normal**: All targets in a 30-foot burst are affected when you channel energy. You can only choose whether or not you are affected.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `selective_channeling` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Self-Sufficient
*(feat)*

**Tags:** General
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 116, 133
**Foundry id:** `8VZQJOyAXbXghxd7`

> *You know how to get along in the wild and how to effectively treat wounds.*
>
> **Benefits**: You get a +2 bonus on all Heal checks and Survival checks. If you have 10 or more ranks in one of these skills, the bonus increases to +4 for that skill.

**Mechanical encoding:** `changes`: 2
  - `2 + if(gte(@skills.hea.ranks, 10), 2)` → `skill.hea`  (untyped)
  - `2 + if(gte(@skills.sur.ranks, 10), 2)` → `skill.sur`  (untyped)

**In our coverage tracker:** absent (slug `self_sufficient` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shake It Off
*(feat)*

**Tags:** Teamwork
**Prerequisites:** —
**Source:** Bestiary (PZO1118) p. 118
**Foundry id:** `WoUopEGAWb3pGp6I`

> *You support your allies and help them recover from crippling effects.*
>
> **Benefit**: When you are adjacent to one or more allies who also have this feat, you gain a +1 bonus on saving throws per such ally (maximum +4).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `shake_it_off` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shark Leap
*(feat)*

**Tags:** Combat
**Prerequisites:** Improved Unarmed Strike, Shark Style, Shark Tear, Swim 10 ranks, base attack bonus +10 or monk level 10th
**Source:** PZO92102 (PZO92102) p. 58-59
**Foundry id:** `GD9p63eAGY4TppNL`

> *Like a deadly predator, you bolt at unsuspecting foes from below.*
>
> **Prerequisites**: Improved Unarmed Strike, Shark Style, Shark Tear, Swim 10 ranks, base attack bonus +10 or monk level 10th.
>
> **Benefits**: While in Shark Style, when you're underwater with neutral, rising, or swiftly rising buoyancy, you can perform a terrifying leap to attack opponents directly above you. This works similarly to the charge action, except you can move only straight up, and you make a single piercing unarmed strike or bite attack. If the attack hits, it deals double damage; if the attack roll's result is also higher than 11 + the target's Swim modifier, the attack knocks the target off-balance until its next turn. Like with a charge, you can perform a partial version when limited to a single standard action (such as in the surprise round); in addition to moving half as far as normal for a partial charge, the attack doubles only the damage dice (as per Vital Strike) rather than the full damage roll.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `shark_leap` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shark Style
*(feat)*

**Tags:** Combat, Style
**Prerequisites:** Improved Unarmed Strike, Swim 3 ranks, base attack bonus +3 or monk level 3rd
**Source:** PZO92102 (PZO92102) p. 59
**Foundry id:** `RaOVZlAzRHFKyr24`

> *You fight like a shark, shredding your foes.*
>
> **Prerequisites**: Improved Unarmed Strike, Swim 3 ranks, base attack bonus +3 or monk level 3rd.
>
> **Benefits**: You can deal piercing or bludgeoning damage with your unarmed strikes. Your piercing unarmed strikes and bite attacks deal an additional 1d6 points of bleed damage.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `shark_style` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shark Tear
*(feat)*

**Tags:** Combat
**Prerequisites:** Improved Unarmed Strike, Shark Style, Swim 6 ranks, base attack bonus +6 or monk level 6th
**Source:** PZO92102 (PZO92102) p. 59
**Foundry id:** `yg43xz1qpQ3jEGk2`

> *You tear into bleeding foes and can smell their blood in the water.*
>
> **Prerequisites**: Improved Unarmed Strike, Shark Style, Swim 6 ranks, base attack bonus +6 or monk level 6th.
>
> **Benefits**: While in Shark Style, you gain scent while in water, but only against bleeding creatures. You also gain a +1 bonus on attack and damage rolls against bleeding creatures.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `shark_tear` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shatter Defenses
*(feat)*

**Tags:** Combat, Offensive
**Prerequisites:** Weapon Focus, Dazzling Display, base attack bonus +6, proficiency with weapon
**Source:** Core Rulebook (PZO1110) p. 117, 133
**Foundry id:** `kn854Ovz0BDA2Dgz`

> *Your skill with your chosen weapon leaves opponents unable to defend themselves if you strike them when their defenses are already compromised.*
>
> **Prerequisites**: Weapon Focus, Dazzling Display, base attack bonus +6, proficiency with weapon.
>
> **Benefits**: Any shaken, frightened, or panicked opponent hit by you this round is flat-footed to your attacks until the end of your next turn. This includes any additional attacks you make this round.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `shatter_defenses` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shield Focus
*(feat)*

**Tags:** Combat, Combat Trick, Defensive
**Prerequisites:** Shield Proficiency, base attack bonus +1
**Source:** Core Rulebook (PZO1110) p. 116, 133
**Foundry id:** `7mD4ZksvKFaorAfj`

> *You are skilled at deflecting blows with your shield.*
>
> **Prerequisites**: Shield Proficiency, base attack bonus +1.
>
> **Benefits**: Increase the AC bonus granted by any shield you are using by 1.
>
> ##### Combat Trick
>
> When an attack is made against you while you are using a shield, you can spend up to 2 stamina points. If you do, the shield’s bonus to AC against that attack increases by an amount equal to the number of stamina points you spent.

**Mechanical encoding:** `changes`: 1
  - `if(@shield.type, 1)` → `sac`  (untyped)

**In our coverage tracker:** absent (slug `shield_focus` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shield Master
*(feat)*

**Tags:** Combat, Offensive
**Prerequisites:** Improved Shield Bash, Shield Proficiency, Shield Slam, Two-Weapon Fighting, base attack bonus +11
**Source:** Core Rulebook (PZO1110) p. 116, 133
**Foundry id:** `yB4JlE2GC1MYlweS`

> *Your mastery of the shield allows you to fight with it without hindrance.*
>
> **Prerequisites**: Improved Shield Bash, Shield Proficiency, Shield Slam, Two-Weapon Fighting, base attack bonus +11.
>
> **Benefits**: You do not suffer any penalties on attack rolls made with a shield while you are wielding another weapon. Add your shield's enhancement bonus to attacks and damage rolls made with the shield as if it was a weapon enhancement bonus.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `shield_master` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shield of Swings
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Str 13, Power Attack, base attack bonus +1
**Source:** Advanced Race Guide (PZO1131) p. 131; Advanced Player's Guide (PZO1115) p. 169
**Foundry id:** `j7eMQ1ExZORIO63I`

> *A wild frenzy of attacks serves to bolster your defenses.*
>
> **Prerequisites**: Str 13, Power Attack, base attack bonus +1.
>
> **Benefits**: When you take a full-attack action while wielding a two-handed weapon, you can choose to reduce the damage by 1/2 to gain a +4 shield bonus to AC and CMD until the beginning of your next turn. The reduction in damage applies until the beginning of your next turn.
>
> ##### Combat Trick
>
> When using this feat, you can spend 2 stamina points to reduce your damage dealt by half only until the end of your turn, but you gain the +2 shield bonus to AC only from the end of your turn until the start of your next turn.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `shield_of_swings` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shield Proficiency
*(feat)*

**Tags:** Combat
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 116, 133
**Foundry id:** `WZj7zDvuelEoeXWX`

> *You are trained in how to properly use a shield.*
>
> **Benefits**: When you use a shield (except a tower shield), the shield's armor check penalty only applies to Strength- and Dexterity-based skills.
>
> **Normal**: When you are using a shield with which you are not proficient, you take the shield's armor check penalty on attack rolls and on all skill checks that involve moving.
>
> **Special**: Barbarians, bards, clerics, druids, fighters, paladins, and rangers all automatically have Shield Proficiency as a bonus feat. They need not select it.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `shield_proficiency` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shield Slam
*(feat)*

**Tags:** Combat, Offensive
**Prerequisites:** Improved Shield Bash, Shield Proficiency, Two-Weapon Fighting, base attack bonus +6
**Source:** Core Rulebook (PZO1110) p. 116, 133
**Foundry id:** `GEo7nDHxddLxi66j`

> *In the right position, your shield can be used to send opponents flying.*
>
> **Prerequisites**: Improved Shield Bash, Shield Proficiency, Two-Weapon Fighting, base attack bonus +6.
>
> **Benefits**: Any opponents hit by your shield bash are also hit with a free bull rush attack, substituting your attack roll for the combat maneuver check (see Combat). This bull rush does not provoke an attack of opportunity. Opponents who cannot move back due to a wall or other surface are knocked prone after moving the maximum possible distance. You may choose to move with your target if you are able to take a 5-foot step or to spend an action to move this turn.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `shield_slam` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Shot on the Run
*(feat)*

**Tags:** Combat, Ranged, Weapon, Offensive
**Prerequisites:** Dex 13, Dodge, Mobility, Point-Blank Shot, base attack bonus +4
**Source:** Core Rulebook (PZO1110) p. 116, 133
**Foundry id:** `ymtj17MI4MdwB0v2`

> *You can move, fire a ranged weapon, and move again before your foes can react.*
>
> **Prerequisites**: Dex 13, Dodge, Mobility, Point-Blank Shot, base attack bonus +4.
>
> **Benefits**: As a full-round action, you can move up to your speed and make a single ranged attack at any point during your movement.
>
> **Normal**: You cannot move before and after an attack with a ranged weapon.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `shot_on_the_run` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Sickening Critical
*(feat)*

**Tags:** Combat, Critical, Offensive
**Prerequisites:** Critical Focus, base attack bonus +11
**Source:** Core Rulebook (PZO1110) p. 114, 133
**Foundry id:** `Amz4lAaIp0x0ehPf`

> *Your critical hits cause opponents to become sickened.*
>
> **Prerequisites**: Critical Focus, base attack bonus +11.
>
> **Benefits**: Whenever you score a critical hit, your opponent becomes sickened for 1 minute. The effects of this feat do not stack. Additional hits instead add to the effect's duration.
>
> **Special**: You can only apply the effects of one critical feat to a given critical hit unless you possess Critical Mastery.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `sickening_critical` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Sidestep
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Dex 13, Dodge, Mobility
**Source:** Advanced Race Guide (PZO1131) p. 131; Advanced Player's Guide (PZO1115) p. 169
**Foundry id:** `gagxv8M42Z8M0hvW`

> *You can reposition yourself after a foe's missed swing.*
>
> **Prerequisites**: Dex 13, Dodge, Mobility.
>
> **Benefits**: Whenever an opponent misses you with a melee attack, you may move 5 feet as an immediate action so long as you remain within that opponent's threatened area. This movement does not provoke attacks of opportunity. If you take this step, you cannot take a 5-foot step during your next turn. If you take an action to move during your next turn, subtract 5 feet from your total movement.
>
> ##### Combat Trick
>
> When this feat lets you move, you can spend 2 stamina points to move 10 feet instead of 5. You must still remain in your opponent's threatened area. You still lose your 5-foot step or 5 feet of movement — the movement lost doesn't increase to 10 feet.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `sidestep` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Acrobatics)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 82
**Foundry id:** `WzxMRQNiRbWuR7Gw`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Acrobatics, you earn the following.
>
> **5 Ranks**: You can move at normal speed through a threatened square without provoking an attack of opportunity by increasing the DC of the check by 5 (instead of by 10). You aren’t denied your Dexterity bonus when attempting Acrobatics checks with DCs of 20 or lower.
>
> **10 Ranks**: You can attempt an Acrobatics check at a –10 penalty and use the result as your CMD against trip maneuvers. You can also attempt an Acrobatics check at a –10 penalty in place of a Reflex save to avoid falling. You must choose to use this ability before the trip attempt or Reflex save is rolled. With a successful DC 20 Acrobatics check, you treat an unintentional fall as 10 feet shorter plus 10 feet for every 10 by which you exceed the DC, and treat an intentional fall as 10 feet shorter for every 10 by which you exceed the DC.
>
> **15 Ranks**: You do not provoke attacks of opportunity when standing up from prone.
>
> **20 Ranks**: You double the result of any Acrobatics check when jumping and never fall prone at the end of a fall as long as you remain conscious.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_acrobatics` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Appraise)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 82
**Foundry id:** `qjtxhqhbtzfhsCGn`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Appraise, you earn the following.
>
> **5 Ranks**: A successful DC 20 Appraise check reveals whether an item is magical, and a second check (DC = 25 + the item’s caster level) unveils its properties. You can use Appraise to detect non-written forgeries and counterfeits.
>
> **10 Ranks**: You can determine the most expensive object a creature is wearing or wielding (or in a 5-foot cube) as a standard action by succeeding at a DC 20 check. You never make a wildly inaccurate appraisal of an item’s value.
>
> **15 Ranks**: Determining the most expensive object as above is a move action. You can substitute an Appraise check at a –10 penalty for a Will save to disbelieve a figment or glamer.
>
> **20 Ranks**: Determining the most expensive object as above is a move action, and if the check succeeds, you gain a +2 circumstance bonus on combat maneuver checks to steal that object or disarm a creature of that object for 1 minute.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_appraise` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Bluff)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 82
**Foundry id:** `6Qttn4c2JAddxXP4`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Bluff, you earn the following.
>
> **5 Ranks**: The penalty to Bluff a creature after a failed check is halved unless you failed by 5 or more.
>
> **10 Ranks**: You take no penalty to Bluff a creature after a failed check unless you failed by 5 or more.
>
> **15 Ranks**: Creatures magically attempting to read your thoughts, detect your alignment, or reveal when you are lying must attempt a caster level check (DC = 11 + your ranks in Bluff ) or the effect reveals nothing.
>
> **20 Ranks**: As a full-round action, you can make a suggestion (as the spell, maximum duration 1 hour) to a creature within 30 feet (Will negates, DC = 15 + your Charisma modifier). A creature that saves against your suggestion is immune to further uses of this effect for 24 hours, and whenever the suggested creature is specifically confronted with proof of your manipulation, it receives another saving throw. This is an extraordinary mindaffecting compulsion.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_bluff` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Climb)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 82
**Foundry id:** `Aj5upleDpV0t2wda`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Climb, you earn the following.
>
> **5 Ranks**: You are no longer denied your Dexterity bonus when climbing.
>
> **10 Ranks**: You gain a natural climb speed (but not the +8 racial bonus on Climb checks) of 10 feet, but only on surfaces with a Climb DC of 20 or lower.
>
> **15 Ranks**: You gain a natural climb speed (but not the +8 racial bonus on Climb checks) equal to your base speed on surfaces with a Climb DC of 20 or lower, and of 10 feet on all other surfaces.
>
> **20 Ranks**: You gain a natural climb speed equal to your base speed on all surfaces. If you have both hands free, you gain a +8 racial bonus on Climb checks.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_climb` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Craft)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 83
**Foundry id:** `zN9kRaSjKJ1qsfDE`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Craft, you earn the following.
>
> **5 Ranks**: When determining your weekly progress, double the result of your Craft check before multiplying the result by the item’s DC.
>
> **10 Ranks**: You do not ruin any of your raw materials unless you fail a check by 10 or more.
>
> **15 Ranks**: When you determine your progress, the result of your check is how much work you complete each day in silver pieces.
>
> **20 Ranks**: You can craft magic armor, magic weapons, magic rings, and wondrous items that fall under your category of Craft using the normal Craft rules.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_craft` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Diplomacy)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 83
**Foundry id:** `mI0ymYPoggxjOWwQ`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Diplomacy, you earn the following.
>
> **5 Ranks**: The time required to influence a creature’s attitude or gather information is halved.
>
> **10 Ranks**: You can attempt to adjust a creature’s attitude in 1 round by taking a –10 penalty. If you take 1 minute to adjust a creature’s attitude, add your Charisma bonus to the number of hours that attitude change persists.
>
> **15 Ranks**: You can attempt to adjust a creature’s attitude in 1 round with no penalty. If you take 1 minute to adjust a creature’s attitude, the duration of the resulting change is measured in days, not hours. You can gather information in 10 minutes by taking a –5 penalty.
>
> **20 Ranks**: You can attempt to adjust a creature’s attitude in 1 round with no penalty. If you take 1 minute to adjust a creature’s attitude, the duration of the resulting change is measured in weeks, not hours. You can gather information in 1d4 minutes with no penalty.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_diplomacy` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Disable Device)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 83
**Foundry id:** `pyyYB527dUcwvK66`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Disable Device, you earn the following.
>
> **5 Ranks**: Reduce the time required to disarm a trap or open a lock by taking a –5 penalty on your Disable Device check for each step by which you reduce the time required: 2d4 rounds, 1d4 rounds, 1 round, a standard action, a move action, a swift action.
>
> **10 Ranks**: You can disarm magical traps at a –10 penalty even if you lack the trapfinding ability. If you possess the trapfinding ability, when attempting to disable magic traps, you never trigger them, even if you perform the trigger action (such as looking at a symbol). If you fail the check, you can still trigger the trap, and you can’t use this ability to bypass it.
>
> **15 Ranks**: When attacked by a trap, you can attempt a Disable Device check as an immediate action (adding your trap sense bonus, if any) opposed by the trap’s attack roll or its save DC. If you succeed, you take half damage (or no damage if you exceed the DC by at least 10).
>
> **20 Ranks**: You halve the penalties for performing a quick disarm as described in the 5 Ranks entry. If you possess the trapfinding ability and accept a –20 penalty while using the ability unlocked at 15 ranks, all nearby allies gain the benefit, and you disable the trap as an immediate action before it can trigger if you exceed the DC by at least 10.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_disable_device` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Disguise)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 83
**Foundry id:** `45zmh18kvRS0H641`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Disguise, you earn the following.
>
> **5 Ranks**: You can create a disguise in 1d3 minutes.
>
> **10 Ranks**: You can create a disguise in 1d3 rounds. If you take the full normal amount of time to create your disguise, you take no penalty for disguising your gender, race, or age category.
>
> **15 Ranks**: You can create a disguise as a full-round action.
>
> **20 Ranks**: You can create a disguise as a standard action, or as a full-round action combined with a Bluff check to create a diversion to hide.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_disguise` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Escape Artist)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 84
**Foundry id:** `AtAPt8O9FxrYjiej`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Escape Artist, you earn the following.
>
> **5 Ranks**: If you take a –10 penalty, the time required to use this skill is halved; escaping a grapple or pin is a move action, and escaping a net, animate rope, command plants, or control plants spell is a standard action.
>
> **10 Ranks**: You can attempt to escape from any entangling effect as a standard action with an Escape Artist check (DC = the effect’s save DC + 10). You can attempt an Escape Artist check as a move action to set the DC for a creature to escape from ropes or bindings; you gain a +10 bonus on the check if you instead attempt it as a full-round action.
>
> **15 Ranks**: You can escape any entangling effect (as above) as a move action. As a standard action, you can attempt an Escape Artist check (DC = the effect’s save DC + 20) to suppress a slow or paralysis effect for 1 round, plus 1 round for every 5 by which you exceed the DC. This action counts as purely mental for the purpose of being able to take it while paralyzed.
>
> **20 Ranks**: You can escape being entangled, grappled, or pinned as an immediate action with an Escape Artist check (DC = the effect’s DC + 10 or the attacker’s CMB + 10). You can attempt to suppress a slow or paralysis effect as a standard action (increasing the DC by 10), a move action (increasing the DC by 15), or an immediate action (increasing the DC by 20).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_escape_artist` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Fly)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 84
**Foundry id:** `rZb2Q25YleDEih3J`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Fly, you earn the following.
>
> **5 Ranks**: A successful DC 20 Fly check allows you to make a 45-degree turn without sacrificing movement.
>
> **10 Ranks**: A successful DC 30 Fly check allows you to ascend at a 45-degree angle at full speed. You treat falls after midair collisions as 10 feet shorter with a successful DC 10 Fly check, plus 10 feet for every 10 points by which you exceed the DC.
>
> **15 Ranks**: A successful DC 30 Fly check allows you to make a 90-degree turn without sacrificing movement, or a 180-degree turn by sacrificing 5 feet of movement. You are considered one size category larger when determining wind effects on Fly checks.
>
> **20 Ranks**: A successful DC 35 Fly check allows you to fly straight up at full speed. You are considered two size categories larger when determining wind effects on Fly checks.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_fly` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Handle Animal)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 84
**Foundry id:** `Jsoscf4TXFoHYOd0`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Handle Animal, you earn the following.
>
> **5 Ranks**: Creatures you have trained gain a +2 bonus on Will saves when adjacent to you.
>
> **10 Ranks**: Creatures you have trained gain a +2 bonus on Will saves whenever you are within 30 feet and clearly visible. You can teach a trick in 1 day by increasing the DC by 20.
>
> **15 Ranks**: You can train an animal to understand your speech (as speak with animals) with 1 week of effort and a successful DC 30 Handle Animal check. Its actions are still limited by its Intelligence. You can teach a trick in 1 day (increasing the DC by 10) or 1 hour (increasing the DC by 20).
>
> **20 Ranks**: You can make your speech understandable to any animal for 24 hours with a successful DC 30 Handle Animal check (DC 40 for magical beasts or vermin). You can teach a trick in 1 day, 1 hour (increasing the DC by 10), or 1 minute (increasing the DC by 20).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_handle_animal` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Heal)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 84
**Foundry id:** `8GgeuFw6SDXaHGh1`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Heal, you earn the following.
>
> **5 Ranks**: When you treat deadly wounds, the target recovers hit points and ability damage as if it had rested for a full day.
>
> **10 Ranks**: When you treat deadly wounds, the target recovers hit points as if it had rested for a full day with long-term care.
>
> **15 Ranks**: When you treat deadly wounds, the creature recovers hit point and ability damage as if it had rested for 3 days.
>
> **20 Ranks**: When you treat deadly wounds, the target recovers hit point and ability damage as if it had rested for 3 days with long-term care.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_heal` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Intimidate)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 85
**Foundry id:** `D10dGyw3V0n77Msl`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Intimidate, you earn the following. **An asterisk (*) indicates the total duration cannot exceed 1 round plus 1 round for every 5 by which you exceed the DC.
>
> 5 Ranks**: If you exceed the DC to demoralize a target by at least 10, it is frightened for 1 round and shaken thereafter.* A Will save (DC = 10 + your number of ranks in Intimidate) negates the frightened condition, but the target is still shaken, even if it has the stalwart ability.
>
> **10 Ranks**: If you exceed the DC to demoralize a target by at least 10, it is panicked for 1 round or frightened for 1d4 rounds (your choice) and shaken thereafter.* A Will save (DC = 10 + your number of ranks in Intimidate) negates the frightened or panicked condition, but the target is still shaken, even if it has the stalwart ability.
>
> **15 Ranks**: If you exceed the DC to demoralize a target by at least 20, it is cowering for 1 round or panicked for 1d4 rounds (your choice) and frightened thereafter.* A Will save (DC = 10 + your number of ranks in Intimidate) negates the cowering, panicked, and frightened conditions, but the target is still shaken, even if it has the stalwart ability.
>
> **20 Ranks**: If you exceed the DC to demoralize a target by at least 20, it is cowering for 1d4 rounds and panicked thereafter.* A Will save (DC = 10 + your number of ranks in Intimidate) negates the cowering and panicked conditions, but the target is still shaken, even if it has the stalwart ability.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_intimidate` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Knowledge)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 85
**Foundry id:** `75XcMJS5yUIuhzsU`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Knowledge, you earn the following.
>
> **5 Ranks**: When you successfully identify a creature, you gain one additional piece of information for every 5 ranks you possess in that Knowledge skill.
>
> **10 Ranks**: When you successfully identify a creature, you gain a +1 competence bonus on attack rolls, opposed ability checks, skill checks, and caster level checks against creatures of that kind (e.g., glabrezu demons, but not other demons or evil outsiders) for 1 minute. This bonus increases by 1 for every 5 ranks beyond 10 you possess in that Knowledge skill.
>
> **15 Ranks**: When you fail a Knowledge check, you can reroll the check at a –10 penalty. The competence bonus above also applies to saving throws against exceptional, spell-like, or supernatural abilities used by creatures you identify.
>
> **20 Ranks**: Whenever you attempt a Knowledge check, you can roll twice and take the better result.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_knowledge` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Linguistics)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 85
**Foundry id:** `4Z5VmbdMnFWyBLwf`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Linguistics, you earn the following.
>
> **5 Ranks**: You can use Linguistics instead of Sense Motive to intercept and interpret secret messages (as the Bluff skill). You gain a +1 insight bonus on Perception and Disable Device checks to detect or disarm written magical traps. This bonus increases by 1 for every 5 ranks beyond 5 you possess in Linguistics.
>
> **10 Ranks**: If you succeed at a Linguistics check by at least 10 when examining writing, you can learn the precise meaning rather than general content, and you never draw false conclusions on a failed check. A successful DC 30 Linguistics check reveals the general meaning of speech, a successful DC 35 check reveals 1d4 pieces of specific information, and a successful DC 40 check reveals exact meaning.
>
> **15 Ranks**: You can decipher magical writings (as read magic) by succeeding at a Linguistics check (DC = 25 + caster level). If you identify a written magical trap in this way, you gain a +2 circumstance bonus on Disable Device checks to disarm it.
>
> **20 Ranks**: You can attempt to decipher magical or nonmagical text at a rate of one page per round. If you instead spend 1 minute per page, roll twice and take the better result.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_linguistics` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Perception)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 85
**Foundry id:** `zD6KBnFbY1Nrok5h`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Perception, you earn the following.
>
> **5 Ranks**: You remain alert to sounds even in your sleep, and the normal DC increase to Perception checks when you are sleeping is halved. The distance modifier on the DC of Perception checks you attempt is reduced to +1 per 20 feet.
>
> **10 Ranks**: The distance modifier on the DC of Perception checks you attempt is reduced to +1 per 30 feet. In addition, you gain a +5 bonus on Perception checks to notice or locate an invisible creature or object.
>
> **15 Ranks**: You remain alert to sounds even in your sleep, and the normal DC increase to Perception checks when you are sleeping doesn’t apply to you. The distance modifier on the DC of your Perception checks is reduced to +1 per 40 feet.
>
> **20 Ranks**: You gain a +10 bonus on Perception checks to notice invisible creatures or objects. The distance modifier on the DC of Perception checks you attempt is reduced to +1 per 60 feet.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_perception` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Perform)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 85
**Foundry id:** `YlmQY1Dwjs2EusuT`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Perform, you earn the following.
>
> **5 Ranks**: Whenever you attempt a Bluff, Diplomacy, Handle Animal, or Intimidate check, you can attempt a DC 20 Perform check to gain a +2 circumstance bonus on the check.
>
> **10 Ranks**: Whenever you cast a spell with the emotion or language-dependent descriptor, you can attempt a DC 25 Perform check to increase the save DC by 1.
>
> **15 Ranks**: Whenever you cast a spell with the emotion or language-dependent descriptor, you can attempt a DC 30 Perform check to increase your caster level by 1. You must choose whether to use this ability or the ability unlocked at 10 ranks when casting the spell.
>
> **20 Ranks**: Choose one of the following skills: Bluff, Diplomacy, or Intimidate. When you attempt a skill check with that skill, you can also attempt a Perform check and use the better result to determine the success of that skill check.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_perform` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Profession)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 86
**Foundry id:** `uotzThdayYmtFieG`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Profession, you earn the following.
>
> **5 Ranks**: When using Profession checks to earn income, you earn gold pieces equal to the result of your check each week.
>
> **10 Ranks**: When attempting Profession checks, you can roll twice and take the better result. When answering questions about your Profession, you can always take 10.
>
> **15 Ranks**: You can attempt checks to earn income once per day instead of once per week.
>
> **20 Ranks**: When attempting Profession checks, you can choose to roll once instead of twice. If you do and the result of the roll is less than 10, replace it with 10. When answering questions about your Profession, you can always take 20.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_profession` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Ride)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 86
**Foundry id:** `THh2QoWGXIJUaGsw`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Ride, you earn the following.
>
> **5 Ranks**: Your mount gains a +2 bonus on Fortitude saves or Constitution checks to avoid becoming fatigued or exhausted. This bonus increases by 1 for every 5 ranks beyond 5 you possess in Ride.
>
> **10 Ranks**: When you spur your mount, its speed is increased by 20 feet, and it gains a +2 bonus on Reflex saves and a +2 dodge bonus to AC.
>
> **15 Ranks**: When an opponent targets you or your mount with a bull rush, drag, overrun, reposition, or trip combat maneuver while you are mounted, you can substitute the result of a Ride check in place of your (or your mount’s) CMD.
>
> **20 Ranks**: When you spur your mount, its speed is increased by 30 feet, and it gains a +4 bonus on Reflex saves and a +4 dodge bonus to AC.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_ride` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Sense Motive)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 86
**Foundry id:** `YfSxUIhoYTL1o3Yp`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Sense Motive, you earn the following.
>
> **5 Ranks**: If you were aware of an opponent before rolling initiative (such as when you ambush an enemy or negotiations break down into combat, but not when both sides happen upon each other or you are surprised), you can attempt a Sense Motive check as part of your initiative check (DC = 11 + the highest Bluff modifier among your opponents or DC 15, whichever is higher). If you succeed, you gain a +1 bonus on the initiative check, plus an additional +1 for every 5 by which you exceeded the DC.
>
> **10 Ranks**: After 1 minute of conversation, you can read a creature’s surface thoughts (as detect thoughts) by attempting a Sense Motive check at a –20 penalty opposed by the creature’s Bluff check.
>
> **15 Ranks**: You can read surface thoughts as above after 1 round. In addition, when attacked, you can attempt a Sense Motive check as an immediate action opposed by your target’s attack roll. A successful check grants a +2 insight bonus to your AC against attacks from that specific opponent for 1 minute.
>
> **20 Ranks**: You can read surface thoughts as above as a standard action. A successful check to gain an insight bonus to your AC also negates the attack that triggered it.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_sense_motive` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Sleight of Hand)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 86
**Foundry id:** `8Gd3pvhQtXUmpKi1`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Sleight of Hand, you earn the following.
>
> **5 Ranks**: When attempting a disarm or steal maneuver, a successful Sleight of Hand check against your target’s CMD grants a +2 circumstance bonus on your combat maneuver check.
>
> **10 Ranks**: The penalty for attempting a Sleight of Hand check (including drawing a hidden weapon) as a move action is reduced to –10.
>
> **15 Ranks**: You can attempt a Sleight of Hand check (including drawing a hidden weapon) as a swift action at a –20 penalty.
>
> **20 Ranks**: You take no penalty for using Sleight of Hand as a move action, and take only a –10 penalty when using it as a swift action.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_sleight_of_hand` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Spellcraft)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 86
**Foundry id:** `ZMxgexE56Ru4qrdx`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Spellcraft, you earn the following.
>
> **5 Ranks**: Identifying magic items takes 1 full round, and the time required to learn a spell from a spellbook is halved.
>
> **10 Ranks**: You can identify magic items without using detect magic, though the DC is increased by 10.
>
> **15 Ranks**: Identifying magic items is a standard action, and the time required to learn a new spell from a spellbook is reduced to 1 minute per spell level.
>
> **20 Ranks**: Whenever you attempt a caster level check, attempt a Spellcraft check at a –20 penalty at the same DC. If the spellcraft check succeeds, you gain a +2 circumstance bonus on your caster level check.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_spellcraft` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Stealth)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 86
**Foundry id:** `BbZIN6lmkZDry3ml`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Stealth, you earn the following. 
>
> **5 Ranks**: Reduce the Stealth penalty from sniping by 10. 
>
> **10 Ranks**: Stealth check penalties for moving quickly are halved, including the ability unlocked at 5 ranks, moving full speed, and reaching concealment after creating a distraction. 
>
> **15 Ranks**: If you attack after successfully using Stealth, your target is denied its Dexterity bonus against all attacks that you make before the end of your turn. 
>
> **20 Ranks**: If you attack after successfully using Stealth, your target is denied its Dexterity bonus against all attacks that you make before the beginning of your next turn.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_stealth` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Survival)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 87
**Foundry id:** `k3ZioHnhvOHUQvF9`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Survival, you earn the following.
>
> **5 Ranks**: You reduce all nonlethal damage you take from heat, cold, starvation, or thirst by 1 point for every 5 ranks you possess in Survival.
>
> **10 Ranks**: You can track creatures that leave no tracks, including flying and swimming creatures and creatures using trackless step or pass without trace, taking a –20 penalty on your Survival check.
>
> **15 Ranks**: Once per day, you can spend 1 hour and attempt a DC 30 Survival check. Success grants you cold resistance or fire resistance 5 for 24 hours. You can share this with one ally for every 5 by which you exceeded the check.
>
> **20 Ranks**: You take only a –10 penalty when tracking creatures that leave no tracks.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_survival` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Swim)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 87
**Foundry id:** `QhUjSBWAp6EYFM8K`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Swim, you earn the following. 
>
> **5 Ranks**: You gain a swim speed of 10 feet, but only in water with a Swim DC of 15 or lower. 
>
> **10 Ranks**: You gain a swim speed (though you do not gain the +8 racial bonus on Swim checks) equal to your base speed in water with a Swim DC of 15 or lower, or 10 feet in all other water. 
>
> **15 Ranks**: You ignore the penalties for using slashing or bludgeoning weapons underwater, as freedom of movement. 
>
> **20 Ranks**: You gain a swim speed equal to your base speed in all water. If you have both hands free, you gain a +8 racial bonus on Swim checks.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_swim` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill (Use Magic Device)
*(feat)*

**Tags:** Skill Unlock
**Prerequisites:** Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
**Source:** Advanced Race Guide (PZO1131) p. 87
**Foundry id:** `F8jywnqod8RLELNO`

> **Prerequisites**: Rogue's Edge (UC) or 5 ranks in the choosen skill (see Signature Skill)
>
> With sufficient ranks in Use Magic Device, you earn the following. 
>
> **5 Ranks**: You can use the aid another action to assist another creature’s Use Magic Device check by attempting a check against the item’s Use Magic Device DC. 
>
> **10 Ranks**: If you roll a natural 1 when activating an item, you take a –10 penalty on Use Magic Device checks with that item for 24 hours instead of being unable to activate it. This penalty stacks with itself. 
>
> **15 Ranks**: You can use this skill to emulate two races or two alignments simultaneously. 
>
> **20 Ranks**: If you roll a natural 1 when activating an item, you can reroll the check at a –10 penalty to activate the item. You must take the result of the second check, even if it is worse, and you can’t reroll it again.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill_use_magic_device` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Signature Skill
*(feat)*

**Tags:** —
**Prerequisites:** 5 ranks in the chosen skill
**Source:** Advanced Race Guide (PZO1131) p. 82
**Foundry id:** `zOxJqI5CG4VoycmQ`

> *Your ability with a particular skill is the stuff of legends, and you can do things with that skill that others cannot.*
>
> **Prerequisites**: 5 ranks in the chosen skill.
>
> **Benefit**: Choose one skill. You gain the ability listed in that skill’s 5 Ranks entry. As you gain more ranks in the chosen skill, you gain additional abilities. If you have 10 or more ranks in the chosen skill, you gain the appropriate abilities immediately. If your chosen skill is Craft, Knowledge, Perform, or Profession, you gain the listed powers only for one category of that skill, such as Craft (bows). This feat can be taken only once, but it stacks with the rogue’s edge ability and the cutting edge rogue talent.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `signature_skill` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Silent Spell
*(feat)*

**Tags:** Metamagic, Magic
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 117, 133
**Foundry id:** `2YuxcUNFMPNBpekG`

> *You can cast your spells without making any sound.*
>
> **Benefits**: A silent spell can be cast with no verbal components. Spells without verbal components are not affected. A silent spell uses up a spell slot one level higher than the spell's actual level.
>
> **Special**: Bard spells cannot be enhanced by this feat.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `silent_spell` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Simple Weapon Proficiency
*(feat)*

**Tags:** Combat
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 116, 133
**Foundry id:** `y3GhqdsCdE9IyYQc`

> *You are trained in the use of basic weapons.*
>
> **Benefits**: You make attack rolls with simple weapons without penalty.
>
> **Normal**: When using a weapon with which you are not proficient, you take a -4 penalty on attack rolls.
>
> **Special**: All characters except for druids, monks, and wizards are automatically proficient with all simple weapons. They need not select this feat.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `simple_weapon_proficiency` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Skill Focus
*(feat)*

**Tags:** General, Skill
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 116, 134
**Foundry id:** `7zJTztNW7hdaqjKc`

> *Choose a skill. You are particularly adept at that skill.*
>
> **Benefits**: You get a +3 bonus on all checks involving the chosen skill. If you have 10 or more ranks in that skill, this bonus increases to +6.
>
> **Special**: You can gain this feat multiple times. Its effects do not stack. Each time you take the feat, it applies to a new skill.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `IMPLEMENTED` — +3 to chosen skill (parametric)
**Manual verdict:** `[ ]`
**Notes:**

---

### Snap Shot
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Dex 13, Point-Blank Shot, Rapid Shot, Weapon Focus, base attack bonus +6
**Source:** Advanced Race Guide (PZO1131) p. 132; Bestiary (PZO1118) p. 119-120
**Foundry id:** `tk0zKjZTUTvs0y7g`

> *With a ranged weapon, you can take advantage of any opening in your opponent's defenses.*
>
> **Prerequisites**: Dex 13, Point-Blank Shot, Rapid Shot, Weapon Focus, base attack bonus +6.
>
> **Benefits**: While wielding a ranged weapon with which you have Weapon Focus, you threaten squares within 5 feet of you. You can make attacks of opportunity with that ranged weapon. You do not provoke attacks of opportunity when making a ranged attack as an attack of opportunity.
>
> **Normal**: While wielding a ranged weapon, you threaten no squares and can make no attacks of opportunity with that weapon.
>
> ##### Combat Trick
>
> At the end of your turn, you can spend 2 stamina points to increase the range at which you threaten squares with ranged weapons to 10 feet until you take an attack of opportunity against an opponent in the expanded threat range or the beginning of your next turn, whichever comes first.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `snap_shot` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Snatch Arrows
*(feat)*

**Tags:** Combat, Ranged, Defensive
**Prerequisites:** Dex 15, Deflect Arrows, Improved Unarmed Strike
**Source:** Core Rulebook (PZO1110) p. 115, 134
**Foundry id:** `bHcqTC4Lf3aVl3VO`

> *Instead of knocking an arrow or ranged attack aside, you can catch it in mid-flight.*
>
> **Prerequisites**: Dex 15, Deflect Arrows, Improved Unarmed Strike.
>
> **Benefits**: When using the Deflect Arrows feat you may choose to catch the weapon instead of just deflecting it. Thrown weapons can immediately be thrown back as an attack against the original attacker (even though it isn't your turn) or kept for later use.
>
> You must have at least one hand free (holding nothing) to use this feat.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `snatch_arrows` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Snatch
*(feat)*

**Tags:** Monster
**Prerequisites:** Size Huge or larger
**Source:** —
**Foundry id:** `PBqk2ZYEdehWcprC`

> *This creature can grab other creatures with ease.*
>
> **Prerequisites**: Size Huge or larger.
>
> **Benefits**: The creature can start a grapple when it hits with a claw or bite attack, as though it had the grab ability. If it grapples a creature three or more sizes smaller, it squeezes each round for automatic bite or claw damage with a successful grapple check. A snatched opponent held in the creature's mouth is not allowed a Reflex save against the creature's breath weapon, if it has one.
>
> The creature can drop a creature it has snatched as a free action or use a standard action to fling it aside. A flung creature travels 1d6 x 10 feet, and takes 1d6 points of damage per 10 feet traveled. If the creature flings a snatched opponent while flying, the opponent takes this amount or falling damage, whichever is greater.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `snatch` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Spell Focus
*(feat)*

**Tags:** General, Magic
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 116, 134
**Foundry id:** `V2zY7BltkpSXwejy`

> *Choose a school of magic. Any spells you cast of that school are more difficult to resist.*
>
> **Benefits**: Add +1 to the Difficulty Class for all saving throws against spells from the school of magic you select.
>
> **Special**: You can gain this feat multiple times. Its effects do not stack. Each time you take the feat, it applies to a new school of magic.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `IMPLEMENTED` — +1 DC to chosen school (parametric)
**Manual verdict:** `[ ]`
**Notes:**

---

### Spell Mastery
*(feat)*

**Tags:** General, Magic
**Prerequisites:** 1st-level wizard
**Source:** Core Rulebook (PZO1110) p. 116, 134
**Foundry id:** `KlE26ofz7uAkd0IJ`

> *You have mastered a small handful of spells, and can prepare these spells without referencing your spellbooks at all.*
>
> **Prerequisites**: 1st-level wizard
>
> **Benefits**: Each time you take this feat, choose a number of spells that you already know equal to your Intelligence modifier. From that point on, you can prepare these spells without referring to a spellbook.
>
> **Normal**: Without this feat, you must use a spellbook to prepare all your spells, except *read magic*.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `spell_mastery` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Spell Penetration
*(feat)*

**Tags:** General, Magic
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 116, 134
**Foundry id:** `nWFr8SNcjcMqsXSH`

> *Your spells break through spell resistance more easily than most.*
>
> **Benefits**: You get a +2 bonus on caster level checks (1d20 + caster level) made to overcome a creature's spell resistance.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `IMPLEMENTED` — +2 caster level vs SR
**Manual verdict:** `[ ]`
**Notes:**

---

### Spellbreaker
*(feat)*

**Tags:** Combat, Magic, Offensive
**Prerequisites:** Disruptive, 10th-level fighter
**Source:** —
**Foundry id:** `yE3hVOvBq9rx6TAw`

> *You can strike at enemy spellcasters who fail to cast defensively when you threaten them.*
>
> **Prerequisites**: Disruptive, 10th-level fighter.
>
> **Benefits**: Enemies in your threatened area that fail their checks to cast spells defensively provoke attacks of opportunity from you.
>
> **Normal**: Enemies that fail to cast spells defensively do not provoke attacks of opportunity.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `spellbreaker` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Spirited Charge
*(feat)*

**Tags:** Combat, Mount, Weapon, Offensive, Movement
**Prerequisites:** Ride 1 rank, Mounted Combat, Ride-By Attack
**Source:** Core Rulebook (PZO1110) p. 115, 134
**Foundry id:** `jKVhOxHu6VmUgFdp`

> *Your mounted charge attacks deal a tremendous amount of damage.*
>
> **Prerequisites**: Ride 1 rank, Mounted Combat, Ride-By Attack.
>
> **Benefits**: When mounted and using the charge action, you deal double damage with a melee weapon (or triple damage with a lance).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `spirited_charge` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Spit Venom
*(feat)*

**Tags:** Combat, Nagaji, Combat Trick
**Prerequisites:** Nagaji
**Source:** Ultimate Combat (PZO1121) p. 197
**Foundry id:** `I34hZ82Wa8O0ibpX`

> *You have mastered the nagaji warrior technique of spitting venom into your opponent’s eyes.*
>
> **Prerequisites**: Nagaji.
>
> **Benefit**: As a full-round action, you can spit poison up to 10 feet as a ranged touch attack. If you hit, the target must make a successful Fortitude save or be blinded for 1d6 rounds. The DC of this save is equal to 10 + 1/2 your total Hit Dice + your Constitution modifier. You can use this ability once per day plus one additional time per day for every three Hit Dice you have.
>
> ##### Combat Trick
>
> When you spit poison, you can spend up to 5 stamina points. For each stamina point spent, you can increase the range of the attack by 5 feet.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `spit_venom` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Spring Attack
*(feat)*

**Tags:** Combat, Offensive, Movement
**Prerequisites:** Dex 13, Dodge, Mobility, base attack bonus +4
**Source:** Core Rulebook (PZO1110) p. 114, 134
**Foundry id:** `ugQyUpqPBDsqLyra`

> *You can deftly move up to a foe, strike, and withdraw before he can react.*
>
> **Prerequisites**: Dex 13, Dodge, Mobility, base attack bonus +4.
>
> **Benefits**: As a full-round action, you can move up to your speed and make a single melee attack without provoking any attacks of opportunity from the target of your attack. You can move both before and after the attack, but you must move at least 10 feet before the attack and the total distance that you move cannot be greater than your speed. You cannot use this ability to attack a foe that is adjacent to you at the start of your turn.
>
> **Normal**: You cannot move before and after an attack.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `spring_attack` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Staggering Critical
*(feat)*

**Tags:** Combat, Critical, Offensive
**Prerequisites:** Critical Focus, base attack bonus +13
**Source:** Core Rulebook (PZO1110) p. 114, 134
**Foundry id:** `nVNkWyzh4EVyxouV`

> *Your critical hits cause opponents to slow down.*
>
> **Prerequisites**: Critical Focus, base attack bonus +13.
>
> **Benefits**: Whenever you score a critical hit, your opponent becomes staggered for 1d4+1 rounds. A successful Fortitude save reduces the duration to 1 round. The DC of this Fortitude save is equal to 10 + your base attack bonus. The effects of this feat do not stack. Additional hits instead add to the duration.
>
> **Special**: You can only apply the effects of one critical feat to a given critical hit unless you possess Critical Mastery.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `staggering_critical` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Stand Still
*(feat)*

**Tags:** Combat, Offensive, Movement, Combat Maneuver
**Prerequisites:** Combat Reflexes
**Source:** Core Rulebook (PZO1110) p. 114, 134
**Foundry id:** `3S01BGUthIbp3Hju`

> *You can stop foes that try to move past you.*
>
> **Prerequisites**: Combat Reflexes.
>
> **Benefits**: When a foe provokes an attack of opportunity due to moving through your adjacent squares, you can make a combat maneuver check as your attack of opportunity. If successful, the enemy cannot move for the rest of his turn. An enemy can still take the rest of his action, but cannot move. This feat also applies to any creature that attempts to move from a square that is adjacent to you if such movement provokes an attack of opportunity.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `stand_still` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Stealthy
*(feat)*

**Tags:** General, Skill
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 116, 135
**Foundry id:** `f5FPqAYWlKj3zCIY`

> *You are good at avoiding unwanted attention and slipping out of bonds.*
>
> **Benefits**: You get a +2 bonus on all Escape Artist and Stealth skill checks. If you have 10 or more ranks in one of these skills, the bonus increases to +4 for that skill.

**Mechanical encoding:** `changes`: 2
  - `2 + if(gte(@skills.esc.rank, 10), 2)` → `skill.esc`  (untyped)
  - `2 + if(gte(@skills.ste.rank, 10), 2)` → `skill.ste`  (untyped)

**In our coverage tracker:** `IMPLEMENTED` — +2 stealth/escape_artist
**Manual verdict:** `[ ]`
**Notes:**

---

### Step Up and Strike
*(feat)*

**Tags:** Combat, Movement, Offensive, Combat Trick
**Prerequisites:** Dex 13, Following Step, Step Up, base attack bonus +6
**Source:** Advanced Player's Guide (PZO1115) p. 170; Advanced Race Guide (PZO1131) p. 132
**Foundry id:** `Vq8zGwac1PqaY4IF`

> *When a foe tries to move away, you can follow and make an attack.*
>
> **Prerequisites**: Dex 13, Following Step, Step Up, base attack bonus +6.
>
> **Benefit**: When using the Step Up or Following Step feats to follow an adjacent foe, you may also make a single melee attack against that foe at your highest base attack bonus. This attack counts as one of your attacks of opportunity for the round. Using this feat does not count toward the number of actions you can usually take each round.
>
> **Normal**: You can usually only take one standard action and one 5-foot step each round.
>
> ##### Combat Trick
>
> You can spend 5 stamina points to make this feat’s attack without having that attack count as one of your attacks of opportunity for the round.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `step_up_and_strike` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Step Up
*(feat)*

**Tags:** Combat, Movement, Offensive, Combat Trick
**Prerequisites:** Base attack bonus +1
**Source:** Core Rulebook (PZO1110) p. 116, 135; Advanced Race Guide (PZO1131) p. 132
**Foundry id:** `Mz8ZG6nqW3NKFZhK`

> *You can close the distance when a foe tries to move away.*
>
> **Prerequisites**: Base attack bonus +1.
>
> **Benefits**: Whenever an adjacent foe attempts to take a 5-foot step away from you, you may also make a 5-foot step as an immediate action so long as you end up adjacent to the foe that triggered this ability. If you take this step, you cannot take a 5-foot step during your next turn. If you take an action to move during your next turn, subtract 5 feet from your total movement.
>
> ##### Combat Trick
>
> As long as you have at least 1 stamina point in your stamina pool, on the turn after you use this feat, you can still take a 5-foot step, and you don’t reduce your speed if you take an action to move due to this feat.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `step_up` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Still Spell
*(feat)*

**Tags:** Metamagic, Magic
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 117, 135
**Foundry id:** `jVFjMIyQD6TOAsmj`

> *You can cast spells without moving.*
>
> **Benefits**: A stilled spell can be cast with no somatic components. Spells without somatic components are not affected. A stilled spell uses up a spell slot one level higher than the spell's actual level.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `still_spell` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Stony Step
*(feat)*

**Tags:** Oread
**Prerequisites:** Oread
**Source:** Ultimate Combat (PZO1121) p. 147-148
**Foundry id:** `QsGY4DuSVU3iIfjA`

> *The earth recognizes its kinship with you and does not impede your movement.*
>
> **Prerequisites**: Oread.
>
> **Benefits**: Whenever you move, you may move through 5 feet of earth- or stone-based difficult terrain (rubble, stone stairs, and so on) each round as if it were normal terrain. The effects of this feat stack with similar feats such as Acrobatic Steps and Nimble Moves. This feat allows you to take a 5-foot step into this kind of difficult terrain.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `stony_step` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Strike Back
*(feat)*

**Tags:** Combat
**Prerequisites:** Base attack bonus +11
**Source:** Core Rulebook (PZO1110) p. 116, 135
**Foundry id:** `PkktjwppuVzoLn19`

> *You can strike at foes that attack you using their superior reach, by targeting their limbs or weapons as they come at you.*
>
> **Prerequisites**: Base attack bonus +11.
>
> **Benefits**: You can ready an action to make a melee attack against any foe that attacks you in melee, even if the foe is outside of your reach.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `strike_back` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Stunning Critical
*(feat)*

**Tags:** Combat, Critical, Offensive
**Prerequisites:** Critical Focus, Staggering Critical, base attack bonus +17
**Source:** Core Rulebook (PZO1110) p. 114, 135
**Foundry id:** `lgMKavJ4ePylzlqA`

> *Your critical hits cause opponents to become stunned.*
>
> **Prerequisites**: Critical Focus, Staggering Critical, base attack bonus +17.
>
> **Benefits**: Whenever you score a critical hit, your opponent becomes stunned for 1d4 rounds. A successful Fortitude save reduces this to staggered for 1d4 rounds. The DC of this Fortitude save is equal to 10 + your base attack bonus. The effects of this feat do not stack. Additional hits instead add to the duration.
>
> **Special**: You can only apply the effects of one critical feat to a given critical hit unless you possess Critical Mastery.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `stunning_critical` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Stunning Fist
*(feat)*

**Tags:** Combat, Unarmed, Offensive
**Prerequisites:** Dex 13, Wis 13, Improved Unarmed Strike, base attack bonus +8
**Source:** Core Rulebook (PZO1110) p. 115, 135
**Foundry id:** `GsjouI6B8X7BA5wN`

> *You know just where to strike to temporarily stun a foe.*
>
> **Prerequisites**: Dex 13, Wis 13, Improved Unarmed Strike, base attack bonus +8.
>
> **Benefits**: You must declare that you are using this feat before you make your attack roll (thus, a failed attack roll ruins the attempt). Stunning Fist forces a foe damaged by your unarmed attack to make a Fortitude saving throw (DC 10 + 1/2 your character level + your Wis modifier), in addition to dealing damage normally. A defender who fails this saving throw is stunned for 1 round (until just before your next turn). A stunned character drops everything held, can't take actions, loses any Dexterity bonus to AC, and takes a -2 penalty to AC. You may attempt a stunning attack once per day for every four levels you have attained (but see Special), and no more than once per round. Constructs, oozes, plants, undead, incorporeal creatures, and creatures immune to critical hits cannot be stunned.
>
> **Special**: A monk receives Stunning Fist as a bonus feat at 1st level, even if he does not meet the prerequisites. A monk may attempt a stunning attack a number of times per day equal to his monk level, plus one more time per day for every four levels he has in classes other than monk.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `stunning_fist` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Sundering Strike
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Str 13, Improved Sunder, Power Attack, base attack bonus +9
**Source:** Advanced Race Guide (PZO1131) p. 133; Advanced Player's Guide (PZO1115) p. 171-172
**Foundry id:** `kl3ehmJ2wydNdtvu`

> *Your critical hits can sunder your foes' weapons.*
>
> **Prerequisites**: Str 13, Improved Sunder, Power Attack, base attack bonus +9.
>
> **Benefits**: Whenever you score a critical hit with a melee attack, you can sunder your opponent's weapon, in addition to the normal damage dealt by the attack. If your confirmation roll exceeds your opponent's CMD, you may deal damage to your opponent's weapon as if from the sunder combat maneuver (roll normal damage to the weapon separately). This does not provoke an attack of opportunity.
>
> **Normal**: You must perform a sunder combat maneuver to sunder an opponent's weapon.
>
> **Special**: You can only apply the effects of one of the following feats to a given critical hit: Bull Rush Strike, Disarming Strike, Repositioning Strike, Sundering Strike, or Tripping Strike. You may choose to use this feat after you make your confirmation roll.
>
> ##### Combat Trick
>
> When you fail to confirm a critical hit with a melee attack, you can spend 2 stamina points to attempt to sunder the target's weapon anyway. When you do, reroll the confirmation roll and use it to determine if the sunder attempt exceeds the opponent's CMD. This reroll is used only for the sunder combat maneuver; it can't cause the critical hit to be confirmed. You still can't make the attempt if the target is immune to critical hits.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `sundering_strike` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Swap Places
*(feat)*

**Tags:** Teamwork, Combat, Combat Trick
**Prerequisites:** —
**Source:** Advanced Player's Guide (PZO1115) p. 172
**Foundry id:** `4FheAz49TCHTCl6O`

> *You are skilled at changing places with your ally during a chaotic melee.*
>
> **Benefit**: Whenever you are adjacent to an ally who also has this feat, you can move into your ally’s square as part of normal movement. At the same time, your ally moves into your previous space as an immediate action. Both you and your ally must be willing and able to move to take advantage of this feat. Your ally must be the same size as you to utilize this feat. Your ally does not provoke an attack of opportunity from this movement, but you provoke as normal. This movement does not count against your ally’s movement on his next turn.
>
> ##### Combat Trick
>
> When using this feat, you can spend 2 stamina points. If you do, your movement during the swap doesn’t provoke attacks of opportunity.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `swap_places` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Tail Terror
*(feat)*

**Tags:** Combat Trick, Kobold
**Prerequisites:** Base attack bonus +1, kobold
**Source:** Ultimate Combat (PZO1121) p. 137
**Foundry id:** `XAQntETXIH2e5GwF`

> *You have strengthened your tail enough to make slap attacks with it.*
>
> **Prerequisites**: Base attack bonus +1, kobold.
>
> **Benefit**: You can make a tail slap attack with your tail. This is a secondary natural attack that deals 1d4 points of bludgeoning damage. Furthermore, you can augment your tail slap attack with a kobold tail attachment. For the purpose of weapon feats, you are considered proficient with all kobold tail attachments.
>
> ##### Combat Trick
>
> At the start of your turn, you can spend 5 stamina points to treat your tail slap as a primary natural attack until the beginning of your next turn. The tail slap is treated as a primary attack even if used along with weapon attacks as part of a full attack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `tail_terror` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Technologist
*(feat)*

**Tags:** General
**Prerequisites:** —
**Source:** PZO9000-15E (PZO9000-15E) p. 9; PZO9272 (PZO9272) p. 7
**Foundry id:** `1foaZv9wfqZVrZ90`

> *You are familiar with the basic mechanics of technology.*
>
> **Benefits**: You are considered to be trained in any skill used against a technology-based subject. If the skill in question requires training to use even against non-technological subjects, you must still have ranks in that skill in order to gain the benefit of Technologist.
>
> **Normal**: You treat all skill checks made against technology as if they were untrained skill checks. This may mean that you cannot attempt certain skill checks, even if you possess ranks in the skill in question.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `technologist` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Technology Adept
*(feat)*

**Tags:** Combat
**Prerequisites:** Dex 13, Exotic Weapon Proficiency (firearms), Point-Blank Shot
**Source:** PZO9272 (PZO9272) p. 7
**Foundry id:** `3vO9s9gtQcRAjNl2`

> *You utilize high-tech firearms to maximum effect.*
>
> **Prerequisites**: Dex 13, Exotic Weapon Proficiency (firearms), Point-Blank Shot
>
> **Benefits**: When you attack with a technological firearm that consumes charges, the save DC of any effect caused by that firearm increases by 1. If your bonuses from Point-Blank Shot apply, it increases by 2 instead.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `technology_adept` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Technophobe
*(feat)*

**Tags:** General
**Prerequisites:** Improved Sunder
**Source:** PZO9272 (PZO9272) p. 7
**Foundry id:** `4ZCIdXMHwxWABqK7`

> *Smashing technological abominations brings you joy.*
>
> **Prerequisites**: Improved Sunder
>
> **Benefits**: When you reduce a robot to 0 hit points or destroy a technological item possessed by an enemy, you receive a +2 morale bonus on ability checks, attack rolls, saving throws, and skill checks for a number of rounds equal to your Wisdom bonus (minimum 1 round). You receive this bonus for destroying an unattended object so long as it was in the possession of an enemy within the last round.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `technophobe` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Throw Anything
*(feat)*

**Tags:** Combat, Offensive, Weapon
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 135
**Foundry id:** `gGfXQq0IZrxdcZDx`

> *You are used to throwing things you have on hand.*
>
> **Benefits**: You do not suffer any penalties for using an improvised ranged weapon. You receive a +1 circumstance bonus on attack rolls made with thrown splash weapons.
>
> **Normal**: You take a -4 penalty on attack rolls made with an improvised weapon.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `throw_anything` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Tiring Critical
*(feat)*

**Tags:** Combat, Critical, Offensive
**Prerequisites:** Critical Focus, base attack bonus +13
**Source:** Core Rulebook (PZO1110) p. 114, 135
**Foundry id:** `0bpGtfB3ksWHe0lW`

> *Your critical hits cause opponents to become fatigued.*
>
> **Prerequisites**: Critical Focus, base attack bonus +13.
>
> **Benefits**: Whenever you score a critical hit, your opponent becomes fatigued. This feat has no additional effect on a fatigued or exhausted creature.
>
> **Special**: You can only apply the effects of one critical feat to a given critical hit unless you possess Critical Mastery.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `tiring_critical` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Toughness
*(feat)*

**Tags:** General, Defensive
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 116, 135
**Foundry id:** `8snLqsJN4LLL00Nq`

> *You have enhanced physical stamina.*
>
> **Benefits**: You gain +3 hit points. For every Hit Die you possess beyond 3, you gain an additional +1 hit point. If you have more than 3 Hit Dice, you gain +1 hit points whenever you gain a Hit Die (such as when you gain a level).

**Mechanical encoding:** `changes`: 1
  - `max(3, @attributes.hd.total)` → `mhp`  (untyped)

**In our coverage tracker:** `IMPLEMENTED` — +max(3, level) hp_max
**Manual verdict:** `[ ]`
**Notes:**

---

### Tower Shield Proficiency
*(feat)*

**Tags:** Combat
**Prerequisites:** Shield Proficiency
**Source:** Core Rulebook (PZO1110) p. 116, 135-136
**Foundry id:** `PxwM4Uf4mcYs3Auq`

> *You are trained in how to properly use a tower shield.*
>
> **Prerequisites**: Shield Proficiency.
>
> **Benefits**: When you use a tower shield, the shield's armor check penalty only applies to Strength and Dexterity-based skills.
>
> **Normal**: A character using a shield with which he is not proficient takes the shield's armor check penalty on attack rolls and on all skill checks that involve moving, including Ride.
>
> **Special**: Fighters automatically have Tower Shield Proficiency as a bonus feat. They need not select it.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `tower_shield_proficiency` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Trample
*(feat)*

**Tags:** Combat, Mount, Offensive, Movement, Combat Maneuver
**Prerequisites:** Ride 1 rank, Mounted Combat
**Source:** Core Rulebook (PZO1110) p. 115, 136
**Foundry id:** `8mS9B8Uc8odklIpl`

> *While mounted, you can ride down opponents and trample them under your mount.*
>
> **Prerequisites**: Ride 1 rank, Mounted Combat.
>
> **Benefits**: When you attempt to overrun an opponent while mounted, your target may not choose to avoid you. Your mount may make one hoof attack against any target you knock down, gaining the standard +4 bonus on attack rolls against prone targets.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `trample` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Trick Riding
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Ride 9 ranks, Mounted Combat
**Source:** Advanced Race Guide (PZO1131) p. 134; Advanced Player's Guide (PZO1115) p. 173
**Foundry id:** `tcBSikJXg2YhVXPF`

> *You are not only skilled at controlling a horse in combat; you can make it look like art.*
>
> **Prerequisites**: Ride 9 ranks, Mounted Combat.
>
> **Benefits**: While wearing light or no armor, you do not need to make Ride skill checks for any task listed in the Ride skill with a DC of 15 or lower. You do not take a -5 penalty for riding a mount bareback. You can make a check using Mounted Combat to negate a hit on your mount twice per round instead of just once.
>
> ##### Combat Trick
>
> As long as you have 1 stamina point in your stamina pool, you gain the effects of this feat when wearing medium armor.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `trick_riding` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Turn Undead
*(feat)*

**Tags:** Channeling
**Prerequisites:** Channel positive energy class feature
**Source:** Core Rulebook (PZO1110) p. 116, 136
**Foundry id:** `O7Dn4bXZtMW0UstG`

> *Calling upon higher powers, you cause undead to flee from the might of your unleashed divine energy.*
>
> **Prerequisites**: Channel positive energy class feature.
>
> **Benefits**: You can, as a standard action, use one of your uses of channel positive energy to cause all undead within 30 feet of you to flee, as if panicked. Undead receive a Will save to negate the effect. The DC for this Will save is equal to 10 + 1/2 your cleric level + your Charisma modifier. Undead that fail their save flee for 1 minute. Intelligent undead receive a new saving throw each round to end the effect. If you use channel energy in this way, it has no other effect (it does not heal or harm nearby creatures).

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `turn_undead` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Two-Handed Thrower
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Str 15
**Source:** Advanced Race Guide (PZO1131) p. 134; Bestiary (PZO1118) p. 123
**Foundry id:** `ZyqqdwtKnQncl5Fd`

> *You hurl weapons with both hands and with great force, sometimes using a whirling technique to send your weapon flying through the air at tremendous speeds.*
>
> **Prerequisites**: Str 15.
>
> **Benefits**: Whenever you use two hands to throw a one-handed or two-handed weapon, you gain a bonus on damage rolls equal to 1-1/2 times your Strength bonus. Using two hands to throw any weapon requires only a standard action for you. If you also have the Quick Draw feat, you can throw two-handed weapons at your full normal rate of attacks.
>
> **Normal**: You add your Strength bonus on thrown weapon damage, regardless of available hands. Throwing a two-handed weapon is a full-round action.
>
> ##### Combat Trick
>
> When you throw a one-handed thrown weapon with two hands or throw a two-handed thrown weapon, you can spend 2 stamina points to add twice your Strength bonus to that attack's damage instead of 1-1/2 times your Strength bonus.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `two_handed_thrower` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Two-Weapon Defense
*(feat)*

**Tags:** Combat, Weapon, Two Weapons, Defensive
**Prerequisites:** Dex 15, Two-Weapon Fighting
**Source:** Core Rulebook (PZO1110) p. 116, 136
**Foundry id:** `YDqp3yrAsuXh103W`

> *You are skilled at defending yourself while dual-wielding.*
>
> **Prerequisites**: Dex 15, Two-Weapon Fighting.
>
> **Benefits**: When wielding a double weapon or two weapons (not including natural weapons or unarmed strikes), you gain a +1 shield bonus to your AC.
>
> When you are fighting defensively or using the total defense action, this shield bonus increases to +2.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `two_weapon_defense` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Two-Weapon Feint
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Dex 15, Int 13, Combat Expertise, Two-Weapon Fighting
**Source:** Bestiary (PZO1118) p. 123; Advanced Race Guide (PZO1131) p. 135
**Foundry id:** `BTrciHHPtsTY01Hq`

> *You use one weapon to distract your enemy while slipping another past his defenses.*
>
> **Prerequisites**: Dex 15, Int 13, Combat Expertise, Two-Weapon Fighting.
>
> **Benefits**: While using Two-Weapon Fighting to make melee attacks, you can forgo your first primary-hand melee attack to make a Bluff check to feint an opponent.
>
> ##### Combat Trick
>
> You can select this feat even if you don't meet the ability score prerequisite (Intelligence 13). You gain the benefits of this feat only as long as you have at least 1 stamina point in your stamina pool. When using Two-Weapon Fighting to make a melee attack, you can spend 5 stamina points to forgo any one of your melee attacks (not just your first primary-hand attack) to attempt a Bluff check to feint an opponent. This feint attempt occurs before all of your attacks, even if you give up a later attack.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `two_weapon_feint` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Two-Weapon Fighting
*(feat)*

**Tags:** Combat, Weapon, Two Weapons, Offensive
**Prerequisites:** Dex 15
**Source:** Core Rulebook (PZO1110) p. 116, 136
**Foundry id:** `Ee7JHADKEK37tTHs`

> *You can fight with a weapon wielded in each of your hands. You can make one extra attack each round with the secondary weapon.*
>
> **Prerequisites**: Dex 15.
>
> **Benefits**: Your penalties on attack rolls for fighting with two weapons are reduced. The penalty for your primary hand lessens by 2 and the one for your off hand lessens by 6. See Two-Weapon Fighting in Combat.
>
> **Normal**: If you wield a second weapon in your off hand, you can get one extra attack per round with that weapon. When fighting in this way you suffer a -6 penalty with your regular attack or attacks with your primary hand and a -10 penalty to the attack with your off hand. If your off-hand weapon is light, the penalties are reduced by 2 each. An unarmed strike is always considered light.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `NOT_IMPLEMENTED` — extra off-hand attack with reduced penalties
**Manual verdict:** `[ ]`
**Notes:**

---

### Two-Weapon Rend
*(feat)*

**Tags:** Combat, Weapon, Two Weapons, Offensive
**Prerequisites:** Dex 17, Double Slice, Improved Two-Weapon Fighting, Two-Weapon Fighting, base attack bonus +11
**Source:** Core Rulebook (PZO1110) p. 116, 136
**Foundry id:** `tGDNVHHZnNFPPgiY`

> *Striking with both of your weapons simultaneously, you can use them to deliver devastating wounds.*
>
> **Prerequisites**: Dex 17, Double Slice, Improved Two-Weapon Fighting, Two-Weapon Fighting, base attack bonus +11.
>
> **Benefits**: If you hit an opponent with both your primary hand and your off-hand weapon, you deal an additional 1d10 points of damage plus 1-1/2 times your Strength modifier. You can only deal this additional damage once each round.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `two_weapon_rend` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Unseat
*(feat)*

**Tags:** Combat, Mount, Movement, Offensive, Combat Maneuver
**Prerequisites:** Str 13, Ride 1 rank, Mounted Combat, Power Attack, Improved Bull Rush, base attack bonus +1
**Source:** Core Rulebook (PZO1110) p. 115, 136
**Foundry id:** `4fAgch4ut1JYPBbL`

> *You are skilled at unseating your mounted opponents.*
>
> **Prerequisites**: Str 13, Ride 1 rank, Mounted Combat, Power Attack, Improved Bull Rush, base attack bonus +1.
>
> **Benefits**: When charging an opponent while mounted and wielding a lance, resolve the attack as normal. If it hits, you may immediately make a free bull rush attempt in addition to the normal damage. If successful, the target is knocked off his horse and lands prone in a space adjacent to his mount that is directly away from you.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `unseat` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Versatile Summon Monster
*(feat)*

**Tags:** —
**Prerequisites:** Knowledge (arcana) 1 rank, Knowledge (planes) 1 rank
**Source:** PZO9458 (PZO9458) p. 18
**Foundry id:** `ezNxW33BtSafLl0J`

> *You've learned to summon a more diverse array of monsters.*
>
> **Prerequisites**: Knowledge (arcana) 1 rank, Knowledge (planes) 1 rank.
>
> **Benefit**: Pick any two templates from the following list (see Simple Summoning Templates on @Source[PZO9458;pages=18]): @UUID[Compendium.pf1.monster-templates.Item.Ovo97rjBymtgkjdH], @UUID[Compendium.pf1.monster-templates.Item.xXxuV1C3GQrAgvE9], @UUID[Compendium.pf1.monster-templates.Item.TIsuPNyZbmvj0Jdx], @UUID[Compendium.pf1.monster-templates.Item.8wcgAdUOucEtYJcD], @UUID[Compendium.pf1.monster-templates.Item.ubKX7esqMFnhbExt], or @UUID[Compendium.pf1.monster-templates.Item.gMtxmfemM0rZFyZO]. When you summon one or more creatures that would normally be available with the celestial, entropic, fiendish, or resolute template using a summon monster spell (or an effect that mimics such a spell), you can instead apply one of the chosen templates to each creature. You can apply a different template to each creature you summon.
>
> **Special**: You can select this feat more than once. Each time you do, you can choose an additional two templates.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `versatile_summon_monster` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Versatile Summon Nature's Ally
*(feat)*

**Tags:** —
**Prerequisites:** @UUID[Compendium.pf1.feats.Item.7bJjKqNRrvpXJ4L3], @UUID[Compendium.pf1.feats.Item.V2zY7BltkpSXwejy] (conjuration), Knowledge (nature) 1 rank, Knowledge (planes) 1 rank
**Source:** PZO9458 (PZO9458) p. 18
**Foundry id:** `R5nnb83RW7qHkVmA`

> *You've learned to summon a wider array of creatures.*
>
> **Prerequisites**: @UUID[Compendium.pf1.feats.Item.7bJjKqNRrvpXJ4L3], @UUID[Compendium.pf1.feats.Item.V2zY7BltkpSXwejy] (conjuration), Knowledge (nature) 1 rank, Knowledge (planes) 1 rank.
>
> **Benefit**: When you summon one or more animals, humanoids, or vermin using a summon nature's ally spell (or an effect that mimics such a spell), instead of granting them the benefit from Augment Summoning, you can instead apply one of the following templates to them: @UUID[Compendium.pf1.monster-templates.Item.Ovo97rjBymtgkjdH], @UUID[Compendium.pf1.monster-templates.Item.xXxuV1C3GQrAgvE9], @UUID[Compendium.pf1.monster-templates.Item.TIsuPNyZbmvj0Jdx], @UUID[Compendium.pf1.monster-templates.Item.ubKX7esqMFnhbExt], or @UUID[Compendium.pf1.monster-templates.Item.gMtxmfemM0rZFyZO]. If you summon multiple creatures with one casting, they must all have the same template.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `versatile_summon_nature_s_ally` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Vicious Stomp
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Combat Reflexes, Improved Unarmed Strike
**Source:** Bestiary (PZO1118) p. 123
**Foundry id:** `r0oGCxDYVKC5NJF9`

> *You take advantage of the moment to brutally kick an enemy when he is down.*
>
> **Prerequisites**: Combat Reflexes, Improved Unarmed Strike.
>
> **Benefit**: Whenever an opponent falls prone adjacent to you, that opponent provokes an attack of opportunity from you. This attack must be an unarmed strike.
>
> ##### Combat Trick
>
> When an opponent provokes an unarmed strike attack of opportunity from you by falling prone, you can spend 2 stamina points to deal an additional 1d6 points of damage with that unarmed strike.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `vicious_stomp` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Vital Strike
*(feat)*

**Tags:** Combat, Offensive
**Prerequisites:** Base attack bonus +6
**Source:** Core Rulebook (PZO1110) p. 117, 136
**Foundry id:** `26k1Gi7t5BoqxhIj`

> *You make a single attack that deals significantly more damage than normal.*
>
> **Prerequisites**: Base attack bonus +6.
>
> **Benefits**: When you use the attack action, you can make one attack at your highest base attack bonus that deals additional damage. Roll the weapon's damage dice for the attack twice and add the results together before adding bonuses from Strength, weapon abilities (such as *flaming*), precision based damage, and other damage bonuses. These extra weapon damage dice are not multiplied on a critical hit, but are added to the total.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `vital_strike` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Wave Strike
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Weapon expertise class feature or Quick Draw, Bluff 1 rank
**Source:** Advanced Race Guide (PZO1131) p. 135; Bestiary (PZO1118) p. 123
**Foundry id:** `TEK26tHXdje9NV4Y`

> *You present a serene facade until you unsheathe your weapon and strike in one fluid motion.*
>
> **Prerequisites**: Weapon expertise class feature or Quick Draw, Bluff 1 rank.
>
> **Benefits**: If on your first turn of combat you draw a melee weapon to attack an opponent within your reach, you can spend a swift action to make a Bluff check to feint against that opponent.
>
> ##### Combat Trick
>
> You can spend 2 stamina points to use this feat on your second or subsequent turns in a combat. You can use this combat trick only once per combat, though you can use it in addition to using the feat on your first turn.

**Mechanical encoding:** has `actions`, has `scriptCalls`

**In our coverage tracker:** absent (slug `wave_strike` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Weapon Finesse
*(feat)*

**Tags:** Combat, Weapon
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 117, 136
**Foundry id:** `vWiTqHC4Y3Xn1Pme`

> *You are trained in using your agility in melee combat, as opposed to brute strength.*
>
> **Benefits**: With a light weapon, rapier, whip, or spiked chain made for a creature of your size category, you may use your Dexterity modifier instead of your Strength modifier on attack rolls. If you carry a shield, its armor check penalty applies to your attack rolls.
>
> **Special**: Natural weapons are considered light weapons.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `IMPLEMENTED` — use Dex for melee attack rolls; via combatant.is_finesse path
**Manual verdict:** `[ ]`
**Notes:**

---

### Weapon Focus
*(feat)*

**Tags:** Combat, Weapon, Offensive
**Prerequisites:** Proficiency with selected weapon, base attack bonus +1
**Source:** Core Rulebook (PZO1110) p. 117, 136
**Foundry id:** `n250dFlbykAIAg5Z`

> *Choose one type of weapon. You can also choose unarmed strike or grapple (or ray, if you are a spellcaster) as your weapon for the purposes of this feat.*
>
> **Prerequisites**: Proficiency with selected weapon, base attack bonus +1.
>
> **Benefits**: You gain a +1 bonus on all attack rolls you make using the selected weapon.
>
> **Special**: You can gain this feat multiple times. Its effects do not stack. Each time you take the feat, it applies to a new type of weapon.

*No mechanical encoding — prose only.*

**In our coverage tracker:** `IMPLEMENTED` — +1 attack with chosen weapon (parametric)
**Manual verdict:** `[ ]`
**Notes:**

---

### Weapon Specialization
*(feat)*

**Tags:** Combat, Weapon, Offensive
**Prerequisites:** Proficiency with selected weapon, Weapon Focus with selected weapon, fighter level 4th
**Source:** Core Rulebook (PZO1110) p. 117, 137
**Foundry id:** `YLCvMNeAF9V31m1h`

> *You are skilled at dealing damage with one weapon. Choose one type of weapon (including unarmed strike or grapple) for which you have already selected the Weapon Focus feat. You deal extra damage when using this weapon.*
>
> **Prerequisites**: Proficiency with selected weapon, Weapon Focus with selected weapon, fighter level 4th.
>
> **Benefits**: You gain a +2 bonus on all damage rolls you make using the selected weapon.
>
> **Special**: You can gain this feat multiple times. Its effects do not stack. Each time you take the feat, it applies to a new type of weapon.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `weapon_specialization` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Whip Mastery
*(feat)*

**Tags:** Combat, Combat Trick
**Prerequisites:** Weapon Focus (whip), base attack bonus +2
**Source:** Bestiary (PZO1118) p. 123; Advanced Race Guide (PZO1131) p. 135
**Foundry id:** `pUmoxJHnoITAStYq`

> *Your superior expertise with this weapon does not provoke attacks of opportunity from your enemies.*
>
> **Prerequisites**: Weapon Focus (whip), base attack bonus +2.
>
> **Benefits**: You no longer provoke attacks of opportunity when attacking with a whip. You can deal lethal damage with a whip, although you can still deal nonlethal damage when you want. Further, you can deal damage with a whip despite a creature's armor bonus or natural armor bonus.
>
> **Normal**: Attacking with a whip provokes attacks of opportunity as if you used a ranged weapon. A whip deals no damage to a creature that has an armor bonus of +1 or natural armor bonus of +3.
>
> ##### Combat Trick
>
> When using a whip to deal nonlethal damage, as long as you have at least 1 stamina point in your stamina pool, the whip deals 1d8 points of nonlethal damage (1d6 for a Small whip). At the start of your turn, you can spend 2 stamina points to increase the damage die of the whip as if it were one size category larger for your next attack, regardless of whether you are dealing lethal or nonlethal damage. For nonlethal attacks, these two increases stack. This effect doesn't stack with other effects that treat the weapon as a larger size category unless they increase the actual size.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `whip_mastery` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Whirlwind Attack
*(feat)*

**Tags:** Combat, Offensive
**Prerequisites:** Dex 13, Int 13, Combat Expertise, Dodge, Mobility, Spring Attack, base attack bonus +4
**Source:** Core Rulebook (PZO1110) p. 114, 137
**Foundry id:** `UnmST9BvRhxT4vq3`

> *You can strike out at every foe within reach.*
>
> **Prerequisites**: Dex 13, Int 13, Combat Expertise, Dodge, Mobility, Spring Attack, base attack bonus +4.
>
> **Benefits**: When you use the full-attack action, you can give up your regular attacks and instead make one melee attack at your highest base attack bonus against each opponent within reach. You must make a separate attack roll against each opponent.
>
> When you use the Whirlwind Attack feat, you also forfeit any bonus or extra attacks granted by other feats, spells, or abilities.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `whirlwind_attack` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Widen Spell
*(feat)*

**Tags:** Metamagic, Magic
**Prerequisites:** —
**Source:** Core Rulebook (PZO1110) p. 117, 137
**Foundry id:** `h8Ap9cxdsXWRC6Tc`

> *You can cast your spells so that they occupy a larger space.*
>
> **Benefits**: You can alter a burst, emanation, or spread-shaped spell to increase its area. Any numeric measurements of the spell's area increase by 100%. A widened spell uses up a spell slot three levels higher than the spell's actual level.
>
> Spells that do not have an area of one of these four sorts are not affected by this feat.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `widen_spell` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Wind Stance
*(feat)*

**Tags:** Combat, Defensive, Movement
**Prerequisites:** Dex 15, Dodge, base attack bonus +6
**Source:** Core Rulebook (PZO1110) p. 114, 137
**Foundry id:** `9p0aAtCyLdcwnftS`

> *Your erratic movements make it difficult for enemies to pinpoint your location.*
>
> **Prerequisites**: Dex 15, Dodge, base attack bonus +6.
>
> **Benefits**: If you move more than 5 feet this turn, you gain 20% concealment for 1 round against ranged attacks.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `wind_stance` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Wingover
*(feat)*

**Tags:** General
**Prerequisites:** Fly speed
**Source:** PZO1112 (PZO1112) p. 316
**Foundry id:** `V041fsvlhNcFhz5k`

> *This creature can make turns with ease while flying.*
>
> **Prerequisites**: Fly speed.
>
> **Benefits**: Once each round, a creature with this feat can turn up to 180 degrees as a free action without making a Fly skill check. This free turn does not consume any additional movement from the creature.
>
> **Normal**: A flying creature can turn up to 90 degrees by making a DC 15 Fly skill check and expending 5 feet of movement. A flying creature can turn up to 180 degrees by making a DC 20 Fly skill check and expending 10 feet of movement.

**Mechanical encoding:** has `actions`

**In our coverage tracker:** absent (slug `wingover` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

### Wrest Charge
*(feat)*

**Tags:** General
**Prerequisites:** Disable Device 5 ranks, Knowledge (engineering) 5 ranks
**Source:** PZO9272 (PZO9272) p. 7
**Foundry id:** `UatLCbhallkclT6U`

> *You can extract a charge from otherwise depleted technology.*
>
> **Prerequisites**: Disable Device 5 ranks, Knowledge (engineering) 5 ranks
>
> **Benefits**: With a successful DC 20 Disable Device check, you can jury-rig a depleted (but not destroyed) battery so it provides 1 more charge. Using this charge or failing your check by 5 or more permanently depletes the battery. 
>
> You can attempt the same check to add 1 last charge to a discharged piece of timeworn technology. Regardless of the outcome, no other attempts can be made, even by another person. Using this feat takes 1 minute. You can attempt to wrest a charge as a move action by taking a -10 penalty on your check. This feat does not stack with the charge cycling deed.

*No mechanical encoding — prose only.*

**In our coverage tracker:** absent (slug `wrest_charge` not in `coverage.FEATS`)
**Manual verdict:** `[ ]`
**Notes:**

---

