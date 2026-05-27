from abc import ABC, abstractmethod
from typing import NamedTuple
import typing

from comprehensivetui.events.event import ResizeEvent
from comprehensivetui.layouts.constraints import Constraints, clamp_value

if typing.TYPE_CHECKING:
    from ..widgets.widget import Widget


class LayoutSize(NamedTuple):
    """A size measurement given by a layout to a child member"""

    width: int
    height: int


class Layout(ABC):
    """A layout that handles resizing and combining widgets"""

    __slots__ = "width", "height", "parent"

    parent: "Widget"
    """Parent widget that contains layout children"""
    width: int
    """Number of columns/chars wide"""
    height: int
    """Number of lines/rows tall"""

    def __init__(self):
        self.width = -1
        self.height = -1

    def set_parent(self, parent):
        self.parent = parent

    @abstractmethod
    def handle_resize(self, event: ResizeEvent):
        self.width = clamp_value(
            self.parent.min_width, self.parent.max_width, event.width
        )
        print(event.height)
        self.height = clamp_value(
            self.parent.min_height, self.parent.max_height, event.height
        )
        print(self.height, self.parent.min_height, self.parent.max_height)
        for child in self.parent.children:
            child_size = self.calculate_widget_size(child)
            child.handle_event(ResizeEvent(child_size.width, child_size.height))

    @abstractmethod
    def calculate_widget_size(self, child: "Widget") -> LayoutSize:
        if child is self.parent:
            return LayoutSize(self.width, self.height)
        return LayoutSize(-1, -1)

    def get_widget_size(self, child: "Widget") -> LayoutSize:
        if (
            child.get_layout() is not self
            and child.parent is not None
            and child.parent.get_layout() is not self
        ):
            raise IndexError("Could not find child in layout")
        return self.calculate_widget_size(child)

    @abstractmethod
    def draw(self) -> list[str]: ...
