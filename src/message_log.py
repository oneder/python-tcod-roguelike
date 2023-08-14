from typing import Iterable, List, Reversible, Tuple
import textwrap

import tcod

import src.color as color

class Message:
    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.plain_text = text
        self.fg = fg
        self.count = 1

    @property
    def full_text(self) -> str:
        # the full text of this message
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text
    
class MessageLog:
    def __init__(self) -> None:
        self.messages: List[Message] = []

    def add_message(
            self, text: str, fg: Tuple[int, int, int] = color.white, *, stack: bool = True,
    ) -> None:
        # `text` is the message text, `fg` is the text color
        # if stack=true, then the message can stack with a previous message
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(
            self, console: tcod.console.Console, x: int, y: int, width: int, height: int,
    ) -> None:
        # render this log over the given area
        # `x`, `y`, `width`, `height` is the rectangular region to render onto the console
        self.render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def wrap(string: str, width: int) -> Iterable[str]:
        # return a wrapped text message
        for line in string.splitlines():
            yield from textwrap.wrap(
                line, width, expand_tabs=True,
            )

    @classmethod
    def render_messages(
        cls,
        console: tcod.Console,
        x: int,
        y: int,
        width: int,
        height: int,
        messages: Reversible[Message],
    ) -> None:
        # render the messages provided
        # last message, first
        y_offset = height - 1

        for message in reversed(messages):
            for line in reversed(list(cls.wrap(message.full_text, width))):
                console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
                y_offset -= 1
                if y_offset < 0:
                    return