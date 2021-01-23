import os


class AppConfig:
    # Celery

    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'SOME_SECRET_KEY')

    # database
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask restplus
    ERROR_404_HELP = False
    RESTPLUS_MASK_SWAGGER = False

    # mailgun
    MAILGUN_DOMAIN = os.environ['MAILGUN_DOMAIN']
    MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']

    # swagger
    SWAGGER_UI_DOC_EXPANSION = "list"
    SWAGGER_SUPPORTED_SUBMIT_METHODS = []  # disable 'Try it out' buttons
    SENTRY_ENV = os.getenv('SENTRY_ENV', 'Not set')
    # support
    SUPPORT_EMAIL = os.getenv("OURFM_SUPPORT_EMAIL")

    CLIENT_ID = os.environ['OURFM_CLIENT_ID']
    CLIENT_SECRET = os.environ['OURFM_CLIENT_SECRET']
    REDIRECT_URI = os.environ['OURFM_REDIRECT_URI']

    SCOPE = 'user-read-recently-played ' \
            'user-read-playback-state ' \
            'user-top-read ' \
            'playlist-modify-private ' \
            'playlist-modify-public ' \
            'playlist-read-private ' \
            'playlist-read-collaborative ' \
            'user-read-email ' \
            'user-read-private ' \
            'user-follow-read ' \
            'user-follow-modify '
