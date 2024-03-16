import re


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

    def start_of_line(self):
        return self.col == 0

    def croak(self, msg):
        self.line
        self.col
        raise SyntaxError(f"{self.line}:{self.col} {msg}")


class TokenStream:
    def __init__(self, input):
        self.input = input
        self.current = None

    def read_next(self):
        if self.is_start_of_line():
            indent_val = self.read_indent()
            if indent_val > 0:
                return {"type": "indent", "value": indent_val}
        self.read_while(self.is_whitespace)
        if self.input.eof():
            return None
        ch = self.input.peek()
        if ch == "#":
            self.skip_comment()
            return self.read_next()
        elif ch == '"':
            return self.read_string()
        elif self.is_digit(ch):
            return self.read_number()
        elif self.is_punc(ch):
            return {"type": "punc", "value": self.input.next()}
        elif self.is_char(ch):
            return {"type": "name", "value": self.read_while(self.is_char)}
        elif ch == "\n":
            self.input.next()
            return {"type": "newline"}
        else:
            self.input.croak(f"Can't handle character: {ch}")

    def read_indent(self):
        return len(self.read_while(self.is_whitespace))

    def is_start_of_line(self):
        return self.input.start_of_line()

    def read_while(self, predicate):
        str = ""
        while not self.input.eof() and predicate(self.input.peek()):
            str += self.input.next()
        return str

    def is_whitespace(self, ch):
        return re.match(r"[ \t\f\r]", ch)

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

    def croak(self, msg):
        self.input.croak(msg)


class AST:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name}: {self.value}"

    def __repr__(self):
        return f"{self.name}: {self.value}"

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)


class Parser:
    def __init__(self, input):
        self.input = input

    def parse(self):
        ast = {}
        while True:
            token = self.input.read_next()
            if token is None:
                break
            if token["type"] == "name":
                name = token["value"]
                token = self.input.read_next()
                if token is None:
                    self.input.croak("Unexpected end of input")
                if token["type"] != "punc" or token["value"] != ":":
                    self.input.croak("Expected :")
                token = self.input.read_next()
                if token["type"] == "string" or token["type"] == "number":
                    value = token["value"]
                    ast[name] = value
                elif token["type"] == "indent" or token["type"] == "newline":
                    value = self.parse()
                    ast[name] = value
                else:
                    self.input.croak("Unexpected token")
        return AST("root", ast)


def parse(config: str):
    return Parser(config).parse()


if __name__ == "__main__":
    config = """string: "hello_world"
    game:
            value: 1
    """
    inp = parse(TokenStream(InputStream(config)))
    print(inp)
    # while True:
    #     token = inp.read_next()
    #     if token is None:
    #         break
    #     print(token)
