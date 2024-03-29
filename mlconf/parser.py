import os
from pathlib import Path

from mlconf.input_stream import InputStream
from mlconf.mlconfig import MLConfig
from mlconf.tokenizer import TokenStream
from mlconf.utils import get_import_path_if_exists, get_var_stack, merge_dicts


def parse_config(token_stream, indent_count=0, base_path=Path(".")):
    """
    This parses an entire configuration file
    """
    mlconfig = MLConfig()
    import_vars = {}
    while True:
        token = token_stream.read_next()
        if token is None:
            break
        elif is_import(token):
            import_vars = merge_dicts(import_vars, parse_import(token_stream, base_path))
            if import_vars is None:
                token_stream.croak(f"Import failed (probably same variable name is being redefined): {token['value']}")
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
    return interpet_config(mlconfig, import_vars)


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


def parse_import(token_stream, base_path):
    """
    This parses an import
    """
    res_path = ""
    file_name = ""
    while True:
        token = token_stream.read_next()
        if token["type"] == "string" or token["type"] == "name":
            res_path += token["value"]
            token = token_stream.read_next()
            if token["type"] == "punc" and token["value"] == ".":
                res_path += "/"
                continue
            elif token["type"] == "newline":
                file_name = Path(res_path).stem
                break
            elif token["type"] == "as":
                token = token_stream.read_next()
                if token["type"] == "name":
                    file_name = token["value"]
                    break
                else:
                    token_stream.croak(f"Expected a name, got: {token['value']}")
            else:
                token_stream.croak(f"Expected a newline or 'as', got: {token['value']}")
        else:
            token_stream.croak(f"Expected a string or a name, got: {token['value']}")
            break
    file_path = get_import_path_if_exists(res_path, base_path)
    if file_path is None:
        token_stream.croak(f"File {token['value']} not found")
    with open(file_path, "r") as f:
        config = f.read()
    config = parse(config, base_path=file_path.parent)
    var_stack = get_var_stack(config, file_name)
    return var_stack


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


def is_import(token):
    """
    This checks if the token is an import
    """
    return token["type"] == "import"


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
    if token is None:
        return
    elif token["type"] == "newline" or token["type"] == "dedent":
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


def parse(input, base_path=Path(".")):
    return parse_config(TokenStream(InputStream(input)), base_path=base_path)


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


def interpet_config(config: MLConfig, var_stack):
    leafnode_name_value_list = config.leafnode_name_value_list
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
                    raise ValueError(f"Variable {var_name} not defined")
                val = var_stack[var_name]
                if isinstance(val, str):
                    res += str(var_stack[var_name])
                else:
                    # TODO: Error out if a non string followed by a string
                    res = val
                    break
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
    return res


if __name__ == "__main__":
    cfg_str = (
        "import h1h2\n"
        "import sub_test.h2h1\n"
        "import h3h1 as imp\n"
        + "a: 1\n"
        + "b: 2\n"
        + "c: True\n"
        + "d: ${{imp.test.test1}}\n"
        + "e:\n"
        + "  b: 3e+2\n"
        + "  c: +4e2\n"
        + "  d: ${{ h2h1.c.d}}\n"
        + "  e: ${{ h1h2.b.c }}\n"
        + "  g:\n"
        + "    a: ttt\n"
        + "    b: -6e-3\n"
        + "g: ${{ h1h2.a }}\n"
    )
    # config = "string:test\n"
    # config += "string2: \n"
    # config += "  test:1\n"
    # config += "  string3:\n"
    # config += "    test:1\n"
    # config += "number: 1.0"
    print(parse(cfg_str, base_path=Path("/home/robot/projects/mlconf/tests/test_confs")))
