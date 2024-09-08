import re
from abc import ABC, abstractmethod

from mlconf.config import Config
from mlconf.regex_utils import REGEX_FLOAT_MATCH, REGEX_INT_MATCH


class Resolver(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def resolve(self, config: Config) -> Config:
        pass


class NumberResolver(Resolver):
    def resolve(self, config: Config) -> Config:
        for key, value in config.items():
            if isinstance(value, str):
                if re.match(REGEX_INT_MATCH, value):
                    config[key] = int(value)
                elif re.match(REGEX_FLOAT_MATCH, value):
                    config[key] = float(value)
        return config
