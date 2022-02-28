"""
    Just some shortcuts to print colorful stuff
"""
import cmd2
from cmd2 import Fg


def red(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=Fg.RED, bold=False)


def green(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=Fg.GREEN, bold=False)


def yellow(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=Fg.YELLOW, bold=False)


def blue(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=Fg.BLUE, bold=False)


def magenta(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=Fg.MAGENTA, bold=False)


def cyan(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=Fg.CYAN, bold=False)


def white(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=Fg.LIGHT_GRAY, bold=False)


###################################################################################################


def bright_red(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=Fg.LIGHT_RED, bold=False)


def bright_green(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=Fg.LIGHT_GREEN, bold=False)


def bright_yellow(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=Fg.LIGHT_YELLOW, bold=False)


def bright_blue(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=Fg.LIGHT_BLUE, bold=False)


def bright_magenta(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=Fg.LIGHT_MAGENTA, bold=False)


def bright_cyan(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=Fg.LIGHT_CYAN, bold=False)


def bright_white(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=Fg.WHITE, bold=False)


###################################################################################################


def print_error(err: str) -> None:
    print(bright_red(f'\n{err}\n'))
