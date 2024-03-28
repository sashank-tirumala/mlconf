import pytest

from mlconf.mlconfig import MLConfig


@pytest.fixture
def basic_config():
    cfg = MLConfig()
    cfg["a"] = 1
    cfg["b"] = "2"
    cfg["c"] = True
    cfg["d"] = None
    cfg["e"] = MLConfig()
    cfg["e"]["f"] = 3
    cfg["e"]["g"] = "4"
    cfg["e"]["h"] = False
    cfg["e"]["i"] = None
    cfg["e"]["j"] = MLConfig()
    cfg["e"]["j"]["k"] = 5
    cfg["e"]["j"]["l"] = "6"
    cfg["f"] = +7e-2
    return cfg


def test_mlconfig_str(basic_config):
    cfg = basic_config
    assert (
        str(cfg)
        == "a: 1\nb: 2\nc: True\nd: None\ne:\n  f: 3\n  g: 4\n  h: False\n  i: None\n  j:\n    k: 5\n    l: 6\nf: 0.07\n"
    )
    cfg_names = cfg.__cfgnamestr__()
    assert cfg_names == "a\nb\nc\nd\ne.f\ne.g\ne.h\ne.i\ne.j.k\ne.j.l\nf\n"
    assert len(cfg) == 6


def test_children(basic_config):
    cfg = basic_config
    assert cfg.children == ["a", "b", "c", "d", "e", "f"]
    assert cfg["e"].children == ["f", "g", "h", "i", "j"]
    assert cfg["e"]["j"].children == ["k", "l"]


def test_get_leafnode_val(basic_config):
    cfg = basic_config
    assert cfg.get_leafnode_val("e.j.k") == 5
    assert cfg.get_leafnode_val("e.j.l") == "6"
    assert cfg.get_leafnode_val("e.j.m") is None
    assert cfg.get_leafnode_val("e.j") is None
    assert cfg.get_leafnode_val("e.j.k.l") is None
    assert cfg.get_leafnode_val("e.j.k.l.m.n.o") is None
    assert cfg.get_leafnode_val("a.b.c.d.e") is None
    assert cfg.get_leafnode_val("f") == 0.07
    assert cfg.get_leafnode_val("b") == "2"
    assert cfg.get_leafnode_val("c") == True
    assert cfg.get_leafnode_val("d") == None


def test_leafnode_name_value_list(basic_config):
    cfg = basic_config
    assert cfg.leafnode_name_value_list == [
        ("a", 1),
        ("b", "2"),
        ("c", True),
        ("d", None),
        ("e.f", 3),
        ("e.g", "4"),
        ("e.h", False),
        ("e.i", None),
        ("e.j.k", 5),
        ("e.j.l", "6"),
        ("f", 0.07),
    ]
