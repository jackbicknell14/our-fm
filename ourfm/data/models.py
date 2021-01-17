from sqlalchemy.dialects.postgresql import JSON, UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship, composite
from sqlalchemy.sql.expression import text as sqlalchemy_text
from sqlalchemy.sql import func, expression
from sqlalchemy.sql.schema import Column, ForeignKey, Index, UniqueConstraint
from sqlalchemy.sql.sqltypes import Date, DateTime, String, Integer, Boolean, Text, Float

from ourfm import db
from ourfm.data import UUIDMixin


class Artist(UUIDMixin, db.Model):
    __tablename__ = 'artists'
    name = Column(String, nullable=False)
    genres = Column(ARRAY(String))
    href = Column(String)
    popularity = Column(Integer)
    uri = Column(String)
    external_urls = Column(String)
    spotify_id = Column(String)

    tracks = relationship("Track", secondary='artist_tracks', back_populates='artists')


class ArtistTrack(UUIDMixin, db.Model):
    __tablename__ = 'artist_tracks'
    artist_id = Column(UUID(as_uuid=True), ForeignKey('artists.id'), index=True, nullable=False)
    track_id = Column(UUID(as_uuid=True), ForeignKey('tracks.id'), index=True, nullable=False)


class Track(UUIDMixin, db.Model):
    __tablename__ = 'tracks'
    name = Column(String, nullable=False)
    details = Column(JSONB)
    spotify_id = Column(String)
    artists = relationship("Artist", secondary='artist_tracks', back_populates='tracks')
    playlists = relationship("Playlist", secondary='playlist_tracks')


class Playlist(UUIDMixin, db.Model):
    __tablename__ = 'playlists'

    name = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True, nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey('groups.id'), index=True, nullable=True)
    spotify_id = Column(String)

    details = Column(JSONB)
    track_total = Column(Integer)

    tracks = relationship("Track", secondary="playlist_tracks")


class PlaylistTrack(UUIDMixin, db.Model):
    __tablename__ = 'playlist_tracks'

    track_id = Column(UUID(as_uuid=True), ForeignKey('tracks.id'), index=True, nullable=False)
    playlist_id = Column(UUID(as_uuid=True), ForeignKey('playlists.id'), index=True, nullable=False)
    added_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True, nullable=False)

    track = relationship("Track", backref="playlists_association")
    playlist = relationship("Playlist", backref="tracks_association")


class User(UUIDMixin, db.Model):
    __tablename__ = 'users'

    email = Column(String, nullable=False, unique=True, index=True)
    refresh_token = Column(String)
    spotify_id = Column(String)
    data = Column(JSONB)


class Friend(UUIDMixin, db.Model):
    __tablename__ = 'friends'
    __table_args__ = (UniqueConstraint('user_id', 'friend_id'), {},)

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True, nullable=False)
    friend_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True, nullable=False)



class Group(UUIDMixin, db.Model):
    __tablename__ = 'groups'

    name = Column(String, nullable=False)
    is_private = Column(Boolean, server_default=expression.true(), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True, nullable=False)


class GroupUser(UUIDMixin, db.Model):
    __tablename__ = 'group_users'

    group_id = Column(UUID(as_uuid=True), ForeignKey('groups.id'), index=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True, nullable=False)


class UserTrack(UUIDMixin, db.Model):
    __tablename__ = 'user_tracks'

    track_id = Column(UUID(as_uuid=True), ForeignKey('tracks.id'), index=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True, nullable=False)
    device = Column(String)
    shuffle_state = Column(String)
    repeat_state = Column(String)
    timestamp = Column(String)
    context = Column(String)
    progress_ms = Column(String)
    item = Column(String)
    currently_playing_type = Column(String)
    actions = Column(String)
    is_playing = Column(String)
