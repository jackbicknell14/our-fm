from flask import current_app as app
import os

from ourfm.data import models as md
from ourfm.domain import spotify, email


def create_playlist(user_id):
    user = md.User.get(id=user_id)
    playlist = spotify.playlists.create(user=user, duration='month')
    return playlist


def create_playlists():
    users = md.User.all()
    playlists = [spotify.playlists.create(user=user, duration='month') for user in users]
    spotify.artists.save(method='playlist')
    spotify.tracks.save('playlist')
    return playlists


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


def get_current_playing_track():
    pass
