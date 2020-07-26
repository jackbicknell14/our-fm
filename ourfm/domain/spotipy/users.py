from ourfm.domain.users import operations
import spotipy


def save_new_user(access_token, refresh_token):
    sp = spotipy.Spotify(auth=access_token)
    user = sp.current_user()
    operations.save_new_user(email=user['email'],
                             refresh_token=refresh_token,
                             spotify_id=user['id'],
                             data=user)
    return user
