from ourfm.domain.auth import token
from ourfm.domain.spotify import users


def get_url():
    return token.prepare_user_auth_url()


def get_refresh_token(authorization_code):
    refresh_token = token.get_refresh_token(authorization_code=authorization_code)
    access_token = token.get_new_access_token(refresh_token=refresh_token)
    user = users.save_new_user(access_token, refresh_token)
    return user


