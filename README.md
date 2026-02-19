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

The output looks like:

[comment]: <> (✂✂✂ auto generated main help start ✂✂✂)
```
dev-shell commands
──────────────────
coverage        install             publish    test    version
fix_code_style  list_venv_packages  pyupgrade  update

Uncategorized Commands
──────────────────────
alias  help  history  macro  quit  set  shortcuts
```
[comment]: <> (✂✂✂ auto generated main help end ✂✂✂)




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

[comment]: <> (✂✂✂ auto generated history start ✂✂✂)

* [v0.10.2](https://github.com/jedie/dev-shell/compare/v0.10.1...v0.10.2)
  * 2026-02-19 - apply manageprojects updates
  * 2026-02-19 - Bugfix colorful helpers if a Path instance should be printed.
* [v0.10.1](https://github.com/jedie/dev-shell/compare/v0.10.0...v0.10.1)
  * 2026-02-10 - Bugfix text color styles
* [v0.10.0](https://github.com/jedie/dev-shell/compare/v0.9.1...v0.10.0)
  * 2026-02-10 - Cleanup
  * 2026-02-09 - Update project
* [v0.9.1](https://github.com/jedie/dev-shell/compare/v0.9.0...v0.9.1)
  * 2025-03-11 - Fix usage as package in external projects

<details><summary>Expand older history entries ...</summary>

* [v0.9.0](https://github.com/jedie/dev-shell/compare/v0.8.0...v0.9.0)
  * 2025-03-11 - fix publish
  * 2025-03-11 - Replace `poetry` with `uv`
* [v0.8.0](https://github.com/jedie/dev-shell/compare/v0.7.0...v0.8.0)
  * 2024-04-09 - Bump version to v0.8.0
  * 2024-04-09 - Remove "gnureadline" as dependency and update boot script
  * 2024-04-09 - Remove "gnureadline" as dependency
  * 2023-07-09 - Update requirements
* [v0.7.0](https://github.com/jedie/dev-shell/compare/v0.6.1...v0.7.0)
  * 2023-04-25 - Bugfix RedirectStdOutErr
  * 2023-04-25 - Update test matrix
  * 2023-04-25 - Update requirements
  * 2022-09-19 - skip linting (we use darker)
  * 2022-09-19 - CI: cache packages
* [v0.6.1](https://github.com/jedie/dev-shell/compare/v0.6.0...v0.6.1)
  * 2022-09-02 - Update README.md
  * 2022-09-02 - v0.6.1 - update tests adn README
  * 2022-09-02 - remove "pytest-flake8" and "pytest-isort"
  * 2022-09-02 - update requirements
  * 2022-09-02 - Call "poetry update" with "-v"
  * 2022-09-02 - skip Poetry v1.2.0
  * 2022-09-02 - Set default timeout to 5Min.
* [v0.6.0](https://github.com/jedie/dev-shell/compare/v0.5.0...v0.6.0)
  * 2022-07-19 - updates
  * 2022-07-19 - dd "pyupgrade" as shell command
  * 2022-07-19 - Update README.md
  * 2022-07-19 - Update requirements
* [v0.5.0](https://github.com/jedie/dev-shell/compare/v0.4.0...v0.5.0)
  * 2022-05-29 - update flake8 config
  * 2022-05-29 - simplify isort config
  * 2022-05-29 - fix isort checks
  * 2022-05-29 - v0.5.0.rc1
  * 2022-05-29 - update tox settings
  * 2022-05-29 - line_length = 100
  * 2022-05-29 - call github tests via tox
  * 2022-05-29 - Add "tox" and "poetry" commands
  * 2022-05-29 - Test also with Python 3.10
  * 2022-05-29 - Update requirements
* [v0.4.0](https://github.com/jedie/dev-shell/compare/v0.3.0...v0.4.0)
  * 2022-02-28 - Release v0.4.0
  * 2022-02-28 - Update requirements
* [v0.3.0](https://github.com/jedie/dev-shell/compare/v0.2.4...v0.3.0)
  * 2022-01-30 - Remove "flynt" form linting/fix code style
* [v0.2.4](https://github.com/jedie/dev-shell/compare/v0.2.3...v0.2.4)
  * 2022-01-22 - Switch to darker and use pytest-darker
  * 2022-01-22 - update requirements
* [v0.2.3](https://github.com/jedie/dev-shell/compare/v0.2.2...v0.2.3)
  * 2021-11-15 - Fix #29 - Flynt args can be change via CommandSet
  * 2021-11-15 - update requirements
  * 2021-11-15 - Update test.yml
* [v0.2.2](https://github.com/jedie/dev-shell/compare/v0.2.1...v0.2.2)
  * 2021-04-12 - include source "bootstrap" file
* [v0.2.1](https://github.com/jedie/dev-shell/compare/v0.2.0...v0.2.1)
  * 2021-04-12 - Handle if "poetry-publish" is not installed
* [v0.2.0](https://github.com/jedie/dev-shell/compare/v0.1.0...v0.2.0)
  * 2021-04-11 - Fix flake8 call: Remove arguments and add .flake8 config file
  * 2021-04-11 - Update dependencies + add "update" command
  * 2021-04-11 - Release 0.2.0rc1
  * 2021-04-11 - Fix #24 test under windows
  * 2021-04-10 - The DocTest will not work on Windows. Replace it with a normal test ;)
  * 2021-04-10 - Bugfix error on Windows:   File "C:\Users\sysop\PycharmProjects\dev-shell\dev_shell\utils\subprocess_utils.py", line 125, in prepare_popenargs     command = shutil.which(command_path, path=bin_path)   File "C:\Users\sysop\AppData\Local\Programs\Python\Python39\lib\shutil.py", line 1441, in which     if any(cmd.lower().endswith(ext.lower()) for ext in pathext):   File "C:\Users\sysop\AppData\Local\Programs\Python\Python39\lib\shutil.py", line 1441, in <genexpr>     if any(cmd.lower().endswith(ext.lower()) for ext in pathext): AttributeError: 'WindowsPath' object has no attribute 'lower' EXCEPTION of type 'AttributeError' occurred with message: ''WindowsPath' object has no attribute 'lower''
  * 2021-04-10 - Replace "SubprocessMock" with a simple function
  * 2021-04-10 - Bugfix calls outside the project directory...
  * 2021-04-10 - Do linting via tests
  * 2021-04-10 - Update also "setuptools", too.
  * 2021-04-05 - fix tests
  * 2021-04-05 - code style
  * 2021-04-05 - recognize "--update" and "--help" calls better
  * 2021-04-05 - remove "max-parallel"
  * 2021-03-26 - Rename: "dev-shell.py => devshell.py" and add tests for it
  * 2021-03-26 - Auto update .venv if poetry.lock changed
  * 2021-03-22 - Update README.md
  * 2021-03-22 - Remove "path" argument from flynt and autopep8
* [v0.1.0](https://github.com/jedie/dev-shell/compare/v0.0.2...v0.1.0)
  * 2021-03-22 - release v0.1.0
  * 2021-03-22 - Better "run as CLI" implementation
  * 2021-03-22 - Update README.md
  * 2021-03-19 - Bugfix handle of sys.exit() and return code (Imporant for CI usage)
  * 2021-03-22 - Update test.yml
  * 2021-03-20 - +!.github
  * 2021-03-20 - Update dev-shell.py
  * 2021-03-20 - add gitignore
  * 2021-03-19 - Bugfix subprocess call: Don't feed shutil.which() with Path() instance
* [v0.0.2](https://github.com/jedie/dev-shell/compare/v0.0.1...v0.0.2)
  * 2021-03-19 - refactor colorful
* [v0.0.1](https://github.com/jedie/dev-shell/compare/ad5dca7...v0.0.1)
  * 2021-03-19 - activate codecov.io
  * 2021-03-19 - Run linters on github actions
  * 2021-03-19 - Bugfix linting
  * 2021-03-19 - bump to version v0.0.1
  * 2021-03-19 - refactor and add linting and "fix_code_style" commands
  * 2021-03-19 - fix code style
  * 2021-03-19 - subprocess utils: Search for command in PATH
  * 2021-03-19 - update requirements
  * 2021-03-19 - Create a generic CmdAppBaseTestCase
  * 2021-03-19 - code cleanup
  * 2021-03-19 - Update README.md
  * 2021-03-19 - Bugfix Python 3.7 subprocess calls with Path() instances
  * 2021-03-19 - Bugfixes for windows
  * 2021-03-19 - Test on macos, too - TODO: Add windows support
  * 2021-03-19 - Update README
  * 2021-03-18 - add readme
  * 2021-03-18 - bugfix github action
  * 2021-03-18 - Activate github actions
  * 2021-03-18 - make it alive
  * 2021-03-18 - init
  * 2021-03-18 - Initial commit

</details>


[comment]: <> (✂✂✂ auto generated history end ✂✂✂)

## Project links

* Github: https://github.com/jedie/dev-shell/
* PyPi: https://pypi.org/project/dev-shell/
