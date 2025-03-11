import sys
from pathlib import Path
from unittest.mock import patch


from cmd2 import CommandResult

import dev_shell
from dev_shell.tests.fixtures import DevShellAppBaseTestCase
from dev_shell.tests.utils import call_mocked_subprocess
from dev_shell.utils.assertion import assert_is_file


OWN_DEV_SHELL_PATH = Path(dev_shell.__file__).parent.parent / 'devshell.py'
OWN_DEV_SHELL_PATH = OWN_DEV_SHELL_PATH.relative_to(Path().cwd())
assert_is_file(OWN_DEV_SHELL_PATH)


class DevShellAppTestCase(DevShellAppBaseTestCase):
    def test_help_raw(self):
        out = self.app.app_cmd('help')

        assert isinstance(out, CommandResult)
        assert 'Documented commands' in out.stdout

        assert 'Documented commands' in out.stdout

    def test_help_via_execute(self):
        stdout, stderr = self.execute('help')
        self.assertEqual(stderr, '')
        assert 'Documented commands' in stdout

    def test_do_test(self):
        with patch('dev_shell.command_sets.dev_shell_commands.run_unittest_cli') as check_call_mock:
            stdout, stderr = self.execute(command='test')
        self.assertEqual(stdout, '')
        self.assertEqual(stderr, '')
        check_call_mock.assert_called_once()

    def test_do_update(self):
        origin_sys_argv = sys.argv.copy()
        try:
            sys.argv = ['TheDevScript.py']
            check_calls, (stdout, stderr) = call_mocked_subprocess(
                'check_call',
                self.execute,
                command='update'
            )

            self.assertEqual(stderr, '')
            calls = ' '.join(str(call) for call in check_calls)
            self.assertIn('.venv/bin/uv lock --upgrade', calls)

            self.assertIn('\nPlease restart "TheDevScript.py" !\n', stdout)
        finally:
            sys.argv = origin_sys_argv

    def test_do_pyupgrade(self):
        stdout, stderr = self.execute(command='pyupgrade')
        self.assertEqual(stderr, '')

        assert 'Run PyUpgrade' in stdout
        assert '(min version: 3.11)' in stdout
        assert '0 have been updated' in stdout

    def test_fix_code_style(self):
        with patch('dev_shell.command_sets.dev_shell_commands.code_style.fix') as check_call_mock:
            stdout, stderr = self.execute(command='fix_code_style')

        self.assertEqual(stdout, '')
        self.assertEqual(stderr, '')

        check_call_mock.assert_called()
