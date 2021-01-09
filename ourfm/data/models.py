from sqlalchemy.dialects.postgresql import JSON, UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
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

    tracks = relationship("Track", secondary='artisttracks', back_populates='artists')


class ArtistTrack(UUIDMixin, db.Model):
    __tablename__ = 'artisttracks'
    artist_id = Column(UUID(as_uuid=True), ForeignKey('artists.id'), index=True, nullable=False)
    track_id = Column(UUID(as_uuid=True), ForeignKey('tracks.id'), index=True, nullable=False)


class Track(UUIDMixin, db.Model):
    __tablename__ = 'tracks'
    name = Column(String, nullable=False)
    details = Column(JSONB)
    spotify_id = Column(String)
    artists = relationship("Artist", secondary='artisttracks', back_populates='tracks')


class Playlist(UUIDMixin, db.Model):
    __tablename__ = 'playlists'

    name = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True, nullable=False)
    spotify_id = Column(String)

    details = Column(JSONB)
    track_total = Column(Integer)


class PlaylistTrack(UUIDMixin, db.Model):
    __tablename__ = 'playlisttracks'

    track_id = Column(UUID(as_uuid=True), ForeignKey('tracks.id'), index=True, nullable=False)
    playlist_id = Column(UUID(as_uuid=True), ForeignKey('playlists.id'), index=True, nullable=False)
    added_by = Column(String)


class User(UUIDMixin, db.Model):
    __tablename__ = 'users'

    email = Column(String, nullable=False, unique=True, index=True)
    refresh_token = Column(String)
    spotify_id = Column(String)
    data = Column(JSONB)
