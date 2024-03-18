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

    inp = 'str123ing :     "hel3qrtlo_wor:$$*rld" \n'
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "str123ing"},
        {"type": "punc", "value": ":"},
        {"type": "string", "value": "hel3qrtlo_wor:$$*rld"},
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


def test_num_decimal():
    inp = "num: 123.456\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "num"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": 123.456},
        {"type": "newline", "value": "\n"},
    ]

    inp = "num : -123.456\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "num"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": -123.456},
        {"type": "newline", "value": "\n"},
    ]

    inp = "num : 123.456e-2\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "num"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": 1.23456},
        {"type": "newline", "value": "\n"},
    ]

    inp = "num : 123.456e+2\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "num"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": 12345.6},
        {"type": "newline", "value": "\n"},
    ]

    inp = "num : 123.456E2\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "num"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": 12345.6},
        {"type": "newline", "value": "\n"},
    ]


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

    invalid_inps = [
        "num : --123\n",
        "num : ++123\n",
        "num : +-123\n",
        "num : -+123\n",
        "num : +123.456e-+2\n",
        "num : +123.456.789\n",
    ]
    for inp in invalid_inps:
        with pytest.raises(SyntaxError):
            get_tokens(inp)


def test_multi_line_simple():
    string_inp = "string: 'hello_world'"
    newline_inp = "\n"
    num_inp = "num: 123"
    name_inp = "name: value"
    assert_string = [
        {"type": "name", "value": "string"},
        {"type": "punc", "value": ":"},
        {"type": "string", "value": "hello_world"},
    ]
    assert_newline = [{"type": "newline", "value": "\n"}]
    assert_num = [
        {"type": "name", "value": "num"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": 123.0},
    ]
    assert_name = [
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
    ]
    inp = string_inp + newline_inp + num_inp + newline_inp + name_inp
    assert_inp = assert_string + assert_newline + assert_num + assert_newline + assert_name
    tokens = get_tokens(inp)
    assert tokens == assert_inp

    inp = string_inp + newline_inp + newline_inp + num_inp + newline_inp + name_inp + newline_inp
    assert_inp = (
        assert_string + assert_newline + assert_newline + assert_num + assert_newline + assert_name + assert_newline
    )
    tokens = get_tokens(inp)
    assert tokens == assert_inp

    inp = (
        string_inp
        + " "
        + num_inp
        + " "
        + name_inp
        + " "
        + string_inp
        + " "
        + name_inp
        + " "
        + num_inp
        + " "
        + string_inp
    )
    assert_inp = assert_string + assert_num + assert_name + assert_string + assert_name + assert_num + assert_string
    tokens = get_tokens(inp)
    assert tokens == assert_inp


def test_simple_name():
    inp = "name: value\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
    ]

    inp = "name : value\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
    ]

    inp = "name :value   \n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
    ]


def test_complex_name():
    inp = "name: value_123\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value_123"},
        {"type": "newline", "value": "\n"},
    ]

    invalid_inps = [
        "name: value-uef\n",
        "name: value+uef\n",
    ]
    for inp in invalid_inps:
        with pytest.raises(SyntaxError):
            get_tokens(inp)

    # TODO : activate harder tests
    # invalid_inps = [
    #     "name: value-123\n",
    #     "name: value.887\n",
    # ]
    # for inp in invalid_inps:
    #     with pytest.raises(SyntaxError):
    #         get_tokens(inp)


def test_indentation_simple1():
    inp = "name: value\n" + "  name: value\n" + "    name: value\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
        {"type": "indent", "value": 2},
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
        {"type": "indent", "value": 4},
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
        {"type": "dedent", "value": 0},
    ]


def test_indentation_simple2():
    inp = "name: value\n" + "  name: value\n" + "    name: value\n" + "  name: value\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
        {"type": "indent", "value": 2},
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
        {"type": "indent", "value": 4},
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
        {"type": "dedent", "value": 2},
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
        {"type": "dedent", "value": 0},
    ]


def test_indentation_simple3():
    inp = "name: value\n" + "  name: value\n" + "name: value\n" + " name: value\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
        {"type": "indent", "value": 2},
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
        {"type": "dedent", "value": 0},
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
        {"type": "indent", "value": 1},
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
        {"type": "dedent", "value": 0},
    ]


def test_indentation_simple4():
    invalid_inps = [
        "name: value\n" + "  name: value\n" + "    name: value\n" + " name: value\n" + "name: value\n",
        "name: value\n" + "  name: value\n" + "    name: value\n" + "   name: value\n" + "  name: value\n",
    ]
    for inp in invalid_inps:
        with pytest.raises(SyntaxError):
            get_tokens(inp)


def test_null():
    inp = "name: null\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "null", "value": None},
        {"type": "newline", "value": "\n"},
    ]

    inp = "name: None\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "null", "value": None},
        {"type": "newline", "value": "\n"},
    ]


def test_bool():
    inp = "name: true\n" + "name: false\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "bool", "value": True},
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "bool", "value": False},
        {"type": "newline", "value": "\n"},
    ]

    inp = "name: True\n" + "name: False\n"
    tokens = get_tokens(inp)
    assert tokens == [
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "bool", "value": True},
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "bool", "value": False},
        {"type": "newline", "value": "\n"},
    ]
