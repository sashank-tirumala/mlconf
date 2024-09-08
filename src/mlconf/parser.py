from typing import Any, Dict, List, Tuple

from mlconf.config import Config
from mlconf.resolver import PythonDataTypeResolver, resolve
from mlconf.tokenizer import ParseTokenStream, Token, TokenType

INLINE_LIST_DELIMITER = Token(TokenType.PUNC, "]")
INLINE_LIST_SEPARATOR = Token(TokenType.PUNC, ",")


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
                if (
                    token.token_type == TokenType.WORD
                    or token.token_type == TokenType.PUNC
                    or token.token_type == TokenType.STRING
                ):
                    ast[key] = parse_inline_expression(token_stream)
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
            token_stream.next()
        elif token.token_type == TokenType.EOF:
            break
        else:
            token_stream.croak(
                f"Expected WORD or NEWLINE token, but got {token.token_type}"
            )
    return ast


def parse_inline_expression(token_stream: ParseTokenStream) -> Any:
    res = ""
    while not token_stream.is_eof():
        token = token_stream.peek()
        if token.token_type == TokenType.WORD:
            res += token.value
            break
        elif token.token_type == TokenType.PUNC and token.value == "-":
            res += token.value
            token_stream.next()
        elif token.token_type == TokenType.STRING:
            res += token.value
            break
        elif token.token_type == TokenType.PUNC and token.value == "[":
            token_stream.next()
            return parse_list(
                token_stream, INLINE_LIST_DELIMITER, INLINE_LIST_SEPARATOR
            )
        elif token.token_type == TokenType.PUNC and token.value == "(":
            token_stream.next()
            return parse_tuple(token_stream)
        elif token.token_type in [TokenType.NEWLINE, TokenType.EOF, TokenType.DEDENT]:
            break
        else:
            token_stream.croak(f"Expected WORD or PUNC token, but got {token}")
    return res


def parse_list(
    token_stream: ParseTokenStream, delimiter: Token, separator: Token
) -> List[Any]:
    res: List[Any] = []
    delimited = False
    while not token_stream.is_eof():
        token = token_stream.peek()
        res += [parse_inline_expression(token_stream)]
        token_stream.next()
        token = token_stream.peek()
        if token.token_type == delimiter.token_type and token.value == delimiter.value:
            delimited = True
            break
        elif (
            token.token_type == separator.token_type and token.value == separator.value
        ):
            token_stream.next()
            continue
        else:
            token_stream.croak(
                f"Expected '{delimiter.value}' or '{separator.value}' but got '{token.value}'"
            )
    if not delimited:
        token_stream.croak(f"Expected '{delimiter.value}', but got EOF")
    return res


def parse_tuple(token_stream: ParseTokenStream) -> Tuple[Any]:
    res = parse_list(
        token_stream, Token(TokenType.PUNC, ")"), Token(TokenType.PUNC, ",")
    )
    res_tuple = tuple(res)
    return res_tuple


def parse(string: str) -> Config:
    parse_token_stream = ParseTokenStream(string)
    ast = parse_block(parse_token_stream, till_dedent=False)
    config = Config(ast)
    config = resolve(config, [PythonDataTypeResolver()])
    return config
