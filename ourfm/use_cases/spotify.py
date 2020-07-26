from ourfm.domain.auth import token
import spotipy


def create_month_playlist(user):
    access_token = token.get_new_access_token(refresh_token=user.refresh_token)
    sp = spotipy.Spotify(auth=access_token)
    user = sp.current_user()
    top_tracks = sp.current_user_top_tracks(time_range='short_term', limit=50)['items']
    tracks = [i['id'] for i in top_tracks]
    playlist_name = f'JULY 20: YourFM'
    playlist_id = sp.user_playlist_create(user['id'], playlist_name)['id']
    sp.user_playlist_add_tracks(user['id'], playlist_id, tracks)

