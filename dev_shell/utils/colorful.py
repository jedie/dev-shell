"""
Just some shortcuts to print colorful stuff using rich
"""

from rich.console import Console
from rich.text import Text


def red(msg: str) -> str:
    return str(Text(msg, style='red'))


def green(msg: str) -> str:
    return str(Text(msg, style='green'))


def yellow(msg: str) -> str:
    return str(Text(msg, style='yellow'))


def blue(msg: str) -> str:
    return str(Text(msg, style='blue'))


def magenta(msg: str) -> str:
    return str(Text(msg, style='magenta'))


def cyan(msg: str) -> str:
    return str(Text(msg, style='cyan'))


def white(msg: str) -> str:
    return str(Text(msg, style='white'))


###################################################################################################


def bright_red(msg: str) -> str:
    return str(Text(msg, style='bright_red'))


def bright_green(msg: str) -> str:
    return str(Text(msg, style='bright_green'))


def bright_yellow(msg: str) -> str:
    return str(Text(msg, style='bright_yellow'))


def bright_blue(msg: str) -> str:
    return str(Text(msg, style='bright_blue'))


def bright_magenta(msg: str) -> str:
    return str(Text(msg, style='bright_magenta'))


def bright_cyan(msg: str) -> str:
    return str(Text(msg, style='bright_cyan'))


def bright_white(msg: str) -> str:
    return str(Text(msg, style='bright_white'))


###################################################################################################


def print_error(err: str) -> None:
    console = Console()
    console.print(f'\n{err}\n', style='bold bright_red')
