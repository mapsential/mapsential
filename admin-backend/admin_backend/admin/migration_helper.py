import abc
import datetime
import json
import sqlite3
from collections import deque
from enum import Enum
from pathlib import Path
from typing import cast
from typing import Generic
from typing import Iterable
from typing import Literal
from typing import Optional
from typing import TypeVar
from typing import Union

from db_backup import backup_sqlite_db
from paths import DB_PATH
from piccolo.apps.migrations.auto import MigrationManager


T = TypeVar("T")


class Member(Generic[T]):
    value: T


class MemberIterable(Iterable[Member[T]]):
    pass


sqlite_connection = sqlite3.connect(DB_PATH)


def create_forwards_for_sql_files(
    file_path,
    *args,
    **kwargs,
):
    file_path = Path(file_path).resolve()
    path_stem = file_path.stem
    migrations_path = file_path.parent
    sql_migrate_file_path = migrations_path / f"{path_stem}_migrate.sql"
    sql_revert_file_path = migrations_path / f"{path_stem}_revert.sql"

    async def forwards():
        manager = MigrationManager(*args, **kwargs)

        def migrate():
            backup_sqlite_db(sqlite_connection, type_="before_migration")

            _execute_sql_script(sql_migrate_file_path)

        def revert():
            backup_sqlite_db(sqlite_connection, type_="before_migration_revert")

            _execute_sql_script(sql_revert_file_path)

        manager.add_raw(migrate)
        manager.add_raw_backwards(revert)

        return manager

    return forwards


def _execute_sql_script(sql_script_path: Path):
    with open(sql_script_path) as sql_script:
        script_string = sql_script.read()
        sqlite_connection.executescript(script_string)


