from flask_restplus import Resource
from flask import current_app as app, request

from ourfm.use_cases import spotify
logger = app.logger


class Playlist(Resource):

    def get(self):
        """Get playlist by id"""
        playlist = spotify.get_playlist(playlist_id=request.args['playlist_id'])
        return playlist.name


class PlaylistMonthAll(Resource):

    def post(self):
        """Create monthly playlists"""
        playlist = spotify.create_playlists()
        return playlist
