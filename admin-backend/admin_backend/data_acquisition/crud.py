import datetime

from admin.tables import DataAcquisitionDetailsDrinkingFountain
from admin.tables import DataAcquisitionDetailsSoupKitchen
from admin.tables import DataAcquisitionDetailsToilet
from admin.tables import DataAcquisitionLocations
from admin.tables import Details
from admin.tables import Locations
from admin.tables import Sources
from enums import LocationType
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


async def delete_all_locations_by_type(type_: LocationType) -> None:
    # For some reason cascading deleting is not working in sqlite.
    # Because of this the rows in the 'details' table need to be deleted explicitly.
    to_be_deleted_details_ids = [
        row["id"] for row in await Locations.select().where(Locations.type == type_).run()
    ]
    if len(to_be_deleted_details_ids) > 0:
        await Details.delete().where(Details.id.is_in(to_be_deleted_details_ids)).run()

    await Locations.delete().where(Locations.type == type_).run()
    await DataAcquisitionLocations.delete().where(DataAcquisitionLocations.type == type_).run()

    if type_ is LocationType.TOILET:
        await DataAcquisitionDetailsToilet.delete(force=True)
    elif type_ is LocationType.DRINKING_FOUNTAIN:
        await DataAcquisitionDetailsDrinkingFountain.delete(force=True)
    elif type_ is LocationType.SOUP_KITCHEN:
        await DataAcquisitionDetailsSoupKitchen.delete(force=True)
    else:
        raise ValueError(f"Unknown location type '{type_}'")
