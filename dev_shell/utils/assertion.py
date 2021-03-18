from pathlib import Path


def assert_is_dir(path):
    """
    Check if given path is a directory
    """
    if not isinstance(path, Path):
        path = Path(path)
    assert path.is_dir(), f'Directory does not exists: {path}'


def assert_is_file(path):
    """
    Check if given path is a file
    """
    if not isinstance(path, Path):
        path = Path(path)
    assert_is_dir(path.parent)
    assert path.is_file(), f'File does not exists: {path}'
