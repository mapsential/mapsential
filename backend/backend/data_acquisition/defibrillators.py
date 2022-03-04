import datetime
from pathlib import Path
from typing import cast
from typing import Generator
from typing import Iterable
from typing import Optional
from typing import TypedDict

# Add admin_backend package root to path if file is being executed directly
if __name__ == "__main__":
    import sys
    sys.path.append(str(Path(__file__).parent.parent.resolve()))

from db.tables import Locations, DataAcquisitionLocations, DetailsDefibrillator, DataAcquisitionDetailsDefibrillator
from data_acquisition.crud import repopulate_with_locations_and_details, create_or_update_source, \
    construct_locations_and_da_row, construct_details_defibrillator_and_da_row
from data_acquisition.json_utils import get_obj_from_most_recently_json_file_in_dir
from enums import LocationType

DIR_PATH = Path(__file__).parent.resolve()
DEFIBRILLATOR_DATA_PATH = DIR_PATH / "defibrillator_data"
DEFIBRILLATOR_DATA_SOURCE_NAME = "Research done by Denis and Lucas"
DEFIBRILLATOR_DATA_SOURCE_URL = "https://mapsential.de"
FALLBACK_DEFIBRILLATOR_LOCATION_NAME = "Defibrillator"


class JsonFileLocationSchema(TypedDict):
    dauerhaftOffen: bool
    land: str
    latitude: float
    longitude: float
    postleitzahl: str
    stadt: str
    standortName: str
    strasse: str


JsonFileSchema = list[JsonFileLocationSchema]


async def repopulate_with_defibrillators() -> None:
    locations_rows, da_locations_rows, details_rows, da_details_rows = await construct_locations_and_details_rows()

    await repopulate_with_locations_and_details(
        LocationType.DEFIBRILLATOR,
        locations_rows,
        da_locations_rows,
        details_rows,
        da_details_rows,
    )


async def construct_locations_and_details_rows() -> tuple[
    list[Locations],
    list[DataAcquisitionLocations],
    list[DetailsDefibrillator],
    list[DataAcquisitionDetailsDefibrillator],
]:
    locations_rows = []
    da_locations_rows = []
    details_rows = []
    da_details_rows = []

    source_id = await create_or_update_defibrillator_source(datetime.datetime.now())

    for json_location in get_normalized_json_locations_from_path(DEFIBRILLATOR_DATA_PATH):
        locations_row, da_locations_row = construct_locations_and_da_row_from_json_location(
            source_id,
            json_location,
        )
        details_row, da_details_row = construct_details_and_da_row_from_json_location(
            source_id,
            json_location,
        )

        locations_rows.append(locations_row)
        da_locations_rows.append(da_locations_row)
        details_rows.append(details_row)
        da_details_rows.append(da_details_row)

    return locations_rows, da_locations_rows, details_rows, da_details_rows


def get_normalized_json_locations_from_path(path: Path) -> Iterable[JsonFileLocationSchema]:
    for json_location in cast(
            JsonFileSchema,
            get_obj_from_most_recently_json_file_in_dir(path)
    ):
        name = json_location["standortName"]
        if name is None:
            normalized_name = name
        else:
            normalized_name = name.strip()

        yield dict(
            dauerhaftOffen=json_location["dauerhaftOffen"],
            land=json_location["land"].strip(),
            latitude=json_location["latitude"],
            longitude=json_location["longitude"],
            postleitzahl=json_location["postleitzahl"].strip(),
            stadt=json_location["stadt"].strip(),
            standortName=normalized_name,
            strasse=json_location["strasse"].strip(),
        )


async def create_or_update_defibrillator_source(access_time: datetime.datetime) -> int:
    return await create_or_update_source(
        name=DEFIBRILLATOR_DATA_SOURCE_NAME,
        url=DEFIBRILLATOR_DATA_SOURCE_URL,
        access_time=access_time,
    )


def construct_locations_and_da_row_from_json_location(
        source_id: int,
        json_location: JsonFileLocationSchema,
) -> tuple[Locations, DataAcquisitionLocations]:
    return construct_locations_and_da_row(
        type=LocationType.DEFIBRILLATOR,
        name=json_location["standortName"] or FALLBACK_DEFIBRILLATOR_LOCATION_NAME,
        name_source_id=source_id,
        address=get_address_from_json_location(json_location),
        address_source_id=source_id,
        latitude=json_location["latitude"],
        latitude_source_id=source_id,
        longitude=json_location["longitude"],
        longitude_source_id=source_id,
    )


def construct_details_and_da_row_from_json_location(
        source_id: int,
        json_location: JsonFileLocationSchema,
) -> tuple[DetailsDefibrillator, DataAcquisitionDetailsDefibrillator]:
    return construct_details_defibrillator_and_da_row(
        operator=json_location["standortName"],
        operator_source_id=source_id,
        opening_times=get_opening_times_from_json_location(json_location),
        opening_times_source_id=source_id,
        street=json_location["strasse"],
        street_source_id=source_id,
        city=json_location["stadt"],
        city_source_id=source_id,
        postal_code=json_location["postleitzahl"],
        postal_code_source_id=source_id,
        country=json_location["land"],
        country_source_id=source_id,
        json_data=json_location,
        json_data_source_id=source_id,
    )


def get_address_from_json_location(json_location: JsonFileLocationSchema) -> str:
    components = []
    if json_location["standortName"] is not None:
        components.append(json_location["standortName"])

    components += [
        json_location["strasse"],
        f"{json_location['postleitzahl']} {json_location['stadt']}",
    ]

    return ", ".join(components)


def get_opening_times_from_json_location(json_location: JsonFileLocationSchema) -> Optional[str]:
    if json_location["dauerhaftOffen"]:
        return "24/7"

    return None


if __name__ == "__main__":
    import asyncio

    asyncio.run(repopulate_with_defibrillators())
