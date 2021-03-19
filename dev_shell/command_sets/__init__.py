from cmd2 import CommandSet

from dev_shell.config import DevShellConfig


class DevShellBaseCommandSet(CommandSet):
    def __init__(self, config: DevShellConfig):
        super().__init__()

        self.config = config
