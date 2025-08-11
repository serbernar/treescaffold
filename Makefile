.PHONY: setup lint test build

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip
	. .venv/bin/activate && pip install -e .[dev]
	pre-commit install

lint:
	ruff check --fix
	black src tests

test:
	pytest -q

build:
	python -m build
