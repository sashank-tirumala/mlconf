import re

from mlconf.regex_utils import REGEX_FLOAT_MATCH, REGEX_INT_MATCH


def test_regex_int_match():
    assert re.match(REGEX_INT_MATCH, "123")
    assert int("123") == 123
    assert re.match(REGEX_INT_MATCH, "-123")
    assert int("-123") == -123
    assert re.match(REGEX_INT_MATCH, "+123")
    assert int("+123") == 123
    assert re.match(REGEX_INT_MATCH, "012")
    assert int("012") == 12
    assert not re.match(REGEX_INT_MATCH, "123.0")
    assert not re.match(REGEX_INT_MATCH, "123.0.0")
    assert not re.match(REGEX_INT_MATCH, "1 1 1")


def test_regex_float_match():
    assert re.match(REGEX_FLOAT_MATCH, "123.0")
    assert float("123.0") == 123.0
    assert re.match(REGEX_FLOAT_MATCH, "-123.0")
    assert float("-123.0") == -123.0
    assert re.match(REGEX_FLOAT_MATCH, "+123.0")
    assert float("+123.0") == 123.0
    assert re.match(REGEX_FLOAT_MATCH, "01.01")
    assert float("01.01") == 1.01
    assert re.match(REGEX_FLOAT_MATCH, ".01")
    assert float(".01") == 0.01
    assert re.match(REGEX_FLOAT_MATCH, "01.")
    assert float("01.") == 1.0

    assert not re.match(REGEX_FLOAT_MATCH, "123.0.0")
    assert not re.match(REGEX_FLOAT_MATCH, "1 1 1")
