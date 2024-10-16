from typing import Any, List, Tuple


class ExtendedList(List[Any]):
    def __getitem__(self, key: Any) -> Any:
        if isinstance(key, int):
            return super().__getitem__(key)
        elif isinstance(key, str):
            if key.startswith("l"):
                key = key[1:]
                if key.isdigit():
                    return super().__getitem__(int(key))
                else:
                    raise ValueError(f"Invalid key: {key}")
            else:
                raise ValueError(f"Invalid key: {key}")

    def __getattr__(self, name: str, /) -> Any:
        if name.startswith("l"):
            name = name[1:]
            if name.isdigit():
                return super().__getitem__(int(name))
            else:
                raise ValueError(f"Invalid key: {name}")
        else:
            return super().__getattribute__(name)

    def __contains__(self, key: object, /) -> bool:
        keys = [f"l{i}" for i in range(len(self))]
        return super().__contains__(key) or key in keys


class ExtendedTuple(Tuple[Any]):
    def __getitem__(self, key: Any) -> Any:
        if isinstance(key, int):
            return super().__getitem__(key)
        elif isinstance(key, str):
            if key.startswith("t"):
                key = key[1:]
                if key.isdigit():
                    return super().__getitem__(int(key))
                else:
                    raise ValueError(f"Invalid key: {key}")
            else:
                raise ValueError(f"Invalid key: {key}")

    def __getattr__(self, name: str, /) -> Any:
        if name.startswith("t"):
            name = name[1:]
            if name.isdigit():
                return super().__getitem__(int(name))
            else:
                raise ValueError(f"Invalid key: {name}")
        else:
            return super().__getattribute__(name)

    def __contains__(self, key: object, /) -> bool:
        keys = [f"t{i}" for i in range(len(self))]
        return super().__contains__(key) or key in keys
