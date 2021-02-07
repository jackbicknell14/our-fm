import random
from ourfm.domain import groups, spotify


def create(user_id, group_name):
    group = groups.operations.create(user_id, group_name)
    return spotify.playlists.create(user_id=user_id, playlist_name=f'OurFM: {group.name}', public=True,
                                    description=f'OurFM: {group.name}', group_id=group.id)


def get(group_id):
    return groups.operations.get(group_id)


def add_user(group_id, user_id):
    if groups.is_user_member(group_id, user_id):
        return 'Already a member'
    group = groups.operations.get(group_id)
    groups.operations.add_user(group_id, user_id)
    spotify.playlists.create(user_id=user_id, playlist_name=f'OurFM: {group.name}', public=True,
                             description=f'OurFM: {group.name}', group_id=group.id)
    return f'Added {user_id} to {group.name}'


def get_users(group_id):
    return groups.get_id_for_all_users(group_id)


def create_playlist(group_id):
    playlists = groups.get_id_for_all_playlists(group_id)
    users_id = groups.get_id_for_all_users(group_id)

    group_tracks = [spotify.users.get_top_tracks(user_id=user_id, duration='month', total=10) for user_id in users_id]
    random.shuffle(group_tracks)
    group_tracks = [i for i in group_tracks for i in i]
    group_tracks = spotify.tracks.save_all(group_tracks)

    for playlist in playlists:
        spotify.playlists.replace_tracks(user_id=playlist.user_id, playlist_id=playlist.id, tracks_to_add=group_tracks)

