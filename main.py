import os
from pytui.events import ResizeEvent
from pytui.layouts import VerticalLayout
from pytui.layouts.align import Align
from pytui.layouts.horizontal import HorizontalLayout
from pytui.utils.definitions import CYAN, RESET
from pytui.widgets import Frame, Label


def main():
    print("Hello from pytui!")

    term_size = os.get_terminal_size()
    resize_event = ResizeEvent(term_size.columns, term_size.lines)

    program = Frame(
        [
            # Frame(
            #     [
            #         Label(f"{CYAN}Test1", Align.center, name="1"),
            #         Label(f"{CYAN}Test2", Align.center, name="2"),
            #         Label(f"{CYAN}Test3", Align.center, name="3"),
            #     ],
            #     HorizontalLayout(),
            #     name="Bar",
            # ),
            Label(f"{CYAN}Test1", Align.center, name="4"),
            # Frame(
            #     [
            #         Label(f"{CYAN}foo", Align.center, name="1"),
            #         Label(f"{CYAN}bar", Align.center, name="2"),
            #         Label(f"{CYAN}baz", Align.center, name="3"),
            #     ],
            #     HorizontalLayout(),
            #     name="Bar",
            # ),
            Label(f"{CYAN}Test2", Align.center, name="6"),
            Label(f"{CYAN}Test3", Align.center, name="6"),
            Frame(
                [
                    Label(f"{CYAN}foo", Align.center, name="1"),
                    Label(f"{CYAN}bar", Align.center, name="2"),
                    Label(f"{CYAN}baz", Align.center, name="3"),
                ],
                HorizontalLayout(),
                name="Bar",
            ),
            Label(f"{CYAN}Test4", Align.center, name="6"),
            Label(f"{CYAN}Test4", Align.center, name="6"),
            Label(f"{CYAN}Test4", Align.center, name="6"),
            Label(f"{CYAN}Test4", Align.center, name="6"),
            Label(f"{CYAN}Test4", Align.center, name="6"),
        ],
        VerticalLayout(),
        name="program",
    )
    program.handle_event(resize_event)

    print(program.children[0].width, program.children[0].height)

    program.draw()
    print(len(program.view.lines), term_size.lines)
    print("-" * term_size.columns)
    print(program.view.to_flat(term_size.lines, term_size.columns - 3))
    print("-" * term_size.columns)
    print(len(program.view.lines))


if __name__ == "__main__":
    main()
