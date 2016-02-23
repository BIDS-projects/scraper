import sqlalchemy.ext.declarative as sad
from sqlalchemy_utils import ArrowType
import sqlalchemy as sa
import mongoengine as me
import arrow


class Base(object):
    """requirements for all objects"""


    def save(self):
        """save object in place"""
        raise NotImplementedError()


    def delete(self):
        """delete object"""
        raise NotImplementedError()


class MySQLBase(sad.declarative_base(), object):
    """MySQL base object"""

    __abstract__ = True
    db = None

    id = sa.Column(sa.Integer, primary_key=True)
    updated_at = sa.Column(ArrowType)
    updated_by = sa.Column(sa.Integer)
    created_at = sa.Column(ArrowType, default=arrow.now('US/Pacific'))
    created_by = sa.Column(sa.Integer)
    is_active = sa.Column(sa.Boolean, default=True)

    @classmethod
    def get_or_create(cls, **data):
        """Get or create the object"""
        return cls.query().filter_by(**data).one_or_none() or cls(**data).save()

    def update(self, **kwargs):
        """updates object with kwargs"""
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self

    @classmethod
    def objects(cls, give_query=False, **data):
        query = cls.query().filter_by(**data)
        return query if give_query else query.all()

    @classmethod
    def query(cls):
        """Returns query object"""
        return cls.db.session.query(cls)

    def save(self):
        """save object to database"""
        self.db.session.add(self)
        self.db.session.commit()
        return self

ForeignColumn = lambda *args, **kwargs: sad.declared_attr(
    lambda _: sa.Column(*args, **kwargs))


class MongoBase(me.Document):
    """MongoDB base object"""

    meta = {
        'abstract': True
    }
