from pathlib import Path

import pytest


@pytest.fixture
def simple_config_str():
    return """
    training:
        name: MLConf
        epochs: 10
        batch_size: 32
        learning_rate: 0.001
    """


@pytest.fixture
def simple_config_dict_str():
    return {
        "training": {
            "name": "MLConf",
            "epochs": "10",
            "batch_size": "32",
            "learning_rate": "0.001",
        }
    }


@pytest.fixture
def config_dir():
    return Path(__file__).parent / "test_configs"


@pytest.fixture
def test1_config_str(config_dir):
    test1 = config_dir / "test1.conf"
    with open(test1) as f:
        test_1_str = f.read()
    return test_1_str


@pytest.fixture
def test1_var_str(config_dir):
    test1 = config_dir / "test_var.conf"
    with open(test1) as f:
        test_1_str = f.read()
    return test_1_str


@pytest.fixture
def test_import_config(config_dir):
    test1 = config_dir / "test_imports/test.conf"
    with open(test1) as f:
        test_1_str = f.read()
    return test_1_str


@pytest.fixture
def bad_indent_config(config_dir):
    test1 = config_dir / "test_bad_indent.conf"
    with open(test1) as f:
        test_1_str = f.read()
    return test_1_str
