from flask_restplus import Resource
from flask import current_app as app, request

from ourfm.use_cases import spotify
logger = app.logger


class UserTrackCurrent(Resource):

    def post(self):
        """create a playlist for user"""
        user_id = request.form['user_id']
        track = spotify.get_current_playing_track(user_id=user_id)
        return track.name
