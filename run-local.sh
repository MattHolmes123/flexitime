#!/bin/bash

echo "Restarting nginx"
sudo systemctl restart nginx

echo "Activating venv"
source venv/bin/activate

echo "starting uwsgi"
uwsgi --ini local_deployment/flexitime_uwsgi.ini
