import sys

from dev_shell.constants import BIN_PATH


if sys.platform == 'win32':
    VENV_PYTHON = BIN_PATH / 'python.exe'
    VENV_PIP = BIN_PATH / 'pip.exe'
    VENV_POETRY = BIN_PATH / 'poetry.exe'
    VENV_DEVSHELL = BIN_PATH / 'devshell'  # No ".exe" !
else:
    VENV_PYTHON = BIN_PATH / 'python'
    VENV_PIP = BIN_PATH / 'pip'
    VENV_POETRY = BIN_PATH / 'poetry'
    VENV_DEVSHELL = BIN_PATH / 'devshell'

DEVSHELL_CALL = f'{VENV_PYTHON} {VENV_DEVSHELL}'  # e.g.: ".venv/bin/python .venv/bin/devshell"
