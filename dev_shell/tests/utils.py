from unittest import mock

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
            for call in self.mock.call_args_list:
                kwargs = call.kwargs

                args = call.args
                assert len(args) == 1
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
