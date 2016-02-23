"""
Database Models
---
BIDS Institutional Ecosystem Mapping
"""

from .models import MySQLBase as Base, ForeignColumn
import sqlalchemy as sa


class HTML(Base):
    """webpage"""

    __tablename__ = 'html'

    domain = sa.Column(sa.Text)
    url = sa.Column(sa.Text)
    body = sa.Column(sa.String(50))
    request = sa.Column(sa.Text)


class Link(Base):
    """link between webpages"""

    __tablename__ = 'link'

    from_html = ForeignColumn(sa.Integer, sa.ForeignKey('html.id'))
    to_html = ForeignColumn(sa.Integer, sa.ForeignKey('html.id'))
