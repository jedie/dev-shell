import argparse
import subprocess
import sys

import cmd2
from cli_base.cli_tools.dev_tools import run_coverage, run_unittest_cli
from cli_base.cli_tools.git import Git
from cli_base.cli_tools.subprocess_utils import ToolsExecutor
from cli_base.run_pip_audit import run_pip_audit
from cmd2 import Cmd2ArgumentParser, with_argparser

import dev_shell
from dev_shell import __version__
from dev_shell.command_sets import DevShellBaseCommandSet
from dev_shell.constants import DEV_SHELL_PKG_PATH
from dev_shell.utils.colorful import bright_green
from dev_shell.utils.subprocess_utils import verbose_check_call


try:
    from manageprojects.utilities.publish import publish_package  # dev dependency
except ModuleNotFoundError:
    publish_package = None


@cmd2.with_default_category('dev-shell commands')
class DevShellCommandSet(DevShellBaseCommandSet):
    """
    This command set may be used in external project, too.
    """

    MIN_PY_MAJOR_VERSION = 3
    MIN_PY_MINOR_VERSION = 12

    pyupgrade_argparser = Cmd2ArgumentParser()
    pyupgrade_argparser.add_argument(
        '--major-version', dest='major', action='store_const', default=MIN_PY_MAJOR_VERSION
    )
    pyupgrade_argparser.add_argument(
        '--minor-version', dest='minor', action='store_const', default=MIN_PY_MINOR_VERSION
    )

    @with_argparser(pyupgrade_argparser)
    def do_pyupgrade(self, args: argparse.Namespace):
        """
        Run pyupgrade
        """
        base_path = self.config.base_path
        print(f'Run PyUpgrade over "{base_path}" (min version: {args.major}.{args.minor})')
        args.min_version = (args.major, args.minor)

        # uv tool run pyupgrade --py312-plus $(git ls-files -- '*.py')

        git = Git()
        files = [str(path) for path in git.ls_files() if path.suffix == '.py']

        try:
            verbose_check_call(
                'uv',
                'tool',
                'run',
                'pyupgrade',
                f'--py{args.major}{args.minor}-plus',
                *files,
                verbose=True,
                exit_on_error=False,
            )
        except subprocess.CalledProcessError:
            return  # info already printed by verbose_check_call

    def do_test(self, statement: cmd2.Statement):
        """
        Run the project's test suite using the unittest runner.
        """
        run_unittest_cli(argv=statement.arg_list)

    def do_coverage(self, statement: cmd2.Statement):
        """
        Run the project's test suite using the unittest runner and create a coverage report.
        """
        run_coverage()

    def do_install(self, statement: cmd2.Statement):
        """
        Install current project as editable via pip
        """
        tools_executor = ToolsExecutor(cwd=self.config.base_path)
        tools_executor.verbose_check_call('pip', 'install', '-e', '.')

    def do_update(self, statement: cmd2.Statement):
        """
        Call "poetry update" to update all dependencies in .venv
        """
        tools_executor = ToolsExecutor(cwd=self.config.base_path)
        tools_executor.verbose_check_call('uv', 'lock', '--upgrade')

        run_pip_audit(base_path=self.config.base_path)

        # Install new dependencies in current .venv:
        tools_executor.verbose_check_call('uv', 'sync')

        if tools_executor.is_executable('pre-commit'):
            # Update git pre-commit hooks:
            tools_executor.verbose_check_call('pre-commit', 'autoupdate')

        print(bright_green('\n\nPlease restart the shell !\n'))
        sys.exit(0)  # Stop cmd

    def do_fix_code_style(self, statement: cmd2.Statement):
        """
        Fix code style by running ruff
        """
        verbose_check_call(
            'uv',
            'tool',
            'run',
            'ruff',
            'check',
            '--fix',
            exit_on_error=False,
        )

    def do_list_venv_packages(self, statement: cmd2.Statement):
        """
        Just call "pip freeze" to list all installed venv packages
        """
        verbose_check_call('uv', 'pip', 'freeze', cwd=self.config.base_path)

    def do_publish(self, statement: cmd2.Statement):
        """
        Publish "dev-shell" to PyPi
        """
        run_unittest_cli(verbose=False, exit_after_run=False)  # Don't publish a broken state

        publish_package(
            module=dev_shell,
            package_path=DEV_SHELL_PKG_PATH.parent,
            distribution_name='dev-shell',
        )

    def do_version(self, statement: cmd2.Statement):
        print(__version__)
        sys.exit(0)  # Stop cmd


if publish_package is None:
    # Remove the "publish" command
    del DevShellCommandSet.do_publish
