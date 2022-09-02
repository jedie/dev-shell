import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
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
        assert stderr == ''
        assert 'Documented commands' in stdout

    def test_do_pytest(self):
        with patch.object(subprocess, 'check_call') as check_call_mock:
            stdout, stderr = self.execute(command='pytest')

        assert stderr == ''
        check_call_mock.assert_called_once()
        popenargs = check_call_mock.call_args[0][0]
        command = popenargs[0]
        assert 'pytest' in command

        # The call will be printed:
        assert 'pytest' in stdout

    def test_do_update(self):
        origin_sys_argv = sys.argv.copy()
        try:
            sys.argv = ['TheDevScript.py']
            check_calls, (stdout, stderr) = call_mocked_subprocess(
                'check_call',
                self.execute,
                command='update'
            )

            assert stderr == ''

            assert len(check_calls) == 1
            if sys.platform == 'win32':
                assert check_calls[0].endswith(r'.venv\Scripts\poetry.exe update -v')
                assert '\n+ .venv\\Scripts\\poetry.exe update -v\n' in stdout
            else:
                assert check_calls[0].endswith('.venv/bin/poetry update -v')
                assert '\n+ .venv/bin/poetry update -v\n' in stdout

            assert '\nPlease restart "TheDevScript.py" !\n' in stdout
        finally:
            sys.argv = origin_sys_argv

    def test_do_pyupgrade(self):
        stdout, stderr = self.execute(command='pyupgrade')

        print(stdout)
        print(stderr)

        assert stderr == ''

        assert 'Run PyUpgrade' in stdout
        assert '(min version: 3.7)' in stdout
        assert '0 have been updated' in stdout

    def test_fix_code_style(self):
        with patch.object(subprocess, 'check_call') as check_call_mock:
            stdout, stderr = self.execute(command='fix_code_style')

        print(stdout)
        print(stderr)

        assert stderr == ''

        # The call will be printed:
        if sys.platform == 'win32':
            assert '+ .venv\\Scripts\\darker.exe\n' in stdout
        else:
            assert '+ .venv/bin/darker\n' in stdout

        check_call_mock.assert_called()

    def test_return_code(self):
        """
        If pytest failed, the cmd2 app should sys.exit() with >0 return code.
        Otherwise it's not useable in CI pipelines ;)

        This tests also the "run as CLI" implementation.
        """
        def call_pytest(*args):
            return subprocess.run(
                [sys.executable, str(OWN_DEV_SHELL_PATH), 'pytest'] + list(args),
                capture_output=True,
                text=True
            )

        # Provoke an error by trying to test a path that does not exist:
        p = call_pytest('/path/does/not/exists/')
        assert p.returncode > 0
        assert 'file or directory not found: /path/does/not/exists/' in p.stderr
        assert 'pytest /path/does/not/exists/' in p.stdout
        assert f'finished with exit code {p.returncode}' in p.stdout

        # Do something that normally should never fail:
        p = call_pytest('--version')
        stderr = p.stderr
        stdout = p.stdout
        assert f'pytest {pytest.__version__}\n' in stdout
        assert 'finished with exit code' not in stdout
        assert p.returncode == 0
        assert stderr == ''
