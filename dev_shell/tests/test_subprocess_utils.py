import os
import platform
from pathlib import Path
from unittest import TestCase

from dev_shell.constants import BASE_PATH, BIN_PATH, VENV_PATH
from dev_shell.tests.constants import VENV_PYTHON
from dev_shell.tests.utils import RedirectStdOutErr, call_mocked_subprocess
from dev_shell.utils.subprocess_utils import _print_info, prepare_popenargs, verbose_check_call, verbose_check_output


class SubprocessUtilsTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.origin_cwd = Path.cwd()
        os.chdir(BASE_PATH)

    def tearDown(self):
        super().tearDown()
        os.chdir(self.origin_cwd)

    def test_prepare_popenargs(self):
        popenargs, cwd = prepare_popenargs(
            popenargs=[BASE_PATH / 'devshell.py'],
            cwd=None
        )
        assert popenargs == [str(BASE_PATH / 'devshell.py')]
        assert cwd == BASE_PATH

        popenargs, cwd = prepare_popenargs(
            popenargs=['python', '--version'],
            cwd=None
        )
        assert popenargs == [str(VENV_PYTHON), '--version']
        assert cwd == BASE_PATH

        popenargs, cwd = prepare_popenargs(
            popenargs=['python', '--version'],
            cwd=Path.cwd()
        )
        assert popenargs == [str(VENV_PYTHON), '--version']
        assert cwd == BASE_PATH

        popenargs, cwd = prepare_popenargs(
            popenargs=['python', '--version'],
            cwd=BIN_PATH
        )
        assert popenargs == [str(VENV_PYTHON), '--version']
        assert cwd == BIN_PATH

        popenargs, cwd = prepare_popenargs(
            popenargs=['python', '--version'],
            cwd=BIN_PATH.parent  # .../dev-shell/.venv/
        )
        assert popenargs == [str(VENV_PYTHON), '--version']
        assert cwd == BIN_PATH.parent

        popenargs, cwd = prepare_popenargs(
            popenargs=['python', '--version'],
            cwd=Path(__file__).parent
        )
        assert popenargs == [str(VENV_PYTHON), '--version']
        assert cwd == Path(__file__).parent

        with self.assertRaises(NotADirectoryError) as cm:
            prepare_popenargs(
                popenargs=['does not exists'],
                cwd='/does/not/exists/'
            )
        assert cm.exception.args[0] == 'Directory does not exists: "/does/not/exists"'

        with self.assertRaises(FileNotFoundError) as cm:
            prepare_popenargs(popenargs=['does not exists'])
        assert cm.exception.args[0] == 'Command "does not exists" not found in PATH!'

    def test_print_info(self):
        def call_print_info(*args, **kwargs):
            with RedirectStdOutErr() as redirector:
                _print_info(*args, **kwargs)

            output = redirector.get_output(remove_ansi=True)
            output = output.strip()
            output = output.lstrip('\n_')
            return output

        output = call_print_info(
            popenargs=['python', '--version'],
            cwd=Path.cwd(),
            kwargs={}
        )
        assert output == '+ ./python --version'

        output = call_print_info(
            popenargs=['foo', '--bar'],
            cwd=Path('/somewhere/'),
            kwargs={'shell': False}
        )
        assert output == '+ /somewhere$ foo --bar (kwargs: shell=False)'

        output = call_print_info(
            popenargs=[str(VENV_PYTHON), '--version'],
            cwd=Path(BIN_PATH / '..').resolve(),  # .../dev-shell/.venv/,
            kwargs={}
        )
        assert output == '+ .venv$ bin/python --version'

    def test_verbose_check_call(self):
        with RedirectStdOutErr() as redirector:
            check_calls = call_mocked_subprocess(
                'check_call',
                verbose_check_call,
                str(VENV_PYTHON), '--version',
                cwd=Path(BIN_PATH / '..').resolve(),  # .../dev-shell/.venv/,
                shell=False
            )
            assert check_calls == [f'{VENV_PATH}$ {VENV_PYTHON} --version']

        output = redirector.get_output(remove_ansi=True)
        output = output.strip()
        output = output.lstrip('\n_')
        assert output == '+ .venv$ bin/python --version (kwargs: shell=False)'

    def test_check_output_mocked(self):
        with RedirectStdOutErr() as redirector:
            check_calls = call_mocked_subprocess(
                'check_output',
                verbose_check_output,
                VENV_PYTHON, '--version',
                cwd=Path(BIN_PATH / '..').resolve(),  # .../dev-shell/.venv/
                shell=False
            )
            assert check_calls == [f'{VENV_PATH}$ {VENV_PYTHON} --version']

        output = redirector.get_output(remove_ansi=True)
        output = output.strip()
        output = output.lstrip('\n_')
        assert output == '+ .venv$ bin/python --version (kwargs: shell=False)'

    def test_check_output(self):
        with RedirectStdOutErr() as redirector:
            output = verbose_check_output(
                VENV_PYTHON, '--version',
                cwd=Path(BIN_PATH / '..').resolve(),  # .../dev-shell/.venv/
                shell=False
            )
            assert output == f'Python {platform.python_version()}\n'

        output = redirector.get_output(remove_ansi=True)
        output = output.strip()
        output = output.lstrip('\n_')
        assert output == '+ .venv$ bin/python --version (kwargs: shell=False)'
