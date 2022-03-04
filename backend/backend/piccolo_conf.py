import os

from passwords import get_password
from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine


BASE_POSTGRES_CONFIG = dict(
    port="5432",
    user="postgres",
    database="postgres",
    password=get_password("postgres/password"),
)


def get_postgres_prod_config() -> dict:
    return dict(
        **BASE_POSTGRES_CONFIG,
        host="localhost",
    )


def get_postgres_docker_dev_config() -> dict:
    return dict(
        **BASE_POSTGRES_CONFIG,
        host="db",
    )


def get_postgres_dev_config() -> dict:
    return dict(
        **BASE_POSTGRES_CONFIG,
        host="localhost",
    )


DB = PostgresEngine(
    config={
        "prod": get_postgres_prod_config(),
        "docker-dev": get_postgres_docker_dev_config(),
    }.get(os.environ["ENV"], get_postgres_dev_config())
)

APP_REGISTRY = AppRegistry(
    apps=["db.piccolo_app", "piccolo_admin.piccolo_app"]
)
