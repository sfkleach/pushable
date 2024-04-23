# Lists available commands
help:
    just --list

# Builds the documentation
docs:
	cd docs && poetry run make html

# Cleans the docs directory
clean:
	cd docs && poetry run make clean

# ATM I do not intend for updates of the PyPI archive to be run automagically.
# So these commands should be run locally before trying to update the PyPI
# archives.
# 	poetry config repositories.pypi https://pypi.org/legacy/
# 	poetry config pypi-token.pypi <your-token>
# 	poetry config repositories.test-pypi https://test.pypi.org/legacy/
# 	poetry config pypi-token.test-pypi <your-token>

# Publishes the package to PyPI
publish:
	poetry publish --build

# Publishes the package to the test PyPI
publish-to-test:
	poetry publish -r test-pypi --build


# Post-installation tests
test: type_check unit_test

# Type checks the code
type_check:
	poetry run mypy --check-untyped-defs src/pushable/pushable.py
	MYPYPATH=src poetry run mypy --check-untyped-defs tests/test_pushable.py

# ut = unit tests
#	If this fails because it cannot find the pushable package, check
#	that you have done a local poetry install.
# Runs unit tests
unit_test:
	poetry run pytest tests
