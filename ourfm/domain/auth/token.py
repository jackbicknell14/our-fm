from flask import current_app as app
import urllib
import requests

logger = app.logger

CLIENT_ID = app.config['CLIENT_ID']
CLIENT_SECRET = app.config['CLIENT_SECRET']
REDIRECT_URI = app.config['REDIRECT_URI']
SCOPE = app.config['SCOPE']


def prepare_user_auth_url():
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': SCOPE,
        'redirect_uri': REDIRECT_URI
    }
    url = 'https://accounts.spotify.com/authorize?'
    return url + urllib.parse.urlencode(params)


def get_refresh_token(authorization_code):
    data = {
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code': authorization_code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    url = 'https://accounts.spotify.com/api/token'
    logger.info(data)
    response = requests.post(url, data=data)
    logger.info(response.url)
    response.raise_for_status()
    data = response.json()
    refresh_token = data['refresh_token']
    return refresh_token


def get_new_access_token(refresh_token):
    url = 'https://accounts.spotify.com/api/token'
    body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(url=url, data=body)
    data = response.json()
    return data['access_token']
