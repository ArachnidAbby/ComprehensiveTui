"""A module containing our base widget"""

from abc import ABC, ABCMeta, abstractmethod
from types import GenericAlias

from comprehensivetui.layouts.layout import Layout, LayoutSize
from comprehensivetui.widgets.view import DrawableView
from ..events.event import Event, ResizeEvent


class DirtyProperty[T]():
    """A property that sets something as dirty"""

    __slots__ = "name"

    def __set_name__(self, owner, name: str):
        self.name = "_dirty_" + name

    def __set__(self, instance: "Widget", value: T):
        setattr(instance, self.name, value)
        instance.dirty = True

    def __get__(self, instance: "Widget", owner):
        return getattr(instance, self.name)


type Dirty[T] = T
"""Uses some magic to automatically set widgets as dirty when this attribute is modified"""


class WidgetMeta(ABCMeta):
    """Metaclass that makes `Dirty[T] work fully"""

    def __new__(cls, clsname, bases, attrs: dict):
        dirty_props = {
            name: annot
            for name, annot in bases[0].__annotations__.items()
            if isinstance(annot, GenericAlias) and annot.__name__ == Dirty.__name__
        }
        for prop in dirty_props.keys():
            attrs[prop] = DirtyProperty()

        if "__slots__" in attrs.keys():
            attrs["__slots__"] = (
                *(
                    slot
                    for slot in attrs.get("__slots__", [])
                    if slot not in dirty_props.keys()
                ),
                *("_dirty_" + prop for prop in dirty_props.keys()),
            )

        x = super().__new__(cls, clsname, bases, attrs)
        return x


class Widget(ABC, metaclass=WidgetMeta):
    """A basic widget. It controls how it draws and its what it does with captured inputs"""

    __slots__ = (
        "children",
        "_layout",
        "parent",
        "_size",
        "view",
        "visible",
        "_name",
        "dirty",
    )

    children: Dirty[list["Widget"]]
    """Child elements, necessary for passing inputs, events, etc."""
    _layout: Dirty[Layout | None]
    """The layout of the widget- controls resizing"""
    parent: "Widget | None"
    _size: Dirty[LayoutSize]
    _name: str
    view: DrawableView
    """The drawn frame for this widget"""
    dirty: bool
    """Whether or not the widget needs to be redrawn."""

    def __init__(self, *, name=""):
        self.children = []
        self._size = LayoutSize(-1, -1)
        self.parent = None
        self._layout = None
        self.view = DrawableView()
        self._name = name

    def set_children(self, children: list["Widget"]):
        for child in children:
            self.add_child(child)

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
        return self._size.width

    @property
    def height(self) -> int:
        return self._size.height

    @abstractmethod
    def handle_event(self, event: Event) -> bool:
        """Handles a given event- returns whether or not the event was handled here"""
        match event:
            case ResizeEvent(_, _):
                if self._layout is not None:
                    self._layout.handle_resize(event)
                self._size = self.get_layout().get_widget_size(self)
                return True
        return False

    @abstractmethod
    def draw_buffer(self):
        """Mutate self.view to draw the widget. Modified in sub-classes"""

    def draw(self):
        """Mutate self.view to draw the widget"""
        if not self.dirty:
            return
        if self._layout is not None:
            self.view.lines = self._layout.draw()
        else:
            self.draw_buffer()

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} "{self._name}">'


__all__ = ["Widget", "Dirty", "WidgetMeta", "DirtyProperty"]
