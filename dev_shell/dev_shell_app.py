import dev_shell
from dev_shell.base_cmd2_app import DevShellBaseApp, run_cmd2_app
from dev_shell.command_sets.dev_shell_commands import DevShellCommandSet
from dev_shell.config import DevShellConfig


class DevShellApp(DevShellBaseApp):
    """
    The "dev-shell" Cmd2 App
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Just print the help table on startup if no CLI usage (no command passed as argument):
        if not self._startup_commands:
            self._startup_commands = [
                'help',
            ]


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


def main():
    """
    Entry point to start the "dev-shell" cmd2 app.
    Used in: [project.scripts]
    """
    app = DevShellApp(**get_devshell_app_kwargs())
    run_cmd2_app(app)  # Run a cmd2 App as CLI or shell
