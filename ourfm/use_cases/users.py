from ourfm.data import models as md
from ourfm.domain import spotify
from ourfm.domain.users import operations


def register(email):
    return operations.save_new_user(email)


def add_friend(user_id, friend_id):
    user = md.User.get(id=user_id)
    friend = md.User.get(id=friend_id)
    operations.friendship(user_id, friend_id)
    return friend.id


def get(user_id):
    return md.User.get(id=user_id).__dict__
