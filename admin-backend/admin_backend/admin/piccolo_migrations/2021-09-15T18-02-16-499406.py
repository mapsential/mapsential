from pathlib import Path
import sqlite3

from piccolo.apps.migrations.auto import MigrationManager

ID = "2021-09-15T18:02:16:499406"
VERSION = "0.47.0"
DESCRIPTION = "Create tables."
CURRENT_DIR = Path(__file__).resolve().parent
DB_PATH = CURRENT_DIR / "../../../../db/db.sqlite"


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="app", description=DESCRIPTION
    )

    def run():
        con = sqlite3.connect(DB_PATH)

        with open(CURRENT_DIR / "2021-09-15T18-02-16-499406_create_tables.sql") as sql_script:
            con.executescript(sql_script.read())

    def revert():
        con = sqlite3.connect(DB_PATH)

        with open(CURRENT_DIR / "2021-09-15T18-02-16-499406_drop_tables.sql") as sql_script:
            con.executescript(sql_script.read())

    manager.add_raw_backwards(revert)

    manager.add_raw(run)

    return manager
