import sys
from pathlib import Path


BASE_PATH = Path(__file__).parent.parent.resolve()
assert Path(BASE_PATH / 'dev_shell').is_dir(), f'Path wrong: {BASE_PATH}'


if sys.platform == 'win32':  # wtf
    BIN_NAME = 'Scripts'
else:
    BIN_NAME = 'bin'

VENV_PATH = BASE_PATH / '.venv'

BIN_PATH = VENV_PATH / BIN_NAME
assert BIN_PATH.is_dir()


# The source file path for external projects:
BOOTSTRAP_SOURCE_FILE = BASE_PATH / 'dev_shell' / 'bootstrap-source.py'
