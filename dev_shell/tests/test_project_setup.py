from unittest import TestCase

from cli_base.cli_tools.code_style import assert_code_style
from manageprojects.test_utils.project_setup import check_editor_config, get_py_max_line_length

from dev_shell.constants import PACKAGE_ROOT


class ProjectSetupTestCase(TestCase):
    def test_code_style(self):
        return_code = assert_code_style(package_root=PACKAGE_ROOT)
        self.assertEqual(return_code, 0, 'Code style error, see output above!')

    def test_check_editor_config(self):
        check_editor_config(package_root=PACKAGE_ROOT)

        max_line_length = get_py_max_line_length(package_root=PACKAGE_ROOT)
        self.assertEqual(max_line_length, 119)
