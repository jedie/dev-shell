#!/usr/bin/env python3

"""
    developer shell
    ~~~~~~~~~~~~~~~

    Just call this file, and the magic happens ;)

    This file is from: https://pypi.org/project/dev-shell/
    Source: https://github.com/jedie/dev-shell/blob/main/devshell.py

    :copyleft: 2021-2024 by Jens Diemer
    :license: GNU GPL v3 or above
"""
import argparse
import hashlib
import shlex
import signal
import subprocess
import sys
import venv
from pathlib import Path


def print_no_pip_error():
    print('Error: Pip not available!')
    print('Hint: "apt-get install python3-venv"\n')


try:
    from ensurepip import version
except ModuleNotFoundError as err:
    print(err)
    print('-' * 100)
    print_no_pip_error()
    raise
else:
    if not version():
        print_no_pip_error()
        sys.exit(-1)


assert sys.version_info >= (3, 11), f'Python version {sys.version_info} is too old!'


if sys.platform == 'win32':  # wtf
    # Files under Windows, e.g.: .../.venv/Scripts/python.exe
    BIN_NAME = 'Scripts'
    FILE_EXT = '.exe'
else:
    # Files under Linux/Mac and all other than Windows, e.g.: .../.venv/bin/python3
    BIN_NAME = 'bin'
    FILE_EXT = ''

BASE_PATH = Path(__file__).parent
VENV_PATH = BASE_PATH / '.venv'
BIN_PATH = VENV_PATH / BIN_NAME
PYTHON_PATH = BIN_PATH / f'python3{FILE_EXT}'
PIP_PATH = BIN_PATH / f'pip{FILE_EXT}'
UV_PATH = BIN_PATH / f'uv{FILE_EXT}'

DEP_LOCK_PATH = BASE_PATH / 'uv.lock'
DEP_HASH_PATH = VENV_PATH / '.dep_hash'

# script file defined in pyproject.toml as [console_scripts]
# (Under Windows: ".exe" not added!)
PROJECT_SHELL_SCRIPT = BIN_PATH / 'devshell'


def get_dep_hash():
    """Get SHA512 hash from lock file content."""
    return hashlib.sha512(DEP_LOCK_PATH.read_bytes()).hexdigest()


def store_dep_hash():
    """Generate .venv/.dep_hash"""
    DEP_HASH_PATH.write_text(get_dep_hash())


def venv_up2date():
    """Is existing .venv is up-to-date?"""
    if DEP_HASH_PATH.is_file():
        return DEP_HASH_PATH.read_text() == get_dep_hash()
    return False


def verbose_check_call(*popen_args):
    print(f'\n+ {shlex.join(str(arg) for arg in popen_args)}\n')
    return subprocess.check_call(popen_args)


def noop_signal_handler(signal_num, frame):
    """
    Signal handler that does nothing: Used to ignore "Ctrl-C" signals
    """


def main(argv):
    assert DEP_LOCK_PATH.is_file(), f'File not found: "{DEP_LOCK_PATH}" !'

    if len(argv) == 2 and argv[1] in ('--update', '--help'):
        parser = argparse.ArgumentParser(
            prog=Path(__file__).name,
            description='Developer shell',
            epilog='...live long and prosper...'
        )
        parser.add_argument(
            '--update', default=False, action='store_true',
            help='Force create/upgrade virtual environment'
        )
        parser.add_argument(
            'command_args',
            nargs=argparse.ZERO_OR_MORE,
            help='arguments to pass to dev-setup shell/cli',
        )
        options = parser.parse_args(argv)
        force_update = options.update
        extra_args = argv[2:]
    else:
        force_update = False
        extra_args = argv[1:]

    # Create virtual env in ".venv/":
    if not PYTHON_PATH.is_file() or force_update:
        print(f'Create virtual env here: {VENV_PATH.absolute()}')
        builder = venv.EnvBuilder(symlinks=True, upgrade=True, with_pip=True)
        builder.create(env_dir=VENV_PATH)

    if not PROJECT_SHELL_SCRIPT.is_file() or not venv_up2date() or force_update:
        # Update pip
        verbose_check_call(PYTHON_PATH, '-m', 'pip', 'install', '-U', 'pip')

        # Install uv
        verbose_check_call(PYTHON_PATH, '-m', 'pip', 'install', '-U', 'uv')

        # install requirements
        verbose_check_call(UV_PATH, 'sync')

        # install project
        verbose_check_call(PIP_PATH, 'install', '--no-deps', '-e', '.')
        store_dep_hash()

    # The cmd2 shell should not abort on Ctrl-C => ignore "Interrupt from keyboard" signal:
    signal.signal(signal.SIGINT, noop_signal_handler)

    # Call our entry point CLI:
    try:
        verbose_check_call(PROJECT_SHELL_SCRIPT, *extra_args)
    except subprocess.CalledProcessError as err:
        sys.exit(err.returncode)


if __name__ == '__main__':
    main(sys.argv)
