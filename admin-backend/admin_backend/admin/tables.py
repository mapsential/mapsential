from enum import Enum

from piccolo.columns import ForeignKey, Real, Timestamp, Varchar
from piccolo.table import Table


class Details(Table):
    opening_time = Timestamp(null=True)
    closing_time = Timestamp(null=True)


class Locations(Table):
    class Type(str, Enum):
        SOUP_KITCHEN = "soup_kitchen"
        TOILET = "toilet"
        water_fountain = "water_fountain"

    type = Varchar(length=127, choices=Type)
    name = Varchar(length=255)
    longitude = Real()
    latitude = Real()
    details_id = ForeignKey(references=Details)
