release: python manage.py migrate 
python manage.py readBaseData 
python manage.py readMatches
web: gunicorn aoematchups.wsgi --log-file -