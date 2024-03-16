from mlconf.parser import InputStream, TokenStream, get_tokens


def test_string_simple():
    inp = "string: 'hello_world'\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "string"},
        {"type": "punc", "value": ":"},
        {"type": "string", "value": "hello_world"},
        {"type": "newline", "value": "\n"},
    ]

    inp = 'string : "hello_world" \n'
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "string"},
        {"type": "punc", "value": ":"},
        {"type": "string", "value": "hello_world"},
        {"type": "newline", "value": "\n"},
    ]

    inp = 'string :"hello_world" \n'
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "string"},
        {"type": "punc", "value": ":"},
        {"type": "string", "value": "hello_world"},
        {"type": "newline", "value": "\n"},
    ]


def test_string_complex():
    inp = 'string :     "hel3qrtlo_wor$$*rld" \n'
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "string"},
        {"type": "punc", "value": ":"},
        {"type": "string", "value": "hel3qrtlo_wor$$*rld"},
        {"type": "newline", "value": "\n"},
    ]

    inp = 'str123ing :     "hel3qrtlo_wor$$*rld" \n'
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "str123ing"},
        {"type": "punc", "value": ":"},
        {"type": "string", "value": "hel3qrtlo_wor$$*rld"},
        {"type": "newline", "value": "\n"},
    ]

    inp = "string: 'hell\\%r_world'\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "string"},
        {"type": "punc", "value": ":"},
        {"type": "string", "value": "hell%r_world"},
        {"type": "newline", "value": "\n"},
    ]


def test_string_newline():
    inp = "\n" + "string: 'hello_world'\n\n\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "string"},
        {"type": "punc", "value": ":"},
        {"type": "string", "value": "hello_world"},
        {"type": "newline", "value": "\n"},
        {"type": "newline", "value": "\n"},
        {"type": "newline", "value": "\n"},
    ]

    inp = "# v$^&*(::abc123---)\n" + "string: 'hello_world'\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "string"},
        {"type": "punc", "value": ":"},
        {"type": "string", "value": "hello_world"},
        {"type": "newline", "value": "\n"},
    ]
