from datetime import datetime
from datetime import timedelta
from functools import lru_cache
from typing import cast
from typing import Iterable
from typing import TypedDict

from asyncpg.exceptions import ForeignKeyViolationError
from colors import CustomColor
from colors import get_values_and_nearest_colors
from constants import LOCATION_TYPE_NAMES
from enums import LocationType
from env import is_production
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from internationalized_terms import get_plural
from internationalized_terms import get_singular
from internationalized_terms import get_translation
from piccolo.engine import engine_finder
from pydantic import BaseModel
from pydantic import validator

from .captcha_util import CAPTCHA_TEXT_LENGTH
from .captcha_util import check_captcha_answer_and_delete
from .captcha_util import create_captcha_token_and_jpeg_str
from .captcha_util import generate_captcha_token
from db.tables import Comments
from db.tables import Details
from db.tables import Locations


# Setup
# ============================================================================


api = FastAPI(root_path="/api")


api.add_middleware(GZipMiddleware)


if is_production():
    api.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:8000",
            "http://localhost:8100",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    print("test")

else:
    api.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:8000",
            "http://localhost:8100",
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


locations_compact_cache: Iterable["LocationsCompactResponse"]


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


@api.on_event('shutdown')
async def close_database_connection_pool():
    engine = engine_finder()
    await engine.close_connection_pool()


# Locations
# ============================================================================


MAX_LOCATIONS_LIMIT = 100
LOCATIONS_COMPACT_CACHE_DURATION = timedelta(hours=3)
LOCATION_TYPE_TRANSLATION_COUNTRY_CODES = ["de"]
COLORS_LIGHTNESS = -0.2
LOCATION_TYPE_TO_TARGET_COLOR = {
    LocationType.DRINKING_FOUNTAIN.value: CustomColor.from_rgb((2, 126, 221)),  # Light blue
}


LocationsCompactResponse = dict[
    str,
    "LocationCompactResponseRows",
]

class LocationCompactResponseRows(TypedDict):
    id: list[int]
    did: list[int]
    lat: list[float]
    lon: list[float]
    trans: dict[str, "LocationTypeTranslationEntry"]
    color: str


class LocationTypeTranslationEntry(TypedDict):
    singular: str
    plural: str


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
        location_type_name: {
            "id": [],
            "did": [],
            "lat": [],
            "lon": [],
            "trans": {
                country_code: translations[location_type_name]
                for country_code, translations in generate_location_type_translations()
            },
            "color": color,
        }
        for location_type_name, color in get_location_types_and_colors()
    }

    for location in (await Locations.select()):
        location_type = location["type"]

        (rows := compact[location_type])["id"].append(location["id"])
        rows["did"].append(location["details_id"])
        rows["lat"].append(location["latitude"])
        rows["lon"].append(location["longitude"])

    return compact


@lru_cache(maxsize=1)
def generate_location_type_translations() -> list[tuple[str, dict[
    str,  # Country code
    LocationTypeTranslationEntry,
]]]:
    translations: list[tuple[str, dict[str, LocationTypeTranslationEntry]]] = []

    for country_code in LOCATION_TYPE_TRANSLATION_COUNTRY_CODES:
        translations_for_lang: dict[str, LocationTypeTranslationEntry] = {}
        for location_type in LOCATION_TYPE_NAMES:
            translation = get_translation(location_type.replace("_", " "), country_code)
            translations_for_lang[location_type] = {
                "singular": get_singular(translation),
                "plural": get_plural(translation),
            }

        translations.append((country_code, translations_for_lang))

    return translations


@lru_cache(maxsize=1)
def get_location_types_and_colors() -> list[tuple[str, str]]:
    location_types_and_target_colors = list(LOCATION_TYPE_TO_TARGET_COLOR.items())
    rest_location_types = [
        location_type for location_type in LOCATION_TYPE_NAMES
        if location_type not in LOCATION_TYPE_TO_TARGET_COLOR
    ]

    return [
        (location_type, color.to_hex())
        for location_type, color in get_values_and_nearest_colors(
            location_types_and_target_colors,
            rest_location_types,
            lightness=COLORS_LIGHTNESS,
        )
    ]


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
    return generate_location_type_translations()


