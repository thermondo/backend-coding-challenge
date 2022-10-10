help:
	@echo "=========== Welcome to Thermondo App makefile Help ==========="
	@echo "=========== Example usages are as below. ==========="
	@echo "make up 		=> To start an environment (docker-compose up --build)"
	@echo "make tail 	=> Show docker-compose logs"
	@echo "make cli		=> SSH into app (app) server with django shell_plus"

up:
	@docker-compose up --build

down:
	@docker-compose down


start:
	@docker-compose start

stop:
	@docker-compose stop

status:
	@docker-compose ps

restart: stop start

clean: stop
	@docker-compose rm --force
	@find . -name \*.pyc -delete

test:
	@docker-compose run --rm app pytest

migrate:
	@docker-compose run --rm app python ./manage.py migrate

makemigrations:
	@docker-compose run --rm app python ./manage.py makemigrations

cli:
	@docker-compose run --rm app bash

shell_plus:
	@docker-compose run --rm app python manage.py shell_plus

tail:
	@docker-compose logs -f

.PHONY: start stop status restart clean test up down migrate cli tail