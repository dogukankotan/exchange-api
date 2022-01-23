#!/bin/sh

python manage.py migrate --no-input
gunicorn base.wsgi --log-file - -w 4 -b 0.0.0.0:8000
