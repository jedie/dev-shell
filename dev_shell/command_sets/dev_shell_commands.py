import argparse
import sys
from pathlib import Path

import cmd2
from cli_base.cli_tools import code_style
from cli_base.cli_tools.dev_tools import run_coverage, run_unittest_cli
from cli_base.cli_tools.subprocess_utils import ToolsExecutor
from cli_base.run_pip_audit import run_pip_audit
from cmd2 import Cmd2ArgumentParser, with_argparser

import dev_shell
from dev_shell import __version__
from dev_shell.command_sets import DevShellBaseCommandSet
from dev_shell.constants import PACKAGE_ROOT
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
    MIN_PY_MINOR_VERSION = 11

    pyupgrade_argparser = Cmd2ArgumentParser()
    pyupgrade_argparser.add_argument('--exit-zero-even-if-changed', action='store_true')
    pyupgrade_argparser.add_argument('--keep-percent-format', action='store_true')
    pyupgrade_argparser.add_argument('--keep-mock', action='store_true')
    pyupgrade_argparser.add_argument('--keep-runtime-typing', action='store_true')
    pyupgrade_argparser.add_argument(
        '--major-version', dest='major', action='store_const', const=3, default=MIN_PY_MAJOR_VERSION
    )
    pyupgrade_argparser.add_argument(
        '--minor-version', dest='minor', action='store_const', const=7, default=MIN_PY_MINOR_VERSION
    )

    @with_argparser(pyupgrade_argparser)
    def do_pyupgrade(self, args: argparse.Namespace):
        """
        Run pyupgrade
        """
        base_path = self.config.base_path
        print(f'Run PyUpgrade over "{base_path}" (min version: {args.major}.{args.minor})')
        args.min_version = (args.major, args.minor)

        from pyupgrade._main import _fix_file

        total_count = 0
        change_count = 0

        for file_path in base_path.glob('**/*.py'):
            rel_path = file_path.relative_to(base_path)
            dir_name = rel_path.parts[0]
            if dir_name.startswith('.'):
                continue

            total_count += 1
            changed = _fix_file(filename=file_path, args=args)
            if changed:
                change_count += 1
        print(f'Out of {total_count} files, {change_count} have been updated.')

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

    def do_update(self, statement: cmd2.Statement):
        """
        Call "poetry update" to update all dependencies in .venv
        """
        tools_executor = ToolsExecutor(cwd=PACKAGE_ROOT)

        tools_executor.verbose_check_call('pip', 'install', '-U', 'pip')
        tools_executor.verbose_check_call('pip', 'install', '-U', 'uv')
        tools_executor.verbose_check_call('uv', 'lock', '--upgrade')

        run_pip_audit(base_path=PACKAGE_ROOT)

        # Install new dependencies in current .venv:
        tools_executor.verbose_check_call('uv', 'sync')

        script_name = Path(sys.argv[0]).name
        print(bright_green(f'\n\nPlease restart "{script_name}" !\n'))
        sys.exit(0)  # Stop cmd

    def do_fix_code_style(self, statement: cmd2.Statement):
        """
        Fix code style by running darker
        """
        code_style.fix(package_root=self.config.base_path)

    def do_check_code_style(self, statement: cmd2.Statement):
        """
        Check code style by running darker
        """
        code_style.check(package_root=self.config.base_path)

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
        run_unittest_cli(verbose=False, exit_after_run=False)  # Don't publish a broken state

        publish_package(module=dev_shell, package_path=PACKAGE_ROOT, distribution_name='dev-shell')

    def do_version(self, statement: cmd2.Statement):
        print(__version__)
        sys.exit(0)  # Stop cmd


if publish_package is None:
    # Remove the "publish" command
    del DevShellCommandSet.do_publish
