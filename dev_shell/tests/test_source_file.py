import filecmp
import shutil
from unittest import TestCase

from bx_py_utils.path import assert_is_file

from dev_shell.constants import BOOTSTRAP_SOURCE_FILE
from dev_shell.tests.constants import DEV_SHELL_PACKAGE_ROOT


class SourceFileTestCase(TestCase):
    def test_source_file_is_up2date(self):
        own_bootstrap_file = DEV_SHELL_PACKAGE_ROOT / 'devshell.py'
        assert_is_file(own_bootstrap_file)

        are_the_same = filecmp.cmp(own_bootstrap_file, BOOTSTRAP_SOURCE_FILE, shallow=False)
        if not are_the_same:
            shutil.copyfile(
                src=own_bootstrap_file,
                dst=BOOTSTRAP_SOURCE_FILE,
                follow_symlinks=False
            )
            raise AssertionError(f'Bootstrap source "{BOOTSTRAP_SOURCE_FILE}" updated!')
