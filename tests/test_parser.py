from pathlib import Path

import pytest

import mlconf
from mlconf import __version__


def test_basic_import():
    import mlconf

    assert mlconf.__version__ == __version__


@pytest.fixture
def basic_config():
    return (
        "string: 'test'\n"
        + "# comment\n"
        + "\n\n\n"
        + 'string2: "test"\n'
        + 'string3: "test:12"\n'
        + "string4: test\n"
        + 'string5: "true"\n'
        + "float1: 1\n"
        + "float2: 1.0\n"
        + "float3: 1e-2\n"
        + "float4: 1.0e-2\n"
        + "float5: 1.0e2\n"
        + "float6: 1.0e+2\n"
        + "float7: 1e+2\n"
        + "float8: 1e2\n"
        + "bool1: true\n"
        + "bool2: false\n"
        + "bool3: True\n"
        + "bool4: False\n"
        + "random: null\n"
    )


invalid_names = [
    # "name: value uef\n",
    "name: value+uef\n",
    "name: value-123\n",
    "name: value.887\n",
    "name.-886: value\n",
    # "name tr: value\n",
]


def assert_basic_config(parse):
    assert parse["string"] == "test"
    assert parse["string2"] == "test"
    assert parse["string3"] == "test:12"
    assert parse["string4"] == "test"
    assert parse["string5"] == "true"
    assert parse["float1"] == 1.0
    assert parse["float2"] == 1.0
    assert parse["float3"] == 0.01
    assert parse["float4"] == 0.01
    assert parse["float5"] == 100.0
    assert parse["float6"] == 100.0
    assert parse["float7"] == 100.0
    assert parse["float8"] == 100.0
    assert parse["bool1"] == True
    assert parse["bool2"] == False
    assert parse["bool3"] == True
    assert parse["bool4"] == False
    assert parse["random"] == None


def test_basic_parse(basic_config):
    parse = mlconf.parse(basic_config)
    assert_basic_config(parse)


def test_basic_parse_with_space_and_comment(basic_config):
    new_basic_config1 = ""
    counter = 0
    for line in basic_config.split("\n"):
        if counter == 0 or counter == 6 or counter == 12:
            new_basic_config1 += "\n"
        if counter == 0 or counter == 5 or counter == 10:
            new_basic_config1 += "# comment\n"
        new_basic_config1 += str(line) + "\n"
        counter += 1
    counter = 0
    new_basic_config2 = ""
    for line in basic_config.split("\n"):
        if counter == 0 or counter == 3 or counter == 9:
            new_basic_config2 += "   # comment\n"
        new_basic_config2 += str(line) + "\n"
        counter += 1
    new_basic_config2 + "  "
    assert_basic_config(mlconf.parse(new_basic_config1))
    assert_basic_config(mlconf.parse(new_basic_config2))


@pytest.mark.parametrize("invalid_name", invalid_names)
def test_invalid_names(invalid_name):
    with pytest.raises(SyntaxError):
        mlconf.parse(invalid_name)


def test_simple_indentation():
    config = (
        "abc: def\n"
        + "ghi:\n"
        + "  j_kl: mno\n"
        + "  p1q: null\n"
        + "  oio:\n"
        + "    r2s: 3.14\n"
        + "    why: true\n"
        + "  maybe: false\n"
        + "  hi: there\n"
        + "tef: -0.123\n"
        + "rock: solid\n"
    )
    parsed_config = mlconf.parse(config)
    assert parsed_config["abc"] == "def"
    assert parsed_config.abc == "def"

    assert parsed_config["ghi"]["j_kl"] == "mno"
    assert parsed_config.ghi.j_kl == "mno"

    assert parsed_config["ghi"]["p1q"] == None
    assert parsed_config.ghi.p1q == None

    assert parsed_config["ghi"]["oio"]["r2s"] == 3.14
    assert parsed_config.ghi.oio.r2s == 3.14

    assert parsed_config["ghi"]["oio"]["why"] == True
    assert parsed_config.ghi.oio.why == True

    assert parsed_config["ghi"]["maybe"] == False
    assert parsed_config.ghi.maybe == False

    assert parsed_config["ghi"]["hi"] == "there"
    assert parsed_config.ghi.hi == "there"

    assert parsed_config["tef"] == -0.123
    assert parsed_config.tef == -0.123

    assert parsed_config["rock"] == "solid"
    assert parsed_config.rock == "solid"

    assert len(parsed_config) == 4


