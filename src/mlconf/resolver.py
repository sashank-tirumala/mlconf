import re
from abc import ABC, abstractmethod
from typing import Any, List, Tuple

from mlconf.config import Config
from mlconf.regex_utils import REGEX_FLOAT_MATCH, REGEX_INT_MATCH


class Resolver(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def resolve(self, value: str) -> Any:
        pass


class NumberResolver(Resolver):
    def resolve(self, value: str) -> Any:
        if isinstance(value, str):
            if re.match(REGEX_INT_MATCH, value):
                return int(value)
            elif re.match(REGEX_FLOAT_MATCH, value):
                return float(value)
            else:
                return value
        else:
            return value


def resolve(config: Config, resolvers: List[Resolver]) -> Any:
    for key, value in config.items():
        if isinstance(value, Config):
            resolve(value, resolvers)
        elif isinstance(value, List):
            config[key] = resolve_list(value, resolvers)
        elif isinstance(value, tuple):
            config[key] = resolve_tuple(value, resolvers)
        else:
            for resolver in resolvers:
                config.dict[key] = resolver.resolve(value)
    return config


def resolve_list(value: List[Any], resolvers: List[Resolver]) -> List[Any]:
    for i, item in enumerate(value):
        if isinstance(item, Config):
            resolve(item, resolvers)
        elif isinstance(item, List):
            value[i] = resolve_list(item, resolvers)
        elif isinstance(item, tuple):
            value[i] = resolve_tuple(item, resolvers)
        else:
            for resolver in resolvers:
                value[i] = resolver.resolve(item)
    return value


def resolve_tuple(value: Tuple[Any], resolvers: List[Resolver]) -> Tuple[Any]:
    value_list: List[Any] = list(value)
    for i, item in enumerate(value):
        if isinstance(item, Config):
            resolve(item, resolvers)
        elif isinstance(item, List):
            value_list[i] = resolve_list(item, resolvers)
        elif isinstance(item, tuple):
            value_list[i] = resolve_tuple(item, resolvers)
        else:
            for resolver in resolvers:
                value_list[i] = resolver.resolve(item)
    return tuple(value_list)
