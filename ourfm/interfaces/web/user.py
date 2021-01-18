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


@user_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')
