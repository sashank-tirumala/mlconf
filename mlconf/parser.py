import logging
import os

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
    return interpet_config(mlconfig)


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
        if count <= 1:
            val = os.getenv(token["value"], None)
            if val is None:
                token_stream.croak(f"Environment variable not found: {token['value']}")
        else:
            val = "var(" + token["value"]
            while True:
                token = token_stream.read_next()
                if token["type"] == "punc" and token["value"] == "}":
                    break
                elif token["type"] == "punc" and token["value"] == ".":
                    val += "."
                    token = token_stream.read_next()
                    if token["type"] == "name":
                        val += token["value"]
                    else:
                        token_stream.croak(f"Expected a name, got: {token}")
                else:
                    token_stream.croak("Expected a '.' or '}'" + f", got: {token}")
            val += ")"
        return val
    elif token["type"] == "punc" and token["value"] == "{":
        if count <= 1:
            val = parse_var(token_stream, count + 1)
            if count == 0:
                skip_punc(token_stream, "}")
        else:
            token_stream.croak(
                f"Invalid number of brackets (more than 2), if this is a string please enclose it with quotes {token_stream.input.peek()}"
            )
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


def skip_punc(token_stream, punc, no_croak=False):
    """
    This skips a punc-token
    """
    token = token_stream.read_next()
    if token["value"] == punc:
        return True
    else:
        if no_croak:
            return False
        else:
            print(token)
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


def read_till_delimiter(token_stream, delimiter):
    """
    This reads till a delimiter
    """
    value = ""
    while True:
        token = token_stream.read_next()
        if token["type"] == delimiter and token["value"] == delimiter:
            return value
        else:
            value += token["value"]


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


def interpet_config(config: MLConfig):
    leafnode_name_value_list = config.leafnode_name_value_list
    var_stack = {}
    for name, value in leafnode_name_value_list:
        if name in var_stack:
            raise ValueError(f"Variable {name} already exists")
        if isinstance(value, str):
            var = parse_local_var(value, var_stack)
            config.set_leafnode_val(name, var)
            var_stack[name] = var
        else:
            var_stack[name] = value
    return config


def parse_local_var(value, var_stack):
    res = ""
    i = 0
    last4_chars = ""
    read_var_state = False
    for i in range(len(value)):
        char = value[i]
        if read_var_state:
            if char == ")":
                if var_name not in var_stack:
                    raise ValueError(f"Variable {res} not defined")
                res += str(var_stack[var_name])
                read_var_state = False
            else:
                var_name += char
        else:
            if len(last4_chars) == 4:
                last4_chars = last4_chars[1:] + char
            else:
                last4_chars += char
            if last4_chars == "var(":
                last4_chars = ""
                res = res[:-3]
                read_var_state = True
                var_name = ""
            else:
                res += char
        i += 1
    # print(res)
    return res


if __name__ == "__main__":
    config = "string:test\n"
    config += "string2: \n"
    config += "  test:1\n"
    config += "  string3:\n"
    config += "    test:1\n"
    config += "number: 1.0"
    print(parse(config))
