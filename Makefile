run-app:
	source .env && python manage.py run --port=5001
lint-py:
	flake8 src/
lint-md:
	markdownlint-cli2 '**/*.md'
.PHONY: lint-md
