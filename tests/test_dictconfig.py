import pytest

from mlconf import Config


@pytest.fixture
def config():
    return {
        "training": {
            "name": "MLConf",
            "epochs": 10,
            "batch_size": 32,
            "learning_rate": 0.001,
        }
    }


def test_access_Config(config):
    config = Config(config)
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
    config1 = Config(config)
    config2 = Config(config)
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
    config1 = Config(config)
    config1.training.name = "MLConf2"
    assert config1.training.name == "MLConf2"
    config1["training"]["name"] = "MLConf3"
    assert config1["training"].name == "MLConf3"
    config1["training"] = {"name": "MLConf4"}
    assert config1.training.name == "MLConf4"
    config1.training["name2"] = "MLConf5"
    assert config1.training.name2 == "MLConf5"
    pytest.raises(AttributeError, config1.__setattr__, "abc", 123)
