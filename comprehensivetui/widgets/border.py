from comprehensivetui.events.event import Event, ResizeEvent
from comprehensivetui.layouts.constraints import Constraints
from comprehensivetui.layouts.layout import LayoutSize
from comprehensivetui.utils.definitions import (
    ENTER_LINE_DRAWING_MODE,
    EXIT_LINE_DRAWING_MODE,
)
from comprehensivetui.utils.strutils import normalize_line, visible_len
from comprehensivetui.widgets.widget import Dirty, Widget


class Border(Widget):
    __slots__ = ("show_left", "show_right", "show_up", "show_down")

    show_left: Dirty[bool]
    show_right: Dirty[bool]
    show_up: Dirty[bool]
    show_down: Dirty[bool]

    def __init__(
        self,
        inner: Widget | None = None,
        /,
        *,
        left: bool = True,
        right: bool = True,
        up: bool = True,
        down: bool = True,
        name="",
        constraints: Constraints = Constraints(),
    ):
        super().__init__(name=name, constraints=constraints)
        self.show_left = left
        self.show_right = right
        self.show_up = up
        self.show_down = down
        if inner:
            self.add_child(inner)

    def get_default_child_size(self) -> LayoutSize:
        return LayoutSize(
            self.width - self.show_left - self.show_right,
            self.height - self.show_up - self.show_down,
        )

    def handle_event(self, event: Event) -> bool:
        """Handles a given event- returns whether or not the event was handled here"""
        match event:
            case ResizeEvent(_, _):

                modified_event = ResizeEvent(
                    event.width - self.show_left - self.show_right,
                    event.height - self.show_up - self.show_down,
                )
                if self._layout is not None:
                    self._layout.handle_resize(modified_event)

                    given_size = self._layout.get_widget_size(self)
                    self._size = LayoutSize(
                        given_size.width + self.show_left + self.show_right,
                        given_size.height + self.show_up + self.show_down,
                    )
                else:
                    self._size = self.get_layout().get_widget_size(self)

                for child in self.children:
                    child.handle_event(modified_event)
                return True
        return any(child.handle_event(event) for child in self.children)

    def draw_buffer(self):
        """Mutate self.view to draw the widget. Modified in sub-classes"""
        if len(self.children) > 1:
            return
        self.children[0].draw()

        self.children[0].view.lines = self.children[0].view.to_normalized(
            self.children[0].height, self.children[0].width
        )

        top_line = [
            ENTER_LINE_DRAWING_MODE
            + ("l" if self.show_left else " ")
            + "q" * (self.width - 2)
            + ("k" if self.show_right else " ")
            + EXIT_LINE_DRAWING_MODE
        ] * self.show_up
        bottom_line = [
            ENTER_LINE_DRAWING_MODE
            + ("m" if self.show_left else " ")
            + "q" * (self.width - 2)
            + ("j" if self.show_right else " ")
            + EXIT_LINE_DRAWING_MODE
        ] * self.show_down

        self.view.lines = [
            *top_line,
            *(
                (
                    f"{ENTER_LINE_DRAWING_MODE}x{EXIT_LINE_DRAWING_MODE}"
                    * self.show_left
                    + line
                    + f"{ENTER_LINE_DRAWING_MODE}x{EXIT_LINE_DRAWING_MODE}"
                    * self.show_right
                )
                for line in self.children[0].view.lines
            ),
            *bottom_line,
        ]

    def draw(self):
        """Mutate self.view to draw the widget."""
        if not self.dirty:
            return
        super().draw()
