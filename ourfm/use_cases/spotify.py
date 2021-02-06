from flask import current_app as app
import os

from ourfm.data import models as md
from ourfm.domain import spotify, email

logger = app.logger


def create_user_month_playlist(user_id, duration='month', total=50):
    playlist_name = spotify.playlists.get_your_fm_name()
    if md.Playlist.exists(name=playlist_name, user_id=user_id):
        return md.Playlist.get(name=playlist_name, user_id=user_id)

    top_tracks = spotify.users.get_top_tracks(user_id=user_id, duration=duration, total=total)
    top_tracks = spotify.tracks.save_all(top_tracks)
    playlist = spotify.playlists.create(user_id=user_id, playlist_name=playlist_name)
    playlist = spotify.playlists.add_tracks(user_id=user_id, playlist_id=playlist.id, tracks_to_add=top_tracks)
    return playlist


def create_playlists():
    users = md.User.all()
    return [create_user_month_playlist(user_id=user.id, duration='month', total=50) for user in users]


def get_playlist(playlist_id):
    return spotify.playlists.get(playlist_id)


def send_create_playlist_emails(playlists):
    for playlist in playlists:
        user = md.User.get(id=playlist.user_id)
        playlist_email(user.email, playlist.name)


def playlist_email(user_email, playlist_name):
    text_template = open(os.path.join(app.static_folder, "playlist_email.txt")).read()
    html_template = open(os.path.join(app.static_folder, 'playlist_email.html')).read()
    html_template = html_template.replace('{user_email}', user_email).replace('{playlist_name}', playlist_name)
    email.send(
        to=user_email,
        from_=f"OurFM <noreply@{app.config['MAILGUN_DOMAIN']}>",
        subject=f"{playlist_name} playlist is ready!",
        text_content=text_template,
        html_content=html_template,
    )


def get_current_playing_tracks():
    for user in md.User.all():
        get_current_playing_track(user.id)


def get_current_playing_track(user_id):
    track = spotify.users.get_current_track_for_user(user_id)
    if track is None:
        return None
    logger.info(f'{track["item"]["name"]} collected for {user_id}')
    spotify.tracks.save_track(track['item'])
    current_track = spotify.users.save_current_track(track, user_id)
    return current_track
