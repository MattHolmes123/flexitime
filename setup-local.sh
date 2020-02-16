#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

virtualenv -p python3.6 venv
  
. venv/bin/activate
  
pip install -r requirements.txt

python manage.py migrate

# TODO Ideally this would be a migration
# I ran into this problem before: https://stackoverflow.com/questions/31735042/adding-django-admin-permissions-in-a-migration-permission-matching-query-does-n
python manage.py create_flexitime_groups

python manage.py create_test_admin_user

python manage.py create_test_user_data
