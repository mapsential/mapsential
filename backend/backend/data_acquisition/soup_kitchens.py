import datetime
from pathlib import Path
from typing import cast
from typing import Optional
from typing import TypedDict

# Add admin_backend package root to path if file is being executed directly
if __name__ == "__main__":
    import sys
    sys.path.append(str(Path(__file__).parent.parent.resolve()))

from enums import LocationType
from db.tables import Locations, DataAcquisitionLocations, Details, DataAcquisitionDetailsSoupKitchen, \
    DetailsSoupKitchen
from crud import create_or_update_source, repopulate_with_locations_and_details, \
    construct_details_soup_kitchen_and_da_row, construct_locations_and_da_row
from geolocation import get_lat_long_from_address
from json_utils import get_obj_from_most_recently_json_file_in_dir


DIR_PATH = Path(__file__).parent.resolve()
SOUP_KITCHENS_DATA_PATH = DIR_PATH / "soup_kitchens_data"
BERLINER_TAFEL_SOURCE_NAME = "Berliner Tafel E.V."
BERLINER_TAFEL_SOURCE_URL = "https://www.berliner-tafel.de/laib-und-seele/die-praxis/kunden/ausgabestellen"
BERLINER_TAFEL_LOCATION_NAME = "Ausgabestelle der Berliner Tafel"
BERLINER_TAFEL_OPERATOR = "Berliner Tafel E.V."


class JsonFileTimeDataItemSchema(TypedDict):
    day: str
    time: list[str]


class JsonFileLocationSchema(TypedDict):
    address: str
    time_data: list[JsonFileTimeDataItemSchema]
    info: str


class JsonFileSchema(TypedDict):
    data: list[JsonFileLocationSchema]


async def repopulate_with_soup_kitchens() -> None:
    locations_rows, da_locations_rows, details_rows, da_details_rows = await construct_locations_and_details_rows()

    await repopulate_with_locations_and_details(
        LocationType.SOUP_KITCHEN,
        locations_rows,
        da_locations_rows,
        details_rows,
        da_details_rows,
    )


async def construct_locations_and_details_rows() -> tuple[
    list[Locations],
    list[DataAcquisitionLocations],
    list[DetailsSoupKitchen],
    list[DataAcquisitionDetailsSoupKitchen],
]:
    locations_rows = []
    da_locations_rows = []
    details_rows = []
    da_details_rows = []

    operator_source_id = await create_or_update_berliner_tafel_source(datetime.datetime.now())

    for json_location in cast(
            JsonFileSchema,
            get_obj_from_most_recently_json_file_in_dir(SOUP_KITCHENS_DATA_PATH)
    )["data"]:
        locations_row, da_locations_row = await construct_locations_and_da_row_from_json_location(
            operator_source_id,
            json_location,
        )
        details_row, da_details_row = construct_details_and_da_row_from_json_location(
            operator_source_id,
            json_location,
        )

        locations_rows.append(locations_row)
        da_locations_rows.append(da_locations_row)
        details_rows.append(details_row)
        da_details_rows.append(da_details_row)

    return locations_rows, da_locations_rows, details_rows, da_details_rows


async def construct_locations_and_da_row_from_json_location(
        operator_source_id: int,
        json_location: JsonFileLocationSchema,
) -> tuple[Locations, DataAcquisitionLocations]:
    address = json_location["address"]
    lat_long_source_id, lat, long = await get_lat_long_from_address(address)

    return construct_locations_and_da_row(
        type=LocationType.SOUP_KITCHEN,
        name=BERLINER_TAFEL_LOCATION_NAME,
        name_source_id=operator_source_id,
        address=address,
        address_source_id=operator_source_id,
        latitude=lat,
        latitude_source_id=lat_long_source_id,
        longitude=long,
        longitude_source_id=lat_long_source_id,
    )


def construct_details_and_da_row_from_json_location(
        operator_source_id: int,
        json_location: JsonFileLocationSchema,
) -> tuple[Details, DataAcquisitionDetailsSoupKitchen]:
    if json_location["info"] is None:
        info = None
        info_source_id = None
    else:
        info = json_location["info"]
        info_source_id = operator_source_id

    return construct_details_soup_kitchen_and_da_row(
        operator=BERLINER_TAFEL_OPERATOR,
        operator_source_id=operator_source_id,
        opening_times=get_opening_times_from_json_location(json_location),
        opening_times_source_id=operator_source_id,
        info=info,
        info_source_id=info_source_id,
        json_data=json_location,
        json_data_source_id=operator_source_id,
    )


def get_opening_times_from_json_location(json_location: JsonFileLocationSchema) -> Optional[str]:
    lines = []
    try:
        time_data = json_location["time_data"]
    except KeyError:
        return None

    for time_data_item in time_data:
        try:
            time_span = time_data_item["time"]
        except KeyError:
            continue

        if len(time_span) == 1:
            time_span_str = f"ab {time_span[0]}"
        elif len(time_span) == 2:
            time_span_str = f"{time_span[0]} - {time_span[1]}"
        else:
            raise ValueError(
                f"No time span given for day '{time_data_item['day']}' for soup kitchen '{json_location['address']}'"
            )

        lines.append(f"{time_data_item['day']}: {time_span_str}")

    if len(lines) == 0:
        return None

    return "\n".join(lines)


async def create_or_update_berliner_tafel_source(access_time: datetime.datetime) -> int:
    return await create_or_update_source(
        name=BERLINER_TAFEL_SOURCE_NAME,
        url=BERLINER_TAFEL_SOURCE_URL,
        access_time=access_time,
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(repopulate_with_soup_kitchens())
