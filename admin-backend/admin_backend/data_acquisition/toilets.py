import datetime
import pathlib
import re
from functools import cache
from typing import Any
from typing import Optional
from typing import TypeVar
from typing import Union

import overpy

# Add parent dir to path if file is being executed directly
if __name__ == "__main__":
    import sys
    sys.path.append(str(pathlib.Path(__file__).parent.parent.resolve()))

from admin.tables import Details, DataAcquisitionDetailsToilet, Locations, DataAcquisitionLocations, Sources
from enums import LocationType, YesNoLimited, HandDryingMethod
from crud import create_or_update_source, delete_all_locations_by_type
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


async def repopulate_with_toilets():
    await delete_all_locations_by_type(LocationType.TOILET)
    await populate_with_toilets()


async def populate_with_toilets():
    overpass_source_id, nodes = await get_nodes_from_overpass()
    for node in nodes:
        await insert_toilet_from_overpass_node(overpass_source_id, node)


async def insert_toilet_from_overpass_node(overpass_source_id, node):
    address_source_id, address = await get_address_from_lat_long(node.lat, node.lon)

    details_insert_result = await Details.insert(Details(
        **get_column_values_with_source_columns(
            overpass_source_id,
            dict(
                operator=get_operator_from_overpass_node(node),
                opening_times=get_opening_time_from_overpass_node(node),
                **get_toilet_details_row_column_values("toilet_", node),
            ),
        )
    )).run()
    details_id = details_insert_result[0]["id"]

    da_details_insert_result = await DataAcquisitionDetailsToilet.insert(DataAcquisitionDetailsToilet(
        **get_column_values_with_source_columns(overpass_source_id, dict(
            overpass_node_id=node.id,
            overpass_node_data=dict(
                id=node.id,
                attributes=node.attributes,
                tags=node.tags,
                lat=node.lat,
                lon=node.lon,
            ),
            operator=get_operator_from_overpass_node(node),
            opening_times=get_opening_time_from_overpass_node(node),
            **get_toilet_details_row_column_values("", node),
        ))
    )).run()
    da_details_id = da_details_insert_result[0]["id"]

    await Locations.insert(Locations(
        type=LocationType.TOILET,
        **get_column_values_with_source_columns(address_source_id, dict(address=address)),
        **get_column_values_with_source_columns(overpass_source_id, dict(
            name=get_str_from_overpass_node_tag(node, "name") or DEFAULT_LOCATION_NAME,
            latitude=node.lat,
            longitude=node.lon,
        )),
        details_id=details_id,
    )).run()

    await DataAcquisitionLocations.insert(DataAcquisitionLocations(
        type=LocationType.TOILET,
        **get_column_values_with_source_columns(address_source_id, dict(address=address)),
        **get_column_values_with_source_columns(overpass_source_id, dict(
            name=get_str_from_overpass_node_tag(node, "name") or DEFAULT_LOCATION_NAME,
            latitude=node.lat,
            longitude=node.lon,
        )),
        details_id=da_details_id,
    )).run()


def get_column_values_with_source_columns(
        source_id: int,
        column_values: dict[str, Union[T, int]],
) -> dict[str, Union[T, int]]:
    column_values_with_source_columns = {}
    for column_name, column_value in column_values.items():
        column_values_with_source_columns[column_name] = column_value
        column_values_with_source_columns[f"{column_name}_source_id"] = source_id
    return column_values_with_source_columns


def get_operator_from_overpass_node(node):
    return node.tags.get("operator", None)


@cache
def get_opening_time_from_overpass_node(node):
    return node.tags.get("opening_hours", None)


