from pathlib import Path


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
