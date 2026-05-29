"""A module containing our base widget"""

from abc import ABC, ABCMeta, abstractmethod
from types import GenericAlias

from comprehensivetui.layouts.constraints import Constraints
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
        instance._dirty = True

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
        "_dirty",
        "_constraints",
    )

    children: Dirty[list["Widget"]]
    """Child elements, necessary for passing inputs, events, etc."""
    _layout: Dirty[Layout | None]
    """The layout of the widget- controls resizing"""
    parent: "Widget | None"
    _size: Dirty[LayoutSize]
    _constraints: Dirty[Constraints]
    """Size constraints"""
    _name: str
    view: DrawableView
    """The drawn frame for this widget"""
    _dirty: bool
    """Whether or not the widget needs to be redrawn."""

    def __init__(self, *, name="", constraints: Constraints = Constraints()):
        self.children = []
        self._size = LayoutSize(-1, -1)
        self.parent = None
        self._layout = None
        self.view = DrawableView()
        self._name = name
        self._constraints = constraints

    def set_constraints(self, constraints: Constraints):
        self._constraints = constraints

    @property
    def min_width(self) -> int | None:
        if self._constraints.min_width is None and len(self.children) > 0:
            return sum(
                child.min_width
                for child in self.children
                if child.min_width is not None
            )
        return self._constraints.min_width

    @property
    def min_height(self) -> int | None:
        if self._constraints.min_height is None and len(self.children) > 0:
            return sum(
                child.min_height
                for child in self.children
                if child.min_height is not None
            )
        return self._constraints.min_height

    @property
    def max_width(self) -> int | None:
        return self._constraints.max_width

    @property
    def max_height(self) -> int | None:
        return self._constraints.max_height

    @property
    def width(self) -> int:
        return self._size.width

    @property
    def height(self) -> int:
        return self._size.height

    @property
    def dirty(self):
        return self._dirty or any(child.dirty for child in self.children)

    def set_children(self, children: list["Widget"]):
        for child in children:
            self.add_child(child)

    def add_child(self, child: "Widget"):
        child.parent = self
        self.children.append(child)
        self._dirty = True

    def remove_child(self, child: "Widget"):
        if child.parent is not self:
            return
        child.parent = None
        self.children.remove(child)
        self._dirty = True

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

    def dispatch_event(self, event: Event) -> bool:
        """Give an event to this widget to handle and propagate to its children"""
        own_output = self.handle_event(event)
        return self.propagate_event(event) or own_output

    def propagate_event(self, event) -> bool:
        out = False
        for child in self.children:
            out = out | child.dispatch_event(event)
        return out

    def get_default_child_size(self) -> LayoutSize:
        """The default size of an indirect child-element if a direct child has no layout (but has children)"""
        return self._size

    @abstractmethod
    def draw_buffer(self):
        """Mutate self.view to draw the widget. Modified in sub-classes"""

    def draw(self):
        """Mutate self.view to draw the widget"""
        if not self.dirty:
            return
        self.view.clear()
        if self._layout is not None:
            self.view.lines = self._layout.draw()
        self.draw_buffer()
        self._dirty = False

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} "{self._name}">'


__all__ = ["Widget", "Dirty", "WidgetMeta", "DirtyProperty"]
