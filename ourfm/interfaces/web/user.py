import flask
from flask import render_template, request, redirect, url_for
from ourfm.use_cases import users
from ourfm.data import models as md
URL_PREFIX = '/user_old'

user_blueprint = flask.Blueprint('user_blueprint', __name__, url_prefix=URL_PREFIX, template_folder='templates')


@user_blueprint.route('/')
def profile():
    user = md.User.get(email='jackbicknell@live.co.uk')
    return render_template('user.html', page='User', user=user)




