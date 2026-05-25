import sys

if sys.platform != "win32":
    raise ImportError("Cannot import module on linux/mac platforms")

import msvcrt

# Key combinations
BACKSPACE = 8
LEFT_ARROW = 75
RIGHT_ARROW = 77
UP_ARROW = 72
DOWN_ARROW = 80
PG_UP = 73
PG_DOWN = 81
ENTER = 13


def arrow_pressed(key: int) -> bool:
    """detects if an arrow-key was pressed. Arrow keys are combinations of 2 key presses. The first being keycode 224"""
    return key == 224


def setup_terminal():
    """A common function for setting up the terminal.
    Enables ANSI codes in systems which might not immediately support them"""
    import ctypes

    kernel32 = ctypes.windll.kernel32
    # -11 corresponds to the standard output (stdout) handle
    handle = kernel32.GetStdHandle(-11)
    # Flags: ENABLE_VIRTUAL_TERMINAL_PROCESSING (0x0004)
    mode = ctypes.c_ulong()
    if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
        # Apply the virtual terminal flag, keeping other modes intact
        kernel32.SetConsoleMode(handle, mode.value | 0x0004)

    # Enable Windows ANSI/VT processing
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(handle, 7)


def next_char() -> bytes:
    """Alias msvcrt.getch() to have a common interface on all platforms"""
    return msvcrt.getch()


def has_char() -> bool:
    """Alias for msvcrt.kbhit() to have a common interface. Checks if another byte is available in stdin"""
    return msvcrt.kbhit()


__all__ = [
    # constants
    "BACKSPACE",
    "LEFT_ARROW",
    "RIGHT_ARROW",
    "UP_ARROW",
    "DOWN_ARROW",
    "PG_UP",
    "PG_DOWN",
    "ENTER",
    # functions
    "arrow_pressed",
    "setup_terminal",
    "next_char",
    "has_char",
]
