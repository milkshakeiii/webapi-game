"""The runtime view of a participant in combat.

A ``Combatant`` is the *mutable* view that lives on the grid: HP, active
conditions, position, expended-resource counters, and the modifier
collection that drives every derived stat. Static data — race, class,
level-up plan, monster template — is referenced via ``template``; the
Combatant never mutates it.

Two factories build Combatants:

- ``combatant_from_monster(monster, position, team)`` — full-featured;
  monsters carry their full stat block in content.
- ``combatant_from_character(character, registry, position, team)`` —
  partial; awaits the equipment catalog before attack options can be
  computed automatically.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from .characters import (
    AbilityScores,
    Character,
    apply_racial_modifiers,
    racial_ability_modifiers,
)
from .combat import DefenseProfile
from .content import ContentRegistry, Monster
from .modifiers import Modifier, ModifierCollection, compute, mod
from .sizes import get_size, size_modifiers


# ---------------------------------------------------------------------------
# Combatant
# ---------------------------------------------------------------------------


# Filters used to derive situational AC values.
_TOUCH_EXCLUDED_TYPES = frozenset({"armor", "shield", "natural"})


@dataclass
class Combatant:
    """Runtime state for a single combat participant."""

    id: str
    name: str
    team: str             # for friend/foe checks; same team = ally
    size: str
    speed: int            # base land speed in feet
    reach_class: str      # "tall" or "long" — determines natural reach

    # Bases are inherent values for this combatant, before any typed
    # modifiers apply. Examples: AC base is 10; CMD base is 10 + BAB;
    # CMB base is BAB.
    bases: dict[str, int]

    # Every typed modifier from race, class, equipment, conditions,
    # spells, etc. is in here.
    modifiers: ModifierCollection

    # Pre-built attack options. For monsters these come from the JSON
    # stat block; for characters they're computed from equipment (TBD).
    attack_options: list[dict]

    # Mutable state.
    current_hp: int
    max_hp: int
    position: tuple[int, int]
    facing: str = "north"
    conditions: set[str] = field(default_factory=set)
    resources: dict[str, int] = field(default_factory=dict)

    # Reference back to the source data.
    template_kind: str = "unknown"   # "monster" or "character"
    template: Any = None             # Monster or Character

    # Spells the combatant can cast (filtered to their class list at
    # levels they have slots for). Empty for non-casters and monsters.
    castable_spells: set[str] = field(default_factory=set)

    # Casting model: "spontaneous" (sorcerer / bard / oracle) or
    # "prepared" (wizard / cleric / druid / paladin / ranger / witch
    # / magus). Determines how _do_cast consumes spells:
    #   - spontaneous: any spell in castable_spells of legal level
    #     can be cast; only the slot is consumed.
    #   - prepared: the spell must be in prepared_spells[level], and
    #     casting consumes both the slot AND one entry from that list
    #     (re-cast requires preparing the spell again).
    # ``""`` means non-caster / not modeled — spells fall through the
    # spontaneous path.
    casting_type: str = ""

    # Per-level list of prepared spell IDs. Populated at construction
    # for prepared casters from Character.spells_prepared (or class
    # defaults if the character didn't pre-pick). Duplicates allowed.
    prepared_spells: dict[int, list[str]] = field(default_factory=dict)

    # Smite target id (paladin Smite Evil declared target). Empty when none.
    smite_target_id: str | None = None

    # Damage reduction: ``(amount, bypass_keywords)`` or ``None``. Read
    # by ``defense_profile()`` and applied by combat.resolve_attack.
    damage_reduction: tuple[int, frozenset[str]] | None = None

    # PF1 RAW: a creature dies when HP drops to a negative amount equal
    # to its Constitution score. Cached at construction time from
    # template data. Undead and constructs are destroyed at HP 0
    # (threshold = 0). Default fallback -10 (3.5e behavior) for
    # combatants built without enough info.
    death_threshold: int = -10

    # Per-round AoO bookkeeping for Combat Reflexes. Reset by
    # turn_executor when ``aoos_used_this_round_marker`` doesn't
    # match the current round. Default limit is 1 AoO/round; Combat
    # Reflexes raises it by the combatant's Dex modifier.
    aoos_used_this_round: int = 0
    aoos_used_round_marker: int = -1

    # Per-combatant feat overrides — feats granted at runtime that
    # aren't in the underlying template (e.g., level-up plan grants,
    # test injections). Read alongside ``template.feats`` by
    # ``turn_executor._has_feat``.
    extra_feats: list[str] = field(default_factory=list)

    # Conditions this combatant is immune to (e.g., undead are immune
    # to "stunned", "paralyzed", "charmed", etc.). Populated at
    # construction from racial traits / monster type. Consumers that
    # apply conditions (``add_condition``, spell handlers, stunning
    # fist) check this set first and skip the application if matched.
    condition_immunities: set[str] = field(default_factory=set)

    # Weapon proficiency categories (e.g. ``{"simple", "martial"}``).
    # Populated at construction from class data. Empty set means
    # "proficiency not modeled here" (e.g., natural-attack monsters).
    # Read by ``turn_executor._weapon_not_proficient`` to apply the
    # -4 attack penalty when wielding a non-proficient weapon.
    weapon_proficiency_categories: set[str] = field(default_factory=set)

    # Armor proficiency: which armor categories the actor can wear
    # without penalty. Categories: "light", "medium", "heavy",
    # "shields_normal", "shield_tower". Empty set = "not modeled here"
    # (monsters / natural-armor creatures). Read by
    # ``turn_executor._armor_not_proficient`` to apply the armor-check
    # penalty as a flat attack penalty.
    armor_proficiency_categories: set[str] = field(default_factory=set)

    # Generic bleed damage: HP lost per round (top of the actor's
    # turn) until healed. Stops when the combatant receives any
    # healing or successful Heal-skill DC 15 stabilization. Set
    # externally by spell handlers / weapon special properties.
    # ``ferocity`` and ``dying`` bleed are tracked separately in
    # tick_round (those are PF1 RAW, this is the generic
    # condition-based bleed for things like wounding weapons,
    # bleeding critical, etc.).
    bleed: int = 0

    # Fast healing: HP automatically restored each round (capped by
    # max_hp). Applied in ``tick_round``.
    fast_healing: int = 0

    # Regeneration: HP/round; like fast_healing but the creature also
    # cannot die from non-bypassed damage (it falls to negative HP and
    # stays there until the bypass-type damage finishes the kill).
    # ``regeneration_bypass`` lists the damage-type keywords that DO
    # finish the kill (e.g., ``frozenset({"fire", "acid"})`` for trolls).
    # The "treat-non-bypass-damage-as-nonlethal" semantics aren't yet
    # modeled; v1 just heals each round.
    regeneration: int = 0
    regeneration_bypass: frozenset[str] = field(default_factory=frozenset)

    # Mount / rider link. While ``mount_id`` is set on this combatant,
    # the combatant is riding that mount: its ``position`` mirrors the
    # mount's position, and the grid no longer carries the rider as a
    # separate occupancy. ``rider_id`` is the inverse — set on the
    # mount while it carries a rider. See dnd/engine/turn_executor.py
    # ``_do_mount`` / ``_do_dismount``.
    mount_id: str | None = None
    rider_id: str | None = None

    # Energy resistance: ``{damage_type: amount}`` (e.g.,
    # ``{"fire": 10}`` reduces fire damage by 10/hit, min 0).
    # Energy immunity: ``{damage_type, ...}`` — completely ignores
    # damage of these types. Read by spells.apply_typed_damage.
    energy_resistance: dict[str, int] = field(default_factory=dict)
    energy_immunity: set[str] = field(default_factory=set)

    # Concealment: percentage miss chance an attacker rolls against
    # this combatant (0 = none, 20 = standard concealment, 50 = total
    # concealment). Read by turn_executor._do_attack: after the
    # attack roll, if outcome.hit, roll 1d100; if ≤ concealment, the
    # attack misses despite the to-hit. Default 0; set externally
    # (invisibility, dim light, etc. when those subsystems wire in).
    concealment: int = 0

    # Per-source-tracking of conditions applied by ongoing effects.
    # Spell handlers that call ``add_condition`` should also call
    # ``register_sourced_condition(source, condition_id)`` so dispel /
    # spell-removal can find and clear those conditions. The mapping
    # is ``source → set of condition_ids``. Modifiers already carry
    # their own source on the Modifier record; this dict is just for
    # conditions, which are otherwise plain strings in the set.
    sourced_conditions: dict[str, set[str]] = field(default_factory=dict)

    # ── Derived stat queries ──────────────────────────────────────────────

    def ac(self, situation: str = "normal") -> int:
        """Return AC for the given situation: ``normal``, ``touch``, or
        ``flat_footed``."""
        mods = list(self.modifiers.for_target("ac"))
        if situation == "touch":
            mods = [m for m in mods if m.type not in _TOUCH_EXCLUDED_TYPES]
        elif situation == "flat_footed":
            mods = [
                m for m in mods
                if m.type != "dodge" and "dex" not in m.source.lower()
            ]
        elif situation != "normal":
            raise ValueError(f"unknown AC situation {situation!r}")
        return compute(self.bases.get("ac", 10), mods)

    def save(self, kind: str, context: dict | None = None) -> int:
        """Return Fort/Ref/Will save total.

        ``context`` is the qualifier-evaluation context (e.g.
        ``{"effect_tags": ["poison"]}``). Pass it when situational
        save bonuses (hardy vs poison, illusion_resistance vs
        illusion) should apply. With no context, only unconditional
        save modifiers contribute.
        """
        if kind not in ("fort", "ref", "will"):
            raise ValueError(f"unknown save kind {kind!r}")
        target = f"{kind}_save"
        from .modifiers import compute_with_context
        return compute_with_context(
            self.bases.get(target, 0),
            self.modifiers.for_target(target),
            context or {},
        )

    def cmb(self, context: dict | None = None) -> int:
        from .modifiers import compute_with_context
        return compute_with_context(
            self.bases.get("cmb", 0),
            self.modifiers.for_target("cmb"),
            context or {},
        )

    def cmd(self, context: dict | None = None) -> int:
        """Maneuver Defense.

        ``context`` is forwarded to the qualifier check, so situational
        bonuses like dwarven Stability (+4 CMD vs trip/bullrush) only
        apply when the resolving maneuver matches.
        """
        from .modifiers import compute_with_context
        return compute_with_context(
            self.bases.get("cmd", 10),
            self.modifiers.for_target("cmd"),
            context or {},
        )

    def skill_total(self, skill_id: str) -> int:
        target = f"skill:{skill_id}"
        return compute(0, self.modifiers.for_target(target))

    def initiative_modifier(self) -> int:
        return compute(self.bases.get("initiative", 0),
                       self.modifiers.for_target("initiative"))

    def defense_profile(self) -> DefenseProfile:
        """Bundle the AC values for combat resolution."""
        return DefenseProfile(
            ac=self.ac("normal"),
            touch_ac=self.ac("touch"),
            flat_footed_ac=self.ac("flat_footed"),
            dr=self.damage_reduction,
        )

    @property
    def hp_pct(self) -> float:
        return (self.current_hp / self.max_hp) if self.max_hp else 0.0

    # ── Liveness ──────────────────────────────────────────────────────────

    def is_alive(self) -> bool:
        return "dead" not in self.conditions

    def is_dying(self) -> bool:
        return "dying" in self.conditions

    def is_unconscious(self) -> bool:
        return "unconscious" in self.conditions or "dying" in self.conditions

    def is_immune_to_bleed(self) -> bool:
        """Undead and constructs ignore bleed effects per PF1.

        Used by ``tick_round`` to skip ferocity-bleed and dying-bleed
        for these creature types. Living creatures are always
        susceptible.
        """
        if self.template_kind != "monster" or self.template is None:
            return False
        mtype = (getattr(self.template, "type", "") or "").lower()
        return mtype in ("undead", "construct")

    # ── Mutations ─────────────────────────────────────────────────────────

    def take_damage(self, amount: int) -> None:
        if amount < 0:
            raise ValueError(f"damage must be >= 0, got {amount}")
        self.current_hp -= amount

    def heal(self, amount: int) -> None:
        if amount < 0:
            raise ValueError(f"heal must be >= 0, got {amount}")
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def add_condition(self, condition_id: str) -> bool:
        """Apply ``condition_id`` unless the combatant is immune.

        Returns True when the condition was actually applied, False
        when blocked by an immunity or because a stronger tier of the
        condition is already in effect (e.g., applying ``fatigued``
        when ``exhausted`` is already present is a no-op).

        Side effects: certain conditions add typed modifiers / mutate
        speed when applied, and the matching ``remove_condition`` undoes
        those side effects. See ``_on_condition_applied``.
        """
        if self.is_immune_to_condition(condition_id):
            return False
        # Fatigued is masked by the stronger exhausted tier.
        if condition_id == "fatigued" and "exhausted" in self.conditions:
            return False
        if condition_id in self.conditions:
            return True  # already present, no double-application
        self.conditions.add(condition_id)
        self._on_condition_applied(condition_id)
        return True

    def is_immune_to_condition(self, condition_id: str) -> bool:
        return condition_id in self.condition_immunities

    def remove_condition(self, condition_id: str) -> None:
        if condition_id not in self.conditions:
            return
        self.conditions.discard(condition_id)
        self._on_condition_removed(condition_id)
        # Drop the source-tracking entry too, if any.
        for src, conds in list(self.sourced_conditions.items()):
            conds.discard(condition_id)
            if not conds:
                del self.sourced_conditions[src]

    def register_sourced_condition(self, source: str, condition_id: str) -> None:
        """Mark ``condition_id`` as having been added by ``source``.

        Used by spell handlers so dispel-style cleanup can find which
        conditions came from a given spell source. Idempotent.
        """
        self.sourced_conditions.setdefault(source, set()).add(condition_id)

    def remove_effects_from_source(self, source: str) -> tuple[int, list[str]]:
        """Drop every modifier and tracked condition from ``source``.

        Returns ``(modifier_count_removed, condition_ids_removed)``.
        Used by dispel magic and similar effect-ending spells.
        """
        mod_count = self.modifiers.remove_by_source(source)
        cond_ids = list(self.sourced_conditions.pop(source, set()))
        for cid in cond_ids:
            if cid in self.conditions:
                self.conditions.discard(cid)
                self._on_condition_removed(cid)
        return mod_count, cond_ids

    def _on_condition_applied(self, condition_id: str) -> None:
        """Apply the mechanical side effects of a newly-added condition.

        Penalties are added as typed modifiers sourced under the
        condition name so that ``remove_condition`` can clear them with
        ``modifiers.remove_by_source``.
        """
        if condition_id == "fatigued":
            self.modifiers.add(Modifier(value=-2, type="untyped",
                                        target="ability:str",
                                        source="fatigued"))
            self.modifiers.add(Modifier(value=-2, type="untyped",
                                        target="ability:dex",
                                        source="fatigued"))
        elif condition_id == "exhausted":
            # Exhausted supersedes fatigued. Drop any existing fatigued
            # state before applying the heavier penalty.
            if "fatigued" in self.conditions:
                self.conditions.discard("fatigued")
                self.modifiers.remove_by_source("fatigued")
            self.modifiers.add(Modifier(value=-6, type="untyped",
                                        target="ability:str",
                                        source="exhausted"))
            self.modifiers.add(Modifier(value=-6, type="untyped",
                                        target="ability:dex",
                                        source="exhausted"))
            self.speed = self.speed // 2
        elif condition_id == "grappled":
            self.modifiers.add(Modifier(value=-2, type="untyped",
                                        target="attack",
                                        source="grappled"))
            self.modifiers.add(Modifier(value=-4, type="untyped",
                                        target="ability:dex",
                                        source="grappled"))

    def _on_condition_removed(self, condition_id: str) -> None:
        """Undo the side effects of a condition that's leaving."""
        if condition_id == "fatigued":
            self.modifiers.remove_by_source("fatigued")
        elif condition_id == "exhausted":
            self.modifiers.remove_by_source("exhausted")
            self.speed = self.speed * 2
        elif condition_id == "grappled":
            self.modifiers.remove_by_source("grappled")

    def add_modifier(self, modifier: Modifier) -> None:
        self.modifiers.add(modifier)

    def remove_modifiers_from_source(self, source: str) -> int:
        return self.modifiers.remove_by_source(source)

    def tick_round(self, current_round: int, roller=None) -> list[Modifier]:
        """End-of-round housekeeping.

        Order:
          1. Prune expired modifiers.
          2. Expire timed conditions (stunned via side-channel
             ``stunned_until_round``).
          3. Apply per-round HP losses: ferocity bleed, dying bleed.
             A dying creature first attempts a DC 10 Constitution
             check (if a roller is provided) to stabilize and
             suppress the bleed.
          4. Apply per-round HP gains: fast healing, regeneration.

        ``roller``: optional. When provided, dying combatants roll a
        DC 10 Con stabilization check; on success, the ``stable``
        condition is added (which suppresses the bleed below).
        """
        expired = self.modifiers.prune_expired(current_round)
        stun_until = self.resources.get("stunned_until_round")
        if stun_until is not None and current_round >= stun_until:
            self.remove_condition("stunned")
            del self.resources["stunned_until_round"]
        bleed_immune = self.is_immune_to_bleed()
        # Stabilization check: dying creature rolls Con vs DC 10.
        if (
            roller is not None
            and "dying" in self.conditions
            and "stable" not in self.conditions
            and "dead" not in self.conditions
        ):
            r = roller.roll("1d20")
            nat = r.terms[0].rolls[0]
            con_score = self._read_con_score()
            con_mod = (con_score - 10) // 2 if con_score > 0 else 0
            if nat + con_mod >= 10:
                self.add_condition("stable")
        # PF1 ferocity: a creature kept conscious below 0 HP bleeds
        # 1 HP per round until killed outright.
        if (
            "ferocity_active" in self.conditions
            and self.current_hp <= 0
            and not bleed_immune
        ):
            self.current_hp -= 1
            if self.current_hp <= self.death_threshold:
                self.add_condition("dead")
                self.remove_condition("ferocity_active")
                self.remove_condition("staggered")
                self.remove_condition("dying")
        # PF1 dying: a dying creature loses 1 HP per round and dies
        # when it reaches its negative-Con threshold. Stable suppresses
        # the loss.
        elif (
            "dying" in self.conditions
            and "stable" not in self.conditions
            and "dead" not in self.conditions
            and not bleed_immune
        ):
            self.current_hp -= 1
            if self.current_hp <= self.death_threshold:
                self.add_condition("dead")
                self.remove_condition("dying")
        # Generic bleed damage. PF1 RAW: stops when the creature
        # receives any healing — but tick_round runs healing at the
        # end of the turn, so bleed applies first this round (it
        # stops next round once the heal lands).
        if (
            self.bleed > 0
            and "dead" not in self.conditions
            and not bleed_immune
        ):
            self.current_hp -= self.bleed
            if self.current_hp <= self.death_threshold:
                self.add_condition("dead")
                self.bleed = 0
        # Per-round healing.
        if "dead" not in self.conditions and self.current_hp < self.max_hp:
            heal = self.fast_healing + self.regeneration
            if heal > 0:
                self.current_hp = min(self.max_hp, self.current_hp + heal)
                # Any healing stops bleed.
                if self.bleed > 0:
                    self.bleed = 0
        return expired

    def _read_con_score(self) -> int:
        """Read the combatant's effective Constitution score.

        Used by the stabilization check. Returns 0 when no Con score
        applies (undead, constructs).
        """
        if self.template is None:
            return 10
        if self.template_kind == "monster":
            scores = getattr(self.template, "ability_scores", None) or {}
            return int(scores.get("con", 10) or 0)
        if self.template_kind == "character":
            base = self.template.base_ability_scores.get("con") or 10
            for m in self.modifiers.for_target("ability:con"):
                base += m.value
            return int(base)
        return 10


