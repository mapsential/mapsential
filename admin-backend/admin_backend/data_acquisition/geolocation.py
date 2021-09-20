import datetime
from typing import Any

from crud import create_or_update_source
from geopy.geocoders import Nominatim


NOMINATIM_USER_AGENT = "nominatim.openstreetmap.org"
NOMINATIM_SOURCE_URL = f"https://{NOMINATIM_USER_AGENT}"
NOMINATIM_GEOLOCATOR = Nominatim(user_agent=NOMINATIM_USER_AGENT)


async def get_address_from_lat_long(
        lat: float,
        long: float,
        geolocator=NOMINATIM_GEOLOCATOR
) -> tuple[int, str]:
    source = await create_or_update_nominatim_source(access_time=datetime.datetime.now())
    return source, geolocator.reverse(f"{lat}, {long}").address


async def create_or_update_nominatim_source(access_time: datetime.datetime) -> int:
    return await create_or_update_source(
        name="Nominatim",
        url=NOMINATIM_SOURCE_URL,
        access_time=access_time,
    )
