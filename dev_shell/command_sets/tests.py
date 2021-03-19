import shutil

import cmd2

from dev_shell.command_sets import DevShellBaseCommandSet
from dev_shell.utils.subprocess_utils import verbose_check_call


@cmd2.with_default_category('Tests')
class TestCommandSet(DevShellBaseCommandSet):
    def do_pytest(self, statement: cmd2.Statement):
        """
        Run dev-shell tests via pytest
        """
        pytest = shutil.which('pytest')
        popenargs = [pytest] + statement.arg_list
        verbose_check_call(*popenargs)

    def do_list_venv_packages(self, statement: cmd2.Statement):
        """
        Just call "pip freeze" to list all installed venv packages
        """
        pip = shutil.which('pip')
        verbose_check_call(pip, 'freeze')
