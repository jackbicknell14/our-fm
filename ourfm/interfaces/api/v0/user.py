from flask_restplus import Resource
from flask import current_app as app, request, render_template

from ourfm.data import models as md
from ourfm.use_cases import spotify, users

logger = app.logger


class User(Resource):

    def get(self):
        return users.get(user_id=request.args['user_id'])

    def post(self):
        return users.register(email=request.form['email'])


class UserTrackCurrent(Resource):

    def post(self):
        """create a playlist for user"""
        user_id = request.form['user_id']
        track = spotify.get_current_playing_track(user_id=user_id)
        return track.name


class UserContact(Resource):

    def get(self):
        return users.get_friends(user_id=request.args['user_id'])

    def post(self):
        """create a playlist for user"""
        user_id = request.form['user_id']
        friend_id = request.form['friend_id']
        friendship = users.add_friend(user_id=user_id, friend_id=friend_id)
        return str(friendship)


class UserGroup(Resource):

    def get(self):
        return users.get_groups(user_id=request.args['user_id'])


class UserPlaylist(Resource):

    def get(self):
        return users.get_playlists(user_id=request.args['user_id'])
