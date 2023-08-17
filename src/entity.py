from __future__ import annotations

import copy
import math
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING, Union

import src.constants as constants

from src.render_order import RenderOrder

from src.components.fighter import Fighter
from src.components.inventory import Inventory
from src.components.level import Level

if TYPE_CHECKING:
    from src.components.ai import BaseAI
    from src.components.consumable import Consumable
    from src.components.equipment import Equipment
    from src.components.equipable import Equipable
    from src.game_map import GameMap

T = TypeVar("T", bound="Entity")

class Entity:
    """
        generic object to represent players, enemies, items etc
    """

    parent: Union[GameMap, Inventory]

    def __init__(
        self, 
        parent: Optional[GameMap] = None,
        x: int = 0, 
        y: int = 0, 
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool=False,
        render_order: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            # if parent isn't provided now then it will be set later
            self.parent = parent
            parent.entities.add(self)

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone
    
    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        # place this entity at a new location
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "parent"):
                if self.parent is self.gamemap:
                    self.gamemap.entities.remove(self)
            self.parent = gamemap
            gamemap.entities.add(self)

    def distance(self, x: int, y: int) -> float:
        # return the distance between the current entity and given (x, y) coordinate
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

class Actor(Entity):
    def __init__(
            self, 
            *, 
            x: int = 0, 
            y: int = 0, 
            char: str = "?", 
            color: Tuple[int, int, int] = (255, 255, 255), 
            name: str = "<Unnamed>", 
            ai_cls: Type[BaseAI],
            equipment: Equipment,
            fighter: Fighter,
            inventory: Inventory,
            level: Level,
            speed: int,
    ):
        super().__init__(
            x=x, 
            y=y, 
            char=char, 
            color=color, 
            name=name, 
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )

        self.ai: Optional[BaseAI] = ai_cls(self)

        self.equipment: Equipment = equipment
        self.equipment.parent = self

        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self

        self.level = level
        self.level.parent = self

        self.speed = speed
        self.wait = 0

    def move(self, dx: int, dy: int) -> None:
        super().move(dx=dx, dy=dy)     

        # whenever an actor moves, initiate wait
        self.wait = self.speed

    @property
    def is_alive(self) -> bool:
        return bool(self.ai) # true as long as actor can perform actions
    
class Player(Actor):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = constants.ENTITY_PLAYER_DEFAULT_COLOR,
        name: str = "<Unnamed>",
        ai_cls: Type[BaseAI],
        equipment: Equipment,
        character_cls: str = "",
    ):
        self.character_cls = character_cls
        self.color = self.get_color_by_class(character_cls)
        self.fighter = self.get_fighter_by_class(character_cls)
        self.inventory = self.get_inventory_by_class(character_cls)
        self.level = self.get_level_by_class(character_cls)
        self.speed = self.get_speed_by_class(character_cls)

        super().__init__(
            x=x,
            y=y,
            char=char,
            color=self.color,
            name=name,
            ai_cls=ai_cls,
            equipment=equipment,
            fighter=self.fighter,
            inventory=self.inventory,
            level=self.level,
            speed=self.speed
        )   

    def get_color_by_class(self, character_cls: str) -> Tuple[int, int, int]:
        if len(character_cls) > 0:
            if character_cls == constants.ENTITY_PLAYER_TYPE_HUMAN:
                return constants.ENTITY_HUMAN_BASE_COLOR
            elif character_cls == constants.ENTITY_PLAYER_TYPE_MECH:
                return constants.ENTITY_MECH_BASE_COLOR
            elif character_cls == constants.ENTITY_PLAYER_TYPE_FUNGUS:
                return constants.ENTITY_FUNGUS_BASE_COLOR
            
        return constants.ENTITY_PLAYER_DEFAULT_COLOR

    def get_fighter_by_class(self, character_cls: str) -> Optional[Fighter]:
        if len(character_cls) > 0:
            if character_cls == constants.ENTITY_PLAYER_TYPE_HUMAN:
                return Fighter(
                    hp=constants.ENTITY_HUMAN_BASE_HP,
                    base_defense=constants.ENTITY_HUMAN_BASE_DEFENSE,
                    base_power=constants.ENTITY_HUMAN_BASE_POWER,
                    base_attack_speed=constants.ENTITY_HUMAN_BASE_ATTACK_SPEED
                )
            elif character_cls == constants.ENTITY_PLAYER_TYPE_MECH:
                return Fighter(
                    hp=constants.ENTITY_MECH_BASE_HP,
                    base_defense=constants.ENTITY_MECH_BASE_DEFENSE,
                    base_power=constants.ENTITY_MECH_BASE_POWER,
                    base_attack_speed=constants.ENTITY_MECH_BASE_ATTACK_SPEED
                )
            elif character_cls == constants.ENTITY_PLAYER_TYPE_FUNGUS:
                return Fighter(
                    hp=constants.ENTITY_FUNGUS_BASE_HP,
                    base_defense=constants.ENTITY_FUNGUS_BASE_DEFENSE,
                    base_power=constants.ENTITY_FUNGUS_BASE_POWER,
                    base_attack_speed=constants.ENTITY_FUNGUS_BASE_ATTACK_SPEED
                )

        return None
    
    def get_inventory_by_class(self, character_cls: str) -> Optional[Inventory]:
        if len(character_cls) > 0:
            if character_cls == constants.ENTITY_PLAYER_TYPE_HUMAN:
                return Inventory(capacity=constants.ENTITY_HUMAN_BASE_INVENTORY_CAPACITY)
            elif character_cls == constants.ENTITY_PLAYER_TYPE_MECH:
                return Inventory(capacity=constants.ENTITY_MECH_BASE_INVENTORY_CAPACITY)
            elif character_cls == constants.ENTITY_PLAYER_TYPE_FUNGUS:
                return Inventory(capacity=constants.ENTITY_FUNGUS_BASE_INVENTORY_CAPACITY)
         
        return None
    
    def get_level_by_class(self, character_cls: str) -> Optional[Level]:
        if len(character_cls) > 0:
            if character_cls == constants.ENTITY_PLAYER_TYPE_HUMAN:
                return Level(level_up_base=constants.ENTITY_HUMAN_BASE_LEVEL_UP_BASE)
            elif character_cls == constants.ENTITY_PLAYER_TYPE_MECH:
                return Level(level_up_base=constants.ENTITY_MECH_BASE_LEVEL_UP_BASE)
            elif character_cls == constants.ENTITY_PLAYER_TYPE_FUNGUS:
                return Level(level_up_base=constants.ENTITY_FUNGUS_BASE_LEVEL_UP_BASE)
        
        return None
    
    def get_speed_by_class(self, character_cls: str) -> int:
        if len(character_cls) > 0:
            if character_cls == constants.ENTITY_PLAYER_TYPE_HUMAN:
                return constants.ENTITY_HUMAN_BASE_MOVEMENT_SPEED
            elif character_cls == constants.ENTITY_PLAYER_TYPE_MECH:
                return constants.ENTITY_MECH_BASE_MOVEMENT_SPEED
            elif character_cls == constants.ENTITY_PLAYER_TYPE_FUNGUS:
                return constants.ENTITY_FUNGUS_BASE_MOVEMENT_SPEED
        
        return 1

class Item(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        consumable: Optional[Consumable] = None,
        equipable: Optional[Equipable] = None,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
        )

        self.consumable = consumable

        if self.consumable:
            self.consumable.parent = self

        self.equipable = equipable

        if self.equipable:
            self.equipable.parent = self