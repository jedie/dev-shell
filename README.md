# A "dev-shell" for Python projects ;)

[![pytest](https://github.com/jedie/dev-shell/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/jedie/dev-shell/actions?query=branch%3Amain)
[![codecov](https://codecov.io/gh/jedie/dev-shell/branch/main/graph/badge.svg)](https://codecov.io/gh/jedie/dev-shell)

This small project is intended to improve the start-up for collaborators.

The idea is to make the project setup as simple as possible. Just clone the sources and start a script and you're done ;)

Run Tests? Just start the script and call the "run test command".

The "dev-shell" is the base to create a CLI and a shell. It also

It also shows how to make a project bootstrap as simply as possible, e.g.:

```bash
~$ git clone https://github.com/jedie/dev-shell.git
~$ cd dev-shell
~/dev-shell$ ./dev-shell.py pytest
```


## How it works

First start of the Python script [./dev-shell.py](https://github.com/jedie/dev-shell/blob/main/dev-shell.py) will bootstrap:

* Generate a Python virtual environment (in short: `venv`)
* Install poetry
* Install project dependencies and the project himself

The output on first bootstrap start looks like:

```bash
~/dev-shell$ ./dev-shell.py
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


Developer shell - dev_shell - v0.0.1alpha0


Documented commands (use 'help -v' for verbose/'help <topic>' for details):

Publish
=======
publish

Tests
=====
pytest

...

(dev_shell) quit
~/dev-shell$
```

The first bootstrap start takes a few seconds. Each later startup detects the existing virtualenv and is very fast:

```bash
~/dev-shell$ ./dev-shell.py

Developer shell - dev_shell - v0.0.1alpha0

(dev_shell)
~/dev-shell$ ./dev-shell.py --update
```


To update existing virtualenv, call with `--update`:

```bash
~/dev-shell$ ./dev-shell.py --update
```

Or just delete `/.venv/` and start `dev-shell.py` ;)

## compatibility

| dev-shell version | OS                      | Python version |
|-------------------|-------------------------|----------------|
| v0.0.1            | Linux + MacOS + Windows | 3.9, 3.8, 3.7  |

See also github test configuration: [.github/workflows/test.yml](https://github.com/jedie/dev-shell/blob/main/.github/workflows/test.yml)

## History

* [*dev*](https://github.com/jedie/dev-shell/compare/v0.0.1...master)
  * TBC
* [v0.0.1 - 2021-03-19](https://github.com/jedie/poetry-publish/compare/ad5dca...v0.0.1)
  * first "useable" version

## Project links

* Github: https://github.com/jedie/dev-shell/
* PyPi: https://pypi.org/project/dev-shell/
