from enum import Enum
from typing import Any, List

from mlconf.char import CharStream


class TokenType(Enum):
    WORD = 1
    STRING = 2
    PUNC = 3
    NEWLINE = 4
    WHITESPACE = 5
    WHITESPACE_INDENT = 6
    INDENT = 7
    DEDENT = 8
    EOF = 9


class Token:
    def __init__(self, token_type: TokenType, value: str, line: int = -1) -> None:
        self.token_type = token_type
        self.value = value
        self.line = line

    def __str__(self) -> str:
        return f"Token({self.token_type}, {self.value})"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Token):
            return False
        return self.token_type == other.token_type and self.value == other.value


class TokenStream:
    def __init__(self, charstream: CharStream):
        self.ch = charstream
        self.indentation_handled = False

    def get_next(self) -> Token:
        while not self.ch.is_eof():
            ch = self.ch.peek()
            if self.ch.col == 0 and not self.indentation_handled:
                self.indentation_handled = True
                return self.get_indent()
            elif ch == "\n":
                self.indentation_handled = False
                self.ch.next()
                return Token(TokenType.NEWLINE, "NEWLINE", self.ch.row)
            elif ch == " ":
                self.ch.next()
                continue
            elif ch in "[]():,-":
                self.ch.next()
                return Token(TokenType.PUNC, ch, self.ch.row)
            elif ch == "#":
                while not self.ch.is_eof() and self.ch.peek() != "\n":
                    self.ch.next()
                continue
            elif ch == '"' or ch == "'":
                string_token = self.get_string(delimiter=ch)
                self.ch.next()
                return string_token
            elif (
                ch
                in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*_+=<>?/\\|;."
            ):
                return self.get_word()
            else:
                self.ch.croak("Unknown character")
        return Token(TokenType.EOF, "", self.ch.row + 1)

    def get_word(self) -> Token:
        word = ""
        while not self.ch.is_eof():
            ch = self.ch.peek()
            if (
                ch
                in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*_+=<>?/\\|;."
            ):
                word += ch
                self.ch.next()
            else:
                break
        return Token(TokenType.WORD, word, self.ch.row)

    def get_string(self, delimiter: str) -> Token:
        string = ""
        delimited = False
        while not self.ch.is_eof():
            ch = self.ch.next()
            if ch == delimiter:
                delimited = True
                break
            string += ch
        if not delimited:
            self.ch.croak("Unterminated string")
        return Token(TokenType.STRING, string, self.ch.row)

    def get_whitespace(self) -> Token:
        whitespace = ""
        while not self.ch.is_eof():
            ch = self.ch.peek()
            if ch == " ":
                whitespace += ch
                self.ch.next()
            else:
                break
        return Token(TokenType.WHITESPACE, str(len(whitespace)), self.ch.row)

    def get_indent(self) -> Token:
        indent = ""
        while not self.ch.is_eof():
            ch = self.ch.peek()
            if ch == " ":
                indent += ch
                self.ch.next()
            else:
                break
        return Token(TokenType.WHITESPACE_INDENT, str(len(indent)), self.ch.row)


def get_raw_tokens(string: str) -> List[Token]:
    charstream = CharStream(string)
    tokenstream = TokenStream(charstream)
    tokens = []
    while not charstream.is_eof():
        tokens.append(tokenstream.get_next())
    return tokens


def get_tokens(string: str) -> List[Token]:
    tokens = get_raw_tokens(string)
    tokens = strip_eof_tokens(tokens)
    tokens = replace_whitespace_with_indent_dedent_tokens(tokens)
    tokens = strip_indent_tokens(tokens)
    return tokens


def strip_eof_tokens(tokens: List[Token]) -> List[Token]:
    if tokens[-1].token_type == TokenType.EOF:
        return tokens[:-1]
    return tokens


