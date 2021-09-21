import zipfile
from contextlib import contextmanager
from pathlib import Path
from shutil import rmtree
from typing import Iterator
from typing import Union


@contextmanager
def make_tmp_dir(path: Union[str, Path], parents: bool = True, **kwargs) -> Iterator[Path]:
    resolved_dir_path = Path(path).resolve()

    try:
        resolved_dir_path.mkdir(parents=parents, **kwargs)
        yield resolved_dir_path
    finally:
        rmtree(resolved_dir_path)


def unzip(target_path: Union[str, Path], dst_path: Union[str, Path]) -> None:
    resolved_target_path = Path(target_path).resolve()
    resolved_dst_path = Path(dst_path).resolve()

    with zipfile.ZipFile(resolved_target_path, 'r') as zip_file:
        zip_file.extractall(resolved_dst_path)
