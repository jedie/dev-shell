import sys

import dev_shell
from dev_shell.base_cmd2_app import DevShellBaseApp
from dev_shell.command_sets.dev_shell_commands import DevShellCommandSet
from dev_shell.config import DevShellConfig


class DevShellApp(DevShellBaseApp):
    """
    The "dev-shell" Cmd2 App
    """
    pass


def get_devshell_app_kwargs():
    """
    Generate the kwargs for the cmd2 App.
    (Separated because we needs the same kwargs in tests)
    """
    config = DevShellConfig(package_module=dev_shell)

    # initialize all CommandSet() with context:
    kwargs = dict(
        config=config
    )

    app_kwargs = dict(
        config=config,
        command_sets=[
            DevShellCommandSet(**kwargs),
        ]
    )
    return app_kwargs


def devshell_cmdloop():
    """
    Entry point to start the "dev-shell" cmd2 app.
    Used in: [tool.poetry.scripts]
    """
    c = DevShellApp(**get_devshell_app_kwargs())
    sys.exit(c.cmdloop())
