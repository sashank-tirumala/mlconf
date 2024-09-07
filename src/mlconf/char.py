from typing import List


class CharStream:
    def __init__(self, string: str) -> None:
        self.lines = CharStream.get_lines(string)
        self.row = 0
        self.col = 0

    @staticmethod
    def get_lines(string: str) -> List[str]:
        lines = string.split("\n")
        for i, line in enumerate(lines):
            lines[i] = line + "\n"
        lines[-1] = lines[-1].rstrip("\n")
        lines[-1] += "\0"
        return lines

    def peek(self) -> str:
        assert self.row < len(self.lines)
        assert self.col < len(self.lines[self.row])
        return self.lines[self.row][self.col]

    def next(self) -> str:
        if (
            self.col == len(self.lines[self.row]) - 1
            and self.row == len(self.lines) - 1
        ):
            return self.peek()
        self.col += 1
        if self.col < len(self.lines[self.row]):
            return self.peek()
        self.row += 1
        self.col = 0
        return self.peek()

    def is_eof(self) -> bool:
        return self.peek() == "\0"

    def croak(self, message: str) -> None:
        raise Exception(
            f"Error: {self.row},{self.col} - {self.lines[self.row]}: {message}"
        )
