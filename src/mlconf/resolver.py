import os
import re
from abc import ABC, abstractmethod
from typing import Any, List, Tuple

from mlconf.config import Config
from mlconf.regex_utils import REGEX_FLOAT_MATCH, REGEX_INT_MATCH
from mlconf.word import Word


class Resolver(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def resolve(self, value: Word) -> Any:
        raise NotImplementedError


class PythonDataTypeResolver(Resolver):
    def resolve(self, value: Word) -> Any:
        if isinstance(value, Word):
            if re.match(REGEX_INT_MATCH, value.text):
                return int(value.text)
            elif re.match(REGEX_FLOAT_MATCH, value.text):
                return float(value.text)
            elif value.text == "true" or value.text == "True":
                return True
            elif value.text == "false" or value.text == "False":
                return False
            elif value.text == "none" or value.text == "null" or value.text == "None":
                return None
            else:
                return value
        else:
            return value


class EnvironmentVariableResolver(Resolver):
    def resolve(self, value: Word) -> Any:
        if isinstance(value, Word):
            if value.text.startswith("$") and value.text[1:] in os.environ:
                return os.environ[value.text[1:]]
            else:
                return value
        else:
            return value


class StringResolver(Resolver):
    def resolve(self, value: Word) -> Any:
        if isinstance(value, Word):
            return str(value)
        else:
            return value


# class VariableResolver(Resolver):
#     def __init__(self, cfg: Config) -> None:
#         self.cfg = cfg
#         self.vars = []

#     def resolve(self, value: Word, var_path: str) -> Any:
#         self.vars.append(var_path)
#         if isinstance(value, Word):
#             if value.text in self.vars:
#                 self.cfg.get_item_from_dot_notation(var_path)
#         return value


class Resolvers:
    def __init__(self) -> None:
        self.python_datatype_resolver = PythonDataTypeResolver()
        self.environment_variable_resolver = EnvironmentVariableResolver()
        self.string_resolver = StringResolver()
        # self.variable_resolver = VariableResolver(cfg)

    def __iter__(self) -> Any:
        return iter(
            [
                self.python_datatype_resolver,
                self.environment_variable_resolver,
                self.string_resolver,
            ]
        )


def resolve(config: Config, resolvers: Resolvers) -> Any:
    for key, value in config.items():
        if isinstance(value, Config):
            resolve(value, resolvers)
        elif isinstance(value, List):
            config[key] = resolve_list(value, resolvers)
        elif isinstance(value, tuple):
            config[key] = resolve_tuple(value, resolvers)
        else:
            for resolver in resolvers:
                value = resolver.resolve(value)
            config[key] = value
    return config


def resolve_list(value: List[Any], resolvers: Resolvers) -> List[Any]:
    for i, item in enumerate(value):
        if isinstance(item, Config):
            resolve(item, resolvers)
        elif isinstance(item, List):
            value[i] = resolve_list(item, resolvers)
        elif isinstance(item, tuple):
            value[i] = resolve_tuple(item, resolvers)
        else:
            for resolver in resolvers:
                item = resolver.resolve(item)
            value[i] = item
    return value


def resolve_tuple(value: Tuple[Any], resolvers: Resolvers) -> Tuple[Any]:
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
                item = resolver.resolve(item)
            value_list[i] = item
    return tuple(value_list)
