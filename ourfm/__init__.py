import config
import logging

from flask import Flask
from ourfm.data import db, migrate


def create_app(environment=None):

    environment = 'development'
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
        app.logger.setLevel(logging.INFO)

        # Blueprints
        from ourfm.data import models
        from ourfm.interfaces.api import v0
        from ourfm.interfaces.web import register, user
        app.register_blueprint(v0.api_blueprint)
        app.register_blueprint(register.register_blueprint)
        app.register_blueprint(user.user_blueprint)

    return app

