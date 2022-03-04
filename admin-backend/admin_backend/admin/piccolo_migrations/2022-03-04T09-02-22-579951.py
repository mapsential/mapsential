from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.base import OnDelete
from piccolo.columns.base import OnUpdate
from piccolo.columns.column_types import ForeignKey
from piccolo.columns.column_types import Serial
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Timestamp
from piccolo.columns.column_types import Varchar
from piccolo.columns.defaults.timestamp import TimestampNow
from piccolo.columns.indexes import IndexMethod
from piccolo.table import Table


class Locations(Table, tablename="locations"):  # type: ignore
    id = Serial(
        null=False,
        primary_key=True,
        unique=False,
        index=False,
        index_method=IndexMethod.btree,
        choices=None,
        db_column_name="id",
        secret=False,
    )


ID = "2022-03-04T09:02:22:579951"
VERSION = "0.69.1"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="admin", description=DESCRIPTION
    )

    manager.add_table("Comments", tablename="comments")

    manager.add_column(
        table_class_name="Comments",
        tablename="comments",
        column_name="locations_id",
        db_column_name="locations_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Locations,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "target_column": None,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="Comments",
        tablename="comments",
        column_name="author_name",
        db_column_name="author_name",
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
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="Comments",
        tablename="comments",
        column_name="content",
        db_column_name="content",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="Comments",
        tablename="comments",
        column_name="timestamp",
        db_column_name="timestamp",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "default": TimestampNow(),
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    return manager
