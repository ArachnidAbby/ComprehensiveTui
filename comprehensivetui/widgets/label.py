from enum import IntEnum, auto

from pytui.events.event import Event, ResizeEvent
from pytui.layouts.align import Align
from pytui.utils.definitions import CYAN
from pytui.utils.strutils import visible_len
from pytui.widgets.widget import Widget


class Label(Widget):
    __slots__ = "_text", "_text_visible_size", "align"

    _text: str
    align: Align
    _text_visible_size: int
    """Visible length of the text- auto calculated as to be cached"""

    def __init__(self, text, align=Align.left, /, *, name=""):
        super().__init__(name=name)
        self.text = text
        self.align = align

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        self._text_visible_size = visible_len(value)

    def handle_event(self, event: Event) -> bool:
        """Handles a given event- returns whether or not the event was handled here"""
        return super().handle_event(event)

    def draw_buffer(self):
        """Mutate self.view to draw the widget. Modified in sub-classes"""
        match self.align:
            case Align.left:
                self.view[0] = self.text
            case Align.center:
                size = (self.width - self._text_visible_size) // 2
                self.view[0] = " " * size + self.text + " " * size
            case Align.right:
                size = self.width - self._text_visible_size
                self.view[0] = self.text + " " * size


__all__ = ["Label"]
