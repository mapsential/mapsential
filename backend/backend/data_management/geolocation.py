import re

from errors import GeolocationError
from geopy.geocoders import Nominatim
from geopy.location import Location as GeopyLocation
# Docs: https://geopy.readthedocs.io/en/latest/


NOMINATIM_USER_AGENT = "nominatim.openstreetmap.org"
NOMINATIM_SOURCE_URL = f"https://{NOMINATIM_USER_AGENT}"
NOMINATIM_GEOLOCATOR = Nominatim(user_agent=NOMINATIM_USER_AGENT)
POST_CODE_REGEX = re.compile(r"\d{5} Berlin", re.IGNORECASE)


def get_geopy_location_from_address(address: str, geolocator=NOMINATIM_GEOLOCATOR) -> GeopyLocation:
    location = geolocator.geocode(address)

    general_err_msg = f"Could not determine location of address '{address}'"

    if location is None:
        try:
            postcode = get_postcode_in_str(address)
        except ValueError:
            raise GeolocationError(f"{general_err_msg} by extracting postcode from address")

        location = get_geopy_location_from_address(postcode)

    return _normalize_geopy_return_value_or_error(
        location,
        error_message=general_err_msg,
    )


def get_postcode_in_str(s: str) -> str:
    matches = POST_CODE_REGEX.findall(s)
    if matches is None:
        raise ValueError(f"No postcode found in '{s}'")
    elif len(matches) > 1:
        raise ValueError(f"Multiple postcodes found '{matches}'!")
    else:
        return matches[0]


def get_geopy_location_from_lat_long(
    lat: float,
    long: float,
    geolocator=NOMINATIM_GEOLOCATOR,
) -> GeopyLocation:
    return _normalize_geopy_return_value_or_error(
        geolocator.reverse(f"{lat}, {long}"),
        error_message=f"Geopy could not find location for coordinate (latitude={lat}, longitude={long})",
    )


def _normalize_geopy_return_value_or_error(
    return_value: GeopyLocation | list[GeopyLocation] | None,
    *,
    error_message: str = "Geopy geolocation failed",
) -> GeopyLocation:
    """Normalize return value of geopy geoencoding and reverse gencoding.

    Geopy geoencoding or reverse geoencoding may return either a geopy location object,
    a list of location objects or none.

    If a single object is returned, we return the object.

    If a list of objects is return, we return the first.

    If 'None' is returned, we raise an error.
    """
    if return_value is None:
        raise GeolocationError(error_message)

    if type(return_value) is list:
        return return_value[0]

    return return_value
