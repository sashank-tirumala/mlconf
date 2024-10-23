import os

import pytest

from mlconf.parser import parse


def test_parser(simple_config_str, simple_config_dict_str):
    conf = parse(simple_config_str)
    assert conf.training.name == "MLConf"
    assert conf.training.epochs == 10
    assert conf.training.batch_size == 32
    assert conf.training.learning_rate == 0.001


def test_test1_config(test1_config_str):
    conf = parse(test1_config_str)
    assert conf.a1.b1.c1 == 122
    assert conf.a1.b1.c2 == 2.01
    assert conf.a1.b2 == -2.11
    assert conf.a1.b3 == 0.01
    assert conf.a1.b4.c3 == 3.0
    assert conf.a1.b4.c4 == "hello"
    assert conf.a1.b4.c5.d1 is None
    assert conf.a1.b4.c5.d2 is None
    assert conf.a1.b4.c5.d3.e1 == "world"
    assert conf.a1.b4.c5.d3.e2 == 2
    assert conf.a1.b4.c5.d4 == [12, "hello", "world", [1, [1.1, "base"], 3]]
    assert conf.a1.b4.c5.d5 == (1, 2, (3, 4), 5)
    assert conf.a1.b4.c6
    assert conf.a1.b4.c7
    assert not conf.a1.b5
    assert not conf.a1.b6
    assert conf.a2 == 2
    assert conf.a3 == 3
    assert conf.a4.b7.c8.d5 == "brave new world~!@#$%^&*()_+=-`[]{}|;':,.<>?/\\"
    assert conf.a4.b7.c8.d6 == 'brave new world~!@#$%^&*()_+=-`[]{}|;":,.<>?/\\'
    assert conf.a4.b7.c9[0] == "x1"
    assert conf.a4.b7.c9[1] == 10.2
    assert "list" in conf.a4.b7.c9[2]
    assert conf.a4.b7.c9[2].list.a == 1
    assert conf.a4.b7.c9.l2.list.a == 1
    assert conf.a4.b7.c9[2]["list"]["b"] == 2
    assert conf.a4.b7.c9[2].list.c.d == 3
    assert conf.a4.b7.c9[2].list.c.e[0] == 1
    assert conf.a4.b7.c9[2].list.c.e[1] == (2, ("a", "b"), 3)
    assert conf.a4.b7.c9[2].list.c.e[2] == 3
    assert conf.a4.b7.c9[2].list.c.e[3] == ["hello", "world"]
    assert conf.a5 == "True"
    assert conf.a6 == "$123"
    assert conf.a7 == os.environ["HOME"]
    assert conf.a8.b8[0] == conf.a1.b4.c5.d5
    assert conf.a8.b8[1] == conf.a1.b4.c5.d4.l1
    assert conf.a8.b8[2] == conf.a4.b7.c9[2].list.c.e[1][1][0]


def test_test1_var(test1_var_str):
    conf = parse(test1_var_str)
    assert conf.a1 == "hello"
    assert conf.a2.b1 == "world"
    assert conf.a3 == conf.a1
    assert conf.a4 == conf.a2.b1
    assert conf.a5.b1.c1[0] == "world"
    assert conf.a5.b1.c1[1] == os.environ["HOME"]
    assert conf.a5.b1.c1[2].b1 == "world"
    assert conf.a5.b1.c1[2].b2 == os.environ["HOME"]


def test_bad_indent(bad_indent_config: str) -> None:
    with pytest.raises(IndentationError) as exc_info:
        parse(bad_indent_config)
    assert "Error at line 7:" in str(exc_info.value)


# def test_parse_import_config(test_import_config: str) -> None:
#     conf = parse(test_import_config)
#     assert conf.a == "Hello from level 2 nested dir"
#     assert conf.b.c == "Hello from same dir"
#     assert conf.b.d == "Hello from level 1 nested dir"
