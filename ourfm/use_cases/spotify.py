import datetime

from ourfm.data import models as md
from ourfm.domain import spotify


def create_playlists():
    users = md.User.all()
    playlists = [spotify.playlists.create(user=user, duration='month') for user in users]
    return playlists


def get_playlist(playlist_id):
    return spotify.playlists.get(playlist_id)