# Details
# ============================================================================


@api.get("/details/{detail_id}")
async def get_details(detail_id: int):
    return (await Details.select().where(Details.id == detail_id))[0]


# Captcha
# ============================================================================


CAPTCHA_TOKEN_EXPECTED_LENGTH = len(generate_captcha_token())
CAPTCHA_ANSWER_EXPECTED_LENGTH = CAPTCHA_TEXT_LENGTH


class CaptchaResponseModel(BaseModel):
    token: str
    jpeg: str


@api.get("/captcha/")
async def get_captcha_token_and_jpeg_str():
    token, jpeg_str = await create_captcha_token_and_jpeg_str()
    return CaptchaResponseModel(
        token=token,
        jpeg=jpeg_str,
    )


# Comments
# ============================================================================


COMMENTS_AUTHOR_NAME_MAX_LENGTH = 256
COMMENTS_CONTENT_MAX_LENGTH = 2048


@api.get("/comments/")
async def get_comments(location_id: int):
    return await Comments.select().where(Comments.location_id == location_id)


@api.get("/comment/{comment_id}")
async def get_comment(comment_id: int):
    return await Comments.select().where(Comments.id == comment_id)


class CommentCreationModel(BaseModel):
    location_id: int
    captcha_token: str
    captcha_answer: str
    author_name: str
    content: str

    # Check lengths to avoid large database entries
    @validator("captcha_token")
    def token_must_have_correct_length(cls, token: str) -> str:
        if len(token) == CAPTCHA_TOKEN_EXPECTED_LENGTH:
            return token

        raise HTTPException(
            status_code=413,
            detail={
                "msg": "Captcha token must have correct length",
                "field": "captcha_token",
                "expected_len": CAPTCHA_TOKEN_EXPECTED_LENGTH,
            }
        )

    @validator("captcha_answer")
    def captcha_answer_must_have_correct_length(cls, answer: str) -> str:
        if len(answer) == CAPTCHA_ANSWER_EXPECTED_LENGTH:
            return answer

        raise HTTPException(
            status_code=413,
            detail={
                "msg": "Captcha answer must have correct length",
                "field": "captcha_answer",
                "expected_len": CAPTCHA_ANSWER_EXPECTED_LENGTH,
            }
        )

    @validator("author_name")
    def author_name_cannot_exceed_max_length(cls, name: str) -> str:
        if len(name) <= COMMENTS_AUTHOR_NAME_MAX_LENGTH:
            return name

        raise HTTPException(
            status_code=413,
            detail={
                "msg": "Comment author name too long",
                "field": "author_name",
                "max_len": COMMENTS_AUTHOR_NAME_MAX_LENGTH,
            }
        )

    @validator("content")
    def content_cannot_exceed_max_length(cls, content: str) -> str:
        if len(content) <= COMMENTS_CONTENT_MAX_LENGTH:
            return content

        raise HTTPException(
            status_code=413,
            detail={
                "msg": "Comment content too long",
                "field": "content",
                "max_len": COMMENTS_CONTENT_MAX_LENGTH,
            }
        )


@api.post("/comment/")
async def create_comment(comment: CommentCreationModel):  # type: ignore[valid-type]
    if not (await check_captcha_answer_and_delete(comment.captcha_token, comment.captcha_answer)):
        new_captcha_token, new_captcha_jpeg = await create_captcha_token_and_jpeg_str()
        raise HTTPException(
            status_code=401,
            detail={
                "msg": "Incorrect answer to captcha",
                "new_captcha_token": new_captcha_token,
                "new_captcha_jpeg": new_captcha_jpeg,
            }
        )

    try:
        db_entry_dict = comment.dict()
        del db_entry_dict["captcha_token"]
        del db_entry_dict["captcha_answer"]
        db_entry_dict["timestamp"] = datetime.now()

        await Comments.insert(Comments(**db_entry_dict))  # type: ignore[attr-defined]
    except ForeignKeyViolationError as err:
        raise HTTPException(
            status_code=409,
            detail=f"No location exists with id={comment.location_id}",  # type: ignore[attr-defined]
        ) from err