# ---------------------------------------------------------------------------
# Factories
# ---------------------------------------------------------------------------


def _new_id() -> str:
    return f"combatant_{uuid.uuid4().hex[:8]}"


def _parse_dr_trait(trait_id: str) -> tuple[int, frozenset[str]] | None:
    """Parse a racial-trait ID like ``dr_5_bludgeoning`` into the
    ``DefenseProfile.dr`` tuple ``(amount, bypass_keywords)``.

    Examples:
      ``dr_5_bludgeoning`` → ``(5, frozenset({"bludgeoning"}))``
      ``dr_10_silver``     → ``(10, frozenset({"silver"}))``

    Returns ``None`` if the ID isn't a DR trait. Multi-keyword DRs
    (e.g., ``DR 10/silver and magic``) aren't yet expressible in the
    bypass-keyword set semantics; they need a richer model.
    """
    if not trait_id.startswith("dr_"):
        return None
    parts = trait_id.split("_")
    if len(parts) < 3:
        return None
    try:
        amount = int(parts[1])
    except ValueError:
        return None
    return amount, frozenset(parts[2:])


def _monster_damage_reduction(
    monster: Monster,
) -> tuple[int, frozenset[str]] | None:
    """Walk the monster's racial_traits and return the first DR found."""
    for t in monster.racial_traits or []:
        if not isinstance(t, dict):
            continue
        parsed = _parse_dr_trait(t.get("id", ""))
        if parsed is not None:
            return parsed
    return None


