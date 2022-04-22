#!/bin/sh
echo DB MIGRATION START
poetry run flask db upgrade
echo DB MIGRATION FINISHED
echo START SERVER
poetry run gunicorn --bind 0.0.0.0:5000 -w 3 wsgi:app
