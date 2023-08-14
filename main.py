import traceback

import tcod

import src.color as color
import src.exceptions as exceptions
import src.input_handlers as input_handlers
import src.setup_game as setup_game

def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    # if the current event handler has an active Engine then save it
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")

def main():
    screen_width = 80
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(
        "rouge_imgfile.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    with tcod.context.new_terminal(
       screen_width,
       screen_height,
       tileset=tileset,
       title="Roog Tuts",
       vsync=True, 
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
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
        except BaseException: # svae on any other unexpected exception
            save_game(handler, "savegame.sav")
            raise

if __name__ == "__main__":
    main()