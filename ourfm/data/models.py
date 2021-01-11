from sqlalchemy.dialects.postgresql import JSON, UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship, composite
from sqlalchemy.sql.expression import text as sqlalchemy_text
from sqlalchemy.sql import func, expression
from sqlalchemy.sql.schema import Column, ForeignKey, Index
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
    spotify_id = Column(String)

    details = Column(JSONB)
    track_total = Column(Integer)

    tracks = relationship("Track", secondary="playlist_tracks")


class PlaylistTrack(UUIDMixin, db.Model):
    __tablename__ = 'playlist_tracks'

    track_id = Column(UUID(as_uuid=True), ForeignKey('tracks.id'), index=True, nullable=False)
    playlist_id = Column(UUID(as_uuid=True), ForeignKey('playlists.id'), index=True, nullable=False)
    added_by = Column(String)

    track = relationship("Track", backref="playlists_association")
    playlist = relationship("Playlist", backref="tracks_association")


class User(UUIDMixin, db.Model):
    __tablename__ = 'users'

    email = Column(String, nullable=False, unique=True, index=True)
    refresh_token = Column(String)
    spotify_id = Column(String)
    data = Column(JSONB)
    friends_added = relationship("User", secondary="friends", foreign_keys='Friend.from_user_id')
    friends_accepted = relationship("User", secondary="friends", foreign_keys='Friend.to_user_id')


class Friendship(object):
    def __init__(self, user1, user2):
        self.users = sorted([str(user1), str(user2)])
        self.user1, self.user2 = self.users

    def __composite_values__(self):
        return '-'.join(self.users)

    def __repr__(self):
        return  '-'.join(self.users)

    def __eq__(self, other):
        return isinstance(other, Friendship) and \
            other.user1 == self.user1 and \
            other.user2 == self.user2

    def __ne__(self, other):
        return not self.__eq__(other)


class Friend(UUIDMixin, db.Model):
    __tablename__ = 'friends'
    from_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True, nullable=False)
    to_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True, nullable=False)

    #     rel = column_property('-'.join(sorted([str(from_user_id), str(to_user_id)])))
    friendship = composite(Friendship, from_user_id, to_user_id)
    from_user = relationship("User", foreign_keys='Friend.from_user_id')
    to_user = relationship("User", foreign_keys='Friend.to_user_id')


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
