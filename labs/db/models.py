import sqlalchemy.ext.declarative as sad
import sqlalchemy as sa
import mongoengine as me


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


class MongoBase(me.Document):
    """MongoDB base object"""

    meta = {
        'abstract': True
    }
