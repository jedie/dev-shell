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
from dev_shell.tests.utils import SubprocessMock
from dev_shell.utils.assertion import assert_is_dir, assert_is_file


if sys.platform == 'win32':
    BIN_PATH = Path('.venv', 'Scripts')
    VENV_PYTHON = BIN_PATH / 'python3.exe'
    VENV_PIP = BIN_PATH / 'pip.exe'
    VENV_POETRY = BIN_PATH / 'poetry.exe'
    VENV_DEVSHELL = BIN_PATH / 'devshell'  # No ".exe" !
else:
    BIN_PATH = Path('.venv', 'bin')
    VENV_PYTHON = BIN_PATH / 'python3'
    VENV_PIP = BIN_PATH / 'pip'
    VENV_POETRY = BIN_PATH / 'poetry'
    VENV_DEVSHELL = BIN_PATH / 'devshell'

DEVSHELL_CALL = f'{VENV_PYTHON} {VENV_DEVSHELL}'  # e.g.: ".venv/bin/python3 .venv/bin/devshell"


def call_devsetup_main(*args, catch_sys_exit=False):
    out = io.StringIO()
    err = io.StringIO()
    with redirect_stdout(out), redirect_stderr(err), \
            SubprocessMock('check_call') as check_call_mock:

        try:
            devshell.main(args)
        except SystemExit:
            if not catch_sys_exit:
                raise

    check_calls = check_call_mock.check_calls

    if sys.platform == 'win32':
        # FIXME: e.g.: https://github.com/jedie/dev-shell/runs/2272270967
        check_calls = [entry.replace("'", '').replace('"', '') for entry in check_calls]

    return check_calls, out.getvalue(), err.getvalue()


class BootstrapTestCase(TestCase):
    def test_up2date_bootstrap(self):
        # .dep_hash is up-to-date -> no "poetry install" call:
        check_calls, stdout, stderr = call_devsetup_main()
        assert stderr == ''
        assert f'{DEVSHELL_CALL}\n' in stdout
        assert check_calls == [DEVSHELL_CALL]
        assert 'poetry' not in stdout

    def test_poetry_install_call(self):
        base_path = Path(devshell.__file__).parent
        assert_is_dir(base_path / 'dev_shell')

        DEP_HASH_PATH = base_path / '.venv' / '.dep_hash'
        assert_is_file(DEP_HASH_PATH)

        DEP_LOCK_PATH = base_path / 'poetry.lock'

        current_hash = sha512(DEP_LOCK_PATH.read_bytes()).hexdigest()

        assert DEP_HASH_PATH.read_text() == current_hash

        # Change the hash -> "poetry install" should be called:

        try:
            DEP_HASH_PATH.write_text('this is not the hash')

            check_calls, stdout, stderr = call_devsetup_main()
            assert stderr == ''
            assert f'{VENV_POETRY} install' in stdout
            assert f'{VENV_PYTHON} {VENV_DEVSHELL}\n' in stdout
            assert check_calls == [
                f'{VENV_POETRY} install',  # <<< install called?
                DEVSHELL_CALL
            ]
        finally:
            DEP_HASH_PATH.write_text(current_hash)

    def test_force_update(self):
        # EnvBuilder.create() will ran into "SameFileError" because we call the create()
        # from the same venv to update the same venv ;)
        # So we mock this call here.
        with mock.patch('venv.EnvBuilder.create') as create_mock:
            check_calls, stdout, stderr = call_devsetup_main('devshell.py', '--update')

        assert stderr == ''
        assert f'{VENV_POETRY} install' in stdout
        assert f'{DEVSHELL_CALL}\n' in stdout
        assert check_calls == [
            f'{VENV_PYTHON} -m pip install -U pip',
            f'{VENV_PIP} install poetry',
            f'{VENV_POETRY} install',
            DEVSHELL_CALL
        ]
        create_mock.assert_called_once_with(env_dir=Path('.venv'))

    def test_help(self):
        check_calls, stdout, stderr = call_devsetup_main(
            'devshell.py', '--help',
            catch_sys_exit=True
        )
        assert stderr == ''
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
        assert stderr == ''
        assert 'not_existing_command --help' in stdout
        assert check_calls == [
            f'{DEVSHELL_CALL} not_existing_command --help'
        ]
