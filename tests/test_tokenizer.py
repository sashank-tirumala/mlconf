import pytest

from mlconf.tokenizer import get_tokens


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
        {"type": "dedent", "value": 4},
        {"type": "dedent", "value": 2},
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
        {"type": "dedent", "value": 4},
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
        {"type": "dedent", "value": 2},
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
        {"type": "dedent", "value": 2},
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
        {"type": "indent", "value": 1},
        {"type": "name", "value": "name"},
        {"type": "punc", "value": ":"},
        {"type": "name", "value": "value"},
        {"type": "newline", "value": "\n"},
        {"type": "dedent", "value": 1},
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


def test_bug_config_repeat_nested():
    """
    This test is to check if the tokenizer can handle an input with repeated nested keys
    """
    cfg = (
        "import a12bcd\n"
        "a: 1\n"
        + "b: 2\n"
        + "c: True\n"
        + "d: None\n"
        + "e:\n"
        + "  b: 3e+2\n"
        + "  c: +4e2\n"
        + "  d: False\n"
        + "  e: null\n"
        + "  f:\n"
        + "    a: 5\n"
        + "    b: -6e-3\n"
        + "f: 0.07\n"
    )
    tokens = get_tokens(cfg)
    assert tokens == [
        {"type": "import", "value": "import"},
        {"type": "name", "value": "a12bcd"},
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "a"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": 1.0},
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "b"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": 2.0},
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "c"},
        {"type": "punc", "value": ":"},
        {"type": "bool", "value": True},
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "d"},
        {"type": "punc", "value": ":"},
        {"type": "null", "value": None},
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "e"},
        {"type": "punc", "value": ":"},
        {"type": "newline", "value": "\n"},
        {"type": "indent", "value": 2},
        {"type": "name", "value": "b"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": 300.0},
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "c"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": 400.0},
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "d"},
        {"type": "punc", "value": ":"},
        {"type": "bool", "value": False},
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "e"},
        {"type": "punc", "value": ":"},
        {"type": "null", "value": None},
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "f"},
        {"type": "punc", "value": ":"},
        {"type": "newline", "value": "\n"},
        {"type": "indent", "value": 4},
        {"type": "name", "value": "a"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": 5.0},
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "b"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": -0.006},
        {"type": "newline", "value": "\n"},
        {"type": "dedent", "value": 4},
        {"type": "dedent", "value": 2},
        {"type": "name", "value": "f"},
        {"type": "punc", "value": ":"},
        {"type": "number", "value": 0.07},
        {"type": "newline", "value": "\n"},
    ]


def test_var_format():
    config = "path: $HO1ME__25\n"
    config += "path2: ${{HOME}}\n"
    config += "path_$HI_3: ${HOME_HOMEY}/config/dev\n"
    config += "path3: ${{path2.path3.path.pathx}}\n"
    tokens = get_tokens(config)
    assert tokens == [
        {"type": "name", "value": "path"},
        {"type": "punc", "value": ":"},
        {"type": "punc", "value": "$"},
        {"type": "name", "value": "HO1ME__25"},
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "path2"},
        {"type": "punc", "value": ":"},
        {"type": "punc", "value": "$"},
        {"type": "punc", "value": "{"},
        {"type": "punc", "value": "{"},
        {"type": "name", "value": "HOME"},
        {"type": "punc", "value": "}"},
        {"type": "punc", "value": "}"},
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "path_"},
        {"type": "punc", "value": "$"},
        {"type": "name", "value": "HI_3"},
        {"type": "punc", "value": ":"},
        {"type": "punc", "value": "$"},
        {"type": "punc", "value": "{"},
        {"type": "name", "value": "HOME_HOMEY"},
        {"type": "punc", "value": "}"},
        {"type": "punc", "value": "/"},
        {"type": "name", "value": "config"},
        {"type": "punc", "value": "/"},
        {"type": "name", "value": "dev"},
        {"type": "newline", "value": "\n"},
        {"type": "name", "value": "path3"},
        {"type": "punc", "value": ":"},
        {"type": "punc", "value": "$"},
        {"type": "punc", "value": "{"},
        {"type": "punc", "value": "{"},
        {"type": "name", "value": "path2"},
        {"type": "punc", "value": "."},
        {"type": "name", "value": "path3"},
        {"type": "punc", "value": "."},
        {"type": "name", "value": "path"},
        {"type": "punc", "value": "."},
        {"type": "name", "value": "pathx"},
        {"type": "punc", "value": "}"},
        {"type": "punc", "value": "}"},
        {"type": "newline", "value": "\n"},
    ]


def test_import_statement():
    cfg = "import config\n"
    tokens = get_tokens(cfg)
    assert tokens == [
        {"type": "import", "value": "import"},
        {"type": "name", "value": "config"},
        {"type": "newline", "value": "\n"},
    ]
