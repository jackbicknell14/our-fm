from ourfm.data import models as md
from ourfm.domain import spotify
from ourfm.domain.users import operations


def register(email):
    return operations.save_new_user(email)


def add_friend(user_id, friend_id):
    friend = md.User.get(id=friend_id)
    operations.friendship(user_id, friend_id)
    return friend.id


def get(user_id):
    return md.User.get(id=user_id).__dict__


def get_friends(user_id):
    friend_ids = [i.friend_id for i in md.Friend.all(user_id=user_id)]
    friends = [md.User.get(id=friend_id) for friend_id in friend_ids]
    return [{'username': friend.username,
             'city': friend.city,
             'country': friend.country,
             'status': friend.status} for friend in friends]


def get_groups(user_id):
    group_ids = [i.group_id for i in md.GroupUser.all(user_id=user_id)]
    groups = [md.Group.get(id=group_id) for group_id in group_ids]
    return [{'name': group.name,
             'is_private': group.is_private,
             'created_by': md.User.get(id=group.created_by).username,
             'members': [{
                 'username': member.username
             } for member in group.members]} for group in groups]


def get_playlists(user_id):
    playlists = md.Playlist.all(user_id=user_id)
    return [{'name': playlist.name,
             'tracks_total': playlist.track_total,
             'group': md.Group.get(id=playlist.group_id).name if playlist.group_id else None} for playlist in
            playlists]
