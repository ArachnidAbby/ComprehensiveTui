from comprehensivetui.events.event import Event
from comprehensivetui.layouts.constraints import Constraints
from comprehensivetui.layouts.layout import Layout
from comprehensivetui.widgets.widget import Widget


class Frame(Widget):
    __slots__ = ()

    def __init__(
        self,
        children: list[Widget],
        layout: Layout,
        *,
        name="",
        constraints: Constraints = Constraints(),
    ):
        super().__init__(name=name, constraints=constraints)
        self.set_children(children)
        self.set_layout(layout)

    def handle_event(self, event: Event) -> bool:
        """Handles a given event- returns whether or not the event was handled here"""
        return super().handle_event(event)

    def draw_buffer(self):
        """Mutate self.view to draw the widget. Modified in sub-classes"""


__all__ = ["Frame"]
