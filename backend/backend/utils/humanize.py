"""Utilities for expressing data in a human readable format."""
from dataclasses import dataclass
from typing import Callable
from typing import Iterable
from typing import Literal
from typing import TypeVar

from requests import get


T = TypeVar("T")


def humanize_iterable(
        items: Iterable[T],
        conjunction: Literal["and", "or"] = "and",
        start_items_separator: str = ", ",
        item_transformation: Callable[[T], str] | None = None,
        str_transformation: Callable[[str], str] | None = None,
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


@dataclass
class _ShortendTerm:
    original: str
    words: list[str]
    used_chars: list[str]
    used_chars_words_masks: list[list[bool]]

    def __init__(self, original: str, get_words: Callable[[str], Iterable[str]]) -> None:
        self.original = original
        self.words = list(get_words(original.lower()))
        self.used_chars = []
        self.used_chars_words_masks = [[False for _ in range(len(word))] for word in self.words]

    def get(self) -> str:
        return "".join(self.used_chars)

    def use_next_unused_char(self) -> str:
        return self.used_char(*self.find_next_unused_char())

    def used_char(self, word_index: int, char_index: int) -> str:
        self.used_chars_words_masks[word_index][char_index] = True

        char = self.words[word_index][char_index]

        self.used_chars.append(char)

        return char

    def find_next_unused_char(self) -> tuple[int, int]:
        char_index = 0
        while True:
            words_are_too_long = True

            for word_index in range(len(self.words)):
                try:
                    if not self.used_chars_words_masks[word_index][char_index]:
                        return word_index, char_index

                    words_are_too_long = False
                except IndexError:
                    pass

            if words_are_too_long:
                raise ValueError("Could not find unused char")

            char_index += 1


def get_shortend_to_originals(
    terms: Iterable[str],
    get_words: Callable[[str], Iterable[str]] | None = None,
) -> dict[str, str]:
    terms = list(terms)

    if get_words is None:
        get_words = _get_words

    shorted_terms = [_ShortendTerm(term, get_words=get_words) for term in terms]

    while True:
        for shortend_term in shorted_terms:
            shortend_term.use_next_unused_char()

        if len(set(shortend_term.get() for shortend_term in shorted_terms)) >= len(shorted_terms):
            return {shortend_term.get(): shortend_term.original for shortend_term in shorted_terms}


def _get_words(s: str) -> Iterable[str]:
    word_chars = []
    for char in s:
        if char.isalpha():
            word_chars.append(char)
        elif word_chars:
            yield "".join(word_chars)
            word_chars.clear()

    if word_chars:
        yield "".join(word_chars)
