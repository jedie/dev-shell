import io
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

from cmd2.ansi import strip_style

from dev_shell.utils.subprocess_utils import argv2str


class SubprocessMock:
    def __init__(self, func_name: str = 'check_call'):
        self.func_name = func_name
        self.check_calls = None

    def __enter__(self):
        self.mock = mock.patch(f'subprocess.{self.func_name}').__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.check_calls = []
            for args_list in self.mock.call_args_list:
                # TODO: Use "call.kwargs" and "call.args" if we drop Python 3.7 support!
                args, kwargs = args_list

                popenargs = args[0]
                if isinstance(popenargs, str):
                    command_str = popenargs
                else:
                    command_str = argv2str(popenargs)

                cwd = kwargs.get('cwd')
                if cwd:
                    command_str = f'{cwd}$ {command_str}'

                self.check_calls.append(command_str)
        finally:
            self.mock.__exit__()


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
