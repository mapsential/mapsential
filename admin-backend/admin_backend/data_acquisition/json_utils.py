import json
from pathlib import Path
from typing import TypeVar
from typing import Union


T = TypeVar("T")


def get_obj_from_most_recently_json_file_in_dir(
        dir_path: Union[str, Path],
        # Determine most recent file by name. E.g. '2021_10_21.json' is more recent than '2021_09_24.json'
        most_recent_key = lambda path: path.name,
) -> T:
    resolved_path = Path(dir_path).resolve()

    most_recent_json_file = max(
        (child for child in resolved_path.iterdir() if child.is_file() and child.suffix == ".json"),
        key=most_recent_key
    )

    return get_obj_from_json_file(most_recent_json_file)


def get_obj_from_json_file(file_path: Union[str, Path]) -> T:
    resolved_path = Path(file_path).resolve()

    with open(resolved_path, "r") as file:
        return json.loads(file.read())
