import argparse
from pathlib import Path

from mlconf.mlconfig import MLConfig
from mlconf.parser import parse


def load(file: str) -> MLConfig:
    with open(file, "r") as f:
        return parse(f.read())


def loads(string: str) -> MLConfig:
    return parse(string)


def dump(config: MLConfig, file: str, write_mode: str = "w"):
    with open(file, write_mode) as f:
        f.write(config)


def dumps(config: MLConfig) -> str:
    return str(config)


def load_argparse(config_arg: str = "config"):
    parser = argparse.ArgumentParser()
    parser.add_argument(f"--{config_arg}", type=Path, default=Path("abc"), help="Path to the configuration file")
    parser.add_argument("--other", type=str, default="def", help="Other argument")
    args = parser.parse_known_args()
    if getattr(args[0], config_arg) == Path("abc"):
        raise ValueError(f"Please specify a config file using the --{config_arg} flag")
    if not getattr(args[0], config_arg).exists():
        raise FileNotFoundError(f"Config file --{getattr(args[0], config_arg)} not found")
    cfg = load(getattr(args[0], config_arg))
    import pdb

    pdb.set_trace()


if __name__ == "__main__":
    load_argparse()
