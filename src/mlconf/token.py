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
    def __init__(self, token_type: TokenType, value: str) -> None:
        self.token_type = token_type
        self.value = value

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
                return Token(TokenType.NEWLINE, "")
            elif ch == " ":
                return self.get_whitespace()
            elif ch in "[]():,\"'-":
                self.ch.next()
                return Token(TokenType.PUNC, ch)
            elif (
                ch
                in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*_+=<>?/\\|;."
            ):
                return self.get_word()
            else:
                self.ch.croak("Unknown character")
        return Token(TokenType.EOF, "")

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
        return Token(TokenType.WORD, word)

    def get_whitespace(self) -> Token:
        whitespace = ""
        while not self.ch.is_eof():
            ch = self.ch.peek()
            if ch == " ":
                whitespace += ch
                self.ch.next()
            else:
                break
        return Token(TokenType.WHITESPACE, str(len(whitespace)))


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


if __name__ == "__main__":
    print(get_tokens("hello world"))
