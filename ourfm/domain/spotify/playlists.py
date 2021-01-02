import datetime

from . import auth

SPOTIFY_TIMES = {
    'month': 'short_term',
    'halfyear': 'medium_term',
    'year': 'long_term'
}


def create(user, duration='month'):
    sp = auth.login(user)
    user = sp.current_user()
    top_tracks = sp.current_user_top_tracks(time_range=SPOTIFY_TIMES[duration], limit=50)['items']
    tracks = [i['id'] for i in top_tracks]
    playlist_name = f'YourFM: {datetime.date.today().strftime("%B %Y")}'
    playlist_id = sp.user_playlist_create(user['id'], playlist_name)['id']
    sp.user_playlist_add_tracks(user['id'], playlist_id, tracks)
