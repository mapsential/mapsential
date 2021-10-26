from decimal import Decimal
from enum import Enum

from piccolo.apps.migrations.auto import MigrationManager
from piccolo.columns.base import OnDelete
from piccolo.columns.base import OnUpdate
from piccolo.columns.column_types import BigInt
from piccolo.columns.column_types import Boolean
from piccolo.columns.column_types import ForeignKey
from piccolo.columns.column_types import Integer
from piccolo.columns.column_types import JSON
from piccolo.columns.column_types import Numeric
from piccolo.columns.column_types import Real
from piccolo.columns.column_types import Serial
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Timestamp
from piccolo.columns.column_types import Varchar
from piccolo.columns.defaults.timestamp import TimestampNow
from piccolo.columns.indexes import IndexMethod
from piccolo.table import Table


class Details(Table, tablename="details"):  # type: ignore
    id = Serial(
        null=False,
        primary_key=True,
        unique=False,
        index=False,
        index_method=IndexMethod.btree,
        choices=None,
        db_column_name="id",
    )


class Sources(Table, tablename="sources"):  # type: ignore
    id = Serial(
        null=False,
        primary_key=True,
        unique=False,
        index=False,
        index_method=IndexMethod.btree,
        choices=None,
        db_column_name="id",
    )


ID = "2021-10-21T10:48:58:562869"
VERSION = "0.57.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="admin", description=DESCRIPTION
    )

    manager.add_table(
        "DataAcquisitionDetailsSoupKitchen", tablename="da_details_soup_kitchen"
    )

    manager.add_table("Sources", tablename="sources")

    manager.add_table(
        "DataAcquisitionDetailsDrinkingFountain",
        tablename="da_details_drinking_fountain",
    )

    manager.add_table("Locations", tablename="locations")

    manager.add_table("Details", tablename="details")

    manager.add_table("DataAcquisitionLocations", tablename="da_locations")

    manager.add_table(
        "DataAcquisitionDetailsToilet", tablename="da_details_toilet"
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsSoupKitchen",
        tablename="da_details_soup_kitchen",
        column_name="opening_times",
        db_column_name="opening_times",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsSoupKitchen",
        tablename="da_details_soup_kitchen",
        column_name="operator",
        db_column_name="operator",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsSoupKitchen",
        tablename="da_details_soup_kitchen",
        column_name="json_data",
        db_column_name="json_data",
        column_class_name="JSON",
        column_class=JSON,
        params={
            "default": "{}",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsSoupKitchen",
        tablename="da_details_soup_kitchen",
        column_name="info",
        db_column_name="info",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsSoupKitchen",
        tablename="da_details_soup_kitchen",
        column_name="info_source_id",
        db_column_name="info_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsSoupKitchen",
        tablename="da_details_soup_kitchen",
        column_name="json_data_source_id",
        db_column_name="json_data_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsSoupKitchen",
        tablename="da_details_soup_kitchen",
        column_name="opening_times_source_id",
        db_column_name="opening_times_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsSoupKitchen",
        tablename="da_details_soup_kitchen",
        column_name="operator_source_id",
        db_column_name="operator_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Sources",
        tablename="sources",
        column_name="name",
        db_column_name="name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Sources",
        tablename="sources",
        column_name="url",
        db_column_name="url",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": True,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Sources",
        tablename="sources",
        column_name="initial_access",
        db_column_name="initial_access",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "default": TimestampNow(),
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Sources",
        tablename="sources",
        column_name="last_access",
        db_column_name="last_access",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "default": TimestampNow(),
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsDrinkingFountain",
        tablename="da_details_drinking_fountain",
        column_name="opening_times",
        db_column_name="opening_times",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsDrinkingFountain",
        tablename="da_details_drinking_fountain",
        column_name="operator",
        db_column_name="operator",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsDrinkingFountain",
        tablename="da_details_drinking_fountain",
        column_name="google_maps_kml_placemark",
        db_column_name="google_maps_kml_placemark",
        column_class_name="JSON",
        column_class=JSON,
        params={
            "default": "{}",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsDrinkingFountain",
        tablename="da_details_drinking_fountain",
        column_name="google_maps_kml_placemark_source_id",
        db_column_name="google_maps_kml_placemark_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsDrinkingFountain",
        tablename="da_details_drinking_fountain",
        column_name="opening_times_source_id",
        db_column_name="opening_times_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsDrinkingFountain",
        tablename="da_details_drinking_fountain",
        column_name="operator_source_id",
        db_column_name="operator_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Locations",
        tablename="locations",
        column_name="type",
        db_column_name="type",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 127,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "LocationType",
                {
                    "DRINKING_FOUNTAIN": "drinking_fountain",
                    "SOUP_KITCHEN": "soup_kitchen",
                    "TOILET": "toilet",
                },
            ),
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Locations",
        tablename="locations",
        column_name="name",
        db_column_name="name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Locations",
        tablename="locations",
        column_name="address",
        db_column_name="address",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Locations",
        tablename="locations",
        column_name="latitude",
        db_column_name="latitude",
        column_class_name="Real",
        column_class=Real,
        params={
            "default": 0.0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Locations",
        tablename="locations",
        column_name="longitude",
        db_column_name="longitude",
        column_class_name="Real",
        column_class=Real,
        params={
            "default": 0.0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Locations",
        tablename="locations",
        column_name="details_id",
        db_column_name="details_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Details,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": True,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Locations",
        tablename="locations",
        column_name="address_source_id",
        db_column_name="address_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Locations",
        tablename="locations",
        column_name="latitude_source_id",
        db_column_name="latitude_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Locations",
        tablename="locations",
        column_name="longitude_source_id",
        db_column_name="longitude_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Locations",
        tablename="locations",
        column_name="name_source_id",
        db_column_name="name_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="opening_times",
        db_column_name="opening_times",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="operator",
        db_column_name="operator",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="soup_kitchen_info",
        db_column_name="soup_kitchen_info",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_fee",
        db_column_name="toilet_has_fee",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_fee",
        db_column_name="toilet_fee",
        column_class_name="Numeric",
        column_class=Numeric,
        params={
            "default": Decimal("0"),
            "digits": (4, 2),
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_is_customer_only",
        db_column_name="toilet_is_customer_only",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_female",
        db_column_name="toilet_female",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_male",
        db_column_name="toilet_male",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_unisex",
        db_column_name="toilet_unisex",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_child",
        db_column_name="toilet_child",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_seated",
        db_column_name="toilet_has_seated",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_urinal",
        db_column_name="toilet_has_urinal",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_squat",
        db_column_name="toilet_has_squat",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_change_table",
        db_column_name="toilet_change_table",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 31,
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "YesNoLimited", {"YES": "yes", "NO": "no", "LIMITED": "limited"}
            ),
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_wheelchair_accessible",
        db_column_name="toilet_wheelchair_accessible",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 31,
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "YesNoLimited", {"YES": "yes", "NO": "no", "LIMITED": "limited"}
            ),
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_wheelchair_access_info",
        db_column_name="toilet_wheelchair_access_info",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_hand_washing",
        db_column_name="toilet_has_hand_washing",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_soap",
        db_column_name="toilet_has_soap",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_hand_disinfectant",
        db_column_name="toilet_has_hand_disinfectant",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_hand_creme",
        db_column_name="toilet_has_hand_creme",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_hand_drying",
        db_column_name="toilet_has_hand_drying",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_hand_drying_method",
        db_column_name="toilet_hand_drying_method",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 31,
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "HandDryingMethod",
                {
                    "ELECTRIC_HAND_DRYER": "electric_hand_dryer",
                    "PAPER_TOWEL": "paper_towel",
                    "TOWEL": "towel",
                },
            ),
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_paper",
        db_column_name="toilet_has_paper",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_hot_water",
        db_column_name="toilet_has_hot_water",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_shower",
        db_column_name="toilet_has_shower",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_drinking_water",
        db_column_name="toilet_has_drinking_water",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="opening_times_source_id",
        db_column_name="opening_times_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="operator_source_id",
        db_column_name="operator_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="soup_kitchen_info_source_id",
        db_column_name="soup_kitchen_info_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_change_table_source_id",
        db_column_name="toilet_change_table_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_child_source_id",
        db_column_name="toilet_child_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_fee_source_id",
        db_column_name="toilet_fee_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_female_source_id",
        db_column_name="toilet_female_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_hand_drying_method_source_id",
        db_column_name="toilet_hand_drying_method_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_drinking_water_source_id",
        db_column_name="toilet_has_drinking_water_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_fee_source_id",
        db_column_name="toilet_has_fee_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_hand_creme_source_id",
        db_column_name="toilet_has_hand_creme_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_hand_disinfectant_source_id",
        db_column_name="toilet_has_hand_disinfectant_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_hand_drying_source_id",
        db_column_name="toilet_has_hand_drying_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_hand_washing_source_id",
        db_column_name="toilet_has_hand_washing_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_hot_water_source_id",
        db_column_name="toilet_has_hot_water_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_paper_source_id",
        db_column_name="toilet_has_paper_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_seated_source_id",
        db_column_name="toilet_has_seated_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_shower_source_id",
        db_column_name="toilet_has_shower_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_soap_source_id",
        db_column_name="toilet_has_soap_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_squat_source_id",
        db_column_name="toilet_has_squat_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_has_urinal_source_id",
        db_column_name="toilet_has_urinal_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_is_customer_only_source_id",
        db_column_name="toilet_is_customer_only_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_male_source_id",
        db_column_name="toilet_male_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_unisex_source_id",
        db_column_name="toilet_unisex_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_wheelchair_access_info_source_id",
        db_column_name="toilet_wheelchair_access_info_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="Details",
        tablename="details",
        column_name="toilet_wheelchair_accessible_source_id",
        db_column_name="toilet_wheelchair_accessible_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionLocations",
        tablename="da_locations",
        column_name="type",
        db_column_name="type",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 127,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "LocationType",
                {
                    "DRINKING_FOUNTAIN": "drinking_fountain",
                    "SOUP_KITCHEN": "soup_kitchen",
                    "TOILET": "toilet",
                },
            ),
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionLocations",
        tablename="da_locations",
        column_name="name",
        db_column_name="name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionLocations",
        tablename="da_locations",
        column_name="address",
        db_column_name="address",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionLocations",
        tablename="da_locations",
        column_name="latitude",
        db_column_name="latitude",
        column_class_name="Real",
        column_class=Real,
        params={
            "default": 0.0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionLocations",
        tablename="da_locations",
        column_name="longitude",
        db_column_name="longitude",
        column_class_name="Real",
        column_class=Real,
        params={
            "default": 0.0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionLocations",
        tablename="da_locations",
        column_name="details_id",
        db_column_name="details_id",
        column_class_name="Integer",
        column_class=Integer,
        params={
            "default": 0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionLocations",
        tablename="da_locations",
        column_name="address_source_id",
        db_column_name="address_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionLocations",
        tablename="da_locations",
        column_name="latitude_source_id",
        db_column_name="latitude_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionLocations",
        tablename="da_locations",
        column_name="longitude_source_id",
        db_column_name="longitude_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionLocations",
        tablename="da_locations",
        column_name="name_source_id",
        db_column_name="name_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="opening_times",
        db_column_name="opening_times",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="operator",
        db_column_name="operator",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="overpass_node_id",
        db_column_name="overpass_node_id",
        column_class_name="BigInt",
        column_class=BigInt,
        params={
            "default": 0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="overpass_node_data",
        db_column_name="overpass_node_data",
        column_class_name="JSON",
        column_class=JSON,
        params={
            "default": "{}",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_fee",
        db_column_name="has_fee",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="fee",
        db_column_name="fee",
        column_class_name="Numeric",
        column_class=Numeric,
        params={
            "default": Decimal("0"),
            "digits": (4, 2),
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="is_customer_only",
        db_column_name="is_customer_only",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="female",
        db_column_name="female",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="male",
        db_column_name="male",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="unisex",
        db_column_name="unisex",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="child",
        db_column_name="child",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_seated",
        db_column_name="has_seated",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_urinal",
        db_column_name="has_urinal",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_squat",
        db_column_name="has_squat",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="change_table",
        db_column_name="change_table",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 31,
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "YesNoLimited", {"YES": "yes", "NO": "no", "LIMITED": "limited"}
            ),
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="wheelchair_accessible",
        db_column_name="wheelchair_accessible",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 31,
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "YesNoLimited", {"YES": "yes", "NO": "no", "LIMITED": "limited"}
            ),
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="wheelchair_access_info",
        db_column_name="wheelchair_access_info",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_hand_washing",
        db_column_name="has_hand_washing",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_soap",
        db_column_name="has_soap",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_hand_disinfectant",
        db_column_name="has_hand_disinfectant",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_hand_creme",
        db_column_name="has_hand_creme",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_hand_drying",
        db_column_name="has_hand_drying",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="hand_drying_method",
        db_column_name="hand_drying_method",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 31,
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "HandDryingMethod",
                {
                    "ELECTRIC_HAND_DRYER": "electric_hand_dryer",
                    "PAPER_TOWEL": "paper_towel",
                    "TOWEL": "towel",
                },
            ),
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_paper",
        db_column_name="has_paper",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_hot_water",
        db_column_name="has_hot_water",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_shower",
        db_column_name="has_shower",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_drinking_water",
        db_column_name="has_drinking_water",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="change_table_source_id",
        db_column_name="change_table_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="child_source_id",
        db_column_name="child_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="fee_source_id",
        db_column_name="fee_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="female_source_id",
        db_column_name="female_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="hand_drying_method_source_id",
        db_column_name="hand_drying_method_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_drinking_water_source_id",
        db_column_name="has_drinking_water_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_fee_source_id",
        db_column_name="has_fee_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_hand_creme_source_id",
        db_column_name="has_hand_creme_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_hand_disinfectant_source_id",
        db_column_name="has_hand_disinfectant_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_hand_drying_source_id",
        db_column_name="has_hand_drying_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_hand_washing_source_id",
        db_column_name="has_hand_washing_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_hot_water_source_id",
        db_column_name="has_hot_water_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_paper_source_id",
        db_column_name="has_paper_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_seated_source_id",
        db_column_name="has_seated_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_shower_source_id",
        db_column_name="has_shower_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_soap_source_id",
        db_column_name="has_soap_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_squat_source_id",
        db_column_name="has_squat_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="has_urinal_source_id",
        db_column_name="has_urinal_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="is_customer_only_source_id",
        db_column_name="is_customer_only_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="male_source_id",
        db_column_name="male_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="opening_times_source_id",
        db_column_name="opening_times_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="operator_source_id",
        db_column_name="operator_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="overpass_node_data_source_id",
        db_column_name="overpass_node_data_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="overpass_node_id_source_id",
        db_column_name="overpass_node_id_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="unisex_source_id",
        db_column_name="unisex_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="wheelchair_access_info_source_id",
        db_column_name="wheelchair_access_info_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    manager.add_column(
        table_class_name="DataAcquisitionDetailsToilet",
        tablename="da_details_toilet",
        column_name="wheelchair_accessible_source_id",
        db_column_name="wheelchair_accessible_source_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Sources,
            "on_delete": OnDelete.no_action,
            "on_update": OnUpdate.cascade,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
        },
    )

    return manager
