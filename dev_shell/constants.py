from pathlib import Path

from bx_py_utils.path import assert_is_file

import dev_shell


DEV_SHELL_PKG_PATH = Path(dev_shell.__file__).parent.resolve()

# The source file path for external projects:
BOOTSTRAP_SOURCE_FILE = DEV_SHELL_PKG_PATH / 'bootstrap-source.py'
assert_is_file(BOOTSTRAP_SOURCE_FILE)
