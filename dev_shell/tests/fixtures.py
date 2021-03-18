from unittest.case import TestCase


from cmd2 import CommandResult
from cmd2_ext_test import ExternalTestMixin

from dev_shell.cmd2app import DevShellApp,  get_devshell_app_kwargs


class DevShellAppTester(ExternalTestMixin, DevShellApp):
    pass


class DevShellAppBaseTestCase(TestCase):
    def setUp(self):
        super().setUp()

        # Init in the same way as in: bx_dev_setup.dev_setup.shell() !
        self.app = DevShellAppTester(**get_devshell_app_kwargs())

        self.app.fixture_setup()

    def tearDown(self):
        super().tearDown()
        self.app.fixture_teardown()

    def execute(self, command):
        out = self.app.app_cmd(command)

        assert isinstance(out, CommandResult)
        if out.stdout is None:
            stdout = ''
        else:
            stdout = str(out.stdout)

        if out.stderr is None:
            stderr = ''
        else:
            stderr = str(out.stderr)

        return stdout, stderr
