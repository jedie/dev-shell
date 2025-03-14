"""
    Note: It's not needed to test the complete bootstrap of a new .venv
    Because the CI will automatically failed if the shell is not setup right ;)
"""
import io
import sys
from contextlib import redirect_stderr, redirect_stdout
from hashlib import sha512
from pathlib import Path
from unittest import TestCase, mock

import devshell
from dev_shell.tests.utils import call_mocked_subprocess
from dev_shell.utils.assertion import assert_is_dir, assert_is_file


def call_devsetup_main(*args, catch_sys_exit=False):
    out = io.StringIO()
    err = io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        check_calls, result = call_mocked_subprocess(
            'check_call',
            devshell.main,
            args,
            catch_sys_exit=catch_sys_exit
        )

    if sys.platform == 'win32':
        # FIXME: e.g.: https://github.com/jedie/dev-shell/runs/2272270967
        check_calls = [entry.replace("'", '').replace('"', '') for entry in check_calls]

    return check_calls, out.getvalue(), err.getvalue()


class BootstrapTestCase(TestCase):
    def test_up2date_bootstrap(self):
        # .dep_hash is up-to-date -> no "uv install" call:
        check_calls, stdout, stderr = call_devsetup_main()
        self.assertEqual(stderr, '')
        self.assertIn('.venv/bin/devshell', stdout)
        self.assertNotIn('uv ', stdout)

    def test_uv_install_call(self):
        base_path = Path(devshell.__file__).parent
        assert_is_dir(base_path / 'dev_shell')

        DEP_HASH_PATH = base_path / '.venv' / '.dep_hash'
        assert_is_file(DEP_HASH_PATH)

        DEP_LOCK_PATH = base_path / 'uv.lock'

        current_hash = sha512(DEP_LOCK_PATH.read_bytes()).hexdigest()

        assert DEP_HASH_PATH.read_text() == current_hash

        # Change the hash -> "uv install" should be called:

        try:
            DEP_HASH_PATH.write_text('this is not the hash')

            check_calls, stdout, stderr = call_devsetup_main()
            self.assertEqual(stderr, '')
            self.assertIn('uv sync', stdout)
            self.assertIn('.venv/bin/devshell', stdout)
        finally:
            DEP_HASH_PATH.write_text(current_hash)

    def test_force_update(self):
        # EnvBuilder.create() will ran into "SameFileError" because we call the create()
        # from the same venv to update the same venv ;)
        # So we mock this call here.
        with mock.patch('venv.EnvBuilder.create') as create_mock:
            check_calls, stdout, stderr = call_devsetup_main('devshell.py', '--update')

        self.assertEqual(stderr, '')
        self.assertIn('Create virtual env here:', stdout)
        self.assertIn('uv sync', stdout)
        self.assertIn('.venv/bin/devshell\n', stdout)
        create_mock.assert_called_once()

    def test_help(self):
        check_calls, stdout, stderr = call_devsetup_main(
            'devshell.py', '--help',
            catch_sys_exit=True
        )
        self.assertEqual(stderr, '')
        assert 'usage: devshell.py [-h] [--update] [command_args ' in stdout
        assert stdout.endswith('...live long and prosper...\n')
        assert check_calls == []

    def test_pass_help(self):
        """
        A "--help" argument should be pass to a cmd2 command
        """
        check_calls, stdout, stderr = call_devsetup_main(
            'devshell.py', 'not_existing_command', '--help',
            catch_sys_exit=True
        )
        self.assertEqual(stderr, '')
        assert 'not_existing_command --help' in stdout
        self.assertIn('.venv/bin/devshell not_existing_command --help', check_calls[0])
