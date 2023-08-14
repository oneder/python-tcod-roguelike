from __future__ import annotations

from typing import TYPE_CHECKING

from src.components.base_component import BaseComponent
from src.equipment_types import EquipmentType

if TYPE_CHECKING:
    from src.entity import Item

class Equipable(BaseComponent):
    parent: Item
    
    def __init__(
        self,
        equipment_type: EquipmentType,
        power_bonus: int = 0,
        defense_bonus: int = 0,
    ):
        self.equipment_type = equipment_type
    
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus

class Dagger(Equipable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=2)

class Sword(Equipable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4)

class LeatherArmor(Equipable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1)

class ChainMail(Equipable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3)