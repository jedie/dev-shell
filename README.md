# A "dev-shell" for Python projects ;)

**Note: The continuation of this project is uncertain!**

[![tests](https://github.com/jedie/dev-shell/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/dev-shell/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/dev_shell/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/dev_shell)
[![dev_shell @ PyPi](https://img.shields.io/pypi/v/dev_shell?label=dev_shell%20%40%20PyPi)](https://pypi.org/project/dev_shell/)
[![Python Versions](https://img.shields.io/pypi/pyversions/dev_shell)](https://github.com/jedie/dev-shell/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/dev_shell)](https://github.com/jedie/dev-shell/blob/main/LICENSE)


This small project is intended to improve the start-up for collaborators.

The idea is to make the project setup as simple as possible. Just clone the sources and start a script and you're done ;)

Why in hell not just a `Makefile`? Because it doesn't out-of-the-box under Windows and MacOS, the dev-shell does ;)

Run Tests? Just start the script and call the "run test command".

The "dev-shell" is the base to create a CLI and a shell. It also shows how to make a project bootstrap as simply as possible, e.g.:


At least `uv` is needed. Install e.g.: via pipx:
```bash
apt-get install pipx
pipx install uv
```

Clone the project and just start the CLI help commands.
A virtual environment will be created/updated automatically.

```bash
~$ git clone https://github.com/jedie/dev-shell.git
~$ cd dev-shell
~/dev-shell$ devshell.py --help
~/dev-shell$ devshell.py test
```


The output on first bootstrap start looks like:

```bash
~/dev-shell$ ./devshell.py

Developer shell - dev_shell - v0.10.0


dev-shell commands
──────────────────
check_code_style  fix_code_style  list_venv_packages  pyupgrade  update
coverage          install         publish             test       version

Uncategorized Commands
──────────────────────
alias  help  history  macro  quit  set  shortcuts

(dev_shell) quit
~/dev-shell$
```


## compatibility

| dev-shell version | OS                      | Python version      |
|-------------------|-------------------------|---------------------|
| >=v0.10.0         | Linux + MacOS + Windows | 3.14, 3.13, 3.12    |
| >=v0.7.0          | Linux + MacOS + Windows | 3.11, 3.10, 3.9     |
| >=v0.5.0          | Linux + MacOS + Windows | 3.10, 3.9, 3.8, 3.7 |
| >=v0.0.1          | Linux + MacOS + Windows | 3.9, 3.8, 3.7       |

See also:
* github test configuration: [.github/workflows/test.yml](https://github.com/jedie/dev-shell/blob/main/.github/workflows/test.yml)
* Nox configuration: [noxfile.py](https://github.com/jedie/dev-shell/blob/main/noxfile.py)

## History

* [*dev*](https://github.com/jedie/dev-shell/compare/v0.10.1...main)
  * TBC
* [0.10.1 - 2026-02-10](https://github.com/jedie/dev-shell/compare/v0.10.0...v0.10.1)
  * Bugfix colorful shortcuts
* [0.10.0 - 2026-02-10](https://github.com/jedie/dev-shell/compare/v0.9.1...v0.10.0)
  * Modernize codebase
* [0.9.1 - 2025-03-11](https://github.com/jedie/dev-shell/compare/v0.9.0...v0.9.1)
  * Fix usage as package in external projects
* [0.9.0 - 2025-03-11](https://github.com/jedie/dev-shell/compare/v0.8.0...v0.9.0)
  * Replace `poetry` with `uv`
* [0.8.0 - 2024-04-09](https://github.com/jedie/dev-shell/compare/v0.7.0...v0.8.0)
  * Remove "gnureadline" as dependency
  * update boot script
  * update requirements
* [0.7.0 - 2023-04-25](https://github.com/jedie/dev-shell/compare/v0.6.1...v0.7.0)
  * Update test matrix
  * update requirements
* [0.6.1 - 2022-09-02](https://github.com/jedie/dev-shell/compare/v0.6.0...v0.6.1)
  * Set default subprocess timeout to 5 Min.
  * Skip buggy Poetry v1.2.0
  * Update requirements
* [0.6.0 - 2022-07-19](https://github.com/jedie/dev-shell/compare/v0.5.0...v0.6.0)
  * Add "pyupgrade" as shell command
* [0.5.0 - 2022-05-29](https://github.com/jedie/dev-shell/compare/v0.4.0...v0.5.0)
  * Add "tox" and "poetry" commands to call them installed in created ```.venv```
  * Update requirements
* [v0.4.0 - 2022-02-28](https://github.com/jedie/dev-shell/compare/v0.3.0...v0.4.0)
  * Update to new cmd2, colorama and pytest versions
* [v0.3.0 - 2022-01-30](https://github.com/jedie/dev-shell/compare/v0.2.4...v0.3.0)
  * Remove "flynt" form linting/fix code style
* [v0.2.4 - 2022-01-30](https://github.com/jedie/dev-shell/compare/v0.2.3...v0.2.4)
  * Update requirements
  * Use darker as code formatter and pytest-darker for linting
* [v0.2.3 - 2021-11-15](https://github.com/jedie/dev-shell/compare/v0.2.2...v0.2.3)
  * Update requirements
  * [Flynt arguments can be changes via CommandSet](https://github.com/jedie/dev-shell/issues/29)
* [v0.2.2 - 2021-04-13](https://github.com/jedie/dev-shell/compare/v0.2.1...v0.2.2)
  * Include bootstrap file, to it's possible to use it in external projects, too.
* [v0.2.1 - 2021-04-12](https://github.com/jedie/dev-shell/compare/v0.2.0...v0.2.1)
  * Handle if "poetry-publish" is not installed, so a project that used "dev-shell" must not install it.
* [v0.2.0 - 2021-04-11](https://github.com/jedie/dev-shell/compare/v0.1.0...v0.2.0)
  * Rename: "dev-shell.py => devshell.py" because of better autocomplete
  * Add `DevShellConfig.base_path` and use it in own commands like, `pytest`, `linting` etc. (So they are usable in external project, too.)
  * recognize "--update" and "--help" arguments better in `./devshell.py` calls.
  * Update `setuptools` on `.venv` creation, too.
  * Fix Bugs/tests under Windows
* [v0.1.0 - 2021-03-22](https://github.com/jedie/dev-shell/compare/v0.0.2...v0.1.0)
  * Fix CI usage: Exit with correct return code if tests failed
  * Better "run as CLI" implementation via new `run_cmd2_app()`
  * Bugfix errors that only occur on Windows.
  * Simplify `devshell.py` boot script and fix raise error if `ensurepip` missing
* [v0.0.2 - 2021-03-19](https://github.com/jedie/dev-shell/compare/v0.0.1...v0.0.2)
  * refactor colorful shortcuts
  * display subprocess calls with separated colors
* [v0.0.1 - 2021-03-19](https://github.com/jedie/dev-shell/compare/ad5dca...v0.0.1)
  * first "useable" version

## Project links

* Github: https://github.com/jedie/dev-shell/
* PyPi: https://pypi.org/project/dev-shell/
