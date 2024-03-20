all: run-app run-tests migrate-db lint-py lint-md
.PHONY: all

run-app:
	source .env && python manage.py run --port=5001
run-tests:
	source .env && python manage.py test
migrate-db:
	flask db stamp head && flask db migrate && flask db upgrade
lint-py:
	flake8 src/ tests/
lint-md:
	markdownlint-cli2 '**/*.md'
