from typing import Iterable
from typing import Optional

from enums import HandDryingMethod
from enums import LocationType
from enums import YesNoLimited
from piccolo.columns import Boolean
from piccolo.columns import Column
from piccolo.columns import Decimal
from piccolo.columns import ForeignKey
from piccolo.columns import Integer
from piccolo.columns import JSON
from piccolo.columns import OnDelete
from piccolo.columns import Real
from piccolo.columns import Text
from piccolo.columns import Timestamp
from piccolo.columns import Varchar
from piccolo.table import Table

from .tables_helper import column_attrs


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


class SourceColumnContainer:

    def __init_subclass__(
            cls,
            /,
            add_source_columns: Optional[Iterable[str]] = None,
            **kwargs,
    ):
        for column_name in column_attrs(cls):
            if add_source_columns is not None and column_name not in add_source_columns:
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


class DetailsMixin:
    operator = Varchar(length=255, null=True)


class DetailsOpeningTimesMixin:
    opening_times = Text(null=True)


class CommonToiletDetails:

    def __init_subclass__(cls, toilet_details_prefix: str = "", **kwargs):
        columns: dict[str, Column] = dict(
            # see https://wiki.openstreetmap.org/wiki/Tag:amenity%3Dtoilets
            has_fee=Boolean(null=True),
            fee=Decimal(
                # Stores dd.dd
                # This will cause a problem if there are toilets that charge more that 99 Euro.
                # I don't think that will be a problem.
                digits=(4, 2),
            ),
            is_customer_only=Boolean(null=True),

            female=Boolean(null=True),
            male=Boolean(null=True),
            unisex=Boolean(null=True),
            child=Boolean(null=True),

            has_seated=Boolean(null=True),
            has_urinal=Boolean(null=True),
            has_squat=Boolean(null=True),

            change_table=Varchar(length=31, choices=YesNoLimited),

            wheelchair_accessible=Varchar(length=31, choices=YesNoLimited),
            wheelchair_access_info=Text(null=True),

            has_hand_washing=Boolean(null=True),
            has_soap=Boolean(null=True),
            has_hand_disinfectant=Boolean(null=True),
            has_hand_creme=Boolean(null=True),
            has_hand_drying=Boolean(null=True),
            hand_drying_method=Varchar(length=31, choices=HandDryingMethod),
            has_paper=Boolean(null=True),
            has_hot_water=Boolean(null=True),
            has_shower=Boolean(null=True),
            has_drinking_water=Boolean(null=True),
        )

        for column_name, column in columns.items():
            setattr(cls, f"{toilet_details_prefix}{column_name}", column)

        try:
            super().__init_subclass__(**kwargs)  # type: ignore
        except KeyError:
            super().__init_subclass__()


class Details(
    DetailsMixin,
    DetailsOpeningTimesMixin,
    CommonToiletDetails,
    SourceColumnContainer,
    Table,
    toilet_details_prefix="toilet_"
):
    pass


class DataAcquisitionDetailsToilet(
    DetailsMixin,
    DetailsOpeningTimesMixin,
    CommonToiletDetails,
    SourceColumnContainer,
    Table,
    tablename="da_details_toilet",
):
    overpass_node_id = Integer()
    overpass_node_data = JSON()


class LocationsMixin:
    type = Varchar(length=127, choices=LocationType)
    name = Varchar(length=255)
    address = Varchar()
    latitude = Real()
    longitude = Real()


class Locations(
    LocationsMixin,
    SourceColumnContainer,
    Table,
    add_source_columns=["name", "address", "longitude", "latitude"],
):
    details_id = ForeignKey(references=Details, unique=True)


class DataAcquisitionLocations(
    LocationsMixin,
    SourceColumnContainer,
    Table,
    tablename="da_locations",
    add_source_columns=["name", "address", "longitude", "latitude"],
):
    # Does not use foreign key because the integer references different tables based on location type.
    details_id = Integer(unique=True)
