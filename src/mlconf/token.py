from enum import Enum
from typing import Any, List

from mlconf.char import CharStream


class TokenType(Enum):
    WORD = 1
    STRING = 2
    PUNC = 3
    NEWLINE = 4
    WHITESPACE = 5
    EOF = 6


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

    def get_next(self) -> Token:
        while not self.ch.is_eof():
            ch = self.ch.peek()
            if ch == "\n":
                self.ch.next()
                return Token(TokenType.NEWLINE, "", self.ch.row)
            elif ch == " ":
                return self.get_whitespace()
            elif ch in "[]():,\"'-":
                self.ch.next()
                return Token(TokenType.PUNC, ch, self.ch.row)
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
    tokens = strip_newline_or_whitespace_tokens(tokens)
    tokens = filter_nonindent_whitespace_tokens(tokens)
    return tokens


def strip_eof_tokens(tokens: List[Token]) -> List[Token]:
    if tokens[-1].token_type == TokenType.EOF:
        return tokens[:-1]
    return tokens


def strip_newline_or_whitespace_tokens(tokens: List[Token]) -> List[Token]:
    tokens = strip_newline_or_whitespace_front(tokens)
    tokens = strip_newline_or_whitespace_back(tokens)
    return tokens


def strip_newline_or_whitespace_front(tokens: List[Token]) -> List[Token]:
    count = 0
    for token in tokens:
        if token.token_type == TokenType.NEWLINE:
            count += 1
        elif token.token_type == TokenType.WHITESPACE:
            count += 1
        else:
            break
    return tokens[count:]


def strip_newline_or_whitespace_back(tokens: List[Token]) -> List[Token]:
    count = 0
    for token in reversed(tokens):
        if token.token_type == TokenType.NEWLINE:
            count += 1
        elif token.token_type == TokenType.WHITESPACE:
            count += 1
        else:
            break
    return tokens[: len(tokens) - count]


def filter_nonindent_whitespace_tokens(tokens: List[Token]) -> List[Token]:
    invalid_idxs = []
    for i, token in enumerate(tokens):
        if token.token_type == TokenType.WHITESPACE:
            if tokens[i - 1].token_type == TokenType.NEWLINE:
                continue
            else:
                invalid_idxs.append(i)
    return [token for i, token in enumerate(tokens) if i not in invalid_idxs]


class ParseTokenStream:
    def __init__(self, string: str):
        self.tokens = get_tokens(string)
        self.lines = CharStream.get_lines(string)
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
        line_str = self.lines[line]
        raise Exception(f"Error at line {line}: {message}\n{line_str}")


if __name__ == "__main__":
    print(get_tokens("hello world"))
