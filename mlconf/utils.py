from pathlib import Path

from mlconf.mlconfig import MLConfig


def get_import_path_if_exists(path_str, base_path):
    path_strs = []
    if "." in path_str:
        path_strs = [path_str]
    else:
        path_strs.append(path_str + ".mlconf")
        path_strs.append(path_str + ".yml")
        path_strs.append(path_str + ".yaml")
    for path_str in path_strs:
        rel_path = base_path / path_str
        if rel_path.exists():
            return rel_path
    for path_str in path_strs:
        abs_path = Path(path_str)
        if abs_path.exists():
            return abs_path
    return None


def get_var_stack(config: MLConfig, cfg_name=""):
    leafnode_name_value_list = config.leafnode_name_value_list
    var_stack = {}
    for name, value in leafnode_name_value_list:
        var_stack[cfg_name + "." + name] = value
    return var_stack


def merge_dicts(dict1, dict2):
    try:
        merged_dict = dict1.copy()
        merged_dict.update(dict2)
        return merged_dict
    except Exception as e:
        return None
