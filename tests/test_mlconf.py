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
        + 'string2: "test"\n'
        + 'string3: "test:12\n'
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


def assert_basic_config(parse):
    assert parse.string == "test"
    assert parse.string2 == "test"
    assert parse.string3 == "test:123"
    assert parse.string4 == "test"
    assert parse.string5 == "true"
    assert parse.float1 == 1.0
    assert parse.float2 == 1.0
    assert parse.float3 == 0.01
    assert parse.float4 == 0.01
    assert parse.float5 == 100.0
    assert parse.float6 == 100.0
    assert parse.float7 == 100.0
    assert parse.float8 == 100.0
    assert parse.bool1 == True
    assert parse.bool2 == False
    assert parse.bool3 == True
    assert parse.bool4 == False
    assert parse.random == None


def test_basic_parse(basic_config):
    print(basic_config)
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
            new_basic_config2 += " # comment\n"
        if ":" in line:
            split_colon = line.split(":")
            new_basic_config2 += split_colon[0] + " : " + split_colon[1] + "\n"
        counter += 1
    new_basic_config3 = ""
    counter = 0
    for line in basic_config.split("\n"):
        if counter == 0 or counter == 5 or counter == 7:
            new_basic_config3 += " #$$$$\n"
        if ":" in line:
            split_colon = line.split(":")
            new_basic_config3 += split_colon[0] + ": " + split_colon[1] + "\n"
        counter += 1
    assert_basic_config(mlconf.parse(new_basic_config1))
    assert_basic_config(mlconf.parse(new_basic_config2))


def test_version():
    assert __version__ == "0.1.0"
