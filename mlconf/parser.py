import os
import re

from mlconf.input_stream import InputStream
from mlconf.mlconfig import MLConfig
from mlconf.tokenizer import TokenStream

BASH_VAR_PATTERN_WITH_BRACKETS = r"\$\{([a-zA-Z0-9_]+)\}(?!\})"  # This matches ${name} but not ${{name}}
BASH_VAR_PATTERN_RAW = r"\$(?:(\w+))"


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
            skip_punc(token_stream, ":")
            mlconfig[name] = parse_value(token_stream)
        elif token["type"] == "newline" or token["type"] == "indent":
            continue
        elif token["type"] == "dedent":
            if token["value"] == indent_count:
                return mlconfig
            else:
                token_stream.croak(f"Expected an indent of {indent_count}, got: {token['value']}")
        elif token["type"] == "punc" and token["value"] == "$":
            name = parse_var(token_stream)
            skip_punc(token_stream, ":")
            mlconfig[name] = parse_value(token_stream)
        else:
            token_stream.croak(f"Unexpected token, probably a number or a string with no name: {token}")
    return mlconfig


def parse_value(token_stream):
    """
    This parses a value
    """
    while True:
        token = token_stream.read_next()
        if token is None:
            token_stream.croak("Unexpected end of file")
        elif token["type"] in ["name", "string", "number", "bool", "null"]:
            value = token["value"]
            skip_value_end(token_stream)
            return value
        elif token["type"] == "indent":
            indent_count = token["value"]
            return parse_config(token_stream, indent_count)
        elif token["type"] == "newline":
            continue
        elif token["type"] == "punc" and token["value"] == "$":
            value = parse_var(token_stream)
            skip_value_end(token_stream)
            return value
        else:
            token_stream.croak(f"Unexpected token: {token}")


def parse_var(token_stream):
    """
    This parses a variable
    """
    token = token_stream.read_next()
    if token["type"] == "name":
        val = os.getenv(token["value"], None)
        if val is None:
            token_stream.croak(f"Environment variable not found: {token['value']}")
        return val
    else:
        token_stream.croak(f"Invalid_variable: {token}")


def skip_punc(token_stream, punc):
    """
    This skips a newline
    """
    token = token_stream.read_next()
    if token["value"] == punc:
        return
    else:
        token_stream.croak(f"Expected a {punc}, got: {token_stream.input.peek()}")


def skip_value_end(token_stream):
    """
    This skips a newline
    """
    token = token_stream.read_next()
    if token["type"] == "newline" or token["type"] == "dedent" or token is None:
        return
    else:
        token_stream.croak(f"Expected a newline, got: {token}")


def evaluate_name(string):
    """
    This evaluates a name
    """
    pattern = r"\$(?:(\w+))"  # This matches $name
    string = substitute_os_var(string, pattern)
    pattern = r"\$\{([a-zA-Z0-9_]+)\}(?!\})"  # This matches ${name} but not ${{name}}
    string = substitute_os_var(string, pattern)
    return string


def substitute_os_var(string, pattern):
    def replace_func(match):
        var_name = match.group(1)
        return os.getenv(var_name, match.group(0))

    return re.sub(pattern, replace_func, string)


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
