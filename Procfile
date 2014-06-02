web: python manage.py runserver --settings=ciupy3.settings.dev 0.0.0.0:8000
worker: celery -B -A ciupy3 worker -l info -Q high,default
