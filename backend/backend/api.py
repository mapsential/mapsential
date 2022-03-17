from datetime import datetime
from datetime import timedelta
from typing import Iterable
from typing import TypedDict
from typing import TypeVar

from asyncpg.exceptions import ForeignKeyViolationError
from constants import LOCATION_TYPE_NAMES
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from internationalized_terms import get_plural
from internationalized_terms import get_singular
from internationalized_terms import get_translation
from piccolo.engine import engine_finder
from piccolo.table import Table
from piccolo.utils.pydantic import create_pydantic_model

from db.tables import Comments
from db.tables import Details
from db.tables import Locations


TableSpecialization = TypeVar("TableSpecialization", bound=Table)

LocationsCompactResponse = dict[
    str,  # shortend location name
    "LocationCompactResponseRows",
]

class LocationCompactResponseRows(TypedDict):
    id: list[int]
    did: list[int]
    lat: list[float]
    lon: list[float]


MAX_LOCATIONS_LIMIT = 100
LOCATIONS_COMPACT_CACHE_DURATION = timedelta(hours=3)
LOCATION_TYPE_TRANSLATIONS = {
    country_code: {
        location_type_name: {
            "singular": get_singular(translated := get_translation(location_type_name.replace("_", " "), "de")),
            "plural": get_plural(translated),
        } for location_type_name in LOCATION_TYPE_NAMES
    } for country_code in ["de"]
}


# Setup
# ============================================================================


api = FastAPI()

locations_compact_cache: Iterable[LocationsCompactResponse]


# Use piccolo/asyncpg/postgres connection pool
@api.on_event('startup')
async def open_database_connection_pool():
    engine = engine_finder()
    await engine.start_connection_pool()

    global locations_compact_cache
    locations_compact_cache = create_locations_compact_cache()
    # Prime cache
    async for _ in locations_compact_cache:
        break


async def create_locations_compact_cache():
    cached_locations = await get_locations_compact_from_db()
    last_cache_refresh = datetime.now()

    while True:
        yield cached_locations

        # Only refresh cache after usage in order not to slow down response time
        if last_cache_refresh < (now := datetime.now()) - LOCATIONS_COMPACT_CACHE_DURATION:
            cached_locations = await get_locations_compact_from_db()
            last_cache_refresh = now


async def get_locations_compact_from_db() -> LocationsCompactResponse:
    compact: LocationsCompactResponse = {
        location_type_name: {"id": [], "did": [], "lat": [], "lon": []}
        for location_type_name in LOCATION_TYPE_NAMES
    }

    for location in (await Locations.select()):
        (rows := compact[location["type"]])["id"].append(location["id"])
        rows["did"].append(location["details_id"])
        rows["lat"].append(location["latitude"])
        rows["lon"].append(location["longitude"])

    return compact



@api.on_event('shutdown')
async def close_database_connection_pool():
    engine = engine_finder()
    await engine.close_connection_pool()


# Locations
# ============================================================================

# This endpoint is optimized for size and speed, because we return a lot of locations
@api.get("/locations-compact")
async def get_locations_compact():
    async for locations_compact in locations_compact_cache:
        return locations_compact


@api.get("/locations")
async def get_locations(
    skip: int,
    limit: int = Query(default=100, gt=0, lt=MAX_LOCATIONS_LIMIT + 1)
):
    return await Locations.select().order_by(Locations.id).offset(skip).limit(limit)


@api.get("/location/{location_id}")
async def get_location(location_id: int):
    return await Locations.select().where(Locations.id == location_id)


@api.get("/location-type-translations")
async def get_location_type_translations():
    return LOCATION_TYPE_TRANSLATIONS


# Details
# ============================================================================


@api.get("/details/{detail_id}")
async def get_details(detail_id: int):
    return await Details.select().where(Details.id == detail_id)


# Comments
# ============================================================================


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
