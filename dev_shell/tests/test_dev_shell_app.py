import subprocess
from unittest.mock import patch

from cmd2 import CommandResult

from dev_shell.tests.fixtures import DevShellAppBaseTestCase


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
        assert command.endswith('/.venv/bin/pytest')

        # The call will be printed:
        assert '.venv/bin/' in stdout
        assert 'pytest' in stdout
