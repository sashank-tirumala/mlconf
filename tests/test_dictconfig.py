from mlconf import DictConfig


def test_dictconfig():
    config = {
        "training": {
            "epochs": 10,
            "batch_size": 32,
            "learning_rate": 0.001,
        }
    }
    config = DictConfig(config)
    assert config.training.epochs == 10
    assert config.training.batch_size == 32
    assert config.training.learning_rate == 0.001
    assert config["training"]["epochs"] == 10
    assert config["training"]["batch_size"] == 32
    assert config["training"]["learning_rate"] == 0.001
    assert config["training"].epochs == 10
    assert config["training"].batch_size == 32
    assert config["training"].learning_rate == 0.001
    assert config["training"] == DictConfig(
        {"epochs": 10, "batch_size": 32, "learning_rate": 0.001}
    )
