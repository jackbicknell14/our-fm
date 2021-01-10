from . import artists

from ourfm.data import models as md


def save(track):
    if md.Track.exists(spotify_id=track['id']):
        return md.Track.get(spotify_id=track['id'])

    track_artists = artists.save(method='track', data=track)
    return md.Track.save(spotify_id=track['id'],
                         name=track['name'],
                         details=str(track),
                         artists=track_artists)
