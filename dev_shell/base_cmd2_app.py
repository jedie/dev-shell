import os
import shlex
import sys
from pathlib import Path

import cmd2

from dev_shell.config import DevShellConfig
from dev_shell.utils.colorful import bright_blue, bright_yellow


class DevShellBaseApp(cmd2.Cmd):
    """
    Base cmd2 App with some gimmicks ;)
    """

    # Remove some default cmd2 commands:
    delattr(cmd2.Cmd, 'do_edit')
    delattr(cmd2.Cmd, 'do_shell')
    delattr(cmd2.Cmd, 'do_run_script')
    delattr(cmd2.Cmd, 'do_run_pyscript')

    def __init__(self, *args, config: DevShellConfig, **kwargs):
        kwargs.update(dict(persistent_history_file='.history', allow_cli_args=False))
        super().__init__(*args, **kwargs)

        self.config = config

        self.intro = f'\n\nDeveloper shell - {bright_yellow(config.package_path.name)} - v{config.version}\n'
        self.prompt = f'\n({bright_blue(config.package_path.name)}) '

        # Set aliases:
        self.aliases.update(
            {
                'q': 'quit',
                '--help': 'help',  # Support --help as alias for help
            }
        )

        # Display Tracebacks on errors:
        self.debug = True

        self.update_path()

    def update_path(self):
        """
        Add our .venv/bin/ directory into PATH at first position.
        """
        bin_path = str(Path(sys.executable).parent.absolute())
        env_path = os.environ.get('PATH', '')
        if not env_path.startswith(bin_path):
            os.environ['PATH'] = bin_path + os.pathsep + env_path


def run_cmd2_app(app: cmd2.Cmd) -> None:
    """
    Run a cmd2 App as CLI or shell.
    Handle exit code return value, too.
    """
    if len(sys.argv) > 1:
        # CLI usage => run only one command and then exit
        app.onecmd_plus_hooks(line=shlex.join(sys.argv[1:]))
        exit_code = app.exit_code
    else:
        exit_code = app.cmdloop()

    sys.exit(exit_code)
