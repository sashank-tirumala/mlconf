from mlconf.extended_list_and_tuple import ExtendedList, ExtendedTuple


def test_extended_list():
    l1 = ExtendedList([1, 2, 3])
    assert l1[0] == l1.l0 == l1["l0"] == 1
    assert l1[1] == l1.l1 == l1["l1"] == 2
    assert l1[2] == l1.l2 == l1["l2"] == 3


def test_extended_tuple():
    t0 = ExtendedTuple((1, 2, 3))
    assert t0[0] == t0.t0 == t0["t0"] == 1
    assert t0[1] == t0.t1 == t0["t1"] == 2
    assert t0[2] == t0.t2 == t0["t2"] == 3
