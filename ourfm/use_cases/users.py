from ourfm.data import models as md
from ourfm.domain import spotify
from ourfm.domain.users import operations


def register(email):
    return operations.save_new_user(email)


def add_friend(user_id, friend_id):
    user = md.User.get(id=user_id)
    friend = md.User.get(id=friend_id)
    friendship = md.Friend(from_user=user, to_user=friend).save()
    return friendship


