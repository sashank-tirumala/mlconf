from typing import Any, Dict, List, Tuple

from mlconf.config import Config
from mlconf.resolver import Resolvers, resolve
from mlconf.tokenizer import ParseTokenStream, Token, TokenType
from mlconf.word import Word

INLINE_LIST_DELIMITER = Token(TokenType.PUNC, "]")
INLINE_LIST_SEPARATOR = Token(TokenType.PUNC, ",")


def skip_tokens(token_stream: ParseTokenStream, token_types: List[TokenType]) -> None:
    while True:
        token = token_stream.peek()
        if token.token_type not in token_types:
            break
        token_stream.next()


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
                        token = token_stream.peek()
                        if token.token_type == TokenType.PUNC and token.value == "-":
                            ast[key] = parse_yaml_list(token_stream)
                        else:
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
        # elif token.token_type == TokenType.KEY_WORD and till_dedent is False:
        #     if token.value == KeyWords.IMPORT:
        #         parse_
        else:
            token_stream.croak(
                f"Expected WORD or NEWLINE token, but got {token.token_type}"
            )
    return ast


def parse_yaml_list(token_stream: ParseTokenStream) -> List[Any]:
    res: List[Any] = []
    while not token_stream.is_eof():
        token = token_stream.peek()
        if token.token_type == TokenType.PUNC and token.value == "-":
            token_stream.next()
            next_token = token_stream.peek_next()
            if next_token.token_type == TokenType.PUNC and next_token.value == ":":
                res += [parse_block(token_stream, till_dedent=True)]
            else:
                res += [parse_inline_expression(token_stream)]
                token_stream.next()
        elif token.token_type == TokenType.NEWLINE:
            token_stream.next()
        elif token.token_type == TokenType.EOF or token.token_type == TokenType.DEDENT:
            break
        else:
            token_stream.croak(f"Expected PUNC token, but got {token}")
    return res


def parse_inline_expression(token_stream: ParseTokenStream) -> Any:
    res = ""
    is_word = False
    while not token_stream.is_eof():
        token = token_stream.peek()
        if token.token_type == TokenType.WORD:
            is_word = True
            res += token.value
            break
        elif token.token_type == TokenType.PUNC and token.value == "-":
            is_word = True
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
    if is_word:
        return Word(res)
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
    # vars = parse_imports(parse_token_stream) TODO: Activate
    ast = parse_block(parse_token_stream, till_dedent=False)
    config = Config(ast)
    resolvers = Resolvers(config)
    config = resolve(config, resolvers)
    return config
