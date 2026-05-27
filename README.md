# ComprehensiveTui

This package is meant for people who hate using curses and curses-like libraries. It is widget based and similar to QT in the layout system.

This means no playing around with how individual lines draw or making sure everything sizes perfectly.
This library will attempt to handle it for you. Where it can't- functionality can be easily added by you for your particular needs.

# Demo

![Window Resizing and components respond instantly](docs/static/resizing_demo.gif)

# Example (blocking render loop)

```python
from comprehensivetui.widgets import Program, TextBoard, Frame, Label
from comprehensivetui.events import ResizeEvent
from comprehensivetui.layouts import HorizontalLayout, VerticalLayout

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
                        Label(f"{CYAN}Test1", Align.center, name="1"),
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

program = ExampleProgram(rate=60, title="Example Title")
program.start()
```

# Example (draw single widget)

```python
from comprehensivetui.widgets import Frame, Label
from comprehensivetui.events import ResizeEvent
from comprehensivetui.layouts import HorizontalLayout

import os


widget = Frame(
    [
        Label(f"{CYAN}Test1", Align.center, name="1"),
        Label(f"{CYAN}Test2", Align.center, name="2"),
        Label(f"{CYAN}Test3", Align.center, name="3"),
    ],
    HorizontalLayout(),
    name="container frame"
)

term_size = os.get_terminal_size()
resize_event = ResizeEvent(term_size.columns, term_size.lines)

frame.dispatch_event(resize_event) # tell our frame to resize

print(widget.view.to_flat(term_size.lines, term_size.columns))

```

# What is `Dirty[T]`?????

The definition of `Dirty[T]` is this:

```python
type Dirty[T] = T
```

you may think to yourself, "this does nothing?!".
You are correct (kind of)!

## How is this useful

When a widget is created- it will look at all of the dirty properties and create accessors for them.
This means that when you set an attribute marked "dirty", it will automatically set your widget as "dirty".
A dirty widget is one who must be redrawn.

A widget will set itself as "clean" (`.dirty == False`) after a redraw has occured.

# I called draw and nothing happened :(

Calling `.draw()` does NOT draw the widget to the screen. Instead it draws it to it's internal `.view` object.
To get a print-able representation do `.view.to_flat(rows, columns)`. This will crop the view to the given size and concatinate the lines.
This makes it perfect for printing :)
