import os
import time
from comprehensivetui.events import ResizeEvent
from comprehensivetui.events.event import Event
from comprehensivetui.layouts import VerticalLayout
from comprehensivetui.layouts.constraints import Align, Constraints
from comprehensivetui.layouts.horizontal import HorizontalLayout
from comprehensivetui.utils.definitions import CYAN, RESET
from comprehensivetui.widgets import Frame, Label
from comprehensivetui.widgets.border import Border
from comprehensivetui.widgets.program import Program
from comprehensivetui.widgets.textboard import TextBoard


class ExampleProgram(Program):
    __slots__ = ("label", "last_timer", "highest")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        board = TextBoard(Align.center)
        board.lines = [str(i) for i in range(35)]
        self.label = Label(f"{CYAN}Test1\nTest4", Align.center, name="1")
        self.last_timer = time.perf_counter()
        self.highest = 0

        self.set_children(
            [
                Frame(
                    [
                        self.label,
                        Label(f"{CYAN}Test2", Align.center, name="2"),
                        Label(f"{CYAN}Test3", Align.center, name="3"),
                    ],
                    HorizontalLayout(),
                    name="Bar",
                ),
                Label(f"{CYAN}Test1", Align.center, name="4"),
                Frame(
                    [
                        Label(f"{CYAN}foo", Align.center, name="1"),
                        Label(f"{CYAN}bar", Align.center, name="2"),
                        Label(f"{CYAN}baz", Align.center, name="3"),
                    ],
                    HorizontalLayout(),
                    name="Bar",
                ),
                Label(f"{CYAN}Test2", Align.center, name="6"),
                board,
            ]
        )

        self.set_layout(VerticalLayout())

    def on_frame(self):
        t = time.perf_counter()
        dif = t - self.last_timer
        if dif > self.highest:
            self.label.text = f"perf: {self.highest:f}"
            self.highest = dif
        self.last_timer = t


def main():
    print("Hello from comprehensivetui!")

    # program = ExampleProgram(rate=60, title="Example Title")
    # program.start()

    program = Border(
        Frame(
            [
                Border(
                    Label(
                        f"{CYAN}foo",
                        Align.right,
                        name="1",
                        constraints=Constraints(min_height=8, max_width=20),
                    ),
                    name="fungus",
                ),
                Label(f"{CYAN}bar", Align.right, name="2"),
                Label(f"{CYAN}baz", Align.center, name="3"),
            ],
            VerticalLayout(),
            name="Bar",
        ),
    )
    program.set_layout(VerticalLayout())

    term_size = os.get_terminal_size()
    resize_event = ResizeEvent(term_size.columns, term_size.lines)
    program.handle_event(resize_event)

    print(program.width, program.height)
    print(program.children[0].width, program.children[0].height)
    program.draw()
    # print(len(program.view.lines), term_size.lines)
    # print("-" * term_size.columns)
    print(program.view.to_flat(program.height, program.width))
    # print("-" * term_size.columns)
    # print(len(program.view.lines))


if __name__ == "__main__":
    main()