def _monster_death_threshold(monster: Monster) -> int:
    """PF1 RAW: HP <= -CON kills a living creature.

    Undead and constructs have no Con score and are destroyed when
    reduced to 0 HP — return 0 for them.
    """
    mtype = (monster.type or "").lower()
    if mtype in ("undead", "construct"):
        return 0
    con = int((monster.ability_scores or {}).get("con", 10) or 0)
    if con <= 0:
        # Defensive: a living creature with no Con shouldn't exist;
        # treat as instant-kill at 0 HP.
        return 0
    return -con


# PF1 RAW: undead are immune to mind-affecting effects, paralysis,
# sleep, stun, fatigue/exhaustion, disease/poison/nausea/sickness,
# bleed, and death effects.
UNDEAD_CONDITION_IMMUNITIES: frozenset[str] = frozenset({
    "charmed",       # mind-affecting / charm
    "fascinated",    # mind-affecting / mental
    "shaken",        # mind-affecting / fear
    "frightened",    # mind-affecting / fear
    "panicked",      # mind-affecting / fear
    "cowering",      # mind-affecting / fear
    "dazed",         # mind-affecting / mental
    "confused",      # mind-affecting / mental
    "sleeping",      # sleep effects
    "paralyzed",     # paralysis
    "stunned",       # stun effects
    "fatigued",      # physical fatigue
    "exhausted",     # exhaustion
    "nauseated",     # disease / poison / smell-based
    "sickened",      # disease / poison
})

