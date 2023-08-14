from src.components.ai import HostileEnemy
from src.components import consumable, equipable
from src.components.equipment import Equipment
from src.components.fighter import Fighter
from src.components.inventory import Inventory
from src.components.level import Level
from src.entity import Actor, Item

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=2, base_power=5),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

orc = Actor(
    char="o", 
    color=(63, 127, 63), 
    name="Orc", 
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

troll = Actor(
    char="T", 
    color=(0, 127, 0), 
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=15, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100)
)

health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)

lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

dagger = Item(char="/", color=(0, 191, 255), name="Dagger", equipable=equipable.Dagger())
sword = Item(char="/", color=(0, 191, 255), name="Sword", equipable=equipable.Sword())

leather_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    equipable=equipable.LeatherArmor(),
)

chain_mail = Item(char="[", color=(139, 19, 19), name="Chain Mail", equipable=equipable.ChainMail())

confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10)
)

fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)