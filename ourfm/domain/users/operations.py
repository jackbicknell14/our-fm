from ourfm.data import models as md


def save_new_user(email, refresh_token, spotify_id, data):
    user = md.User.get_or_create(email=email)
    user.update(refresh_token=refresh_token,
                spotify_id=spotify_id,
                data=data)
    return user
