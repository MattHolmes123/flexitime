#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

virtualenv -p python3.6 venv
  
. venv/bin/activate
  
pip install -r requirements.txt

python manage.py migrate 
