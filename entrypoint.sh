#!/bin/bash

echo "Apply database migrations here"
pwd
ls -la
poetry run python manage.py makemigrations
poetry run python manage.py migrate

# Start server
echo "Starting server"
# poetry run python manage.py runserver 0.0.0.0:8000