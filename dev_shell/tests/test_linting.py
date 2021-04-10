from unittest import TestCase

from dev_shell.command_sets.dev_shell_commands import run_linters


class LintingTestCase(TestCase):
    def test_linting(self):
        run_linters()
