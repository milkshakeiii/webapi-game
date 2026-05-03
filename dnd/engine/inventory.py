"""Inventory system: held items + carried items with HP / hardness.

PF1 items have HP and hardness for sundering; the engine tracks each
held item as a unique instance with its own ``current_hp`` so two
identical items (e.g., two longswords) can be in different damaged
states. Carried items (potions, scrolls, miscellaneous gear) are
addressable for steal targeting.

Item HP / hardness defaults are computed from weight + category when
the item template doesn't specify them. The numbers are rough — PF1
RAW has a per-material table, and we approximate it by weapon
material assumed to be steel for martial weapons, wood for simple
two-handed-only weapons (quarterstaff), and so on.

Held-item slots:
  - ``main_hand``: primary weapon
  - ``off_hand``: off-hand weapon (for two-weapon fighting) OR shield
  - ``armor``: worn armor
  - ``shield``: shield (when not held in off-hand — shields are
    technically held, but for character-sheet simplicity we model
    them as their own slot when off-hand isn't a weapon)

Carried-item list: anything else the combatant possesses but isn't
actively wearing/wielding. Steal works on carried_items.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field


# Material → (hardness, hp_per_pound). Weapons are assumed to be
# steel/iron unless flagged otherwise; we don't track item material
# at v1 content level.
_DEFAULT_HARDNESS = 10  # steel
_DEFAULT_HP_PER_POUND = 5


@dataclass
class InventoryItem:
    """A unique instance of an item in someone's inventory.

    ``instance_id`` distinguishes two otherwise-identical items.
    ``item_id`` is the registry id (e.g., "longsword", "potion_cure_light").
    """

    instance_id: str
    item_id: str
    item_type: str        # "weapon" / "shield" / "armor" / "consumable" / "misc"
    current_hp: int
    max_hp: int
    hardness: int
    broken: bool = False
    properties: dict = field(default_factory=dict)

    def take_damage(self, amount: int) -> int:
        """Apply ``amount`` damage to the item, accounting for hardness.

        Returns the actual HP loss. PF1 RAW: damage less than or equal
        to hardness is fully absorbed. The item gains the ``broken``
        flag at half max HP and is destroyed at 0.
        """
        if amount <= self.hardness:
            return 0
        loss = amount - self.hardness
        self.current_hp = max(0, self.current_hp - loss)
        if self.current_hp <= self.max_hp // 2:
            self.broken = True
        return loss

    def is_destroyed(self) -> bool:
        return self.current_hp <= 0

    def to_dict(self) -> dict:
        return {
            "instance_id": self.instance_id,
            "item_id": self.item_id,
            "item_type": self.item_type,
            "current_hp": self.current_hp,
            "max_hp": self.max_hp,
            "hardness": self.hardness,
            "broken": self.broken,
            "properties": dict(self.properties),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "InventoryItem":
        return cls(
            instance_id=str(d["instance_id"]),
            item_id=str(d["item_id"]),
            item_type=str(d["item_type"]),
            current_hp=int(d["current_hp"]),
            max_hp=int(d["max_hp"]),
            hardness=int(d["hardness"]),
            broken=bool(d.get("broken", False)),
            properties=dict(d.get("properties") or {}),
        )


def _new_instance_id() -> str:
    return f"item_{uuid.uuid4().hex[:12]}"


def _default_hp_for_weight(weight: float) -> int:
    """Compute item HP from weight in pounds."""
    return max(1, int(weight * _DEFAULT_HP_PER_POUND))


def make_weapon_item(weapon_id: str, registry) -> InventoryItem:
    """Construct an InventoryItem from a weapon registry entry."""
    weapon = registry.get_weapon(weapon_id)
    hp = _default_hp_for_weight(weapon.weight)
    # Wooden weapons (quarterstaff, club) get lower hardness.
    hardness = _DEFAULT_HARDNESS
    if weapon_id in ("quarterstaff", "club", "longspear", "spear",
                     "shortspear", "dart", "javelin"):
        hardness = 5
    return InventoryItem(
        instance_id=_new_instance_id(),
        item_id=weapon_id,
        item_type="weapon",
        current_hp=hp,
        max_hp=hp,
        hardness=hardness,
    )


def make_armor_item(armor_id: str, registry) -> InventoryItem:
    armor = registry.get_armor(armor_id)
    hp = _default_hp_for_weight(armor.weight)
    return InventoryItem(
        instance_id=_new_instance_id(),
        item_id=armor_id,
        item_type="armor",
        current_hp=hp,
        max_hp=hp,
        hardness=_DEFAULT_HARDNESS,
    )


def make_shield_item(shield_id: str, registry) -> InventoryItem:
    shield = registry.get_shield(shield_id)
    hp = _default_hp_for_weight(shield.weight)
    hardness = 5 if "wooden" in shield_id else _DEFAULT_HARDNESS
    return InventoryItem(
        instance_id=_new_instance_id(),
        item_id=shield_id,
        item_type="shield",
        current_hp=hp,
        max_hp=hp,
        hardness=hardness,
    )


def make_consumable_item(item_id: str, charges: int = 1) -> InventoryItem:
    """Generic consumable (potion, scroll, etc.). HP/hardness aren't
    used in practice — these can't be sundered as they have negligible
    HP and break trivially. Charges go in properties."""
    return InventoryItem(
        instance_id=_new_instance_id(),
        item_id=item_id,
        item_type="consumable",
        current_hp=1,
        max_hp=1,
        hardness=0,
        properties={"charges": charges},
    )
