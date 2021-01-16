from flask_restplus import Resource
from flask import current_app as app, request

from ourfm.use_cases import groups

logger = app.logger


class Group(Resource):

    def post(self):
        """create a playlist for user"""
        user_id = request.form['user_id']
        group_name = request.form['group_name']
        group = groups.create(user_id, group_name)
        return str(group.id)

    def get(self):
        """Returns a group"""
        return str(groups.get(request.form['group_id']).id)


class GroupUser(Resource):

    def post(self):
        """Adds a user to a group"""
        group_id = request.form['group_id']
        user_id = request.form['user_id']
        return groups.add_user(group_id=group_id, user_id=user_id)

    def get(self):
        """Returns all users for a group"""
        group_id = request.form['group_id']
        return str(groups.get_users(group_id=group_id))


class GroupPlaylist(Resource):

    def post(self):
        """Creates a playlist for a group"""
        group_id = request.form['group_id']
        return groups.create_playlist(group_id)
