from ourfm.data import models as md


def save_new_user(email, refresh_token, spotify_id, data):
    user = md.User.get_or_create(email=email)
    user.update(refresh_token=refresh_token,
                spotify_id=spotify_id,
                data=data)
    return user


def friendship(user_1_id, user_2_id):
    md.Friend.get_or_create(user_id=user_1_id, friend_id=user_2_id)
    md.Friend.get_or_create(user_id=user_2_id, friend_id=user_1_id)
