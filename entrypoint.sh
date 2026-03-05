#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- Préparation des fichiers statiques ---"
python manage.py collectstatic --no-input

echo "--- Application des migrations ---"
python manage.py migrate

echo "--- Injection des données fictives ---"
python manage.py seed_data

echo "--- Démarrage du serveur Gunicorn ---"
exec gunicorn autoklik.wsgi:application --bind 0.0.0.0:8000
