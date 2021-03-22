import os
import sys
from pathlib import Path

import cmd2 as cmd2

from dev_shell.config import DevShellConfig
from dev_shell.utils.colorful import bright_blue, bright_yellow
from dev_shell.utils.subprocess_utils import argv2str


class DevShellBaseApp(cmd2.Cmd):
    """
    Base cmd2 App with some gimmicks ;)
    """

    def __init__(self, *args, config: DevShellConfig, **kwargs):
        kwargs.update(dict(
            persistent_history_file='.history',
            allow_cli_args=False
        ))
        super().__init__(*args, **kwargs)

        self.config = config

        self.intro = (
            f'\n\nDeveloper shell - {bright_yellow(config.package_path.name)} - v{config.version}\n'
        )
        self.prompt = f'\n({bright_blue(config.package_path.name)}) '

        # work-a-round: https://github.com/python-cmd2/cmd2/issues/1072
        args = sys.argv[1:]
        if args:
            # CLI usage => execute command and exit
            self.intro = None
            command = argv2str(args)
            self._startup_commands = [command]
        else:
            self._startup_commands = ['help']

        # Set aliases:
        self.aliases.update({
            'q': 'quit',
        })

        # Display Tracebacks on errors:
        self.debug = True

        self.update_path()

    def onecmd(self, *args, **kwargs):
        """
        1. Exit cmdloop if shell was used as CLI ;)
        2. Pass sys.exit() code
        """
        try:
            stop = super().onecmd(*args, **kwargs)
        except SystemExit as exit_code:
            # Pass the sys.exit() code
            # See also: https://github.com/python-cmd2/cmd2/pull/1076
            self.exit_code = exit_code
            stop = True

        return stop

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
        app.onecmd_plus_hooks(line=argv2str(sys.argv[1:]))
        exit_code = app.exit_code
    else:
        exit_code = app.cmdloop()

    sys.exit(exit_code)
