import asyncio
import datetime
from typing import Any
from typing import Optional
from typing import Type
from typing import TypedDict
from typing import TypeVar

from admin.tables import DataAcquisitionDetails
from admin.tables import DataAcquisitionDetailsDefibrillator
from admin.tables import DataAcquisitionDetailsDrinkingFountain
from admin.tables import DataAcquisitionDetailsSoupKitchen
from admin.tables import DataAcquisitionDetailsToilet
from admin.tables import DataAcquisitionLocations
from admin.tables import Details
from admin.tables import DetailsDefibrillator
from admin.tables import DetailsDrinkingFountain
from admin.tables import DetailsSoupKitchen
from admin.tables import DetailsToilet
from admin.tables import Locations
from admin.tables import Sources
from enums import HandDryingMethod
from enums import LocationType
from enums import YesNoLimited
from errors import DatabaseCrudError
from piccolo.columns.combination import WhereRaw
from piccolo.table import Table
from utils.humanize import humanize_iterable
from utils.humanize import quote


T = TypeVar("T")


class InsertResult(TypedDict):
    id: int


InsertResults = list[InsertResult]


# Sources
# ============================================================================


async def create_or_update_source(
        name: str,
        url: str,
        access_time: datetime.datetime,
) -> int:
    rows = await Sources.select().where(Sources.url == url).run()

    if len(rows) == 0:
        return await create_source(name, url, access_time)

    return await update_source(rows[0]["id"], name, access_time)


async def create_source(
    name: str,
    url: str,
    access_time: datetime.datetime
) -> int:
    result = await Sources.insert(Sources(
        name=name,
        url=url,
        initial_access=access_time,
        last_access=access_time,
    )).run()

    return result[0]["id"]


async def update_source(
        id: int,
        name: str,
        access_time: datetime.datetime
) -> int:
    await Sources.update({
        Sources.name: name,
        Sources.last_access: access_time
    }).where(WhereRaw(f"id = '{id}'")).run()

    return id


# Details
# ============================================================================

# Defibrillator Details
# ----------------------------------------------------------------------------


def construct_details_defibrillator_and_da_row(
        *,
        operator: Optional[str],
        operator_source_id: Optional[int],
        opening_times: Optional[str],
        opening_times_source_id: Optional[int],
        street: Optional[str],
        street_source_id: Optional[int],
        city: Optional[str],
        city_source_id: Optional[int],
        postal_code: Optional[str],
        postal_code_source_id: Optional[int],
        country: Optional[str],
        country_source_id: Optional[int],
        json_data: Optional[T],
        json_data_source_id: Optional[int],
):
    assert postal_code is not None and len(postal_code) == 5 and postal_code.isnumeric(), DatabaseCrudError(
        f"`postal_code` must be a 5 character long string of numbers\n`postal_code={postal_code}`"
    )

    column_values = dict(
        operator=operator,
        operator_source_id=operator_source_id,
        opening_times=opening_times,
        opening_times_source_id=opening_times_source_id,
    )

    da_column_values = dict(
        street=street,
        street_source_id=street_source_id,
        city=city,
        city_source_id=city_source_id,
        postal_code=postal_code,
        postal_code_source_id=postal_code_source_id,
        country=country,
        country_source_id=country_source_id,
        json_data=json_data,
        json_data_source_id=json_data_source_id,
    )

    return construct_table_and_da_table_rows(
        table=DetailsDefibrillator,
        da_table=DataAcquisitionDetailsDefibrillator,
        column_values=column_values,
        da_column_values=da_column_values,
    )


# Drinking Fountain Details
# ----------------------------------------------------------------------------


def construct_details_drinking_fountain_and_da_row(
        *,
        operator: Optional[str],
        operator_source_id: Optional[int],
        opening_times: Optional[str],
        opening_times_source_id: Optional[int],
        google_maps_kml_placemark: Optional[T],
        google_maps_kml_placemark_source_id: Optional[int],
):
    column_values = dict(
        operator=operator,
        operator_source_id=operator_source_id,
        opening_times=opening_times,
        opening_times_source_id=opening_times_source_id,
    )

    da_column_values = dict(
        google_maps_kml_placemark=google_maps_kml_placemark,
        google_maps_kml_placemark_source_id=google_maps_kml_placemark_source_id,
    )

    return construct_table_and_da_table_rows(
        table=DetailsDrinkingFountain,
        da_table=DataAcquisitionDetailsDrinkingFountain,
        column_values=column_values,
        da_column_values=da_column_values,
    )


