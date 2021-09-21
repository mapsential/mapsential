import datetime
import json
from pathlib import Path
from typing import cast
from typing import Generic
from typing import Optional
from typing import TypedDict
from typing import TypeVar
from typing import Union

# Add admin_backend package root to path if file is being executed directly
if __name__ == "__main__":
    import sys
    sys.path.append(str(Path(__file__).parent.parent.resolve()))

from enums import LocationType
from admin.tables import Locations, DataAcquisitionLocations, Details, DataAcquisitionDetailsSoupKitchen
from crud import delete_all_locations_by_type, create_or_update_source
from geolocation import get_lat_long_from_address


T = TypeVar("T")


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
    await delete_all_locations_by_type(LocationType.SOUP_KITCHEN)
    await populate_with_soup_kitchens()


async def populate_with_soup_kitchens() -> None:
    locations, da_locations = await get_location_rows_and_create_details()

    await Locations.insert(*locations).run()
    await DataAcquisitionLocations.insert(*da_locations).run()


async def get_location_rows_and_create_details() -> tuple[
    list[Locations],
    list[DataAcquisitionLocations],
]:
    locations = []
    da_locations = []

    berliner_tafel_source_id = await create_or_update_berliner_tafel_source(datetime.datetime.now())

    for json_location in cast(
            JsonFileSchema,
            get_obj_from_most_recently_json_file_in_dir(SOUP_KITCHENS_DATA_PATH)
    )["data"]:
        common_details_kwargs = dict(
            operator=BERLINER_TAFEL_OPERATOR,
            operator_source_id=berliner_tafel_source_id,
            opening_times=get_opening_times_from_json_location(json_location),
            opening_times_source_id=berliner_tafel_source_id,
        )

        if json_location["info"] is None:
            soup_kitchen_info = None
        else:
            soup_kitchen_info = json_location["info"]
        details_result = await Details.insert(Details(
            **common_details_kwargs,
            soup_kitchen_info=soup_kitchen_info,
            soup_kitchen_info_source_id=berliner_tafel_source_id,
        )).run()
        details_id = details_result[0]["id"]

        da_details_result = await DataAcquisitionDetailsSoupKitchen.insert(
            DataAcquisitionDetailsSoupKitchen(
                **common_details_kwargs,
                **dict(
                    json_data=json_location,
                    json_data_source_id=berliner_tafel_source_id,
                ),
                info=json_location["info"],
                info_source_id=berliner_tafel_source_id,
            )).run()
        da_details_id = da_details_result[0]["id"]

        address = json_location["address"]
        lat_long_source_id, lat, long = await get_lat_long_from_address(address)

        common_location_kwargs = dict(
            type=LocationType.SOUP_KITCHEN,
            name=BERLINER_TAFEL_LOCATION_NAME,
            name_source_id=berliner_tafel_source_id,
            address=address,
            address_source_id=berliner_tafel_source_id,
            latitude=lat,
            latitude_source_id=lat_long_source_id,
            longitude=long,
            longitude_source_id=lat_long_source_id,
        )

        locations.append(Locations(
            **common_location_kwargs,
            details_id=details_id,
        ))

        da_locations.append(DataAcquisitionLocations(
            **common_location_kwargs,
            details_id=da_details_id,
        ))

    return locations, da_locations


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


def get_obj_from_most_recently_json_file_in_dir(
        dir_path: Union[str, Path],
        # Determine most recent file by name. E.g. '2021_10_21.json' is more recent than '2021_09_24.json'
        most_recent_key = lambda path: path.name,
) -> T:
    resolved_path = Path(dir_path).resolve()

    most_recent_json_file = max(
        (child for child in resolved_path.iterdir() if child.is_file() and child.suffix == ".json"),
        key=most_recent_key
    )

    return get_obj_from_json_file(most_recent_json_file)


def get_obj_from_json_file(file_path: Union[str, Path]) -> T:
    resolved_path = Path(file_path).resolve()

    with open(resolved_path, "r") as file:
        return json.loads(file.read())


if __name__ == "__main__":
    import asyncio

    asyncio.run(repopulate_with_soup_kitchens())
