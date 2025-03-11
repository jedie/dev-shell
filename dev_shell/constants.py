import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).parent.parent.resolve()
assert Path(PACKAGE_ROOT / 'dev_shell').is_dir(), f'Path wrong: {PACKAGE_ROOT}'


if sys.platform == 'win32':  # wtf
    BIN_NAME = 'Scripts'
else:
    BIN_NAME = 'bin'

VENV_PATH = PACKAGE_ROOT / '.venv'

BIN_PATH = VENV_PATH / BIN_NAME
assert BIN_PATH.is_dir()


# The source file path for external projects:
BOOTSTRAP_SOURCE_FILE = PACKAGE_ROOT / 'dev_shell' / 'bootstrap-source.py'
