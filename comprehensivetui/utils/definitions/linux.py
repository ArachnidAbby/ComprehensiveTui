import sys

if sys.platform == "win32":
    raise ImportError("Cannot import module on windows platforms")

import tty
import select
import termios
import atexit

BACKSPACE = 127
LEFT_ARROW = 68
RIGHT_ARROW = 67
UP_ARROW = 65
DOWN_ARROW = 66
PG_UP = 53
PG_DOWN = 54
ENTER = 10

ARROW_COMBINATION_SIZE = 4


def arrow_pressed(keys: list[int]) -> bool:
    """Checks if an arrow key is pressed. This is a combination of 4 keys- [27, 91, 91, ARROW_KEY_CODE]"""
    if len(keys) < 4 or keys[0] != 27:
        return False
    return keys[1] == 91 and keys[2] == 91


def _enable_echo(fd, enabled):
    """Enables and disable input echoing"""
    iflag, oflag, cflag, lflag, ispeed, ospeed, cc = termios.tcgetattr(fd)

    if enabled:
        lflag |= termios.ECHO
    else:
        lflag &= ~termios.ECHO

    new_attr = [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
    termios.tcsetattr(fd, termios.TCSANOW, new_attr)


def setup_terminal():
    """Sets up the terminal environment."""
    tty.setcbreak(sys.stdin)
    _enable_echo(sys.stdin.fileno(), False)
    atexit.register(_enable_echo, sys.stdin.fileno(), True)


def next_char() -> bytes:
    """Get next char from stdin"""
    return sys.stdin.read(1).encode()


def has_char() -> bool:
    """Checks if another char is available in stdin. Common interfacing"""
    return select.select([sys.stdin], [], [], 0)[0]


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
    "ARROW_COMBINATION_SIZE",
    # functions
    "arrow_pressed",
    "setup_terminal",
    "next_char",
    "has_char",
]
