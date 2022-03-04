import datetime
import pathlib
import re
from functools import cache
from typing import Optional
from typing import Protocol
from typing import TypeVar

import overpy

# Add parent dir to path if file is being executed directly
if __name__ == "__main__":
    import sys
    sys.path.append(str(pathlib.Path(__file__).parent.parent.resolve()))

from db.tables import Details, DataAcquisitionDetailsToilet, Locations, DataAcquisitionLocations, Sources, \
    DetailsToilet
from enums import LocationType, YesNoLimited, HandDryingMethod
from crud import create_or_update_source, delete_all_locations_by_type, construct_locations_and_da_row, \
    construct_details_toilet_and_da_row, repopulate_with_locations_and_details
from geolocation import get_address_from_lat_long


T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


OVERPASS_SOURCE_NAME = "Overpass-API"
OVERPASS_BERLIN_AREA_ID = "3600062422"
OVERPASS_QUERY = f"""node
    [amenity=toilets]
    (area:{OVERPASS_BERLIN_AREA_ID});
out;"""
# This regex is more permissive than it needs to be in case there is incorrectly formatted data.
# see https://wiki.openstreetmap.org/wiki/Key:charge
OVERPASS_CHARGE_REGEX = re.compile(
    r"(\d+|\d+\.\d*|\d*\.\d+)\s*EUR",
    re.IGNORECASE
)
DEFAULT_LOCATION_NAME = "Toilette"


overpass_api = overpy.Overpass()


class OsmNodeSchema(Protocol):
    id: int
    tags: dict[str, str]
    attributes: dict[str, str]
    lat: float
    lon: float

    def __hash__(self):
        pass


async def repopulate_with_toilets():
    locations_rows, da_locations_rows, details_rows, da_details_rows = await construct_locations_and_details_rows()

    await repopulate_with_locations_and_details(
        LocationType.TOILET,
        locations_rows,
        da_locations_rows,
        details_rows,
        da_details_rows,
    )


async def construct_locations_and_details_rows() ->  tuple[
    list[Locations],
    list[DataAcquisitionLocations],
    list[DetailsToilet],
    list[DataAcquisitionDetailsToilet],
]:
    locations_rows = []
    da_locations_rows = []
    details_rows = []
    da_details_rows = []

    map_provider_source_id, osm_nodes = await get_nodes_from_overpass()

    for osm_node in osm_nodes:
        locations_row, da_locations_row = await construct_locations_and_da_row_from_osm_node(
            map_provider_source_id,
            osm_node,
        )
        details_row, da_details_row = construct_details_and_da_row_from_osm_node(
            map_provider_source_id,
            osm_node,
        )

        locations_rows.append(locations_row)
        da_locations_rows.append(da_locations_row)
        details_rows.append(details_row)
        da_details_rows.append(da_details_row)

    return locations_rows, da_locations_rows, details_rows, da_details_rows


async def construct_locations_and_da_row_from_osm_node(
        map_provider_source_id: int,
        osm_node: OsmNodeSchema,
) -> tuple[Locations, DataAcquisitionLocations]:
    address_source_id, address = await get_address_from_lat_long(osm_node.lat, osm_node.lon)

    return construct_locations_and_da_row(
        type=LocationType.TOILET,
        address=address,
        address_source_id=address_source_id,
        name=get_str_from_osm_node_tag(osm_node, "name") or DEFAULT_LOCATION_NAME,
        name_source_id=map_provider_source_id,
        latitude=osm_node.lat,
        latitude_source_id=map_provider_source_id,
        longitude=osm_node.lon,
        longitude_source_id=map_provider_source_id,
    )


