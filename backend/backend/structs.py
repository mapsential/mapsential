from typing import NamedTuple

from db.tables import Details
from db.tables import Locations


class DbEntitiesGroup(NamedTuple):
    location: Locations
    details: Details
