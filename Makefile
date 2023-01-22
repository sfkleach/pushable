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
.DEFAULT_GOAL:=all

# Delete targets if their recipe exits with a non-zero exit code.
.DELETE_ON_ERROR:


################################################################################
### Main Contents
################################################################################

.PHONY: help
help:
	# Valid targets are:
	#	publish-to-main - publishes to the PyPi archive.
	#   publish-to-test - publishes to the Pypi Test archive.

# These commands should be run locally before continuing
# 	poetry config repositories.pypi https://pypi.org/legacy/
# 	poetry config pypi-token.pypi <your-token>
# 	poetry config repositories.test-pypi https://test.pypi.org/legacy/
# 	poetry config pypi-token.test-pypi <your-token>

.PHONY: publish-to-main
publish-to-main:
	poetry publish -r pypi --dry-run --build


.PHONY: publish-to-test
publish-to-test: 
	if [ -e tests/pushable.py ]; then echo RETEST_WITHOUT_LINK; exit 1; fi
	poetry publish -r test-pypi --dry-run --build

# Post-installation tests
.PHONY: test
test:
	poetry run pytest tests

