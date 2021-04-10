import dataclasses
from pathlib import Path
from typing import Any


@dataclasses.dataclass
class DevShellConfig:
    package_module: Any = None  # The module for this shell

    # Set by post init from package_module:
    version: str = dataclasses.field(init=False)
    package_path: Path = dataclasses.field(init=False)
    base_path: Path = dataclasses.field(init=False)

    def __post_init__(self):
        assert self.package_module, 'Package module must be set!'

        assert hasattr(self.package_module, '__version__'), (
            f'{self.package_module!r} must have a __version__ attribute!'
        )
        assert hasattr(self.package_module, '__file__'), (
            f'{self.package_module!r} must have a __file__ attribute!'
        )

        self.version = self.package_module.__version__
        self.package_path = Path(self.package_module.__file__).parent
        self.base_path = self.package_path.parent
