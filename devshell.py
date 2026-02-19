#!/usr/bin/env python3

"""
developer shell
~~~~~~~~~~~~~~~

Just call this file, and the magic happens ;)

The `uv` tool is required to run the development CLI.

e.g.: Install `uv` via `pipx`
    apt install pipx
    pipx install uv

This file is from: https://pypi.org/project/dev-shell/
Source: https://github.com/jedie/dev-shell/blob/main/devshell.py

:copyleft: 2021-2024 by Jens Diemer
:license: GNU GPL v3 or above
"""

import os
import shlex
import shutil
import signal
import subprocess
import sys
from pathlib import Path


assert sys.version_info >= (3, 12), f'Python version {sys.version_info} is too old!'


BASE_PATH = Path(__file__).parent.resolve()

# Create and use  "<project-directory>/.venv/" for virtualenv:
VIRTUAL_ENV = str(BASE_PATH / '.venv')


def print_uv_error_and_exit():
    print('\nError: "uv" command not found in PATH. Please install "uv" first!\n')
    print('Hint:')
    print('\tapt-get install pipx\n')
    print('\tpipx install uv\n')
    sys.exit(1)


def verbose_check_call(*popen_args):
    print(f'\n+ {shlex.join(str(arg) for arg in popen_args)}\n')
    env = {
        'VIRTUAL_ENV': VIRTUAL_ENV,
        'UV_VENV': VIRTUAL_ENV,
        **os.environ,
    }
    return subprocess.check_call(
        popen_args,
        env=env,
        cwd=BASE_PATH,  # Needed if called from other working directory
    )


def noop_signal_handler(signal_num, frame):
    """
    Signal handler that does nothing: Used to ignore "Ctrl-C" signals
    """


def main(argv):
    uv_bin = shutil.which('uv')  # Ensure 'uv' is available in PATH
    if not uv_bin:
        print_uv_error_and_exit()

    if not Path(VIRTUAL_ENV).is_dir():
        verbose_check_call(uv_bin, 'venv', VIRTUAL_ENV)

        # Activate git pre-commit hooks:
        verbose_check_call(uv_bin, 'run', '--active', '-m', 'pre_commit', 'install')

    # The cmd2 shell should not abort on Ctrl-C => ignore "Interrupt from keyboard" signal:
    signal.signal(signal.SIGINT, noop_signal_handler)

    # Call our entry point CLI:
    try:
        verbose_check_call(uv_bin, 'run', '--active', '-m', 'dev_shell', *argv[1:])
    except subprocess.CalledProcessError as err:
        sys.exit(err.returncode)


if __name__ == '__main__':
    main(sys.argv)
