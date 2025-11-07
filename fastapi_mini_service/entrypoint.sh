#!/bin/sh

[ -d ./allstaticfiles/static ] || mkdir -p ./allstaticfiles/static
[ -d ./media ] || mkdir -p ./media

python manage.py makemigrations --noinput --merge
python manage.py migrate
python manage.py collectstatic --no-input

python manage.py createsuperuser --no-input

exec "$@"
