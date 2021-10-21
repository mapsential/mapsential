from env import is_production
from passwords import get_password
from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine


BASE_POSTGRES_CONFIG = dict(
    host="localhost",
    port="5432",
    user="postgres",
    database="postgres",
)


def get_postgres_production_config() -> dict:
    return dict(
        **BASE_POSTGRES_CONFIG,
        passfile="/run/secrets/postgres_password",
    )


def get_postgres_development_config() -> dict:
    return dict(
        **BASE_POSTGRES_CONFIG,
        password=get_password("postgres/password"),
    )


DB = PostgresEngine(
    config=get_postgres_production_config() if is_production() else get_postgres_development_config()
)

APP_REGISTRY = AppRegistry(
    apps=["admin.piccolo_app", "piccolo_admin.piccolo_app"]
)
