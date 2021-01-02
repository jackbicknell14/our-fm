import os


class AppConfig:
    # Celery

    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'SOME_SECRET_KEY')

    # database
    SQLALCHEMY_DATABASE_URI = os.environ["OURFM_DB_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask restplus
    ERROR_404_HELP = False
    RESTPLUS_MASK_SWAGGER = False

    # swagger
    SWAGGER_UI_DOC_EXPANSION = "list"
    SWAGGER_SUPPORTED_SUBMIT_METHODS = []  # disable 'Try it out' buttons
    SENTRY_ENV = os.getenv('SENTRY_ENV', 'Not set')
    # support
    SUPPORT_EMAIL = os.getenv("OURFM_SUPPORT_EMAIL")

    CLIENT_ID = os.environ['OURFM_CLIENT_ID']
    CLIENT_SECRET = os.environ['OURFM_CLIENT_SECRET']
    REDIRECT_URI = os.environ['OURFM_REDIRECT_URI']

    SCOPE = 'user-read-private ' \
            'user-read-email ' \
            'ugc-image-upload ' \
            'playlist-modify-public ' \
            'playlist-read-private ' \
            'playlist-modify-private  ' \
            'user-library-read ' \
            'user-top-read ' \
            'user-read-recently-played'
