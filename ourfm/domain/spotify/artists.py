from ourfm.data import models as md


def save(method, data):
    return {"playlist": save_from_playlist,
            "album": save_from_album,
            "track": save_from_track}[method](data)


def save_from_playlist(playlist):
    for playlist_track in playlist['items']:
        pass


def save_from_album(album):
    pass


def save_from_track(track):
    artists = []
    for track_artist in track['artists']:
        artist = md.Artist.get_or_create(spotify_id=track_artist['id'], name=track_artist['name'])
        if artist.uri is None:
            artist.update(name=track_artist['name'],
                          genres=track_artist.get('genres'),
                          href=track_artist['href'],
                          popularity=track_artist.get('popularity'),
                          uri=track_artist['uri'],
                          external_urls=str(track_artist['external_urls']))
        artists.append(artist)
    return artists
