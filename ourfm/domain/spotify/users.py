import spotipy

from . import auth
from ourfm.data import models as md
from ourfm.domain.users import operations


def save_new_user(access_token, refresh_token):
    sp = spotipy.Spotify(auth=access_token)
    user = sp.current_user()
    user = operations.save_new_user(email=user['email'],
                                    refresh_token=refresh_token,
                                    spotify_id=user['id'],
                                    data=user)
    return user


def get_current_track_for_user(user_id):
    user = md.User.get(id=user_id)
    sp = auth.login(user)
    track = sp.current_playback()
