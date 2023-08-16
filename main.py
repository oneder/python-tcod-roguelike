import traceback

import time
import tcod

from configparser import ConfigParser

import src.color as color
import src.exceptions as exceptions
import src.input_handlers as input_handlers
import src.setup_game as setup_game

FPS = 1/60

config = ConfigParser()
config.read("config.ini")

def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    # if the current event handler has an active Engine then save it
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")

def main():
    screen_width = int(config.get("GAME INFO", "SCREEN_WIDTH"))
    screen_height = int(config.get("GAME INFO", "SCREEN_HEIGHT"))

    tileset = tcod.tileset.load_tilesheet(
        config.get("GAME INFO", "TILESHEET_PATH"), 
        int(config.get("GAME INFO", "TILESHEET_COLUMNS")), 
        int(config.get("GAME INFO", "TILESHEET_ROWS")), 
        tcod.tileset.CHARMAP_TCOD
    )

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    with tcod.context.new_terminal(
       screen_width,
       screen_height,
       tileset=tileset,
       title=config.get("GAME INFO", "TITLE"),
       vsync=True, 
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.get():
                        context.convert_event(event)
                        handler = handler.handle_events(event)

                    if isinstance(handler, input_handlers.EventHandler):
                        handler.real_time_update()

                    time.sleep(FPS)
                except Exception: # handle exceptions in game
                    traceback.print_exc() # print error to stderr

                    # then print the error to the message log
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit: # save and quit
            save_game(handler, "savegame.sav")
            raise
        except BaseException: # save on any other unexpected exception
            save_game(handler, "savegame.sav")
            raise

if __name__ == "__main__":
    main()