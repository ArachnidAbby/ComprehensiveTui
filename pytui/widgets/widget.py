"""A module containing our base widget"""

from abc import ABC, abstractmethod

from pytui.layouts.layout import Layout, LayoutSize
from pytui.widgets.view import DrawableView
from ..events.event import Event, ResizeEvent


class Widget(ABC):
    """A basic widget. It controls how it draws and its what it does with captured inputs"""

    __slots__ = "children", "_layout", "parent", "__size", "view", "visible", "_name"

    children: list["Widget"]
    """Child elements, necessary for passing inputs, events, etc."""
    _layout: Layout | None
    """The layout of the widget- controls resizing"""
    parent: "Widget | None"
    __size: LayoutSize
    _name: str
    view: DrawableView
    """The drawn frame for this widget"""

    def __init__(self, *, name=""):
        self.children = []
        self.__size = LayoutSize(-1, -1)
        self.parent = None
        self._layout = None
        self.view = DrawableView()
        self._name = name

    def add_child(self, child: "Widget"):
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: "Widget"):
        if child.parent is not self:
            return
        child.parent = None
        self.children.remove(child)

    def set_layout(self, layout: Layout):
        if self._layout is not None:
            del self._layout.parent
        layout.parent = self
        self._layout = layout

    def get_layout(self) -> Layout:
        if self._layout is not None:
            return self._layout
        elif self.parent is not None:
            return self.parent.get_layout()
        else:
            raise Exception("Parent not found for widget")

    @property
    def width(self) -> int:
        return self.__size.width

    @property
    def height(self) -> int:
        return self.__size.height

    @abstractmethod
    def handle_event(self, event: Event) -> bool:
        """Handles a given event- returns whether or not the event was handled here"""
        match event:
            case ResizeEvent(_, _):
                if self._layout is not None:
                    self._layout.handle_resize(event)
                self.__size = self.get_layout().get_widget_size(self)
                return True
        return False

    @abstractmethod
    def draw_buffer(self):
        """Mutate self.view to draw the widget. Modified in sub-classes"""

    def draw(self):
        """Mutate self.view to draw the widget"""
        if self._layout is not None:
            self.view.lines = self._layout.draw()
        else:
            self.draw_buffer()

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} "{self._name}">'


__all__ = ["Widget"]
