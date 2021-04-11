import os
import platform
import sys
from pathlib import Path
from unittest import TestCase

from dev_shell.constants import BASE_PATH, BIN_PATH, VENV_PATH
from dev_shell.tests.constants import VENV_PYTHON
from dev_shell.tests.utils import RedirectStdOutErr, call_mocked_subprocess
from dev_shell.utils.subprocess_utils import (
    _print_info,
    argv2str,
    make_relative_path,
    prepare_popenargs,
    verbose_check_call,
    verbose_check_output,
)


class UtilsTestCase(TestCase):
    def test_argv2str(self):
        result = argv2str([Path('/foo/bar'), '--foo'])
        if sys.platform == 'win32':
            assert result == "'\\foo\\bar' --foo"
        else:
            assert result == '/foo/bar --foo'

    def assert_make_relative_path(self, path, relative_to, result):
        p = make_relative_path(path=Path(path), relative_to=Path(relative_to))
        assert p == Path(result)

    def test_basic(self):
        if sys.platform == 'win32':
            result = r'.venv/Scripts'
        else:
            result = '.venv/bin'

        self.assert_make_relative_path(
            path=VENV_PYTHON.parent,
            relative_to=VENV_PYTHON.parent.parent.parent,
            result=result
        )


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
        assert popenargs == [BASE_PATH / 'devshell.py']
        assert cwd == BASE_PATH

        popenargs, cwd = prepare_popenargs(
            popenargs=['python', '--version'],
            cwd=None
        )
        assert popenargs == [VENV_PYTHON, '--version']
        assert cwd == BASE_PATH

        popenargs, cwd = prepare_popenargs(
            popenargs=['python', '--version'],
            cwd=Path.cwd()
        )
        assert popenargs == [VENV_PYTHON, '--version']
        assert cwd == BASE_PATH

        popenargs, cwd = prepare_popenargs(
            popenargs=['python', '--version'],
            cwd=BIN_PATH
        )
        assert popenargs == [VENV_PYTHON, '--version']
        assert cwd == BIN_PATH

        popenargs, cwd = prepare_popenargs(
            popenargs=['python', '--version'],
            cwd=BIN_PATH.parent  # .../dev-shell/.venv/
        )
        assert popenargs == [VENV_PYTHON, '--version']
        assert cwd == BIN_PATH.parent

        popenargs, cwd = prepare_popenargs(
            popenargs=['python', '--version'],
            cwd=Path(__file__).parent
        )
        assert popenargs == [VENV_PYTHON, '--version']
        assert cwd == Path(__file__).parent

        with self.assertRaises(NotADirectoryError) as cm:
            prepare_popenargs(
                popenargs=['does not exists'],
                cwd='/does/not/exists/'
            )
        if sys.platform == 'win32':
            assert cm.exception.args[0] == r'Directory does not exists: "\does\not\exists"'
        else:
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
            popenargs=[VENV_PYTHON, '--version'],
            cwd=Path.cwd(),
            kwargs={}
        )
        if sys.platform == 'win32':
            assert output == r'+ .venv\Scripts\python.exe --version'
        else:
            assert output == '+ .venv/bin/python --version'

        output = call_print_info(
            popenargs=[str(VENV_PYTHON), '--version'],
            cwd=Path(BIN_PATH / '..').resolve(),  # .../dev-shell/.venv/,
            kwargs={}
        )
        if sys.platform == 'win32':
            assert output == r'+ .venv$ Scripts\python.exe --version'
        else:
            assert output == '+ .venv$ bin/python --version'

    def test_verbose_check_call(self):
        with RedirectStdOutErr() as redirector:
            check_calls, result = call_mocked_subprocess(
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
        if sys.platform == 'win32':
            assert output == r'+ .venv$ Scripts\python.exe --version (kwargs: shell=False)'
        else:
            assert output == '+ .venv$ bin/python --version (kwargs: shell=False)'

    def test_check_output_mocked(self):
        with RedirectStdOutErr() as redirector:
            check_calls, result = call_mocked_subprocess(
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
        if sys.platform == 'win32':
            assert output == r'+ .venv$ Scripts\python.exe --version (kwargs: shell=False)'
        else:
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
        if sys.platform == 'win32':
            assert output == r'+ .venv$ Scripts\python.exe --version (kwargs: shell=False)'
        else:
            assert output == '+ .venv$ bin/python --version (kwargs: shell=False)'
