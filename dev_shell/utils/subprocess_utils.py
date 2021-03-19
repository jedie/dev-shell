import os
import re
import shlex
import shutil
import subprocess
from pathlib import Path

from dev_shell.utils.colorful import blue_bold, yellow_bold


def argv2str(argv):
    """
    >>> argv2str(['foo', '--bar=123'])
    'foo --bar=123'
    """
    return ' '.join(a if re.match(r'^[-0-9a-zA-Z_.=]+$', a) else shlex.quote(a) for a in argv)


def _print_info(popenargs, kwargs):
    command = argv2str(popenargs)

    print()
    print('_' * 100)
    msg = f'Call: {yellow_bold(command)}'
    verbose_kwargs = ', '.join(f'{k}={v!r}' for k, v in sorted(kwargs.items()))
    if verbose_kwargs:
        msg += f' (kwargs: {blue_bold(verbose_kwargs)})'

    print(f'{msg}\n', flush=True)


def prepare_popenargs(popenargs):
    popenargs = [str(part) for part in popenargs]  # e.g.: Path() instance -> str

    command = Path(popenargs[0])
    if not command.is_file():
        command = shutil.which(command)
        if not command:
            raise FileNotFoundError(f'Command "{popenargs[0]}" not found in PATH!')
        popenargs[0] = str(command)

    return popenargs


def verbose_check_call(
        *popenargs,
        verbose=True,
        cwd=None,
        extra_env=None,
        **kwargs):
    """ 'verbose' version of subprocess.check_call() """

    popenargs = prepare_popenargs(popenargs)

    if verbose:
        _print_info(popenargs, kwargs)

    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)

    subprocess.check_call(
        popenargs,
        universal_newlines=True,
        env=env,
        cwd=cwd,
        **kwargs
    )


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
