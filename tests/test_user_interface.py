import pytest

import mlconf


@pytest.fixture()
def config_file(tmp_path, config_str):
    with open(tmp_path / "test_config.yaml", "w") as f:
        f.write(config_str)
    return tmp_path / "test_config.yaml"


@pytest.fixture()
def config_str():
    return (
        "a: 1\n"
        + "b16: 2\n"
        + "c_0d: True\n"
        + "d: None\n"
        + "e:\n"
        + "  b16: 3e+2\n"
        + "  c_0d: +4e2\n"
        + "  d: False\n"
        + "  e: null\n"
        + "  f:\n"
        + "    f: 5.0\n"
        + "    g: -6e-3\n"
        + "f: 0.07\n"
    )


def cfg_test(cfg):
    assert cfg.a == 1
    assert cfg.b16 == 2
    assert cfg.c_0d == True
    assert cfg.d == None
    assert cfg.e.b16 == 300.0
    assert cfg.e.c_0d == 400.0
    assert cfg.e.d == False
    assert cfg.e.e == None
    assert cfg.e.f.f == 5
    assert cfg.e.f.g == -0.006
    assert cfg.f == 0.07


def test_load(config_file):
    cfg = mlconf.load(config_file)
    cfg_test(cfg)


def test_loads(config_str):
    cfg = mlconf.loads(config_str)
    cfg_test(cfg)


def test_dump(tmp_path, config_str):
    config_file = tmp_path / "test_out_onfig.yaml"
    cfg = mlconf.loads(config_str)
    mlconf.dump(cfg, config_file)
    cfg2 = mlconf.load(config_file)
    assert cfg == cfg2


def test_dumps(config_str):
    cfg = mlconf.loads(config_str)
    cfg2 = mlconf.loads(mlconf.dumps(cfg))
    assert cfg == cfg2
