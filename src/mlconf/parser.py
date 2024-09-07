from typing import Any, Dict

from mlconf.config import Config
from mlconf.tokenizer import ParseTokenStream, TokenType


def parse_block(
    token_stream: ParseTokenStream, till_dedent: bool = False
) -> Dict[str, Any]:
    ast: Dict[str, Any] = {}
    while not token_stream.is_eof():
        token = token_stream.peek()
        if token.token_type == TokenType.WORD:
            key = token.value
            token_stream.next()
            token = token_stream.peek()
            if token.token_type == TokenType.PUNC and token.value == ":":
                token_stream.next()
                token = token_stream.peek()
                if token.token_type == TokenType.WORD:
                    value = token.value
                    ast[key] = value
                    token_stream.next()
                elif token.token_type == TokenType.NEWLINE:
                    token_stream.next()
                    token = token_stream.peek()
                    if token.token_type == TokenType.INDENT:
                        token_stream.next()
                        ast[key] = parse_block(token_stream, till_dedent=True)
                else:
                    token_stream.croak(f"Expected WORD token, but got {token}")
            else:
                token_stream.croak(f"Expected PUNC token, but got {token}")
        elif token.token_type == TokenType.NEWLINE:
            token_stream.next()
        elif token.token_type == TokenType.INDENT:
            token_stream.croak("Unexpected Indent")
        elif token.token_type == TokenType.DEDENT:
            if till_dedent:
                token_stream.next()
                break
            token_stream.croak("Unexpected Dedent")
        elif token.token_type == TokenType.EOF:
            break
        else:
            token_stream.croak(
                f"Expected WORD or NEWLINE token, but got {token.token_type}"
            )
    return ast


def parse(string: str) -> Config:
    parse_token_stream = ParseTokenStream(string)
    ast = parse_block(parse_token_stream, till_dedent=False)
    return Config(ast)