def get_toilet_details_row_column_values(toilet_columns_prefix: str, node) -> dict[str, Any]:
    has_soap = get_bool_from_overpass_node_tag(node, "handwashing:soap")
    has_hand_disinfectant = get_bool_from_overpass_node_tag(node, "handwashing:hand_disinfectant")
    has_hand_washing = (
       get_bool_from_overpass_node_tag(node, "toilets:handwashing")
       or has_soap
       or has_hand_disinfectant
    )
    hand_drying_method = get_hand_drying_method_from_overpass_node(node)
    has_hand_drying = hand_drying_method is not None

    unprocessed_column_values: dict[str, Any] = dict(
        has_fee=get_bool_from_overpass_node_tag(node, "fee"),
        fee=get_fee_from_overpass_node(node),
        is_customer_only=get_is_customer_only_from_overpass_node(node),

        female=get_bool_from_overpass_node_tag(node, "female"),
        male=get_bool_from_overpass_node_tag(node, "male"),
        unisex=get_bool_from_overpass_node_tag(node, "unisex"),
        child=get_bool_from_overpass_node_tag(node, "child"),

        has_seated=get_has_seated_from_overpass_node(node),
        has_urinal=get_has_seated_from_overpass_node(node),
        has_squat=get_has_seated_from_overpass_node(node),

        change_table=get_yes_no_limited_from_overpass_node_tag(
            node,
            "toilets:change_table",
            "change_table",
        ),

        wheelchair_accessible=get_yes_no_limited_from_overpass_node_tag(
            node,
            "toilets:wheelchair",
            "wheelchair",
        ),
        wheelchair_access_info=get_str_from_overpass_node_tag(
            node,
            "wheelchair:description:de",
            "wheelchair:description",
        ),

        has_hand_washing=has_hand_washing,
        has_soap=has_soap,
        has_hand_disinfectant=has_hand_disinfectant,
        has_hand_creme=get_bool_from_overpass_node_tag(node, "handwashing:creme"),
        has_hand_drying=has_hand_drying,
        hand_drying_method=hand_drying_method,
        has_hot_water=get_bool_from_overpass_node_tag(node, "hot_water"),
        has_shower=get_bool_from_overpass_node_tag(node, "shower"),
        has_drinking_water=get_bool_from_overpass_node_tag(node, "drinking_water:legal", "drinking_water"),
    )

    return {
        f"{toilet_columns_prefix}{column_name}": column_value
        for column_name, column_value in unprocessed_column_values.items()
    }


def get_bool_from_overpass_node_tag(node, tag_name: str, *fallback_tag_names: str) -> Optional[bool]:
    try:
        tag_value = node.tags[tag_name]
    except KeyError:
        if fallback_tag_names:
            return get_bool_from_overpass_node_tag(node, *fallback_tag_names)
        return None

    if tag_value == "yes":
        return True
    elif tag_value == "no":
        return False

    # TODO: Handle values that cannot be parsed!
    return None


def get_fee_from_overpass_node(node) -> Optional[float]:
    try:
        tag_value = node.tags["charge"]
    except KeyError:
        return None

    match = OVERPASS_CHARGE_REGEX.match(tag_value)

    if match is None:
        # TODO: Handle values that cannot be parsed!
        return None

    return float(match.group(1))


def get_is_customer_only_from_overpass_node(node) -> Optional[bool]:
    try:
        tag_value = node.tags["access"]
    except KeyError:
        return None

    return tag_value == "customers"


def get_has_seated_from_overpass_node(node) -> Optional[bool]:
    positions = get_toilets_positions_from_overpass_node(node)
    return "seated" in positions


def get_has_urinal_from_overpass_node(node) -> Optional[bool]:
    positions = get_toilets_positions_from_overpass_node(node)
    return "urinal" in positions


def get_has_squat_from_overpass_node(node) -> Optional[bool]:
    positions = get_toilets_positions_from_overpass_node(node)
    return "squat" in positions


@cache
def get_toilets_positions_from_overpass_node(node) -> list[str]:
    try:
        return node.tags["toilets:position"].split(";")
    except KeyError:
        return []


def get_yes_no_limited_from_overpass_node_tag(
        node,
        tag_name: str,
        *fallback_tag_names: str
) -> Optional[YesNoLimited]:
    try:
        tag_value = node.tags[tag_name]
    except KeyError:
        if fallback_tag_names:
            return get_yes_no_limited_from_overpass_node_tag(node, *fallback_tag_names)
        return None

    if tag_value == "yes":
        return YesNoLimited.YES
    elif tag_value == "no":
        return YesNoLimited.NO
    elif tag_value == "limited":
        return YesNoLimited.LIMITED

    # TODO: Handle values that cannot be parsed!
    return None


def get_str_from_overpass_node_tag(node, tag_name: str, *fallback_tag_names: str) -> Optional[str]:
    try:
        return node.tags[tag_name]
    except KeyError:
        if fallback_tag_names:
            return get_str_from_overpass_node_tag(node, *fallback_tag_names)

    return None


def get_hand_drying_method_from_overpass_node(node):
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
