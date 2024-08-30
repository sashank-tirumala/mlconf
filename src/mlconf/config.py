from typing import Any, Dict, List


class Config:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.__dict__["dict"] = {}
        for key, value in config.items():
            assert isinstance(key, str), "Key must be a string"
            if isinstance(value, dict):
                self.__setitem__(key, Config(value))
            else:
                self.__setitem__(key, value)

    def __getitem__(self, key: str) -> Any:
        return self.dict[key]

    def __getattr__(self, key: str) -> Any:
        return self.dict[key]

    def __setitem__(self, key: str, value: Any) -> None:
        if isinstance(value, dict):
            self.dict[key] = Config(value)
        else:
            self.dict[key] = value

    def __setattr__(self, key: str, value: Any) -> None:
        if key not in self.dict:
            raise AttributeError(f"'Config' object has no attribute '{key}'")
        if isinstance(value, dict):
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

    def keys(self) -> List[Any]:
        return list(self.dict.keys())

    def items(self) -> Any:
        return self.dict.items()
