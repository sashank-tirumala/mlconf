from pathlib import Path

from mlconf.parser import parse
from mlconf.utils import get_import_path_if_exists, get_var_stack


def test_get_import_path_if_exists_yml(tmpdir):
    config_file = tmpdir / "config.yml"
    config_file.write("a: 1")
    assert get_import_path_if_exists("config", Path(tmpdir)) == Path(config_file)


def test_get_import_path_if_exists_yaml(tmpdir):
    config_file = tmpdir / "config.yaml"
    config_file.write("a: 1")
    assert get_import_path_if_exists("config", Path(tmpdir)) == Path(config_file)


def test_get_import_path_if_exists_mlconf(tmpdir):
    config_file = tmpdir / "config.mlconf"
    config_file.write("a: 1")
    assert get_import_path_if_exists("config", Path(tmpdir)) == Path(config_file)


def test_get_import_path_if_exists_no_file(tmpdir):
    config_file = tmpdir / "config.abc"
    config_file.write("a: 1")
    assert get_import_path_if_exists("config", Path(tmpdir)) == None


def test_get_import_path_if_exists_no_dir(tmpdir):
    assert get_import_path_if_exists("config", Path(tmpdir)) == None


def test_get_import_path_if_exists_abs_path(tmpdir):
    config_file = tmpdir / "config.yml"
    config_file.write("a: 1")
    assert get_import_path_if_exists(str(config_file), Path(tmpdir)) == Path(config_file)

    config_file = tmpdir / "config.yaml"
    config_file.write("a: 1")
    assert get_import_path_if_exists(str(config_file), Path(tmpdir)) == Path(config_file)

    config_file = tmpdir / "config.mlconf"
    config_file.write("a: 1")
    assert get_import_path_if_exists(str(config_file), Path(tmpdir)) == Path(config_file)

    config_file = tmpdir / "config.abc"
    config_file.write("a: 1")
    assert get_import_path_if_exists(str(config_file), Path(tmpdir)) == Path(config_file)

    assert get_import_path_if_exists("config.xyz", Path(tmpdir)) == None


def test_get_var_stack():
    cfg_str = (
        "a: 1\n"
        + "b: 2\n"
        + "c: True\n"
        + "d: None\n"
        + "e:\n"
        + "  b: 3e+2\n"
        + "  c: +4e2\n"
        + "  d: False\n"
        + "  e: null\n"
        + "  g:\n"
        + "    h: 1\n"
        + "    i: 2\n"
        + "    j: True\n"
        + "    k: None\n"
        + "    l:\n"
        + "      m: 3e+2\n"
        + "      n: +4e2\n"
        + "      o: False\n"
        + "      p: null\n"
    )
    cfg = parse(cfg_str)
    var_stack = get_var_stack(cfg)
    assert var_stack == {
        ".a": 1,
        ".b": 2,
        ".c": True,
        ".d": None,
        ".e.b": 3e2,
        ".e.c": 4e2,
        ".e.d": False,
        ".e.e": None,
        ".e.g.h": 1,
        ".e.g.i": 2,
        ".e.g.j": True,
        ".e.g.k": None,
        ".e.g.l.m": 3e2,
        ".e.g.l.n": 4e2,
        ".e.g.l.o": False,
        ".e.g.l.p": None,
    }

    var_stack = get_var_stack(cfg, "h1l1")
    assert var_stack == {
        "h1l1.a": 1,
        "h1l1.b": 2,
        "h1l1.c": True,
        "h1l1.d": None,
        "h1l1.e.b": 3e2,
        "h1l1.e.c": 4e2,
        "h1l1.e.d": False,
        "h1l1.e.e": None,
        "h1l1.e.g.h": 1,
        "h1l1.e.g.i": 2,
        "h1l1.e.g.j": True,
        "h1l1.e.g.k": None,
        "h1l1.e.g.l.m": 3e2,
        "h1l1.e.g.l.n": 4e2,
        "h1l1.e.g.l.o": False,
        "h1l1.e.g.l.p": None,
    }
