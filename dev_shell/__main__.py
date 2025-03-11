"""
Allow dev_shell to be executable
through `python -m dev_shell`.
"""

from dev_shell.dev_shell_app import devshell_cmdloop


if __name__ == '__main__':
    devshell_cmdloop()
