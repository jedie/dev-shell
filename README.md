# A "dev-shell" for Python projects ;)

[![Test](https://github.com/jedie/dev-shell/actions/workflows/test.yml/badge.svg?branch=bugfix-path)](https://github.com/jedie/dev-shell/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/jedie/dev-shell/branch/main/graph/badge.svg)](https://codecov.io/gh/jedie/dev-shell)

[![ddev-shell @ PyPi](https://img.shields.io/pypi/v/dev-shell?label=dev-shell%20%40%20PyPi)
![Python Versions](https://img.shields.io/pypi/pyversions/dev-shell)
![License GPL V3+](https://img.shields.io/pypi/l/dev-shell)](https://pypi.org/project/dev-shell/)

This small project is intended to improve the start-up for collaborators.

The idea is to make the project setup as simple as possible. Just clone the sources and start a script and you're done ;)

Why in hell not just a `Makefile`? Because it doesn't out-of-the-box under Windows and MacOS, the dev-shell does ;)

Run Tests? Just start the script and call the "run test command".

The "dev-shell" is the base to create a CLI and a shell. It also shows how to make a project bootstrap as simply as possible, e.g.:

```bash
~$ git clone https://github.com/jedie/dev-shell.git
~$ cd dev-shell
~/dev-shell$ ./devshell.py pytest
```


## How it works

First start of the Python script [./devshell.py](https://github.com/jedie/dev-shell/blob/main/devshell.py) will bootstrap:

* Generate a Python virtual environment (in short: `venv`)
* Install poetry
* Install project dependencies and the project himself

The output on first bootstrap start looks like:

```bash
~/dev-shell$ ./devshell.py
Create venv here: ~/dev-shell/.venv
Collecting pip
...
Successfully installed pip-21.0.1
Collecting poetry
...
Installing dependencies from lock file

Package operations: 31 installs, 1 update, 0 removals

...

Installing the current project: dev-shell (0.0.1alpha0)


+ .venv/bin/python .venv/bin/devshell


Developer shell - dev_shell - v0.2.0


Documented commands (use 'help -v' for verbose/'help <topic>' for details):

dev-shell commands
==================
fix_code_style  linting  list_venv_packages  publish  pytest  update

...

(dev_shell) quit
~/dev-shell$
```

The first bootstrap start takes a few seconds. Each later startup detects the existing virtualenv and is very fast:

```bash
~/dev-shell$ ./devshell.py

Developer shell - dev_shell - v0.2.0

(dev_shell) help
```

Info: The `.venv` will be automatically updated via `poetry install` call if the `poetry.lock` file has been changed.

A call with `--update` will force to call some create/update steps, e.g.:

```bash
~/dev-shell$ ./devshell.py --update
```

You can also just delete `/.venv/` and start `devshell.py` again ;)

(Using `--update` is not to be confused with the call of "update" command.)


## compatibility

| dev-shell version | OS                      | Python version      |
|-------------------|-------------------------|---------------------|
| >=v0.7.0          | Linux + MacOS + Windows | 3.11, 3.10, 3.9     |
| >=v0.5.0          | Linux + MacOS + Windows | 3.10, 3.9, 3.8, 3.7 |
| >=v0.0.1          | Linux + MacOS + Windows | 3.9, 3.8, 3.7       |

See also github test configuration: [.github/workflows/test.yml](https://github.com/jedie/dev-shell/blob/main/.github/workflows/test.yml)

## History

* [*dev*](https://github.com/jedie/dev-shell/compare/v0.7.0...main)
  * TBC
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
