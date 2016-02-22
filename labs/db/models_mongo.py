from .models import MongoBase


class Link(MongoBase):
    """link on webpage"""

    name = me.StringField(maxlength=100)
    email = me.StringField(maxlength=50, unique=True)


class Page(MongoBase):
    """webpage source"""

    name = me.StringField(maxlength=100)
    email = me.StringField(maxlength=50, unique=True)


class BaseLink(MongoBase):
    """many to many link between pages and links"""

    pass
