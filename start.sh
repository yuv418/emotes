
gunicorn --bind 0.0.0.0:5000 emotes.wsgi:app &
celery -A emotes.wsgi.celery -c 1 worker

fg %1
