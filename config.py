import os


class AppConfig(object):
    # flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'SOME_SECRET_KEY')

    # database
    SQLALCHEMY_DATABASE_URI = os.getenv("OURFM_DB_URL")
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/ourfm"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask restplus
    ERROR_404_HELP = False
    RESTPLUS_MASK_SWAGGER = False

    # swagger
    SWAGGER_UI_DOC_EXPANSION = "list"
    SWAGGER_SUPPORTED_SUBMIT_METHODS = []  # disable 'Try it out' buttons

    # support
    SUPPORT_EMAIL = os.getenv("OURFM_SUPPORT_EMAIL")
