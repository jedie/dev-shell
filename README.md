# A "dev-shell" for Python projects ;)

[![pytest](https://github.com/jedie/dev-shell/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/jedie/dev-shell/actions?query=branch%3Amain)

tbd.

## Quickstart

First start of the Python script `./dev-shell.py` will bootstrap:

* Generate a virtualenv
* Install poetry
* Install dependencies and the project

e.g.:

Just clone the source and start the shell:

```bash
~$ git clone https://github.com/jedie/dev-shell.git
~$ cd dev-shell
~/dev-shell$ ./dev-shell.py
```

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


## Project links

* Github: https://github.com/jedie/dev-shell/
* PyPi: https://pypi.org/project/dev-shell/
