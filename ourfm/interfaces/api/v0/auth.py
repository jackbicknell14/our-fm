from flask_restplus import Resource
from flask import current_app as app, redirect, request, url_for
from ourfm.use_cases import auth, spotify
logger = app.logger


class Authorise(Resource):

    def get(self):
        return redirect(auth.get_url())


class Callback(Resource):

    def get(self):
        authorization_code = request.args['code']
        user = auth.get_refresh_token(authorization_code=authorization_code)
        spotify.create_user_month_playlist(user=user, duration='month')
        return redirect(url_for('user_blueprint.profile'))
