"""
    Note: It's not needed to test the complete bootstrap of a new .venv
    Because the CI will automatically failed if the shell is not setup right ;)
"""
import io
import sys
from contextlib import redirect_stderr, redirect_stdout
from hashlib import sha512
from pathlib import Path
from unittest import TestCase

import devshell
from dev_shell.tests.utils import SubprocessMock
from dev_shell.utils.assertion import assert_is_dir, assert_is_file


if sys.platform == 'win32':
    BIN_PATH = '.venv/Scripts'
    FILE_EXT = '.exe'
else:
    BIN_PATH = '.venv/bin'
    FILE_EXT = ''


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
    return check_calls, out.getvalue(), err.getvalue()


class BootstrapTestCase(TestCase):
    def test_up2date_bootstrap(self):
        # .dep_hash is up-to-date -> no "poetry install" call:
        check_calls, stdout, stderr = call_devsetup_main()
        assert stderr == ''
        assert f'{BIN_PATH}/python3{FILE_EXT} {BIN_PATH}/devshell\n' in stdout
        assert check_calls == [f'{BIN_PATH}/python3{FILE_EXT} {BIN_PATH}/devshell']
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
            assert f'{BIN_PATH}/poetry{FILE_EXT} install' in stdout
            assert f'{BIN_PATH}/python3{FILE_EXT} {BIN_PATH}/devshell\n' in stdout
            assert check_calls == [
                f'{BIN_PATH}/poetry{FILE_EXT} install',  # <<< install called?
                f'{BIN_PATH}/python3{FILE_EXT} {BIN_PATH}/devshell'
            ]
        finally:
            DEP_HASH_PATH.write_text(current_hash)

    def test_force_update(self):
        check_calls, stdout, stderr = call_devsetup_main('devshell.py', '--update')
        assert stderr == ''
        assert f'{BIN_PATH}/poetry install' in stdout
        assert f'{BIN_PATH}/python3{FILE_EXT} {BIN_PATH}/devshell\n' in stdout
        assert check_calls == [
            f'{BIN_PATH}/python3{FILE_EXT} -m pip install -U pip',
            f'{BIN_PATH}/pip{FILE_EXT} install poetry',
            f'{BIN_PATH}/poetry{FILE_EXT} install',
            f'{BIN_PATH}/python3{FILE_EXT} {BIN_PATH}/devshell'
        ]

    def test_help(self):
        check_calls, stdout, stderr = call_devsetup_main(
            'devshell.py', '--help',
            catch_sys_exit=True
        )
        assert stderr == ''
        assert 'usage: devshell.py [-h] [--update] [command_args ' in stdout
        assert stdout.endswith('...live long and prosper...\n')
        assert check_calls == []
