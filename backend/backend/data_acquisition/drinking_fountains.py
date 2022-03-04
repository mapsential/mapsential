import datetime
from dataclasses import dataclass
from pathlib import Path
from string import whitespace
from typing import Iterable
from typing import Union
from xml.etree import ElementTree

import requests

# Add admin_backend package root to path if file is being executed directly
if __name__ == "__main__":
    import sys
    sys.path.append(str(Path(__file__).parent.parent.resolve()))

from utils.dirs_and_files import unzip, make_tmp_dir
from enums import LocationType
from db.tables import Locations, DataAcquisitionLocations, Details, DataAcquisitionDetailsDrinkingFountain, \
    DetailsDrinkingFountain
from crud import delete_all_locations_by_type, create_or_update_source, construct_locations_and_da_row, \
    construct_details_drinking_fountain_and_da_row, repopulate_with_locations_and_details

GOOGLE_MAPS_DRINKING_FOUNTAIN_KMZ_URL = \
    "https://www.google.com/maps/d/u/0/kml?forcekml=0&mid=1XJunMq4YF0zaZxh4AVtyA5v6FWjYV90I&lid=1RcQnxo4AnQ"
BERLINER_WASSERBETRIEBE_SOURCE_NAME = "Berliner Wasserbetriebe - Öffentliche Trinkbrunnen"
BERLINER_WASSERBETRIEBE_SOURCE_URL = "https://www.bwb.de/de/trinkbrunnen.php"
BERLINER_WASSERBETRIEBE_OPERATOR = "Berliner Wasserbetriebe"
BERLINER_WASSERBETRIEBE_LOCATION_NAME = "Trinkbrunnen der Berliner Wasserbetriebe"


@dataclass(frozen=True)
class BWBParsedLocation:
    name: str
    address: str
    operating_times: str
    latitude: float
    longitude: float
    kml_dict: dict


async def repopulate_with_drinking_fountains() -> None:
    locations_rows, da_locations_rows, details_rows, da_details_rows = await construct_locations_and_details_rows()

    await repopulate_with_locations_and_details(
        LocationType.DRINKING_FOUNTAIN,
        locations_rows,
        da_locations_rows,
        details_rows,
        da_details_rows,
    )


async def construct_locations_and_details_rows() -> tuple[
    list[Locations],
    list[DataAcquisitionLocations],
    list[DetailsDrinkingFountain],
    list[DataAcquisitionDetailsDrinkingFountain],
]:
    locations_rows = []
    da_locations_rows = []
    details_rows = []
    da_details_rows = []

    operator_source_id = await create_or_update_bwb_source(datetime.datetime.now())

    for parsed_location in get_bwb_parsed_locations_from_kmz_url(GOOGLE_MAPS_DRINKING_FOUNTAIN_KMZ_URL):
        locations_row, da_locations_row = construct_locations_and_da_row_from_parsed_location(
            operator_source_id,
            parsed_location,
        )
        details_row, da_details_row = construct_details_and_da_row_from_parsed_location(
            operator_source_id,
            parsed_location,
        )

        locations_rows.append(locations_row)
        da_locations_rows.append(da_locations_row)
        details_rows.append(details_row)
        da_details_rows.append(da_details_row)

    return locations_rows, da_locations_rows, details_rows, da_details_rows


def construct_locations_and_da_row_from_parsed_location(
        operator_source_id: int,
        parsed_location: BWBParsedLocation,
) -> tuple[Locations, DataAcquisitionLocations]:
    return construct_locations_and_da_row(
        type=LocationType.DRINKING_FOUNTAIN,
        name=parsed_location.name,
        name_source_id=operator_source_id,
        address=parsed_location.address,
        address_source_id=operator_source_id,
        latitude=parsed_location.latitude,
        latitude_source_id=operator_source_id,
        longitude=parsed_location.longitude,
        longitude_source_id=operator_source_id,
    )


