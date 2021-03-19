import shutil

import cmd2
from poetry_publish.publish import poetry_publish

from dev_shell.command_sets import DevShellBaseCommandSet
from dev_shell.utils.subprocess_utils import verbose_check_call


def run_linters():
    """
    Run code formatters and linter
    """
    verbose_check_call(
        'flake8',
        '--exclude=.git,__pycache__,.tox,.venv',
        '--max-line-length=119',
    )
    verbose_check_call('isort', '--check-only', '.')
    verbose_check_call('flynt', '--fail-on-change', '--line_length=119', 'dev_shell')


@cmd2.with_default_category('dev-shell commands')
class DevShellCommandSet(DevShellBaseCommandSet):
    def do_pytest(self, statement: cmd2.Statement):
        """
        Run dev-shell tests via pytest
        """
        verbose_check_call('pytest', *statement.arg_list)

    def do_linting(self, statement: cmd2.Statement):
        """
        Linting: Check code style with flake8, isort and flynt
        """
        run_linters()

    def do_fix_code_style(self, statement: cmd2.Statement):
        """
        Fix code style by running: flynt, autopep8 and isort
        """
        verbose_check_call('flynt', '--line_length=119', 'dev_shell')
        verbose_check_call(
            'autopep8', '--aggressive', '--aggressive', '--in-place', '--recursive', 'dev_shell'
        )
        verbose_check_call('isort', '.')

    def do_list_venv_packages(self, statement: cmd2.Statement):
        """
        Just call "pip freeze" to list all installed venv packages
        """
        pip = shutil.which('pip')
        verbose_check_call(pip, 'freeze')

    def do_publish(self, statement: cmd2.Statement):
        """
        Publish "dev-shell" to PyPi
        """
        # Don't publish if test failed or code linting wrong:
        verbose_check_call('pytest', '-x')
        run_linters()

        poetry_publish(
            package_root=self.config.package_path,
            version=self.config.version,
        )
