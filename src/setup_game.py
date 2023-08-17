# handle the loading and initialization of game sessions
from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional
from configparser import ConfigParser

import tcod

import src.color as color
from src.engine import Engine
import src.entity_factories as entity_factories
from src.game_map import GameWorld
import src.input_handlers as input_handlers
import src.constants as constants

config = ConfigParser()
config.read("config.ini")

# load the background image and remove the alpha channel
background_image = tcod.image.load(config.get("GAME INFO", "MAIN_MENU_BG_PATH"))[:, :, :3]

def new_game(character_cls: str) -> Engine:
    # return a brand new game session as an Engine instance
    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = entity_factories.get_player(character_cls)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
    )

    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        "Hello, and welcome, adventurer, to yet another dungeon!", color.welcome_text
    )

    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)

    dagger.parent = player.inventory
    leather_armor.parent = player.inventory

    player.inventory.items.append(dagger)
    #player.equipment.toggle_equip(dagger, add_message=False)

    player.inventory.items.append(leather_armor)
    #player.equipment.toggle_equip(leather_armor, add_message=False)

    return engine

def load_game(filename: str) -> Engine:
    # laod an engine instance from a file
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine

class MainMenu(input_handlers.BaseEventHandler):
    menu_items = ["New Game", "Continue Last Game", "Quit"]
    current_index = 0

    # handle the main menu rendering and input
    def on_render(self, console: tcod.Console) -> None:
        # render the main menu on a background image
        # console.draw_semigraphics(background_image, 0, 0)

        console.draw_frame(1, 1, console.width-2, console.height-2)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            config.get("GAME INFO", "TITLE"),
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        console.print_box(
            0, console.height - 2, console.width, 1, "┤ BY ONEDER ├", alignment=tcod.CENTER
        )

        menu_width = 18
        for i, text in enumerate(self.menu_items):
            menu_item_color = color.menu_text
            if self.current_index == i:
                menu_item_color = color.selected_menu_text

            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=menu_item_color,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )
        
        console.print(
            (console.width // 4) * 3,
            console.height // 2 - 2 + self.current_index,
            string="<"
        )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym == tcod.event.K_ESCAPE:
            raise SystemExit()
        elif event.sym in constants.CONFIRM_KEYS or event.sym == tcod.event.K_x:
            try:
                if self.current_index == 0:
                    return CharacterSelect()
                elif self.current_index == 1:
                    return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
                elif self.current_index == 2:
                    raise SystemExit()                       
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc() # print to stderr
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
                    
        return None
    
    def ev_keyup(
        self, event: tcod.event.KeyUp
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym == tcod.event.K_UP:
            if self.current_index == 0:
                self.current_index = len(self.menu_items) - 1
            else:
                self.current_index -= 1
        elif event.sym == tcod.event.K_DOWN:
            if self.current_index == len(self.menu_items) - 1:
                self.current_index = 0
            else:
                self.current_index += 1

        return None
    
class CharacterSelect(input_handlers.BaseEventHandler):
    class_items = [
        constants.ENTITY_PLAYER_TYPE_HUMAN, 
        constants.ENTITY_PLAYER_TYPE_MECH,
        constants.ENTITY_PLAYER_TYPE_FUNGUS,
    ]

    current_class = 0

    # handle the main menu rendering and input
    def on_render(self, console: tcod.Console) -> None:
        console.draw_frame(1, 1, console.width-2, console.height-2)

        console.print(
            console.width // 2,
            console.height // 5,
            "Character Select:",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        console.print(console.width // 4, console.height // 3, "Class:", fg=color.white)
        for i, text in enumerate(self.class_items):
            class_item_color = color.menu_text
            if self.current_class == i:
                class_item_color = color.selected_menu_text

            console.print(                
                console.width // 4 + 4,
                console.height // 3 + (i + 1),
                text,
                fg=class_item_color,
            )       
        
        console.print(
            console.width // 4,
            console.height // 3 +(1 + self.current_class),
            string=">"
        )
    
    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            return MainMenu()
        elif event.sym in constants.CONFIRM_KEYS or event.sym == tcod.event.K_x:
            return input_handlers.MainGameEventHandler(new_game(self.class_items[self.current_class]))
        
        return None
    
    def ev_keyup(
        self, event: tcod.event.KeyUp
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym == tcod.event.K_UP:
            if self.current_class == 0:
                self.current_class = len(self.class_items) - 1
            else:
                self.current_class -= 1
        elif event.sym == tcod.event.K_DOWN:
            if self.current_class == len(self.class_items) - 1:
                self.current_class = 0
            else:
                self.current_class += 1

        return None