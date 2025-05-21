web: gunicorn proyectoDjango.wsgi
worker: celery -A proyectoDjango worker --loglevel=info
beat: celery -A proyectoDjango beat --loglevel=info