"""String utilities"""


def is_ansi_code(text: str, *, offset=0) -> int:
    """Returns 0 if this text does not start with an ANSI code
    otherwise- returns the length of the ansi code."""
    if len(text) - offset < 3 or text[offset : offset + 2] != "\u001b[":
        return 0
    for i in range(2 + offset, len(text)):
        if (
            (text[i - 1] == ";" and text[i].isalpha())
            or (text[i] == ";" and not text[i - 1].isnumeric())
        ) and not text[i].isalnum():
            return 0
        if text[i].isalpha():
            return i + 1 - offset
    return 0


def remove_ansi_codes(text: str) -> str:
    """Removes ansi codes from text if any are available to be removed."""
    while (i := text.find("\u001b[")) != -1:
        if code := is_ansi_code(text, offset=i):
            text = text[0:i] + text[i + code :]
    return text


def visible_len(text: str) -> int:
    """Get the length of the text- minus the size of invisible ANSI codes"""
    offset = 0
    i = 0
    while (i := text.find("\u001b[", i)) != -1:
        if code := is_ansi_code(text, offset=i):
            offset += code
            i += code
            continue
        i += 1
    return len(text) - offset


def get_visible_index(text: str, idx: int) -> int:
    """Mutates the passed idx by skipping ahead of invisible ANSI codes to give you
    the index into ONLY the visible characters.
    returns `idx` if it couldn't get to the translated index.
    ex:
    get_visible_index(f"hel{RED}lo{RESET}", 4) == 9
    """
    i = 0
    offset = 0
    while i <= idx:
        if code := is_ansi_code(text, offset=offset + i):
            offset += code
            continue
        i += 1
        if i + offset > len(text):
            return idx
    return i + offset - 1


def break_and_wrap_text(text: str, width: int) -> list[str]:
    """Break text by lines and do line wrapping. Does this purely by visible length (skipping ahead of ANSI codes)"""
    lines = text.split("\n")
    output = []
    while len(lines) > 0:
        line = lines.pop(0)
        if visible_len(line) > width:
            output.append(line[0 : get_visible_index(line, width)])
            lines.insert(
                0, line[get_visible_index(line, width) :]
            )  # insert rest of line back into input buffer to be processed
            continue
        output.append(line)
    return output


def normalize_line(text: str, width: int) -> str:
    """truncates the text to a specific *visible* size. Adds ` ` characters where needed"""
    text = text.strip("\n")
    if visible_len(text) <= width:
        return f"{text}{" " * (width-visible_len(text))}"
    text = text[
        : min(get_visible_index(text, width), len(text))
    ]  # cutoff text that's too long
    return f"{text}{" " * (width-visible_len(text))}"
