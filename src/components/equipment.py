from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from src.components.base_component import BaseComponent
from src.equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Actor, Item

class Equipment(BaseComponent):
    parent: Actor

    def __init__(self, weapon: Optional[Item] = None, armor: Optional[Item] = None):
        self.weapon = weapon
        self.armor = armor
    
    @property
    def defense_bonus(self) -> int:
        bonus = 0

        if self.weapon is not None and self.weapon.equipable is not None:
            bonus += self.weapon.equipable.defense_bonus

        if self.armor is not None and self.armor.equipable is not None:
            bonus += self.armor.equipable.defense_bonus

        return bonus
    
    @property
    def power_bonus(self) -> int:
        bonus = 0

        if self.weapon is not None and self.weapon.equipable is not None:
            bonus += self.weapon.equipable.power_bonus

        if self.armor is not None and self.armor.equipable is not None:
            bonus += self.armor.equipable.power_bonus

        return bonus
    
    def item_is_equipped(self, item: Item) -> bool:
        return self.weapon == item or self.armor == item
    
    def unequip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(f"You remove the {item_name}.")

    def equip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(f"You equip the {item_name}.")

    def equip_to_slot(self, slot: str, item: Item, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if current_item is not None:
            self.unequip_from_slot(slot, add_message)

        setattr(self, slot, item)

        if add_message:
            self.equip_message(item.name)

    def unequip_from_slot(self, slot: str, add_message: bool) -> None:
        current_item = getattr(self, slot)

        setattr(self, slot, None)

        if add_message:
            self.unequip_message(current_item.name)

    def toggle_equip(self, equipable_item: Item, add_message: bool = True) -> None:
        if equipable_item.equipable and equipable_item.equipable.equipment_type == EquipmentType.WEAPON:
            slot = "weapon"
        else:
            slot = "armor"

        if getattr(self, slot) == equipable_item:
            self.unequip_from_slot(slot, add_message)
        else:
            self.equip_to_slot(slot, equipable_item, add_message)