from functools import cache
from typing import Callable
from typing import TypeVar

import fastapi
from asyncpg.exceptions import ForeignKeyViolationError
from enums import LocationType
from fastapi import FastAPI
from fastapi import HTTPException
from piccolo.columns import Column
from piccolo.table import Table
from piccolo.utils.pydantic import create_pydantic_model

from db.tables import Comments
from db.tables import Details
from db.tables import Locations


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


@api.get("/details/{detail_id}")
async def get_details(detail_id: int):
    return await select_columns_from_details().where(Details.id == detail_id)


@api.get("/comments/")
async def get_comments(location_id: int):
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
async def create_comment(comment: CommentCreationModel):  # type: ignore[valid-type]
    try:
        await Comments.insert(Comments(**comment.dict()))  # type: ignore[attr-defined]
    except ForeignKeyViolationError as err:
        raise HTTPException(
            status_code=409,
            detail=f"No location exists with id={comment.location_id}",  # type: ignore[attr-defined]
        ) from err


def select_columns_from_locations():
    return Locations.select(*get_api_columns(Locations))


def select_columns_from_details():
    return Details.select(*get_api_columns(Details))


@cache
def get_api_columns(table: TableSpecialization):
    excluders: tuple[Callable[[Table, str], bool], ...] = (
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
