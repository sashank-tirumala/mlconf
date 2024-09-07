from typing import List


class CharIdx:
    def __init__(self, value: str, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.value = value

    def __repr__(self) -> str:
        return f"CharIdx({self.row}, {self.col}, {self.value})"

    def __str__(self) -> str:
        return f"CharIdx({self.row}, {self.col}, {self.value})"


def get_lines(string: str) -> List[str]:
    lines = string.split("\n")
    for i, line in enumerate(lines):
        lines[i] = line + "\n"
    lines[-1] = lines[-1].rstrip("\n")
    return lines


def peek(lines: List[str], row: int, col: int) -> CharIdx:
    assert row < len(lines)
    assert col < len(lines[row])
    return CharIdx(lines[row][col], row, col)


def peek_next_value(lines: List[str], row: int, col: int) -> str:
    next_char = next(lines, row, col)
    return next_char.value


def next(lines: List[str], row: int, col: int) -> CharIdx:
    if col + 1 < len(lines[row]):
        return CharIdx(lines[row][col + 1], row, col + 1)
    elif row + 1 < len(lines):
        return CharIdx(lines[row + 1][0], row + 1, 0)
    else:
        return CharIdx("\0", row, col)
