from flask import Blueprint, current_app
import flask_restplus

from ourfm.domain.api import Api, ResourceAdder

VERSION = '0.0'
APP_VERSION_HEADER = current_app.config.get('VERSION_HEADER')


# Create api
api_blueprint = Blueprint('api', __name__)

swagger_url = '/documentation/'
restplus_api = flask_restplus.Api(
    app=api_blueprint,
    version=VERSION,
    title="OurFM REST APIs",
    doc=False
)


@api_blueprint.route(swagger_url)
def swagger_docs():
    return flask_restplus.apidoc.ui_for(restplus_api)


resources = ResourceAdder(restplus_api)
api = Api(restplus_api)


from .check import Ok
from .auth import Authorise, Callback
from .groups import Group, GroupUser, GroupPlaylist
from .playlist import PlaylistMonthAll, Playlist
from .track import Tracks
from .user import UserTrackCurrent, UserFriend, User, UserGroup, UserPlaylist

base_api = restplus_api.namespace('', description='Legacy operations')
resources.add(base_api, Ok, '/check/ok', endpoint='ok')
resources.add(base_api, Authorise, '/auth', endpoint='auth')
resources.add(base_api, Callback, '/auth/callback', endpoint='auth-callback')
resources.add(base_api, PlaylistMonthAll, '/playlists/month/all', endpoint='create-all-monthly-playlists')
resources.add(base_api, Playlist, '/playlist', endpoint='get-single-playlist')
resources.add(base_api, UserTrackCurrent, '/user/current', endpoint='save-current-user-track')
resources.add(base_api, User, '/user', endpoint='user-data')
resources.add(base_api, UserFriend, '/user/friend', endpoint='user-friend')
resources.add(base_api, UserGroup, '/user/group', endpoint='user-groups')
resources.add(base_api, UserPlaylist, '/user/playlist', endpoint='user-playlist')
resources.add(base_api, Group, '/group', endpoint='group')
resources.add(base_api, GroupUser, '/group/user', endpoint='group-user')
resources.add(base_api, GroupPlaylist, '/group/playlist', endpoint='group-playlist')
resources.add(base_api, Tracks, '/tracks/all/now', endpoint='get-all-tracks-right-now')

