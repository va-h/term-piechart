PACKAGE = term_piechart

.PHONY: lint
lint:
	$(info Running Python linters)
	ruff check --exit-zero $(PACKAGE) tests
	pylint $(PACKAGE)

.PHONY: format
format:
	$(info Formatting Python code)
	ruff check --select I --fix $(PACKAGE) tests
	ruff format $(PACKAGE) tests

.PHONY: init
init:
	python -m pip install --upgrade pip
	python -m pip install --upgrade -r requirements/dev.txt
	python -m pip check

.PHONY: update
update:
	$(info Running uv -U)
	python -m pip install --upgrade pip uv
	uv pip compile --extra dev -o requirements/dev.txt pyproject.toml

.PHONY: test
test:
	$(info Running tests)
	python -m pytest

.PHONY: upgrade
upgrade: update init
