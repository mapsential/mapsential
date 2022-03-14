import sys

sys.path.append("backend")

from piccolo.columns import Column
from piccolo.table import Table
from backend.api import get_api_columns


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
