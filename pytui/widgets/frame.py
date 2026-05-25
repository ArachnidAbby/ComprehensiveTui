from pytui.events.event import Event
from pytui.layouts.layout import Layout
from pytui.widgets.widget import Widget


class Frame(Widget):
    __slots__ = ()

    def __init__(self, children: list[Widget], layout: Layout, *, name=""):
        super().__init__(name=name)
        for child in children:
            self.add_child(child)

        self.set_layout(layout)

    def handle_event(self, event: Event) -> bool:
        """Handles a given event- returns whether or not the event was handled here"""
        return super().handle_event(event) or any(
            [child.handle_event(event) for child in self.children]
        )  # uses list form so all children handle the event

    def draw_buffer(self):
        """Mutate self.view to draw the widget. Modified in sub-classes"""


__all__ = ["Frame"]
