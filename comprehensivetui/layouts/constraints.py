from enum import IntEnum, auto
from typing import NamedTuple


class Align(IntEnum):
    """Alignment of text and widgets"""

    left = auto()
    center = auto()
    right = auto()


class Constraints(NamedTuple):
    """Size Constraints for a widget"""

    min_width: int | None = None
    min_height: int | None = None
    max_width: int | None = None
    max_height: int | None = None


def clamp_value(min_value: int | None, max_value: int | None, ideal_value: int) -> int:
    match min_value, max_value:
        case None, None:
            return ideal_value
        case None, int(max_v):
            return min(ideal_value, max_v)
        case int(min_v), None:
            return max(ideal_value, min_v)
        case int(min_v), int(max_v):
            return min(max(ideal_value, min_v), max_v)
    return ideal_value  # fallback so my IDE stops crying


__all__ = ["Align"]
