from typing import Callable
from typing import Container
from typing import Iterable
from typing import Optional
from typing import TypeVar

from enums import HandDryingMethod
from enums import LocationType
from enums import YesNoLimited
from piccolo.columns import BigInt
from piccolo.columns import Boolean
from piccolo.columns import Column
from piccolo.columns import ForeignKey
from piccolo.columns import Integer
from piccolo.columns import JSON
from piccolo.columns import Numeric
from piccolo.columns import OnDelete
from piccolo.columns import Real
from piccolo.columns import Serial
from piccolo.columns import Text
from piccolo.columns import Timestamp
from piccolo.columns import Varchar
from piccolo.table import Table

from .tables_helper import column_attrs


TABLE_NAME_DETAILS_DEFIBRILLATOR = "details_defibrillator"
TABLE_NAME_DETAILS_DRINKING_FOUNTAIN = "details_drinking_fountain"
TABLE_NAME_DETAILS_SOUP_KITCHEN = "details_soup_kitchen"
TABLE_NAME_DETAILS_TOILET = "details_toilet"
TABLE_NAME_LOCATIONS = "locations"


# Sources
# ============================================================================


class Sources(Table):
    name = Varchar(length=255)
    url = Varchar(null=True, unique=True)
    initial_access = Timestamp(
        null=True,
        help_text="When did the application or an admin first make modifications using data from the data source?"
    )
    last_access = Timestamp(
        null=True,
        help_text="When did the application or an admin last make modifications using data from the data source?"
    )


class SourceColumnContainerMixin:

    def __init_subclass__(
            cls,
            /,
            exclude_source_for_columns: Container[str] = (),
            include_source_for_id_columns: Container[str] = (),
            **kwargs,
    ):
        for column_name in column_attrs(cls):
            if column_name in exclude_source_for_columns:
                continue

            # Skip primary and foreign key columns by default
            if column_name not in include_source_for_id_columns and column_name.endswith("id"):
                continue

            for source_column_name, source_column in get_source_columns(column_name):
                setattr(cls, source_column_name, source_column)

        try:
            super().__init_subclass__(**kwargs)  # type: ignore
        except TypeError:
            super().__init_subclass__()


def get_source_columns(column_name: str) -> tuple[tuple[str, Column], ...]:
    return (
        (f"{column_name}_source_id", ForeignKey(references=Sources, on_delete=OnDelete.no_action)),
    )


# Details
# ============================================================================


class DetailsOperatorMixin:
    operator = Varchar(length=255, null=True)


class DetailsOpeningTimesMixin:
    opening_times = Text(null=True)


# Defibrillator Details
# ----------------------------------------------------------------------------


class CommonDetailsDefibrillatorMixin(DetailsOperatorMixin, DetailsOpeningTimesMixin):
    pass


class DetailsDefibrillator(
    CommonDetailsDefibrillatorMixin,
    SourceColumnContainerMixin,
    Table,
    tablename=TABLE_NAME_DETAILS_DEFIBRILLATOR,
):
    pass


class DataAcquisitionDetailsDefibrillator(
    CommonDetailsDefibrillatorMixin,
    SourceColumnContainerMixin,
    Table,
    tablename=f"da_{TABLE_NAME_DETAILS_DEFIBRILLATOR}"
):
    details_id = ForeignKey(references=DetailsDefibrillator)

    street = Text(null=True)
    city = Varchar(length=255)
    # Stored as varchar because postal codes starting with 0 could cause
    # unexpected bugs if they were handled as integers.
    postal_code = Varchar(length=5, null=True)
    country = Varchar(length=255)

    json_data = JSON(null=True)


# Drinking Fountain Details
# ----------------------------------------------------------------------------


class CommonDetailsDrinkingFountainMixin(DetailsOperatorMixin, DetailsOpeningTimesMixin):
    pass


class DetailsDrinkingFountain(
    CommonDetailsDrinkingFountainMixin,
    SourceColumnContainerMixin,
    Table,
    tablename=TABLE_NAME_DETAILS_DRINKING_FOUNTAIN
):
    pass


class DataAcquisitionDetailsDrinkingFountain(
    CommonDetailsDrinkingFountainMixin,
    SourceColumnContainerMixin,
    Table,
    tablename=f"da_{TABLE_NAME_DETAILS_DRINKING_FOUNTAIN}"
):
    details_id = ForeignKey(references=DetailsDrinkingFountain)

    google_maps_kml_placemark = JSON(null=True)


