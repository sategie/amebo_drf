release: python manage.py makemigrations && python manage.py migrate

web: gunicorn amebo-drf.wsgi
