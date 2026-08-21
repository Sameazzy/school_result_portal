#!/usr/bin/env bash
set -o errexit

#install django dependencies
pip install -r requirements.txt

#Collect static files
python manage.py collectstatic --no-input

#Run database migration
python manage.py migrate

#create admin
python manage.py create_admin