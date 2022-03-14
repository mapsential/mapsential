from enum import Enum
from typing import cast
from typing import TypeVar


T = TypeVar("T")


def get_values(enum_: Enum) -> list[T]:
    values = []
    for member in enum_.__members__.values():  # type: ignore[attr-defined]
        value = member.value

        if value not in values:
            values.append(value)

    return values
