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
        elif is_name_or_var(token):
            if token["type"] == "name":
                name = token["value"]
            else:
                name = parse_var(token_stream)
            name += parse_string_var_combo(token_stream, is_colon)
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
        elif token["type"] in ["string", "number", "bool", "null"]:
            value = token["value"]
            skip_value_end(token_stream)
            return value
        elif token["type"] == "indent":
            indent_count = token["value"]
            return parse_config(token_stream, indent_count)
        elif token["type"] == "newline":
            continue
        elif is_name_or_var(token):
            if token["type"] == "name":
                name = token["value"]
            else:
                name = parse_var(token_stream)
            name += parse_string_var_combo(token_stream, is_end)
            return name
        else:
            token_stream.croak(f"Unexpected token: {token}")


def parse_var(token_stream, count=0):
    """
    This parses a variable
    """
    token = token_stream.read_next()
    if token["type"] == "name":
        val = os.getenv(token["value"], None)
        if val is None:
            token_stream.croak(f"Environment variable not found: {token['value']}")
        return val
    elif token["type"] == "punc" and token["value"] == "{":
        if count == 0:
            val = parse_var(token_stream, count + 1)
            skip_punc(token_stream, "}")
        return val
    else:
        token_stream.croak(f"Invalid_variable: {token}")


def parse_string_var_combo(token_stream, delimiter):
    """
    This parses till a delimiter
    """
    value = ""
    while True:
        token = token_stream.read_next()
        if token["type"] in ["string", "name"]:
            value += token["value"]
        elif token["type"] == "punc" and token["value"] == "$":
            value += parse_var(token_stream)
        elif token["type"] == "punc" and token["value"] == "/":
            value += "/"
            continue
        elif delimiter(token):
            return value
        else:
            token_stream.croak(f"Unexpected char: {token_stream.input.peek()}")


def is_name_or_var(token):
    """
    This checks if the token is a name or a variable
    """
    return token["type"] == "name" or (token["type"] == "punc" and token["value"] == "$")


def is_colon(token):
    """
    This checks if the token is a colon
    """
    return token["type"] == "punc" and token["value"] == ":"


def skip_punc(token_stream, punc):
    """
    This skips a newline
    """
    token = token_stream.read_next()
    if token["value"] == punc:
        return
    else:
        token_stream.croak(f"Expected a {punc}, got: {token_stream.input.peek()}")


def is_end(token):
    """
    This checks if the token is a newline
    """
    return token["type"] == "newline" or token["type"] == "dedent" or token is None


def skip_value_end(token_stream):
    """
    This skips a newline
    """
    token = token_stream.read_next()
    if token["type"] == "newline" or token["type"] == "dedent" or token is None:
        return
    else:
        token_stream.croak(f"Expected a newline, got: {token}")


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
