import os
import sys
import time
from typing import Self

from comprehensivetui.events.event import Event, KeySentEvent, ResizeEvent
from comprehensivetui.layouts.constraints import Constraints
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
    restore_cursor,
    save_cursor,
    set_cursor,
)
from comprehensivetui.utils.definitions.windows import setup_terminal
from comprehensivetui.widgets.widget import Widget


class Program(Widget):
    __slots__ = "running", "rate", "title"

    running: bool
    rate: int
    """framerate"""
    title: str

    def __init__(
        self,
        title: str,
        rate: int,
        *,
        name="",
        constraints: Constraints = Constraints(),
    ):
        super().__init__(name=name, constraints=constraints)
        self.running = False
        self.rate = rate  # framerate
        self.title = title

    def handle_event(self, event: Event) -> bool:
        """Handles a given event- returns whether or not the event was handled here"""
        return super().handle_event(event)

    def draw_buffer(self):
        """Mutate self.view to draw the widget. Modified in sub-classes"""

    def on_frame(self): ...

    def start(self: Self):
        """Entry point for the program."""
        self.running = True
        term_size = os.get_terminal_size()
        events: list[Event] = [ResizeEvent(term_size.columns, term_size.lines)]
        try:
            setup_terminal()
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

                while len(events) > 0 and (event := events.pop(0)):
                    self.dispatch_event(event)

                self.draw()
                sys.stdout.write(set_cursor(0, 0))
                sys.stdout.write(self.view.to_flat(self.height, self.width))
                sys.stdout.flush()
                self.on_frame()
                time.sleep(1 / self.rate)
        except KeyboardInterrupt:
            pass
        finally:
            sys.stdout.write(
                enable_cursor()
                + enter_normal_mode()
                + clear_screen()
                + restore_cursor()
            )
            sys.stdout.flush()
