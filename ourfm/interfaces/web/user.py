import flask
from flask import render_template, request, redirect, url_for
from ourfm.use_cases import users
from ourfm.data import models as md

from ..api import v0

user_blueprint = flask.Blueprint('user_blueprint', __name__, template_folder='templates')


@user_blueprint.route('/profile')
def profile():
    user = v0.User().get()
    return render_template('user.html', page='User', user=user)


@user_blueprint.route('/friends')
def friends():
    friends = v0.UserContact().get()
    return render_template('friends.html', page='Friends', friends=friends)


@user_blueprint.route('/groups')
def groups():
    groups = v0.UserGroup().get()
    return render_template('groups.html', page='Groups', groups=groups)


@user_blueprint.route('/playlists')
def playlists():
    playlists = v0.UserPlaylist().get()
    return render_template('playlists.html', page='Playlists', playlists=playlists)


@user_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')
