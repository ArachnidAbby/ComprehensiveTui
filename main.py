import os
from comprehensivetui.events import ResizeEvent
from comprehensivetui.layouts import VerticalLayout
from comprehensivetui.layouts.align import Align
from comprehensivetui.layouts.horizontal import HorizontalLayout
from comprehensivetui.utils.definitions import CYAN, RESET
from comprehensivetui.widgets import Frame, Label
from comprehensivetui.widgets.program import Program
from comprehensivetui.widgets.textboard import TextBoard


class ExampleProgram(Program):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        board = TextBoard(Align.center)
        board.lines = [str(i) for i in range(35)]

        self.set_children(
            [
                Frame(
                    [
                        Label(f"{CYAN}Test1\nTest4", Align.center, name="1"),
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


def main():
    print("Hello from comprehensivetui!")

    # term_size = os.get_terminal_size()
    # resize_event = ResizeEvent(term_size.columns, term_size.lines)

    program = ExampleProgram(rate=60, title="Example Title")
    program.start()
    # print(program.children[0].width, program.children[0].height)
    # program.draw()
    # print(len(program.view.lines), term_size.lines)
    # print("-" * term_size.columns)
    # print(program.view.to_flat(term_size.lines, term_size.columns - 3))
    # print("-" * term_size.columns)
    # print(len(program.view.lines))


if __name__ == "__main__":
    main()
