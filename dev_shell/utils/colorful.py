"""
    Just some shortcuts to print colorful stuff
"""
import cmd2
from cmd2 import fg


def green_bold(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.bright_green, bold=True)


def yellow_bold(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.bright_yellow, bold=True)


def blue_bold(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.bright_blue, bold=True)


def magenta_bold(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.bright_magenta, bold=True)


def print_error(err: str) -> None:
    print(cmd2.ansi.style(
        f'\n{err}\n',
        fg=fg.bright_red, bold=True
    ))


def print_green_bold(msg: str) -> None:
    print(green_bold(msg))


def print_yellow_bold(msg: str) -> None:
    print(yellow_bold(msg))