def test_bug_config_repeat_nested(monkeypatch):
    """
    This test is to check if the parser can handle an input with repeated nested keys
    """
    monkeypatch.setenv("MLCONF_TEST", "test")
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
        + "    a: $MLCONF_TEST\n"
        + "    b: -6e-3\n"
        + "g: 0.07\n"
    )
    cfg = mlconf.parse(cfg_str)
    assert cfg.a == 1
    assert cfg.b == 2
    assert cfg.c == True
    assert cfg.d == None
    assert cfg.e.b == 300
    assert cfg.e.c == 400
    assert cfg.e.d == False
    assert cfg.e.e == None
    assert cfg.e.g.a == "test"
    assert cfg.e.g.b == -0.006
    assert cfg.g == 0.07
    assert len(cfg) == 6


def test_var_substitution(monkeypatch):
    """
    This test is to check if the parser can handle variable substitution
    """
    monkeypatch.setenv("HOME_DIR", "/home/user")
    monkeypatch.setenv("USER_NAME", "sash")
    monkeypatch.setenv("DATA_DIR", "data")
    cfg_str = (
        "home_dir: $HOME_DIR\n"
        + "user_name: $USER_NAME\n"
        + "nested:\n"
        + "  home_dir: $HOME_DIR\n"
        + "  $USER_NAME: sash\n"
        + "  $HOME_DIR: $USER_NAME\n"
        + "  nested:\n"
        + "    home_dir: ${HOME_DIR}/$USER_NAME\n"
        + "    ${HOME_DIR}/$USER_NAME: True\n"
        + "    ${HOME_DIR}/$USER_NAME/${DATA_DIR}: ${{user_name}}_${{nested.home_dir}}\n"
        + "  ${HOME_DIR}/${USER_NAME}/${DATA_DIR}: ${DATA_DIR}_$USER_NAME\n"
        + "  ${HOME_DIR}/$USER_NAME/data1: ${{ nested.home_dir }}\n"
        + "  ${HOME_DIR}/$USER_NAME/data2: ${{ nested.nested.home_dir }}\n"
    )
    cfg = mlconf.parse(cfg_str)
    assert cfg.home_dir == "/home/user"
    assert cfg.user_name == "sash"
    assert cfg.nested.home_dir == "/home/user"
    assert cfg.nested.sash == "sash"
    assert cfg.nested["/home/user"] == "sash"
    assert cfg.nested.nested.home_dir == "/home/user/sash"
    assert cfg.nested.nested["/home/user/sash"] == True
    assert cfg.nested.nested["/home/user/sash/data"] == "sash_/home/user"
    assert cfg.nested["/home/user/sash/data"] == "data_sash"
    assert cfg.nested["/home/user/sash/data1"] == "/home/user"
    assert cfg.nested["/home/user/sash/data2"] == "/home/user/sash"


def test_import_substitution(tmpdir, monkeypatch):
    monkeypatch.setenv("MLCONF_TEST", "test")
    import_config = tmpdir / "h1h2.mlconf"
    with open(import_config, "w") as f:
        f.write("a: 1\nb: 2\n")
    import_config2 = tmpdir / "h2h1.yml"
    with open(import_config2, "w") as f:
        f.write("c: test\na: None\n")
    cfg_str = (
        "import h1h2\n"
        "import h2h1\n"
        + "a: 1\n"
        + "b: 2\n"
        + "c: True\n"
        + "d: None\n"
        + "e:\n"
        + "  b: 3e+2\n"
        + "  c: +4e2\n"
        + "  d: ${{ h2h1.c }}\n"
        + "  e: ${{ h1h2.b }}\n"
        + "  g:\n"
        + "    a: $MLCONF_TEST\n"
        + "    b: -6e-3\n"
        + "g: ${{ h1h2.a }}\n"
    )
    cfg = mlconf.parse(cfg_str, base_path=Path(tmpdir))
    assert cfg.a == 1
    assert cfg.b == 2
    assert cfg.c == True
    assert cfg.d == None
    assert cfg.e.b == 300
    assert cfg.e.c == 400
    assert cfg.e.d == "test"
    assert cfg.e.e == 2.0
    assert cfg.e.g.a == "test"
    assert cfg.e.g.b == -0.006
    assert cfg.g == 1.0


def test_version():
    assert __version__ == "0.1.0"
