import datetime
from typing import Any

from admin.tables import Sources
from piccolo.columns.combination import WhereRaw


async def create_or_update_source(
        name: str,
        url: str,
        access_time: datetime.datetime,
) -> int:
    rows = await Sources.select().where(Sources.url == url).run()

    if len(rows) == 0:
        return await create_source(name, url, access_time)

    return await update_source(rows[0]["id"], name, access_time)


async def create_source(
    name: str,
    url: str,
    access_time: datetime.datetime
) -> int:
    result = await Sources.insert(Sources(
        name=name,
        url=url,
        initial_access=access_time,
        last_access=access_time,
    )).run()

    return result[0]["id"]


async def update_source(
        id: int,
        name: str,
        access_time: datetime.datetime
) -> int:
    await Sources.update({
        Sources.name: name,
        Sources.last_access: access_time
    }).where(WhereRaw(f"id = '{id}'")).run()

    return id
