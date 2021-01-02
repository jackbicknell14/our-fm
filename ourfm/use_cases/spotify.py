import datetime

from ourfm.data import models as md
from ourfm.domain import spotify


def create_playlists():
    users = md.User.all()
    for user in users:
        spotify.playlists.create(user=user, duration='month')


