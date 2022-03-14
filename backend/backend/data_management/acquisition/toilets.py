from functools import partial
from typing import Iterable
from typing import Protocol

import overpy
from country_codes import get_german_country_name_from_code
from enums import HandDryingMethod
from enums import LocationType
from enums import YesNoLimited
from errors import CountryCodeError
from structs import DbEntitiesGroup

from db.tables import Details
from db.tables import Locations


class OSMNodeSchema(Protocol):
    id: int
    tags: dict[str, str]
    attributes: dict[str, str | dict[str, str]]
    lat: float
    lon: float


OVERPASS_SOURCE_NAME = "Overpass-API"
OVERPASS_BERLIN_AREA_ID = "3600062422"
OVERPASS_QUERY = f"""node
    [amenity=toilets]
    (area:{OVERPASS_BERLIN_AREA_ID});
out;"""
FALLBACK_NAME = "Toilette"


OverpassApi = overpy.Overpass()


def acquire() -> Iterable[DbEntitiesGroup]:
    for osm_node in fetch_osm_nodes():
        yield create_entities(osm_node)


def fetch_osm_nodes() -> Iterable[OSMNodeSchema]:
    return OverpassApi.query(OVERPASS_QUERY).nodes


def create_entities(osm_node: OSMNodeSchema) -> DbEntitiesGroup:
    return DbEntitiesGroup(
        location=create_location_entity(osm_node),
        details=create_details_entity(osm_node),
    )


def create_location_entity(osm_node: OSMNodeSchema) -> Locations:
    return Locations(
        type=LocationType.TOILET,
        latitude=osm_node.lat,
        longitude=osm_node.lon,
    )


def create_details_entity(osm_node: OSMNodeSchema) -> Details:
    return create_details_table_from_osm_tags(osm_node.tags)


def create_details_table_from_osm_tags(tags: dict[str, str]) -> Details:
    convert_yes_no_to_bool_or_none = \
        partial(convert_yes_no_osm_tag_to_bool_or_none, tags)
    convert_yes_no_limited_to_enum_or_none = \
        partial(convert_yes_no_limited_osm_tag_to_enum_or_none, tags)
    convert_hand_drying_method_to_enum_or_none = \
        partial(convert_hand_drying_method_osm_tag_to_enum_or_none, tags)
    has_toilets_position_or_none = \
        partial(osm_tags_have_toilets_position_or_none, tags)

    has_soap = convert_yes_no_to_bool_or_none("handwashing:soap")
    has_hand_disinfectant = convert_yes_no_to_bool_or_none("handwashing:hand_disinfectant")
    has_hand_washing = (
        convert_yes_no_to_bool_or_none("toilets:handwashing")
        or has_soap
        or has_hand_disinfectant
    )
    hand_drying_method = convert_hand_drying_method_to_enum_or_none("toilets:hand_drying")
    has_hand_drying = hand_drying_method is not None

    details = Details(
        name=tags.get("name:de", tags.get("name", FALLBACK_NAME)),
        operator=tags.get("operator", None),
        opening_times=tags.get("opening_hours", None),

        address=get_address_from_osm_tags_or_none(tags),
        street=capitalize_noneable_or_none(tags.get("addr:street", None)),
        district=capitalize_noneable_or_none(tags.get("addr:suburb", tags.get("addr:province", None))),
        city=capitalize_noneable_or_none(tags.get("addr:city", None)),
        postcode=capitalize_noneable_or_none(tags.get("addr:postcode", None)),
        country=get_german_country_name_from_noneable_code_or_one(tags.get("addr:country", None)),
        country_code=uppercase_noneable_or_none(tags.get("addr:country", None)),

        has_fee=convert_yes_no_to_bool_or_none("fee"),
        is_customer_only=tags.get("access") == "customers",

        female=convert_yes_no_to_bool_or_none("female"),
        male=convert_yes_no_to_bool_or_none("male"),
        unisex=convert_yes_no_to_bool_or_none("unisex"),
        child=convert_yes_no_to_bool_or_none("child"),

        has_seated=has_toilets_position_or_none("seated"),
        has_urinal=has_toilets_position_or_none("urinal"),
        has_squat=has_toilets_position_or_none("squat"),

        change_table=convert_yes_no_limited_to_enum_or_none(
            "toilets:change_table",
            "change_table",
        ),

        wheelchair_accessible=convert_yes_no_limited_to_enum_or_none(
            "toilets:wheelchair",
            "wheelchair",
        ),
        wheelchair_access_info=convert_yes_no_limited_to_enum_or_none(
            "wheelchair:description:de",
            "wheelchair:description",
        ),

        has_paper=convert_yes_no_to_bool_or_none(
            "toilets:paper_supplied",
            "toilets:byop",
        ),
        has_hand_washing=has_hand_washing,
        has_soap=has_soap,
        has_hand_disinfectant=has_hand_disinfectant,
        has_hand_creme=convert_yes_no_to_bool_or_none("handwashing:creme"),
        has_hand_drying=has_hand_drying,
        hand_drying_method=hand_drying_method,
        has_hot_water=convert_yes_no_to_bool_or_none("hot_water"),
        has_shower=convert_yes_no_to_bool_or_none("shower"),
        has_drinking_water=convert_yes_no_to_bool_or_none(
            "drinking_water:legal",
            "drinking_water",
        ),
    )

    return details


