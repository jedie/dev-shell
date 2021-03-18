import shutil

import cmd2

from dev_shell.command_sets import DevShellBaseCommandSet
from dev_shell.utils.subprocess_utils import verbose_check_call


@cmd2.with_default_category('Tests')
class TestCommandSet(DevShellBaseCommandSet):
    def do_pytest(self, statement: cmd2.Statement):

        pytest = shutil.which('pytest')

        # pytest_path = Path(sys.exec_prefix) / 'pytest'
        # assert_is_file(pytest_path)

        popenargs = [pytest] + statement.arg_list
        verbose_check_call(*popenargs)
