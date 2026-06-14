#!/usr/bin/env bash

#python manage.py migrate --noinput
#python manage.py collectstatic --noinput
#python manage.py compilemessages
#
#python manage.py runserver 0.0.0.0:8000

uv run python manage.py migrate --noinput
uv run python manage.py collectstatic --noinput
uv run python manage.py compilemessages

uv run python manage.py runserver 0.0.0.0:8000