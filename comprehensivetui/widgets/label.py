from enum import IntEnum, auto

from comprehensivetui.events.event import Event, ResizeEvent
from comprehensivetui.layouts.align import Align
from comprehensivetui.utils.definitions import CYAN
from comprehensivetui.utils.strutils import break_and_wrap_text, visible_len
from comprehensivetui.widgets.widget import Dirty, Widget


class Label(Widget):
    __slots__ = "text", "align"

    text: Dirty[str]
    align: Dirty[Align]
    """Visible length of the text- auto calculated as to be cached"""

    def __init__(self, text, align=Align.left, /, *, name=""):
        super().__init__(name=name)
        self.text = text
        self.align = align

    def handle_event(self, event: Event) -> bool:
        """Handles a given event- returns whether or not the event was handled here"""
        return super().handle_event(event)

    def draw_buffer(self):
        """Mutate self.view to draw the widget. Modified in sub-classes"""
        lines = break_and_wrap_text(self.text, self.width)
        for c, line in enumerate(lines):
            match self.align:
                case Align.left:
                    self.view[c] = line
                case Align.center:
                    size = (self.width - visible_len(line)) // 2
                    self.view[c] = " " * size + line + " " * size
                case Align.right:
                    size = self.width - visible_len(line)
                    self.view[c] = self.text + " " * size


__all__ = ["Label"]
