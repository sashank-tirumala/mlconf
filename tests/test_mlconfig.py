from mlconf.mlconfig import MLConfig


def test_mlconfig_str():
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
    assert (
        str(cfg)
        == "a: 1\nb: 2\nc: True\nd: None\ne:\n  f: 3\n  g: 4\n  h: False\n  i: None\n  j:\n    k: 5\n    l: 6\nf: 0.07\n"
    )
    cfg_names = cfg.__cfgnamestr__()
    assert cfg_names == "a\nb\nc\nd\ne.f\ne.g\ne.h\ne.i\ne.j.k\ne.j.l\nf\n"