# Soup Kitchen Details
# ----------------------------------------------------------------------------


def construct_details_soup_kitchen_and_da_row(
        *,
        operator: Optional[str],
        operator_source_id: Optional[int],
        opening_times: Optional[str],
        opening_times_source_id: Optional[int],
        info: Optional[str],
        info_source_id: Optional[int],
        json_data: Optional[T],
        json_data_source_id: Optional[int],
):
    column_values = dict(
        operator=operator,
        operator_source_id=operator_source_id,
        opening_times=opening_times,
        opening_times_source_id=opening_times_source_id,
        info=info,
        info_source_id=info_source_id,
    )

    da_column_values = dict(
        json_data=json_data,
        json_data_source_id=json_data_source_id,
    )

    return construct_table_and_da_table_rows(
        table=DetailsSoupKitchen,
        da_table=DataAcquisitionDetailsSoupKitchen,
        column_values=column_values,
        da_column_values=da_column_values,
    )


# Toilet Details
# ----------------------------------------------------------------------------


def construct_details_toilet_and_da_row(
        *,
        operator: Optional[str],
        operator_source_id: Optional[int],
        opening_times: Optional[str],
        opening_times_source_id: Optional[int],

        has_fee: Optional[bool],
        has_fee_source_id: Optional[int],
        is_customer_only: Optional[bool],
        is_customer_only_source_id: Optional[int],

        female: Optional[bool],
        female_source_id: Optional[int],
        male: Optional[bool],
        male_source_id: Optional[int],
        unisex: Optional[bool],
        unisex_source_id: Optional[int],
        child: Optional[bool],
        child_source_id: Optional[int],

        has_seated: Optional[bool],
        has_seated_source_id: Optional[int],
        has_urinal: Optional[bool],
        has_urinal_source_id: Optional[int],
        has_squat: Optional[bool],
        has_squat_source_id: Optional[int],

        change_table: Optional[YesNoLimited],
        change_table_source_id: Optional[int],

        wheelchair_accessible: Optional[YesNoLimited],
        wheelchair_accessible_source_id: Optional[int],
        wheelchair_access_info: Optional[str],
        wheelchair_access_info_source_id: Optional[int],

        has_hand_washing: Optional[bool],
        has_hand_washing_source_id: Optional[int],
        has_soap: Optional[bool],
        has_soap_source_id: Optional[int],
        has_hand_disinfectant: Optional[bool],
        has_hand_disinfectant_source_id: Optional[int],
        has_hand_creme: Optional[bool],
        has_hand_creme_source_id: Optional[int],
        has_hand_drying: Optional[bool],
        has_hand_drying_source_id: Optional[int],
        hand_drying_method: Optional[HandDryingMethod],
        hand_drying_method_source_id: Optional[int],
        has_paper: Optional[bool],
        has_paper_source_id: Optional[int],
        has_hot_water: Optional[bool],
        has_hot_water_source_id: Optional[int],
        has_shower: Optional[bool],
        has_shower_source_id: Optional[int],
        has_drinking_water: Optional[bool],
        has_drinking_water_source_id: Optional[int],

        osm_node_id: Optional[int],
        osm_node_id_source_id: Optional[int],
        osm_node_data: Optional[T],
        osm_node_data_source_id: Optional[int],
):
    column_values = dict(
        operator=operator,
        operator_source_id=operator_source_id,
        opening_times=opening_times,
        opening_times_source_id=opening_times_source_id,

        has_fee=has_fee,
        has_fee_source_id=has_fee_source_id,
        is_customer_only=is_customer_only,
        is_customer_only_source_id=is_customer_only_source_id,

        female=female,
        female_source_id=female_source_id,
        male=male,
        male_source_id=male_source_id,
        unisex=unisex,
        unisex_source_id=unisex_source_id,
        child=child,
        child_source_id=child_source_id,

        has_seated=has_seated,
        has_seated_source_id=has_seated_source_id,
        has_urinal=has_urinal,
        has_urinal_source_id=has_urinal_source_id,
        has_squat=has_squat,
        has_squat_source_id=has_squat_source_id,

        change_table=change_table,
        change_table_source_id=change_table_source_id,

        wheelchair_accessible=wheelchair_accessible,
        wheelchair_accessible_source_id=wheelchair_accessible_source_id,
        wheelchair_access_info=wheelchair_access_info,
        wheelchair_access_info_source_id=wheelchair_accessible_source_id,

        has_hand_washing=has_hand_washing,
        has_hand_washing_source_id=has_hand_washing_source_id,
        has_soap=has_soap,
        has_soap_source_id=has_soap_source_id,
        has_hand_disinfectant=has_hand_disinfectant,
        has_hand_disinfectant_source_id=has_hand_disinfectant_source_id,
        has_hand_creme=has_hand_creme,
        has_hand_creme_source_id=has_hand_creme_source_id,
        has_hand_drying=has_hand_drying,
        has_hand_drying_source_id=has_hand_drying_source_id,
        hand_drying_method=hand_drying_method,
        hand_drying_method_source_id=hand_drying_method_source_id,
        has_paper=has_paper,
        has_paper_source_id=has_paper_source_id,
        has_hot_water=has_hot_water,
        has_hot_water_source_id=has_hot_water_source_id,
        has_shower=has_shower,
        has_shower_source_id=has_shower_source_id,
        has_drinking_water=has_drinking_water,
        has_drinking_water_source_id=has_drinking_water_source_id,
    )

    da_column_values = dict(
        osm_node_id=osm_node_id,
        osm_node_id_source_id=osm_node_id_source_id,
        osm_node_data=osm_node_data,
        osm_node_data_source_id=osm_node_data_source_id,
    )

    return construct_table_and_da_table_rows(
        table=DetailsToilet,
        da_table=DataAcquisitionDetailsToilet,
        column_values=column_values,
        da_column_values=da_column_values,
    )


