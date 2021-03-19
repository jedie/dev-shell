"""
    Just some shortcuts to print colorful stuff
"""
import cmd2
from cmd2 import fg


def red(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.red, bold=False)


def green(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.green, bold=False)


def yellow(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.yellow, bold=False)


def blue(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.blue, bold=False)


def magenta(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.magenta, bold=False)


def cyan(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.cyan, bold=False)


def white(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.white, bold=False)


###################################################################################################


def bright_red(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.bright_red, bold=False)


def bright_green(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.bright_green, bold=False)


def bright_yellow(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.bright_yellow, bold=False)


def bright_blue(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.bright_blue, bold=False)


def bright_magenta(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.bright_magenta, bold=False)


def bright_cyan(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.bright_cyan, bold=False)


def bright_white(msg: str) -> str:
    return cmd2.ansi.style(msg, fg=fg.bright_white, bold=False)


###################################################################################################


def print_error(err: str) -> None:
    print(bright_red(f'\n{err}\n'))
