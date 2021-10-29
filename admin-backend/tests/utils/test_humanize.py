import pytest
from admin_backend.utils import humanize


def test_humanize_iterable():
    with pytest.raises(ValueError) as excinfo:
        humanize.humanize_iterable([])
    assert "must not be empty" in str(excinfo)

    humanize.humanize_iterable([], raise_if_is_empty=False)

    assert humanize.humanize_iterable(["a"]) == "a"
    assert humanize.humanize_iterable(["a", "b", "c", "d"]) == "a, b, c and d"
    assert humanize.humanize_iterable(
        (x for x in [0, 1, 2, 3]),
        conjunction="or",
        start_items_separator=" ... ",
        item_transformation=lambda x: 2**x,
        str_transformation=lambda s: bin(int(s))[2:]
    ) == "1 ... 10 ... 100 or 1000"


def test_humanize_iterable_with_quote():
    assert humanize.humanize_iterable(
        ("foo", "bar", "baz"),
        str_transformation=humanize.quote,
    ) == '"foo", "bar" and "baz"'


def test_humanize_iterable_with_quote_code():
    assert humanize.humanize_iterable(
        ("foo", "bar", "baz"),
        str_transformation=humanize.quote_code,
    ) == '`foo`, `bar` and `baz`'