def convert_yes_no_osm_tag_to_bool_or_none(
    tags: dict[str, str],
    *tag_names: str,
) -> bool | None:
    for tag_name in tag_names:
        try:
            return convert_yes_no_to_bool(tags[tag_name])
        except KeyError:
            pass
        except ValueError:
            # TODO: Add logging for missformated tags
            pass

    return None


def get_address_from_osm_tags_or_none(tags: dict[str, str]) -> str | None:
    house_number = tags.get("addr:housenumber", None)
    floor = get_german_floor_name_from_noneable_or_none(tags.get("addr:floor", None))
    street = capitalize_noneable_or_none(tags.get("addr:street", None))
    suburb = capitalize_noneable_or_none(tags.get("addr:suburb", None))
    province = capitalize_noneable_or_none(tags.get("addr:province", None))
    city = capitalize_noneable_or_none(tags.get("addr:city", None))
    state = capitalize_noneable_or_none(tags.get("addr:state", None))
    postcode = capitalize_noneable_or_none(tags.get("addr:postcode", None))
    country = get_german_country_name_from_noneable_code_or_one(tags.get("addr:country", None))

    if (house_number or postcode) and street and city and country:
        return ", ".join(
            segment for segment in (
                house_number,
                floor,
                street,
                suburb,
                province,
                city,
                state,
                postcode,
                country,
            ) if segment
        )

    return None


def capitalize_noneable_or_none(noneable_str: str | None) -> str | None:
    if noneable_str is None:
        return None

    return noneable_str.capitalize()


def uppercase_noneable_or_none(noneable_str: str | None) -> str | None:
    if noneable_str is None:
        return None

    return noneable_str.upper()


def get_german_floor_name_from_noneable_or_none(num: int | str | None) -> str | None:
    if num is None:
        return None

    try:
        num = int(num)
    except ValueError:
        # TODO: Add logging

        return None

    if num == 0:
        return "EG"
    if num > 0:
        return f"{num}. OG"
    else:
        return "UG"


def get_german_country_name_from_noneable_code_or_one(country_code: str | None) -> str | None:
    if country_code is None:
        return None

    try:
        return get_german_country_name_from_code(country_code)
    except CountryCodeError:
        # TODO: Add logging

        return None


def convert_yes_no_to_bool(s: str) -> bool:
    if s == "yes":
        return True

    if s == "no":
        return False

    raise ValueError(f"Expected 'yes' or 'no', got '{s}'")


def convert_yes_no_limited_osm_tag_to_enum_or_none(
    tags: dict[str, str],
    *tag_names: str,
) -> YesNoLimited | None:
    for tag_name in tag_names:
        try:
            convert_yes_no_limited_to_enum(tags[tag_name])
        except KeyError:
            pass
        except ValueError:
            # TODO: Add logging for missformated tags
            pass

    return None


def convert_yes_no_limited_to_enum(s: str) -> YesNoLimited:
    if s == "yes":
        return YesNoLimited.YES
    elif s == "no":
        return YesNoLimited.NO
    elif s == "limited":
        return YesNoLimited.LIMITED

    raise ValueError("Expected 'yes', 'no' or 'limited', got '{s}'")


def convert_hand_drying_method_osm_tag_to_enum_or_none(
    tags: dict[str, str],
    *tag_names: str,
) -> HandDryingMethod | None:
    for tag_name in tag_names:
        try:
            return convert_hand_drying_method_to_enum(tags[tag_name])
        except KeyError:
            pass
        except ValueError:
            # TODO: Add logging for missformated tags
            pass

    return None


def convert_hand_drying_method_to_enum(s: str):
    if s == "electric_hand_dryer":
        return HandDryingMethod.ELECTRIC_HAND_DRYER
    elif s == "paper_towel":
        return HandDryingMethod.PAPER_TOWEL
    elif s == "towel":
        return HandDryingMethod.TOWEL

    raise ValueError("Expected 'electric_hand_dryer', 'paper_towel' or 'towel', got '{s}'")


def osm_tags_have_toilets_position_or_none(tags: dict[str, str], position: str) -> bool | None:
    try:
        return position in tags["toilets:position"].split(";")
    except KeyError:
        return None
