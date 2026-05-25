import typing

from comprehensivetui.events.event import ResizeEvent
from comprehensivetui.layouts.layout import Layout, LayoutSize

if typing.TYPE_CHECKING:
    from ..widgets.widget import Widget


class VerticalLayout(Layout):
    """A layout that handles resizing and combining widgets"""

    __slots__ = ()

    def handle_resize(self, event: ResizeEvent):
        super().handle_resize(event)

    def calculate_widget_size(self, child: "Widget"):
        if child is self.parent:
            return LayoutSize(self.width, self.height)
        missing_lines = self.height % len(self.parent.children)
        return LayoutSize(
            self.width,
            self.height // len(self.parent.children)
            + ((self.parent.children.index(child) + 1) % max(missing_lines, 1) > 0),
        )

    def draw(self) -> list[str]:
        output = []
        for child in self.parent.children:
            child.draw()
            output += child.view.to_normalized(child.height, child.width)
        return output
