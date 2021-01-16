from ourfm.data import models as md


def create(user_id, group_name):
    group = md.Group.get_or_create(created_by=user_id, name=group_name)
    md.GroupUser.get_or_create(group_id=group.id, user_id=user_id)
    return group


def get(group_id):
    return md.Group.get(id=group_id)


def add_user(group_id, user_id):
    return md.GroupUser.create(group_id=group_id, user_id=user_id)
