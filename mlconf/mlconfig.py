import logging


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

    def __eq__(self, other):
        if isinstance(other, MLConfig):
            return self.__dict__ == other.__dict__
        return False

    def get_leafnode_val(self, key):
        """
        Returns the leafnode of the key,
        A nested key can be accessed using a dot (.) separator (e.g. a.b.c)
        """
        cur_cfg = self
        attrs = key.split(".")
        while len(attrs) > 1:
            if not isinstance(cur_cfg, MLConfig) or attrs[0] not in cur_cfg.__dict__:
                logging.error(f"Key {key} not found in {cur_cfg}")
                return None
            cur_cfg = getattr(cur_cfg, attrs.pop(0))
        if type(cur_cfg) is not MLConfig:
            logging.error(f"Key {key} is not a leafnode in {cur_cfg}")
            return None
        else:
            if attrs[0] not in cur_cfg.__dict__:
                logging.error(f"Key {key} not found in {cur_cfg}")
                return None
            value = getattr(cur_cfg, attrs[0])
            if isinstance(value, MLConfig):
                logging.error(f"Key {key} is not a leafnode in {cur_cfg}")
                return None
            return value

    @property
    def children(self):
        return list(self.__dict__.keys())

    @property
    def names_children_dict(self):
        cfg_name_str_list = self.__cfgnamestrlist__()
        for name in cfg_name_str_list:
            val = self.get_leafnode(name)
            if val is not None:
                self.leafnode_repr_list.append((name, val))
            else:
                logging.error(f"Key {name} not found in {self}, skipping")
