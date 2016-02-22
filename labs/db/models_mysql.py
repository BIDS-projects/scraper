"""
Database Models
---
BIDS Institutional Ecosystem Mapping
"""

from .models import MySQLBase as Base


class Page(Base):
    """webpage"""

    __tablename__ = 'page'

    meta = sa.Column(sa.Text)
    html = sa.Column(sa.String(50), unique=True)
