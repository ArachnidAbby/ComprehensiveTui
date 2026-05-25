"""Test the strutils module"""

from comprehensivetui.utils.definitions import BRIGHT_RED, CYAN, RED, RESET, YELLOW
from comprehensivetui.utils.strutils import (
    break_and_wrap_text,
    get_visible_index,
    is_ansi_code,
    normalize_line,
    remove_ansi_codes,
    visible_len,
)


def test_is_ansi_code():
    assert is_ansi_code("hello") == 0
    assert is_ansi_code(f"{RED}hello") == len(RED)
    assert f"{RED}hello"[is_ansi_code(f"{RED}hello")] == "h"

    assert is_ansi_code(f"{RED}hello{CYAN}") == len(RED)
    assert is_ansi_code(f"hello{CYAN}") == 0
    assert is_ansi_code(f"{RED}hello{CYAN}", offset=len(RED) + 5) == len(CYAN)
    assert is_ansi_code(f"{RED}hello{CYAN}", offset=len(RED) + 3) == 0
    # Test that it works with ANSI codes with extra params
    assert is_ansi_code(f"{BRIGHT_RED}hello{CYAN}") == len(BRIGHT_RED)

    # test code with no params
    fake_ansi_code = "\u001b[m"
    assert is_ansi_code(f"{fake_ansi_code}hello{CYAN}") == len(fake_ansi_code)

    assert is_ansi_code(f"{BRIGHT_RED}{RED}hello{CYAN}") == len(BRIGHT_RED)


def test_remove_ansi_codes():
    assert remove_ansi_codes("hello") == "hello"
    assert remove_ansi_codes(f"hello{CYAN}") == "hello"
    assert remove_ansi_codes(f"{RED}{YELLOW}hello{CYAN}") == "hello"

    assert remove_ansi_codes(f"{RED}{YELLOW}hello{CYAN}") == "hello"


def test_visible_len():
    assert visible_len("hello") == len("hello")
    assert visible_len(f"hello{CYAN}") == len("hello")
    assert visible_len(f"{RED}{YELLOW}hello{CYAN}") == len("hello")

    assert visible_len(f"{RED}{YELLOW}hello{CYAN}") == len("hello")


def test_get_visible_index():
    assert get_visible_index("hello", 0) == 0
    assert get_visible_index(f"{RED}hello", 0) == len(RED)
    assert get_visible_index(f"{RED}{YELLOW}hello", 0) == len(RED) + len(YELLOW)

    assert get_visible_index(f"{RED}{YELLOW}hello", 1) == len(RED) + len(YELLOW) + 1

    assert get_visible_index(f"{RED}{YELLOW}hello", 4) == len(RED) + len(YELLOW) + 4


def test_break_and_wrap_text():
    wrap_size = 10
    assert break_and_wrap_text("hello", wrap_size) == ["hello"]
    # shouldn't wrap for invisible chars
    assert break_and_wrap_text(f"{RED}{YELLOW}hellohello", wrap_size) == [
        f"{RED}{YELLOW}hellohello"
    ]

    assert break_and_wrap_text(f"{RED}{YELLOW}hellohello\n", wrap_size) == [
        f"{RED}{YELLOW}hellohello",
        "",
    ]

    assert break_and_wrap_text(f"{RED}{YELLOW}hellohelloo\n", wrap_size) == [
        f"{RED}{YELLOW}hellohello",
        "o",
        "",
    ]

    assert break_and_wrap_text(f"{RED}{YELLOW}hellohelloo\n1234567890", wrap_size) == [
        f"{RED}{YELLOW}hellohello",
        "o",
        "1234567890",
    ]

    assert break_and_wrap_text(
        f"{RED}{YELLOW}hellohelloo\n123456789010", wrap_size
    ) == [f"{RED}{YELLOW}hellohello", "o", "1234567890", "10"]

    assert break_and_wrap_text(
        f"{RED}{YELLOW}hellohelloo\n{YELLOW}1234567890{RED}10", wrap_size
    ) == [f"{RED}{YELLOW}hellohello", "o", f"{YELLOW}1234567890{RED}", f"10"]


def test_normalize_line():
    size = 10
    assert normalize_line("hello", size) == "hello     "
    assert normalize_line(f"{RED}hello", size) == f"{RED}hello     "
    assert normalize_line(f"{RED}hello{RESET}", size) == f"{RED}hello{RESET}     "
    assert (
        normalize_line(f"{RED}hel{CYAN}lohello{RESET}", size)
        == f"{RED}hel{CYAN}lohello{RESET}"
    )
    assert (
        normalize_line(f"{RED}hel{CYAN}lohello TOO LONG HERE{RESET}", size)
        == f"{RED}hel{CYAN}lohello"
    )
