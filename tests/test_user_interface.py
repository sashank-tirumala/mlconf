import subprocess
import sys

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


def cfg_test(
    cfg, a=1, b16=2, c_0d=True, d=None, e_b16=300.0, e_c_0d=400, e_d=False, e_e=None, e_f_f=5.0, e_f_g=-0.006, f=0.07
):
    assert cfg.a == a
    assert cfg.b16 == b16
    assert cfg.c_0d == c_0d
    assert cfg.d == d
    assert cfg.e.b16 == e_b16
    assert cfg.e.c_0d == e_c_0d
    assert cfg.e.d == e_d
    assert cfg.e.e == e_e
    assert cfg.e.f.f == e_f_f
    assert cfg.e.f.g == e_f_g
    assert cfg.f == f


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


def test_load_argparse(monkeypatch, config_file):
    test_args = ["program_name", f"--config", str(config_file)]
    monkeypatch.setattr(sys, "argv", test_args)
    cfg = mlconf.load_argparse()
    cfg_test(cfg)

    test_args = [
        "program_name",
        f"--config",
        str(config_file),
        "--a",
        "null",
        "--e.b16",
        "4e6",
        "--e.f.f",
        "True",
        "--f",
        "3.14",
    ]
    monkeypatch.setattr(sys, "argv", test_args)
    cfg = mlconf.load_argparse()
    cfg_test(cfg, a=None, e_b16=4000000.0, e_f_f=True, f=3.14)
