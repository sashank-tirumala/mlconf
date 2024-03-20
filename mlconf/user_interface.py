import argparse
from pathlib import Path

from mlconf.mlconfig import MLConfig
from mlconf.parser import parse, parse_cli_input


def load(file: str) -> MLConfig:
    with open(file, "r") as f:
        return parse(f.read())


def loads(string: str) -> MLConfig:
    return parse(string)


def dump(config: MLConfig, file: str, write_mode: str = "w"):
    with open(file, write_mode) as f:
        f.write(str(config))


def dumps(config: MLConfig) -> str:
    return str(config)


def load_argparse(config_arg: str = "config"):
    # TODO: add cli support for negative numbers
    parser = argparse.ArgumentParser()
    parser.add_argument(f"--{config_arg}", type=Path, default=Path("abc"), help="Path to the configuration file")
    args = parser.parse_known_args()
    if getattr(args[0], config_arg) == Path("abc"):
        raise ValueError(f"Please specify a config file using the --{config_arg} flag")
    if not getattr(args[0], config_arg).exists():
        raise FileNotFoundError(f"Config file --{getattr(args[0], config_arg)} not found")
    cfg = load(getattr(args[0], config_arg))
    for name in cfg.__cfgnamestrlist__():
        parser.add_argument(f"--{name}", type=str, default=None, help=f"config param: {name}", dest=name)
    args = parser.parse_args()
    for attr, value in args.__dict__.items():
        if attr != config_arg and value is not None:
            cur_cfg = cfg
            attrs = attr.split(".")
            while len(attrs) > 1:
                cur_cfg = getattr(cur_cfg, attrs.pop(0))
            setattr(cur_cfg, attrs[0], parse_cli_input(value))
    return cfg


if __name__ == "__main__":
    load_argparse()
