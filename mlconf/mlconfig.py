class MLConfig:
    def __init__(self, key=None, value=None):
        if key is not None and value is not None:
            setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self, indent=0):
        indent_str = "  " * indent
        res_str = ""
        for attr, value in self.__dict__.items():
            if isinstance(value, MLConfig):
                res_str += indent_str + f"{attr}:\n" + value.__str__(indent + 1)
            else:
                res_str += indent_str + f"{attr}: {value}\n"
        return res_str

    def __str__(self, indent=0, show_type=False):
        indent_str = "  " * indent
        res_str = ""
        for attr, value in self.__dict__.items():
            if isinstance(value, MLConfig):
                res_str += indent_str + f"{attr}:\n" + value.__str__(indent + 1)
            else:
                if show_type:
                    res_str += indent_str + f"{attr}: {value}({type(value)})\n"
                else:
                    res_str += indent_str + f"{attr}: {value}\n"
        return res_str

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        return iter(self.__dict__)

    def __cfgnamestr__(self, base_str=""):
        """
        Returns argparse style names for the configuration files
        """
        res_str = ""
        for attr, value in self.__dict__.items():
            # print(attr)
            if isinstance(value, MLConfig):
                res_str += value.__cfgnamestr__(f"{base_str}{attr}.")
            else:
                res_str += base_str + attr + "\n"
        return res_str

    def __cfgnamestrlist__(self):
        """
        Return a list of argparse style names for the configuration files
        """
        return self.__cfgnamestr__().split("\n")
