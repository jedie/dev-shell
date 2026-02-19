from bx_py_utils.auto_doc import assert_readme_block
from bx_py_utils.path import assert_is_file
from cli_base.cli_tools.test_utils.assertion import assert_in
from cli_base.cli_tools.test_utils.rich_test_utils import NoColorEnvRich, invoke
from manageprojects.tests.base import BaseTestCase

from dev_shell.constants import DEV_SHELL_PKG_PATH


def assert_cli_help_in_readme(text_block: str, marker: str):
    README_PATH = DEV_SHELL_PKG_PATH.parent / 'README.md'
    assert_is_file(README_PATH)

    text_block = '\n'.join(text_block.splitlines()[2:])

    text_block = f'```\n{text_block.strip()}\n```'
    assert_readme_block(
        readme_path=README_PATH,
        text_block=text_block,
        start_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} start ✂✂✂)',
        end_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} end ✂✂✂)',
    )


class ReadmeTestCase(BaseTestCase):
    def test_devshell_help(self):
        with NoColorEnvRich():
            stdout = invoke(cli_bin=DEV_SHELL_PKG_PATH.parent / 'devshell.py', args=['help'])

        assert_in(
            content=stdout,
            parts=(
                'dev-shell commands',
                'fix_code_style',
                'publish',
            ),
        )

        assert_cli_help_in_readme(text_block=stdout, marker='main help')
