class InputStream:
    def __init__(self, input: str):
        assert type(input) == str, "Input must be a string"
        self.input = input
        self.pos = 0
        self.line = 1
        self.col = 0

    def next(self):
        ch = self.input[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 0
        else:
            self.col += 1
        return ch

    def peek(self):
        return self.input[self.pos]

    def eof(self):
        return self.pos >= len(self.input)

    def start_of_line(self):
        return self.col == 0

    def croak(self, msg):
        raise SyntaxError(f"{self.line}:{self.col} {msg}")
