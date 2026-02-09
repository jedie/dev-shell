from unittest.case import TestCase

from bx_py_utils.test_utils.redirect import RedirectOut
from cli_base.cli_tools.test_utils.rich_test_utils import NoColorEnvRich

from dev_shell.dev_shell_app import DevShellApp, get_devshell_app_kwargs


class CmdAppBaseTestCase(TestCase):
    """
    Base class for cmd2 app test cases
    """

    maxDiff = None

    def get_app_instance(self):
        """
        :return: cmd2 app instance
        """
        raise NotImplementedError

    def execute(self, command):
        with RedirectOut() as out_buffer, NoColorEnvRich():
            app = self.get_app_instance()
            app.onecmd_plus_hooks(command)
        return out_buffer.stdout, out_buffer.stderr


class DevShellAppBaseTestCase(CmdAppBaseTestCase):
    """
    Base class for dev-shell tests
    """

    def get_app_instance(self):
        # Init the test app with the same kwargs as the real app
        # see: dev_shell.cmd2app.devshell_cmdloop()
        app = DevShellApp(**get_devshell_app_kwargs())
        return app
