from ourfm.data import models as md


def save(track, artists):
    if md.Track.exists(spotify_id=track['id']):
        return md.Track.get(spotify_id=track['id'])

    return md.Track.save(spotify_id=track['id'],
                         name=track['name'],
                         details=str(track),
                         artists=artists)
