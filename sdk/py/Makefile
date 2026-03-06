.PHONY: install install-dev lint lint-fix type qa test test-cov test-cov-ci
# Installs production dependencies
install:
	pip install .;

# Installs development dependencies
install-dev:
	pip install -e ".[dev]";
	pre-commit install

lint:
	ruff check .
	ruff format .

lint-fix:
	ruff check . --fix
	ruff format .

type:
	pyright

qa:
	make install-dev
	make lint
	make type
	make test-cov-ci

test:
	python -m unittest discover -s tests --buffer --failfast

test-cov:
	coverage run -m unittest discover --start-directory tests --buffer --failfast
	coverage report -m

test-cov-ci:
	coverage run -m unittest discover --start-directory tests --buffer --failfast