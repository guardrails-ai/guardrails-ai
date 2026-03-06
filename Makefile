.PHONY: install build

install:
	pip install -r dev-requirements.txt;
	pre-commit install