# Constructs share most undead immunities (no metabolism either).
CONSTRUCT_CONDITION_IMMUNITIES: frozenset[str] = UNDEAD_CONDITION_IMMUNITIES


def _monster_condition_immunities(monster: Monster) -> set[str]:
    mtype = (monster.type or "").lower()
    if mtype == "undead":
        return set(UNDEAD_CONDITION_IMMUNITIES)
    if mtype == "construct":
        return set(CONSTRUCT_CONDITION_IMMUNITIES)
    return set()


# Map keys in monster.ac dict → modifier types.
_AC_KEY_TO_TYPE: dict[str, str] = {
    "armor":      "armor",
    "shield":     "shield",
    "natural":    "natural",
    "deflection": "deflection",
    "dodge":      "dodge",
    "size":       "size",
    "dex":        "ability",  # Dex is an ability mod, not a typed combat bonus
}


def _parse_class_weapon_proficiencies(
    prof_string: str,
    registry,
) -> set[str]:
    """Translate a class-data ``weapon_proficiencies`` string into a set of
    proficiency tokens.

    A token is either a category name ("simple", "martial", "exotic") or a
    specific weapon ID (e.g. "longsword"). The returned set is matched
    against an attack's ``weapon_category`` and ``weapon_id`` by
    ``turn_executor._weapon_not_proficient``.
    """
    out: set[str] = set()
    if not prof_string:
        return out
    s = prof_string.strip()
    if s.startswith("all_simple_and_martial"):
        out.update({"simple", "martial"})
        return out
    if s.startswith("all_simple_plus_"):
        out.add("simple")
        # "deity_favored" / similar tail tokens aren't modeled yet.
        return out
    if s == "all_simple" or s.startswith("all_simple"):
        out.add("simple")
        return out
    if s.startswith("simple_plus_"):
        out.add("simple")
        s = s[len("simple_plus_"):]
    # Greedily consume known weapon IDs from the registry.
    known_ids = sorted(
        getattr(registry, "weapons", {}).keys(),
        key=len,
        reverse=True,  # longest-first so "heavy_crossbow" beats "heavy".
    )
    remaining = s
    while remaining:
        matched = False
        for wid in known_ids:
            if remaining == wid or remaining.startswith(wid + "_"):
                out.add(wid)
                remaining = remaining[len(wid):]
                if remaining.startswith("_"):
                    remaining = remaining[1:]
                matched = True
                break
        if not matched:
            # Unknown token; consume up to next underscore and skip.
            idx = remaining.find("_")
            if idx == -1:
                break
            remaining = remaining[idx + 1:]
    return out