# Soup Kitchen Details
# ----------------------------------------------------------------------------


class CommonDetailsSoupKitchensMixin(DetailsOperatorMixin, DetailsOpeningTimesMixin):
    info = Text(null=True)


class DetailsSoupKitchen(
    CommonDetailsSoupKitchensMixin,
    SourceColumnContainerMixin,
    Table,
    tablename=TABLE_NAME_DETAILS_SOUP_KITCHEN
):
    pass


class DataAcquisitionDetailsSoupKitchen(
    CommonDetailsSoupKitchensMixin,
    SourceColumnContainerMixin,
    Table,
    tablename=f"da_{TABLE_NAME_DETAILS_SOUP_KITCHEN}"
):
    details_id = ForeignKey(references=DetailsSoupKitchen)

    json_data = JSON(null=True)


# Toilet Details
# ----------------------------------------------------------------------------


class CommonDetailsToilet(DetailsOperatorMixin, DetailsOpeningTimesMixin):
    # see https://wiki.openstreetmap.org/wiki/Tag:amenity%3Dtoilets
    has_fee = Boolean(null=True)
    fee = Numeric(
        # Stores dd.dd
        # This will cause a problem if there are toilets that charge more that 99 Euro.
        # I don't think that will be a problem.
        digits=(4, 2),
        null=True,
    ),
    is_customer_only = Boolean(null=True)

    female = Boolean(null=True)
    male = Boolean(null=True)
    unisex = Boolean(null=True)
    child = Boolean(null=True)

    has_seated = Boolean(null=True)
    has_urinal = Boolean(null=True)
    has_squat = Boolean(null=True)

    change_table = Varchar(length=31, choices=YesNoLimited, null=True)

    wheelchair_accessible = Varchar(length=31, choices=YesNoLimited, null=True)
    wheelchair_access_info = Text(null=True)

    has_hand_washing = Boolean(null=True)
    has_soap = Boolean(null=True)
    has_hand_disinfectant = Boolean(null=True)
    has_hand_creme = Boolean(null=True)
    has_hand_drying = Boolean(null=True)
    hand_drying_method = Varchar(length=31, choices=HandDryingMethod, null=True)
    has_paper = Boolean(null=True)
    has_hot_water = Boolean(null=True)
    has_shower = Boolean(null=True)
    has_drinking_water = Boolean(null=True)


class DetailsToilet(
    CommonDetailsToilet,
    SourceColumnContainerMixin,
    Table,
    tablename=TABLE_NAME_DETAILS_TOILET
):
    pass


class DataAcquisitionDetailsToilet(
    CommonDetailsToilet,
    SourceColumnContainerMixin,
    Table,
    tablename=f"da_{TABLE_NAME_DETAILS_TOILET}",
    include_source_for_id_columns=["osm_node_id"],
):
    details_id = ForeignKey(references=DetailsToilet)

    osm_node_id = BigInt(null=True)
    osm_node_data = JSON(null=True)


# ----------------------------------------------------------------------------


Details = TypeVar(
    "Details",
    DetailsDefibrillator,
    DetailsDrinkingFountain,
    DetailsSoupKitchen,
    DetailsToilet
)

DataAcquisitionDetails = TypeVar(
    "DataAcquisitionDetails",
    DataAcquisitionDetailsDefibrillator,
    DataAcquisitionDetailsDrinkingFountain,
    DataAcquisitionDetailsSoupKitchen,
    DataAcquisitionDetailsToilet,
)


# Locations
# ============================================================================


class LocationsMixin:
    type = Varchar(length=127, choices=LocationType)
    name = Varchar(length=255)
    address = Varchar()
    latitude = Real()
    longitude = Real()


class Locations(
    LocationsMixin,
    SourceColumnContainerMixin,
    Table,
):
    # Does not use foreign key because the integer references different tables based on location type.
    details_id = Integer()


class DataAcquisitionLocations(
    LocationsMixin,
    SourceColumnContainerMixin,
    Table,
    tablename="da_locations",
    exclude_source_for_columns=["type"],
):
    locations_id = ForeignKey(references=Locations)
    # Does not use foreign key because the integer references different tables based on location type.
    details_id = Integer()


class Comments(Table):
    location_id = ForeignKey(references=Locations)

    author_name = Varchar(length=255)
    content = Text()
    timestamp = Timestamp()
