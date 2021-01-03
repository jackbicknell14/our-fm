import datetime

from . import auth
from ourfm.data import models as md

SPOTIFY_TIMES = {
    'month': 'short_term',
    'halfyear': 'medium_term',
    'year': 'long_term'
}


def create(user, duration='month'):
    playlist_name = f'YourFM: {datetime.date.today().strftime("%B %Y")}'
    sp = auth.login(user)
    sp_user = sp.current_user()
    playlist = md.Playlist.get_or_create(name=playlist_name, user_id=user.id)
    if playlist.details is not None:
        return
    top_tracks = sp.current_user_top_tracks(time_range=SPOTIFY_TIMES[duration], limit=50)['items']
    track_ids = [i['id'] for i in top_tracks]
    sp_playlist = sp.user_playlist_create(sp_user['id'], playlist_name)
    sp.user_playlist_add_tracks(sp_user['id'], sp_playlist['id'], track_ids)
    sp_playlist = sp.user_playlist(sp_user, sp_playlist['id'])
    sp_tracks = sp.user_playlist_tracks(user, playlist_id=sp_playlist['id'])
    if sp_tracks['next'] is not None:
        return ValueError('Next to fix pagination for this playlist')
    playlist_tracks = sp_tracks.pop('items')
    playlist_uuid = md.Playlist().b64_to_hex(sp_playlist['id'])
    playlist.update(id=playlist_uuid,
                    track_total=len(playlist_tracks),
                    details=sp_playlist).save()
    for playlist_track in playlist_tracks:
        artists = []
        for playlist_artist in playlist_track['track']['artists']:
            artist_id = md.Artist.b64_to_hex(playlist_artist['id'])
            artist = md.Artist.get_or_create(id=artist_id,
                                             name=playlist_artist['name'],
                                             genres=playlist_artist.get('genres'),
                                             href=playlist_artist['href'],
                                             popularity=playlist_artist.get('popularity'),
                                             uri=playlist_artist['uri'],
                                             external_urls=str(playlist_artist['external_urls']))
            artists.append(artist)

        track_id = md.Track.b64_to_hex(playlist_track['track']['id'])
        track = md.Track.get_or_create(id=track_id, name=playlist_track['track']['name'])
        if track.details is None:
            track.update(artists=artists, details=str(playlist_track))
        md.PlaylistTrack.get_or_create(track_id=track.id, playlist_id=playlist_uuid,
                                       added_by=playlist_track['added_by']['href'])

    return playlist


def get(playlist_id):
    return md.Playlist.get(id=playlist_id)
