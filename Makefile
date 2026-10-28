.PHONY: install serve build test clean

install:
	pip install -r requirements.txt pytest

serve:
	mkdocs serve

build:
	mkdocs build --strict

test:
	pytest -q code/python/tests

clean:
	rm -rf site .cache
