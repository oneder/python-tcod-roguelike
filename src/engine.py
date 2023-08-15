from __future__ import annotations

import lzma
import pickle
from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

from configparser import ConfigParser

import src.exceptions as exceptions
from src.message_log import MessageLog
import src.render_functions as render_functions

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld

config = ConfigParser()
config.read("config.ini")

class Engine:
    FOV_RADIUS=int(config.get("GAME INFO", "DEFAULT_FOV_RADIUS")) 

    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.message_log = MessageLog(
            int(config.get("GAME INFO", "MESSAGE_LOG_X")), 
            int(config.get("GAME INFO", "MESSAGE_LOG_Y")),
        )
        self.mouse_location = (0, 0)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    if entity.wait > 0:
                        entity.wait -= 1
                    else:
                        entity.ai.perform()
                except exceptions.Impossible:
                    pass # ignore impossible action exceptions from AI

    def update_fov(self) -> None:
        # compute the visible area based on the player's POV
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=self.FOV_RADIUS,
        )

        # add
        self.game_map.explored |= self.game_map.visible
            
    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(
            console=console, 
            x=self.message_log.x, 
            y=self.message_log.y, 
            width=self.message_log.width, 
            height=self.message_log.height
        )

        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=int(config.get("GAME INFO", "HP_BAR_WIDTH")),
        )

        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.game_world.current_floor,
            location=(
                int(config.get("GAME INFO", "DUNGEON_LEVEL_LBL_X")),
                int(config.get("GAME INFO", "DUNGEON_LEVEL_LBL_Y"))    
            ),
        )

        render_functions.render_names_at_mouse_location(
            console=console, 
            x=int(config.get("GAME INFO", "AT_MOUSE_LBL_X")), 
            y=int(config.get("GAME INFO", "AT_MOUSE_LBL_Y")), 
            engine=self
        )

    def save_as(self, filename: str) -> None:
        # save this engine isntance as a compressed file
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)