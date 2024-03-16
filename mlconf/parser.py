class Parser:
    def __init__(self, config: str):
        self.config = config

    def parse(self):
        return None


class InputStream:
    def __init__(self, input):
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
        self.pos
        return self.input[self.pos]

    def eof(self):
        self.pos
        return self.pos >= len(self.input)

    def croak(self, msg):
        self.line
        self.col
        raise Exception(f"{msg} ({self.line}:{self.col})")


def parse(config: str):
    return Parser(config).parse()


if __name__ == "__main__":
    config = """
    string: test
    string2: "test"
    string3: 'test:123'
    string4: "test"
    """
    inp = InputStream(config)
    while not inp.eof():
        print(inp.next(), end="")
