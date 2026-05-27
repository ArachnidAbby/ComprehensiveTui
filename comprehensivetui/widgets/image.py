import math
from typing import Protocol, SupportsIndex, overload

from comprehensivetui.events.event import Event
from comprehensivetui.layouts.constraints import Constraints
from comprehensivetui.utils.definitions import rgb_to_ansi
from comprehensivetui.widgets.widget import Dirty, Widget

type Color = tuple[int, int, int]


class ArrayLikePixelRow[T: Color](Protocol):
    """A row of pixels that is indexable like an array"""

    @overload
    def __getitem__(self, i: SupportsIndex, /) -> T: ...
    @overload
    def __getitem__(self, s: slice[SupportsIndex | None], /) -> list[T]: ...

    def __len__(self) -> int: ...


class ArrayLikeImage[T: ArrayLikePixelRow](Protocol):
    """A list of pixel rows that is indexable like an array"""

    @overload
    def __getitem__(self, i: SupportsIndex, /) -> T: ...
    @overload
    def __getitem__(self, s: slice[SupportsIndex | None], /) -> list[T]: ...

    def __setitem__(self, s: SupportsIndex, value: T, /): ...

    def __len__(self) -> int: ...


def get_brightness(r: int, g: int, b: int) -> int:
    """Returns a brightness between 0-255"""
    return math.floor((r * 0.299) + (g * 0.587) + (b * 0.114))


class Palates:
    regular = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:\"^'.`"
    blocky = "██▓▓▒▒░░@@##{}++"
    """might not fully work on some systems"""
    blocky_minimal = "██▓▓▒▒░░"
    """Might not work on some systems"""


class Image(Widget):
    __slots__ = "image", "palate"

    image: Dirty[ArrayLikeImage]
    palate: Dirty[str]

    def __init__(
        self,
        image: ArrayLikeImage,
        /,
        palate: str = Palates.regular,
        *,
        name="",
        constraints: Constraints = Constraints(),
    ):
        super().__init__(name=name, constraints=constraints)
        self.image = image
        self.palate = palate

    def handle_event(self, event: Event) -> bool:
        """Handles a given event- returns whether or not the event was handled here"""
        return super().handle_event(event)

    def draw_buffer(self):
        """Mutate self.view to draw the widget. Modified in sub-classes"""

        for row in range(len(self.image)):
            row_data = self.image[row]
            for col in range(len(row_data)):
                pixel = row_data[col]
                raw_brightness = get_brightness(*pixel)
                brightness = (len(self.palate) // 2) - (
                    raw_brightness // (len(self.palate) // 2)
                )
                self.view[
                    row
                ] += f"{rgb_to_ansi(*pixel)}{self.palate[brightness: brightness+2]}"
