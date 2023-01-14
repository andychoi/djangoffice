#!/bin/bash

read -p "Are you sure? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then

echo "-- deleting SQlite data"
rm djangoffice/db.sqlite3

if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "-- creating python .venv environment"
    python -m venv .venv && source .venv/bin/activate
    python -m pip install --upgrade pip wheel
    python -m pip install -r requirements.txt
fi

echo "-- migrating"
python manage.py migrate

echo "-- creating admin user and demo users"
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(username='admin', email='admin@example.com', password='demo')"
# python manage.py wflow_demo
p manage.py runserver

fi