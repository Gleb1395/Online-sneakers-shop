#!/bin/bash
python src/manage.py makemigrations
python src/manage.py migrate
python src/manage.py check
python src/manage.py collectstatic --noinput
gunicorn -w ${WSGI_WORKERS} -b 0:${WSGI_PORT} --chdir /src config.wsgi:applicarion --log-level=${WSGI_LOG_LEVEL}
python src/manage.py runserver 0:8010