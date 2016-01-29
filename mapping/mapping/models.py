"""
BIDS Institutional Ecosystem Mapping Models
---

This is the standdard structure for all BIDS IEM data. All maps will at
minimum contain information about the following.
"""

def Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    updated_at = db.Column(ArrowType)
    updated_by = db.Column(db.Integer)
    created_at = db.Column(ArrowType, default=arrow.now('US/Pacific'))
    created_by = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)


def Graph(Base):
    """abstract for a graph"""

    __abstract__ = True

    vertices = db.relationship('Vertex', backref='graph')
    edges = db.relationship('Edge', backref='graph')


def Vertex(Base):
    """abstract for a graph vertex"""

    __abstract__ = True

    value = db.Column(db.String)
    graph_id = db.Column(db.Integer, db.ForeignKey('graph.id'))


def Edge(Base):
    """abstract for a graph edge"""

    __abstract__ = True

    value = db.Column(db.String)
    graph_id = db.Column(db.Integer, db.ForeignKey('graph.id'))
    from_id = db.Column(db.Integer, db.ForeignKey('vertex.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('vertex.id'))
