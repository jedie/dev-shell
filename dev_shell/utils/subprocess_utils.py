import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

from dev_shell.utils.assertion import assert_is_dir
from dev_shell.utils.colorful import blue, bright_blue, bright_white, bright_yellow, cyan, green, print_error


def argv2str(argv):
    """
    >>> argv2str(['foo', '--bar=123'])
    'foo --bar=123'
    >>> argv2str([Path('/foo/bar'), '--foo'])
    '/foo/bar --foo'
    """
    items = []
    for item in argv:
        if isinstance(item, Path):
            item = str(item)

        if re.match(r'^[-0-9a-zA-Z_.=]+$', item):
            items.append(item)
        else:
            items.append(shlex.quote(item))

    return ' '.join(items)


def make_relative_path(path, relative_to):
    """
    Makes {path} relative to {relative_to}, e.g.:
    >>> str(make_relative_path(Path('/one/two/three'), relative_to=Path('/one')))
    'two/three'

    >>> str(make_relative_path(Path('/foo/bar/.venv/bin/python'), relative_to=Path('/foo/bar/.venv')))
    'bin/python'

    Will resolve the paths, e.g.:
    >>> str(make_relative_path(Path('../one/two/three'), relative_to=Path('../one')))
    'two/three'

    Does nothing if {path} doesn't start with {relative_to}, e.g:
    >>> str(make_relative_path(Path('/one/two'), relative_to=Path('/other/path')))
    '/one/two'
    """
    assert isinstance(path, Path)
    assert isinstance(relative_to, Path)

    path = path.absolute()
    relative_to = relative_to.absolute()

    try:
        is_relative_to = path.is_relative_to(relative_to)
    except AttributeError:  # is_relative_to() is new in Python 3.9
        try:
            path = path.relative_to(relative_to)
        except ValueError:
            # {path} doesn't start with {relative_to} -> do nothing
            pass
    else:
        if is_relative_to:
            path = path.relative_to(relative_to)

    return path


def _print_info(popenargs, *, cwd, kwargs):
    print()
    print('_' * 100)

    command_str = argv2str(popenargs)

    if ' ' in command_str:
        command, args = command_str.split(' ', 1)
    else:
        command = command_str
        args = ''

    command_path = make_relative_path(Path(command), relative_to=cwd)
    cwd = make_relative_path(cwd, relative_to=Path.cwd())

    command_name = command_path.name
    command_dir = command_path.parent

    info = ''

    if cwd.absolute() != Path.cwd().absolute():
        info = f'{bright_blue(str(cwd))}{bright_white("$")} '

    if command_dir and command_dir != Path.cwd():
        info += green(f'{command_dir}{os.sep}')

    if command_name:
        info += bright_yellow(command_name)

    if args:
        info += f' {blue(args)}'

    msg = f'+ {info}'

    verbose_kwargs = ', '.join(f'{k}={v!r}' for k, v in sorted(kwargs.items()))
    if verbose_kwargs:
        msg += f' (kwargs: {cyan(verbose_kwargs)})'

    print(f'{msg}\n', flush=True)


def prepare_popenargs(popenargs, cwd=None):
    popenargs = [str(part) for part in popenargs]  # e.g.: Path() instance -> str

    if cwd is None:
        cwd = Path.cwd()
    else:
        assert_is_dir(cwd)

    command_path = Path(popenargs[0])

    if not command_path.is_file():
        # Lookup in current venv bin path first:
        bin_path = str(Path(sys.executable).parent.absolute())
        command = shutil.which(str(command_path), path=bin_path)
        if not command:
            # Search in PATH for this command that doesn't point to a existing file:
            command = shutil.which(str(command_path))
            if not command:
                raise FileNotFoundError(f'Command "{popenargs[0]}" not found in PATH!')

        # Replace command name with full path:
        popenargs[0] = command

    return popenargs, cwd


def verbose_check_call(
        *popenargs,
        verbose=True,
        cwd=None,
        extra_env=None,
        exit_on_error=False,
        **kwargs):
    """ 'verbose' version of subprocess.check_call() """

    popenargs, cwd = prepare_popenargs(popenargs, cwd=cwd)

    if verbose:
        _print_info(popenargs, cwd=cwd, kwargs=kwargs)

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

    popenargs, cwd = prepare_popenargs(popenargs, cwd=cwd)

    if verbose:
        _print_info(popenargs, cwd=cwd, kwargs=kwargs)

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
