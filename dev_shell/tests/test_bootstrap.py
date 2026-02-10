"""
    Note: It's not needed to test the complete bootstrap of a new .venv
    Because the CI will automatically failed if the shell is not setup right ;)
"""
import subprocess
from unittest import TestCase

from bx_py_utils.path import assert_is_file
from cli_base.cli_tools.test_utils.assertion import assert_in

from dev_shell.tests.constants import DEV_SHELL_PACKAGE_ROOT


class BootstrapTestCase(TestCase):
    def test_help(self):
        test_path = DEV_SHELL_PACKAGE_ROOT / 'devshell.py'
        assert_is_file(test_path)
        stdout = subprocess.check_output(
            args=('python3', 'devshell.py', '--help'), text=True, cwd=DEV_SHELL_PACKAGE_ROOT
        )
        assert_in(
            content=stdout,
            parts=(
                'dev-shell commands',
                'test',
                'list_venv_packages',
            ),
        )

    def test_pass_help(self):
        """
        A "--help" argument should be pass to a cmd2 command
        """
        stdout = subprocess.check_output(
            args=('python3', 'devshell.py', 'pyupgrade', '--help'), text=True, cwd=DEV_SHELL_PACKAGE_ROOT
        )
        assert_in(
            content=stdout,
            parts=(
                'Usage: pyupgrade [-h] [--major-version] [--minor-version]',
                'Run pyupgrade',
                '--major-version',
                '--minor-version',
            ),
        )
