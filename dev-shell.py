#!/usr/bin/env python3

"""
    developer shell
    ~~~~~~~~~~~~~~~

    Just call this file, and the magic happens ;)
"""

import argparse
import os
import signal
import subprocess
import sys
import venv
from pathlib import Path

try:
    import ensurepip  # noqa
except ImportError as err:
    print('Error: Pip not available!')
    print(f'\n(Origin error: {err}\n')
    print('Hint: "apt-get install python3-venv"')
    raise

VENV_PATH = Path('.venv')
BIN_PATH = VENV_PATH / 'bin'
PYTHON_PATH = BIN_PATH / 'python3'
PIP_PATH = BIN_PATH / 'pip'
POETRY_PATH = BIN_PATH / 'poetry'

# file defined in pyproject.toml as [tool.poetry.scripts]
PROJECT_SHELL_SCRIPT = BIN_PATH / 'devshell'


assert sys.version_info >= (3, 7), 'Python version is too old!'
assert sys.platform != 'win32', 'Windows not supported, yet!'


def noop_signal_handler(signal_num, frame):
    pass


if __name__ == '__main__':
    if '--update' in sys.argv or '--help' in sys.argv:
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
        options = parser.parse_args()
        force_update = options.update
        extra_args = sys.argv[2:]
    else:
        force_update = False
        extra_args = sys.argv[1:]

    if not PIP_PATH.is_file() or force_update:
        # make virtual env in ./venv/
        print('Create venv here:', VENV_PATH.absolute())
        builder = venv.EnvBuilder(symlinks=True, upgrade=True, with_pip=True)
        builder.create(env_dir=VENV_PATH)

    if not POETRY_PATH.is_file() or force_update:
        # install/update "pip" and "poetry"
        subprocess.check_call([PIP_PATH, 'install', '-U', 'pip'])
        subprocess.check_call([PIP_PATH, 'install', 'poetry'])

    # install / update via poetry
    if not PROJECT_SHELL_SCRIPT.is_file():
        subprocess.check_call([POETRY_PATH, 'install'])
    elif force_update:
        subprocess.check_call([POETRY_PATH, 'update'])
        print('\nUpdate done.')

    # The cmd2 shell should not abort on Ctrl-C => ignore "Interrupt from keyboard" signal:
    signal.signal(signal.SIGINT, noop_signal_handler)

    # Run project cmd shell via "setup.py" entrypoint:
    subprocess.call([PROJECT_SHELL_SCRIPT] + extra_args)
