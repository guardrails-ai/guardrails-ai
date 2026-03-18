.PHONY: install build docs docs-clean view-docs

install:
	pip install -r dev-requirements.txt;
	pre-commit install

# Build HTML docs for all packages from the root docs directory
docs:
	sphinx-build -b html docs-build docs

# Remove generated docs
docs-clean:
	rm -rf docs docs-build/_build docs-build/autoapi docs-build/_packages

view-docs:
	open docs/index.html