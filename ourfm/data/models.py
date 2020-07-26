from sqlalchemy.dialects.postgresql import JSON, UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text as sqlalchemy_text
from sqlalchemy.sql import func, expression
from sqlalchemy.sql.schema import Column, ForeignKey, Index
from sqlalchemy.sql.sqltypes import Date, DateTime, String, Integer, Boolean, Text, Float

from ourfm import db
from ourfm.data import UUIDMixin


class User(UUIDMixin, db.Model):
    __tablename__ = 'users'

    email = Column(String, nullable=False, unique=True, index=True)
    refresh_token = Column(String)
    spotify_id = Column(String)
    data = Column(JSONB)