def _parse_class_armor_proficiencies(prof_string: str) -> set[str]:
    """Translate a class-data ``armor_proficiencies`` string into a set
    of armor-category tokens.

    Tokens:
      - ``"light"``, ``"medium"``, ``"heavy"`` for armor
      - ``"shields_normal"`` for non-tower shields
      - ``"shield_tower"`` for tower shields
      - ``"_modeled_"`` sentinel — included whenever a class string is
        provided (even if it expanded to nothing). Distinguishes
        "modeled with no proficiencies" (wizard, ``"none"``) from
        "not modeled" (monster / empty string).
    """
    out: set[str] = set()
    if not prof_string:
        return out  # not modeled
    s = prof_string.strip()
    out.add("_modeled_")
    if s == "none":
        return out
    if s == "all_armor_shields_including_tower":
        out.update({"light", "medium", "heavy", "shields_normal",
                    "shield_tower"})
        return out
    if s == "light_no_shields":
        out.add("light")
        return out
    if s == "light_shields_no_tower":
        out.update({"light", "shields_normal"})
        return out
    if s == "light_medium_shields_no_tower":
        out.update({"light", "medium", "shields_normal"})
        return out
    if s == "light_medium_no_metal_shields_no_metal_no_tower":
        # Druid: light & medium (non-metal) + shields (non-metal,
        # non-tower). We don't track metal/non-metal yet — approximate
        # as light + medium + non-tower shields.
        out.update({"light", "medium", "shields_normal"})
        return out
    # Fallback: leave empty (caller treats as "not modeled" → no penalty).
    return out


def _parse_racial_weapon_familiarity(race) -> set[str]:
    """Pull weapon proficiencies granted by racial traits.

    Translates ``weapon_familiarity_*`` traits into proficiency tokens.
    Tag-based clauses ("treat any weapon with 'orc' in its name as
    martial") aren't expanded here — they're just summary text we'd
    have to scan the registry for; deferred to a later pass.
    """
    out: set[str] = set()
    for t in race.traits or []:
        if not isinstance(t, dict):
            continue
        tid = t.get("id", "")
        if tid == "weapon_familiarity_orc":
            out.update({"greataxe", "falchion"})
        elif tid == "weapon_familiarity_halfling":
            out.add("sling")
        elif tid == "weapon_familiarity_elven":
            out.update({"longbow", "longsword", "rapier", "shortbow"})
        # Dwarf/gnome racial familiarity reads weapons by name-substring
        # ("dwarven", "gnome") — those weapon entries aren't in v1
        # content, so nothing to add here yet.
    return out


