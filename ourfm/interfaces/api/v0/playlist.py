from flask_restplus import Resource
from flask import current_app as app

from ourfm.use_cases import spotify
logger = app.logger


class PlaylistMonthAll(Resource):

    def post(self):
        """Create monthly playlists"""
        spotify.create_playlists()
        return 200
