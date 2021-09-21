from typing import Any
from typing import Type

from admin.migration_helper import create_forwards_for_sql_files
from admin.migration_helper import SqliteSqlFilesGenerator
from enums import HandDryingMethod
from enums import LocationType
from enums import YesNoLimited


ID = "2021-09-20T13:56:47:375450"
VERSION = "0.49.0"
DESCRIPTION = ""


with SqliteSqlFilesGenerator(__file__) as gen:
    def get_location_mixin_columns():
        return [
            gen.Varchar("type", length=127, choices=LocationType),
            gen.Varchar("name", length=255, with_sources_columns=True),
            gen.Varchar("address", with_sources_columns=True),
            gen.Real("longitude", with_sources_columns=True),
            gen.Real("latitude", with_sources_columns=True),
        ]

    gen.create_table("locations", [
        *get_location_mixin_columns(),
        gen.ForeignKey("details_id", references="details", unique=True),
    ])

    gen.create_table("da_locations", [
        *get_location_mixin_columns(),
        gen.Integer("details_id"),
    ])

    def get_details_mixin_columns():
        return [
            gen.Varchar("operator", length=255, null=True, with_sources_columns=True),
        ]

    def get_details_opening_time_mixin():
        return [
            gen.Text("opening_times", null=True, with_sources_columns=True),
        ]

    def get_common_soup_kitchen_details(column_name_prefix: str = ""):
        column_data: list[tuple[str, Type[SqliteSqlFilesGenerator.Column], list[Any], dict[str, Any]]] = [
            ("info", gen.JSON, [], {"null": True})
        ]

        columns = []
        for column_name, column_cls, args, kwargs in column_data:
            kwargs["with_sources_columns"] = True
            columns.append(column_cls(f"{column_name_prefix}{column_name}", *args, **kwargs))

        return columns

    def get_common_toilet_details(column_name_prefix: str = ""):
        column_data: list[tuple[str, Type[SqliteSqlFilesGenerator.Column], list[Any], dict[str, Any]]] = [
            ("has_fee", gen.Boolean, [], {"null": True}),
            ("fee", gen.Decimal, [(4, 2)], {"null": True}),
            ("is_customer_only", gen.Boolean, [], {"null": True}),

            ("female", gen.Boolean, [], {"null": True}),
            ("male", gen.Boolean, [], {"null": True}),
            ("unisex", gen.Boolean, [], {"null": True}),
            ("child", gen.Boolean, [], {"null": True}),

            ("has_seated", gen.Boolean, [], {"null": True}),
            ("has_urinal", gen.Boolean, [], {"null": True}),
            ("has_squat", gen.Boolean, [], {"null": True}),

            ("change_table", gen.Varchar, [], {"null": True, "length": 31, "choices": YesNoLimited}),

            ("wheelchair_accessible", gen.Varchar, [], {"null": True, "length": 31, "choices": YesNoLimited}),
            ("wheelchair_access_info", gen.Text, [], {"null": True}),

            ("has_hand_washing", gen.Boolean, [], {"null": True}),
            ("has_soap", gen.Boolean, [], {"null": True}),
            ("has_hand_disinfectant", gen.Boolean, [], {"null": True}),
            ("has_hand_creme", gen.Boolean, [], {"null": True}),
            ("has_hand_drying", gen.Boolean, [], {"null": True}),
            ("hand_drying_method", gen.Varchar, [], {"null": True, "choices": HandDryingMethod}),
            ("has_paper", gen.Boolean, [], {"null": True}),
            ("has_hot_water", gen.Boolean, [], {"null": True}),
            ("has_shower", gen.Boolean, [], {"null": True}),
            ("has_drinking_water", gen.Boolean, [], {"null": True}),
        ]

        columns = []
        for column_name, column_cls, args, kwargs in column_data:
            kwargs["with_sources_columns"] = True
            columns.append(column_cls(f"{column_name_prefix}{column_name}", *args, **kwargs))

        return columns

    gen.create_table("details", [
        *get_details_mixin_columns(),
        *get_details_opening_time_mixin(),
        *get_common_soup_kitchen_details(column_name_prefix="soup_kitchen_"),
        *get_common_toilet_details(column_name_prefix="toilet_"),
    ])

    gen.create_table("da_details_soup_kitchen", [
        *get_details_mixin_columns(),
        *get_details_opening_time_mixin(),
        *get_common_soup_kitchen_details(),
        gen.JSON("json_data", null=True, with_sources_columns=True),
    ])

    gen.create_table("da_details_drinking_fountain", [
        *get_details_mixin_columns(),
        *get_details_opening_time_mixin(),
        gen.JSON("google_maps_kml_placemark", null=True, with_sources_columns=True),
    ])

    gen.create_table("da_details_toilet", [
        *get_details_mixin_columns(),
        *get_details_opening_time_mixin(),
        gen.Integer("overpass_node_id", with_sources_columns=True),
        gen.JSON("overpass_node_data", with_sources_columns=True),
        *get_common_toilet_details(),
    ])

    gen.create_table("sources", [
        gen.Varchar("name", length=255),
        gen.Varchar("url", null="True", unique=True),
        gen.Timestamp("initial_access", null=True),
        gen.Timestamp("last_access", null=True),
    ])


forwards = create_forwards_for_sql_files(__file__, migration_id=ID, app_name="admin", description=DESCRIPTION)
