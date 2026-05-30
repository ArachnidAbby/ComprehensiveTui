import os
import time
from comprehensivetui.events import ResizeEvent
from comprehensivetui.events.event import Event, KeySentEvent
from comprehensivetui.layouts import VerticalLayout
from comprehensivetui.layouts.constraints import Align, Constraints
from comprehensivetui.layouts.horizontal import HorizontalLayout
from comprehensivetui.utils.definitions import CYAN, RESET
from comprehensivetui.utils.definitions import (
    BACKSPACE,
    ENTER,
    LEFT_ARROW,
    RIGHT_ARROW,
    UP_ARROW,
    DOWN_ARROW,
    arrow_pressed,
)
from comprehensivetui.widgets import Frame, Label
from comprehensivetui.widgets.border import Border
from comprehensivetui.widgets.editor import Editor
from comprehensivetui.widgets.image import ArrayLikeImage, Image, Palates
from comprehensivetui.widgets.program import Program
from comprehensivetui.widgets.textboard import TextBoard


class CustomEditor(Editor):
    __slots__ = ("debug",)

    def __init__(self, debug: Label, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.debug = debug

    @property
    def wrap_len(self) -> int:
        return super().wrap_len - 3

    def prepare_line(self, line: str, current_line: int, line_i: int, sub_line_i: int):
        """Prepares the line by doing edits to it. Can be modified to add line effects
        args:
        - line: the sub_line of text we are modifying
        - current_line: the current drawing-line we are on
        - line_i: the current line of text we are on
        - sub_line_i: the sub-line (accounting for line-wrapping) line we are on."""
        if sub_line_i == 0:
            return f"{line_i}) " + self.pad_line(line)
        else:
            return f"{" "*(len(str(line_i))-1)}.) " + self.pad_line(line)

    def handle_event(self, event: Event) -> bool:
        if super().handle_event(event):
            return True

        match event:
            case KeySentEvent(codes):
                if len(codes) == 1:
                    if codes[0] not in (BACKSPACE, ENTER):
                        self.push_char(chr(codes[0]))
                    elif (
                        codes[0] == ENTER
                    ):  # enter might be \r (like in windows. so we need to manually do this)
                        self.push_char("\n")
                    else:
                        self.backspace()
                elif arrow_pressed(codes):
                    if codes[-1] == LEFT_ARROW:
                        self.cursor_left()
                    if codes[-1] == RIGHT_ARROW:
                        self.cursor_right()
                    if codes[-1] == UP_ARROW:
                        self.cursor_up()
                    if codes[-1] == DOWN_ARROW:
                        self.cursor_down()
                self.debug.text = (
                    chr(codes[0])
                    if codes[0] != ENTER
                    else "\\n" + f" {self.cursor_row} {self.cursor_col} {self.scroll}"
                )
                # self.debug._dirty = True
                return True
        return False


class ExampleProgram(Program):
    __slots__ = ("label", "last_timer", "highest")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        board = TextBoard(Align.center)
        board.lines = [str(i) for i in range(35)]
        self.label = Label(f"{CYAN}Test1\nTest4", Align.center, name="1")
        self.last_timer = time.perf_counter()
        self.highest = 0
        image_data = [[(y * 20, 255, x * 10) for x in range(10)] for y in range(10)]

        editor = CustomEditor(self.label)
        editor.text = "bozo"

        self.set_children(
            [
                Border(
                    Frame(
                        [
                            self.label,
                            Border(
                                editor,
                            ),
                            Image(image_data, Palates.regular),
                            Label(f"{CYAN}bar", Align.right, name="2"),
                            Label(f"{CYAN}baz", Align.center, name="3"),
                        ],
                        VerticalLayout(),
                        name="Bar",
                    ),
                )
            ]
        )

        self.set_layout(VerticalLayout())

    def on_frame(self):
        t = time.perf_counter()
        self.label.text = f"{t}"
        dif = t - self.last_timer
        if dif > self.highest:
            self.label.text = f"perf: {self.highest:f}"
            self.highest = dif
        self.last_timer = t


def main():
    print("Hello from comprehensivetui!")

    program = ExampleProgram(rate=60, title="Example Title")
    program.start()

    # program = Border(
    #     Frame(
    #         [
    #             Border(
    #                 Label(
    #                     f"{CYAN}foo",
    #                     Align.right,
    #                     name="1",
    #                     constraints=Constraints(min_height=8, max_width=20),
    #                 ),
    #                 name="fungus",
    #             ),
    #             Label(f"{CYAN}bar", Align.right, name="2"),
    #             Label(f"{CYAN}baz", Align.center, name="3"),
    #         ],
    #         VerticalLayout(),
    #         name="Bar",
    #     ),
    # )
    # program.set_layout(VerticalLayout())

    # term_size = os.get_terminal_size()
    # resize_event = ResizeEvent(term_size.columns, term_size.lines)
    # program.dispatch_event(resize_event)

    # print(program.width, program.height)
    # print(program.children[0].width, program.children[0].height)
    # program.draw()
    # # print(len(program.view.lines), term_size.lines)
    # # print("-" * term_size.columns)
    # print(program.view.to_flat(program.height, program.width))
    # print("-" * term_size.columns)
    # print(len(program.view.lines))


if __name__ == "__main__":
    main()
