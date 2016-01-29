"""
Database Models
---
BIDS Institutional Ecosystem Mapping
"""

from sqlalchemy.ext.declarative import declarative_base

__Base = declarative_base()

def Base(__Base):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    updated_at = db.Column(ArrowType)
    updated_by = db.Column(db.Integer)
    created_at = db.Column(ArrowType, default=arrow.now('US/Pacific'))
    created_by = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
