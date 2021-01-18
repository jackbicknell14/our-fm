from celery import Celery
import config
import os
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from flask import Flask
from ourfm.data import db, migrate


celery = Celery(__name__, broker=config.AppConfig.CELERY_BROKER_URL)


def create_app(environment=None):
    if environment is None:
        environment = os.getenv('FLASK_ENV', 'production')
    # Step 2: App creation
    app = Flask(__name__, static_folder='assets')
    app.config.from_object(config.AppConfig)

    # Step 3: Plugin Initialization
    db.init_app(app)
    migrate.init_app(app)

    with app.app_context():
        # Logging
        handler = logging.StreamHandler()
        logging_format = ("%(asctime)s - %(name)s - level=%(levelname)s - "
                          "%(message)s")
        handler.setFormatter(logging.Formatter(logging_format))
        logging.getLogger().addHandler(handler)

        sentry_sdk.init(environment=app.config['SENTRY_ENV'],
                        integrations=[FlaskIntegration(), SqlalchemyIntegration()])
        app.logger.setLevel(logging.INFO)

        # Blueprints
        from ourfm.data import models
        from ourfm.interfaces.api import v0
        from ourfm.interfaces.web import register, user
        app.register_blueprint(register.register_blueprint)
        app.register_blueprint(v0.api_blueprint)
        app.register_blueprint(user.user_blueprint)

    return app

