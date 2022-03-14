from typing import cast
from typing import Iterable
from typing import TypedDict

import paths
from enums import LocationType
from structs import DbEntitiesGroup
from utils.json import get_obj_from_most_recently_json_file_in_dir

from db.tables import Details
from db.tables import Locations


DataSchema = list["DataEntrySchema"]


class DataEntrySchema(TypedDict):
    address: str
    time_data: list["DayOpeningTimeEntrySchema"]
    info: str


class DayOpeningTimeEntrySchema(TypedDict):
    day: str
    time: list[str]


DATA_PATH = paths.DATA_DIR / "soup_kitchens"
NAME = "Ausgabestelle der Berliner Tafel"
OPERATOR = "Berliner Tafel E.V."


def acquire() -> Iterable[DbEntitiesGroup]:
    data = cast(DataSchema, get_obj_from_most_recently_json_file_in_dir(DATA_PATH)["data"])

    for entry in data:
        yield create_entities(entry)


def create_entities(entry: DataEntrySchema) -> DbEntitiesGroup:
    return DbEntitiesGroup(
        location=Locations(
            type=LocationType.SOUP_KITCHEN,
        ),
        details=Details(
            name=NAME,
            operator=OPERATOR,
            opening_times=get_opening_times_repr_or_none(entry),
            address=entry["address"],
            soup_kitchen_info=entry["info"] if entry["info"] != "" else None,
        )
    )


def get_opening_times_repr_or_none(entry: DataEntrySchema) -> str | None:
    try:
        return get_opening_times_repr(entry["time_data"])
    except KeyError:
        return None


def get_opening_times_repr(
    days_opening_times_entries: list[DayOpeningTimeEntrySchema]
) -> str:
    days = [entry["day"] for entry in days_opening_times_entries]
    times = [get_time_repr(entry.get("time", [])) for entry in days_opening_times_entries]

    days_column_width = max(len(s) for s in days)
    times_column_width = max(len(s) for s in times)

    return "\n".join(
        f"{day_repr.ljust(days_column_width)}  {time_repr.center(times_column_width)}"
        for day_repr, time_repr in zip(days, times)
    )


def get_time_repr(times: list[str]) -> str:
    if (len_ := len(times)) == 0:
        return ""

    return f"{times[0]}-{times[1]}" if len_ >= 2 else f"ab {times[0]}"
