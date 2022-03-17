from enums import LocationType
from utils.enums import get_values as get_enum_values
from utils.humanize import get_shortend_to_originals


ADMIN_CONTAINER_NAME = "mapsential_admin_backend"

LOCATION_TYPE_NAMES = get_enum_values(LocationType)
LOCATION_TYPE_NAMES_SHORTEND_TO_ORIGINALS = get_shortend_to_originals(LOCATION_TYPE_NAMES)
