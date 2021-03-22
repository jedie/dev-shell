import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

from dev_shell.utils.colorful import blue, bright_yellow, cyan, green, print_error


def argv2str(argv):
    """
    >>> argv2str(['foo', '--bar=123'])
    'foo --bar=123'
    """
    return ' '.join(a if re.match(r'^[-0-9a-zA-Z_.=]+$', a) else shlex.quote(a) for a in argv)


def _print_info(popenargs, kwargs):
    print()
    print('_' * 100)

    command_str = argv2str(popenargs)

    if ' ' in command_str:
        command, args = command_str.split(' ', 1)
    else:
        command = command_str
        args = ''

    command_path = Path(command)
    command_name = command_path.name
    command_dir = command_path.parent

    info = ''
    if command_dir:
        info += green(f'{command_dir}{os.sep}')
    if command_name:
        info += bright_yellow(command_name)
    if args:
        info += f' {blue(args)}'

    msg = f'Call: {info}'

    verbose_kwargs = ', '.join(f'{k}={v!r}' for k, v in sorted(kwargs.items()))
    if verbose_kwargs:
        msg += f' (kwargs: {cyan(verbose_kwargs)})'

    print(f'{msg}\n', flush=True)


def prepare_popenargs(popenargs):
    popenargs = [str(part) for part in popenargs]  # e.g.: Path() instance -> str

    command = popenargs[0]
    if not Path(command).is_file():
        # Search in PATH for this command that doesn't point to a existing file:
        command = shutil.which(command)
        if not command:
            raise FileNotFoundError(f'Command "{popenargs[0]}" not found in PATH!')

        # Replace command name with full path:
        popenargs[0] = command

    return popenargs


def verbose_check_call(
        *popenargs,
        verbose=True,
        cwd=None,
        extra_env=None,
        exit_on_error=False,
        **kwargs):
    """ 'verbose' version of subprocess.check_call() """

    popenargs = prepare_popenargs(popenargs)

    if verbose:
        _print_info(popenargs, kwargs)

    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)

    try:
        return subprocess.check_call(
            popenargs,
            universal_newlines=True,
            env=env,
            cwd=cwd,
            **kwargs
        )
    except subprocess.CalledProcessError as err:
        if exit_on_error:
            if verbose:
                print_error(f'Process "{popenargs[0]}" finished with exit code {err.returncode!r}')
            sys.exit(err.returncode)
        raise


def verbose_check_output(*popenargs, verbose=True, cwd=None, extra_env=None, **kwargs):
    """ 'verbose' version of subprocess.check_output() """

    popenargs = prepare_popenargs(popenargs)

    if verbose:
        _print_info(popenargs, kwargs)

    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)

    try:
        output = subprocess.check_output(
            popenargs,
            universal_newlines=True,
            env=env,
            cwd=cwd,
            stderr=subprocess.STDOUT,
            **kwargs
        )
    except subprocess.CalledProcessError as err:
        print('\n***ERROR:')
        print(err.output)
        raise
    return output
