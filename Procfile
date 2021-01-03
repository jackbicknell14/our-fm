release: flask db upgrade
web: gunicorn "ourfm:create_app()"
worker: celery -A ourfm.interfaces.tasks.celery_worker.celery worker -B --loglevel=INFO
