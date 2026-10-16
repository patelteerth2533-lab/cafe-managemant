#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files with WhiteNoise
python manage.py collectstatic --no-input

# Run migrations (applies 0004 data migration automatically)
python manage.py migrate

# Ensure seed data and admin exist
python seed_data.py