def construct_details_and_da_row_from_osm_node(
        map_provider_source_id: int,
        osm_node: OsmNodeSchema,
) -> tuple[DetailsToilet, DataAcquisitionDetailsToilet]:
    has_soap = get_bool_from_osm_node_tag(osm_node, "handwashing:soap")
    has_hand_disinfectant = get_bool_from_osm_node_tag(osm_node, "handwashing:hand_disinfectant")
    has_hand_washing = (
            get_bool_from_osm_node_tag(osm_node, "toilets:handwashing")
            or has_soap
            or has_hand_disinfectant
    )
    hand_drying_method = get_hand_drying_method_from_osm_node(osm_node)
    has_hand_drying = hand_drying_method is not None

    return construct_details_toilet_and_da_row(
        operator=get_operator_from_osm_node(osm_node),
        operator_source_id=map_provider_source_id,
        opening_times=get_opening_time_from_osm_node(osm_node),
        opening_times_source_id=map_provider_source_id,

        has_fee=get_bool_from_osm_node_tag(osm_node, "fee"),
        has_fee_source_id=map_provider_source_id,
        is_customer_only=get_is_customer_only_from_osm_node(osm_node),
        is_customer_only_source_id=map_provider_source_id,

        female=get_bool_from_osm_node_tag(osm_node, "female"),
        female_source_id=map_provider_source_id,
        male=get_bool_from_osm_node_tag(osm_node, "male"),
        male_source_id=map_provider_source_id,
        unisex=get_bool_from_osm_node_tag(osm_node, "unisex"),
        unisex_source_id=map_provider_source_id,
        child=get_bool_from_osm_node_tag(osm_node, "child"),
        child_source_id=map_provider_source_id,

        has_seated=get_has_seated_from_osm_node(osm_node),
        has_seated_source_id=map_provider_source_id,
        has_urinal=get_has_seated_from_osm_node(osm_node),
        has_urinal_source_id=map_provider_source_id,
        has_squat=get_has_seated_from_osm_node(osm_node),
        has_squat_source_id=map_provider_source_id,

        change_table=get_yes_no_limited_from_osm_node_tag(
            osm_node,
            "toilets:change_table",
            "change_table",
        ),
        change_table_source_id=map_provider_source_id,

        wheelchair_accessible=get_yes_no_limited_from_osm_node_tag(
            osm_node,
            "toilets:wheelchair",
            "wheelchair",
        ),
        wheelchair_accessible_source_id=map_provider_source_id,
        wheelchair_access_info=get_str_from_osm_node_tag(
            osm_node,
            "wheelchair:description:de",
            "wheelchair:description",
        ),
        wheelchair_access_info_source_id=map_provider_source_id,

        has_paper=get_str_from_osm_node_tag(
            osm_node,
            "toilets:paper_supplied",
            "toilets:byop",
        ),
        has_paper_source_id=map_provider_source_id,
        has_hand_washing=has_hand_washing,
        has_hand_washing_source_id=map_provider_source_id,
        has_soap=has_soap,
        has_soap_source_id=map_provider_source_id,
        has_hand_disinfectant=has_hand_disinfectant,
        has_hand_disinfectant_source_id=map_provider_source_id,
        has_hand_creme=get_bool_from_osm_node_tag(osm_node, "handwashing:creme"),
        has_hand_creme_source_id=map_provider_source_id,
        has_hand_drying=has_hand_drying,
        has_hand_drying_source_id=map_provider_source_id,
        hand_drying_method=hand_drying_method,
        hand_drying_method_source_id=map_provider_source_id,
        has_hot_water=get_bool_from_osm_node_tag(osm_node, "hot_water"),
        has_hot_water_source_id=map_provider_source_id,
        has_shower=get_bool_from_osm_node_tag(osm_node, "shower"),
        has_shower_source_id=map_provider_source_id,
        has_drinking_water=get_bool_from_osm_node_tag(osm_node, "drinking_water:legal", "drinking_water"),
        has_drinking_water_source_id=map_provider_source_id,

        osm_node_id=osm_node.id,
        osm_node_id_source_id=map_provider_source_id,
        osm_node_data=dict(
            id=osm_node.id,
            attributes=osm_node.attributes,
            tags=osm_node.tags,
            lat=osm_node.lat,
            lon=osm_node.lon,
        ),
        osm_node_data_source_id=map_provider_source_id,
    )


