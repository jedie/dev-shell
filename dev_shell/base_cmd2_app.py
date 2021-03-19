import os
import sys
from pathlib import Path

import cmd2 as cmd2

from dev_shell.config import DevShellConfig
from dev_shell.utils.colorful import blue_bold, yellow_bold
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
            f'\n\nDeveloper shell - {yellow_bold(config.package_path.name)} - v{config.version}\n'
        )
        self.prompt = f'\n({blue_bold(config.package_path.name)}) '

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

    def onecmd_plus_hooks(self, *args, **kwargs):
        """
        Exit cmdloop if shell was used as CLI ;)
        """
        stop = super().onecmd_plus_hooks(*args, **kwargs)
        if len(sys.argv) > 1:
            # cli usage => exit cmd loop
            stop = True
            print()
        return stop

    def update_path(self):
        """
        Add our .venv/bin/ directory into PATH at first position.
        """
        bin_path = str(Path(sys.executable).parent.absolute())
        env_path = os.environ.get('PATH', '')
        if not env_path.startswith(bin_path):
            os.environ['PATH'] = bin_path + os.pathsep + env_path
