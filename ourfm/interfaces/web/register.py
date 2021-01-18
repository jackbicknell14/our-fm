import flask
from flask import render_template, request, redirect, url_for
from ourfm.use_cases import users


register_blueprint = flask.Blueprint('register_blueprint', __name__, template_folder='templates')


@register_blueprint.route('/', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        return redirect(url_for('api.auth'))




