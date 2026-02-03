#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Run migrations (This creates/updates your db.sqlite3 file)
python manage.py collectstatic --no-input
python manage.py migrate
