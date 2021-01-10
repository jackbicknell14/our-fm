from flask_restplus import Resource
from flask import current_app as app, request

from ourfm.use_cases import spotify, users

logger = app.logger


class UserTrackCurrent(Resource):

    def post(self):
        """create a playlist for user"""
        user_id = request.form['user_id']
        track = spotify.get_current_playing_track(user_id=user_id)
        return track.name


class UserFriend(Resource):

    def post(self):
        """create a playlist for user"""
        user_id = request.form['user_id']
        friend_id = request.form['friend_id']
        friendship = users.add_friend(user_id=user_id, friend_id=friend_id)
        return str(friendship.from_user_id) + ' ' + str(friendship.to_user_id)
