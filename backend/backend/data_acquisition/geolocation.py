import datetime
import re

from crud import create_or_update_source
from geopy.geocoders import Nominatim
from geopy.location import Location as GeopyLocation


NOMINATIM_USER_AGENT = "nominatim.openstreetmap.org"
NOMINATIM_SOURCE_URL = f"https://{NOMINATIM_USER_AGENT}"
NOMINATIM_GEOLOCATOR = Nominatim(user_agent=NOMINATIM_USER_AGENT)
POST_CODE_REGEX = re.compile(r"\d{5} Berlin", re.IGNORECASE)


async def get_lat_long_from_address(
        address: str,
        geolocator=NOMINATIM_GEOLOCATOR,
) -> tuple[int, float, float]:
    source = await create_or_update_nominatim_source(access_time=datetime.datetime.now())
    location = get_geopy_location_from_address(address, geolocator=geolocator)

    return source, location.latitude, location.longitude


def get_geopy_location_from_address(address: str, geolocator=NOMINATIM_GEOLOCATOR) -> GeopyLocation:
    location = geolocator.geocode(address)

    if location is None:
        try:
            post_code = get_postcode_in_str(address)
        except ValueError:
            raise ValueError(f"Could not determine location of address '{address}'")

        location = get_geopy_location_from_address(post_code)

    return location


def get_postcode_in_str(s: str) -> str:
    matches = POST_CODE_REGEX.findall(s)
    if matches is None:
        raise ValueError(f"No postcode found in '{s}'")
    elif len(matches) > 1:
        raise ValueError(f"Multiple postcodes found '{matches}'!")
    else:
        return matches[0]


async def get_address_from_lat_long(
        lat: float,
        long: float,
        geolocator=NOMINATIM_GEOLOCATOR,
) -> tuple[int, str]:
    source = await create_or_update_nominatim_source(access_time=datetime.datetime.now())
    return source, geolocator.reverse(f"{lat}, {long}").address


async def create_or_update_nominatim_source(access_time: datetime.datetime) -> int:
    return await create_or_update_source(
        name="Nominatim",
        url=NOMINATIM_SOURCE_URL,
        access_time=access_time,
    )
