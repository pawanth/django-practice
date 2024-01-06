#!/bin/bash

python manage.py migrate # Apply database migrations
python manage.py collectstatic --no-input # Gather static files
python manage.py runserver 0:8000 # Start the Django server