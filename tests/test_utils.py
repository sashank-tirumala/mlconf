from pathlib import Path

from mlconf.utils import get_import_path_if_exists


def test_get_import_path_if_exists_yml(tmpdir):
    config_file = tmpdir / "config.yml"
    config_file.write("a: 1")
    assert get_import_path_if_exists("config", Path(tmpdir)) == Path(config_file)


def test_get_import_path_if_exists_yaml(tmpdir):
    config_file = tmpdir / "config.yaml"
    config_file.write("a: 1")
    assert get_import_path_if_exists("config", Path(tmpdir)) == Path(config_file)


def test_get_import_path_if_exists_mlconf(tmpdir):
    config_file = tmpdir / "config.mlconf"
    config_file.write("a: 1")
    assert get_import_path_if_exists("config", Path(tmpdir)) == Path(config_file)


def test_get_import_path_if_exists_no_file(tmpdir):
    config_file = tmpdir / "config.abc"
    config_file.write("a: 1")
    assert get_import_path_if_exists("config", Path(tmpdir)) == None


def test_get_import_path_if_exists_no_dir(tmpdir):
    assert get_import_path_if_exists("config", Path(tmpdir)) == None


def test_get_import_path_if_exists_abs_path(tmpdir):
    config_file = tmpdir / "config.yml"
    config_file.write("a: 1")
    assert get_import_path_if_exists(str(config_file), Path(tmpdir)) == Path(config_file)

    config_file = tmpdir / "config.yaml"
    config_file.write("a: 1")
    assert get_import_path_if_exists(str(config_file), Path(tmpdir)) == Path(config_file)

    config_file = tmpdir / "config.mlconf"
    config_file.write("a: 1")
    assert get_import_path_if_exists(str(config_file), Path(tmpdir)) == Path(config_file)

    config_file = tmpdir / "config.abc"
    config_file.write("a: 1")
    assert get_import_path_if_exists(str(config_file), Path(tmpdir)) == Path(config_file)

    assert get_import_path_if_exists("config.xyz", Path(tmpdir)) == None
