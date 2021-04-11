import io
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

from cmd2.ansi import strip_style


def call_mocked_subprocess(func_name, func, *args, catch_sys_exit=False, **kwargs):
    with mock.patch(f'subprocess.{func_name}') as cm:
        try:
            result = func(*args, **kwargs)
        except SystemExit:
            if not catch_sys_exit:
                raise
            result = None

        check_calls = []
        for args_list in cm.call_args_list:
            # TODO: Use "call.kwargs" and "call.args" if we drop Python 3.7 support!
            args, kwargs = args_list

            popenargs = args[0]
            if isinstance(popenargs, str):
                command_str = popenargs
            else:
                command_str = ' '.join(popenargs)

            cwd = kwargs.get('cwd')
            if cwd:
                command_str = f'{cwd}$ {command_str}'

            check_calls.append(command_str)

        return check_calls, result


class RedirectStdOutErr:
    """
    Buffer stdout + stderr with optional strip_style() call
    """

    def __init__(self):
        self._buffer = io.StringIO()
        self._output = None

    def __enter__(self):
        self._stdout_redirect = redirect_stdout(self._buffer).__enter__()
        self._stderr_redirect = redirect_stderr(self._buffer).__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._output = self._buffer.getvalue()
        finally:
            self._stdout_redirect.__exit__(exc_type, exc_val, exc_tb)
            self._stderr_redirect.__exit__(exc_type, exc_val, exc_tb)

    def get_output(self, remove_ansi=False):
        output = self._output
        if remove_ansi:
            output = strip_style(output)
        return output
