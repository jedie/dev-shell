from unittest.case import TestCase

from cmd2 import CommandResult
from cmd2.ansi import strip_style
from cmd2_ext_test import ExternalTestMixin

from dev_shell.dev_shell_app import DevShellApp, get_devshell_app_kwargs


class CmdAppBaseTestCase(TestCase):
    """
    Base class for cmd2 app test cases
    """

    def get_app_instance(self):
        """
        :return: cmd2 app instance
        """
        raise NotImplementedError

    def setUp(self):
        super().setUp()
        self.app = self.get_app_instance()
        self.app.fixture_setup()

    def tearDown(self):
        super().tearDown()
        self.app.fixture_teardown()

    def execute(self, command, remove_colors=True):
        out = self.app.app_cmd(command)

        assert isinstance(out, CommandResult)
        if out.stdout is None:
            stdout = ''
        else:
            stdout = str(out.stdout)
            if remove_colors:
                stdout = strip_style(stdout)

        if out.stderr is None:
            stderr = ''
        else:
            stderr = str(out.stderr)
            if remove_colors:
                stderr = strip_style(stderr)

        return stdout, stderr


class DevShellAppTester(ExternalTestMixin, DevShellApp):
    pass


class DevShellAppBaseTestCase(CmdAppBaseTestCase):
    """
    Base class for dev-shell tests
    """

    def get_app_instance(self):
        # Init the test app with the same kwargs as the real app
        # see: dev_shell.cmd2app.devshell_cmdloop()
        app = DevShellAppTester(**get_devshell_app_kwargs())
        return app
