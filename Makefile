.PHONY: setup lint test build

setup:
\tpython -m venv .venv && . .venv/bin/activate && pip install -U pip
\t. .venv/bin/activate && pip install -e .[dev]
\tpre-commit install

lint:
\truff check --fix
\tblack src tests

test:
\tpytest -q

build:
\tpython -m build