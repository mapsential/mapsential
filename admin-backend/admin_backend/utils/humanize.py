"""Utilities for expressing data in a human readable format."""
from typing import Callable
from typing import cast
from typing import Iterable
from typing import Literal
from typing import Optional
from typing import TypeVar


T = TypeVar("T")


def humanize_iterable(
        items: Iterable[T],
        conjunction: Literal["and", "or"] = "and",
        start_items_separator: str = ", ",
        item_transformation: Optional[Callable[[T], str]] = None,
        str_transformation: Optional[Callable[[str], str]] = None,
        raise_if_is_empty: bool = True,
) -> str:
    def to_str(item) -> str:
        if item_transformation is None:
            return str(item)

        return str(item_transformation(item))

    def to_str_and_post_process(item) -> str:
        if str_transformation is None:
            return to_str(item)

        return str_transformation(to_str(item))

    try:
        *start_items_strings, last_item_string = [to_str_and_post_process(item) for item in items]
    except ValueError as err:
        if raise_if_is_empty:
            raise ValueError("Iterable must not be empty") from err

        return ""

    if len(start_items_strings) == 0:
        return last_item_string

    return f"{start_items_separator.join(start_items_strings)} {conjunction} {last_item_string}"


def quote_code(s: str) -> str:
    return quote(s, quote_char="`")


def quote(s: str, quote_char: Literal["\"", "'", "`"] = "\"") -> str:
    return f"{quote_char}{s}{quote_char}"
