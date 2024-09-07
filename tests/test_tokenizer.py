from typing import List

from mlconf.token import (
    Token,
    TokenType,
    get_tokens,
    replace_whitespace_with_indent_dedent_tokens,
)


def test_lexer(simple_config_str):
    tokens = get_tokens(simple_config_str)
    assert tokens == [
        Token(TokenType.WORD, "training"),
        Token(TokenType.PUNC, ":"),
        Token(TokenType.NEWLINE, ""),
        Token(TokenType.INDENT, ""),
        Token(TokenType.WORD, "name"),
        Token(TokenType.PUNC, ":"),
        Token(TokenType.WORD, "MLConf"),
        Token(TokenType.NEWLINE, ""),
        Token(TokenType.WORD, "epochs"),
        Token(TokenType.PUNC, ":"),
        Token(TokenType.WORD, "10"),
        Token(TokenType.NEWLINE, ""),
        Token(TokenType.WORD, "batch_size"),
        Token(TokenType.PUNC, ":"),
        Token(TokenType.WORD, "32"),
        Token(TokenType.NEWLINE, ""),
        Token(TokenType.WORD, "learning_rate"),
        Token(TokenType.PUNC, ":"),
        Token(TokenType.WORD, "0.001"),
        Token(TokenType.DEDENT, ""),
    ]


def create_white_space_tokens_from_list_of_ints(
    white_space_list: List[int],
) -> List[Token]:
    return [Token(TokenType.WHITESPACE, str(i)) for i in white_space_list]


def indent_equal_dedent_tokens(tokens: List[Token]) -> None:
    indents = len([x for x in tokens if x.token_type == TokenType.INDENT])
    dedents = len([x for x in tokens if x.token_type == TokenType.DEDENT])
    assert indents == dedents


def test_indent_dedent_tokens():
    tokens = create_white_space_tokens_from_list_of_ints([2, 4, 6, 4, 2])
    res1 = replace_whitespace_with_indent_dedent_tokens(tokens)
    tokens = create_white_space_tokens_from_list_of_ints(
        [
            2,
            2,
            2,
            4,
            4,
            6,
            6,
            6,
            4,
            4,
            4,
            2,
            2,
        ]
    )
    res2 = replace_whitespace_with_indent_dedent_tokens(tokens)
    tokens = create_white_space_tokens_from_list_of_ints([2, 4, 4, 4, 4, 6, 6, 6, 6])
    res3 = replace_whitespace_with_indent_dedent_tokens(tokens)
    assert res1 == res2
    assert res1 == res3
    indent_equal_dedent_tokens(res1)

    tokens = create_white_space_tokens_from_list_of_ints(
        [1, 2, 2, 3, 3, 3, 2, 2, 3, 3, 3, 2, 1, 1, 2, 2, 3, 3]
    )
    res1 = replace_whitespace_with_indent_dedent_tokens(tokens)
    indent_equal_dedent_tokens(res1)
