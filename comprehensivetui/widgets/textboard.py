from comprehensivetui.events.event import Event, ResizeEvent
from comprehensivetui.layouts.constraints import Align, Constraints
from comprehensivetui.utils.strutils import break_and_wrap_text, visible_len
from comprehensivetui.widgets.widget import Dirty, Widget


class TextBoard(Widget):
    """A board full of scrollable messages."""

    __slots__ = "lines", "draw_lines", "scroll", "align"

    lines: Dirty[list[str]]
    draw_lines: list[str]
    """broken and wrapped lines"""
    align: Dirty[Align]
    scroll: Dirty[int]
    """scroll offset going from -inf to 0"""

    def __init__(
        self,
        align=Align.left,
        /,
        *,
        name="",
        constraints: Constraints = Constraints(),
    ):
        super().__init__(name=name, constraints=constraints)
        self.lines = []
        self.draw_lines = []
        self.align = align
        self.scroll = 0

    def handle_event(self, event: Event) -> bool:
        """Handles a given event- returns whether or not the event was handled here"""
        if isinstance(event, ResizeEvent):
            self.draw_lines = [
                line
                for raw_line in self.lines
                for line in break_and_wrap_text(raw_line, event.width)
            ]

        return super().handle_event(event)

    def prepare_line(self, text: str) -> str:
        """Mutate self.view to draw the widget. Modified in sub-classes"""
        match self.align:
            case Align.left:
                return text
            case Align.center:
                size = (self.width - visible_len(text)) // 2
                return " " * size + text + " " * size
            case Align.right:
                size = self.width - visible_len(text)
                return text + " " * size

    def draw_buffer(self):
        """Mutate self.view to draw the widget. Modified in sub-classes"""

        start = min(
            max(len(self.draw_lines) + self.scroll - self.height, 0),
            len(self.draw_lines),
        )
        end = start + self.height
        self.view.clear()
        for c, line in enumerate(self.draw_lines[start:end]):
            self.view[c] = self.prepare_line(line)


__all__ = ["TextBoard"]
