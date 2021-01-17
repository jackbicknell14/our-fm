from . import operations

from ourfm.data import models as md


def is_user_member(group_id, user_id):
    return md.GroupUser.exists(group_id=group_id, user_id=user_id)


def get_id_for_all_users(group_id):
    users = md.GroupUser.all(group_id=group_id)
    return [i.user_id for i in users]
