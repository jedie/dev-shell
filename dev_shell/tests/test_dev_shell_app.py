from pathlib import Path
from unittest.mock import patch

from bx_py_utils.path import assert_is_file
from cli_base.cli_tools.test_utils.assertion import assert_in

import dev_shell
from dev_shell.tests.fixtures import DevShellAppBaseTestCase


OWN_DEV_SHELL_PATH = Path(dev_shell.__file__).parent.parent / 'devshell.py'
OWN_DEV_SHELL_PATH = OWN_DEV_SHELL_PATH.relative_to(Path().cwd())
assert_is_file(OWN_DEV_SHELL_PATH)


class DevShellAppTestCase(DevShellAppBaseTestCase):
    def test_help_via_execute(self):
        stdout, stderr = self.execute('help')
        self.assertEqual(stderr, '')

        assert_in(
            content=stdout,
            parts=(
                'dev-shell commands',
                'test',
                'list_venv_packages',
            ),
        )

    def test_do_test(self):
        with patch('dev_shell.command_sets.dev_shell_commands.run_unittest_cli') as check_call_mock:
            stdout, stderr = self.execute(command='test')
        self.assertEqual(stdout, '')
        self.assertEqual(stderr, '')
        check_call_mock.assert_called_once()

    def test_do_pyupgrade(self):
        stdout, stderr = self.execute(command='pyupgrade')
        self.assertEqual(stderr, '')
        assert_in(
            content=stdout,
            parts=(
                'Run PyUpgrade',
                'uv tool run pyupgrade',
            ),
        )

    def test_fix_code_style(self):
        stdout, stderr = self.execute(command='fix_code_style')
        self.assertEqual(stderr, '')
        assert_in(
            content=stdout,
            parts=('uv tool run ruff check --fix',),
        )
