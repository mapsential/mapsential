from typing import cast
from typing import Iterable
from typing import TypedDict

import paths
from enums import LocationType
from structs import DbEntitiesGroup
from utils.json import get_obj_from_most_recently_json_file_in_dir

from db.tables import Details
from db.tables import Locations


DataSchema = Iterable["DataEntrySchema"]
class DataEntrySchema(TypedDict):
    dauerhaftOffen: bool
    land: str
    latitude: float
    longitude: float
    postleitzahl: str
    stadt: str
    standortName: str
    strasse: str


DATA_PATH = paths.DATA_DIR / "defibrillators"
FALLBACK_NAME = "Defibrillator"
ALWAYS_OPEN_STR = "24/7"


def acquire() -> Iterable[DbEntitiesGroup]:
    data = get_obj_from_most_recently_json_file_in_dir(DATA_PATH)
    normalized_data = normalize(data)

    for entry in normalized_data:
        yield create_entities(entry)


def normalize(data: DataSchema) -> DataSchema:
    normalizers = [
        remove_leading_and_trailing_whitespaces,
        # Add further normalizers here
    ]

    for entry in data:
        for func in normalizers:
            entry = func(entry)

        yield entry


def remove_leading_and_trailing_whitespaces(entry: DataEntrySchema) -> DataEntrySchema:
    return cast(DataEntrySchema, {
        key.strip(): val.strip() if type(val) is str else val
        for key, val in entry.items()
    })


def create_entities(entry: DataEntrySchema) -> DbEntitiesGroup:
    return DbEntitiesGroup(
        location=create_location_without_details_id(entry),
        details=create_details(entry)
    )


def create_location_without_details_id(entry: DataEntrySchema) -> Locations:
    return Locations(
        type=LocationType.DEFIBRILLATOR,
        latitude=entry["longitude"],
        longitude=entry["latitude"],
    )


def create_details(entry: DataEntrySchema) -> Details:
    return Details(
        name=entry.get("standortName", FALLBACK_NAME),
        operator=entry["standortName"],
        opening_times=ALWAYS_OPEN_STR if entry["dauerhaftOffen"] else None,
        street=entry["strasse"],
        city=entry["stadt"],
        postcode=entry["postleitzahl"],
        country=entry["land"],
    )
