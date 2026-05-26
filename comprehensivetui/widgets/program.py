import os
import sys
import time
from typing import Self

from comprehensivetui.events.event import Event, KeySentEvent, ResizeEvent
from comprehensivetui.utils.definitions import (
    has_char,
    next_char,
    arrow_pressed,
    ARROW_COMBINATION_SIZE,
)
from comprehensivetui.utils.definitions.controlcodes import (
    clear_screen,
    disable_cursor,
    enable_cursor,
    enter_alternative_mode,
    enter_normal_mode,
    set_cursor,
)
from comprehensivetui.widgets.widget import Widget


class Program(Widget):
    __slots__ = "running", "rate", "title"

    running: bool
    rate: int
    """framerate"""
    title: str

    def __init__(self, title: str, rate: int, *, name=""):
        super().__init__(name=name)
        self.running = False
        self.rate = rate  # framerate
        self.title = title

    def handle_event(self, event: Event) -> bool:
        """Handles a given event- returns whether or not the event was handled here"""
        return super().handle_event(event) or any(
            child.handle_event(event) for child in self.children
        )

    def draw_buffer(self):
        """Mutate self.view to draw the widget. Modified in sub-classes"""

    def start(self: Self):
        """Entry point for the program."""
        self.running = True
        term_size = os.get_terminal_size()
        events: list[Event] = [ResizeEvent(term_size.columns, term_size.lines)]
        try:
            sys.stdout.write(set_cursor(0, 0))
            sys.stdout.write(disable_cursor() + enter_alternative_mode())
            sys.stdout.write(f"\u001b]0;{self.title}\007")
            sys.stdout.flush()

            while self.running:
                keys = []
                while has_char():
                    char = next_char()
                    key = ord(char)
                    keys.append(key)
                while len(keys) > 0:
                    if arrow_pressed(keys):
                        events.append(
                            KeySentEvent(bytes(keys[:ARROW_COMBINATION_SIZE]))
                        )
                        keys = keys[ARROW_COMBINATION_SIZE:]
                        continue
                    key = keys.pop(0)
                    events.append(KeySentEvent(bytes([key])))  # push keys as-is

                term_size = os.get_terminal_size()
                if term_size.columns != self.width or term_size.lines != self.height:
                    events.append(ResizeEvent(term_size.columns, term_size.lines))

                for event in events:
                    self.handle_event(event)

                self.draw()
                sys.stdout.write(set_cursor(0, 0))
                sys.stdout.write(self.view.to_flat(self.height, self.width))
                sys.stdout.flush()
                time.sleep(1 / self.rate)
        except KeyboardInterrupt:
            sys.stdout.write(clear_screen())
        finally:
            sys.stdout.write(enable_cursor() + enter_normal_mode())
            sys.stdout.flush()
