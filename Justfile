set dotenv-load

# Lists available commands
@default:
    just --list

# Builds the documentation
docs:
	cd docs && uv run make html

# Cleans the docs directory
clean:
	cd docs && uv run make clean

# ATM I do not intend for updates of the PyPI archive to be run automagically.
# So these commands should be run locally before trying to update the PyPI
# archives.
# 	export UV_PUBLISH_TOKEN=<your-pypi-token>
# 	export UV_PUBLISH_TOKEN=<your-test-pypi-token>  (for test-pypi)

# Publishes the package to PyPI
publish:
	uv build && uv publish

# Publishes the package to the test PyPI
publish-to-test:
	uv build && uv publish --publish-url https://test.pypi.org/legacy/


# Post-installation tests
test: type_check unit_test

# Type checks the code
type_check:
	uv run mypy --check-untyped-defs src/pushable/pushable.py
	MYPYPATH=src uv run mypy --check-untyped-defs tests/test_pushable.py

# ut = unit tests
#	If this fails because it cannot find the pushable package, check
#	that you have done a local uv sync.
# Runs unit tests
unit_test:
	uv run pytest tests
