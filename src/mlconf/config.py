import copy
from typing import Any, Dict, List, Tuple


class Config:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.__dict__["dict"] = {}
        for key, value in config.items():
            assert isinstance(key, str), "Key must be a string"
            self.__setitem__(key, value)

    def __getstate__(self) -> Dict[str, Any]:
        return {"dict": self.dict}

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self.__dict__["dict"] = state["dict"]

    def __getitem__(self, key: str) -> Any:
        return self.dict[key]

    def __getattr__(self, key: str) -> Any:
        return self.dict[key]

    def __setitem__(self, key: str, value: Any) -> None:
        if isinstance(value, Dict):
            self.dict[key] = Config(value)
        elif isinstance(value, List):
            value = list(value)
            value = self.resolve_list(value)
            self.dict[key] = value
        elif isinstance(value, tuple):
            value = list(value)
            value = self.resolve_tuple(value)
            self.dict[key] = value
        else:
            self.dict[key] = value

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
        return value

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
        return tuple(value_list)

    def __setattr__(self, key: str, value: Any) -> None:
        if key == "dict":
            self.__dict__["dict"] = value
        elif key not in self.dict:
            raise AttributeError(f"'Config' object has no attribute '{key}'")
        elif isinstance(value, Dict):
            self.dict[key] = Config(value)
        else:
            self.dict[key] = value

    def __eq__(self, other: Any) -> bool:
        for key, value in self.dict.items():
            if key not in other.dict or value != other.dict[key]:
                return False
        for key, value in other.dict.items():
            if key not in self.dict or value != self.dict[key]:
                return False
        return True

    def __repr__(self) -> str:
        return f"Config({self.dict})"

    def __str__(self) -> str:
        return str(self.dict)

    def __len__(self) -> int:
        return len(self.dict)

    def keys(self) -> List[Any]:
        return list(self.dict.keys())

    def items(self) -> Any:
        return self.dict.items()

    def __deepcopy__(self, memo: Dict[int, Any]) -> "Config":
        new_instance = Config({})
        new_instance.__dict__["dict"] = copy.deepcopy(self.dict, memo)
        return new_instance
