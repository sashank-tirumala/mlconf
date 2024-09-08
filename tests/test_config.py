from copy import deepcopy as copy

import pytest

from mlconf import Config


@pytest.fixture
def config():
    return Config(
        {
            "training": {
                "name": "MLConf",
                "epochs": 10,
                "batch_size": 32,
                "learning_rate": 0.001,
            }
        }
    )


def test_access_Config(config):
    assert config.training.name == "MLConf"
    assert config.training.epochs == 10
    assert config.training.batch_size == 32
    assert config.training.learning_rate == 0.001
    assert config["training"]["name"] == "MLConf"
    assert config["training"]["epochs"] == 10
    assert config["training"]["batch_size"] == 32
    assert config["training"]["learning_rate"] == 0.001
    assert config["training"].name == "MLConf"
    assert config["training"].epochs == 10
    assert config["training"].batch_size == 32
    assert config["training"].learning_rate == 0.001
    assert config["training"] == Config(
        {"name": "MLConf", "epochs": 10, "batch_size": 32, "learning_rate": 0.001}
    )
    assert config.training["name"] == "MLConf"
    assert config.training["epochs"] == 10
    assert config.training["batch_size"] == 32
    assert config.training["learning_rate"] == 0.001


def test_equals(config):
    config1 = copy(config)
    config2 = copy(config)
    assert config1 == config2
    config2.training.name = "MLConf2"
    assert config1 != config2
    config2.training.name = "MLConf"
    config1["abc"] = 123
    assert config1 != config2
    config2["abc"] = 123
    assert config1 == config2
    config1["def"] = 456
    assert config1 != config2


def test_modify_Config(config):
    config.training.name = "MLConf2"
    assert config.training.name == "MLConf2"
    config["training"]["name"] = "MLConf3"
    assert config["training"].name == "MLConf3"
    config["training"] = {"name": "MLConf4"}
    assert config.training.name == "MLConf4"
    config.training["name2"] = "MLConf5"
    assert config.training.name2 == "MLConf5"
    pytest.raises(AttributeError, config.__setattr__, "abc", 123)


def test_keys(config):
    assert list(config.keys()) == ["training"]
    assert list(config.training.keys()) == [
        "name",
        "epochs",
        "batch_size",
        "learning_rate",
    ]


def test_items(config):
    config = Config(config)
    assert list(config.items()) == [
        (
            "training",
            Config(
                {
                    "name": "MLConf",
                    "epochs": 10,
                    "batch_size": 32,
                    "learning_rate": 0.001,
                }
            ),
        )
    ]
    assert list(config.training.items()) == [
        ("name", "MLConf"),
        ("epochs", 10),
        ("batch_size", 32),
        ("learning_rate", 0.001),
    ]


def test_lists(config):
    config = Config(config)
    config["list"] = [1, 2, 3]
    assert config.list == [1, 2, 3]

    config["list"] = [1, {"a": 1}, 2]
    assert config.list == [1, Config({"a": 1}), 2]

    config["list"] = [1, [1, 2], 2]
    assert config.list == [1, [1, 2], 2]

    config["list"] = [1, [1, {"a": [1, 2, {"b": 3}]}, 2]]
    assert config.list == [1, [1, Config({"a": [1, 2, Config({"b": 3})]}), 2]]


def test_tuples(config):
    config = Config(config)
    config["tuple"] = (1, 2, 3)
    assert config.tuple == (1, 2, 3)

    config["tuple"] = (1, {"a": 1}, 2)
    assert config.tuple == (1, Config({"a": 1}), 2)

    config["tuple"] = (1, [1, 2], 2)
    assert config.tuple == (1, [1, 2], 2)

    config["tuple"] = (1, [1, {"a": [1, 2, {"b": 3}]}, 2])
    assert config.tuple == (1, [1, Config({"a": [1, 2, Config({"b": 3})]}), 2])


def test_len(config):
    config = Config(config)
    assert len(config) == 1