def get_operator_from_osm_node(osm_node: OsmNodeSchema) -> Optional[str]:
    return osm_node.tags.get("operator", None)


@cache
def get_opening_time_from_osm_node(osm_node: OsmNodeSchema) -> Optional[str]:
    return osm_node.tags.get("opening_hours", None)


def get_bool_from_osm_node_tag(osm_node: OsmNodeSchema, tag_name: str, *fallback_tag_names: str) -> Optional[bool]:
    try:
        tag_value = osm_node.tags[tag_name]
    except KeyError:
        if fallback_tag_names:
            return get_bool_from_osm_node_tag(osm_node, *fallback_tag_names)
        return None

    if tag_value == "yes":
        return True
    elif tag_value == "no":
        return False

    # TODO: Handle values that cannot be parsed!
    return None


def get_fee_from_osm_node(node) -> Optional[float]:
    try:
        tag_value = node.tags["charge"]
    except KeyError:
        return None

    match = OVERPASS_CHARGE_REGEX.match(tag_value)

    if match is None:
        # TODO: Handle values that cannot be parsed!
        return None

    return float(match.group(1))


def get_is_customer_only_from_osm_node(osm_node: OsmNodeSchema) -> Optional[bool]:
    try:
        tag_value = osm_node.tags["access"]
    except KeyError:
        return None

    return tag_value == "customers"


def get_has_seated_from_osm_node(osm_node: OsmNodeSchema) -> Optional[bool]:
    positions = get_toilets_positions_from_osm_node(osm_node)
    return "seated" in positions


def get_has_urinal_from_osm_node(osm_node: OsmNodeSchema) -> Optional[bool]:
    positions = get_toilets_positions_from_osm_node(osm_node)
    return "urinal" in positions


def get_has_squat_from_osm_node(osm_node: OsmNodeSchema) -> Optional[bool]:
    positions = get_toilets_positions_from_osm_node(osm_node)
    return "squat" in positions


@cache
def get_toilets_positions_from_osm_node(node) -> list[str]:
    try:
        return node.tags["toilets:position"].split(";")
    except KeyError:
        return []


def get_yes_no_limited_from_osm_node_tag(
        osm_node: OsmNodeSchema,
        tag_name: str,
        *fallback_tag_names: str
) -> Optional[YesNoLimited]:
    try:
        tag_value = osm_node.tags[tag_name]
    except KeyError:
        if fallback_tag_names:
            return get_yes_no_limited_from_osm_node_tag(osm_node, *fallback_tag_names)
        return None

    if tag_value == "yes":
        return YesNoLimited.YES
    elif tag_value == "no":
        return YesNoLimited.NO
    elif tag_value == "limited":
        return YesNoLimited.LIMITED

    # TODO: Handle values that cannot be parsed!
    return None


def get_str_from_osm_node_tag(node, tag_name: str, *fallback_tag_names: str) -> Optional[str]:
    try:
        return node.tags[tag_name]
    except KeyError:
        if fallback_tag_names:
            return get_str_from_osm_node_tag(node, *fallback_tag_names)

    return None


def get_hand_drying_method_from_osm_node(node):
    try:
        tag_value = node.tags["toilets:hand_drying"]
    except KeyError:
        return None

    if tag_value == "electric_hand_dryer":
        return HandDryingMethod.ELECTRIC_HAND_DRYER
    elif tag_value == "paper_towel":
        return HandDryingMethod.PAPER_TOWEL
    elif tag_value == "towel":
        return HandDryingMethod.TOWEL

    # TODO: Handle values that cannot be parsed!
    return None


async def get_nodes_from_overpass():
    source_id = await create_or_update_source(
        name=OVERPASS_SOURCE_NAME,
        url=overpass_api.default_url,
        access_time=datetime.datetime.now(),
    )

    return source_id, get_data_from_overpass().nodes


def get_data_from_overpass():
    return overpass_api.query(OVERPASS_QUERY)


if __name__ == "__main__":
    import asyncio

    asyncio.run(repopulate_with_toilets())
