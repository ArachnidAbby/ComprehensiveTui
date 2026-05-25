from typing import overload, override

from pytui.utils.definitions import RESET
from pytui.utils.strutils import normalize_line


class DrawableView:
    """A buffer of lines that are easy to draw to the console"""

    __slots__ = "lines"

    lines: list[str]

    def __init__(self):
        self.lines = []

    def __setitem__(self, key: int, value: str):
        if key >= len(self.lines):
            self.lines += [""] * (key - len(self.lines) + 1)
        self.lines[key] = value

    @overload
    def __getitem__(self, key: int) -> str: ...

    @overload
    def __getitem__(self, key: slice) -> list[str]: ...

    def __getitem__(self, key: int | slice) -> str | list[str]:
        if isinstance(key, int) and key <= len(self.lines):
            self.lines += [""] * (key - len(self.lines) + 1)
        elif isinstance(key, slice) and key.stop <= len(self.lines):
            self.lines += [""] * (key.stop - len(self.lines) + 1)

        return self.lines[key]

    def reset(self):
        """Resets the value of self.lines"""
        for i in range(len(self.lines)):
            self.lines[i] = ""

    def reset_full(self):
        """Reset the view fully by emptying self.lines fully- equivelent to instantiating a new view"""
        self.lines = []

    def to_flat(self, rows: int, columns: int) -> str:
        """Turns the view into a flat string to be shown on the console"""
        if rows < len(self.lines):
            self.lines += [""] * (rows - len(self.lines) + 1)
        return "\n".join(
            normalize_line(line, columns) + RESET for line in self.lines[:rows]
        )

    def to_normalized(self, rows: int, columns: int) -> list[str]:
        """Create a normalized list of lines"""
        if rows < len(self.lines):
            self.lines += [""] * (rows - len(self.lines) + 1)
        return [normalize_line(line, columns) + RESET for line in self.lines[:rows]]


__all__ = ["DrawableView"]
