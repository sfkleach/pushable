################################################################################
### Standard Makefile intro
################################################################################

# Important check
MAKEFLAGS+=--warn-undefined-variables

# Causes the commands in a recipe to be issued in the same shell (beware cd commands not executed in a subshell!)
.ONESHELL:
SHELL:=/bin/bash

# When using ONESHELL, we want to exit on error (-e) and error if a command fails in a pipe (-o pipefail)
# When overriding .SHELLFLAGS one must always add a tailing `-c` as this is the default setting of Make.
.SHELLFLAGS:=-e -o pipefail -c

# Invoke the all target when no target is explicitly specified.
.DEFAULT_GOAL:=help

# Delete targets if their recipe exits with a non-zero exit code.
.DELETE_ON_ERROR:


################################################################################
### Main Contents
################################################################################

.PHONY: help
help:
	# Valid targets are:
	#	test 			- runs the unit tests
	#	docs			- builds Sphinx docs locally
	#	publish         - publishes to the PyPi archive.
	#   publish-to-test - publishes to the Pypi Test archive.

.PHONY: docs
docs:
	poetry run make -C docs html

# ATM I do not intend for updates of the PyPI archive to be run automagically.
# So these commands should be run locally before trying to update the PyPI
# archives.
# 	poetry config repositories.pypi https://pypi.org/legacy/
# 	poetry config pypi-token.pypi <your-token>
# 	poetry config repositories.test-pypi https://test.pypi.org/legacy/
# 	poetry config pypi-token.test-pypi <your-token>

.PHONY: publish
publish:
	poetry publish --build

.PHONY: publish-to-test
publish-to-test:
	poetry publish -r test-pypi --build


# Post-installation tests
.PHONY: test
test: tc ut

# tc = type check
.PHONY: tc
tc:
	poetry run mypy --check-untyped-defs src/pushable/pushable.py
	MYPYPATH=src poetry run mypy --check-untyped-defs tests/test_pushable.py

# ut = unit tests
.PHONY: ut
ut:
	poetry run pytest tests