# ----------------------------------------------------------------------------


def get_detail_tables_by_location_type(locations_type: LocationType) -> tuple[Type[Table], Type[Table]]:
    if locations_type is LocationType.DEFIBRILLATOR:
        return DetailsDefibrillator, DataAcquisitionDetailsDefibrillator
    elif locations_type is LocationType.DRINKING_FOUNTAIN:
        return DetailsDrinkingFountain, DataAcquisitionDetailsDrinkingFountain
    elif locations_type is LocationType.SOUP_KITCHEN:
        return DetailsSoupKitchen, DataAcquisitionDetailsSoupKitchen
    elif locations_type is LocationType.TOILET:
        return DetailsToilet, DataAcquisitionDetailsToilet
    else:
        raise DatabaseCrudError(f"Could not find details tables for location type \"{locations_type}\"")


async def delete_all_details_by_location_type(locations_type: LocationType) -> None:
    details_table, da_details_table = get_detail_tables_by_location_type(locations_type)

    await asyncio.gather(
        details_table.delete(force=True).run(),
        details_table.delete(force=True).run(),
    )


async def insert_details(
        details: list[Details],
        da_details: list[DataAcquisitionDetails],
) -> tuple[InsertResults, InsertResults]:
    if len(details) != len(da_details):
        raise DatabaseCrudError(
            "Insert requires an equal number of `details` and `da_details`"
        )

    if len(details) == 0:
        return [], []

    details_type = type(details[0])
    da_details_table_type = type(da_details[0])

    details_insert_results = await details_type.insert(*details).run()

    # Add one-sided 1:1 relationship from `da_details` to `details`
    for da_detail, detail_insert_result in zip(da_details, details_insert_results):
        da_detail.details_id = detail_insert_result["id"]

    da_details_insert_results = await da_details_table_type.insert(*da_details).run()

    return details_insert_results, da_details_insert_results


# Locations
# ============================================================================


