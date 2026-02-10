"""
Just some shortcuts to print colorful stuff using rich
"""
from cmd2.rich_utils import rich_text_to_string
from rich.console import Console
from rich.text import Text


def red(msg: str) -> str:
    return rich_text_to_string(Text(msg, style='red'))


def green(msg: str) -> str:
    return rich_text_to_string(Text(msg, style='green'))


def yellow(msg: str) -> str:
    return rich_text_to_string(Text(msg, style='yellow'))


def blue(msg: str) -> str:
    return rich_text_to_string(Text(msg, style='blue'))


def magenta(msg: str) -> str:
    return rich_text_to_string(Text(msg, style='magenta'))


def cyan(msg: str) -> str:
    return rich_text_to_string(Text(msg, style='cyan'))


def white(msg: str) -> str:
    return rich_text_to_string(Text(msg, style='white'))


###################################################################################################


def bright_red(msg: str) -> str:
    return rich_text_to_string(Text(msg, style='bright_red'))


def bright_green(msg: str) -> str:
    return rich_text_to_string(Text(msg, style='bright_green'))


def bright_yellow(msg: str) -> str:
    return rich_text_to_string(Text(msg, style='bright_yellow'))


def bright_blue(msg: str) -> str:
    return rich_text_to_string(Text(msg, style='bright_blue'))


def bright_magenta(msg: str) -> str:
    return rich_text_to_string(Text(msg, style='bright_magenta'))


def bright_cyan(msg: str) -> str:
    return rich_text_to_string(Text(msg, style='bright_cyan'))


def bright_white(msg: str) -> str:
    return rich_text_to_string(Text(msg, style='bright_white'))


###################################################################################################


def print_error(err: str) -> None:
    console = Console()
    console.print(f'\n{err}\n', style='bold bright_red')

