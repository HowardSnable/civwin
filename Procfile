release: python manage.py migrate
release: python manage.py readBaseData
release: python manage.py readMatches
web: gunicorn aoematchups.wsgi --log-file -