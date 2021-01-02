import spotipy

from ourfm.domain.auth import token


def login(user):
    access_token = token.get_new_access_token(refresh_token=user.refresh_token)
    sp = spotipy.Spotify(auth=access_token)
    return sp
