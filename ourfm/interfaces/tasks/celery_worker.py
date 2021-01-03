import datetime
import os
import logging
from celery.schedules import crontab
import requests
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
    sender.add_periodic_task(crontab(minute='0', hour='0', day_of_month='4'),
                             create_monthly_playlists.s(),
                             name='create-monthly-playlists')
    sender.add_periodic_task(crontab(minute='*'),
                             minute_ping.s(),
                             name='minute-ping')


@celery.task
def create_monthly_playlists():
    logging.info('Creating monthly playlists for all users.')
    playlists = spotify.create_playlists()
#    spotify.send_create_playlist_emails(playlists)


@celery.task
def minute_ping():
    requests.get('https://ourfm-production.herokuapp.com/check/ok')


