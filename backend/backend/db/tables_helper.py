from typing import Iterable
from typing import Optional

from piccolo.columns import Column


def column_attrs(cls, include_inherited: bool = True) -> Iterable[str]:
    for class_attr in class_attrs(cls, include_inherited=include_inherited):
        attr_val = getattr(cls, class_attr)

        if isinstance(attr_val, Column):
            yield class_attr


def class_attrs(
        cls,
        include_inherited: bool = True,
        exclude_attrs_with_prefixes: Optional[Iterable[str]] = None,
) -> Iterable[str]:
    if exclude_attrs_with_prefixes is None:
        # Exclude dunder methods by default.
        # This also prevents inconsistent behaviour when 'include_parent_attrs' is changed.
        exclude_attrs_with_prefixes = {"__"}

    if include_inherited:
        attrs = dir(cls)
    else:
        attrs = [attr for attr in cls.__dict__.keys() if not is_inherited_attr(cls, attr)]

    for class_attr in attrs:
        if not starts_with_a_prefix(class_attr, prefixes=exclude_attrs_with_prefixes):
            yield class_attr


def is_inherited_attr(cls, attr_name) -> bool:
    attr_val = getattr(cls, attr_name)
    for base in cls.__mro__:
        if hasattr(base, attr_name) and attr_val is getattr(base, attr_name):
            return True

    return False


def starts_with_a_prefix(s: str, prefixes: Iterable[str]) -> bool:
    for prefix in prefixes:
        if s.startswith(prefix):
            return True
    return False
