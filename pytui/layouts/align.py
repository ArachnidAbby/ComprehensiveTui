from enum import IntEnum, auto


class Align(IntEnum):
    """Alignment of text and widgets"""

    left = auto()
    center = auto()
    right = auto()


__all__ = ["Align"]