class SqliteSqlFilesGenerator:

    class Column(Generic[T]):

        def __init__(
                self,
                name: str,
                null: Optional[bool] = False,
                unique: Optional[bool] = False,
                default: Optional[T] = None,
                with_sources_columns: bool = False
        ):
            self.name = name
            self.null = null
            self.unique = unique
            self.default = default
            self.with_sources_columns = with_sources_columns

        def get_column_defs(self, indent: str) -> list[str]:
            non_source_column_def = self.add_column_def_end(f"{self.name} {self.get_column_type_def(indent)}")

            if self.with_sources_columns:
                return [
                    non_source_column_def,
                    f"{self.name}_source_id INTEGER",
                ]

            return [non_source_column_def]

        @abc.abstractmethod
        def get_column_type_def(self, indent: str) -> str:
            ...

        def add_column_def_end(self, column_def: str) -> str:
            return self.add_not_null_to_column_def(
                self.add_unique_to_column_def(
                    self.add_default_to_column_def(
                        column_def
                    )
                )
            )

        def add_unique_to_column_def(self, column_def: str) -> str:
            if self.unique:
                return f"{column_def} UNIQUE"
            return column_def

        def add_not_null_to_column_def(self, column_def: str) -> str:
            if self.null:
                return column_def
            return f"{column_def} NOT NULL"

        def add_default_to_column_def(self, column_def: str) -> str:
            if self.default is None:
                return column_def

            if type(self.default) is bool:
                return f"{column_def} DEFAULT {int(self.default)}"

            if type(self.default) is str:
                return f"{column_def} DEFAULT '{self.default}'"

            return f"{column_def} DEFAULT {self.default}"

        def get_constraints(self, indent: str) -> list[str]:
            if self.with_sources_columns:
                return [
                    f"FOREIGN KEY({self.name}_source_id) REFERENCES sources(id)\n"
                    f"{indent}ON DELETE NO ACTION\n"
                    f"{indent}ON UPDATE CASCADE"
                ]

            return []

    class Integer(Column[int]):

        def get_column_type_def(self, indent: str):
            return f"INTEGER"

    class PrimaryKey(Integer):

        def get_column_type_def(self, indent: str) -> str:
            return f"{super().get_column_type_def(indent)} PRIMARY KEY"

    class ForeignKey(Integer):
        def __init__(
                self, name: str,
                references: str,
                references_column_name: str = "id",
                on_delete: Literal["cascade", "restrict", "no_action", "set_null", "set_default"] = "cascade",
                on_update: Literal["cascade", "restrict", "no_action", "set_null", "set_default"] = "cascade",
                **kwargs
        ):
            super().__init__(name, **kwargs)
            self.references = references
            self.references_column_name = references_column_name
            self.on_delete = on_delete
            self.on_update = on_update

        def get_constraints(self, indent: str) -> list[str]:
            return [
                f"FOREIGN KEY({self.name}) REFERENCES {self.references}({self.references_column_name})\n"
                f"{indent}ON DELETE {self.on_delete.replace('_', ' ').upper()}\n"
                f"{indent}ON UPDATE {self.on_update.replace('_', ' ').upper()}",
            ]

    class Boolean(Integer):
        def __init__(self, name: str, default: Optional[bool] = None, **kwargs):
            if default is None:
                integer_default = None
            else:
                integer_default = int(default)
            super().__init__(name, default=integer_default, **kwargs)

        def get_constraints(self, indent: str) -> list[str]:
            return [f"CONSTRAINT check_{self.name}_is_bool\n{indent}CHECK ({self.name} = 0 OR {self.name} = 1)"]

    class Varchar(Column[str]):
        def __init__(
                self,
                name: str,
                length: Optional[int] = None,
                choices: Optional[T] = None,
                **kwargs,
        ):
            super().__init__(name, **kwargs)
            self.length = length
            self.choices = cast(MemberIterable[str], choices)

        def get_column_type_def(self, indent: str) -> str:
            if self.length is None:
                return f"VARCHAR"
            return f"VARCHAR({self.length})"

        def get_constraints(self, indent: str) -> list[str]:
            if self.choices is not None:
                choices_str = ", ".join(f"'{mem.value}'" for mem in self.choices)
                return [
                    f"CONSTRAINT check_{self.name}_matches_choices\n{indent}CHECK ({self.name} IN ({choices_str}))"
                ]
            return []

    class Text(Column[str]):

        def get_column_type_def(self, indent: str) -> str:
            return "TEXT"

    # Timestamps are saved by piccolo as strings in ISO-format
    class Timestamp(Text):
        def __init__(self, name: str, default: Optional[datetime.datetime] = None, **kwargs):
            if default is None:
                default_text = None
            else:
                default_text = self.default_to_iso_date_str(default)

            super().__init__(name, default=default_text, **kwargs)

        def default_to_iso_date_str(self, default: datetime.datetime) -> str:
            raise NotImplementedError

    # JSON is stored as serialized strings by piccolo.
    class JSON(Text):
        def __init__(self, name: str, default: Optional[Union[str, list, dict]] = None, **kwargs):
            if default is None:
                text_default = None
            else:
                text_default = json.dumps(default)

            super().__init__(name, default=text_default, **kwargs)

    class Real(Column[float]):

        def get_column_type_def(self, indent: str) -> str:
            return "REAL"

    class Decimal(Column):
        def __init__(self, name: str, digits: tuple[int, int], default: Optional[float] = None, **kwargs):
            super().__init__(name, default=default, **kwargs)
            self.digits = digits

        def get_column_type_def(self, indent: str) -> str:
            return f"DECIMAL({self.digits[0]}, {self.digits[1]})"

    def __init__(self, file_path, indent=" "*4):
        file_path = Path(file_path).resolve()
        migrations_path = file_path.parent
        self.migrate_file_path = migrations_path / f"{file_path.stem}_migrate.sql"
        self.revert_file_path = migrations_path / f"{file_path.stem}_revert.sql"

        self.indent = indent

        self.migrate_sql_commands: list[str] = []
        self.revert_sql_commands: deque[str] = deque()

    def __enter__(self):
        return self

    def __exit__(self, _, error, *__):
        # Do not write to files if error is raised in body.
        if error is not None:
            raise error

        self.write()

    def write(self):
        with open(self.migrate_file_path, "w") as migrate_file:
            migrate_file.write("\n\n".join(self.migrate_sql_commands))

        with open(self.revert_file_path, "w") as revert_file:
            revert_file.write("\n\n".join(self.revert_sql_commands))

    def add_raw_sql(self, migrate: str, revert: Optional[str]):
        self.migrate_sql_commands.append(migrate)
        if revert is not None:
            self.revert_sql_commands.appendleft(revert)

    def create_table(self, table_name: str, columns: Optional[list[Column]] = None, add_primary_key: bool = True):
        if columns is None:
            columns = []
        else:
            columns = list(columns)

        if add_primary_key:
            columns.insert(0, self.PrimaryKey("id"))

        drop_command = f"DROP TABLE {table_name};"
        create_command_start = f"CREATE TABLE {table_name}"

        column_defs = []
        constraints = []
        for column in columns:
            column_defs.extend(column.get_column_defs(2 * self.indent))
            constraints.extend(column.get_constraints(2 * self.indent))

        inner = f",\n{self.indent}".join(column_defs + constraints)
        self.add_raw_sql(
            migrate=(
                f"{create_command_start} (\n{self.indent}{inner}\n);"
            ),
            revert=drop_command,
        )

    def add_column(self, table_name: str, column: Column):
        self.add_raw_sql(
            migrate=f"ALTER TABLE {table_name} ADD {column.get_column_defs(self.indent)};",
            revert=self._get_drop_column_sql_command(table_name, column),
        )

        for constraint in column.get_constraints(self.indent):
            self.add_raw_sql(
                migrate=f"ALTER TABLE {table_name} ADD {constraint};",
                revert=None,
            )

    @staticmethod
    def _get_drop_column_sql_command(table_name: str, column: Column):
        raise NotImplementedError(
            "Python 3.9 uses old sqlite that does not support drop column. "
            "TODO: Implement workaround -> see https://www.sqlite.org/faq.html#q11"
        )

    def add_columns(self, table_name: str, columns: list[Column]):
        for column in columns:
            self.add_column(table_name, column)
