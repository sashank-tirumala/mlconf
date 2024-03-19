class MLConfig:
    def __init__(self, key=None, value=None):
        if key is not None and value is not None:
            setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        res_str = ""
        for attr, value in self.__dict__.items():
            res_str += f"{attr}: {value}\n"
        return res_str

    def __str__(self, indent=0):
        indent_str = "  " * indent
        res_str = ""
        for attr, value in self.__dict__.items():
            if isinstance(value, MLConfig):
                res_str += indent_str + f"{attr}:\n" + value.__str__(indent + 1)
            else:
                res_str += indent_str + f"{attr}: {value}\n"
        return res_str

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __len__(self):
        return len(self.__dict__)
