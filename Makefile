install:
	poetry install

lint:
	poetry run flake8 poll_api tests

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=poll_api --cov-report xml
