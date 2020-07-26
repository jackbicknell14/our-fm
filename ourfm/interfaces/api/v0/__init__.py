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

legacy_api = restplus_api.namespace('', description='Legacy operations')
resources.add(legacy_api, Ok, '/check/ok', endpoint='ok')
