from collections.abc import Iterable
from typing import TypeVar


T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E", bound=Exception)


def chunk_iter(it: Iterable[T], size: int) -> Iterable[list[T]]:
    chunk = []
    chunk_index = 0

    for item in it:
        chunk.append(item)

        chunk_index += 1
        if chunk_index >= size:
            yield chunk

            chunk = []
            chunk_index = 0

    if chunk:
        yield chunk


def flatten(it: Iterable[Iterable[T]]) -> Iterable[T]:
    for child_it in it:
        yield from child_it
