.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: clean-pyc ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with flake8
	pylint twindb_table_compare

vagrant-up:
	cd vagrant && vagrant up

vagrant-provision:
	cd vagrant && vagrant provision

.PHONY: bootstrap
bootstrap: ## bootstrap the development environment
	pip install -U "setuptools==32.3.1"
	pip install -U "pip==9.0.1"
	pip install -U "pip-tools>=1.6.0"
	pip-sync requirements.txt requirements_dev.txt
	pip install --editable .

.PHONY: rebuild-requirements
rebuild-requirements: ## Rebuild requirements files requirements.txt and requirements_dev.txt
	pip-compile --verbose --no-index --output-file requirements.txt requirements.in
	pip-compile --verbose --no-index --output-file requirements_dev.txt requirements_dev.in

.PHONY: upgrade-requirements
upgrade-requirements: ## Upgrade requirements
	pip-compile --upgrade --verbose --no-index --output-file requirements.txt requirements.in
	pip-compile --upgrade --verbose --no-index --output-file requirements_dev.txt requirements_dev.in

test:  ## run tests quickly with the default Python
	py.test -vx tests/unit/

test-functional:  ## run functional tests
	py.test -vx tests/functional/

test-all: ## run tests on every Python version with tox
	tox

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/twindb_table_compare.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ twindb_table_compare
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

coverage:
	py.test --cov=twindb_table_compare --cov-report term-missing tests/unit

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install
