import csv
from functools import cache
from pathlib import Path
from typing import cast
from typing import TypedDict

import paths
from errors import CountryCodeError


Data = tuple["DataEntry"]


class DataEntry(TypedDict):
    country_code: str
    country_name: str


GERMAN_CSV_NAME = "german_country_codes"
GERMAN_CSV_PATH = paths.DATA_DIR / f"{GERMAN_CSV_NAME}.csv"
CSV_DICT_READER_FIELDS = ("country_code", "country_name")


@cache
def get_german_country_name_from_code(code: str) -> str:
    return get_country_name_from_code(code, get_german_data())


def get_country_code_from_name(name: str, data: Data) -> str:
    normalized_name = name.capitalize()

    for entry in data:
        if entry["country_name"] == normalized_name:
            return entry["country_code"]

    raise CountryCodeError(f"Could not find code for country with name {normalized_name}")


@cache
def get_german_country_code_from_name(code: str) -> str:
    return get_country_code_from_name(code, get_german_data())


def get_country_name_from_code(code: str, data: Data) -> str:
    normalized_code = code.upper()

    for entry in data:
        if entry["country_code"] == normalized_code:
            return entry["country_name"]

    raise CountryCodeError(f"Could not find country with code {normalized_code}")


def get_german_data() -> Data:
    return get_data_from_csv(GERMAN_CSV_PATH)


@cache
def get_data_from_csv(csv_file_path: Path) -> Data:
    with open(csv_file_path, newline="") as csv_file:
        return cast(Data, tuple(csv.DictReader(csv_file, fieldnames=CSV_DICT_READER_FIELDS)))
