import flask
from flask import render_template, request, redirect, url_for
from ourfm.use_cases import users

URL_PREFIX = '/user'

user_blueprint = flask.Blueprint('user_blueprint', __name__, url_prefix=URL_PREFIX, template_folder='templates')


@user_blueprint.route('/')
def profile():
    return render_template('user.html')




