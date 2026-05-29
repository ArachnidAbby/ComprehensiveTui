from enum import IntEnum, auto

from comprehensivetui.events.event import Event, ResizeEvent
from comprehensivetui.layouts.constraints import Align, Constraints
from comprehensivetui.utils.definitions import RESET, REVERSE
from comprehensivetui.utils.strutils import (
    break_and_wrap_text,
    get_visible_index,
    visible_len,
)
from comprehensivetui.widgets.widget import Dirty, Widget


class Editor(Widget):
    """A very functional editor with well-designed cursor controls (not bound to keys- subclass to bind events)"""

    __slots__ = (
        "_text",
        "lines",
        "scroll",
        "cursor_row",
        "cursor_col",
        "align",
        "focused",
        "insert_mode",
    )

    _text: Dirty[str]
    lines: list[str]
    """Calculated lines of our self.text"""
    cursor_col: Dirty[int]
    cursor_row: Dirty[int]
    focused: bool
    """broken and wrapped lines"""
    align: Align
    scroll: Dirty[int]
    """scroll offset going from 0 - inf"""

    def __init__(
        self,
        align=Align.left,
        /,
        *,
        name="",
        constraints: Constraints = Constraints(),
    ):
        super().__init__(name=name, constraints=constraints)
        self.text = ""
        self.focused = True
        self.align = align
        self.scroll = 0
        self.insert_mode = False
        self.cursor_col = 0
        self.cursor_row = 0

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        self.lines = value.split("\n")

    @property
    def wrap_len(self) -> int:
        """The amount of characters before line wrapping occurs. Default: self.width"""
        return self.width

    def handle_event(self, event: Event) -> bool:
        """Handles a given event- returns whether or not the event was handled here"""
        return super().handle_event(event)

    def cursor_left(self):
        """moves the cursor left by one"""
        if self.cursor_col == 0 and self.cursor_row != 0:
            self.cursor_up()
            self.cursor_col = visible_len(self.lines[self.cursor_row])
        else:
            self.cursor_col = max(self.cursor_col - 1, 0)

    def cursor_right(self):
        """moves the cursor right by one"""

        if self.cursor_col == visible_len(
            self.lines[self.cursor_row]
        ) - 1 and self.cursor_row != len(self.lines):
            self.cursor_down()
            self.cursor_col = 0
        else:
            self.cursor_col = min(self.cursor_col + 1, len(self.text))

    def cursor_up(self):
        """Moves the cursor up by one"""
        sub_lines = break_and_wrap_text(self.lines[self.cursor_row], self.wrap_len)
        original_row = self.cursor_row
        if len(sub_lines) > 1 and self.cursor_col >= self.wrap_len:
            self.cursor_col = max(
                self.cursor_col - self.wrap_len, 0
            )  # move our cursor up *visually* by moving our cursor left
        elif len(sub_lines) > 1 and self.scroll == 0:
            self.cursor_col = 0
        else:
            self.cursor_row = max(self.cursor_row - 1, 0)  # move cursor up
            if self.cursor_row < self.scroll:  # move scroll to make our cursor visible
                self.scroll = self.cursor_row
        if (
            len(sub_lines) > 1
            and original_row + self.cursor_col // self.wrap_len < self.scroll
        ):
            self.scroll = (
                original_row + self.cursor_col // self.wrap_len
            )  # visually move our scroll based on how many sub_lines down we are

    def cursor_down(self):
        """moves the cursor down by one"""
        sub_lines = break_and_wrap_text(self.lines[self.cursor_row], self.wrap_len)
        original_row = self.cursor_row
        if (
            len(sub_lines) > 1
            and self.cursor_col <= len(self.lines[self.cursor_row]) - self.wrap_len
        ):
            self.cursor_col += (
                self.wrap_len
            )  # move our cursor down *visually* by moving our cursor right
        elif len(sub_lines) > 1:
            self.cursor_col = len(self.lines[self.cursor_row])
        else:
            self.cursor_row = min(
                self.cursor_row + 1, len(self.lines) - 1
            )  # move cursor up
            if self.cursor_row > self.scroll:  # move scroll to make our cursor visible
                self.scroll = self.cursor_row
        if (
            len(sub_lines) > 1
            and original_row + self.cursor_col // self.wrap_len
            >= self.scroll + self.height - 1
        ):
            self.scroll += (
                1  # visually move our scroll based on how many sub_lines down we are
            )

    def push_char(self, char: str):
        """Puts a char at the current cursor position"""
        lines = [line + "\n" for line in self.lines]
        if self.cursor_col > visible_len(lines[self.cursor_row]):
            lines[self.cursor_row] += char
        # case: cursor is in the middle of a line
        else:
            lines[self.cursor_row] = (
                # all text upto our cursor
                lines[self.cursor_row][
                    0 : get_visible_index(lines[self.cursor_row], self.cursor_col)
                ]
                + char
                # rest of the text
                + lines[self.cursor_row][
                    get_visible_index(lines[self.cursor_row], self.cursor_col) :
                ]
            )
        self.text = "\n".join(lines)
        self.cursor_right()

    def pad_line(self, text: str) -> str:
        """Mutate self.view to draw the widget. Modified in sub-classes"""
        match self.align:
            case Align.left:
                return text
            case Align.center:
                size = (self.wrap_len - visible_len(text)) // 2
                return " " * size + text + " " * size
            case Align.right:
                size = self.wrap_len - visible_len(text)
                return text + " " * size

    def backspace(self):
        """Does the logic to move the cursor and remove a character at the current cursor position"""
        lines = [line + "\n" for line in self.lines]

        if self.cursor_row == 0 and self.cursor_col == 0:
            return
        # case: at end of line. Just remove last character
        if self.cursor_col > visible_len(lines[self.cursor_row]):
            lines[self.cursor_row] = lines[self.cursor_row][
                0 : get_visible_index(
                    lines[self.cursor_row], len(lines[self.cursor_row]) - 1
                )
            ]
        # case: cursor is in the middle of a line
        else:
            lines[self.cursor_row] = (
                # all text before our cursor
                lines[self.cursor_row][
                    0 : get_visible_index(lines[self.cursor_row], self.cursor_col - 1)
                ]
                # rest of the text
                + lines[self.cursor_row][
                    get_visible_index(lines[self.cursor_row], self.cursor_col) :
                ]
            )
        self.text = "".join(lines)
        self.cursor_left()  # move cursor left by one

    def add_cursor_to_line(self, line: str, col: int) -> str:
        real_col = get_visible_index(line, min(col, visible_len(line)))
        if real_col < len(line):
            return (
                line[:real_col]
                + REVERSE
                + line[real_col]
                + RESET
                + (
                    " "
                    if col == visible_len(line) - 1
                    else line[get_visible_index(line, col + 1) :]
                )
            )
        else:
            return line[:] + REVERSE + " " + RESET

    def prepare_line(self, line: str, current_line: int, line_i: int, sub_line_i: int):
        """Prepares the line by doing edits to it. Can be modified to add line effects
        args:
        - line: the sub_line of text we are modifying
        - current_line: the current drawing-line we are on
        - line_i: the current line of text we are on
        - sub_line_i: the sub-line (accounting for line-wrapping) line we are on."""
        return self.pad_line(line)

    def draw_buffer(self):
        """Mutate self.view to draw the widget. Modified in sub-classes"""

        current_line = -1

        for line_c, line in enumerate(self.lines):
            if current_line >= self.height:
                break
            for sub_c, sub_line in enumerate(break_and_wrap_text(line, self.wrap_len)):
                if current_line >= self.height:
                    break
                if current_line < self.scroll:
                    continue
                current_line += 1
                if line_c == self.cursor_row:
                    translated_cursor = self.cursor_col - sub_c * self.wrap_len
                    if visible_len(sub_line) > translated_cursor >= 0:
                        self.view[current_line] = self.prepare_line(
                            self.add_cursor_to_line(line, translated_cursor),
                            current_line,
                            line_c,
                            sub_c,
                        )
                else:
                    self.view[current_line] = self.prepare_line(
                        line, current_line, line_c, sub_c
                    )


__all__ = ["Editor"]
