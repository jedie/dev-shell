import filecmp
import shutil
import subprocess
import sys
from unittest import TestCase

from dev_shell.constants import BOOTSTRAP_SOURCE_FILE, PACKAGE_ROOT
from dev_shell.utils.assertion import assert_is_file


class SourceFileTestCase(TestCase):
    def test_source_file_is_up2date(self):
        own_bootstrap_file = PACKAGE_ROOT / 'devshell.py'
        assert_is_file(own_bootstrap_file)

        are_the_same = filecmp.cmp(own_bootstrap_file, BOOTSTRAP_SOURCE_FILE, shallow=False)
        if not are_the_same:
            shutil.copyfile(
                src=own_bootstrap_file,
                dst=BOOTSTRAP_SOURCE_FILE,
                follow_symlinks=False
            )
            raise AssertionError(f'Bootstrap source "{BOOTSTRAP_SOURCE_FILE}" updated!')

    def test_wrong_call(self):
        # The bootstrap script should only work if "uv.lock" file exists in same path!
        p = subprocess.run(
            [sys.executable, str(BOOTSTRAP_SOURCE_FILE)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False
        )
        assert p.returncode == 1
        output = p.stdout.strip()
        assert 'File not found' in output
        if sys.platform == 'win32':
            assert output.endswith(r'\dev_shell\uv.lock" !')
        else:
            assert output.endswith('/dev_shell/uv.lock" !')
