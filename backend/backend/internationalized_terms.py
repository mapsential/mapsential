import functools
from functools import cache
from typing import Any
from typing import Callable
from typing import cast
from typing import Literal
from typing import NamedTuple
from typing import ParamSpec
from typing import TypedDict

from errors import InternationalizedTermError


P = ParamSpec("P")  # Function parameters


class TermInfo(NamedTuple):
    country_code: str
    grammatical_number: "GrammaticalNumber"
    entry: "TermsEntry"


GrammaticalNumber = Literal["sg", "pl"]


TermEntryKey = Literal["en_sg", "en_pl", "de_sg", "de_pl"]


class TermsEntry(TypedDict):
    en_sg: str
    en_pl: str
    de_sg: str
    de_pl: str


# TODO: switch to gettext
TERMS: list[TermsEntry] = [
    {"en_sg": "defibrillator", "en_pl": "defibrillators", "de_sg": "Defibrillator", "de_pl": "Defibrillatoren"},
    {"en_sg": "drinking fountain", "en_pl": "drinking fountains", "de_sg": "Trinkbrunnen", "de_pl": "Trinkbrunnen"},
    {"en_sg": "soup kitchen", "en_pl": "soup kitchens", "de_sg": "Tafel", "de_pl": "Tafeln"},
    {"en_sg": "toilet", "en_pl": "toilets", "de_sg": "Toilette", "de_pl": "Toiletten"},
]


def term_operation_with_fallback(
    func: Callable[..., str]
) -> Callable[..., str]:
    @functools.wraps(func)
    def wrapper(term: str, *args: Any, fallback: str | None = None, **kwargs: Any) -> str:
        try:
            return func(term, *args, **kwargs)
        except InternationalizedTermError as err:
            if fallback is None:
                raise err

            return fallback

    return wrapper


@term_operation_with_fallback
def get_translation(term: str, translation_country_code: str) -> str:
    info = find_term_info(term)
    key = cast(TermEntryKey, f"{translation_country_code.lower()}_{info.grammatical_number}")
    return info.entry[key]


@term_operation_with_fallback
def get_plural(term: str) -> str:
    return _get_singular_or_plural(term, "pl")


@term_operation_with_fallback
def get_singular(term: str) -> str:
    return _get_singular_or_plural(term, "sg")


@cache
def _get_singular_or_plural(term: str, target_grammatical_number: GrammaticalNumber) -> str:
    info = find_term_info(term)

    current_key = cast(TermEntryKey, f"{info.country_code}_{info.grammatical_number}")
    target_key = cast(TermEntryKey, f"{info.country_code}_{target_grammatical_number}")

    if (
        info.grammatical_number == target_grammatical_number
        # Check that singular and plural differ
        and info.entry[current_key] != info.entry[target_key]
    ):
        raise InternationalizedTermError(f"Term '{term}' is already entered as plural")

    try:
        return info.entry[target_key]
    except KeyError as err:
        raise InternationalizedTermError(f"No plural entered for term '{term}'") from err


@cache
def find_term_info(term: str) -> TermInfo:
    for entry in TERMS:
        for other_term_type, other_term in entry.items():
            if term == other_term:
                country_code, grammatical_number = other_term_type.split("_")
                return TermInfo(
                    country_code=country_code,
                    grammatical_number=cast(GrammaticalNumber, grammatical_number),
                    entry=entry
                )

    raise InternationalizedTermError(f"Could not find term '{term}' in terms")