def combatant_from_monster(
    monster: Monster,
    position: tuple[int, int],
    team: str,
    *,
    name: str | None = None,
) -> Combatant:
    """Build a Combatant from a monster template.

    Monsters' stat blocks are pre-computed: HP, AC components, saves,
    attacks all come straight from the JSON. We unpack the AC
    breakdown into typed modifiers so that situational AC (touch /
    flat-footed) can be computed by filtering them.
    """
    coll = ModifierCollection()
    source_prefix = f"monster:{monster.id}"

    # Unpack AC modifiers from the breakdown dict.
    for key, value in monster.ac.items():
        if key in ("total", "touch", "flat_footed"):
            continue
        if value == 0:
            continue
        mod_type = _AC_KEY_TO_TYPE.get(key, "untyped")
        if key == "dex":
            coll.add(mod(int(value), mod_type, "ac", f"{source_prefix}:dex_modifier"))
        else:
            coll.add(mod(int(value), mod_type, "ac", f"{source_prefix}:{key}"))

    # Initiative bonus comes from the JSON's `init` field.
    if monster.init != 0:
        coll.add(mod(monster.init, "untyped", "initiative",
                     f"{source_prefix}:init"))

    # Skills: each entry's value is the full skill total. Treat as
    # untyped modifier so skill_total() returns the JSON number.
    for skill_id, total in monster.skills.items():
        if total != 0:
            coll.add(mod(int(total), "untyped", f"skill:{skill_id}",
                         f"{source_prefix}:skill_block"))

    return Combatant(
        id=_new_id(),
        name=name or monster.name,
        team=team,
        size=monster.size,
        speed=monster.speed,
        reach_class="tall" if monster.size in ("medium", "small") else _infer_reach_class(monster),
        bases={
            "ac":        10,
            "fort_save": int(monster.saves.get("fort", 0)),
            "ref_save":  int(monster.saves.get("ref",  0)),
            "will_save": int(monster.saves.get("will", 0)),
            "bab":       monster.bab,
            "cmb":       monster.cmb,
            "cmd":       monster.cmd,
            "initiative": 0,  # already added as a modifier above
        },
        modifiers=coll,
        attack_options=[dict(a) for a in monster.attacks],
        current_hp=monster.hp,
        max_hp=monster.hp,
        position=position,
        conditions=set(monster.permanent_conditions),
        resources={},
        template_kind="monster",
        template=monster,
        damage_reduction=_monster_damage_reduction(monster),
        death_threshold=_monster_death_threshold(monster),
        condition_immunities=_monster_condition_immunities(monster),
    )


def _infer_reach_class(monster: Monster) -> str:
    """Heuristic for monster reach class.

    PF1 doesn't store this on stat blocks directly; we guess from type.
    Animals, oozes, vermin tend to be 'long'. Humanoids and giants are
    'tall'. For v1 this is approximate; we'll annotate templates later
    if it matters.
    """
    if monster.type in ("animal", "vermin", "ooze"):
        return "long"
    return "tall"


def combatant_from_hero_record(
    hero_record,
    registry: ContentRegistry,
    position: tuple[int, int],
    team: str,
) -> Combatant:
    """Materialize a Combatant for a deployment from a sandbox HeroRecord.

    The HeroRecord carries the static ``Character`` plus carry-over
    state (current HP from prior deployments, etc.). This factory
    builds a fresh combat-ready combatant honoring that carry-over.
    """
    c = combatant_from_character(
        hero_record.character, registry, position, team,
    )
    # Honor carried HP if the record has been initialized; otherwise
    # the character's max_hp as set by the engine is the right starting
    # value (used at first spawn).
    if hero_record.current_hp > 0:
        c.current_hp = min(hero_record.current_hp, c.max_hp)
    # Cache max_hp on the record for UI; persisted on next save.
    hero_record.max_hp = c.max_hp
    if hero_record.current_hp <= 0:
        hero_record.current_hp = c.max_hp
    return c


