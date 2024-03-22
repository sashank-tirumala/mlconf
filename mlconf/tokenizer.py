import os
import re
from enum import Enum, auto

from mlconf.input_stream import InputStream


class PARSER_STATES(Enum):
    DEDENT = auto()


class TokenStream:
    def __init__(self, input: InputStream):
        assert type(input) == InputStream, "Input must be an InputStream"
        self.input = input
        self.indents = [0]
        self.current = None
        self.is_last_token = False
        self.dedents = []

    def read_next(self):
        if self.dedents:
            return self.dedents.pop(0)
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
                indent_count = 0
                while indent_count < self.indents[-1]:
                    return {"type": "dedent", "value": self.indents.pop()}
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
                self.dedents.append({"type": "dedent", "value": self.indents.pop()})
            if indent_count != self.indents[-1]:
                self.input.croak(f"Invalid indentation: {indent_count}")
            return self.dedents.pop(0)

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
        return ch in "{},:[]$"

    def is_char(self, ch):
        return re.match(r"[a-z|A-Z|_|0-9|/]", ch)

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


def get_tokens(input):
    tokenstream = TokenStream(InputStream(input))
    tokens = []
    while True:
        token = tokenstream.read_next()
        if token is None:
            break
        tokens.append(token)
    return tokens
