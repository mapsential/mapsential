from functools import cache
from typing import Callable, TypeVar

from asyncpg.exceptions import ForeignKeyViolationError
from db.tables import (
    Comments,
    Details, 
    DetailsDefibrillator, 
    DetailsDrinkingFountain, 
    DetailsSoupKitchen, 
    DetailsToilet
)
from db.tables import Locations
from enums import LocationType
import fastapi
from fastapi import FastAPI, HTTPException
from piccolo.columns import Column
from piccolo.table import Table
from piccolo.utils.pydantic import create_pydantic_model


api = FastAPI()


TableSpecialization = TypeVar("TableSpecialization", bound=Table)


@api.get("/locations")
async def get_locations(types: list[LocationType] = fastapi.Query(alias="type", default=[])):
    if len(types) == 0:
        return await select_columns_from_locations()

    return await select_columns_from_locations().where(Locations.type.is_in([type_.value for type_ in types]))


@api.get("/location/{location_id}")
async def get_location(location_id: int):
    return await select_columns_from_locations().where(Locations.id == location_id)


@api.get("/detail/{location_type}/{detail_id}")
async def get_detail(location_type: LocationType, detail_id: int):
    return await select_columns_from_details(location_type).where(
        get_details_table_from_location_type(location_type).id == detail_id
    )


@api.get("/comments/")
async def get_comment(location_id: int):
    return await Comments.select().where(Comments.location_id == location_id)


@api.get("/comment/{comment_id}")
async def get_comment(comment_id: int):
    return await Comments.select().where(Comments.id == comment_id)


CommentCreationModel = create_pydantic_model(
    Comments, 
    exclude_columns=(
        Comments.id,
        Comments.timestamp,
    )
)


@api.post("/comment/")
async def create_comment(comment: CommentCreationModel):
    try:
        await Comments.insert(Comments(**comment.dict()))
    except ForeignKeyViolationError as err:
        raise HTTPException(
            status_code=409, 
            detail=f"No location exists with id={comment.location_id}",
        ) from err


def select_columns_from_locations():
    return Locations.select(*get_api_columns(Locations))


def select_columns_from_details(location_type: LocationType):
    table = get_details_table_from_location_type(location_type)

    return table.select(*get_details_api_columns_by_location_type(location_type))


def get_details_api_columns_by_location_type(location_type: LocationType) -> list[Column]:
    return get_api_columns(get_details_table_from_location_type(location_type))


@cache
def get_details_table_from_location_type(location_type: LocationType) -> Details:
    match location_type:
        case LocationType.DEFIBRILLATOR:
            return DetailsDefibrillator
        case LocationType.DRINKING_FOUNTAIN:
            return DetailsDrinkingFountain
        case LocationType.SOUP_KITCHEN:
            return DetailsSoupKitchen
        case LocationType.TOILET:
            return DetailsToilet
        case _:
            raise ValueError(f"Invalid location_type '{_}'")


@cache
def get_api_columns(table: TableSpecialization):
    excluders: list[Callable[[str], bool]] = (
        is_not_column,
        starts_with_underscores,
        ends_with_source_id,
    )

    columns: list[Column] = []
    
    for attr in table.__dict__:
        if any(func(table, attr) for func in excluders):
            continue

        columns.append(table.__dict__[attr])

    return columns


def is_not_column(table: TableSpecialization, attr: str) -> bool:
    return not isinstance(table.__dict__[attr], Column)


def starts_with_underscores(_: TableSpecialization, attr: str) -> bool:
    return attr.startswith("_")


def ends_with_source_id(_: TableSpecialization, attr: str) -> bool:
    return attr.endswith("source_id")