def construct_locations_and_da_row(
        *,
        type: LocationType,
        name: str,
        name_source_id: int,
        address: str,
        address_source_id: int,
        latitude: float,
        latitude_source_id: int,
        longitude: float,
        longitude_source_id: int,
        details_id: Optional[int] = None,
):
    column_values = dict(
        type=type,
        name=name,
        name_source_id=name_source_id,
        address=address,
        address_source_id=address_source_id,
        latitude=latitude,
        latitude_source_id=latitude_source_id,
        longitude=longitude,
        longitude_source_id=longitude_source_id,
        details_id=details_id,
    )

    da_column_values: dict = dict()

    return construct_table_and_da_table_rows(
        table=Locations,
        da_table=DataAcquisitionLocations,
        column_values=column_values,
        da_column_values=da_column_values,
    )


async def delete_all_locations_by_type(type_: LocationType) -> None:
    await asyncio.gather(
        Locations.delete().where(Locations.type == type_).run(),
        DataAcquisitionLocations.delete().where(DataAcquisitionLocations.type == type_).run(),
        delete_all_details_by_location_type(type_),
    )


async def insert_locations(
        locations_rows: list[Locations],
        da_locations_rows: list[DataAcquisitionLocations],
) -> tuple[InsertResults, InsertResults]:
    if len(locations_rows) != len(da_locations_rows):
        raise DatabaseCrudError(
            "Insert requires an equal number of `locations` and `da_locations`"
        )

    if len(locations_rows) == 0:
        return [], []

    locations_insert_results = await Locations.insert(*locations_rows).run()

    # Add one-sided 1:1 relationship from `da_locations` to `locations`
    for da_locations_row, locations_insert_result in zip(da_locations_rows, locations_insert_results):
        da_locations_row.locations_id = locations_insert_result["id"]

    da_locations_insert_results = await DataAcquisitionLocations.insert(*da_locations_rows).run()

    return locations_insert_results, da_locations_insert_results


# ============================================================================


async def repopulate_with_locations_and_details(
        locations_type: LocationType,
        locations_rows: list[Locations],
        da_locations_rows: list[DataAcquisitionLocations],
        details_rows: list[Details],
        da_detail_rows: list[DataAcquisitionDetails],
) -> None:
    await delete_all_locations_by_type(locations_type)

    details_insert_results, da_details_insert_results = await insert_details(
        details_rows,
        da_detail_rows,
    )

    # Add one-sided 1:1 relationship from `location` to `details`
    for locations_row, details_insert_result in zip(locations_rows, details_insert_results):
        locations_row.details_id = details_insert_result["id"]

    # Add one-sided 1:1 relationship from `da_location` to `da_details`
    for da_locations_row, da_details_insert_result in zip(da_locations_rows, da_details_insert_results):
        da_locations_row.details_id = da_details_insert_result["id"]

    await insert_locations(locations_rows, da_locations_rows)


def construct_table_and_da_table_rows(
        table: Type[Table],
        da_table: Type[Table],
        column_values: dict[str, Any],
        da_column_values: dict[str, Any],
) -> tuple[Table, Table]:
    """
    Returns a tuple containing an instance of `table` and one of `da_table`.

    `table` is initialized with the arguments from `column_values`, whereas
    `da_table` is initialized with the arguments from `column_values` and `da_column_values`.
    Consequently, `da_column_values` may only extend `column_values`. If `column_values` and
    `da_columns` contain columns of the same name (keys), then an exception is raised.
    """

    # Raise an exception if keys clash
    common_keys = column_values.keys() & da_column_values.keys()
    if len(common_keys) > 0:
        raise DatabaseCrudError(
            "`column_values` and `da_column_values` must not contain the same "
            f"{'keys' if len(column_values) > 1 else 'key'}: "
            f"{humanize_iterable(common_keys, str_transformation=quote)}"
        )

    all_column_values = column_values | da_column_values

    # Raise an exception if `<column_name>` is set, but `<column_name>_source_id` is `None`
    for column_name, column_value in all_column_values.items():
        if column_value is not None:
            try:
                column_source_id_name = f"{column_name}_source_id"
                column_source_id_value = all_column_values[column_source_id_name]
                assert all_column_values[f"{column_name}_source_id"] is not None, DatabaseCrudError(
                    "The source id for a column must be set if the column is set\n"
                    f"`{column_name}={column_value}; {column_source_id_name}={column_source_id_value} "
                    f"=> {column_source_id_name} != {column_source_id_value}`"
                )
            except KeyError:
                pass

    return table(**column_values), da_table(**column_values, **da_column_values)
