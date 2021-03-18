from pathlib import Path

from poetry_publish.publish import poetry_publish
from poetry_publish.utils.subprocess_utils import verbose_check_call


import dev_shell

PACKAGE_ROOT = Path(__file__).parent


def publish():
    """
    Publish to PyPi
    Call this via:
        $ make publish
    """
    # verbose_check_call('make', 'pytest')  # don't publish if tests fail
    # verbose_check_call('make', 'fix-code-style')  # don't publish if code style wrong

    poetry_publish(
        package_root=PACKAGE_ROOT,
        version=dev_shell.__version__,
    )


if __name__ == '__main__':
    publish()
