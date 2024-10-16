import copy
from typing import Any, Dict, List, Tuple

from mlconf.extended_list_and_tuple import ExtendedList, ExtendedTuple


class Config:
    def __init__(self, config: Dict[str, Any]) -> None:
        self._config: Dict[str, Any] = {}
        for key, value in config.items():
            assert isinstance(key, str), "Key must be a string"
            self.__setitem__(key, value)

    def __getitem__(self, key: str) -> Any:
        return self._config[key]

    def __getattr__(self, key: str) -> Any:
        return self._config[key]

    def __setitem__(self, key: str, value: Any) -> None:
        if isinstance(value, Dict):
            self._config[key] = Config(value)
        elif isinstance(value, List):
            value = list(value)
            value = self.resolve_list(value)
            self._config[key] = value
        elif isinstance(value, tuple):
            value = list(value)
            value = self.resolve_tuple(value)
            self._config[key] = value
        else:
            self._config[key] = value

    def resolve_list(self, value: List[Any]) -> List[Any]:
        for i, item in enumerate(value):
            if isinstance(item, Dict):
                value[i] = Config(item)
            elif isinstance(item, List):
                value[i] = self.resolve_list(item)
            elif isinstance(item, tuple):
                value[i] = self.resolve_tuple(item)
            else:
                value[i] = item
        return ExtendedList(value)

    def resolve_tuple(self, value: Tuple[Any]) -> Tuple[Any]:
        value_list: List[Any] = list(value)
        for i, item in enumerate(value):
            if isinstance(item, Dict):
                value_list[i] = Config(item)
            elif isinstance(item, List):
                value_list[i] = self.resolve_list(item)
            elif isinstance(item, tuple):
                value_list[i] = self.resolve_tuple(item)
            else:
                value_list[i] = item
        return ExtendedTuple(value_list)

    def __setattr__(self, key: str, value: Any) -> None:
        if key == "_config":
            self.__dict__["_config"] = value
        elif key not in self._config:
            raise AttributeError(f"'Config' object has no attribute '{key}'")
        elif isinstance(value, Dict):
            self._config[key] = Config(value)
        else:
            self._config[key] = value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Config):
            return False
        for key, value in self._config.items():
            if key not in other._config or value != other._config[key]:
                return False
        for key, value in other._config.items():
            if key not in self._config or value != self._config[key]:
                return False
        return True

    def __repr__(self) -> str:
        return f"Config({self._config})"

    def __str__(self) -> str:
        return str(self._config)

    def __len__(self) -> int:
        return len(self._config)

    def keys(self) -> List[Any]:
        return list(self._config.keys())

    def items(self) -> Any:
        return self._config.items()

    def __contains__(self, key: str) -> bool:
        return key in self._config

    def __deepcopy__(self, memo: Dict[int, Any]) -> "Config":
        new_instance = Config({})
        new_instance.__dict__["_config"] = copy.deepcopy(self._config, memo)
        return new_instance

    def get_item_from_dot_notation(self, item: str) -> Any:
        keys = item.split(".")
        value = self._config
        for key in keys:
            if key not in value:
                raise KeyError(f"'{item}' not found in config")
            value = value[key]
        return value
