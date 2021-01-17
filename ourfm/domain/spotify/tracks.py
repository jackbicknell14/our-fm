from . import artists

from ourfm.data import models as md


def save_track(track):
    if md.Track.exists(spotify_id=track['id']):
        return md.Track.get(spotify_id=track['id'])

    track_artists = artists.save(method='track', data=track)
    return md.Track(spotify_id=track['id'],
                    name=track['name'],
                    details=str(track),
                    artists=track_artists).save()


def save_all(tracks_to_save):
    return [save_track(track) for track in tracks_to_save]
