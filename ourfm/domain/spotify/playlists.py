import datetime

from . import auth, artists, tracks
from ourfm import errors
from ourfm.data import models as md

SPOTIFY_TIMES = {
    'month': 'short_term',
    'halfyear': 'medium_term',
    'year': 'long_term'
}


def rename(user_id, playlist_id, new_name):
    user = md.User.get(id=user_id)
    sp = auth.login(user)
    sp_user = sp.current_user()
    playlist = md.Playlist.get(id=playlist_id)
    sp.user_playlist(user, playlist.spotify_id)
    sp.user_playlist_change_details(sp_user, playlist.spotify_id, name=new_name)
    playlist.update(name=new_name)
    return playlist


def create(user, duration='month'):
    month = (datetime.date.today() - datetime.timedelta(3)).strftime("%B %Y")
    playlist_name = f'YourFM: {month}'
    sp = auth.login(user)
    sp_user = sp.current_user()

    if md.Playlist.exists(name=playlist_name, user_id=user.id):
        return md.Playlist.get(name=playlist_name, user_id=user.id)

    # get top tracks
    top_tracks = sp.current_user_top_tracks(time_range=SPOTIFY_TIMES[duration], limit=5)['items']

    # save artists and tracks
    playlist_tracks = []
    for track in top_tracks:
        track = track
        track_artists = artists.save('track', track)
        playlist_tracks.append(tracks.save(track, track_artists))

    # create and save playlist
    sp_playlist = sp.user_playlist_create(sp_user['id'], playlist_name)
    sp.user_playlist_add_tracks(sp_user['id'], sp_playlist['id'], [t['id'] for t in top_tracks])
    sp_playlist = sp.user_playlist(sp_user, sp_playlist['id'])
    sp_tracks = sp.user_playlist_tracks(user, playlist_id=sp_playlist['id'])

    if sp_tracks['next'] is not None:
        return ValueError('Next to fix pagination for this playlist')

    playlist = md.Playlist.create(name=playlist_name,
                                  user_id=user.id,
                                  spotify_id=sp_playlist['id'],
                                  track_total=len(sp_tracks['items']),
                                  details=sp_playlist,
                                  tracks=playlist_tracks)

    return playlist


def get(playlist_id):
    return md.Playlist.get(id=playlist_id)
