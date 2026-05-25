import typing
from typing import Literal

if typing.TYPE_CHECKING:
    from . import AnsiCode


def cursor_up(n: int = 0, /) -> "AnsiCode":
    return f"\u001b[{n}A"


def cursor_down(n: int = 0, /) -> "AnsiCode":
    return f"\u001b[{n}B"


def cursor_left(n: int = 0, /) -> "AnsiCode":
    return f"\u001b[{n}D"


def cursor_right(n: int = 0, /) -> "AnsiCode":
    return f"\u001b[{n}C"


def set_cursor(x: int, y: int, /) -> "AnsiCode":
    return f"\u001b[{x};{y}H"


def set_cursor_column(x: int, /) -> "AnsiCode":
    return f"\u001b[{x}G"


def next_line(n: int = 0, /) -> "AnsiCode":
    return f"\u001b[{n}E"


def previous_line(n: int = 0, /) -> "AnsiCode":
    return f"\u001b[{n}F"


def clear_screen(n: Literal[0] | Literal[1] | Literal[2] = 2, /) -> "AnsiCode":
    """Clears the screen. Will cause flickering.
    - 0 = clear cursor till end of screen
    - 1 = clear from beginning of screen till to the cursor
    - 2 - default = clear entire screen"""
    return f"\u001b[{n}J"


def clear_line(n: Literal[0] | Literal[1] | Literal[2] = 2, /) -> "AnsiCode":
    """Clears the current line. Will cause flickering.
    - 0 = clear cursor till end of line
    - 1 = clear from beginning of line till to the cursor
    - 2 - default = clear entire line"""
    return f"\u001b[{n}K"


def disable_cursor() -> "AnsiCode":
    return "\u001b[?25l"


def enable_cursor() -> "AnsiCode":
    return "\u001b[?25h"


def enter_alternative_mode() -> "AnsiCode":
    """Enter alternative drawing mode"""
    return "\u001b[?1049h"


def enter_normal_mode() -> "AnsiCode":
    """Exit alternative drawing mode"""
    return "\u001b[?1049l"


__all__ = [
    "cursor_up",
    "cursor_down",
    "cursor_left",
    "cursor_right",
    "set_cursor",
    "set_cursor_column",
    "next_line",
    "previous_line",
    "clear_screen",
    "clear_line",
    "disable_cursor",
    "enable_cursor",
    "enter_alternative_mode",
    "enter_normal_mode",
]
