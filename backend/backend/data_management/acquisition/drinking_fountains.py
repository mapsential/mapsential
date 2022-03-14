import xml.etree.ElementTree as XMLElementTree
from dataclasses import dataclass
from functools import cache
from io import BufferedWriter
from typing import cast
from typing import Iterable
from typing import Iterator
from xml.etree.ElementTree import Element as XMLElement

import requests
from enums import LocationType
from structs import DbEntitiesGroup
from utils.dirs_and_files import make_tmp_dir
from utils.dirs_and_files import unzip

from db.tables import Details
from db.tables import Locations


XMLTupleSchema = tuple[str | tuple[str | tuple[str | tuple, ...], ...], ...]


GOOGLE_MAPS_DRINKING_FOUNTAIN_KMZ_URL = \
    "https://www.google.com/maps/d/u/0/kml?forcekml=0&mid=1XJunMq4YF0zaZxh4AVtyA5v6FWjYV90I&lid=1RcQnxo4AnQ"
OPERATOR="Berliner Wasserbetriebe"
XML_LOCATION_TAG = "Placemark"
XML_LOCATION_NODE_SCHEMA: XMLTupleSchema = (
    "name",
    "description",
    ("Point", (
        "coordinates",
    )),
)


@dataclass(frozen=True)
class IntermediateRepr:
    name: str | None
    operating_times: str
    latitude: float
    longitude: float


def acquire() -> Iterable[DbEntitiesGroup]:
    kml_xml = read_kml_xml_file_from_downloaded_and_extracted_kmz_zip_file(
        GOOGLE_MAPS_DRINKING_FOUNTAIN_KMZ_URL,
    )

    for drinking_foutain in create_intermediate_reprs(kml_xml):
        yield create_entities(drinking_foutain)


def read_kml_xml_file_from_downloaded_and_extracted_kmz_zip_file(url: str) -> str:
    with make_tmp_dir("./.tmp_kmz_download") as tmp_dir_path:
        # Download zip
        zip_file_path = tmp_dir_path / "kmz.zip"
        with open(zip_file_path, "wb") as f:
            download_kmz_to_zip_file(url, f)

        # Extract zip
        extracted_dir_path = tmp_dir_path / "km"
        unzip(zip_file_path, extracted_dir_path)

        # Read xml file from extracted dir
        xml_file_path = extracted_dir_path / "doc.kml"
        with open(xml_file_path) as f:
            return f.read()


def download_kmz_to_zip_file(url: str, file_io_handler: BufferedWriter) -> None:
    response = requests.get(url, stream=True)

    file_io_handler.write(response.raw.read())


def create_intermediate_reprs(kml_xml: str) -> Iterator[IntermediateRepr]:
    xml_root_node = XMLElementTree.fromstring(kml_xml)

    xml_namespace = get_xml_node_namespace(xml_root_node)

    for xml_location_node in findall_xml_nodes_with_tag(
        xml_namespace,
        xml_root_node,
        XML_LOCATION_TAG
    ):
        yield create_intermediate_repr(xml_namespace, xml_location_node)


def get_xml_node_namespace(node: XMLElement) -> str:
    tag = node.tag
    return tag[tag.find("{") + 1:tag.find("}")]


def findall_xml_nodes_with_tag(namespace: str, root_node: XMLElement, tag: str) -> Iterable[XMLElement]:
    return root_node.findall(f".//{{{namespace}}}{tag}")


def create_intermediate_repr(xml_namespace, xml_location_node) -> IntermediateRepr:
    lat, long = get_lat_long(xml_namespace, xml_location_node)

    return IntermediateRepr(
        name=find_xml_location_child_node_by_rel_path(
            xml_namespace,
            xml_location_node,
            "name"
        ).text,
        operating_times=get_operating_times(xml_namespace, xml_location_node),
        latitude=lat,
        longitude=long,
    )


def get_lat_long(xml_namespace: str, xml_location_node: XMLElement) -> tuple[float, float]:
    coordinates_str = cast(str, find_xml_location_child_node_by_rel_path(
        xml_namespace,
        xml_location_node,
        "Point/coordinates",
    ).text)
    long_str, lat_str, *_ = coordinates_str.replace(" ", "").split(",")
    return float(lat_str), float(long_str)


def get_operating_times(xml_namespace: str, xml_location_node: XMLElement) -> str:
    description = cast(str, find_xml_location_child_node_by_rel_path(
        xml_namespace,
        xml_location_node,
        "description",
    ).text)
    german_text = description.strip().split("<br>")[0]
    return german_text.removeprefix("Betriebszeit:").strip()


def find_xml_location_child_node_by_rel_path(namespace: str, location_node: XMLElement, path: str) -> XMLElement:
    validate_xml_rel_path_against_schema(XML_LOCATION_NODE_SCHEMA, path)

    path_with_namespace = "/".join(f"{{{namespace}}}{segment}" for segment in path.split("/"))
    return cast(XMLElement, location_node.find(f"./{path_with_namespace}"))


@cache
def validate_xml_rel_path_against_schema(schema: XMLTupleSchema, path: str) -> None:
    segments = path.split("/")

    def validate(schema_: XMLTupleSchema, segment_index: int) -> None:
        if segment_index == len(segments):
            return

        segment = segments[segment_index]
        try:
            return validate(
                get_xml_schema_entry(schema_, segment),
                segment_index + 1
            )
        except KeyError as err:
            raise ValueError(
                f"Invalid path '{path}'. "
                f"'{'/'.join(segments[:segment_index + 1])}' not found in schema '{schema}'"
            ) from err

    validate(schema, segment_index=0)


def get_xml_schema_entry(schema: XMLTupleSchema, entry: str) -> XMLTupleSchema:
    for item in schema:
        if type(item) is str and entry == item:
            return ()
        elif entry == item[0]:
            return cast(XMLTupleSchema, item[1])

    raise KeyError(f"No entry '{entry}' found in schema '{schema}'")


def create_entities(drinking_fountain: IntermediateRepr) -> Iterator[DbEntitiesGroup]:
    return DbEntitiesGroup(
        location=Locations(
            type=LocationType.DRINKING_FOUNTAIN,
            latitude=drinking_fountain.latitude,
            longitude=drinking_fountain.longitude,
        ),
        details=Details(
            name=drinking_fountain.name,
            operator=OPERATOR,
        )
    )
