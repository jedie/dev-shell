import argparse
import sys
from pathlib import Path

import cmd2
from cmd2 import Cmd2ArgumentParser, with_argparser

from dev_shell.command_sets import DevShellBaseCommandSet
from dev_shell.utils.colorful import bright_green
from dev_shell.utils.subprocess_utils import verbose_check_call


@cmd2.with_default_category('dev-shell commands')
class DevShellCommandSet(DevShellBaseCommandSet):
    """
    This command set may be used in external project, too.
    """

    MIN_PY_MAJOR_VERSION = 3
    MIN_PY_MINOR_VERSION = 7

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

    def do_pytest(self, statement: cmd2.Statement):
        """
        Run dev-shell tests via pytest
        """
        verbose_check_call(
            'pytest', *statement.arg_list, cwd=self.config.base_path, exit_on_error=True
        )

    def do_tox(self, statement: cmd2.Statement):
        """
        Call tox and pass all given arguments to it.
        """
        verbose_check_call(
            'tox', *statement.arg_list, cwd=self.config.base_path, exit_on_error=True
        )

    def do_poetry(self, statement: cmd2.Statement):
        """
        Call poetry and pass all given arguments to it.
        """
        verbose_check_call(
            'poetry', *statement.arg_list, cwd=self.config.base_path, exit_on_error=True
        )

    def do_update(self, statement: cmd2.Statement):
        """
        Call "poetry update" to update all dependencies in .venv
        """
        verbose_check_call(
            'poetry',
            'update',
            '-v',
            *statement.arg_list,
            cwd=self.config.base_path,
            exit_on_error=True
        )
        script_name = Path(sys.argv[0]).name
        print(bright_green(f'\n\nPlease restart "{script_name}" !\n'))
        sys.exit(0)  # Stop cmd

    def do_fix_code_style(self, statement: cmd2.Statement):
        """
        Fix code style by running darker
        """
        verbose_check_call('darker', cwd=self.config.base_path)

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
        self.do_pytest(statement)

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
