from flask_restplus import Resource
from ourfm.use_cases import spotify


class Tracks(Resource):

    def get(self):
        """Create monthly playlists"""
        spotify.get_current_playing_tracks()
