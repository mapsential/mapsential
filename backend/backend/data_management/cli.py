#!/bin/python
import click
from constants import LOCATION_TYPE_NAMES
from constants import LOCATION_TYPE_NAMES_SHORTEND_TO_ORIGINALS
from enums import LocationType
from utils.iterables import flatten

from . import update


@click.group(help="Data management commands.")
@click.option(
    "-l", "--location-type", "location_types",
    type=click.Choice(list(flatten(zip(LOCATION_TYPE_NAMES, LOCATION_TYPE_NAMES_SHORTEND_TO_ORIGINALS.keys())))),
    multiple=True,
    default=LOCATION_TYPE_NAMES,
)
@click.pass_context
def cli(ctx, location_types) -> None:
    ctx.ensure_object(dict)

    if len(location_types) == 0:
        location_types = LOCATION_TYPE_NAMES

    ctx.obj = {"location_types": [
        LocationType(
            location_type
            if location_type in LOCATION_TYPE_NAMES
            else LOCATION_TYPE_NAMES_SHORTEND_TO_ORIGINALS[location_type]
        ) for location_type in location_types
    ]}


@cli.command(name="update")
@click.pass_context
def cli_update(ctx):
    update(ctx.obj["location_types"])
