import sys
from pathlib import Path

import cmd2

from dev_shell.command_sets import DevShellBaseCommandSet
from dev_shell.utils.colorful import bright_green
from dev_shell.utils.subprocess_utils import verbose_check_call


def run_linters(cwd=None):
    """
    Run code formatters and linter
    """
    verbose_check_call(
        'flake8',
        cwd=cwd,
        exit_on_error=True
    )
    verbose_check_call(
        'isort', '--check-only', '.',
        cwd=cwd,
        exit_on_error=True
    )
    verbose_check_call(
        'flynt', '--fail-on-change', '--line_length=119', '.',
        cwd=cwd,
        exit_on_error=True
    )


@cmd2.with_default_category('dev-shell commands')
class DevShellCommandSet(DevShellBaseCommandSet):
    """
    This command set may be used in external project, too.
    """

    def do_pytest(self, statement: cmd2.Statement):
        """
        Run dev-shell tests via pytest
        """
        verbose_check_call(
            'pytest',
            *statement.arg_list,
            cwd=self.config.base_path,
            exit_on_error=True
        )

    def do_update(self, statement: cmd2.Statement):
        """
        Call "poetry update" to update all dependencies in .venv
        """
        verbose_check_call(
            'poetry', 'update',
            *statement.arg_list,
            cwd=self.config.base_path,
            exit_on_error=True
        )
        script_name = Path(sys.argv[0]).name
        print(bright_green(f'\n\nPlease restart "{script_name}" !\n'))
        sys.exit(0)  # Stop cmd

    def do_linting(self, statement: cmd2.Statement):
        """
        Linting: Check code style with flake8, isort and flynt
        """
        run_linters(cwd=self.config.base_path)

    def do_fix_code_style(self, statement: cmd2.Statement):
        """
        Fix code style by running: flynt, autopep8 and isort
        """
        verbose_check_call(
            'flynt', '--line_length=119', '.',
            cwd=self.config.base_path
        )
        verbose_check_call(
            'autopep8', '--aggressive', '--aggressive', '--in-place', '--recursive', '.',
            cwd=self.config.base_path
        )
        verbose_check_call(
            'isort', '.',
            cwd=self.config.base_path
        )

    def do_list_venv_packages(self, statement: cmd2.Statement):
        """
        Just call "pip freeze" to list all installed venv packages
        """
        verbose_check_call(
            'pip', 'freeze',
            cwd=self.config.base_path
        )

    def do_publish(self, statement: cmd2.Statement):
        """
        Publish "dev-shell" to PyPi
        """
        # Maybe a project that use dev-shell doesn't use poetry-publish, too!
        # So import it here to make this dependency "optional"
        from poetry_publish.publish import poetry_publish  # noqa

        # Don't publish if test failed or code linting wrong:
        verbose_check_call(
            'pytest', '-x',
            cwd=self.config.base_path,
            exit_on_error=True,
        )
        run_linters(cwd=self.config.base_path)

        poetry_publish(
            package_root=self.config.base_path,
            version=self.config.version,
        )


# Maybe a project that use dev-shell doesn't use poetry-publish:
try:
    import poetry_publish  # noqa
except ModuleNotFoundError:
    # Remove the "publish" command
    del DevShellCommandSet.do_publish
