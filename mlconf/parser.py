import re


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


class TokenStream:
    def __init__(self, input: InputStream):
        assert type(input) == InputStream, "Input must be an InputStream"
        self.input = input
        self.indents = [0]
        self.current = None
        self.is_last_token = False

    def read_next(self):
        if self.is_last_token:
            return None
        if self.is_start_of_line():
            indent = self.read_indent()
            if indent is not None:
                return indent
        self.read_while(self.is_whitespace)
        if self.input.eof():
            self.is_last_token = True
            if self.indents[-1] > 0:
                while self.indents[-1] > 0:
                    self.indents.pop()
                return {"type": "dedent", "value": 0}
            else:
                return None
        ch = self.input.peek()
        if ch == "#":
            self.skip_comment()
            return self.read_next()
        elif ch == '"' or ch == "'":
            return self.read_string(ch)
        elif self.is_digit(ch):
            return self.read_number()
        elif self.is_punc(ch):
            return {"type": "punc", "value": self.input.next()}
        elif self.is_char(ch):
            return self.read_keyword()
        elif ch == "\n":
            self.input.next()
            return {"type": "newline", "value": "\n"}
        else:
            self.input.croak(f"Can't handle character: {ch}")

    def read_indent(self):
        indent_count = len(self.read_while(self.is_whitespace))
        if indent_count == self.indents[-1]:
            return None
        if indent_count > self.indents[-1]:
            if self.input.peek() == "\n" or self.input.eof() or self.input.peek() == "#":
                return None
            self.indents.append(indent_count)
            return {"type": "indent", "value": indent_count}
        if indent_count < self.indents[-1]:
            while indent_count < self.indents[-1]:
                self.indents.pop()
            if indent_count != self.indents[-1]:
                self.input.croak(f"Invalid indentation: {indent_count}")
            return {"type": "dedent", "value": indent_count}

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

    def read_string(self, end='"'):
        return {"type": "string", "value": self.read_escaped(end)}

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
        return re.match(r"\d|\.|\-|\+", ch)

    def read_number(self):
        str = self.read_while(lambda ch: self.is_digit(ch) or re.match(r"e|E", ch))
        try:
            return {"type": "number", "value": float(str)}
        except ValueError:
            self.croak(f"Invalid number: {str}")

    def is_punc(self, ch):
        return re.match(r"[:]", ch)

    def is_char(self, ch):
        return re.match(r"[a-z|A-Z|_|0-9]", ch)

    def is_null(self, ch):
        return re.match(r"null", ch)

    def read_keyword(self):
        str = self.read_while(lambda ch: self.is_char(ch))
        if str == "true" or str == "True":
            return {"type": "bool", "value": True}
        elif str == "false" or str == "False":
            return {"type": "bool", "value": False}
        elif str == "null" or str == "None":
            return {"type": "null", "value": None}
        else:
            return {"type": "name", "value": str}

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


def parse_config(token_stream, indent_count=0):
    """
    This parses an entire configuration file
    """
    ast = {}
    while True:
        token = token_stream.read_next()
        if token is None:
            break
        elif token["type"] == "name":
            name = token["value"]
            token = token_stream.read_next()
            if token["type"] == "punc":
                if token["value"] == ":":
                    ast[name] = parse_value(token_stream)
                else:
                    token_stream.croak(f"Expected a colon, got: {token}")
        elif token["type"] == "newline" or token["type"] == "indent":
            continue
        elif token["type"] == "dedent":
            print("hi", ast)
            if token["value"] <= indent_count:
                return ast
            else:
                token = token_stream.read_next()
                ast[token["value"]] = parse_value(token_stream)
        else:
            token_stream.croak(f"Unexpected token, probably a number or a string with no name: {token}")
    return ast


def parse_value(token_stream):
    """
    This parses an expression
    """
    while True:
        token = token_stream.read_next()
        if token is None:
            token_stream.croak("Unexpected end of file")
        elif (
            token["type"] == "name"
            or token["type"] == "string"
            or token["type"] == "number"
            or token["type"] == "bool"
            or token["type"] == "null"
        ):
            value = token["value"]
            next_token = token_stream.read_next()
            if next_token is None or next_token["type"] == "newline" or next_token == {"type": "dedent", "value": 0}:
                return value
            else:
                token_stream.croak(f"Expected a newline, got: {next_token}")
        elif token["type"] == "indent":
            indent_count = token["value"]
            return parse_config(token_stream, indent_count)
        elif token["type"] == "newline":
            continue
        else:
            token_stream.croak(f"Unexpected token: {token}")


def parse_indent(token_stream, indent_count):
    ast = {}
    while True:
        token = token_stream.read_next()
        if token["type"] == "dedent":
            if token["value"] < indent_count:
                return ast
        else:
            ast[token["value"]] = parse_config(token_stream)


def parse(input):
    return parse_config(TokenStream(InputStream(input)))


def get_tokens(input):
    tokenstream = TokenStream(InputStream(input))
    tokens = []
    while True:
        token = tokenstream.read_next()
        if token is None:
            break
        tokens.append(token)
    return tokens


if __name__ == "__main__":
    config = "string:test\n"
    config += "string2: \n"
    config += "  test:1\n"
    config += "  string3: 'test:12'\n"
    config += "number: 1.0"
    # print(get_tokens(config))
    print(parse(config))
