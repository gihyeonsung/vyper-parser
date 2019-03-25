from pathlib import (
    Path,
)
from typing import (
    Any,
    Iterator,
    Tuple,
)
import os
import sys


def get_id(fixture_path: Path) -> str:
    return str(fixture_path.resolve())


def get_lib_path():
    if os.name == 'nt':
        # Special case for windows
        if 'PyPy' in sys.version:
            return Path(sys.prefix) / 'lib-python' / sys.winver
        else:
            return Path(sys.prefix) / 'Lib'

    # General case
    major = sys.version_info.major
    minor = sys.version_info.minor
    version_str = f'{major}.{minor}'

    return Path([x for x in sys.path if x.endswith(version_str)][0])


def find_fixture_files():
    return tuple(get_lib_path().glob('*.py'))


def mark_fixtures(all_fixture_paths: Tuple[Path, ...]) -> Iterator[Path]:
    for fixture_path in sorted(all_fixture_paths):
        yield fixture_path


def generate_fixture_tests(metafunc: Any) -> None:
    if 'fixture_path' in metafunc.fixturenames:
        all_fixture_paths = tuple(mark_fixtures(
            all_fixture_paths=find_fixture_files(),
        ))

        if len(all_fixture_paths) == 0:
            raise Exception("Invariant: found zero fixtures")

        metafunc.parametrize('fixture_path', all_fixture_paths, ids=get_id)
