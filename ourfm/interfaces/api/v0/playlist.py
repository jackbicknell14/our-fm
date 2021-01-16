from flask_restplus import Resource
from flask import current_app as app, request

from ourfm.use_cases import spotify
logger = app.logger


class Playlist(Resource):

    def get(self):
        """Get playlist by id"""
        playlist = spotify.get_playlist(playlist_id=request.args['playlist_id'])
        return playlist.name

    def post(self):
        """create a playlist for user"""
        user_id = request.form['user_id']
        playlist = spotify.create_user_month_playlist(user_id=user_id)
        return playlist.name


class PlaylistMonthAll(Resource):

    def post(self):
        """Create monthly playlists"""
        playlist = spotify.create_playlists()
        return playlist
