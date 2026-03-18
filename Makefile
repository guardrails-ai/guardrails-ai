.PHONY: install build docs docs-clean view-docs

install:
	pip install -r dev-requirements.txt;
	pre-commit install

# Build HTML docs for all packages from the root docs directory
docs:
	sphinx-build -b html docs docs/_build

# Remove generated docs
docs-clean:
	rm -rf docs/_build docs/autoapi docs/_packages

view-docs:
	open docs/_build/index.html