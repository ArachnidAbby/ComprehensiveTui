"""A module containing definitions of important ANSI escape codes and key codes"""

import math
import sys
from typing import Literal, overload, override

# COLORS- 8 (supported everywhere)
BLACK = "\u001b[30m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
BLUE = "\u001b[34m"
MAGENTA = "\u001b[35m"
CYAN = "\u001b[36m"
WHITE = "\u001b[37m"
## bright
BRIGHT_BLACK = "\u001b[30;1m"
BRIGHT_RED = "\u001b[31;1m"
BRIGHT_GREEN = "\u001b[32;1m"
BRIGHT_YELLOW = "\u001b[33;1m"
BRIGHT_BLUE = "\u001b[34;1m"
BRIGHT_MAGENTA = "\u001b[35;1m"
BRIGHT_CYAN = "\u001b[36;1m"
BRIGHT_WHITE = "\u001b[37;1m"

# COLORS_bg - 8 (supported everywhere)
BG_BLACK = "\u001b[40m"
BG_RED = "\u001b[41m"
BG_GREEN = "\u001b[42m"
BG_YELLOW = "\u001b[43m"
BG_BLUE = "\u001b[44m"
BG_MAGENTA = "\u001b[45m"
BG_CYAN = "\u001b[46m"
BG_WHITE = "\u001b[47m"
## bright
BG_BRIGHT_BLACK = "\u001b[40;1m"
BG_BRIGHT_RED = "\u001b[41;1m"
BG_BRIGHT_GREEN = "\u001b[42;1m"
BG_BRIGHT_YELLOW = "\u001b[43;1m"
BG_BRIGHT_BLUE = "\u001b[44;1m"
BG_BRIGHT_MAGENTA = "\u001b[45;1m"
BG_BRIGHT_CYAN = "\u001b[46;1m"
BG_BRIGHT_WHITE = "\u001b[47;1m"

# SPECIAL
RESET = "\u001b[0m"
BOLD = "\u001b[1m"
UNDERLINE = "\u001b[4m"
REVERSE = "\u001b[7m"

# CONTROL_Codes

FOREGROUND: Literal["38"] = "38"
BACKGROUND: Literal["48"] = "48"
type BG_OR_FG = Literal["38"] | Literal["48"]

type AnsiCode = str

# useful constants
COLOR_CUBE_WIDTH = 240 ** (1 / 3)  # represents a side length of the ANSI-256 color-cube


@overload
def color_256(r: int, /, *, ground: BG_OR_FG = FOREGROUND) -> AnsiCode:
    """Create an ANSI 256 color given its color id"""


@overload
def color_256(
    r: float, g: float, b: float, /, *, ground: BG_OR_FG = FOREGROUND
) -> AnsiCode: ...


def color_256(
    r: float,
    g: float | None = None,
    b: float | None = None,
    /,
    *,
    ground: BG_OR_FG = FOREGROUND,
) -> AnsiCode:
    """Create an ansi color using the 256-color ANSI color cube. 256 colors to choose from"""
    if g is None or b is None:
        return f"\u001b[{ground};5;{r}m"
    # clamp from 0-COLOR_CUB_WIDTH
    r = max(min(r, COLOR_CUBE_WIDTH), 0)
    g = max(min(g, COLOR_CUBE_WIDTH), 0)
    b = max(min(b, COLOR_CUBE_WIDTH), 0)
    # Create final color code
    final_code = min(
        16 + math.ceil(g + (b * COLOR_CUBE_WIDTH) + (r * COLOR_CUBE_WIDTH**2)), 256
    )

    return f"\u001b[{ground};5;{final_code}m"


def rgb_to_ansi(
    r: int, g: int, b: int, /, *, ground: BG_OR_FG = FOREGROUND
) -> AnsiCode:
    """Convert the 256**3 color space (rgb) into the ANSI-256 color cube"""
    r_percent = r / 256
    g_percent = g / 256
    b_percent = b / 256

    ansi_r = r_percent * COLOR_CUBE_WIDTH  # goes 0 - cube_width
    ansi_g = max(g_percent * COLOR_CUBE_WIDTH - 1, 0)
    ansi_b = b_percent * COLOR_CUBE_WIDTH

    final_code = min(
        16
        + math.ceil(
            ansi_g + (ansi_b * COLOR_CUBE_WIDTH) + (ansi_r * COLOR_CUBE_WIDTH**2)
        ),
        256,
    )

    return f"\u001b[38;5;{final_code}m"


if sys.platform == "win32":
    from .windows import (
        BACKSPACE,
        LEFT_ARROW,
        RIGHT_ARROW,
        UP_ARROW,
        DOWN_ARROW,
        PG_UP,
        PG_DOWN,
        ENTER,
        arrow_pressed,
        setup_terminal,
        next_char,
        has_char,
    )
else:
    from .linux import (
        BACKSPACE,
        LEFT_ARROW,
        RIGHT_ARROW,
        UP_ARROW,
        DOWN_ARROW,
        PG_UP,
        PG_DOWN,
        ENTER,
        arrow_pressed,
        setup_terminal,
        next_char,
        has_char,
    )

from .controlcodes import (
    cursor_up,
    cursor_down,
    cursor_left,
    cursor_right,
    set_cursor,
    set_cursor_column,
    next_line,
    previous_line,
    clear_screen,
    clear_line,
    disable_cursor,
    enable_cursor,
    enter_alternative_mode,
    enter_normal_mode,
)
from . import controlcodes

__all__ = [
    # modules
    "controlcodes",
    # colors
    "BLACK",
    "RED",
    "GREEN",
    "YELLOW",
    "BLUE",
    "MAGENTA",
    "CYAN",
    "WHITE",
    "BRIGHT_BLACK",
    "BRIGHT_RED",
    "BRIGHT_GREEN",
    "BRIGHT_YELLOW",
    "BRIGHT_BLUE",
    "BRIGHT_MAGENTA",
    "BRIGHT_CYAN",
    "BRIGHT_WHITE",
    # colors bg
    "BG_BLACK",
    "BG_RED",
    "BG_GREEN",
    "BG_YELLOW",
    "BG_BLUE",
    "BG_MAGENTA",
    "BG_CYAN",
    "BG_WHITE",
    "BG_BRIGHT_BLACK",
    "BG_BRIGHT_RED",
    "BG_BRIGHT_GREEN",
    "BG_BRIGHT_YELLOW",
    "BG_BRIGHT_BLUE",
    "BG_BRIGHT_MAGENTA",
    "BG_BRIGHT_CYAN",
    "BG_BRIGHT_WHITE",
    # special
    "RESET",
    "BOLD",
    "UNDERLINE",
    "REVERSE",
    "BACKGROUND",
    "FOREGROUND",
    # types
    "AnsiCode",
    # functions
    "color_256",
    "rgb_to_ansi",
    # platform stuff
    ## constants
    "BACKSPACE",
    "LEFT_ARROW",
    "RIGHT_ARROW",
    "UP_ARROW",
    "DOWN_ARROW",
    "PG_UP",
    "PG_DOWN",
    "ENTER",
    ## functions
    "arrow_pressed",
    "setup_terminal",
    "next_char",
    "has_char",
    # controlcodes
    ## functions
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
