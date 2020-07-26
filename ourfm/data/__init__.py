import flask_sqlalchemy
import flask_migrate
import sqlalchemy

from ourfm import errors as of_errors


class QueryMixin:
    """Mixins for models to add common operations."""
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, commit=True, **data):
        for k, v in data.items():
            setattr(self, k, v)

        if commit:
            self.save()
        return self

    @classmethod
    def _filter(cls, **filters):
        return db.session.query(cls).filter_by(**filters)

    @classmethod
    def get(cls, **filters):
        try:
            return cls._filter(**filters).one()
        except sqlalchemy.orm.exc.NoResultFound:
            raise of_errors.NoRecordExistsError(f'{cls.__class__}: {filters} does not exist')

    @classmethod
    def get_all(cls, **filters):
        return cls._filter(**filters).all()

    @classmethod
    def get_or_create(cls, **kwargs):
        instance = cls._filter(**kwargs).one_or_none()
        if instance is not None:
            return instance
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def scalar(cls, entity, **filters):
        return db.session.query(entity).filter_by(**filters).scalar()


class OFBase(flask_sqlalchemy.Model, QueryMixin):
    """Base class for all models."""
    created = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True),
                                server_default=sqlalchemy.sql.func.now(),
                                nullable=False)
    updated = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True),
                                server_default=sqlalchemy.sql.func.now(),
                                onupdate=sqlalchemy.sql.func.now())

    def __repr__(self):
        pk_values = (f'{pk.name}={getattr(self, pk.name)}'
                     for pk in list(self.__table__.primary_key))
        return f"<{self.__class__.__name__}({', '.join(pk_values)})>"


db = flask_sqlalchemy.SQLAlchemy(model_class=OFBase)
migrate = flask_migrate.Migrate(db=db, directory='ourfm/data/migrations')


class UUIDMixin:
    """Creates a UUID primary key column named id."""
    id = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID(as_uuid=True),
                           primary_key=True,
                           server_default=sqlalchemy.text("uuid_generate_v4()"))

