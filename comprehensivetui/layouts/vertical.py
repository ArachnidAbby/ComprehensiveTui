import typing

from comprehensivetui.events.event import ResizeEvent
from comprehensivetui.layouts.constraints import clamp_value
from comprehensivetui.layouts.layout import Layout, LayoutSize

if typing.TYPE_CHECKING:
    from ..widgets.widget import Widget


class VerticalLayout(Layout):
    """A layout that handles resizing and combining widgets"""

    __slots__ = ()

    def handle_resize(self, event: ResizeEvent):
        super().handle_resize(event)

    def calculate_widget_size(self, child: "Widget") -> LayoutSize:
        if child is self.parent:
            return LayoutSize(self.width, self.height)
        if child not in self.parent.children:
            return (child.parent or child).get_default_child_size()

        child_idx = self.parent.children.index(child)
        if child_idx == 0:
            missing_lines = self.height % len(self.parent.children)
            ideal_height = self.height // len(self.parent.children) + (
                (child_idx + 1) % max(missing_lines, 1) > 0
            )
            return LayoutSize(
                clamp_value(child.min_width, child.max_width, self.width),
                clamp_value(child.min_height, child.max_height, ideal_height),
            )
        already_taken_space = sum(
            self.calculate_widget_size(child).height
            for child in self.parent.children[:child_idx]
        )
        space_left = self.height - already_taken_space

        missing_lines = space_left % (len(self.parent.children) - child_idx)
        ideal_height = space_left // (len(self.parent.children) - child_idx) + (
            (child_idx + 1) % max(missing_lines, 1) > 0
        )
        return LayoutSize(
            clamp_value(child.min_width, child.max_width, self.width),
            clamp_value(child.min_height, child.max_height, ideal_height),
        )

    def draw(self) -> list[str]:
        output = []
        for child in self.parent.children:
            child.draw()
            output += child.view.to_normalized(child.height, child.width)
        return output
