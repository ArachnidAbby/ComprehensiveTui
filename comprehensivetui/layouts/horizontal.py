import typing

from comprehensivetui.events.event import ResizeEvent
from comprehensivetui.layouts.layout import Layout, LayoutSize

if typing.TYPE_CHECKING:
    from ..widgets.widget import Widget


class HorizontalLayout(Layout):
    """A layout that handles resizing and combining widgets"""

    __slots__ = ()

    def handle_resize(self, event: ResizeEvent):
        super().handle_resize(event)

    def calculate_widget_size(self, child: "Widget"):
        if child is self.parent:
            return LayoutSize(self.width, self.height)
        return LayoutSize(self.width // len(self.parent.children), self.height)

    def draw(self) -> list[str]:
        frames = []

        for child in self.parent.children:
            child.draw()
            frames.append(child.view.to_normalized(child.height, child.width))

        output = [""] * max(len(frame) for frame in frames)
        for frame in frames:
            for c, line in enumerate(frame):
                output[c] += line

        return output
