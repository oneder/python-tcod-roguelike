from configparser import ConfigParser

from typing import Optional

from src.components.ai import HostileEnemy
from src.components import consumable, equipable
from src.components.equipment import Equipment
from src.components.fighter import Fighter
from src.components.inventory import Inventory
from src.components.level import Level
from src.entity import Actor, Player, Item

import src.color as color
import src.constants as constants

config = ConfigParser()
config.read("config.ini")

""" ACTORS """

def get_player(character_cls: str) -> Optional[Player]:
    if len(character_cls) > 0:
        return Player(
            char="@",
            color=constants.ENTITY_PLAYER_DEFAULT_COLOR,
            name="Player",
            ai_cls=HostileEnemy,
            equipment=Equipment(),
            character_cls=character_cls
        )        

    return None

orc = Actor(
    char="o", 
    color=color.orc_alive, 
    name="Orc", 
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(
        hp=10, 
        base_defense=0, 
        base_power=3, 
        base_attack_speed=60
    ),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
    speed=30,
)

troll = Actor(
    char="T", 
    color=color.troll_alive, 
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(
        hp=15, 
        base_defense=1, 
        base_power=4, 
        base_attack_speed=60
    ),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
    speed=40,
)

""" POTIONS """

health_potion = Item(
    char="!",
    color=color.health_potion,
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)

""" SCROLLS """

confusion_scroll = Item(
    char="~",
    color=color.confusion_scroll,
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10)
)

lightning_scroll = Item(
    char="~",
    color=color.lightning_scroll,
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

fireball_scroll = Item(
    char="~",
    color=color.fireball_scroll,
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)

""" WEAPONS """

dagger = Item(char="/", color=color.dagger, name="Dagger", equipable=equipable.Dagger())
sword = Item(char="/", color=color.sword, name="Sword", equipable=equipable.Sword())

""" EQUIPMENT """

leather_armor = Item(
    char="[",
    color=color.leather_armor,
    name="Leather Armor",
    equipable=equipable.LeatherArmor(),
)

chain_mail = Item(char="[", color=color.chain_mail, name="Chain Mail", equipable=equipable.ChainMail())