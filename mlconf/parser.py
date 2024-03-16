import re


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


class TokenStream:
    def __init__(self, input):
        self.input = input
        self.current = None

    def read_next(self):
        self.read_while(self.is_whitespace)
        if self.input.eof():
            return None
        ch = self.input.peek()
        if ch == "#":
            self.skip_comment()
            return self.read_next()
        if ch == '"':
            return self.read_string()
        if self.is_digit(ch):
            return self.read_number()
        if self.is_punc(ch):
            return {"type": "punc", "value": self.input.next()}
        if self.is_char(ch):
            return {"type": "name", "value": self.read_while(self.is_char)}
        self.input.croak(f"Can't handle character: {ch}")

    def read_while(self, predicate):
        str = ""
        while not self.input.eof() and predicate(self.input.peek()):
            str += self.input.next()
        return str

    def is_whitespace(self, ch):
        return re.match(r"\s", ch)

    def skip_comment(self):
        self.read_while(lambda ch: ch != "\n")
        self.input.next()

    def read_string(self):
        return {"type": "string", "value": self.read_escaped('"')}

    def read_escaped(self, end):
        escaped = False
        str = ""
        self.input.next()
        while not self.input.eof():
            ch = self.input.next()
            if escaped:
                str += ch
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == end:
                break
            else:
                str += ch
        return str

    def is_digit(self, ch):
        return re.match(r"\d|\.|-", ch)

    def read_number(self):
        str = self.read_while(lambda ch: re.match(r"\d|\.|e|-", ch))
        return {"type": "number", "value": float(str)}

    def is_punc(self, ch):
        return re.match(r"[:]", ch)

    def is_char(self, ch):
        return re.match(r"[a-zA-Z_]", ch)


def parse(config: str):
    return Parser(config).parse()


if __name__ == "__main__":
    config = """
    string: "hello_world\n \\" boy \\" hello"
    val : -1.2
    """
    inp = TokenStream(InputStream(config))
    while not inp.input.eof():
        print(inp.read_next())
