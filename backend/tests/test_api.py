import sys

sys.path.append("backend")

from unittest.mock import Mock
from backend.enums import LocationType

from piccolo.columns import Column
from piccolo.table import Table
import pytest

from backend.db.tables import (
    Locations,
    DetailsDefibrillator,
    DetailsDrinkingFountain,
    DetailsSoupKitchen,
    DetailsToilet,
)
from backend.api import get_api_columns, get_details_api_columns_by_location_type


Locations = Mock()


def test_get_api_columns_excludes_attrs_that_are_not_columns():
    id_column = Column("id")
    str_column = "str"

    class MyTable(Table):
        id = id_column
        s = str_column

    assert get_api_columns(MyTable) == [id_column]


def test_get_api_columns_excludes_attrs_starting_with_underscores():
    id_column = Column("id")
    private_column = Column("private_column")

    class MyTable(Table):
        id = id_column
        _private = private_column

    assert get_api_columns(MyTable) == [id_column]


def test_get_api_columns_excludes_attrs_ending_with_source_id():
    id_column = Column("id")
    my_column = Column("col")
    my_source_id_my_column = Column("col_source_id")

    class MyTable(Table):
        id = id_column
        col = my_column
        col_source_id = my_source_id_my_column

    assert get_api_columns(MyTable) == [id_column, my_column]


@pytest.mark.parametrize(
    "location_type,expected_columns,expected_excluded_columns",
    [
        (LocationType.DEFIBRILLATOR, {
            DetailsDefibrillator.id,
            DetailsDefibrillator.operator,
            DetailsDefibrillator.opening_times,
        }, {
            DetailsDefibrillator.operator_source_id,
            DetailsDefibrillator.opening_times_source_id,
        }),
        (LocationType.DRINKING_FOUNTAIN, {
            DetailsDrinkingFountain.id,
            DetailsDrinkingFountain.operator,
            DetailsDrinkingFountain.opening_times,
        }, {
            DetailsDrinkingFountain.operator_source_id,
            DetailsDrinkingFountain.opening_times_source_id,
        }),
        (LocationType.SOUP_KITCHEN, {
            DetailsSoupKitchen.id,
            DetailsSoupKitchen.operator,
            DetailsSoupKitchen.opening_times,
        }, {
            DetailsSoupKitchen.operator_source_id,
            DetailsSoupKitchen.opening_times_source_id,
        }),
        (LocationType.TOILET, {
            DetailsToilet.id,
            DetailsToilet.operator,
            DetailsToilet.opening_times,
            DetailsToilet.wheelchair_accessible,
            DetailsToilet.wheelchair_access_info,
        }, {
            DetailsToilet.operator_source_id,
            DetailsToilet.wheelchair_accessible_source_id,
            DetailsToilet.wheelchair_access_info_source_id,
        })
    ]
)
def test_get_details_api_columns_by_location_type_returns_correct_columns(
    location_type,
    expected_columns,
    expected_excluded_columns,
):
    columns_set = set(get_details_api_columns_by_location_type(location_type))

    assert expected_columns.issubset(columns_set)
    assert expected_excluded_columns & columns_set == set()