def combatant_from_character(
    character: Character,
    registry: ContentRegistry,
    position: tuple[int, int],
    team: str,
) -> Combatant:
    """Build a Combatant from a character, including equipped gear and
    multi-level progression if the character has a level plan."""
    race = registry.get_race(character.race_id)
    class_ = registry.get_class(character.class_id)

    # Walk the level-up plan (or trivially construct L1 state) to get
    # cumulative HP, BAB, saves, feats, skill ranks, and ability bumps.
    from .level_plan import LevelUpPlan
    from .leveling import apply_plan
    if character.level_plan and character.level > 1:
        plan = LevelUpPlan.from_dict(character.level_plan)
    else:
        plan = LevelUpPlan(name="<l1>", target_level=1, levels={})
    cumulative = apply_plan(
        plan=plan,
        base_scores=character.base_ability_scores,
        race=race,
        free_choice=character.free_ability_choice,
        starting_class_id=class_.id,
        starting_feats=list(character.feats),
        starting_skill_ranks=dict(character.skill_ranks),
        starting_class_choices=dict(character.class_choices),
        registry=registry,
    )

    coll = ModifierCollection()

    coll.add_many(racial_ability_modifiers(race, character.free_ability_choice))
    coll.add_many(size_modifiers(race.size))

    # Racial trait passive modifiers (e.g., Halfling Luck, Keen Senses).
    from .racial_effects import racial_modifiers as _race_mods
    coll.add_many(_race_mods(race))

    # Per-feat passive modifiers (e.g., Toughness, Dodge, Skill Focus).
    from .feat_effects import feat_modifiers as _feat_mods
    for fid in character.feats:
        coll.add_many(_feat_mods(fid, character))

    final_scores: AbilityScores = cumulative.final_ability_scores

    str_mod = final_scores.modifier("str")
    dex_mod = final_scores.modifier("dex")
    con_mod = final_scores.modifier("con")
    wis_mod = final_scores.modifier("wis")

    # ── Equipment lookups ─────────────────────────────────────────────────
    armor_data = None
    if character.equipped_armor and character.equipped_armor != "none":
        armor_data = registry.get_armor(character.equipped_armor)
    shield_data = None
    if character.equipped_shield:
        shield_data = registry.get_shield(character.equipped_shield)
    weapon_data = None
    if character.equipped_weapon:
        weapon_data = registry.get_weapon(character.equipped_weapon)

    # ── Encumbrance load (computed early so Max-Dex / speed factor in) ──
    from .encumbrance import (
        LOAD_ACP_PENALTY,
        LOAD_MAX_DEX,
        carried_weight as _carried,
        effective_speed as _effective_speed,
        load_category as _load_cat,
    )
    load_weight = _carried(character, registry)
    load = _load_cat(load_weight, final_scores.get("str") or 0)
    load_acp = LOAD_ACP_PENALTY.get(load, 0)
    load_max_dex = LOAD_MAX_DEX.get(load)

    # ── AC: Dex (capped by armor and/or load), armor bonus, shield bonus ──
    ac_dex_mod = dex_mod
    if armor_data is not None and armor_data.max_dex_bonus < dex_mod:
        ac_dex_mod = armor_data.max_dex_bonus
    if load_max_dex is not None and load_max_dex < ac_dex_mod:
        ac_dex_mod = load_max_dex
    if ac_dex_mod != 0:
        coll.add(mod(ac_dex_mod, "ability", "ac", "dex_modifier"))
    if armor_data is not None and armor_data.ac_bonus > 0:
        coll.add(mod(armor_data.ac_bonus, "armor", "ac",
                     f"armor:{armor_data.id}"))
    if shield_data is not None and shield_data.ac_bonus > 0:
        coll.add(mod(shield_data.ac_bonus, "shield", "ac",
                     f"shield:{shield_data.id}"))

    # Saves: Fort gets Con, Ref gets Dex, Will gets Wis.
    if con_mod != 0:
        coll.add(mod(con_mod, "ability", "fort_save", "con_modifier"))
    if dex_mod != 0:
        coll.add(mod(dex_mod, "ability", "ref_save", "dex_modifier"))
    if wis_mod != 0:
        coll.add(mod(wis_mod, "ability", "will_save", "wis_modifier"))

    # CMB / CMD.
    if str_mod != 0:
        coll.add(mod(str_mod, "ability", "cmb", "str_modifier"))
        coll.add(mod(str_mod, "ability", "cmd", "str_modifier"))
    if dex_mod != 0:
        coll.add(mod(dex_mod, "ability", "cmd", "dex_modifier"))

    # Initiative: Dex.
    if dex_mod != 0:
        coll.add(mod(dex_mod, "ability", "initiative", "dex_modifier"))

    # Skills: cumulative ranks + class skill bonus + ability modifier + ACP.
    class_skills = set(class_.level_1.class_skills)
    for cid in cumulative.class_levels:
        if cid != class_.id:
            try:
                class_skills.update(registry.get_class(cid).level_1.class_skills)
            except Exception:
                pass
    for skill_id, ranks in cumulative.skill_ranks.items():
        if ranks <= 0:
            continue
        try:
            skill = registry.get_skill(skill_id)
        except KeyError:
            continue
        coll.add(mod(ranks, "untyped", f"skill:{skill_id}", "ranks"))
        ab = final_scores.modifier(skill.ability)
        if ab != 0:
            coll.add(mod(ab, "ability", f"skill:{skill_id}",
                         f"{skill.ability}_modifier"))
        if skill_id in class_skills:
            coll.add(mod(3, "untyped", f"skill:{skill_id}", "class_skill_bonus"))
        # Armor check penalty applies to a known set of skills.
        if skill.armor_check_penalty:
            acp = 0
            if armor_data is not None:
                acp += armor_data.armor_check_penalty
            if shield_data is not None:
                acp += shield_data.armor_check_penalty
            acp += load_acp
            if acp < 0:
                coll.add(mod(acp, "untyped", f"skill:{skill_id}",
                             "armor_check_penalty"))

    # ── Attack options from equipped weapon ───────────────────────────────
    attack_options: list[dict] = []
    if weapon_data is not None:
        size_data = get_size(race.size)
        size_mod_atk = size_data.ac_attack_mod
        bab = cumulative.bab
        if weapon_data.is_melee:
            ability_mod = (max(str_mod, dex_mod)
                           if weapon_data.is_finesse else str_mod)
            attack_bonus = bab + ability_mod + size_mod_atk
            if weapon_data.wield == "two_handed":
                damage_bonus = (str_mod * 3) // 2
            else:
                damage_bonus = str_mod
            attack_type = "melee"
        else:
            attack_bonus = bab + dex_mod + size_mod_atk
            damage_bonus = 0
            attack_type = "ranged"
        attack_options.append({
            "type": attack_type,
            "name": weapon_data.name,
            "weapon_id": weapon_data.id,
            "weapon_category": weapon_data.category,
            "attack_bonus": attack_bonus,
            "damage": weapon_data.damage_dice,
            "damage_bonus": damage_bonus,
            "damage_type": weapon_data.damage_type,
            "crit_range": list(weapon_data.crit_range),
            "crit_multiplier": weapon_data.crit_multiplier,
            "range_increment": weapon_data.range_increment,
            "wield": weapon_data.wield,
        })

    # Off-hand weapon (PF1 two-weapon fighting). Uses the same to-hit
    # math as the primary, but damage uses 1/2 Str modifier (rounded
    # toward zero). Per-attack penalties for dual-wielding are applied
    # at full-attack time, not baked into ``attack_bonus`` here.
    offhand_weapon_data = None
    if (character.equipped_offhand_weapon
            and character.equipped_offhand_weapon != "none"):
        offhand_weapon_data = registry.get_weapon(
            character.equipped_offhand_weapon,
        )
    if offhand_weapon_data is not None:
        if offhand_weapon_data.is_melee:
            ability_mod = (max(str_mod, dex_mod)
                           if offhand_weapon_data.is_finesse else str_mod)
            off_attack_bonus = cumulative.bab + ability_mod + size_mod_atk
            off_damage_bonus = str_mod // 2
            off_attack_type = "melee"
        else:
            off_attack_bonus = cumulative.bab + dex_mod + size_mod_atk
            off_damage_bonus = 0
            off_attack_type = "ranged"
        attack_options.append({
            "type": off_attack_type,
            "name": offhand_weapon_data.name,
            "weapon_id": offhand_weapon_data.id,
            "weapon_category": offhand_weapon_data.category,
            "attack_bonus": off_attack_bonus,
            "damage": offhand_weapon_data.damage_dice,
            "damage_bonus": off_damage_bonus,
            "damage_type": offhand_weapon_data.damage_type,
            "crit_range": list(offhand_weapon_data.crit_range),
            "crit_multiplier": offhand_weapon_data.crit_multiplier,
            "range_increment": offhand_weapon_data.range_increment,
            "wield": offhand_weapon_data.wield,
            "is_offhand": True,
        })

    # HP from cumulative HD + Con; add any hp_max modifiers (Toughness etc).
    from .modifiers import compute as _compute
    hp_max = cumulative.hp_max + _compute(0, coll.for_target("hp_max"))
    bab = cumulative.bab

    # Determine the casting model from the primary class's
    # spell_progression (prepared / spontaneous / "" for non-casters).
    casting_type = ""
    sp = class_.spell_progression
    if sp:
        casting_type = str(sp.get("type", ""))

    # Populate castable spells based on class + level.
    castable: set[str] = set()
    if cumulative.spells_per_day:
        max_castable_level = max(
            (int(k) for k, v in cumulative.spells_per_day.items()
             if (isinstance(v, int) and v > 0) or v == "at_will"),
            default=0,
        )
        if casting_type == "spontaneous" and character.spells_known:
            # Spontaneous caster: castable = explicitly-known spells (per
            # the character sheet), filtered by level cap and validated
            # against the registry.
            for level_key, ids in character.spells_known.items():
                lvl = int(level_key)
                if lvl > max_castable_level:
                    continue
                for sid in ids:
                    if sid in registry.spells:
                        castable.add(sid)
        else:
            # Default / prepared casters: all class-list spells up to
            # the level cap are castable in principle (prepared casters
            # additionally need them in prepared_spells to actually
            # cast).
            for sid, spell in registry.spells.items():
                if class_.id in spell.level_by_class:
                    if spell.level_by_class[class_.id] <= max_castable_level:
                        castable.add(sid)
                # Multiclass casters: include spells from other caster
                # classes.
                for cid in cumulative.class_levels:
                    if cid != class_.id and cid in spell.level_by_class:
                        castable.add(sid)

    # Prepared casters: bake spells_prepared from the character sheet
    # into the combatant's prepared_spells. Without explicit prep, we
    # leave it empty — _do_cast will reject casts with a clear error
    # rather than silently letting them through.
    prepared_spells: dict[int, list[str]] = {}
    if casting_type == "prepared" and character.spells_prepared:
        for level_key, ids in character.spells_prepared.items():
            lvl = int(level_key)
            prepared_spells[lvl] = list(ids)
    # Slot resources keyed by spell level.
    spell_slot_resources: dict[str, int] = {}
    if cumulative.spells_per_day:
        for slvl, count in cumulative.spells_per_day.items():
            if isinstance(count, int):
                spell_slot_resources[f"spell_slot_{slvl}"] = count

    # Class-specific per-day / per-encounter pools.
    cha_mod = final_scores.modifier("cha")
    barbarian_levels = cumulative.class_levels.get("barbarian", 0)
    paladin_levels = cumulative.class_levels.get("paladin", 0)
    cleric_levels = cumulative.class_levels.get("cleric", 0)
    bard_levels = cumulative.class_levels.get("bard", 0)
    monk_levels = cumulative.class_levels.get("monk", 0)
    if barbarian_levels > 0:
        # Rage rounds: 4 + Con + 2/level beyond 1st.
        spell_slot_resources["rage_rounds"] = (
            4 + con_mod + 2 * max(0, barbarian_levels - 1)
        )
    if paladin_levels > 0:
        # Smite Evil: 1/day at L1, +1 every 3 levels.
        spell_slot_resources["smite_evil_uses"] = 1 + (paladin_levels - 1) // 3
    if cleric_levels > 0:
        # Channel Energy: 3 + Cha mod per day.
        spell_slot_resources["channel_uses"] = max(0, 3 + cha_mod)
    if bard_levels > 0:
        # Bardic Performance: 4 + Cha + 2/level beyond 1st rounds/day.
        spell_slot_resources["performance_rounds"] = (
            4 + cha_mod + 2 * max(0, bard_levels - 1)
        )
    if monk_levels > 0:
        # Stunning Fist: monk level + 1 (other classes can have it via feat).
        spell_slot_resources["stunning_fist_uses"] = monk_levels

    # Weapon proficiencies from class + multiclass + race. The set holds
    # category names ("simple", "martial") and/or specific weapon IDs.
    weapon_profs: set[str] = _parse_class_weapon_proficiencies(
        class_.level_1.weapon_proficiencies, registry,
    )
    for cid in cumulative.class_levels:
        if cid == class_.id:
            continue
        try:
            other = registry.get_class(cid)
        except Exception:
            continue
        weapon_profs |= _parse_class_weapon_proficiencies(
            other.level_1.weapon_proficiencies, registry,
        )
    weapon_profs |= _parse_racial_weapon_familiarity(race)

    # Armor proficiencies from class + multiclass.
    armor_profs: set[str] = _parse_class_armor_proficiencies(
        class_.level_1.armor_proficiencies,
    )
    for cid in cumulative.class_levels:
        if cid == class_.id:
            continue
        try:
            other = registry.get_class(cid)
        except Exception:
            continue
        armor_profs |= _parse_class_armor_proficiencies(
            other.level_1.armor_proficiencies,
        )

    return Combatant(
        id=_new_id(),
        name=character.name,
        team=team,
        size=race.size,
        speed=_effective_speed(race.speed, armor_data, load),
        reach_class="tall",
        bases={
            "ac":        10,
            "fort_save": int(cumulative.saves.get("fort", 0)),
            "ref_save":  int(cumulative.saves.get("ref",  0)),
            "will_save": int(cumulative.saves.get("will", 0)),
            "bab":       bab,
            "cmb":       bab,       # size & ability via modifiers
            "cmd":       10 + bab,  # size, Str, Dex via modifiers
            "initiative": 0,
        },
        modifiers=coll,
        attack_options=attack_options,
        current_hp=hp_max,
        max_hp=hp_max,
        position=position,
        conditions=set(),
        resources=spell_slot_resources,
        template_kind="character",
        template=character,
        castable_spells=castable,
        casting_type=casting_type,
        prepared_spells=prepared_spells,
        death_threshold=-int(final_scores.get("con") or 10),
        weapon_proficiency_categories=weapon_profs,
        armor_proficiency_categories=armor_profs,
    )
