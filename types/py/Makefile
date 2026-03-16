.PHONY: install install-dev lint lint-fix type qa test test-cov test-cov-ci docs docs-html docs-md docs-clean view-docs
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
	python -m unittest discover -s tests -t . --buffer --failfast

test-cov:
	coverage run -m unittest discover --start-directory tests --top-level-directory . --buffer --failfast
	coverage report -m

test-cov-ci:
	coverage run -m unittest discover --start-directory tests --top-level-directory . --buffer --failfast

view-test-cov:
	coverage run -m unittest discover --start-directory tests --top-level-directory . --buffer --failfast
	coverage html
	open htmlcov/index.html

# Install docs dependencies
install-docs:
	pip install -e ".[docs]"

# Build HTML and Markdown docs
docs:
	make docs-html
	make docs-md

# Build HTML docs
docs-html:
	sphinx-build -b html docs docs/_build/html

# Build Markdown docs
docs-md:
	sphinx-build -b markdown docs/ docs/_build/markdown/

# Remove generated docs
docs-clean:
	rm -rf docs/_build docs/autoapi

view-docs:
	open docs/_build/html/index.html