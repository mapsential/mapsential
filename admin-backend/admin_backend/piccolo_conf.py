from paths import DB_PATH
from piccolo.conf.apps import AppRegistry
from piccolo.engine.sqlite import SQLiteEngine


DB = SQLiteEngine(path=str(DB_PATH))
APP_REGISTRY = AppRegistry(
    apps=["admin.piccolo_app", "piccolo_admin.piccolo_app"]
)
