import os
import re
from abc import ABC, abstractmethod
from typing import Any, List, Set, Tuple

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


class VariableResolver:
    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg
        self.vars: Set[str] = set()

    def resolve(self, value: Word, var_path: str) -> Any:
        self.vars.add(var_path)
        if isinstance(value, Word):
            if value.text in self.vars:
                return self.cfg.get_item_from_dot_notation(value.text)
        return value


class Resolvers:
    def __init__(self, cfg: Config) -> None:
        self.python_datatype_resolver = PythonDataTypeResolver()
        self.environment_variable_resolver = EnvironmentVariableResolver()
        self.variable_resolver = VariableResolver(cfg)
        self.string_resolver = StringResolver()

    def resolve(self, value: Any, var_path: str = "") -> Any:
        value = self.python_datatype_resolver.resolve(value)
        value = self.environment_variable_resolver.resolve(value)
        value = self.variable_resolver.resolve(value, var_path)
        value = self.string_resolver.resolve(value)
        return value

    def update_vars(self, prefix: str) -> None:
        self.variable_resolver.vars.add(prefix)


def resolve(config: Config, resolvers: Resolvers, prefix: str = "") -> Any:
    for key, value in config.items():
        if isinstance(value, Config):
            resolve(value, resolvers, prefix + key + ".")
        elif isinstance(value, List):
            config[key] = resolve_list(value, resolvers, prefix + key + ".")
        elif isinstance(value, tuple):
            config[key] = resolve_tuple(value, resolvers, prefix + key + ".")
        else:
            value = resolvers.resolve(value, prefix + key)
            config[key] = value
    resolvers.update_vars(prefix[:-1])
    return config


def resolve_list(value: List[Any], resolvers: Resolvers, prefix: str = "") -> List[Any]:
    for i, item in enumerate(value):
        if isinstance(item, Config):
            resolve(item, resolvers, prefix + str(i) + ".")
        elif isinstance(item, List):
            value[i] = resolve_list(item, resolvers, prefix + str(i) + ".")
        elif isinstance(item, tuple):
            value[i] = resolve_tuple(item, resolvers, prefix + str(i) + ".")
        else:
            item = resolvers.resolve(item, prefix + str(i))
            value[i] = item
    resolvers.update_vars(prefix[:-1])
    return value


def resolve_tuple(
    value: Tuple[Any], resolvers: Resolvers, prefix: str = ""
) -> Tuple[Any]:
    value_list: List[Any] = list(value)
    for i, item in enumerate(value):
        if isinstance(item, Config):
            resolve(item, resolvers, prefix + str(i) + ".")
        elif isinstance(item, List):
            value_list[i] = resolve_list(item, resolvers, prefix + str(i) + ".")
        elif isinstance(item, tuple):
            value_list[i] = resolve_tuple(item, resolvers, prefix + str(i) + ".")
        else:
            item = resolvers.resolve(item, prefix + str(i))
            value_list[i] = item
    resolvers.update_vars(prefix)
    return tuple(value_list)
