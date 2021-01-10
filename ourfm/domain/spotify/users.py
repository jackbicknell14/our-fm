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
    return sp.current_playback()


def save_current_track(track, user_id):
    track_data = md.Track.get(spotify_id=track['item']['id'])
    md.UserTrack(
        user_id=user_id,
        track_id=track_data.id,
        device=str(track['device']),
        shuffle_state=track['shuffle_state'],
        repeat_state=track['repeat_state'],
        timestamp=track['timestamp'],
        context=str(track['context']),
        progress_ms=track['progress_ms'],
        item=str(track['item']),
        currently_playing_type=track['currently_playing_type'],
        actions=str(track['actions']),
        is_playing=track['is_playing']).save()
    return track_data
