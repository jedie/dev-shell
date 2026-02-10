import subprocess
from unittest import TestCase

from bx_py_utils.path import assert_is_file
from cli_base.cli_tools.code_style import assert_code_style
from cli_base.cli_tools.test_utils.assertion import assert_in
from manageprojects.test_utils.project_setup import check_editor_config, get_py_max_line_length
from packaging.version import Version

from dev_shell import __version__
from dev_shell.tests.constants import DEV_SHELL_PACKAGE_ROOT


class ProjectSetupTestCase(TestCase):
    def test_version(self):
        self.assertIsNotNone(__version__)

        version = Version(__version__)  # Will raise InvalidVersion() if wrong formatted
        self.assertEqual(str(version), __version__)

        dev_cli_bin = DEV_SHELL_PACKAGE_ROOT / 'devshell.py'
        assert_is_file(dev_cli_bin)

        output = subprocess.check_output([dev_cli_bin, 'version'], text=True)
        assert_in(content=output, parts=(__version__,))

    def test_code_style(self):
        return_code = assert_code_style(package_root=DEV_SHELL_PACKAGE_ROOT)
        self.assertEqual(return_code, 0, 'Code style error, see output above!')

    def test_check_editor_config(self):
        check_editor_config(package_root=DEV_SHELL_PACKAGE_ROOT)

        max_line_length = get_py_max_line_length(package_root=DEV_SHELL_PACKAGE_ROOT)
        self.assertEqual(max_line_length, 119)

    # def test_pre_commit_hooks(self):
    #     executor = ToolsExecutor(cwd=DEV_SHELL_PACKAGE_ROOT)
    #     for command in ('migrate-config', 'validate-config', 'validate-manifest'):
    #         executor.verbose_check_call('pre-commit', command, exit_on_error=True)
