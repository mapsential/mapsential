import datetime
import os
import sqlite3

from paths import DB_BACKUPS_PATH


# see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
DATETIME_NAME_STR_FORMAT = "%Y_%m_%dT%H_%M_%S_%f"
BACK_PREFIX = "db_backup"
SQLITE_DB_EXT = ".sqlite"


def backup_sqlite_db(db_connection, type_=None, delete_oldest_if_more_than: int = 3):
    backup_db_path = DB_BACKUPS_PATH / get_sqlite_backup_db_name(type_=type_)
    backup_db_connection = sqlite3.connect(backup_db_path)
    with backup_db_connection:
        db_connection.backup(backup_db_connection)
    backup_db_connection.close()

    remove_old_backups(DB_BACKUPS_PATH, delete_oldest_if_more_than=delete_oldest_if_more_than)


def get_sqlite_backup_db_name(type_=None):
    if type_ is None:
        suffix = SQLITE_DB_EXT
    else:
        suffix = f"_{type_}{SQLITE_DB_EXT}"

    return f"{BACK_PREFIX}_{get_datetime_name_str()}{suffix}"


def get_datetime_name_str():
    now = datetime.datetime.now()
    return now.strftime(DATETIME_NAME_STR_FORMAT)


def remove_old_backups(db_backups_path, delete_oldest_if_more_than: int):
    db_file_count = 0
    for child in sorted(db_backups_path.iterdir(), key=lambda path: os.path.getctime(path)):
        if child.is_file() and child.suffix == SQLITE_DB_EXT:
            if db_file_count >= delete_oldest_if_more_than:
                child.unlink()
            else:
                db_file_count += 1
