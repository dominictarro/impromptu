# lint code
.PHONY: lint
lint:
	pipenv run python -m pylint --version
	pipenv run python -m pylint distillery
# run unit tests
.PHONY: unittest
unittest:
	pipenv run python -m unittest discover -p "test_*.py" -s "tests" -v
