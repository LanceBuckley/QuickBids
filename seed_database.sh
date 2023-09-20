#!/bin/bash

rm db.sqlite3
rm -rf ./quickbidsapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations quickbidsapi
python3 manage.py migrate quickbidsapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata contractors
python3 manage.py loaddata jobs
python3 manage.py loaddata bids
python3 manage.py loaddata fields
python3 manage.py loaddata job_fields