from ourfm.domain import groups, spotify


def create(user_id, group_name):
    return groups.operations.create(user_id, group_name)


def get(group_id):
    return groups.operations.get(group_id)


def add_user(group_id, user_id):
    if groups.is_user_member(group_id, user_id):
        return 'Already a member'
    group = groups.operations.get(group_id)
    groups.operations.add_user(group_id, user_id)
    return f'Added {user_id} to {group.name}'


def get_users(group_id):
    return groups.get_all_users(group_id)


def create_playlist(group_id):
    group = groups.operations.get(group_id)
    users = groups.get_all_users(group_id)
    to_add = []
    for user in users:
        tracks = spotify.users.get_top_tracks(user_id=user.id, duration='month', total=10)
        to_add.append((user.id, tracks))
