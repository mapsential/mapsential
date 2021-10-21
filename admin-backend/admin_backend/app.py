from admin.piccolo_app import APP_CONFIG
from env import is_production
from fastapi import FastAPI
from piccolo_admin.endpoints import create_admin
from starlette.routing import Mount


app = FastAPI(
    routes=[
        Mount(
            "/piccolo-admin/",
            create_admin(
                tables=APP_CONFIG.table_classes,
                production=is_production(),
                # Required when running under HTTPS:
                # allowed_hosts=['my_site.com']
            ),
        ),
    ],
)
