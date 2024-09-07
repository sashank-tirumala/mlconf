from typing import Any, Dict

from mlconf.token import ParseTokenStream, TokenType


def parse(token_stream: ParseTokenStream) -> Dict[str, Any]:
    ast = {}
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
                else:
                    token_stream.croak(f"Expected WORD token, but got {token}")
            else:
                token_stream.croak(f"Expected PUNC token, but got {token}")
        elif token.token_type == TokenType.NEWLINE:
            token_stream.next()
        else:
            token_stream.croak(f"Expected WORD or NEWLINE token, but got {token}")
    return ast


if __name__ == "__main__":
    string = "training: MLConf\nepochs: 10 \nbatch_size: 32\nlearning_rate: 0.001"
    parse_token_stream = ParseTokenStream(string)
    ast = parse(parse_token_stream)
    print(ast)
