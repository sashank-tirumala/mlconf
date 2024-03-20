from mlconf.input_stream import InputStream
from mlconf.mlconfig import MLConfig
from mlconf.tokenizer import TokenStream


def parse_config(token_stream, indent_count=0):
    """
    This parses an entire configuration file
    """
    mlconfig = MLConfig()
    while True:
        token = token_stream.read_next()
        if token is None:
            break
        elif token["type"] == "name":
            name = token["value"]
            token = token_stream.read_next()
            if token["type"] == "punc":
                if token["value"] == ":":
                    mlconfig[name] = parse_value(token_stream)
                else:
                    token_stream.croak(f"Expected a colon, got: {token}")
        elif token["type"] == "newline" or token["type"] == "indent":
            continue
        elif token["type"] == "dedent":
            if token["value"] == indent_count:
                return mlconfig
            else:
                token_stream.croak(f"Expected an indent of {indent_count}, got: {token['value']}")
        else:
            token_stream.croak(f"Unexpected token, probably a number or a string with no name: {token}")
    return mlconfig


def parse_value(token_stream):
    """
    This parses an expression
    """
    while True:
        token = token_stream.read_next()
        if token is None:
            token_stream.croak("Unexpected end of file")
        elif token["type"] in ["name", "string", "number", "bool", "null"]:
            value = token["value"]
            next_token = token_stream.read_next()
            if next_token is None or next_token["type"] == "newline" or next_token == {"type": "dedent", "value": 0}:
                return value
            else:
                token_stream.croak(f"Expected a newline, got: {next_token}")
        elif token["type"] == "indent":
            indent_count = token["value"]
            return parse_config(token_stream, indent_count)
        elif token["type"] == "newline":
            continue
        else:
            token_stream.croak(f"Unexpected token: {token}")


def parse(input):
    return parse_config(TokenStream(InputStream(input)))


def parse_cli_input(input):
    try:
        return float(input)
    except ValueError:
        if input == "true" or input == "True":
            return True
        elif input == "false" or input == "False":
            return False
        elif input == "null" or input == "None":
            return None
        else:
            return input


if __name__ == "__main__":
    config = "string:test\n"
    config += "string2: \n"
    config += "  test:1\n"
    config += "  string3:\n"
    config += "    test:1\n"
    config += "number: 1.0"
    print(parse(config))
