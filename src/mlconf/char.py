from typing import List


class CharStream:
    def __init__(self, string: str) -> None:
        self.lines = CharStream.get_lines(string)
        self.row = 0
        self.col = 0

    @staticmethod
    def get_lines(string: str) -> List[str]:
        lines = string.split("\n")
        final_lines = []
        for i, line in enumerate(lines):
            is_empty = True
            final_char = ""
            for char in line:
                if char != " ":
                    is_empty = False
                    final_char = char
                    break
            if final_char == "#":
                continue
            if not is_empty:
                final_lines.append(line + "\n")
        final_lines[-1] = final_lines[-1].rstrip("\n")
        final_lines[-1] += "\0"
        return final_lines

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
