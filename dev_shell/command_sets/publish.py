import cmd2
from dev_shell.command_sets import DevShellBaseCommandSet
from poetry_publish.publish import poetry_publish


@cmd2.with_default_category('Publish')
class PublishCommandSet(DevShellBaseCommandSet):
    def do_publish(self, statement: cmd2.Statement):
        poetry_publish(
            package_root=self.config.package_path,
            version=self.config.version,
        )
