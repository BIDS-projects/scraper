from utils.models import Base


class Text(Base):
    """text for a webpage"""
    link_id = db.Column(db.)
    text = db.Column(db.Text)

class Link(Base):
    """URLs"""

    domain = db.Column(db.Integer, db.ForeignKey('domain.id'))
    url = db.Column(db.Text)

class Domain(Base):
    """domains"""

    url = db.Column(db.Text)
    text = db.Column(db.Text)
