from mlconf.config import Config
from mlconf.parser import parse


def test_parser(simple_config_str, simple_config_dict_str):
    conf = parse(simple_config_str)
    dict_conf = Config(simple_config_dict_str)
    assert conf.dict == dict_conf.dict


def test_test1_config(test1_config_str):
    conf = parse(test1_config_str)
    assert conf.a1.b1.c1 == "1"
    assert conf.a1.b1.c2 == "2"
    assert conf.a1.b2 == "2"
    assert conf.a1.b3 == "3"
    assert conf.a1.b4.c3 == "3"
    assert conf.a1.b4.c4 == "hello"
    assert conf.a1.b4.c5.d1 == "1"
    assert conf.a1.b4.c5.d2 == "2"
    assert conf.a1.b4.c5.d3.e1 == "world"
    assert conf.a1.b4.c5.d3.e2 == "2"
    assert conf.a1.b4.c5.d4 == "4"
    assert conf.a1.b4.c6 == "6"
    assert conf.a1.b4.c7 == "7"
    assert conf.a1.b5 == "5"
    assert conf.a1.b6 == "6"
    assert conf.a1.a2 == "2"
    assert conf.a1.a3 == "3"