def strip_indent_dedent_tokens(tokens: List[Token]) -> List[Token]:
    if tokens[-1].token_type == TokenType.DEDENT:
        tokens = tokens[:-1]
    if tokens[0].token_type == TokenType.INDENT:
        tokens = tokens[1:]
    return tokens


def strip_newline_or_indent_tokens(tokens: List[Token]) -> List[Token]:
    tokens = strip_indent_tokens(tokens)
    return tokens


def strip_newline_tokens(tokens: List[Token]) -> List[Token]:
    res_tokens: List[Token] = []
    encountered_word = False
    for token in tokens:
        if token.token_type == TokenType.NEWLINE and not encountered_word:
            continue
        if token.token_type == TokenType.WORD or token.token_type == TokenType.PUNC:
            encountered_word = True
        res_tokens.append(token)
    encountered_word = False
    for token in reversed(res_tokens):
        if token.token_type == TokenType.NEWLINE:
            res_tokens.remove(token)
        if token.token_type == TokenType.WORD or token.token_type == TokenType.PUNC:
            encountered_word = True
            break
    return res_tokens


def strip_indent_tokens(tokens: List[Token]) -> List[Token]:
    res_tokens: List[Token] = []
    encountered_word = False
    count = 0
    for token in tokens:
        if token.token_type == TokenType.INDENT and not encountered_word:
            count += 1
            continue
        elif token.token_type == TokenType.WORD or token.token_type == TokenType.PUNC:
            encountered_word = True
        res_tokens.append(token)
    return res_tokens


def filter_nonindent_whitespace_tokens(tokens: List[Token]) -> List[Token]:
    invalid_idxs = []
    for i, token in enumerate(tokens):
        if token.token_type == TokenType.WHITESPACE:
            if tokens[i - 1].token_type == TokenType.NEWLINE:
                continue
            else:
                invalid_idxs.append(i)
    return [token for i, token in enumerate(tokens) if i not in invalid_idxs]


def replace_whitespace_with_indent_dedent_tokens(tokens: List[Token]) -> List[Token]:
    white_space_tokens: List[Token] = []
    white_space_tokens.append(Token(TokenType.WHITESPACE_INDENT, "0"))
    res_tokens: List[Token] = []
    for i, token in enumerate(tokens):
        if token.token_type == TokenType.WHITESPACE_INDENT:
            top_token = white_space_tokens[-1]
            if int(token.value) > int(top_token.value):
                res_tokens.append(Token(TokenType.INDENT, "", token.line))
                white_space_tokens.append(token)
            elif int(token.value) == int(top_token.value):
                continue
            else:
                while True:
                    if int(token.value) == int(top_token.value):
                        break
                    if int(token.value) > int(top_token.value):
                        raise IndentationError(
                            f"Error at line {token.line}: IndentationError, Indent does not match any outer indentation level"
                        )
                    res_tokens.append(Token(TokenType.DEDENT, "", token.line))
                    white_space_tokens.pop()
                    top_token = white_space_tokens[-1]
        else:
            res_tokens.append(token)
    while len(white_space_tokens) > 1:
        white_space_tokens.pop()
        res_tokens.append(Token(TokenType.DEDENT, "", tokens[-1].line))
    return res_tokens


class ParseTokenStream:
    def __init__(self, string: str):
        self.lines = CharStream.get_lines(string)
        self.tokens = get_tokens(string)
        self.idx = 0

    def peek(self) -> Token:
        if self.is_eof():
            return Token(TokenType.EOF, "")
        return self.tokens[self.idx]

    def next(self) -> None:
        self.idx += 1

    def peek_next(self) -> Token:
        assert not self.is_eof()
        if self.idx + 1 >= len(self.tokens):
            return Token(TokenType.EOF, "")
        return self.tokens[self.idx + 1]

    def is_eof(self) -> bool:
        return self.idx >= len(self.tokens)

    def croak(self, message: str) -> None:
        line = self.tokens[self.idx].line
        raise Exception(f"Error at line {line}: {message}\n{self.lines[line]}")