def construct_details_and_da_row_from_parsed_location(
        operator_source_id: int,
        parsed_location: BWBParsedLocation,
) -> tuple[DetailsDrinkingFountain, DataAcquisitionDetailsDrinkingFountain]:
    return construct_details_drinking_fountain_and_da_row(
        operator=BERLINER_WASSERBETRIEBE_OPERATOR,
        operator_source_id=operator_source_id,
        opening_times=parsed_location.operating_times,
        opening_times_source_id=operator_source_id,
        google_maps_kml_placemark=parsed_location.kml_dict,
        google_maps_kml_placemark_source_id=operator_source_id,
    )


async def create_or_update_bwb_source(access_time: datetime.datetime) -> int:
    return await create_or_update_source(
        name=BERLINER_WASSERBETRIEBE_SOURCE_NAME,
        url=BERLINER_WASSERBETRIEBE_SOURCE_URL,
        access_time=access_time,
    )


def get_bwb_parsed_locations_from_kmz_url(url: str) -> Iterable[BWBParsedLocation]:
    with make_tmp_dir("./.tmp_kmz_download") as tmp_dir_path:
        zip_file_path = tmp_dir_path / "google_maps_drinking_fountains.kmz"
        extracted_dir_path = tmp_dir_path / "google_maps_drinking_fountains"
        kml_file_path = extracted_dir_path / "doc.kml"

        download_kmz_file(url, zip_file_path)
        unzip(zip_file_path, extracted_dir_path)
        yield from parse_bwb_xml(kml_file_path)


def download_kmz_file(url: str, dst_path: Union[str, Path]) -> None:
    resolved_dst_path = Path(dst_path).resolve()

    response = requests.get(url, stream=True)

    with open(resolved_dst_path, "wb") as dst_file:
        dst_file.write(response.raw.read())


def parse_bwb_xml(path: Union[str, Path]) -> Iterable[BWBParsedLocation]:
    resolved_path = Path(path).resolve()

    tree = ElementTree.parse(resolved_path)
    root = tree.getroot()
    for placemark in get_xml_children_with_tag_endswith(root, "Placemark"):
        yield get_bwb_parsed_location(placemark)


def get_bwb_parsed_location(placemark) -> BWBParsedLocation:
    name_element = next(get_xml_children_with_tag_endswith(placemark, "name"))
    description_element = next(get_xml_children_with_tag_endswith(placemark, "description"))
    coordinates_element = next(get_xml_children_with_tag_endswith(placemark, "coordinates"))

    latitude, longitude = get_latitude_and_longitude_from_bwb_coordinates(coordinates_element.text)

    return BWBParsedLocation(
        name=BERLINER_WASSERBETRIEBE_SOURCE_NAME,
        address=name_element.text.strip(),
        operating_times=get_operating_times_from_bwb_description(description_element.text),
        latitude=latitude,
        longitude=longitude,
        kml_dict=xml_element_to_dict(placemark),
    )


def get_latitude_and_longitude_from_bwb_coordinates(coordinates: str) -> tuple[float, float]:
    long_text, lat_text, *_ = coordinates.replace(whitespace, "").split(",")
    return float(lat_text), float(long_text)


def get_operating_times_from_bwb_description(description: str) -> str:
    german_text = description.strip().split("<br>")[0]
    return german_text.removeprefix("Betriebszeit:").strip()


def xml_element_to_dict(element) -> dict:
    return {
        "tag": element.tag,
        "attributes": element.attrib,
        "text": element.text,
        "tail": element.tail,
        "children": [xml_element_to_dict(child) for child in element]
    }


def get_xml_children_with_tag_endswith(root, child_tag: str):
    for child in root:
        if child.tag.endswith(child_tag):
            yield child
        else:
            yield from get_xml_children_with_tag_endswith(child, child_tag)


if __name__ == "__main__":
    import asyncio

    asyncio.run(repopulate_with_drinking_fountains())
