import datetime
import os
import logging
from celery.schedules import crontab
from ourfm import celery, create_app

app = create_app(os.getenv('FLASK_ENV'))
app.app_context().push()

from ourfm.use_cases import spotify

timezone = 'Europe/London'
celery.conf.update = {
    'timezone': timezone
}


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0,
                             create_monthly_playlists.s(),
                             name='create-monthly-playlists')


@celery.task
def create_monthly_playlists():
    logging.info('testing hello function')
    spotify.create_playlists()


