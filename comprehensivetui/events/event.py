from abc import ABC, abstractmethod
from enum import Enum


class EventType(Enum):
    """An EventType enum- extend to add more functionality"""

    TERM_RESIZE = 0
    KEY_SENT = 1
    CLOSE = -1  # close program


class Event[T: EventType](ABC):
    """A basic event"""

    __slots__ = ()

    @property
    @abstractmethod
    def type(self) -> EventType:
        return EventType.TERM_RESIZE


class SimpleEvent[T: EventType](Event):
    """A simple code-only event"""

    __slots__ = "_type"

    _type: T
    """The type of the event"""

    def __init__(self, _type: T):
        self._type = _type

    @property
    def type(self) -> EventType:
        return self._type


class ResizeEvent(Event):
    __slots__ = "width", "height"
    __match_args__ = ("width", "height")

    width: int
    """The number of columns in the resized window"""

    height: int
    """The number of rows/lines in the resized window"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    @property
    def type(self) -> EventType:
        return EventType.TERM_RESIZE


class KeySentEvent(Event):
    """A key press has been sent"""

    __slots__ = "chars"
    __match_args__ = ("codes",)

    chars: bytes
    """The bytes sent in this key event.
    Multiple can be sent in the case of functional keys (arrows, pgup/down, etc)"""

    def __init__(self, chars: bytes):
        self.chars = chars

    @property
    def codes(self) -> list[int]:
        return [char for char in self.chars]

    @property
    def type(self) -> EventType:
        return EventType.KEY_SENT


__all__ = ["EventType", "Event", "SimpleEvent", "ResizeEvent", "KeySentEvent"]
