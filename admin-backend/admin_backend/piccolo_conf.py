from piccolo.engine.sqlite import SQLiteEngine

from piccolo.conf.apps import AppRegistry

from paths import DB_PATH


DB = SQLiteEngine(path=str(DB_PATH))
APP_REGISTRY = AppRegistry(
    apps=["admin.piccolo_app", "piccolo_admin.piccolo_app"]
)
