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
