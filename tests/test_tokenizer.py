import pytest

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


def test_num_simple():
    inp = "num: 123\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "num"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": 123.0},
        {"type": "newline", "value": "\n"},
    ]

    inp = "num : 123\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "num"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": 123.0},
        {"type": "newline", "value": "\n"},
    ]

    inp = "num :123   \n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "num"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": 123.0},
        {"type": "newline", "value": "\n"},
    ]


# def test_num_decimal():
#     inp = "num: 123.456\n"
#     tokens = get_tokens(inp)
#     assert tokens == [
#         {"type": "name", "value": "num"},
#         {"type": "punc", "value": ":"},
#         {"type": "number", "value": 123.456},
#         {"type": "newline", "value": "\n"},
#     ]

#     inp = "num : -123.456\n"
#     tokens = get_tokens(inp)
#     assert tokens == [
#         {"type": "name", "value": "num"},
#         {"type": "punc", "value": ":"},
#         {"type": "number", "value": -123.456},
#         {"type": "newline", "value": "\n"},
#     ]

#     inp = "num : 123.456e-2\n"
#     tokens = get_tokens(inp)
#     assert tokens == [
#         {"type": "name", "value": "num"},
#         {"type": "punc", "value": ":"},
#         {"type": "number", "value": 1.23456},
#         {"type": "newline", "value": "\n"},
#     ]

#     inp = "num : 123.456e+2\n"
#     tokens = get_tokens(inp)
#     assert tokens == [
#         {"type": "name", "value": "num"},
#         {"type": "punc", "value": ":"},
#         {"type": "number", "value": 12345.6},
#         {"type": "newline", "value": "\n"},
#     ]

#     inp = "num : 123.456e2\n"
#     tokens = get_tokens(inp)
#     assert tokens == [
#         {"type": "name", "value": "num"},
#         {"type": "punc", "value": ":"},
#         {"type": "number", "value": 12345.6},
#         {"type": "newline", "value": "\n"},
#     ]


def test_num_sign():
    inp = "num: +123\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "num"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": 123.0},
        {"type": "newline", "value": "\n"},
    ]

    inp = "num : -123\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "num"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": -123.0},
        {"type": "newline", "value": "\n"},
    ]

    inps = ["num : --123\n", "num : ++123\n", "num : +-123\n", "num : -+123\n"]
    for inp in inps:
        with pytest.raises(SyntaxError):
            get_tokens(inp)
