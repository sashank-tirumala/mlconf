from mlconf.token import Token, TokenType, get_tokens


def test_lexer(simple_config_str):
    tokens = get_tokens(simple_config_str)
    assert tokens == [
        Token(TokenType.WORD, "training"),
        Token(TokenType.PUNC, ":"),
        Token(TokenType.NEWLINE, ""),
        Token(TokenType.WHITESPACE, "8"),
        Token(TokenType.WORD, "name"),
        Token(TokenType.PUNC, ":"),
        Token(TokenType.WORD, "MLConf"),
        Token(TokenType.NEWLINE, ""),
        Token(TokenType.WHITESPACE, "8"),
        Token(TokenType.WORD, "epochs"),
        Token(TokenType.PUNC, ":"),
        Token(TokenType.WORD, "10"),
        Token(TokenType.NEWLINE, ""),
        Token(TokenType.WHITESPACE, "8"),
        Token(TokenType.WORD, "batch_size"),
        Token(TokenType.PUNC, ":"),
        Token(TokenType.WORD, "32"),
        Token(TokenType.NEWLINE, ""),
        Token(TokenType.WHITESPACE, "8"),
        Token(TokenType.WORD, "learning_rate"),
        Token(TokenType.PUNC, ":"),
        Token(TokenType.WORD, "0.001"),
    ]
