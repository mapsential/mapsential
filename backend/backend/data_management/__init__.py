import asyncio
from typing import Callable
from typing import Iterable

from country_codes import get_german_country_code_from_name
from country_codes import get_german_country_name_from_code
from enums import LocationType
from errors import GeolocationError
from geopy.location import Location as GeopyLocation
from structs import DbEntitiesGroup
from utils.iterables import chunk_iter

from .acquisition.defibrillators import acquire as acquire_defibrillators
from .acquisition.drinking_fountains import acquire as acquire_drinking_fountains
from .acquisition.soup_kitchens import acquire as acquire_soup_kitchens
from .acquisition.toilets import acquire as acquire_toilets
from .geolocation import get_geopy_location_from_address
from .geolocation import get_geopy_location_from_lat_long
from db.tables import Details
from db.tables import Locations


LOCATION_TYPE_TO_ACQUIRER = {
    LocationType.DEFIBRILLATOR: acquire_defibrillators,
    LocationType.DRINKING_FOUNTAIN: acquire_drinking_fountains,
    LocationType.SOUP_KITCHEN: acquire_soup_kitchens,
    LocationType.TOILET: acquire_toilets,
}
CHUNK_SIZE = 100
GEOPY_LOCATION_RAW_TO_DETAILS_CONVERSION: tuple[tuple[str, str] | tuple[str, str, Callable[[str], str]], ...] = (
    ("road", "street", str.capitalize),
    ("district", "district", str.capitalize),
    ("town", "town", str.capitalize),
    ("city", "city", str.capitalize),
    ("postcode", "postcode"),
    ("country", "country", str.capitalize),
    ("country_code", "country_code", str.upper),
)


def update(location_types: list[LocationType]) -> None:
    async def async_update() -> None:
        for location_type in location_types:
            await update_location_type(location_type)

    asyncio.run(async_update())


async def update_location_type(location_type: LocationType) -> None:
    acquire = LOCATION_TYPE_TO_ACQUIRER[location_type]

    print(f"acquiring {location_type.value}s data...")
    incomplete_entity_groups = acquire()
    print(f"acquired {location_type.value}s data\n")

    print(f"completing {location_type.value}s data...")
    completed_entity_groups = complete_entities(incomplete_entity_groups)
    print(f"completed {location_type.value}s data\n")

    print(f"updating {location_type.value}s in database...")
    await update_database(location_type, completed_entity_groups)
    print(f"updated {location_type.value}s in database\n")


def complete_entities(entity_groups: Iterable[DbEntitiesGroup]) -> Iterable[DbEntitiesGroup]:
    for entity_group in entity_groups:
        location = entity_group.location
        details = entity_group.details

        has_lat_long = location.latitude is not None and location.longitude is not None
        has_address = details.address is not None

        if has_lat_long and has_address:
            continue

        try:
            if has_lat_long:
                geopy_location = get_geopy_location_from_lat_long(
                    location.latitude,
                    location.longitude
                )

                details.address = geopy_location.address
            elif has_address:
                geopy_location = get_geopy_location_from_address(details.address)

                location.latitude = geopy_location.latitude
                location.longitude = geopy_location.longitude
            else:
                raise ValueError()

            complete_details_from_geopy_location(details, geopy_location)

            yield entity_group
        except GeolocationError as err:
            # TODO: add logging
            pass


def complete_details_from_geopy_location(
    details: Details,
    geopy_location: GeopyLocation
) -> None:
    for conversion in GEOPY_LOCATION_RAW_TO_DETAILS_CONVERSION:
        if len(conversion) == 3:
            geopy_field, detail_name, converter = conversion  # type: ignore[misc]
            geopy_val = geopy_location.raw.get(geopy_field, None)
            if geopy_val is None:
                setattr(details, detail_name, None)
            else:
                setattr(details, detail_name, converter(geopy_val))
        elif len(conversion) == 2:
            geopy_field, detail_name = conversion  # type: ignore[misc]
            setattr(details, detail_name, geopy_location.raw.get(geopy_field, None))
        else:
            raise ValueError()

    if not details.country and details.country_code:
        details.country = get_german_country_name_from_code(details.country_code)
    elif details.country and not details.country_code:
        details.country_code = get_german_country_code_from_name(details.country)


async def update_database(location_type: LocationType, entity_groups: Iterable[DbEntitiesGroup]) -> None:
    async with Locations._meta.db.transaction():
        print(f"deleting {location_type.value}s from database...")
        await delete_from_database(location_type)
        print(f"deleted {location_type.value}s from database")

        print(f"inserting {location_type.value}s into database...")
        # Insert in chunks to prevent high memory overhead
        for i, entity_groups_chunk in enumerate(chunk_iter(entity_groups, size=CHUNK_SIZE)):
            print(f"inserting chunk {i + 1} into database...")
            await insert_into_database(entity_groups_chunk)
            print(f"inserted chunk {i + 1} into database...")
        print(f"inserted {location_type.value}s int database")


async def delete_from_database(location_type: LocationType) -> None:
    await Locations.delete().where(Locations.type == location_type)


async def insert_into_database(entity_groups: Iterable[DbEntitiesGroup]) -> None:
    locations = [entity_group.location for entity_group in entity_groups]
    all_details = [entity_group.details for entity_group in entity_groups]

    details_insert_results = await Details.insert(*all_details)

    # Link tables
    for result, location in zip(details_insert_results, locations):
        location.details_id = result["id"]

    await Locations.insert(*locations)
