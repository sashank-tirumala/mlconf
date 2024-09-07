from mlconf.config import Config
from mlconf.parser import parse


def test_parser(simple_config_str, simple_config_dict_str):
    conf = parse(simple_config_str)
    dict_conf = Config(simple_config_dict_str)
    assert conf.dict == dict_conf.dict
