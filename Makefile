run-app:
	source .env && python manage.py run --port=5001
run-tests:
	python manage.py test
migrate-db:
	flask db migrate && flask db upgrade
lint-py:
	flake8 src/ tests/
lint-md:
	markdownlint-cli2 '**/*.md'
.PHONY: lint-md
