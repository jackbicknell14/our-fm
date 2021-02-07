import datetime

from . import auth, artists, tracks, users
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


def get_your_fm_name():
    month = (datetime.date.today() - datetime.timedelta(30)).strftime("%B %Y")
    playlist_name = f'OurFM: {month}'
    return playlist_name


def create(user_id, playlist_name, public=True, collaborative=False, description='OurFM playlist', group_id=None):
    # create and save playlist
    user = md.User.get(id=user_id)
    sp = auth.login(user)
    data = {"name": playlist_name, "public": public, "description": description, "collaborative": collaborative}
    sp_playlist = sp._post(f"users/{user.spotify_id}/playlists", payload=data)
    return md.Playlist.create(name=playlist_name,
                              user_id=user.id,
                              spotify_id=sp_playlist['id'],
                              track_total=0,
                              details=sp_playlist,
                              group_id=group_id)


def add_tracks(user_id, playlist_id, tracks_to_add):
    user = md.User.get(id=user_id)
    playlist = md.Playlist.get(id=playlist_id)

    owner = md.User.get(id=playlist.user_id)
    sp = auth.login(owner)

    # if track already exists in playlist then skip
    tracks_to_add = [track for track in tracks_to_add if
                     not md.PlaylistTrack.exists(playlist_id=playlist_id, track_id=track.id, added_by=user_id)]
    if not tracks_to_add:
        return playlist

    sp.user_playlist_add_tracks(user=owner.id,
                                playlist_id=playlist.spotify_id, tracks=[t.spotify_id for t in tracks_to_add])
    # get updated playlist tracks
    sp_tracks = sp.user_playlist_tracks(user=user.spotify_id, playlist_id=playlist.spotify_id)
    if sp_tracks['next'] is not None:
        return ValueError('Next to fix pagination for this playlist')

    # record tracks added in database
    for track in tracks_to_add:
        md.PlaylistTrack.get_or_create(track_id=track.id, playlist_id=playlist_id, added_by=user_id)

    sp_playlist = sp.user_playlist(user=user.spotify_id, playlist_id=playlist.spotify_id)
    playlist.update(track_total=len(sp_tracks['items']),
                    details=sp_playlist)

    return playlist


def replace_tracks(user_id, playlist_id, tracks_to_add):
    user = md.User.get(id=user_id)
    playlist = md.Playlist.get(id=playlist_id)

    owner = md.User.get(id=playlist.user_id)
    sp = auth.login(owner)
    # replace tracks to playlist
    sp.user_playlist_replace_tracks(user=owner.id,
                                    playlist_id=playlist.spotify_id,
                                    tracks=[i.spotify_id for i in tracks_to_add])

def get(playlist_id):
    return md.Playlist.get(id=playlist_id)
